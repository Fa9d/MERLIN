"""Routes de réservation de créneaux (client authentifié ou vérifié)."""
from __future__ import annotations

from datetime import date, datetime, time, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, require_verified_email_user
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.enums import (
    AppRole,
    SessionTypeCode,
    SlotStatus,
)
from app.models.schedule import BookingSlot
from app.schemas.schedule import BookingSlotOut
from app.services.booking_flow import (
    confirm_slot_for_client_record,
    expire_hold,
    get_client_record_for_user,
    restore_entitlement_for_slot,
    send_booking_confirmation_email_for_slot,
)

router = APIRouter(prefix="/bookings", tags=["bookings"])

_HOLD_MINUTES = 15  # durée du hold avant libération automatique


# ---------------------------------------------------------------------------
# Schemas locaux
# ---------------------------------------------------------------------------

class BookingHoldIn(BaseModel):
    # Option A : ID d'un BookingSlot existant
    slot_id: str | None = None
    # Option B : créneau virtuel (non encore persisté en base)
    praticien_id: str | None = None
    slot_date: date | None = None
    start_time: time | None = None
    end_time: time | None = None
    session_type: SessionTypeCode | None = None


class BookingConfirmIn(BaseModel):
    slot_id: str
    notes: str | None = None


class BookingCancelIn(BaseModel):
    slot_id: str


# ---------------------------------------------------------------------------
# POST /bookings/hold  — placer un hold sur un créneau disponible
# ---------------------------------------------------------------------------

@router.post(
    "/hold",
    response_model=BookingSlotOut,
    status_code=status.HTTP_200_OK,
    summary="Placer un hold (réservation temporaire) sur un créneau",
)
def hold_slot(
    body: BookingHoldIn,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_verified_email_user),
) -> BookingSlotOut:
    now_utc = datetime.now(timezone.utc)
    hold_expires = now_utc + timedelta(minutes=_HOLD_MINUTES)

    if body.slot_id:
        # ── Cas A : slot déjà persisté ──
        slot: BookingSlot | None = db.query(BookingSlot).filter(BookingSlot.id == body.slot_id).first()
        if not slot:
            raise HTTPException(status_code=404, detail="Créneau introuvable.")
        expire_hold(slot)
        if slot.status != SlotStatus.available:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ce créneau n'est plus disponible.",
            )
    else:
        # ── Cas B : créneau virtuel (gabarit) ──
        if not all([body.praticien_id, body.slot_date, body.start_time, body.end_time]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Fournissez slot_id ou praticien_id+slot_date+start_time+end_time.",
            )
        praticien = db.get(AppUser, body.praticien_id)
        if praticien is None or praticien.role != AppRole.practitioner:
            raise HTTPException(status_code=404, detail="Praticien introuvable.")

        # Cherche un slot existant pour ce créneau
        existing: BookingSlot | None = (
            db.query(BookingSlot)
            .filter(
                BookingSlot.praticien_id == body.praticien_id,
                BookingSlot.slot_date == body.slot_date,
                BookingSlot.start_time == body.start_time,
            )
            .first()
        )
        if existing:
            expire_hold(existing)
            db.flush()
            if existing.status in (SlotStatus.hold, SlotStatus.confirmed):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Ce créneau n'est plus disponible.",
                )
            slot = existing
        else:
            slot = BookingSlot(
                praticien_id=body.praticien_id,
                slot_date=body.slot_date,
                start_time=body.start_time,
                end_time=body.end_time,
                session_type=body.session_type or SessionTypeCode.standard,
                status=SlotStatus.available,
            )
            db.add(slot)
            db.flush()

    slot.status = SlotStatus.hold
    slot.client_id = current_user.id
    slot.hold_expires_at = hold_expires
    db.commit()
    db.refresh(slot)
    return BookingSlotOut.model_validate(slot)


# ---------------------------------------------------------------------------
# POST /bookings/confirm  — confirmer un hold
# ---------------------------------------------------------------------------

@router.post(
    "/confirm",
    response_model=BookingSlotOut,
    status_code=status.HTTP_200_OK,
    summary="Confirmer un hold pour finaliser la réservation",
)
async def confirm_slot(
    body: BookingConfirmIn,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_verified_email_user),
) -> BookingSlotOut:
    slot: BookingSlot | None = db.query(BookingSlot).filter(BookingSlot.id == body.slot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Créneau introuvable.")

    expire_hold(slot)

    if slot.status != SlotStatus.hold or slot.client_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ce créneau ne peut pas être confirmé (hold expiré ou appartient à un autre client).",
        )

    client_record = get_client_record_for_user(db, current_user)
    confirm_slot_for_client_record(
        db,
        slot,
        client_record,
        user_id=current_user.id,
        notes=body.notes,
    )
    db.commit()
    db.refresh(slot)

    await send_booking_confirmation_email_for_slot(db, slot, current_user)

    return BookingSlotOut.model_validate(slot)


# ---------------------------------------------------------------------------
# POST /bookings/cancel  — annuler une réservation confirmée ou hold
# ---------------------------------------------------------------------------

@router.post(
    "/cancel",
    response_model=BookingSlotOut,
    status_code=status.HTTP_200_OK,
    summary="Annuler un rendez-vous (client ou praticien)",
)
def cancel_slot(
    body: BookingCancelIn,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_verified_email_user),
) -> BookingSlotOut:
    """Annule un créneau (hold ou confirmed).

    Sécurité (BACK-BOOK-001) : aligné sur hold/confirm — exige email vérifié.
    Autorisé : client propriétaire, praticien concerné, ou opérateur.
    """
    slot: BookingSlot | None = db.query(BookingSlot).filter(BookingSlot.id == body.slot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Créneau introuvable.")

    # Autorisé : le client propriétaire, le praticien concerné, ou un opérateur
    is_owner = slot.client_id == current_user.id
    is_praticien = slot.praticien_id == current_user.id
    is_operator = current_user.role == AppRole.operator
    if not (is_owner or is_praticien or is_operator):
        raise HTTPException(status_code=403, detail="Non autorisé.")

    if slot.status not in (SlotStatus.hold, SlotStatus.confirmed):
        raise HTTPException(status_code=409, detail="Ce créneau ne peut pas être annulé.")

    if slot.status == SlotStatus.confirmed:
        restore_entitlement_for_slot(db, slot)

    slot.status = SlotStatus.cancelled
    slot.hold_expires_at = None
    db.commit()
    db.refresh(slot)
    return BookingSlotOut.model_validate(slot)


# ---------------------------------------------------------------------------
# GET /bookings/my  — mes réservations (client connecté)
# ---------------------------------------------------------------------------

@router.get(
    "/my",
    response_model=list[BookingSlotOut],
    summary="Mes réservations (client connecté)",
)
def my_bookings(
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user),
) -> list[BookingSlotOut]:
    slots = (
        db.query(BookingSlot)
        .filter(
            BookingSlot.client_id == current_user.id,
            BookingSlot.status.in_([SlotStatus.hold, SlotStatus.confirmed]),
        )
        .order_by(BookingSlot.slot_date, BookingSlot.start_time)
        .all()
    )
    return [BookingSlotOut.model_validate(s) for s in slots]





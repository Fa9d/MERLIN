"""Routes de réservation de créneaux (client authentifié ou vérifié)."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, require_verified_email_user
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.enums import AppRole, SlotStatus
from app.models.schedule import BookingSlot
from app.schemas.schedule import BookingSlotOut
from app.services.email import make_booking_confirmation_email, send_email

router = APIRouter(prefix="/bookings", tags=["bookings"])

_HOLD_MINUTES = 15  # durée du hold avant libération automatique


# ---------------------------------------------------------------------------
# Schemas locaux
# ---------------------------------------------------------------------------

class BookingHoldIn(BaseModel):
    slot_id: str  # ID d'un BookingSlot existant (status=available)


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
    slot: BookingSlot | None = db.query(BookingSlot).filter(BookingSlot.id == body.slot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Créneau introuvable.")

    # Libérer les holds expirés sur ce créneau
    _expire_hold(slot)

    if slot.status != SlotStatus.available:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ce créneau n'est plus disponible.",
        )

    slot.status = SlotStatus.hold
    slot.client_id = current_user.id
    slot.hold_expires_at = datetime.now(timezone.utc) + timedelta(minutes=_HOLD_MINUTES)
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

    _expire_hold(slot)

    if slot.status != SlotStatus.hold or slot.client_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ce créneau ne peut pas être confirmé (hold expiré ou appartient à un autre client).",
        )

    if body.notes:
        slot.notes = body.notes
    slot.status = SlotStatus.confirmed
    slot.hold_expires_at = None
    db.commit()
    db.refresh(slot)

    # Envoi courriel de confirmation
    praticien: AppUser | None = db.query(AppUser).filter(AppUser.id == slot.praticien_id).first()
    if praticien:
        from app.schemas.schedule import SESSION_TYPE_LABELS
        import locale
        slot_date_str = slot.slot_date.strftime("%A %d %B %Y")
        slot_time_str = slot.start_time.strftime("%Hh%M")
        session_label = SESSION_TYPE_LABELS.get(slot.session_type, slot.session_type)
        from app.core.config import settings
        cancel_url = f"{settings.frontend_url}/rendez-vous/annuler?slot={slot.id}"
        html, text = make_booking_confirmation_email(
            display_name=current_user.display_name,
            praticien_name=praticien.display_name,
            slot_date=slot_date_str,
            slot_time=slot_time_str,
            session_type_label=session_label,
            cancel_url=cancel_url,
        )
        await send_email(
            current_user.email,
            f"Votre rendez-vous le {slot_date_str} — IVIA",
            html,
            text,
        )

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
    current_user: AppUser = Depends(get_current_user),
) -> BookingSlotOut:
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


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _expire_hold(slot: BookingSlot) -> None:
    """Libère un hold expiré (in-place, sans commit)."""
    if (
        slot.status == SlotStatus.hold
        and slot.hold_expires_at
        and slot.hold_expires_at < datetime.now(timezone.utc)
    ):
        slot.status = SlotStatus.available
        slot.client_id = None
        slot.hold_expires_at = None



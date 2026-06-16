"""Routes de réservation de créneaux (client authentifié ou vérifié)."""
from __future__ import annotations

from datetime import date, datetime, time, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, require_verified_email_user
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.client import Client
from app.models.client_entitlement import ClientEntitlement
from app.models.enums import (
    AppRole,
    ClientEntitlementTypeCode,
    DataSensitivityClass,
    RecordStatus,
    RetentionClass,
    SessionChannelCode,
    SessionModeCode,
    SessionStatusCode,
    SessionTypeCode,
    SlotStatus,
)
from app.models.schedule import BookingSlot
from app.models.session import SessionRecord
from app.schemas.schedule import BookingSlotOut


class PilotBookOut(BookingSlotOut):
    """BookingSlotOut étendu avec l'identifiant de la séance pré-créée."""
    session_id: str | None = None
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


class PilotBookIn(BaseModel):
    """Payload pour réservation pilote tout-en-un (sans paiement Stripe)."""
    praticien_id: str
    slot_date: date
    start_time: time
    end_time: time
    session_type: SessionTypeCode | None = None
    notes: str | None = None


class BookingCheckoutIn(BaseModel):
    """Payload pour régler un créneau en hold — le prix vient TOUJOURS du serveur."""
    slot_id: str
    notes: str | None = None
    success_url: str | None = None
    cancel_url: str | None = None


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


# ---------------------------------------------------------------------------
# POST /bookings/pilot-book  — réservation pilote (hold + crédit auto + confirm)
# ---------------------------------------------------------------------------

@router.post(
    "/pilot-book",
    response_model=PilotBookOut,
    status_code=status.HTTP_200_OK,
    summary="Réservation pilote tout-en-un — hold + crédit gratuit + confirmation sans Stripe",
)
async def pilot_book_slot(
    body: PilotBookIn,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_verified_email_user),
) -> PilotBookOut:
    """Phase pilote uniquement.

    Atomique : crée le dossier client si absent, accorde un crédit de séance
    gratuit, et confirme le créneau en une seule requête.
    """
    now_utc = datetime.now(timezone.utc)

    # 1. Vérifier le praticien
    praticien = db.get(AppUser, body.praticien_id)
    if praticien is None or praticien.role != AppRole.practitioner:
        raise HTTPException(status_code=404, detail="Praticien introuvable.")

    # 2. Récupérer ou créer le slot
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

    # 3. Mettre en hold transitoire
    slot.status = SlotStatus.hold
    slot.client_id = current_user.id
    slot.hold_expires_at = now_utc + timedelta(minutes=_HOLD_MINUTES)
    db.flush()

    # 4. Dossier client (créer si absent)
    client_record: Client | None = (
        db.query(Client).filter(Client.app_user_id == current_user.id).first()
    )
    if client_record is None:
        display = current_user.display_name or current_user.email or "Client"
        parts = display.split(" ", 1)
        client_record = Client(
            app_user_id=current_user.id,
            first_name_or_alias=parts[0],
            last_name=parts[1] if len(parts) > 1 else None,
            email=current_user.email,
        )
        db.add(client_record)
        db.flush()

    # 5. Accorder un crédit pilote gratuit (1 séance de suivi)
    pilot_entitlement = ClientEntitlement(
        client_id=client_record.id,
        entitlement_type_code=ClientEntitlementTypeCode.follow_up_session_credit,
        quantity_total=1,
        quantity_remaining=0,  # consommé immédiatement
        starts_at=now_utc,
        record_status=RecordStatus.active,
    )
    db.add(pilot_entitlement)
    db.flush()

    # 6. Confirmer le créneau (consomme le crédit pilote)
    if body.notes:
        slot.notes = body.notes
    slot.status = SlotStatus.confirmed
    slot.hold_expires_at = None
    slot.consumed_entitlement_id = pilot_entitlement.id
    slot.consumed_entitlement_units = 1
    db.add(slot)
    db.commit()
    db.refresh(slot)

    await send_booking_confirmation_email_for_slot(db, slot, current_user)

    # 7. Créer la SessionRecord liée (praticien = opérateur de sa propre séance)
    from sqlalchemy import func, select as sa_select

    latest_seq = db.scalar(
        sa_select(func.max(SessionRecord.session_sequence_number)).where(
            SessionRecord.client_id == client_record.id
        )
    )
    scheduled_start = datetime.combine(
        slot.slot_date,
        slot.start_time,
        tzinfo=timezone.utc,
    )
    session_record = SessionRecord(
        client_id=client_record.id,
        operator_user_id=slot.praticien_id,
        praticien_id=slot.praticien_id,
        session_mode_code=SessionModeCode.standard,
        session_channel_code=SessionChannelCode.audio_live,
        session_status_code=SessionStatusCode.scheduled,
        session_sequence_number=(latest_seq or 0) + 1,
        scheduled_start_at=scheduled_start,
        data_sensitivity_class=DataSensitivityClass.high,
        retention_class=RetentionClass.standard,
        record_status=RecordStatus.active,
    )
    db.add(session_record)
    db.commit()
    db.refresh(slot)
    db.refresh(session_record)

    out = PilotBookOut.model_validate(slot)
    out.session_id = session_record.id
    return out


# ---------------------------------------------------------------------------
# POST /bookings/checkout  — régler un créneau en hold via Stripe (prix serveur)
# ---------------------------------------------------------------------------

@router.post(
    "/checkout",
    status_code=status.HTTP_201_CREATED,
    summary="Créer la session de paiement Stripe pour un créneau en hold",
)
async def checkout_held_slot(
    body: BookingCheckoutIn,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_verified_email_user),
):
    """Le client paie son créneau en hold ; le webhook Stripe confirme au paiement.

    Sécurité : le montant vient de la configuration serveur
    (`MERLIN_STRIPE_SEANCE_AMOUNT_CENTS`), jamais du payload. Le `slot_id` est posé
    en métadonnées de la commande → `_auto_confirm_paid_slot_if_any` confirme le
    créneau quand `checkout.session.completed` arrive.
    """
    from app.api.routes.payments import _create_checkout_order
    from app.core.config import settings
    from app.models.enums import PaymentFulfillmentModeCode, PaymentProductKindCode
    from app.schemas.payment import PaymentCheckoutCreate
    from app.services.booking_flow import entitlement_type_for_slot

    slot: BookingSlot | None = db.query(BookingSlot).filter(BookingSlot.id == body.slot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Créneau introuvable.")

    expire_hold(slot)
    if slot.status != SlotStatus.hold or slot.client_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ce créneau ne peut pas être réglé (hold expiré ou appartient à un autre client).",
        )

    # Dossier client — créé au vol au premier passage (même logique que pilot-book)
    client_record: Client | None = (
        db.query(Client).filter(Client.app_user_id == current_user.id).first()
    )
    if client_record is None:
        display = current_user.display_name or current_user.email or "Client"
        parts = display.split(" ", 1)
        client_record = Client(
            app_user_id=current_user.id,
            first_name_or_alias=parts[0],
            last_name=parts[1] if len(parts) > 1 else None,
            email=current_user.email,
        )
        db.add(client_record)
        db.flush()

    if body.notes:
        slot.notes = body.notes
        db.add(slot)
    db.flush()

    kind = (
        PaymentProductKindCode.session_intake
        if slot.session_type == SessionTypeCode.intake
        else PaymentProductKindCode.session_follow_up
    )

    # Prix selon la durée du créneau : ≤ 30 min → 49 $ (live 30 min), sinon → 75 $ (live 1 h).
    from datetime import date as _date
    duree_min = (
        datetime.combine(_date.min, slot.end_time) - datetime.combine(_date.min, slot.start_time)
    ).seconds // 60
    # Prix fixé par le praticien (sinon défaut serveur).
    prat = db.get(AppUser, slot.praticien_id) if slot.praticien_id else None
    if duree_min <= 30:
        amount_cents = (prat.session_price_30min_cents if prat and prat.session_price_30min_cents
                        else settings.stripe_seance_30min_amount_cents)
        duree_label = "30 min"
    else:
        amount_cents = (prat.session_price_60min_cents if prat and prat.session_price_60min_cents
                        else settings.stripe_seance_amount_cents)
        duree_label = "1 h"

    payload = PaymentCheckoutCreate(
        client_id=client_record.id,
        slot_id=slot.id,
        product_code="seance_live_booking",
        product_label=(
            f"Séance live IVIA · {duree_label} — {slot.slot_date.isoformat()} "
            f"{slot.start_time.strftime('%H:%M')}"
        ),
        product_kind_code=kind,
        fulfillment_mode_code=PaymentFulfillmentModeCode.grant_entitlement_only,
        amount_cents=amount_cents,
        currency=settings.stripe_seance_currency,
        entitlement_type_code=entitlement_type_for_slot(slot),
        entitlement_quantity=1,
        success_url=body.success_url,
        cancel_url=body.cancel_url,
    )
    return await _create_checkout_order(payload, db)


from __future__ import annotations

from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.app_user import AppUser
from app.models.client import Client
from app.models.client_entitlement import ClientEntitlement
from app.models.enums import (
    ClientEntitlementTypeCode,
    RecordStatus,
    SessionTypeCode,
    SlotStatus,
)
from app.models.schedule import BookingSlot
from app.services.email import make_booking_confirmation_email, send_email


def expire_hold(slot: BookingSlot) -> None:
    if (
        slot.status == SlotStatus.hold
        and slot.hold_expires_at
        and slot.hold_expires_at < datetime.now(timezone.utc)
    ):
        slot.status = SlotStatus.available
        slot.client_id = None
        slot.hold_expires_at = None


def get_client_record_for_user(db: Session, current_user: AppUser) -> Client:
    client_record = db.query(Client).filter(Client.app_user_id == current_user.id).first()
    if client_record is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Aucun dossier client actif n'est rattaché à ce compte.",
        )
    return client_record


def entitlement_type_for_slot(slot: BookingSlot) -> ClientEntitlementTypeCode:
    if slot.session_type == SessionTypeCode.intake:
        return ClientEntitlementTypeCode.intake_session_credit
    return ClientEntitlementTypeCode.follow_up_session_credit


def reserve_entitlement_for_slot(
    db: Session,
    slot: BookingSlot,
    client_id: str,
) -> ClientEntitlement:
    entitlement_type_code = entitlement_type_for_slot(slot)
    now_utc = datetime.now(timezone.utc)
    entitlement = (
        db.query(ClientEntitlement)
        .filter(ClientEntitlement.client_id == client_id)
        .filter(ClientEntitlement.entitlement_type_code == entitlement_type_code)
        .filter(ClientEntitlement.record_status == RecordStatus.active)
        .filter(ClientEntitlement.quantity_remaining > 0)
        .filter(ClientEntitlement.starts_at <= now_utc)
        .filter(
            or_(
                ClientEntitlement.expires_at.is_(None),
                ClientEntitlement.expires_at >= now_utc,
            )
        )
        .order_by(ClientEntitlement.created_at.asc())
        .first()
    )
    if entitlement is None:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Aucun crédit actif n'est disponible pour ce type de rendez-vous.",
        )

    entitlement.quantity_remaining -= 1
    db.add(entitlement)
    db.flush()
    return entitlement


def restore_entitlement_for_slot(db: Session, slot: BookingSlot) -> None:
    if not slot.consumed_entitlement_id:
        return

    entitlement = db.get(ClientEntitlement, slot.consumed_entitlement_id)
    if entitlement is not None:
        entitlement.quantity_remaining += slot.consumed_entitlement_units or 1
        db.add(entitlement)

    slot.consumed_entitlement_id = None
    slot.consumed_entitlement_units = None


def confirm_slot_for_client_record(
    db: Session,
    slot: BookingSlot,
    client_record: Client,
    *,
    user_id: str,
    notes: str | None = None,
) -> ClientEntitlement:
    expire_hold(slot)

    if slot.status != SlotStatus.hold or slot.client_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ce créneau ne peut pas être confirmé (hold expiré ou appartient à un autre client).",
        )

    entitlement = reserve_entitlement_for_slot(db, slot, client_record.id)
    if notes:
        slot.notes = notes
    slot.status = SlotStatus.confirmed
    slot.hold_expires_at = None
    slot.consumed_entitlement_id = entitlement.id
    slot.consumed_entitlement_units = 1
    db.add(slot)
    db.flush()
    return entitlement


async def send_booking_confirmation_email_for_slot(
    db: Session,
    slot: BookingSlot,
    current_user: AppUser,
) -> None:
    praticien: AppUser | None = db.query(AppUser).filter(AppUser.id == slot.praticien_id).first()
    if praticien is None or not current_user.email:
        return

    from app.schemas.schedule import SESSION_TYPE_LABELS

    slot_date_str = slot.slot_date.strftime("%A %d %B %Y")
    slot_time_str = slot.start_time.strftime("%Hh%M")
    session_label = SESSION_TYPE_LABELS.get(slot.session_type, slot.session_type)
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
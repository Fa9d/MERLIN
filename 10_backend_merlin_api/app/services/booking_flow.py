from __future__ import annotations

import logging
from datetime import date, datetime, timedelta, timezone

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
from app.services.email import (
    make_appointment_reminder_email,
    make_booking_confirmation_email,
    send_email,
)

logger = logging.getLogger(__name__)


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


# ---------------------------------------------------------------------------
# Rappel automatique 24h avant le rendez-vous
# ---------------------------------------------------------------------------

_REMINDER_FLAG_PREFIX = "reminder_24h_sent:"


async def send_appointment_reminders(db: Session) -> int:
    """Envoie les rappels 24h pour tous les créneaux confirmés qui ont lieu demain.

    Utilise le champ `notes` pour marquer les créneaux déjà notifiés
    (préfixe «reminder_24h_sent:») afin d'éviter les doublons.
    Retourne le nombre de rappels envoyés.
    """
    from app.schemas.schedule import SESSION_TYPE_LABELS

    now = datetime.now(timezone.utc)
    tomorrow: date = (now + timedelta(hours=24)).date()

    slots = (
        db.query(BookingSlot)
        .filter(
            BookingSlot.status == SlotStatus.confirmed,
            BookingSlot.slot_date == tomorrow,
        )
        .all()
    )

    sent = 0
    for slot in slots:
        # Déduplication : on vérifie si le flag est déjà dans notes
        if slot.notes and _REMINDER_FLAG_PREFIX in slot.notes:
            continue

        client_user: AppUser | None = (
            db.query(AppUser).filter(AppUser.id == slot.client_id).first()
        )
        praticien: AppUser | None = (
            db.query(AppUser).filter(AppUser.id == slot.praticien_id).first()
        )

        if client_user is None or not client_user.email or praticien is None:
            continue

        slot_date_str = slot.slot_date.strftime("%A %d %B %Y")
        slot_time_str = slot.start_time.strftime("%Hh%M")
        session_label = SESSION_TYPE_LABELS.get(slot.session_type, str(slot.session_type))
        join_url = f"{settings.frontend_url}/mon-espace"

        html, text = make_appointment_reminder_email(
            display_name=client_user.display_name,
            praticien_name=praticien.display_name,
            slot_date=slot_date_str,
            slot_time=slot_time_str,
            session_type_label=session_label,
            join_url=join_url,
        )

        ok = await send_email(
            client_user.email,
            f"Rappel — votre rendez-vous demain à {slot_time_str} — IVIA",
            html,
            text,
        )

        if ok:
            # Marquer comme notifié
            flag = f"{_REMINDER_FLAG_PREFIX}{now.isoformat()}"
            slot.notes = (slot.notes or "") + f"\n{flag}" if slot.notes else flag
            db.add(slot)
            sent += 1
            logger.info("Rappel 24h envoyé pour slot %s → %s", slot.id, client_user.email)

    if sent > 0:
        db.commit()

    return sent


# ---------------------------------------------------------------------------
# Reprise de lien 48 h — demande d'entrée restée sans suite
# ---------------------------------------------------------------------------

_REPRISE_FLAG_PREFIX = "reprise_48h_sent:"


async def send_intake_reprise_48h(db: Session) -> int:
    """Relance unique 48 h après une demande d'entrée restée sans suite.

    Cible : demandes actives au statut «new», créées il y a 48 h à 7 jours,
    dont le client a un courriel et aucun créneau confirmé.
    Déduplication via le préfixe «reprise_48h_sent:» dans handling_notes.
    Une seule relance, jamais plus (plan de mise en marché §11).
    """
    from app.models.intake_request import IntakeRequest
    from app.models.enums import IntakeHandlingStatusCode
    from app.services.email import make_reprise_lien_email

    now = datetime.now(timezone.utc)
    window_start = now - timedelta(days=7)
    window_end = now - timedelta(hours=48)

    requests = (
        db.query(IntakeRequest)
        .filter(
            IntakeRequest.record_status == RecordStatus.active,
            IntakeRequest.handling_status_code == IntakeHandlingStatusCode.new,
            IntakeRequest.created_at >= window_start,
            IntakeRequest.created_at <= window_end,
        )
        .all()
    )

    sent = 0
    for req in requests:
        if req.handling_notes and _REPRISE_FLAG_PREFIX in req.handling_notes:
            continue

        client: Client | None = db.query(Client).filter(Client.id == req.client_id).first()
        if client is None:
            continue

        # Courriel : fiche client, sinon compte lié
        email = client.email
        display_name = client.first_name_or_alias
        if not email and client.app_user_id:
            user = db.query(AppUser).filter(AppUser.id == client.app_user_id).first()
            if user:
                email = user.email
                display_name = user.display_name or display_name
        if not email:
            continue

        # Ne pas relancer si un créneau est déjà confirmé pour ce compte
        if client.app_user_id:
            has_booking = (
                db.query(BookingSlot)
                .filter(
                    BookingSlot.client_id == client.app_user_id,
                    BookingSlot.status == SlotStatus.confirmed,
                )
                .first()
            )
            if has_booking:
                continue

        html, text = make_reprise_lien_email(
            display_name=display_name,
            reserve_url=f"{settings.frontend_url}/reserver.html",
        )
        ok = await send_email(email, "La porte est toujours ouverte — IVIA", html, text)

        if ok:
            flag = f"{_REPRISE_FLAG_PREFIX}{now.isoformat()}"
            req.handling_notes = f"{req.handling_notes}\n{flag}" if req.handling_notes else flag
            db.add(req)
            sent += 1
            logger.info("Reprise 48h envoyée pour demande %s → %s", req.id, email)

    if sent > 0:
        db.commit()

    return sent
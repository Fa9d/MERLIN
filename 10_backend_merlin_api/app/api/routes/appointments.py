"""Routes pour créneaux (slots) et rendez-vous (appointments)."""
import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import require_client, require_practitioner
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.appointment import Appointment, PractitionerSlot
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentOut,
    AppointmentStatusUpdate,
    PractitionerSlotCreate,
    PractitionerSlotOut,
    PractitionerSlotUpdate,
)
from app.services.email import (
    make_appointment_status_email,
    make_booking_confirmation_email,
    send_email,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/slots", tags=["calendar"])


# ── PRATICIEN SLOTS (CRUD) ──────────────────────────────────────────────────

@router.get("/me", response_model=list[PractitionerSlotOut])
def get_my_slots(
    current_user: AppUser = Depends(require_practitioner()),
    db: Session = Depends(get_db),
):
    """Liste mes créneaux disponibilité (praticien)."""
    slots = db.execute(
        select(PractitionerSlot)
        .where(PractitionerSlot.practitioner_id == current_user.id)
        .order_by(PractitionerSlot.start_time)
    ).scalars().all()
    
    return [PractitionerSlotOut.from_orm(s) for s in slots]


@router.post("/me", response_model=PractitionerSlotOut, status_code=status.HTTP_201_CREATED)
def create_slot(
    slot_data: PractitionerSlotCreate,
    current_user: AppUser = Depends(require_practitioner()),
    db: Session = Depends(get_db),
):
    """Créer un créneau (praticien)."""
    # Validation : end_time > start_time
    if slot_data.end_time <= slot_data.start_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="end_time must be after start_time",
        )
    
    # Créer slot
    slot = PractitionerSlot(
        practitioner_id=current_user.id,
        start_time=slot_data.start_time,
        end_time=slot_data.end_time,
        duration_minutes=slot_data.duration_minutes,
        is_available=slot_data.is_available,
        notes=slot_data.notes,
    )
    
    db.add(slot)
    db.commit()
    db.refresh(slot)
    
    logger.info(f"Created slot for practitioner {current_user.id}: {slot.id}")
    
    return PractitionerSlotOut.from_orm(slot)


@router.patch("/{slot_id}", response_model=PractitionerSlotOut)
def update_slot(
    slot_id: str,
    slot_data: PractitionerSlotUpdate,
    current_user: AppUser = Depends(require_practitioner()),
    db: Session = Depends(get_db),
):
    """Modifier un créneau (praticien)."""
    slot = db.execute(
        select(PractitionerSlot)
        .where(PractitionerSlot.id == slot_id)
        .where(PractitionerSlot.practitioner_id == current_user.id)
    ).scalar()
    
    if not slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Slot not found",
        )
    
    # Update fields (only non-None)
    update_data = slot_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(slot, field, value)
    
    slot.updated_at = datetime.now(timezone.utc)
    db.add(slot)
    db.commit()
    db.refresh(slot)
    
    logger.info(f"Updated slot {slot_id} for practitioner {current_user.id}")
    
    return PractitionerSlotOut.from_orm(slot)


@router.delete("/{slot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_slot(
    slot_id: str,
    current_user: AppUser = Depends(require_practitioner()),
    db: Session = Depends(get_db),
):
    """Supprimer un créneau (praticien)."""
    slot = db.execute(
        select(PractitionerSlot)
        .where(PractitionerSlot.id == slot_id)
        .where(PractitionerSlot.practitioner_id == current_user.id)
    ).scalar()
    
    if not slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Slot not found",
        )
    
    db.delete(slot)
    db.commit()
    
    logger.info(f"Deleted slot {slot_id} for practitioner {current_user.id}")


# ── PUBLIC: Available Slots for Praticien ──────────────────────────────────

@router.get("/available/{practitioner_id}", response_model=list[PractitionerSlotOut])
def get_available_slots(
    practitioner_id: str,
    db: Session = Depends(get_db),
):
    """Liste créneaux disponibles pour un praticien (client peut voir)."""
    slots = db.execute(
        select(PractitionerSlot)
        .where(PractitionerSlot.practitioner_id == practitioner_id)
        .where(PractitionerSlot.is_available == True)  # noqa: E712
        .where(PractitionerSlot.start_time > datetime.now(timezone.utc))
        .order_by(PractitionerSlot.start_time)
    ).scalars().all()
    
    return [PractitionerSlotOut.from_orm(s) for s in slots]


# ── APPOINTMENTS (CRUD) ─────────────────────────────────────────────────────

@router.get("/appointments/me", response_model=list[AppointmentOut])
def get_my_appointments(
    current_user: AppUser = Depends(require_client()),
    db: Session = Depends(get_db),
):
    """Liste mes rendez-vous (client)."""
    appointments = db.execute(
        select(Appointment)
        .where(Appointment.client_id == current_user.id)
        .order_by(Appointment.start_time.desc())
    ).scalars().all()
    
    return [AppointmentOut.from_orm(a) for a in appointments]


@router.post("/appointments", response_model=AppointmentOut, status_code=status.HTTP_201_CREATED)
async def create_appointment(
    appt_data: AppointmentCreate,
    current_user: AppUser = Depends(require_client()),
    db: Session = Depends(get_db),
):
    """Créer un rendez-vous (client réserve) + envoyer email de confirmation."""
    # Validation : end_time > start_time
    if appt_data.end_time <= appt_data.start_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="end_time must be after start_time",
        )
    
    # Vérifier praticien existe
    praticien = db.execute(
        select(AppUser).where(AppUser.id == appt_data.practitioner_id)
    ).scalar()
    
    if not praticien:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Practitioner not found",
        )

    # Si un créneau est référencé : le verrouiller (anti double-réservation)
    slot = None
    if appt_data.slot_id:
        slot = db.execute(
            select(PractitionerSlot)
            .where(PractitionerSlot.id == appt_data.slot_id)
            .where(PractitionerSlot.practitioner_id == appt_data.practitioner_id)
            .with_for_update()
        ).scalar()
        if not slot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Slot not found",
            )
        if not slot.is_available:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Slot is no longer available",
            )

    # Garde anti-chevauchement : pas de rendez-vous actif du praticien sur la plage
    overlap = db.execute(
        select(Appointment.id)
        .where(Appointment.practitioner_id == appt_data.practitioner_id)
        .where(Appointment.status != "cancelled")
        .where(Appointment.start_time < appt_data.end_time)
        .where(Appointment.end_time > appt_data.start_time)
        .limit(1)
    ).scalar()
    if overlap:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Practitioner already has an appointment on this time range",
        )
    
    # Créer appointment (+ marquer le créneau réservé)
    appointment = Appointment(
        client_id=current_user.id,
        practitioner_id=appt_data.practitioner_id,
        slot_id=appt_data.slot_id,
        start_time=appt_data.start_time,
        end_time=appt_data.end_time,
        duration_minutes=appt_data.duration_minutes,
        status="scheduled",
    )
    if slot:
        slot.is_available = False
        db.add(slot)
    
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    
    logger.info(f"Created appointment {appointment.id} for client {current_user.id}")
    
    # Courriel de confirmation (non bloquant)
    try:
        html, text = make_booking_confirmation_email(
            display_name=current_user.display_name or "Client",
            praticien_name=praticien.display_name or "Praticien·ne",
            slot_date=appointment.start_time.strftime("%d-%m-%Y"),
            slot_time=appointment.start_time.strftime("%H:%M"),
            session_type_label=f"Séance ({appointment.duration_minutes} min)",
            cancel_url="https://ivia.quebec/client/agenda.html",
        )
        await send_email(
            to_email=current_user.email,
            subject="Confirmation de votre réservation IVIA",
            html_body=html,
            text_body=text,
        )
    except Exception as e:
        logger.error(f"Failed to send booking confirmation email: {e}")
        # Don't fail appointment creation if email fails
    
    return AppointmentOut.from_orm(appointment)


@router.patch("/appointments/{appointment_id}", response_model=AppointmentOut)
async def update_appointment_status(
    appointment_id: str,
    status_data: AppointmentStatusUpdate,
    current_user: AppUser = Depends(require_practitioner()),
    db: Session = Depends(get_db),
):
    """Mettre à jour le statut d'un rendez-vous (praticien) + envoyer email de notification."""
    appointment = db.execute(
        select(Appointment)
        .where(Appointment.id == appointment_id)
        .where(Appointment.practitioner_id == current_user.id)
    ).scalar()
    
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found",
        )
    
    # Valider statut
    valid_statuses = {"scheduled", "confirmed", "paid", "noted", "cancelled"}
    if status_data.status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}",
        )
    
    # Update status + timestamp
    old_status = appointment.status
    appointment.status = status_data.status
    now = datetime.now(timezone.utc)
    
    if status_data.status == "confirmed":
        appointment.confirmed_at = now
    elif status_data.status == "paid":
        appointment.paid_at = now
    elif status_data.status == "noted":
        appointment.noted_at = now
    elif status_data.status == "cancelled" and appointment.slot_id:
        # Libérer le créneau si le rendez-vous n'a pas encore eu lieu
        slot = db.get(PractitionerSlot, appointment.slot_id)
        if slot and slot.start_time > now:
            slot.is_available = True
            db.add(slot)
    
    appointment.updated_at = now
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    
    logger.info(f"Updated appointment {appointment_id} status to {status_data.status}")
    
    # Courriel de notification (non bloquant)
    try:
        client = db.execute(
            select(AppUser).where(AppUser.id == appointment.client_id)
        ).scalar()
        if client and old_status != appointment.status:
            made = make_appointment_status_email(
                display_name=client.display_name or "Client",
                status_code=appointment.status,
                praticien_name=current_user.display_name,
            )
            if made:
                html, text = made
                await send_email(
                    to_email=client.email,
                    subject="Mise à jour de votre rendez-vous IVIA",
                    html_body=html,
                    text_body=text,
                )
    except Exception as e:
        logger.error(f"Failed to send status email: {e}")
        # Don't fail status update if email fails
    
    return AppointmentOut.from_orm(appointment)


@router.delete("/appointments/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_appointment(
    appointment_id: str,
    current_user: AppUser = Depends(require_client()),
    db: Session = Depends(get_db),
):
    """Annuler un rendez-vous (client)."""
    appointment = db.execute(
        select(Appointment)
        .where(Appointment.id == appointment_id)
        .where(Appointment.client_id == current_user.id)
    ).scalar()
    
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found",
        )
    
    # Soft-delete par changement de status + libération du créneau
    appointment.status = "cancelled"
    now = datetime.now(timezone.utc)
    appointment.updated_at = now
    if appointment.slot_id:
        slot = db.get(PractitionerSlot, appointment.slot_id)
        if slot and slot.start_time > now:
            slot.is_available = True
            db.add(slot)
    db.add(appointment)
    db.commit()
    
    logger.info(f"Cancelled appointment {appointment_id}")

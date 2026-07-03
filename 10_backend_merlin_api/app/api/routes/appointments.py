"""Routes pour créneaux (slots) et rendez-vous (appointments)."""
import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.deps import require_client, require_practitioner
from app.db.session import get_db
from app.models.app_user import AppUser
from app.models.appointment import Appointment, PractitionerSlot
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentOut,
    AppointmentStatusUpdate,
    AppointmentUpdate,
    PractitionerSlotCreate,
    PractitionerSlotOut,
    PractitionerSlotUpdate,
)
from app.services.email_service import EmailService

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
def create_appointment(
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
    
    # Créer appointment
    appointment = Appointment(
        client_id=current_user.id,
        practitioner_id=appt_data.practitioner_id,
        slot_id=appt_data.slot_id,
        start_time=appt_data.start_time,
        end_time=appt_data.end_time,
        duration_minutes=appt_data.duration_minutes,
        status="scheduled",
    )
    
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    
    logger.info(f"Created appointment {appointment.id} for client {current_user.id}")
    
    # Send booking confirmation email (non-blocking)
    try:
        email_service = EmailService(settings)
        email_service.send_booking_confirmation(
            client_email=current_user.email,
            client_name=current_user.first_name or "Client",
            practitioner_name=praticien.first_name or "Praticien",
            appointment_date=appointment.start_time.strftime("%d-%m-%Y"),
            appointment_time=appointment.start_time.strftime("%H:%M")
        )
        logger.info(f"Booking confirmation email sent to {current_user.email}")
    except Exception as e:
        logger.error(f"Failed to send booking confirmation email: {e}")
        # Don't fail appointment creation if email fails
    
    return AppointmentOut.from_orm(appointment)


@router.patch("/appointments/{appointment_id}", response_model=AppointmentOut)
def update_appointment_status(
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
    
    appointment.updated_at = now
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    
    logger.info(f"Updated appointment {appointment_id} status to {status_data.status}")
    
    # Send status update email (non-blocking)
    try:
        client = db.execute(
            select(AppUser).where(AppUser.id == appointment.client_id)
        ).scalar()
        
        if client:
            email_service = EmailService(settings)
            
            if appointment.status == "paid":
                email_service.send_payment_confirmation(
                    client_email=client.email,
                    client_name=client.first_name or "Client",
                    amount_cents=appointment.amount_cents or 0,
                    currency="CAD"
                )
                logger.info(f"Payment confirmation email sent to {client.email}")
            
            elif appointment.status == "noted":
                email_service.send_status_update(
                    client_email=client.email,
                    client_name=client.first_name or "Client",
                    status="noted",
                    session_notes=getattr(status_data, 'notes', None)
                )
                logger.info(f"Status update email sent to {client.email}")
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
    
    # Soft-delete par changement de status
    appointment.status = "cancelled"
    appointment.updated_at = datetime.now(timezone.utc)
    db.add(appointment)
    db.commit()
    
    logger.info(f"Cancelled appointment {appointment_id}")

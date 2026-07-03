"""Schémas pour créneaux et rendez-vous."""
from datetime import datetime

from pydantic import BaseModel, Field


class PractitionerSlotCreate(BaseModel):
    """Créer un créneau praticien."""
    start_time: datetime = Field(..., description="Start time (ISO 8601 with TZ)")
    end_time: datetime = Field(..., description="End time (ISO 8601 with TZ)")
    duration_minutes: int = Field(default=60, ge=15, le=480, description="Duration in minutes")
    is_available: bool = Field(default=True, description="Available for booking?")
    notes: str | None = Field(None, max_length=500, description="Optional notes")


class PractitionerSlotUpdate(BaseModel):
    """Modifier un créneau praticien."""
    start_time: datetime | None = None
    end_time: datetime | None = None
    duration_minutes: int | None = Field(None, ge=15, le=480)
    is_available: bool | None = None
    notes: str | None = Field(None, max_length=500)


class PractitionerSlotOut(BaseModel):
    """Réponse créneau praticien."""
    id: str
    practitioner_id: str
    start_time: datetime
    end_time: datetime
    duration_minutes: int
    is_available: bool
    notes: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AppointmentCreate(BaseModel):
    """Créer un rendez-vous (client réserve)."""
    practitioner_id: str = Field(..., description="Praticien UUID")
    start_time: datetime = Field(..., description="Start time (ISO 8601 with TZ)")
    end_time: datetime = Field(..., description="End time (ISO 8601 with TZ)")
    duration_minutes: int = Field(default=60, ge=15, le=480)
    slot_id: str | None = Field(None, description="Optional reference to practitioner_slots")


class AppointmentUpdate(BaseModel):
    """Modifier un rendez-vous (praticien updates status)."""
    status: str | None = Field(None, description="scheduled/confirmed/paid/noted/cancelled")
    session_id: str | None = None
    payment_order_id: str | None = None
    session_notes_id: str | None = None


class AppointmentOut(BaseModel):
    """Réponse rendez-vous."""
    id: str
    client_id: str
    practitioner_id: str
    slot_id: str | None
    start_time: datetime
    end_time: datetime
    duration_minutes: int
    status: str
    session_id: str | None
    payment_order_id: str | None
    session_notes_id: str | None
    created_at: datetime
    updated_at: datetime
    confirmed_at: datetime | None
    paid_at: datetime | None
    noted_at: datetime | None

    class Config:
        from_attributes = True


class AppointmentStatusUpdate(BaseModel):
    """Update appointment status (praticien workflow)."""
    status: str = Field(..., description="New status: scheduled/confirmed/paid/noted/cancelled")

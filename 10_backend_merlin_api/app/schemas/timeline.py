"""Schémas Pydantic pour les endpoints de timeline et notes de séance (Phase 5)."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AppointmentHistoryItem(BaseModel):
    """Item dans la timeline client — historique des rendez-vous."""

    id: str
    created_at: datetime
    scheduled_at: datetime
    duration_minutes: int

    # Praticien
    practitioner_id: str
    practitioner_name: str
    practitioner_audio_url: Optional[str] = None  # Presigned URL

    # Status
    status: str  # scheduled | confirmed | paid | noted | cancelled
    confirmed_at: Optional[datetime] = None
    paid_at: Optional[datetime] = None
    noted_at: Optional[datetime] = None

    # Payment
    amount_cents: Optional[int] = None
    currency: str = "CAD"

    # Notes
    session_notes: Optional[str] = None  # Visible to client
    practitioner_notes: Optional[str] = None  # Only visible to praticien

    class Config:
        from_attributes = True


class AppointmentHistoryResponse(BaseModel):
    """Response pour GET /appointments/history."""

    count: int
    appointments: list[AppointmentHistoryItem]


class PractitionerStatsResponse(BaseModel):
    """Response pour GET /me/appointments/stats."""

    appointments_this_week: int = Field(ge=0)
    appointments_this_month: int = Field(ge=0)
    total_revenue_cents: int = Field(ge=0)
    completed_count: int = Field(ge=0)
    pending_confirmations: int = Field(ge=0)
    upcoming_appointments: list[AppointmentHistoryItem] = Field(default_factory=list)


class AuditTrailEntry(BaseModel):
    """Entry dans l'audit trail d'un rendez-vous."""

    action: str  # created | confirmed | paid | noted | cancelled
    by: str  # Client email, Praticien email, ou "stripe"
    at: datetime


class AppointmentDetailResponse(BaseModel):
    """Response détaillée pour GET /appointments/{id}."""

    id: str
    created_at: datetime
    scheduled_at: datetime
    duration_minutes: int

    # Praticien
    practitioner_id: str
    practitioner_name: str

    # Status
    status: str
    confirmed_at: Optional[datetime] = None
    paid_at: Optional[datetime] = None
    noted_at: Optional[datetime] = None

    # Payment
    amount_cents: Optional[int] = None
    currency: str = "CAD"

    # Notes
    session_notes: Optional[str] = None
    practitioner_notes: Optional[str] = None

    # Audit trail
    audit_trail: list[AuditTrailEntry] = Field(default_factory=list)

    class Config:
        from_attributes = True


class AddSessionNotesRequest(BaseModel):
    """Request pour PATCH /appointments/{id}/notes."""

    session_notes: Optional[str] = Field(
        None,
        max_length=2000,
        description="Notes visibles au client"
    )
    practitioner_notes: Optional[str] = Field(
        None,
        max_length=2000,
        description="Notes internes (praticien seulement)"
    )

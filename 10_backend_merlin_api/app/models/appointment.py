"""Modèles pour créneaux et rendez-vous praticiens."""
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class PractitionerSlot(Base):
    """Créneau disponibilité praticien — éditable par praticien lui-même."""
    __tablename__ = "practitioner_slots"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    practitioner_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("app_users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    end_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    duration_minutes: Mapped[int] = mapped_column(
        Integer, nullable=False, default=60
    )
    is_available: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relations
    practitioner = relationship("AppUser", foreign_keys=[practitioner_id])


class Appointment(Base):
    """Rendez-vous réservé — création par client, édition par praticien."""
    __tablename__ = "appointments"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    client_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("app_users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    practitioner_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("app_users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    slot_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("practitioner_slots.id", ondelete="SET NULL"), nullable=True
    )
    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    end_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    duration_minutes: Mapped[int] = mapped_column(
        Integer, nullable=False, default=60
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="scheduled"
        # scheduled, confirmed, paid, noted, cancelled
    )
    session_id: Mapped[str | None] = mapped_column(
        String(36), nullable=True  # FK to audio_sessions (added later if needed)
    )
    payment_order_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("payment_orders.id", ondelete="SET NULL"), nullable=True
    )
    session_notes_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("session_notes.id", ondelete="SET NULL"), nullable=True
    )
    stripe_session_id: Mapped[str | None] = mapped_column(
        String(255), nullable=True, index=True
    )
    payment_intent_id: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )
    amount_cents: Mapped[int | None] = mapped_column(
        Integer, nullable=True  # e.g., 3500 = $35.00 CAD
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    confirmed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    paid_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    noted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    session_notes: Mapped[str | None] = mapped_column(
       Text, nullable=True  # Client-facing notes from praticien
    )
    practitioner_notes: Mapped[str | None] = mapped_column(
       Text, nullable=True  # Praticien-only internal notes
    )

    # Relations
    client = relationship("AppUser", foreign_keys=[client_id])
    practitioner = relationship("AppUser", foreign_keys=[practitioner_id])
    slot: Mapped["PractitionerSlot | None"] = relationship(
       "PractitionerSlot", foreign_keys=[slot_id]
    )

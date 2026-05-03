"""Modèles SQLAlchemy pour la gestion des disponibilités praticien et des créneaux."""
from __future__ import annotations

from datetime import date, datetime, time, timezone
from uuid import uuid4

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    Time,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import DayOfWeek, ExceptionType, SessionTypeCode, SlotStatus


class PractitionerSchedule(Base):
    """Gabarit hebdomadaire de disponibilités d'un praticien."""
    __tablename__ = "practitioner_schedules"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    praticien_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("app_users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    day_of_week: Mapped[int] = mapped_column(Integer, nullable=False)          # 0=lundi … 6=dimanche
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    session_duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=60)
    buffer_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=15)
    session_type: Mapped[str] = mapped_column(
        Enum(SessionTypeCode, native_enum=False), nullable=False, default=SessionTypeCode.standard
    )
    valid_from: Mapped[date | None] = mapped_column(Date, nullable=True)
    valid_until: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # relations
    praticien: Mapped["app.models.app_user.AppUser"] = relationship(  # type: ignore[name-defined]
        "AppUser", foreign_keys=[praticien_id]
    )


class ScheduleException(Base):
    """Exception ponctuelle au gabarit (journée bloquée ou créneau supplémentaire)."""
    __tablename__ = "schedule_exceptions"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    praticien_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("app_users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    exception_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    exception_type: Mapped[str] = mapped_column(
        Enum(ExceptionType, native_enum=False), nullable=False, default=ExceptionType.blocked
    )
    start_time: Mapped[time | None] = mapped_column(Time, nullable=True)   # None = journée entière
    end_time: Mapped[time | None] = mapped_column(Time, nullable=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )


class BookingSlot(Base):
    """Créneau matérialisé prêt à être réservé par un client."""
    __tablename__ = "booking_slots"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    praticien_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("app_users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    schedule_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("practitioner_schedules.id", ondelete="SET NULL"), nullable=True
    )
    client_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("app_users.id", ondelete="SET NULL"), nullable=True
    )
    slot_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    session_type: Mapped[str] = mapped_column(
        Enum(SessionTypeCode, native_enum=False), nullable=False, default=SessionTypeCode.standard
    )
    status: Mapped[str] = mapped_column(
        Enum(SlotStatus, native_enum=False), nullable=False, default=SlotStatus.available
    )
    hold_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

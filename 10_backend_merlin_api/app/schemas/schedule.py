"""Schémas Pydantic pour disponibilités praticien et créneaux de réservation."""
from __future__ import annotations

from datetime import date, datetime, time
from typing import Any

from pydantic import BaseModel, field_validator, model_validator

from app.models.enums import DayOfWeek, ExceptionType, SessionTypeCode, SlotStatus

SESSION_DURATIONS: dict[str, int] = {
    SessionTypeCode.intake: 90,
    SessionTypeCode.standard: 60,
    SessionTypeCode.follow_up: 45,
    SessionTypeCode.any: 60,
}

DAY_LABELS: dict[int, str] = {
    0: "Lundi", 1: "Mardi", 2: "Mercredi",
    3: "Jeudi", 4: "Vendredi", 5: "Samedi", 6: "Dimanche",
}

SESSION_TYPE_LABELS: dict[str, str] = {
    SessionTypeCode.intake: "Évaluation initiale (90 min)",
    SessionTypeCode.standard: "Consultation standard (60 min)",
    SessionTypeCode.follow_up: "Suivi court (45 min)",
    SessionTypeCode.any: "Type libre",
}


# ---------------------------------------------------------------------------
# PractitionerSchedule (gabarit hebdomadaire)
# ---------------------------------------------------------------------------

class ScheduleSlotCreate(BaseModel):
    day_of_week: int                             # 0=lundi…6=dimanche
    start_time: time
    end_time: time
    session_duration_minutes: int = 60
    buffer_minutes: int = 15
    session_type: SessionTypeCode = SessionTypeCode.standard
    valid_from: date | None = None
    valid_until: date | None = None

    @field_validator("day_of_week")
    @classmethod
    def validate_day(cls, v: int) -> int:
        if v not in range(7):
            raise ValueError("day_of_week doit être entre 0 (lundi) et 6 (dimanche)")
        return v

    @model_validator(mode="after")
    def validate_times(self) -> "ScheduleSlotCreate":
        if self.end_time <= self.start_time:
            raise ValueError("end_time doit être après start_time")
        return self


class ScheduleSlotUpdate(BaseModel):
    start_time: time | None = None
    end_time: time | None = None
    session_duration_minutes: int | None = None
    buffer_minutes: int | None = None
    session_type: SessionTypeCode | None = None
    valid_from: date | None = None
    valid_until: date | None = None
    is_active: bool | None = None


class ScheduleSlotOut(BaseModel):
    id: str
    praticien_id: str
    day_of_week: int
    day_label: str
    start_time: time
    end_time: time
    session_duration_minutes: int
    buffer_minutes: int
    session_type: SessionTypeCode
    session_type_label: str
    valid_from: date | None
    valid_until: date | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_with_labels(cls, obj: Any) -> "ScheduleSlotOut":
        data = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
        data["day_label"] = DAY_LABELS.get(obj.day_of_week, str(obj.day_of_week))
        data["session_type_label"] = SESSION_TYPE_LABELS.get(obj.session_type, obj.session_type)
        return cls(**data)


# ---------------------------------------------------------------------------
# ScheduleException
# ---------------------------------------------------------------------------

class ScheduleExceptionCreate(BaseModel):
    exception_date: date
    exception_type: ExceptionType = ExceptionType.blocked
    start_time: time | None = None    # None = journée entière
    end_time: time | None = None
    reason: str | None = None


class ScheduleExceptionOut(BaseModel):
    id: str
    praticien_id: str
    exception_date: date
    exception_type: ExceptionType
    start_time: time | None
    end_time: time | None
    reason: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# BookingSlot (créneaux disponibles)
# ---------------------------------------------------------------------------

class AvailableSlotOut(BaseModel):
    """Créneau calculé (pas forcément persisté), pour la vue publique de réservation."""
    praticien_id: str
    praticien_name: str
    slot_date: date
    start_time: time
    end_time: time
    session_type: SessionTypeCode
    session_type_label: str
    duration_minutes: int
    # ID du slot si déjà persisté en base (None si slot virtuel)
    slot_id: str | None = None
    status: SlotStatus = SlotStatus.available


class BookingSlotOut(BaseModel):
    id: str
    praticien_id: str
    client_id: str | None
    slot_date: date
    start_time: time
    end_time: time
    session_type: SessionTypeCode
    status: SlotStatus
    hold_expires_at: datetime | None
    notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

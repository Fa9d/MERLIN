from datetime import datetime

from app.models.enums import DataSensitivityClass, EmotionalChargeCode, RecordStatus
from app.schemas.common import MerlinSchema


class SessionTemporalAnchorCreate(MerlinSchema):
    session_id: str
    session_note_id: str | None = None
    client_id: str
    life_event_id: str | None = None
    verbatim_fragment: str | None = None
    said_at_offset_sec: int | None = None
    event_year_approx: int | None = None
    client_age_ref: int | None = None
    gap_years: int | None = None  # calculé côté client ou laissé à None pour calcul auto
    interpretation_note: str | None = None
    emotional_charge: EmotionalChargeCode | None = None
    is_silence_marker: bool = False


class SessionTemporalAnchorUpdate(MerlinSchema):
    life_event_id: str | None = None
    verbatim_fragment: str | None = None
    said_at_offset_sec: int | None = None
    event_year_approx: int | None = None
    client_age_ref: int | None = None
    gap_years: int | None = None
    interpretation_note: str | None = None
    emotional_charge: EmotionalChargeCode | None = None
    is_silence_marker: bool | None = None
    record_status: RecordStatus | None = None


class SessionTemporalAnchorRead(MerlinSchema):
    id: str
    session_id: str
    session_note_id: str | None = None
    client_id: str
    life_event_id: str | None = None
    verbatim_fragment: str | None = None
    said_at_offset_sec: int | None = None
    event_year_approx: int | None = None
    client_age_ref: int | None = None
    gap_years: int | None = None
    interpretation_note: str | None = None
    emotional_charge: EmotionalChargeCode | None = None
    is_silence_marker: bool
    record_status: RecordStatus
    data_sensitivity_class: DataSensitivityClass
    created_at: datetime
    updated_at: datetime

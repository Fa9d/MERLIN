from datetime import datetime

from pydantic import field_validator

from app.models.enums import (
    DataSensitivityClass,
    JournalEntryKindCode,
    JournalEntryTypeCode,
    RecordStatus,
    RetentionClass,
    SessionPhaseCode,
)
from app.schemas.common import MerlinSchema

# Axes canoniques MERLIN (voir 00_DOCTRINE/correspondances-vivantes.md)
CANONICAL_AXES = {
    "territoire", "corps", "metabolisme", "emotions", "mental", "relations",
    "famille", "transgenerationnel", "societe", "spirituel", "urgence",
}


class _JournalStructuredMixin(MerlinSchema):
    entry_kind: JournalEntryKindCode = JournalEntryKindCode.libre
    dimensions: list[str] | None = None
    structured_payload: dict | None = None
    session_id: str | None = None
    session_phase: SessionPhaseCode | None = None

    @field_validator("dimensions")
    @classmethod
    def _valider_axes(cls, v: list[str] | None) -> list[str] | None:
        if v is None:
            return v
        inconnus = [a for a in v if a not in CANONICAL_AXES]
        if inconnus:
            raise ValueError(f"Axes inconnus : {inconnus}. Axes valides : {sorted(CANONICAL_AXES)}")
        return v


class ClientJournalEntryCreate(_JournalStructuredMixin):
    client_id: str
    linked_event_id: str | None = None
    entry_type: JournalEntryTypeCode = JournalEntryTypeCode.aujourd_hui
    body_text: str
    emotional_tone: str | None = None
    event_year_ref: int | None = None
    written_at: datetime | None = None  # si omis, now() en base


class MyJournalEntryCreate(_JournalStructuredMixin):
    """Utilisé par /me/journal — client_id est injecté depuis la session, pas envoyé par le client."""

    linked_event_id: str | None = None
    entry_type: JournalEntryTypeCode = JournalEntryTypeCode.aujourd_hui
    body_text: str
    emotional_tone: str | None = None
    event_year_ref: int | None = None
    written_at: datetime | None = None


class ClientJournalEntryUpdate(MerlinSchema):
    linked_event_id: str | None = None
    entry_type: JournalEntryTypeCode | None = None
    body_text: str | None = None
    emotional_tone: str | None = None
    event_year_ref: int | None = None
    record_status: RecordStatus | None = None
    entry_kind: JournalEntryKindCode | None = None
    dimensions: list[str] | None = None
    structured_payload: dict | None = None
    session_id: str | None = None
    session_phase: SessionPhaseCode | None = None


class ClientJournalEntryRead(MerlinSchema):
    id: str
    client_id: str
    linked_event_id: str | None = None
    entry_type: JournalEntryTypeCode
    body_text: str
    emotional_tone: str | None = None
    event_year_ref: int | None = None
    entry_kind: JournalEntryKindCode
    dimensions: list[str] | None = None
    structured_payload: dict | None = None
    session_id: str | None = None
    session_phase: SessionPhaseCode | None = None
    written_at: datetime
    record_status: RecordStatus
    data_sensitivity_class: DataSensitivityClass
    retention_class: RetentionClass
    created_at: datetime

from datetime import datetime

from app.models.enums import DataSensitivityClass, JournalEntryTypeCode, RecordStatus, RetentionClass
from app.schemas.common import MerlinSchema


class ClientJournalEntryCreate(MerlinSchema):
    client_id: str
    linked_event_id: str | None = None
    entry_type: JournalEntryTypeCode = JournalEntryTypeCode.aujourd_hui
    body_text: str
    emotional_tone: str | None = None
    event_year_ref: int | None = None
    written_at: datetime | None = None  # si omis, now() en base


class MyJournalEntryCreate(MerlinSchema):
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


class ClientJournalEntryRead(MerlinSchema):
    id: str
    client_id: str
    linked_event_id: str | None = None
    entry_type: JournalEntryTypeCode
    body_text: str
    emotional_tone: str | None = None
    event_year_ref: int | None = None
    written_at: datetime
    record_status: RecordStatus
    data_sensitivity_class: DataSensitivityClass
    retention_class: RetentionClass
    created_at: datetime

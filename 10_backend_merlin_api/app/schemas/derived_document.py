from app.models.enums import DataSensitivityClass, RecordStatus, RetentionClass
from app.schemas.common import MerlinSchema, TimestampedReadSchema


class DerivedDocumentCreate(MerlinSchema):
    client_id: str
    session_id: str
    source_note_id: str
    document_kind_code: str = "session_summary"
    audience_code: str = "client"
    title: str
    body_text: str
    client_visible: bool = False
    record_status: RecordStatus = RecordStatus.active
    data_sensitivity_class: DataSensitivityClass = DataSensitivityClass.high
    retention_class: RetentionClass = RetentionClass.standard


class DerivedDocumentRead(TimestampedReadSchema):
    id: str
    client_id: str
    session_id: str
    source_note_id: str
    document_kind_code: str
    audience_code: str
    title: str
    body_text: str
    client_visible: bool
    record_status: RecordStatus
    data_sensitivity_class: DataSensitivityClass
    retention_class: RetentionClass

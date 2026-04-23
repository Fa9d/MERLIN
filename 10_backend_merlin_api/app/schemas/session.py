from datetime import datetime

from app.models.enums import (
    AnalysisNextStepCode,
    DataSensitivityClass,
    RecordStatus,
    RetentionClass,
    RiskLevelCode,
    SessionChannelCode,
    SessionModeCode,
    SessionStatusCode,
)
from app.schemas.common import MerlinSchema, TimestampedReadSchema
from app.schemas.derived_document import DerivedDocumentRead
from app.schemas.session_note import SessionNoteRead


class SessionCreate(MerlinSchema):
    client_id: str
    intake_request_id: str | None = None
    session_sequence_number: int | None = None
    session_mode_code: SessionModeCode = SessionModeCode.standard
    session_channel_code: SessionChannelCode = SessionChannelCode.phone
    scheduled_start_at: datetime | None = None
    actual_start_at: datetime | None = None
    actual_end_at: datetime | None = None
    duration_minutes: int | None = None
    session_status_code: SessionStatusCode = SessionStatusCode.scheduled
    record_status: RecordStatus = RecordStatus.active
    data_sensitivity_class: DataSensitivityClass = DataSensitivityClass.high
    retention_class: RetentionClass = RetentionClass.standard


class SessionRead(TimestampedReadSchema):
    id: str
    client_id: str
    intake_request_id: str | None = None
    session_sequence_number: int
    session_mode_code: SessionModeCode
    session_channel_code: SessionChannelCode
    scheduled_start_at: datetime | None = None
    actual_start_at: datetime | None = None
    actual_end_at: datetime | None = None
    duration_minutes: int | None = None
    room_name: str | None = None
    room_sid: str | None = None
    egress_id: str | None = None
    audio_file_path: str | None = None
    operator_user_id: str
    session_status_code: SessionStatusCode
    record_status: RecordStatus
    data_sensitivity_class: DataSensitivityClass
    retention_class: RetentionClass


class SessionClose(MerlinSchema):
    actual_start_at: datetime | None = None
    actual_end_at: datetime | None = None
    session_status_code: SessionStatusCode = SessionStatusCode.completed
    presenting_topic_text: str
    session_highlights_text: str
    operator_assessment_text: str | None = None
    vigilance_level_code: RiskLevelCode = RiskLevelCode.non_urgent
    coeur_summary_text: str | None = None
    corps_summary_text: str | None = None
    esprit_summary_text: str | None = None
    etre_summary_text: str | None = None
    immediate_context_text: str | None = None
    context_factors_json: dict | list | None = None
    identified_tensions_json: dict | list | None = None
    next_step_type_code: AnalysisNextStepCode | None = None
    client_facing_summary_text: str | None = None
    supervision_summary_text: str | None = None
    research_notes_text: str | None = None
    transcript_text: str | None = None
    follow_up_actions_text: str | None = None
    next_session_focus_text: str | None = None
    client_visible: bool = False


class SessionStart(MerlinSchema):
    actual_start_at: datetime | None = None


class SessionCloseResult(MerlinSchema):
    session: SessionRead
    generated_note: SessionNoteRead
    generated_document: DerivedDocumentRead


class SessionRoomRead(MerlinSchema):
    session_id: str
    room_name: str
    room_sid: str | None = None
    livekit_url: str
    practitioner_identity: str
    practitioner_token: str
    client_identity: str
    client_token: str


class SessionRecordingRead(MerlinSchema):
    session_id: str
    room_name: str
    room_sid: str | None = None
    egress_id: str | None = None
    audio_file_path: str | None = None
    audio_recording_id: str | None = None
    status: str

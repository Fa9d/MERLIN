from datetime import datetime

from app.models.enums import (
    AnalysisNextStepCode,
    DataSensitivityClass,
    RecordStatus,
    RetentionClass,
    RiskLevelCode,
)
from app.schemas.common import MerlinSchema, TimestampedReadSchema


class SessionNoteCreate(MerlinSchema):
    session_id: str
    client_id: str
    note_sequence_number: int | None = None
    summary_text: str
    observations_text: str | None = None
    follow_up_actions_text: str | None = None
    next_session_focus_text: str | None = None
    coeur_summary_text: str | None = None
    corps_summary_text: str | None = None
    esprit_summary_text: str | None = None
    etre_summary_text: str | None = None
    immediate_context_text: str | None = None
    context_factors_json: dict | list | None = None
    context_hypotheses_json: dict | list | None = None
    identified_tensions_json: dict | list | None = None
    vigilance_level_code: RiskLevelCode = RiskLevelCode.non_urgent
    next_step_type_code: AnalysisNextStepCode | None = None
    client_facing_summary_text: str | None = None
    supervision_summary_text: str | None = None
    research_notes_text: str | None = None
    model_used: str | None = None
    prompt_version: str | None = None
    complexity_score: int | None = None
    validated_by_practitioner: bool = False
    validated_at: datetime | None = None
    practitioner_corrections: dict | list | None = None
    client_visible: bool = False
    record_status: RecordStatus = RecordStatus.active
    data_sensitivity_class: DataSensitivityClass = DataSensitivityClass.high
    retention_class: RetentionClass = RetentionClass.standard


class SessionNoteRead(TimestampedReadSchema):
    id: str
    session_id: str
    client_id: str
    note_sequence_number: int
    summary_text: str
    observations_text: str | None = None
    follow_up_actions_text: str | None = None
    next_session_focus_text: str | None = None
    coeur_summary_text: str | None = None
    corps_summary_text: str | None = None
    esprit_summary_text: str | None = None
    etre_summary_text: str | None = None
    immediate_context_text: str | None = None
    context_factors_json: dict | list | None = None
    context_hypotheses_json: dict | list | None = None
    identified_tensions_json: dict | list | None = None
    vigilance_level_code: RiskLevelCode
    next_step_type_code: AnalysisNextStepCode | None = None
    client_facing_summary_text: str | None = None
    supervision_summary_text: str | None = None
    research_notes_text: str | None = None
    model_used: str | None = None
    prompt_version: str | None = None
    complexity_score: int | None = None
    validated_by_practitioner: bool
    validated_at: datetime | None = None
    practitioner_corrections: dict | list | None = None
    client_visible: bool
    record_status: RecordStatus
    data_sensitivity_class: DataSensitivityClass
    retention_class: RetentionClass


class SessionNoteValidationPayload(MerlinSchema):
    validated: bool
    corrections: dict | None = None

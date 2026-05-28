from datetime import datetime

from app.models.enums import (
    AuthoredByCode,
    DataSensitivityClass,
    EventTypeCode,
    LifeStageCode,
    RecordStatus,
)
from app.schemas.common import MerlinSchema


class ClientLifeEventCreate(MerlinSchema):
    client_id: str
    parent_event_id: str | None = None
    era_tag: str | None = None
    first_mentioned_session_id: str | None = None
    event_year_approx: int | None = None
    client_age_at_event: int | None = None
    life_stage: LifeStageCode | None = None
    family_role: str | None = None
    gender_lived_then: str | None = None
    event_type: EventTypeCode = EventTypeCode.autre
    title: str
    is_intergenerational: bool = False
    narrative_then: str | None = None
    narrative_now: str | None = None
    authored_by: AuthoredByCode = AuthoredByCode.practitioner
    record_status: RecordStatus = RecordStatus.active
    data_sensitivity_class: DataSensitivityClass = DataSensitivityClass.restricted


class ClientLifeEventUpdate(MerlinSchema):
    parent_event_id: str | None = None
    era_tag: str | None = None
    first_mentioned_session_id: str | None = None
    event_year_approx: int | None = None
    client_age_at_event: int | None = None
    life_stage: LifeStageCode | None = None
    family_role: str | None = None
    gender_lived_then: str | None = None
    event_type: EventTypeCode | None = None
    title: str | None = None
    is_intergenerational: bool | None = None
    narrative_then: str | None = None
    narrative_now: str | None = None
    record_status: RecordStatus | None = None


class ClientLifeEventRead(MerlinSchema):
    id: str
    client_id: str
    parent_event_id: str | None = None
    era_tag: str | None = None
    first_mentioned_session_id: str | None = None
    event_year_approx: int | None = None
    client_age_at_event: int | None = None
    life_stage: LifeStageCode | None = None
    family_role: str | None = None
    gender_lived_then: str | None = None
    event_type: EventTypeCode
    title: str
    is_intergenerational: bool
    narrative_then: str | None = None
    narrative_now: str | None = None
    authored_by: AuthoredByCode
    record_status: RecordStatus
    data_sensitivity_class: DataSensitivityClass
    created_at: datetime
    updated_at: datetime

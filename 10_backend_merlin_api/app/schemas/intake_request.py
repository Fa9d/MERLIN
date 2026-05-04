from app.models.enums import NeedCode, RecordStatus, RequestChannelCode, RequestForCode, RiskLevelCode
from app.schemas.common import MerlinSchema, TimestampedReadSchema


class IntakeRequestCreate(MerlinSchema):
    client_id: str
    request_channel_code: RequestChannelCode
    request_for_code: RequestForCode
    primary_need_code: NeedCode
    perceived_urgency_code: RiskLevelCode = RiskLevelCode.non_urgent
    support_already_in_place: bool = False
    requested_outcome_text: str | None = None
    entry_summary_text: str | None = None
    referential_version: str = "v1"
    record_status: RecordStatus = RecordStatus.active


class IntakeRequestRead(TimestampedReadSchema):
    id: str
    client_id: str
    request_channel_code: RequestChannelCode
    request_for_code: RequestForCode
    primary_need_code: NeedCode
    perceived_urgency_code: RiskLevelCode
    support_already_in_place: bool
    requested_outcome_text: str | None = None
    entry_summary_text: str | None = None
    referential_version: str
    record_status: RecordStatus

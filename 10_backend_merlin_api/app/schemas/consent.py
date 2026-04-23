from datetime import datetime

from app.models.enums import (
    ConsentTypeCode,
    GrantedByActorCode,
    RecordStatus,
    RevocationScopeCode,
)
from app.schemas.common import MerlinSchema, TimestampedReadSchema


class ConsentCreate(MerlinSchema):
    client_id: str
    session_id: str | None = None
    consent_type_code: ConsentTypeCode
    consent_value: bool
    consent_version_code: str = "v1"
    granted_by_actor_code: GrantedByActorCode
    granted_at: datetime | None = None
    revoked_at: datetime | None = None
    revocation_scope_code: RevocationScopeCode | None = None
    notes: str | None = None
    record_status: RecordStatus = RecordStatus.active


class ConsentRead(TimestampedReadSchema):
    id: str
    client_id: str
    session_id: str | None = None
    consent_type_code: ConsentTypeCode
    consent_value: bool
    consent_version_code: str
    granted_by_actor_code: GrantedByActorCode
    granted_at: datetime
    revoked_at: datetime | None = None
    revocation_scope_code: RevocationScopeCode | None = None
    notes: str | None = None
    record_status: RecordStatus

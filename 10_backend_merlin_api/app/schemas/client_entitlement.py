from app.models.enums import ClientEntitlementTypeCode, RecordStatus
from app.schemas.common import TimestampedReadSchema


class ClientEntitlementRead(TimestampedReadSchema):
    id: str
    client_id: str
    payment_order_id: str | None = None
    entitlement_type_code: ClientEntitlementTypeCode
    quantity_total: int
    quantity_remaining: int
    starts_at: TimestampedReadSchema.model_fields["created_at"].annotation
    expires_at: TimestampedReadSchema.model_fields["created_at"].annotation | None = None
    record_status: RecordStatus
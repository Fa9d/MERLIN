from app.models.enums import SessionModeCode
from app.schemas.common import MerlinSchema


class StripeAudioAsyncCheckoutCreate(MerlinSchema):
    client_id: str
    operator_user_id: str
    intake_request_id: str | None = None
    session_mode_code: SessionModeCode = SessionModeCode.follow_up
    success_url: str | None = None
    cancel_url: str | None = None


class StripeCheckoutSessionRead(MerlinSchema):
    checkout_session_id: str
    checkout_url: str
    amount_cents: int
    currency: str


class StripeWebhookAck(MerlinSchema):
    status: str
    session_id: str | None = None

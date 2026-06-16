from pydantic import field_validator, model_validator

from app.models.enums import (
    ClientEntitlementTypeCode,
    PaymentFulfillmentModeCode,
    PaymentProductKindCode,
    SessionModeCode,
)
from app.schemas.common import MerlinSchema


class PaymentCheckoutCreate(MerlinSchema):
    client_id: str
    operator_user_id: str | None = None
    intake_request_id: str | None = None
    slot_id: str | None = None
    product_code: str
    product_label: str
    product_kind_code: PaymentProductKindCode = PaymentProductKindCode.custom
    fulfillment_mode_code: PaymentFulfillmentModeCode = (
        PaymentFulfillmentModeCode.grant_entitlement_only
    )
    amount_cents: int
    currency: str = "cad"
    entitlement_type_code: ClientEntitlementTypeCode | None = None
    entitlement_quantity: int | None = None
    success_url: str | None = None
    cancel_url: str | None = None

    @field_validator("product_code", "product_label")
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Ce champ est requis.")
        return cleaned

    @field_validator("amount_cents")
    @classmethod
    def validate_amount(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("amount_cents doit etre superieur a 0.")
        return value

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        cleaned = value.strip().lower()
        if len(cleaned) != 3:
            raise ValueError("currency doit etre un code ISO a 3 lettres.")
        return cleaned

    @model_validator(mode="after")
    def validate_entitlement_payload(self) -> "PaymentCheckoutCreate":
        requires_entitlement = self.fulfillment_mode_code in {
            PaymentFulfillmentModeCode.grant_entitlement_only,
            PaymentFulfillmentModeCode.grant_entitlement_and_create_audio_async_session,
        }
        if requires_entitlement:
            if self.entitlement_type_code is None:
                raise ValueError("entitlement_type_code est requis pour ce mode de fulfillment.")
            if self.entitlement_quantity is None or self.entitlement_quantity <= 0:
                raise ValueError("entitlement_quantity doit etre superieur a 0.")
        return self


class StripeAudioAsyncCheckoutCreate(MerlinSchema):
    client_id: str
    operator_user_id: str
    intake_request_id: str | None = None
    session_mode_code: SessionModeCode = SessionModeCode.follow_up
    success_url: str | None = None
    cancel_url: str | None = None


class SoloRecordingCheckoutCreate(MerlinSchema):
    """Achat d'un crédit d'enregistrement solo — client résolu côté serveur."""
    success_url: str | None = None
    cancel_url: str | None = None


class StripeCheckoutSessionRead(MerlinSchema):
    order_id: str
    product_code: str
    checkout_session_id: str
    checkout_url: str
    amount_cents: int
    currency: str


class StripeWebhookAck(MerlinSchema):
    status: str
    order_id: str | None = None
    entitlement_id: str | None = None
    session_id: str | None = None


class InteracEtransferCreate(MerlinSchema):
    client_id: str
    operator_user_id: str | None = None
    intake_request_id: str | None = None
    slot_id: str | None = None
    product_code: str
    product_label: str
    product_kind_code: PaymentProductKindCode = PaymentProductKindCode.custom
    fulfillment_mode_code: PaymentFulfillmentModeCode = (
        PaymentFulfillmentModeCode.grant_entitlement_only
    )
    amount_cents: int
    currency: str = "cad"
    entitlement_type_code: ClientEntitlementTypeCode | None = None
    entitlement_quantity: int | None = None

    @field_validator("product_code", "product_label")
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Ce champ est requis.")
        return cleaned

    @field_validator("amount_cents")
    @classmethod
    def validate_amount(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("amount_cents doit etre superieur a 0.")
        return value

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        cleaned = value.strip().lower()
        if len(cleaned) != 3:
            raise ValueError("currency doit etre un code ISO a 3 lettres.")
        return cleaned

    @model_validator(mode="after")
    def validate_entitlement_payload(self) -> "InteracEtransferCreate":
        requires_entitlement = self.fulfillment_mode_code in {
            PaymentFulfillmentModeCode.grant_entitlement_only,
            PaymentFulfillmentModeCode.grant_entitlement_and_create_audio_async_session,
        }
        if requires_entitlement:
            if self.entitlement_type_code is None:
                raise ValueError("entitlement_type_code est requis pour ce mode de fulfillment.")
            if self.entitlement_quantity is None or self.entitlement_quantity <= 0:
                raise ValueError("entitlement_quantity doit etre superieur a 0.")
        return self


class InteracEtransferRequestRead(MerlinSchema):
    order_id: str
    status: str
    amount_cents: int
    currency: str
    recipient_name: str
    recipient_email: str
    transfer_reference: str
    instructions_text: str
    instructions_emailed: bool


class ManualPaymentAck(MerlinSchema):
    status: str
    order_id: str
    entitlement_id: str | None = None
    session_id: str | None = None

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.enums import (
    ClientEntitlementTypeCode,
    PaymentFulfillmentModeCode,
    PaymentOrderStatusCode,
    PaymentProductKindCode,
    PaymentProviderCode,
)


class PaymentOrder(Base):
    __tablename__ = "payment_orders"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    client_id: Mapped[str] = mapped_column(
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    operator_user_id: Mapped[str | None] = mapped_column(
        ForeignKey("app_users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    intake_request_id: Mapped[str | None] = mapped_column(
        ForeignKey("intake_requests.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    provider_code: Mapped[PaymentProviderCode] = mapped_column(
        Enum(PaymentProviderCode, native_enum=False),
        nullable=False,
        default=PaymentProviderCode.stripe,
    )
    product_code: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    product_label: Mapped[str] = mapped_column(String(160), nullable=False)
    product_kind_code: Mapped[PaymentProductKindCode] = mapped_column(
        Enum(PaymentProductKindCode, native_enum=False),
        nullable=False,
    )
    fulfillment_mode_code: Mapped[PaymentFulfillmentModeCode] = mapped_column(
        Enum(PaymentFulfillmentModeCode, native_enum=False),
        nullable=False,
    )
    entitlement_type_code: Mapped[ClientEntitlementTypeCode | None] = mapped_column(
        Enum(ClientEntitlementTypeCode, native_enum=False),
        nullable=True,
    )
    entitlement_quantity: Mapped[int | None] = mapped_column(Integer, nullable=True)
    amount_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str] = mapped_column(String(8), nullable=False, default="cad")
    status_code: Mapped[PaymentOrderStatusCode] = mapped_column(
        Enum(PaymentOrderStatusCode, native_enum=False),
        nullable=False,
        default=PaymentOrderStatusCode.pending,
    )
    provider_checkout_session_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        unique=True,
        index=True,
    )
    provider_payment_intent_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True,
    )
    metadata_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    fulfilled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
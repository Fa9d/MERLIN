"""add payment orders and client entitlements

Revision ID: 20260518_0025
Revises: 20260513_0024
Create Date: 2026-05-18
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260518_0025"
down_revision: Union[str, Sequence[str], None] = "20260513_0024"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "payment_orders",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("client_id", sa.String(length=36), nullable=False),
        sa.Column("operator_user_id", sa.String(length=36), nullable=True),
        sa.Column("intake_request_id", sa.String(length=36), nullable=True),
        sa.Column("provider_code", sa.Enum("stripe", "interac_terminal", "interac_etransfer", name="paymentprovidercode"), nullable=False),
        sa.Column("product_code", sa.String(length=64), nullable=False),
        sa.Column("product_label", sa.String(length=160), nullable=False),
        sa.Column("product_kind_code", sa.Enum("session_intake", "session_follow_up", "journal_days_pack", "audio_async_follow_up", "custom", name="paymentproductkindcode"), nullable=False),
        sa.Column("fulfillment_mode_code", sa.Enum("grant_entitlement_only", "grant_entitlement_and_create_audio_async_session", name="paymentfulfillmentmodecode"), nullable=False),
        sa.Column("entitlement_type_code", sa.Enum("intake_session_credit", "follow_up_session_credit", "journal_day", name="cliententitlementtypecode"), nullable=True),
        sa.Column("entitlement_quantity", sa.Integer(), nullable=True),
        sa.Column("amount_cents", sa.Integer(), nullable=False),
        sa.Column("currency", sa.String(length=8), nullable=False),
        sa.Column("status_code", sa.Enum("pending", "paid", "failed", "cancelled", "refunded", name="paymentorderstatuscode"), nullable=False),
        sa.Column("provider_checkout_session_id", sa.String(length=255), nullable=True),
        sa.Column("provider_payment_intent_id", sa.String(length=255), nullable=True),
        sa.Column("metadata_json", sa.Text(), nullable=True),
        sa.Column("paid_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("fulfilled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["client_id"], ["clients.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["intake_request_id"], ["intake_requests.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["operator_user_id"], ["app_users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("provider_checkout_session_id"),
    )
    op.create_index("ix_payment_orders_client_id", "payment_orders", ["client_id"])
    op.create_index("ix_payment_orders_intake_request_id", "payment_orders", ["intake_request_id"])
    op.create_index("ix_payment_orders_operator_user_id", "payment_orders", ["operator_user_id"])
    op.create_index("ix_payment_orders_product_code", "payment_orders", ["product_code"])
    op.create_index("ix_payment_orders_provider_checkout_session_id", "payment_orders", ["provider_checkout_session_id"])
    op.create_index("ix_payment_orders_provider_payment_intent_id", "payment_orders", ["provider_payment_intent_id"])

    op.create_table(
        "client_entitlements",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("client_id", sa.String(length=36), nullable=False),
        sa.Column("payment_order_id", sa.String(length=36), nullable=True),
        sa.Column("entitlement_type_code", sa.Enum("intake_session_credit", "follow_up_session_credit", "journal_day", name="cliententitlementtypecode"), nullable=False),
        sa.Column("quantity_total", sa.Integer(), nullable=False),
        sa.Column("quantity_remaining", sa.Integer(), nullable=False),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("record_status", sa.Enum("draft", "active", "validated", "closed", "deprecated", "archived", name="recordstatus"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["client_id"], ["clients.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["payment_order_id"], ["payment_orders.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("payment_order_id"),
    )
    op.create_index("ix_client_entitlements_client_id", "client_entitlements", ["client_id"])
    op.create_index("ix_client_entitlements_entitlement_type_code", "client_entitlements", ["entitlement_type_code"])
    op.create_index("ix_client_entitlements_payment_order_id", "client_entitlements", ["payment_order_id"])


def downgrade() -> None:
    op.drop_index("ix_client_entitlements_payment_order_id", table_name="client_entitlements")
    op.drop_index("ix_client_entitlements_entitlement_type_code", table_name="client_entitlements")
    op.drop_index("ix_client_entitlements_client_id", table_name="client_entitlements")
    op.drop_table("client_entitlements")

    op.drop_index("ix_payment_orders_provider_payment_intent_id", table_name="payment_orders")
    op.drop_index("ix_payment_orders_provider_checkout_session_id", table_name="payment_orders")
    op.drop_index("ix_payment_orders_product_code", table_name="payment_orders")
    op.drop_index("ix_payment_orders_operator_user_id", table_name="payment_orders")
    op.drop_index("ix_payment_orders_intake_request_id", table_name="payment_orders")
    op.drop_index("ix_payment_orders_client_id", table_name="payment_orders")
    op.drop_table("payment_orders")
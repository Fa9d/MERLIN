"""Ventilation séance : frais plateforme IVIA + part praticien sur la commande.

Revision ID: 20260616_0035
Revises: 20260616_0034
Create Date: 2026-06-16
"""

from alembic import op
import sqlalchemy as sa

revision = "20260616_0035"
down_revision = "20260616_0034"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("payment_orders", sa.Column("platform_fee_cents", sa.Integer(), nullable=True))
    op.add_column("payment_orders", sa.Column("practitioner_share_cents", sa.Integer(), nullable=True))
    op.add_column("payment_orders", sa.Column("practitioner_user_id", sa.String(length=36), nullable=True))


def downgrade() -> None:
    op.drop_column("payment_orders", "practitioner_user_id")
    op.drop_column("payment_orders", "practitioner_share_cents")
    op.drop_column("payment_orders", "platform_fee_cents")

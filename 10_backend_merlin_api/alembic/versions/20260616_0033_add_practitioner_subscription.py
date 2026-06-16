"""Abonnement praticien — suivi interne (statut + date), sans prélèvement auto.

Revision ID: 20260616_0033
Revises: 20260616_0032
Create Date: 2026-06-16
"""

from alembic import op
import sqlalchemy as sa

revision = "20260616_0033"
down_revision = "20260616_0032"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "app_users",
        sa.Column("subscription_status", sa.String(length=16), nullable=False, server_default="inactive"),
    )
    op.add_column(
        "app_users",
        sa.Column("subscription_since", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("app_users", "subscription_since")
    op.drop_column("app_users", "subscription_status")

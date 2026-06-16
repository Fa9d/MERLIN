"""Tarifs de séance fixés par le praticien (30 min / 1 h).

Revision ID: 20260616_0034
Revises: 20260616_0033
Create Date: 2026-06-16
"""

from alembic import op
import sqlalchemy as sa

revision = "20260616_0034"
down_revision = "20260616_0033"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("app_users", sa.Column("session_price_30min_cents", sa.Integer(), nullable=True))
    op.add_column("app_users", sa.Column("session_price_60min_cents", sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column("app_users", "session_price_60min_cents")
    op.drop_column("app_users", "session_price_30min_cents")

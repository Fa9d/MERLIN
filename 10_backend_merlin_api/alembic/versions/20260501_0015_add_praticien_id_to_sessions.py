"""add praticien_id to sessions

Revision ID: 20260501_0015
Revises: 20260501_0014
Create Date: 2026-05-01
"""

import sqlalchemy as sa
from alembic import op

revision = "20260501_0015"
down_revision = "20260501_0014"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "sessions",
        sa.Column("praticien_id", sa.String(36), sa.ForeignKey("app_users.id"), nullable=True, index=True),
    )


def downgrade() -> None:
    op.drop_column("sessions", "praticien_id")

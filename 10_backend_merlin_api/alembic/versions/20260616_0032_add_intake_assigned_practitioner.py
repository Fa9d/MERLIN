"""Assignation d'une demande d'entrée à un praticien nommé.

Revision ID: 20260616_0032
Revises: 20260616_0031
Create Date: 2026-06-16
"""

from alembic import op
import sqlalchemy as sa

revision = "20260616_0032"
down_revision = "20260616_0031"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "intake_requests",
        sa.Column("assigned_practitioner_id", sa.String(length=36), nullable=True),
    )
    op.create_index(
        "ix_intake_requests_assigned_practitioner_id",
        "intake_requests",
        ["assigned_practitioner_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_intake_requests_assigned_practitioner_id", table_name="intake_requests")
    op.drop_column("intake_requests", "assigned_practitioner_id")

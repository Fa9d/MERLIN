"""add practitioner validation timestamp

Revision ID: 20260422_0008
Revises: 20260422_0007
Create Date: 2026-04-22 18:10:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260422_0008"
down_revision: Union[str, Sequence[str], None] = "20260422_0007"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("session_notes", sa.Column("validated_at", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column("session_notes", "validated_at")

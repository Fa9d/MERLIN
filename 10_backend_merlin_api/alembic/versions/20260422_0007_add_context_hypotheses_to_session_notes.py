"""add context hypotheses to session notes

Revision ID: 20260422_0007
Revises: 20260422_0006
Create Date: 2026-04-22 17:10:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260422_0007"
down_revision: Union[str, Sequence[str], None] = "20260422_0006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("session_notes", sa.Column("context_hypotheses_json", sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column("session_notes", "context_hypotheses_json")

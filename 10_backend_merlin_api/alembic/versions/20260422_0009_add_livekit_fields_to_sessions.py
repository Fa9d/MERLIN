"""add livekit fields to sessions

Revision ID: 20260422_0009
Revises: 20260422_0008
Create Date: 2026-04-22 19:10:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260422_0009"
down_revision: Union[str, Sequence[str], None] = "20260422_0008"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("sessions", sa.Column("room_name", sa.String(length=160), nullable=True))
    op.add_column("sessions", sa.Column("room_sid", sa.String(length=160), nullable=True))
    op.add_column("sessions", sa.Column("egress_id", sa.String(length=160), nullable=True))
    op.add_column("sessions", sa.Column("audio_file_path", sa.String(length=512), nullable=True))


def downgrade() -> None:
    op.drop_column("sessions", "audio_file_path")
    op.drop_column("sessions", "egress_id")
    op.drop_column("sessions", "room_sid")
    op.drop_column("sessions", "room_name")

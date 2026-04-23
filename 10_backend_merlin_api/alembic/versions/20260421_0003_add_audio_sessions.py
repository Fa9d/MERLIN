"""add audio sessions

Revision ID: 20260421_0003
Revises: 20260421_0002
Create Date: 2026-04-21 19:10:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260421_0003"
down_revision: Union[str, Sequence[str], None] = "20260421_0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "audio_sessions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("session_id", sa.String(length=36), nullable=False),
        sa.Column(
            "provider_code",
            sa.Enum("livekit", "manual", name="audioprovidercode", native_enum=False),
            nullable=False,
        ),
        sa.Column(
            "audio_session_status_code",
            sa.Enum(
                "provisioned",
                "active",
                "closed",
                "failed",
                name="audiosessionstatuscode",
                native_enum=False,
            ),
            nullable=False,
        ),
        sa.Column("room_name", sa.String(length=160), nullable=False),
        sa.Column("provider_room_url", sa.String(length=255), nullable=True),
        sa.Column("recording_enabled", sa.Boolean(), nullable=False),
        sa.Column("operator_participant_identity", sa.String(length=120), nullable=False),
        sa.Column("client_participant_identity", sa.String(length=120), nullable=False),
        sa.Column("practitioner_participant_identity", sa.String(length=120), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["sessions.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("room_name"),
    )
    op.create_index(op.f("ix_audio_sessions_session_id"), "audio_sessions", ["session_id"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_audio_sessions_session_id"), table_name="audio_sessions")
    op.drop_table("audio_sessions")

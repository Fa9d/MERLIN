"""add audio recordings

Revision ID: 20260421_0004
Revises: 20260421_0003
Create Date: 2026-04-21 21:15:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260421_0004"
down_revision: Union[str, Sequence[str], None] = "20260421_0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "audio_recordings",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("audio_session_id", sa.String(length=36), nullable=False),
        sa.Column(
            "provider_code",
            sa.Enum("livekit", "manual", name="audioprovidercode", native_enum=False),
            nullable=False,
        ),
        sa.Column(
            "audio_recording_status_code",
            sa.Enum(
                "starting",
                "recording",
                "ready",
                "failed",
                name="audiorecordingstatuscode",
                native_enum=False,
            ),
            nullable=False,
        ),
        sa.Column("provider_recording_id", sa.String(length=160), nullable=True),
        sa.Column("output_location", sa.String(length=512), nullable=True),
        sa.Column("failure_reason", sa.Text(), nullable=True),
        sa.Column("requested_by_user_id", sa.String(length=64), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["audio_session_id"], ["audio_sessions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_audio_recordings_audio_session_id"),
        "audio_recordings",
        ["audio_session_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_audio_recordings_provider_recording_id"),
        "audio_recordings",
        ["provider_recording_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_audio_recordings_provider_recording_id"), table_name="audio_recordings")
    op.drop_index(op.f("ix_audio_recordings_audio_session_id"), table_name="audio_recordings")
    op.drop_table("audio_recordings")

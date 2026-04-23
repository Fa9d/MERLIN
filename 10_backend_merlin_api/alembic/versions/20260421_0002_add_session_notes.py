"""add session notes

Revision ID: 20260421_0002
Revises: 20260421_0001
Create Date: 2026-04-21 18:25:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260421_0002"
down_revision: Union[str, Sequence[str], None] = "20260421_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "session_notes",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("session_id", sa.String(length=36), nullable=False),
        sa.Column("client_id", sa.String(length=36), nullable=False),
        sa.Column("note_sequence_number", sa.Integer(), nullable=False),
        sa.Column("summary_text", sa.Text(), nullable=False),
        sa.Column("observations_text", sa.Text(), nullable=True),
        sa.Column("follow_up_actions_text", sa.Text(), nullable=True),
        sa.Column("next_session_focus_text", sa.Text(), nullable=True),
        sa.Column("client_visible", sa.Boolean(), nullable=False),
        sa.Column(
            "record_status",
            sa.Enum(
                "draft",
                "active",
                "validated",
                "closed",
                "deprecated",
                "archived",
                name="recordstatus",
                native_enum=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "data_sensitivity_class",
            sa.Enum(
                "low",
                "moderate",
                "high",
                "restricted",
                name="datasensitivityclass",
                native_enum=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "retention_class",
            sa.Enum(
                "ephemeral",
                "short_term",
                "standard",
                "extended",
                "archival",
                name="retentionclass",
                native_enum=False,
            ),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["client_id"], ["clients.id"]),
        sa.ForeignKeyConstraint(["session_id"], ["sessions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_session_notes_client_id"), "session_notes", ["client_id"], unique=False)
    op.create_index(op.f("ix_session_notes_session_id"), "session_notes", ["session_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_session_notes_session_id"), table_name="session_notes")
    op.drop_index(op.f("ix_session_notes_client_id"), table_name="session_notes")
    op.drop_table("session_notes")

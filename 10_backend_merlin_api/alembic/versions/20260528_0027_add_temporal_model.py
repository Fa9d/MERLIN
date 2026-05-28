"""add temporal model (era_context, client_life_events, client_journal_entries, session_temporal_anchors)

Revision ID: 20260528_0027
Revises: 20260518_0026
Create Date: 2026-05-28
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "20260528_0027"
down_revision: Union[str, None] = "20260518_0026"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ------------------------------------------------------------------
    # 1. era_contexts — référentiel sociétal (pas de FK sortante)
    # ------------------------------------------------------------------
    op.create_table(
        "era_contexts",
        sa.Column("tag", sa.String(80), primary_key=True),
        sa.Column("label", sa.String(255), nullable=False),
        sa.Column("period_start", sa.Integer(), nullable=False),
        sa.Column("period_end", sa.Integer(), nullable=True),
        sa.Column("territory_code", sa.String(16), nullable=False, server_default="QC"),
        sa.Column("data", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )

    # ------------------------------------------------------------------
    # 2. Colonnes sur clients
    # ------------------------------------------------------------------
    op.add_column("clients", sa.Column("birth_year", sa.Integer(), nullable=True))
    op.add_column("clients", sa.Column("gender_identity", sa.String(64), nullable=True))

    # ------------------------------------------------------------------
    # 3. client_life_events
    # ------------------------------------------------------------------
    op.create_table(
        "client_life_events",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "client_id",
            sa.String(36),
            sa.ForeignKey("clients.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "parent_event_id",
            sa.String(36),
            sa.ForeignKey("client_life_events.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "era_tag",
            sa.String(80),
            sa.ForeignKey("era_contexts.tag", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "first_mentioned_session_id",
            sa.String(36),
            sa.ForeignKey("sessions.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("event_year_approx", sa.Integer(), nullable=True),
        sa.Column("client_age_at_event", sa.Integer(), nullable=True),
        sa.Column("life_stage", sa.String(32), nullable=True),
        sa.Column("family_role", sa.String(64), nullable=True),
        sa.Column("gender_lived_then", sa.String(64), nullable=True),
        sa.Column("event_type", sa.String(64), nullable=False, server_default="autre"),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("is_intergenerational", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("narrative_then", sa.Text(), nullable=True),
        sa.Column("narrative_now", sa.Text(), nullable=True),
        sa.Column("authored_by", sa.String(32), nullable=False, server_default="practitioner"),
        sa.Column("record_status", sa.String(20), nullable=False, server_default="active"),
        sa.Column("data_sensitivity_class", sa.String(20), nullable=False, server_default="restricted"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )
    op.create_index("ix_client_life_events_client_id", "client_life_events", ["client_id"])
    op.create_index("ix_client_life_events_era_tag", "client_life_events", ["era_tag"])
    op.create_index("ix_client_life_events_session_id", "client_life_events", ["first_mentioned_session_id"])

    # ------------------------------------------------------------------
    # 4. client_journal_entries
    # ------------------------------------------------------------------
    op.create_table(
        "client_journal_entries",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "client_id",
            sa.String(36),
            sa.ForeignKey("clients.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "linked_event_id",
            sa.String(36),
            sa.ForeignKey("client_life_events.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("entry_type", sa.String(32), nullable=False, server_default="aujourd_hui"),
        sa.Column("body_text", sa.Text(), nullable=False),
        sa.Column("emotional_tone", sa.String(64), nullable=True),
        sa.Column("event_year_ref", sa.Integer(), nullable=True),
        sa.Column(
            "written_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column("record_status", sa.String(20), nullable=False, server_default="active"),
        sa.Column("data_sensitivity_class", sa.String(20), nullable=False, server_default="restricted"),
        sa.Column("retention_class", sa.String(20), nullable=False, server_default="extended"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )
    op.create_index("ix_client_journal_entries_client_id", "client_journal_entries", ["client_id"])

    # ------------------------------------------------------------------
    # 5. session_temporal_anchors
    # ------------------------------------------------------------------
    op.create_table(
        "session_temporal_anchors",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "session_id",
            sa.String(36),
            sa.ForeignKey("sessions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "session_note_id",
            sa.String(36),
            sa.ForeignKey("session_notes.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "client_id",
            sa.String(36),
            sa.ForeignKey("clients.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "life_event_id",
            sa.String(36),
            sa.ForeignKey("client_life_events.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("verbatim_fragment", sa.Text(), nullable=True),
        sa.Column("said_at_offset_sec", sa.Integer(), nullable=True),
        sa.Column("event_year_approx", sa.Integer(), nullable=True),
        sa.Column("client_age_ref", sa.Integer(), nullable=True),
        sa.Column("gap_years", sa.Integer(), nullable=True),
        sa.Column("interpretation_note", sa.Text(), nullable=True),
        sa.Column("emotional_charge", sa.String(20), nullable=True),
        sa.Column("is_silence_marker", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("record_status", sa.String(20), nullable=False, server_default="active"),
        sa.Column("data_sensitivity_class", sa.String(20), nullable=False, server_default="restricted"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )
    op.create_index(
        "ix_session_temporal_anchors_session_id",
        "session_temporal_anchors",
        ["session_id"],
    )
    op.create_index(
        "ix_session_temporal_anchors_client_id",
        "session_temporal_anchors",
        ["client_id"],
    )


def downgrade() -> None:
    op.drop_table("session_temporal_anchors")
    op.drop_table("client_journal_entries")
    op.drop_table("client_life_events")
    op.drop_column("clients", "gender_identity")
    op.drop_column("clients", "birth_year")
    op.drop_table("era_contexts")

"""add cercle axes to session notes

Revision ID: 20260422_0005
Revises: 20260421_0004
Create Date: 2026-04-22 11:40:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260422_0005"
down_revision: Union[str, Sequence[str], None] = "20260421_0004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("session_notes", sa.Column("coeur_summary_text", sa.Text(), nullable=True))
    op.add_column("session_notes", sa.Column("corps_summary_text", sa.Text(), nullable=True))
    op.add_column("session_notes", sa.Column("esprit_summary_text", sa.Text(), nullable=True))
    op.add_column("session_notes", sa.Column("etre_summary_text", sa.Text(), nullable=True))
    op.add_column("session_notes", sa.Column("immediate_context_text", sa.Text(), nullable=True))
    op.add_column("session_notes", sa.Column("context_factors_json", sa.JSON(), nullable=True))
    op.add_column("session_notes", sa.Column("identified_tensions_json", sa.JSON(), nullable=True))
    op.add_column(
        "session_notes",
        sa.Column(
            "vigilance_level_code",
            sa.Enum(
                "non_urgent",
                "watch",
                "priority",
                "urgent",
                name="perceivedurgencycode",
                native_enum=False,
            ),
            nullable=False,
            server_default="non_urgent",
        ),
    )
    op.add_column(
        "session_notes",
        sa.Column(
            "next_step_type_code",
            sa.Enum(
                "continue_to_structure",
                "clarify_major_point",
                "stabilize_rhythm_and_load",
                "mobilize_relational_resource",
                "orient_to_appropriate_service",
                "propose_follow_up",
                "escalate_immediate_relay",
                name="analysisnextstepcode",
                native_enum=False,
            ),
            nullable=True,
        ),
    )
    op.add_column("session_notes", sa.Column("client_facing_summary_text", sa.Text(), nullable=True))
    op.add_column("session_notes", sa.Column("supervision_summary_text", sa.Text(), nullable=True))
    op.add_column("session_notes", sa.Column("research_notes_text", sa.Text(), nullable=True))
    op.add_column("session_notes", sa.Column("model_used", sa.String(length=128), nullable=True))
    op.add_column("session_notes", sa.Column("prompt_version", sa.String(length=64), nullable=True))
    op.add_column("session_notes", sa.Column("complexity_score", sa.Integer(), nullable=True))
    op.add_column(
        "session_notes",
        sa.Column(
            "validated_by_practitioner",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )
    op.add_column("session_notes", sa.Column("practitioner_corrections", sa.JSON(), nullable=True))
    op.alter_column("session_notes", "vigilance_level_code", server_default=None)
    op.alter_column("session_notes", "validated_by_practitioner", server_default=None)


def downgrade() -> None:
    op.drop_column("session_notes", "practitioner_corrections")
    op.drop_column("session_notes", "validated_by_practitioner")
    op.drop_column("session_notes", "complexity_score")
    op.drop_column("session_notes", "prompt_version")
    op.drop_column("session_notes", "model_used")
    op.drop_column("session_notes", "research_notes_text")
    op.drop_column("session_notes", "supervision_summary_text")
    op.drop_column("session_notes", "client_facing_summary_text")
    op.drop_column("session_notes", "next_step_type_code")
    op.drop_column("session_notes", "vigilance_level_code")
    op.drop_column("session_notes", "identified_tensions_json")
    op.drop_column("session_notes", "context_factors_json")
    op.drop_column("session_notes", "immediate_context_text")
    op.drop_column("session_notes", "etre_summary_text")
    op.drop_column("session_notes", "esprit_summary_text")
    op.drop_column("session_notes", "corps_summary_text")
    op.drop_column("session_notes", "coeur_summary_text")

"""add derived documents

Revision ID: 20260424_0010
Revises: 20260422_0009
Create Date: 2026-04-24 09:20:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260424_0010"
down_revision: Union[str, Sequence[str], None] = "20260422_0009"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "derived_documents",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("client_id", sa.String(length=36), nullable=False),
        sa.Column("session_id", sa.String(length=36), nullable=False),
        sa.Column("source_note_id", sa.String(length=36), nullable=False),
        sa.Column("document_kind_code", sa.String(length=64), nullable=False),
        sa.Column("audience_code", sa.String(length=32), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("body_text", sa.Text(), nullable=False),
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
        sa.ForeignKeyConstraint(["source_note_id"], ["session_notes.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_derived_documents_client_id"),
        "derived_documents",
        ["client_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_derived_documents_session_id"),
        "derived_documents",
        ["session_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_derived_documents_source_note_id"),
        "derived_documents",
        ["source_note_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_derived_documents_source_note_id"), table_name="derived_documents")
    op.drop_index(op.f("ix_derived_documents_session_id"), table_name="derived_documents")
    op.drop_index(op.f("ix_derived_documents_client_id"), table_name="derived_documents")
    op.drop_table("derived_documents")

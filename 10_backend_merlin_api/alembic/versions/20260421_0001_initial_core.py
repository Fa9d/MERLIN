"""initial core

Revision ID: 20260421_0001
Revises:
Create Date: 2026-04-21 16:30:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20260421_0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "app_users",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("display_name", sa.String(length=160), nullable=False),
        sa.Column(
            "role",
            sa.Enum(
                "public_client",
                "operator",
                "supervisor",
                "admin_tech",
                name="approle",
                native_enum=False,
            ),
            nullable=False,
        ),
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
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_app_users_email"), "app_users", ["email"], unique=True)

    op.create_table(
        "clients",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("public_client_code", sa.String(length=16), nullable=False),
        sa.Column("first_name_or_alias", sa.String(length=120), nullable=False),
        sa.Column("last_name", sa.String(length=120), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=40), nullable=True),
        sa.Column("language_code", sa.String(length=16), nullable=False),
        sa.Column("timezone", sa.String(length=64), nullable=False),
        sa.Column("territory_code", sa.String(length=16), nullable=False),
        sa.Column("is_adult_confirmed", sa.Boolean(), nullable=False),
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
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("public_client_code"),
    )

    op.create_table(
        "intake_requests",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("client_id", sa.String(length=36), nullable=False),
        sa.Column("request_channel_code", sa.String(length=32), nullable=False),
        sa.Column(
            "request_for_code",
            sa.Enum("self", "relative", "other", name="requestforcode", native_enum=False),
            nullable=False,
        ),
        sa.Column(
            "primary_need_code",
            sa.Enum(
                "clarification",
                "support",
                "orientation",
                "loneliness",
                "distress",
                "other",
                name="needcode",
                native_enum=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "perceived_urgency_code",
            sa.Enum(
                "non_urgent",
                "watch",
                "priority",
                "urgent",
                name="perceivedurgencycode",
                native_enum=False,
            ),
            nullable=False,
        ),
        sa.Column("support_already_in_place", sa.Boolean(), nullable=False),
        sa.Column("requested_outcome_text", sa.Text(), nullable=True),
        sa.Column("entry_summary_text", sa.Text(), nullable=True),
        sa.Column("referential_version", sa.String(length=32), nullable=False),
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
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["client_id"], ["clients.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_intake_requests_client_id"), "intake_requests", ["client_id"], unique=False)

    op.create_table(
        "sessions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("client_id", sa.String(length=36), nullable=False),
        sa.Column("intake_request_id", sa.String(length=36), nullable=True),
        sa.Column("session_sequence_number", sa.Integer(), nullable=False),
        sa.Column(
            "session_mode_code",
            sa.Enum("standard", "intake", "follow_up", name="sessionmodecode", native_enum=False),
            nullable=False,
        ),
        sa.Column(
            "session_channel_code",
            sa.Enum("phone", "video", "in_person", "async", name="sessionchannelcode", native_enum=False),
            nullable=False,
        ),
        sa.Column("scheduled_start_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("actual_start_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("actual_end_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("duration_minutes", sa.Integer(), nullable=True),
        sa.Column("operator_user_id", sa.String(length=64), nullable=False),
        sa.Column(
            "session_status_code",
            sa.Enum(
                "scheduled",
                "in_progress",
                "completed",
                "cancelled",
                "no_show",
                "escalated",
                name="sessionstatuscode",
                native_enum=False,
            ),
            nullable=False,
        ),
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
        sa.ForeignKeyConstraint(["intake_request_id"], ["intake_requests.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_sessions_client_id"), "sessions", ["client_id"], unique=False)
    op.create_index(op.f("ix_sessions_intake_request_id"), "sessions", ["intake_request_id"], unique=False)

    op.create_table(
        "consents",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("client_id", sa.String(length=36), nullable=False),
        sa.Column("session_id", sa.String(length=36), nullable=True),
        sa.Column(
            "consent_type_code",
            sa.Enum(
                "consent_session",
                "consent_session_note",
                "consent_history",
                "consent_recording",
                "consent_transcription",
                "consent_client_delivery",
                "consent_third_party_transmission",
                name="consenttypecode",
                native_enum=False,
            ),
            nullable=False,
        ),
        sa.Column("consent_value", sa.Boolean(), nullable=False),
        sa.Column("consent_version_code", sa.String(length=32), nullable=False),
        sa.Column(
            "granted_by_actor_code",
            sa.Enum("client", "operator", "system", name="grantedbyactorcode", native_enum=False),
            nullable=False,
        ),
        sa.Column("granted_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "revocation_scope_code",
            sa.Enum(
                "future_only",
                "future_and_pending",
                name="revocationscopecode",
                native_enum=False,
            ),
            nullable=True,
        ),
        sa.Column("notes", sa.Text(), nullable=True),
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
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["client_id"], ["clients.id"]),
        sa.ForeignKeyConstraint(["session_id"], ["sessions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_consents_client_id"), "consents", ["client_id"], unique=False)
    op.create_index(op.f("ix_consents_session_id"), "consents", ["session_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_consents_session_id"), table_name="consents")
    op.drop_index(op.f("ix_consents_client_id"), table_name="consents")
    op.drop_table("consents")
    op.drop_index(op.f("ix_sessions_intake_request_id"), table_name="sessions")
    op.drop_index(op.f("ix_sessions_client_id"), table_name="sessions")
    op.drop_table("sessions")
    op.drop_index(op.f("ix_intake_requests_client_id"), table_name="intake_requests")
    op.drop_table("intake_requests")
    op.drop_table("clients")
    op.drop_index(op.f("ix_app_users_email"), table_name="app_users")
    op.drop_table("app_users")

"""6ᵉ couche de profilage : types jungiens (attitude + 4 fonctions).

Ajoute la table `profile_types_jungian` — même pattern que les 5 couches de 0039 :
append-only versionné, sujet polymorphe (client/praticien), un seul profil COURANT
par sujet (index UNIQUE partiel), posture non-diagnostic (`status` défaut 'hypothese'),
Loi 25 (consentement, sensibilité 'high'). Enums en VARCHAR (native_enum=False côté modèle).

Cadre : 00_DOCTRINE/INDIVIDUATION_cadre_jungien_v0.1.md — repères de compréhension de soi,
jamais un diagnostic ni une étiquette exposée au client.

Revision ID: 20260701_0040
Revises: 20260625_0039
Create Date: 2026-07-01
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text

revision = "20260701_0040"
down_revision = "20260625_0039"
branch_labels = None
depends_on = None


def _common_columns() -> list[sa.Column]:
    """Colonnes communes (miroir de ProfileLayerMixin) — identique à 0039."""
    return [
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("subject_kind", sa.String(length=16), nullable=False),
        sa.Column(
            "client_id", sa.String(length=36),
            sa.ForeignKey("clients.id", ondelete="CASCADE"), nullable=True,
        ),
        sa.Column(
            "practitioner_user_id", sa.String(length=36),
            sa.ForeignKey("app_users.id", ondelete="CASCADE"), nullable=True,
        ),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("is_current", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("assessed_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now()),
        sa.Column("valid_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("source", sa.String(length=32), nullable=False, server_default="self_report"),
        sa.Column("instrument", sa.String(length=64), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="hypothese"),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column(
            "assessed_by_user_id", sa.String(length=36),
            sa.ForeignKey("app_users.id", ondelete="SET NULL"), nullable=True,
        ),
        sa.Column(
            "validated_by_user_id", sa.String(length=36),
            sa.ForeignKey("app_users.id", ondelete="SET NULL"), nullable=True,
        ),
        sa.Column("validated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "consent_id", sa.String(length=36),
            sa.ForeignKey("consents.id", ondelete="SET NULL"), nullable=True,
        ),
        sa.Column("data_sensitivity_class", sa.String(length=16), nullable=False,
                  server_default="high"),
        sa.Column("record_status", sa.String(length=16), nullable=False, server_default="active"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("raw_payload", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now()),
    ]


def _common_indexes(table: str) -> None:
    op.create_check_constraint(
        f"ck_{table}_subject_exclusive", table,
        "(subject_kind = 'client' AND client_id IS NOT NULL AND practitioner_user_id IS NULL) "
        "OR (subject_kind = 'practitioner' AND practitioner_user_id IS NOT NULL "
        "AND client_id IS NULL)",
    )
    op.create_index(f"ix_{table}_subject_kind", table, ["subject_kind"])
    op.create_index(f"ix_{table}_client_id", table, ["client_id"])
    op.create_index(f"ix_{table}_practitioner_user_id", table, ["practitioner_user_id"])
    op.create_index(
        f"uq_{table}_client_current", table, ["client_id"], unique=True,
        postgresql_where=text("is_current AND client_id IS NOT NULL"),
    )
    op.create_index(
        f"uq_{table}_prat_current", table, ["practitioner_user_id"], unique=True,
        postgresql_where=text("is_current AND practitioner_user_id IS NOT NULL"),
    )
    op.create_index(
        f"ix_{table}_subject_current", table, ["subject_kind"],
        postgresql_where=text("is_current"),
    )


def upgrade() -> None:
    # 6 — Types jungiens (attitude + 4 fonctions)
    op.create_table(
        "profile_types_jungian", *_common_columns(),
        sa.Column("introversion", sa.Float(), nullable=True),
        sa.Column("thinking", sa.Float(), nullable=True),
        sa.Column("feeling", sa.Float(), nullable=True),
        sa.Column("sensing", sa.Float(), nullable=True),
        sa.Column("intuition", sa.Float(), nullable=True),
        sa.Column("dominant_function", sa.String(length=16), nullable=True),
    )
    _common_indexes("profile_types_jungian")
    op.create_index("ix_ptj_dominant_function", "profile_types_jungian", ["dominant_function"])
    op.create_index(
        "ix_jung_match", "profile_types_jungian",
        ["dominant_function", "introversion"],
        postgresql_where=text("is_current"),
    )


def downgrade() -> None:
    op.drop_table("profile_types_jungian")  # drop_table retire aussi index + contraintes

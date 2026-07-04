"""Profilage comportemental à 5 couches (OCEAN, Schwartz, Amour×8, Bartholomew, VAD).

Append-only versionné, sujet polymorphe (client/praticien), index de matching, un
seul profil COURANT par sujet/layer (index UNIQUE partiel). Posture non-diagnostic :
`status` défaut 'hypothese'. Loi 25 : lien consentement, sensibilité 'high'.

Enums stockés en VARCHAR (cohérent avec `native_enum=False` côté modèle).

Revision ID: 20260625_0039
Revises: 20260622_0038
Create Date: 2026-06-25
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text

revision = "20260625_0039"
down_revision = "20260622_0038"
branch_labels = None
depends_on = None


def _common_columns() -> list[sa.Column]:
    """Colonnes communes (miroir de ProfileLayerMixin)."""
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
    # Un seul profil COURANT par sujet (intégrité + lecture rapide)
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
    # 1 — OCEAN (Big Five)
    op.create_table(
        "profile_traits_ocean", *_common_columns(),
        sa.Column("openness", sa.Float(), nullable=True),
        sa.Column("conscientiousness", sa.Float(), nullable=True),
        sa.Column("extraversion", sa.Float(), nullable=True),
        sa.Column("agreeableness", sa.Float(), nullable=True),
        sa.Column("neuroticism", sa.Float(), nullable=True),
    )
    _common_indexes("profile_traits_ocean")
    op.create_index(
        "ix_ocean_match", "profile_traits_ocean",
        ["extraversion", "agreeableness", "neuroticism"],
        postgresql_where=text("is_current"),
    )

    # 2 — Schwartz (10 valeurs)
    op.create_table(
        "profile_values_schwartz", *_common_columns(),
        *(sa.Column(c, sa.Float(), nullable=True) for c in (
            "self_direction", "stimulation", "hedonism", "achievement", "power",
            "security", "conformity", "tradition", "benevolence", "universalism")),
    )
    _common_indexes("profile_values_schwartz")
    op.create_index(
        "ix_schwartz_match", "profile_values_schwartz",
        ["benevolence", "universalism", "security"],
        postgresql_where=text("is_current"),
    )

    # 3 — Expressions de l'Amour (8)
    op.create_table(
        "profile_relational_love", *_common_columns(),
        *(sa.Column(c, sa.Float(), nullable=True) for c in (
            "paroles_valorisantes", "moments_qualite", "contact_physique", "services_rendus",
            "cadeaux", "soutien_emotionnel", "espace_autonomie", "engagement_fiabilite")),
    )
    _common_indexes("profile_relational_love")
    op.create_index(
        "ix_love_match", "profile_relational_love",
        ["moments_qualite", "soutien_emotionnel", "paroles_valorisantes"],
        postgresql_where=text("is_current"),
    )

    # 4 — Bartholomew (4 quadrants)
    op.create_table(
        "profile_attachment_bartholomew", *_common_columns(),
        sa.Column("secure_score", sa.Float(), nullable=True),
        sa.Column("preoccupied_score", sa.Float(), nullable=True),
        sa.Column("dismissing_score", sa.Float(), nullable=True),
        sa.Column("fearful_score", sa.Float(), nullable=True),
        sa.Column("self_model_anxiety", sa.Float(), nullable=True),
        sa.Column("other_model_avoidance", sa.Float(), nullable=True),
        sa.Column("primary_style", sa.String(length=16), nullable=True),
    )
    _common_indexes("profile_attachment_bartholomew")
    op.create_index("ix_pab_primary_style", "profile_attachment_bartholomew", ["primary_style"])
    op.create_index(
        "ix_attach_match", "profile_attachment_bartholomew", ["primary_style"],
        postgresql_where=text("is_current"),
    )

    # 5 — VAD (état dynamique)
    op.create_table(
        "profile_state_vad", *_common_columns(),
        sa.Column("valence", sa.Float(), nullable=True),
        sa.Column("arousal", sa.Float(), nullable=True),
        sa.Column("dominance", sa.Float(), nullable=True),
    )
    _common_indexes("profile_state_vad")
    op.create_index("ix_vad_recent", "profile_state_vad", ["client_id", "assessed_at"])
    op.create_index(
        "ix_vad_match", "profile_state_vad", ["valence", "arousal"],
        postgresql_where=text("is_current"),
    )


def downgrade() -> None:
    for table in (
        "profile_state_vad",
        "profile_attachment_bartholomew",
        "profile_relational_love",
        "profile_values_schwartz",
        "profile_traits_ocean",
    ):
        op.drop_table(table)  # drop_table retire aussi index + contraintes

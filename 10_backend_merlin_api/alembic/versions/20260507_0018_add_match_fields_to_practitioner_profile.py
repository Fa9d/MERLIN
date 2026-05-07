"""add_match_fields_to_practitioner_profile

Revision ID: 20260507_0018
Revises: 072fa69b58e4
Create Date: 2026-05-07 00:00:00
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20260507_0018"
down_revision: Union[str, Sequence[str], None] = "072fa69b58e4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _column_exists(inspector: sa.Inspector, table_name: str, column_name: str) -> bool:
    return any(col["name"] == column_name for col in inspector.get_columns(table_name))


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not inspector.has_table("practitioner_profiles"):
        op.create_table(
            "practitioner_profiles",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("user_id", sa.String(length=36), nullable=False),
            sa.Column("display_name", sa.String(length=120), nullable=True),
            sa.Column("bio", sa.Text(), nullable=True),
            sa.Column("modalites", sa.JSON(), nullable=False),
            sa.Column("langues", sa.JSON(), nullable=False),
            sa.Column("approches", sa.JSON(), nullable=False),
            sa.Column("public_visible", sa.Boolean(), nullable=False),
            sa.Column("accepting_clients", sa.Boolean(), nullable=False),
            sa.Column("title_line", sa.String(length=200), nullable=True),
            sa.Column("intro_text", sa.Text(), nullable=True),
            sa.Column("presentation_audio_url", sa.String(length=500), nullable=True),
            sa.Column("domaines", sa.Text(), nullable=True),
            sa.Column("disponibilites", sa.Text(), nullable=True),
            sa.Column("tarif_horaire_cents", sa.Integer(), nullable=True),
            sa.Column("actif", sa.Boolean(), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(["user_id"], ["app_users.id"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(
            op.f("ix_practitioner_profiles_user_id"),
            "practitioner_profiles",
            ["user_id"],
            unique=True,
        )
        return

    with op.batch_alter_table("practitioner_profiles") as batch_op:
        if not _column_exists(inspector, "practitioner_profiles", "bio"):
            batch_op.add_column(sa.Column("bio", sa.Text(), nullable=True))
        if not _column_exists(inspector, "practitioner_profiles", "modalites"):
            batch_op.add_column(sa.Column("modalites", sa.JSON(), nullable=True))
        if not _column_exists(inspector, "practitioner_profiles", "langues"):
            batch_op.add_column(sa.Column("langues", sa.JSON(), nullable=True))
        if not _column_exists(inspector, "practitioner_profiles", "approches"):
            batch_op.add_column(sa.Column("approches", sa.JSON(), nullable=True))
        if not _column_exists(inspector, "practitioner_profiles", "public_visible"):
            batch_op.add_column(sa.Column("public_visible", sa.Boolean(), nullable=True))
        if not _column_exists(inspector, "practitioner_profiles", "accepting_clients"):
            batch_op.add_column(sa.Column("accepting_clients", sa.Boolean(), nullable=True))

    op.execute(
        "UPDATE practitioner_profiles SET modalites = '[]'::json "
        "WHERE modalites IS NULL"
    )
    op.execute(
        "UPDATE practitioner_profiles SET langues = '[]'::json "
        "WHERE langues IS NULL"
    )
    op.execute(
        "UPDATE practitioner_profiles SET approches = '[]'::json "
        "WHERE approches IS NULL"
    )
    op.execute(
        "UPDATE practitioner_profiles SET public_visible = false "
        "WHERE public_visible IS NULL"
    )
    op.execute(
        "UPDATE practitioner_profiles SET accepting_clients = true "
        "WHERE accepting_clients IS NULL"
    )

    with op.batch_alter_table("practitioner_profiles") as batch_op:
        batch_op.alter_column("modalites", nullable=False)
        batch_op.alter_column("langues", nullable=False)
        batch_op.alter_column("approches", nullable=False)
        batch_op.alter_column("public_visible", nullable=False)
        batch_op.alter_column("accepting_clients", nullable=False)


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not inspector.has_table("practitioner_profiles"):
        return

    with op.batch_alter_table("practitioner_profiles") as batch_op:
        if _column_exists(inspector, "practitioner_profiles", "accepting_clients"):
            batch_op.drop_column("accepting_clients")
        if _column_exists(inspector, "practitioner_profiles", "public_visible"):
            batch_op.drop_column("public_visible")
        if _column_exists(inspector, "practitioner_profiles", "approches"):
            batch_op.drop_column("approches")
        if _column_exists(inspector, "practitioner_profiles", "langues"):
            batch_op.drop_column("langues")
        if _column_exists(inspector, "practitioner_profiles", "modalites"):
            batch_op.drop_column("modalites")
        if _column_exists(inspector, "practitioner_profiles", "bio"):
            batch_op.drop_column("bio")

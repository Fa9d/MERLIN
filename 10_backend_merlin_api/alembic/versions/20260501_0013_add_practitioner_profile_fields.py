"""add practitioner profile fields

Revision ID: 20260501_0013
Revises: 20260501_0012
Create Date: 2026-05-01

"""
from alembic import op
import sqlalchemy as sa

revision = "20260501_0013"
down_revision = "20260501_0012"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("app_users", sa.Column("title_line", sa.String(255), nullable=True))
    op.add_column("app_users", sa.Column("intro_text", sa.Text, nullable=True))
    op.add_column("app_users", sa.Column("presentation_audio_url", sa.String(500), nullable=True))
    op.add_column("app_users", sa.Column("spoken_languages", sa.Text, nullable=True))
    op.add_column("app_users", sa.Column("available_channels", sa.Text, nullable=True))
    op.add_column(
        "app_users",
        sa.Column("is_publicly_listed", sa.Boolean, nullable=False, server_default="false"),
    )


def downgrade() -> None:
    op.drop_column("app_users", "is_publicly_listed")
    op.drop_column("app_users", "available_channels")
    op.drop_column("app_users", "spoken_languages")
    op.drop_column("app_users", "presentation_audio_url")
    op.drop_column("app_users", "intro_text")
    op.drop_column("app_users", "title_line")

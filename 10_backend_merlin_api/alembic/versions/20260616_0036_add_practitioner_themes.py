"""Thèmes d'accompagnement du praticien (profil public).

Revision ID: 20260616_0036
Revises: 20260616_0035
Create Date: 2026-06-16
"""

from alembic import op
import sqlalchemy as sa

revision = "20260616_0036"
down_revision = "20260616_0035"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("app_users", sa.Column("themes", sa.Text(), nullable=True))  # JSON array


def downgrade() -> None:
    op.drop_column("app_users", "themes")

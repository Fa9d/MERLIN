"""Champ lieu de naissance sur clients (profil obligatoire).

Revision ID: 20260616_0031
Revises: 20260615_0030
Create Date: 2026-06-16
"""

from alembic import op
import sqlalchemy as sa

revision = "20260616_0031"
down_revision = "20260615_0030"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("clients", sa.Column("birthplace", sa.String(length=120), nullable=True))


def downgrade() -> None:
    op.drop_column("clients", "birthplace")

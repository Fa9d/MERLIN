"""Table app_settings — réglages runtime clé→valeur (interrupteurs facturation par offre).

Revision ID: 20260615_0030
Revises: 20260615_0029
Create Date: 2026-06-15
"""

from alembic import op
import sqlalchemy as sa

revision = "20260615_0030"
down_revision = "20260615_0029"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "app_settings",
        sa.Column("key", sa.String(length=64), primary_key=True),
        sa.Column("value", sa.Text(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("app_settings")

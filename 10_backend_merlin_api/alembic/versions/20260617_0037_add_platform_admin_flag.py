"""Drapeau admin par compte (cumul sur le rôle, accordé depuis l'interface admin).

Revision ID: 20260617_0037
Revises: 20260616_0036
Create Date: 2026-06-17
"""

from alembic import op
import sqlalchemy as sa

revision = "20260617_0037"
down_revision = "20260616_0036"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "app_users",
        sa.Column(
            "is_platform_admin",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )


def downgrade() -> None:
    op.drop_column("app_users", "is_platform_admin")

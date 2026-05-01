"""add legal_name to app_users

Revision ID: 20260501_0012
Revises: 20260430_0011
Create Date: 2026-05-01 00:00:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20260501_0012"
down_revision: Union[str, Sequence[str], None] = "20260430_0011"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "app_users",
        sa.Column("legal_name", sa.String(length=255), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("app_users", "legal_name")

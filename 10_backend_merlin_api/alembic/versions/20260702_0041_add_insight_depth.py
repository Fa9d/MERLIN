"""add_insight_depth_to_app_users

Revision ID: 20260702_0041
Revises: 20260622_0038
Create Date: 2026-07-02 12:57:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20260702_0041'
down_revision: Union[str, Sequence[str], None] = '20260622_0038'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('app_users', sa.Column('insight_depth', sa.Enum('basic', 'intermediate', 'expert', name='insightdepth'), nullable=False, server_default='basic'))


def downgrade() -> None:
    op.drop_column('app_users', 'insight_depth')


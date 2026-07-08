"""add_practitioner_audio_profiles

Revision ID: 20260703_0043
Revises: 20260702_0042
Create Date: 2026-07-03 07:40:00.000000

Praticiens audio profiles : enregistrement vocal + métadonnées (durée, taille, etc.)
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20260703_0043'
down_revision: Union[str, Sequence[str], None] = '20260702_0042'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create practitioner_audio_profiles table
    op.create_table(
        'practitioner_audio_profiles',
        sa.Column('id', sa.String(36), nullable=False, primary_key=True),
        sa.Column('practitioner_id', sa.String(36), nullable=False, index=True),
        sa.Column('s3_key', sa.String(255), nullable=False, unique=True),
        sa.Column('duration_seconds', sa.Integer(), nullable=True),
        sa.Column('file_size_kb', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['practitioner_id'], ['app_users.id'], ondelete='CASCADE'),
    )


def downgrade() -> None:
    op.drop_table('practitioner_audio_profiles')

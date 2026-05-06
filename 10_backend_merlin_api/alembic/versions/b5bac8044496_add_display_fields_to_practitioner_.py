"""add_display_fields_to_practitioner_profile

Revision ID: b5bac8044496
Revises: cfe9090adc2f
Create Date: 2026-05-06 11:38:59.073202
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b5bac8044496'
down_revision: Union[str, Sequence[str], None] = 'cfe9090adc2f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('practitioner_profiles', sa.Column('display_name', sa.String(120), nullable=True))
    op.add_column('practitioner_profiles', sa.Column('title_line', sa.String(200), nullable=True))
    op.add_column('practitioner_profiles', sa.Column('intro_text', sa.Text(), nullable=True))
    op.add_column('practitioner_profiles', sa.Column('presentation_audio_url', sa.String(500), nullable=True))


def downgrade() -> None:
    op.drop_column('practitioner_profiles', 'presentation_audio_url')
    op.drop_column('practitioner_profiles', 'intro_text')
    op.drop_column('practitioner_profiles', 'title_line')
    op.drop_column('practitioner_profiles', 'display_name')


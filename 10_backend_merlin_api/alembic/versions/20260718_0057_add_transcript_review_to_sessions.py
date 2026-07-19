"""add_transcript_review_to_sessions — le praticien reprend la main sur la transcription

Revision ID: 20260718_0057
Revises: 20260709_0056
Create Date: 2026-07-18 21:00:00.000000

Circuit de relecture : la transcription automatique (faster-whisper) devient un
brouillon que le praticien peut corriger puis valider avant de (re)lancer
l'analyse. Traçabilité opposable : l'original automatique est conservé à la
première correction, la validation est horodatée et signée. Migration idempotente.
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260718_0057'
down_revision = '20260709_0056'
branch_labels = None
depends_on = None


def _has_column(table: str, column: str) -> bool:
    bind = op.get_bind()
    return column in [c['name'] for c in sa.inspect(bind).get_columns(table)]


def upgrade() -> None:
    # 'auto' = brouillon machine · 'corrected' = retouché praticien · 'validated' = validé
    if not _has_column('sessions', 'transcript_status'):
        op.add_column('sessions', sa.Column('transcript_status', sa.String(16), nullable=False, server_default='auto'))
    if not _has_column('sessions', 'transcript_original_text'):
        op.add_column('sessions', sa.Column('transcript_original_text', sa.Text(), nullable=True))
    if not _has_column('sessions', 'transcript_validated_at'):
        op.add_column('sessions', sa.Column('transcript_validated_at', sa.DateTime(timezone=True), nullable=True))
    if not _has_column('sessions', 'transcript_validated_by_user_id'):
        op.add_column('sessions', sa.Column('transcript_validated_by_user_id', sa.String(36), nullable=True))


def downgrade() -> None:
    op.drop_column('sessions', 'transcript_validated_by_user_id')
    op.drop_column('sessions', 'transcript_validated_at')
    op.drop_column('sessions', 'transcript_original_text')
    op.drop_column('sessions', 'transcript_status')

"""add_practitioner_journal — journal de pratique (espace personnel du praticien)

Revision ID: 20260709_0055
Revises: 20260709_0054
Create Date: 2026-07-09 11:30:00.000000

Retours de pratique : ce qui s'est passé EN le praticien (résonances,
évitements, fatigue) — strictement personnel, hors dossier client,
invisible à l'admin. Optionnel dans la forme, ADN IVIA dans l'esprit.
Migration idempotente.
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260709_0055'
down_revision = '20260709_0054'
branch_labels = None
depends_on = None


def _has_table(name: str) -> bool:
    bind = op.get_bind()
    return name in sa.inspect(bind).get_table_names()


def upgrade() -> None:
    if _has_table('practitioner_journal_entries'):
        return
    op.create_table(
        'practitioner_journal_entries',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('praticien_id', sa.String(36),
                  sa.ForeignKey('app_users.id', ondelete='CASCADE'),
                  nullable=False, index=True),
        sa.Column('session_id', sa.String(36),
                  sa.ForeignKey('sessions.id', ondelete='SET NULL'), nullable=True),
        sa.Column('body_text', sa.Text(), nullable=False),
        sa.Column('record_status', sa.String(16), nullable=False, server_default='active'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now()),
    )


def downgrade() -> None:
    if _has_table('practitioner_journal_entries'):
        op.drop_table('practitioner_journal_entries')

"""add_analysis_deliveries — restitutions client validées par le praticien

Revision ID: 20260708_0053
Revises: 20260708_0052
Create Date: 2026-07-08 23:55:00.000000

Étape 4 du chantier Analyses : la triade Observation/Hypothèse/Orientation
relue et éditée par le praticien avant d'atteindre le client. Validation
humaine constitutionnelle — aucune sortie IA ne va au client sans elle.
Migration idempotente.
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260708_0053'
down_revision = '20260708_0052'
branch_labels = None
depends_on = None


def _has_table(name: str) -> bool:
    bind = op.get_bind()
    return name in sa.inspect(bind).get_table_names()


def upgrade() -> None:
    if _has_table('analysis_deliveries'):
        return
    op.create_table(
        'analysis_deliveries',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('analysis_result_id', sa.String(36),
                  sa.ForeignKey('analysis_results.id', ondelete='CASCADE'),
                  nullable=False, index=True),
        sa.Column('client_id', sa.String(36),
                  sa.ForeignKey('clients.id', ondelete='CASCADE'),
                  nullable=False, index=True),
        sa.Column('session_id', sa.String(36),
                  sa.ForeignKey('sessions.id', ondelete='SET NULL'), nullable=True),
        sa.Column('delivered_by_user_id', sa.String(36),
                  sa.ForeignKey('app_users.id', ondelete='SET NULL'), nullable=False),
        sa.Column('observation', sa.Text(), nullable=False),
        sa.Column('hypothese', sa.Text(), nullable=False),
        sa.Column('orientation', sa.Text(), nullable=False),
        sa.Column('record_status', sa.String(16), nullable=False, server_default='active'),
        sa.Column('delivered_at', sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now()),
    )


def downgrade() -> None:
    if _has_table('analysis_deliveries'):
        op.drop_table('analysis_deliveries')

"""add_llm_usage_events — grand livre des coûts LLM réels

Revision ID: 20260709_0056
Revises: 20260709_0055
Create Date: 2026-07-09 20:00:00.000000

Un événement par appel Anthropic : modèle, tokens réels, coût USD au tarif du
moment, rattachements optionnels (séance/client/praticien/analyse). Source de
vérité des coûts d'analyse pour la console admin Économie — fin du forfait
estimé. Aucun contenu stocké, uniquement des compteurs. Migration idempotente.
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260709_0056'
down_revision = '20260709_0055'
branch_labels = None
depends_on = None


def _has_table(name: str) -> bool:
    bind = op.get_bind()
    return name in sa.inspect(bind).get_table_names()


def upgrade() -> None:
    if _has_table('llm_usage_events'):
        return
    op.create_table(
        'llm_usage_events',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('purpose', sa.String(64), nullable=False, index=True),
        sa.Column('model', sa.String(64), nullable=False),
        sa.Column('input_tokens', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('output_tokens', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('cost_usd', sa.Float(), nullable=False, server_default='0'),
        sa.Column('session_id', sa.String(36),
                  sa.ForeignKey('sessions.id', ondelete='SET NULL'),
                  nullable=True, index=True),
        sa.Column('client_id', sa.String(36),
                  sa.ForeignKey('clients.id', ondelete='SET NULL'),
                  nullable=True, index=True),
        sa.Column('praticien_user_id', sa.String(36),
                  sa.ForeignKey('app_users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('analysis_result_id', sa.String(36), nullable=True),
        sa.Column('created_by_user_id', sa.String(36),
                  sa.ForeignKey('app_users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('occurred_at', sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now(), index=True),
    )


def downgrade() -> None:
    if _has_table('llm_usage_events'):
        op.drop_table('llm_usage_events')

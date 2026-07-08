"""add_acquisition_source — provenance déclarée à l'inscription (mesure des canaux)

Revision ID: 20260706_0048
Revises: 20260704_0047
Create Date: 2026-07-06 14:20:00.000000

Colonne facultative app_users.acquisition_source : réponse à
« Comment as-tu entendu parler d'IVIA ? » (plan de mise en marché §11).
Migration idempotente.
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260706_0048'
down_revision = '20260704_0047'
branch_labels = None
depends_on = None


def _has_column(table: str, column: str) -> bool:
    bind = op.get_bind()
    cols = [c['name'] for c in sa.inspect(bind).get_columns(table)]
    return column in cols


def upgrade() -> None:
    if not _has_column('app_users', 'acquisition_source'):
        op.add_column('app_users', sa.Column('acquisition_source', sa.String(64), nullable=True))


def downgrade() -> None:
    if _has_column('app_users', 'acquisition_source'):
        op.drop_column('app_users', 'acquisition_source')

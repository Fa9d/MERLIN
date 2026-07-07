"""add_client_intentions — intentions/pratiques suivies entre les séances

Revision ID: 20260707_0050
Revises: 20260707_0049
Create Date: 2026-07-07 16:20:00.000000

Table client_intentions : cap court formulé par le client (ou proposé en séance),
suivi entre les séances. Repère d'autonomie, jamais une prescription.
Migration idempotente.
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260707_0050'
down_revision = '20260707_0049'
branch_labels = None
depends_on = None

_TABLE = 'client_intentions'


def _has_table(name: str) -> bool:
    bind = op.get_bind()
    return name in sa.inspect(bind).get_table_names()


def upgrade() -> None:
    if _has_table(_TABLE):
        return
    op.create_table(
        _TABLE,
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('client_id', sa.String(36),
                  sa.ForeignKey('clients.id', ondelete='CASCADE'), nullable=False),
        sa.Column('session_id', sa.String(36),
                  sa.ForeignKey('sessions.id', ondelete='SET NULL'), nullable=True),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('kind', sa.String(16), nullable=False, server_default='intention'),
        sa.Column('dimension', sa.String(32), nullable=True),
        sa.Column('status', sa.String(16), nullable=False, server_default='active'),
        sa.Column('created_by', sa.String(16), nullable=False, server_default='client'),
        sa.Column('realized_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('record_status', sa.String(16), nullable=False, server_default='active'),
        sa.Column('data_sensitivity_class', sa.String(32), nullable=False,
                  server_default='restricted'),
        sa.Column('retention_class', sa.String(16), nullable=False, server_default='extended'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text('now()')),
    )
    op.create_index(f'ix_{_TABLE}_client_id', _TABLE, ['client_id'])
    op.create_index(f'ix_{_TABLE}_session_id', _TABLE, ['session_id'])
    op.create_index(f'ix_{_TABLE}_status', _TABLE, ['status'])


def downgrade() -> None:
    if _has_table(_TABLE):
        op.drop_table(_TABLE)

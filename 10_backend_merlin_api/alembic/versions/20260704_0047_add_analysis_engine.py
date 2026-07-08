"""add_analysis_engine — capacités, credentials praticiens, résultats, journal d'accès

Revision ID: 20260704_0047
Revises: 20260704_0046
Create Date: 2026-07-04 16:00:00.000000

Socle « moteur plein / vannes par profil » (voir app/models/analysis.py).
Migration idempotente (IF NOT EXISTS via inspection) pour tolérer un replay.
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260704_0047'
down_revision = '20260704_0046'
branch_labels = None
depends_on = None


def _has_table(name: str) -> bool:
    bind = op.get_bind()
    return sa.inspect(bind).has_table(name)


def upgrade() -> None:
    if not _has_table('analysis_capability_flags'):
        op.create_table(
            'analysis_capability_flags',
            sa.Column('profile', sa.String(64), primary_key=True),
            sa.Column('capability', sa.String(64), primary_key=True),
            sa.Column('enabled', sa.Boolean, nullable=False, server_default=sa.text('true')),
            sa.Column('updated_by_user_id', sa.String(36), nullable=True),
            sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False,
                      server_default=sa.text('now()')),
        )

    if not _has_table('practitioner_credentials'):
        op.create_table(
            'practitioner_credentials',
            sa.Column('id', sa.String(36), primary_key=True),
            sa.Column('practitioner_user_id', sa.String(36),
                      sa.ForeignKey('app_users.id'), nullable=False, index=True),
            sa.Column('order_body', sa.String(160), nullable=False),
            sa.Column('license_number', sa.String(80), nullable=True),
            sa.Column('scope_notes', sa.Text, nullable=True),
            sa.Column('status', sa.String(20), nullable=False,
                      server_default='pending', index=True),
            sa.Column('recognized_by_order', sa.Boolean, nullable=False,
                      server_default=sa.text('false')),
            sa.Column('verified_by_user_id', sa.String(36), nullable=True),
            sa.Column('verified_at', sa.DateTime(timezone=True), nullable=True),
            sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), nullable=False,
                      server_default=sa.text('now()')),
        )

    if not _has_table('analysis_results'):
        op.create_table(
            'analysis_results',
            sa.Column('id', sa.String(36), primary_key=True),
            sa.Column('capability', sa.String(64), nullable=False, index=True),
            sa.Column('sensitivity', sa.String(32), nullable=False, index=True),
            sa.Column('client_id', sa.String(36),
                      sa.ForeignKey('clients.id'), nullable=True, index=True),
            sa.Column('recording_id', sa.String(36), nullable=True, index=True),
            sa.Column('session_id', sa.String(36), nullable=True, index=True),
            sa.Column('engine_version', sa.String(64), nullable=True),
            sa.Column('payload_json', sa.Text, nullable=False),
            sa.Column('created_by_user_id', sa.String(36), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), nullable=False,
                      server_default=sa.text('now()'), index=True),
        )
        op.create_index('ix_analysis_results_subject', 'analysis_results',
                        ['client_id', 'capability'])

    if not _has_table('analysis_access_logs'):
        op.create_table(
            'analysis_access_logs',
            sa.Column('id', sa.String(36), primary_key=True),
            sa.Column('user_id', sa.String(36), nullable=False, index=True),
            sa.Column('analysis_result_id', sa.String(36), nullable=False, index=True),
            sa.Column('client_id', sa.String(36), nullable=True, index=True),
            sa.Column('sensitivity', sa.String(32), nullable=False),
            sa.Column('context', sa.String(160), nullable=True),
            sa.Column('accessed_at', sa.DateTime(timezone=True), nullable=False,
                      server_default=sa.text('now()'), index=True),
        )


def downgrade() -> None:
    for table in ('analysis_access_logs', 'analysis_results',
                  'practitioner_credentials', 'analysis_capability_flags'):
        if _has_table(table):
            op.drop_table(table)

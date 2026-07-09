"""add_client_praticien_link — relation d'accompagnement durable + transferts

Revision ID: 20260709_0054
Revises: 20260708_0053
Create Date: 2026-07-09 09:00:00.000000

Décision fondateur (2026-07-09) : le lien client→praticien est une relation
durable de première classe. NULL = client autonome (journal seul).
- clients.praticien_id : rétro-peuplé depuis la séance la plus récente ;
- client_practitioner_transfers : audit des changements de praticien
  (mode 'resume' par défaut ; 'integral' exige le consentement du client).
Migration idempotente.
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260709_0054'
down_revision = '20260708_0053'
branch_labels = None
depends_on = None


def _has_table(name: str) -> bool:
    bind = op.get_bind()
    return name in sa.inspect(bind).get_table_names()


def _has_column(table: str, column: str) -> bool:
    bind = op.get_bind()
    return column in [c["name"] for c in sa.inspect(bind).get_columns(table)]


def upgrade() -> None:
    if not _has_column('clients', 'praticien_id'):
        op.add_column(
            'clients',
            sa.Column('praticien_id', sa.String(36),
                      sa.ForeignKey('app_users.id', ondelete='SET NULL'),
                      nullable=True),
        )
        op.create_index('ix_clients_praticien_id', 'clients', ['praticien_id'])
        # Rétro-peuplement : le praticien de la séance la plus récente du client.
        op.execute(sa.text("""
            UPDATE clients SET praticien_id = (
                SELECT s.praticien_id FROM sessions s
                WHERE s.client_id = clients.id AND s.praticien_id IS NOT NULL
                ORDER BY s.session_sequence_number DESC LIMIT 1
            )
        """))

    if not _has_table('client_practitioner_transfers'):
        op.create_table(
            'client_practitioner_transfers',
            sa.Column('id', sa.String(36), primary_key=True),
            sa.Column('client_id', sa.String(36),
                      sa.ForeignKey('clients.id', ondelete='CASCADE'),
                      nullable=False, index=True),
            sa.Column('from_praticien_id', sa.String(36),
                      sa.ForeignKey('app_users.id', ondelete='SET NULL'), nullable=True),
            sa.Column('to_praticien_id', sa.String(36),
                      sa.ForeignKey('app_users.id', ondelete='SET NULL'), nullable=True),
            sa.Column('mode', sa.String(16), nullable=False, server_default='resume'),
            sa.Column('client_consent_obtained', sa.Boolean(), nullable=False,
                      server_default=sa.false()),
            sa.Column('note', sa.Text(), nullable=True),
            sa.Column('transferred_by_user_id', sa.String(36),
                      sa.ForeignKey('app_users.id', ondelete='SET NULL'), nullable=True),
            sa.Column('transferred_at', sa.DateTime(timezone=True), nullable=False,
                      server_default=sa.func.now()),
        )


def downgrade() -> None:
    if _has_table('client_practitioner_transfers'):
        op.drop_table('client_practitioner_transfers')
    if _has_column('clients', 'praticien_id'):
        op.drop_index('ix_clients_praticien_id', 'clients')
        op.drop_column('clients', 'praticien_id')

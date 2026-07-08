"""add_s3_and_payment_fields

Revision ID: 20260703_0045
Revises: 20260703_0044
Create Date: 2026-07-03 12:00:00.000000

Migration idempotente : les tables creees par 0043/0044 contiennent deja
certaines de ces colonnes ; on n'ajoute que ce qui manque reellement.
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260703_0045'
down_revision = '20260703_0044'
branch_labels = None
depends_on = None


def _existing_columns(table: str) -> set[str]:
    bind = op.get_bind()
    insp = sa.inspect(bind)
    if table not in insp.get_table_names():
        return set()
    return {c['name'] for c in insp.get_columns(table)}


def _existing_indexes(table: str) -> set[str]:
    bind = op.get_bind()
    insp = sa.inspect(bind)
    if table not in insp.get_table_names():
        return set()
    return {i['name'] for i in insp.get_indexes(table)}


def upgrade() -> None:
    # Champs S3 sur practitioner_audio_profiles (0043 cree deja s3_key)
    audio_cols = _existing_columns('practitioner_audio_profiles')
    for name, col in (
        ('s3_key', sa.Column('s3_key', sa.String, nullable=True)),
        ('s3_presigned_url', sa.Column('s3_presigned_url', sa.String, nullable=True)),
        ('presigned_url_expires_at', sa.Column('presigned_url_expires_at', sa.DateTime, nullable=True)),
    ):
        if name not in audio_cols:
            op.add_column('practitioner_audio_profiles', col)

    # Champs paiement sur appointments (0044 cree deja payment_order_id,
    # confirmed_at, paid_at, noted_at)
    apt_cols = _existing_columns('appointments')
    for name, col in (
        ('stripe_session_id', sa.Column('stripe_session_id', sa.String, nullable=True)),
        ('payment_intent_id', sa.Column('payment_intent_id', sa.String, nullable=True)),
        ('amount_cents', sa.Column('amount_cents', sa.Integer, nullable=True)),
        ('payment_order_id', sa.Column('payment_order_id', sa.String, nullable=True)),
        ('confirmed_at', sa.Column('confirmed_at', sa.DateTime, nullable=True)),
        ('paid_at', sa.Column('paid_at', sa.DateTime, nullable=True)),
        ('noted_at', sa.Column('noted_at', sa.DateTime, nullable=True)),
    ):
        if name not in apt_cols:
            op.add_column('appointments', col)

    # Index (idempotents)
    apt_idx = _existing_indexes('appointments')
    if 'ix_appointments_payment_order_id' not in apt_idx:
        op.create_index('ix_appointments_payment_order_id', 'appointments', ['payment_order_id'])
    if 'ix_appointments_stripe_session_id' not in apt_idx:
        op.create_index('ix_appointments_stripe_session_id', 'appointments', ['stripe_session_id'])


def downgrade() -> None:
    apt_idx = _existing_indexes('appointments')
    if 'ix_appointments_stripe_session_id' in apt_idx:
        op.drop_index('ix_appointments_stripe_session_id')
    if 'ix_appointments_payment_order_id' in apt_idx:
        op.drop_index('ix_appointments_payment_order_id')

    apt_cols = _existing_columns('appointments')
    for name in ('stripe_session_id', 'payment_intent_id', 'amount_cents'):
        if name in apt_cols:
            op.drop_column('appointments', name)

    audio_cols = _existing_columns('practitioner_audio_profiles')
    for name in ('presigned_url_expires_at', 's3_presigned_url'):
        if name in audio_cols:
            op.drop_column('practitioner_audio_profiles', name)

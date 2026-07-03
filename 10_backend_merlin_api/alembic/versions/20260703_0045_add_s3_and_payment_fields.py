"""add_s3_and_payment_fields

Revision ID: 20260703_0045
Revises: 20260703_0044
Create Date: 2026-07-03 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20260703_0045'
down_revision = '20260703_0044'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add S3 fields to practitioner_audio_profiles
    op.add_column(
        'practitioner_audio_profiles',
        sa.Column('s3_key', sa.String, nullable=True)
    )
    op.add_column(
        'practitioner_audio_profiles',
        sa.Column('s3_presigned_url', sa.String, nullable=True)
    )
    op.add_column(
        'practitioner_audio_profiles',
        sa.Column('presigned_url_expires_at', sa.DateTime, nullable=True)
    )
    
    # Add payment fields to appointments
    op.add_column(
        'appointments',
        sa.Column('stripe_session_id', sa.String, nullable=True)
    )
    op.add_column(
        'appointments',
        sa.Column('payment_intent_id', sa.String, nullable=True)
    )
    op.add_column(
        'appointments',
        sa.Column('amount_cents', sa.Integer, nullable=True)
    )
    op.add_column(
        'appointments',
        sa.Column('payment_order_id', sa.String, nullable=True)
    )
    op.add_column(
        'appointments',
        sa.Column('confirmed_at', sa.DateTime, nullable=True)
    )
    op.add_column(
        'appointments',
        sa.Column('paid_at', sa.DateTime, nullable=True)
    )
    op.add_column(
        'appointments',
        sa.Column('noted_at', sa.DateTime, nullable=True)
    )
    
    # Create index on payment_order_id for fast lookup
    op.create_index(
        'ix_appointments_payment_order_id',
        'appointments',
        ['payment_order_id']
    )
    
    # Create index on stripe_session_id for webhook verification
    op.create_index(
        'ix_appointments_stripe_session_id',
        'appointments',
        ['stripe_session_id']
    )


def downgrade() -> None:
    # Remove indexes
    op.drop_index('ix_appointments_stripe_session_id')
    op.drop_index('ix_appointments_payment_order_id')
    
    # Remove payment fields
    op.drop_column('appointments', 'noted_at')
    op.drop_column('appointments', 'paid_at')
    op.drop_column('appointments', 'confirmed_at')
    op.drop_column('appointments', 'payment_order_id')
    op.drop_column('appointments', 'amount_cents')
    op.drop_column('appointments', 'payment_intent_id')
    op.drop_column('appointments', 'stripe_session_id')
    
    # Remove S3 fields
    op.drop_column('practitioner_audio_profiles', 'presigned_url_expires_at')
    op.drop_column('practitioner_audio_profiles', 's3_presigned_url')
    op.drop_column('practitioner_audio_profiles', 's3_key')

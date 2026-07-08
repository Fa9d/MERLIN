"""Add slots and appointments tables for calendar CRUD

Revision ID: 20260703_0044
Revises: 20260703_0043
Create Date: 2026-07-03 08:00:00.000000

Tables:
  - practitioner_slots: praticien availability slots (hourly/custom duration)
  - appointments: booked sessions (client + praticien + payment + notes)
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '20260703_0044'
down_revision: Union[str, Sequence[str], None] = '20260703_0043'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create practitioner_slots table
    op.create_table(
        'practitioner_slots',
        sa.Column('id', sa.String(36), nullable=False, primary_key=True),
        sa.Column('practitioner_id', sa.String(36), nullable=False, index=True),
        sa.Column('start_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('duration_minutes', sa.Integer(), nullable=False, default=60),
        sa.Column('is_available', sa.Boolean(), nullable=False, default=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['practitioner_id'], ['app_users.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_practitioner_slots_practitioner_id_start_time', 'practitioner_slots', 
                    ['practitioner_id', 'start_time'])

    # Create appointments table
    op.create_table(
        'appointments',
        sa.Column('id', sa.String(36), nullable=False, primary_key=True),
        sa.Column('client_id', sa.String(36), nullable=False, index=True),
        sa.Column('practitioner_id', sa.String(36), nullable=False, index=True),
        sa.Column('slot_id', sa.String(36), nullable=True),
        sa.Column('start_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('duration_minutes', sa.Integer(), nullable=False, default=60),
        sa.Column('status', sa.String(20), nullable=False, default='scheduled'),  # scheduled, confirmed, paid, noted, cancelled
        sa.Column('session_id', sa.String(36), nullable=True),  # FK to sessions table (audio/video session)
        sa.Column('payment_order_id', sa.String(36), nullable=True),  # FK to payment_orders table
        sa.Column('session_notes_id', sa.String(36), nullable=True),  # FK to session_notes table
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('confirmed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('paid_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('noted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['client_id'], ['app_users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['practitioner_id'], ['app_users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['slot_id'], ['practitioner_slots.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['session_id'], ['audio_sessions.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['payment_order_id'], ['payment_orders.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['session_notes_id'], ['session_notes.id'], ondelete='SET NULL'),
    )
    op.create_index('ix_appointments_client_id_start_time', 'appointments', 
                    ['client_id', 'start_time'])
    op.create_index('ix_appointments_practitioner_id_start_time', 'appointments', 
                    ['practitioner_id', 'start_time'])
    op.create_index('ix_appointments_status', 'appointments', ['status'])


def downgrade() -> None:
    op.drop_index('ix_appointments_status', 'appointments')
    op.drop_index('ix_appointments_practitioner_id_start_time', 'appointments')
    op.drop_index('ix_appointments_client_id_start_time', 'appointments')
    op.drop_table('appointments')

    op.drop_index('ix_practitioner_slots_practitioner_id_start_time', 'practitioner_slots')
    op.drop_table('practitioner_slots')

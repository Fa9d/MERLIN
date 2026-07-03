"""add_session_notes

Revision ID: 20260704_0046
Revises: 20260703_0045
Create Date: 2026-07-04 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20260704_0046'
down_revision = '20260703_0045'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add notes columns to appointments
    op.add_column(
        'appointments',
        sa.Column('session_notes', sa.Text, nullable=True)
    )
    op.add_column(
        'appointments',
        sa.Column('practitioner_notes', sa.Text, nullable=True)
    )


def downgrade() -> None:
    # Remove notes columns
    op.drop_column('appointments', 'practitioner_notes')
    op.drop_column('appointments', 'session_notes')

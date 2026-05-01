"""add practitioner role to app_users

Revision ID: 20260430_0011
Revises: 20260424_0010
Create Date: 2026-04-30 00:00:00
"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "20260430_0011"
down_revision: Union[str, Sequence[str], None] = "20260424_0010"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # The role column uses native_enum=False (VARCHAR), so no PG type to alter.
    # Drop and recreate the CHECK constraint to include 'practitioner'.
    op.execute("ALTER TABLE app_users DROP CONSTRAINT IF EXISTS approle;")
    op.execute(
        """
        ALTER TABLE app_users
        ADD CONSTRAINT approle
        CHECK (role IN (
            'public_client',
            'practitioner',
            'operator',
            'supervisor',
            'admin_tech'
        ))
        """
    )


def downgrade() -> None:
    op.execute("ALTER TABLE app_users DROP CONSTRAINT IF EXISTS approle;")
    op.execute(
        """
        ALTER TABLE app_users
        ADD CONSTRAINT approle
        CHECK (role IN (
            'public_client',
            'operator',
            'supervisor',
            'admin_tech'
        ))
        """
    )

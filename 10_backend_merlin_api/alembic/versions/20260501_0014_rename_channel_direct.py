"""rename phone video channels to direct

Revision ID: 20260501_0014
Revises: 20260501_0013_add_practitioner_profile_fields
Create Date: 2026-05-01
"""

from alembic import op

revision = "20260501_0014"
down_revision = "20260501_0013"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Migrer les séances existantes : phone et video → direct
    op.execute(
        "UPDATE sessions SET session_channel_code = 'direct' "
        "WHERE session_channel_code IN ('phone', 'video')"
    )
    # Mettre à jour available_channels de David (et tout profil avec phone/video)
    op.execute(
        "UPDATE app_users SET available_channels = '[\"direct\"]' "
        "WHERE available_channels LIKE '%phone%' OR available_channels LIKE '%video%'"
    )


def downgrade() -> None:
    # Rollback symbolique — on remet phone (non destructif)
    op.execute(
        "UPDATE sessions SET session_channel_code = 'phone' "
        "WHERE session_channel_code = 'direct'"
    )

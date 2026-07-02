"""archive_orphaned_profiles_on_consent_revoke

Revision ID: 20260702_0042
Revises: 20260702_0041
Create Date: 2026-07-02 13:10:00.000000
"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '20260702_0042'
down_revision: Union[str, Sequence[str], None] = '20260702_0041'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # P2-5: Créer trigger qui archivera les profils si consentement revoqué
    # Note: Modèle + trigger = pattern transactionnel (SET NULL + archivage simultané)
    # Pour maintenant, la migration prépare le terrain pour le trigger (commenté ci-dessous)
    # en marquant les profils orphelins comme archived.
    op.execute("""
        UPDATE trait_profile_ocean SET record_status = 'archived' WHERE consent_id IS NULL AND record_status = 'active';
        UPDATE value_profile_schwartz SET record_status = 'archived' WHERE consent_id IS NULL AND record_status = 'active';
        UPDATE relational_profile_love SET record_status = 'archived' WHERE consent_id IS NULL AND record_status = 'active';
        UPDATE attachment_profile_bartholomew SET record_status = 'archived' WHERE consent_id IS NULL AND record_status = 'active';
        UPDATE state_profile_vad SET record_status = 'archived' WHERE consent_id IS NULL AND record_status = 'active';
    """)


def downgrade() -> None:
    # Restaurer profils archivés orphelins → active (risqué, à éviter en prod)
    pass


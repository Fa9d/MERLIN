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
    # P2-5 P2-7: Archiver les profils orphelins (consentement révoqué ou praticien supprimé)
    # Idempotent : check existence des tables avant de les updater (évite erreur si migration 0039/0040 n'a pas encore créé)
    op.execute("""
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'trait_profile_ocean') THEN
                UPDATE trait_profile_ocean SET record_status = 'archived' WHERE consent_id IS NULL AND record_status = 'active';
                UPDATE value_profile_schwartz SET record_status = 'archived' WHERE consent_id IS NULL AND record_status = 'active';
                UPDATE relational_profile_love SET record_status = 'archived' WHERE consent_id IS NULL AND record_status = 'active';
                UPDATE attachment_profile_bartholomew SET record_status = 'archived' WHERE consent_id IS NULL AND record_status = 'active';
                UPDATE state_profile_vad SET record_status = 'archived' WHERE consent_id IS NULL AND record_status = 'active';
            END IF;
        END $$;
    """)


def downgrade() -> None:
    # Restaurer profils archivés orphelins → active (risqué, à éviter en prod)
    pass


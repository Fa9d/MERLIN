"""add_session_types — types de séance + matrice (type × capacité)

Revision ID: 20260708_0051
Revises: 20260707_0050
Create Date: 2026-07-08 21:30:00.000000

Gouvernance des analyses par type de séance (Atelier des lectures) :
- session_types : référentiel administrable (3 types semés) ;
- session_type_capabilities : enabled (autorise) + auto_run (post-transcription) ;
- sessions.session_type_code : rattachement optionnel (défaut permissif).
Migration idempotente.
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260708_0051'
down_revision = '20260707_0050'
branch_labels = None
depends_on = None


def _has_table(name: str) -> bool:
    bind = op.get_bind()
    return name in sa.inspect(bind).get_table_names()


def _has_column(table: str, column: str) -> bool:
    bind = op.get_bind()
    return column in [c["name"] for c in sa.inspect(bind).get_columns(table)]


def upgrade() -> None:
    if not _has_table('session_types'):
        op.create_table(
            'session_types',
            sa.Column('code', sa.String(32), primary_key=True),
            sa.Column('label', sa.String(120), nullable=False),
            sa.Column('description', sa.Text(), nullable=True),
            sa.Column('active', sa.Boolean(), nullable=False, server_default=sa.true()),
            sa.Column('created_at', sa.DateTime(timezone=True), nullable=False,
                      server_default=sa.func.now()),
            sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False,
                      server_default=sa.func.now()),
        )
        op.bulk_insert(
            sa.table(
                'session_types',
                sa.column('code', sa.String),
                sa.column('label', sa.String),
                sa.column('description', sa.Text),
            ),
            [
                {
                    'code': 'ecoute',
                    'label': 'Écoute simple',
                    'description': "Présence et écoute — le minimum d'analyse, le maximum d'attention.",
                },
                {
                    'code': 'suivi',
                    'label': 'Suivi en profondeur',
                    'description': "Accompagnement dans la durée — toute la panoplie de lectures peut s'appliquer.",
                },
                {
                    'code': 'express',
                    'label': 'Séance express',
                    'description': 'Rencontre courte par lien partagé — lectures légères.',
                },
            ],
        )

    if not _has_table('session_type_capabilities'):
        op.create_table(
            'session_type_capabilities',
            sa.Column('id', sa.String(36), primary_key=True),
            sa.Column('session_type_code', sa.String(32),
                      sa.ForeignKey('session_types.code', ondelete='CASCADE'),
                      nullable=False, index=True),
            sa.Column('capability', sa.String(64), nullable=False),
            sa.Column('enabled', sa.Boolean(), nullable=False, server_default=sa.true()),
            sa.Column('auto_run', sa.Boolean(), nullable=False, server_default=sa.false()),
            sa.UniqueConstraint('session_type_code', 'capability',
                                name='uq_session_type_capability'),
        )

    if not _has_column('sessions', 'session_type_code'):
        op.add_column(
            'sessions',
            sa.Column('session_type_code', sa.String(32),
                      sa.ForeignKey('session_types.code', ondelete='SET NULL'),
                      nullable=True),
        )


def downgrade() -> None:
    if _has_column('sessions', 'session_type_code'):
        op.drop_column('sessions', 'session_type_code')
    if _has_table('session_type_capabilities'):
        op.drop_table('session_type_capabilities')
    if _has_table('session_types'):
        op.drop_table('session_types')

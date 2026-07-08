"""add_exercises — catalogue d'exercices + propositions au client

Revision ID: 20260708_0052
Revises: 20260708_0051
Create Date: 2026-07-08 22:30:00.000000

Exercices (Atelier des lectures) : catalogue administrable de pratiques sobres
(vocabulaire Loi 21) + table de proposition praticien→client avec cheminement
(propose → en_cours → termine/abandonne). Trois exercices semés.
Migration idempotente.
"""
from alembic import op
import sqlalchemy as sa
from uuid import uuid4

# revision identifiers, used by Alembic.
revision = '20260708_0052'
down_revision = '20260708_0051'
branch_labels = None
depends_on = None


def _has_table(name: str) -> bool:
    bind = op.get_bind()
    return name in sa.inspect(bind).get_table_names()


def upgrade() -> None:
    if not _has_table('exercises'):
        op.create_table(
            'exercises',
            sa.Column('id', sa.String(36), primary_key=True),
            sa.Column('code', sa.String(48), nullable=False, unique=True),
            sa.Column('title', sa.String(160), nullable=False),
            sa.Column('instructions', sa.Text(), nullable=False),
            sa.Column('dimension', sa.String(32), nullable=True),
            sa.Column('active', sa.Boolean(), nullable=False, server_default=sa.true()),
            sa.Column('created_at', sa.DateTime(timezone=True), nullable=False,
                      server_default=sa.func.now()),
            sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False,
                      server_default=sa.func.now()),
        )
        op.bulk_insert(
            sa.table(
                'exercises',
                sa.column('id', sa.String),
                sa.column('code', sa.String),
                sa.column('title', sa.String),
                sa.column('instructions', sa.Text),
                sa.column('dimension', sa.String),
            ),
            [
                {
                    'id': str(uuid4()),
                    'code': 'respiration_ancrage',
                    'title': "Respiration d'ancrage (3 minutes)",
                    'instructions': (
                        "Assieds-toi confortablement, les deux pieds au sol. Inspire par le nez "
                        "en comptant jusqu'à 4, laisse l'air ressortir lentement en comptant "
                        "jusqu'à 6. Recommence pendant trois minutes. Si l'esprit part ailleurs, "
                        "c'est normal — reviens simplement au souffle, sans te juger."
                    ),
                    'dimension': 'corps',
                },
                {
                    'id': str(uuid4()),
                    'code': 'ecriture_du_soir',
                    'title': "Trois lignes du soir",
                    'instructions': (
                        "Avant de dormir, écris trois lignes dans ton journal : une chose qui a "
                        "pesé aujourd'hui, une chose qui a aidé, une chose que tu veux déposer "
                        "avant la nuit. Pas de style, pas d'obligation — juste déposer."
                    ),
                    'dimension': 'emotions',
                },
                {
                    'id': str(uuid4()),
                    'code': 'marche_attentive',
                    'title': "Marche attentive (10 minutes)",
                    'instructions': (
                        "Marche dehors dix minutes sans téléphone. Porte attention à trois "
                        "choses que tu vois, deux que tu entends, une que tu sens. Rien à "
                        "réussir — juste être là où tes pieds sont."
                    ),
                    'dimension': 'territoire',
                },
            ],
        )

    if not _has_table('client_exercises'):
        op.create_table(
            'client_exercises',
            sa.Column('id', sa.String(36), primary_key=True),
            sa.Column('client_id', sa.String(36),
                      sa.ForeignKey('clients.id', ondelete='CASCADE'),
                      nullable=False, index=True),
            sa.Column('exercise_id', sa.String(36),
                      sa.ForeignKey('exercises.id', ondelete='CASCADE'),
                      nullable=False, index=True),
            sa.Column('session_id', sa.String(36),
                      sa.ForeignKey('sessions.id', ondelete='SET NULL'), nullable=True),
            sa.Column('assigned_by_user_id', sa.String(36),
                      sa.ForeignKey('app_users.id', ondelete='SET NULL'), nullable=True),
            sa.Column('message', sa.Text(), nullable=True),
            sa.Column('status', sa.String(16), nullable=False, server_default='propose'),
            sa.Column('client_note', sa.Text(), nullable=True),
            sa.Column('record_status', sa.String(16), nullable=False, server_default='active'),
            sa.Column('proposed_at', sa.DateTime(timezone=True), nullable=False,
                      server_default=sa.func.now()),
            sa.Column('done_at', sa.DateTime(timezone=True), nullable=True),
        )


def downgrade() -> None:
    if _has_table('client_exercises'):
        op.drop_table('client_exercises')
    if _has_table('exercises'):
        op.drop_table('exercises')

"""add_journal_structured_fields — données structurées du journal (fin des blobs ARCHI_*::)

Revision ID: 20260707_0049
Revises: 20260706_0048
Create Date: 2026-07-07 15:45:00.000000

Ajoute à client_journal_entries :
- entry_kind : libre | checkin | exercice | moment (nature structurelle de l'entrée)
- dimensions : axes MERLIN touchés (JSON, sous-ensemble des 11 axes canoniques)
- structured_payload : charge structurée (humeur, énergie, sommeil, stressors…) en JSON
- session_id / session_phase : rattachement optionnel à une séance (avant | apres | entre)

Rétro-migration NON destructive : les entrées existantes préfixées ARCHI_INTERIEUR:: /
ARCHI_EXERCICE:: sont analysées → entry_kind + structured_payload remplis, body_text
conservé tel quel (les frontends plus anciens continuent de fonctionner).
Migration idempotente.
"""
import json

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260707_0049'
down_revision = '20260706_0048'
branch_labels = None
depends_on = None

_TABLE = 'client_journal_entries'


def _has_column(table: str, column: str) -> bool:
    bind = op.get_bind()
    cols = [c['name'] for c in sa.inspect(bind).get_columns(table)]
    return column in cols


def upgrade() -> None:
    if not _has_column(_TABLE, 'entry_kind'):
        op.add_column(
            _TABLE,
            sa.Column('entry_kind', sa.String(16), nullable=False, server_default='libre'),
        )
        op.create_index(f'ix_{_TABLE}_entry_kind', _TABLE, ['entry_kind'])
    if not _has_column(_TABLE, 'dimensions'):
        op.add_column(_TABLE, sa.Column('dimensions', sa.JSON(), nullable=True))
    if not _has_column(_TABLE, 'structured_payload'):
        op.add_column(_TABLE, sa.Column('structured_payload', sa.JSON(), nullable=True))
    if not _has_column(_TABLE, 'session_id'):
        op.add_column(
            _TABLE,
            sa.Column(
                'session_id',
                sa.String(36),
                sa.ForeignKey('sessions.id', ondelete='SET NULL'),
                nullable=True,
            ),
        )
        op.create_index(f'ix_{_TABLE}_session_id', _TABLE, ['session_id'])
    if not _has_column(_TABLE, 'session_phase'):
        op.add_column(_TABLE, sa.Column('session_phase', sa.String(8), nullable=True))

    _backfill_archi_prefixes()


def _backfill_archi_prefixes() -> None:
    """Analyse les entrées préfixées ARCHI_*:: → entry_kind + structured_payload.

    body_text est conservé intact (rétro-compatibilité lecture des anciens frontends).
    Idempotent : ne touche que les lignes encore en entry_kind = 'libre'.
    """
    bind = op.get_bind()
    rows = bind.execute(
        sa.text(
            f"SELECT id, body_text FROM {_TABLE} "
            "WHERE entry_kind = 'libre' AND ("
            "body_text LIKE 'ARCHI_INTERIEUR::%' OR body_text LIKE 'ARCHI_EXERCICE::%')"
        )
    ).fetchall()

    for row in rows:
        body = row.body_text or ''
        if body.startswith('ARCHI_INTERIEUR::'):
            kind, raw = 'checkin', body[len('ARCHI_INTERIEUR::'):]
        else:
            kind, raw = 'exercice', body[len('ARCHI_EXERCICE::'):]
        try:
            payload = json.loads(raw)
        except (ValueError, TypeError):
            continue  # blob illisible : on n'y touche pas
        bind.execute(
            sa.text(
                f"UPDATE {_TABLE} SET entry_kind = :kind, structured_payload = :payload "
                "WHERE id = :id"
            ),
            {'kind': kind, 'payload': json.dumps(payload, ensure_ascii=False), 'id': row.id},
        )


def downgrade() -> None:
    for col in ('session_phase', 'session_id', 'structured_payload', 'dimensions', 'entry_kind'):
        if _has_column(_TABLE, col):
            if col in ('entry_kind', 'session_id'):
                op.drop_index(f'ix_{_TABLE}_{col}', table_name=_TABLE)
            op.drop_column(_TABLE, col)

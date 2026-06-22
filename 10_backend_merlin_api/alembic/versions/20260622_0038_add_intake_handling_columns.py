"""Ajoute les colonnes de traitement des demandes d'entrée (handling_*).

Dérive modèle/migration : ces colonnes existent dans le modèle `IntakeRequest` ET en
production (créées hors de la chaîne de migrations, à une époque `create_all`), mais
aucune migration ne les déclarait. Conséquence : toute base reconstruite **depuis les
migrations** (CI, et surtout une **restauration de sauvegarde** en cas de sinistre) en
manquait — ce qui faisait échouer `test_public_intake_flow`.

Migration **idempotente** : ajoute chaque colonne uniquement si elle est absente. Donc
sûre aussi bien en prod (colonnes déjà là → on stampe juste la révision) qu'à neuf.

Revision ID: 20260622_0038
Revises: 20260617_0037
Create Date: 2026-06-22
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

revision = "20260622_0038"
down_revision = "20260617_0037"
branch_labels = None
depends_on = None

TABLE = "intake_requests"

# Colonnes du groupe « traitement » manquantes dans la chaîne de migrations.
_COLS = {
    "handling_status_code": sa.Column(
        "handling_status_code", sa.String(length=32), nullable=False, server_default="new"
    ),
    "handling_notes": sa.Column("handling_notes", sa.Text(), nullable=True),
    "handled_by_user_id": sa.Column("handled_by_user_id", sa.String(length=36), nullable=True),
    "handled_at": sa.Column("handled_at", sa.DateTime(timezone=True), nullable=True),
}


def _existing_columns() -> set[str]:
    return {c["name"] for c in inspect(op.get_bind()).get_columns(TABLE)}


def upgrade() -> None:
    have = _existing_columns()
    for name, col in _COLS.items():
        if name not in have:
            op.add_column(TABLE, col)


def downgrade() -> None:
    have = _existing_columns()
    for name in reversed(list(_COLS)):
        if name in have:
            op.drop_column(TABLE, name)

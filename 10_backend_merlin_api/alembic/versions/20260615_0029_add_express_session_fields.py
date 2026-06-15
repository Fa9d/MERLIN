"""Ajoute les champs de séance express sur sessions.

Séance express (MVP) : le praticien crée une séance ad hoc et obtient un lien
partageable. On stocke le token hashé du lien, le statut de paiement (métadonnée
praticien, pas un flux Stripe) et des notes privées.

Revision ID: 20260615_0029
Revises: 20260612_0028
Create Date: 2026-06-15
"""

from alembic import op
import sqlalchemy as sa

revision = "20260615_0029"
down_revision = "20260612_0028"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("sessions", sa.Column("express_token_hash", sa.String(length=128), nullable=True))
    op.add_column("sessions", sa.Column("payment_status", sa.String(length=32), nullable=True))
    op.add_column("sessions", sa.Column("private_notes", sa.Text(), nullable=True))
    op.create_index(
        "ix_sessions_express_token_hash", "sessions", ["express_token_hash"], unique=False
    )


def downgrade() -> None:
    op.drop_index("ix_sessions_express_token_hash", table_name="sessions")
    op.drop_column("sessions", "private_notes")
    op.drop_column("sessions", "payment_status")
    op.drop_column("sessions", "express_token_hash")

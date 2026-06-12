"""Ajoute sessions.transcript_text — transcription persistée des séances.

La transcription (faster-whisper / AssemblyAI) n'était utilisée que pour générer
la note praticien puis perdue. On la persiste pour que le client puisse relire
ses propres mots (enregistrements solo, canal audio_async) et pour éviter de
retranscrire en cas de relance du pipeline.

Revision ID: 20260612_0028
Revises: 20260528_0027
Create Date: 2026-06-12
"""

from alembic import op
import sqlalchemy as sa

revision = "20260612_0028"
down_revision = "20260528_0027"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("sessions", sa.Column("transcript_text", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("sessions", "transcript_text")

"""Journal de pratique — l'espace strictement personnel du praticien.

Le retour de pratique (2-3 minutes après une séance, ou n'importe quand) :
ce qui s'est passé EN LUI — résonances, évitements, fatigue, fiertés.
Optionnel dans la forme, ADN IVIA dans l'esprit (décision fondateur
2026-07-09) : le geste est invité et tissé dans le flux, jamais imposé.

STRICTEMENT PERSONNEL : invisible aux clients, aux autres praticiens ET à
l'admin — le pendant exact du journal intime client. Ne fait partie d'aucun
dossier client ; ne nourrit JAMAIS les analyses des clients.
"""
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.enums import RecordStatus


class PractitionerJournalEntry(Base):
    __tablename__ = "practitioner_journal_entries"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    praticien_id: Mapped[str] = mapped_column(
        ForeignKey("app_users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    # Séance d'où vient le retour (optionnel — on peut écrire hors séance)
    session_id: Mapped[str | None] = mapped_column(
        ForeignKey("sessions.id", ondelete="SET NULL"), nullable=True
    )
    body_text: Mapped[str] = mapped_column(Text, nullable=False)
    record_status: Mapped[RecordStatus] = mapped_column(
        Enum(RecordStatus, native_enum=False),
        nullable=False,
        default=RecordStatus.active,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

"""
client_journal_entry — entrées du journal rédigées par le client dans son espace.

Le journal est le lieu de la narration autonome : le client écrit librement,
ancre ou non à un événement biographique, et exprime son état présent.
Accessible uniquement par le client (et le praticien avec consentement explicite).
"""
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import (
    DataSensitivityClass,
    JournalEntryTypeCode,
    RecordStatus,
    RetentionClass,
)


class ClientJournalEntry(Base):
    __tablename__ = "client_journal_entries"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    # -- Relations principales ---------------------------------------------------
    client_id: Mapped[str] = mapped_column(
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # Lien optionnel vers un événement biographique connu
    linked_event_id: Mapped[str | None] = mapped_column(
        ForeignKey("client_life_events.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # -- Contenu -----------------------------------------------------------------
    entry_type: Mapped[JournalEntryTypeCode] = mapped_column(
        Enum(JournalEntryTypeCode, native_enum=False),
        nullable=False,
        default=JournalEntryTypeCode.aujourd_hui,
    )
    body_text: Mapped[str] = mapped_column(Text, nullable=False)
    # Ton émotionnel libre saisi par le client (ex: "calme", "anxieux", "confus")
    emotional_tone: Mapped[str | None] = mapped_column(String(64), nullable=True)
    # Année de référence si l'entrée évoque une période passée
    event_year_ref: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # -- Horodatage précis de l'écriture -----------------------------------------
    written_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    # -- Méta --------------------------------------------------------------------
    record_status: Mapped[RecordStatus] = mapped_column(
        Enum(RecordStatus, native_enum=False),
        nullable=False,
        default=RecordStatus.active,
    )
    data_sensitivity_class: Mapped[DataSensitivityClass] = mapped_column(
        Enum(DataSensitivityClass, native_enum=False),
        nullable=False,
        default=DataSensitivityClass.restricted,
    )
    retention_class: Mapped[RetentionClass] = mapped_column(
        Enum(RetentionClass, native_enum=False),
        nullable=False,
        default=RetentionClass.extended,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    # -- Relationships -----------------------------------------------------------
    client = relationship("Client", back_populates="journal_entries")
    linked_event = relationship("ClientLifeEvent", back_populates="journal_entries")

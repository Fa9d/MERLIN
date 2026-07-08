"""
client_intention — intention ou pratique suivie entre les séances.

Une intention est un cap court formulé par le client (ou proposé par un praticien
en séance) et suivi dans la durée : « marcher 20 minutes trois fois cette semaine »,
« nommer ce que je ressens avant de répondre ». Elle peut être rattachée à une séance
et à un axe MERLIN. Aucune valeur clinique : c'est un repère d'autonomie, pas une
prescription (constitution §6.4).
"""
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import (
    DataSensitivityClass,
    IntentionKindCode,
    IntentionStatusCode,
    RecordStatus,
    RetentionClass,
)


class ClientIntention(Base):
    __tablename__ = "client_intentions"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    client_id: Mapped[str] = mapped_column(
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # Séance d'origine, si l'intention a été posée en séance
    session_id: Mapped[str | None] = mapped_column(
        ForeignKey("sessions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # -- Contenu -------------------------------------------------------------
    text: Mapped[str] = mapped_column(Text, nullable=False)
    kind: Mapped[IntentionKindCode] = mapped_column(
        Enum(IntentionKindCode, native_enum=False),
        nullable=False,
        default=IntentionKindCode.intention,
    )
    # Axe MERLIN canonique principal (validé côté schéma), optionnel
    dimension: Mapped[str | None] = mapped_column(String(32), nullable=True)
    status: Mapped[IntentionStatusCode] = mapped_column(
        Enum(IntentionStatusCode, native_enum=False),
        nullable=False,
        default=IntentionStatusCode.active,
        index=True,
    )
    # Qui a formulé l'intention : "client" ou "praticien"
    created_by: Mapped[str] = mapped_column(String(16), nullable=False, default="client")
    realized_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # -- Méta ------------------------------------------------------------------
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
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    client = relationship("Client")

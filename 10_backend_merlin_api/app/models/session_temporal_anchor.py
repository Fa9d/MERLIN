"""
session_temporal_anchor — lie un moment de séance à un temps biographique précis.

C'est ici que se calcule le GAP (Z − Y) : l'écart entre l'année de l'événement
vécu et l'année de la séance. Cet écart est la donnée analytique centrale
du modèle temporel IVIA/Merlin.

Créé par le praticien pendant ou après la séance, optionnellement depuis
l'audio (offset secondes).
"""
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import DataSensitivityClass, EmotionalChargeCode, RecordStatus


class SessionTemporalAnchor(Base):
    __tablename__ = "session_temporal_anchors"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    # -- Relations principales ---------------------------------------------------
    session_id: Mapped[str] = mapped_column(
        ForeignKey("sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    session_note_id: Mapped[str | None] = mapped_column(
        ForeignKey("session_notes.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    client_id: Mapped[str] = mapped_column(
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # Si l'événement est déjà dans la ligne de vie
    life_event_id: Mapped[str | None] = mapped_column(
        ForeignKey("client_life_events.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # -- Ce qui a été dit --------------------------------------------------------
    verbatim_fragment: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Position dans l'enregistrement audio (secondes depuis le début)
    said_at_offset_sec: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # -- Ancrage temporel --------------------------------------------------------
    # Année évoquée (si pas de life_event lié, ou pour préciser)
    event_year_approx: Mapped[int | None] = mapped_column(Integer, nullable=True)
    client_age_ref: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # Calculé : année_séance − event_year_approx
    gap_years: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # -- Analyse du praticien ----------------------------------------------------
    interpretation_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    emotional_charge: Mapped[EmotionalChargeCode | None] = mapped_column(
        Enum(EmotionalChargeCode, native_enum=False),
        nullable=True,
    )
    # Zone d'évitement : le client tourne autour sans dire
    is_silence_marker: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

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

    # -- Relationships -----------------------------------------------------------
    session = relationship("SessionRecord", back_populates="temporal_anchors")
    session_note = relationship("SessionNote", back_populates="temporal_anchors")
    client = relationship("Client", back_populates="temporal_anchors")
    life_event = relationship("ClientLifeEvent", back_populates="temporal_anchors")

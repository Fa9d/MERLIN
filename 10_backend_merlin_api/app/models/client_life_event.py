"""
client_life_event — événements biographiques datés avec ancrage temporel précis.

Capture la distinction fondamentale :
  - Y  : l'année où l'événement s'est produit (temps vécu)
  - Z  : le moment où il est raconté en séance (session_id / created_at)
  - gap: l'écart Y→Z calculé par session_temporal_anchor

Inspiré de :
  - Glen Elder — Life Course Theory (timing & historical embeddedness)
  - Ricoeur — Temps et Récit (temps vécu vs. temps raconté)
  - Young — Schema Therapy (schémas précoces comme événements datables)
"""
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import (
    AuthoredByCode,
    DataSensitivityClass,
    EventTypeCode,
    LifeStageCode,
    RecordStatus,
)


class ClientLifeEvent(Base):
    __tablename__ = "client_life_events"

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
    # Transmission intergénérationnelle : événement vécu par un parent/ancêtre
    parent_event_id: Mapped[str | None] = mapped_column(
        ForeignKey("client_life_events.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    # Contexte sociétal de l'époque de l'événement
    era_tag: Mapped[str | None] = mapped_column(
        ForeignKey("era_contexts.tag", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    # Séance lors de laquelle l'événement a été mentionné pour la première fois
    first_mentioned_session_id: Mapped[str | None] = mapped_column(
        ForeignKey("sessions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # -- Ancrage temporel (Y) ----------------------------------------------------
    event_year_approx: Mapped[int | None] = mapped_column(Integer, nullable=True)
    client_age_at_event: Mapped[int | None] = mapped_column(Integer, nullable=True)
    life_stage: Mapped[LifeStageCode | None] = mapped_column(
        Enum(LifeStageCode, native_enum=False),
        nullable=True,
    )
    family_role: Mapped[str | None] = mapped_column(String(64), nullable=True)
    # Genre tel que vécu À ce moment précis (peut différer du genre actuel)
    gender_lived_then: Mapped[str | None] = mapped_column(String(64), nullable=True)

    # -- Nature de l'événement ---------------------------------------------------
    event_type: Mapped[EventTypeCode] = mapped_column(
        Enum(EventTypeCode, native_enum=False),
        nullable=False,
        default=EventTypeCode.autre,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    is_intergenerational: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # -- Double narration (Ricoeur) -----------------------------------------------
    # Comment c'était vécu à l'époque (reconstitué)
    narrative_then: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Comment le sujet le raconte aujourd'hui (temps Z)
    narrative_now: Mapped[str | None] = mapped_column(Text, nullable=True)

    # -- Méta --------------------------------------------------------------------
    authored_by: Mapped[AuthoredByCode] = mapped_column(
        Enum(AuthoredByCode, native_enum=False),
        nullable=False,
        default=AuthoredByCode.practitioner,
    )
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
    client = relationship("Client", back_populates="life_events")
    era = relationship("EraContext", back_populates="life_events")
    children = relationship(
        "ClientLifeEvent",
        backref="parent_event",
        foreign_keys="[ClientLifeEvent.parent_event_id]",
        remote_side="[ClientLifeEvent.id]",
    )
    first_mentioned_session = relationship(
        "SessionRecord",
        foreign_keys=[first_mentioned_session_id],
    )
    journal_entries = relationship("ClientJournalEntry", back_populates="linked_event")
    temporal_anchors = relationship("SessionTemporalAnchor", back_populates="life_event")

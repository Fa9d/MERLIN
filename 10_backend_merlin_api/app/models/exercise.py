"""Exercices — pratiques proposées au client entre les séances.

Deux tables :
- ``Exercise`` : le CATALOGUE (Atelier des lectures, administrable) — des
  pratiques sobres rédigées par des humains (jamais générées vers le client
  sans validation), formulées dans le vocabulaire autorisé (Loi 21).
- ``ClientExercise`` : la PROPOSITION — un praticien propose un exercice à un
  client (dans le cadre d'une séance) ; le client chemine à son rythme
  (propose → en_cours → termine/abandonne) et peut y déposer une note.

Un exercice est une invitation, jamais une prescription : le statut
``abandonne`` est un choix respecté, pas un échec.
"""
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.enums import ExerciseStatusCode, RecordStatus


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    code: Mapped[str] = mapped_column(String(48), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    # Consignes rédigées pour le client — vocabulaire autorisé uniquement.
    instructions: Mapped[str] = mapped_column(Text, nullable=False)
    # Axe MERLIN principal (territoire, corps, émotions…) — optionnel.
    dimension: Mapped[str | None] = mapped_column(String(32), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
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


class ClientExercise(Base):
    __tablename__ = "client_exercises"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    client_id: Mapped[str] = mapped_column(
        ForeignKey("clients.id", ondelete="CASCADE"), nullable=False, index=True
    )
    exercise_id: Mapped[str] = mapped_column(
        ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False, index=True
    )
    # Séance dans laquelle la proposition a été faite (traçabilité).
    session_id: Mapped[str | None] = mapped_column(
        ForeignKey("sessions.id", ondelete="SET NULL"), nullable=True
    )
    assigned_by_user_id: Mapped[str | None] = mapped_column(
        ForeignKey("app_users.id", ondelete="SET NULL"), nullable=True
    )
    # Mot d'accompagnement du praticien (optionnel, visible par le client).
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[ExerciseStatusCode] = mapped_column(
        Enum(ExerciseStatusCode, native_enum=False),
        nullable=False,
        default=ExerciseStatusCode.propose,
    )
    # Note du client sur son vécu de l'exercice (optionnelle).
    client_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    record_status: Mapped[RecordStatus] = mapped_column(
        Enum(RecordStatus, native_enum=False),
        nullable=False,
        default=RecordStatus.active,
    )
    proposed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    done_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

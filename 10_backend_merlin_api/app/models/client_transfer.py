"""Transferts de praticien — audit de la relation d'accompagnement.

Quand un client change de praticien (décision fondateur 2026-07-09) :
- mode ``resume`` (DÉFAUT) : le nouveau praticien repart du fil visible
  (notes validées, journal sous consentement) — le matériau brut des séances
  passées reste dans l'ancienne relation. Minimisation Loi 25 ; la parole
  confiée ne voyage pas sans son auteur.
- mode ``integral`` : accès complet transféré — exige le consentement
  explicite du client, enregistré ici et opposable.

Les séances passées gardent leur praticien historique — on ne réécrit
jamais qui a réellement reçu la personne.
"""
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ClientPractitionerTransfer(Base):
    __tablename__ = "client_practitioner_transfers"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    client_id: Mapped[str] = mapped_column(
        ForeignKey("clients.id", ondelete="CASCADE"), nullable=False, index=True
    )
    from_praticien_id: Mapped[str | None] = mapped_column(
        ForeignKey("app_users.id", ondelete="SET NULL"), nullable=True
    )
    to_praticien_id: Mapped[str | None] = mapped_column(
        ForeignKey("app_users.id", ondelete="SET NULL"), nullable=True
    )
    mode: Mapped[str] = mapped_column(String(16), nullable=False, default="resume")
    client_consent_obtained: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    transferred_by_user_id: Mapped[str | None] = mapped_column(
        ForeignKey("app_users.id", ondelete="SET NULL"), nullable=True
    )
    transferred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

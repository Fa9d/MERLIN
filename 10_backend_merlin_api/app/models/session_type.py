"""Types de séance — 3e dimension de la gouvernance des analyses.

Un type de séance (défini par l'admin dans l'Atelier des lectures) décrit la
nature de la rencontre (écoute simple, suivi en profondeur, séance express…)
et gouverne QUELLES capacités d'analyse s'y appliquent :

- ``SessionType`` : référentiel administrable (code, nom, description) ;
- ``SessionTypeCapability`` : matrice (type × capacité) — ``enabled`` autorise
  la production pour ce type, ``auto_run`` la déclenche automatiquement après
  transcription (sinon : à la demande du praticien).

Défaut PERMISSIF : une séance sans type, ou un couple (type, capacité) sans
ligne, n'est pas restreint — la vanne (profil × capacité) reste le verrou
principal ; le type de séance est un raffinement, pas un contournement.
"""
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class SessionType(Base):
    __tablename__ = "session_types"

    code: Mapped[str] = mapped_column(String(32), primary_key=True)
    label: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
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


class SessionTypeCapability(Base):
    __tablename__ = "session_type_capabilities"
    __table_args__ = (
        UniqueConstraint("session_type_code", "capability", name="uq_session_type_capability"),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    session_type_code: Mapped[str] = mapped_column(
        ForeignKey("session_types.code", ondelete="CASCADE"), nullable=False, index=True
    )
    capability: Mapped[str] = mapped_column(String(64), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    auto_run: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

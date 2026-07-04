"""Moteur d'analyse MERLIN — capacités, credentials praticiens, résultats, traçabilité.

Architecture « moteur plein / vannes par profil » :

- Le moteur d'analyse tourne toujours à pleine capacité (prosodie, sémantique,
  profilage, connecteurs SaaS…). Les sorties brutes sont stockées avec un
  **niveau de sensibilité** (`observation` → `recherche`).
- Ce qui varie selon le contexte, c'est **l'exposition** : des interrupteurs
  par (profil de déploiement × capacité) filtrent les sorties à la lecture,
  jamais à la production (voir ``app/services/capability_gate.py``).
- Profils : ``ivia_quebec_client`` (Loi 25/21, triade O/H/O), ``praticien_certifie``
  (accès complet réservé aux praticiens vérifiés), ``recherche_societale``
  (agrégats, SaaS externes autorisés).

Tier praticien certifié :

- ``PractitionerCredential`` : reconnaissance par un ordre/instance (OPQ,
  OTSTCFQ…), vérifiée par un admin. Un praticien vérifié voit les inférences
  complètes ; il ne peut les **transmettre à un client** que si son credential
  porte ``recognized_by_order=True``.
- Toute consultation d'une sortie de niveau ``inference_clinique`` ou
  ``recherche`` est journalisée (``AnalysisAccessLog``) — preuve de conformité.
"""
from __future__ import annotations

import enum
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


def _uuid() -> str:
    return str(uuid4())


def _now() -> datetime:
    return datetime.now(timezone.utc)


class AnalysisSensitivity(str, enum.Enum):
    """Niveau de sensibilité d'une sortie d'analyse (ordre croissant)."""

    observation = "observation"            # descriptif factuel, exposable au client
    hypothese = "hypothese"                # hypothèse prudente (triade O/H/O)
    inference_clinique = "inference_clinique"  # réservé praticien vérifié
    recherche = "recherche"                # réservé profil recherche/agrégats


class CredentialStatus(str, enum.Enum):
    pending = "pending"
    verified = "verified"
    revoked = "revoked"
    expired = "expired"


class AnalysisCapabilityFlag(Base):
    """Interrupteur (profil × capacité). Le catalogue des capacités vit dans
    ``capability_gate.CAPABILITIES`` ; l'absence de ligne = valeur par défaut du profil."""

    __tablename__ = "analysis_capability_flags"

    profile: Mapped[str] = mapped_column(String(64), primary_key=True)
    capability: Mapped[str] = mapped_column(String(64), primary_key=True)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    updated_by_user_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now, onupdate=_now
    )


class PractitionerCredential(Base):
    """Reconnaissance professionnelle d'un praticien (ordre, permis, portée)."""

    __tablename__ = "practitioner_credentials"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    practitioner_user_id: Mapped[str] = mapped_column(
        ForeignKey("app_users.id"), nullable=False, index=True
    )
    order_body: Mapped[str] = mapped_column(String(160), nullable=False)  # ex. OPQ, OTSTCFQ
    license_number: Mapped[str | None] = mapped_column(String(80), nullable=True)
    scope_notes: Mapped[str | None] = mapped_column(Text, nullable=True)  # portée reconnue
    status: Mapped[CredentialStatus] = mapped_column(
        Enum(CredentialStatus, native_enum=False),
        nullable=False,
        default=CredentialStatus.pending,
        index=True,
    )
    # Vrai = l'instance appropriée reconnaît au praticien le droit de transmettre
    # au client des contenus de niveau inference_clinique.
    recognized_by_order: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    verified_by_user_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now
    )


class AnalysisResult(Base):
    """Sortie brute d'un analyseur, stockée à pleine capacité, filtrée à la lecture."""

    __tablename__ = "analysis_results"
    __table_args__ = (
        Index("ix_analysis_results_subject", "client_id", "capability"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    capability: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    sensitivity: Mapped[AnalysisSensitivity] = mapped_column(
        Enum(AnalysisSensitivity, native_enum=False), nullable=False, index=True
    )
    client_id: Mapped[str | None] = mapped_column(
        ForeignKey("clients.id"), nullable=True, index=True
    )
    recording_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    session_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    engine_version: Mapped[str | None] = mapped_column(String(64), nullable=True)
    payload_json: Mapped[str] = mapped_column(Text, nullable=False)  # JSON sérialisé
    created_by_user_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now, index=True
    )


class AnalysisAccessLog(Base):
    """Journal d'accès aux sorties sensibles (inference_clinique / recherche)."""

    __tablename__ = "analysis_access_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    user_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    analysis_result_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    client_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    sensitivity: Mapped[str] = mapped_column(String(32), nullable=False)
    context: Mapped[str | None] = mapped_column(String(160), nullable=True)
    accessed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now, index=True
    )

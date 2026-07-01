"""Profilage comportemental à 5 couches (MERLIN).

Posture (constitution IVIA, opposable) : ces profils sont des OBSERVATIONS /
HYPOTHÈSES versionnées, **jamais des diagnostics**. `status` défaut = `hypothese`,
provenance tracée, validation humaine possible, lien de consentement (Loi 25),
classe de sensibilité `high`.

Conception : append-only versionné. Un layer = une table ; chaque ré-évaluation
crée une nouvelle ligne (`version` +1, `is_current=True`, l'ancienne passe à False).
Le « score courant » = la ligne `is_current` (un index UNIQUE partiel garantit
qu'il n'y en a qu'une par sujet/layer). L'historique = toutes les lignes d'un même
(sujet, layer). Sujet polymorphe : client OU praticien (pour le matching).

Les scores sont normalisés [0,1] sauf VAD (valence/arousal/dominance : [-1,1]).
"""
from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, declared_attr, mapped_column
from sqlalchemy.sql import text

from app.db.base import Base
from app.models.enums import (
    AttachmentStyle,
    DataSensitivityClass,
    JungianFunction,
    ProfileSource,
    ProfileStatus,
    ProfileSubjectKind,
    RecordStatus,
)


def _uuid() -> str:
    return str(uuid4())


class ProfileLayerMixin:
    """Colonnes communes à toutes les couches (sujet, version, traçabilité, gouvernance)."""

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)

    # ── Sujet polymorphe : exactement un des deux (cf. CheckConstraint) ──
    subject_kind: Mapped[ProfileSubjectKind] = mapped_column(
        Enum(ProfileSubjectKind, native_enum=False), nullable=False, index=True
    )

    @declared_attr
    def client_id(cls) -> Mapped[str | None]:
        return mapped_column(
            ForeignKey("clients.id", ondelete="CASCADE"), nullable=True, index=True
        )

    @declared_attr
    def practitioner_user_id(cls) -> Mapped[str | None]:
        return mapped_column(
            ForeignKey("app_users.id", ondelete="CASCADE"), nullable=True, index=True
        )

    # ── Versionnement (append-only) ──
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    is_current: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    assessed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    valid_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # ── Traçabilité & gouvernance (Loi 21 / Loi 25) ──
    source: Mapped[ProfileSource] = mapped_column(
        Enum(ProfileSource, native_enum=False),
        nullable=False,
        default=ProfileSource.self_report,
    )
    instrument: Mapped[str | None] = mapped_column(String(64), nullable=True)  # ex. "BFI-2", "PVQ-21"
    status: Mapped[ProfileStatus] = mapped_column(
        Enum(ProfileStatus, native_enum=False),
        nullable=False,
        default=ProfileStatus.hypothese,
    )
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)  # [0,1]

    @declared_attr
    def assessed_by_user_id(cls) -> Mapped[str | None]:
        return mapped_column(ForeignKey("app_users.id", ondelete="SET NULL"), nullable=True)

    @declared_attr
    def validated_by_user_id(cls) -> Mapped[str | None]:
        return mapped_column(ForeignKey("app_users.id", ondelete="SET NULL"), nullable=True)

    validated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    @declared_attr
    def consent_id(cls) -> Mapped[str | None]:
        # Le consentement (N2/N3) qui autorise ce profilage — Loi 25.
        return mapped_column(ForeignKey("consents.id", ondelete="SET NULL"), nullable=True)

    data_sensitivity_class: Mapped[DataSensitivityClass] = mapped_column(
        Enum(DataSensitivityClass, native_enum=False),
        nullable=False,
        default=DataSensitivityClass.high,
    )
    record_status: Mapped[RecordStatus] = mapped_column(
        Enum(RecordStatus, native_enum=False), nullable=False, default=RecordStatus.active
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    raw_payload: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON brut de l'instrument

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


def _common_table_args(table: str) -> tuple:
    """Contraintes + index communs : sujet exclusif, profil courant UNIQUE, matching."""
    return (
        CheckConstraint(
            "(subject_kind = 'client' AND client_id IS NOT NULL AND practitioner_user_id IS NULL) "
            "OR (subject_kind = 'practitioner' AND practitioner_user_id IS NOT NULL "
            "AND client_id IS NULL)",
            name=f"ck_{table}_subject_exclusive",
        ),
        # Un seul profil COURANT par client (intégrité + lecture rapide)
        Index(
            f"uq_{table}_client_current",
            "client_id",
            unique=True,
            postgresql_where=text("is_current AND client_id IS NOT NULL"),
        ),
        # Un seul profil COURANT par praticien
        Index(
            f"uq_{table}_prat_current",
            "practitioner_user_id",
            unique=True,
            postgresql_where=text("is_current AND practitioner_user_id IS NOT NULL"),
        ),
        # Matching : balayer tous les profils courants d'un type de sujet (index partiel)
        Index(
            f"ix_{table}_subject_current",
            "subject_kind",
            postgresql_where=text("is_current"),
        ),
    )


# ── Couche 1 — Traits stables : Big Five OCEAN ────────────────────────────────
class TraitProfileOcean(ProfileLayerMixin, Base):
    __tablename__ = "profile_traits_ocean"

    openness: Mapped[float | None] = mapped_column(Float, nullable=True)
    conscientiousness: Mapped[float | None] = mapped_column(Float, nullable=True)
    extraversion: Mapped[float | None] = mapped_column(Float, nullable=True)
    agreeableness: Mapped[float | None] = mapped_column(Float, nullable=True)
    neuroticism: Mapped[float | None] = mapped_column(Float, nullable=True)

    __table_args__ = (
        *_common_table_args("profile_traits_ocean"),
        Index(
            "ix_ocean_match",
            "extraversion",
            "agreeableness",
            "neuroticism",
            postgresql_where=text("is_current"),
        ),
    )


# ── Couche 2 — Valeurs profondes : Schwartz (10 valeurs) ──────────────────────
class ValueProfileSchwartz(ProfileLayerMixin, Base):
    __tablename__ = "profile_values_schwartz"

    self_direction: Mapped[float | None] = mapped_column(Float, nullable=True)
    stimulation: Mapped[float | None] = mapped_column(Float, nullable=True)
    hedonism: Mapped[float | None] = mapped_column(Float, nullable=True)
    achievement: Mapped[float | None] = mapped_column(Float, nullable=True)
    power: Mapped[float | None] = mapped_column(Float, nullable=True)
    security: Mapped[float | None] = mapped_column(Float, nullable=True)
    conformity: Mapped[float | None] = mapped_column(Float, nullable=True)
    tradition: Mapped[float | None] = mapped_column(Float, nullable=True)
    benevolence: Mapped[float | None] = mapped_column(Float, nullable=True)
    universalism: Mapped[float | None] = mapped_column(Float, nullable=True)

    __table_args__ = (
        *_common_table_args("profile_values_schwartz"),
        Index(
            "ix_schwartz_match",
            "benevolence",
            "universalism",
            "security",
            postgresql_where=text("is_current"),
        ),
    )


# ── Couche 3 — Style relationnel : 8 Expressions de l'Amour ───────────────────
class RelationalProfileLove(ProfileLayerMixin, Base):
    __tablename__ = "profile_relational_love"

    # 8 expressions (noms internes ; libellés configurables côté référentiel)
    paroles_valorisantes: Mapped[float | None] = mapped_column(Float, nullable=True)
    moments_qualite: Mapped[float | None] = mapped_column(Float, nullable=True)
    contact_physique: Mapped[float | None] = mapped_column(Float, nullable=True)
    services_rendus: Mapped[float | None] = mapped_column(Float, nullable=True)
    cadeaux: Mapped[float | None] = mapped_column(Float, nullable=True)
    soutien_emotionnel: Mapped[float | None] = mapped_column(Float, nullable=True)
    espace_autonomie: Mapped[float | None] = mapped_column(Float, nullable=True)
    engagement_fiabilite: Mapped[float | None] = mapped_column(Float, nullable=True)

    __table_args__ = (
        *_common_table_args("profile_relational_love"),
        Index(
            "ix_love_match",
            "moments_qualite",
            "soutien_emotionnel",
            "paroles_valorisantes",
            postgresql_where=text("is_current"),
        ),
    )


# ── Couche 4 — Style d'attachement : Bartholomew (4 quadrants) ────────────────
class AttachmentProfileBartholomew(ProfileLayerMixin, Base):
    __tablename__ = "profile_attachment_bartholomew"

    # Scores par quadrant (proéminence relative)
    secure_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    preoccupied_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    dismissing_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    fearful_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    # Axes sous-jacents : modèle de soi (anxiété), modèle de l'autre (évitement)
    self_model_anxiety: Mapped[float | None] = mapped_column(Float, nullable=True)
    other_model_avoidance: Mapped[float | None] = mapped_column(Float, nullable=True)
    primary_style: Mapped[AttachmentStyle | None] = mapped_column(
        Enum(AttachmentStyle, native_enum=False), nullable=True, index=True
    )

    __table_args__ = (
        *_common_table_args("profile_attachment_bartholomew"),
        Index(
            "ix_attach_match",
            "primary_style",
            postgresql_where=text("is_current"),
        ),
    )


# ── Couche 5 — État dynamique : Circumplex VAD (Valence-Arousal-Dominance) ────
class StateProfileVad(ProfileLayerMixin, Base):
    __tablename__ = "profile_state_vad"

    valence: Mapped[float | None] = mapped_column(Float, nullable=True)    # [-1,1]
    arousal: Mapped[float | None] = mapped_column(Float, nullable=True)    # [-1,1]
    dominance: Mapped[float | None] = mapped_column(Float, nullable=True)  # [-1,1]

    __table_args__ = (
        *_common_table_args("profile_state_vad"),
        # L'état est volatil : on requête souvent le plus récent dans une fenêtre
        Index("ix_vad_recent", "client_id", "assessed_at"),
        Index(
            "ix_vad_match",
            "valence",
            "arousal",
            postgresql_where=text("is_current"),
        ),
    )


# ── Couche 6 — Types jungiens : attitude + 4 fonctions ────────────────────────
class TypeProfileJungian(ProfileLayerMixin, Base):
    """Jung : repères de compréhension de soi (individuation), **jamais** un
    diagnostic ni une case exposée au client. Cf.
    `00_DOCTRINE/INDIVIDUATION_cadre_jungien_v0.1.md`. Proéminences [0,1]."""

    __tablename__ = "profile_types_jungian"

    # Attitude : proéminence introvertie (extraversion = pôle opposé)
    introversion: Mapped[float | None] = mapped_column(Float, nullable=True)
    # 4 fonctions psychiques (proéminence relative) — se comprendre, pas se classer
    thinking: Mapped[float | None] = mapped_column(Float, nullable=True)   # pensée
    feeling: Mapped[float | None] = mapped_column(Float, nullable=True)    # sentiment
    sensing: Mapped[float | None] = mapped_column(Float, nullable=True)    # sensation
    intuition: Mapped[float | None] = mapped_column(Float, nullable=True)  # intuition
    # Fonction dominante (repère, jamais exposée telle quelle au client)
    dominant_function: Mapped[JungianFunction | None] = mapped_column(
        Enum(JungianFunction, native_enum=False), nullable=True, index=True
    )

    __table_args__ = (
        *_common_table_args("profile_types_jungian"),
        Index(
            "ix_jung_match",
            "dominant_function",
            "introversion",
            postgresql_where=text("is_current"),
        ),
    )

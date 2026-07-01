"""Schémas du profilage comportemental à 5 couches.

GARDE-FOU (constitution IVIA, opposable) :
- Ces profils sont des OBSERVATIONS / HYPOTHÈSES, jamais des diagnostics.
- Le `...Read` complet (scores) est réservé aux rôles internes (praticien/superviseur/
  admin), sous validation humaine. Le client NE reçoit JAMAIS ses scores bruts ni
  une étiquette catégorielle : il reçoit, au besoin, une restitution prudente en
  langage IVIA (Observation → Hypothèse → Orientation), via `ClientFacingProfileView`.
- Toute création doit référencer le consentement (N2/N3) qui l'autorise.
"""
from __future__ import annotations

from datetime import datetime

from pydantic import Field

from app.models.enums import (
    AttachmentStyle,
    JungianFunction,
    ProfileSource,
    ProfileStatus,
    ProfileSubjectKind,
)
from app.schemas.common import MerlinSchema


# ── Base commune (création) ───────────────────────────────────────────────────
class ProfileLayerCreate(MerlinSchema):
    """Champs communs de création. Le sujet (client_id/practitioner_user_id) et le
    consentement sont fournis/validés côté service, pas par le client final."""

    subject_kind: ProfileSubjectKind
    client_id: str | None = None
    practitioner_user_id: str | None = None
    source: ProfileSource = ProfileSource.self_report
    instrument: str | None = Field(default=None, max_length=64)
    status: ProfileStatus = ProfileStatus.hypothese  # jamais 'diagnostic'
    confidence: float | None = Field(default=None, ge=0, le=1)
    consent_id: str | None = None
    valid_until: datetime | None = None
    notes: str | None = None
    raw_payload: str | None = None


class ProfileLayerRead(MerlinSchema):
    """Lecture INTERNE (praticien/superviseur/admin) — inclut les métadonnées."""

    id: str
    subject_kind: ProfileSubjectKind
    client_id: str | None = None
    practitioner_user_id: str | None = None
    version: int
    is_current: bool
    assessed_at: datetime
    valid_until: datetime | None = None
    source: ProfileSource
    instrument: str | None = None
    status: ProfileStatus
    confidence: float | None = None
    validated_by_user_id: str | None = None
    validated_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


# ── Couche 1 — OCEAN ──────────────────────────────────────────────────────────
class OceanScores(MerlinSchema):
    openness: float | None = Field(default=None, ge=0, le=1)
    conscientiousness: float | None = Field(default=None, ge=0, le=1)
    extraversion: float | None = Field(default=None, ge=0, le=1)
    agreeableness: float | None = Field(default=None, ge=0, le=1)
    neuroticism: float | None = Field(default=None, ge=0, le=1)


class OceanCreate(ProfileLayerCreate, OceanScores):
    pass


class OceanRead(ProfileLayerRead, OceanScores):
    pass


# ── Couche 2 — Schwartz ───────────────────────────────────────────────────────
class SchwartzScores(MerlinSchema):
    self_direction: float | None = Field(default=None, ge=0, le=1)
    stimulation: float | None = Field(default=None, ge=0, le=1)
    hedonism: float | None = Field(default=None, ge=0, le=1)
    achievement: float | None = Field(default=None, ge=0, le=1)
    power: float | None = Field(default=None, ge=0, le=1)
    security: float | None = Field(default=None, ge=0, le=1)
    conformity: float | None = Field(default=None, ge=0, le=1)
    tradition: float | None = Field(default=None, ge=0, le=1)
    benevolence: float | None = Field(default=None, ge=0, le=1)
    universalism: float | None = Field(default=None, ge=0, le=1)


class SchwartzCreate(ProfileLayerCreate, SchwartzScores):
    pass


class SchwartzRead(ProfileLayerRead, SchwartzScores):
    pass


# ── Couche 3 — 8 Expressions de l'Amour ───────────────────────────────────────
class LoveScores(MerlinSchema):
    paroles_valorisantes: float | None = Field(default=None, ge=0, le=1)
    moments_qualite: float | None = Field(default=None, ge=0, le=1)
    contact_physique: float | None = Field(default=None, ge=0, le=1)
    services_rendus: float | None = Field(default=None, ge=0, le=1)
    cadeaux: float | None = Field(default=None, ge=0, le=1)
    soutien_emotionnel: float | None = Field(default=None, ge=0, le=1)
    espace_autonomie: float | None = Field(default=None, ge=0, le=1)
    engagement_fiabilite: float | None = Field(default=None, ge=0, le=1)


class LoveCreate(ProfileLayerCreate, LoveScores):
    pass


class LoveRead(ProfileLayerRead, LoveScores):
    pass


# ── Couche 4 — Bartholomew ────────────────────────────────────────────────────
class AttachmentScores(MerlinSchema):
    secure_score: float | None = Field(default=None, ge=0, le=1)
    preoccupied_score: float | None = Field(default=None, ge=0, le=1)
    dismissing_score: float | None = Field(default=None, ge=0, le=1)
    fearful_score: float | None = Field(default=None, ge=0, le=1)
    self_model_anxiety: float | None = Field(default=None, ge=0, le=1)
    other_model_avoidance: float | None = Field(default=None, ge=0, le=1)
    primary_style: AttachmentStyle | None = None


class AttachmentCreate(ProfileLayerCreate, AttachmentScores):
    pass


class AttachmentRead(ProfileLayerRead, AttachmentScores):
    pass


# ── Couche 5 — VAD (état dynamique) ───────────────────────────────────────────
class VadScores(MerlinSchema):
    valence: float | None = Field(default=None, ge=-1, le=1)
    arousal: float | None = Field(default=None, ge=-1, le=1)
    dominance: float | None = Field(default=None, ge=-1, le=1)


class VadCreate(ProfileLayerCreate, VadScores):
    pass


class VadRead(ProfileLayerRead, VadScores):
    pass


# ── Couche 6 — Types jungiens (attitude + 4 fonctions) ────────────────────────
class JungianScores(MerlinSchema):
    # Attitude : proéminence introvertie [0,1] (extraversion = pôle opposé)
    introversion: float | None = Field(default=None, ge=0, le=1)
    # 4 fonctions psychiques — proéminence relative, pour se comprendre (pas se classer)
    thinking: float | None = Field(default=None, ge=0, le=1)
    feeling: float | None = Field(default=None, ge=0, le=1)
    sensing: float | None = Field(default=None, ge=0, le=1)
    intuition: float | None = Field(default=None, ge=0, le=1)
    dominant_function: JungianFunction | None = None


class JungianCreate(ProfileLayerCreate, JungianScores):
    pass


class JungianRead(ProfileLayerRead, JungianScores):
    pass


# ── Vue orientée CLIENT — jamais de scores bruts ni d'étiquette ───────────────
class ClientFacingProfileView(MerlinSchema):
    """Restitution prudente au client : aucun score, aucune catégorie diagnostique.

    Le service compose `observation`/`hypothese`/`orientation` en langage IVIA, à
    partir des couches internes, sous validation humaine. Vocabulaire Loi 21 filtré.
    """

    observation: str
    hypothese: str
    orientation: str
    updated_at: datetime | None = None

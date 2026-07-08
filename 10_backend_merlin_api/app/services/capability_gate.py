"""Vanne de capacités — filtre l'exposition des analyses, jamais leur production.

Principes (décision fondateur, 2026-07-04) :

- Le moteur produit toujours tout (« maximum des capacités d'analyse »).
- L'exposition est gouvernée par (profil de déploiement × capacité) — réglable
  en un clic depuis la console admin (``/admin/analysis-capabilities``).
- Le profil ``ivia_quebec_client`` reste conforme Loi 25 / Loi 21 : analyses
  locales uniquement, sorties limitées à observation/hypothèse (triade O/H/O).
- Les praticiens **vérifiés** (credential ``verified``) accèdent aux inférences
  complètes ; la transmission au client exige ``recognized_by_order``.
- Tout accès à une sortie ``inference_clinique``/``recherche`` est journalisé.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.analysis import (
    AnalysisAccessLog,
    AnalysisCapabilityFlag,
    AnalysisResult,
    AnalysisSensitivity,
    CredentialStatus,
    PractitionerCredential,
)
from app.models.app_user import AppUser

logger = logging.getLogger("merlin.capability_gate")

# ── Catalogue des capacités (source de vérité, versionnée en code) ────────────
# max_sensitivity = niveau maximal que cette capacité peut produire.
CAPABILITIES: dict[str, dict] = {
    "prosody_local": {
        "label": "Analyse prosodique locale (débit, pauses, F0, énergie)",
        "category": "prosody",
        "max_sensitivity": AnalysisSensitivity.inference_clinique,
        "data_leaves_server": False,
    },
    "emotion_saas": {
        "label": "Analyse émotionnelle via API SaaS externe",
        "category": "prosody",
        "max_sensitivity": AnalysisSensitivity.recherche,
        "data_leaves_server": True,
    },
    "semantic_llm": {
        "label": "Analyse sémantique LLM (Anthropic)",
        "category": "semantic",
        "max_sensitivity": AnalysisSensitivity.inference_clinique,
        "data_leaves_server": True,
    },
    "semantic_embeddings": {
        "label": "Embeddings sémantiques locaux (recherche inter-séances)",
        "category": "semantic",
        "max_sensitivity": AnalysisSensitivity.hypothese,
        "data_leaves_server": False,
    },
    "behavioral_profiling": {
        "label": "Profilage comportemental 5 couches",
        "category": "profiling",
        "max_sensitivity": AnalysisSensitivity.inference_clinique,
        "data_leaves_server": True,
    },
    "societal_aggregation": {
        "label": "Agrégats sociétaux anonymisés",
        "category": "research",
        "max_sensitivity": AnalysisSensitivity.recherche,
        "data_leaves_server": False,
    },
    "carte_de_vie": {
        "label": "Carte de Vie — lecture multidimensionnelle (axes, tensions, triade O/H/O)",
        "category": "lecture",
        "max_sensitivity": AnalysisSensitivity.hypothese,
        "data_leaves_server": False,
    },
}

# ── Profils de déploiement et défauts ────────────────────────────────────────
# Défaut par profil : capacité activée ? (surchargeable en DB, un clic admin)
PROFILES: dict[str, dict] = {
    "ivia_quebec_client": {
        "label": "IVIA Québec — client (Loi 25/21, écoute enracinée)",
        "max_sensitivity": AnalysisSensitivity.hypothese,
        # Décision fondateur 2026-07-04 : tout actif par défaut en phase test —
        # désactivation en un clic depuis /admin/analysis/capabilities au besoin
        # (à réévaluer avant mise en marché pour les capacités data_leaves_server).
        # Reconfirmée le 2026-07-08 (emotion_saas reste active par défaut).
        "defaults": {c: True for c in CAPABILITIES},
    },
    "praticien_certifie": {
        "label": "Praticien certifié — accès analytique complet",
        "max_sensitivity": AnalysisSensitivity.inference_clinique,
        "defaults": {c: True for c in CAPABILITIES},
    },
    "recherche_societale": {
        "label": "Recherche sociétale — pleine capacité + SaaS",
        "max_sensitivity": AnalysisSensitivity.recherche,
        "defaults": {c: True for c in CAPABILITIES},
    },
}

_SENSITIVITY_ORDER = [
    AnalysisSensitivity.observation,
    AnalysisSensitivity.hypothese,
    AnalysisSensitivity.inference_clinique,
    AnalysisSensitivity.recherche,
]


def sensitivity_rank(level: AnalysisSensitivity | str) -> int:
    if isinstance(level, str):
        level = AnalysisSensitivity(level)
    return _SENSITIVITY_ORDER.index(level)


# ── Interrupteurs ─────────────────────────────────────────────────────────────
def is_capability_enabled(db: Session, profile: str, capability: str) -> bool:
    """Interrupteur effectif : ligne DB si présente, sinon défaut du profil."""
    if capability not in CAPABILITIES or profile not in PROFILES:
        return False
    row = db.get(AnalysisCapabilityFlag, (profile, capability))
    if row is not None:
        return bool(row.enabled)
    return bool(PROFILES[profile]["defaults"].get(capability, False))


def set_capability(
    db: Session, profile: str, capability: str, enabled: bool, updated_by: str | None
) -> None:
    row = db.get(AnalysisCapabilityFlag, (profile, capability))
    if row is None:
        row = AnalysisCapabilityFlag(profile=profile, capability=capability, enabled=enabled)
    else:
        row.enabled = enabled
    row.updated_by_user_id = updated_by
    db.add(row)


def capability_matrix(db: Session) -> dict[str, dict[str, bool]]:
    """Matrice complète {profil: {capacité: activée}} pour la console admin."""
    return {
        profile: {cap: is_capability_enabled(db, profile, cap) for cap in CAPABILITIES}
        for profile in PROFILES
    }


# ── Credentials praticiens ────────────────────────────────────────────────────
def active_credential(db: Session, practitioner_user_id: str) -> PractitionerCredential | None:
    """Credential vérifié et non expiré du praticien, s'il existe."""
    now = datetime.now(timezone.utc)
    rows = db.execute(
        select(PractitionerCredential).where(
            PractitionerCredential.practitioner_user_id == practitioner_user_id,
            PractitionerCredential.status == CredentialStatus.verified,
        )
    ).scalars().all()
    for row in rows:
        if row.expires_at is not None and row.expires_at.replace(tzinfo=row.expires_at.tzinfo or timezone.utc) < now:
            continue
        return row
    return None


def profile_for_user(db: Session, user: AppUser) -> str:
    """Profil d'exposition effectif d'un utilisateur."""
    role = getattr(user.role, "value", user.role)
    if role in ("practitioner", "operator", "supervisor", "admin_tech"):
        if active_credential(db, user.id) is not None:
            return "praticien_certifie"
    return "ivia_quebec_client"


def max_sensitivity_for_user(db: Session, user: AppUser) -> AnalysisSensitivity:
    return PROFILES[profile_for_user(db, user)]["max_sensitivity"]


def can_transmit_to_client(db: Session, practitioner_user_id: str) -> bool:
    """Vrai si le praticien peut livrer au client des contenus inference_clinique."""
    cred = active_credential(db, practitioner_user_id)
    return cred is not None and bool(cred.recognized_by_order)


# ── Filtrage + traçabilité à la lecture ───────────────────────────────────────
def filter_results(
    db: Session,
    user: AppUser,
    results: list[AnalysisResult],
    *,
    context: str | None = None,
) -> list[AnalysisResult]:
    """Ne retourne que les sorties visibles pour l'utilisateur ; journalise les accès sensibles."""
    profile = profile_for_user(db, user)
    ceiling = sensitivity_rank(PROFILES[profile]["max_sensitivity"])
    visible: list[AnalysisResult] = []
    for r in results:
        if not is_capability_enabled(db, profile, r.capability):
            continue
        if sensitivity_rank(r.sensitivity) > ceiling:
            continue
        if sensitivity_rank(r.sensitivity) >= sensitivity_rank(AnalysisSensitivity.inference_clinique):
            db.add(
                AnalysisAccessLog(
                    user_id=user.id,
                    analysis_result_id=r.id,
                    client_id=r.client_id,
                    sensitivity=getattr(r.sensitivity, "value", str(r.sensitivity)),
                    context=context,
                )
            )
        visible.append(r)
    return visible

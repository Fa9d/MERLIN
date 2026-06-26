"""Service de profilage comportemental — écriture versionnée + adaptateurs ORM↔dict.

Garde-fous de sécurité (cf. SECURITY_REVIEW_PROFILAGE_v1.0) :
- **B2** : `record_layer` REFUSE l'écriture sans `consent_id`.
- bascule `is_current` atomique (l'ancien courant passe à False).
- **journalisation** des événements critiques SANS valeurs/scores en clair (F-LOG-1).
- garde d'urgence déterministe sur les champs libres (B4).

Aucune route ici ; aucune exposition. Migration `0039` requise avant usage réel en base.
"""
from __future__ import annotations

import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.behavioral_profile import (
    AttachmentProfileBartholomew,
    RelationalProfileLove,
    StateProfileVad,
    TraitProfileOcean,
    ValueProfileSchwartz,
)
from app.models.enums import ProfileSource, ProfileSubjectKind
from app.services.intake_analysis import analyse_intake_text
from app.services.profile_matching import LAYER_DIMENSIONS

logger = logging.getLogger("merlin.profiling")

LAYER_MODELS = {
    "ocean": TraitProfileOcean,
    "schwartz": ValueProfileSchwartz,
    "love": RelationalProfileLove,
    "attachment": AttachmentProfileBartholomew,
    "vad": StateProfileVad,
}


class ConsentRequiredError(PermissionError):
    """B2 — toute écriture de profil exige un consentement (Loi 25)."""


class EmergencyDetectedError(RuntimeError):
    """B4 — un signal d'urgence interdit la production d'un profil/insight."""

    def __init__(self, signals: list[str]):
        self.signals = signals
        super().__init__("Signal d'urgence détecté — profilage interrompu, escalade humaine.")


# ── Garde d'urgence (B4) ──────────────────────────────────────────────────────
def guard_free_text(free_text: str | None) -> None:
    """Lève EmergencyDetectedError si un champ libre révèle une urgence (déterministe)."""
    if not free_text:
        return
    result = analyse_intake_text(free_text)
    if getattr(result, "suggested_urgency", "non_urgent") != "non_urgent":
        codes = [getattr(s, "code", str(s)) for s in getattr(result, "signals", [])]
        logger.warning("URGENCE détectée dans un champ libre de profilage — escalade. signals=%s", codes)
        raise EmergencyDetectedError(codes)


# ── Adaptateurs ORM → dict (pour matching / insights) ─────────────────────────
def row_to_scores(layer: str, row) -> dict:
    """Convertit une ligne ORM en dict de scores {dimension: valeur} (+ primary_style)."""
    dims = LAYER_DIMENSIONS.get(layer, [])
    out = {d: getattr(row, d, None) for d in dims}
    if layer == "attachment":
        out["primary_style"] = getattr(row, "primary_style", None)
        if out["primary_style"] is not None:
            out["primary_style"] = getattr(out["primary_style"], "value", out["primary_style"])
    return out


def _subject_filter(model, *, client_id, practitioner_user_id):
    if client_id is not None:
        return model.client_id == client_id
    return model.practitioner_user_id == practitioner_user_id


def get_current_profile(db: Session, *, client_id: str | None = None,
                        practitioner_user_id: str | None = None) -> dict[str, dict]:
    """Profil 5 couches COURANT d'un sujet, au format attendu par le matcher/insights."""
    profile: dict[str, dict] = {}
    for layer, model in LAYER_MODELS.items():
        row = db.scalar(
            select(model)
            .where(_subject_filter(model, client_id=client_id, practitioner_user_id=practitioner_user_id))
            .where(model.is_current.is_(True))
        )
        if row is not None:
            profile[layer] = row_to_scores(layer, row)
    return profile


# ── Écriture versionnée (B2 + bascule is_current + journalisation) ────────────
def record_layer(
    db: Session,
    *,
    layer: str,
    scores: dict,
    subject_kind: ProfileSubjectKind,
    consent_id: str | None,
    client_id: str | None = None,
    practitioner_user_id: str | None = None,
    source: ProfileSource = ProfileSource.self_report,
    assessed_by_user_id: str | None = None,
    instrument: str | None = None,
):
    """Enregistre une nouvelle version d'une couche. REFUSE sans consentement (B2)."""
    if layer not in LAYER_MODELS:
        raise ValueError(f"Couche inconnue : {layer}")
    if consent_id is None:
        raise ConsentRequiredError("Écriture de profil refusée : consentement (consent_id) requis.")
    if (client_id is None) == (practitioner_user_id is None):
        raise ValueError("Exactement un sujet attendu (client_id XOR practitioner_user_id).")

    model = LAYER_MODELS[layer]
    prev = db.scalar(
        select(model)
        .where(_subject_filter(model, client_id=client_id, practitioner_user_id=practitioner_user_id))
        .where(model.is_current.is_(True))
    )
    version = (prev.version + 1) if prev else 1
    if prev is not None:
        prev.is_current = False
        db.add(prev)

    row = model(
        subject_kind=subject_kind,
        client_id=client_id,
        practitioner_user_id=practitioner_user_id,
        version=version,
        is_current=True,
        consent_id=consent_id,
        source=source,
        assessed_by_user_id=assessed_by_user_id,
        instrument=instrument,
        **scores,
    )
    db.add(row)
    db.flush()

    subject_id = client_id or practitioner_user_id
    # Journalisation SANS valeurs/scores (F-LOG-1) : qui/quoi/quand/consentement.
    logger.info(
        "profil enregistré layer=%s subject_kind=%s subject=%s version=%s consent=%s source=%s",
        layer, subject_kind.value, subject_id, version, consent_id, source.value,
    )
    return row

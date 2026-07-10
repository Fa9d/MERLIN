"""Croisement prosodie × sémantique — capacité `croisement_prosodie_semantique`.

Étape 3b du chantier Analyses : lecture croisée du COMMENT (prosodie mesurée
localement) et du QUOI (synthèse sémantique) d'une même séance. Première
capacité de sensibilité `inference_clinique` — la route exige un praticien
VÉRIFIÉ (credential actif → profil `praticien_certifie`).

Entrées : les deux `AnalysisResult` existants de la séance (`prosody_local`
et `semantic_llm`) — le croisement ne réanalyse rien, il confronte des
lectures déjà produites et tracées.

Garde-fous :
- Constitution intégrale malgré le niveau de sensibilité : hypothèses de
  travail au conditionnel, jamais de diagnostic ; bloc `limites` OBLIGATOIRE
  (la prosodie n'est ni un détecteur de mensonge ni un détecteur de trouble).
- Pas de filtre lexical Loi 21 ici : la sortie n'est NI client NI publique
  (le filtre s'applique aux surfaces client — .claude/rules/safety.md) et un
  praticien vérifié a besoin d'un langage de travail prudent mais précis.
  L'exposition reste sous vanne + accès journalisés ; la transmission client
  exige `recognized_by_order` (droit distinct).
- Coût/activation : plafond et modèle des insights, `settings.insights_enabled`.
- Confidentialité : aucun contenu de séance dans les logs.
"""
from __future__ import annotations

import json
import logging
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai.anthropic_session_note_pipeline import _extract_json_payload
from app.ai.prompt_loader import load_prompt
from app.models.analysis import AnalysisResult
from app.models.session import SessionRecord
from app.services.behavioral_insights import (
    BehavioralInsightsError,
    _bump_daily,
    _call_claude,
    _check_daily_cap,
)
from app.services import llm_ledger

logger = logging.getLogger("merlin.croisement")

CROISEMENT_PROMPT_ID = "PROD-ANA-003"
ENGINE_VERSION = "croisement-v1.0"

_REQUIRED_KEYS = {"registre_vocal", "croisements", "synthese", "limites"}
_CROISEMENT_TYPES = {"convergence", "divergence"}


class CroisementError(RuntimeError):
    pass


def _latest_result(db: Session, session_id: str, capability: str) -> AnalysisResult | None:
    return db.scalar(
        select(AnalysisResult)
        .where(
            AnalysisResult.session_id == session_id,
            AnalysisResult.capability == capability,
        )
        .order_by(AnalysisResult.created_at.desc())
    )


def build_input(db: Session, record: SessionRecord) -> dict[str, Any]:
    """Assemble les deux lectures existantes ; lève si l'une manque."""
    prosodie = _latest_result(db, record.id, "prosody_local")
    semantique = _latest_result(db, record.id, "semantic_llm")
    if prosodie is None:
        raise CroisementError(
            "Aucune analyse prosodique pour cette séance — produire prosody_local d'abord."
        )
    if semantique is None:
        raise CroisementError(
            "Aucune synthèse sémantique pour cette séance — produire semantic_llm d'abord."
        )
    return {
        "prosodie": json.loads(prosodie.payload_json),
        "semantique": json.loads(semantique.payload_json),
        "contexte": {
            "numero_seance": record.session_sequence_number,
        },
    }


def _validate(payload: dict[str, Any]) -> dict[str, Any]:
    missing = _REQUIRED_KEYS - payload.keys()
    if missing:
        raise CroisementError(f"Croisement incomplet, clés manquantes : {sorted(missing)}")
    if not str(payload.get("limites", "")).strip():
        raise CroisementError("Bloc 'limites' vide — obligatoire (la mesure n'est pas un verdict).")
    croisements = payload.get("croisements")
    if not isinstance(croisements, list):
        raise CroisementError("Bloc 'croisements' invalide.")
    for c in croisements:
        if not isinstance(c, dict) or c.get("type") not in _CROISEMENT_TYPES:
            raise CroisementError("Croisement sans type valide (convergence|divergence).")
        # Double ancrage : chaque croisement cite ses deux sources.
        if not str(c.get("prosodie", "")).strip() or not str(c.get("semantique", "")).strip():
            raise CroisementError("Croisement sans double ancrage (prosodie ET sémantique requis).")
    return payload


async def croiser(db: Session, record: SessionRecord) -> dict[str, Any]:
    """Produit la lecture croisée validée. Lève CroisementError ou
    BehavioralInsightsError — la route traduit en HTTP."""
    entree_dict = build_input(db, record)

    _check_daily_cap()
    template = load_prompt(CROISEMENT_PROMPT_ID)
    entree = json.dumps(entree_dict, ensure_ascii=False, indent=2)
    prompt = f"{template}\n\n## Entrée (les deux lectures)\n```json\n{entree}\n```\n"

    raw, usage = await _call_claude(prompt, max_tokens=4096)
    _bump_daily()
    llm_ledger.record(db, purpose="croisement", usage=usage,
                      session_id=record.id, client_id=record.client_id,
                      praticien_user_id=record.praticien_id)
    result = _validate(_extract_json_payload(raw))

    logger.info(
        "croisement OK session=%s croisements=%s in=%s out=%s",
        record.id, len(result["croisements"]),
        usage.get("input_tokens"), usage.get("output_tokens"),
    )
    return result


__all__ = [
    "ENGINE_VERSION",
    "BehavioralInsightsError",
    "CroisementError",
    "build_input",
    "croiser",
]

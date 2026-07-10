"""Reflet de séance — restitution DIRECTE au client autonome (voix enregistrée).

Décision fondateur 2026-07-10 (`00_GOUVERNANCE/IVIA_DECISION_MODE_AUTONOME_
SEANCE_v1.0.md`) : deuxième sortie IA→client sans relecture praticien, sous
le MÊME triple verrou que le reflet de journal :

1. safety suite dédiée `seance_client_safety_suite_v1` ≥ 0.90 (registre) ;
2. filtre Loi 21 EN CODE sur toute la voix du reflet (échec = rien ne sort) ;
3. protocole d'urgence : signal détecté → ressources de crise (9-8-8, 8-1-1)
   INJECTÉES EN CODE, reflet réduit à la présence, aucune analyse.

Autres gardes : UN reflet par enregistrement (idempotent — le second appel
renvoie l'existant) ; sa matière seulement (l'enregistrement appartient au
client connecté — vérifié par la route) ; plafond quotidien global des
insights ; aucun contenu de transcript dans les logs. Ce reflet n'est PAS
le compte rendu praticien : la lecture professionnelle reste sur sa voie
validée (analysis_deliveries).
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
from app.services import llm_ledger
from app.services.behavioral_insights import (
    BehavioralInsightsError,
    _bump_daily,
    _call_claude,
    _check_daily_cap,
)
from app.services.loi21_filter import Loi21ViolationError, assert_client_safe

logger = logging.getLogger("merlin.session_reflection")

SEANCE_REFLET_PROMPT_ID = "PROD-ANA-006"
ENGINE_VERSION = "seance-reflet-v1.0"
MAX_TRANSCRIPT_CHARS = 24_000  # ~30-40 min de parole ; au-delà on tronque (dit au modèle)

RESSOURCES_URGENCE = (
    "Ce que tu as dit mérite une présence humaine, maintenant. Tu peux "
    "appeler ou texter le 9-8-8 (Ligne d'aide en cas de crise, 24/7) ou le "
    "8-1-1 option 2 (Info-Social). Si tu es en danger immédiat, appelle le "
    "9-1-1. Ta parole reste là — et toi aussi, on l'espère de tout cœur."
)

_REQUIRED_KEYS = {"reflet", "fils", "question_ouverte", "piste", "vigilance", "ressources"}
_VIGILANCE_LEVELS = {"aucun", "attention", "urgence"}


class SeanceRefletError(RuntimeError):
    pass


def existing_reflet(db: Session, record_id: str) -> AnalysisResult | None:
    """Un reflet par enregistrement : s'il existe déjà, on rend l'existant."""
    return db.scalar(
        select(AnalysisResult)
        .where(
            AnalysisResult.session_id == record_id,
            AnalysisResult.capability == "seance_reflet_client",
        )
        .order_by(AnalysisResult.created_at.desc())
    )


def build_input(record: SessionRecord) -> dict[str, Any]:
    transcript = (record.transcript_text or "").strip()
    if not transcript:
        raise SeanceRefletError(
            "La transcription n'est pas encore prête — reviens dans un moment."
        )
    truncated = len(transcript) > MAX_TRANSCRIPT_CHARS
    if truncated:
        transcript = transcript[:MAX_TRANSCRIPT_CHARS]
    return {
        "date": record.created_at.isoformat(),
        "duree_minutes": record.duration_minutes,
        "transcript_tronque": truncated,
        "transcript": transcript,
    }


def _validate(payload: dict[str, Any]) -> dict[str, Any]:
    missing = _REQUIRED_KEYS - payload.keys()
    if missing:
        raise SeanceRefletError(f"Reflet incomplet, clés manquantes : {sorted(missing)}")
    vig = payload.get("vigilance")
    if not isinstance(vig, dict) or vig.get("niveau") not in _VIGILANCE_LEVELS:
        raise SeanceRefletError("Bloc 'vigilance' invalide.")
    return payload


def _texts_of(payload: dict[str, Any]):
    yield payload.get("reflet", "")
    for f in payload.get("fils") or []:
        yield from (str(f.get("titre", "")), str(f.get("echo", "")))
    yield payload.get("question_ouverte", "")
    yield payload.get("piste", "")


def _post_filter(payload: dict[str, Any]) -> dict[str, Any]:
    """Pare-feu Loi 21 EN CODE sur toute la voix du reflet (mêmes raisons que
    le reflet de journal : la surface est le client, on filtre TOUT)."""
    for text in _texts_of(payload):
        if text:
            assert_client_safe(str(text))
    return payload


def _normalize(t: str) -> str:
    """Normalisation pour la comparaison de citations : espaces réduits et
    apostrophes/guillemets typographiques ramenés aux formes droites — le
    modèle écrit « l’eau » là où le transcript porte « l'eau »."""
    t = (t.replace("’", "'").replace("ʼ", "'")
         .replace("“", '"').replace("”", '"'))
    return " ".join(t.split())


def assert_verbatims_fideles(payload: dict[str, Any], transcript: str) -> dict[str, Any]:
    """Verrou EN CODE : toute citation « … » doit être une sous-chaîne contiguë
    du transcript (espaces normalisés). Le prompt l'exige ; le code le GARANTIT —
    une citation lissée ou reconstruite ne sort jamais vers le client."""
    import re

    haystack = _normalize(transcript)
    for text in _texts_of(payload):
        for quote in re.findall(r"«\s*(.*?)\s*»", str(text)):
            if quote and _normalize(quote) not in haystack:
                raise SeanceRefletError(
                    "Citation non fidèle au transcript — reflet rejeté (réessaie)."
                )
    return payload


def _apply_urgence_protocol(payload: dict[str, Any]) -> dict[str, Any]:
    """Verrou 3 : ressources injectées EN CODE, analyse neutralisée."""
    if payload["vigilance"]["niveau"] == "urgence":
        payload["ressources"] = RESSOURCES_URGENCE
        payload["fils"] = []
        payload["question_ouverte"] = ""
        payload["piste"] = ""
    return payload


async def generate_seance_reflet(db: Session, record: SessionRecord) -> dict[str, Any]:
    """Produit le reflet validé + filtré + protocole appliqué. La route stocke.

    L'appartenance de l'enregistrement au client connecté est vérifiée PAR LA
    ROUTE avant l'appel — ici on ne traite que la matière.
    """
    entree_dict = build_input(record)
    _check_daily_cap()
    template = load_prompt(SEANCE_REFLET_PROMPT_ID)
    entree = json.dumps(entree_dict, ensure_ascii=False, indent=2)
    prompt = f"{template}\n\n## Entrée (ta parole enregistrée)\n```json\n{entree}\n```\n"

    raw, usage = await _call_claude(prompt)
    _bump_daily()
    llm_ledger.record(
        db, purpose="seance_reflet_client", usage=usage,
        session_id=record.id, client_id=record.client_id,
    )
    payload = _validate(_extract_json_payload(raw))
    assert_verbatims_fideles(payload, entree_dict["transcript"])
    payload = _apply_urgence_protocol(_post_filter(payload))

    niveau = payload["vigilance"]["niveau"]
    if niveau == "urgence":
        logger.warning(
            "seance_reflet VIGILANCE URGENCE client=%s session=%s (mode autonome)",
            record.client_id, record.id,
        )
    logger.info(
        "seance_reflet OK client=%s session=%s vigilance=%s in=%s out=%s",
        record.client_id, record.id, niveau,
        usage.get("input_tokens"), usage.get("output_tokens"),
    )
    return payload


__all__ = [
    "ENGINE_VERSION",
    "MAX_TRANSCRIPT_CHARS",
    "RESSOURCES_URGENCE",
    "BehavioralInsightsError",
    "Loi21ViolationError",
    "SeanceRefletError",
    "assert_verbatims_fideles",
    "existing_reflet",
    "generate_seance_reflet",
]

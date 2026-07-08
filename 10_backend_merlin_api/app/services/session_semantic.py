"""Synthèse sémantique d'une séance transcrite — capacité `semantic_llm`.

Étape 3a du chantier Analyses (cadrage) : lecture du transcript d'une séance
(thèmes, moments marquants, triade O/H/O). Prompt `PROD-ANA-002` (11_PROMPTS,
jamais en dur) → Claude (patron httpx du repo) → JSON structuré stocké comme
`AnalysisResult` (sensibilité `hypothese`, sous vanne).

Garde-fous :
- **Matière** : transcript de LA séance uniquement (produit localement par
  faster-whisper sous les consentements captés en séance) ; tronqué au-delà
  d'un plafond de caractères, avec marqueur explicite `[...]`.
- **Post-filtre Loi 21** sur toutes les sorties textuelles.
- **Vigilance** : `urgence` propagée telle quelle et journalisée en WARNING —
  l'escalade reste humaine.
- **Coût / activation** : plafond quotidien et modèle des insights
  (`MERLIN_INSIGHTS_*`), interrupteur `settings.insights_enabled` côté route.
- **Confidentialité** : aucun contenu de séance dans les logs.
"""
from __future__ import annotations

import json
import logging
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai.anthropic_session_note_pipeline import _extract_json_payload
from app.ai.prompt_loader import load_prompt
from app.models.client_intention import ClientIntention
from app.models.enums import IntentionStatusCode, RecordStatus
from app.models.session import SessionRecord
from app.models.session_note import SessionNote
from app.services.behavioral_insights import (
    BehavioralInsightsError,
    _bump_daily,
    _call_claude,
    _check_daily_cap,
)
from app.services.loi21_filter import Loi21ViolationError, assert_client_safe

logger = logging.getLogger("merlin.session_semantic")

SESSION_PROMPT_ID = "PROD-ANA-002"
ENGINE_VERSION = "session-semantic-v1.0"

# Plafond de matière envoyée au modèle : au-delà, on garde le début et la fin
# (l'ouverture et la fermeture d'une séance portent souvent l'essentiel du mouvement).
MAX_TRANSCRIPT_CHARS = 30_000
_HEAD_CHARS = 10_000

_REQUIRED_KEYS = {"synthese", "themes", "moments", "axes_touches", "focus_prevu", "vigilance", "triade"}
_VIGILANCE_LEVELS = {"aucun", "attention", "urgence"}


class SessionSemanticError(RuntimeError):
    pass


# ── Matière ───────────────────────────────────────────────────────────────────


def _truncate_transcript(text: str) -> tuple[str, bool]:
    if len(text) <= MAX_TRANSCRIPT_CHARS:
        return text, False
    tail = MAX_TRANSCRIPT_CHARS - _HEAD_CHARS
    return f"{text[:_HEAD_CHARS]}\n[...]\n{text[-tail:]}", True


def build_input(db: Session, record: SessionRecord) -> tuple[dict[str, Any], bool]:
    transcript, truncated = _truncate_transcript(record.transcript_text or "")
    intentions = list(
        db.execute(
            select(ClientIntention)
            .where(
                ClientIntention.client_id == record.client_id,
                ClientIntention.record_status == RecordStatus.active,
                ClientIntention.status == IntentionStatusCode.active,
            )
            .order_by(ClientIntention.created_at.desc())
            .limit(10)
        ).scalars()
    )
    # Focus proposé par la dernière note validée AVANT cette séance
    previous_note = db.scalar(
        select(SessionNote)
        .where(
            SessionNote.client_id == record.client_id,
            SessionNote.session_id != record.id,
            SessionNote.validated_by_practitioner.is_(True),
            SessionNote.record_status == RecordStatus.active,
        )
        .order_by(SessionNote.created_at.desc())
    )
    return (
        {
            "transcript": transcript,
            "intentions_actives": [i.text for i in intentions],
            "focus_prevu": previous_note.next_session_focus_text if previous_note else None,
        },
        truncated,
    )


# ── Validation + pare-feu Loi 21 ──────────────────────────────────────────────


def _validate(payload: dict[str, Any]) -> dict[str, Any]:
    missing = _REQUIRED_KEYS - payload.keys()
    if missing:
        raise SessionSemanticError(f"Synthèse incomplète, clés manquantes : {sorted(missing)}")
    vig = payload.get("vigilance")
    if not isinstance(vig, dict) or vig.get("niveau") not in _VIGILANCE_LEVELS:
        raise SessionSemanticError("Bloc 'vigilance' invalide.")
    triade = payload.get("triade")
    if not isinstance(triade, dict) or {"observation", "hypothese", "orientation"} - triade.keys():
        raise SessionSemanticError("Bloc 'triade' invalide.")
    return payload


def _texts_of(payload: dict[str, Any]):
    yield payload["synthese"]
    for th in payload.get("themes") or []:
        yield from (th.get("titre", ""), th.get("observation", ""), th.get("hypothese", ""))
    for m in payload.get("moments") or []:
        yield m.get("lecture", "")  # le verbatim est la parole du client — non filtré
    fp = payload.get("focus_prevu")
    if isinstance(fp, dict):
        yield fp.get("commentaire", "")
    yield from payload["triade"].values()


def _post_filter(payload: dict[str, Any]) -> dict[str, Any]:
    """Pare-feu Loi 21 sur la voix de l'ANALYSE (pas sur les verbatims du client)."""
    for text in _texts_of(payload):
        if text:
            assert_client_safe(str(text))
    return payload


# ── Pipeline ──────────────────────────────────────────────────────────────────


async def synthesize_session(db: Session, record: SessionRecord) -> dict[str, Any]:
    """Produit la synthèse validée + filtrée (dict, avec drapeau `transcript_tronque`).

    Lève SessionSemanticError (transcript absent, sortie invalide),
    Loi21ViolationError ou BehavioralInsightsError — la route traduit en HTTP.
    """
    if not (record.transcript_text or "").strip():
        raise SessionSemanticError("Aucun transcript pour cette séance.")

    _check_daily_cap()
    entree_dict, truncated = build_input(db, record)
    template = load_prompt(SESSION_PROMPT_ID)
    entree = json.dumps(entree_dict, ensure_ascii=False, indent=2)
    prompt = f"{template}\n\n## Entrée (séance)\n```json\n{entree}\n```\n"

    raw, usage = await _call_claude(prompt)
    _bump_daily()
    result = _post_filter(_validate(_extract_json_payload(raw)))
    result["transcript_tronque"] = truncated

    niveau = result["vigilance"]["niveau"]
    if niveau == "urgence":
        logger.warning(
            "session_semantic VIGILANCE URGENCE client=%s session=%s",
            record.client_id, record.id,
        )
    logger.info(
        "session_semantic OK session=%s tronque=%s vigilance=%s in=%s out=%s",
        record.id, truncated, niveau,
        usage.get("input_tokens"), usage.get("output_tokens"),
    )
    return result


__all__ = [
    "ENGINE_VERSION",
    "MAX_TRANSCRIPT_CHARS",
    "BehavioralInsightsError",
    "Loi21ViolationError",
    "SessionSemanticError",
    "synthesize_session",
]

"""Retour de pratique — analyse franche du praticien sur sa propre pratique.

Décision fondateur 2026-07-09 : FRANC JEU — constats directs et ancrés sur
SES retours, pistes de travail concrètes, pas d'enrobage. Les seules limites
sont structurelles : clients protégés à travers ses notes, pas d'étiquette
clinique, supervision nommée (pas remplacée), protocole de détresse.
Prompt `PROD-ANA-005`, capacité `praticien_reflet`.

Garde-fous :
- Matière : SES retours uniquement (`practitioner_journal_entries`) —
  fenêtre 30 jours, 40 retours max ; cooldown 20 h.
- Protocole de détresse EN CODE : signal → ressources injectées serveur
  (9-8-8, 8-1-1, pair/supervision), analyse neutralisée.
- Pas de filtre lexical Loi 21 : surface praticien-sur-lui-même, ni client
  ni publique (même choix documenté que le croisement) — le prompt interdit
  néanmoins toute étiquette sur le praticien et tout profilage des clients
  à travers ses notes (verrou = safety suite dédiée).
- Confidentialité : aucun contenu dans les logs ; les retours ne nourrissent
  JAMAIS les analyses des clients.
"""
from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta, timezone
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai.anthropic_session_note_pipeline import _extract_json_payload
from app.ai.prompt_loader import load_prompt
from app.models.analysis import AnalysisResult
from app.models.enums import RecordStatus
from app.models.practitioner_journal import PractitionerJournalEntry
from app.services.behavioral_insights import (
    BehavioralInsightsError,
    _bump_daily,
    _call_claude,
    _check_daily_cap,
)

logger = logging.getLogger("merlin.practice_reflection")

PRATIQUE_PROMPT_ID = "PROD-ANA-005"
ENGINE_VERSION = "praticien-reflet-v1.0"
WINDOW_DAYS = 30
COOLDOWN_HOURS = 20

RESSOURCES_DETRESSE = (
    "Ce que tu portes là mérite une présence humaine, pas un miroir. Tu peux "
    "appeler ou texter le 9-8-8 (24/7) ou le 8-1-1 option 2 (Info-Social) — "
    "et joindre un pair ou ta supervision sans attendre le prochain rendez-vous. "
    "Accompagner ne veut pas dire porter seul."
)

_REQUIRED_KEYS = {"reflet", "constats", "pistes", "vigilance", "ressources"}
_VIGILANCE_LEVELS = {"aucun", "attention", "urgence"}


class PratiqueRefletError(RuntimeError):
    pass


class PratiqueCooldownError(PratiqueRefletError):
    pass


def _last_reflet(db: Session, praticien_id: str) -> AnalysisResult | None:
    return db.scalar(
        select(AnalysisResult)
        .where(
            AnalysisResult.capability == "praticien_reflet",
            AnalysisResult.created_by_user_id == praticien_id,
        )
        .order_by(AnalysisResult.created_at.desc())
    )


def build_input(db: Session, praticien_id: str) -> dict[str, Any]:
    cutoff = datetime.now(timezone.utc) - timedelta(days=WINDOW_DAYS)
    retours = list(
        db.execute(
            select(PractitionerJournalEntry)
            .where(
                PractitionerJournalEntry.praticien_id == praticien_id,
                PractitionerJournalEntry.record_status == RecordStatus.active,
                PractitionerJournalEntry.created_at >= cutoff,
            )
            .order_by(PractitionerJournalEntry.created_at.asc())
            .limit(40)
        ).scalars()
    )
    if not retours:
        raise PratiqueRefletError(
            "Rien à refléter — dépose d'abord un retour de pratique ou deux."
        )
    dates = [r.created_at for r in retours]
    return {
        "periode": {"de": min(dates).isoformat(), "a": max(dates).isoformat()},
        "retours": [
            {
                "date": r.created_at.isoformat(),
                "texte": r.body_text,
                "seance_liee": bool(r.session_id),
            }
            for r in retours
        ],
    }


def _validate(payload: dict[str, Any]) -> dict[str, Any]:
    missing = _REQUIRED_KEYS - payload.keys()
    if missing:
        raise PratiqueRefletError(f"Reflet incomplet, clés manquantes : {sorted(missing)}")
    vig = payload.get("vigilance")
    if not isinstance(vig, dict) or vig.get("niveau") not in _VIGILANCE_LEVELS:
        raise PratiqueRefletError("Bloc 'vigilance' invalide.")
    return payload


def _apply_detresse_protocol(payload: dict[str, Any]) -> dict[str, Any]:
    """Protocole EN CODE : ressources injectées serveur, analyse neutralisée."""
    if payload["vigilance"]["niveau"] == "urgence":
        payload["ressources"] = RESSOURCES_DETRESSE
        payload["constats"] = []
        payload["pistes"] = []
    return payload


async def generate_practice_reflet(db: Session, praticien_id: str) -> dict[str, Any]:
    last = _last_reflet(db, praticien_id)
    if last is not None:
        age = datetime.now(timezone.utc) - last.created_at.replace(tzinfo=timezone.utc)
        if age < timedelta(hours=COOLDOWN_HOURS):
            raise PratiqueCooldownError(
                "Ton dernier reflet est tout récent — laisse-lui du temps, reviens demain."
            )

    entree_dict = build_input(db, praticien_id)
    _check_daily_cap()
    template = load_prompt(PRATIQUE_PROMPT_ID)
    entree = json.dumps(entree_dict, ensure_ascii=False, indent=2)
    prompt = f"{template}\n\n## Entrée (tes retours de pratique)\n```json\n{entree}\n```\n"

    raw, usage = await _call_claude(prompt)
    _bump_daily()
    payload = _apply_detresse_protocol(_validate(_extract_json_payload(raw)))

    niveau = payload["vigilance"]["niveau"]
    if niveau == "urgence":
        logger.warning("praticien_reflet DETRESSE praticien=%s", praticien_id)
    logger.info(
        "praticien_reflet OK praticien=%s vigilance=%s in=%s out=%s",
        praticien_id, niveau, usage.get("input_tokens"), usage.get("output_tokens"),
    )
    return payload


__all__ = [
    "COOLDOWN_HOURS",
    "ENGINE_VERSION",
    "RESSOURCES_DETRESSE",
    "BehavioralInsightsError",
    "PratiqueCooldownError",
    "PratiqueRefletError",
    "generate_practice_reflet",
]

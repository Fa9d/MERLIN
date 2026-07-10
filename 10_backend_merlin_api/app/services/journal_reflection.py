"""Reflet de journal — restitution DIRECTE au client (mode autonome).

Décision fondateur 2026-07-09 (`00_GOUVERNANCE/IVIA_DECISION_MODE_AUTONOME_
JOURNAL_v1.0.md`) : première sortie IA→client sans relecture praticien.
La validation humaine par restitution est remplacée par un TRIPLE VERROU :

1. safety suite dédiée `journal_client_safety_suite_v1` ≥ 0.90 (registre) ;
2. filtre Loi 21 EN CODE sur toute la voix du reflet (échec = rien ne sort) ;
3. protocole d'urgence : signal détecté → ressources de crise (9-8-8, 8-1-1)
   INJECTÉES EN CODE (jamais dépendantes du seul modèle), reflet réduit à la
   présence, aucune analyse.

Autres gardes : fenêtre = 21 jours d'écriture ; un reflet par 20 h (rythme
sain + coût) ; plafond quotidien global des insights ; aucun contenu de
journal dans les logs. Le client lit SON journal — aucun consentement tiers
requis : c'est sa matière, son reflet.
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
from app.models.client import Client
from app.models.client_intention import ClientIntention
from app.models.client_journal_entry import ClientJournalEntry
from app.models.enums import IntentionStatusCode, RecordStatus
from app.services.behavioral_insights import (
    BehavioralInsightsError,
    _bump_daily,
    _call_claude,
    _check_daily_cap,
)
from app.services import llm_ledger
from app.services.loi21_filter import Loi21ViolationError, assert_client_safe

logger = logging.getLogger("merlin.journal_reflection")

REFLET_PROMPT_ID = "PROD-ANA-004"
ENGINE_VERSION = "journal-reflet-v1.0"
WINDOW_DAYS = 21
COOLDOWN_HOURS = 20

# Ressources de crise — INJECTÉES EN CODE quand vigilance=urgence, pour ne
# jamais dépendre du seul modèle. Source : protocole du prompt PROD-ANA-004.
RESSOURCES_URGENCE = (
    "Ce que tu as écrit mérite une présence humaine, maintenant. Tu peux "
    "appeler ou texter le 9-8-8 (Ligne d'aide en cas de crise, 24/7) ou le "
    "8-1-1 option 2 (Info-Social). Si tu es en danger immédiat, appelle le "
    "9-1-1. Ton journal reste là — et toi aussi, on l'espère de tout cœur."
)

_REQUIRED_KEYS = {"reflet", "fils", "question_ouverte", "piste", "vigilance", "ressources"}
_VIGILANCE_LEVELS = {"aucun", "attention", "urgence"}


class JournalRefletError(RuntimeError):
    pass


class RefletCooldownError(JournalRefletError):
    pass


def _last_reflet(db: Session, client_id: str) -> AnalysisResult | None:
    return db.scalar(
        select(AnalysisResult)
        .where(
            AnalysisResult.client_id == client_id,
            AnalysisResult.capability == "journal_reflet_client",
        )
        .order_by(AnalysisResult.created_at.desc())
    )


def build_input(db: Session, client: Client) -> dict[str, Any]:
    cutoff = datetime.now(timezone.utc) - timedelta(days=WINDOW_DAYS)
    entries = list(
        db.execute(
            select(ClientJournalEntry)
            .where(
                ClientJournalEntry.client_id == client.id,
                ClientJournalEntry.record_status == RecordStatus.active,
                ClientJournalEntry.created_at >= cutoff,
            )
            .order_by(ClientJournalEntry.created_at.asc())
            .limit(40)
        ).scalars()
    )
    if not entries:
        raise JournalRefletError(
            "Rien à refléter pour l'instant — écris d'abord quelques lignes."
        )
    intentions = list(
        db.execute(
            select(ClientIntention)
            .where(
                ClientIntention.client_id == client.id,
                ClientIntention.record_status == RecordStatus.active,
                ClientIntention.status == IntentionStatusCode.active,
            )
            .limit(10)
        ).scalars()
    )
    dates = [e.created_at for e in entries]
    return {
        "periode": {"de": min(dates).isoformat(), "a": max(dates).isoformat()},
        "entrees": [
            {
                "date": e.created_at.isoformat(),
                "nature": getattr(e.entry_kind, "value", str(e.entry_kind)),
                "ton": e.emotional_tone,
                "axes": e.dimensions or [],
                "texte": e.body_text,
            }
            for e in entries
        ],
        "intentions_actives": [i.text for i in intentions],
    }


def _validate(payload: dict[str, Any]) -> dict[str, Any]:
    missing = _REQUIRED_KEYS - payload.keys()
    if missing:
        raise JournalRefletError(f"Reflet incomplet, clés manquantes : {sorted(missing)}")
    vig = payload.get("vigilance")
    if not isinstance(vig, dict) or vig.get("niveau") not in _VIGILANCE_LEVELS:
        raise JournalRefletError("Bloc 'vigilance' invalide.")
    return payload


def _texts_of(payload: dict[str, Any]):
    yield payload.get("reflet", "")
    for f in payload.get("fils") or []:
        yield from (str(f.get("titre", "")), str(f.get("echo", "")))
    yield payload.get("question_ouverte", "")
    yield payload.get("piste", "")


def _post_filter(payload: dict[str, Any]) -> dict[str, Any]:
    """Pare-feu Loi 21 EN CODE sur toute la voix du reflet (verbatims du client
    inclus dans `echo` : ici la surface est le client lui-même — le lexique
    reste interdit dans la voix d'IVIA, ses propres mots cités sont les siens,
    mais on filtre TOUT par prudence : un reflet peut être relu par d'autres)."""
    for text in _texts_of(payload):
        if text:
            assert_client_safe(str(text))
    return payload


def _apply_urgence_protocol(payload: dict[str, Any]) -> dict[str, Any]:
    """Verrou 3 : ressources injectées EN CODE, analyse neutralisée."""
    if payload["vigilance"]["niveau"] == "urgence":
        payload["ressources"] = RESSOURCES_URGENCE
        payload["fils"] = []          # aucune analyse sur un signal d'urgence
        payload["question_ouverte"] = ""
        payload["piste"] = ""
    return payload


async def generate_reflet(db: Session, client: Client) -> dict[str, Any]:
    """Produit le reflet validé + filtré + protocole appliqué. La route stocke."""
    last = _last_reflet(db, client.id)
    if last is not None:
        age = datetime.now(timezone.utc) - last.created_at.replace(tzinfo=timezone.utc)
        if age < timedelta(hours=COOLDOWN_HOURS):
            raise RefletCooldownError(
                "Ton dernier reflet est tout récent — laisse-lui un peu de temps, "
                "reviens demain."
            )

    entree_dict = build_input(db, client)
    _check_daily_cap()
    template = load_prompt(REFLET_PROMPT_ID)
    entree = json.dumps(entree_dict, ensure_ascii=False, indent=2)
    prompt = f"{template}\n\n## Entrée (ta période d'écriture)\n```json\n{entree}\n```\n"

    raw, usage = await _call_claude(prompt, max_tokens=2048)
    _bump_daily()
    llm_ledger.record(db, purpose="journal_reflet_client", usage=usage, client_id=client.id)
    payload = _apply_urgence_protocol(_post_filter(_validate(_extract_json_payload(raw))))

    niveau = payload["vigilance"]["niveau"]
    if niveau == "urgence":
        logger.warning("journal_reflet VIGILANCE URGENCE client=%s (mode autonome)", client.id)
    logger.info(
        "journal_reflet OK client=%s vigilance=%s in=%s out=%s",
        client.id, niveau, usage.get("input_tokens"), usage.get("output_tokens"),
    )
    return payload


__all__ = [
    "COOLDOWN_HOURS",
    "ENGINE_VERSION",
    "RESSOURCES_URGENCE",
    "BehavioralInsightsError",
    "JournalRefletError",
    "Loi21ViolationError",
    "RefletCooldownError",
    "generate_reflet",
]

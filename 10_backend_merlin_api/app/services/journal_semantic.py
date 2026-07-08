"""Synthèse sémantique du journal entre deux séances — capacité `journal_semantic`.

Étape 2 du chantier Analyses (cadrage v1.2) : le journal écrit entre les séances
nourrit la préparation de la suivante. Prompt `PROD-ANA-001` (11_PROMPTS, jamais
en dur) → Claude (patron httpx du repo, réutilisé de `behavioral_insights`) →
JSON structuré stocké comme `AnalysisResult` (sensibilité `hypothese`, sous vanne).

Garde-fous :
- **Consentement** : aucune lecture du journal sans `consent_history` actif,
  positif et non révoqué (même verrou que le dossier de préparation).
- **Post-filtre Loi 21** sur TOUTES les sorties textuelles : une formulation
  interdite fait échouer la synthèse (rien n'est stocké).
- **Vigilance** : `niveau = "urgence"` est propagé tel quel au praticien et
  journalisé en WARNING — l'escalade reste humaine, l'analyse ne décide rien.
- **Coût** : partage le plafond quotidien et le modèle des insights
  (`MERLIN_INSIGHTS_*`), activation pilotée par `settings.insights_enabled`.
- **Confidentialité** : aucun contenu de journal dans les logs.
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
from app.models.client_journal_entry import ClientJournalEntry
from app.models.consent import Consent
from app.models.enums import ConsentTypeCode, IntentionStatusCode, RecordStatus
from app.models.session import SessionRecord
from app.services.behavioral_insights import (
    BehavioralInsightsError,
    _bump_daily,
    _call_claude,
    _check_daily_cap,
)
from app.services.loi21_filter import Loi21ViolationError, assert_client_safe

logger = logging.getLogger("merlin.journal_semantic")

JOURNAL_PROMPT_ID = "PROD-ANA-001"
ENGINE_VERSION = "journal-semantic-v1.0"

_REQUIRED_KEYS = {"synthese", "fils", "axes_touches", "mouvements_intentions", "vigilance", "triade"}
_VIGILANCE_LEVELS = {"aucun", "attention", "urgence"}


class JournalSemanticError(RuntimeError):
    pass


# ── Verrou de consentement (partagé avec le dossier de préparation) ───────────


def journal_consent_active(db: Session, client_id: str) -> bool:
    """Vrai si le client a un consent_history actif, positif et non révoqué."""
    consent = db.scalar(
        select(Consent)
        .where(
            Consent.client_id == client_id,
            Consent.consent_type_code == ConsentTypeCode.consent_history,
            Consent.consent_value.is_(True),
            Consent.revoked_at.is_(None),
            Consent.record_status == RecordStatus.active,
        )
        .order_by(Consent.granted_at.desc())
    )
    return consent is not None


# ── Fenêtre inter-séances et matière ──────────────────────────────────────────


def previous_session_cutoff(db: Session, record: SessionRecord):
    """Borne temporelle : fin (ou début) de la séance précédente du même client."""
    previous = db.scalar(
        select(SessionRecord)
        .where(
            SessionRecord.client_id == record.client_id,
            SessionRecord.id != record.id,
            SessionRecord.record_status == RecordStatus.active,
            SessionRecord.session_sequence_number < record.session_sequence_number,
        )
        .order_by(SessionRecord.session_sequence_number.desc())
    )
    if previous is None:
        return None
    return previous.actual_end_at or previous.actual_start_at or previous.scheduled_start_at


def collect_journal_window(db: Session, record: SessionRecord) -> list[ClientJournalEntry]:
    """Entrées du journal depuis la séance précédente (30 max, récentes d'abord)."""
    stmt = (
        select(ClientJournalEntry)
        .where(
            ClientJournalEntry.client_id == record.client_id,
            ClientJournalEntry.record_status == RecordStatus.active,
        )
        .order_by(ClientJournalEntry.created_at.desc())
        .limit(30)
    )
    cutoff = previous_session_cutoff(db, record)
    if cutoff is not None:
        stmt = stmt.where(ClientJournalEntry.created_at >= cutoff)
    return list(db.execute(stmt).scalars())


def build_input(
    db: Session, record: SessionRecord, entries: list[ClientJournalEntry]
) -> dict[str, Any]:
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
    dates = [e.created_at for e in entries]
    return {
        "periode": {
            "de": min(dates).isoformat() if dates else None,
            "a": max(dates).isoformat() if dates else None,
        },
        "entrees": [
            {
                "date": e.created_at.isoformat(),
                "nature": getattr(e.entry_kind, "value", str(e.entry_kind)),
                "ton": e.emotional_tone,
                "axes": e.dimensions or [],
                "texte": e.body_text,
            }
            for e in reversed(entries)  # ordre chronologique pour la lecture
        ],
        "intentions_actives": [i.text for i in intentions],
    }


# ── Validation + pare-feu Loi 21 ──────────────────────────────────────────────


def _validate(payload: dict[str, Any]) -> dict[str, Any]:
    missing = _REQUIRED_KEYS - payload.keys()
    if missing:
        raise JournalSemanticError(f"Synthèse incomplète, clés manquantes : {sorted(missing)}")
    vig = payload.get("vigilance")
    if not isinstance(vig, dict) or vig.get("niveau") not in _VIGILANCE_LEVELS:
        raise JournalSemanticError("Bloc 'vigilance' invalide.")
    triade = payload.get("triade")
    if not isinstance(triade, dict) or {"observation", "hypothese", "orientation"} - triade.keys():
        raise JournalSemanticError("Bloc 'triade' invalide.")
    return payload


def _texts_of(payload: dict[str, Any]):
    yield payload["synthese"]
    for fil in payload.get("fils") or []:
        yield from (fil.get("titre", ""), fil.get("observation", ""), fil.get("hypothese", ""))
    for mv in payload.get("mouvements_intentions") or []:
        yield mv.get("indice", "")
    yield from payload["triade"].values()


def _post_filter(payload: dict[str, Any]) -> dict[str, Any]:
    """Pare-feu Loi 21 sur toute la sortie : formulation interdite → rien n'est stocké."""
    for text in _texts_of(payload):
        if text:
            assert_client_safe(str(text))
    return payload


# ── Pipeline ──────────────────────────────────────────────────────────────────


async def synthesize_journal(
    db: Session, record: SessionRecord
) -> tuple[dict[str, Any], int]:
    """Produit la synthèse (dict validé + filtré) et le nombre d'entrées lues.

    Lève JournalSemanticError (matière absente, sortie invalide),
    Loi21ViolationError (formulation interdite) ou BehavioralInsightsError
    (API indisponible / plafond) — la route traduit en HTTP.
    """
    entries = collect_journal_window(db, record)
    if not entries:
        raise JournalSemanticError("Aucune entrée de journal depuis la séance précédente.")

    _check_daily_cap()
    template = load_prompt(JOURNAL_PROMPT_ID)
    entree = json.dumps(build_input(db, record, entries), ensure_ascii=False, indent=2)
    prompt = f"{template}\n\n## Entrée (journal de la période)\n```json\n{entree}\n```\n"

    raw, usage = await _call_claude(prompt)
    _bump_daily()
    result = _post_filter(_validate(_extract_json_payload(raw)))

    niveau = result["vigilance"]["niveau"]
    if niveau == "urgence":
        # Escalade HUMAINE : on signale fort, on ne décide rien à la place du praticien.
        logger.warning(
            "journal_semantic VIGILANCE URGENCE client=%s session=%s",
            record.client_id, record.id,
        )
    logger.info(
        "journal_semantic OK session=%s entrees=%s vigilance=%s in=%s out=%s",
        record.id, len(entries), niveau,
        usage.get("input_tokens"), usage.get("output_tokens"),
    )
    return result, len(entries)


__all__ = [
    "ENGINE_VERSION",
    "BehavioralInsightsError",
    "JournalSemanticError",
    "Loi21ViolationError",
    "collect_journal_window",
    "journal_consent_active",
    "previous_session_cutoff",
    "synthesize_journal",
]

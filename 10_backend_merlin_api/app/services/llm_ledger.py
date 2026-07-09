"""Comptabilisation des appels LLM — coût réel par appel, en dollars.

Un seul point d'entrée : `record(db, ...)`, appelé juste après chaque appel
Anthropic réussi. Calcule le coût au tarif du modèle (USD / MTok) et écrit un
`LlmUsageEvent`. L'échec de comptabilisation ne doit JAMAIS faire échouer
l'analyse elle-même (best effort, journalisé).

Conversion CAD à l'affichage : taux `MERLIN_USD_CAD_RATE` (défaut 1.40) —
approximation assumée, le réel vient du relevé Anthropic/carte.
"""
from __future__ import annotations

import logging

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.llm_usage import LlmUsageEvent

logger = logging.getLogger("merlin.llm_ledger")

# Tarifs USD par million de tokens (input, output) — préfixe le plus long gagne.
# Source : grille Anthropic (vérifiée 2026-07). À tenir à jour à chaque
# changement de modèle dans MERLIN_INSIGHTS_MODEL ou le pipeline de notes.
PRICING_USD_PER_MTOK: dict[str, tuple[float, float]] = {
    "claude-fable-5": (10.0, 50.0),
    "claude-opus-4": (5.0, 25.0),
    "claude-sonnet-5": (3.0, 15.0),
    "claude-sonnet-4": (3.0, 15.0),
    "claude-haiku-4": (1.0, 5.0),
    "claude-3-5-haiku": (0.8, 4.0),
}
_DEFAULT_PRICING = (5.0, 25.0)  # inconnu → tarif Opus (prudence haute)


def pricing_for(model: str) -> tuple[float, float]:
    best: tuple[float, float] | None = None
    best_len = -1
    for prefix, rates in PRICING_USD_PER_MTOK.items():
        if model.startswith(prefix) and len(prefix) > best_len:
            best, best_len = rates, len(prefix)
    return best or _DEFAULT_PRICING


def cost_usd(model: str, input_tokens: int, output_tokens: int) -> float:
    pin, pout = pricing_for(model)
    return (input_tokens * pin + output_tokens * pout) / 1_000_000


def usd_to_cad_cents(usd: float) -> int:
    return round(usd * settings.usd_cad_rate * 100)


def record(
    db: Session,
    *,
    purpose: str,
    usage: dict | None,
    model: str | None = None,
    session_id: str | None = None,
    client_id: str | None = None,
    praticien_user_id: str | None = None,
    analysis_result_id: str | None = None,
    created_by_user_id: str | None = None,
) -> None:
    """Écrit l'événement d'usage (add + flush ; le commit suit le flux appelant).

    Best effort : toute erreur est journalisée, jamais propagée — la
    comptabilité ne casse pas l'analyse.
    """
    try:
        usage = usage or {}
        model = model or settings.insights_model
        input_tokens = int(usage.get("input_tokens") or 0)
        output_tokens = int(usage.get("output_tokens") or 0)
        db.add(
            LlmUsageEvent(
                purpose=purpose,
                model=model,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost_usd=cost_usd(model, input_tokens, output_tokens),
                session_id=session_id,
                client_id=client_id,
                praticien_user_id=praticien_user_id,
                analysis_result_id=analysis_result_id,
                created_by_user_id=created_by_user_id,
            )
        )
        db.flush()
    except Exception:  # noqa: BLE001 — la comptabilité ne casse jamais l'analyse
        logger.exception("llm_ledger.record a échoué (purpose=%s)", purpose)


__all__ = [
    "PRICING_USD_PER_MTOK",
    "cost_usd",
    "pricing_for",
    "record",
    "usd_to_cad_cents",
]

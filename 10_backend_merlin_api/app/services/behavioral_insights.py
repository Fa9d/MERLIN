"""Insights comportementaux (LLM) — activation CONTRÔLÉE (Prompt 5).

Assemble le profil 5 couches → prompt `PROD-PROF-002` (11_PROMPTS, jamais en dur) →
Claude (httpx, patron du repo) → JSON structuré + résumé client.

Garde-fous d'activation :
- **B1** : l'appel réel reste piloté par `settings.insights_enabled` (défaut False) côté route.
- **Post-filtre Loi 21** sur la sortie destinée au client (`resume_client`) : si une
  formulation interdite passe le LLM, on **refuse** (→ fallback), on journalise l'incident.
- **Fallback** : aucune exception ne remonte au client ; en cas d'échec API / dérive, on
  renvoie une dégradation sûre (`generate_with_fallback`).
- **Coût** : `max_tokens` borné + plafond souple d'appels/jour (mémoire process) + log
  d'usage (tokens, coût estimé) **sans** contenu.
- **Secrets** : clé lue depuis `settings`, jamais journalisée ni renvoyée.
"""
from __future__ import annotations

import asyncio
import json
import logging
from datetime import date
from typing import Any

import httpx

from app.ai.anthropic_session_note_pipeline import _extract_json_payload  # parseur JSON tolérant
from app.ai.prompt_loader import load_prompt
from app.core.config import settings
from app.services.loi21_filter import Loi21ViolationError, assert_client_safe

logger = logging.getLogger("merlin.profiling")

INSIGHTS_PROMPT_ID = "PROD-PROF-002"
ANTHROPIC_MESSAGES_URL = "https://api.anthropic.com/v1/messages"

_REQUIRED_KEYS = {"praticien", "tensions_internes", "ressources_exercices", "resume_client"}

# Tarifs indicatifs (cents / 1M tokens) par modèle, pour estimation de coût.
_PRICING = {"claude-sonnet-4-6": (300, 1500), "claude-opus-4-8": (500, 2500)}

# Plafond souple d'appels/jour — compteur EN MÉMOIRE PROCESS (best-effort).
# Pour un vrai garde-fou multi-process, persister (DB/Redis) — voir plan.
_DAILY_COUNT: dict[str, int] = {}


class BehavioralInsightsError(RuntimeError):
    pass


class InsightsCapExceededError(BehavioralInsightsError):
    pass


# ── Préparation de l'entrée ───────────────────────────────────────────────────
def build_insights_input(profile: dict[str, dict], *, fiabilite: str = "bonne") -> dict[str, Any]:
    layers = ("ocean", "schwartz", "love", "attachment", "vad")
    payload: dict[str, Any] = {l: profile[l] for l in layers if profile.get(l)}
    payload["fiabilite"] = fiabilite
    return payload


def render_insights_prompt(insights_input: dict[str, Any]) -> str:
    template = load_prompt(INSIGHTS_PROMPT_ID)
    entree = json.dumps(insights_input, ensure_ascii=False, indent=2)
    return f"{template}\n\n## Entrée (profil du client)\n```json\n{entree}\n```\n"


# ── Validation + post-filtre Loi 21 ───────────────────────────────────────────
def _validate(payload: dict[str, Any]) -> dict[str, Any]:
    missing = _REQUIRED_KEYS - payload.keys()
    if missing:
        raise BehavioralInsightsError(f"Insights incomplets, clés manquantes : {sorted(missing)}")
    prat = payload.get("praticien")
    if not isinstance(prat, dict) or "style_communication" not in prat:
        raise BehavioralInsightsError("Bloc 'praticien' invalide.")
    return payload


def _post_filter(payload: dict[str, Any]) -> dict[str, Any]:
    """Pare-feu Loi 21 sur la sortie destinée au client. Refuse si formulation interdite."""
    try:
        assert_client_safe(payload.get("resume_client", ""))
    except Loi21ViolationError as exc:
        logger.warning("INSIGHTS rejetés : le LLM a produit une formulation interdite (%s).", exc.matches)
        raise BehavioralInsightsError("Sortie non conforme (post-filtre Loi 21).") from exc
    return payload


# ── Coût / quota ──────────────────────────────────────────────────────────────
def _check_daily_cap() -> None:
    cap = settings.insights_daily_cap
    if cap and cap > 0:
        today = date.today().isoformat()
        if _DAILY_COUNT.get(today, 0) >= cap:
            raise InsightsCapExceededError(f"Plafond quotidien d'insights atteint ({cap}).")


def _bump_daily() -> None:
    today = date.today().isoformat()
    _DAILY_COUNT[today] = _DAILY_COUNT.get(today, 0) + 1


def _estimate_cost_cents(model: str, usage: dict) -> float:
    pin, pout = _PRICING.get(model, _PRICING["claude-sonnet-4-6"])
    return (usage.get("input_tokens", 0) * pin + usage.get("output_tokens", 0) * pout) / 1_000_000


# ── Appel Anthropic (retry, sans fuite de secret) ─────────────────────────────
async def _call_claude(prompt: str) -> tuple[str, dict]:
    if not settings.anthropic_api_key:
        raise BehavioralInsightsError("ANTHROPIC_API_KEY est absente.")
    body = {
        "model": settings.insights_model,
        "max_tokens": settings.insights_max_tokens,
        "temperature": 0.3,
        "messages": [{"role": "user", "content": prompt}],
    }
    headers = {
        "x-api-key": settings.anthropic_api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    last_exc: Exception | None = None
    async with httpx.AsyncClient(timeout=httpx.Timeout(120.0, connect=10.0)) as client:
        for attempt in range(2):  # 1 essai + 1 retry sur erreur transitoire
            try:
                resp = await client.post(ANTHROPIC_MESSAGES_URL, headers=headers, json=body)
            except httpx.HTTPError as exc:
                last_exc = exc
                await asyncio.sleep(0.5 * (attempt + 1))
                continue
            if resp.status_code in (429, 500, 502, 503, 529):
                last_exc = BehavioralInsightsError(f"Anthropic transitoire ({resp.status_code}).")
                await asyncio.sleep(0.5 * (attempt + 1))
                continue
            if resp.status_code >= 400:
                raise BehavioralInsightsError(f"Échec Anthropic ({resp.status_code}).")
            data = resp.json()
            if data.get("stop_reason") == "max_tokens":
                raise BehavioralInsightsError("Réponse tronquée (max_tokens).")
            parts = data.get("content") or []
            text = "".join(p.get("text", "") for p in parts if p.get("type") == "text")
            if not text:
                raise BehavioralInsightsError("Réponse Claude vide.")
            return text, (data.get("usage") or {})
    raise BehavioralInsightsError(f"Anthropic indisponible après retries : {last_exc}")


# ── Pipelines ─────────────────────────────────────────────────────────────────
async def generate_behavioral_insights(profile: dict[str, dict], *, fiabilite: str = "bonne") -> dict[str, Any]:
    """Pipeline strict : peut lever. Pour la route, préférer `generate_with_fallback`."""
    _check_daily_cap()
    prompt = render_insights_prompt(build_insights_input(profile, fiabilite=fiabilite))
    raw, usage = await _call_claude(prompt)
    _bump_daily()
    result = _post_filter(_validate(_extract_json_payload(raw)))
    cost = _estimate_cost_cents(settings.insights_model, usage)
    # Journalisation : usage + coût, JAMAIS le contenu ni le profil.
    logger.info(
        "insights OK model=%s in=%s out=%s cost=%.4f¢",
        settings.insights_model, usage.get("input_tokens"), usage.get("output_tokens"), cost,
    )
    return result


_FALLBACK = {
    "praticien": {
        "style_communication": "Rester à un rythme posé et à l'écoute.",
        "points_attention": ["Insight automatique indisponible — s'appuyer sur l'observation directe."],
        "approches": ["Nommer ce qui est entendu avant d'orienter."],
    },
    "tensions_internes": [],
    "ressources_exercices": [],
    "resume_client": "Votre profil est bien enregistré. Une lecture plus détaillée pourra vous être proposée plus tard.",
}


async def generate_with_fallback(profile: dict[str, dict], *, fiabilite: str = "bonne") -> dict[str, Any]:
    """Pour la route : ne lève jamais. En cas d'échec/dérive → dégradation sûre."""
    try:
        insights = await generate_behavioral_insights(profile, fiabilite=fiabilite)
        return {"ok": True, "degraded": False, "insights": insights}
    except InsightsCapExceededError as exc:
        logger.warning("insights dégradés (plafond) : %s", exc)
        return {"ok": False, "degraded": True, "reason": "cap", "insights": _FALLBACK}
    except BehavioralInsightsError as exc:
        logger.warning("insights dégradés (échec/non-conforme) : %s", exc)
        return {"ok": False, "degraded": True, "reason": "error", "insights": _FALLBACK}

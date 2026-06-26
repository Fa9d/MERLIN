"""Insights comportementaux (LLM) à partir du profil 5 couches (Prompt 5).

Assemble le profil (OCEAN, Schwartz, 8 Expressions, Attachement, VAD) en entrée du
prompt `PROD-PROF-002` (chargé depuis 11_PROMPTS, jamais en dur), appelle Claude
(même patron httpx que la note de séance), et renvoie un JSON structuré + résumé
client narratif.

Posture (constitution IVIA) : observations/hypothèses d'aide à la posture praticien,
**jamais un diagnostic**. Sortie ≤ 800 tokens, ton bienveillant, vocabulaire Loi 21.
"""
from __future__ import annotations

import json
from typing import Any

import httpx

from app.ai.prompt_loader import load_prompt
from app.ai.anthropic_session_note_pipeline import _extract_json_payload  # réutilise le parseur JSON tolérant
from app.core.config import settings

INSIGHTS_PROMPT_ID = "PROD-PROF-002"
CLAUDE_MODEL = "claude-sonnet-4-6"   # cohérent avec le pipeline existant (coût maîtrisé)
ANTHROPIC_MESSAGES_URL = "https://api.anthropic.com/v1/messages"

_REQUIRED_KEYS = {"praticien", "tensions_internes", "ressources_exercices", "resume_client"}


class BehavioralInsightsError(RuntimeError):
    pass


def build_insights_input(profile: dict[str, dict], *, fiabilite: str = "bonne") -> dict[str, Any]:
    """Normalise le profil 5 couches en entrée du prompt (couches absentes omises)."""
    layers = ("ocean", "schwartz", "love", "attachment", "vad")
    payload: dict[str, Any] = {l: profile[l] for l in layers if profile.get(l)}
    payload["fiabilite"] = fiabilite
    return payload


def render_insights_prompt(insights_input: dict[str, Any]) -> str:
    """Concatène le template (11_PROMPTS) et l'entrée JSON du profil."""
    template = load_prompt(INSIGHTS_PROMPT_ID)
    entree = json.dumps(insights_input, ensure_ascii=False, indent=2)
    return f"{template}\n\n## Entrée (profil du client)\n```json\n{entree}\n```\n"


def _validate(payload: dict[str, Any]) -> dict[str, Any]:
    missing = _REQUIRED_KEYS - payload.keys()
    if missing:
        raise BehavioralInsightsError(f"Insights incomplets, clés manquantes : {sorted(missing)}")
    prat = payload.get("praticien")
    if not isinstance(prat, dict) or "style_communication" not in prat:
        raise BehavioralInsightsError("Bloc 'praticien' invalide.")
    return payload


async def _call_claude(prompt: str) -> str:
    """Appel Anthropic (httpx) — isolé pour être monkeypatché en test."""
    if not settings.anthropic_api_key:
        raise BehavioralInsightsError("ANTHROPIC_API_KEY est absente.")
    async with httpx.AsyncClient(timeout=httpx.Timeout(120.0, connect=10.0)) as client:
        response = await client.post(
            ANTHROPIC_MESSAGES_URL,
            headers={
                "x-api-key": settings.anthropic_api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": CLAUDE_MODEL,
                "max_tokens": 1100,          # cible ≤ 800 tokens de sortie + marge
                "temperature": 0.3,           # un peu de chaleur, mais cadré
                "messages": [{"role": "user", "content": prompt}],
            },
        )
    if response.status_code >= 400:
        raise BehavioralInsightsError(f"Échec Anthropic ({response.status_code}): {response.text}")
    data = response.json()
    if data.get("stop_reason") == "max_tokens":
        raise BehavioralInsightsError("Réponse tronquée (max_tokens) : JSON incomplet.")
    parts = data.get("content") or []
    text = "".join(p.get("text", "") for p in parts if p.get("type") == "text")
    if not text:
        raise BehavioralInsightsError("Réponse Claude vide.")
    return text


async def generate_behavioral_insights(
    profile: dict[str, dict],
    *,
    fiabilite: str = "bonne",
) -> dict[str, Any]:
    """Pipeline complet : profil → prompt → Claude → JSON validé."""
    prompt = render_insights_prompt(build_insights_input(profile, fiabilite=fiabilite))
    raw = await _call_claude(prompt)
    return _validate(_extract_json_payload(raw))

from __future__ import annotations

import json
from typing import Any

import httpx

from app.ai.prompts.session_note_cercle_v1 import (
    SESSION_NOTE_CERCLE_PROMPT_VERSION,
    render_session_note_cercle_prompt,
)
from app.core.config import settings


# claude-sonnet-4-20250514 retiré le 2026-06-15 → Sonnet 4.6 (même tarif 3$/15$ par M, même API).
CLAUDE_SONNET_4_MODEL = "claude-sonnet-4-6"
ANTHROPIC_MESSAGES_URL = "https://api.anthropic.com/v1/messages"


class AnthropicSessionNoteError(RuntimeError):
    pass


def _strip_code_fence(content: str) -> str:
    """Retire un éventuel encadrement markdown ```...``` (avec ou sans langue)."""
    if not content.startswith("```"):
        return content
    lines = content.splitlines()
    if len(lines) >= 2 and lines[-1].strip().startswith("```"):
        # première ligne = ```json (ou ```), dernière ligne = ```
        return "\n".join(lines[1:-1]).strip()
    return content


def _first_json_object(content: str) -> str | None:
    """Extrait le premier objet JSON équilibré {...} d'un texte (prose autour tolérée)."""
    start = content.find("{")
    if start == -1:
        return None
    depth = 0
    in_string = False
    escaped = False
    for i in range(start, len(content)):
        ch = content[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
        else:
            if ch == '"':
                in_string = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return content[start : i + 1]
    return None


def _extract_json_payload(raw_text: str) -> dict[str, Any]:
    content = _strip_code_fence(raw_text.strip())

    # Claude peut entourer le JSON de prose ou de fences ; on tente plusieurs voies.
    candidates: list[str] = [content]
    extracted = _first_json_object(content)
    if extracted and extracted != content:
        candidates.append(extracted)

    payload: Any = None
    last_exc: json.JSONDecodeError | None = None
    for candidate in candidates:
        try:
            payload = json.loads(candidate)
            break
        except json.JSONDecodeError as exc:
            last_exc = exc
            payload = None

    if payload is None:
        raise AnthropicSessionNoteError(
            "Reponse Claude invalide: JSON non parsable."
        ) from last_exc

    if not isinstance(payload, dict):
        raise AnthropicSessionNoteError("Reponse Claude invalide: objet JSON attendu.")
    return payload


async def generate_session_note_from_transcript(
    transcript_text: str,
    *,
    session_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not settings.anthropic_api_key:
        raise AnthropicSessionNoteError("ANTHROPIC_API_KEY est absente.")

    prompt = render_session_note_cercle_prompt(
        transcript_text,
        session_context=session_context,
    )

    # Lecture longue : la génération de note (4000 tokens) peut dépasser 60 s sous charge
    # → ReadTimeout et perte de l'analyse. Marge confortable (connexion courte, lecture longue).
    async with httpx.AsyncClient(timeout=httpx.Timeout(180.0, connect=10.0)) as client:
        response = await client.post(
            ANTHROPIC_MESSAGES_URL,
            headers={
                "x-api-key": settings.anthropic_api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": CLAUDE_SONNET_4_MODEL,
                # 4000 tokens étaient trop justes : une note multi-axes complète
                # pouvait être tronquée (stop_reason=max_tokens) → JSON incomplet.
                "max_tokens": 8000,
                "temperature": 0,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            },
        )

    if response.status_code >= 400:
        raise AnthropicSessionNoteError(
            f"Echec Anthropic ({response.status_code}): {response.text}"
        )

    payload = response.json()
    if payload.get("stop_reason") == "max_tokens":
        raise AnthropicSessionNoteError(
            "Reponse Claude tronquee (max_tokens atteint) : JSON incomplet."
        )
    content_items = payload.get("content", [])
    text_parts: list[str] = []
    for item in content_items:
        if item.get("type") == "text" and item.get("text"):
            text_parts.append(item["text"])

    if not text_parts:
        raise AnthropicSessionNoteError("Reponse Claude vide.")

    parsed = _extract_json_payload("\n".join(text_parts))
    parsed.setdefault("metadata", {})
    parsed["metadata"]["model_used"] = CLAUDE_SONNET_4_MODEL
    parsed["metadata"]["prompt_version"] = SESSION_NOTE_CERCLE_PROMPT_VERSION
    parsed["metadata"]["complexity_score"] = None
    parsed["metadata"]["validated_by_practitioner"] = False
    parsed["metadata"]["practitioner_corrections"] = None
    return parsed

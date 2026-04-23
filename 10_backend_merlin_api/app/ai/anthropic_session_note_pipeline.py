from __future__ import annotations

import json
from typing import Any

import httpx

from app.ai.prompts.session_note_cercle_v1 import (
    SESSION_NOTE_CERCLE_PROMPT_VERSION,
    render_session_note_cercle_prompt,
)
from app.core.config import settings


CLAUDE_SONNET_4_MODEL = "claude-sonnet-4-20250514"
ANTHROPIC_MESSAGES_URL = "https://api.anthropic.com/v1/messages"


class AnthropicSessionNoteError(RuntimeError):
    pass


def _extract_json_payload(raw_text: str) -> dict[str, Any]:
    content = raw_text.strip()
    if content.startswith("```"):
        lines = content.splitlines()
        if len(lines) >= 3:
            content = "\n".join(lines[1:-1]).strip()

    try:
        payload = json.loads(content)
    except json.JSONDecodeError as exc:
        raise AnthropicSessionNoteError("Reponse Claude invalide: JSON non parsable.") from exc

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

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            ANTHROPIC_MESSAGES_URL,
            headers={
                "x-api-key": settings.anthropic_api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": CLAUDE_SONNET_4_MODEL,
                "max_tokens": 4000,
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

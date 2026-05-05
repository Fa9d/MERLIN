"""Chargement dynamique des prompts Markdown depuis la bibliothèque canonique 11_PROMPTS/.

Expose `load_prompt(prompt_id)` — lit les fichiers Markdown, extrait le corps
après le frontmatter YAML, et applique un cache mémoire simple.

Portée actuelle : METH-001, METH-002, METH-003 (Vague 3 Phase A).
Pour étendre la portée, ajouter une entrée dans `_PROMPT_PATHS`.
"""

from __future__ import annotations

from pathlib import Path


class PromptNotFoundError(FileNotFoundError):
    """Erreur levée quand un prompt attendu est introuvable dans 11_PROMPTS."""


_PROMPT_PATHS: dict[str, str] = {
    "METH-001": "02_METH/METH-001-quebec-context-hypotheses-v1.md",
    "METH-002": "02_METH/METH-002-quebec-context-signals-v1.md",
    "METH-003": "02_METH/METH-003-session-note-cercle-system-prompt-v1.md",
}

_PROMPT_CACHE: dict[str, str] = {}


def _prompts_root() -> Path:
    """Retourne le chemin absolu du dossier canonique 11_PROMPTS du repo MERLIN."""

    return Path(__file__).resolve().parents[3] / "11_PROMPTS"


def _read_prompt_file(path: Path) -> str:
    """Lit un fichier Markdown de prompt et retourne son contenu UTF-8."""

    return path.read_text(encoding="utf-8")


def _extract_markdown_body(markdown_text: str) -> str:
    """Extrait la section de contenu située après le deuxième délimitateur YAML `---`."""

    lines = markdown_text.splitlines()
    delimiter_positions = [idx for idx, line in enumerate(lines) if line.strip() == "---"]

    if len(delimiter_positions) >= 2:
        content_lines = lines[delimiter_positions[1] + 1 :]
        return "\n".join(content_lines).strip()

    return markdown_text.strip()


def load_prompt(prompt_id: str) -> str:
    """Charge un prompt Markdown à partir de son identifiant et applique un cache mémoire simple."""

    if prompt_id in _PROMPT_CACHE:
        return _PROMPT_CACHE[prompt_id]

    relative_path = _PROMPT_PATHS.get(prompt_id)
    if not relative_path:
        raise PromptNotFoundError(
            f"Prompt id introuvable dans la table de routage: {prompt_id}"
        )

    prompt_path = _prompts_root() / relative_path
    if not prompt_path.exists():
        raise PromptNotFoundError(
            f"Fichier prompt introuvable pour {prompt_id}: {prompt_path}"
        )

    markdown_text = _read_prompt_file(prompt_path)
    prompt_body = _extract_markdown_body(markdown_text)
    _PROMPT_CACHE[prompt_id] = prompt_body
    return prompt_body

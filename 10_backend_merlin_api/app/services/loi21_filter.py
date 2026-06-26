"""Post-filtre déterministe Loi 21 (B4) — pare-feu avant toute sortie client.

Refuse toute formulation interdite (diagnostic / pathologie / verdict) AVANT qu'un
texte n'atteigne le client. C'est un filet de sécurité *hors LLM* : même si un prompt
dérive, le texte fautif est bloqué ici. Voir `.claude/rules/safety.md`,
`managed_agents/evals/profiling_safety_suite_v1.yaml`.
"""
from __future__ import annotations

import re

# Termes interdits Loi 21 (vocabulaire clinique) + formulations de diagnostic/verdict
# spécifiques au profilage. Comparaison insensible à la casse, sur les mots.
_FORBIDDEN = [
    r"th[ée]rapeutique", r"th[ée]rapie", r"th[ée]rapeute", r"diagnostic", r"pronostic",
    r"traitement", r"gu[ée]rison", r"trouble\b", r"pathologie", r"psychoth[ée]rapie",
    r"soin clinique", r"maladie",
    # Verdicts / étiquettes figées issues du profilage
    r"trouble de l['e ]attachement", r"personnalit[ée] n[ée]vrotique",
    r"vous souffrez", r"vous [êe]tes (d[ée]pressif|anxieux|bipolaire|n[ée]vros[ée])",
]
_PATTERNS = [re.compile(p, re.IGNORECASE) for p in _FORBIDDEN]


class Loi21ViolationError(ValueError):
    """Levée quand un texte destiné au client contient une formulation interdite."""

    def __init__(self, matches: list[str]):
        self.matches = matches
        super().__init__(f"Formulation(s) interdite(s) Loi 21 : {', '.join(matches)}")


def find_violations(text: str | None) -> list[str]:
    if not text:
        return []
    found: list[str] = []
    for pat in _PATTERNS:
        m = pat.search(text)
        if m:
            found.append(m.group(0).lower())
    return found


def assert_client_safe(text: str | None) -> str:
    """Renvoie le texte s'il est sûr, sinon lève Loi21ViolationError. À appeler sur
    TOUTE chaîne destinée à un client (restitution, résumé)."""
    violations = find_violations(text)
    if violations:
        raise Loi21ViolationError(violations)
    return text or ""

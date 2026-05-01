"""
Analyse reglementaire des reponses libres d'entree client.

Aucune dependance externe (regex pur). Concu pour etre appele
sur entry_summary_text ou requested_outcome_text avant ou apres
la creation d'une IntakeRequest.

Deux familles de signaux:
  - risk_signals    : indices de detresse aigue ou de risque clinique
  - gap_signals     : signaux de non-reponse / donnees insuffisantes
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

# Chaque entree: (code, regex, niveau_urgence_suggere)
_RISK_PATTERNS: list[tuple[str, str, str]] = [
    # --- rouge: risque vital ---
    ("suicide_explicite",     r"\bsuicid",                         "urgent"),
    ("automutilation",        r"\b(me (couper|blesser|faire du mal)|automutilation|me mutiler)", "urgent"),
    ("fin_de_vie",            r"\b(en finir|plus envie de vivre|ne plus vouloir vivre|me tuer|mourir)", "urgent"),
    ("idees_noires",          r"\b(id[eé]es? noires?|pens[eé]es? noires?)",                    "urgent"),
    ("crise_aigue",           r"\b(crise (aigue|sev[eè]re)|je n('|')en peux plus|(vraiment|tres|trop) au bout)", "urgent"),
    # --- orange: surveillance ---
    ("detresse_montante",     r"\b(d[eé]sesp[eé]r[eé]|effondr[eé]|submerg[eé]|d[eé]bord[eé]|perdu[e]?)", "priority"),
    ("peur_intense",          r"\b(j('|')ai (tellement|tres|vraiment) peur|terrifi[eé]|terrifiant)", "priority"),
    ("isolement_severe",      r"\b(compl[eè]tement seul[e]?|personne autour|plus personne|abandonn[eé])", "priority"),
    ("symptome_physique",     r"\b(ne mange plus|ne dort plus|ne sort plus|cloue? au lit)",      "priority"),
    # --- jaune: a surveiller ---
    ("difficulte_quotidien",  r"\b(tr[eè]s difficile|plus capable|plus la force|a bout)",       "watch"),
    ("anxiete_mentionnee",    r"\b(anxi[eé]t[eé]|panique|attaque de panique|stresse?)",         "watch"),
    ("deuil_perte",           r"\b(deuil|perte|d[eé]c[eè]s|mort de|perdu (mon|ma|mes|son|sa))", "watch"),
    ("rupture_lien",          r"\b(s[eé]paration|rupture|divorce|quitt[eé])",                   "watch"),
]

_GAP_PATTERNS: list[tuple[str, str]] = [
    ("texte_vide",           r"^\s*$"),
    ("texte_tres_court",     r"^.{1,15}$"),           # moins de 15 caracteres
    ("reponse_generique",    r"^(oui|non|ok|rien|aucun|pas grand chose)\.?\s*$"),
    ("sans_sujet_personnel", r"(?!.*(je|j'|moi|ma|mon|mes|nous|notre|on)).{20,}"),  # long sans pronom
]

# Urgence minimale garantie par niveau suggere
_URGENCY_RANK = {"non_urgent": 0, "watch": 1, "priority": 2, "urgent": 3}
_URGENCY_FROM_RANK = {v: k for k, v in _URGENCY_RANK.items()}


# ---------------------------------------------------------------------------
# Types de retour
# ---------------------------------------------------------------------------

@dataclass
class IntakeSignal:
    code: str
    label: str
    severity: str   # "rouge" | "orange" | "jaune" | "info"


@dataclass
class IntakeAnalysisResult:
    risk_signals: list[IntakeSignal] = field(default_factory=list)
    gap_signals: list[IntakeSignal] = field(default_factory=list)
    suggested_urgency: str = "non_urgent"
    has_risk: bool = False
    has_gaps: bool = False


_SEVERITY_BY_URGENCY = {"urgent": "rouge", "priority": "orange", "watch": "jaune"}

_GAP_LABELS = {
    "texte_vide":           "Reponse libre absente",
    "texte_tres_court":     "Reponse trop courte (moins de 15 caracteres)",
    "reponse_generique":    "Reponse generique sans contenu clinique",
    "sans_sujet_personnel": "Texte sans pronom personnel — possible reponse impersonnelle",
}

_RISK_LABELS = {
    "suicide_explicite":    "Mention explicite du suicide",
    "automutilation":       "Mention d'automutilation ou de blessure intentionnelle",
    "fin_de_vie":           "Expression de vouloir en finir ou de ne plus vouloir vivre",
    "idees_noires":         "Mention d'idees noires",
    "crise_aigue":          "Indicateur de crise aigue ou de debordement severe",
    "detresse_montante":    "Indicateur de detresse montante (desespoir, effondrement)",
    "peur_intense":         "Peur intense mentionnee",
    "isolement_severe":     "Isolement severe mentionne",
    "symptome_physique":    "Symptome physique de retrait (sommeil, alimentation, mobilite)",
    "difficulte_quotidien": "Difficulte quotidienne marquee",
    "anxiete_mentionnee":   "Anxiete ou attaque de panique mentionnee",
    "deuil_perte":          "Deuil ou perte recente mentionnes",
    "rupture_lien":         "Rupture de lien (separation, divorce) mentionnee",
}


# ---------------------------------------------------------------------------
# Fonction principale
# ---------------------------------------------------------------------------

def analyse_intake_text(text: str | None, current_urgency: str = "non_urgent") -> IntakeAnalysisResult:
    """
    Analyse un texte libre d'entree et retourne les signaux detectes.

    Args:
        text: contenu de entry_summary_text ou requested_outcome_text
        current_urgency: valeur actuelle de perceived_urgency_code (pour comparaison)

    Returns:
        IntakeAnalysisResult avec listes de signaux et urgence suggeree
    """
    result = IntakeAnalysisResult()
    effective_text = text or ""
    max_urgency_rank = _URGENCY_RANK.get(current_urgency, 0)

    # --- signaux de risque ---
    for code, pattern, urgency in _RISK_PATTERNS:
        if re.search(pattern, effective_text, re.IGNORECASE):
            result.risk_signals.append(IntakeSignal(
                code=code,
                label=_RISK_LABELS.get(code, code),
                severity=_SEVERITY_BY_URGENCY.get(urgency, "jaune"),
            ))
            rank = _URGENCY_RANK.get(urgency, 0)
            if rank > max_urgency_rank:
                max_urgency_rank = rank

    # --- signaux de non-reponse ---
    for code, pattern in _GAP_PATTERNS:
        if re.search(pattern, effective_text, re.IGNORECASE | re.DOTALL):
            result.gap_signals.append(IntakeSignal(
                code=code,
                label=_GAP_LABELS.get(code, code),
                severity="info",
            ))

    result.suggested_urgency = _URGENCY_FROM_RANK.get(max_urgency_rank, "non_urgent")
    result.has_risk = len(result.risk_signals) > 0
    result.has_gaps = len(result.gap_signals) > 0
    return result

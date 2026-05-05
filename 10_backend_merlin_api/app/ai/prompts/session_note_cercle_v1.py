from __future__ import annotations

import json
from typing import Any

from app.ai.prompt_loader import load_prompt


SESSION_NOTE_CERCLE_PROMPT_VERSION = "session_note_cercle_v1"

def _parse_prompt_bullets(prompt_text: str) -> list[str]:
    """Extrait les lignes a puce Markdown (`- ...`) et retourne des chaines nettoyees."""

    bullet_lines: list[str] = []
    for raw_line in prompt_text.splitlines():
        line = raw_line.strip()
        if line.startswith("- "):
            bullet_lines.append(line[2:].strip())
    return bullet_lines


# Source: 11_PROMPTS/02_METH/METH-001-quebec-context-hypotheses-v1.md
QUEBEC_CONTEXT_HYPOTHESES = _parse_prompt_bullets(load_prompt("METH-001"))

# Source: 11_PROMPTS/02_METH/METH-002-quebec-context-signals-v1.md
QUEBEC_CONTEXT_SIGNALS = _parse_prompt_bullets(load_prompt("METH-002"))


SESSION_NOTE_CERCLE_OUTPUT_SCHEMA: dict[str, Any] = {
    "production_note": {
        "summary_text": "string",
        "observations_text": "string",
        "coeur_summary_text": "string|null",
        "corps_summary_text": "string|null",
        "esprit_summary_text": "string|null",
        "etre_summary_text": "string|null",
        "immediate_context_text": "string|null",
        "context_factors_json": [
            {
                "factor_family_code": "materiel|travail_ou_charge|logement_et_stabilite|reseau_relationnel|rapport_aux_institutions|territoire_langue_culture",
                "impact_direction_code": "support|fragilite|contrainte",
                "summary_text": "string",
            }
        ],
        "context_hypotheses_json": [
            {
                "hypothesis_code": "pression_silence_et_minimisation|pression_performance_travail|pression_isolement_relationnel|pression_honte_ambition_ou_reussite|pression_identite_collective_fragile|pression_medicalisation_du_sens|pression_deconnexion_somatique|pression_vide_de_sens_ou_de_cadre|pression_rapport_aux_institutions",
                "summary_text": "string",
                "matched_signals": ["string"],
                "primary_dimension": "coeur|corps|esprit|etre",
                "confidence_code": "faible|moyen|eleve",
            }
        ],
        "identified_tensions_json": [
            {
                "tension_code": "tension_rythme|tension_reciprocite|tension_appartenance|tension_sens|tension_dignite|tension_charge_exigences|tension_isolement|tension_insecurite|tension_confusion|tension_desorientation",
                "description": "string",
                "dimensions_impactees": ["coeur|corps|esprit|etre"],
                "intensite_presumee": "faible|moderee|marquee",
                "niveau_de_confiance": "faible|moyen|eleve",
            }
        ],
        "vigilance_level_code": "non_urgent|watch|priority|urgent",
        "vigilance_summary_text": "string",
        "next_step_type_code": "continue_to_structure|clarify_major_point|stabilize_rhythm_and_load|mobilize_relational_resource|orient_to_appropriate_service|propose_follow_up|escalate_immediate_relay",
        "follow_up_actions_text": "string|null",
        "next_session_focus_text": "string|null",
    },
    "client_delivery": {
        "client_visible_recommended": "boolean",
        "client_facing_summary_text": "string|null",
    },
    "supervision": {
        "supervision_summary_text": "string|null",
        "detected_context_signals": ["string"],
        "low_confidence_flags": ["string"],
        "excluded_from_client_delivery": ["string"],
    },
    "research": {
        "research_notes_text": "string|null",
        "experimental_hypotheses": ["string"],
    },
    "metadata": {
        "model_used": "claude-sonnet-4-20250514",
        "prompt_version": SESSION_NOTE_CERCLE_PROMPT_VERSION,
        "complexity_score": "null",
        "validated_by_practitioner": "false",
        "practitioner_corrections": "null",
    },
}


# Source: 11_PROMPTS/02_METH/METH-003-session-note-cercle-system-prompt-v1.md
SESSION_NOTE_CERCLE_SYSTEM_PROMPT = load_prompt("METH-003")


def render_session_note_cercle_prompt(
    transcript_text: str,
    *,
    session_context: dict[str, Any] | None = None,
) -> str:
    context_block = json.dumps(session_context or {}, ensure_ascii=True, indent=2)
    schema_block = json.dumps(SESSION_NOTE_CERCLE_OUTPUT_SCHEMA, ensure_ascii=True, indent=2)

    return (
        f"{SESSION_NOTE_CERCLE_SYSTEM_PROMPT}\n\n"
        "Contexte de seance:\n"
        f"{context_block}\n\n"
        "Transcription ou resume source:\n"
        f"{transcript_text}\n\n"
        "Schema JSON attendu:\n"
        f"{schema_block}\n"
    )

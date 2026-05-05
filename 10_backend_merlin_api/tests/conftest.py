"""Fixtures partagees pour les tests ROD-TEST-001-A.

Fournit :
- clear_prompt_cache : reinitialise le cache entre chaque test
- transcript_fixture  : transcription de test 40 mots (francais quebecois)
- session_context_fixture : contexte de seance minimal
- valid_session_note_json : reponse JSON Claude valide (hardcodee)
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.ai import prompt_loader


@pytest.fixture(autouse=True)
def clear_prompt_cache() -> None:
    """Reinitialise le cache de prompts avant chaque test."""
    prompt_loader._PROMPT_CACHE.clear()
    yield
    prompt_loader._PROMPT_CACHE.clear()


@pytest.fixture
def transcript_fixture() -> str:
    """Transcription de test en francais quebecois (~45 mots)."""
    return (
        "C'est une bonne seance aujourd'hui. Je me sens moins seul depuis qu'on se parle. "
        "J'ai encore de la misere au travail, le boss me met de la pression. "
        "J'arrive pas a dormir. Depuis la separation, c'est rough. "
        "Mais je commence a voir un peu de lumiere au bout du tunnel."
    )


@pytest.fixture
def session_context_fixture() -> dict:
    """Contexte de seance minimal pour tests."""
    return {
        "operator_user_id": "test-operator-001",
        "session_type": "cercle",
        "session_number": 3,
    }


@pytest.fixture
def valid_session_note_json() -> dict:
    """Reponse JSON Claude valide et complete (fixture statique)."""
    return {
        "production_note": {
            "summary_text": "Client exprime un mieux-etre progressif malgre des stresseurs persistants (travail, insomnie, separation).",
            "observations_text": "Alliance therapeutique positive. Humour present. Discours plus nuance que sessions precedentes.",
            "coeur_summary_text": "Sentiment de solitude en reduction. Lien therapeutique ressenti comme ressource.",
            "corps_summary_text": "Insomnie persistante. Fatigue mentale liee a la pression professionnelle.",
            "esprit_summary_text": "Rumination autour du milieu de travail. Cadre cognitif commence a s'assouplir.",
            "etre_summary_text": "Debut de sens post-separation. Formulation de la lumiere au bout du tunnel notable.",
            "immediate_context_text": "Separation recente. Pression patronale. Insomnie.",
            "context_factors_json": [
                {
                    "factor_family_code": "travail_ou_charge",
                    "impact_direction_code": "fragilite",
                    "summary_text": "Pression du superieur, surmenage potentiel.",
                }
            ],
            "context_hypotheses_json": [
                {
                    "hypothesis_code": "pression_performance_travail",
                    "summary_text": "Charge normalisee, honte du repos possible.",
                    "matched_signals": ["burnout_normalise", "somatisation_non_verbalisee"],
                    "primary_dimension": "corps",
                    "confidence_code": "moyen",
                }
            ],
            "identified_tensions_json": [
                {
                    "tension_code": "tension_rythme",
                    "description": "Rythme de vie non soutenable depuis la separation.",
                    "dimensions_impactees": ["corps", "coeur"],
                    "intensite_presumee": "moderee",
                    "niveau_de_confiance": "moyen",
                }
            ],
            "vigilance_level_code": "watch",
            "vigilance_summary_text": "Insomnie et pression professionnelle a surveiller. Pas de signal urgent.",
            "next_step_type_code": "continue_to_structure",
            "follow_up_actions_text": "Valider qualite du sommeil a la prochaine seance.",
            "next_session_focus_text": "Explorer strategies de regulation face a la pression patronale.",
        },
        "client_delivery": {
            "client_visible_recommended": True,
            "client_facing_summary_text": "Seance positive. Vous exprimez un mieux-etre progressif.",
        },
        "supervision": {
            "supervision_summary_text": "RAS. Alliance solide. Surveiller insomnie.",
            "detected_context_signals": ["burnout_normalise", "solitude_non_nommee"],
            "low_confidence_flags": [],
            "excluded_from_client_delivery": [],
        },
        "research": {
            "research_notes_text": None,
            "experimental_hypotheses": [],
        },
        "metadata": {
            "model_used": "claude-sonnet-4-20250514",
            "prompt_version": "session_note_cercle_v1",
            "complexity_score": None,
            "validated_by_practitioner": False,
            "practitioner_corrections": None,
        },
    }

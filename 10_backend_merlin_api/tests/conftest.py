# conftest.py
# Fixtures partagées et configuration pytest pour 10_backend_merlin_api/tests/

import pytest


# ---------------------------------------------------------------------------
# Enregistrement des marqueurs custom
# ---------------------------------------------------------------------------

def pytest_configure(config):
    """Enregistre les marqueurs pytest custom pour éviter les PytestUnknownMarkWarning."""
    config.addinivalue_line(
        "markers",
        "integration: tests nécessitant des ressources externes (API, réseau, clés). "
        "Exclure avec: pytest -m 'not integration'"
    )


# ---------------------------------------------------------------------------
# Fixtures partagées
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=False)
def clear_prompt_cache():
    """Vide le cache des prompts avant chaque test qui en a besoin."""
    from app.ai import prompt_loader
    if hasattr(prompt_loader, '_PROMPT_CACHE'):
        prompt_loader._PROMPT_CACHE.clear()
    yield
    if hasattr(prompt_loader, '_PROMPT_CACHE'):
        prompt_loader._PROMPT_CACHE.clear()


@pytest.fixture
def transcript_fixture() -> str:
    """Transcription de cercle minimale pour les tests unitaires."""
    return (
        "Animateur : Bonjour. Comment vous arrivez ?\n"
        "Alice : Fatiguée mais présente.\n"
        "Bob : Curieux, avec des questions.\n"
        "Animateur : Quel thème ce soir ?\n"
        "Alice : L'épuisement et le rythme.\n"
        "Bob : L'authenticité dans les choix.\n"
    )


@pytest.fixture
def session_context_fixture() -> dict:
    """Contexte de session minimal pour les tests."""
    return {
        "date": "2025-01-15",
        "animateur": "MERLIN",
        "participants": ["Alice", "Bob"],
        "duree_minutes": 60,
    }


@pytest.fixture
def valid_session_note_json() -> dict:
    """Note de session valide conforme à la structure SESSION_NOTE_CERCLE_OUTPUT_SCHEMA."""
    return {
        "production_note": {
            "summary_text": "Session centrée sur l'épuisement et l'authenticité.",
            "observations_text": "Alice et Bob ont exprimé des thèmes complémentaires.",
            "coeur_summary_text": None,
            "corps_summary_text": None,
            "esprit_summary_text": None,
            "etre_summary_text": None,
            "immediate_context_text": None,
            "context_factors_json": [],
            "context_hypotheses_json": [],
            "identified_tensions_json": [],
            "vigilance_level_code": "non_urgent",
            "vigilance_summary_text": "Aucun signal de vigilance détecté.",
            "next_step_type_code": "continue_to_structure",
            "follow_up_actions_text": None,
            "next_session_focus_text": None,
        },
        "client_delivery": {
            "client_visible_recommended": False,
            "client_facing_summary_text": None,
        },
        "supervision": {
            "supervision_summary_text": None,
            "detected_context_signals": [],
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

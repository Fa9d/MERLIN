# conftest.py
# Fixtures partagÃ©es et configuration pytest pour 10_backend_merlin_api/tests/

import pytest


# ---------------------------------------------------------------------------
# Enregistrement des marqueurs custom
# ---------------------------------------------------------------------------

def pytest_configure(config):
    """Enregistre les marqueurs pytest custom pour Ã©viter les PytestUnknownMarkWarning."""
    config.addinivalue_line(
        "markers",
        "integration: tests nÃ©cessitant des ressources externes (API, rÃ©seau, clÃ©s). "
        "Exclure avec: pytest -m 'not integration'"
    )


# ---------------------------------------------------------------------------
# Fixtures partagÃ©es
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
        "Alice : FatiguÃ©e mais prÃ©sente.\n"
        "Bob : Curieux, avec des questions.\n"
        "Animateur : Quel thÃ¨me ce soir ?\n"
        "Alice : L'Ã©puisement et le rythme.\n"
        "Bob : L'authenticitÃ© dans les choix.\n"
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
    """Note de session valide conforme Ã  la structure SESSION_NOTE_CERCLE_OUTPUT_SCHEMA."""
    return {
        "production_note": {
            "summary_text": "Session centrÃ©e sur l'Ã©puisement et l'authenticitÃ©.",
            "observations_text": "Alice et Bob ont exprimÃ© des thÃ¨mes complÃ©mentaires.",
            "coeur_summary_text": None,
            "corps_summary_text": None,
            "esprit_summary_text": None,
            "etre_summary_text": None,
            "immediate_context_text": None,
            "context_factors_json": [],
            "context_hypotheses_json": [],
            "identified_tensions_json": [],
            "vigilance_level_code": "non_urgent",
            "vigilance_summary_text": "Aucun signal de vigilance dÃ©tectÃ©.",
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


# ---------------------------------------------------------------------------
# Reset DB avant chaque smoke test
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def reset_app_users():
    """Vide la table AppUser avant chaque test pour garantir DB vide.

    Si la base est injoignable (ex. tests unitaires purs lancés sans Postgres local),
    la fixture saute silencieusement le reset au lieu de bloquer toute la suite. Les
    tests qui ont réellement besoin de la DB échoueront d'eux-mêmes à leur propre étape.
    """
    import socket

    from app.db.base import load_models
    from app.db.session import engine
    from app.models.app_user import AppUser
    from sqlalchemy.exc import SQLAlchemyError
    from sqlalchemy.orm import Session

    # Pré-vérification rapide : si la base Postgres est injoignable (tests sans DB locale),
    # on saute IMMÉDIATEMENT au lieu d'attendre le timeout de connexion (~30 s) à chaque test.
    # Sqlite (host vide) et toute base réellement joignable suivent le chemin normal.
    url = engine.url
    if url.get_backend_name().startswith("postgresql") and url.host:
        try:
            with socket.create_connection((url.host, url.port or 5432), timeout=1.5):
                pass
        except OSError:
            yield
            return

    try:
        load_models()
        with Session(engine) as db:
            db.query(AppUser).delete()
            db.commit()
    except SQLAlchemyError:
        # Pas de DB disponible : on n'empêche pas les tests sans DB de s'exécuter.
        pass
    yield


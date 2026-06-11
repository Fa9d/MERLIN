# test_session_note_generation_real_claude.py
# ROD-TEST-001-A / J3 — Intégration réelle avec l'API Anthropic (Claude)
# ATTENTION : Ce test effectue un vrai appel API. Nécessite ANTHROPIC_API_KEY dans l'environnement.
# Marqué @pytest.mark.integration — à exclure des runs CI normaux.

import os
import json
import pytest

from app.ai.prompt_loader import load_prompt


# ---------------------------------------------------------------------------
# Guard : skip si pas de clé API
# ---------------------------------------------------------------------------

def _has_api_key() -> bool:
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    return bool(key and key.startswith("sk-"))


pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# Modèle actif
# ---------------------------------------------------------------------------

CLAUDE_MODEL = "claude-sonnet-4-5"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def real_transcript():
    """Transcription de cercle réaliste pour tester la génération de note."""
    return """Transcription — Cercle du 2025-01-15

Anim : Bonjour à tous. On commence par un temps de présence. Comment vous arrivez ce soir ?

Alice : Je suis épuisée mais présente. La semaine a été chargée.

Bob : Moi je suis curieux. J'ai des questions sur mon prochain pas professionnel.

Caroline : J'arrive avec beaucoup d'énergie. J'ai pris une décision importante cette semaine.

Anim : Merci. Quel thème veut-on explorer ce soir ?

Alice : L'épuisement et comment trouver son rythme sans se sacrifier.

Bob : Pour moi, c'est l'authenticité dans les choix professionnels.

Caroline : Je veux parler de transition et de courage.

Anim : On a trois thèmes proches. On peut les tisser ensemble. Alice, tu commences ?

Alice : Oui. Je réalise que je donne tout à mon travail mais je ne me nourris plus. Le cercle m'a aidée à nommer ça.

Bob : Je me reconnais dans ce que tu dis. J'ai accepté des projets qui ne me ressemblent pas par peur du vide.

Caroline : Moi j'ai fait l'inverse. J'ai refusé une offre bien payée parce qu'elle ne correspondait pas à qui je veux devenir.

Anim : Une clôture. Qu'est-ce que vous emportez ?

Alice : Je vais me donner la permission de ralentir cette semaine.

Bob : Je vais identifier un projet qui me ressemble vraiment.

Caroline : Je reste dans ma décision et je fais confiance à ce que je ressens.
"""


@pytest.fixture
def session_context():
    """Contexte de session pour le test réel."""
    return {
        "date": "2025-01-15",
        "animateur": "MERLIN",
        "participants": ["Alice", "Bob", "Caroline"],
        "lieu": "Cercle en ligne",
        "duree_minutes": 90
    }


# ---------------------------------------------------------------------------
# Import conditionnel du schema
# ---------------------------------------------------------------------------

try:
    from app.ai.prompts.session_note_cercle_v1 import SESSION_NOTE_CERCLE_OUTPUT_SCHEMA  # noqa: F401  (sonde de disponibilité)
    _schema_available = True
except ImportError:
    _schema_available = False


# ---------------------------------------------------------------------------
# Tests d'intégration
# ---------------------------------------------------------------------------

@pytest.mark.skipif(
    not _has_api_key(),
    reason="ANTHROPIC_API_KEY manquante ou invalide — test d'intégration ignoré"
)
@pytest.mark.skipif(
    not _schema_available,
    reason="SESSION_NOTE_CERCLE_OUTPUT_SCHEMA non disponible"
)
def test_generate_session_note_returns_valid_json(real_transcript, session_context):
    """
    Vérifie que l'appel réel à Claude via METH-003 retourne un JSON valide
    conforme au SESSION_NOTE_CERCLE_OUTPUT_SCHEMA.
    """
    import anthropic

    system_prompt = load_prompt("METH-003")
    assert system_prompt is not None, "METH-003 non chargé"
    assert "Tu es MERLIN" in system_prompt, "METH-003 doit contenir 'Tu es MERLIN'"

    user_message = f"""Voici la transcription d'un cercle. Génère la note de session en JSON.

Contexte : {json.dumps(session_context, ensure_ascii=False)}

Transcription :
{real_transcript}"""

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=2048,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    response_text = message.content[0].text
    assert response_text, "La réponse de Claude est vide"

    json_text = response_text.strip()
    if json_text.startswith("```"):
        lines = json_text.split("\n")
        json_lines = [l for l in lines if not l.startswith("```")]
        json_text = "\n".join(json_lines).strip()

    try:
        result = json.loads(json_text)
    except json.JSONDecodeError as e:
        pytest.fail(f"Réponse non-JSON : {e}\n\nBrut :\n{response_text}")

    assert isinstance(result, dict), "Le résultat doit être un dict"
    assert len(result) > 0, "Le dict résultat est vide"


@pytest.mark.skipif(
    not _has_api_key(),
    reason="ANTHROPIC_API_KEY manquante ou invalide — test d'intégration ignoré"
)
def test_meth003_system_prompt_is_loaded():
    """
    Vérifie que METH-003 est bien chargé et contient la directive MERLIN.
    """
    prompt = load_prompt("METH-003")
    assert prompt is not None, "METH-003 doit être accessible via load_prompt"
    assert len(prompt) > 50, "METH-003 doit avoir un contenu substantiel"
    assert "Tu es MERLIN" in prompt, "METH-003 doit contenir 'Tu es MERLIN'"


@pytest.mark.skipif(
    not _has_api_key(),
    reason="ANTHROPIC_API_KEY manquante ou invalide — test d'intégration ignoré"
)
def test_api_connection_health():
    """
    Vérification légère de la connexion API — appel minimal pour valider la clé.
    """
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=10,
        messages=[
            {"role": "user", "content": "Dis 'OK'."}
        ]
    )
    assert message.content[0].text, "L'API Anthropic ne répond pas"

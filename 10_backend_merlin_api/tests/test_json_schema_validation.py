# test_json_schema_validation.py
# ROD-TEST-001-A / J2 — Validation schéma JSON sortie session note
# Critère : valider SESSION_NOTE_CERCLE_OUTPUT_SCHEMA sans appel API

import pytest
import jsonschema
from jsonschema import validate, ValidationError

from app.ai.prompts.session_note_cercle_v1 import SESSION_NOTE_CERCLE_OUTPUT_SCHEMA


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def valid_note():
    """Session note minimale valide selon le schéma."""
    return {
        "titre": "Note de session — Cercle du 2025-01-15",
        "date": "2025-01-15",
        "participants": ["Alice", "Bob"],
        "themes_principaux": ["autonomie", "transition"],
        "observations": "Les participants ont exprimé une clarté notable.",
        "recommandations": ["Suivre l'évolution du thème autonomie."],
        "niveau_energie": "élevé",
        "prochaine_etape": "Préparer le cercle de suivi."
    }


@pytest.fixture
def note_missing_required():
    """Session note sans champ requis (titre absent)."""
    return {
        "date": "2025-01-15",
        "participants": ["Alice"],
        "themes_principaux": ["autonomie"],
        "observations": "Observation.",
        "recommandations": ["Recommandation."],
        "niveau_energie": "moyen",
        "prochaine_etape": "Suite."
    }


@pytest.fixture
def note_wrong_type():
    """Session note avec type incorrect pour participants (string au lieu de liste)."""
    return {
        "titre": "Note de session",
        "date": "2025-01-15",
        "participants": "Alice, Bob",
        "themes_principaux": ["autonomie"],
        "observations": "Observation.",
        "recommandations": ["Recommandation."],
        "niveau_energie": "moyen",
        "prochaine_etape": "Suite."
    }


@pytest.fixture
def note_empty_participants():
    """Session note avec liste participants vide."""
    return {
        "titre": "Note de session",
        "date": "2025-01-15",
        "participants": [],
        "themes_principaux": ["autonomie"],
        "observations": "Observation.",
        "recommandations": [],
        "niveau_energie": "moyen",
        "prochaine_etape": "Suite."
    }


# ---------------------------------------------------------------------------
# Tests — Schéma importé et structuré
# ---------------------------------------------------------------------------

def test_schema_is_dict():
    """Le schéma doit être un dictionnaire Python valide."""
    assert isinstance(SESSION_NOTE_CERCLE_OUTPUT_SCHEMA, dict)


def test_schema_has_type_object():
    """Le schéma doit définir un objet JSON."""
    assert SESSION_NOTE_CERCLE_OUTPUT_SCHEMA.get("type") == "object"


def test_schema_has_required_fields():
    """Le schéma doit définir des champs requis."""
    required = SESSION_NOTE_CERCLE_OUTPUT_SCHEMA.get("required", [])
    assert len(required) > 0, "Le schéma doit avoir au moins un champ requis"


def test_schema_has_properties():
    """Le schéma doit définir des propriétés."""
    props = SESSION_NOTE_CERCLE_OUTPUT_SCHEMA.get("properties", {})
    assert len(props) > 0, "Le schéma doit définir des propriétés"


# ---------------------------------------------------------------------------
# Tests — Validation données valides
# ---------------------------------------------------------------------------

def test_valid_note_passes_schema(valid_note):
    """Une note valide doit passer la validation sans erreur."""
    validate(instance=valid_note, schema=SESSION_NOTE_CERCLE_OUTPUT_SCHEMA)


def test_valid_note_has_all_keys(valid_note):
    """Une note valide doit contenir tous les champs requis du schéma."""
    required = SESSION_NOTE_CERCLE_OUTPUT_SCHEMA.get("required", [])
    for field in required:
        assert field in valid_note, f"Champ requis manquant dans la fixture : {field}"


# ---------------------------------------------------------------------------
# Tests — Validation données invalides
# ---------------------------------------------------------------------------

def test_missing_required_field_raises(note_missing_required):
    """Une note sans champ requis doit lever ValidationError."""
    with pytest.raises(ValidationError):
        validate(instance=note_missing_required, schema=SESSION_NOTE_CERCLE_OUTPUT_SCHEMA)


def test_wrong_type_raises(note_wrong_type):
    """Un type incorrect doit lever ValidationError si le schéma le définit."""
    required = SESSION_NOTE_CERCLE_OUTPUT_SCHEMA.get("required", [])
    props = SESSION_NOTE_CERCLE_OUTPUT_SCHEMA.get("properties", {})
    participants_prop = props.get("participants", {})
    if participants_prop.get("type") == "array":
        with pytest.raises(ValidationError):
            validate(instance=note_wrong_type, schema=SESSION_NOTE_CERCLE_OUTPUT_SCHEMA)
    else:
        pytest.skip("Le schéma ne contraindra pas le type de 'participants'")


def test_empty_list_accepted_or_rejected(note_empty_participants):
    """Valide le comportement du schéma face à des listes vides."""
    props = SESSION_NOTE_CERCLE_OUTPUT_SCHEMA.get("properties", {})
    participants_prop = props.get("participants", {})
    min_items = participants_prop.get("minItems", 0)
    if min_items > 0:
        with pytest.raises(ValidationError):
            validate(instance=note_empty_participants, schema=SESSION_NOTE_CERCLE_OUTPUT_SCHEMA)
    else:
        # Listes vides acceptées — aucune erreur attendue
        validate(instance=note_empty_participants, schema=SESSION_NOTE_CERCLE_OUTPUT_SCHEMA)


# ---------------------------------------------------------------------------
# Tests — Champs connus dans le schéma
# ---------------------------------------------------------------------------

def test_schema_contains_titre_field():
    """Le schéma doit contenir une propriété 'titre'."""
    props = SESSION_NOTE_CERCLE_OUTPUT_SCHEMA.get("properties", {})
    assert "titre" in props, "Propriété 'titre' absente du schéma"


def test_schema_contains_participants_field():
    """Le schéma doit contenir une propriété 'participants'."""
    props = SESSION_NOTE_CERCLE_OUTPUT_SCHEMA.get("properties", {})
    assert "participants" in props, "Propriété 'participants' absente du schéma"


def test_schema_contains_recommandations_field():
    """Le schéma doit contenir une propriété 'recommandations'."""
    props = SESSION_NOTE_CERCLE_OUTPUT_SCHEMA.get("properties", {})
    assert "recommandations" in props, "Propriété 'recommandations' absente du schéma"

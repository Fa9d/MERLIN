# test_json_schema_validation.py
# ROD-TEST-001-A / J2 — Validation structure SESSION_NOTE_CERCLE_OUTPUT_SCHEMA
# NOTE : SESSION_NOTE_CERCLE_OUTPUT_SCHEMA est un dict Python descriptif (pas un JSON Schema),
# il utilise des cles de domaine (production_note, client_delivery, etc.) avec des valeurs string.
# Les tests valident la structure reelle du dict, pas jsonschema.validate().

from app.ai.prompts.session_note_cercle_v1 import SESSION_NOTE_CERCLE_OUTPUT_SCHEMA


# ---------------------------------------------------------------------------
# Tests — Structure du schema
# ---------------------------------------------------------------------------

def test_schema_is_dict():
    """Le schema doit etre un dictionnaire Python valide."""
    assert isinstance(SESSION_NOTE_CERCLE_OUTPUT_SCHEMA, dict)


def test_schema_has_top_level_keys():
    """Le schema doit avoir des cles de domaine au premier niveau."""
    assert len(SESSION_NOTE_CERCLE_OUTPUT_SCHEMA) > 0, "Le schema est vide"


def test_schema_contains_production_note():
    """Le schema doit contenir la cle 'production_note'."""
    assert "production_note" in SESSION_NOTE_CERCLE_OUTPUT_SCHEMA, (
        "Cle 'production_note' absente du schema"
    )


def test_schema_contains_client_delivery():
    """Le schema doit contenir la cle 'client_delivery'."""
    assert "client_delivery" in SESSION_NOTE_CERCLE_OUTPUT_SCHEMA, (
        "Cle 'client_delivery' absente du schema"
    )


def test_schema_contains_metadata():
    """Le schema doit contenir la cle 'metadata'."""
    assert "metadata" in SESSION_NOTE_CERCLE_OUTPUT_SCHEMA, (
        "Cle 'metadata' absente du schema"
    )


def test_schema_contains_supervision():
    """Le schema doit contenir la cle 'supervision'."""
    assert "supervision" in SESSION_NOTE_CERCLE_OUTPUT_SCHEMA, (
        "Cle 'supervision' absente du schema"
    )


def test_schema_contains_research():
    """Le schema doit contenir la cle 'research'."""
    assert "research" in SESSION_NOTE_CERCLE_OUTPUT_SCHEMA, (
        "Cle 'research' absente du schema"
    )


# ---------------------------------------------------------------------------
# Tests — Structure de production_note
# ---------------------------------------------------------------------------

def test_production_note_is_dict():
    """production_note doit etre un sous-dict."""
    pn = SESSION_NOTE_CERCLE_OUTPUT_SCHEMA["production_note"]
    assert isinstance(pn, dict), "production_note doit etre un dict"


def test_production_note_has_summary_text():
    """production_note doit contenir 'summary_text'."""
    pn = SESSION_NOTE_CERCLE_OUTPUT_SCHEMA["production_note"]
    assert "summary_text" in pn, "Cle 'summary_text' absente de production_note"


def test_production_note_has_context_hypotheses():
    """production_note doit contenir 'context_hypotheses_json'."""
    pn = SESSION_NOTE_CERCLE_OUTPUT_SCHEMA["production_note"]
    assert "context_hypotheses_json" in pn, (
        "Cle 'context_hypotheses_json' absente de production_note"
    )


def test_production_note_has_vigilance_level():
    """production_note doit contenir 'vigilance_level_code'."""
    pn = SESSION_NOTE_CERCLE_OUTPUT_SCHEMA["production_note"]
    assert "vigilance_level_code" in pn, (
        "Cle 'vigilance_level_code' absente de production_note"
    )


# ---------------------------------------------------------------------------
# Tests — Structure de client_delivery
# ---------------------------------------------------------------------------

def test_client_delivery_is_dict():
    """client_delivery doit etre un sous-dict."""
    cd = SESSION_NOTE_CERCLE_OUTPUT_SCHEMA["client_delivery"]
    assert isinstance(cd, dict), "client_delivery doit etre un dict"


def test_client_delivery_has_client_visible_recommended():
    """client_delivery doit contenir 'client_visible_recommended'."""
    cd = SESSION_NOTE_CERCLE_OUTPUT_SCHEMA["client_delivery"]
    assert "client_visible_recommended" in cd, (
        "Cle 'client_visible_recommended' absente de client_delivery"
    )


# ---------------------------------------------------------------------------
# Tests — Structure de metadata
# ---------------------------------------------------------------------------

def test_metadata_is_dict():
    """metadata doit etre un sous-dict."""
    meta = SESSION_NOTE_CERCLE_OUTPUT_SCHEMA["metadata"]
    assert isinstance(meta, dict), "metadata doit etre un dict"


def test_metadata_has_prompt_version():
    """metadata doit contenir 'prompt_version'."""
    meta = SESSION_NOTE_CERCLE_OUTPUT_SCHEMA["metadata"]
    assert "prompt_version" in meta, "Cle 'prompt_version' absente de metadata"


def test_metadata_has_model_used():
    """metadata doit contenir 'model_used'."""
    meta = SESSION_NOTE_CERCLE_OUTPUT_SCHEMA["metadata"]
    assert "model_used" in meta, "Cle 'model_used' absente de metadata"


# ---------------------------------------------------------------------------
# Tests — Integrite globale du schema
# ---------------------------------------------------------------------------

def test_schema_has_at_least_5_top_level_keys():
    """Le schema doit avoir au moins 5 sections de domaine."""
    assert len(SESSION_NOTE_CERCLE_OUTPUT_SCHEMA) >= 5, (
        f"Le schema n'a que {len(SESSION_NOTE_CERCLE_OUTPUT_SCHEMA)} cles, 5 attendues minimum"
    )


def test_all_top_level_values_are_dicts():
    """Toutes les valeurs de premier niveau doivent etre des sous-dicts."""
    for key, value in SESSION_NOTE_CERCLE_OUTPUT_SCHEMA.items():
        assert isinstance(value, dict), (
            f"La valeur de '{key}' doit etre un dict, trouve : {type(value).__name__}"
        )

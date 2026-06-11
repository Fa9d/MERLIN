"""Tests du registre des référentiels vivants (app.referentiels.registry).

Vérifie le chargement, la validation d'enveloppe, l'unicité des codes, et la cohérence
des référentiels avec leurs sources doctrinales (nombre d'entrées, codes attendus).
Aucun appel réseau — lecture de fichiers YAML uniquement.
"""

from __future__ import annotations

import pytest

from app.referentiels import (
    RegistryError,
    available_referentiels,
    get_codes,
    get_entries,
    load_referentiel,
)
from app.referentiels.registry import (
    RegistryValidationError,
    _validate_envelope,
    clear_cache,
)

TOUS_REFERENTIELS = [
    "axes",
    "tensions",
    "familles_contexte",
    "pressions_societales",
    "signaux_contextuels",
    "vigilance",
    "prochaines_etapes",
]


@pytest.fixture(autouse=True)
def _reset_cache():
    """Repart d'un cache vide à chaque test."""
    clear_cache()
    yield
    clear_cache()


def test_tous_les_referentiels_sont_decouverts():
    decouverts = available_referentiels()
    for name in TOUS_REFERENTIELS:
        assert name in decouverts, f"référentiel '{name}' non découvert sur disque"


@pytest.mark.parametrize("name", TOUS_REFERENTIELS)
def test_chaque_referentiel_charge_et_valide(name):
    data = load_referentiel(name)
    assert data["referentiel"] == name
    assert data["statut"] == "actif"
    assert data["version"]
    assert data["source_doctrine"]
    assert data["entrees"]


@pytest.mark.parametrize("name", TOUS_REFERENTIELS)
def test_codes_uniques_et_non_vides(name):
    codes = get_codes(name)
    assert codes, f"aucun code dans '{name}'"
    assert len(codes) == len(set(codes)), f"codes dupliqués dans '{name}'"
    assert all(isinstance(c, str) and c for c in codes)


def test_axes_fidelite_doctrine():
    """Les 11 axes, territoire fondateur en premier (ordre doctrinal)."""
    entries = get_entries("axes")
    assert len(entries) == 11
    premier = sorted(entries, key=lambda e: e["ordre"])[0]
    assert premier["code"] == "territoire"
    assert premier["fondateur"] is True


def test_tensions_fidelite_doctrine():
    """Les 10 tensions canoniques exactes."""
    codes = set(get_codes("tensions"))
    assert codes == {
        "tension_rythme",
        "tension_reciprocite",
        "tension_appartenance",
        "tension_sens",
        "tension_dignite",
        "tension_charge_exigences",
        "tension_isolement",
        "tension_insecurite",
        "tension_confusion",
        "tension_desorientation",
    }


def test_familles_contexte_six():
    assert len(get_codes("familles_contexte")) == 6


def test_pressions_neuf():
    assert len(get_codes("pressions_societales")) == 9


def test_signaux_douze_fidelite():
    """METH-002 §7 définit 12 signaux contextuels."""
    assert len(get_codes("signaux_contextuels")) == 12


def test_vigilance_quatre_niveaux():
    assert get_codes("vigilance") == ["non_urgent", "watch", "priority", "urgent"]


def test_prochaines_etapes_sept():
    assert len(get_codes("prochaines_etapes")) == 7


def test_prochaines_etapes_alignees_sur_enum_runtime():
    """v1.1 : codes alignés sur AnalysisNextStepCode (décision fondateur 2026-06-10)."""
    from app.models.enums import AnalysisNextStepCode

    assert get_codes("prochaines_etapes") == [code.value for code in AnalysisNextStepCode]


def test_referentiel_absent_leve_erreur():
    with pytest.raises(RegistryError):
        load_referentiel("referentiel_inexistant")


def test_validation_rejette_enveloppe_incoherente():
    with pytest.raises(RegistryValidationError):
        _validate_envelope("axes", {"referentiel": "autre_nom", "entrees": []})


def test_validation_rejette_codes_dupliques():
    payload = {
        "referentiel": "axes",
        "version": "1.0",
        "statut": "actif",
        "source_doctrine": "x",
        "description": "x",
        "entrees": [{"code": "a"}, {"code": "a"}],
    }
    with pytest.raises(RegistryValidationError):
        _validate_envelope("axes", payload)

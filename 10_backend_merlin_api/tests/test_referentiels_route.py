"""Tests de la route read-only des référentiels (app.api.routes.referentiels).

Appelle directement les fonctions de route (aucune dépendance DB, pas de démarrage app).
"""

from __future__ import annotations

import pytest
from fastapi import HTTPException

from app.api.routes.referentiels import get_referentiel, list_referentiels


def test_list_referentiels():
    payload = list_referentiels()
    assert payload["count"] == len(payload["available"])
    assert "axes" in payload["available"]
    assert "tensions" in payload["available"]


def test_get_referentiel_ok():
    data = get_referentiel("axes")
    assert data["referentiel"] == "axes"
    assert len(data["entrees"]) == 11


def test_get_referentiel_absent_404():
    with pytest.raises(HTTPException) as exc:
        get_referentiel("inconnu")
    assert exc.value.status_code == 404

"""Route read-only exposant les référentiels vivants (axes, tensions, contexte, …).

Sert la même source de vérité que le moteur d'analyse : les fichiers YAML versionnés de
`00_DOCTRINE/referentiels/`, chargés et validés par `app.referentiels.registry`.

Accès non authentifié assumé : ces référentiels sont des **taxonomies doctrinales** (axes,
tensions, niveaux de vigilance…), pas des données personnelles. Aucune PII n'y transite.
Le frontend (Carte de Vie, formulaires) les consomme pour rester aligné sur la doctrine
sans recopier les codes à la main.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.referentiels import (
    RegistryError,
    available_referentiels,
    load_referentiel,
)

router = APIRouter(prefix="/referentiels", tags=["referentiels"])


@router.get("")
def list_referentiels() -> dict[str, object]:
    """Liste les référentiels disponibles (noms logiques)."""

    noms = available_referentiels()
    return {"available": noms, "count": len(noms)}


@router.get("/{name}")
def get_referentiel(name: str) -> dict[str, object]:
    """Retourne un référentiel complet (enveloppe + entrées) par son nom logique.

    404 si le référentiel n'existe pas.
    """

    try:
        return load_referentiel(name)
    except RegistryError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

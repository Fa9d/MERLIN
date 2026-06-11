"""Registre des référentiels vivants MERLIN.

Expose le chargement déclaratif des référentiels de sens (axes, tensions, familles
de contexte, pressions sociétales, signaux contextuels, vigilance, prochaines étapes)
depuis `00_DOCTRINE/referentiels/*.yaml`.

Principe directeur : *tout est référentiel*. Le sens vit dans des fichiers YAML
versionnés et gouvernés par la doctrine ; le code n'est qu'un moteur de chargement.
Ajouter un axe ou une tension = ajouter une entrée YAML, jamais réécrire du code.
"""

from app.referentiels.registry import (
    RegistryError,
    RegistryValidationError,
    available_referentiels,
    get_codes,
    get_entries,
    load_referentiel,
)

__all__ = [
    "RegistryError",
    "RegistryValidationError",
    "available_referentiels",
    "get_codes",
    "get_entries",
    "load_referentiel",
]

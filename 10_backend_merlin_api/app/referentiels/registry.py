"""Chargement et validation des référentiels vivants depuis 00_DOCTRINE/referentiels/.

Calque la convention de `app/ai/prompt_loader.py` : les fichiers de doctrine sont lus
depuis la racine du repo via un chemin relatif, avec un cache mémoire simple.

Enveloppe commune attendue pour chaque référentiel YAML :

    referentiel: <nom>           # doit correspondre au nom logique demandé
    version: "<x.y>"
    statut: actif | deprecated
    source_doctrine: <chemin du document doctrinal source>
    description: <texte>
    entrees:                     # liste non vide
      - code: <slug-unique>      # chaque entrée porte un `code` unique
        ...

La validation est volontairement légère et explicite (pas de schéma externe) afin de
rester auditable et sans dépendance lourde. Toute violation lève `RegistryValidationError`.

Note déploiement : comme `prompt_loader`, ce module lit depuis `parents[3]` (racine du
repo). En conteneur, `00_DOCTRINE/referentiels` doit donc être présent dans l'image ou
monté — au même titre que `11_PROMPTS` l'est déjà pour les prompts.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

# Statuts de référentiel acceptés.
_STATUTS_VALIDES = {"actif", "deprecated"}

# Cache mémoire : nom logique du référentiel -> contenu parsé et validé.
_REGISTRY_CACHE: dict[str, dict[str, Any]] = {}


class RegistryError(FileNotFoundError):
    """Référentiel introuvable dans 00_DOCTRINE/referentiels/."""


class RegistryValidationError(ValueError):
    """Référentiel présent mais non conforme à l'enveloppe attendue."""


def _referentiels_root() -> Path:
    """Retourne le chemin absolu du dossier canonique des référentiels."""

    return Path(__file__).resolve().parents[3] / "00_DOCTRINE" / "referentiels"


def _referentiel_path(name: str) -> Path:
    """Résout le chemin du fichier YAML d'un référentiel (`<name>.v1.yaml`).

    On accepte le nom logique seul (`axes`) ; la version courante est `v1`.
    """

    return _referentiels_root() / f"{name}.v1.yaml"


def _validate_envelope(name: str, data: Any) -> dict[str, Any]:
    """Valide l'enveloppe commune et retourne le document si conforme."""

    if not isinstance(data, dict):
        raise RegistryValidationError(
            f"Référentiel '{name}' : le document racine doit être un mapping YAML."
        )

    declared = data.get("referentiel")
    if declared != name:
        raise RegistryValidationError(
            f"Référentiel '{name}' : champ `referentiel` attendu '{name}', trouvé '{declared}'."
        )

    statut = data.get("statut")
    if statut not in _STATUTS_VALIDES:
        raise RegistryValidationError(
            f"Référentiel '{name}' : `statut` invalide '{statut}' "
            f"(attendu l'un de {sorted(_STATUTS_VALIDES)})."
        )

    for required in ("version", "source_doctrine", "description"):
        if not data.get(required):
            raise RegistryValidationError(
                f"Référentiel '{name}' : champ obligatoire manquant ou vide : `{required}`."
            )

    entries = data.get("entrees")
    if not isinstance(entries, list) or not entries:
        raise RegistryValidationError(
            f"Référentiel '{name}' : `entrees` doit être une liste non vide."
        )

    seen: set[str] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise RegistryValidationError(
                f"Référentiel '{name}' : entrée #{index} n'est pas un mapping."
            )
        code = entry.get("code")
        if not code or not isinstance(code, str):
            raise RegistryValidationError(
                f"Référentiel '{name}' : entrée #{index} sans `code` valide."
            )
        if code in seen:
            raise RegistryValidationError(
                f"Référentiel '{name}' : `code` dupliqué '{code}'."
            )
        seen.add(code)

    return data


def load_referentiel(name: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Charge un référentiel par son nom logique, validé et mis en cache.

    Lève `RegistryError` si le fichier est absent, `RegistryValidationError` si le
    contenu ne respecte pas l'enveloppe commune.
    """

    if use_cache and name in _REGISTRY_CACHE:
        return _REGISTRY_CACHE[name]

    path = _referentiel_path(name)
    if not path.exists():
        raise RegistryError(f"Référentiel introuvable pour '{name}' : {path}")

    raw = path.read_text(encoding="utf-8")
    data = yaml.safe_load(raw)
    validated = _validate_envelope(name, data)

    if use_cache:
        _REGISTRY_CACHE[name] = validated
    return validated


def get_entries(name: str) -> list[dict[str, Any]]:
    """Retourne la liste des entrées d'un référentiel."""

    return load_referentiel(name)["entrees"]


def get_codes(name: str) -> list[str]:
    """Retourne la liste ordonnée des `code` d'un référentiel.

    Utile pour valider qu'une sortie d'analyse n'emploie que des codes autorisés.
    """

    return [entry["code"] for entry in get_entries(name)]


def available_referentiels() -> list[str]:
    """Liste les noms logiques des référentiels présents sur disque (triés)."""

    root = _referentiels_root()
    if not root.exists():
        return []
    names = {path.name.split(".", 1)[0] for path in root.glob("*.v1.yaml")}
    return sorted(names)


def clear_cache() -> None:
    """Vide le cache mémoire (utile en test ou après rechargement à chaud)."""

    _REGISTRY_CACHE.clear()

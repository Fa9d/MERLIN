# Référentiels vivants MERLIN

**Statut** : v0.2 — fondation de l'architecture modulaire
**Chargés par** : `10_backend_merlin_api/app/referentiels/registry.py`
**Gouvernés par** : la doctrine (`00_DOCTRINE/`) — chaque fichier cite sa source autoritative.

---

## Principe : *tout est référentiel*

Le **sens** de MERLIN (axes, tensions, familles de contexte, pressions sociétales,
signaux, niveaux de vigilance, types d'orientation) ne vit plus à moitié dans les prompts
et à moitié codé en dur. Il vit ici, dans des **fichiers YAML déclaratifs, versionnés et
gouvernés**, chargés à l'exécution par un registre unique.

> Ajouter un axe, une tension ou une langue = ajouter une entrée YAML + un cas d'eval.
> **Jamais** réécrire le moteur. C'est ce qui rend le système configurable et adaptable
> au fil de l'évolution du projet.

## Référentiels présents

| Fichier | Source autoritative | Contenu |
|---------|---------------------|---------|
| `axes.v1.yaml` | `correspondances-vivantes.md` §3 | 11 axes (territoire fondateur) |
| `tensions.v1.yaml` | `MERLIN_GOUV_SPEC_AXES_ANALYSE_CERCLE_V1.md` §5 | 10 tensions canoniques |
| `familles_contexte.v1.yaml` | idem §4 | 6 familles de contexte |
| `pressions_societales.v1.yaml` | `METH-001` §7 | 9 pressions sociétales (interne) |
| `signaux_contextuels.v1.yaml` | `METH-002` §7 | 12 signaux d'entretien (supervision) |
| `vigilance.v1.yaml` | idem §6 | 4 niveaux de vigilance |
| `prochaines_etapes.v1.yaml` | idem §7 | 7 types d'orientation |
| `../ivia_living_lexicon.yaml` | `correspondances-vivantes.md` | lexique expressions → axes (référentiel historique, déjà en place) |

## Enveloppe commune

Chaque référentiel respecte une enveloppe validée par le registre :

```yaml
referentiel: <nom>          # = nom logique (doit matcher le fichier)
version: "1.0"
statut: actif | deprecated
source_doctrine: <chemin doctrine>
description: <texte>
entrees:                    # liste non vide
  - code: <slug-unique>     # code unique obligatoire
    ...
```

## Usage côté backend

```python
from app.referentiels import load_referentiel, get_codes, available_referentiels

axes = load_referentiel("axes")          # dict validé + caché
codes = get_codes("tensions")            # ['tension_rythme', ...] pour valider une sortie
noms = available_referentiels()          # ['axes', 'familles_contexte', ...]
```

## Gouvernance (héritée du lexique vivant)

- **Ajout / modification** : PR avec entrée complète + au moins un cas d'eval.
- **Modification d'un sens sensible** (formulation client, niveau de risque) : relecture
  humaine explicite (fondateur ou personne mandatée).
- **Suppression interdite** : on déprécie (`statut: deprecated`), on ne supprime pas — la
  mémoire est préservée.
- **Versionnement** : chaque fichier porte un `version:` incrémenté à chaque modification.
- **Évaluations** : toute évolution doit faire passer la safety suite
  (`managed_agents/evals/safety_suite_v1.yaml`).

## Migration progressive (cible)

Les prompts (METH-001/002, session_note_cercle) dupliquent encore une partie de ces données
en texte. Cible : faire des prompts des **consommateurs** du registre (injection depuis les
référentiels) plutôt que des copies, pour éliminer toute dérive prompt↔code↔doctrine.

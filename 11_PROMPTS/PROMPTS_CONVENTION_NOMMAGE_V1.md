---
titre: Convention de nommage des prompts — MERLIN
id: MERLIN-PROMPTS-CONV-NOMMAGE-V1
statut: active
type: charte
couche: PROD
périmètre: 11_PROMPTS
auteur: fondateur
date: 2026-05-05
version: 1.1
dépend_de: [MERLIN-CONVENTION-NOMMAGE-V2, ADR-0002, MERLIN-MODELE-COUCHES-V1]
remplace: []
arbitrage_requis: oui — toute modification de ces règles de nommage
source_canonique: 11_PROMPTS/PROMPTS_CONVENTION_NOMMAGE_V1.md
---

# MERLIN — Convention de nommage des prompts V1

> **Statut** : active — 2026-05-05
> **S'applique** : à tout nouveau fichier prompt créé dans `11_PROMPTS/`.
> **Migration** : les fichiers existants (structure héritée) seront renommés en Vague 3 de manière traçable.

---

## Principe directeur

Un nom de fichier prompt doit permettre de comprendre :
- à quelle couche il appartient (FOND, METH, EDIT, ADMIN, PROD, SYSTEME),
- son sujet ou sa fonction,
- sa version.

Sans lire le contenu du fichier, le nom seul doit répondre à : *C'est quoi, pour quoi, quelle version ?*

---

## 1. Format obligatoire

```
MERLIN_PROMPT_[COUCHE]-[SUJET]_v[MAJOR].[MINOR].md
```

### Composantes

| Composant | Règle | Exemple |
|---|---|---|
| `MERLIN_PROMPT_` | Préfixe fixe obligatoire | `MERLIN_PROMPT_` |
| `[COUCHE]` | Code de couche en majuscules (voir section 2) | `METH`, `FOND`, `EDIT`, `ADMIN`, `PROD`, `SYSTEME` |
| `-` | Séparateur entre couche et sujet | `-` |
| `[SUJET]` | Sujet en MAJUSCULES, mots séparés par `_`, ASCII uniquement | `NOTE_SEANCE_CERCLE` |
| `_v` | Séparateur de version (fixe) | `_v` |
| `[MAJOR].[MINOR]` | Version sémantique à deux niveaux | `1.0`, `2.3` |
| `.md` | Extension Markdown obligatoire | `.md` |

### Règles additionnelles

1. **ASCII uniquement** — pas d'accents, pas de caractères spéciaux.
2. **MAJUSCULES** pour le code de couche et le sujet.
3. **Tiret** `-` entre le code de couche et le sujet.
4. **Underscore** `_` dans le sujet (jamais d'espace).
5. **Pas de date dans le nom** — la date est dans les métadonnées.
6. **Pas de doublon** — deux prompts distincts ne peuvent pas avoir le même sujet et la même couche ; créer un sujet plus précis.

---

## 2. Codes de couche

| Code | Couche MERLIN | Dossier cible | Usage |
|---|---|---|---|
| `SYSTEME` | — (transversal) | `00_SYSTEME/` | Prompts d'identité globale du système MERLIN (persona, contraintes absolues) |
| `FOND` | FOND | `01_FOND/` | Doctrine, contexte culturel, valeurs, cadre québécois, nations autochtones |
| `METH` | METH | `02_METH/` | Méthodes cliniques et d'orientation : note de séance, triage, supervision |
| `EDIT` | EDIT | `03_EDIT/` | Génération de contenus publics : lettres client, pages, offres, campagnes |
| `ADMIN` | METH/PROD | `04_ADMIN/` | Administration : onboarding, routage, audit de dossier |
| `PROD` | PROD | `05_PROD/` | Validation technique, tests, pilote, schémas de sortie |

---

## 3. Règles de versionnage

### Bump MAJOR (ex. : v1.0 → v2.0)

Obligatoire quand :
- la logique métier du prompt change (ex. : nouvelles instructions, nouveau persona),
- le schéma de sortie change structurellement,
- les contraintes absolues (ce que le modèle ne doit pas faire) sont modifiées,
- le prompt est réécrit substantiellement.

Un bump MAJOR d'un prompt de couche METH ou FOND exige un arbitrage explicite.

### Bump MINOR (ex. : v1.0 → v1.1)

Obligatoire quand :
- une formulation est clarifiée sans changer le sens,
- un exemple est ajouté ou mis à jour,
- une erreur typographique est corrigée dans une instruction.

### Règle d'or

**Ne jamais modifier un prompt actif sans bumper sa version.**
Un prompt modifié sans bump est une violation de gouvernance documentaire.

---

## 4. Règles de statut

| Statut | Signification | Règle |
|---|---|---|
| `draft` | En rédaction, non testé | Ne pas utiliser en production |
| `active` | Testé, validé, en production ou prêt pour production | Version de référence |
| `deprecated` | Retiré sans successeur direct | Archiver, ne pas supprimer |
| `superseded` | Remplacé par une version plus récente | Indiquer le successeur dans les métadonnées |

---

## 5. Règles de placement

| Condition | Règle |
|---|---|
| Prompt système global (identité MERLIN) | → `00_SYSTEME/` |
| Prompt mobilisant une doctrine ou un cadre culturel | → `01_FOND/` |
| Prompt implémentant une méthode clinique ou d'orientation | → `02_METH/` |
| Prompt générant un contenu public ou éditorial | → `03_EDIT/` |
| Prompt administratif (onboarding, routage, audit) | → `04_ADMIN/` |
| Prompt technique (validation, test, schéma) | → `05_PROD/` |
| Prompt hybride (ex. : note + supervision) | → couche dominante, mention des couches secondaires dans les métadonnées |

---

## 6. Exemples concrets MERLIN

| Fichier | Explication |
|---|---|
| `MERLIN_PROMPT_METH-NOTE_SEANCE_CERCLE_v2.0.md` | Prompt METH, note de séance selon le Cercle V1, version 2.0 |
| `MERLIN_PROMPT_SYSTEME-IDENTITE_MERLIN_v1.0.md` | Prompt système, identité globale de MERLIN comme moteur documentaire |
| `MERLIN_PROMPT_FOND-CONTEXTE_QUEBEC_v1.0.md` | Prompt FOND, hypothèses et signaux contextuels québécois |
| `MERLIN_PROMPT_METH-TRIAGE_PREMIERE_LIGNE_v1.0.md` | Prompt METH, triage d'une demande de première ligne |
| `MERLIN_PROMPT_EDIT-LETTRE_CLIENT_SYNTHESE_v1.0.md` | Prompt EDIT, lettre de synthèse à destination du client |
| `MERLIN_PROMPT_ADMIN-ONBOARDING_CLIENT_v1.0.md` | Prompt ADMIN, onboarding d'un nouveau client |
| `MERLIN_PROMPT_PROD-VALIDATION_CONTENU_DIFFUSION_v1.0.md` | Prompt PROD, validation avant diffusion client |

---

## 7. Cas non couverts

Si aucun code de couche ne convient clairement, le fondateur doit :
1. Identifier la couche dominante par la nature de la décision que le prompt implémente.
2. Si toujours ambigu, créer un arbitrage et documenter le choix.
3. Mettre à jour cette convention si un nouveau code de couche est nécessaire (ADR requis).

---

## Historique de révisions

| Version | Date | Auteur | Nature de la révision |
|---|---|---|---|
| 1.0 | 2026-05-05 | fondateur | Création initiale — Vague 2 structuration prompts |

| 1.1 | 2026-06-30 | fondateur | Ajout code de couche CSUITE (ADR-0008) + dossier 06_CSUITE/ dans structure cible |

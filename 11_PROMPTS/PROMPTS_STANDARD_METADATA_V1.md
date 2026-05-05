---
titre: Standard de métadonnées des prompts — MERLIN
id: MERLIN-PROMPTS-STANDARD-META-V1
statut: active
type: charte
couche: PROD
périmètre: 11_PROMPTS
auteur: fondateur
date: 2026-05-05
version: 1.0
dépend_de: [MERLIN-STANDARD-META-V1, ADR-0002, PROMPTS-CONVENTION-NOMMAGE-V1]
remplace: []
arbitrage_requis: oui — ajout ou modification d'un champ obligatoire
source_canonique: 11_PROMPTS/PROMPTS_STANDARD_METADATA_V1.md
---

# MERLIN — Standard de métadonnées des prompts V1

> **Statut** : active — 2026-05-05
> **Complète** `MERLIN_STANDARD_METADATA_V1.md` avec les champs spécifiques aux prompts.

---

## Préambule

Les prompts MERLIN sont des documents de gouvernance au même titre que les chartes
et les ADR. Ils doivent pouvoir être audités, revisés, et délégués sans lire le code
source qui les utilise.

Ce standard définit les métadonnées minimales d'un fichier prompt dans `11_PROMPTS/`.
Il étend le standard général (`MERLIN_STANDARD_METADATA_V1.md`) avec des champs
spécifiques au domaine des prompts.

---

## 1. Champs de métadonnées — liste complète

| Champ | Obligatoire | Description |
|---|---|---|
| `titre` | Oui | Titre complet et lisible du prompt |
| `id` | Oui | Identifiant unique stable (format : `MERLIN-PROMPT-[COUCHE]-[SUJET]-V[N]`) |
| `statut` | Oui | `draft` / `active` / `deprecated` / `superseded` |
| `couche` | Oui | Couche MERLIN principale : `SYSTEME` / `FOND` / `METH` / `EDIT` / `ADMIN` / `PROD` |
| `type` | Oui | Toujours `prompt` |
| `périmètre` | Oui | Surface d'usage : `backend` / `frontend` / `supervision` / `admin` / `test` |
| `auteur` | Oui | Auteur principal |
| `date` | Oui | Date de création initiale (YYYY-MM-DD) |
| `version` | Oui | Version sémantique : `MAJOR.MINOR` |
| `modèle_cible` | Oui | Modèle(s) IA pour lequel ce prompt a été écrit et testé |
| `dépend_de` | Non | IDs des documents dont ce prompt dépend (méthodes, fondements) |
| `utilisé_par` | Non | Modules ou routes backend/frontend qui chargent ce prompt |
| `remplace` | Non | ID du prompt que celui-ci remplace |
| `arbitrage_requis` | Non | `oui` + condition, ou `non` |
| `validation_requise` | Non | `praticien` / `superviseur` / `fondateur` / `non` |
| `données_sensibles` | Non | `oui` (niveau 2 ou 3 selon ADR-0003) ou `non` |

---

## 2. Modèle YAML frontmatter (recommandé)

```yaml
---
titre: [Titre complet du prompt]
id: MERLIN-PROMPT-[COUCHE]-[SUJET]-V[N]
statut: draft
type: prompt
couche: [SYSTEME | FOND | METH | EDIT | ADMIN | PROD]
périmètre: [backend | frontend | supervision | admin | test]
auteur: fondateur
date: YYYY-MM-DD
version: 1.0
modèle_cible: [claude-sonnet-4-20250514 | claude-haiku-3 | tous]
dépend_de: []
utilisé_par: []
remplace: []
arbitrage_requis: [non | oui — condition]
validation_requise: [non | praticien | superviseur | fondateur]
données_sensibles: [non | oui]
---
```

---

## 3. Modèle bloc Markdown simple (alternatif)

Pour les prompts documentés sans YAML frontmatter :

```markdown
> **Titre** : [Titre du prompt]
> **ID** : MERLIN-PROMPT-[COUCHE]-[SUJET]-V[N]
> **Statut** : draft | active | deprecated
> **Couche** : SYSTEME | FOND | METH | EDIT | ADMIN | PROD
> **Périmètre** : backend | frontend | supervision | admin | test
> **Auteur** : fondateur
> **Date** : YYYY-MM-DD
> **Version** : 1.0
> **Modèle cible** : [modèle IA]
> **Dépend de** : [liste ou vide]
> **Utilisé par** : [liste ou vide]
> **Données sensibles** : oui | non
```

---

## 4. Exemple concret — Prompt note de séance Cercle V1

```yaml
---
titre: Prompt système — Note de séance Cercle V1 (MERLIN moteur documentaire IVIA)
id: MERLIN-PROMPT-METH-NOTE_SEANCE_CERCLE-V1
statut: active
type: prompt
couche: METH
périmètre: backend
auteur: fondateur
date: 2026-04-22
version: 1.0
modèle_cible: claude-sonnet-4-20250514
dépend_de: [MERLIN-METH-CERCLE-V1, ADR-0003]
utilisé_par: [app/ai/prompts/session_note_cercle_v1.py, app/ai/anthropic_session_note_pipeline.py]
remplace: []
arbitrage_requis: oui — tout changement de logique de triage ou de schéma de sortie
validation_requise: superviseur
données_sensibles: oui
---
```

---

## 5. Exemple concret — Prompt contexte québécois (FOND)

```yaml
---
titre: Prompt — Hypothèses et signaux contextuels québécois
id: MERLIN-PROMPT-FOND-CONTEXTE_QUEBEC-V1
statut: active
type: prompt
couche: FOND
périmètre: backend
auteur: fondateur
date: 2026-04-22
version: 1.0
modèle_cible: claude-sonnet-4-20250514
dépend_de: [MERLIN-MODELE-COUCHES-V1, MERLIN-NATQ-CADRE-V1]
utilisé_par: [app/ai/prompts/session_note_cercle_v1.py]
remplace: []
arbitrage_requis: oui — tout ajout ou retrait d'une hypothèse ou d'un signal
validation_requise: fondateur
données_sensibles: non
---
```

---

## 6. Structure type d'un fichier prompt

Tout fichier prompt dans `11_PROMPTS/` doit suivre cette structure de contenu :

```markdown
---
[YAML frontmatter — voir modèle ci-dessus]
---

# MERLIN — [Titre du prompt] V[N]

## 1. Contexte et usage

[Quand ce prompt est utilisé, par quel module, dans quel flux.]

## 2. Persona / Rôle

[Instruction de rôle pour le modèle : "Tu es MERLIN..."]

## 3. Instructions

[Liste numérotée des instructions.]

## 4. Contraintes absolues

[Ce que le modèle ne doit jamais faire dans ce contexte.]

## 5. Format de sortie

[Description du format attendu : JSON structuré, texte libre, etc.]

## 6. Entrée attendue

[Ce que le prompt reçoit en entrée.]

## 7. Exemple de sortie

[Exemple représentatif, idéalement anonymisé.]

---

## Historique de révisions

| Version | Date | Auteur | Nature |
|---|---|---|---|
| 1.0 | YYYY-MM-DD | fondateur | Création initiale |
```

---

## 7. Règles spécifiques aux prompts sensibles

Un prompt est considéré **sensible** (champ `données_sensibles: oui`) quand :
- il traite des transcriptions de séances,
- il reçoit des informations de santé mentale,
- il génère des documents destinés au client,
- il mobilise des données de niveau 2 ou 3 (voir ADR-0003).

Pour ces prompts :
- la validation par un praticien ou un superviseur est **obligatoire** avant passage en `active`,
- tout bump MAJOR exige un arbitrage explicite,
- les exemples de sortie dans le fichier doivent être **anonymisés ou fictifs**.

---

## Historique de révisions

| Version | Date | Auteur | Nature de la révision |
|---|---|---|---|
| 1.0 | 2026-05-05 | fondateur | Création initiale — Vague 2 structuration prompts |

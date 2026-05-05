---
titre: Taxonomie documentaire — MERLIN
id: MERLIN-TAXONOMIE-DOC-V1
statut: active
type: charte
couche: FOND
périmètre: repo entier
auteur: fondateur
date: 2026-05-05
version: 1.0
dépend_de: [MERLIN-MODELE-COUCHES-V1]
remplace: []
arbitrage_requis: oui — ajout ou suppression d'un type documentaire
source_canonique: 00_GOUVERNANCE/MERLIN_TAXONOMIE_DOCUMENTAIRE_V1.md
---

# MERLIN — Taxonomie documentaire V1

> **Statut** : active — 2026-05-05
> **Tout nouveau type de document doit être ajouté ici par arbitrage.**

---

## Préambule

La taxonomie documentaire définit les catégories de documents autorisées dans MERLIN.
Elle ne prescrit pas le contenu de chaque document ; elle définit sa **nature** et ses règles
de classification, de localisation et de cycle de vie.

Un document sans type identifiable est un signe de classement erroné ou d'un type manquant
à la taxonomie.

---

## Types documentaires autorisés

---

### TYPE 1 — Charte

**Finalité** : Définir les principes fondateurs, les règles constitutives, ou l'architecture
globale d'un système ou d'un sous-système. Une charte est un document de référence durable.

**Emplacement recommandé** : `00_GOUVERNANCE/`, `01_FONDATEUR/`

**Statuts possibles** : `draft` → `active` → `deprecated`

**Exemples** :
- `MERLIN_CHARTE_ARCHITECTURE_V1.md`
- `MERLIN_CONVENTION_NOMMAGE_V2.md`

**Risques de mauvais classement** :
- Confondre avec une politique (une charte définit *ce qu'est* le système ; une politique définit *comment on agit*).
- Confondre avec une doctrine (une charte est plus opérationnelle ; une doctrine est plus philosophique).
- Créer une charte pour un sujet trop étroit (risque d'inflation documentaire).

---

### TYPE 2 — ADR / Arbitrage

**Finalité** : Capturer une décision structurante, son contexte, les options considérées,
et ses conséquences. Un ADR est un document de traçabilité de gouvernance.

**Emplacement recommandé** : `00_GOUVERNANCE/ADR/` pour les ADR formels ;
`00_GOUVERNANCE/` pour les arbitrages informels.

**Statuts possibles** : `proposed` → `accepted` → `deprecated` / `superseded`

**Exemples** :
- `ADR-0001-modele-couches.md`
- `MERLIN_GOUV_ARBITRAGE_PHILOSOPHIE_CONSTRUIT_QUEBECOIS_V0_V1.md`

**Risques de mauvais classement** :
- Créer un ADR pour un choix tactique sans impact structurel.
- Ne pas créer d'ADR pour une décision qui en requiert une (modification silencieuse).
- Stocker un ADR dans un dossier de méthode ou de produit.

---

### TYPE 3 — Fondement

**Finalité** : Exprimer les visées, la philosophie, la doctrine ou les principes éthiques
qui motivent MERLIN. Un fondement justifie l'existence du projet et ses orientations de fond.

**Emplacement recommandé** : `01_FONDATEUR/`, `00_GOUVERNANCE/` (si lié à une décision)

**Statuts possibles** : `draft` → `active` → `deprecated`

**Exemples** :
- `MERLIN_FONDEMENTS_VISEES.md`
- `MERLIN_GOUV_DOCTRINE_APPUIS_THEORIQUES_MERLIN_v1.0.md`
- `MERLIN_GOUV_DOCTRINE_CERCLE_NOYAU_UTILISABLE_V1.md`

**Risques de mauvais classement** :
- Élever un plan éditorial ou une promesse marketing au rang de fondement.
- Confondre fondement et méthode : un fondement dit *pourquoi*, une méthode dit *comment*.
- Stocker un fondement dans `04_METHODES/`.

---

### TYPE 4 — Preuve / Source

**Finalité** : Documenter une référence externe, une synthèse de recherche, un audit,
ou tout matériau qui soutient les affirmations ou les décisions de MERLIN.

**Emplacement recommandé** : `05_PREUVES_SOURCES/`

**Statuts possibles** : `brut` → `analysé` → `intégré` → `archivé`

**Exemples** :
- `MERLIN_PREU_AUDIT_AUTOCHTONES_2026-04-18_v1.0.md`
- `MERLIN_PREU_CADRE_BASE_CONNAISSANCE_SOINS_v1.0.md`

**Risques de mauvais classement** :
- Stocker une synthèse de recherche dans `04_METHODES/` alors qu'elle n'est pas encore une méthode.
- Confondre preuve et méthode : une preuve supporte ; une méthode prescrit.
- Diluer les preuves dans `00_GOUVERNANCE/` sans lien à une décision.

---

### TYPE 5 — Méthode

**Finalité** : Prescrire comment MERLIN atteint un objectif. Une méthode est opérationnelle,
versionnée, et peut évoluer avec le terrain. Elle est la traduction pratique des fondements.

**Emplacement recommandé** : `04_METHODES/`

**Statuts possibles** : `draft` → `active` → `révision` → `deprecated`

**Exemples** :
- `MERLIN_METH_CADRE_METHODE_11_NATIONS_QC_INTL_v1.0.md`
- `MERLIN_METH_CAS_SIMULES_PREMIERE_LIGNE_SANTE_MENTALE_v1.0.md`

**Risques de mauvais classement** :
- Stocker un log d'exécution d'une méthode comme si c'était la méthode elle-même.
- Mettre une politique de haut niveau dans `04_METHODES/`.
- Confondre méthode et case study (→ les cas simulés sont des méthodes ; un cas réel est une preuve).

---

### TYPE 6 — Export

**Finalité** : Livrable produit à destination externe, dans son état publié ou publiable.
Un export n'est pas édité directement dans MERLIN ; il est généré depuis une source.

**Emplacement recommandé** : `07_EXPORTS/`

**Statuts possibles** : `draft` → `publié` → `archivé`

**Exemples** :
- `07_EXPORTS/IVIA_SITE_PREVIEW/index.html`

**Risques de mauvais classement** :
- Modifier un export directement sans modifier la source dans MERLIN.
- Stocker un export dans `04_METHODES/` ou `00_GOUVERNANCE/`.
- Confondre export et document éditorial source.

---

### TYPE 7 — Prompt

**Finalité** : Instruction système ou métier à destination d'un modèle IA. Un prompt
dans MERLIN est versionné, localisé, auditable, et relié à une couche et un usage.

**Emplacement recommandé** : `11_PROMPTS/`

**Statuts possibles** : `draft` → `active` → `deprecated`

**Exemples** :
- `11_PROMPTS/01_session/MERLIN_PROMPT_SESSION_TRIAGE_v1.0.md` (à créer)

**Risques de mauvais classement** :
- Hardcoder un prompt directement dans le code sans version Markdown dans `11_PROMPTS/`.
- Stocker un prompt dans `04_METHODES/` sans lien à la bibliothèque de prompts.
- Ne pas bumper la version d'un prompt avant de le déployer en prod.
- Confondre prompt système (PROD) et politique d'usage (FOND/METH).

---

### TYPE 8 — Spec produit

**Finalité** : Décrire les fonctionnalités, interfaces, flux et comportements attendus
d'un produit ou d'un module. Une spec produit guide l'implémentation.

**Emplacement recommandé** : `00_GOUVERNANCE/` (specs fonctionnelles) ou dans le dossier produit concerné

**Statuts possibles** : `draft` → `validé` → `implémenté` → `deprecated`

**Exemples** :
- `MERLIN_GOUV_SPEC_ECRANS_V1_PARCOURS_CLIENT_IVIA_MERLIN.md`
- `MERLIN_GOUV_SPEC_DONNEES_V1_IVIA_MERLIN.md`

**Risques de mauvais classement** :
- Confondre spec produit et fondement : une spec décrit ce qu'on construit, pas pourquoi.
- Mettre une spec dans `04_METHODES/` sans lien à un backlog ou à une implémentation.
- Ne pas marquer une spec comme `deprecated` quand elle est remplacée par l'implémentation.

---

### TYPE 9 — Protocole

**Finalité** : Décrire une procédure formelle pas à pas, répétable et vérifiable.
Un protocole est plus prescriptif qu'une méthode ; il est pensé pour être suivi
sans interprétation.

**Emplacement recommandé** : `04_METHODES/`, `00_GOUVERNANCE/` (si protocole de gouvernance)

**Statuts possibles** : `draft` → `actif` → `deprecated`

**Exemples** :
- `MERLIN_GOUV_PROCEDURE_REDEPLOIEMENT_STANDARD_VPS_BACKEND_V1.md`
- `MERLIN_GOUV_CHECKLIST_RECETTE_PROD_E2E_J8_V1.md`

**Risques de mauvais classement** :
- Confondre protocole et méthode : un protocole est plus rigide (checklist, étapes exactes).
- Stocker un protocole technique dans `04_METHODES/` quand il relève de l'exploitation (→ `08_EMPLOI/`).

---

### TYPE 10 — Politique

**Finalité** : Définir une règle d'action que MERLIN s'engage à respecter dans un domaine
précis. Une politique est normative : elle dit ce qui doit être fait, pas comment.

**Emplacement recommandé** : `00_GOUVERNANCE/` (avec préfixe `POLICY_`)

**Statuts possibles** : `draft` → `active` → `deprecated`

**Exemples** :
- `MERLIN_GOUV_POLICY_CONSENTEMENTS_SEANCES_DONNEES_v1.0.md`
- `MERLIN_GOUV_POLICY_TRANSCRIPTION_GOUVERNEE_v1.0.md`
- `MERLIN_GOUV_POLICY_VERSIONNAGE_REFERENTIELS_BDD_APP_v1.0.md`

**Risques de mauvais classement** :
- Confondre politique et charte : une charte définit le système ; une politique prescrit un comportement.
- Confondre politique et procédure : une politique dit *quoi* ; un protocole dit *comment*.
- Créer une politique sans la lier à un fondement ou à une décision.

---

### TYPE 11 — Audit

**Finalité** : Enregistrer le résultat d'une évaluation formelle ou d'un contrôle qualité.
Un audit documente l'état d'un système, d'un corpus ou d'une pratique à un moment donné.

**Emplacement recommandé** : `05_PREUVES_SOURCES/`, `00_GOUVERNANCE/` (logs d'audit)

**Statuts possibles** : `en cours` → `complété` → `archivé`

**Exemples** :
- `MERLIN_PREU_AUDIT_AUTOCHTONES_2026-04-18_v1.0.md`
- `AUDIT_REPERTOIRES_MESANGE_6MOIS.md`

**Risques de mauvais classement** :
- Confondre audit et méthode : un audit est un résultat, pas une prescription.
- Stocker un audit dans `04_METHODES/` ou `01_FONDATEUR/`.
- Archiver un audit sans l'horodatage précis (date d'exécution obligatoire).

---

### TYPE 12 — Note temporaire

**Finalité** : Capturer une réflexion, une hypothèse, un brouillon ou une idée en cours
de maturation. Une note temporaire n'est pas un document de référence.

**Emplacement recommandé** : `memory/` ou dans le dossier concerné avec préfixe `NOTE_`

**Statuts possibles** : `en cours` → `intégré` (dans un document de référence) → `supprimé`

**Exemples** :
- Fichiers dans `memory/`
- Notes de session exportées depuis des outils externes

**Risques de mauvais classement** :
- Laisser une note temporaire dans `00_GOUVERNANCE/` sans la convertir ou la supprimer.
- Élever une note temporaire au rang de politique ou de fondement sans arbitrage.
- Accumuler des notes sans les intégrer ou les archiver (dette documentaire).

---

## Tableau de synthèse

| Type | Couche principale | Emplacement | Stabilité | Versionné |
|---|---|---|---|---|
| Charte | FOND | 00_GOUVERNANCE/ | Très haute | Oui |
| ADR / Arbitrage | FOND | 00_GOUVERNANCE/ADR/ | Permanente | Non (cicatrice) |
| Fondement | FOND | 01_FONDATEUR/ | Très haute | Oui |
| Preuve / Source | METH/FOND | 05_PREUVES_SOURCES/ | Haute | Oui |
| Méthode | METH | 04_METHODES/ | Haute | Oui |
| Export | EDIT/PROD | 07_EXPORTS/ | Basse | Par release |
| Prompt | PROD | 11_PROMPTS/ | Haute | Oui — obligatoire |
| Spec produit | PROD | 00_GOUVERNANCE/ | Moyenne | Oui |
| Protocole | METH/PROD | 04_METHODES/ ou 08_EMPLOI/ | Haute | Oui |
| Politique | FOND/METH | 00_GOUVERNANCE/ | Haute | Oui |
| Audit | PROD | 05_PREUVES_SOURCES/ | Fixe (horodatage) | Non |
| Note temporaire | — | memory/ | Faible | Non |

---

## Historique de révisions

| Version | Date | Auteur | Nature de la révision |
|---|---|---|---|
| 1.0 | 2026-05-05 | fondateur | Création initiale — Vague 1 structuration |

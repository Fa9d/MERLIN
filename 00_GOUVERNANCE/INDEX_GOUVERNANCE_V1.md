---
titre: Index de gouvernance — 00_GOUVERNANCE
id: MERLIN-INDEX-GOUV-V1
statut: active
type: charte
couche: FOND
périmètre: 00_GOUVERNANCE
auteur: fondateur
date: 2026-05-05
version: 1.0
dépend_de: []
remplace: []
arbitrage_requis: non
source_canonique: 00_GOUVERNANCE/INDEX_GOUVERNANCE_V1.md
---

# MERLIN — Index de gouvernance V1

> **Porte d'entrée humaine dans `00_GOUVERNANCE/`**
> **Statut** : active — 2026-05-05
> **Ce fichier doit être tenu à jour à chaque ajout de document structurant.**

---

## Rôle du dossier `00_GOUVERNANCE/`

`00_GOUVERNANCE/` est le centre nerveux de MERLIN.

Il contient :
- les chartes et règles constitutives du système,
- les décisions structurantes et les arbitrages,
- les politiques internes (données, consentement, sécurité, exploitation),
- le registre centralisé des décisions,
- les backlogs et les plans d'exécution,
- les spécifications fonctionnelles et les cadres de gouvernance des produits,
- les simulations économiques et les analyses de marché,
- les runbooks et checklists d'exploitation.

`00_GOUVERNANCE/` ne contient **pas** :
- le code source (→ `09_app_ivia_merlin/`, `10_backend_merlin_api/`),
- les contenus éditoriaux publiés (→ `07_EXPORTS/`),
- les méthodes cliniques ou d'orientation (→ `04_METHODES/`),
- les preuves et sources externes (→ `05_PREUVES_SOURCES/`),
- les prompts système (→ `11_PROMPTS/`).

---

## Ordre de lecture recommandé

Pour un nouvel entrant dans MERLIN, lire dans cet ordre :

1. **`MERLIN_CHARTE_ARCHITECTURE_V1.md`** — Comprendre ce qu'est MERLIN et sa structure descendante
2. **`MERLIN_MODELE_DE_COUCHES_V1.md`** — Comprendre les 4 couches FOND / METH / EDIT / PROD
3. **`MERLIN_REGLES_DE_DECISION_V1.md`** — Comprendre quand et comment prendre une décision traçable
4. **`MERLIN_TAXONOMIE_DOCUMENTAIRE_V1.md`** — Comprendre les types de documents et leurs règles
5. **`MERLIN_STANDARD_METADATA_V1.md`** — Comprendre comment annoter un document
6. **`MERLIN_CONVENTION_NOMMAGE_V2.md`** — Comprendre comment nommer les fichiers
7. **`MERLIN_GOUV_REGISTRE_DECISIONS_REVISIONS_IVIA_MERLIN_V1.md`** — Voir l'historique des décisions
8. **`ADR/`** — Lire les décisions architecturales dans l'ordre chronologique

---

## Documents de référence — Couche fondatrice (FOND)

| Fichier | Rôle |
|---|---|
| `MERLIN_CHARTE_ARCHITECTURE_V1.md` | Définit MERLIN comme repo-système canonique et sa structure descendante |
| `MERLIN_MODELE_DE_COUCHES_V1.md` | Définit les 4 couches FOND / METH / EDIT / PROD avec rôles et exemples |
| `MERLIN_REGLES_DE_DECISION_V1.md` | Définit quand créer un ADR, qui valide quoi, interdictions strictes |
| `MERLIN_TAXONOMIE_DOCUMENTAIRE_V1.md` | Définit les 12 types documentaires autorisés et leurs règles |
| `MERLIN_STANDARD_METADATA_V1.md` | Définit le standard de métadonnées pour les documents structurants |
| `MERLIN_CONVENTION_NOMMAGE_V2.md` | Convention de nommage des fichiers (remplace V1) |

---

## Documents de registre et de décision

| Fichier | Rôle |
|---|---|
| `MERLIN_GOUV_REGISTRE_DECISIONS_REVISIONS_IVIA_MERLIN_V1.md` | Registre tabulaire de toutes les décisions (DEC-001 à DEC-035+) |
| `ADR/` | Dossier des Architecture Decision Records formels (ADR-0001+) |

---

## Documents de gouvernance opérationnelle

| Fichier | Rôle |
|---|---|
| `MERLIN_GOUV_BACKLOG_MAITRE_V1.md` | Backlog maître du projet |
| `MERLIN_GOUV_JOURNAL_EXECUTION_V1.md` | Journal d'exécution des sprints et tâches |
| `MERLIN_GOUV_TABLEAU_BORD_HEBDO_V1.md` | Tableau de bord hebdomadaire |
| `MERLIN_GOUV_PLANNING_OPERATIONNEL_10_JOURS_V1.md` | Planning court terme |
| `MERLIN_GOUV_DECISION_GO_NO_GO_PILOTE_FERME_2026-04-26_v1.0.md` | Décision GO/NO-GO pilote 2026-04-26 |

---

## Politiques internes (POLICY_)

| Fichier | Rôle |
|---|---|
| `MERLIN_GOUV_POLICY_CONSENTEMENTS_SEANCES_DONNEES_v1.0.md` | Règles de consentement pour les séances et données |
| `MERLIN_GOUV_POLICY_TRANSCRIPTION_GOUVERNEE_v1.0.md` | Politique de transcription audio |
| `MERLIN_GOUV_POLICY_ENREGISTREMENT_TRANSCRIPTION_HISTORIQUE_CLIENT_v1.0.md` | Politique de conservation des enregistrements |
| `MERLIN_GOUV_POLICY_VERSIONNAGE_REFERENTIELS_BDD_APP_v1.0.md` | Politique de versionnage base de données et app |
| `MERLIN_GOUV_POLICY_SAUVEGARDE_RESTAURATION_V1.md` | Politique de sauvegarde et restauration |
| `MERLIN_GOUV_POLICY_MINEURS_PARENTS_SANTE_MENTALE_v1.0.md` | Politique pour les mineurs et parents |
| `MERLIN_GOUV_POLICY_MEMOIRE_EVOLUTIVE_v1.0.md` | Politique de mémoire évolutive |
| `MERLIN_GOUV_CADRE_OPERATOIRE_TRAITEMENT_DONNEES_IVIA_MERLIN_V1.md` | Cadre opératoire de traitement des données |

---

## Spécifications fonctionnelles

| Fichier | Rôle |
|---|---|
| `MERLIN_GOUV_SPEC_ECRANS_V1_PARCOURS_CLIENT_IVIA_MERLIN.md` | Spec des écrans du parcours client |
| `MERLIN_GOUV_SPEC_ECRANS_ADMIN_MESANGE_V1.md` | Spec des écrans admin MESANGE |
| `MERLIN_GOUV_SPEC_DONNEES_V1_IVIA_MERLIN.md` | Spec des données IVIA/MERLIN |
| `MERLIN_GOUV_SPEC_AXES_ANALYSE_CERCLE_V1.md` | Spec des axes d'analyse du Cercle |
| `MERLIN_GOUV_SPEC_WORKFLOW_DIFFUSION_CLIENT_V1.md` | Spec du workflow de diffusion client |

---

## Runbooks et checklists d'exploitation

| Fichier | Rôle |
|---|---|
| `MERLIN_GOUV_PROCEDURE_REDEPLOIEMENT_STANDARD_VPS_BACKEND_V1.md` | Procédure standard de redéploiement backend |
| `MERLIN_GOUV_RUNBOOK_BACKUP_RESTORE_V1.md` | Runbook sauvegarde et restauration |
| `MERLIN_GOUV_RUNBOOK_COMPTES_SECRETS_ACCES_TEST_V1.md` | Runbook comptes, secrets et accès test |
| `MERLIN_GOUV_CHECKLIST_RECETTE_PROD_E2E_J8_V1.md` | Checklist de recette E2E prod |
| `MERLIN_GOUV_CHECKLIST_VALIDATION_AUDIO_PROD_V1.md` | Checklist de validation audio prod |
| `MERLIN_GOUV_CHECKLIST_HEBDO_SAUVEGARDES_V1.md` | Checklist hebdomadaire des sauvegardes |

---

## Rôle du dossier `ADR/`

`ADR/` (Architecture Decision Records) est un sous-dossier de `00_GOUVERNANCE/`.

Il contient les décisions architecturales formelles de MERLIN :
chaque décision est un fichier autonome, horodaté, avec contexte, options et conséquences.

Ces documents sont **permanents** : ils ne sont jamais supprimés.
Un ADR supersédé est marqué `superseded` et référence son successeur.

| Fichier | Décision |
|---|---|
| `ADR-0001-modele-couches.md` | Adoption du modèle FOND / METH / EDIT / PROD |
| `ADR-0002-gouvernance-prompts.md` | Versionnage et auditabilité des prompts structurels |
| `ADR-0003-politique-donnees-ia.md` | Politique initiale de données et IA dans le contexte québécois |

---

## Note de maintenance

Cet index doit être mis à jour :
- à chaque ajout d'un document structurant dans `00_GOUVERNANCE/`,
- à chaque création d'un ADR,
- à chaque passage d'un document de `draft` à `active`.

Il n'a **pas** vocation à lister tous les fichiers opérationnels, logs, et analyses
économiques du dossier — seulement les documents de référence structurante.

---

## Historique de révisions

| Version | Date | Auteur | Nature de la révision |
|---|---|---|---|
| 1.0 | 2026-05-05 | fondateur | Création initiale — Vague 1 structuration |

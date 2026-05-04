# MERLIN — Système de gestion opérationnel V1

Date: 2026-05-04
Statut: actif
Objet: définir les règles, les niveaux et les conventions du système de pilotage quotidien de MERLIN / IVIA

---

## 1. Finalité

Ce système a un seul but : rendre visible, à tout moment, ce qui est en cours, ce qui est bloqué, et ce qui vient ensuite.

Il ne remplace pas les documents existants. Il les relie.

Il doit être utilisable demain matin, seul, sans réunion et sans outil tiers.

---

## 2. Périmètre

Le système couvre l'ensemble du projet MERLIN / IVIA :

- gouvernance et méthode
- backend FastAPI / Alembic / PostgreSQL (dossier `10_backend_merlin_api/`)
- frontend Next.js / IVIA (dossier `09_app_ivia_merlin/`)
- infrastructure VPS / Docker (VPS `ubuntu@137.74.42.121`, docker-compose.prod.yml)
- contenu éditorial (articles IVIA, corpus, dossier `04_METHODES/articles/`)
- diffusion client (plans, calendriers)

Hors périmètre :
- MESANGE (projet distinct, en attente de démarrage)
- les documents fondateurs et doctrinaux (référence stable, pas de gestion active)

---

## 3. Les 5 fichiers du système

| Fichier | Rôle | Fréquence mise à jour |
|---|---|---|
| `MERLIN_GOUV_SYSTEME_GESTION_OPERATIONNEL_V1.md` | Référence du système, règles, conventions | Quand les règles changent |
| `MERLIN_GOUV_TABLEAU_BORD_HEBDO_V1.md` | Vue active de la semaine en cours | Chaque jour ouvrable |
| `MERLIN_GOUV_BACKLOG_MAITRE_V1.md` | Toutes les tâches connues, triées par domaine | À chaque nouvelle tâche ou changement de statut |
| `MERLIN_GOUV_JOURNAL_EXECUTION_V1.md` | Trace chronologique de ce qui a été fait | À chaque action significative |
| `MERLIN_GOUV_MODE_EMPLOI_SYSTEME_GESTION_V1.md` | Comment utiliser le système au quotidien | Quand le système évolue |

---

## 4. Articulation avec les documents existants

Ces documents sont des références stables. Le système les cite, ne les duplique pas.

| Document | Rôle | Usage dans le système |
|---|---|---|
| `MERLIN_GOUV_REGISTRE_DECISIONS_REVISIONS_IVIA_MERLIN_V1.md` | Décisions structurantes DEC-001 → DEC-035+ | Cité dans le journal et le backlog |
| `MERLIN_GOUV_PLANNING_OPERATIONNEL_10_JOURS_V1.md` | Sprint J1-J10, base du pilote ferme | Référence exécutée — sert de point de départ du journal |
| `MERLIN_GOUV_DECISION_GO_NO_GO_PILOTE_FERME_2026-04-26_v1.0.md` | GO pilote ferme encadré (2026-04-26) | Référence décisionnelle de fond |
| `MERLIN_GOUV_PROCEDURE_REDEPLOIEMENT_STANDARD_VPS_BACKEND_V1.md` | Procédure technique VPS | Lié aux tâches domaine infra |
| `MERLIN_GOUV_CHECKLIST_RECETTE_PROD_E2E_J8_V1.md` | Recette e2e production | Preuve cible pour tâches de validation |
| `MERLIN_GOUV_CHECKLIST_VALIDATION_AUDIO_PROD_V1.md` | Recette audio prod | Preuve cible pour chantier audio |
| `MERLIN_GOUV_RUNBOOK_BACKUP_RESTORE_V1.md` | Sauvegarde / restauration | Référence opérationnelle VPS |
| `MERLIN_GOUV_BACKLOG_IMPLEMENTATION_ROLES_ACCES_VISIBILITE_V1.md` | Backlog technique rôles/accès | Absorbé dans le backlog maître (domaine: backend) |
| `MERLIN_GOUV_RETROPLANNING_BUILD_8_SEMAINES_V1.md` | Vision macro 8 semaines | Référence stratégique pour calibrer les priorités |
| `MERLIN_CONVENTION_NOMMAGE_V2.md` | Conventions de nommage fichiers repo | Référence système |
| `MERLIN_GOUV_PLAN_EXECUTION_OPTIMAL_PROJET_V1.md` | Ordre d'exécution optimal, couches du projet | Référence stratégique |

---

## 5. Niveaux de pilotage

```
Vision → Chantier → Tâche → Livrable → Preuve → Décision
```

| Niveau | Description | Où c'est documenté |
|---|---|---|
| Vision | Objectif stratégique (lancement public, pilote ferme) | `MERLIN_GOUV_RETROPLANNING_BUILD_8_SEMAINES_V1.md` |
| Chantier | Ensemble de travail cohérent sur 1 à 3 semaines | Tableau de bord hebdo |
| Tâche | Action unitaire réalisable en moins d'un jour | Backlog maître |
| Livrable | Fichier, commit, résultat mesurable | Backlog maître |
| Preuve | Commit git, log terminal, URL, capture | Journal d'exécution |
| Décision | Choix structurant, daté, justifié | `MERLIN_GOUV_REGISTRE_DECISIONS_REVISIONS_IVIA_MERLIN_V1.md` |

---

## 6. Statuts normalisés

| Statut | Signification |
|---|---|
| `todo` | Identifié, non démarré |
| `active` | En cours (cette semaine ou cette session) |
| `blocked` | Bloqué — la raison doit être documentée explicitement |
| `done` | Terminé — une preuve est disponible |
| `archived` | Obsolète ou remplacé — conservé pour référence |

Règle : une tâche ne passe en `done` que si une preuve est identifiable (commit, log, fichier créé, URL).

---

## 7. Niveaux de priorité

| Priorité | Signification |
|---|---|
| `P1` | Critique / bloquant — à faire aujourd'hui |
| `P2` | Haute — à faire cette semaine |
| `P3` | Normale — dans ce sprint (15 jours) |
| `P4` | Basse — backlog long terme |

---

## 8. Types de livrables

| Type | Exemples |
|---|---|
| `commit` | Correctif ou feature poussé sur GitHub |
| `fichier-repo` | Document markdown créé ou mis à jour dans le repo |
| `action-vps` | Commande exécutée sur le VPS (migration, rebuild, scp) |
| `recette` | Checklist de validation exécutée et validée |
| `décision` | Entrée ajoutée dans le registre de décisions |
| `contenu` | Article, corpus, page publiable créé |

---

## 9. Cadence de revue

| Fréquence | Action |
|---|---|
| Quotidien | Mettre à jour le tableau de bord (chantiers actifs, blocages, priorité du jour) et ajouter une ligne au journal |
| Hebdomadaire | Revoir le backlog maître, ajuster les priorités, fermer les tâches `done`, identifier les nouveaux chantiers |
| 10 jours | Vérifier l'alignement avec les jalons stratégiques, décider si un chantier s'ouvre ou se ferme |

---

## 10. Règles de mise à jour

1. Toute action significative (commit, commande VPS, décision) génère une ligne dans le journal le jour même.
2. Un changement de statut dans le backlog est fait le jour même, pas en lot.
3. Le tableau de bord reflète l'état réel, pas l'état souhaité.
4. Les blocages sont nommés explicitement : cause + prochaine action débloquante.
5. Aucune information n'est dupliquée : si elle existe ailleurs, on fait référence au fichier source.
6. Les nouvelles tâches entrent dans le backlog maître avant d'être démarrées.

---

## 11. Règles d'archivage

- Un chantier terminé reste dans le backlog avec statut `done` pendant 2 semaines, puis passe en `archived`.
- Les logs d'incidents restent permanents dans `00_GOUVERNANCE/`.
- Le tableau de bord hebdo est remis à zéro chaque lundi, mais une ligne par chantier clôturé est d'abord ajoutée au journal.
- Les décisions du registre ne sont jamais supprimées.
- Les documents de politique (`POLICY_*`) et de procédure (`RUNBOOK_*`, `PROCEDURE_*`) sont versionnés plutôt qu'archivés.

---

## 12. Domaines du backlog

| Domaine | Contenu |
|---|---|
| `gouvernance` | Organisation, conventions, documentation système |
| `fondements` | Documents fondateurs, doctrine, méthode |
| `méthodes` | Cadre méthode, cas simulés, contenu MERLIN |
| `frontend` | Next.js, composants, parcours client IVIA |
| `backend` | FastAPI, Alembic, modèles, schémas, routes |
| `infra` | VPS, Docker, Nginx, TLS, sauvegardes |
| `contenu-éditorial` | Articles IVIA, corpus, pages publiables |
| `diffusion` | Plans de diffusion, calendriers, canaux |

# MERLIN — Tableau de bord hebdomadaire V1

Semaine: 2026-05-04 → 2026-05-09
Mis à jour: 2026-05-04
Statut global: **déploiement VPS bloquant — à résoudre en priorité absolue**

> Ce tableau est la vue opérationnelle de la semaine. Il est mis à jour chaque jour ouvrable.
> Les détails des tâches sont dans `MERLIN_GOUV_BACKLOG_MAITRE_V1.md`.
> Les preuves d'exécution sont dans `MERLIN_GOUV_JOURNAL_EXECUTION_V1.md`.

---

## Vue d'ensemble de la semaine

| Chantier | Domaine | Priorité | Statut | Livrable suivant | Blocage | Preuve récente | Décision requise |
|---|---|---|---|---|---|---|---|
| Déploiement VPS — migration + rebuild | infra | P1 | `active` | `make migrate` + `make up` exécutés | Aucun blocage technique — action manuelle requise | migration 0017 copiée sur VPS (scp exit 0) | Non |
| Backend — quick wins mai 2026 | backend | P1 | `done` | — | — | commits `fbcd670` `b43dfe5` `0a9520a` `c8846c5` | Non |
| Frontend — stabilisation Next.js | frontend | P2 | `todo` | middleware.ts → proxy.ts | Dépend de la confirmation que le VPS est OK | commit `62e3a46` (ClientPayload) | Non |
| Recette e2e pilote — post-déploiement | infra | P2 | `todo` | Checklist `CHECKLIST_RECETTE_PROD_E2E_J8_V1` rejouée | Dépend du déploiement VPS (P1) | GO pilote 2026-04-26 | Non |
| Contenu éditorial — intégration web | contenu-éditorial | P3 | `todo` | Route `/ressources` ou `/blog` dans Next.js | Dépend de la stabilisation frontend | 16 articles pushés sur GitHub (`4af888b`) | Non |
| Système de gestion opérationnel | gouvernance | P2 | `active` | 5 fichiers créés dans `00_GOUVERNANCE/` | — | — | Non |

---

## Priorité absolue aujourd'hui — 2026-05-04

**Chantier : Déploiement VPS**

Ce qui est fait :
- migration 0017 copiée sur VPS via `scp` ✅
- `docker-compose.prod.yml` modifié (volume alembic) et commité (`c4dc4d5`) ✅
- 7 fichiers Python backend modifiés et commités sur GitHub ✅

Ce qui reste à faire (dans l'ordre) :
1. `scp` de `docker-compose.prod.yml` vers `/opt/merlin/`
2. `scp` des 7 fichiers Python backend modifiés vers `/opt/merlin/10_backend_merlin_api/app/`
3. `ssh ubuntu@137.74.42.121` → `cd /opt/merlin && make migrate`
4. `make up`
5. Vérifier `https://api.ivia.quebec/api/health` → `status: ok`

Référence procédure : `MERLIN_GOUV_PROCEDURE_REDEPLOIEMENT_STANDARD_VPS_BACKEND_V1.md`

---

## Chantiers actifs — détail

### 1. Déploiement VPS

**Statut :** `active` — bloquant, priorité immédiate
**Contexte :** 5 quick wins backend mergés sur master, migration 0017 créée manuellement (DB inaccessible localement). Tout est prêt côté code. L'action est sur le VPS.
**Fichiers concernés :**
- `docker-compose.prod.yml` (commit `c4dc4d5`)
- `10_backend_merlin_api/app/main.py` (commit `0a9520a`)
- `10_backend_merlin_api/app/core/deps.py` (commit `b43dfe5`)
- `10_backend_merlin_api/app/models/enums.py` (commit `a622b82`)
- `10_backend_merlin_api/app/models/intake_request.py` (commit `fbcd670`)
- `10_backend_merlin_api/app/schemas/intake_request.py` (commit `fbcd670`)
- `10_backend_merlin_api/app/api/routes/sessions.py` (commit `c8846c5`)
- `10_backend_merlin_api/app/api/routes/bookings.py` (commit `b43dfe5`)
**Critère de sortie :** `api.ivia.quebec/api/health` répond `200` après `make up`

---

### 2. Backend — quick wins mai 2026

**Statut :** `done`
**Réalisé :**
- `SlotStatus` nettoyé (5 valeurs parasites retirées) — `a622b82`
- `POST /{session_id}/room` → `410 Gone` — `c8846c5`
- CORS `allow_methods` explicite — `0a9520a`
- `require_verified_email_user` sur `hold_slot` et `confirm_slot` — `b43dfe5`
- `RequestChannelCode` enum + modèle + schéma + migration `0017` — `fbcd670`
- `ClientPayload` TypeScript — `record_status` + `data_sensitivity_class` — `62e3a46`
**Preuve :** commits sur master, `git log --oneline` HEAD = `4af888b`

---

### 3. Frontend — stabilisation Next.js

**Statut :** `todo` (démarrage semaine prochaine)
**Tâches :**
- `middleware.ts` → `proxy.ts` (warning Next.js 16.2.4)
- `reserver/page.tsx` → `confirmation/page.tsx` (état `confirmed`)
- Vérification parcours réservation bout-en-bout
**Dépendance :** déploiement VPS validé (P1)

---

### 4. Recette e2e pilote

**Statut :** `todo`
**Référence :** `MERLIN_GOUV_CHECKLIST_RECETTE_PROD_E2E_J8_V1.md`
**Flux à rejouer :** `public → operator → supervisor → public`
**Dépendance :** déploiement VPS + `make up` exécuté

---

### 5. Contenu éditorial — intégration web

**Statut :** `todo`
**Contexte :** 16 articles IVIA complétés, pushés, dans `04_METHODES/articles/`. Pas encore intégrés dans Next.js.
**Prochaine action :** créer route `/ressources` + système de rendu MDX ou markdown
**Dépendance :** frontend stabilisé

---

### 6. Système de gestion opérationnel

**Statut :** `active`
**Contexte :** création des 5 fichiers de pilotage en cours (cette session)
**Critère de sortie :** 5 fichiers créés dans `00_GOUVERNANCE/` + commit `docs(gouv): mise en place systeme de gestion operationnel MERLIN v1`

---

## Blocages actifs

| Blocage | Impact | Prochaine action débloquante |
|---|---|---|
| `make migrate` + `make up` pas encore exécutés | Migration 0017 non appliquée en prod | Ouvrir SSH, exécuter scp + make migrate + make up |

---

## Décisions en attente

Aucune décision structurante requise cette semaine.

Référence registre : décisions DEC-001 → DEC-035 dans `MERLIN_GOUV_REGISTRE_DECISIONS_REVISIONS_IVIA_MERLIN_V1.md`.

---

## Note de mise à jour

> Remplacer l'entête `Semaine: ...` et la ligne `Mis à jour: ...` à chaque modification.
> En fin de semaine, archiver les chantiers `done` dans `MERLIN_GOUV_JOURNAL_EXECUTION_V1.md` (une ligne par chantier clôturé), puis réinitialiser le tableau.

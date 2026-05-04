# MERLIN — Journal d'exécution V1

Date création: 2026-05-04
Statut: actif
Objet: trace chronologique des actions significatives réalisées sur le projet MERLIN / IVIA

> Ce journal est cumulatif. On n'y efface rien. On y ajoute une ligne à chaque action significative.
> Format d'une entrée : `Date | Action | Zone | Commit / Référence | Résultat | Prochaine étape`

---

## Convention

| Colonne | Contenu |
|---|---|
| Date | `AAAA-MM-JJ` |
| Action | Description courte de ce qui a été fait |
| Zone | Dossier ou composant impacté (`00_GOUVERNANCE/`, `backend`, `frontend`, `VPS`, etc.) |
| Commit / Réf | Hash git court ou référence document |
| Résultat | Ce qui est vrai après l'action |
| Prochaine étape | Ce que ça débloque ou ce qui reste |

---

## Entrées

| Date | Action | Zone | Commit / Réf | Résultat | Prochaine étape |
|---|---|---|---|---|---|
| 2026-04-26 | Sprint J1-J10 — validation production J1 à J8 complète | VPS + backend + frontend | `MERLIN_GOUV_PLANNING_OPERATIONNEL_10_JOURS_V1.md` | Droits, TLS, frontend, workflow documentaire validés en prod | GO pilote ferme encadré |
| 2026-04-26 | Décision GO pilote ferme encadré | gouvernance | `MERLIN_GOUV_DECISION_GO_NO_GO_PILOTE_FERME_2026-04-26_v1.0.md` | Pilote autorisé pour comptes internes et utilisateurs tests | Ouvrir J9 (supervision exploitable) + audio |
| 2026-04-27 | Checklist validation audio prod créée | `00_GOUVERNANCE/` | `MERLIN_GOUV_CHECKLIST_VALIDATION_AUDIO_PROD_V1.md` | Recette audio disponible et rejouable | Rejouer la recette avec jonction navigateur réelle |
| 2026-04-27 | Compte rendu état avancement pilote praticiens produit | `00_GOUVERNANCE/` | `MERLIN_GOUV_COMPTE_RENDU_ETAT_AVANCEMENT_PILOTE_PRATICIENS_2026-04-27_v1.0.*` | PDF + HTML générés et archivés | — |
| 2026-05-04 | Quick win 1 — `SlotStatus` nettoyé (5 valeurs parasites retirées) | `10_backend_merlin_api/app/models/enums.py` | `a622b82` | Enum propre, cohérent avec le frontend | — |
| 2026-05-04 | Quick win 2 — CORS `allow_methods` explicite sur FastAPI | `10_backend_merlin_api/app/main.py` | `0a9520a` | Méthodes CORS déclarées explicitement | — |
| 2026-05-04 | Quick win 3 — `POST /{session_id}/room` → `410 Gone` | `10_backend_merlin_api/app/api/routes/sessions.py` | `c8846c5` | Route dépréciée gère ses appels proprement | — |
| 2026-05-04 | Quick win 4 — `require_verified_email_user` sur `hold_slot` + `confirm_slot` | `10_backend_merlin_api/app/core/deps.py` + `routes/bookings.py` | `b43dfe5` | Vérification email obligatoire avant réservation | — |
| 2026-05-04 | Quick win 5 — `RequestChannelCode` enum + modèle + schéma + migration 0017 | `10_backend_merlin_api/` | `fbcd670` | Cohérence frontend/backend sur le canal de demande | `make migrate` VPS en attente |
| 2026-05-04 | Migration 0017 copiée sur VPS via `scp` | VPS `/opt/merlin/10_backend_merlin_api/alembic/versions/` | — | Fichier présent sur le VPS | `make migrate` + `make up` à exécuter |
| 2026-05-04 | `docker-compose.prod.yml` — volume mount `alembic/versions` ajouté | `.` (racine repo) | `c4dc4d5` | Volume disponible pour migrations live | `scp` vers VPS + `make up` |
| 2026-05-04 | `ClientPayload` TypeScript — `record_status` + `data_sensitivity_class` ajoutés | `09_app_ivia_merlin/src/lib/merlin-api.ts` | `62e3a46` | Types frontend alignés avec le backend | — |
| 2026-05-04 | 16 articles éditoriaux IVIA complétés et pushés (sections 1.1 à 4.4) | `04_METHODES/articles/` | `4af888b` (HEAD) | Corpus éditorial complet sur GitHub | Intégration web (Next.js) |
| 2026-05-04 | Système de gestion opérationnel MERLIN V1 — 5 fichiers créés | `00_GOUVERNANCE/` | *(commit en cours)* | Pilotage quotidien opérationnel | Commit + push |

---

## Prochaines entrées attendues

Les entrées suivantes doivent être ajoutées dès que les actions sont réalisées :

| Entrée attendue | Condition |
|---|---|
| `scp` 8 fichiers + `make migrate` + `make up` | Dès l'action VPS effectuée |
| Smoke test post-déploiement | Dès `make up` terminé |
| Recette e2e complète | Dès smoke test OK |
| `middleware.ts` → `proxy.ts` | Dès commit frontend |

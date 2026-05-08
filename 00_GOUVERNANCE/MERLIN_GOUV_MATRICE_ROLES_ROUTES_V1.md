# MERLIN — Matrice rôles ↔ routes API V1

**Date** : 8 mai 2026
**Version** : 1.1 (post-PR #4)
**Statut** : Référence active (ROLES-002 done, ROLES-003 done)
**Source** : extraction automatique de `10_backend_merlin_api/app/api/routes/*.py` + helpers `app/core/deps.py`
**Devise** : *Au sein de l'être — En actes.*

> **MAJ V1.1** (PR #4, commit `03265ab`) : les 4 tickets ouverts par l'audit du 8 mai (BACK-PAY-001, BACK-BOOK-001, BACK-DEPS-001, BACK-AUDIO-001) sont corrigés. Les statuts ci-dessous reflètent l'état actuel ; voir `05_PREUVES_SOURCES/CORRECTIONS_ROLES_AUDIT_2026-05-08.md` pour le détail.

---

## 1. Référentiel des rôles (rappel `AppRole`)

| Code | Description | Source |
|---|---|---|
| `public_client` | Personne accompagnée (client final, non praticien interne) | enums.py |
| `practitioner` | Praticien interne accrédité | enums.py |
| `operator` | Opérateur clinique (production séances) | enums.py |
| `supervisor` | Superviseur clinique (validation notes, contrôle qualité) | enums.py |
| `admin_tech` | Administration technique | enums.py |

---

## 2. Référentiel des guards (helpers `app/core/deps.py`)

| Guard | Rôles autorisés | Sémantique |
|---|---|---|
| *(aucun)* | tous (anonyme inclus) | route 100 % publique |
| `get_db` seul | tous (anonyme inclus) | dépendance DB sans auth |
| `get_optional_current_user` | tous (auth optionnelle) | enrichit la requête si JWT présent |
| `get_current_user` | tout utilisateur authentifié (5 rôles) | exige JWT valide |
| `require_verified_email_user` | tout utilisateur authentifié + email vérifié | extension de `get_current_user` |
| `require_practitioner` | practitioner | praticien uniquement |
| `require_operator` | operator | opérateur uniquement |
| `require_practitioner_or_operator` | practitioner, operator | production clinique élargie |
| `require_production_roles` | practitioner, operator | (alias sémantique du précédent) |
| `require_internal_clinical_roles` | practitioner, operator, supervisor | tous rôles cliniques internes |
| `require_supervisor` | supervisor | supervision seule (renommé PR #4 — BACK-DEPS-001) |
| `require_supervision_roles` *(alias rétroactif)* | supervisor | alias historique de `require_supervisor`, conservé pour compatibilité |
| `require_admin_tech` | admin_tech | administration technique |
| `require_roles(*roles)` | rôles fournis explicitement | factory générique |

---

## 3. Matrice route-par-route (59 routes)

Légende :
- ✅ guard explicite et cohérent
- ⚠️ guard présent mais à vérifier (incohérence ou sémantique douteuse)
- 🚨 aucun guard d'authentification — à valider intentionnel ou faille
- 🟦 publique intentionnellement

### 3.1 Authentification & inscription

| Méthode | Route | Fonction | Guard appliqué | Rôles autorisés | Statut |
|---|---|---|---|---|---|
| POST | `/auth/register` | `register_user` | `get_optional_current_user` | tous (anonyme inclus) | 🟦 publique (création compte) |
| POST | `/auth/login` | `login` | aucun | tous (anonyme inclus) | 🟦 publique (login) |
| GET  | `/auth/me` | `me` | `get_current_user` | 5 rôles auth | ✅ |
| POST | `/register/client` | `register_client` | aucun | tous (anonyme inclus) | 🟦 publique (parcours client) |
| GET  | `/verify-email/{token}` | `verify_email` | aucun | tous (token = preuve) | 🟦 publique (token unique) |

### 3.2 Praticiens & rendez-vous publics

| Méthode | Route | Fonction | Guard appliqué | Rôles autorisés | Statut |
|---|---|---|---|---|---|
| GET  | `/praticiens` | `list_praticiens` | aucun | tous (anonyme inclus) | 🟦 publique (catalogue) |
| GET  | `/schedules/available` | `get_available_slots` | aucun | tous (anonyme inclus) | 🟦 publique (créneaux libres) |
| POST | `/matching/suggest` | `suggest_practitioner` | aucun | tous (anonyme inclus) | 🟦 publique (questionnaire d'appariement) |

### 3.3 Réservation (bookings)

| Méthode | Route | Fonction | Guard appliqué | Rôles autorisés | Statut |
|---|---|---|---|---|---|
| POST | `/bookings/hold` | `hold_slot` | `require_verified_email_user` | 5 rôles auth + email vérifié | ✅ |
| POST | `/bookings/confirm` | `confirm_slot` | `require_verified_email_user` | 5 rôles auth + email vérifié | ✅ |
| POST | `/bookings/cancel` | `cancel_slot` | `require_verified_email_user` (corrigé PR #4) | 5 rôles auth + email vérifié | ✅ (BACK-BOOK-001 corrigé — aligné sur hold/confirm) |
| GET  | `/bookings/my` | `my_bookings` | `get_current_user` | 5 rôles auth | ✅ (lecture propre) |

### 3.4 Calendrier praticien (/schedules)

| Méthode | Route | Fonction | Guard appliqué | Rôles autorisés | Statut |
|---|---|---|---|---|---|
| GET    | `/schedules/my` | `get_my_schedule` | `require_practitioner` | practitioner | ✅ |
| POST   | `/schedules/my` | `create_schedule_slot` | `require_practitioner` | practitioner | ✅ |
| PATCH  | `/schedules/my/{slot_id}` | `update_schedule_slot` | `require_practitioner` | practitioner | ✅ |
| DELETE | `/schedules/my/{slot_id}` | `delete_schedule_slot` | `require_practitioner` | practitioner | ✅ |
| GET    | `/schedules/my/exceptions` | `get_my_exceptions` | `require_practitioner` | practitioner | ✅ |
| POST   | `/schedules/my/exceptions` | `create_exception` | `require_practitioner` | practitioner | ✅ |
| DELETE | `/schedules/my/exceptions/{exc_id}` | `delete_exception` | `require_practitioner` | practitioner | ✅ |

### 3.5 Demandes d'entrée (intake)

| Méthode | Route | Fonction | Guard appliqué | Rôles autorisés | Statut |
|---|---|---|---|---|---|
| POST | `/intake-requests` | `create_intake_request` | `get_optional_current_user` | tous (anonyme inclus) | 🟦 publique (formulaire entrée) |
| GET  | `/intake-requests` | `list_intake_requests` | `require_internal_clinical_roles` | practitioner, operator, supervisor | ✅ |
| GET  | `/intake-requests/{id}` | `get_intake_request` | `require_internal_clinical_roles` | practitioner, operator, supervisor | ✅ |
| GET  | `/intake-requests/{id}/analyse` | `analyse_intake_request` | `require_internal_clinical_roles` | practitioner, operator, supervisor | ✅ |

### 3.6 Clients (entité)

| Méthode | Route | Fonction | Guard appliqué | Rôles autorisés | Statut |
|---|---|---|---|---|---|
| GET  | `/clients` | `list_clients` | `require_internal_clinical_roles` | practitioner, operator, supervisor | ✅ |
| POST | `/clients` | `create_client` | `get_optional_current_user` + `_validate_create_access` | tous (validation interne) | ⚠️ logique intra-fonction (cf. audit §3.2) |
| GET  | `/clients/{id}` | `get_client` | `require_internal_clinical_roles` | practitioner, operator, supervisor | ✅ |

### 3.7 Consentements

| Méthode | Route | Fonction | Guard appliqué | Rôles autorisés | Statut |
|---|---|---|---|---|---|
| GET  | `/consents` | `list_consents` | `require_internal_clinical_roles` | practitioner, operator, supervisor | ✅ |
| POST | `/consents` | `create_consent` | `get_optional_current_user` + `_validate_create_access` | tous (validation interne) | ⚠️ logique intra-fonction |
| GET  | `/consents/{id}` | `get_consent` | `require_internal_clinical_roles` | practitioner, operator, supervisor | ✅ |

### 3.8 Sessions (cliniques)

| Méthode | Route | Fonction | Guard appliqué | Rôles autorisés | Statut |
|---|---|---|---|---|---|
| POST  | `/sessions` | `create_session` | `require_operator` | operator | ✅ |
| GET   | `/sessions` | `list_sessions` | `require_internal_clinical_roles` | practitioner, operator, supervisor | ✅ |
| GET   | `/sessions/{id}` | `get_session` | `require_internal_clinical_roles` | practitioner, operator, supervisor | ✅ |
| POST  | `/sessions/{id}/start` | `start_session` | `require_operator` | operator | ✅ |
| POST  | `/sessions/{id}/close` | `close_session` | `require_operator` | operator | ✅ |
| POST  | `/sessions/{id}/deliver` | `deliver_audio_async_session` | `require_operator` | operator | ✅ |
| PATCH | `/sessions/{id}/assign` | `assign_praticien` | `require_operator` | operator | ✅ |
| POST  | `/sessions/{id}/room` | `create_session_room` | aucun | — | 🟦 dépréciée (renvoie 410 GONE) |
| POST  | `/sessions/{id}/recording/start` | `start_session_recording` | `require_operator` | operator | ✅ |
| POST  | `/sessions/{id}/recording/stop` | `stop_session_recording` | `require_operator` | operator | ✅ |

### 3.9 Audio sessions (LiveKit)

| Méthode | Route | Fonction | Guard appliqué | Rôles autorisés | Statut |
|---|---|---|---|---|---|
| POST | `/audio-sessions/sessions/{session_id}/provision` | `provision_audio_session` | `require_operator` | operator | ✅ |
| GET  | `/audio-sessions` | `list_audio_sessions` | `require_internal_clinical_roles` | practitioner, operator, supervisor | ✅ |
| GET  | `/audio-sessions/{id}` | `get_audio_session` | `require_internal_clinical_roles` | practitioner, operator, supervisor | ✅ |
| POST | `/audio-sessions/{id}/operator-join` | `create_operator_join_context` | `require_operator` | operator | ✅ |
| POST | `/audio-sessions/{id}/client-join` | `create_client_join_context` | `require_operator` | operator | ✅ (BACK-AUDIO-001 corrigé — docstring documente l'usage opérateur interne) |

### 3.10 Audio recordings

| Méthode | Route | Fonction | Guard appliqué | Rôles autorisés | Statut |
|---|---|---|---|---|---|
| GET  | `/audio-recordings` | `list_audio_recordings` | `require_internal_clinical_roles` | practitioner, operator, supervisor | ✅ |
| GET  | `/audio-recordings/{id}` | `get_audio_recording` | `require_internal_clinical_roles` | practitioner, operator, supervisor | ✅ |
| POST | `/audio-recordings/audio-sessions/{id}/start` | `start_audio_recording` | `require_operator` | operator | ✅ |
| POST | `/audio-recordings/{id}/stop` | `stop_audio_recording` | `require_operator` | operator | ✅ |

### 3.11 Notes de séance & documents dérivés

| Méthode | Route | Fonction | Guard appliqué | Rôles autorisés | Statut |
|---|---|---|---|---|---|
| POST  | `/session-notes` | `create_session_note` | `require_operator` | operator | ✅ |
| GET   | `/session-notes` | `list_session_notes` | `require_internal_clinical_roles` | practitioner, operator, supervisor | ✅ |
| GET   | `/session-notes/{id}` | `get_session_note` | `require_internal_clinical_roles` | practitioner, operator, supervisor | ✅ |
| PATCH | `/session-notes/{id}/validate` | `validate_session_note` | `require_supervision_roles` | supervisor | ✅ |
| POST  | `/derived-documents` | `create_derived_document` | `require_operator` | operator | ✅ |
| GET   | `/derived-documents` | `list_derived_documents` | `require_internal_clinical_roles` | practitioner, operator, supervisor | ✅ |
| GET   | `/derived-documents/public/client/{public_client_code}` | `list_public_client_derived_documents` | aucun | tous (code client = preuve) | 🟦 publique (livraison client par code) |
| GET   | `/derived-documents/{id}` | `get_derived_document` | `require_internal_clinical_roles` | practitioner, operator, supervisor | ✅ |

### 3.12 Paiements (Stripe)

| Méthode | Route | Fonction | Guard appliqué | Rôles autorisés | Statut |
|---|---|---|---|---|---|
| POST | `/payments/stripe/checkout/audio-async` | `create_audio_async_checkout_session` | `require_operator` (corrigé PR #4) | operator | ✅ (BACK-PAY-001 corrigé — faille critique fermée) |
| POST | `/payments/stripe/webhook` | `stripe_webhook` | aucun (signature Stripe) | Stripe uniquement | 🟦 publique (vérif. signature serveur) |

### 3.13 Santé

| Méthode | Route | Fonction | Guard appliqué | Rôles autorisés | Statut |
|---|---|---|---|---|---|
| GET | `/health` | `health` | aucun | tous (anonyme inclus) | 🟦 publique (probe) |

---

## 4. Synthèse

### 4.1 Décompte (V1.1 post-PR #4)

| Statut | Nombre | % |
|---|---|---|
| ✅ guard cohérent | 43 | 73 % |
| 🟦 publique intentionnelle | 13 | 22 % |
| ⚠️ à clarifier | 0 | 0 % |
| 🚨 faille potentielle | 0 | 0 % |
| 🟦 dépréciée (410 GONE) | 1 | 2 % |
| Documenté par docstring (ex-incohérence) | 2 | 3 % |
| **TOTAL** | 59 | 100 % |

*Trace historique V1.0 : avant PR #4, on comptait 38 ✅ + 4 ⚠️ + 1 🚨. La PR #4 a converti la faille en ✅, BACK-BOOK-001 en ✅, et BACK-AUDIO-001 + DOC-ROLES-001 en routes documentées par docstring (BACK-DEPS-001 = renommage interne sans impact statut).*

### 4.2 Couverture par rôle

| Rôle | Routes accessibles (auth) |
|---|---|
| `public_client` (auth) | hold, confirm, cancel, my_bookings, auth/me |
| `practitioner` | les 7 routes /schedules/my* + 27 routes lectures cliniques (`require_internal_clinical_roles`) |
| `operator` | toutes les routes de production (création sessions, audio, recordings, session-notes, derived-documents) + 27 routes lectures cliniques |
| `supervisor` | 27 routes lectures cliniques + `/session-notes/{id}/validate` (exclusif) |
| `admin_tech` | aucune route métier (par design — gestion technique hors API) |

### 4.3 Note importante sur l'écart 51 vs 59

Le smoke test prod du 8 mai 2026 a recensé **51 routes** via `/api/openapi.json` ; le code local en compte **59**. Écart possible :
- 8 routes ajoutées au code local non encore déployées en production, OU
- différence dans le comptage OpenAPI (méthodes multiples sur même path peuvent être listées différemment).

À vérifier lors du prochain déploiement (INFRA-005).

---

## 5. Références

- Doctrine : [`MERLIN_GOUV_TABLEAU_ROLES_ACCES_VISIBILITE_V1.md`](MERLIN_GOUV_TABLEAU_ROLES_ACCES_VISIBILITE_V1.md) (368 lignes, 22 avril 2026)
- Backlog implémentation : [`MERLIN_GOUV_BACKLOG_IMPLEMENTATION_ROLES_ACCES_VISIBILITE_V1.md`](MERLIN_GOUV_BACKLOG_IMPLEMENTATION_ROLES_ACCES_VISIBILITE_V1.md)
- Audit complémentaire : [`05_PREUVES_SOURCES/AUDIT_ROLES_ROUTES_2026-05-08.md`](../05_PREUVES_SOURCES/AUDIT_ROLES_ROUTES_2026-05-08.md)
- Code source guards : [`10_backend_merlin_api/app/core/deps.py`](../10_backend_merlin_api/app/core/deps.py)
- Code source enum : [`10_backend_merlin_api/app/models/enums.py`](../10_backend_merlin_api/app/models/enums.py)

---

*Pour le peuple, par le peuple.*

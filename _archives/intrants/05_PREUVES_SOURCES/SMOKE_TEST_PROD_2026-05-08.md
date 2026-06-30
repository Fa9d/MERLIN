---
id: SMOKE-PROD-2026-05-08
type: preuve / recette prod
date: 2026-05-08
auteur: David Phaneuf (audit assisté)
contexte: Validation INFRA-001 → INFRA-004 du Backlog Maître V2
statut: ✅ PASS
---

# Smoke test production MERLIN — 8 mai 2026

## Contexte

Le backlog maître V2 (daté du 6 mai 2026) listait `INFRA-001` à `INFRA-004` comme `todo`. Vérification à distance le 8 mai 2026 démontre que ces tickets sont en réalité **réalisés** : l'API tourne en prod, le code prod = code local, le schéma BD est aligné.

## Méthode

Smoke test exclusivement à distance (HTTPS) — aucun accès SSH au VPS requis pour cette vérification.

- Endpoint santé inspecté
- OpenAPI prod téléchargé et comparé au code local
- 6 routes critiques testées (publiques + auth + validation)
- Schéma `PraticienPublic` comparé entre prod et local

## Résultats

### 1. Santé API

| Endpoint | Statut HTTP | Réponse |
|---|---|---|
| `GET https://api.ivia.quebec/api/health` | `200` | `{"status":"ok","service":"MERLIN API","environment":"production","database":"ok"}` |

### 2. Frontend production

| URL | Statut |
|---|---|
| `https://ivia.quebec` | `200` |
| `https://ivia.quebec/praticiens` | `200` |
| `https://ivia.quebec/demarche` | `200` |
| `https://ivia.quebec/rendez-vous` | `200` |
| `https://ivia.quebec/ressources` | `200` |

### 3. OpenAPI / parité routes

- OpenAPI exposé sur `https://api.ivia.quebec/api/openapi.json` (51 routes)
- Documentation interactive : `/api/docs`, `/api/redoc`
- **Comparaison code local vs prod** : 48/48 routes définies en local sont présentes en prod (les écarts apparents proviennent de routers à préfixe interne, pas de routes manquantes)

### 4. Routes critiques testées

| Méthode | Endpoint | Statut attendu | Statut obtenu |
|---|---|---|---|
| `GET` | `/api/health` | 200 | ✅ 200 |
| `GET` | `/api/v1/praticiens` | 200 | ✅ 200 (1 praticien publié) |
| `GET` | `/api/v1/auth/me` (sans token) | 401 | ✅ 401 |
| `POST` | `/api/v1/intake-requests` (body vide) | 422 | ✅ 422 (Pydantic actif) |
| `POST` | `/api/v1/auth/login` (body vide) | 422 | ✅ 422 |
| `POST` | `/api/v1/register/client` (body vide) | 422 | ✅ 422 |

### 5. Cohérence schéma BD

`GET /api/v1/praticiens` retourne pour le praticien publié les champs : `id`, `display_name`, `title_line`, `intro_text`, `spoken_languages`, `available_channels`.

C'est exactement le schéma `PraticienPublic` défini dans `app/schemas/auth.py` local. Aucun drift.

## Conclusion

| Ticket | Ancien statut | Nouveau statut | Preuve |
|---|---|---|---|
| INFRA-001 | `todo` | `done` | OpenAPI prod = code local (48 routes) |
| INFRA-002 | `todo` | `done` | Schéma `PraticienPublic` prod = local |
| INFRA-003 | `todo` | `done` | `/api/health` 200, env=production, db=ok |
| INFRA-004 | `todo` | `done` | 6 endpoints testés, codes attendus reçus |
| CONT-002 | `todo` | `done` | `ivia.quebec/ressources` répond 200 |

## Limites de cette preuve

- **Pas testé** : version exacte de la migration Alembic appliquée en prod (nécessite SSH). Hypothèse : la dernière migration `0018_add_match_fields_to_practitioner_profile` est probablement appliquée mais le schéma `PraticienPublic` ne dépend pas des champs match donc impossible de confirmer à distance.
- **Pas testé** : INFRA-005 (recette e2e complète opérateur+superviseur), INFRA-006 (audio prod LiveKit), INFRA-007 (cookies sécurisés + CORS), INFRA-008 (Certbot dry-run) — tous restent `todo`.

## Suite

Recette `INFRA-005`, `INFRA-006`, `INFRA-007` à planifier dans le pilote MERLIN actif (Mylène + Émilie). Documentation à conserver dans le journal pilote.

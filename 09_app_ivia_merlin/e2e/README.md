# Tests e2e — IVIA / MERLIN

Tests end-to-end Playwright pour le frontend Next.js.

## Périmètre

**Couvert** :
- Pages publiques (5) : accueil, praticiens, démarche, rendez-vous, ressources
- API santé : `/api/health`, `/api/openapi.json`
- Routes critiques publiques : `/api/v1/praticiens`
- Sécurité : endpoints protégés rejettent sans auth (401)
- Validation Pydantic : endpoints refusent body vide (422)
- Console JS : aucune erreur sur pages publiques

**Pas couvert (à venir)** :
- Parcours réservation authentifié (FRONT-004 : hold → confirm → confirmation)
- Espace praticien authentifié (FRONT-005)
- Rôles & accès (ROLES-009)
- Performance / Lighthouse (FRONT-006)

## Installation

```bash
cd 09_app_ivia_merlin
npm install
npm run test:e2e:install   # télécharge le binaire Chromium (~300 MB)
```

## Utilisation

### Tester contre la production (par défaut)

```bash
npm run test:e2e
# ou explicitement
npm run test:e2e:prod
```

Les tests ciblent `https://ivia.quebec` et `https://api.ivia.quebec`.

⚠️ **Aucune action mutative n'est exécutée en prod.** Tous les tests POST utilisent des body vides pour vérifier la validation Pydantic.

### Tester en local

Démarrer en parallèle dans deux terminaux :

```bash
# terminal 1 : API
cd 10_backend_merlin_api
uvicorn app.main:app --reload --port 8000

# terminal 2 : frontend
cd 09_app_ivia_merlin
npm run dev   # port 3000

# terminal 3 : tests
cd 09_app_ivia_merlin
npm run test:e2e:local
```

### Variables d'environnement

| Variable | Défaut | Description |
|---|---|---|
| `BASE_URL` | `https://ivia.quebec` | URL frontend |
| `API_BASE_URL` | `https://api.ivia.quebec` | URL API |
| `CI` | — | si présent : 2 retries, 1 worker, reporter github |

## Structure

```
e2e/
├── README.md                          ← ce fichier
├── parcours-public-critique.spec.ts   ← pages publiques + console errors
└── api-sante-prod.spec.ts             ← API health, openapi, sécurité, validation
```

## CI/CD (à venir)

Les tests sont prêts à être exécutés par GitHub Actions. Voir `ROLES-009` pour le plan d'intégration. Les artefacts (traces, screenshots, vidéos) sont générés en cas d'échec uniquement.

## Convention

- 1 spec = 1 préoccupation
- `test.describe()` regroupe les assertions logiquement liées
- Aucun mock : on teste ce qui est réellement déployé
- Messages d'erreur explicites : `expect(x, 'pourquoi').toBe(y)`

## Référence

- Backlog : `00_GOUVERNANCE/MERLIN_GOUV_BACKLOG_MAITRE_V2.md` FRONT-004
- Smoke test prod : `05_PREUVES_SOURCES/SMOKE_TEST_PROD_2026-05-08.md`

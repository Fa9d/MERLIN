# Skill — repo-map

> À charger pour s'orienter avant une modif transverse, sans lire tout le monorepo.

## Carte minimale

```
MERLIN/
├── 00_ai/                  # Cette structure (skills, lessons)
├── 00_GOUVERNANCE/         # Décisions, backlog, journal — lecture seule pour agents code
├── 04_METHODES/            # Méthodes cliniques, cas simulés
├── 05_PREUVES_SOURCES/     # Audits, base de connaissance
├── 09_app_ivia_merlin/     # Frontend Next.js 16 (IVIA) — voir skill ivia-frontend
├── 10_backend_merlin_api/  # Backend FastAPI — voir skill merlin-backend
├── 11_PROMPTS/             # Prompts IA versionnés — bumper la version à toute modif
├── 12_JURIDIQUE_AFFAIRES/  # Stratégique / juridique — ne pas toucher sans demande explicite
├── deploy/                 # prod-up.sh et scripts
├── docs/                   # Docs ops (deploy-ovh, ops-docker-compose, ai-workflow)
├── nginx/                  # Conf Nginx + Certbot
└── docker-compose.{,prod}.yml
```

## Où chercher quoi

| Besoin | Aller voir |
|---|---|
| Endpoint API existant | `10_backend_merlin_api/app/api/routes/` |
| Modèle SQLAlchemy | `10_backend_merlin_api/app/models/` |
| Schéma Pydantic | `10_backend_merlin_api/app/schemas/` |
| Migration DB | `10_backend_merlin_api/alembic/versions/` |
| Page / route Next.js | `09_app_ivia_merlin/src/app/` |
| Client API frontend | `09_app_ivia_merlin/src/lib/merlin-api.ts` |
| Prompt système | `11_PROMPTS/<domaine>/<nom>.md` |
| Décision produit | `00_GOUVERNANCE/` |

## Règles d'exploration

- **Pas de `find` ou `grep -r` aveugle** sur la racine — exclure `node_modules/`, `.next/`, `.venv/`, `prisma/generated/`.
- Préférer `Glob`/`Grep` ciblé par sous-projet.
- Si tu cherches un symbole, commencer par le sous-projet le plus probable (frontend vs backend) avant d'élargir.
- Ne lire `00_GOUVERNANCE/` qu'à la demande explicite — gros volume textuel français, peu utile pour le code.

## Sortie attendue après orientation

Avant d'écrire du code, énoncer en 1 phrase : *« je modifie X dans `<chemin>` parce que Y »*. Si ce n'est pas clair, recharger ce skill ou demander.

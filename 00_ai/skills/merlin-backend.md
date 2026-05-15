# Skill — merlin-backend

> À charger pour tout travail dans `10_backend_merlin_api/`.

## Stack

- Python 3 / FastAPI / SQLAlchemy 2 / Alembic.
- PostgreSQL 15 — migration HEAD : `20260504_0017` (vérifier avec `alembic current`).
- Tests : `pytest` (`pytest.ini` à la racine du backend).

## Layout

```
10_backend_merlin_api/app/
├── main.py                 # FastAPI app, CORS, montage routers
├── core/
│   ├── deps.py             # require_verified_email_user, get_current_user
│   └── config.py
├── models/                 # SQLAlchemy + enums
├── schemas/                # Pydantic
├── api/routes/             # Endpoints — un fichier par domaine
└── alembic/versions/       # Migrations
```

## Conventions

- **Auth** : utiliser les deps existantes (`require_verified_email_user`, `get_current_user`) — ne pas réimplémenter.
- **Enums** : centralisés dans `app/models/enums.py` (`SlotStatus`, `RequestChannelCode`, …). Réutiliser, ne pas dupliquer en string.
- **Endpoint déprécié** : `POST /sessions/{id}/room` retourne `410 Gone` — ne pas le rétablir.
- **Migrations** : toute modif de modèle ⇒ `alembic revision --autogenerate -m "<desc>"` puis revue manuelle du diff avant `upgrade head`.

## Commandes locales

```bash
cd 10_backend_merlin_api
# venv Windows par défaut dans CLAUDE.md ; sur Linux : python -m venv .venv && source .venv/bin/activate
python -m uvicorn app.main:app --reload
pytest                                  # tests
alembic current                         # version DB
alembic upgrade head                    # appliquer migrations
alembic revision --autogenerate -m "…"  # nouvelle migration
```

## Prod / déploiement

- Ne **jamais** appeler `docker compose` sans `--env-file .env.prod`.
- Préférer `make <cible>` ou `bash deploy/prod-up.sh`. Voir `docs/ops-docker-compose.md`.
- `scp` ciblé acceptable pour hotfix : `scp 10_backend_merlin_api/app/<fichier> ubuntu@137.74.42.121:/opt/merlin/10_backend_merlin_api/app/<fichier>`.

## Anti-patterns

- Logique métier dans une route → la déplacer dans un service/module dédié.
- Validation manuelle alors qu'un schéma Pydantic existe.
- Hardcoder une clé/URL d'env — passer par `app/core/config.py`.

## Avant de marquer terminé

Charger [`verification`](verification.md). Au minimum : `pytest` + `alembic current` (cohérence migration).

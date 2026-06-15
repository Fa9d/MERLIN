---
paths:
  - "10_backend_merlin_api/**"
---

# Règles backend (FastAPI / SQLAlchemy / Alembic)

- Toute route nouvelle doit être déclarée dans `app/api/routes/` et enregistrée dans `main.py`.
- La protection d'une route se fait via `require_verified_email_user()` ou `get_current_user()` depuis `app/core/deps.py` — jamais inline.
- Chaque migration Alembic : un seul fichier, révision séquentielle, format `YYYYMMDD_NNNN_<slug>.py`.
- Après `alembic upgrade head`, vérifier avec `make prod-ps` que le conteneur DB est sain.
- Aucune clé API ni secret dans le code — toujours via `config.py` / `.env`.
- HEAD courant des migrations : `20260615_0029`. Avant toute nouvelle migration, `alembic current`.
- Schémas Pydantic : `app/schemas/` — distinguer `Create`, `Read`, `Update`.
- Enums métier dans `app/models/enums.py` — ne pas dupliquer ailleurs.
- Commandes officielles : `make migrate`, `make prod-logs-api`, `make config-check`.

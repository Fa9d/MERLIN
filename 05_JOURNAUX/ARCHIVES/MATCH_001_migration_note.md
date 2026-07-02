# MATCH-001 — Note de migration Alembic

## Commande à exécuter

```bash
cd 10_backend_merlin_api
alembic revision --autogenerate -m "add_practitioner_profiles"
alembic upgrade head
```

## Ce que la migration crée

Table `practitioner_profiles` avec :
- `id` SERIAL PRIMARY KEY
- `user_id` INTEGER UNIQUE FK → `users.id`
- `display_name` VARCHAR(120) NOT NULL
- `slug` VARCHAR(120) UNIQUE NOT NULL (index)
- `bio` TEXT
- `photo_url` VARCHAR(500)
- `domaines` TEXT[] — ex: `{travail,anxiete}`
- `approches` TEXT[] — ex: `{ecoute_active,narratif}`
- `langues` TEXT[] — ex: `{fr}`
- `disponibilites` TEXT[] — ex: `{soir,fin_semaine}`
- `tarif_horaire` INTEGER (cents CAD, nullable)
- `actif` BOOLEAN DEFAULT TRUE
- `created_at` TIMESTAMPTZ DEFAULT now()
- `updated_at` TIMESTAMPTZ (auto on update)

## Relation User à ajouter

Dans `app/models/user.py`, ajouter :

```python
from sqlalchemy.orm import relationship

# Dans la classe User :
practitioner_profile = relationship(
    "PractitionerProfile",
    back_populates="user",
    uselist=False
)
```

## Enregistrement du router

Dans `app/main.py` :

```python
from app.routers import matching
app.include_router(matching.router)
```

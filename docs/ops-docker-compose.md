# Exploitation Docker Compose — MERLIN prod

## Pourquoi `--env-file .env.prod` est obligatoire

`docker-compose.prod.yml` utilise des variables pour les ports LiveKit :

```yaml
ports:
  - "${LIVEKIT_RTC_PORT_RANGE_START}-${LIVEKIT_RTC_PORT_RANGE_END}:${LIVEKIT_RTC_PORT_RANGE_START}-${LIVEKIT_RTC_PORT_RANGE_END}/udp"
```

Sans `--env-file`, ces variables restent vides, ce qui produit `"-:/udp"` et l'erreur :

```
invalid containerPort: -
```

Docker Compose **ne charge pas automatiquement `.env.prod`**. Il chercherait `.env` à la racine
(qui n'existe pas dans ce repo). L'`--env-file` est donc obligatoire à chaque invocation directe.

---

## Commandes officielles

Toutes les commandes prod passent par le **Makefile**, qui intègre déjà `--env-file .env.prod` :

```bash
# Démarrer / rebuilder la stack
make up

# Appliquer les migrations Alembic
make migrate

# État des conteneurs
make prod-ps

# Logs de l'API (temps réel)
make prod-logs-api

# Tous les logs
make prod-logs

# Valider la config avant tout redémarrage
make config-check

# Arrêter la stack
make down
```

---

## Script de déploiement complet

Pour un déploiement en une seule commande (depuis `/opt/merlin`) :

```bash
bash deploy/prod-up.sh
```

Ce script enchaîne : `config-check → up --build → wait healthy → alembic upgrade head`.

---

## Diagnostic standard

```bash
# Vérifier la config (ne démarre rien)
docker compose --env-file .env.prod -f docker-compose.prod.yml config --quiet

# État des conteneurs
docker compose --env-file .env.prod -f docker-compose.prod.yml ps

# Smoke test API
curl -s https://api.ivia.quebec/api/health | python3 -m json.tool

# Smoke test frontend
curl -o /dev/null -sw "ivia.quebec: HTTP %{http_code}\n" https://ivia.quebec

# Logs d'un conteneur spécifique
docker compose --env-file .env.prod -f docker-compose.prod.yml logs -f --tail=200 api
docker compose --env-file .env.prod -f docker-compose.prod.yml logs -f --tail=200 frontend
docker compose --env-file .env.prod -f docker-compose.prod.yml logs -f --tail=200 nginx

# Migration Alembic (état courant)
docker compose --env-file .env.prod -f docker-compose.prod.yml exec -T api alembic current
```

---

## Règle d'or

> **Ne jamais appeler `docker compose` directement sans `--env-file .env.prod` sur ce projet.**
> Utiliser `make <cible>` ou `bash deploy/prod-up.sh`.

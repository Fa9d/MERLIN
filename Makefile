ENV_FILE ?= .env.prod
COMPOSE = docker compose --env-file $(ENV_FILE) -f docker-compose.prod.yml

.PHONY: up down restart logs migrate ps prod-ps prod-logs-api prod-logs config-check

up:
	$(COMPOSE) up -d --build

down:
	$(COMPOSE) down

restart:
	$(COMPOSE) restart

logs:
	$(COMPOSE) logs -f --tail=200

migrate:
	$(COMPOSE) exec -T api alembic upgrade head

# --- Diagnostic prod ---
ps:
	$(COMPOSE) ps

prod-ps:
	$(COMPOSE) ps

prod-logs-api:
	$(COMPOSE) logs -f --tail=200 api

prod-logs:
	$(COMPOSE) logs -f --tail=200

config-check:
	$(COMPOSE) config --quiet && echo "CONFIG VALIDE"

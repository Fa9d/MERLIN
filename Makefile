ENV_FILE ?= .env.prod
COMPOSE = docker compose --env-file $(ENV_FILE) -f docker-compose.prod.yml

.PHONY: up down restart logs migrate ps prod-ps prod-logs-api prod-logs config-check validate-managed-agents telescope-minimal telescope-note-e2e

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

validate-managed-agents:
	python tools/validate_managed_agents.py

telescope-minimal:
	python tools/run_telescope_minimal.py

telescope-note-e2e:
	python tools/run_telescope_note_e2e.py

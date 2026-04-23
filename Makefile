ENV_FILE ?= .env.prod
COMPOSE = docker compose --env-file $(ENV_FILE) -f docker-compose.prod.yml

.PHONY: up down logs migrate

up:
	$(COMPOSE) up -d --build

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f --tail=200

migrate:
	$(COMPOSE) exec -T api alembic upgrade head

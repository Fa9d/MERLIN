#!/bin/bash
set -e
cd /opt/merlin

echo "=== BUILD API ==="
docker compose --env-file .env.prod -f docker-compose.prod.yml build api
echo "Build API termine."

echo ""
echo "=== MIGRATION ALEMBIC ==="
docker compose --env-file .env.prod -f docker-compose.prod.yml run --rm api alembic upgrade head
echo "Migration terminee."

echo ""
echo "=== RESTART API ==="
docker compose --env-file .env.prod -f docker-compose.prod.yml up -d --no-deps api
echo "API redemarree."

echo ""
echo "=== BUILD FRONTEND ==="
docker compose --env-file .env.prod -f docker-compose.prod.yml build frontend
echo "Build frontend termine."

echo ""
echo "=== RESTART FRONTEND ==="
docker compose --env-file .env.prod -f docker-compose.prod.yml up -d --no-deps frontend
echo "Frontend redemarre."

echo ""
echo "=== ETAT FINAL ==="
docker compose --env-file .env.prod -f docker-compose.prod.yml ps

#!/usr/bin/env bash
# deploy/prod-up.sh — Déploiement prod complet
#
# Usage (depuis /opt/merlin sur le VPS) :
#   bash deploy/prod-up.sh
#
# Pré-requis : .env.prod présent dans le répertoire courant.

set -euo pipefail

COMPOSE="docker compose --env-file .env.prod -f docker-compose.prod.yml"

echo "==> [1/4] Vérification de la configuration..."
$COMPOSE config --quiet
echo "    CONFIG VALIDE"

echo "==> [2/4] Démarrage / rebuild de la stack..."
$COMPOSE up -d --build

echo "==> [3/4] Attente que l'API soit healthy..."
for i in $(seq 1 24); do
  STATUS=$(docker inspect --format='{{.State.Health.Status}}' merlin-api-1 2>/dev/null || echo "absent")
  if [ "$STATUS" = "healthy" ]; then
    echo "    API healthy"
    break
  fi
  if [ "$i" -eq 24 ]; then
    echo "    ERREUR : API non healthy après 120s"
    docker logs --tail=50 merlin-api-1 2>&1 || true
    exit 1
  fi
  sleep 5
done

echo "==> [4/4] Application des migrations Alembic..."
$COMPOSE exec -T api alembic upgrade head

echo ""
echo "==> Déploiement terminé."
$COMPOSE ps

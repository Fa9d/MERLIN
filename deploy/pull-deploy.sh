#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Déploiement TRACÉ — la prod est alignée sur un commit Git (remplace le tar manuel).
#
#   • Statique seul (site ivia_site_v2/) : `git pull` suffit — nginx sert les fichiers
#     directement depuis /opt/merlin/ivia_site_v2 (bind mount).
#   • Backend / docker-compose / migrations : ajouter --build → rebuild image + alembic.
#
# Prérequis : /opt/merlin est un dépôt Git (clé de déploiement lecture seule configurée
# via git config core.sshCommand). Workflow : commit + push en local → pull-deploy sur le VPS.
#
# Usage (depuis le VPS) : bash deploy/pull-deploy.sh [--build]
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail
cd /opt/merlin

echo "Avant : $(git rev-parse --short HEAD) — $(git log -1 --pretty=%s)"
git pull --ff-only
echo "Après : $(git rev-parse --short HEAD) — $(git log -1 --pretty=%s)"

if [ "${1:-}" = "--build" ]; then
  echo "Rebuild de la stack + migrations Alembic…"
  bash deploy/prod-up.sh
fi

# ── Smoke test post-déploiement (M14) : un déploiement cassé doit crier ICI, ──
# ── pas dans le navigateur d'un client. Échec = code retour non nul.        ──
echo "Smoke test…"
SMOKE_FAIL=0

api_health="$(curl -fsS -o /dev/null -w '%{http_code}' --max-time 10 https://api.ivia.quebec/api/health || echo ERR)"
if [ "$api_health" = "200" ]; then
  echo "  ✓ API health 200"
else
  echo "  ✗ API health: $api_health (attendu 200)"; SMOKE_FAIL=1
fi

site_home="$(curl -fsS -o /dev/null -w '%{http_code}' --max-time 10 https://ivia.quebec/ || echo ERR)"
if [ "$site_home" = "200" ]; then
  echo "  ✓ Accueil ivia.quebec 200"
else
  echo "  ✗ Accueil: $site_home (attendu 200)"; SMOKE_FAIL=1
fi

if [ "${1:-}" = "--build" ]; then
  # Le head Alembic appliqué en DB doit être le head des fichiers déployés.
  head_fichiers="$(docker compose --env-file .env.prod -f docker-compose.prod.yml \
      exec -T api alembic heads 2>/dev/null | grep -oE '^[a-z0-9_]+' | head -1 || echo ERR)"
  head_db="$(docker compose --env-file .env.prod -f docker-compose.prod.yml \
      exec -T api alembic current 2>/dev/null | grep -oE '^[a-z0-9_]+' | head -1 || echo ERR)"
  if [ "$head_db" = "$head_fichiers" ] && [ "$head_db" != "ERR" ]; then
    echo "  ✓ Alembic: DB au head $head_db"
  else
    echo "  ✗ Alembic: DB=$head_db, fichiers=$head_fichiers"; SMOKE_FAIL=1
  fi
fi

if [ "$SMOKE_FAIL" -ne 0 ]; then
  echo "✗ SMOKE TEST ÉCHOUÉ — la prod ne répond pas comme attendu. Voir docs/ops-docker-compose.md ;"
  echo "  rollback : git checkout <commit_precedent> && bash deploy/pull-deploy.sh --build"
  exit 1
fi

echo "✓ Prod alignée sur le commit $(git rev-parse --short HEAD) — smoke test OK."

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

echo "✓ Prod alignée sur le commit $(git rev-parse --short HEAD)."

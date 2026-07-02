#!/usr/bin/env sh
set -eu

ROOT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"

cd "$ROOT_DIR"

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git pull --ff-only
else
  echo "No git repository detected at $ROOT_DIR, skipping git pull."
fi

docker compose build
docker compose up -d
docker compose exec -T backend alembic upgrade head
docker compose ps

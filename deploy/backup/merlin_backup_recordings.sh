#!/usr/bin/env bash
set -euo pipefail

PROD_DIR="${PROD_DIR:-/opt/merlin}"
BACKUP_ROOT="${BACKUP_ROOT:-/var/backups/merlin/recordings}"
RETENTION_DAYS="${RETENTION_DAYS:-14}"
API_CONTAINER="${API_CONTAINER:-merlin-api-1}"
RECORDINGS_DIR="${RECORDINGS_DIR:-/app/storage/recordings}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
HOSTNAME_TAG="$(hostname -s 2>/dev/null || echo merlin-host)"
TARGET_DIR="${BACKUP_ROOT}/${HOSTNAME_TAG}"
TARGET_FILE="${TARGET_DIR}/merlin_recordings_${STAMP}.tgz"
SHA_FILE="${TARGET_FILE}.sha256"

mkdir -p "$TARGET_DIR"
umask 077

cd "$PROD_DIR"
docker compose --env-file .env.prod -f docker-compose.prod.yml ps api >/dev/null

docker exec "$API_CONTAINER" sh -lc "mkdir -p '$RECORDINGS_DIR' && cd '$RECORDINGS_DIR' && tar -czf - ." \
  >"$TARGET_FILE"

sha256sum "$TARGET_FILE" >"$SHA_FILE"

find "$TARGET_DIR" -type f -name 'merlin_recordings_*.tgz' -mtime +"$RETENTION_DAYS" -delete
find "$TARGET_DIR" -type f -name 'merlin_recordings_*.tgz.sha256' -mtime +"$RETENTION_DAYS" -delete

printf 'recordings-backup-ok file=%s\n' "$TARGET_FILE"

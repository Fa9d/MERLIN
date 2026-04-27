#!/usr/bin/env bash
set -euo pipefail

PROD_DIR="${PROD_DIR:-/opt/merlin}"
BACKUP_ROOT="${BACKUP_ROOT:-/var/backups/merlin/postgres}"
RETENTION_DAYS="${RETENTION_DAYS:-14}"
DB_CONTAINER="${DB_CONTAINER:-merlin-db-1}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
HOSTNAME_TAG="$(hostname -s 2>/dev/null || echo merlin-host)"
TARGET_DIR="${BACKUP_ROOT}/${HOSTNAME_TAG}"
TARGET_FILE="${TARGET_DIR}/merlin_postgres_${STAMP}.sql.gz"
SHA_FILE="${TARGET_FILE}.sha256"

mkdir -p "$TARGET_DIR"
umask 077

cd "$PROD_DIR"
docker compose --env-file .env.prod -f docker-compose.prod.yml ps db >/dev/null

docker exec "$DB_CONTAINER" sh -lc 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB"' \
  | gzip -9 >"$TARGET_FILE"

sha256sum "$TARGET_FILE" >"$SHA_FILE"

find "$TARGET_DIR" -type f -name 'merlin_postgres_*.sql.gz' -mtime +"$RETENTION_DAYS" -delete
find "$TARGET_DIR" -type f -name 'merlin_postgres_*.sql.gz.sha256' -mtime +"$RETENTION_DAYS" -delete

printf 'postgres-backup-ok file=%s\n' "$TARGET_FILE"

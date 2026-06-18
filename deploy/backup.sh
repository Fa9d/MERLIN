#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# IVIA / MERLIN — Sauvegarde chiffrée multi-support (Loi 25)
#
# 1. Dump PostgreSQL (base) + archive des audios (volume merlin_recordings)
# 2. Chiffrement AES-256 (gpg, passphrase depuis .env.prod) — JAMAIS en clair hors VPS
# 3. Copie hors-site vers OVH Object Storage région Québec (BHS), S3-compatible
# 4. Rétention locale (7 dernières) ; rétention hors-site = cycle de vie du bucket OVH
#
# Variables requises dans /opt/merlin/.env.prod :
#   POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD   (déjà présents)
#   MERLIN_BACKUP_PASSPHRASE   secret de chiffrement (long, aléatoire)
#   OVH_S3_ENDPOINT            ex. https://s3.bhs.io.cloud.ovh.net
#   OVH_S3_REGION              ex. bhs
#   OVH_S3_BUCKET              ex. merlin-backups
#   AWS_ACCESS_KEY_ID          clé S3 de l'utilisateur Object Storage OVH
#   AWS_SECRET_ACCESS_KEY      secret S3
# Optionnel : MERLIN_BACKUP_LOCAL_DIR (défaut /opt/merlin/backups), MERLIN_BACKUP_LOCAL_KEEP (défaut 7)
#
# Usage : bash deploy/backup.sh   (ou via cron — voir docs/ops-sauvegarde.md)
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

cd /opt/merlin
set -a; # shellcheck disable=SC1091
source .env.prod
set +a

: "${POSTGRES_DB:?manquant}"; : "${POSTGRES_USER:?manquant}"
: "${MERLIN_BACKUP_PASSPHRASE:?manquant — definir dans .env.prod}"
: "${OVH_S3_ENDPOINT:?manquant}"; : "${OVH_S3_BUCKET:?manquant}"
: "${AWS_ACCESS_KEY_ID:?manquant}"; : "${AWS_SECRET_ACCESS_KEY:?manquant}"

LOCAL="${MERLIN_BACKUP_LOCAL_DIR:-/opt/merlin/backups}"
KEEP="${MERLIN_BACKUP_LOCAL_KEEP:-7}"
REGION="${OVH_S3_REGION:-bhs}"
TS="$(date +%Y%m%d_%H%M%S)"
DC="docker compose --env-file .env.prod -f docker-compose.prod.yml"
AWS="aws --endpoint-url ${OVH_S3_ENDPOINT} --region ${REGION}"
mkdir -p "$LOCAL"

log(){ echo "[$(date '+%F %T')] $*"; }

# 1) Dump base (gzip) ────────────────────────────────────────────────────────
log "Dump PostgreSQL…"
$DC exec -T db pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" | gzip > "$LOCAL/db_${TS}.sql.gz"

# 2) Archive des audios ───────────────────────────────────────────────────────
log "Archive des enregistrements…"
$DC exec -T api tar -czf - -C /app/storage/recordings . > "$LOCAL/recordings_${TS}.tar.gz" 2>/dev/null || \
  log "  (volume audios vide ou indisponible — archive ignorée)"

# 3) Chiffrement AES-256 + suppression des clairs ─────────────────────────────
log "Chiffrement…"
for f in "$LOCAL/db_${TS}.sql.gz" "$LOCAL/recordings_${TS}.tar.gz"; do
  [ -s "$f" ] || continue
  gpg --batch --yes --passphrase "$MERLIN_BACKUP_PASSPHRASE" --cipher-algo AES256 -c -o "${f}.gpg" "$f"
  rm -f "$f"
done

# 4) Copie hors-site OVH (Québec) ─────────────────────────────────────────────
log "Envoi hors-site OVH (${OVH_S3_BUCKET})…"
for f in "$LOCAL"/db_${TS}.sql.gz.gpg "$LOCAL"/recordings_${TS}.tar.gz.gpg; do
  [ -s "$f" ] || continue
  base="$(basename "$f")"; sub="${base%%_*}"   # db / recordings
  $AWS s3 cp "$f" "s3://${OVH_S3_BUCKET}/${sub}/${base}"
done

# 5) Rétention locale (les N plus récentes) ───────────────────────────────────
log "Rétention locale (${KEEP})…"
for p in db recordings; do
  ls -1t "$LOCAL"/${p}_*.gpg 2>/dev/null | tail -n +"$((KEEP+1))" | xargs -r rm -f
done

log "Sauvegarde ${TS} terminée."

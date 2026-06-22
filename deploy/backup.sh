#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# IVIA / MERLIN — Sauvegarde chiffrée multi-support (Loi 25)
#
# Comportement DÉGRADABLE (un seul script pour dev ET prod) :
#   • Toujours : dump PostgreSQL + archive des audios dans un dossier local du VPS.
#   • Chiffrement AES-256 UNIQUEMENT si MERLIN_BACKUP_PASSPHRASE est défini.
#   • Envoi hors-site OVH (Québec, BHS) UNIQUEMENT si les variables OVH sont définies.
#   → En dev (sans OVH, sans passphrase) : sauvegarde LOCALE gratuite, 0 frais.
#   → En prod (vars OVH + passphrase) : chiffré + copie hors-site automatique.
#
# Variables (/opt/merlin/.env.prod) :
#   POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD     (déjà présents — requis)
#   MERLIN_BACKUP_PASSPHRASE   (optionnel) secret de chiffrement AES-256
#   OVH_S3_ENDPOINT / OVH_S3_REGION / OVH_S3_BUCKET / AWS_ACCESS_KEY_ID /
#   AWS_SECRET_ACCESS_KEY      (optionnels, en bloc) → active le hors-site
#   MERLIN_BACKUP_LOCAL_DIR (défaut /opt/merlin/backups), MERLIN_BACKUP_LOCAL_KEEP (défaut 7)
#
# Usage : bash deploy/backup.sh   (ou via cron — voir docs/ops-sauvegarde.md)
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

cd /opt/merlin
set -a; # shellcheck disable=SC1091
source .env.prod
set +a

: "${POSTGRES_DB:?manquant}"; : "${POSTGRES_USER:?manquant}"

LOCAL="${MERLIN_BACKUP_LOCAL_DIR:-/opt/merlin/backups}"
KEEP="${MERLIN_BACKUP_LOCAL_KEEP:-7}"
REGION="${OVH_S3_REGION:-bhs}"
TS="$(date +%Y%m%d_%H%M%S)"
DC="docker compose --env-file .env.prod -f docker-compose.prod.yml"
mkdir -p "$LOCAL"

log(){ echo "[$(date '+%F %T')] $*"; }

# Détection des modes (dégradation gracieuse) ─────────────────────────────────
ENCRYPT=0; [ -n "${MERLIN_BACKUP_PASSPHRASE:-}" ] && ENCRYPT=1
OFFSITE=0
if [ -n "${OVH_S3_ENDPOINT:-}" ] && [ -n "${OVH_S3_BUCKET:-}" ] \
   && [ -n "${AWS_ACCESS_KEY_ID:-}" ] && [ -n "${AWS_SECRET_ACCESS_KEY:-}" ]; then
  OFFSITE=1
fi

# 1) Dump base (gzip) ─────────────────────────────────────────────────────────
log "Dump PostgreSQL…"
$DC exec -T db pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" | gzip > "$LOCAL/db_${TS}.sql.gz"

# 2) Archive des audios ───────────────────────────────────────────────────────
log "Archive des enregistrements…"
$DC exec -T api tar -czf - -C /app/storage/recordings . > "$LOCAL/recordings_${TS}.tar.gz" 2>/dev/null || \
  log "  (volume audios vide ou indisponible — archive ignorée)"

# 3) Chiffrement optionnel + collecte des fichiers produits ───────────────────
FILES=()
for f in "$LOCAL/db_${TS}.sql.gz" "$LOCAL/recordings_${TS}.tar.gz"; do
  [ -s "$f" ] || { rm -f "$f"; continue; }
  if [ "$ENCRYPT" = 1 ]; then
    log "Chiffrement AES-256 de $(basename "$f")…"
    gpg --batch --yes --passphrase "$MERLIN_BACKUP_PASSPHRASE" --cipher-algo AES256 -c -o "${f}.gpg" "$f"
    rm -f "$f"; FILES+=("${f}.gpg")
  else
    FILES+=("$f")
  fi
done

# 4) Copie hors-site OVH (si configurée) ──────────────────────────────────────
if [ "$OFFSITE" = 1 ]; then
  AWS="aws --endpoint-url ${OVH_S3_ENDPOINT} --region ${REGION}"
  log "Envoi hors-site OVH (${OVH_S3_BUCKET})…"
  for f in "${FILES[@]}"; do
    base="$(basename "$f")"; sub="${base%%_*}"   # db / recordings
    $AWS s3 cp "$f" "s3://${OVH_S3_BUCKET}/${sub}/${base}"
  done
else
  log "Hors-site OVH non configuré → sauvegarde LOCALE uniquement (mode dev)."
fi
[ "$ENCRYPT" = 1 ] || log "ATTENTION : pas de MERLIN_BACKUP_PASSPHRASE → dump NON chiffré (ok en dev, PAS avec de vrais clients)."

# 5) Rétention locale (les N plus récentes, .gz comme .gpg) ────────────────────
log "Rétention locale (${KEEP})…"
for p in db recordings; do
  ls -1t "$LOCAL"/${p}_*.sql.gz "$LOCAL"/${p}_*.tar.gz "$LOCAL"/${p}_*.gpg 2>/dev/null \
    | tail -n +"$((KEEP+1))" | xargs -r rm -f
done

log "Sauvegarde ${TS} terminée (chiffrement=${ENCRYPT}, hors-site=${OFFSITE})."

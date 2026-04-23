#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="${REPO_DIR:-/opt/merlin}"
COMPOSE_FILE="${COMPOSE_FILE:-$REPO_DIR/docker-compose.prod.yml}"
ENV_FILE="${ENV_FILE:-$REPO_DIR/.env.prod}"
WEBROOT_DIR="${WEBROOT_DIR:-$REPO_DIR/nginx/certbot/www}"
LETSENCRYPT_DIR="${LETSENCRYPT_DIR:-$REPO_DIR/nginx/certs}"

docker run --rm \
  -v "$WEBROOT_DIR:/var/www/certbot" \
  -v "$LETSENCRYPT_DIR:/etc/letsencrypt" \
  certbot/certbot renew --webroot -w /var/www/certbot --quiet

docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" exec -T nginx nginx -s reload

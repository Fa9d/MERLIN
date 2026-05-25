#!/bin/bash
# deploy_frontend_only.sh — remplace le code frontend et rebuild le conteneur
# Usage : bash /home/ubuntu/deploy_frontend_only.sh
set -e

echo "=== DEPLOY FRONTEND ==="
cd /opt/merlin

echo "--- 1. Extraction du tarball ---"
cd /home/ubuntu
rm -rf /home/ubuntu/09_app_ivia_merlin_new
mkdir -p /home/ubuntu/09_app_ivia_merlin_new
tar -xzf /home/ubuntu/merlin_frontend_vps.tgz -C /home/ubuntu/09_app_ivia_merlin_new
echo "Fichiers extraits: $(find /home/ubuntu/09_app_ivia_merlin_new -type f | wc -l)"

echo "--- 2. Backup + remplacement ---"
sudo rm -rf /opt/merlin/09_app_ivia_merlin_prev
sudo mv /opt/merlin/09_app_ivia_merlin /opt/merlin/09_app_ivia_merlin_prev
sudo cp -a /home/ubuntu/09_app_ivia_merlin_new/09_app_ivia_merlin /opt/merlin/
sudo chown -R ubuntu:ubuntu /opt/merlin/09_app_ivia_merlin

echo "--- 3. Build Docker frontend ---"
cd /opt/merlin
docker compose --env-file .env.prod -f docker-compose.prod.yml build --no-cache frontend

echo "--- 4. Restart conteneur frontend ---"
docker compose --env-file .env.prod -f docker-compose.prod.yml up -d --no-deps frontend

echo "--- 5. Health check (attente 20s) ---"
sleep 20
curl -sf https://ivia.quebec/ | head -c 200 || echo "WARN: site pas encore dispo"

echo ""
echo "=== DEPLOY TERMINE ==="
docker compose --env-file .env.prod -f docker-compose.prod.yml ps frontend

echo ""
echo "--- Setup git pour futurs deploys ---"
if [ ! -d /opt/merlin/09_app_ivia_merlin/.git ]; then
  cd /opt/merlin/09_app_ivia_merlin
  git init
  git remote add origin https://github.com/Fa9d/MERLIN.git
  git fetch origin refonte-ivia-site-unifie --depth=1
  git checkout -b refonte-ivia-site-unifie --track origin/refonte-ivia-site-unifie || \
    git reset --hard origin/refonte-ivia-site-unifie
  echo "Git initialisé — futurs deploys : git pull + docker build"
else
  echo "Git déjà configuré"
fi

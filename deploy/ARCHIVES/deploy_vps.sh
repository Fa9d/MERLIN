#!/bin/bash
set -e

echo "=== 1. ETAT ACTUEL ==="
cd /opt/merlin
docker compose --env-file .env.prod -f docker-compose.prod.yml ps
curl -s https://api.ivia.quebec/api/health && echo "" || echo "health check failed"

echo ""
echo "=== 2. EXTRACTION ARCHIVES ==="
cd /home/ubuntu
rm -rf /home/ubuntu/10_backend_merlin_api_new /home/ubuntu/09_app_ivia_merlin_new
mkdir -p /home/ubuntu/10_backend_merlin_api_new /home/ubuntu/09_app_ivia_merlin_new
tar -xzf /home/ubuntu/merlin_backend_vps.tgz -C /home/ubuntu/10_backend_merlin_api_new
tar -xzf /home/ubuntu/merlin_frontend_vps.tgz -C /home/ubuntu/09_app_ivia_merlin_new
echo "Backend OK: $(ls /home/ubuntu/10_backend_merlin_api_new/10_backend_merlin_api/app/models/ | wc -l) fichiers models"
echo "Frontend OK: $(ls /home/ubuntu/09_app_ivia_merlin_new/09_app_ivia_merlin/src | wc -l) dossiers src"

echo ""
echo "=== 3. BACKUP + REMPLACEMENT ==="
sudo rm -rf /opt/merlin/10_backend_merlin_api_prev /opt/merlin/09_app_ivia_merlin_prev
sudo mv /opt/merlin/10_backend_merlin_api /opt/merlin/10_backend_merlin_api_prev
sudo mv /opt/merlin/09_app_ivia_merlin /opt/merlin/09_app_ivia_merlin_prev
sudo cp -a /home/ubuntu/10_backend_merlin_api_new/10_backend_merlin_api /opt/merlin/
sudo cp -a /home/ubuntu/09_app_ivia_merlin_new/09_app_ivia_merlin /opt/merlin/
sudo chown -R ubuntu:ubuntu /opt/merlin/10_backend_merlin_api /opt/merlin/09_app_ivia_merlin
echo "Verification backend - nouveaux modeles:"
ls /opt/merlin/10_backend_merlin_api/app/models/ | grep -E "payment|entitlement"
echo "Verification frontend - composant sondage:"
ls /opt/merlin/09_app_ivia_merlin/src/components/sondage/
echo "Code en place. Pret pour build."

# Déploiement OVH

## Pré-requis

- Serveur OVH Ubuntu 22.04 avec Docker Engine et Docker Compose plugin installés
- DNS pointant vers le serveur pour le domaine API
- Ports ouverts :
  - `80/tcp`
  - `443/tcp`
  - `7881/tcp`
  - plage UDP LiveKit, par défaut `50000-50020/udp`

## Fichiers de déploiement

- `docker-compose.prod.yml`
- `.env.prod`
- `nginx/default.conf`
- `Makefile`

## Préparation

1. Copier l'exemple d'environnement :

```bash
cp .env.prod.example .env.prod
```

2. Renseigner toutes les valeurs sensibles dans `.env.prod` :

- `POSTGRES_PASSWORD`
- `MERLIN_AUTH_SECRET_KEY`
- `LIVEKIT_API_SECRET`
- `ANTHROPIC_API_KEY`
- `ASSEMBLYAI_API_KEY`

3. Créer les répertoires utilisés par Nginx / Certbot si besoin :

```bash
mkdir -p nginx/certbot/www nginx/certs
```

## Lancement

Construire et démarrer la stack :

```bash
make up
```

Appliquer les migrations Alembic :

```bash
make migrate
```

Suivre les logs :

```bash
make logs
```

Arrêter la stack :

```bash
make down
```

## Vérifications

Depuis le serveur :

```bash
docker compose --env-file .env.prod -f docker-compose.prod.yml ps
curl -I http://127.0.0.1/api/health
```

Notes :

- L'API est publiée via Nginx sur `/api`
- LiveKit est publié via Nginx sur `/livekit`
- Les routes backend attendues en production deviennent `https://votre-domaine/api/v1/...`
- Le backend FastAPI parle à PostgreSQL et à LiveKit via le réseau Docker `merlin_network`

## SSL / Let's Encrypt

Le fichier `nginx/default.conf` est prêt pour un challenge ACME via :

- `/.well-known/acme-challenge/`
- volume webroot : `./nginx/certbot/www`

Procédure recommandée :

1. Démarrer la stack en HTTP
2. Émettre le certificat sur l'hôte avec Certbot en mode webroot

Exemple :

```bash
sudo docker run --rm -it \
  -v "/opt/merlin/nginx/certbot/www:/var/www/certbot" \
  -v "/opt/merlin/nginx/certs:/etc/letsencrypt" \
  certbot/certbot certonly --webroot \
  -w /var/www/certbot \
  -d api.ivia.quebec
```

3. Copier ou monter les certificats dans `./nginx/certs`
4. Décommenter le bloc `server` HTTPS dans `nginx/default.conf`
5. Redéployer :

```bash
make up
```

## Renouvellement automatique TLS

Fichiers fournis :

- `deploy/certbot/renew-merlin-certs.sh`
- `deploy/systemd/merlin-certbot-renew.service`
- `deploy/systemd/merlin-certbot-renew.timer`

Installation recommandÃ©e sur le serveur :

```bash
sudo cp deploy/certbot/renew-merlin-certs.sh /usr/local/bin/merlin-certbot-renew.sh
sudo chmod 755 /usr/local/bin/merlin-certbot-renew.sh
sudo cp deploy/systemd/merlin-certbot-renew.service /etc/systemd/system/
sudo cp deploy/systemd/merlin-certbot-renew.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now merlin-certbot-renew.timer
```

Test manuel :

```bash
sudo systemctl start merlin-certbot-renew.service
sudo systemctl status merlin-certbot-renew.service --no-pager
```

## Notes LiveKit

- Le signal HTTP / WebSocket passe par Nginx sur `/livekit`
- Le trafic RTC média nécessite aussi :
  - `7881/tcp`
  - `50000-50020/udp`
- Ces ports sont publiés directement par le service `livekit`

## Commit

Message prévu :

```text
feat(deploy): add docker-compose.prod.yml for OVH deployment with nginx + LiveKit
```

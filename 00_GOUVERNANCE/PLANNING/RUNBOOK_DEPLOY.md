# RUNBOOK DEPLOY — MERLIN / IVIA

**Ticket** : OPS-001
**Version** : 1.0
**Date création** : 7 mai 2026
**Auteur** : David Phaneuf + Perplexity Computer
**Sources** : Journaux de déploiement Vague 7 (matin) + OPS-002/003 (après-midi)

---

## Architecture de référence

```
┌────────────────────────────────────┐         ┌─────────────────────────────────────┐
│   Poste local Windows              │         │   VPS OVH (137.74.42.121)           │
│   C:\MERLIN (repo git canonique)   │ ─scp──> │   /opt/merlin (déploiement live)    │
│   git push → github.com/Fa9d/MERLIN│         │   PAS un repo git                   │
└────────────────────────────────────┘         └─────────────────────────────────────┘
```

⚠️ **Règle d'or** : `/opt/merlin` n'est pas versionné. Toute modif faite directement sur le VPS doit être **récupérée via scp** vers `C:\MERLIN`, commitée, et poussée sur GitHub. Sinon, dérive garantie au prochain redéploiement.

---

## Pré-requis (one-time)

### Sur le poste Windows

- PowerShell 5.1+ (déjà en place)
- Git for Windows
- OpenSSH client (Windows 10+)
- VSCode + Claude Code + Codex + Copilot
- Clé SSH ED25519 dans `C:\Users\PC\.ssh\id_ed25519` autorisée sur le VPS
- (Optionnel) `ssh-agent` lancé en mode admin pour éviter de retaper la passphrase

### Sur le VPS

- Ubuntu 22.04 LTS, hostname `vps-386c3b6f`
- Docker + Docker Compose v2
- nginx en container (`merlin-nginx-1`)
- Certbot accessible via `docker run certbot/certbot`
- Fichier `/opt/merlin/.env.prod` avec toutes les variables de config

---

## Connexion SSH

```powershell
ssh ubuntu@137.74.42.121
```

**Si la passphrase est demandée à chaque fois**, configurer ssh-agent :

```powershell
# PowerShell EN ADMIN
Set-Service ssh-agent -StartupType Automatic
Start-Service ssh-agent
ssh-add $env:USERPROFILE\.ssh\id_ed25519
```

---

## Procédure de déploiement standard

### Phase 0 — Préparation locale (5 min)

```powershell
cd C:\MERLIN

# Vérifier que master est à jour
git status
git pull origin master

# Vérifier que le code à déployer est commité
git log --oneline -5
```

### Phase 1 — Build des tarballs (10 min)

⚠️ **Pièges PowerShell + tar identifiés en Vague 7** :
- Toujours utiliser `Set-Content -Encoding ascii` (pas `utf8` qui ajoute un BOM en PS 5.1)
- Ne pas utiliser de wildcards inline dans `--exclude` ; utiliser un fichier `-X deploy_excludes.txt`
- Éviter les apostrophes françaises dans les commandes

**Créer `deploy_excludes.txt`** (une fois pour toutes) :

```
node_modules
.next
__pycache__
*.pyc
.pytest_cache
.git
*.log
.env
.env.local
```

**Sauvegarder en ASCII** :
```powershell
Set-Content -Path deploy_excludes.txt -Value $contenu -Encoding ascii
```

**Créer les 3 tarballs** :

```powershell
$STAMP = Get-Date -Format "yyyyMMdd_HHmmss"

# Backend
tar.exe -czf "10_backend_merlin_api_$STAMP.tar.gz" -X deploy_excludes.txt 10_backend_merlin_api

# Frontend
tar.exe -czf "09_app_ivia_merlin_$STAMP.tar.gz" -X deploy_excludes.txt 09_app_ivia_merlin

# Prompts AI
tar.exe -czf "11_PROMPTS_$STAMP.tar.gz" 11_PROMPTS

# Vérifier les tailles attendues : ~70 KB / ~360 KB / ~40 KB
Get-ChildItem *.tar.gz
```

### Phase 2 — Transfert SCP (5 min)

```powershell
scp 10_backend_merlin_api_*.tar.gz ubuntu@137.74.42.121:/tmp/
scp 09_app_ivia_merlin_*.tar.gz ubuntu@137.74.42.121:/tmp/
scp 11_PROMPTS_*.tar.gz ubuntu@137.74.42.121:/tmp/
```

⚠️ **Si tu fais Ctrl+C pendant un scp**, vérifier sur le VPS qu'il ne reste pas un fichier partiel énorme dans `/tmp/`. Ajuster avec `rm /tmp/*.partial*` au besoin.

### Phase 3 — Bascule code sur VPS (10 min)

**Connexion** :
```powershell
ssh ubuntu@137.74.42.121
```

**Sur le VPS** :
```bash
cd /opt/merlin
STAMP=$(date +%Y%m%d_%H%M%S)

# Backup AVANT bascule
mv 10_backend_merlin_api 10_backend_merlin_api.OLD_${STAMP}
mv 09_app_ivia_merlin 09_app_ivia_merlin.OLD_${STAMP}

# Extraction nouveaux tarballs
tar -xzf /tmp/10_backend_merlin_api_*.tar.gz
tar -xzf /tmp/09_app_ivia_merlin_*.tar.gz
tar -xzf /tmp/11_PROMPTS_*.tar.gz -C /opt/merlin/  # écrase 11_PROMPTS existant

# Vérifier l'extraction
ls -la 10_backend_merlin_api 09_app_ivia_merlin 11_PROMPTS
```

### Phase 4 — Migrations Alembic (5 min)

⚠️ **Toujours `--env-file .env.prod` AVANT `-f docker-compose.prod.yml`** :

```bash
cd /opt/merlin

# Voir la révision actuelle
docker compose --env-file .env.prod -f docker-compose.prod.yml run --rm api alembic current

# Appliquer les migrations en attente
docker compose --env-file .env.prod -f docker-compose.prod.yml run --rm api alembic upgrade head

# Vérifier la nouvelle tête
docker compose --env-file .env.prod -f docker-compose.prod.yml run --rm api alembic current
```

### Phase 5 — Build images Docker (15 min)

```bash
docker compose --env-file .env.prod -f docker-compose.prod.yml build api frontend
```

⚠️ **Ne pas faire Ctrl+C pendant le build** même si ça paraît long. Sur le hardware actuel, frontend = ~10 min pour `next build`.

### Phase 6 — Restart stack (5 min)

```bash
docker compose --env-file .env.prod -f docker-compose.prod.yml up -d --force-recreate api frontend

# Vérifier l'état
docker ps
docker logs merlin-api-1 --tail 30
docker logs merlin-frontend-1 --tail 20
```

### Phase 7 — Smoke tests (5 min)

```bash
echo "=== Frontend ==="
curl -sI https://ivia.quebec | head -3

echo "=== API auth requise ==="
curl -sI https://api.ivia.quebec/ | head -3

echo "=== DB tête actuelle ==="
docker compose --env-file .env.prod -f docker-compose.prod.yml run --rm api alembic current

echo "=== Containers ==="
docker ps --format 'table {{.Names}}\t{{.Status}}'

echo "=== Status page ==="
curl -sI https://status.ivia.quebec | head -3
```

**Critères de succès** :
- Frontend → 200
- API → 401 (auth) ou 200 (endpoint public)
- DB → tête attendue (revision la plus récente)
- 9 containers `Up` dont api+frontend `healthy`
- Status page → 200 ou 302

### Phase 8 — Journal + commit (10 min)

**Sur Windows** :
```powershell
cd C:\MERLIN

# Créer le journal du déploiement
$STAMP = Get-Date -Format "yyyyMMddHHmm"
# Édite manuellement 00_GOUVERNANCE/JOURNAUX/JOURNAL_DEPLOY_$STAMP.md
# Suivre le template du journal Vague 7 ou OPS-002/003

git add 00_GOUVERNANCE/JOURNAUX/
git commit -m "docs(gouvernance): journal déploiement <description>"
git push origin master
```

---

## Procédure de hotfix sur VPS (modif directe)

⚠️ **Cas dangereux** : modifier des fichiers directement sur `/opt/merlin/` (ex: nginx config, docker-compose). **Ces modifs ne sont PAS dans git** tant qu'elles ne sont pas pullées vers `C:\MERLIN`.

### Étapes obligatoires après hotfix VPS

```powershell
cd C:\MERLIN

# Backup avant écrasement
$STAMP = Get-Date -Format "yyyyMMdd_HHmmss"
foreach ($f in @("docker-compose.prod.yml", "nginx\default.conf")) {
    Copy-Item $f "$f.bak_$STAMP"
}

# Pull les fichiers modifiés depuis le VPS
scp ubuntu@137.74.42.121:/opt/merlin/docker-compose.prod.yml .\docker-compose.prod.yml
scp ubuntu@137.74.42.121:/opt/merlin/nginx/default.conf .\nginx\default.conf
# Ajouter d'autres fichiers selon le cas

# Vérifier le diff
git diff --stat

# Commit + push
git add -A
git commit -m "feat(infra): hotfix déployé en prod le <date> <description>"
git push origin master
```

---

## Procédure d'ajout d'un nouveau sous-domaine + service

(Pattern OPS-002/003 testé avec Dozzle + Uptime Kuma)

### Étape A — DNS chez OVH (5 min)

1. Web Cloud → Domaines → `ivia.quebec` → Zone DNS
2. Ajouter entrée A : `<sous-domaine>` → `137.74.42.121`
3. Vérifier propagation : `dig +short <sous-domaine>.ivia.quebec`

### Étape B — Certificat Let's Encrypt (3 min)

```bash
# Sur le VPS, ajouter d'abord un block HTTP minimal pour le challenge ACME
cat >> /opt/merlin/nginx/default.conf << 'EOF'

server {
    listen 80;
    server_name <sous-domaine>.ivia.quebec;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 404;
    }
}
EOF

docker exec merlin-nginx-1 nginx -s reload

# Issuer le certificat
docker run --rm \
  -v /opt/merlin/nginx/certs:/etc/letsencrypt \
  -v /opt/merlin/nginx/certbot/www:/var/www/certbot \
  certbot/certbot certonly --webroot -w /var/www/certbot \
  -d <sous-domaine>.ivia.quebec \
  --email bonjour@ivia.quebec \
  --agree-tos --no-eff-email --non-interactive
```

### Étape C — Ajouter le service Docker

Éditer `docker-compose.prod.yml` (avant la section `volumes:`) :

```yaml
  <nom-service>:
    image: <image:tag>
    container_name: merlin-<nom-service>
    restart: unless-stopped
    networks:
      - merlin_network
    # autres options selon l'outil
```

Lancer :
```bash
docker compose --env-file .env.prod -f docker-compose.prod.yml up -d <nom-service>
docker logs merlin-<nom-service> --tail 20
```

### Étape D — Server block HTTPS dans nginx

Ajouter à la fin de `default.conf` :

```nginx
server {
    listen 443 ssl;
    http2 on;
    server_name <sous-domaine>.ivia.quebec;

    ssl_certificate /etc/letsencrypt/live/<sous-domaine>.ivia.quebec/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/<sous-domaine>.ivia.quebec/privkey.pem;

    # Si auth basic souhaitée :
    # auth_basic "<libellé>";
    # auth_basic_user_file /etc/nginx/.htpasswd_<service>;

    location / {
        set $upstream http://<nom-service>:<port>;
        proxy_pass $upstream;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}
```

Recréer nginx si nouveau volume (ex: htpasswd) :
```bash
docker compose --env-file .env.prod -f docker-compose.prod.yml up -d --force-recreate nginx
```

Sinon simple reload :
```bash
docker exec merlin-nginx-1 nginx -s reload
```

### Étape E — Auth basic (si privé)

```bash
PASS=$(openssl rand -base64 16)
echo "Mot de passe : $PASS"
echo "Username : ivia"
HASH=$(openssl passwd -apr1 "$PASS")
echo "ivia:$HASH" > /opt/merlin/nginx/.htpasswd_<service>
```

⚠️ **Ne JAMAIS commiter le fichier `.htpasswd_*`**. Ajouter au `.gitignore` :
```
nginx/.htpasswd_*
```

### Étape F — Sync vers Windows + commit

Voir « Procédure de hotfix sur VPS » ci-dessus.

---

## Bugs connus + solutions

| Bug | Symptôme | Cause | Solution |
|---|---|---|---|
| **PromptNotFoundError** | API restart loop | `prompt_loader.py` utilise `Path(__file__).parents[3] / "11_PROMPTS"` qui résout en `/` dans le container | Volume mount `./11_PROMPTS:/11_PROMPTS:ro` dans compose → fix dans **BACK-010** |
| **tar BOM error** | `tar: Unrecognized --exclude format` | PowerShell 5.1 + `Set-Content -Encoding utf8` ajoute un BOM | `Set-Content -Encoding ascii` |
| **Variables shell SSH** | `STAMP=` substitué localement | PowerShell expand les `$VAR` avant SSH | Quoter avec apostrophes simples ou définir la var côté VPS |
| **`docker compose up` plante** | Containers ne trouvent pas vars | Oubli `--env-file .env.prod` | TOUJOURS `--env-file .env.prod -f docker-compose.prod.yml` |
| **Apostrophes françaises** | Parsing bash échoue | Shell ne reconnaît pas `'` typographique | Éviter dans les commandes, utiliser apostrophe ASCII |
| **Permission denied sur cp** | Backup VPS impossible | Fichier appartient à root | `sudo cp` pour ce backup uniquement |
| **nano ne sauve pas** | Modif perdue | Confusion clavier ou Ctrl+O non confirmé | Préférer script Python pour modifs reproductibles |
| **Dozzle crash loop** | `users.yaml not found` | `DOZZLE_AUTH_PROVIDER: simple` exige fichier YAML | Pas d'auth Dozzle, auth basic au niveau nginx |
| **VPS pas un repo git** | `git status` échoue dans `/opt/merlin` | C'est un déploiement, pas un working tree | Pull modifs via scp vers `C:\MERLIN` |

---

## Backups recommandés

### Avant chaque déploiement

- `docker-compose.prod.yml.bak_<stamp>`
- `nginx/default.conf.bak_<stamp>`
- Dossier `<service>.OLD_<stamp>` pour le code

### Conservation

- Garder les 3 derniers backups
- Supprimer les plus anciens : `find /opt/merlin -name "*.bak_*" -mtime +14 -delete`

---

## Renouvellement Let's Encrypt

⚠️ **À configurer en cron** (TODO OPS-014) :

```bash
# Test manuel
docker run --rm \
  -v /opt/merlin/nginx/certs:/etc/letsencrypt \
  -v /opt/merlin/nginx/certbot/www:/var/www/certbot \
  certbot/certbot renew --dry-run

# Cron quotidien (à ajouter dans crontab -e)
0 3 * * * docker run --rm -v /opt/merlin/nginx/certs:/etc/letsencrypt -v /opt/merlin/nginx/certbot/www:/var/www/certbot certbot/certbot renew --quiet && docker exec merlin-nginx-1 nginx -s reload
```

---

## Estimations standards (calibrées Vague 7 + 8.1)

| Type d'opération | Estimé brut | Coef | Réaliste |
|---|---:|---:|---:|
| Déploiement code (backend + frontend) | 1 h 45 | × 1,5 | 2 h 30 |
| Ajout sous-domaine + service self-hosted | 40 min | × 1,2 | 50 min |
| Hotfix nginx + sync repo | 20 min | × 1,2 | 25 min |
| Migration Alembic seule | 5 min | × 1 | 5 min |
| Renouvellement certificats | 5 min | × 1 | 5 min |

---

## Tickets liés

- **OPS-001** ce runbook (P1, terminé)
- **OPS-014** (à créer, P2) — automatiser renouvellement Let's Encrypt en cron
- **OPS-013** (P3) — sync auto VPS → repo
- **BACK-010** (P2) — refactor `prompt_loader.py` avec env var `PROMPTS_DIR`

---

## Devise IVIA

*Au sein de l'être — En actes.*

---

*Runbook v1.0 — généré 7 mai 2026, 15h25 EDT*
*À enrichir au fil des déploiements futurs.*

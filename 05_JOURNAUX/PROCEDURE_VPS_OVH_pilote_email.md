# Procédure VPS OVH — activation mode pilote email

**Pour qui** : David
**Quand** : maintenant (après commit `2a8b898` et `f5f043a`)
**Combien de temps** : 5 minutes

---

## Préalable

Tu dois savoir 3 choses sur ton VPS OVH (137.74.42.121) :
1. Ton login SSH (probablement `root` ou `ubuntu` ou `merlin`)
2. Le chemin du dossier où vit `.env.prod` (probablement `/opt/merlin/` ou `/home/<user>/MERLIN/`)
3. Comment tu déploies habituellement (via `make` selon `docs/deploy-ovh.md`)

Si tu n'es pas sûr, brief Copilot avec ce fichier — il connaît ton historique de déploiement.

---

## Étape 1 — SSH sur le VPS

Dans PowerShell (ou Terminal Mac) :

```bash
ssh root@137.74.42.121
```

(remplacer `root` par ton vrai user SSH si différent)

---

## Étape 2 — Trouver le dossier du projet

```bash
# Cherche où vit .env.prod
sudo find / -name ".env.prod" -not -path "*/proc/*" 2>/dev/null
```

Probable réponse : `/opt/merlin/.env.prod` ou similaire. Note le chemin du dossier parent — appelons-le `$MERLIN_DIR`.

```bash
cd /opt/merlin   # adapte au vrai chemin
ls -la .env.prod
```

---

## Étape 3 — Sauvegarder l'env actuel

```bash
sudo cp .env.prod .env.prod.backup-$(date +%Y%m%d-%H%M%S)
```

---

## Étape 4 — Ajouter les variables pilote

Ouvre le fichier en édition :

```bash
sudo nano .env.prod
```

Ajoute ce bloc à la fin du fichier (copier-coller entier) :

```env

# ──────────────────────────────────────────────────────────────────────
# MODE PILOTE — ajouté 9 mai 2026 (commit 2a8b898)
# Override emails vers Gmail le temps du pilote P1
# ──────────────────────────────────────────────────────────────────────
MERLIN_PILOT_EMAIL_OVERRIDE=1
MERLIN_PILOT_CLIENT_PRACTITIONER_EMAIL=davidphaneuf@gmail.com
MERLIN_PILOT_ADMIN_EMAIL=lagent009@gmail.com
```

Sauvegarde et quitte nano : `Ctrl+O`, `Entrée`, `Ctrl+X`.

---

## Étape 5 — Pull le dernier code (qui contient le module override)

```bash
cd /opt/merlin   # ton chemin
sudo git pull origin master
```

Tu devrais voir des nouveaux commits dont `2a8b898` et `f5f043a`.

---

## Étape 6 — Redémarrer le backend pour charger les nouvelles variables

Selon `docs/deploy-ovh.md`, tu utilises Docker Compose :

```bash
sudo make down
sudo make up
```

Ou directement :

```bash
sudo docker compose --env-file .env.prod -f docker-compose.prod.yml up -d --force-recreate api
```

---

## Étape 7 — Vérifier que ça marche

```bash
# Le backend répond toujours
curl -s https://api.ivia.quebec/api/health
# Doit retourner: {"status":"ok",...}

# Les variables pilote sont actives (logs)
sudo docker compose -f docker-compose.prod.yml logs api --tail=50 | grep -i "pilot\|override"
```

Test fonctionnel : faire une vraie inscription sur `https://ivia.quebec/demarche` et vérifier que le mail de confirmation arrive sur **davidphaneuf@gmail.com** (pas sur l'email saisi dans le formulaire).

---

## En cas de problème

**Le backend ne démarre plus** :
```bash
sudo docker compose -f docker-compose.prod.yml logs api --tail=100
```

**Restaurer l'ancien env** :
```bash
sudo cp .env.prod.backup-YYYYMMDD-HHMMSS .env.prod
sudo make up
```

**Désactiver le mode pilote** (en P2 quand vrais clients) :
Édite `.env.prod` et change `MERLIN_PILOT_EMAIL_OVERRIDE=0`. Redémarre.

---

## Si tu veux que Copilot fasse tout ça

Brief Copilot dans VS Code :

```
@workspace lis 05_JOURNAUX/PROCEDURE_VPS_OVH_pilote_email.md
et execute les etapes 1 a 7 sur le VPS OVH 137.74.42.121.
Tu connais mon SSH key et le chemin du projet sur le VPS.
Confirme apres chaque etape.
```

---

*Au sein de l'être — En actes.*

# MERLIN - Procedure redeploiement standard VPS backend V1

Date: 2026-04-26
Statut: actif
Objet: figer une procedure canonique, courte et verifiable pour redeployer le backend MERLIN sur le VPS prod sans improvisation

---

## 1) Portee

Cette procedure couvre:

- un redeploiement backend manuel standard vers le VPS;
- un changement de code backend dans `10_backend_merlin_api`;
- un cycle simple `archive -> copie -> remplacement -> build -> migration -> restart -> verification`.

Cette procedure ne couvre pas:

- une remise en etat lourde du runtime Docker;
- un changement TLS ou nginx;
- un redeploiement frontend;
- une migration destructive non revue;
- une ouverture large de prod sans verification finale.

Regle:

`si le runtime VPS est douteux, executer d'abord la checklist de stabilisation J1`

---

## 2) Preconditions

Necessaire:

- acces SSH au VPS via `ubuntu` + cle SSH;
- repertoire cible `/opt/merlin`;
- backend local a jour dans `C:\MERLIN\10_backend_merlin_api`;
- archive de deploiement legere sans `.venv`, caches ni bases locales;
- connaissance explicite du changement deploye;
- verification que la migration Alembic eventuelle existe deja en local.

Documents a avoir sous la main:

- [MERLIN_GOUV_CHECKLIST_STABILISATION_VPS_J1_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_CHECKLIST_STABILISATION_VPS_J1_V1.md)
- [MERLIN_GOUV_LOG_INCIDENT_VPS_RECUPERATION_REDEPLOIEMENT_BACKEND_2026-04-24_v1.0.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_LOG_INCIDENT_VPS_RECUPERATION_REDEPLOIEMENT_BACKEND_2026-04-24_v1.0.md)
- [MERLIN_GOUV_CHECKLIST_RECETTE_PROD_E2E_J8_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_CHECKLIST_RECETTE_PROD_E2E_J8_V1.md)

---

## 3) Regles d'execution

- executer une commande par ligne;
- ne pas coller le prompt shell dans les commandes;
- ne pas toucher `.env.prod` pour un redeploiement code-only;
- ne pas supprimer un repertoire de prod sans avoir un backup immediatement exploitable;
- verifier l'etat du runtime avant le build si un doute existe;
- verifier le code charge dans le conteneur avant tout test fonctionnel important.

Regle de stop:

`si build, migration ou restart echoue, ne pas continuer les tests comme si le redeploiement etait valide`

---

## 4) Sequence canonique

## Etape A - Preflight local Windows

Depuis PowerShell local:

```powershell
cd C:\MERLIN
```

```powershell
tar --exclude='10_backend_merlin_api/.venv' --exclude='10_backend_merlin_api/__pycache__' --exclude='10_backend_merlin_api/.pytest_cache' --exclude='10_backend_merlin_api/.mypy_cache' --exclude='10_backend_merlin_api/.ruff_cache' --exclude='10_backend_merlin_api/htmlcov' --exclude='10_backend_merlin_api/*.db' -czf C:\MERLIN\merlin_backend_vps.tgz 10_backend_merlin_api
```

```powershell
scp -i C:\Users\PC\.ssh\id_ed25519 C:\MERLIN\merlin_backend_vps.tgz ubuntu@137.74.42.121:/home/ubuntu/
```

```powershell
ssh -i C:\Users\PC\.ssh\id_ed25519 ubuntu@137.74.42.121
```

Attendu:

- l'archive est copiee sur le VPS;
- aucune dependance locale parasite n'est embarquee.

## Etape B - Preflight VPS

Depuis la session SSH:

```bash
cd /opt/merlin
```

```bash
docker compose --env-file .env.prod -f docker-compose.prod.yml ps
```

```bash
curl -s https://api.ivia.quebec/api/health
```

Si le runtime semble douteux:

```bash
sudo systemctl status containerd --no-pager
```

```bash
sudo systemctl status docker --no-pager
```

```bash
docker info | grep -E 'Server Version|Runtimes|Default Runtime'
```

Attendu:

- la stack tourne avant intervention;
- `api` repond deja `ok`;
- pas de symptome runtime evident.

## Etape C - Preparation du nouveau code

```bash
cd /home/ubuntu
```

```bash
rm -rf /home/ubuntu/10_backend_merlin_api_new
```

```bash
mkdir -p /home/ubuntu/10_backend_merlin_api_new
```

```bash
tar -xzf /home/ubuntu/merlin_backend_vps.tgz -C /home/ubuntu/10_backend_merlin_api_new
```

```bash
ls -la /home/ubuntu/10_backend_merlin_api_new/10_backend_merlin_api
```

Attendu:

- le dossier extrait existe;
- l'arborescence attendue est presente avant toute copie vers `/opt/merlin`.

## Etape D - Backup et remplacement du code deploye

```bash
sudo rm -rf /opt/merlin/10_backend_merlin_api_prev
```

```bash
sudo mv /opt/merlin/10_backend_merlin_api /opt/merlin/10_backend_merlin_api_prev
```

```bash
sudo cp -a /home/ubuntu/10_backend_merlin_api_new/10_backend_merlin_api /opt/merlin/
```

```bash
sudo chown -R ubuntu:ubuntu /opt/merlin/10_backend_merlin_api
```

```bash
ls -la /opt/merlin/10_backend_merlin_api
```

Attendu:

- le code precedent reste disponible dans `/opt/merlin/10_backend_merlin_api_prev`;
- le nouveau code est en place dans `/opt/merlin/10_backend_merlin_api`.

## Etape E - Build, migration, restart

```bash
cd /opt/merlin
```

```bash
docker compose --env-file .env.prod -f docker-compose.prod.yml build api
```

```bash
docker compose --env-file .env.prod -f docker-compose.prod.yml run --rm api alembic upgrade head
```

```bash
docker compose --env-file .env.prod -f docker-compose.prod.yml up -d --no-deps api
```

```bash
docker compose --env-file .env.prod -f docker-compose.prod.yml ps
```

Attendu:

- l'image `merlin-api` rebuild proprement;
- la migration passe sans erreur;
- le conteneur `merlin-api-1` revient en `Up`.

## Etape F - Verification minimale post-redeploiement

```bash
curl -s https://api.ivia.quebec/api/health
```

```bash
curl -s http://127.0.0.1/api/health
```

```bash
docker logs --tail 80 merlin-api-1
```

```bash
docker exec merlin-api-1 sh -lc "python -c \"import app.main; print('app-main-ok')\""
```

Verification du changement deploye:

- verifier explicitement au moins un symbole, une route ou un comportement lie au changement du jour;
- si le changement ajoute un objet persistant, verifier aussi la revision schema;
- si le changement ajoute une route, verifier sa presence via `openapi.json` ou via l'appel cible.

Exemple de verification schema:

```bash
docker compose --env-file .env.prod -f docker-compose.prod.yml run --rm api alembic current
```

Exemple de verification OpenAPI:

```bash
curl -s https://api.ivia.quebec/openapi.json | grep derived-documents
```

Attendu:

- `health` repond `ok`;
- pas de boucle de crash evidente;
- le changement attendu est bien charge dans le conteneur ou l'API.

---

## 5) Verification metier minimale

Apres un redeploiement purement backend, ne pas se contenter du `healthcheck`.

Verifier au moins:

- une route publique critique si elle est impactee;
- une route authentifiee critique si elle est impactee;
- une verification negative si le changement porte sur les droits ou la diffusion;
- une route de recette `J8` si le changement touche le workflow coeur.

Reference:

- [MERLIN_GOUV_CHECKLIST_RECETTE_PROD_E2E_J8_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_CHECKLIST_RECETTE_PROD_E2E_J8_V1.md)

---

## 6) Rollback minimal

Si le redeploiement echoue apres remplacement du code:

```bash
cd /opt/merlin
```

```bash
sudo rm -rf /opt/merlin/10_backend_merlin_api
```

```bash
sudo mv /opt/merlin/10_backend_merlin_api_prev /opt/merlin/10_backend_merlin_api
```

```bash
sudo chown -R ubuntu:ubuntu /opt/merlin/10_backend_merlin_api
```

```bash
docker compose --env-file .env.prod -f docker-compose.prod.yml build api
```

```bash
docker compose --env-file .env.prod -f docker-compose.prod.yml up -d --no-deps api
```

```bash
curl -s https://api.ivia.quebec/api/health
```

Regle:

- si une migration destructive a ete lancee, ce rollback simple ne suffit plus;
- dans ce cas, arreter et traiter l'incident comme un incident base/schema.

---

## 7) Definition de succes

Le redeploiement est considere termine si:

- la stack reste `Up`;
- `https://api.ivia.quebec/api/health` repond `ok`;
- la migration attendue est appliquee si necessaire;
- le changement deploye est explicitement verifie;
- aucun symptome runtime Docker/containerd nouveau n'apparait;
- au moins une verification metier utile a ete executee.

---

## 8) Ce qu'il ne faut plus refaire

- deployer un backend local non archive proprement;
- pousser du code sans verifier la migration associee;
- tester une fonctionnalite sans verifier que le nouveau code est charge;
- ignorer un symptome runtime en supposant que `docker` "va se replacer";
- melanger redeploiement backend, TLS, nettoyage de test et debug de comptes dans la meme sequence sans checkpoints.

---

## 9) References

- [MERLIN_GOUV_CHECKLIST_STABILISATION_VPS_J1_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_CHECKLIST_STABILISATION_VPS_J1_V1.md)
- [MERLIN_GOUV_LOG_INCIDENT_VPS_RECUPERATION_REDEPLOIEMENT_BACKEND_2026-04-24_v1.0.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_LOG_INCIDENT_VPS_RECUPERATION_REDEPLOIEMENT_BACKEND_2026-04-24_v1.0.md)
- [MERLIN_GOUV_CHECKLIST_RECETTE_PROD_E2E_J8_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_CHECKLIST_RECETTE_PROD_E2E_J8_V1.md)

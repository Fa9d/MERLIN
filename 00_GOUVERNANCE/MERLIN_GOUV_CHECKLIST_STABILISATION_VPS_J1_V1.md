# MERLIN - Checklist stabilisation VPS J1 V1

Date: 2026-04-26
Statut: actif
Objet: executer une verification et une remise en etat minimales du VPS MERLIN apres l'incident Docker / containerd / paquets systeme

---

## 1) But

Cette checklist sert a verifier quatre choses:

- que le systeme paquets n'est plus casse;
- que le runtime Docker est propre;
- que la stack MERLIN redemarre normalement;
- qu'un redeploiement backend simple reste possible sans improvisation.

---

## 2) Regle d'execution

Travailler dans cet ordre:

1. diagnostic
2. reparation paquets
3. verification Docker
4. verification MERLIN
5. mini test de redeploiement

Si une etape echoue:

- ne pas enchainer a l'aveugle;
- capturer la sortie exacte;
- corriger avant de passer a l'etape suivante.

---

## 3) Commandes J1

## Etape A - Diagnostic systeme

Depuis la session SSH:

```bash
hostname
whoami
pwd
date
uname -a
```

```bash
sudo systemctl status containerd --no-pager
sudo systemctl status docker --no-pager
docker info >/tmp/merlin_docker_info.txt && tail -n 40 /tmp/merlin_docker_info.txt
docker ps -a
```

```bash
sudo dpkg --audit
sudo apt-mark showhold
dpkg -l | grep -E 'containerd|docker|runc|dnsmasq|ubuntu-fan'
```

```bash
ls -l /etc/shadow
getent group nogroup
getent passwd dnsmasq || true
```

Attendu:

- `containerd` et `docker` actifs;
- `docker info` sans erreur;
- `dpkg --audit` vide ou tres limite;
- `/etc/shadow` present;
- `nogroup` resolu.

---

## Etape B - Reparation paquets

```bash
sudo dpkg --configure -a
sudo apt-get -f install -y
sudo dpkg --audit
```

Si `dnsmasq-base` ou `ubuntu-fan` restent bloques, verifier avant toute autre action:

```bash
sudo journalctl -u docker -n 50 --no-pager
sudo journalctl -u containerd -n 50 --no-pager
```

Puis relancer:

```bash
sudo dpkg --configure -a
sudo apt-get -f install -y
```

Attendu:

- plus d'etat `half-configured`;
- plus de dette paquets bloquante.

---

## Etape C - Verification runtime Docker

```bash
sudo systemctl restart containerd
sudo systemctl restart docker
sleep 3
sudo systemctl status containerd --no-pager
sudo systemctl status docker --no-pager
docker info | grep -E 'Server Version|Runtimes|Default Runtime'
```

Attendu:

- services actifs;
- runtime par defaut visible;
- plus d'erreur `containerd-shim-runc-v2`.

---

## Etape D - Verification stack MERLIN

```bash
cd /opt/merlin
docker compose --env-file .env.prod -f docker-compose.prod.yml ps
curl -s https://api.ivia.quebec/api/health
curl -s http://127.0.0.1/api/health
```

```bash
docker logs --tail 80 merlin-api-1
docker logs --tail 80 merlin-nginx-1
docker logs --tail 80 merlin-db-1
```

Attendu:

- services principaux presents;
- health `ok`;
- pas de boucle de crash evidente.

---

## Etape E - Mini test de redeploiement backend

Objectif:

- verifier qu'un cycle simple `build -> up -d api` fonctionne encore.

```bash
cd /opt/merlin
docker compose --env-file .env.prod -f docker-compose.prod.yml build api
docker compose --env-file .env.prod -f docker-compose.prod.yml up -d --no-deps api
docker compose --env-file .env.prod -f docker-compose.prod.yml ps
curl -s https://api.ivia.quebec/api/health
```

Verification code charge:

```bash
docker exec merlin-api-1 sh -lc "grep -n '_ensure_terminal_punctuation' /app/app/api/routes/sessions.py"
docker exec merlin-api-1 sh -lc "grep -n '_build_generated_document_title' /app/app/api/routes/sessions.py"
docker exec merlin-api-1 sh -lc "grep -n 'Synthese de seance' /app/app/api/routes/sessions.py"
```

Attendu:

- le conteneur `merlin-api-1` redemarre;
- l'API repond encore `ok`;
- les correctifs backend attendus sont bien charges.

---

## 4) Definition de succes J1

J1 est considere termine si:

- `dpkg --audit` ne remonte plus de dette critique;
- `docker` et `containerd` redemarrent proprement;
- `merlin-api-1` peut etre rebuild puis relance;
- `https://api.ivia.quebec/api/health` repond `ok`;
- la verification du code charge dans le conteneur est concluante.

---

## 5) Si ca casse encore

Ne pas repartir directement sur des reinstallations larges.

Capturer d'abord:

```bash
sudo dpkg --audit
sudo journalctl -u docker -n 120 --no-pager
sudo journalctl -u containerd -n 120 --no-pager
docker info
```

Puis traiter la cause precise.

Le but de J1 est la stabilisation, pas un second chantier infra improvisé.

---

## 6) References

- [MERLIN_GOUV_PROCEDURE_REDEPLOIEMENT_STANDARD_VPS_BACKEND_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_PROCEDURE_REDEPLOIEMENT_STANDARD_VPS_BACKEND_V1.md)
- [MERLIN_GOUV_LOG_INCIDENT_VPS_RECUPERATION_REDEPLOIEMENT_BACKEND_2026-04-24_v1.0.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_LOG_INCIDENT_VPS_RECUPERATION_REDEPLOIEMENT_BACKEND_2026-04-24_v1.0.md)

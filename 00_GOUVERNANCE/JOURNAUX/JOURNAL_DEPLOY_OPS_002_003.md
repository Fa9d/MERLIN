# Journal de déploiement — OPS-002 + OPS-003

**Date** : Jeudi 7 mai 2026
**Période** : 14h27 → 15h15 EDT (≈ 48 min)
**Statut** : ✅ DÉPLOYÉ EN PRODUCTION
**Vague** : 8.1 (extension post-Vague 8)

---

## Objectif

Déployer 2 outils d'observabilité self-hosted :
- **OPS-002 — Dozzle** : UI web pour les logs Docker
- **OPS-003 — Uptime Kuma** : monitoring uptime + status page publique

Sous-domaines dédiés avec TLS Let's Encrypt + auth basic sur les outils internes.

---

## Livrables

### Services en ligne

| Service | URL | Auth | État |
|---|---|---|---|
| Status page publique | https://status.ivia.quebec | Aucune (publique) | ✅ |
| Status page (admin Uptime Kuma) | https://status.ivia.quebec | Compte créé | ✅ |
| Logs Docker (Dozzle) | https://logs.ivia.quebec | Auth basic (`ivia` + mdp généré) | ✅ |

### Monitors Uptime Kuma configurés (5)

1. **IVIA Frontend** — https://ivia.quebec
2. **MERLIN API** — https://api.ivia.quebec/
3. **Logs Dozzle** — https://logs.ivia.quebec
4. **Postgres DB (interne)** — TCP db:5432
5. **Redis (interne)** — TCP redis:6379

Status page publique avec 2 groupes : Services publics + Infrastructure interne.

---

## Modifications versionnées (à committer)

| Fichier | Type | Lignes |
|---|---|---:|
| `docker-compose.prod.yml` | Modifié | +21 |
| `nginx/default.conf` | Modifié | +65 |
| `.gitignore` | Modifié | +2 |

**Total** : ~88 lignes modifiées.

---

## Modifications NON versionnées (sur VPS uniquement)

- `/opt/merlin/nginx/.htpasswd_dozzle` — credentials auth basic Dozzle (volontairement gitignored)
- Certificats Let's Encrypt :
  - `/etc/letsencrypt/live/status.ivia.quebec/` (expire 5 août 2026)
  - `/etc/letsencrypt/live/logs.ivia.quebec/` (expire 5 août 2026)
- Volume Docker `merlin_uptime_data` (données Uptime Kuma)
- Backups locaux VPS :
  - `/opt/merlin/docker-compose.prod.yml.bak_20260507_183839`
  - `/opt/merlin/nginx/default.conf.bak_20260507_183051`

---

## Étapes exécutées

### Phase 1 — DNS (5 min)

1. Ajout 2 entrées A chez OVH :
   - `status.ivia.quebec` → 137.74.42.121
   - `logs.ivia.quebec` → 137.74.42.121
2. Propagation : **instantanée** (vérification `dig`)

### Phase 2 — Certificats Let's Encrypt (3 min)

1. Backup `default.conf` côté VPS
2. Issue certif `status.ivia.quebec` via certbot/webroot ✅
3. Ajout server block HTTP-only pour ACME challenge `logs.ivia.quebec`
4. Reload nginx
5. Issue certif `logs.ivia.quebec` ✅

### Phase 3 — Containers Docker (5 min)

1. Backup `docker-compose.prod.yml`
2. Patch awk : insertion services `dozzle` + `uptime-kuma` avant section `volumes:`
3. Validation `docker compose config --services` → 9 services reconnus
4. `docker compose up -d dozzle uptime-kuma`
5. **Bug Dozzle** : `DOZZLE_AUTH_PROVIDER: simple` exigeait un fichier `users.yaml` absent → crash loop

### Phase 4 — Fix Dozzle (3 min)

**Cause** : ma config initiale ajoutait une auth Dozzle native qui requiert un fichier YAML utilisateurs absent.
**Fix** : suppression de `DOZZLE_AUTH_PROVIDER: simple` via script Python (sed bloqué par permissions).
**Décision** : auth déplacée au niveau nginx (auth basic standard).

### Phase 5 — Auth basic Dozzle (2 min)

1. Génération mot de passe via `openssl rand -base64 16`
2. Création `/opt/merlin/nginx/.htpasswd_dozzle` avec hash apr1
3. Ajout volume mount dans nginx via Python script

### Phase 6 — Configuration nginx finale (5 min)

1. Ajout 2 server blocks HTTPS (status.ivia.quebec + logs.ivia.quebec) via Python
2. `--force-recreate nginx` pour appliquer le nouveau volume
3. Validation logs nginx : 4 workers démarrés, aucune erreur

### Phase 7 — Smoke tests (1 min)

| Test | Résultat |
|---|---|
| `https://status.ivia.quebec` | 302 (redirect setup Uptime Kuma) ✅ |
| `https://logs.ivia.quebec` sans auth | 401 ✅ |
| `https://logs.ivia.quebec` avec auth | 405 sur HEAD (Dozzle accepte que GET) ✅ |
| `https://ivia.quebec` | 200 ✅ |
| `https://api.ivia.quebec/health` | 404 (endpoint inexistant, hors scope) |

### Phase 8 — Configuration Uptime Kuma (15 min)

1. Compte admin créé via `https://status.ivia.quebec`
2. 5 monitors créés (3 HTTPS + 2 TCP)
3. Status page créée avec slug `/status/ivia`
4. 2 groupes : Services publics / Infrastructure interne
5. Monitors ajoutés à la page

### Phase 9 — Synchronisation Windows ↔ VPS (3 min)

**Découverte** : `/opt/merlin/` sur le VPS **n'est pas un repo git**.
**Action** : pull des fichiers modifiés via `scp` depuis le VPS vers `C:\MERLIN\` (repo git canonique).
**Résultat** : `git diff --stat` confirme +86 lignes sur 2 fichiers.

---

## Bugs rencontrés et solutions

### Bug 1 — `cp` permission denied sur `docker-compose.prod.yml`

**Cause** : un backup précédent appartenait à `root` (créé via `sudo` lors d'une opération antérieure), bloquant le nouveau backup au même chemin.
**Fix** : passage par `sudo cp` pour le backup uniquement.

### Bug 2 — Dozzle crash loop

**Cause** : `DOZZLE_AUTH_PROVIDER: simple` requiert un fichier `users.yaml` qui n'existait pas.
**Fix** : retrait de la variable d'env, déplacement de l'auth au niveau nginx (méthode plus standard).

### Bug 3 — `nano` ne sauvegarde pas

**Cause** : probable confusion clavier ou édition non confirmée.
**Fix** : remplacement de l'édition manuelle par script Python (méthode reproductible).

### Bug 4 — VPS pas un repo git

**Cause critique** : `/opt/merlin/` est une copie déployée, pas un working tree git.
**Fix** : pull des fichiers modifiés via scp vers `C:\MERLIN\` pour commit propre.
**Leçon** : à documenter dans **OPS-001 (runbook deploy)** — ne jamais oublier de syncer VPS → repo après hotfix.

---

## Patterns confirmés / acquis

- **Python > sed** sur le VPS quand permissions complexes
- **Auth basic nginx > auth applicative** pour outils self-hosted simples
- **OVH DNS propagation** : quasi instantanée (constaté plusieurs fois aujourd'hui)
- **Certbot webroot** fonctionne tant qu'au moins un server block répond sur `/.well-known/acme-challenge/` pour le hostname concerné
- **Volume mount d'un fichier individuel** : `./fichier:/dest/fichier:ro` (pas un dossier)

---

## Tickets fermés par cette livraison

- ✅ **OPS-002** — Dozzle UI logs Docker
- ✅ **OPS-003** — Uptime Kuma + status.ivia.quebec

---

## Tickets backlog créés

### OPS-001 (P1 maintenant CRITIQUE) — Runbook deploy

À enrichir d'urgence avec :
- Procédure complète Windows → VPS (déploiement)
- Procédure VPS → Windows (récupération hotfix, comme aujourd'hui)
- Pattern Let's Encrypt webroot pour nouveau sous-domaine
- Pattern auth basic nginx pour nouvel outil interne

### OPS-012 (nouveau, P2) — Centraliser les credentials

Stockage propre des credentials générés (Dozzle, futurs outils Infisical, etc.) dans un fichier sécurisé hors-repo.

### OPS-013 (nouveau, P3) — Sync automatique VPS → repo

Script ou hook pour éviter la dérive entre `/opt/merlin/` et `C:\MERLIN\`. Voir **OPS-001 d'abord**.

---

## Bilan estimé / réel

| Métrique | Valeur |
|---|---:|
| **Estimé initial (combiné OPS-002 + OPS-003)** | 40 min |
| **Réaliste avec coef × 1,5** | 60 min |
| **Réel** | 48 min |
| **Écart vs estimé initial** | +8 min (+20 %) |
| **Écart vs réaliste** | −12 min (−20 %) |

**Verdict** : on est **dans la fourchette réaliste**. Les coefficients de calibration de Vague 7 fonctionnent.

---

## Devise IVIA

*Au sein de l'être — En actes.*

---

*Généré par Perplexity Computer — 7 mai 2026, 15h15 EDT*

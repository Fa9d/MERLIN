# Journal de déploiement — INFRA-005 (master `1790999`)

**Date** : 9 mai 2026
**Heure début** : 06:03 EDT
**Heure fin smoke tests verts** : 06:34 EDT
**Durée totale** : ~31 min (dont ~14 min de hangs scriptés à debugger)
**Stamp de référence** : `20260509_0603`
**Stamp backup VPS** : `20260509_061340`
**Opérateur** : David Phaneuf (PowerShell C:\MERLIN + SSH OVH + Perplexity Computer)
**VPS** : `ubuntu@137.74.42.121` → `https://ivia.quebec` + `https://api.ivia.quebec`

---

## 1. Périmètre déployé

### Commits livrés en prod (3 PR mergées le 8 mai 2026)

| Commit | PR | Contenu |
|---|---|---|
| `1790999` | #5 | chore(roles): ROLES-003 done + matrice V1.1 + audit post-PR #4 |
| `d7a9751` | #3 | feat: finalisation outil MERLIN (étapes A→D) |
| `03265ab` | #4 | fix(roles): corrections audit ROLES-003 |

### Tickets fermés cette vague

- **BACK-PAY-001 (P1, CRITIQUE)** — `require_operator()` ajouté sur `POST /api/v1/payments/stripe/checkout/audio-async`. Faille d'auth manquante sur endpoint de checkout Stripe → désormais **401 Unauthorized** pour requêtes non authentifiées (vérifié 3/3 en prod).
- **BACK-BOOK-001 (P2)** — `cancel_slot` aligné sur `require_verified_email_user`.
- **BACK-DEPS-001 (P3)** — `require_supervisor()` créé + alias rétroactif `require_supervision_roles = require_supervisor` (zéro rupture).
- **BACK-AUDIO-001 (P2)** — Docstring complète sur `audio-sessions/client-join`.
- **DOC-ROLES-001 (P3)** — Reporté (non-bloquant).

### Livrables non-runtime

- Matrice rôles V1.1 (59 routes documentées) — `00_GOUVERNANCE/MERLIN_GOUV_MATRICE_ROLES_ROUTES_V1.md`
- Audit rôles statut **done** — `05_PREUVES_SOURCES/AUDIT_ROLES_ROUTES_2026-05-08.md`
- ADR-0005 (DEC-044) — frontière faits/hypothèses (architecture, pas encore implémentée)
- Config Playwright + 2 specs e2e (frontend, no-runtime impact)
- 9 tests pytest validant les guards corrigés (passent en 2.18s)

### Migrations Alembic

**Aucune.** Vérifié — `alembic current` confirme `20260507_0018 (head)` inchangé. Phase 4 du runbook = no-op cette vague.

---

## 2. Procédure exécutée

### Phases réalisées

| Phase | Statut | Notes |
|---|---|---|
| 0. Préparation locale | ✅ | Master à `1790999`, fast-forward sans surprise |
| 1. Build tarballs | ✅ | backend 75K + frontend 372K + prompts 38K |
| 2. SCP transfert | ✅ | 3 tarballs vers `/tmp/` du VPS |
| 3. Bascule code (sudo) | ✅ | Backups `OLD_20260509_061340` créés sur backend + frontend |
| 4. Migrations Alembic | ✅ no-op | `20260507_0018 (head)` confirmé inchangé |
| 5. Build images Docker | ✅ | api + frontend, ~10-15 min |
| 6. Restart stack | ✅ | `merlin-api-1` Up (healthy) en ~45s, frontend Up en ~39s |
| 7. Smoke tests | ✅ | Tous verts, dont 401 confirmé sur BACK-PAY-001 |
| 8. Cleanup tarballs | ✅ | Local + `/tmp/` VPS nettoyés |

### Anomalies rencontrées (pour mémoire runbook)

1. **Encodage script PowerShell** — Premier script généré contenait des caractères UTF-8 (`é`, `—`, apostrophes typographiques) qui ont fait planter le parser PS 5.1 (interprétation Windows-1252). **Fix** : régénération en ASCII pur.
2. **Permission denied sur `mv`** — Phase 3 a échoué initialement parce que `/opt/merlin/10_backend_merlin_api` appartient à `root` (créé par Docker). **Fix** : ajout de `sudo` sur les `mv` et `tar -xzf`. Déjà documenté dans le runbook (ligne 401) mais oublié dans le script v1.
3. **Hang silencieux après `alembic current`** — Le here-string `@'...'@` avec `set -e` + `|| rollback` envoyé via `bash -s` stdin a fait sortir bash silencieusement après Phase 4, sans exécuter Phases 5-7. **Fix** : split en plusieurs `ssh $VPS "commande_simple"` séparés (script v3 `deploy_finish_phase5.ps1`).
4. **Faux positif 404 sur smoke test** — Premier smoke test attaquait `/payments/stripe/checkout/audio-async` (sans préfixe). La vraie route est `/api/v1/payments/stripe/checkout/audio-async` (préfixe `api_v1_prefix` + `/payments/stripe`). **Fix** : test relancé sur l'URL correcte → 401 confirmé 3/3.

---

## 3. Validation post-déploiement

### Containers Docker

```
merlin-api-1            Up (healthy)    Image sha256:19423c27... créée 2026-05-09T10:29:57Z
merlin-frontend-1       Up              Next.js 16.2.4 ready en 348ms
merlin-nginx-1          Up 40h          (inchangé)
merlin-db-1             Up 4d (healthy) (inchangé)
merlin-redis-1          Up 4d (healthy) (inchangé)
merlin-livekit-1        Up 4d           (inchangé)
merlin-livekit-egress-1 Up 4d (healthy) (inchangé)
merlin-uptime-kuma      Up 40h (healthy)(inchangé)
merlin-dozzle           Up 40h          (inchangé)
```

### Code BACK-PAY-001 confirmé dans le container

```
$ docker exec merlin-api-1 grep -A2 'audio-async' /app/app/api/routes/payments.py
    "/checkout/audio-async",
    response_model=StripeCheckoutSessionRead,
    status_code=status.HTTP_201_CREATED,
--
    """Crée une session Stripe Checkout pour le flux audio-async.

    Sécurité (BACK-PAY-001) : route réservée aux opérateurs internes.
```

### Smoke tests

| Endpoint | Méthode | Code attendu | Code obtenu | Verdict |
|---|---|---:|---:|:---:|
| `https://ivia.quebec` | GET | 200 | 200 | ✅ |
| `https://api.ivia.quebec/` | GET | 200/401 | 200 | ✅ |
| `https://api.ivia.quebec/api/v1/payments/stripe/checkout/audio-async` | POST (sans auth) | **401** | **401** | ✅ |
| `https://api.ivia.quebec/api/v1/payments/stripe/checkout/audio-async` | POST body vide | **401** | **401** | ✅ |
| `https://api.ivia.quebec/api/v1/payments/stripe/checkout/audio-async` | POST `{}` JSON | **401** | **401** | ✅ |
| `https://status.ivia.quebec` | GET | 200/302 | 302 | ✅ |

Le **3/3 sur le test BACK-PAY-001** confirme que l'auth est vérifiée AVANT la validation Pydantic — comportement attendu de `require_operator()` injecté en dépendance FastAPI.

### Logs API (post-restart)

```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:33018 - "GET /health HTTP/1.1" 200 OK
```

Aucune erreur de boot, healthchecks passent.

---

## 4. Backups conservés

À supprimer après 24h de validation :

```bash
sudo rm -rf /opt/merlin/10_backend_merlin_api.OLD_20260509_061340
sudo rm -rf /opt/merlin/09_app_ivia_merlin.OLD_20260509_061340
```

---

## 5. Reste différé après cette vague

1. **Implémentation effective ADR-0005** — prompt v1.1 + Pydantic + migration Alembic 0019 + 2 tests
2. **Tests Playwright flux authentifié** hold→confirm
3. **DOC-ROLES-001 (P3)** — pattern `_validate_create_access` dans la doctrine
4. **Investigation écart 51 routes OpenAPI prod vs 59 code local** — à vérifier maintenant que le déploiement est fait (l'écart devrait s'être réduit)

---

## 6. Calibration runbook

| Phase | Estimé runbook | Réel cette session |
|---|---:|---:|
| Phases 0-2 (build + scp) | 20 min | 5 min |
| Phase 3 (bascule) | 10 min | 2 min (1er échec sudo + reprise) |
| Phase 4 (migrations) | 5 min | no-op |
| Phase 5 (build Docker) | 15 min | ~13 min |
| Phase 6 (restart) | 5 min | 1 min |
| Phase 7 (smoke tests) | 5 min | 3 min (avec correction URL) |

**Total runbook estimé sans migrations** : ~45 min
**Total réel** : 31 min de travail effectif + temps de debug scripts (~15 min)

---

## 7. Améliorations runbook à intégrer

À reporter dans `00_GOUVERNANCE/PLANNING/RUNBOOK_DEPLOY.md` :

1. **Ajouter `sudo` aux Phases 3** sur les `mv` et `tar -xzf` dans `/opt/merlin/`
2. **Préciser le préfixe `/api/v1/`** dans les exemples de smoke tests
3. **Recommander script bash en here-string `@'...'@`** (literal) plutôt que `@"..."@` quand on envoie du bash via stdin SSH depuis PowerShell
4. **Recommander split en `ssh $VPS "cmd"` séparés** plutôt qu'un gros `bash -s` quand `set -e` + traps sont impliqués

À transformer en mini-tickets (ou intégrer directement au RUNBOOK_DEPLOY.md à la prochaine session).

---

## Devise IVIA

*Au sein de l'être — En actes.*

---

*Journal généré 9 mai 2026, 06:38 EDT*
*Faille critique BACK-PAY-001 fermée en prod ✅*

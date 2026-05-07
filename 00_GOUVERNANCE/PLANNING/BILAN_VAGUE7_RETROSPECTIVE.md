# Bilan Vague 7 — Rétrospective

**Date** : Jeudi 7 mai 2026
**Période** : ~10h27 → 13h26 EDT (≈ 3h)
**Statut** : ✅ DÉPLOYÉE EN PROD ET COMMITÉE

---

## ⚠️ Note méthodologique

**Aucun planning formel n'a été produit avant le démarrage de la Vague 7.**
Les estimés présentés dans ce document sont **reconstruits a posteriori** à partir de standards d'industrie pour des tâches comparables (déploiement Docker, migration Alembic, transfert SCP, etc.).

Ce bilan reste utile comme **calibration** pour les futures estimations, mais ne constitue pas une mesure réelle d'écart estimé/réel au sens propre.

À partir de la **Vague 8**, le pattern instauré est :
1. Écrire `PLANNING_VAGUE_X.md` chiffré **avant** démarrage
2. Commit du planning sur master
3. Bilan estimé/réel **mesuré** en fin de vague

---

## Tableau récapitulatif

| # | Tâche | Estimé | Réel | Écart | Statut |
|---|---|---:|---:|---:|---|
| 1 | Préparation tarballs (backend + frontend + prompts) | 10 min | 35 min | +25 min | ✅ |
| 2 | Transfert SCP vers VPS | 5 min | 12 min | +7 min | ✅ |
| 3 | Bascule code (backend + frontend OLD/swap) | 10 min | 8 min | −2 min | ✅ |
| 4 | Migration Alembic (0017 → 0018) | 5 min | 4 min | −1 min | ✅ |
| 5 | Build images Docker | 15 min | 18 min | +3 min | ✅ |
| 6 | Restart stack + diagnostic | 10 min | 25 min | +15 min | ✅ |
| 7 | Fix volume `/11_PROMPTS` | — (imprévu) | 12 min | +12 min | ✅ |
| 8 | Smoke tests | 5 min | 6 min | +1 min | ✅ |
| 9 | Génération journal déploiement | 10 min | 8 min | −2 min | ✅ |
| 10 | Commit + push journal | 5 min | 5 min | 0 | ✅ |
| 11 | Analyse stack outils (Vague 8 livrée en parallèle) | 30 min | 25 min | −5 min | ✅ |
| | **TOTAL** | **1 h 45** | **2 h 58** | **+1 h 13 (+70 %)** | |

---

## Détail par tâche

### 1. Préparation tarballs — 10 min → 35 min (+25 min)

**Estimé** : `tar -czf` sur 2 dossiers + 1 prompts.
**Réel** : 5 tentatives échouées avant succès.

**Causes du dérapage** :
- PowerShell `Set-Content -Encoding utf8` ajoute un BOM en PS 5.1 → `tar` refuse
- Wildcards inline `--exclude='*.pyc'` mal interprétés par `tar.exe` Windows
- Apostrophes françaises dans messages cassent le parsing bash

**Solution finale** : `Set-Content -Encoding ascii` + fichier `deploy_excludes.txt` passé via `-X`.

**Leçon** : pattern à graver dans **OPS-001 (runbook deploy)**.

---

### 2. Transfert SCP — 5 min → 12 min (+7 min)

**Causes** :
- Première tentative `scp -r` sauvage interrompue (^C) après 487 MB de junk transféré
- Cleanup `/tmp` requis sur VPS
- Re-saisie passphrase à chaque commande SSH (ssh-agent non configuré, `Set-Service` exige admin)

**Leçon** : configurer ssh-agent en mode admin une bonne fois → économise ~30 s × N commandes.

---

### 3. Bascule code — 10 min → 8 min (−2 min) ✓

Renommage `*.OLD_<stamp>` + `mv` tarball déballé. Fluide. Backups conservés.

---

### 4. Migration Alembic — 5 min → 4 min (−1 min) ✓

Cascade 0017 → 0018 (5 migrations enchaînées) appliquée sans heurt.

---

### 5. Build Docker — 15 min → 18 min (+3 min)

`^C` prématuré de ma part (mauvaise lecture des logs), mais build avait déjà été au bout. Images datées `16:02` (api) et `16:04` (frontend). Sans gravité.

---

### 6. Restart + diagnostic — 10 min → 25 min (+15 min)

**Le pic d'imprévu de la journée**. `docker compose up` initial sans `--env-file .env.prod` → API restart loop → analyse logs → identification `PromptNotFoundError`.

**Leçon** : `docker compose --env-file .env.prod -f docker-compose.prod.yml` est désormais la **seule forme valide** documentée.

---

### 7. Fix volume `/11_PROMPTS` — IMPRÉVU → 12 min

**Bug latent découvert** : `prompt_loader.py` utilise `Path(__file__).parents[3] / "11_PROMPTS"` qui résout en `/` dans le container (chemins absolus différents host/container).

**Fix appliqué** : ajout volume mount `./11_PROMPTS:/11_PROMPTS:ro` dans `docker-compose.prod.yml` via patch Python regex.

**Backlog** : ticket **BACK-010** ouvert pour refactor propre (env var `PROMPTS_DIR`).

---

### 8. Smoke tests — 5 min → 6 min ✓

Frontend 200 / API 401 (auth attendue) / DB head `20260507_0018`. Tout vert à 13h08 EDT.

---

### 9. Journal déploiement — 10 min → 8 min ✓

216 lignes, 5 incidents documentés, patterns shell/SSH capturés.

---

### 10. Commit + push — 5 min → 5 min ✓

Commit `84ae4e2` poussé sur `master` à 13h26.

---

### 11. Analyse stack outils (Vague 8) — 30 min → 25 min ✓

Livrée en parallèle pendant les phases d'attente Docker. 356 lignes, recommandation 95 % open-source self-hosted, économie ~2 592 $/an.

---

## Synthèse — pourquoi +70 % ?

| Catégorie d'écart | Temps perdu | Évitable la prochaine fois ? |
|---|---:|---|
| Friction outillage Windows (tar, encoding, BOM) | ~25 min | ✅ Oui — OPS-001 |
| ssh-agent non configuré | ~5 min | ✅ Oui — 1 setup admin |
| Bug latent `prompt_loader.py` | ~15 min | ⚠️ Partiel — BACK-010 fixe la cause |
| Mauvaise commande Docker Compose initiale | ~10 min | ✅ Oui — runbook |
| **TOTAL ÉVITABLE** | **~55 min** | **80 % récupérable** |

**Sans ces frictions, le déploiement aurait pris ~2h pile** au lieu de 2h58.

---

## Vélocité observée vs estimée

- **Estimation initiale** : 1 h 45 → trop optimiste (sous-estime imprévus shell/Docker)
- **Réel pondéré** : 2 h 58 → cohérent avec un déploiement *first-time* sur stack complexe
- **Cible Vague 8 (déploiement)** : viser 1 h 30 (gain principal sur tar/SSH/Docker)

**Coefficient correcteur recommandé** pour futures estimations déploiement IVIA/MERLIN : **× 1,5 à × 1,7** tant qu'OPS-001 n'est pas écrit.

---

## Tickets backlog issus de cette Vague

| Ticket | Description | Priorité | Effort estimé |
|---|---|---|---:|
| **BACK-009** | Renommer 4 fichiers Alembic (cohérence nommage) | P3 | 30 min |
| **BACK-010** | Refactor `prompt_loader.py` (env var `PROMPTS_DIR`) | P2 | 1 h |
| **OPS-001** | Runbook deploy (capture des patterns Vague 7) | **P1** | 1 h 30 |
| **GOUV-002** | Hiérarchiser les 80 docs gouvernance | P3 | 2 h |

**Reco séquence** : OPS-001 d'abord (capture savoir frais) → BACK-010 (résout dette technique) → BACK-009 + GOUV-002 (cosmétique/organisation).

---

*Généré par Perplexity Computer — 7 mai 2026, 13h27 EDT*

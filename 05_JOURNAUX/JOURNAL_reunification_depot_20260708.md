# JOURNAL — Réunification du dépôt et audit de cohérence

**Date** : 2026-07-08
**Opérateur** : Claude Code (Fable 5), sous direction de David Phaneuf
**Références** : `JOURNAL` précédents dans `05_JOURNAUX/` ; commit de fusion `ddd76f0`.

---

## 1. Contexte

Depuis début juillet, la base de travail locale est `C:\_IVIA` (copie voulue « propre »),
mais la règle `.claude/rules/hygiene-sources.md` déclarait encore `C:/Dev/IVIA/MERLIN`
comme dépôt canonique. Un audit complet a été mené suite à des « problèmes de config »
récurrents.

## 2. Constats de l'audit (2026-07-07 → 08)

1. **Deux copies divergentes** : `C:/Dev/IVIA/MERLIN` gelé au 2026-07-02 (`bf66da6`) ;
   `C:\_IVIA` synchronisé GitHub et contenant tout l'historique. Rien d'unique dans
   l'ancienne copie.
2. **La prod (ivia.quebec) exécutait la branche `agents/cleanup-production-workflow`**
   (confirmé par le prix 75 $ live), pas la branche d'intégration
   `refonte-ivia-site-unifie` — 82 commits d'écart (migrations 0043-0050, Matomo,
   moteur d'analyse, journal structuré, carte de vie praticien).
3. **`.env.prod.example` désynchronisé du code** : bloc `MERLIN_SMTP_*` fantôme (le code
   lit `SMTP_*`), clés réelles manquantes (`FRONTEND_URL`, `MERLIN_ADMIN_EMAILS`,
   `MERLIN_PAYMENTS_TEST_MODE`, Matomo, sauvegarde). Cause plausible des configs cassées
   (courriels/magic links morts sur tout env reconstruit depuis l'exemple).
4. **Docs périmées** : CLAUDE.md donnait deux heads Alembic contradictoires
   (`20260504_0017` et `20260701_0040`) ; réel = `20260707_0050`. `backend.md` disait
   `20260625_0039`.
5. **Résidus** : `test.txt` commité, 4 `.env.prod.bak*` à la racine, rapport
   d'installation Matomo orphelin, variable morte `JWT_SECRET` dans `.env.prod`.
6. **SSH VPS impossible depuis cette machine** (pas de clé — `Permission denied`).
   À rétablir pour redéployer/vérifier la prod d'ici.

## 3. Actions réalisées

- **Fusion** `agents/cleanup-production-workflow` → `refonte-ivia-site-unifie`
  (commit `ddd76f0`). Résolutions : imports `behavioral_profile` + `appointment`
  conservés (`db/base.py`) ; bloc migrations CLAUDE.md unifié (head `20260707_0050`) ;
  `index.html` / `reserver.html` = version prod ; `praticien/seance-en-cours.html`
  supprimé (mock orphelin) ; `profiling_safety_suite_v1` **conservée** (registry +
  fichier — elle n'existait que côté refonte, jamais supprimée volontairement).
  Validation : `app.main` importe (176 routes), chaîne Alembic intacte, head unique.
- **`.env.prod.example` réécrit** — chaque clé correspond à ce que lisent
  `app/core/config.py`, `docker-compose.prod.yml` et `deploy/backup.sh`.
- **Dépôt canonique** : `C:\_IVIA` acté dans `hygiene-sources.md` et CLAUDE.md ;
  `C:/Dev/IVIA/MERLIN` gelé (lecture seule, suppression à décider plus tard).
- **Nettoyage** : rapport Matomo archivé en intrant
  (`_archives/intrants/2026-07/matomo_system_check_20260706.txt`), `.env.prod.bak*`
  déplacés vers `backups/env/` (non versionné), `JWT_SECRET` retiré de `.env.prod`
  local (variable morte ; l'auth lit `MERLIN_AUTH_SECRET_KEY`).

## 4. État Matomo (mesure d'audience souveraine)

Matomo 5 tourne sur le VPS (`stats.ivia.quebec`, conteneurs `matomo` + `matomo-db`,
vhost nginx, script `ivia_site_v2/shared/analytics.js`, événement de conversion
`demande_envoyee`). Reste à faire **par David dans le navigateur** : assistant
d'installation (idSite = 1), réglages Confidentialité (IP anonymisées 2 octets,
purge 90 j, respect DNT), objectif « Demande envoyée », test temps réel.
⚠ Le rapport d'installation signalait « connexion SSL non forcée » — forcer HTTPS
dans Administration → Général avant usage réel. Voir `docs/ops-matomo.md`.

## 5. Suites à donner

1. Push `refonte-ivia-site-unifie` + déploiement tracé (`deploy/pull-deploy.sh --build`
   sur le VPS) pour que la prod repointe sur la branche d'intégration.
2. Rétablir une clé SSH de cette machine vers `ubuntu@137.74.42.121`.
3. Chantier analyse : coordination analyses séances/enregistrements + journal
   inter-séances + restitutions client/praticien (voir directive de David du
   2026-07-07 en session — périmètre à cadrer dans `00_GOUVERNANCE/`).

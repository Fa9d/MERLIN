# JOURNAL — Consolidation des fondations (22 juin 2026)

**Type** : décision structurante + opération prod
**Auteur** : David Phaneuf + Claude Code
**Branche** : `refonte-ivia-site-unifie`
**Références** : `03_MODELE_GOUVERNANCE/MERLIN_MODELE_OPERATOIRE.md`, `.github/workflows/ci.yml`,
`deploy/backup.sh`, `deploy/pull-deploy.sh`, `docs/ops-sauvegarde.md`, `CLAUDE.md` §2/§14

---

## Contexte

Après une série de livraisons « vitrine » (accueil, page praticiens, ressources, 16 articles),
constat partagé : on enchaînait **Cadrer → Construire → expédier en prod**, en sautant les étapes
**Mesurer** et **Stabiliser** du modèle opératoire. Décision : **pause des features, consolidation
des fondations**, sur une base traçable et sauvegardée.

## Problèmes de fond identifiés

1. **Déploiements non traçables** — la prod était poussée par `tar` hors de Git ; `/opt/merlin`
   n'était pas un dépôt → la prod ne correspondait à aucun commit connu.
2. **Filet de tests faible** — le CI ne rend **bloquants** que `ruff` + 3 tests « sans DB ». La
   suite complète Postgres est en `continue-on-error: true` (informatif) et la **safety suite**
   est commentée (manque le secret `ANTHROPIC_API_KEY`). Cf. `ci.yml`.
3. **Sauvegarde** — aucune copie hors-conteneur des données ; OVH hors-site reporté (coûts, phase dev).

## Décisions et actions (faites ce jour)

- **Sauvegarde locale gratuite** — `deploy/backup.sh` rendu **dégradable** : sauvegarde locale
  toujours (dump Postgres + audios dans `/opt/merlin/backups`, rétention 7) ; chiffrement AES-256
  seulement si `MERLIN_BACKUP_PASSPHRASE` ; hors-site OVH seulement si variables OVH présentes.
  Correctif : lecture de `.env.prod` sans `source` (valeurs avec espaces). **1ʳᵉ sauvegarde réussie**
  (base 45K + audios 26M).
- **Prod = checkout Git** — clé de déploiement **lecture seule** ajoutée au dépôt GitHub privé ;
  `/opt/merlin` converti en dépôt Git (`git init` → `fetch` → `reset --hard origin/refonte-ivia-site-unifie`).
  Vérifié : `git diff` vide (**prod == commit `cc070ee`**), `.env.prod` intact et gitignoré, site +
  API + 9 conteneurs sains. Snapshot config pré-bascule conservé dans `backups/_pre_git_config_*.tar.gz`.
- **Flux de déploiement tracé** — `deploy/pull-deploy.sh` : `git pull` (statique) ou `--build`
  (backend/migrations). Le `tar` manuel est **déprécié**.

## Reste à faire (suite « Stabiliser »)

- **Durcir le filet de tests** : faire passer la suite DB en local, la rendre bloquante dans le CI,
  brancher la **safety suite** (action requise : ajouter le secret `ANTHROPIC_API_KEY` dans GitHub).
- **OVH hors-site** : à activer avant l'arrivée de vrais clients (conteneur `merlin-backups` BHS +
  clés S3 + passphrase hors VPS). Voir `docs/ops-sauvegarde.md`.
- **Nettoyage des débris** sur le VPS (`*.OLD_*`, `*.bak_*`, `*_prev`, `docker-compose.prod.yml.bak_*`).
- **Reprendre les features** une fois la base verte.

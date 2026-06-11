# JOURNAL — Référentiels vivants & amorce Carte de Vie

**Date** : 2026-06-10
**Branche** : `refonte-ivia-site-unifie`
**Opérateur** : David Phaneuf + Claude Code (Opus 4.8)
**Référence amont** : `00_DOCTRINE/CARTE_DE_VIE_modele_v0.1.md`, `JOURNAL_REFONTE_PARCOURS_CLIENT_MAGIC_LINK_20260519.md`

---

## 1. Décision structurante

Lancement du **redéploiement modulaire** de MERLIN sous le principe directeur **« tout est
référentiel »** : le sens (axes, tensions, contexte, pressions, signaux, vigilance,
orientations) est extrait des prompts/docs vers des fichiers YAML déclaratifs versionnés,
chargés à l'exécution par un registre unique. Objectif : configurer et faire évoluer le
système sans réécrire le moteur.

## 2. Constat d'état des lieux (vérité-terrain)

- **Fork frontend** : la prod sert le **site statique `ivia_site_v2`** (`nginx/default.conf:78-79`,
  volume monté), pas le conteneur Next.js `09_app_ivia_merlin` (construit mais **non routé**).
  Les 12 derniers commits portent à 100 % sur `ivia_site_v2` (dernier : 2026-06-09). La doc
  (README Next.js, journaux de mai) affirme l'inverse → **doc périmée, à acter**.
- **Migrations** : HEAD réel = `20260528_0027_add_temporal_model` (CLAUDE.md / backend.md
  annoncent encore `20260513_0022` → à corriger).
- **Dépendances** : `anthropic`/`stripe` en `>=` sans borne ; pas de lockfile ; PyYAML
  seulement transitif.
- **Tests** : `conftest.py` impose une fixture **`autouse=True` (`reset_app_users`) qui exige
  un Postgres local pour TOUT test**, même unitaire — bloque les tests rapides hors DB.
  À traiter dans le volet CI (marquer les tests DB, ne pas forcer la connexion en autouse).
- **Modèle Claude codé en dur** : `claude-sonnet-4-20250514` dans le pipeline IA et les
  frontmatter METH — à rendre piloté par config.

## 3. Livré ce jour

**Doctrine**
- `00_DOCTRINE/CARTE_DE_VIE_modele_v0.1.md` — spec fondatrice (proposition) : 5 strates
  (Sol · 11 axes · Ligne de vie · Champs de tension · Horizon), 3 lectures
  (client / praticien / observatoire), adossée au modèle temporel existant.
- `00_DOCTRINE/referentiels/` — 7 référentiels YAML + `README.md` de gouvernance :
  `axes` (11), `tensions` (10), `familles_contexte` (6), `pressions_societales` (9),
  `signaux_contextuels` (12), `vigilance` (4), `prochaines_etapes` (7). Chacun cite sa
  source autoritative et porte une enveloppe commune versionnée.

**Backend**
- `10_backend_merlin_api/app/referentiels/` — module `registry.py` (`load_referentiel`,
  `get_entries`, `get_codes`, `available_referentiels`, validation d'enveloppe + unicité
  des codes, cache mémoire) calqué sur la convention de `prompt_loader.py`.
- `tests/test_referentiels_registry.py` — couverture chargement / validation / fidélité.
- `requirements.txt` — ajout de `pyyaml==6.0.2` (dépendance désormais directe).

**Vérification** : exécution directe (hors pytest, à cause de la fixture DB autouse) —
les 7 référentiels chargent, comptes conformes aux sources, territoire fondateur en ordre 1,
vigilance ordonnée, rejets d'erreur OK. **Tout vert.**

## 4. Correction de fidélité notée

Affirmation initiale erronée (« METH-002 ne liste que 11 signaux ») corrigée : la source
**définit bien 12 signaux**. Référentiel, README et test alignés sur 12.

## 5. Prochaines étapes proposées

1. Prototype **lecture praticien de la Carte de Vie** (visx/D3, données fictives).
2. Filet **CI + qualité** : `uv` + lockfile, `ruff`, GitHub Actions exécutant la safety
   suite ; **corriger la fixture DB autouse** pour permettre les tests unitaires rapides.
3. Swap **AssemblyAI → faster-whisper** (auto-hébergé, données Québec — Loi 25).
4. Faire des prompts METH des **consommateurs du registre** (fin de la duplication).
5. Mettre à jour `CLAUDE.md` / `.claude/rules/backend.md` (HEAD migrations, frontend réel).

> Aucune donnée ni aucun code de production modifié de façon irréversible ; travail sur
> branche, données fictives. Documents `*_v0.1` ouverts à l'amendement du fondateur.

# CONTRIBUTING — MERLIN / IVIA

> Workflow de l'équipe réelle : David Phaneuf (fondateur, arbitre) + agents Claude Code
> (dev/reviewer outillés). Lire `CLAUDE.md` avant tout ; ce fichier ne couvre que le
> flux de livraison.

## Le flux, du besoin à la prod

1. **Partir du canon** : dépôt `C:\_IVIA` (local) / `Fa9d/MERLIN` (GitHub), branche
   d'intégration `refonte-ivia-site-unifie`. Ne jamais travailler sur une autre copie.
2. **Brancher court** : `feat/<sujet>` ou `agents/<sujet>`, durée de vie **< 5 jours**.
   Une branche qui dépasse 20 commits d'écart avec l'intégration doit fusionner ou mourir
   (leçon des 5 jours de divergence de juillet 2026).
3. **Commits** : format `feat|fix|docs|refactor|test(scope): message court`, en français.
   Pas de commits de checkpoint de session sur les branches partagées.
4. **PR** : même en solo. Le template s'affiche seul ; la checklist n'est pas décorative.
   Self-merge autorisé **si et seulement si** la CI est verte.
5. **Gates spéciaux** (non négociables, voir CLAUDE.md §6.1/§8/§11) :
   - `11_PROMPTS/**` touché → bump de version du prompt + safety evals ≥ 0.85 ;
   - auth / paiements / données client / connecteurs → skill `security-review` avant merge ;
   - structure du repo, Makefile, deploy/, managed_agents/, modèles client/praticien,
     conformité → **CLAUDE.md mis à jour dans la même PR**.
6. **Déployer** : uniquement depuis la branche d'intégration, uniquement par
   `bash deploy/pull-deploy.sh [--build]` sur le VPS. La prod correspond TOUJOURS à un
   commit poussé. Le tar/scp manuel est interdit.
7. **Journaliser** : déploiement, décision structurante, incident → un fichier
   `05_JOURNAUX/JOURNAL_<sujet>_<YYYYMMDD>.md` (append-only, on n'écrase jamais).

## Démarrer en local (< 10 min)

```bash
# Backend
cd 10_backend_merlin_api
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload      # nécessite un Postgres local ou MERLIN_DATABASE_URL

# Site public (statique)
cd ivia_site_v2 && python -m http.server 8080

# Tests comme la CI
cd 10_backend_merlin_api
python -m ruff check .
python -m pytest -m "not real_api" -o addopts="" -q   # suite complète (Postgres requis)
python -m pytest tests/test_referentiels_registry.py -o addopts="" -q  # sans DB
```

## Ce qu'on ne fait jamais

- Committer un secret, un `.env` réel, un `.bak` (gitleaks casse la CI, et c'est voulu).
- Poser un diagnostic/prescription dans une sortie client (constitution §6.4 — triade
  Observation / Hypothèse / Orientation, vocabulaire Loi 21 filtré).
- Installer un paquet `ruvnet/*` ou toucher au Next.js archivé (`09_app_ivia_merlin/`).
- Contourner `--env-file .env.prod` en prod (utiliser `make <cible>` ou les scripts).

# CLAUDE.md — MERLIN/IVIA

> Fichier court par design. Détails dans `00_ai/skills/`. Charger un skill **uniquement** quand le sous-domaine concerné est touché.

## Orientation 30 secondes

- **MERLIN** = repo-système canonique (gouvernance, méthodes, prompts, app).
- **IVIA** = couche d'exposition publique (frontend `09_app_ivia_merlin/`, `ivia.quebec`).
- **Backend** : FastAPI / PostgreSQL / Alembic dans `10_backend_merlin_api/`.
- **Frontend** : Next.js 16 + Turbopack dans `09_app_ivia_merlin/`.
- **Contexte** : santé mentale, Québec, Loi 25 — sensibilité max sur les données.

## À charger selon la tâche

| Tâche | Skill |
|---|---|
| S'orienter avant une modif transverse | [`00_ai/skills/repo-map.md`](00_ai/skills/repo-map.md) |
| Travail frontend | [`00_ai/skills/ivia-frontend.md`](00_ai/skills/ivia-frontend.md) |
| Travail backend | [`00_ai/skills/merlin-backend.md`](00_ai/skills/merlin-backend.md) |
| Avant de dire « terminé » | [`00_ai/skills/verification.md`](00_ai/skills/verification.md) |
| Branches / commits / PRs | [`00_ai/skills/git-workflow.md`](00_ai/skills/git-workflow.md) |
| Donnée client / service tiers | [`00_ai/skills/privacy-quebec.md`](00_ai/skills/privacy-quebec.md) |

Sous-projets avec règles locales : `09_app_ivia_merlin/AGENTS.md`. Vue d'ensemble : `00_ai/README.md`.

## Règles absolues (non négociables)

1. **Pas de secret en clair** dans le code ou les commits. Seuls `*.env.example` sont commitables.
2. **Pas de donnée client réelle** dans tests/fixtures/logs/prompts.
3. **Pas de `docker compose` sans `--env-file .env.prod`** — utiliser `make <cible>` ou `bash deploy/prod-up.sh`.
4. **Frontend ne touche pas la DB directement** hors `src/app/api/**`. Tout passe par `src/lib/merlin-api.ts` → backend.
5. **Prompts dans `11_PROMPTS/`** — bumper la version à toute modif (`v1.0 → v1.1`).
6. **Pas de push, pas de PR sans accord humain** quand l'agent tourne en autonomie.
7. **Connecteurs autorisés uniquement** : Anthropic, LiveKit privé, AssemblyAI, OVH. Pas de Supabase, Whisper hosted, Speechmatics, ou autres SaaS sans validation.

## Conventions

- Commits : `feat|fix|docs|refactor|test|chore(scope): message court`.
- Branche par défaut : `master`. Branches dédiées pour features non triviales.
- Code en anglais, commentaires/docstrings en français.
- Langue de communication interne : français.

## Vérification minimale

Avant de marquer terminé : lancer lint + build/test du sous-projet touché, et énoncer dans le rapport ce qui a été vérifié vs non vérifié. Détail : `00_ai/skills/verification.md`.

## Ressources

- Ops Docker : `docs/ops-docker-compose.md`
- Déploiement : `deploy/prod-up.sh`, `docs/deploy-ovh.md`
- Optimisation tokens / usage agents : `docs/ai-workflow/token-optimization.md`
- Gouvernance et backlog : `00_GOUVERNANCE/` (lecture seule pour agents code)

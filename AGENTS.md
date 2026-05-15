# AGENTS.md — MERLIN/IVIA (Cursor & autres agents)

> Miroir court de `CLAUDE.md` pour les agents qui consultent `AGENTS.md` (Cursor, codex, etc.).
> Tout le détail vit dans [`00_ai/skills/`](00_ai/skills/). Ne pas tout charger d'un coup.

## Repo en une phrase

MERLIN = repo-système canonique (gouvernance + app). IVIA = surface publique (`ivia.quebec`). Frontend Next.js 16 dans `09_app_ivia_merlin/`, backend FastAPI dans `10_backend_merlin_api/`. Contexte santé mentale, Québec, Loi 25.

## Comment travailler ici

1. **S'orienter** via [`00_ai/skills/repo-map.md`](00_ai/skills/repo-map.md).
2. **Charger le skill du sous-projet** touché : `ivia-frontend.md` ou `merlin-backend.md`.
3. **Toujours lire** [`00_ai/skills/privacy-quebec.md`](00_ai/skills/privacy-quebec.md) avant de toucher à des données ou un service tiers.
4. **Avant de dire terminé** : [`00_ai/skills/verification.md`](00_ai/skills/verification.md).
5. **Git** : [`00_ai/skills/git-workflow.md`](00_ai/skills/git-workflow.md).

## Règles à mémoriser

- Pas de secret commité. Pas de donnée client réelle.
- Frontend → backend via `src/lib/merlin-api.ts` ; `src/lib/db.ts` réservé aux Route Handlers `app/api/**`.
- `docker compose` toujours avec `--env-file .env.prod`, ou passer par `make`.
- Prompts dans `11_PROMPTS/` — bumper la version à toute modif.
- Pas de push / pas de PR sans autorisation explicite.
- Connecteurs autorisés : Anthropic, LiveKit privé, AssemblyAI, OVH. Pas de Supabase / Whisper hosted / Speechmatics.

## Optimisation tokens en Cursor

Voir [`docs/ai-workflow/token-optimization.md`](docs/ai-workflow/token-optimization.md) pour le réglage `.cursorignore`, l'usage de `@00_ai/...` et le scoping par sous-projet.

## Conventions

- Commits : `feat|fix|docs|refactor|test|chore(scope): message`.
- Branche par défaut : `master`. Branche courante de référence : `ivia-trace-vocale-accueil`.
- Code en anglais, commentaires/docstrings en français.

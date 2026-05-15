# 00_ai/ — Structure d'assistance IA MERLIN/IVIA

> Inspiré des principes publics partagés par Boris Cherny pour Claude Code/Cursor.
> Texte original, ancré dans MERLIN/IVIA. Aucun contenu importé verbatim d'un repo tiers.

## Principes

1. **CLAUDE.md racine court** (≤ ~1000 tokens) — ne contient que l'orientation et des pointeurs.
2. **Skills à la demande** (`00_ai/skills/*.md`) — chargés uniquement quand le sous-domaine est touché.
3. **Contextes par sous-projet** — `09_app_ivia_merlin/AGENTS.md` et `10_backend_merlin_api/` ont leurs propres règles locales.
4. **Vérification systématique** — chaque skill liste les commandes de build/lint/test à exécuter.
5. **Leçons durables** — `00_ai/lessons/` consigne les erreurs récurrentes pour ne pas les rejouer.
6. **Branches/worktrees** — `git-workflow.md` décrit le parallélisme sans casser `master`.

## Index des skills

| Skill | Quand le charger |
|---|---|
| [`repo-map`](skills/repo-map.md) | S'orienter avant toute modif transverse |
| [`ivia-frontend`](skills/ivia-frontend.md) | Travail dans `09_app_ivia_merlin/` |
| [`merlin-backend`](skills/merlin-backend.md) | Travail dans `10_backend_merlin_api/` |
| [`verification`](skills/verification.md) | Avant de marquer une tâche « terminée » |
| [`git-workflow`](skills/git-workflow.md) | Branches, worktrees, commits, PRs |
| [`privacy-quebec`](skills/privacy-quebec.md) | Toute donnée client / Loi 25 / LPRPDE |

## Convention d'usage

- **Claude Code** : ouvrir le skill pertinent au début d'une session sur un sous-projet, pas tous ensemble.
- **Cursor** : pointer ces fichiers via `@00_ai/skills/<nom>.md` dans le chat plutôt que de tout indexer.
- **Sous-agents** : les checklists `verification.md` et `privacy-quebec.md` doivent être lues par tout agent générant ou modifiant du code.

## Lessons

`00_ai/lessons/` — un fichier court par leçon (`YYYY-MM-DD-titre.md`). Ne consigner que ce qui n'est pas évident depuis le code ou git log.

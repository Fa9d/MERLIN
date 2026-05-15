# Skill — git-workflow

> Branches, worktrees, commits, PRs pour MERLIN.

## Branche principale

- `master` est la branche par défaut. En phase solo, des commits directs sont tolérés pour de la doc, du fix mineur, ou des updates `00_ai/`.
- Pour toute fonctionnalité non triviale ou risquée (frontend hero, backend auth, migration DB) : **branche dédiée**.

## Convention de nommage

```
feat/<scope>-<court-titre>       # nouvelle fonctionnalité
fix/<scope>-<court-titre>        # correctif
docs/<scope>-<court-titre>       # documentation
chore/<scope>-<court-titre>      # outillage, deps
ivia-<thème>                     # branche héritée IVIA (ex: ivia-trace-vocale-accueil)
```

## Commits

Format : `feat|fix|docs|refactor|test|chore(scope): message court en français ou anglais`.

Exemples observés :
- `feat(operator): add prospect intake handling queue`
- `fix(rendez-vous): align public prospect intake flow`
- `docs(deploy): journal public rendez-vous production fix`

## Worktrees pour parallélisme

Quand un agent doit travailler en parallèle sans contaminer `master` :

```bash
git worktree add ../MERLIN-<sujet> -b feat/<sujet>
# travail dans ../MERLIN-<sujet>
git worktree remove ../MERLIN-<sujet>   # quand fini et mergé
```

Avantages : pas de stash/switch, IDE séparé, build cache indépendant.

## Avant de pousser

- `git status` propre.
- `git log --oneline origin/<branche>..HEAD` cohérent (pas de commits parasites).
- Skill [`verification`](verification.md) exécuté.

## Push & PR

- **Ne jamais pousser sans autorisation explicite de l'humain** quand l'agent tourne en autonomie.
- PR : titre court + section *Résumé* / *Vérifications* / *Impact*. Voir convention dans le repo (commits récents pour exemples).
- Pas de PR auto-approuvée par un agent.

## Branches sensibles à ne pas casser

| Branche | Pourquoi |
|---|---|
| `master` | Prod référence |
| `ivia-trace-vocale-accueil` | Intègre la vidéo d'accueil — base de travail courante |
| `deploy/prospect-handling-20260511` | Snapshot déploiement, lecture seule |
| `archive/*` | Historique gelé |

Toujours `git fetch` avant de checkout une branche distante pour éviter de partir d'un état obsolète.

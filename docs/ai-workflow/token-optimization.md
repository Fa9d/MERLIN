# Optimisation tokens & efficacité des agents — MERLIN/IVIA

> Comment utiliser la structure `00_ai/` localement et dans Cursor/Claude Code pour réduire la consommation de tokens et obtenir des agents plus précis.

## Principes appliqués au repo

1. **CLAUDE.md court** (~900 tokens) — chargé à chaque session, ne contient que pointeurs et règles absolues.
2. **Skills à la demande** dans [`00_ai/skills/`](../../00_ai/skills/) — un fichier par sous-domaine, chargé uniquement quand pertinent.
3. **AGENTS.md miroir** à la racine et un autre local dans `09_app_ivia_merlin/` pour les outils qui le lisent.
4. **Pas de duplication** : si un détail vit dans un skill, il ne doit pas être recopié dans `CLAUDE.md`.

## Claude Code — usage recommandé

### Début de session

Claude Code lit `CLAUDE.md` automatiquement. Il **ne charge pas** `00_ai/skills/` par défaut.

Pour une tâche ciblée :

> « Je vais modifier le hero de la page d'accueil. Charge `00_ai/skills/ivia-frontend.md` et `00_ai/skills/verification.md`. »

Ne pas charger plusieurs skills si un seul suffit.

### Sous-agents

Pour explorer / faire une recherche large, déléguer à un sous-agent (`Agent` tool, `Explore` ou `general-purpose`) avec un brief précis :

- Limiter le champ : « cherche dans `10_backend_merlin_api/app/api/routes/` uniquement ».
- Demander un rapport court (« report under 200 words »).
- Préférer plusieurs sous-agents parallèles à un seul agent long quand les recherches sont indépendantes.

### Git worktrees pour le parallèle

Pour deux modifs indépendantes (ex: hotfix backend + refonte UI), créer un worktree par sujet — voir [`00_ai/skills/git-workflow.md`](../../00_ai/skills/git-workflow.md). Évite le coût des switch + le rebuild d'index.

## Cursor — usage recommandé

### `.cursorignore`

Ajouter (si pas déjà fait) au minimum :

```
node_modules/
09_app_ivia_merlin/.next/
09_app_ivia_merlin/node_modules/
09_app_ivia_merlin/prisma/generated/
10_backend_merlin_api/.venv/
10_backend_merlin_api/__pycache__/
**/*.pyc
**/__pycache__/
06_IMPORTS_MESANGE/
07_EXPORTS/
DAVID_CORPUS/
ivia_mockups/
public/assets/video/*.mp4
```

Raison : Cursor indexe tout par défaut. Le frontend bundle, les venvs Python, les imports Mésange et les binaires vidéo polluent la recherche et explosent le contexte.

### Référencer un skill dans le chat

Plutôt que de demander « comment fonctionne le frontend », écrire :

```
@00_ai/skills/ivia-frontend.md
Modifie X dans page.tsx en respectant la règle data.
```

Le skill devient le contexte ciblé. ~500 tokens vs ~50 000 tokens si tout le sous-projet est indexé.

### Composer Mode / Agent

- Limiter le contexte au sous-projet touché (`09_app_ivia_merlin/` **ou** `10_backend_merlin_api/`, pas les deux).
- Ajouter `@00_ai/skills/verification.md` à la fin de la consigne pour forcer la vérification.

## Heuristiques générales

| Symptôme | Action |
|---|---|
| L'agent relit des dossiers non concernés | Ajouter au `.cursorignore` ou cibler le skill |
| Réponses verbeuses, peu actionnables | Réduire la fenêtre, exiger un format de sortie court |
| L'agent réintroduit un anti-pattern | Vérifier qu'une leçon existe dans `00_ai/lessons/`, sinon en créer une |
| Tokens consommés par exploration redondante | Déléguer à un sous-agent avec brief précis |
| Cursor lent à indexer après pull | Ajouter les chemins lourds au `.cursorignore` |

## Mesurer

Garder en tête un budget approximatif :

- `CLAUDE.md` racine : ~900 tokens.
- Un skill : 300–600 tokens.
- Session typique avec 2 skills chargés : ~2 000 tokens de contexte stable.

Si une session dépasse durablement ~10 000 tokens de contexte avant le premier prompt utilisateur, c'est qu'un skill ou un fichier de plus haut niveau est trop chargé — le déléguer dans un sous-fichier `00_ai/`.

## Quand mettre à jour cette structure

- Une règle absolue change → `CLAUDE.md` racine.
- Un sous-projet évolue (nouvelle convention, nouveau dossier) → skill correspondant.
- Une erreur récurrente est observée chez les agents → créer un fichier dans [`00_ai/lessons/`](../../00_ai/lessons/) et, si la règle est durable, l'intégrer au skill pertinent.

Le but n'est pas d'accumuler de la doc — c'est de garder le minimum pertinent toujours à jour.

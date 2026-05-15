# Skill — verification

> À charger **avant** de déclarer une tâche terminée. La vérification n'est pas optionnelle.

## Principe

Un agent ne doit pas annoncer « terminé » sur la base d'une simple inspection. Une preuve d'exécution est requise. Si la vérification ne peut pas être faite (env manquant, browser non installé), le dire **explicitement** dans le rapport — ne pas mentir par omission.

## Checklist par sous-projet

### Frontend (`09_app_ivia_merlin/`)

- [ ] `npm run lint` — 0 erreur.
- [ ] `npm run build` — build prod réussi (couvre TypeScript).
- [ ] Si UI modifiée : décrire la vérification visuelle effectuée, ou dire qu'elle ne l'a pas été.
- [ ] Vérifier qu'aucun import `@/lib/db` n'apparaît hors `src/app/api/`.
- [ ] Si `page.tsx` / `styles.css` touchés : confirmer que la vidéo d'accueil reste fonctionnelle.

### Backend (`10_backend_merlin_api/`)

- [ ] `pytest` — vert.
- [ ] Si modèles modifiés : `alembic revision --autogenerate` et inspection du diff.
- [ ] `alembic upgrade head` sur base locale sans erreur.
- [ ] Endpoint touché : test manuel via `curl` ou client HTTP, documenté dans le rapport.

### Transverse

- [ ] `git status` propre des fichiers non voulus (pas de `.env`, `node_modules`, `__pycache__`, fichiers générés).
- [ ] `git diff --stat` raisonnable — pas de drift hors-scope.
- [ ] Commits suivent `feat|fix|docs|refactor|test(scope): message`.

## Si rien ne peut être exécuté

Format de rapport accepté :

> **Vérifications non exécutées** : `npm run build` n'a pas pu être lancé (raison : …).
> **Vérifications partielles** : lecture statique + recherche d'usages — pas de régression apparente, mais non confirmé par exécution.

C'est honnête. Inventer un succès est interdit.

## Leçon associée

Si une régression atteint prod après un « terminé » prématuré, créer une entrée dans [`00_ai/lessons/`](../lessons/) pour fermer la boucle.

# JOURNAL — Unification des dépôts (plan B) — 2026-07-17

## Contexte

Constat fondateur : le travail était dispersé sur quatre dépôts GitHub (`Fa9d/MERLIN`,
`Fa9d/ivia`, `Fa9d/ivia-app`, `Fa9d/_IVIA.map`) avec trois pipelines de blogue
concurrents et deux clones locaux du même dépôt. Décision : **tout unifier dans le
dépôt canonique** (`C:\_IVIA` = `Fa9d/MERLIN`, acté 2026-07-08) — plan B validé.

## État des lieux avant unification

| Dépôt | Rôle réel | Dernier push | Problème |
|---|---|---|---|
| MERLIN | canonique (`C:\_IVIA`) | 07-15 | branche `feat/ivia-blog-deploy` portait une intégration blogue obsolète (5 articles, statique `_IVIA.map`) |
| ivia-app | source réelle du blogue Next.js | 07-15 | vivant en parallèle du canon ; `main` = 37 entrées, export statique configuré |
| _IVIA.map | corpus marketing/SEO (intrant consommé) | 07-13 | **public** (stratégie SEO + vocab Loi 21 exposés) |
| ivia | ancien dépôt unifié | 06-29 | dormant, contenu déjà dans MERLIN |

Clones locaux : `C:\_IVIA` (canon), `C:\ivia-app` (branche `feat/blog-app-router`,
sous-ensemble de `main` — 30 entrées sur 37), `C:\MERLIN` (**220 commits derrière**),
`C:\Dev\IVIA` (gelé le 07-08).

## Ce qui a été fait

1. **`_IVIA.map` passé en privé** sur GitHub (exposition stratégie + Loi 21 corrigée),
   puis archivé (lecture seule). Contenu gelé dans `_archives/intrants/2026-07/ivia-map/`
   (sans `.git`), conformément à la loi d'hygiène (intrants gelés).
2. **Blogue rapatrié** : `ivia-app@origin/main` (le sur-ensemble : 29 articles +
   2 tutos + visuels réseaux, export statique `basePath /ressources/blog`) importé
   dans **`09_blog_app/`** via `git archive` (source seule, sans historique — l'historique
   reste consultable dans le dépôt archivé).
3. **Export statique généré et déposé** dans `ivia_site_v2/ressources/blog/`
   (43 entrées) — pipeline documentée dans `09_blog_app/deploy/README-deploiement.md`.
4. **Purge des intégrations orphelines** de `feat/ivia-blog-deploy` :
   `public/ivia-blog.html`, `src/app/ivia-blog/`, `pages/ivia-blog.tsx`, gitlink
   `ivia-map` (dépôt imbriqué), plus les orphelins racine `build.log` et
   `package-lock.json`.
5. **Dépôts `ivia-app` et `ivia` archivés** sur GitHub (lecture seule).
6. **`C:\MERLIN` neutralisé** (renommé, plus de deuxième copie de travail).
7. `.gitignore` : artefacts de build du blogue ignorés (`09_blog_app/node_modules|.next|out`).
8. `_circulation.md` v1.1 : destination du blogue déclarée (canon `09_blog_app/` →
   dérivé `ivia_site_v2/ressources/blog/`).

## Règle d'or post-unification

**Une seule source de travail : `C:\_IVIA` (repo MERLIN).** Les trois autres dépôts
sont archivés — ne plus rien y pousser. Tout nouveau contenu blogue se fait dans
`09_blog_app/app/articles.ts`, export rebuilt puis déposé (voir README-deploiement).

## Garde-fous et points ouverts

1. ⚠️ **Gate Loi 21 avant prod** : les articles contiennent du vocabulaire réservé —
   `diagnostic` ×7, `psychothérapie` ×3, `soins psychologiques` ×2, `thérapie` ×1
   (comptés dans `app/articles.ts`). Décision fondateur requise avant de merger
   `feat/ivia-blog-deploy` → `refonte-ivia-site-unifie`.
2. La traction réelle du blogue (29 articles + 2 tutos) doit remplacer « 5 articles »
   dans les pièces du dossier de financement consolidé le 17 juillet.
3. La consolidation financement du 17 juillet (20 fichiers) reste **non commitée** —
   volontairement hors du commit d'unification.

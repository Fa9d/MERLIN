# Déployer le blog IVIA sous ivia.quebec/ressources/blog

> **Unification 2026-07-17** : l'app blogue vit désormais dans le dépôt canonique
> (`C:\_IVIA`, repo GitHub **MERLIN**), dossier `09_blog_app/`. L'ancien dépôt
> **ivia-app** est archivé (lecture seule) ; ne plus rien y pousser.

Le blog est une app Next.js **exportée en site 100 % statique** (`output: "export"`
dans `next.config.ts`), servie sous le sous-chemin `/ressources/blog` grâce à
`basePath`. On ne lance **aucun conteneur** et on ne touche **pas** à la config
Nginx : les fichiers exportés sont déposés dans le site statique existant
(`ivia_site_v2/ressources/blog/`), déjà servi par Nginx.

## Architecture
- `ivia.quebec/` (accueil) et `ivia.quebec/ressources/` = site **statique** du
  dossier `ivia_site_v2/`, servi par Nginx.
- La source du blog (canon) est `09_blog_app/` ; l'export statique (dérivé,
  reconstructible) est copié dans `ivia_site_v2/ressources/blog/` et commité
  avec le site.
- Les liens « Ressources » de la page d'accueil pointent déjà vers
  `/ressources/blog`.

## Reconstruire l'export
```bash
cd 09_blog_app
npm ci
npm run build          # génère le dossier out/ (export statique)
```
Le dossier `out/` contient : `index.html` (liste), un dossier par article
(`out/<slug>/index.html`) et `_next/` (CSS/JS, préfixés par /ressources/blog).
`node_modules/`, `.next/` et `out/` sont ignorés par git (voir `.gitignore` racine).

## Déployer dans le site statique
```bash
# depuis la racine du dépôt
rm -rf ivia_site_v2/ressources/blog
mkdir -p ivia_site_v2/ressources/blog
cp -r 09_blog_app/out/. ivia_site_v2/ressources/blog/

git add ivia_site_v2/ressources/blog
git commit -m "deploy(blog): mise à jour export statique /ressources/blog"
git push origin refonte-ivia-site-unifie
```
Sur le VPS : `git pull` puis le service statique habituel sert `ivia_site_v2/`.

## Vérifier en ligne
```bash
curl -I https://ivia.quebec/ressources/blog/                                   # 200
curl -I https://ivia.quebec/ressources/blog/sante-mentale-quebec-etat-des-lieux/  # 200
curl -I https://ivia.quebec/ressources/                                        # 200 (ancienne page intacte)
```

## Notes
- **Rien n'est écrasé** : `/ressources/` (index + anciens articles .html) reste
  intact ; on ajoute seulement le sous-dossier `blog/`.
- **Aucun changement Nginx** requis : le même service statique sert déjà tout
  `ivia_site_v2/`, donc `/ressources/blog/` est servi automatiquement.
- `trailingSlash: true` → les URLs se terminent par `/` et pointent vers un
  `index.html`, ce qui fonctionne avec n'importe quel service de fichiers statiques.
- Pour changer le sous-chemin un jour : modifier `basePath` dans
  `next.config.ts`, rebuild, recopier dans le dossier correspondant.
- ⚠️ **Gate Loi 21 avant mise en prod** : les articles contiennent encore du
  vocabulaire réservé (diagnostic ×7, psychothérapie ×3, soins psychologiques ×2,
  thérapie ×1 dans `app/articles.ts`). Décision fondateur requise avant de merger
  vers `refonte-ivia-site-unifie` (cf. `.claude/rules/safety.md`).

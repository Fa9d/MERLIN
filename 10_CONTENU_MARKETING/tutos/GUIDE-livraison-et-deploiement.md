# Guide de livraison — Tutos IVIA

Ce que je viens de produire et comment le mettre en ligne.

---

## 1. Ce qui est livré (dossier `tutos/`)

- **Scripts vidéo longs** (tournage + voix off) : `01_scripts_video/TUTO-app-client-LONG.md`, `TUTO-app-praticien-LONG.md`
- **Scripts vidéo courts** (60-90 s) : `02_versions_courtes/TUTO-app-client-COURT.md`, `TUTO-app-praticien-COURT.md`
- **Posts réseaux** (LinkedIn, FB, Insta, X, TikTok) : `03_posts_reseaux/app_client/` et `app_praticien/`
- **Programme réutilisable (SOP)** : `04_programme/PROGRAMME-contenu-blog-vers-reseaux.md`
- **Check-lists par réseau** : `05_checklists/CHECKLISTS-par-reseau.md`
- **Répertoire / index maître** : `README-repertoire-tutos.md`
- **Cartographie factuelle des apps** (source de vérité) : `reference-apps.md`

## 2. Section « Tutos » sur le site — DÉJÀ INTÉGRÉE

Une nouvelle catégorie **« Tutoriels & prise en main »** a été ajoutée au blog, avec deux articles :
- `tuto-app-client` → « Prendre en main votre espace client IVIA »
- `tuto-app-praticien` → « La console IVIA : piloter la maison »

Ils apparaissent dans le filtre de catégories du blog et sont accessibles à :
- `https://ivia.quebec/ressources/blog/tuto-app-client/`
- `https://ivia.quebec/ressources/blog/tuto-app-praticien/`

Le blog a été reconstruit (29 pages, build OK) et le nouvel export est déjà déposé dans
`MERLIN/ivia_site_v2/ressources/blog/`. Testé localement : liste + 2 pages tutos répondent 200.

## 3. Mise en ligne (même procédure que le blog)

Sur ton poste (PowerShell / VSCode), depuis le repo MERLIN :
```powershell
git add ivia_site_v2/ressources/blog
git commit -m "Ajout section Tutos (app client + praticien) au blog"
git push origin refonte-ivia-site-unifie
```

Puis sur le VPS :
```bash
ssh ubuntu@137.74.42.121
cd /opt/merlin && git fetch origin && git checkout refonte-ivia-site-unifie && bash deploy/pull-deploy.sh
```

Vérification après déploiement :
```bash
curl -s -o /dev/null -w "%{http_code}\n" https://ivia.quebec/ressources/blog/tuto-app-client/
curl -s -o /dev/null -w "%{http_code}\n" https://ivia.quebec/ressources/blog/tuto-app-praticien/
```
(les deux doivent répondre 200)

> Rappel : on n'écrase pas Docker/Nginx ; c'est un export statique servi par Nginx en bind mount `:ro`.

## 4. Cycle pour un futur article → tutos + réseaux

1. Publier l'article (comme d'habitude, via `ivia-app/app/articles.ts`).
2. Appliquer le **PROGRAMME** (`04_programme/`) : remplir la fiche, décliner sur les 5 réseaux.
3. Produire les visuels (`gen_visuals.py`).
4. Cocher les **check-lists** (`05_checklists/`).
5. Programmer et publier.

## 5. Prochaines actions de ton côté
- [ ] Filmer les captures d'écran en suivant les scripts longs (compte de démo, données remplies).
- [ ] Enregistrer les voix off (texte prêt dans les scripts).
- [ ] Monter les 4 vidéos, exporter les formats (horizontal site + vertical Reels/TikTok).
- [ ] Publier les 10 posts en suivant les check-lists.
- [ ] Déployer la section Tutos (étape 3 ci-dessus).

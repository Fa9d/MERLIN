# Répertoire des tutos IVIA — Index maître

Tout le contenu pour produire les tutos vidéo des apps **Client** et **Praticien**, les décliner sur les réseaux, et appliquer le même programme à chaque futur article de blog.

Dernière mise à jour : 14 juillet 2026.

---

## 📁 Structure du répertoire

```
tutos/
├── README-repertoire-tutos.md         ← vous êtes ici (index maître)
├── reference-apps.md                  ← cartographie factuelle des 2 apps (source de vérité)
│
├── 01_scripts_video/                  ← scripts de tournage + voix off (versions LONGUES)
│   ├── TUTO-app-client-LONG.md
│   └── TUTO-app-praticien-LONG.md
│
├── 02_versions_courtes/               ← scripts 60-90 s (Reels/TikTok/Shorts)
│   ├── TUTO-app-client-COURT.md
│   └── TUTO-app-praticien-COURT.md
│
├── 03_posts_reseaux/                  ← posts prêts à publier
│   ├── app_client/POSTS-app-client.md
│   └── app_praticien/POSTS-app-praticien.md
│
├── 04_programme/                      ← SOP réutilisable pour tout contenu blog
│   └── PROGRAMME-contenu-blog-vers-reseaux.md
│
└── 05_checklists/                     ← check-lists de publication par réseau
    └── CHECKLISTS-par-reseau.md
```

---

## 🎬 Les 4 tutos vidéo

| # | Tuto | Durée | Fichier | Public |
|---|---|---|---|---|
| 1 | App Client — long | 6-8 min | `01_scripts_video/TUTO-app-client-LONG.md` | Personnes accompagnées |
| 2 | App Client — court | 60-90 s | `02_versions_courtes/TUTO-app-client-COURT.md` | Grand public / réseaux |
| 3 | App Praticien — long | 6-8 min | `01_scripts_video/TUTO-app-praticien-LONG.md` | Praticien·nes / admin |
| 4 | App Praticien — court | 60-90 s | `02_versions_courtes/TUTO-app-praticien-COURT.md` | Écosystème / réseaux |

Chaque script long présente **deux colonnes** : actions à l'écran (tournage) + voix off (à lire).

---

## 📣 Répertoire complet des posts + check-liste de publication

Deux campagnes (une par app), **5 réseaux chacune = 10 posts**. Cocher au fur et à mesure.

### Campagne A — App CLIENT
Fichier : `03_posts_reseaux/app_client/POSTS-app-client.md`

| # | Réseau | Format | Rédigé | Visuel | Relu | Programmé | Publié |
|---|--------|--------|:------:|:------:|:----:|:---------:|:------:|
| A1 | LinkedIn | Texte + visuel | ✅ | ☐ | ☐ | ☐ | ☐ |
| A2 | Facebook | Texte + visuel | ✅ | ☐ | ☐ | ☐ | ☐ |
| A3 | Instagram | Carrousel 6 slides + caption | ✅ | ☐ | ☐ | ☐ | ☐ |
| A4 | X/Twitter | Post + variante fil | ✅ | ☐ | ☐ | ☐ | ☐ |
| A5 | TikTok | Script vidéo courte | ✅ | ☐ | ☐ | ☐ | ☐ |

### Campagne B — App PRATICIEN
Fichier : `03_posts_reseaux/app_praticien/POSTS-app-praticien.md`

| # | Réseau | Format | Rédigé | Visuel | Relu | Programmé | Publié |
|---|--------|--------|:------:|:------:|:----:|:---------:|:------:|
| B1 | LinkedIn | Texte + visuel | ✅ | ☐ | ☐ | ☐ | ☐ |
| B2 | Facebook | Texte + visuel | ✅ | ☐ | ☐ | ☐ | ☐ |
| B3 | Instagram | Carrousel 6 slides + caption | ✅ | ☐ | ☐ | ☐ | ☐ |
| B4 | X/Twitter | Post + variante fil | ✅ | ☐ | ☐ | ☐ | ☐ |
| B5 | TikTok | Script vidéo courte | ✅ | ☐ | ☐ | ☐ | ☐ |

> Les check-lists détaillées par réseau (accroche, longueur, hashtags, horaires, alt-text…) sont dans `05_checklists/CHECKLISTS-par-reseau.md`.

---

## ♻️ Programme réutilisable (pour tout futur article de blog)

Le fichier `04_programme/PROGRAMME-contenu-blog-vers-reseaux.md` décrit le pipeline en 6 étapes
(Source → Angle → Atomisation → Déclinaison → Visuels → Publication), les gabarits par réseau,
le gabarit visuel, et la « Definition of Done ». **À appliquer à chaque texte publié sur le blog.**

Cycle rapide pour un nouvel article :
1. Remplir la *Fiche de production* (§2 du programme).
2. Décliner via les *gabarits par réseau* (§3).
3. Produire les visuels (générateur `gen_visuals.py`).
4. Cocher les check-lists (`05_checklists/`).
5. Programmer et publier.

---

## 🔒 Règles transverses (non négociables)
- **Sécurité** : tout contenu sensible affiche les ressources de crise (9-8-8 · 8-1-1 opt. 2 · 9-1-1 · 1 866 APPELLE 277-3553).
- **Confidentialité** : jamais de vraies données client à l'écran ; flouter noms/courriels ; données hébergées au Canada (Loi 25).
- **Ton** : posé, humain, non clinique, fr-CA. On accompagne, on ne diagnostique pas.
- **Conformité** : Loi 21 pour le vocabulaire professionnel côté praticien.

---

## 🌐 Section « Tutos » sur le site
Une page dédiée regroupe les versions texte des tutos, publiée dans le blog à `ivia.quebec/ressources/blog`.
Voir la note de déploiement dans le fichier de livraison.

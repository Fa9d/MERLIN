# Programme éditorial IVIA — Du blog aux réseaux

Procédure réutilisable pour transformer **n'importe quel contenu** (article de blog, tuto, annonce)
en un lot complet de publications multi-réseaux, de façon cohérente et rapide.

> Objectif : chaque texte publié sur `ivia.quebec/ressources/blog` doit générer,
> avec le même gabarit, une déclinaison LinkedIn, Facebook, Instagram, X et TikTok,
> plus (si pertinent) un tuto vidéo.

---

## 0. Principes de marque (à respecter partout)

- **Ton** : posé, humain, non clinique. On accompagne, on ne diagnostique pas. Jamais de promesse de guérison.
- **Langue** : français québécois, `fr-CA`. Vouvoiement.
- **Vocabulaire IVIA** : « présence accompagnée », « littératie du vivant », « s'ancrer », « repères », « ligne de vie ». Éviter le jargon psy.
- **Sécurité** : tout contenu touchant la détresse/le suicide inclut les ressources d'aide (1 866 APPELLE / 277-3553, texto 535353, suicide.ca, 988, 911).
- **Sobriété visuelle** : thème sombre #0d1117, accent vert #3ecf8e, titres DM Serif Display, corps DM Sans.
- **Pas de sur-promesse, pas d'alarmisme, pas d'exploitation de la vulnérabilité.**

---

## 1. Le pipeline en 6 étapes

| # | Étape | Livrable | Qui/Comment |
|---|---|---|---|
| 1 | **Source** | 1 article publié sur le blog | Rédaction + sources vérifiées |
| 2 | **Angle** | 1 phrase = le message central | « Que doit retenir la personne ? » |
| 3 | **Atomisation** | 3-5 « pépites » (stat, citation, conseil, question) | Extraire du corps de l'article |
| 4 | **Déclinaison** | 1 post par réseau (5 réseaux) | Gabarits §3 |
| 5 | **Visuels** | 1 visuel citation + 1 carrousel (option) | Gabarit visuel §4 |
| 6 | **Publication** | Posts programmés + check-list cochée | Check-lists §5 |

---

## 2. Fiche de production (à remplir pour chaque contenu)

```
TITRE DE L'ARTICLE :
URL BLOG :
ANGLE (1 phrase) :
PUBLIC VISÉ : ☐ Personne qui cherche de l'aide  ☐ Proche  ☐ Praticien  ☐ Employeur  ☐ Grand public
PÉPITES :
  1. (stat ou fait)
  2. (citation forte)
  3. (conseil actionnable)
  4. (question qui ouvre)
CTA PRINCIPAL : ☐ Lire l'article  ☐ Réserver  ☐ Découvrir IVIA  ☐ Partager
RESSOURCES D'AIDE À INCLURE ? ☐ Oui ☐ Non
HASHTAGS DE BASE : #IVIA #SantéMentale #Québec #LittératieDuVivant
```

---

## 3. Gabarits par réseau

### LinkedIn (autorité, professionnel, praticiens/employeurs)
- **Longueur** : 900-1 500 caractères. Accroche forte sur la 1re ligne (avant le « …voir plus »).
- **Structure** : Accroche → contexte (1 stat) → 2-3 idées en liste → réflexion → CTA + lien.
- **Style** : phrases courtes, retours à la ligne aérés, 3-5 hashtags en fin.
- **Émojis** : sobres (▪️, →), max 3.

### Facebook (communauté, proches, grand public)
- **Longueur** : 400-800 caractères. Ton chaleureux, direct.
- **Structure** : Question/accroche empathique → 1 idée clé → invitation douce → lien.
- **Style** : conversationnel, on parle « à » quelqu'un. Lien en clair.
- **Hashtags** : 2-3 max.

### Instagram (visuel d'abord, caption en soutien)
- **Format** : carrousel 1080×1080 (4-6 slides) OU visuel citation unique.
- **Caption** : 300-600 caractères. Accroche → développement → CTA « Lien en bio ».
- **Hashtags** : 8-15, en fin ou 1er commentaire. Mix large + niche (#santémentaleQC).
- **Règle** : le message DOIT tenir dans le visuel, la caption complète.

### X / Twitter (concision, fil possible)
- **Longueur** : 1 post ≤ 280 caractères ; ou fil (thread) de 3-5 tweets.
- **Structure** : 1 idée = 1 tweet. Accroche chiffrée. Lien dans le dernier tweet.
- **Hashtags** : 1-2 max, intégrés au texte.

### TikTok (script vidéo courte, 20-45 s)
- **Format** : script parlé, hook dans les 2 premières secondes.
- **Structure** : Hook (« Saviez-vous que… ») → 1 idée développée → 1 conseil → CTA (« Plus de repères en bio »).
- **Style** : oral, rythmé, une seule idée. Texte à l'écran = mots-clés.
- **Caption** : courte + 3-5 hashtags (#santémentale #québec #bienetre).

---

## 4. Gabarit visuel (citation + carrousel)

**Visuel citation (1080×1080)**
- Fond #0d1117, accent #3ecf8e. Titre/citation en DM Serif Display (blanc), attribution/source en DM Sans (gris #96a0ac). Logo IVIA discret.

**Carrousel (4-6 slides, 1080×1080)**
1. Slide titre = l'angle
2-4. Une pépite par slide
5. Récap / message
6. CTA (« Lire l'article complet — lien en bio » + logo)

> Réutiliser le générateur `gen_visuals.py` (PIL, polices de marque) déjà en place.

---

## 5. Règles d'or de publication

- **Cadence** : ne pas tout publier le même jour. Étaler LinkedIn (mardi/jeudi matin), FB/Insta (midi ou soir), X (matin), TikTok (soir).
- **Accessibilité** : texte alternatif sur chaque image ; sous-titres sur chaque vidéo.
- **Traçabilité** : chaque post lié à l'URL blog source (UTM optionnel : `?utm_source=linkedin&utm_medium=social`).
- **Cohérence** : même angle sur tous les réseaux, format adapté à chacun.
- **Sécurité** : si le sujet est sensible, ressources d'aide visibles (post + visuel).

---

## 6. Definition of Done (un contenu est « prêt »)

☐ Article publié et accessible sur le blog
☐ Fiche de production remplie
☐ 5 posts rédigés (LinkedIn, FB, Insta, X, TikTok)
☐ Visuel(s) produit(s) et vérifié(s) (pas de texte coupé)
☐ Ressources d'aide incluses si sujet sensible
☐ Check-list par réseau cochée (voir `05_checklists/`)
☐ Posts programmés / publiés
☐ Liens et UTM vérifiés

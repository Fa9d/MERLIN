# IVIA — Spécification fonctionnelle : Page publique `/praticiens`
**Version :** 1.0  
**Statut :** Brouillon de référence — pilote  
**Auteur :** Équipe stratégique IVIA  
**Date :** 2025  
**Devises :** *Au sein de l'être — En actes.* / *Pour le peuple, par le peuple.*

---

## Table des matières

1. [Objectifs de la page](#1-objectifs-de-la-page)  
2. [Wireframe textuel détaillé](#2-wireframe-textuel-détaillé)  
3. [Critères de listing](#3-critères-de-listing)  
4. [Conformité Loi 25](#4-conformité-loi-25)  
5. [Évolutivité par phases](#5-évolutivité-par-phases)  
6. [Anti-patterns explicitement refusés](#6-anti-patterns-explicitement-refusés)  
7. [Sources de référence](#7-sources-de-référence)

---

## 1. Objectifs de la page

### 1.1 Incarner la doctrine « valeur avant extraction »

La page `/praticiens` est la première surface de confiance qu'une personne en démarche touche avant de prendre toute décision d'engagement. Elle doit livrer une valeur informationnelle réelle et complète sans exiger la moindre donnée personnelle en échange — ni courriel, ni numéro de téléphone, ni création de compte. La doctrine IVIA pose que l'information sur les praticiens est un bien public de la relation d'aide, non un actif à monétiser par l'accès. Le fait de connaître le nom (partiel), le parcours, la philosophie, les voies d'entrée et le tarif d'un praticien avant tout engagement financier n'est pas une concession commerciale : c'est le minimum éthique d'une plateforme qui se réclame du peuple.

Cette page traduit en actes la promesse que la personne accompagnée choisit librement et en connaissance de cause. Elle ne découvre pas son praticien une fois la carte de crédit saisie. Elle le connaît d'abord, décide ensuite. L'ordre de ces deux gestes n'est pas anodin — il fonde l'alliance thérapeutique non-clinique avant même le premier contact.

### 1.2 Différenciateur structurel vis-à-vis des plateformes dominantes

Les plateformes comme BetterHelp et Talkspace ont construit leur modèle sur l'opacité des profils praticiens jusqu'à l'inscription complète, parfois jusqu'au premier paiement. Le praticien y est traité comme un bien de catalogue que la plateforme sélectionne algorithmiquement, souvent selon des critères de rentabilité plutôt que d'adéquation réelle. Le client est assigné. IVIA refuse ce modèle dans sa totalité.

La page `/praticiens` d'IVIA est à l'opposé : chaque profil est lisible, chaque voie d'entrée est expliquée, chaque tarif est affiché sans ambiguïté, et la personne navigue à son propre rythme sans friction d'inscription. Ce différenciateur n'est pas un argument marketing — c'est une position éthique inscrite dans l'architecture de l'information. Il est non-négociable et ne pourra jamais être revu à la baisse pour des raisons de conversion.

### 1.3 Référence : le modèle Grow Therapy comme exemple positif

[Grow Therapy](https://www.growtherapy.com) offre un exemple de pratique sectorielle où les profils de thérapeutes — incluant photo, spécialités, tarifs et disponibilités — sont visibles publiquement avant toute inscription. Ce choix de conception témoigne qu'il est techniquement et commercialement viable de respecter l'agentivité du client dès la première visite. IVIA s'appuie sur ce précédent pour valider que la transparence radicale des profils n'est pas un obstacle à la croissance d'une plateforme, mais en est au contraire un fondement de crédibilité.

De même, [Sesame Care](https://www.sesamecare.com) pratique l'affichage public de tarifs sans abonnement obligatoire, démontrant que la sobriété tarifaire et la lisibilité des prix sont compatibles avec la viabilité économique d'un modèle d'accompagnement. IVIA tire de ces deux références la confirmation que ses choix architecturaux sont défendables et reproductibles.

### 1.4 Permettre au client de choisir, pas d'être assigné

Le verbe « choisir » est central à la doctrine IVIA. La personne qui consulte `/praticiens` doit pouvoir parcourir, filtrer, comparer, lire, revenir, hésiter et décider à son propre rythme. Aucun mécanisme de page ne doit simuler l'urgence, orienter subtilement vers un praticien en particulier pour des raisons commerciales, ou réduire la capacité d'arbitrage de la personne. Le tri par défaut est aléatoire et stable par session. Les filtres sont des outils de précision au service du client, pas des entonnoirs de conversion.

---

## 2. Wireframe textuel détaillé

> **Convention de lecture :** Les blocs sont présentés dans l'ordre d'affichage vertical. Les champs obligatoires sont marqués `[OBL]`. Les champs optionnels au praticien sont marqués `[OPT]`. Les CTA (appels à l'action) sont en majuscules entre crochets.

---

### 2.1 En-tête de page (Header)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  IVIA — navigation globale (logo + liens principaux)                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Nos praticiens                                                         │
│  ──────────────────────────────────────────────────────────────        │
│  Choisissez. Vous n'êtes pas assignée ou assigné.                       │
│                                                                         │
│  Sous-texte (corps, 16px) :                                             │
│  « Chaque profil est lisible sans compte, sans inscription.             │
│    Prenez le temps qu'il vous faut. »                                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Spécifications typographiques :**
- Titre H1 : « Nos praticiens » — taille 36px, poids 600, couleur principale IVIA
- Sous-titre H2 : « Choisissez. Vous n'êtes pas assignée ou assigné. » — taille 22px, poids 400, italique léger
- Sous-texte : corps régulier, 16px, couleur secondaire, max-width 640px centré

---

### 2.2 Bloc de filtres

Le bloc de filtres se situe immédiatement sous le header, en position `sticky` sur desktop (reste visible au défilement). Sur mobile, il se replie en un bouton « Affiner la recherche » qui ouvre un tiroir (drawer) latéral.

#### Filtre 1 — Voie d'entrée (sélection unique ou multiple)

| Valeur affichée | Identifiant interne |
|---|---|
| Ancrage corporel | `voie_corps` |
| Parole et récit | `voie_parole` |
| Pratiques contemplatives | `voie_contemplation` |
| Accompagnement par les savoirs autochtones | `voie_autochtone` |

> Note : Les libellés sont issus de la taxonomie doctrinale IVIA. Ils ne correspondent pas à des actes cliniques réservés.

#### Filtre 2 — Mode d'écoute (sélection unique ou multiple)

| Valeur affichée | Identifiant interne |
|---|---|
| Directif bienveillant | `mode_directif` |
| Non-directif — la parole vous appartient | `mode_non_directif` |
| Miroir actif | `mode_miroir` |
| Ancrage dans le présent | `mode_ancrage` |
| Co-construction narrative | `mode_recit` |

#### Filtre 3 — Langue(s) d'accompagnement (sélection multiple)

| Valeur affichée | Code |
|---|---|
| Français | `fr` |
| Anglais | `en` |
| Innu-aimun | `moe` |
| Atikamekw | `atj` |
| Kanien'kéha (mohawk) | `moh` |
| Anishinaabemowin (ojibwé) | `ojw` |
| Autre (précisé sur profil) | `autre` |

> Les langues autochtones sont affichées avec leur nom d'origine en premier, suivi du nom français entre parenthèses. Aucune hiérarchie visuelle ne place le français ou l'anglais avant les autres langues dans le filtre.

#### Filtre 4 — Disponibilité

| Valeur affichée | Identifiant interne |
|---|---|
| Cette semaine | `dispo_semaine` |
| Dans les 2 prochaines semaines | `dispo_2sem` |
| Flexible — je m'adapte | `dispo_flexible` |

#### Filtre 5 — Modalité

| Valeur affichée | Identifiant interne |
|---|---|
| En personne — Montréal | `modal_presentiel_mtl` |
| Virtuel (vidéo sécurisée) | `modal_virtuel` |
| Hybride (les deux) | `modal_hybride` |

**Comportement des filtres :**
- Chaque filtre est indépendant. L'activation de plusieurs filtres fonctionne en logique `ET` (intersection).
- Un bouton « Réinitialiser les filtres » est visible dès qu'au moins un filtre est actif.
- Le nombre de praticiens correspondants est affiché en temps réel sous le bloc de filtres : « 3 praticiens correspondent à votre recherche. »
- En cas de résultat zéro : afficher le message « Aucun praticien ne correspond exactement à ces critères pour le moment. Vous pouvez élargir vos filtres ou nous écrire — nous vous répondrons dans les 48 heures. [NOUS ÉCRIRE] »

---

### 2.3 Grille de cartes praticien

**Disposition :**
- Desktop (> 1024px) : 3 colonnes
- Tablette (768–1023px) : 2 colonnes
- Mobile (< 768px) : 1 colonne
- Espacement entre cartes : 24px
- Tri par défaut : aléatoire, stable par session (seed basé sur identifiant de session anonyme, pas d'empreinte)

---

#### Structure d'une carte praticien

```
┌──────────────────────────────────────────────────┐
│  [PHOTO]                                         │
│  140×140 px, format carré arrondi                │
│  Alt text : « Portrait de [Prénom] »             │
│                                                  │
│  Prénom + Initiale nom  [OBL]                    │
│  ex. : Mariève T.                                │
│                                                  │
│  Pronom(s)  [OBL]                                │
│  ex. : elle / her  |  iel / them                 │
│                                                  │
│  Formation déclarée (court)  [OBL]               │
│  ex. : Diplômée en travail social (UQAM, 2018)   │
│         Cert. Somatic Experiencing (2021)        │
│                                                  │
│  ──────────────────────────────────────────────  │
│  Voies d'entrée pratiquées  [OBL]                │
│  ○ Ancrage corporel  ○ Parole et récit           │
│                                                  │
│  Mode d'écoute revendiqué  [OBL]                 │
│  « Non-directif — la parole vous appartient »   │
│                                                  │
│  Langues  [OBL]                                  │
│  Français · Innu-aimun                           │
│                                                  │
│  ──────────────────────────────────────────────  │
│  Tarif  [OBL]                                    │
│  80 $ CAD / 60 min (tarif pilote unique)         │
│                                                  │
│  Prochaines disponibilités  [OBL]                │
│  Mer. 14 jan. — 10 h 00                          │
│  Jeu. 15 jan. — 14 h 30                          │
│  Ven. 16 jan. — 9 h 00                           │
│  (Affichage de 3 à 5 créneaux maximum)           │
│                                                  │
│  Badges qualitatifs  [OPT]                       │
│  [ Souvent rebookée ] [ Travaille avec ados ]    │
│                                                  │
│  ──────────────────────────────────────────────  │
│  [VOIR LE PROFIL COMPLET]   [RÉSERVER]           │
└──────────────────────────────────────────────────┘
```

**Spécifications des champs de la carte :**

- **Photo `[OBL]`** : fournie par le praticien, consentement écrit dans le contrat praticien. Format JPG/WebP, dimensions 400×400 px minimum, optimisé. Si photo absente : placeholder sobre avec initiale du prénom sur fond neutre, jamais de silhouette générique.
- **Prénom + Initiale nom `[OBL]`** : anonymat partiel jusqu'au premier RDV confirmé. Le nom complet est transmis uniquement dans la confirmation de réservation, dans un canal sécurisé, après consentement mutuel.
- **Pronom(s) `[OBL]`** : affiché tel que déclaré par le praticien. Aucune validation normative. Accepte les pronoms non-binaires et les doubles pronoms.
- **Formation déclarée `[OBL]`** : déclaration libre, vérifiée par IVIA selon la procédure de vérification (cf. section 2.4.4). Pas de validation par ordre professionnel — IVIA n'est pas une plateforme clinique.
- **Voies d'entrée `[OBL]`** : 1 à 4 options issues de la taxonomie.
- **Mode d'écoute `[OBL]`** : 1 seul mode principal revendiqué, affiché en italique ou entre guillemets pour signaler que c'est la voix du praticien.
- **Langues `[OBL]`** : liste séparée par des points médians (·).
- **Tarif `[OBL]`** : tarif fixe pilote. Libellé exact : « 80 $ CAD / 60 min (tarif pilote unique) ». Aucune variation tarifaire n'est affichée sur la carte en V1.
- **Prochaines disponibilités `[OBL]`** : 3 à 5 créneaux. Format : Jour abrégé. JJ mois — HH h MM. Fuseau horaire : heure de l'Est (HNE/HAE). Si aucune disponibilité dans les 14 jours : afficher « Aucune disponibilité dans les 2 prochaines semaines — [REJOINDRE LA LISTE D'ATTENTE] ».
- **Badges qualitatifs `[OPT]`** : 0 à 3 badges par praticien. Liste autorisée définie par IVIA (cf. section 6.2).
- **CTA « Voir le profil complet » `[OBL]`** : bouton secondaire (contour). Ouvre la page profil détaillé (cf. section 2.4).
- **CTA « Réserver » `[OBL]`** : bouton primaire. Redirige vers le calendrier de réservation du praticien (intégration Cal.com ou équivalent souverain). Ne nécessite pas de compte IVIA au préalable — la création de compte peut survenir au moment de la réservation.

---

### 2.4 Page profil détaillé

La page profil est accessible via le bouton « Voir le profil complet » ou par URL directe `/praticiens/[slug-prenom-initiale]`. Elle est indexable par les moteurs de recherche. Aucun mur d'authentification.

---

#### 2.4.1 En-tête du profil

```
┌─────────────────────────────────────────────────────────────────────────┐
│  [PHOTO AGRANDIE]  200×200 px                                           │
│                                                                         │
│  Prénom + Initiale nom                                                  │
│  Pronom(s)                                                              │
│  Formation principale (1 ligne)                                         │
│  Voies d'entrée : [tags]                                                │
│  Langues : [tags]                                                       │
│  Modalité : [Virtuel / En personne Montréal / Hybride]                  │
│                                                                         │
│  Tarif : 80 $ CAD / 60 min (tarif pilote unique)                        │
│                                                                         │
│  [RÉSERVER UNE SÉANCE]   (ancre vers calendrier en bas de page)        │
└─────────────────────────────────────────────────────────────────────────┘
```

---

#### 2.4.2 Bio longue (300–500 mots)

**Gabarit rédactionnel recommandé au praticien :**

1. Qui êtes-vous avant d'être praticien ? (contexte humain, pas curriculum)
2. Qu'est-ce qui vous a amené à cet accompagnement ?
3. Comment décririez-vous votre façon d'être en séance ?
4. Avec quels types de situations ou de personnes travaillez-vous particulièrement ?
5. Ce que vous ne faites pas (limites claires — ancrage éthique)

**Formatage :**
- Texte en première personne du singulier, voix du praticien.
- Maximum 5 paragraphes. Pas de listes à puces dans la bio — la fluidité du récit prime.
- Un chapeau éditorial d'une phrase peut précéder la bio, rédigé par IVIA et approuvé par le praticien.

---

#### 2.4.3 Parcours et certifications

```
Parcours et formations

• [Diplôme / Certification] — [Institution] — [Année]
• [Diplôme / Certification] — [Institution] — [Année]
• ...

Note : Les formations déclarées ont été vérifiées par IVIA selon le processus
décrit ci-dessous. IVIA n'est pas un ordre professionnel. Ces formations
ne constituent pas des actes cliniques réservés.
```

---

#### 2.4.4 Déclaration éthique signée par le praticien

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Déclaration éthique                                                    │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  [Texte de la déclaration éthique personnelle du praticien,             │
│   rédigée librement dans un gabarit fourni par IVIA.                    │
│   Contenu minimal attendu :                                             │
│   — Ce que je fais.                                                     │
│   — Ce que je ne fais pas (limites non-cliniques).                      │
│   — Ce que je ferai si je perçois une situation de détresse aiguë.     │
│   — Mon engagement de confidentialité.]                                  │
│                                                                         │
│  Signée le [date] par [Prénom + Initiale nom]                           │
│  Politique complète : voir « Politique de bien-être des praticiens »    │
└─────────────────────────────────────────────────────────────────────────┘
```

Cette section est liée au document `politique_bien_etre_praticiens` existant dans le dépôt IVIA. La signature est celle du contrat numérique — elle n'est pas une signature manuscrite numérisée.

---

#### 2.4.5 Témoignages anonymisés (3 à 5)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Ce que des personnes accompagnées ont partagé                          │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  « [Témoignage, 50–150 mots, première personne.] »                      │
│  — Personne accompagnée, [mois et année], voie [ancrage corporel...]    │
│                                                                         │
│  « [Témoignage] »                                                       │
│  — Personne accompagnée, [mois et année], voie [parole et récit...]     │
│                                                                         │
│  ...                                                                    │
└─────────────────────────────────────────────────────────────────────────┘
```

**Règles des témoignages :**
- Recueillis après consentement écrit de la personne accompagnée via formulaire IVIA.
- Anonymisés : aucun prénom, aucune information permettant l'identification.
- Non modifiés dans le fond — des corrections typographiques mineures sont permises avec accord de l'auteur.
- La date et la voie d'entrée sont conservées pour contextualiser sans identifier.
- Pilote V1 : si moins de 3 témoignages disponibles, la section est absente plutôt qu'affichée vide ou partiellement.

---

#### 2.4.6 Encart « Comment IVIA a vérifié ce praticien »

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Comment IVIA a vérifié ce praticien                                    │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  Étape 1 — Vérification documentaire                                    │
│  IVIA a demandé et conservé copie des diplômes et certifications        │
│  déclarés. Les documents sont vérifiés en amont de toute publication.   │
│                                                                         │
│  Étape 2 — Entretien de cadrage éthique                                 │
│  Un entretien structuré d'environ 60 minutes a été conduit par          │
│  l'équipe IVIA pour vérifier la compréhension des limites non-          │
│  cliniques, la doctrine d'accompagnement et la politique de             │
│  bien-être des praticiens.                                              │
│                                                                         │
│  Étape 3 — Signature du contrat et de la déclaration éthique           │
│  Le praticien a signé le contrat type IVIA et sa déclaration            │
│  éthique personnelle. Ces documents sont conservés par IVIA             │
│  conformément à la Loi 25 et ne sont pas rendus publics.               │
│                                                                         │
│  Note : IVIA n'est pas un ordre professionnel et ne délivre             │
│  pas d'agrément clinique. Ces vérifications garantissent                │
│  l'intégrité doctrinale et éthique, pas une accréditation              │
│  réglementée.                                                           │
└─────────────────────────────────────────────────────────────────────────┘
```

---

#### 2.4.7 Calendrier de réservation (ancre bas de page)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Réserver une séance avec [Prénom + Initiale]                           │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  [Interface calendrier intégrée — Cal.com ou équivalent souverain]      │
│  Affichage des disponibilités sur 4 semaines                            │
│                                                                         │
│  Tarif : 80 $ CAD / 60 min (tarif pilote unique)                        │
│  Paiement : au moment de la confirmation, via Stripe ou équivalent.     │
│  Annulation gratuite jusqu'à 24 h avant la séance.                      │
│                                                                         │
│  [CHOISIR UN CRÉNEAU]                                                   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### 2.5 Message de contexte en pied de page de liste

En bas de la liste `/praticiens`, avant le pied de page global :

```
IVIA accompagne, elle ne traite pas.

Les praticiens IVIA offrent un accompagnement non-clinique. Si vous
traversez une crise, appelez le 1 866 APPELLE (277-3553) — ligne
d'intervention de crise disponible 24 h / 24, 7 j / 7 au Québec.

Pour toute question sur notre approche : /comment-ca-fonctionne
```

---

## 3. Critères de listing

### 3.1 Qui apparaît

Un praticien est visible sur `/praticiens` si et seulement si toutes les conditions suivantes sont remplies simultanément :

| Condition | Vérification |
|---|---|
| Contrat IVIA actif et en règle | Signé, non résilié, non suspendu |
| Déclaration éthique complétée et signée | Intégrée au dossier praticien |
| Formation(s) déclarée(s) vérifiée(s) | Étape 1 du processus de vérification franchie |
| Entretien de cadrage éthique complété | Étape 2 franchie |
| Photo fournie (ou placeholder validé) | Consentement photo signé dans le contrat |
| Disponibilités renseignées dans le calendrier | Au moins 1 créneau dans les 30 prochains jours |
| Profil complet publié | Champs obligatoires tous renseignés |

### 3.2 Qui n'apparaît pas

Un praticien est retiré ou masqué de la liste dans les cas suivants :

| Situation | Traitement |
|---|---|
| Vacances / indisponibilité temporaire déclarée | Masquage temporaire — réapparaît automatiquement à la date de retour |
| Surcharge déclarée (plus de créneaux disponibles) | Masquage jusqu'à renseignement d'au moins 1 créneau dans les 30 j |
| Supervision en cours suite à un incident | Masquage jusqu'à levée par l'équipe IVIA |
| Résiliation ou suspension de contrat | Retrait définitif ou jusqu'à rétablissement selon procédure |
| Profil incomplet ou en cours de validation | Non publié — visible uniquement en prévisualisation interne |

### 3.3 Ordre de tri

- **Tri par défaut :** aléatoire, stable par session. Le seed est généré à partir d'un identifiant de session anonyme (non lié à l'utilisateur). Deux visites consécutives sans fermeture de navigateur donnent le même ordre. Une nouvelle session donne un ordre différent.
- **Tri alternatif disponible :** « Par disponibilité immédiate » — les praticiens ayant un créneau dans les 48 heures apparaissent en premier.
- **Ce qui est interdit** : tout tri favorisant un praticien en raison d'un paiement, d'un taux de conversion supérieur, ou d'une relation commerciale avec IVIA. Ce principe est non-négociable et doit être documenté dans le code source sous forme de commentaire explicite.

---

## 4. Conformité Loi 25

### 4.1 Données des praticiens sur la page publique

La photo, le prénom, l'initiale du nom, les pronoms, la bio, la déclaration éthique et les formations des praticiens sont des données personnelles au sens de la Loi 25. Leur publication est encadrée comme suit :

- **Consentement explicite :** Le contrat praticien type IVIA comporte une clause de consentement à la publication des données listées ci-dessus. Le praticien signe cette clause séparément, avec la possibilité de restreindre certains éléments (ex. : choisir un pseudonyme, ne pas publier la ville de résidence).
- **Droit de retrait :** Le praticien peut demander la dépublication de tout ou partie de son profil en tout temps, avec effet dans les 48 heures.
- **Pas de publication sans consentement :** Aucun profil partiel ou anonyme n'est publié sans signature du contrat et de la clause de consentement.

### 4.2 Données des visiteurs de la page

La page `/praticiens` ne collecte aucune donnée personnelle sur le visiteur pour être consultée. Spécifiquement :

| Pratique | Statut |
|---|---|
| Compte ou connexion requis | **Interdit en V1, V2 et V3** |
| Courriel ou numéro de téléphone requis | **Interdit** |
| Cookie d'identification | **Interdit** — seul un cookie de session anonyme est permis pour le tri stable |
| Empreinte numérique (fingerprinting) | **Interdit** |
| Pixel de suivi tiers (Meta, Google Ads, etc.) | **Interdit** sur cette page |

### 4.3 Compteur de vues

Un compteur de vues est maintenu côté serveur pour fins d'analyse opérationnelle (savoir quels profils sont consultés). Ce compteur est :

- **Agrégé :** il compte les vues, pas les visiteurs.
- **Anonymisé :** aucune adresse IP, aucun identifiant d'appareil, aucun identifiant de session persistant n'est associé à un comptage.
- **Non transmis à des tiers.**
- **Conservé** selon la politique de conservation des données IVIA (durée à définir en conformité avec la Loi 25, recommandation : 12 mois glissants).

### 4.4 Responsable de la conformité

Le responsable de la protection des renseignements personnels (RPRP) d'IVIA est responsable de la conformité de cette page. Toute modification au comportement de collecte de données sur `/praticiens` doit être approuvée par le RPRP avant déploiement.

---

## 5. Évolutivité par phases

### 5.1 V1 — Pilote (0 à 6 mois, 1–5 praticiens)

**Architecture :** Statique-dynamique. Les profils sont stockés en base de données, mais la page peut être générée en statique (SSG) et regénérée à chaque mise à jour de profil.

**Fonctionnalités incluses :**
- Grille de cartes avec les 5 filtres de base
- Pages profil détaillées individuelles
- Calendrier de réservation intégré
- Tri aléatoire stable par session
- Tri alternatif par disponibilité immédiate
- Message de contexte en pied de page
- Conformité Loi 25 complète

**Fonctionnalités non incluses en V1 :**
- Recherche textuelle
- Alertes disponibilité par courriel
- Algorithme de suggestion

**Recommandation doctrinale :** Ne pas attendre d'avoir 5 praticiens pour lancer la page. Avec 1 ou 2 praticiens, la page est plus honnête qu'une page vide ou un formulaire d'attente. Le pilote commence quand il commence — la transparence s'applique dès le premier profil.

### 5.2 V2 — Croissance (6 à 12 mois, 5–8 praticiens)

**Fonctionnalités ajoutées :**
- Recherche textuelle dans les bios et les formations (index côté serveur, pas de dépendance à un moteur tiers)
- Alerte disponibilité : le visiteur peut laisser une adresse courriel pour être notifié lorsqu'un praticien spécifique a un nouveau créneau. Cette donnée est soumise à consentement et gérée selon Loi 25.
- Filtres avancés : ajout possible d'un filtre par tranche d'âge de la clientèle (adolescents / adultes / aîné·e·s) si la taxonomie praticienne le supporte
- Statistiques de page enrichies (toujours anonymisées et agrégées)

### 5.3 V3 — Maturité (12 mois et plus)

**Fonctionnalités ajoutées :**
- Algorithme de suggestion explicable : à partir des filtres sélectionnés et, si la personne le souhaite, d'un court questionnaire anonyme (5 questions), IVIA propose 2–3 praticiens en expliquant pour chaque raison de la suggestion (ex. : « Ce praticien pratique la voie que vous avez sélectionnée et a une disponibilité cette semaine »).
- L'algorithme est documenté publiquement sur la page `/comment-ca-fonctionne`.
- Aucun critère commercial n'entre dans l'algorithme de suggestion — cette contrainte est inscrite dans la spécification technique de l'algorithme et auditée annuellement.
- Éventuellement : sous-pages géographiques ou communautaires si IVIA étend sa présence au-delà de Montréal.

---

## 6. Anti-patterns explicitement refusés

Cette section est normative. Aucune des pratiques listées ci-dessous ne peut être introduite dans `/praticiens` ou dans les pages profil, quelle que soit la version ou la pression commerciale.

### 6.1 Monétisation de la visibilité

- **Interdit :** tout mécanisme « profil mis en avant » ou « featured » payant où un praticien paie pour apparaître en tête de liste.
- **Interdit :** tout classement basé sur le chiffre d'affaires généré par le praticien pour IVIA.
- **Interdit :** tout algorithme non documenté favorisant un praticien pour des raisons opérationnelles ou financières.

**Pourquoi :** Ce type de mécanisme transforme la confiance du client en marchandise. IVIA ne vend pas la visibilité de ses praticiens.

### 6.2 Notation à 5 étoiles

- **Interdit :** tout système de notation numérique (étoiles, score, pourcentage de satisfaction).
- **Pourquoi :** Les systèmes d'évaluation à 5 étoiles sont réducteurs, susceptibles de biais de sélection, et créent une pression de performance incompatible avec la sobriété doctrinale IVIA.
- **Alternative autorisée :** Badges qualitatifs discrets, issus de la liste fermée suivante. Un praticien ne peut pas choisir ses propres badges — ils sont attribués par IVIA sur la base d'observations objectives.

| Badge | Critère d'attribution |
|---|---|
| Souvent rebookée / rebooké | Taux de rebooking > 70 % sur 3 mois glissants |
| Travaille avec adolescents | Bio et déclaration éthique mentionnent explicitement ce public |
| Spécialité deuil | Bio et formation mentionnent l'accompagnement du deuil |
| Pratique bilingue | Accompagnement documenté en FR et EN |
| Accompagnement en langue autochtone | Langue autochtone vérifiée dans le contrat |
| Disponible rapidement | Créneau dans les 48 h au moment de l'affichage |

### 6.3 Fausses urgences et manipulations comportementales

- **Interdit :** chronomètre « encore X places ce mois-ci » ou toute variante de rareté artificielle.
- **Interdit :** notification du type « Quelqu'un vient de réserver avec [Prénom] ».
- **Interdit :** pop-up de sortie de page proposant une réduction ou une offre spéciale.
- **Interdit :** barre de progression « Votre profil est complété à 80 % — finissez votre inscription » sur une page publique non connectée.
- **Interdit :** compteur de vues visible par le visiteur sur un profil (utilisé uniquement en interne).

**Pourquoi :** Ces mécanismes, documentés dans la littérature sur les dark patterns de santé mentale numérique, exploitent la vulnérabilité de personnes en démarche d'aide. Ils sont incompatibles avec la doctrine IVIA.

### 6.4 Profilage et extraction de données

- **Interdit :** tout quiz ou questionnaire obligatoire avant l'accès aux profils.
- **Interdit :** demande de courriel pour « voir les disponibilités complètes ».
- **Interdit :** mur de contenu flou (blur) sur les photos ou les bios pour inciter à l'inscription.

---

## 7. Sources de référence

Les pratiques décrites dans cette spécification s'appuient sur les précédents suivants, consultés à des fins d'analyse comparative :

- [Grow Therapy](https://www.growtherapy.com) — Plateforme américaine de mise en relation avec des thérapeutes pratiquant la transparence des profils, des tarifs et des disponibilités avant inscription. Exemple de pratique positive retenu par IVIA comme référence de conception.
- [Sesame Care](https://www.sesamecare.com) — Plateforme de soins de santé américaine affichant publiquement les tarifs des praticiens sans abonnement préalable. Référence de sobriété tarifaire et de lisibilité des prix.

Ces sources sont citées à titre de référence de l'état de l'art sectoriel. IVIA ne s'associe pas commercialement à ces plateformes et ne reproduit pas leurs modèles en totalité — elle en retient les principes éthiques de transparence qu'elle juge compatibles avec sa doctrine.

---

## Notes de déploiement

- **Slug URL :** `/praticiens` (pluriel, sans accent, en français)
- **Pages profil individuelles :** `/praticiens/[prenom-initiale-nom]` (ex. : `/praticiens/marieve-t`)
- **Indexation moteurs :** `robots.txt` autorisé, `sitemap.xml` inclut toutes les pages profil actives
- **Méta-description page liste :** « Découvrez les praticiens IVIA. Choisissez avant de vous engager — profils, voies d'entrée, langues et disponibilités, sans compte requis. »
- **Méta-description page profil :** Générée dynamiquement à partir des deux premières phrases de la bio du praticien.
- **Open Graph :** Photo du praticien + prénom + spécialité principale pour le partage sur les réseaux. Consentement au partage OG inclus dans le contrat praticien.

---

*Au sein de l'être — En actes.*  
*Pour le peuple, par le peuple.*

---

**Fin du document — IVIA_SPEC_PAGE_PRATICIENS_v1.0**

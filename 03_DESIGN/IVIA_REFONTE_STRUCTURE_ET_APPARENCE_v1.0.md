# IVIA — Refonte structure & apparence (v1.0 — à valider)

**Date** : 2026-06-24
**Statut** : proposition à valider AVANT toute implémentation.
**Décisions déjà prises** (toi) :
1. **Cartographie d'abord**, code ensuite.
2. **Enregistrement solo** : *1er dépôt gratuit, puis payant* (offre « enr + rappel 10 min · 35 $ », paiement **avant** d'enregistrer).
3. **On refait aussi l'apparence**, pas seulement les parcours.

> Phrase directrice : **IVIA accueille. MERLIN structure. MÉSANGES accompagne.**
> Tout ce qui suit doit se relire à travers les **4 voies** : accueil/écoute · lecture multidimensionnelle · mise en lien · suivi/équilibre.

---

## 1. La carte du RÉEL — ce qui existe, et pourquoi c'est confus

**Inventaire** : 14 pages publiques · 17 pages espace client · 18 pages praticien/admin · 2 pages admin séparées. ≈ 51 pages.

### Les incohérences qui te perdent (constatées dans le code)

| # | Problème | Preuve concrète |
|---|----------|-----------------|
| 1 | **Même action, deux entrées dissemblables** | `/client/enregistrement.html` = gratuit (bouton « Séance express » de l'espace) **vs** `/client/enregistrement.html?formule=solo30` = payant 35 $ (« Commencer → » de l'accueil). Même page, deux noms, deux prix, deux résultats. |
| 2 | **Réservation en double** | `reserver.html` **et** `rendez-vous.html` — deux pages « Réserver une séance ». |
| 3 | **Entrée de compte éclatée** | 5 pages pour « avoir un compte » : `inscription`, `activer` (magic link), `connexion`, `verify-email`, `confirmation`. On ne sait pas laquelle est la bonne porte. |
| 4 | **4 pages « séance » côté client** | `seances` (liste), `seance` (une séance), `seance-active` (en cours), `seance-express-join` (lien express). Frontières floues. |
| 5 | **3 pages « mes sorties » qui se chevauchent** | `mes-enregistrements` (voix solo), `mes-resumes` (résumés séance), `audio-resume` (résumé audio). On ne sait pas où retrouver quoi. |
| 6 | **Cluster « Voir » redondant** | `carte-de-vie`, `ma-progression`, `premier-ancrage` — trois pages d'une même idée. |
| 7 | **Vocabulaire qui ne guide pas** | Nav client = *Aujourd'hui / Parler / Écrire / Voir*. Mais « Parler » → **séances** (réserver), pas l'enregistrement, qui est caché derrière « Séance express ». Rien ne dit « où je dépose ma voix ». |
| 8 | **Pas de fil conducteur** | Le magic link dépose dans l'espace sans « voici ce que tu peux faire maintenant / l'étape d'avant / d'après ». |
| 9 | **Admin dédoublé** | pages `praticien/admin-*` **et** dossier `admin/` (index + connexion) séparés. |
| 10 | **Socle technique incohérent** | La prod mélange plusieurs époques de design (divergence Git) → une page suit une logique, la suivante une autre. Défaut visible : titre de `client/seance-active.html` en **mojibake** (`SÃ©ance`). |

---

## 2. La structure CIBLE — une seule grammaire

**Principe** : les **mêmes 4 actions**, nommées pareil, du public à l'espace connecté. À chaque écran : *où je suis · ce que je viens de faire · l'étape suivante.*

### Les 4 actions (la grammaire unique)

| Action | Verbe IVIA | Ce que c'est | Voie doctrine |
|--------|-----------|--------------|---------------|
| **Déposer ma voix** | *Déposer* | Enregistrement solo, asynchrone (1er gratuit, puis 35 $) | accueil/écoute |
| **Rencontrer** | *Rencontrer* | Séance live avec un·e praticien·ne (réservation) | mise en lien |
| **Écrire** | *Écrire* | Journal | suivi/équilibre |
| **Voir** | *Voir* | Carte de vie / lecture multidimensionnelle | lecture multidim. |
| *(+ Compte)* | — | Profil, sécurité, facturation | — |

### Espace client — nav cible (remplace les 4 verbes actuels)
`Accueil` · **Déposer** · **Rencontrer** · **Écrire** · **Voir** · `Compte`
→ Une entrée par action, un libellé, un prix. Plus de « Séance express » fantôme.

### Plan de consolidation des pages (fusionner / renommer / retirer)

| Aujourd'hui | Cible |
|-------------|-------|
| `enregistrement` + bouton « Séance express » + « Commencer → » accueil | **1 entrée « Déposer ma voix »** (`enregistrement.html`), 1er gratuit puis paiement |
| `mes-enregistrements` + `audio-resume` | **1 page « Mes dépôts »** (voix + transcription) |
| `reserver` + `rendez-vous` | **1 page « Rencontrer »** (`reserver.html`), `rendez-vous` → redirige |
| `seances` + `seance` + `seance-active` + `seance-express-join` | **« Mes rencontres »** (liste) + **1 page de séance** (états : à venir / en cours / passée) |
| `mes-resumes` | rattaché à **« Mes rencontres »** (le résumé vit dans la séance) |
| `carte-de-vie` + `ma-progression` + `premier-ancrage` | **1 espace « Voir »** (carte + progression ; ancrage = 1er pas du parcours) |
| `inscription` + `activer` + `verify-email` + `confirmation` | **1 parcours d'entrée** clair (magic link prioritaire) ; les autres = étapes internes, pas des portes |
| `admin/` (dossier) + `praticien/admin-*` | **1 console admin** cohérente |

---

## 3. Les parcours CIBLES (avec fil conducteur)

**A — Première fois (depuis l'accueil)**
`Accueil` → « **Essayez — votre 1er dépôt est offert** » → *Déposer ma voix (gratuit)* → à la fin : « créez votre espace pour relire » → *compte (magic link)* → **Accueil de l'espace** avec « voici ce que vous pouvez faire ».

**B — Déposer sa voix (dans l'espace)**
*Déposer* → enregistrer → (si offre payante : **payer 35 $ d'abord**) → soumettre → « transcription en cours » → **Mes dépôts** (relire / partager avec un·e praticien·ne, au choix).

**C — Rencontrer un·e praticien·ne**
*Rencontrer* → choisir praticien·ne + créneau → **payer la séance** → confirmation (étape d'avant/après visible) → jour J : *séance en cours* → après : **résumé** dans la rencontre.

**D — Écrire / Voir** : entrées directes, toujours reliées (« ce dépôt nourrit votre carte », « cette séance a laissé un fil »).

Règle d'or transverse : **chaque page affiche un fil** « ⟵ d'où je viens · où je suis · étape suivante ⟶ ».

---

## 4. L'apparence — direction de refonte (à trancher)

Aujourd'hui : Tailwind CDN, palette forest/sage/cream, Lora + Raleway. Sobre mais **daté et inégal** (chaque époque a son style). La refonte recorder **Signature/Doux** (velours sombre / rosé) a montré une voie plus sensible et habitée — c'est le point de départ.

**Direction retenue (2026-06-24) : « MAISON HABITÉE »** — extension de l'ambiance *Signature* de l'enregistreur à tout le site.

| Token | Valeur |
|-------|--------|
| Fonds | velours sombre (radial `#20241c → #0c0d08`) + ivoire chaud `#F3EFE2` |
| Accents | vert IVIA `#2D6A4F` / `#4A7C59` · cuivre `#C8965A` |
| Texte | `#F3EFE2` (clair), `#A9A693` (atténué) |
| Typo | Lora (titres, serif) · Raleway (texte) |
| Registre | feutré, soir, présence, premium · mouvement lent (ondes, lumière douce) |

Point de vigilance assumé : **sombre = exigeant en lisibilité** → contrastes AA minimum, tailles généreuses, zones claires (cartes ivoire) pour les contenus longs.

**Deux ambiances pour l'espace client (2026-06-24)** : comme les maquettes de téléphone, l'interface client offre **Signature** (velours sombre, défaut) **et Doux** (prune/rosé satiné), au choix de la personne via un sélecteur d'ambiance (persisté). Mêmes tokens que `recorder-card.html` ; un seul composant, deux habillages.

| Token (Doux) | Valeur |
|-------|--------|
| Fonds | rosé satiné (radial `#f7e7e9 → #e4c9d2`) |
| Accents | vert IVIA + rosé `#c98b9b` |
| Texte | `#5b4750` / `#9a7f88` |

On pose un **vrai design system** (tokens couleur/typo/espacement + composants réutilisables) au lieu du Tailwind CDN copié-collé — c'est ce qui garantit la cohérence d'un écran à l'autre. Références vivantes : `design-system/recorder-card.html` + `design-system/espace-client-accueil.html` (Signature/Doux).

---

## 5. Séquencement proposé

1. **Réconcilier la prod** sur **une** branche propre (fin de la divergence/Frankenstein) — prérequis pour déployer sans rebricoler.
2. **Valider** cette cartographie + la direction d'apparence (ce doc).
3. **Design system** (tokens + composants) + **maquettes** des 3–4 écrans clés.
4. **Implémenter** par parcours (A, puis B, C, D), pas page par page.
5. **Déployer** uniquement par `pull-deploy.sh`, page de redirection pour les anciennes URL.

---

## 6. À trancher par toi
1. **Direction d'apparence** (voir question).
2. Le **plan de consolidation** (§2) te convient-il, ou tu veux garder certaines pages séparées ?
3. On enchaîne sur la **réconciliation prod** maintenant (§5.1) ou après la validation des maquettes ?

# IVIA — Spécification fonctionnelle : Page publique `/praticiens`

**Version** : 2.0  
**Statut** : Référence active — pilote sans visages  
**Auteur** : Équipe stratégique IVIA  
**Date** : 9 mai 2026  
**Remplace** : `IVIA_SPEC_PAGE_PRATICIENS_v1.0.md` (archivé)  
**Devises** : *Au sein de l'être — En actes.* / *Pour le peuple, par le peuple.*  
**Documents liés** : `IVIA_DOCTRINE_CARTE_ABSTRAITE_v1.0.md` · `IVIA_CHARTE_DOCTRINAIRE_v2.0.md` · `CADRE_PROPRIETE_INTELLECTUELLE_DONNEES.md` · `IVIA_FUNNEL_QUIZ_TO_GUIDANCE_v1.1.md` · `IVIA_FUNNEL_RESTITUTION_MATRICE_v1.0.md` · `CGU_PRATICIENS.md` · `IVIA_CONSENTEMENT_FUNNEL_LOI25_v1.0.md`

---

## Table des matières

1. [Préambule : pourquoi pas de visages](#1-préambule--pourquoi-pas-de-visages)
2. [Système de carte abstraite v1.0](#2-système-de-carte-abstraite-v10)
3. [Anatomie de la carte](#3-anatomie-de-la-carte)
4. [Microcopy — 3 praticiens fictifs](#4-microcopy--3-praticiens-fictifs)
5. [Accessibilité WCAG AA](#5-accessibilité-wcag-aa)
6. [Page liste /praticiens](#6-page-liste-praticiens)
7. [Page détail /praticiens/\[slug\]](#7-page-détail-praticiensslug)
8. [Cohérence avec le funnel Écran 8](#8-cohérence-avec-le-funnel-écran-8)
9. [Plan technique](#9-plan-technique)
10. [Plan accessibilité audio](#10-plan-accessibilité-audio)
11. [Tickets backlog MVP pilote](#11-tickets-backlog-mvp-pilote)
12. [Ouvertures : questions à arbitrer](#12-ouvertures--questions-à-arbitrer)

---

## 1. Préambule : pourquoi pas de visages

### 1.1 La rupture frontale

La version 1.0 de cette spécification citait [Grow Therapy](https://www.growtherapy.com) comme référence positive de transparence — profils visibles, tarifs affichés, disponibilités accessibles sans inscription. Cette référence reste valide pour ces dimensions.

Mais la v1.0 intégrait également une photo de praticien dans la structure de chaque carte. Cette décision est révoquée dans sa totalité par la version 2.0.

Sur 15 services d'accompagnement et de thérapie en ligne analysés le 9 mai 2026 (données dans `00_DOCTRINE/veille_therapie_en_ligne_15_services_20260509.csv`), 14 utilisent la photo du praticien comme élément central de la carte : [BetterHelp](https://www.betterhelp.com), [Talkspace](https://www.talkspace.com), [Grow Therapy](https://www.growtherapy.com), [Amwell](https://www.amwell.com), [Teladoc Health](https://www.teladoc.com), [Sesame Care](https://www.sesamecare.com), [Brightside Health](https://www.brightside.com), [LiveHealth Online](https://www.livehealthonline.com), [Doctor on Demand](https://www.doctorondemand.com), [MDLIVE](https://www.mdlive.com), [Regain](https://www.regain.us), [Faithful Counseling](https://www.faithfulcounseling.com), [Pride Counseling](https://www.pridecounseling.com), [Online-Therapy.com](https://www.online-therapy.com). IVIA est le seul acteur à poser l'absence de visage comme doctrine.

### 1.2 La cohérence audio

IVIA est une plateforme audio-only. La voix est le vecteur de présence. Le son, le rythme, le silence sont les données primaires de la relation. Il est philosophiquement cohérent que la représentation du praticien soit elle aussi dans le registre sensoriel, non dans le registre visuel-identificatoire.

La doctrine complète est posée dans `00_DOCTRINE/IVIA_DOCTRINE_CARTE_ABSTRAITE_v1.0.md`. La présente spécification en est la traduction fonctionnelle.

### 1.3 Ce que cette décision interdit

Dans la v2.0, les mentions suivantes sont **interdites dans tout le code source, les maquettes, les designs et les communications** concernant `/praticiens` :

- photo / portrait / image de visage / headshot
- placeholder de silhouette humaine
- avatar généré représentant un visage humain
- Open Graph avec visage du praticien (voir section 6.7)

La seule représentation visuelle du praticien autorisée est le motif organique abstrait défini dans le système de carte (section 2).

---

## 2. Système de carte abstraite v1.0

La carte abstraite du praticien comporte 8 dimensions sensorielles. Chacune est obligatoire sauf indication contraire.

### Dimension 1 — Voix `[OBL]`

**Définition** : Échantillon audio de 15 à 30 secondes, enregistré par le praticien lui-même. Le praticien lit un texte court fourni par IVIA ou improvise librement. La qualité technique est importante (casque avec micro, environnement calme, conforme à la décision `MERLIN_GOUV_DECISION_AUDIO_DANS_APP_OPERATEURS_PRATICIENS_V1.md`).

**Format technique** : Opus, mono 48 kHz, 64 kbps maximum. Taille cible : ~200 Ko par échantillon. Stockage CDN (voir section 9.3).

**Affichage** : Bouton d'écoute sobre — icône play + durée en secondes. Pas d'interface de forme d'onde visible sur la carte compacte (seulement sur le profil détaillé).

**Pour le pilote** : David Phaneuf peut prêter sa voix avec différents styles vocaux pour simuler plusieurs praticiens fictifs. Cette décision est documentée ici pour traçabilité.

**Texte de lecture standard proposé** :

> « Je m'appelle [prénom]. Quand vous parlez, j'écoute avant de répondre. Ce que vous traversez mérite du temps et de la précision. C'est ce que je peux vous offrir. »

### Dimension 2 — Fréquence dominante `[OBL]`

**Définition** : Une fréquence en Hz associée à la présence sonore et énergétique du praticien, choisie parmi une liste fermée définie par IVIA et le praticien ensemble.

**Valeurs disponibles (MVP pilote)** :

| Fréquence (Hz) | Description sensorielle affichée |
|---|---|
| 396 Hz | Libération, sol, ancrage |
| 417 Hz | Transition, changement, dépose |
| 432 Hz | Cohérence, harmonique naturelle |
| 528 Hz | Résonance, clarté intérieure |
| 639 Hz | Lien, relation, ouverture |
| 741 Hz | Expression, parole, clarification |
| 852 Hz | Intuition, présence, éveil |

**Garde-fou doctrinal obligatoire** : Aucune de ces fréquences ne peut être présentée comme ayant un effet thérapeutique démontré. La formulation autorisée est : *fréquence associée à la présence de ce praticien — description sensorielle, pas prescription*. Toute affirmation de type « guérit », « traite » ou « soigne » est interdite. Conforme au Principe 7 de la Charte doctrinaire.

**Affichage** : Le chiffre en Hz est affiché discrètement, accompagné de la description sensorielle entre parenthèses. Exemple : `528 Hz (résonance, clarté intérieure)`.

### Dimension 3 — Vibration / texture `[OBL]`

**Définition** : Une description sensorielle textuelle de 10 à 20 mots, rédigée par le praticien, décrivant la texture de sa présence en séance. Cette description utilise des métaphores sensorielles, jamais des qualificatifs cliniques.

**Exemples valides** :
- « Eau profonde, presque immobile. Quelque chose remonte à la surface sans brusquerie. »
- « Chaleur sèche, présence nette. Les mots ont du poids, les silences aussi. »
- « Sable humide sous les doigts. Dense, mais qui cède doucement. »

**Exemples invalides** :
- « Professionnel et empathique » (qualificatifs cliniques génériques)
- « Je vous aide à aller mieux » (promesse thérapeutique)
- « Expert en thérapie cognitivo-comportementale » (acte clinique réservé)

### Dimension 4 — Couleur dominante + palette secondaire `[OBL]`

**Définition** : Une couleur principale (ton, saturation, luminosité définis) et deux à trois couleurs secondaires, choisies par le praticien parmi une palette IVIA de 24 teintes.

**Usage** : La couleur dominante est le fond de la carte. La palette secondaire est utilisée pour les éléments typographiques et les détails du motif organique.

**Contrainte technique** : Contraste minimum WCAG AA (ratio 4.5:1) entre la couleur de fond et le texte superposé. Aucune dérogation.

**Exemples** :
- Praticien A : ocre profond (#8B5E3C) + sauge (#7A9E7E) + crème (#F5E6D3)
- Praticien B : bleu nuit (#1A2B4A) + argent clair (#C8D6E5) + blanc cassé (#F0F4F8)
- Praticien C : vert forêt (#2D5016) + terre cuite (#C2651A) + beige naturel (#E8DCC8)

### Dimension 5 — Motif organique / forme abstraite `[OBL]`

**Définition** : Un motif visuel généré (SVG paramétrique ou WebGL léger) ou choisi parmi une bibliothèque de motifs IVIA. Le motif occupe une portion de la carte compacte (typiquement le quart supérieur ou un angle) et la majeure partie de la carte expandée.

**Logique de génération** : Le motif est paramétré par 4 variables issues du profil du praticien : fréquence dominante (influence la fréquence des oscillations du motif), couleur dominante (teinte de base), voie d'entrée principale (influence la forme — organique sinueuse pour corps/fréquence, géométrique fractale pour connaissance/clarification), mode d'écoute (influence la densité — motif aéré pour mode silence, plus dense pour mode outils).

**Technique** : SVG inline pour le rendu statique (carte compacte). Animation WebGL légère optionnelle pour la carte expandée (profil détaillé), activable par préférence utilisateur. Respect de `prefers-reduced-motion` obligatoire.

**Bibliothèque de motifs** : 20 motifs de base disponibles pour le pilote. Voir section 9.1.

### Dimension 6 — Ambiance sonore d'ouverture `[OPT]`

**Définition** : Un son d'ambiance court (5 à 10 secondes) qui joue en boucle silencieuse par défaut et peut être déclenché par la personne. Il représente l'environnement sonore que le praticien a choisi pour ses séances — cloche tibétaine, pluie légère, silence structuré, bourdon doux.

**Format technique** : Opus, 32 kbps, taille cible < 80 Ko. Auto-play interdit. Déclenchement uniquement par action explicite de l'utilisateur.

**Affichage** : Icône son discrète à côté du bouton voix. Tooltip au survol : *Ambiance de séance*.

### Dimension 7 — Verbatim du praticien `[OBL]`

**Définition** : 3 à 5 lignes rédigées par le praticien lui-même sur sa posture d'accompagnement. Non édité par IVIA dans le fond — corrections orthographiques uniquement avec accord du praticien.

**Gabarit** : Ni biographie, ni liste de certifications. Une posture, une façon d'être en séance. À la première personne du singulier.

**Exemples** :
- « J'écoute d'abord. Je ne présume pas. Ce que vous vivez est singulier — mes outils s'y adaptent, pas l'inverse. »
- « Ma présence est ferme sans être directive. Je peux vous accompagner dans ce qui pèse sans prétendre le résoudre. »
- « Je travaille avec le corps autant qu'avec les mots. Ce qui ne se dit pas encore peut parfois se sentir d'abord. »

### Dimension 8 — Texte structuré `[OBL]`

**Définition** : Les informations textuelles classiques — formation, approche, langues, disponibilités, tarif, modalité — telles que définies dans la v1.0. Ces informations sont inchangées dans leur structure. Ce qui change : elles ne sont plus accompagnées d'une photo, elles cohabitent avec les 7 dimensions sensorielles ci-dessus.

---

## 3. Anatomie de la carte

### 3.1 Carte compacte (grille `/praticiens`)

```
┌──────────────────────────────────────────────────────────┐
│  [MOTIF ORGANIQUE ABSTRAIT — zone supérieure, ~35% haut] │
│  Couleur de fond : couleur dominante du praticien        │
│  Motif animé (si prefers-reduced-motion off)             │
│                                                          │
│  ─────────────────────────────────────────────────────── │
│  Prénom + Initiale nom  [OBL]                            │
│  ex. : Mariève T.                                        │
│                                                          │
│  Pronom(s)  [OBL]         528 Hz (résonance)  [OBL]      │
│  ex. : elle / her                                        │
│                                                          │
│  ─────────────────────────────────────────────────────── │
│  Vibration / texture  [OBL]                              │
│  « Eau profonde. Quelque chose remonte                   │
│    à la surface sans brusquerie. »                       │
│                                                          │
│  ─────────────────────────────────────────────────────── │
│  Voies d'entrée  [OBL]                                   │
│  ○ Ancrage corporel  ○ Parole et récit                   │
│                                                          │
│  Mode d'écoute  [OBL]                                    │
│  « Non-directif — la parole vous appartient »            │
│                                                          │
│  Langues  [OBL]   Formation courte  [OBL]                │
│  Français · Innu-aimun                                   │
│                                                          │
│  ─────────────────────────────────────────────────────── │
│  Tarif  [OBL]                                            │
│  80 $ CAD / 60 min (tarif pilote unique)                 │
│                                                          │
│  Prochaines disponibilités  [OBL]                        │
│  Mer. 14 jan. — 10 h 00                                  │
│  Jeu. 15 jan. — 14 h 30                                  │
│                                                          │
│  [▷ Écouter la voix — 22 s]  [♫ Ambiance]               │
│                                                          │
│  Badges qualitatifs  [OPT]                               │
│  [ Souvent rebookée ] [ Travaille avec ados ]            │
│                                                          │
│  ─────────────────────────────────────────────────────── │
│  [VOIR LE PROFIL COMPLET]        [RÉSERVER]              │
└──────────────────────────────────────────────────────────┘
```

**Spécifications typographiques :**
- Prénom + Initiale : 18px, poids 600, couleur texte contrastée sur couleur dominante
- Fréquence Hz : 13px, poids 400, couleur secondaire palette praticien
- Vibration/texture : 14px, italique, guillemets français, max 2 lignes sur carte compacte
- Mode d'écoute : 13px, guillemets français, couleur secondaire
- Tarif : 15px, poids 600
- Disponibilités : 13px, monospace ou tabular-nums

### 3.2 Pseudo-code HTML/CSS (carte compacte)

```html
<article class="card-praticien" 
         style="--couleur-dominante: #8B5E3C; --couleur-secondaire: #7A9E7E;"
         aria-label="Praticien : Mariève T. — Accompagnement corporel et récit — 528 Hz">

  <!-- Zone motif abstrait -->
  <div class="card-motif" aria-hidden="true">
    <!-- SVG inline généré selon paramètres praticien -->
    <svg viewBox="0 0 400 140" ...>...</svg>
  </div>

  <!-- Zone identité -->
  <div class="card-identite">
    <h2 class="card-prenom">Mariève T.</h2>
    <div class="card-meta-row">
      <span class="card-pronoms">elle / her</span>
      <span class="card-frequence">528 Hz <small>(résonance, clarté)</small></span>
    </div>
  </div>

  <!-- Zone sensorielle -->
  <blockquote class="card-vibration" lang="fr">
    « Eau profonde. Quelque chose remonte à la surface sans brusquerie. »
  </blockquote>

  <!-- Zone voies et mode -->
  <div class="card-voies">
    <span class="voie-tag">Ancrage corporel</span>
    <span class="voie-tag">Parole et récit</span>
  </div>
  <div class="card-mode">
    <span>Mode : </span>
    <em>« Non-directif — la parole vous appartient »</em>
  </div>

  <!-- Zone langues + formation -->
  <div class="card-info-row">
    <span class="card-langues">Français · Innu-aimun</span>
    <span class="card-formation">Trav. social (UQAM, 2018)</span>
  </div>

  <!-- Zone tarif + disponibilités -->
  <div class="card-tarif">80 $ CAD / 60 min <small>(tarif pilote unique)</small></div>
  <ul class="card-dispos" aria-label="Prochaines disponibilités">
    <li>Mer. 14 jan. — 10 h 00</li>
    <li>Jeu. 15 jan. — 14 h 30</li>
  </ul>

  <!-- Contrôles audio -->
  <div class="card-audio" role="group" aria-label="Écouter le praticien">
    <button class="btn-voix" 
            aria-label="Écouter la voix de Mariève T. — 22 secondes">
      ▷ Voix (22 s)
    </button>
    <button class="btn-ambiance" 
            aria-label="Écouter l'ambiance de séance de Mariève T.">
      ♫ Ambiance
    </button>
  </div>

  <!-- Badges -->
  <div class="card-badges" aria-label="Caractéristiques">
    <span class="badge">Souvent rebookée</span>
    <span class="badge">Travaille avec ados</span>
  </div>

  <!-- Actions -->
  <div class="card-actions">
    <a href="/praticiens/marieve-t" class="btn-secondaire">
      Voir le profil complet
    </a>
    <a href="/praticiens/marieve-t/reserver" class="btn-primaire">
      Réserver
    </a>
  </div>

</article>
```

---

## 4. Microcopy — 3 praticiens fictifs

### 4.1 Mariève T. — Voie corps, mode silence

| Dimension | Valeur |
|---|---|
| Prénom + Initiale | Mariève T. |
| Pronoms | elle / her |
| Fréquence | 528 Hz — résonance, clarté intérieure |
| Vibration/texture | « Eau profonde, presque immobile. Quelque chose remonte à la surface sans brusquerie. » |
| Couleur dominante | Bleu ardoise profond (#3D5A80) |
| Palette secondaire | Sable clair (#E0C9A6) + blanc cassé (#F4F1EB) |
| Motif | Ondes sinusoïdales lentes, horizon marin — généré paramétrique |
| Ambiance sonore | Pluie légère sur fenêtre, boucle 8 s |
| Verbatim | « J'écoute le corps avant les mots. Ce que vous portez physiquement dit souvent quelque chose que la parole n'a pas encore formulé. Je travaille dans ce espace-là — lentement, avec précision. » |
| Formation | Trav. social (UQAM, 2018) · Somatic Experiencing (cert. 2021) |
| Voies | Ancrage corporel · Parole et récit |
| Mode d'écoute | Non-directif — la parole vous appartient |
| Langues | Français · Innu-aimun |
| Modalité | Virtuel |
| Disponibilité | Mer. 14 jan. 10 h 00 · Jeu. 15 jan. 14 h 30 |

### 4.2 Samuel K. — Voie connaissance, mode outils

| Dimension | Valeur |
|---|---|
| Prénom + Initiale | Samuel K. |
| Pronoms | il / him |
| Fréquence | 741 Hz — expression, parole, clarification |
| Vibration/texture | « Chaleur sèche, présence nette. Les mots ont du poids, les silences aussi. Un espace où les choses se nomment. » |
| Couleur dominante | Ocre rouge (#9C4A1E) |
| Palette secondaire | Sable doré (#D4A853) + lin naturel (#EDE0CB) |
| Motif | Fractales géométriques angulaires — symétrie imparfaite, généré paramétrique |
| Ambiance sonore | Cloche tibétaine unique, résonance longue, pas de boucle |
| Verbatim | « Je propose des outils concrets — pas des formules. Ce qui marche pour vous, on le construit ensemble à partir de ce que vous vivez. Je ne connais pas votre réponse avant que vous la trouviez. » |
| Formation | Psychologie (Université de Montréal, 2015) · TCC avancée (cert. 2019) |
| Voies | Connaissance et clarification |
| Mode d'écoute | Outils concrets — on construit ensemble |
| Langues | Français · Anglais · Wolof |
| Modalité | Hybride (Montréal + virtuel) |
| Disponibilité | Lun. 13 jan. 9 h 00 · Mar. 14 jan. 16 h 00 |

### 4.3 Anishka M. — Voie contemplation, mode culturel

| Dimension | Valeur |
|---|---|
| Prénom + Initiale | Anishka M. |
| Pronoms | iel / them |
| Fréquence | 396 Hz — libération, sol, ancrage |
| Vibration/texture | « Terre et racines. Une présence ancrée qui ne bouge pas quand vous bougez. Un fond stable sur lequel appuyer ce que vous portez. » |
| Couleur dominante | Vert forêt profond (#2D5016) |
| Palette secondaire | Terre cuite (#C2651A) + beige chaud (#E8DCC8) |
| Motif | Spirales organiques inspirées des plantes — enroulement lent, généré paramétrique |
| Ambiance sonore | Vent dans les feuilles, boucle 10 s |
| Verbatim | « Mon accompagnement part du corps, de la terre, de ce qui est là avant les mots. Je travaille dans un cadre mixte — savoirs issus des traditions de soin anishinaabe et formations occidentales. Ces deux univers ne se contredisent pas dans ma pratique. » |
| Formation | Cert. Relation d'aide (UQAM, 2020) · Formation traditionnelle anishinaabe (non académique, transmise) |
| Voies | Pratiques contemplatives · Savoirs autochtones |
| Mode d'écoute | Cadre culturel et spirituel — ancré dans une vision du monde |
| Langues | Français · Anishinaabemowin (ojibwé) · Anglais |
| Modalité | En personne — Montréal · Virtuel |
| Disponibilité | Ven. 17 jan. 11 h 00 · Sam. 18 jan. 10 h 00 |

---

## 5. Accessibilité WCAG AA

### 5.1 Principes généraux

La carte abstraite ne repose pas sur la vision pour transmettre son contenu essentiel. C'est un avantage par rapport à la carte à photo. Mais elle introduit de nouvelles exigences d'accessibilité pour les éléments visuels abstraits (motifs, couleurs) et audio (voix, ambiance).

Cible : conformité **WCAG 2.1 niveau AA** sur l'ensemble des surfaces. Aucune fonctionnalité ne peut être inaccessible à une personne utilisant un lecteur d'écran, une navigation clavier, ou sans audio.

### 5.2 Alt-text sensoriel pour le motif

Le motif organique est décoratif dans sa dimension visuelle, mais il porte de l'information sensorielle. L'alt-text ne dit pas « image abstraite bleue » — il dit ce que le motif représente sur le plan sensoriel.

**Format d'alt-text sensoriel** :

```
aria-label="Motif de présence de [Prénom] : [description sensorielle du motif en 1-2 phrases]"
```

**Exemples** :
- Mariève T. : `aria-label="Motif de présence de Mariève : ondes lentes et profondes, horizon immobile sous une surface calme"`
- Samuel K. : `aria-label="Motif de présence de Samuel : structures géométriques nettes, symétrie légèrement brisée, présence ferme"`
- Anishka M. : `aria-label="Motif de présence d'Anishka : spirales végétales qui s'enroulent vers le centre, ancrage et enracinement"`

### 5.3 Descriptions textuelles alternatives de la couleur

La couleur dominante est informative — elle fait partie de la carte sensorielle du praticien. Elle doit être communicable sans la vision.

Chaque couleur de la palette IVIA dispose d'une description textuelle sensible dans un attribut `data-couleur-desc` utilisé par les lecteurs d'écran via ARIA :

```html
<div class="card-couleur" 
     aria-label="Couleur d'ambiance : bleu ardoise — calme et profondeur">
```

### 5.4 Transcripts obligatoires pour l'audio

Tout contenu audio a un équivalent textuel accessible.

**Pour l'échantillon de voix** : transcript complet du texte dit, affiché à la demande via un bouton `[Lire la transcription]` adjacent au bouton d'écoute. Ce n'est pas une simple indication « voix disponible » — c'est le texte intégral prononcé.

**Pour l'ambiance sonore** : description textuelle de l'ambiance dans un attribut `aria-description` :
```html
<button class="btn-ambiance" 
        aria-label="Écouter l'ambiance de séance de Mariève"
        aria-description="Pluie légère sur une fenêtre. Son continu, calme, régulier.">
```

### 5.5 Navigation clavier

Toutes les actions (bouton voix, bouton ambiance, voir profil, réserver) sont accessibles au clavier dans l'ordre logique du document. Pas de pièges de focus. Pas d'actions accessibles uniquement au survol de la souris.

### 5.6 Fréquences Hz — décodage sensoriel

Le chiffre en Hz peut être opaque pour les personnes non familières avec le concept. La description sensorielle qui l'accompagne est toujours présente et prioritaire sur le plan de l'accessibilité. Le Hz est le code — la description est le sens.

```html
<span class="card-frequence">
  <span aria-label="Fréquence sonore associée à ce praticien : 528 Hz — résonance et clarté intérieure">
    528 Hz
    <small>(résonance, clarté intérieure)</small>
  </span>
</span>
```

---

## 6. Page liste /praticiens

### 6.1 En-tête de page

```
┌─────────────────────────────────────────────────────────────────────────┐
│  IVIA — navigation globale                                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Nos praticiens                                                          │
│  ──────────────────────────────────────────────────────────────         │
│  Choisissez. Vous n'êtes pas assignée ou assigné.                        │
│                                                                          │
│  « Chaque profil est lisible sans compte, sans inscription.              │
│    Pas de photo — une présence sensorielle. »                            │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

La mention « Pas de photo — une présence sensorielle » est visible et assume la différence. Elle n'est pas défensive — elle est doctrinale.

### 6.2 Bloc de filtres

Les 5 filtres de la v1.0 sont conservés. Un sixième filtre est ajouté pour la v2.0.

#### Filtre 1 — Voie d'entrée

| Valeur affichée | Identifiant |
|---|---|
| Ancrage corporel | `voie_corps` |
| Parole et récit | `voie_parole` |
| Pratiques contemplatives | `voie_contemplation` |
| Savoirs autochtones | `voie_autochtone` |

#### Filtre 2 — Mode d'écoute

| Valeur affichée | Identifiant |
|---|---|
| Directif bienveillant | `mode_directif` |
| Non-directif | `mode_non_directif` |
| Miroir actif | `mode_miroir` |
| Ancrage dans le présent | `mode_ancrage` |
| Co-construction narrative | `mode_recit` |

#### Filtre 3 — Langue

| Valeur affichée | Code |
|---|---|
| Français | `fr` |
| Anglais | `en` |
| Innu-aimun | `moe` |
| Atikamekw | `atj` |
| Kanien'kéha (mohawk) | `moh` |
| Anishinaabemowin (ojibwé) | `ojw` |
| Autre (précisé sur profil) | `autre` |

> Les langues autochtones apparaissent dans leur nom d'origine en premier.

#### Filtre 4 — Disponibilité

| Valeur affichée | Identifiant |
|---|---|
| Cette semaine | `dispo_semaine` |
| Dans les 2 prochaines semaines | `dispo_2sem` |
| Flexible | `dispo_flexible` |

#### Filtre 5 — Modalité

| Valeur affichée | Identifiant |
|---|---|
| En personne — Montréal | `modal_presentiel_mtl` |
| Virtuel | `modal_virtuel` |
| Hybride | `modal_hybride` |

#### Filtre 6 — Fréquence dominante (nouveau v2.0) `[OPT pour l'utilisateur]`

| Valeur affichée | Hz |
|---|---|
| Ancrage et libération | 396 Hz |
| Transition | 417 Hz |
| Cohérence naturelle | 432 Hz |
| Résonance | 528 Hz |
| Relation et lien | 639 Hz |
| Expression | 741 Hz |
| Intuition | 852 Hz |

Ce filtre est un outil de précision optionnel. Il n'est pas promu en premier. Sa présence concrétise la dimension sensorielle du système sans l'imposer.

### 6.3 Grille de cartes

**Disposition** :
- Desktop (> 1024px) : 3 colonnes
- Tablette (768–1023px) : 2 colonnes
- Mobile (< 768px) : 1 colonne
- Espacement inter-cartes : 24px
- Tri par défaut : aléatoire, stable par session (seed anonyme)
- Tri alternatif : « Par disponibilité immédiate »

**Interdiction explicite** : tout tri favorisant un praticien pour des raisons commerciales ou de performance pour IVIA. Commentaire obligatoire dans le code source.

### 6.4 État zéro résultat

```
Aucun praticien ne correspond exactement à ces critères pour le moment.

Vous pouvez élargir vos filtres — ou nous écrire. Nous vous répondrons 
dans les 48 heures.  [NOUS ÉCRIRE]
```

### 6.5 Critères de listing — inchangés de la v1.0

| Condition | Vérification |
|---|---|
| Contrat IVIA actif | Signé, non résilié |
| Déclaration éthique signée | Intégrée au dossier |
| Formations vérifiées | Étape 1 franchie |
| Entretien éthique complété | Étape 2 franchie |
| 8 dimensions carte renseignées | Validées par IVIA et le praticien |
| Échantillon voix livré | Format Opus, < 200 Ko |
| Disponibilités renseignées | Au moins 1 créneau dans les 30 jours |

**Note** : la condition « Photo fournie » de la v1.0 est **supprimée**. Elle est remplacée par « 8 dimensions carte renseignées » et « Échantillon voix livré ».

### 6.6 Conformité Loi 25 — inchangée de la v1.0

La suppression de la photo simplifie la conformité sur un point : les données de représentation du praticien sont désormais uniquement textuelles et sonores — le régime de consentement pour la publication de données biométriques liées à l'image physique ne s'applique plus. Le consentement du praticien porte sur la voix (données biométriques vocales — encadrement spécifique dans le contrat type cf. `IVIA_CONTRAT_PRATICIEN_TYPE_v1.1.md`) et sur les informations textuelles.

### 6.7 Open Graph sans visage

La métadonnée Open Graph pour le partage sur les réseaux sociaux ne contient **jamais** de photo de visage. Elle utilise le motif organique abstrait du praticien comme image de prévisualisation, accompagnée du prénom, de la fréquence dominante et d'une ligne de la description vibration/texture.

```html
<meta property="og:image" content="/api/og/praticien/marieve-t?motif=vagues&couleur=3D5A80" />
<meta property="og:description" content="Mariève T. — 528 Hz — Eau profonde. Quelque chose remonte à la surface sans brusquerie." />
```

L'image OG est générée dynamiquement par une route `/api/og/praticien/[slug]` qui rend le motif SVG en PNG via un service serverless (Satori ou équivalent).

### 6.8 Message de pied de page de liste

```
IVIA accompagne, elle ne traite pas.

Les praticiens IVIA offrent un accompagnement non-clinique.
Si vous traversez une crise :

  1 866 APPELLE (277-3553)      — Ligne crise QC, 24 h / 24
  811 Info-Santé                — Santé QC, 24 h / 24
  Espoir pour le mieux-être     — 1 855 242-3310 (autochtone)
  Tel-Aide                      — 514 935-1101

Pour comprendre notre approche : /comment-ca-fonctionne
```

---

## 7. Page détail /praticiens/[slug]

URL : `/praticiens/[prenom-initiale-nom]` — ex. `/praticiens/marieve-t`  
Indexable. Aucun mur d'authentification.

### 7.1 En-tête du profil

```
┌─────────────────────────────────────────────────────────────────────────┐
│  [MOTIF ORGANIQUE LARGE — toute la largeur, ~250 px haut]               │
│  Animation WebGL légère si prefers-reduced-motion = no                   │
│  Couleur dominante en fond                                               │
│                                                                          │
│  Prénom + Initiale nom     Pronoms                                       │
│  Fréquence dominante : 528 Hz (résonance, clarté intérieure)            │
│  Vibration/texture : « [description sensorielle complète] »              │
│                                                                          │
│  Voies : [tags]    Langues : [tags]    Modalité : [tag]                  │
│                                                                          │
│  Tarif : 80 $ CAD / 60 min (tarif pilote unique)                        │
│                                                                          │
│  [▷ ÉCOUTER LA VOIX — 22 s]   [TRANSCRIPTION]                           │
│  [♫ AMBIANCE DE SÉANCE]                                                  │
│                                                                          │
│  [RÉSERVER UNE SÉANCE] ↓                                                │
└─────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Lecteur audio voix — spécifications

```
┌─────────────────────────────────────────────────────────────────────────┐
│  La voix de Mariève T.                                                   │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                          │
│  [▷ LECTURE]  ──────────────── 0:00 / 0:22                              │
│  Forme d'onde simplifiée (non cliquable — pas d'info cachée)            │
│                                                                          │
│  [TRANSCRIPTION ▾]                                                       │
│  « Je m'appelle Mariève. Quand vous parlez, j'écoute avant de           │
│    répondre. Ce que vous traversez mérite du temps et de la             │
│    précision. C'est ce que je peux vous offrir. »                        │
│                                                                          │
│  Note : Cet échantillon a été enregistré librement par Mariève T.       │
│  Il n'est pas un engagement contractuel sur le style de chaque séance.  │
└─────────────────────────────────────────────────────────────────────────┘
```

### 7.3 Sélecteur de fréquence — visualiseur

```
┌─────────────────────────────────────────────────────────────────────────┐
│  La fréquence associée à Mariève T.                                      │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                          │
│  528 Hz — résonance, clarté intérieure                                   │
│                                                                          │
│  [Animation SVG : onde sinusoïdale douce à la fréquence visuelle        │
│   correspondant à 528 Hz — purement illustratif, non thérapeutique]     │
│                                                                          │
│  ─────────────────────────────────────────────────────────────────────  │
│  Pour en savoir plus sur ce que signifie la fréquence                   │
│  dans l'approche IVIA : [/comment-ca-fonctionne#frequences]             │
│                                                                          │
│  Note obligatoire : La fréquence associée à ce praticien est une        │
│  description sensorielle de sa présence. Elle ne constitue pas une      │
│  affirmation thérapeutique et n'a pas été validée comme traitement      │
│  médical ou psychologique.                                               │
└─────────────────────────────────────────────────────────────────────────┘
```

### 7.4 Visualiseur de motif — interactif

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Le motif de présence                                                    │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                          │
│  [Animation WebGL ou SVG animé — motif organique en boucle lente]       │
│  Interactif : survol de souris ou glisser change légèrement l'animation │
│  Bouton : [Figer l'animation] si prefers-reduced-motion = yes            │
│                                                                          │
│  Description texte : « Ondes lentes et profondes, horizon immobile      │
│  sous une surface calme. Ce motif accompagne la présence de Mariève. »  │
└─────────────────────────────────────────────────────────────────────────┘
```

### 7.5 Verbatim du praticien (section courte)

Affiché entre la zone sensorielle et la bio longue. Formaté comme citation, non encadré dans un bloc gris — il fait partie du flux de lecture.

### 7.6 Bio longue (300-500 mots)

Gabarit inchangé de la v1.0. À la première personne. Sans listes à puces.

1. Qui êtes-vous avant d'être praticien ?
2. Qu'est-ce qui vous a amené à cet accompagnement ?
3. Comment décririez-vous votre façon d'être en séance ?
4. Avec quels types de situations travaillez-vous particulièrement ?
5. Ce que vous ne faites pas (limites claires)

### 7.7 Parcours et certifications

Inchangé de la v1.0. Note de vérification IVIA systématique.

### 7.8 Déclaration éthique

Inchangée de la v1.0. Liée à `IVIA_POLITIQUE_BIEN_ETRE_PRATICIENS_v1.0.md`.

### 7.9 Témoignages anonymisés

Inchangés de la v1.0. 3 à 5 témoignages. Sans photo, sans prénom. Date et voie conservées.

### 7.10 Encart vérification IVIA

Inchangé de la v1.0. 3 étapes publiques.

### 7.11 Calendrier de réservation

Inchangé de la v1.0. Cal.com ou équivalent souverain. Tarif affiché. Annulation gratuite jusqu'à 24 h.

---

## 8. Cohérence avec le funnel Écran 8

La carte praticien v2.0 est cohérente avec la matrice voie × thème de `IVIA_FUNNEL_RESTITUTION_MATRICE_v1.0.md`.

### 8.1 Point d'entrée depuis le funnel

Quand une personne complète le funnel (Écrans 1-8) et arrive à la carte de suggestion praticien (Bloc 4, Écran 8), elle voit une **version compacte** de la carte abstraite v2.0 — motif, couleur dominante, prénom, vibration/texture, voix écoutable. Le lien « Voir le profil complet » mène à `/praticiens/[slug]`.

### 8.2 Paramètres de pré-filtrage

Depuis le funnel, la carte suggérée est pré-sélectionnée selon les 4 critères documentés dans `IVIA_FUNNEL_QUIZ_TO_GUIDANCE_v1.1.md` :
- Voie d'entrée (Écran 4) — poids 35 %
- Mode d'écoute (Écran 6) — poids 35 %
- Disponibilité et géographie — poids 20 %
- Langue (Écran 2) — poids 10 %

La carte dans le funnel est identique visuellement à la carte dans `/praticiens`. Pas deux designs différents. Un seul composant.

### 8.3 Aucun thème de détresse dans le matching

Les thèmes choisis à l'Écran 3 (anxiété, deuil, relations, etc.) n'entrent pas dans le matching praticien — comme documenté dans la v1.1 du funnel. Cette décision est rappelée ici pour cohérence : la carte praticien ne sait pas pourquoi vous venez. Elle dit qui est ce praticien.

---

## 9. Plan technique

### 9.1 Génération des motifs SVG paramétriques

**Approche MVP** : Bibliothèque de 20 motifs SVG de base, paramétrés par :
- `fréquence` → fréquence visuelle des oscillations (basse : ondes lentes, haute : spirales rapides)
- `couleur_dominante` → teinte de base du motif
- `voie` → famille morphologique (organique sinueux / géométrique fractal / spirale végétale / lignes contemplatives)
- `mode_écoute` → densité (aéré / dense)

**Technique** : SVG inline généré côté serveur (Node.js + librairie svgson ou Rough.js pour l'aspect organique). Le SVG est mis en cache par CDN. Hash du SVG inclus dans l'URL pour invalidation.

**Approche post-pilote** : Animation WebGL légère via Three.js ou Shader web-component. Activée uniquement si `prefers-reduced-motion` est désactivé et connexion non lente (détection via `navigator.connection.effectiveType`).

### 9.2 Stockage et compression audio

| Fichier | Format | Qualité | Taille max |
|---|---|---|---|
| Échantillon voix | Opus, mono 48 kHz | 64 kbps | 200 Ko |
| Ambiance sonore | Opus, stéréo 48 kHz | 32 kbps | 80 Ko |
| Ambiance — fallback mobile | MP3, stéréo 44.1 kHz | 64 kbps | 120 Ko |

Pipeline de compression : upload praticien → FFmpeg serverless → validation format → stockage CDN.

Acceptance test obligatoire : l'échantillon de voix doit être intelligible sur casque d'entrée de gamme. Test réalisé par l'équipe IVIA avant publication de chaque profil.

### 9.3 CDN et stockage

Fichiers audio et SVG servis depuis CDN (BunnyCDN, Cloudflare R2, ou OVHcloud Object Storage — choix selon politique de souveraineté de la donnée documentée dans `IVIA_ANALYSE_STACK_OUTILS_v1.1.md`).

Pas de streaming adaptatif pour les échantillons courts (< 30 s) — livraison directe en un seul fichier compressé.

### 9.4 Génération dynamique Open Graph

Route serverless `/api/og/praticien/[slug]` :
- Paramètres : `motif`, `couleur`, `prenom`, `frequence`, `texture_courte`
- Rendu : Satori (JSX → PNG) ou html2canvas
- Taille image : 1200 × 630 px
- Contenu : motif abstrait + prénom + fréquence + une ligne texture
- **Aucun visage. Aucune silhouette humaine.**

### 9.5 Performance

- First Contentful Paint cible : < 1.5 s (connexion 4G)
- Largest Contentful Paint cible : < 2.5 s
- Le motif SVG est rendu inline — pas de requête HTTP supplémentaire pour la carte compacte
- Les boutons audio ne chargent aucun fichier avant clic — lazy loading strict
- Score Lighthouse accessibilité cible : > 95

---

## 10. Plan accessibilité audio

### 10.1 Transcripts obligatoires

Chaque échantillon voix publié sur `/praticiens` ou dans une carte de profil doit avoir :

1. **Transcript complet** du texte prononcé, accessible via bouton `[Lire la transcription]` adjacent
2. **Attribution** : « Ces mots ont été prononcés par [Prénom + Initiale] lors de l'enregistrement de son profil IVIA. »
3. **Langue déclarée** dans l'attribut `lang` du transcript

Le transcript est du texte visible dans le DOM (pas un attribut aria seulement) — pour permettre la copie, la lecture par synthèse vocale, la traduction navigateur.

### 10.2 Sous-titres pour les ambiances

Les ambiances sonores reçoivent une description textuelle complète accessible sans écoute :

```html
<figure class="ambiance-container">
  <button class="btn-ambiance" aria-describedby="desc-ambiance-marieve">
    Écouter l'ambiance
  </button>
  <figcaption id="desc-ambiance-marieve" class="ambiance-description">
    Ambiance sonore de Mariève : pluie légère et régulière sur une fenêtre. 
    Son continu, non perturbé. Durée : 8 secondes en boucle.
  </figcaption>
</figure>
```

### 10.3 Contrôle total par l'utilisateur

- **Aucun audio ne démarre automatiquement** — jamais. Ni voix, ni ambiance.
- Bouton stop toujours visible quand un audio est en cours
- Volume contrôlable via le contrôle natif du navigateur (pas de slider custom qui ne fonctionnerait pas au clavier)
- Respecte le volume système de l'appareil

### 10.4 Test d'accessibilité obligatoire avant publication

Chaque profil passe une checklist accessibilité avant mise en ligne :

- [ ] Alt-text sensoriel du motif rédigé et validé
- [ ] Transcript voix complet et exact
- [ ] Description ambiance sonore rédigée
- [ ] Contraste couleur WCAG AA vérifié (outil automatique + vérification manuelle)
- [ ] Navigation clavier testée sur les 4 actions de la carte
- [ ] Test lecteur d'écran (VoiceOver macOS ou NVDA Windows) sur la carte compacte et le profil détaillé

---

## 11. Tickets backlog MVP pilote

### T-01 — Composant carte abstraite (frontend)

**Priorité** : P0 — bloquant  
**Estimation** : 5 jours  
**Description** : Créer le composant React `<CartePraticien>` avec les 8 dimensions sensorielles. Responsive. Conforme WCAG AA. Props typées TypeScript. Storybook stories pour les 3 praticiens fictifs.  
**Critère d'acceptation** : Carte rendue correctement sur desktop/tablette/mobile. Score Lighthouse accessibilité > 95. Navigation clavier complète.

### T-02 — Génération SVG motifs paramétriques

**Priorité** : P0 — bloquant  
**Estimation** : 3 jours  
**Description** : Service de génération SVG côté serveur. 20 motifs de base. Paramètres : fréquence, couleur, voie, mode. Cache CDN.  
**Critère d'acceptation** : 20 motifs distincts générés. Temps de génération < 50 ms. SVG inline dans le HTML.

### T-03 — Pipeline audio praticien

**Priorité** : P0 — bloquant  
**Estimation** : 2 jours  
**Description** : Workflow d'upload audio dans l'espace praticien → FFmpeg compression Opus → validation format → stockage CDN → URL publique. Limite taille upload : 10 Mo (l'encodage réduit ensuite).  
**Critère d'acceptation** : Upload fonctionnel. Fichier Opus livré < 200 Ko. Lecture dans le navigateur sans erreur.

### T-04 — Page /praticiens — liste et filtres

**Priorité** : P0 — bloquant  
**Estimation** : 4 jours  
**Description** : Page liste avec grille de cartes abstraites. 6 filtres (voie, mode, langue, disponibilité, modalité, fréquence). Tri aléatoire stable par session. Responsive. SSG avec revalidation à chaque mise à jour de profil.  
**Critère d'acceptation** : Filtres fonctionnels en logique ET. Compteur de résultats en temps réel. État zéro résultat. Accessible.

### T-05 — Page /praticiens/[slug] — profil détaillé

**Priorité** : P0 — bloquant  
**Estimation** : 4 jours  
**Description** : Page profil expandée. Lecteur audio voix + transcript. Sélecteur fréquence + visualiseur SVG. Motif animé large. Verbatim. Bio longue. Parcours. Déclaration éthique. Témoignages. Calendrier Cal.com intégré.  
**Critère d'acceptation** : Tous les modules rendus. Lecteur audio accessible. Calendrier fonctionnel. Indexable (meta, sitemap).

### T-06 — Route API /api/og/praticien/[slug]

**Priorité** : P1  
**Estimation** : 1 jour  
**Description** : Génération dynamique d'image Open Graph (1200 × 630 px) avec motif abstrait + prénom + fréquence + texture courte. Aucun visage.  
**Critère d'acceptation** : Image générée < 500 ms. Contenu conforme doctrine (pas de visage, pas de silhouette).

### T-07 — Formulaire onboarding carte praticien

**Priorité** : P0 — bloquant  
**Estimation** : 3 jours  
**Description** : Interface dans l'espace praticien pour renseigner les 8 dimensions de la carte. Choix de couleur dans palette IVIA. Choix ou génération de motif. Upload audio. Aperçu de la carte en temps réel.  
**Critère d'acceptation** : Toutes les dimensions saisissables. Aperçu fidèle à la carte publique. Sauvegarde partielle autorisée (brouillon).

### T-08 — Accessibilité complète — audit et corrections

**Priorité** : P0 — bloquant  
**Estimation** : 2 jours  
**Description** : Audit Lighthouse + test manuel VoiceOver/NVDA sur carte compacte et profil détaillé. Corrections. Rédaction des alt-texts sensoriels pour les 3 praticiens pilotes. Rédaction des transcripts voix.  
**Critère d'acceptation** : Score Lighthouse accessibilité > 95 sur les deux pages. Checklist T-accessibilité (section 10.4) cochée pour les 3 praticiens pilotes.

### T-09 — Intégration carte dans funnel Écran 8

**Priorité** : P1  
**Estimation** : 2 jours  
**Description** : Réutiliser le composant `<CartePraticien>` dans le bloc 4 de l'Écran 8 du funnel. Version compacte. Matching selon les 4 critères documentés. Lien vers profil complet.  
**Critère d'acceptation** : Carte affichée dans le funnel avec les bonnes données. Lien vers profil fonctionnel. Design identique à `/praticiens`.

### T-10 — Conformité Loi 25 — clause voix dans contrat praticien

**Priorité** : P0 — bloquant  
**Estimation** : 0.5 jour (rédactionnel, avec avocat)  
**Description** : Ajouter au contrat type praticien (`IVIA_CONTRAT_PRATICIEN_TYPE_v1.1.md`) une clause de consentement spécifique à la publication de l'échantillon de voix comme donnée biométrique. Préciser les droits de retrait, la durée de conservation, l'usage autorisé.  
**Critère d'acceptation** : Clause rédigée, validée par avocat, intégrée au contrat.

### T-11 — Pipeline compression audio automatisé

**Priorité** : P1  
**Estimation** : 1 jour  
**Description** : Fonction serverless FFmpeg déclenchée à l'upload. Input : tout format audio. Output : Opus 64 kbps mono. Rejet si durée < 10 s ou > 35 s. Notification praticien si rejet.  
**Critère d'acceptation** : Compression fonctionnelle pour MP3, WAV, AAC, M4A en entrée. Taille output conforme. Temps de traitement < 10 s.

### T-12 — Suppression de toutes les références photo v1.0

**Priorité** : P0 — bloquant  
**Estimation** : 0.5 jour  
**Description** : Audit du code source pour identifier et supprimer toute référence à `photo`, `portrait`, `headshot`, `avatar-human`, `placeholder-face`. Vérification dans les schemas Prisma, les types TypeScript, les commentaires.  
**Critère d'acceptation** : `grep -r "photo\|portrait\|headshot" src/` renvoie zéro résultat pertinent. Les migrations Alembic liées aux champs photo sont archivées.

### T-13 — Monitoring audio CDN

**Priorité** : P2  
**Estimation** : 1 jour  
**Description** : Tableau de bord interne (accès IVIA uniquement) affichant : fichiers audio par praticien, taille, dernière écoute agrégée (count, pas identifiant), erreurs de lecture. Données anonymisées, jamais par visiteur.  
**Critère d'acceptation** : Dashboard lisible. Données agrégées uniquement. Aucune donnée d'identification du visiteur.

---

## 12. Ouvertures : questions à arbitrer

Les questions suivantes sont ouvertes à la date du 9 mai 2026. Elles requièrent une décision de David et/ou de l'avocat avant de pouvoir être tranchées en code.

### Q-01 — Voix David pour le pilote : cadrage juridique

David peut prêter sa voix pour simuler plusieurs praticiens fictifs au MVP. Cette décision est pragmatique et assumée.

**Question** : Faut-il le mentionner quelque part sur la plateforme ? Une note du type « Certains échantillons du pilote ont été enregistrés par l'équipe IVIA à titre d'illustration » est-elle nécessaire pour la conformité Loi 25 et pour la doctrine d'honnêteté radicale ?

**Recommandation provisoire** : Oui. Une note discrète sur le profil des praticiens fictifs du pilote (et uniquement eux) indiquant le caractère illustratif de l'échantillon. Dès qu'un praticien réel est actif, son propre échantillon remplace.

### Q-02 — Fréquences Hz : niveau de mise en garde

La doctrine est claire : pas de promesses thérapeutiques. Mais le niveau de mise en garde visible sur la carte compacte (vs. profil détaillé) n'est pas encore tranché.

**Question** : La note de mise en garde sur la nature sensorielle (non thérapeutique) des fréquences doit-elle apparaître sur la carte compacte, ou seulement sur le profil détaillé et la page `/comment-ca-fonctionne` ?

**Option A** : Note sur le profil détaillé seulement — carte compacte reste sobre.  
**Option B** : Infobulles (tooltip) accessible au clic sur le Hz dans la carte compacte — note s'affiche sans alourdir visuellement.  
**Option C** : Ligne systématique sous chaque mention Hz — « description sensorielle, pas prescription » — même sur la carte compacte.

### Q-03 — Motif organique : co-construction ou génération ?

La doctrine dit co-construite avec le praticien. En pratique, deux modèles sont possibles pour le pilote :

**Option A** : Le praticien choisit parmi 20 motifs préfabriqués. Simple, rapide, fiable.  
**Option B** : Le motif est généré automatiquement selon ses paramètres (voie, mode, fréquence, couleur) avec possibilité de régénérer. Plus doctrinal mais plus complexe à onboarder.  
**Option C** : Génération automatique par défaut + interface de personnalisation avancée optionnelle pour post-pilote.

**Recommandation provisoire** : Option C. Génération automatique pour le pilote (moins de friction praticien), personnalisation avancée dans le backlog post-pilote.

### Q-04 — Accessibilité des animations WebGL

L'animation WebGL sur le profil détaillé est conditionnée à `prefers-reduced-motion = no`. Mais certains utilisateurs ayant des besoins d'accessibilité n'ont pas ce paramètre activé sur leur appareil.

**Question** : Faut-il ajouter un toggle visible « Activer / désactiver l'animation » sur la page profil, indépendamment de `prefers-reduced-motion` ?

**Recommandation provisoire** : Oui. Toggle persistant via `localStorage`. Non bloquant pour le MVP — peut être ajouté en T-08bis post-pilote.

### Q-05 — Palette de fréquences Hz : validation externe

La liste de 7 fréquences retenues (396, 417, 432, 528, 639, 741, 852 Hz) est issue de la tradition du Solfège sacré. Elle n'a pas de validation scientifique solide dans la littérature en santé mentale.

**Question** : Avant le lancement public, faut-il faire valider cette liste par un musicothérapeute accrédité ou un chercheur en neurosciences sonores — à titre de conseil externe, sans que cette validation soit présentée comme une endorsement scientifique ?

**Recommandation provisoire** : Oui, consultation informelle d'un musicothérapeute accrédité (ex. : membre de l'Association de musicothérapie du Canada). Objet : vérifier que la liste ne contient rien de doctrinalement problématique et que les descriptions sensorielles associées sont défendables. Délai recommandé : avant la mise en ligne du premier profil public.

### Q-06 — Ambiance sonore : droits et licences

Les ambiances sonores (pluie, cloche tibétaine, etc.) doivent être soit :
- Enregistrées par le praticien lui-même (idéal doctrinal)
- Issues d'une bibliothèque sous licence CC0 ou propriété IVIA

**Question** : IVIA doit-elle constituer une bibliothèque d'ambiances sous licence explicite, ou demander à chaque praticien de fournir son propre enregistrement ?

**Recommandation provisoire** : Bibliothèque IVIA de 10 ambiances sous licence CC0 pour le pilote. Enregistrement propre du praticien encouragé mais non obligatoire pour le MVP.

### Q-07 — Numérotation des versions de cartes

Quand un praticien modifie sa carte (nouveau verbatim, nouvelle couleur, nouvel échantillon voix), faut-il versionner la carte et conserver un historique des versions précédentes pour traçabilité ?

**Question** : Historique de version des cartes : oui ou non, et avec quelle durée de conservation ?

**Recommandation provisoire** : Oui, historique minimal côté serveur (dernière version N-1 conservée 30 jours). Pas d'affichage public des versions précédentes. Conforme à la politique de conservation des données IVIA.

---

## Notes de déploiement

- **Slug URL** : `/praticiens` (pluriel, sans accent, français)
- **Pages profil** : `/praticiens/[prenom-initiale-nom]` (ex. `/praticiens/marieve-t`)
- **Indexation** : `robots.txt` autorisé, `sitemap.xml` inclut toutes les pages profil actives
- **Méta-description liste** : « Choisissez un praticien IVIA. Profils sensoriels, voix, fréquences et disponibilités — sans compte requis, sans photo. »
- **Méta-description profil** : Générée depuis les deux premières phrases du verbatim + vibration/texture
- **Open Graph** : Motif abstrait + prénom + fréquence + texture courte — aucun visage, aucune silhouette

---

*Au sein de l'être — En actes.*  
*Pour le peuple, par le peuple.*

---

**Fin du document — IVIA_SPEC_PAGE_PRATICIENS_v2.0**  
*9 mai 2026 — Remplace intégralement IVIA_SPEC_PAGE_PRATICIENS_v1.0*

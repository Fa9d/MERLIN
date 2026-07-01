## IVIA – Mobile Screens Showcase (3 téléphones scrollables)

### 0. Principes généraux

- Style global : calme, chaleureux, minimal, rassurant.  
- Ton : accompagnant, jamais prescriptif ni dramatique.  
- Typographie :  
  - Sans‑sérif humaniste, ex. `Inter`, `SF Pro`, ou équivalent.  
  - Hiérarchie simple :  
    - H1 : titres d’écran  
    - H2 : sous‑titres / titres de blocs  
    - Body : texte courant  
    - Small : notes et aides contextuelles.  
- Bords : angles légèrement arrondis (8–12 px) pour cartes et boutons.  
- Icônes : simples, lignes ou formes pleines douces, pas d’angles agressifs.

---

### 1. Layout commun des 3 téléphones

- Format : écran mobile type iPhone/Android, ratio 9:19.5, avec safe area.  
- Scroll vertical.  
- Header :  
  - Titre (H1), éventuel sous‑titre (H2), icône discrète (paramètres ou retour).  
- Contenu principal :  
  - Sections verticales : cartes, listes, questions, sliders.  
- **Bottom navigation fixe** (toujours visible) :  
  - 5 éléments :  
    - Icône + label « Accueil »  
    - Icône + label « Check‑in »  
    - **Bouton central rond RGNR (accent principal)**  
    - Icône + label « RGNR »  
    - Icône + label « Praticiens »  
- Bouton central RGNR :  
  - Forme : cercle, légèrement plus grand que les autres icônes.  
  - Fonction : ouvrir une modale « Enregistrer un moment RGNR » (texte, audio, moment important).

---

### 2. Thèmes de couleurs

#### 2.1 Thème clair

- Fond global  
  - `background` : `#F5F4EE` (beige très doux, légèrement chaud).  
- Surfaces (cards, panneaux, bottom bar)  
  - `surface` : `#FFFFFF`.  
- Texte  
  - `text-primary` : `#1F2933` (gris très foncé).  
  - `text-secondary` : `#6B7280` (gris moyen).  
- Accent principal (RGNR)  
  - `accent-rgnr` : `#3B7F6A` (vert profond apaisant).  
- Couleurs de soutien  
  - `accent-soft-1` : `#FBE8D3` (pêche très pâle, fonds d’info).  
  - `accent-soft-2` : `#E3F4E0` (vert pâle, succès doux).  
- Boutons  
  - Primary : fond `accent-rgnr`, texte `#FFFFFF`.  
  - Secondary : fond `#FFFFFF`, bord `accent-rgnr`, texte `accent-rgnr`.  
- Bottom nav  
  - Fond : `#FAFAF8` ou `#FFFFFF`.  
  - Icônes inactives : `#9CA3AF`.  
  - Icône + label actif : `accent-rgnr`.  
  - Bouton central RGNR : cercle avec fond `accent-rgnr`, icône blanche.

#### 2.2 Thème sombre

- Fond global  
  - `background` : `#0F1720` (bleu‑gris très sombre).  
- Surfaces  
  - `surface` : `#111827` ou `#1F2933`.  
- Texte  
  - `text-primary` : `#F9FAFB`.  
  - `text-secondary` : `#9CA3AF`.  
- Accent principal (RGNR)  
  - `accent-rgnr` : `#5BD9A3` (vert turquoise doux, lisible sur fond sombre).  
- Couleurs de soutien  
  - `accent-soft-1` : `#1F2933`.  
  - `accent-soft-2` : `#064E3B`.  
- Boutons  
  - Primary : fond `accent-rgnr`, texte `#03110C`.  
  - Secondary : fond `background`, bord `accent-rgnr`, texte `accent-rgnr`.  
- Bottom nav  
  - Fond : `#020617`.  
  - Icônes inactives : `#6B7280`.  
  - Icône + label actif : `accent-rgnr`.  
  - Bouton central RGNR : cercle `accent-rgnr`, icône foncée.

---

### 3. Téléphone 1 – Découverte + premier check‑in

**Écran 1 – Home (après onboarding)**  
- Header :  
  - Titre : « Bon retour, [Prénom] ».  
- Section principale (carte pleine largeur) :  
  - Titre : « Prendre un moment pour toi ».  
  - Sous‑texte : « Quelques questions pour mieux t’accompagner aujourd’hui. ».  
  - Bouton primary centré : « Faire un check‑in ».  
- Sous‑section : petit texte rassurant « Tu peux arrêter à tout moment. ».

**Écran 2 – Check‑in (Émotions)**  
- Titre : « Comment te sens‑tu en ce moment ? ».  
- Grille ou ligne de 6–7 boutons émotion (icône + mot).  
- Bas d’écran : bouton primary « Suivant », lien texte « Passer pour l’instant ».

**Écran 3 – Check‑in (Corps)**  
- Titre : « Et ton corps, comment va‑t‑il ? ».  
- Liste de cases à cocher : Tensions / Douleurs / Fatigue / Respiration courte / Ça va plutôt bien.  
- Bouton primary « Suivant ».

**Écran 4 – Check‑in (Pensées)**  
- Titre : « À quoi reviennent le plus souvent tes pensées ? ».  
- Chips défilables horizontalement : Travail, Famille, Argent, Santé, Relations, Autre.  
- Bouton primary « Suivant ».

**Écran 5 – Check‑in (Environnement)**  
- Titre : « Autour de toi, ton environnement t’aide ou te pèse aujourd’hui ? ».  
- Slider 1–5 avec labels aux extrêmes (« Plutôt lourd » / « Plutôt soutenant »).  
- Bouton primary « Voir les pistes pour aujourd’hui ».

**Écran 6 – Suggestions du jour**  
- Carte résumé : courte phrase qui combine les réponses (émotion principale, état du corps, contexte dominant).  
- 2–3 cartes de pratiques avec :  
  - Titre  
  - Durée (5–10 min)  
  - Tag (ex. « Doux », « Rapide »).  
- Boutons :  
  - Primary : « Commencer cette pratique »  
  - Secondary : « Voir d’autres pistes ».

Bottom nav fixe visible à chaque écran.

---

### 4. Téléphone 2 – RGNR (accompagnement continu)

**Écran 1 – Vue RGNR**  
- Titre : « Ton chemin de RGNRation ».  
- Bloc visualisation : 4 barres ou mini‑graphes pour Corps / Émotions / Pensées / Environnement (pas médical, très simple).  
- Section « Aujourd’hui » :  
  - Texte : « Où en es‑tu aujourd’hui ? ».  
  - Bouton primary : « Faire un micro check‑in ».  
- Carte « Suggestion du moment » : courte phrase type micro‑pratique.

**Écran 2 – Micro check‑in**  
- Titre : « Depuis la dernière fois, c’est plutôt mieux, pareil ou plus difficile ? ».  
- 3 gros boutons horizontaux : « Mieux » / « Stable » / « Plus difficile ».  
- Petit texte rassurant en dessous.

**Écran 3 – Fil RGNR (timeline)**  
- Liste verticale de cartes :  
  - Date courte (Lun, Mar, etc.).  
  - Petit texte de type : « Tu as pris 5 minutes pour respirer. ».  
  - Icône simple (check, cœur).  

**Écran 4 – Intentions en cours**  
- Titre : « Ce que tu as choisi de nourrir ».  
- 2–3 cartes intention :  
  - Titre  
  - Barre de progression douce (pas de score, juste un sentiment d’avancement).

**Action du bouton central RGNR**  
- Tape → modale pleine largeur ou bottom sheet :  
  - Titre : « Enregistrer un moment ».  
  - 3 boutons :  
    - « Écrire quelques mots ».  
    - « Ajouter une note vocale ».  
    - « Marquer un moment important ».

---

### 5. Téléphone 3 – Lien avec le/la praticien·ne

**Écran 1 – Liste des praticiens**  
- Titre : « Les personnes qui peuvent t’accompagner ».  
- Icône filtre en haut à droite.  
- Liste de cartes :  
  - Photo ronde, nom, type (ex. psychologue, travailleur social, etc.), 1 ligne de description.  
  - Optionnel : badge « En ligne » / « En personne ».

**Écran 2 – Détail praticien**  
- Header : photo, nom, type.  
- Bloc « Comment iel travaille » : 3 puces courtes.  
- Bloc « Langues, région ».  
- Bas d’écran :  
  - Bouton primary : « Demander un rendez‑vous ».  
  - Bouton secondary : « Envoyer un message » (si disponible).

**Écran 3 – Demande de rendez‑vous**  
- Titre : « Demander un rendez‑vous ».  
- Sélecteur de créneau (liste ou mini calendrier).  
- Sélecteur de mode : boutons segmentés « En personne » / « En ligne ».  
- Champ texte : « Ce que tu aimerais aborder (optionnel) ».  
- Bouton primary : « Envoyer la demande ».

**Écran 4 – Résumé avant séance**  
- Carte :  
  - Texte : « Ta prochaine rencontre avec [Nom] est prévue le [date/heure]. ».  
  - Sous‑texte : « On te proposera un court check‑in avant la séance. ».

Bottom nav identique, bouton RGNR central toujours présent.

---
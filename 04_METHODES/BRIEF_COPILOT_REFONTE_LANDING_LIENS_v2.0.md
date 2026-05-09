# BRIEF COPILOT — Réalignement IVIA v2.0

**Version** : 2.0
**Date** : 9 mai 2026
**Statut** : Réaligné après livraison des piliers stratégiques
**Destinataire** : GitHub Copilot (mode auto, VS Code, repo MERLIN)
**Périmètre** : `ivia_mockups/` (site déployé sur https://ivia.pplx.app)
**Auteur du brief** : Computer (Perplexity)
**Mandat** : David Phaneuf, fondateur IVIA

**Documents de référence :**
- Brief v1.0 : `04_METHODES/BRIEF_COPILOT_REFONTE_LANDING_LIENS_v1.0.md`
- Mode d'emploi symbiose : `04_METHODES/SYMBIOSE_COPILOT_COMPUTER_v1.0.md`

---

## 1. CONTEXTE ÉVOLUTIF — Pourquoi une v2.0

### Ce qui existait ce matin (v1.0, 9 mai 2026, ~10h)

Le brief v1.0 identifiait cinq chantiers opérationnels urgents : corriger 112 liens morts répartis sur 32 pages, refonter la landing (hero textuel trop dense, double CTA qui se cannibalisent, scroll de 4500px+), fermer les tunnels test des trois personas (Camille, Mylène, David), exposer les 16 articles de la bibliothèque, et renforcer la cohérence visuelle inter-pages. Ces cinq chantiers restent intégralement valides et constituent la priorité d'entrée de jeu pour Copilot.

### Le pivot du midi — la version botanique ne remplace pas l'architecture Python

Dans la matinée, une version "botanique" du site a été produite par Claude : trois pages superbes, vocabulaire et esthétique parfaitement alignés sur la doctrine IVIA, mais aucune des pages internes (espaces client, praticien, admin), aucune architecture Python, aucun système de build. Cette version devient la **direction artistique de référence**, pas une base de code à adopter. La charte botanique est disponible chez le user sous `C:\MERLIN\07_EXPORTS\ivia_concept_v2_botanique\reference-visuelle.html`. Copilot ne la verra pas directement — elle appartient à l'environnement local du user — mais doit s'y référer via les extraits codifiés dans la section C6 ci-dessous pour aligner palette, typographie et voix sur l'existant Python sans toucher à l'architecture.

### Les trois piliers stratégiques livrés — 4 modules nouveaux imposés

Trois documents de fond ont été livrés au repo entre midi et ce brief :

- `00_DOCTRINE/dispositif_veille_ivia_v1.md` — six paliers de veille (légal, scientifique, marché, culturel, financement, technologique), sources et cadences
- `00_DOCTRINE/etat_marche_quebec_v1.md` — cartographie du marché québécois du mieux-être numérique francophone, positionnement IVIA, données de référence
- `00_DOCTRINE/indicateurs_praticien_v1.md` — cartographie complète des indicateurs (6 financiers, 7 qualitatifs, 7 typologiques, 3 santé praticien, 3 doctrinaux)

Ces trois documents imposent des modules qui n'existaient pas dans la v1.0 : un calendrier de réservation fonctionnel (C7), un cycle audio testable de bout en bout (C8), un dashboard de statistiques praticien et un panneau public de données anonymisées (C9), et un pipeline de contenu data-driven (C10). La charte botanique impose par ailleurs un chantier d'intégration artistique sur le CSS existant (C6).

---

## 2. RÈGLES D'OR (rappel synthétique)

Ces cinq règles ne se discutent pas. Elles sont détaillées dans `04_METHODES/SYMBIOSE_COPILOT_COMPUTER_v1.0.md`.

**Règle 1 — GitHub master = source de vérité unique.** Tout commit passe par `Fa9d/MERLIN`, branche `master`. Aucune modification locale non poussée.

**Règle 2 — Copilot ne déploie pas sur ivia.pplx.app.** Le déploiement est exclusivement géré par Computer (Perplexity) via `deploy_website` + `publish_website`. Le `site_id` `95d9a5aa-bdb5-4aca-a524-dd62c489f205` reste dans l'environnement Computer.

**Règle 3 — Toujours éditer les sources Python, jamais les HTML générés.** Les fichiers à éditer sont `pages_public.py`, `pages_client.py`, `pages_praticien.py`, `pages_admin.py`, `pages_funnel.py`, `article_meta.py`, `page_index.py`. Les `.html` dans `ivia_mockups/` sont des artefacts de build — les modifier directement serait écrasé au prochain `build_pages.py`.

**Règle 4 — Lancer `python build_pages.py` après chaque modification Python.** Commande : `cd ivia_mockups && python build_pages.py`. Vérifier que le build passe sans erreur avant tout commit.

**Règle 5 — Tester localement avant push.** `python -m http.server 8000` depuis `ivia_mockups/`, puis valider sur `http://localhost:8000` les parcours Camille, Mylène et David avant de push.

---

## 3. CHANTIERS v1.0 — RAPPEL (toujours valides, priorité d'exécution)

Ces cinq chantiers sont décrits en détail dans `04_METHODES/BRIEF_COPILOT_REFONTE_LANDING_LIENS_v1.0.md`. Copilot doit les lire intégralement avant de commencer.

**C1 — Refonte landing** (`pages_public.py`, fonction générant `index.html`) : hero en un écran complet (~95vh), titre en deux lignes maximum ("Quand tout se mélange, / commencez par être entendu."), un seul CTA primaire grand ("Commencer une écoute →"), lien secondaire discret ("ou voir comment ça se passe"), visuel SVG inline organique côté droit, bandeau urgence bas du hero. Réorganisation des sections suivantes (action → mécanique → cadre conceptuel). Scroll mobile cible : moins de 2500px.

**C2 — Activation 112 liens morts** : footers internes `client/`, `praticien/`, `admin/` (liens vers `../mentions.html`, `../confidentialite.html`, `../cgu.html`, `mailto:contact@ivia.quebec`), sidebars compte (→ `parametres.html` pour admin, → `abonnement.html` pour praticien), formulaires inscription/connexion/paiement, cards dashboard. Créer : `client/compte.html`, `client/mot-de-passe-oublie.html`, `praticien/compte.html`. Validation : `grep -rh 'href="#"' --include="*.html" | wc -l` doit retourner 0.

**C3 — Correction architecture mobile landing** : cible < 2500px de hauteur totale sur 390px de large. Identifier les sections qui doublent la hauteur sur mobile (grilles qui se stackent mal, textes trop longs, marges inadaptées) et corriger dans le CSS partagé `shared/public.css`.

**C4 — Exposition des 16 articles bibliothèque** : dans `pages_public.py`, `build_bibliotheque()`, ajouter pour chaque article un lien de source `articles_md/IVIA_ARTICLE_{X}_{Y}_v1.0.md`. Vérifier que `articles_md/` est servi par le déploiement.

**C5 — Cohérence visuelle inter-pages** : variables CSS cohérentes (`--color-creme`, `--color-aubergine`, `--color-rose`, `--color-rose-deep`, `--color-abricot`, `--color-miel`, `--color-mousse`, `--color-glacier`, `--color-lavande`, `--color-prune`). Polices : Fraunces (display), Lora (texte), Inter (sans-serif). Aucune couleur hors palette. Aucun emoji dans les textes UI. Ton québécois exclusivement.

---

## 4. CHANTIERS v2.0 — NOUVEAUX MODULES À CONSTRUIRE

### C6 — INTÉGRATION CHARTE BOTANIQUE PAR-DESSUS L'EXISTANT
**Priorité : haute — conditionne la lisibilité de tous les autres chantiers**

La charte "La Coupe" formalise la direction artistique IVIA dans `C:\MERLIN\07_EXPORTS\ivia_concept_v2_botanique\reference-visuelle.html`. Copilot ne peut pas y accéder directement, mais le user peut lui en passer des extraits en contexte. Voici les invariants à appliquer dans `shared/public.css` et les sources Python concernées.

**Palette "La Coupe" — variables à définir ou mettre à jour dans `shared/public.css` :**

```css
:root {
  --color-creme:        #F0E0DC;  /* crème principal */
  --color-creme-deep:   #EEDCC9;  /* crème profonde */
  --color-aubergine:    #2A1A22;  /* couleur texte principale, fonds sombres */
  --color-bois-rose:    #C58A8A;  /* accents chauds */
  --color-abricot:      #DA9266;  /* CTA secondaires, hover */
  --color-miel:         #D9A841;  /* highlights, éléments d'attention */
  --color-mousse:       #6B8568;  /* praticien, calme */
  --color-glacier:      #A1B6C0;  /* admin, distance neutre */
  --color-lavande:      #B6AAC8;  /* client, douceur */
  --color-prune:        #8C5876;  /* accents profonds */
}
```

**Typographie :**

- Fraunces : titres (display, weight 300-700 selon hiérarchie). Import Google Fonts déjà présent ou à ajouter.
- Lora : corps de texte, taille 16-18px, line-height 1.65 minimum.
- Inter : éléments fonctionnels (navigation, boutons, formulaires), jamais pour les contenus éditoriaux.

**Espacements** : padding section minimum 80px vertical sur desktop, 48px sur mobile. Marges généreuses — l'air fait partie du vocabulaire visuel IVIA.

**Adaptation hero landing** : le titre du hero peut s'inspirer du vocabulaire botanique ("Déposer ce que vous portez" est un exemple de ton) sans copier mécaniquement les textes de la version Claude. La doctrine IVIA reste ("Au sein de l'être — En actes"). Composer une illustration cocon ou feuille type botanique en SVG inline, en remplacement de la zone vide actuelle.

**Contraste WCAG AA** : vérifier chaque combinaison texte/fond. L'aubergine `#2A1A22` sur crème `#F0E0DC` passe AA. La bois-rose `#C58A8A` sur crème passe AA uniquement en grand corps (18px+) — ne pas l'utiliser pour du texte courant. Le miel `#D9A841` sur fond blanc ne passe pas AA — réserver aux éléments décoratifs et aux grands titres sur fond foncé.

**Interdits stricts (doctrine charte) :**
- Noir pur `#000000` — interdit. Utiliser `--color-aubergine`.
- Deux couleurs vives sur le même écran (vibrations visuelles).
- Photos de personnes en stock-photo.
- Dégradés saturés (style Instagram 2010).
- Italique pour exprimer la chaleur — la chaleur passe par le vocabulaire, pas par le style de fonte.

**Phasage** : appliquer la charte botanique dans cet ordre. Public d'abord (`shared/public.css`, pages issues de `pages_public.py`). Client ensuite (`shared/client.css` ou équivalent). Praticien et admin : cohérence sobre, pas de charte botanique complète — ces espaces restent fonctionnels et mesurés.

**Référence** : user peut passer des extraits de `reference-visuelle.html` à Copilot via son contexte VS Code.

---

### C7 — CALENDRIER FONCTIONNEL
**Priorité : haute — différenciateur de maturité produit**

Le calendrier est le premier point de contact entre la volonté du client et la disponibilité du praticien. Sans lui, le modèle de rendez-vous n'est pas testable.

**Vue praticien — nouvelle page `praticien/agenda.html`** (enrichir la page existante via `pages_praticien.py`) :

- Grille hebdomadaire 7 jours, créneaux de 30 minutes, 8h-20h fuseau `America/Toronto` (Montréal).
- Trois états de créneau : disponible (fond crème, bordure mousse), réservé (fond lavande, nom client fictif), bloqué (fond gris clair, label "Indisponible").
- Actions : cliquer sur un créneau disponible → modal "Bloquer ce créneau" ou "Marquer disponible". Cliquer sur réservé → modal avec fiche client fictive et lien vers `audio-traiter.html`.
- Navigation : flèches < > semaine précédente / suivante. Bouton "Aujourd'hui".

**Vue client — intégration dans `pages_funnel.py`** (parcours réservation) :

- Sélection du praticien sur `praticiens.html` → clic "Réserver une séance" → page `funnel/choisir-creneau.html`.
- Affichage des créneaux disponibles du praticien sélectionné (données depuis `assets/data/agenda_fixtures.json`).
- Sélection d'un créneau → récapitulatif (praticien, date, heure, durée, tarif) → bouton "Confirmer le rendez-vous" → `client/confirmation-paiement.html` (page existante ou à créer).
- Pas de connexion Stripe pour l'instant.

**Données simulées** : créer `ivia_mockups/assets/data/agenda_fixtures.json` avec 3 semaines de créneaux pour Mylène (praticienne de référence des tests). Format ISO 8601, fuseau explicite : `"2026-05-11T10:00:00-04:00"`.

**JS pur, mobile-first** : aucune dépendance externe pour le calendrier. Le composant doit fonctionner sur 390px sans overflow horizontal. Tablette et desktop : grille élargie.

**Commit attendu** : `feat(calendrier): C7 - agenda praticien + funnel réservation client`

---

### C8 — CYCLE AUDIO TESTABLE DE BOUT EN BOUT
**Priorité : haute — c'est le cœur différenciateur de la plateforme IVIA**

Le cycle audio est ce qui distingue IVIA de toute autre plateforme d'accompagnement. Le rendre testable intégralement, même en simulation, est la démonstration de produit la plus puissante disponible.

**Page client `client/audio-async.html`** (existe peut-être partiellement — vérifier et compléter) :

- Interface d'enregistrement micro via `MediaRecorder API`. Bouton "Commencer à parler" → enregistrement en cours (compteur temps, visualisation onde audio CSS, maximum 5 minutes). Bouton "Terminer et envoyer".
- Si le navigateur ne supporte pas `MediaRecorder` ou si l'utilisateur refuse le micro : basculer automatiquement sur un texte fictif ("Simulation en mode démo — votre dépôt est enregistré").
- Écran de confirmation après envoi : "Votre dépôt a été reçu. Un praticien vous répondra dans 24 à 72 heures." Lien vers `client/dashboard.html`.
- Design : sobre, aubergine sur crème, onde audio CSS animée pendant l'enregistrement.

**Page praticien `praticien/audio-traiter.html`** (existe peut-être partiellement — enrichir) :

- Lecteur audio personnalisé pour écouter le dépôt client (fixture MP3 : `assets/audio/depot_camille_01.mp3`).
- Contrôles : lecture/pause, barre de progression cliquable, vitesse ×0.75 / ×1 / ×1.25, volume.
- Espace notes latéral : textarea libre, sans formatage imposé.
- Section "Enregistrer votre lecture en retour" : même interface que `audio-async.html`, déclenchée par bouton "Commencer la lecture". Limite 10 minutes.
- Bouton "Envoyer la lecture" → confirmation visuelle → retour vers `praticien/audios.html` avec le dépôt marqué "Traité".

**Page client `client/audio-resume.html`** :

- Lecteur de la lecture du praticien (fixture MP3 : `assets/audio/lecture_mylene_01.mp3`).
- Transcription textuelle simulée en dessous (mockup de 6-8 lignes — ton IVIA : clarté, pistes, sans jugement).
- Trois boutons d'état : "Intégré" (→ journal + marquage vert), "À réécouter" (→ rappel fictif dans 7 jours), "Interrompre la suite" (→ modale de confirmation + retour dashboard).
- Liens vers les pistes suggérées : `outil-ou-en-etes-vous.html`, `outil-frequence.html`, `journal.html`.

**Fixtures audio** : créer `ivia_mockups/assets/audio/` avec trois fichiers. Utiliser des tonalités ambiantes libres de droits ou des bips de test :
- `depot_camille_01.mp3` (ou `.ogg`) — simuler 90 secondes de voix
- `lecture_mylene_01.mp3` — simuler 3 minutes de lecture retour
- `silence_30s.mp3` — silence de 30 secondes pour les états d'attente

Si Copilot ne peut pas générer les MP3 directement, créer des fichiers de remplacement vides de 1 octet avec les bons noms et documenter dans un commentaire Python que ce sont des placeholders à remplacer par de vraies fixtures.

**Lecteur audio personnalisé** : un seul composant CSS/JS réutilisable (`shared/audio-player.js` + styles dans `shared/public.css`). Pas de `<audio controls>` natifs — le lecteur doit correspondre à la charte visuelle.

**Commit attendu** : `feat(audio): C8 - cycle audio client/praticien testable bout en bout`

---

### C9 — STATS PRATICIEN + DASHBOARD PUBLIC
**Priorité : moyenne — renforce la crédibilité doctrinale**

Les indicateurs sont définis dans `00_DOCTRINE/indicateurs_praticien_v1.md`. Ce chantier en expose un sous-ensemble réaliste sur trois niveaux : vue praticien, vue admin, panneau public landing.

**Vue praticien — enrichir `praticien/index.html` (dashboard)** :

Six indicateurs financiers simulés (revenu brut mensuel, revenu net après commission IVIA, taux d'occupation calendrier, panier moyen, taux de conversion visite-profil → réservation, lectures complétées vs annulées). Quatre indicateurs qualitatifs (note moyenne client, taux de re-réservation à 90 jours, taux de satisfaction déclarée post-livraison, ratio écoute complète audio). Trois indicateurs typologiques (motifs récurrents de dépôt, fréquences travaillées, tranche d'âge dominante). Deux indicateurs santé praticien (charge hebdomadaire déclarée, dernier jour sans séance). Deux indicateurs doctrinaux (score d'alignement vocabulaire — pourcentage de lectures utilisant le vocabulaire IVIA, taux d'autonomie client déclarée).

Tous ces chiffres sont simulés de manière réaliste (pas de zéros, pas de 100%). Représentation en SVG inline ou CSS pur — pas de Chart.js (alourdit inutilement, crée une dépendance externe). Barres de progression CSS, chiffres clés en grand format Fraunces, tendances en petites flèches Unicode (▲ ▼ →).

**Vue admin praticien — `admin/praticiens/[id].html`** (nouvelle page ou enrichissement de `admin/praticiens.html`) :

Agrégation des mêmes indicateurs pour chaque praticien. Alertes automatiques sur seuils : taux d'occupation < 20% pendant 3 semaines (→ badge orange "Appui suggéré"), note moyenne < 3.5 sur 30 jours (→ badge rouge "À vérifier"), charge hebdomadaire déclarée > 25 séances (→ badge orange "Attention charge"). Ces alertes sont simulées avec des données fictives cohérentes.

**Vue admin réseau — enrichir `admin/index.html`** :

Quatre métriques de santé du collectif : nombre de praticiens actifs, volume de lectures ce mois, taux de satisfaction global anonymisé, répartition géographique des clients (agrégée, sans données nominatives). Graphes en SVG inline.

**Dashboard public landing — section "En direct du collectif"** :

Ajouter dans `pages_public.py` une section sur `index.html` intitulée "En direct du collectif" avec quatre chiffres anonymisés et actualisés manuellement (fixtures JSON dans `assets/data/stats_public.json`) :
- Personnes accompagnées ce mois : ex. 47
- Fréquences mobilisées ce mois : ex. 12 registres distincts
- Régions touchées : ex. 9 régions du Québec
- Motifs récurrents anonymisés : ex. "transition · relation · sens"

Design sobre, chiffres en grand Fraunces aubergine, labels en Lora crème profonde, fond section aubergine léger. Pas de temps réel — mise à jour manuelle mensuelle par David via le fichier JSON.

**Commit attendu** : `feat(stats): C9 - dashboard praticien, vues admin, panneau public collectif`

---

### C10 — PIPELINE CONTENU DATA-DRIVEN
**Priorité : basse pour cette itération — préparer le terrain**

Ce chantier formalise le format des articles liés aux données observées sur la plateforme et à la veille documentée dans `00_DOCTRINE/dispositif_veille_ivia_v1.md`.

**Template à créer** : `ivia_mockups/articles_md/_template_data_driven.md`

```markdown
# [Titre : motif observé, formulé en vocabulaire IVIA]

**Saison** : [ex. printemps 2026]
**Motif de départ** : [ex. "Transition professionnelle — surreprésentation en mars-avril"]
**Source** : [Données internes anonymisées / Veille INSPQ / Veille culturelle]

## Ce qu'on observe ce mois

[2-3 phrases décrivant le signal, en données agrégées anonymisées. Pas de cas individuels.]

## Ce qu'un praticien en dit

[Témoignage praticien anonymisé, max 120 mots. Ton IVIA : présence, clarté, sans diagnostic.]

## Où ça peut mener

[Orientation IVIA en 3 points actionnables. Vocabulaire : déposer / traverser / avancer / repère / voie.]

---
*Article de la bibliothèque IVIA — à votre rythme, sans grille, sans jugement.*
```

**Section "Articles cette saison"** : dans `pages_public.py`, `build_bibliotheque()`, ajouter une section en tête de `bibliotheque.html` qui liste les 2-3 articles marqués `saison: active` dans leur frontmatter. Ces articles apparaissent en premier, avec un badge discret "Cette saison".

**Commit attendu** : `feat(contenu): C10 - template data-driven + section articles saison`

---

## 5. INTÉGRATION VEILLE

La veille documentée dans `00_DOCTRINE/dispositif_veille_ivia_v1.md` (six paliers : légal-réglementaire Québec, scientifique, marché-concurrent, culturel-signal, financement, technologique) doit être accessible à l'admin via une page dédiée.

**Page à créer** : `admin/veille.html` (via `pages_admin.py`)

Contenu simulé :
- Liste des sources surveillées par palier (reprendre les URLs de `dispositif_veille_ivia_v1.md`).
- Alertes du mois (3-4 alertes fictives réalistes — ex. "OPQ : communiqué du 2 mai sur l'encadrement de l'accompagnement non-réglementé. Analyse en cours.").
- Actions prises (colonne "Statut" : En analyse / Intégré / Sans suite).
- Vue admin uniquement — ne pas exposer cette page sur le site public.

Design : sobre, fonctionnel, glacier et aubergine. Tableau HTML standard, pas de fantaisie visuelle.

---

## 6. ESTIMATION GLOBALE

| Chantier | Estimation | Priorité |
|---|---|---|
| C1 → C5 (v1.0 complet) | 2h15 à 3h | Immédiate |
| C6 — Intégration charte botanique | ~2h | Haute |
| C7 — Calendrier fonctionnel | ~3h | Haute |
| C8 — Cycle audio testable | ~3h | Haute |
| C9 — Stats praticien + dashboard public | ~4h | Moyenne |
| C10 — Pipeline contenu data-driven | ~1h | Basse |
| **Total v2.0** | **~15-16h** | |

---

## 7. ORDRE D'EXÉCUTION RECOMMANDÉ

**Sprint 1 — Stabilisation et charte (4-5h)**
Exécuter C1 → C5 dans l'ordre décrit dans `04_METHODES/BRIEF_COPILOT_REFONTE_LANDING_LIENS_v1.0.md`, puis enchaîner avec C6 (CSS charte botanique). Push après C5, push après C6. Computer redéploie et fait la QA visuelle desktop + mobile (390px, 768px, 1280px) avant de valider le passage au Sprint 2.

**Sprint 2 — Calendrier (3h)**
C7 complet : fichier JSON fixtures, composant calendrier JS pur, page `praticien/agenda.html` enrichie, pages funnel réservation client. Push. Computer redéploie, QA visuelle + test parcours Mylène et Camille.

**Sprint 3 — Audio (3h)**
C8 complet : pages `audio-async.html`, `audio-traiter.html`, `audio-resume.html` vérifiées et complètes, lecteur audio personnalisé, fixtures MP3 ou placeholders documentés. Push. Computer redéploie, QA bout-en-bout cycle audio.

**Sprint 4 — Stats et dashboard (4h)**
C9 complet : indicateurs dashboard praticien, vues admin, section "En direct du collectif" sur landing, page `admin/veille.html` (C intégration veille). Push. Computer redéploie, QA visuelle sur les trois rôles.

**Sprint 5 — Contenu (1h, facultatif)**
C10 : template data-driven, section "Articles cette saison". Push. Computer redéploie.

---

## 8. POINTS DE VIGILANCE

**Loi 25 (protection des renseignements personnels)** : aucune donnée personnelle réelle ne doit figurer dans les fixtures JSON, les fichiers audio ou les données simulées. Les noms de clients fictifs dans les fixtures sont des pseudonymes : Camille Tremblay, Alexis Bergeron, Marie-Ève Laplante. Aucun numéro de téléphone, aucune adresse, aucun courriel réel.

**Loi 21 (encadrement de la psychothérapie)** : le vocabulaire sur toutes les pages créées ou modifiées ne doit jamais franchir la ligne psychothérapie. Les mots suivants sont interdits dans le contenu public et client : diagnostic, traitement, guérison, trouble, pathologie, psychothérapie, thérapie, thérapeute (dans le sens de prestataire IVIA), soin clinique. Voir section "À éviter" de `reference-visuelle.html` et la doctrine IVIA. Le champ lexical autorisé : écoute, interprétation, présence, clarté, repère, chemin, voie, déposer, traverser, avancer, rencontre, conversation, séance, équilibre, indépendance, autonomie vitale.

**Mobile-first** : tester systématiquement sur 390px avant desktop. Toute grille doit se stacker proprement. Tout texte doit rester lisible sans zoom. Tout bouton doit avoir une zone tactile de 44px minimum.

**Performance** : aucune dépendance externe non justifiée. Pas de Chart.js, pas de moment.js, pas de jQuery. Le calendrier (C7) est en JS pur. Le lecteur audio (C8) est en JS pur. Les charts (C9) sont en SVG inline ou CSS pur. Les polices Google Fonts peuvent être préchargées avec `preload` pour réduire le délai d'affichage.

**Bandeau Mode démo** : maintenir sur toutes les pages internes (client/, praticien/, admin/) le bandeau "Vous testez IVIA en mode démo · [Sortir du mode démo →]" pointant vers `../tests.html`.

---

## 9. LIVRAISON ATTENDUE DE COPILOT

Après chaque chantier, Copilot doit :

1. Lancer `cd ivia_mockups && python build_pages.py` et vérifier l'absence d'erreurs.
2. Tester le parcours minimal concerné sur `http://localhost:8000`.
3. Committer avec un message conventionnel :

```
feat(site): C6 - intégration charte botanique

- shared/public.css : palette La Coupe, Fraunces+Lora, espacements
- hero landing : illustration SVG botanique, vocabulaire aligné doctrine
- contraste WCAG AA vérifié sur combinaisons principales
- phasage : public CSS mis à jour, client/admin inchangés ce sprint

Build OK. Test local OK. Aucune violation palette.
```

4. Push sur `master` : `git push origin master`.
5. Écrire une entrée dans `04_METHODES/JOURNAL_COPILOT.md` (créer ce fichier au premier commit) :

```markdown
## 2026-05-09 — C6 intégration charte botanique

- Fichiers modifiés : shared/public.css, pages_public.py
- Temps estimé : 2h
- Points de friction : contraste bois-rose sur crème insuffisant en corps 14px — résolu en n'utilisant bois-rose qu'en 18px+
- Reste à faire : appliquer la charte aux espaces client au prochain sprint
```

Computer redéploie après validation du message de Copilot, effectue la QA visuelle (screenshots desktop 1280x900 + mobile 390x844), et remet la main à David avec un rapport court.

Les chantiers C7, C8 et C9 font l'objet d'une QA visuelle desktop et mobile approfondie par Computer avant de passer au sprint suivant.

---

**Au sein de l'être — En actes.**
**Pour le peuple, par le peuple.**

*Brief Copilot v2.0 — 9 mai 2026*
*David Phaneuf, fondateur IVIA*
*Préparé par Computer (Perplexity)*

# AUDIT SANS FILTRE — LES TROIS INTERFACES (client · praticien · admin)

**Version** : 1.0 — 18 juillet 2026
**Statut** : Audit + plan d'évolution priorisé — aucun code modifié
**Auteur** : Claude Code (mandat fondateur, prompt d'audit du 18 juillet)
**Méthode** : cartographie automatisée écran→endpoint (115 fonctions d'`api.js` + appels directs), lecture ciblée du code, aucun fait affirmé sans chemin de fichier. Les hypothèses de conception sont marquées *[opinion]*.
**Périmètre** : `ivia_site_v2/{client,praticien,admin,design-system}` + tunnel public · 49 routeurs de `10_backend_merlin_api/app/api/routes/`.

---

## 1. CARTOGRAPHIE — le réel, pas le supposé

### 1.1 Interface CLIENT (20 écrans : 13 branchés · 7 mockups)

| Écran | État | Branché sur |
|---|---|---|
| journal.html | ✅ | getMyJournal, createMyJournalEntry, getMyBookings, getMyDocuments, getMyRecordings, listMyReflets, requestMyReflet |
| carte-de-vie.html | ✅ | getMyCarteDeVie, getMyDocuments, getMyJournal, listMyReflets, `/referentiels/axes` |
| mon-reflet.html | ✅ | listMyReflets, listMyReperes, listMyExercises, updateMyExercise, requestMyReflet |
| ma-progression, seances, mes-resumes, mes-enregistrements, enregistrement, mon-profil, compte, dashboard, seance-express-join | ✅ | me_journal, me_recordings, me_documents, bookings, express, clients/me, auth |
| **premier-ancrage.html** | ⚠️ **faux branché** | POST `/api/v1/client/ancrage` **n'existe pas** — sauvegarde localStorage (ligne 523 : « Mock save ») |
| **agenda.html** | ❌ mockup | doublon : la réservation réelle vit dans `/reserver.html` (shared/reservation.js) |
| **journal-nouvelle-entree.html** | ❌ mockup | doublon de journal.html (qui crée déjà des entrées) |
| **mes-reperes.html** | ❌ mockup | doublon : listMyReperes est branché… dans mon-reflet.html |
| **mes-exercices.html** | ❌ mockup | doublon : listMyExercises branché dans mon-reflet.html |
| **mot-de-passe-oublie.html** | ❌ mockup | aucune route reset dans `app/api/routes/auth.py` (vérifié) |
| **seance.html / seance-active.html** | ❌ mockups | voir parcours A — la séance en direct n'a pas d'UI |

### 1.2 Interface PRATICIEN (13 écrans : 12 branchés · 1 statique)

Tous branchés : agenda (schedules/bookings/exceptions), clients-journal (clients + journal), dashboard (sessions, notes, `/me/appointments/stats`), compte-rendu-seance (getSessionNote, validateSessionNote, createDerivedDocument), preparation (apiSessionPreparation, exercices, deliverAnalysis, withdrawDelivery), livraisons (sessions, sendClientFollowup, archive/delete), seance-express (createExpressSession), profil (profil/tarifs/schedules/audio-profile), carte-de-vie (getClient, getClientAnalyses, getClientLifeEvents), ma-pratique (retours/reflets pratique), fiche (listPraticiens), compte. `guide.html` = contenu statique (acceptable par nature).

### 1.3 Interface ADMIN (11 écrans : 10 branchés · 1 landing)

Tous branchés sur leurs routeurs admin_* : vue (adminOverview), demandes (adminListIntake + adminUpdateIntakeHandling + listPraticiens pour assigner), dossiers (adminListClients, adminClientDossier), comptes (8 actions), analyses (capabilities + credentials), lectures (session types + exercices), comptabilite (summary + ledger), economie (summary + sessions), facturation (billing flags **seulement**), connexion. `index.html` = landing sans données.

### 1.4 Tunnel public

inscription.html → register ✅ · connexion → auth ✅ · activer.html → `/public/activate/{token}` ✅ · reserver.html → flux complet praticien→créneau→hold→Stripe (shared/reservation.js, garde de session en ligne 6) ✅ · ecoute.html, ou-en-es-tu.html = contenu pur (0 appel — assumé) · checkout/success, attente, confirmation = pages d'état.

### 1.5 Capacités backend SANS interface (endpoints invisibles)

Routeurs sans aucun appel frontend détecté (api.js + toutes pages scannés) :

| Routeur | Ce qui dort |
|---|---|
| **consents** (7 routes) | consultation/gestion des consentements — capture OK côté backend, **aucune UI client pour voir ou retirer** |
| **public_intake `/intake/start`** | l'orchestrateur magic-link « client + intake + consentements + lien » (public_intake.py:189) — **l'entrée publique réelle passe par inscription.html classique** ; le magic link n'est consommé (activer.html) que si quelque chose crée l'intake… et rien côté public ne le crée |
| **audio_sessions + audio_recordings** | l'infra LiveKit (jetons, salles) — **zéro référence LiveKit dans tout ivia_site_v2** (vérifié) |
| **organization_leads** | les leads employeurs — **employeurs.html / travail.html n'ont aucun formulaire branché** ; le marché Loi 27 du BP n'a pas de porte d'entrée |
| **timeline** | le fil chronologique client — construit, jamais affiché |
| **matching** | l'appariement client↔praticien — le tunnel n'en fait rien |
| calendar, client_entitlements, era_contexts, profiling | idem — stockés/servis, jamais montrés |
| createClientLifeEvent (helper api.js) | les ancrages temporels sont affichés (carte-de-vie praticien) mais **aucune page ne permet d'en créer** |

---

## 2. TROIS PARCOURS DE BOUT EN BOUT

### A. Client : premier dépôt → analyse → restitution

`ecoute.html` → `reserver.html` (session requise, sinon `connexion.html`) → `inscription.html` → `premier-ancrage.html` → dépôts (journal/enregistrement) → analyse → `mon-reflet.html`.

**Où ça casse** :
1. 🔴 **Le premier ancrage est perdu.** L'écran d'accueil du parcours (contexte, rythme, limites — la matière la plus précieuse du premier contact) sauvegarde en localStorage (`client/premier-ancrage.html:523`) : jamais transmis au serveur, invisible pour le praticien, perdu au changement d'appareil.
2. 🔴 **La séance promise n'a pas de salle.** reservation.js promet « Format : Audio en direct » ; le backend LiveKit tourne (audio_sessions, jetons) ; `client/seance.html` et `seance-active.html` sont des mockups et **aucune page ne monte LiveKit**. Fait constaté : la séance réservée se déroule nécessairement hors plateforme. *[opinion : si l'express est la voie assumée du pilote, il faut le dire dans l'UX et retirer les mockups ; sinon c'est le trou produit n° 1.]*
3. 🟠 Le magic link « accueil sans friction, 3 consentements » (feuille de route innovation : « Livré ») n'est **pas raccordé** : pas d'appelant pour `/public/intake/start`.
4. 🟠 Consentement : bien capturé à la source (public_intake.py:261, express.py:176, me_recordings.py:247) — mais **aucune UI de consultation/retrait** (7 routes consents muettes). Droit Loi 25 non outillé côté client.
5. 🟡 Restitution : mon-reflet ✅ réel (reflets, repères, exercices). Mais mes-reperes.html/mes-exercices.html mockups en doublon créent deux vérités d'écran pour la même donnée.

### B. Praticien : préparation → séance → compte-rendu → livraison

preparation.html (préparation, exercices, livraisons/retraits) → séance **express** (createExpressSession + lien client) ou rendez-vous agenda → compte-rendu-seance.html (note, axes, validation) → livraisons.html (suivi, relance client).

**État** : le parcours est **réel et complet côté données** — c'est l'interface la plus aboutie. Où ça casse :
1. 🟠 Même trou que A-2 : entre l'agenda (rendez-vous confirmé) et le compte-rendu, la **conduite** de la séance standard n'existe pas dans le produit ; la fiche rendez-vous renvoie vers préparation seulement si une séance/matière existe déjà (`praticien/agenda.html`, ouvrirModalRdv).
2. 🟡 Ancrages temporels : lecture seule (A-carte-de-vie) — le praticien ne peut pas consigner un événement biographique entendu en séance (helper existant, jamais monté).
3. 🟡 Deux entrées pour « mes clients » : clients-journal liste **tous** les clients (`GET /clients`, require_internal_clinical_roles — pas de filtre d'assignation) : au-delà du pilote, un praticien voit les clients des autres. *[fait : clients.py:48-55 ; opinion : à filtrer par assignation avant d'élargir le pilote.]*

### C. Admin : demande entrante → assignation → suivi analyses → facturation

demandes.html (intake + handling + assignation praticien) ✅ → dossiers.html (vue consolidée) ✅ → analyses.html (capacités par profil + accréditations) ✅ → comptabilite/economie ✅.

**Où ça casse** :
1. 🔴 **Minimisation Loi 25** : `admin/dossiers.html:91` affiche la **transcription intégrale** de chaque enregistrement client (« Voir la transcription », `admin_clients.py:208` la sert). Protégé par require_admin, mais un rôle d'administration n'a pas besoin du verbatim de la parole pour opérer — c'est l'écart le plus net entre la doctrine (exposition minimale) et le produit. *[opinion : remplacer par métadonnées + accès exceptionnel journalisé.]*
2. 🟡 facturation.html ne fait que des billing flags — le nom promet plus que l'écran ne tient (la vraie matière est dans comptabilite.html).
3. 🟡 La chaîne intake → assignation existe, mais sans `/intake/start` public (A-3), les demandes n'arrivent que si quelqu'un les crée à la main.

---

## 3. DIAGNOSTIC SANS FILTRE

### CLIENT
- **Faible/cassé** : premier-ancrage factice (preuve §A-1) ; séance live absente (§A-2) ; reset mot de passe inexistant (pas de route dans auth.py — un client qui oublie son mot de passe est bloqué, point) ; 7 écrans sur 20 sont des mockups ou doublons.
- **Incohérent** : repères/exercices vivent à la fois dans mon-reflet (réel) et mes-reperes/mes-exercices (faux) ; agenda client (faux) vs reserver (réel).
- **Manquant pour tenir la promesse** : la salle de séance ; la gestion des consentements ; l'ancrage transmis au praticien.

### PRATICIEN
- **Faible** : rien de cassé — c'est l'interface la plus saine. Le guide est statique (assumé).
- **Incohérent** : « tous les clients » au lieu de « mes clients » (§B-3) ; ancrages temporels affichés mais non créables.
- **Manquant** : la conduite de séance standard ; une vue de l'équilibre des axes dans le temps (les données existent, note par note).

### ADMIN
- **Faible** : facturation.html squelettique.
- **Risqué** : transcripts intégraux (§C-1).
- **Manquant** : un tableau réseau agrégé (les routeurs economics/analyses le permettraient) ; la création manuelle d'une demande d'entrée (téléphone/courriel entrant).

---

## 4. AMÉLIORER / AJOUTER / CHANGER

### CLIENT
| Type | Proposition | Problème résolu | Effort | Touche |
|---|---|---|---|---|
| AMÉLIORER | Brancher premier-ancrage sur un vrai endpoint (`PATCH /clients/me` étendu ou table dédiée) | matière du premier contact perdue | **S/M** | les deux |
| AMÉLIORER | Reset mot de passe (route + page) | client bloqué | **M** | les deux |
| AJOUTER | Page « Mes consentements » (7 routes prêtes) | droit d'accès/retrait Loi 25 | **M** | front |
| AJOUTER | Salle de séance LiveKit (ou décision produit contraire) | promesse « audio en direct » | **L** | les deux |
| CHANGER/RETIRER | Retirer de la nav : agenda, journal-nouvelle-entree, mes-reperes, mes-exercices, seance*, ou les fusionner dans leurs écrans réels | deux vérités d'écran | **S** | front |

### PRATICIEN
| Type | Proposition | Problème résolu | Effort | Touche |
|---|---|---|---|---|
| AMÉLIORER | « Mes clients » filtré par assignation (sessions/bookings) | confidentialité inter-praticiens | **M** | backend |
| AJOUTER | Création d'ancrage temporel depuis carte-de-vie (helper déjà écrit) | mémoire biographique vivante | **S** | front |
| AJOUTER | **Radar d'équilibre des axes** par client (profile-radar.js existe déjà dans design-system !) alimenté par les notes cumulées | l'équilibre CERCLE devient visible, pas juste stocké | **M** | front (+1 endpoint agrégé) |
| AJOUTER | Timeline client (routeur timeline muet) dans préparation | contexte instantané avant séance | **M** | front |

### ADMIN
| Type | Proposition | Problème résolu | Effort | Touche |
|---|---|---|---|---|
| CHANGER | Dossiers : métadonnées seulement, transcript sur action explicite journalisée (« accès exceptionnel — motif ») | minimisation Loi 25 | **M** | les deux |
| AMÉLIORER | Facturation : soit y monter le ledger, soit renommer « Options de facturation » | promesse d'écran | **S** | front |
| AJOUTER | Formulaire employeurs → organization_leads + vue admin des leads | ouvrir la porte Loi 27 (marché du BP) | **M** | front |
| AJOUTER | Création manuelle de demande d'entrée | demandes téléphone/courriel | **S** | front |
| AMBITIEUX | Tableau réseau anonymisé (charge praticiens, axes dominants agrégés, signaux d'urgence) | pilotage réseau | **L** | les deux |

---

## 5. CONFORMITÉ & DOCTRINE

1. **Loi 21 — vocabulaire : conforme.** Toutes les occurrences trouvées côté client sont des démarcations (« pas de diagnostic », « pas une psychothérapie » — attente.html:56-96, cgu.html:24, ecoute.html:7). Aucune promesse clinique détectée.
2. 🔴 **Loi 25 — responsable du traitement erroné** : `confidentialite.html:28` désigne « IVIA inc. », **entité qui n'existe pas encore** (trajectoire canonique : entreprise individuelle → OBNL → SPA, BP v2.4 §2.1.0). Les mentions légales v0.3 ont été corrigées le 17 juillet, la politique du site non — récidive du bloquant B2 de `AUDIT_COHERENCE_POST_DEC-V3-15.md`.
3. 🟠 **Consentements** : capture solide aux trois points d'entrée (public_intake.py:261, express.py:176, me_recordings.py:247) ; **retrait/consultation non outillés** (routeur consents muet).
4. 🔴 **Minimisation** : transcripts intégraux dans la console admin (§C-1).
5. **CERCLE — écart doctrinal à trancher** : le mandat d'audit affirme « CERCLE à 4 axes HUMAIN·SOCIÉTÉ·PEUPLE·TERRE… existe déjà en base (migration 20260422_0005) ». **Fait constaté** : cette migration crée `coeur/corps/esprit/etre_summary_text` — le cadre en production est **Cœur·Corps·Esprit·Être**, produit par `app/ai/prompts/session_note_cercle_v1.py`, affiché au praticien (compte-rendu-seance.html:156). HUMAIN·SOCIÉTÉ·PEUPLE·TERRE n'apparaît nulle part dans le code applicatif (les seules occurrences sont des commentaires sans rapport). Les deux cadres coexistent dans la doctrine documentaire ; le code n'en connaît qu'un. **À arbitrer avant tout chantier « exploitation des axes »**.
6. **Exploitation réelle des axes** : produits par l'IA ✅, stockés ✅, affichés dans le compte-rendu ✅ et la carte de vie client (referentiels/axes) ✅ — mais **aucun calcul d'équilibre** (« aucun axe critique sans réponse ») ni vue longitudinale : aujourd'hui c'est une lecture par séance, pas un instrument de suivi.

---

## 6. PLAN EN 3 VAGUES

### Vague 1 — Quick wins (< 1 jour, ordre exact)
1. **confidentialite.html** : responsable du traitement aligné sur la trajectoire réelle (même formulation que mentions légales v0.3) — conformité, 30 min.
2. **premier-ancrage** : brancher la sauvegarde (extension `PATCH /clients/me` ou champ JSON) — arrêter de perdre la matière du premier contact.
3. **Nav client** : retirer/fusionner les 5 écrans doublons ou morts (agenda, journal-nouvelle-entree, mes-reperes, mes-exercices, mot-de-passe-oublie tant que le reset n'existe pas).
4. **facturation.html** : renommer ou monter le ledger.
5. **Ancrage temporel praticien** : monter createClientLifeEvent dans carte-de-vie (helper prêt).

### Vague 2 — Structurant (1-2 semaines)
- **Décision produit séance** : salle LiveKit dans l'espace (les deux côtés) OU express assumé comme mode unique du pilote (alors retirer seance*.html et documenter le déroulé). C'est LA décision qui débloque le reste.
- Reset mot de passe complet (route + courriel + page).
- Page « Mes consentements » client (+ retrait).
- Admin dossiers : passage en métadonnées + accès transcript journalisé.
- Formulaire employeurs → organization_leads (porte Loi 27).
- « Mes clients » filtré par assignation.
- Raccorder `/public/intake/start` à l'entrée publique (le magic link conçu).

### Vague 3 — Ambitieux
- **Radar d'équilibre des axes** par client, longitudinal (design-system/profile-radar-demo.html attend exactement ça) + règle d'équilibre doctrinale (« axe critique sans orientation » signalé au praticien).
- Timeline client dans la préparation (routeur prêt).
- Matching au tunnel public (routeur prêt).
- Tableau réseau anonymisé admin.
- Boucle d'apprentissage : retours ma-pratique → registre d'évals (managed_agents/evals.registry.yaml).

---

*Non vérifié dans cet audit : le comportement runtime des parcours (audit statique du code, pas de session de test bout en bout) ; la couverture des rôles sur chaque routeur admin au-delà de admin_clients ; l'état exact des workers/livekit côté infra.*

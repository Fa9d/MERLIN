# Référence — Fonctionnement des apps IVIA

> Document factuel produit par lecture directe du code source (`/home/user/workspace/MERLIN/ivia_site_v2/`). Rien n'est déduit au-delà de ce que le HTML/JS affiche ou manipule. Quand une page est majoritairement pilotée par JS (fetch API, rendu dynamique), c'est signalé explicitement, avec les chaînes de texte lues dans les `<script>`.

---

## Vue d'ensemble

Le produit s'appelle **IVIA** (le contenu technique interne — noms de champs, axes — utilise aussi le sigle **MERLIN**, ex. `axe MERLIN` dans l'admin). C'est une plateforme québécoise de santé mentale/bien-être. Le site est constitué de **pages HTML statiques** enrichies par du **JavaScript côté client** qui appelle une API REST (`shared/api.js`, hôte `https://api.ivia.quebec/api/v1/...` observé dans `carte-de-vie.html`) pour charger et écrire les données. Il existe **trois zones applicatives** :

- **App CLIENT** (`/client/*.html`) — l'espace des personnes accompagnées. Thème clair (fond crème `--cream`, vert forêt `--forest`).
- **App PRATICIEN** (`/praticien/*.html`) — l'espace des praticien·nes (hors périmètre strict de ce document, mais référencée depuis l'admin via le lien « ← Espace praticien »).
- **App ADMIN** (`/admin/*.html`) — la console d'administration technique. Thème sombre pour la barre latérale (`#13261A`), réservée aux comptes avec le drapeau `is_admin`.

**Vocabulaire de marque confirmé dans le code :**
- **« les deux gestes »** : les deux actions principales du tableau de bord client — *Réserver* et *Séance expresse*.
- **« les trois lieux de la maison »** : Journal, Miroir, Horizon — la métaphore de la « maison » structure tout l'espace client (« l'état de la maison » apparaît aussi côté admin).
- **Journal · Miroir · Horizon** : le triptyque de navigation principal de l'app client.
- **« onze axes »** : les onze axes de la constellation radiale dans Horizon (territoire/fondateur au centre, corps, métabolisme, émotions, mental, relations, famille, transgénérationnel, société, spirituel/existentiel, repère/urgence).
- **« ligne de vie » / « carte de vie »** : la chronologie de vie, présente à la fois dans Horizon (`carte-de-vie.html`) et dans Ma progression (bloc « Ligne de vie »).
- **« reflet » / « miroir »** : une réflexion générée par IA, demandée par le client à partir de ses entrées de journal ou de ses enregistrements.
- **« repères »** : synthèses en triade (observation / hypothèse / orientation) curées par le praticien, distinctes des « miroirs » (auto-demandés) et des « résumés » (reformulations écrites déposées par le praticien).
- **« ancrage »** : le parcours d'onboarding `premier-ancrage.html` ; le profil de base en 6 dimensions y est aussi appelé **« cercle de départ »**.
- **Triade répétée** (Miroir / Repères / Horizon / L'Atelier des lectures) : *« Ce qui s'observe »* → *« Une hypothèse, prudente »* → *« Une orientation »* (ou *« piste »*), libre.
- **« jalons »** : palier gamifiés (8 badges d'accomplissement) sur la page Ma progression.
- Système d'**Ambiance** (thème visuel) : bascule *Signature / Doux*, stockée dans `localStorage` sous `ivia_recorder_theme`.
- Conformité : **Loi 25** (protection des renseignements personnels, Québec) et **Loi 21** (vocabulaire professionnel encadré, citée côté admin dans « L'Atelier des lectures »). Données « hébergées au Canada ».
- Ressources de crise systématiquement rappelées : **9-8-8** (ligne de crise 24/7), **Info-Social 8-1-1** (option 2), **9-1-1**, et **1 866 APPELLE (277-3553)** (page inscription).
- Tarification observée : séance live 30 min = **49 $**, 1 h = **75 $** ; enregistrement + rappel 10 min = **35 $** (nommé `enr_rappel` côté admin/facturation).

---

## Parcours d'entrée (inscription → vérif email → activation → connexion → premier ancrage)

Toutes les pages publiques sont à la racine du site.

### `inscription.html` — « Créer mon espace »
- **But** : créer un compte, en tant que client·e ou praticien·ne (bascule « Rejoindre IVIA comme praticien·ne »).
- **Champs** : Prénom, Nom, Courriel, Téléphone, sélecteur « Comment avez-vous entendu parler d'IVIA », Mot de passe (min. 12 caractères, indicateur de force), + champs praticien-only si ce rôle est choisi.
- **Consentements** : case N1 (obligatoire) et N2 (optionnelle), conformité Loi 25.
- **CTA** : « Créer mon espace ».
- **Comportement notable** : les inscriptions praticien sont bloquées en phase pilote (message renvoie vers bonjour@ivia.quebec).
- **Succès** : écran « Vérifiez votre boîte courriel » + bouton « J'ai confirmé — me connecter » → `connexion.html`.
- Ressource de crise en pied de page : 1 866 APPELLE (277-3553).

### `connexion.html` — « Se connecter »
- **But** : authentification.
- Bascule de rôle Client·e / Praticien·ne.
- **Champs** : Courriel, Mot de passe, lien « Mot de passe oublié ? » → `/client/mot-de-passe-oublie.html`.
- **CTA** : « Se connecter ».
- Le paramètre `?verif=1` affiche une bannière avec « Renvoyer le lien ».
- Lien vers `inscription.html` en bas de page.

### `verify-email.html`
- Page purement dynamique. Trois états gérés par JS après appel `apiVerifyEmail(token)` :
  1. chargement,
  2. succès — « Courriel confirmé. » + bouton « Me connecter »,
  3. erreur — « Ce lien ne fonctionne pas. » + bouton « Recommencer l'inscription ».
- Lit les paramètres `?token=` et `?redirect=` dans l'URL.

### `activer.html` (lien magique)
- **H1** : « Bienvenue dans la maison du vivant. »
- **CTA** : « Ouvrir mon espace IVIA » → connexion automatique → redirection `/client/dashboard.html`.
- En cas d'erreur : « Recommencer une demande » (→ `/rendez-vous.html`) ou « J'ai déjà un compte » (→ `/connexion.html`).

### `reserver.html` et `rendez-vous.html`
- `reserver.html` exige l'authentification et monte le flux de réservation partagé (`shared/reservation.js`, fonction `renderReservationFlow('reservation-flow')`).
- `rendez-vous.html` est une simple redirection vers `/reserver.html` (en conservant les paramètres de requête).

### `mot-de-passe-oublie.html` — « Mot de passe oublié »
- **Champ** : email.
- **CTA** : « Envoyer le lien de réinitialisation ».
- Message de confirmation « Courriel envoyé » affiché systématiquement (que le compte existe ou non — pratique de sécurité standard), avec lien « Retour à la connexion ».

### Flux de réservation partagé (`shared/reservation.js`) — utilisé par `reserver.html` ET `client/agenda.html`
Indicateur en 3 points : **Praticien·ne → Créneau → Confirmer**.
1. **Étape 1 — « Choisir un·e praticien·ne »** : sous-titre « Toutes les praticien·nes IVIA sont formé·es à la même approche — votre choix est intuitif. » Cartes praticien (nom, ligne de titre, texte d'intro, lecture audio optionnelle) avec CTA « Voir les disponibilités → ». Données via `listPraticiens()`.
2. **Étape 2 — « Créneau »** : calendrier mensuel, créneaux disponibles surlignés, pastilles horaires. Durées fixes selon `?formule=` (30 min = 49 $, 1 h = 75 $). Retour « ← Votre praticien·ne ».
3. **Étape 3 — « Confirmer »** : blocage temporaire de 15 min du créneau (`holdSlot()`, minuteur), récapitulatif + note optionnelle, CTA « Confirmer et payer → » → `bookingCheckout()` → paiement Stripe (redirections `/checkout/success.html` / `/checkout/cancel.html`). Email non vérifié → redirection `/connexion.html?verif=1`.

### Après connexion : premier ancrage
Le nouvel utilisateur est ensuite invité au parcours `premier-ancrage.html` (voir section Client ci-dessous) avant l'utilisation courante de l'espace.

---

## APP CLIENT

### Navigation (menu principal + étendu)
Source : `shared/layout.js`.

- **Menu principal (IVIA_NAV)** : *Mon espace* (`/client/dashboard.html`) · *Journal* (`/client/journal.html`) · *Miroir* (`/client/mon-reflet.html`, fil d'Ariane « Miroir ») · *Horizon* (`/client/carte-de-vie.html`, fil d'Ariane « Horizon »).
- **CTA d'en-tête** : bouton « Séance express » → `/client/enregistrement.html`.
- **Menu déroulant (☰ « Mon compte »)** : bascule d'Ambiance (Signature/Doux), Mon espace, Journal, Miroir, Horizon, séparateur, Séance expresse, Réservation (`/client/agenda.html`), Mon profil (`/client/mon-profil.html`), séparateur, Déconnexion.
- **Pied de page — « Espace client »** : Mon espace, Journal, Mon reflet, Vie, Réserver une séance, Mes séances, Mes enregistrements, Mes exercices, Mes repères, Mes résumés, Séance expresse, Mon compte.
- **Pied de page — « Services »** : Pourquoi IVIA, Pour les praticiens, Réserver une séance.
- **Pied de page — « Ressources »** : 9-8-8 Ligne de crise (24/7) — https://988.ca/fr, Info-Social 8-1-1, Urgence 9-1-1.
- **Pied de page — « Légal »** : Confidentialité, CGU, Mentions légales.
- **Signature du pied de page** : « IVIA — In Vivo, In Actu · Données hébergées au Canada (Loi 25) » / « Pas un service d'urgence · En crise : 9-8-8 · 811 option 2 ».
- **Icône de marque** : logo à trois barres verticales (SVG), mot-symbole « IVIA ».

### `dashboard.html` — « Mon espace »
- **H1** : « Bonjour {prénom}. »
- **But** : point d'entrée quotidien, hub central.
- **Sections** : « les deux gestes » — carte *Réserver* (→ `/client/agenda.html`) et carte *Séance expresse* (→ `/client/enregistrement.html`) ; « les trois lieux de la maison » — cartes Journal, Miroir, Horizon.
- Charge le profil via `apiMe()`.

### `journal.html` — « Journal »
- **Page fortement dynamique** (952 lignes) ; texte visible en grande partie généré par JS.
- **Sections** :
  - « Analyse du jour » — carte résultat générée côté client (résumé, observation, hypothèse, orientation) via `analyserJournee`.
  - Entrée rapide — zone de texte « Écriture libre » + bouton « Enregistrer ».
  - Bloc dépliable **« Mon Architecte intérieur »** — check-in structuré : sélecteur Humeur globale (icônes 🔴🟡🟢🔵), curseur Énergie (1-10), Sommeil, cases HeartMath, déclencheurs de stress, « Moment de grâce », « Leçon du jour », « Score de résilience » calculé en direct, bouton « Enregistrer la version structurée ».
  - « Mon journal » — journal chronologique avec navigation par date, bascule Jour/Semaine/Mois, bouton « Analyse du jour » (appelle `requestMyReflet`).
- **Appels API** : `getMyJournal()`, `getMyDocuments()`, `listMyReflets()`, `getMyRecordings()`, `getMyBookings()`, `createMyJournalEntry()`, `requestMyReflet()`.

### `journal-nouvelle-entree.html` — « Nouvelle entrée »
- **Statut** : probablement une page **legacy/non utilisée** — le gestionnaire de soumission est un stub (`setTimeout`, aucun appel API réel).
- **Champs** : chips de « registre » (Corporel / Émotionnel / Spirituel / Relationnel / Mental, max 3), zone de texte « Ce que je porte aujourd'hui » (2000 caractères), points d'Intensité (1-5).
- **Boutons** : « Annuler » / « Enregistrer l'entrée → ».

### `mon-reflet.html` — « Miroir »
- **Sous-titre** (paraphrasé du contenu) : distinguer voir ses propres schémas plutôt que les vivre à travers autrui.
- **4 sections sur une seule page** :
  1. **« Recevoir un miroir »** — bascule Jour/Semaine/Mois, CTA « Recevoir le miroir de ma semaine » → `requestMyReflet(periode)`.
  2. **« Mes miroirs »** — liste dépliable (fils, question_ouverte, piste) ; encart d'urgence (renvoi 9-8-8/811) si `vigilance.niveau === 'urgence'`.
  3. **« Mes repères »** — triade praticien (observation / hypothèse / orientation).
  4. **« Exercices »** — exercices assignés par le praticien (boutons selon statut : « Je commence » / « J'ai fait » / « Je le mets de côté » / « Je réessaie ») + 3 pratiques libres statiques (Cohérence cardiaque 4-7-8, Respiration carrée 4-4-4-4, Ancrage 5 sens).
- **Note importante** : `mes-reperes.html` et `mes-exercices.html` sont des redirections simples vers les ancres `#reperes` / `#exercices` de cette même page — ce ne sont pas des contenus distincts.

### `carte-de-vie.html` — « Horizon » (H1 : « Horizon émotionnel »)
- **But** : représentation visuelle multi-axes de l'état émotionnel/relationnel du client.
- **Contenu** : constellation radiale en D3.js des **onze axes** (territoire = centre/fondateur, corps, métabolisme, émotions, mental, relations, famille, transgénérationnel, société, spirituel/existentiel, repère/urgence), chacun avec un état de résonance (sourdine / présent / actif / tension).
- « Champs de tension » : intensité faible / modérée / marquée.
- « Progression » — curseur qui parcourt la chronologie.
- « Ce qui a bougé » — différences entre deux points dans le temps.
- Bloc dépliable **« Lecture complète »** : « Le sol », « Le fil à tirer », « La lecture, en trois temps » (Ce qui s'observe / Une hypothèse, prudente / Une orientation, libre).
- **Données** : `getMyCarteDeVie()`, `listMyReflets()`, `getMyDocuments()` ; axes récupérés depuis `https://api.ivia.quebec/api/v1/referentiels/axes` (avec liste de repli locale).

### `agenda.html`
- **But** : réservation de séance, accessible depuis l'espace client.
- Enveloppe fine reprenant le même flux de réservation que `reserver.html` (voir plus haut), montée dans la coquille applicative via `renderLayout('aujourdhui','Réservation')`.

### `seances.html` — « Mes séances »
- **But** : vue calendrier mensuel des rendez-vous (`getMyBookings()`) superposé aux entrées de journal (`getMyJournal()`).
- **Badges** : À venir / Passée / À confirmer.
- **CTA d'en-tête** : « Réserver une séance » → `/reserver.html`.
- **Lien** vers `/client/mes-enregistrements.html` (« vos enregistrements solo → »).

### `seance.html` — « Votre séance »
- **But** : salle de séance en direct synchronisée, en 3 phases : salle d'attente → séance active → fin.
- **Mécanisme** : `BroadcastChannel` + sondage `localStorage` pour signaler l'arrivée du praticien ; bouton de démonstration « [Démo] Simuler l'arrivée du praticien ».
- Enregistrement via `MediaRecorder`, bloc de notes « Mes notes » (raccourci Ctrl+Entrée pour horodatage).
- **CTA** : « Terminer ma séance → ».
- **Écran final** : « Séance terminée. » + boutons « Garder mon audio » / « Mon espace → ».

### `seance-active.html`
- Implémentation alternative/parallèle d'une salle de séance en direct (chevauchement notable avec `seance.html` — probablement deux versions du même concept, à signaler comme telle).
- Salle d'attente « Votre espace est prêt », compte à rebours 3-2-1, bouton « Je suis prêt·e → », enregistrement, CTA « Terminer ma séance → ».

### `seance-express-join.html`
- **But** : page de jointure basée sur un jeton (`?token=`) pour des sessions d'enregistrement express envoyées par un praticien — potentiellement à un·e client·e ou à un·e « Invité·e ».
- **États** : chargement / lien invalide / « Enregistrement déjà reçu » / prêt.
- **Contenu affiché** : nom du praticien, durée, statut de paiement (gratuit / prépayée / à régler après), badge « Loi 25 · Voix effacée à J+30 ».
- **Flux** : enregistrer → pause/reprise/arrêt → écoute/relecture (« Réécoutez avant d'envoyer ») → case de consentement → CTA « Envoyer à mon praticien·ne → » → confirmation « Merci — votre voix est bien arrivée. »
- **API** : `getExpressSession(token)`, `uploadExpressRecording(token, {...})`.

### `enregistrement.html` — « Enregistrer ma voix » (Séance expresse)
- **But** : enregistreur solo personnel, atteint depuis le CTA d'en-tête « Séance express ».
- Sélecteur de thème (Signature/Doux).
- **États** : idle → enregistrement ↔ pause → terminé.
- **Boutons** : « Enregistrer » / « Pause » / « Réinitialiser » / bouton principal dynamique (Enregistrer → Terminer → « Envoyer à IVIA »).
- **Navigation basse** : Journal / Enregistrer (actif) / Espace.
- **À l'envoi** : `uploadMyRecording({audio_data, filename, formule:'libre', duration_seconds})` → message de succès « Reçu — transcription en cours » + CTA « Aller à mon espace » → `/client/mes-enregistrements.html`.

### `mes-enregistrements.html` — « Mes enregistrements »
- **Sous-titre** : « Vue synthèse de vos séances passées : indicateurs et repères, sans transcription complète. »
- **Indicateurs (KPI)** : Séances captées, Minutes cumulées, Moyenne/séance, 30 derniers jours.
- **Liste « Mes séances enregistrées »** — bouton « Recevoir ma lecture » par item (visible seulement si `transcript_ready`) → `requestSeanceReflet(id)` → redirige vers `/client/mon-reflet.html`.
- **« Repères par mois »** — cartes de chronologie.
- **CTA d'en-tête** : « Enregistrer » → `/client/enregistrement.html`.
- **État vide** : CTA « Premier enregistrement ».

### `mes-exercices.html`
- **Redirection simple confirmée** vers `/client/mon-reflet.html#exercices` (`location.replace`).

### `mes-reperes.html`
- **Redirection simple confirmée** vers `/client/mon-reflet.html#reperes`.

### `mes-resumes.html` — « Mes résumés de séance »
- **Sous-titre** : « Les reformulations que votre praticien·ne a déposées pour vous, après relecture. À lire à votre rythme. »
- Liste via `getMyDocuments()`.
- **État vide** : « Après une séance, votre praticien·ne peut déposer ici une reformulation — un repère écrit, rien que pour vous. »
- Contenu distinct des « reflets » (auto-demandés) et des « repères » (Miroir) : ce sont des synthèses écrites par le praticien.

### `ma-progression.html` — « Ma progression »
- **Sous-titre** : « Ce que vos traces réelles dessinent — séances, journal, repères. Rien d'inventé, rien d'interprété à votre place. »
- Graphiques via Chart.js.
- **Sections** :
  - « Vos repères de pratique » — KPI (Séances vécues, Entrées journal, Repères disponibles, Semaines actives) + « Depuis le [date] ».
  - « Vos 7 derniers jours » — grille journalière de contacts par axe.
  - « Votre activité, semaine par semaine » — barres empilées (Séances / Journal / Repères, 10 semaines).
  - « Votre état du jour » — courbe d'énergie 0-10 issue des check-ins structurés.
  - « Ce qui pèse, ce qui recharge » — graphique en barres tiré des signaux de stress/HeartMath/sommeil/humeur (minimum 3 signaux requis pour s'afficher).
  - « Jalons de votre parcours » — 8 badges calculés (1ère entrée journal, 1er état du jour structuré, 1ère séance vécue, 1er repère disponible, 5 entrées journal, 3 semaines actives, 3 séances vécues, 10 entrées journal), compteur « X / 8 jalons » et « Prochain : « ... » ».
  - « Ligne de vie » — chronologie filtrable (Tout/Séances/Journal/Repères) fusionnant rendez-vous + journal + documents + enregistrements, groupée par mois.
- **Note de pied de page** : « cette page se construit uniquement à partir de vos traces réelles... n'est pas un diagnostic. »

### `premier-ancrage.html` — « Premier ancrage » (H1 : « Ce que vous portez en arrivant. »)
- **But** : questionnaire d'onboarding en 8 étapes, avec barre de progression (« Étape X sur 8 »).
- **Lien d'évasion** : « Je reviendrai plus tard » → tableau de bord.
- **Étapes** :
  1. Intention (zone de texte narrative) — « Qu'est-ce qui vous a amené ici, en quelques mots ? »
  2. Durée (choix radio) — Quelques jours/semaines, 2-3 mois, Plusieurs mois (6+), Depuis longtemps, Pas certain·e.
  3. **Profil dimensionnel** — 6 dimensions notées Rarement/Parfois/Souvent : Présence, Compréhension, Choix, Sol, Vivant·e, Réflexion. Texte : « Ces 6 dimensions forment votre cercle de départ — comparées à chaque entrée de journal pour mesurer votre chemin. »
  4. Registres dominants (chips, max 3) — Corps/Sensations, Émotions, Pensées/Mental, Sens/Spirituel, Relations, Identité, Autre.
  5. Intentions/espoirs (chips, max 3) — mieux me comprendre, être entendu·e, travailler quelque chose de précis, trouver une direction, retrouver énergie, reconnecter avec mon corps, explorer sans savoir, sortir de l'isolement, autre.
  6. Format préféré (cartes) — Audio en direct / Audio différé / Écrit accompagné / Sans préférence.
  7. Rythme (cartes) — 1×/semaine, 2×/mois, 1×/mois, au besoin.
  8. Limites (optionnel) + contexte praticien (optionnel) + canal de découverte (chips).
- **Boutons** : « ← Précédent » / « Suivant → » / final « Terminer mon ancrage ✓ ».
- **Écran de confirmation** : « Votre ancrage est posé. » + texte explicatif + CTA « Accéder à mon espace » → tableau de bord.
- **Note factuelle importante** : le gestionnaire de soumission est actuellement un **mock** — il sauvegarde dans `localStorage` (`ivia_ancrage`, avec `ivia_user.ancrage_complete = true`) avec le commentaire inline « Mock save (remplacé par POST /api/v1/client/ancrage) », c.-à-d. non encore connecté à un vrai point d'API backend.

### `mon-profil.html` — « Votre profil »
- **But** : recueillir des informations démographiques pour mieux accompagner le client. Texte : « Quelques repères pour mieux vous accompagner. Ces informations restent confidentielles (hébergées au Québec, Loi 25) et ne sont jamais partagées sans votre accord. »
- **Onglets internes** : « Profil » (actif) / « Compte & sécurité » (→ `compte.html`).
- **Champs** : Tranche d'âge (select 18-24 … 65+), Genre (select : Femme, Homme, Non-binaire, Autre, Préfère ne pas répondre), Lieu de naissance (texte libre), Région de résidence (select provinces canadiennes + Autre/hors Canada).
- **CTA** : « Enregistrer et continuer ».
- Peut afficher un bandeau « Merci de compléter votre profil avant de poursuivre » si `?gate=1`.
- Pré-remplissage via `getMyClient()`, sauvegarde via `updateMyClient(...)`, puis redirection vers `?retour=` ou `/client/dashboard.html`.

### `compte.html` — « Mon compte »
- **Onglets internes** : « Profil » (→ `mon-profil.html`) / « Compte & sécurité » (actif).
- **Section « Informations personnelles »** : Prénom, Nom, Adresse courriel (avec badge « Non vérifiée » si applicable), Téléphone (optionnel). Bouton « Enregistrer (bientôt) » — **désactivé**, fonctionnalité pas encore active.
- **Section « Mot de passe »** : Mot de passe actuel (optionnel si compte créé par lien magique), Nouveau mot de passe (min. 8 caractères). Bouton « Changer le mot de passe » → `apiSetPassword`.
- **Section « Consentements » (badge Loi 25)** : interrupteurs N1 (obligatoire, verrouillé), N2 (« Données anonymisées pour amélioration », activable), N3 (« Recherche et partenaires », avec lien « Détails » → `/confidentialite.html#n3`). Bouton « Enregistrer les préférences (bientôt) » — désactivé.
- **« Zone critique »** : bouton « Fermer mon compte » → confirmation JS puis ouverture d'un lien `mailto:bonjour@ivia.quebec` (pas d'endpoint de suppression automatisé ; la demande passe par un humain, Loi 25 art. 65).

---

## Note — App Praticien (hors périmètre, référencée par l'admin)

L'app praticien (`/praticien/*.html`) n'est pas couverte en détail par ce document (hors périmètre demandé), mais elle est référencée par l'admin via le lien fixe « ← Espace praticien ». Pages identifiées dans l'arborescence (non lues en détail) : dashboard.html, agenda.html, seance-express.html, clients-journal.html, livraisons.html, guide.html, ma-pratique.html, profil.html, compte.html, fiche.html, compte-rendu-seance.html, preparation.html, carte-de-vie.html.

---

## APP PRATICIEN (console d'administration)

### Navigation admin
Source : `shared/session.js` — `ADMIN_NAV`, 9 entrées, rendues dans la barre latérale sombre (`#13261A`) via `renderAdminSidebar()` :
1. **Vue d'ensemble** → `/admin/vue.html`
2. **Dossiers clients** → `/admin/dossiers.html`
3. **Comptes & accès** → `/admin/comptes.html`
4. **Demandes d'entrée** → `/admin/demandes.html`
5. **Comptabilité** → `/admin/comptabilite.html`
6. **Économie IA** → `/admin/economie.html`
7. **Facturation** → `/admin/facturation.html`
8. **Analyses & droits** → `/admin/analyses.html`
9. **Atelier des lectures** → `/admin/lectures.html`

Plus le lien **« ← Espace praticien »** et **Déconnexion**. `enforceAdminPage()` redirige tout utilisateur non-admin vers `/praticien/dashboard.html`.

### `admin/connexion.html` — « Accès réservé »
- **But** : porte d'authentification dédiée à la console admin, distincte de la connexion standard.
- Texte : « Cette porte mène à la console d'administration. Réservée aux comptes autorisés. »
- **Champs** : Courriel, Mot de passe (bouton afficher/masquer).
- **CTA** : « Entrer dans la console ».
- Lien : « Vous n'êtes pas administrateur·rice ? Connexion standard » → `/connexion.html`.
- **Logique** : après `apiLogin()`, vérifie `res.user.is_admin` ; si faux, nettoie la session et affiche « Ce compte n'a pas d'accès à l'administration. » Sinon redirige vers `/admin/` (ou vers l'URL `?retour=` si elle correspond à `/admin/` ou `/praticien/admin-`).

### `admin/index.html` — « Console d'administration »
- **H1** : « Console d'administration. »
- Texte : « Porte réservée. Gérez les comptes, les rôles, les demandes et la comptabilité de la maison. »
- **Grille de tuiles (liens)** : Vue d'ensemble (« État de la maison + vigilances »), Dossiers clients (« Enregistrements, transcriptions, analyses »), Comptes & accès (« Rôles, droit admin, vérification, statut »), Demandes d'entrée (« File du seuil public, tri, assignation »), Comptabilité (« Grand livre, encaissements, ventilation »), Facturation (« Interrupteurs payant/gratuit par offre »), Analyses & droits (« Capacités du moteur par profil, reconnaissances praticiens »).
- Note : « L'espace praticien reste distinct et ne montre aucun outil d'administration. »

### `admin/vue.html` — « Vue d'ensemble »
- **But** : tableau de bord global de l'état de la plateforme, entièrement dynamique (`adminOverview()`).
- Texte : « L'état de la maison en un coup d'œil. Les vigilances appellent une attention humaine. »
- **Cartes-statistiques** (cliquables, renvoient vers la page correspondante) : Comptes, À vérifier, Demandes nouvelles, Encaissé (mois), Vigilance · demandes, Vigilance · analyses (renvoie vers `/praticien/livraisons.html`), Comptes récents (7j).
- **Section « Alertes de vigilance »** : liste des alertes (type Demande/Analyse, niveau, libellé, date). État vide : « Aucune vigilance en cours. 🌿 »

### `admin/dossiers.html` — « Dossiers clients »
- **But** : consulter, pour chaque client, l'ensemble de ses enregistrements, transcriptions et analyses.
- Texte : « Pour chaque personne : enregistrements, transcriptions et analyses, réunis. »
- **Disposition** : liste filtrable à gauche (champ « Filtrer par nom ou courriel… ») + panneau de dossier à droite.
- **Contenu du dossier** (au clic sur un client, via `adminClientDossier(id)`) : identité, cartes Inscription / Activité / Suivi (nb séances live, enregistrements, transcrits, analyses) / Profil (territoire, année de naissance, genre) ; bloc Origine (lieu de naissance, dates d'invitation/activation) ; bloc Enregistrements & transcriptions (badge « transcrit » ou « transcription en cours », détail dépliable « Voir la transcription ») ; bloc Analyses (badges de vigilance, statut « validée »/« à valider », résumé, observation, synthèses par domaine Cœur/Corps/Esprit/Être, et « Reformulation pour le client » si présente).
- **API** : `adminListClients(query)`, `adminClientDossier(id)`.

### `admin/comptes.html` — « Comptes & accès »
- **But** : gérer les comptes, rôles, vérification email, statut d'activation.
- Texte : « Inscriptions, vérification du courriel, rôles, activation. Réservé à l'administration. »
- **Champ de filtre** : « Filtrer par courriel ou nom… », bouton « Rafraîchir ».
- **Actions groupées** (sélection multiple par cases à cocher) via menu déroulant « Action groupée… » : Renvoyer le lien de confirmation, Vérifier le courriel, Suspendre, Réactiver, Abonnement → Actif, Abonnement → Impayé, Abonnement → Inactif, ⚠️ Supprimer le compte (définitif). Bouton « Appliquer ».
- **Garde-fous** : impossible de s'auto-suspendre ou s'auto-supprimer soi-même par action groupée ; suppression exige double confirmation + saisie du mot « SUPPRIMER ».
- **Tableau par compte** : Personne (nom/courriel/date d'inscription), Statut (badges vérifié/non vérifié, actif/suspendu, admin, profil incomplet), Rôle (menu déroulant : Client, Praticien·ne, Opérateur, Superviseur, Admin tech), case Admin (droit admin cumulé au rôle), Abonnement (Actif/Impayé/Inactif, uniquement pour les praticien·nes).
- **API** : `adminListAccounts`, `adminSetRole`, `adminSetSubscription`, `adminSetAdmin`, `adminResendVerification`, `adminVerifyAccount`, `adminSetStatus`, `adminDeleteAccount`.

### `admin/demandes.html` — « Demandes d'entrée »
- **But** : traiter la file des demandes entrantes du seuil public.
- Texte : « Les personnes arrivées par le seuil public. Triez, prenez contact, planifiez — escaladez toute vigilance. »
- **Bouton** : « Rafraîchir ».
- **Tableau** : Date, Demande (besoin principal + badge vigilance si urgence + résumé d'entrée), Statut (menu déroulant : Nouvelle, À rappeler, Contactée, Planifiée, Vigilance, Hors cadre), Praticien·ne (assignation, « — Non assigné — » par défaut), Note (champ texte libre « Note de suivi… »), bouton « Enregistrer » par ligne.
- Les lignes urgentes sont surlignées en rouge clair.
- **API** : `adminListIntake()`, `adminUpdateIntakeHandling(id, statut, note, praticien)`, `listPraticiens()`.

### `admin/analyses.html` — « Analyses & droits »
- **But** : gouverner l'exposition des capacités d'analyse IA par profil d'usage, et gérer les reconnaissances professionnelles des praticiens.
- Texte : « Le moteur analyse toujours à pleine capacité ; ces vannes gouvernent l'exposition par profil d'utilisation. Un clic suffit pour valider ou invalider une capacité selon le cadre (Québec/Canada vs recherche). »
- **Section « Capacités d'analyse par profil »** : matrice à interrupteurs (une ligne par capacité, une colonne par profil), avec badge « sort du serveur » quand une capacité envoie des données à un service externe (label expliqué : « les données transitent vers un service externe — à réévaluer avant la mise en marché pour le profil client IVIA Québec »).
- **Section « Reconnaissances professionnelles »** : texte « Un praticien vérifié accède aux inférences complètes du modèle. Le droit de transmission au client (contenus cliniques) exige la reconnaissance par l'instance appropriée. » Liste des reconnaissances (praticien, ordre/instance, n° de permis, portée, statut : En attente/Vérifié/Révoqué/Expiré), bascule « Transmission client », boutons « Vérifier » / « Révoquer ».
- **Formulaire « Ajouter une reconnaissance »** : champs Praticien·ne (select), Ordre / instance (ex. OPQ, OTSTCFQ), N° de permis (optionnel), Portée reconnue (optionnel). Bouton « Enregistrer ».
- **API** : `adminAnalysisCapabilities()`, `adminSetAnalysisCapability`, `adminListCredentials`, `adminCreateCredential`, `adminUpdateCredential`.

### `admin/lectures.html` — « L'Atelier des lectures »
- **But** : configurer, par type de séance, quelles « lectures » (analyses IA) sont permises ou automatiques ; gérer le catalogue d'exercices proposables aux clients.
- Texte : « Chaque type de séance définit quelles lectures s'appliquent à la rencontre : permise (le praticien peut la demander) et auto (elle se déclenche d'elle-même après transcription). Le type raffine la vanne par profil — il ne la contourne jamais. Une séance sans type n'est pas restreinte. »
- **Section « Types de séance »** : pour chaque type, tableau Lecture / Permise / Auto (interrupteurs). Badge « sort du serveur » identique à `analyses.html`.
- **Formulaire « Nouveau type de séance »** : code (slug), Nom affiché, Description courte (optionnel). Bouton « Créer le type ».
- **Section « Exercices »** : texte « Pratiques sobres que le praticien peut proposer à un client en fin de séance — une invitation, jamais une prescription. Les consignes sont rédigées ici, dans le vocabulaire autorisé (le filtre Loi 21 refuse tout terme interdit). » Liste des exercices existants (titre, code, axe MERLIN, consignes, interrupteur Actif).
- **Formulaire « Nouvel exercice »** : code (slug), Titre, Consignes (10-2000 caractères), Axe MERLIN (optionnel : territoire, corps, émotions…). Bouton « Ajouter au catalogue ».
- **Section « Proposer une nouvelle technique d'analyse »** : texte décrivant le processus de gouvernance en 4 étapes — ① entrée au catalogue `capability_gate.py`, ② prompt versionné dans `11_PROMPTS/07_analyses/` (triade O/H/O, vocabulaire Loi 21, escalade), ③ *safety suite* au registre (≥ 0.90 exigé), ④ security-review avant fusion.
- **API** : `adminAnalysisCapabilities`, `adminListSessionTypes`, `adminCreateSessionType`, `adminPatchSessionTypeCapability`, `adminListExercises`, `adminCreateExercise`, `adminPatchExercise`.

### `admin/comptabilite.html` — « Comptabilité »
- **But** : suivi comptable des encaissements réels, ventilés (HT, taxes, frais, marge).
- Texte : « Encaissements ventilés (HT, taxes, frais, marge). Les paiements de test sont exclus des totaux réels. »
- **Sélecteur de mois** + bouton « Voir ».
- **Cartes** : Encaissé (réel), Revenu HT, TPS à remettre, TVQ à remettre, Frais Stripe, Coût IA, Part praticien, Marge IVIA.
- **Note fiscale** : nombre d'encaissements réels, paiements test exclus, avertissement si non assujetti aux taxes.
- **Tableau grand livre** (par transaction) : Date, Offre (avec badge « test » si applicable), TTC, HT, TPS, TVQ, Stripe, Marge.
- **API** : `adminAccountingSummary(from,to)`, `adminAccountingLedger(from,to)`.

### `admin/facturation.html` — « Facturation — interrupteurs par offre »
- **But** : basculer chaque offre entre payante et gratuite (mode test).
- Texte : « Coché = l'offre est payante. Décoché = gratuite, pour tester le parcours sans paiement Stripe. »
- **Avertissement** : « Réglage global de la plateforme, réservé aux administrateurs (rôle admin_tech ou courriel en liste blanche). Un praticien ordinaire n'y a pas accès. »
- **Offres listées** : *Enregistrement + rappel 10 min* (35 $, « Vous enregistrez ; rappel de 10 min. Transcription + analyse incluses. ») ; *Séance live · 30 min / 1 h* (49 / 75 $, « Séance en direct avec un·e praticien·ne. Transcription + analyse incluses. »).
- Chaque offre affiche un interrupteur (« Payant » / « Gratuit (mode test) »).
- **API** : `apiGetBillingFlags()`, `apiSetBillingFlags({code: bool})`.

### `admin/economie.html` — « Économie IA »
- **But** : croiser les coûts LLM réels avec les revenus générés, par finalité d'analyse et par séance.
- Texte : « Coûts LLM réels (tokens mesurés à chaque appel) croisés avec les revenus. Conversion CAD au taux configuré — le réel vient du relevé Anthropic. »
- **Sélecteur de mois** + bouton « Voir ».
- **Cartes** : Revenus réels (TTC), Marge IVIA avant IA, Coût IA réel (nombre d'appels), Bénéfice net (coloré rouge si négatif, vert si positif).
- **Tableau « Coûts par finalité d'analyse »** : Finalité, Appels, Tokens in, Tokens out, Coût USD, Coût CAD.
- **Tableau « Économie par séance »** : texte explicatif « Séances récentes ayant généré au moins un appel IA. Revenu = commande payée rattachée au rendez-vous ; bénéfice = revenu IVIA − coût IA de la séance. » Colonnes : Date, Praticien, Type, Appels IA, Coût IA, Revenu TTC, Revenu IVIA, Bénéfice.
- **API** : `adminEconomicsSummary(from,to)`, `adminEconomicsSessions(80)`.

---

## Tableau récapitulatif des parcours clés

### App Client

| Parcours | Étapes (pages/actions dans l'ordre) |
|---|---|
| **S'ancrer au quotidien** | Connexion → `dashboard.html` (« Mon espace », « les deux gestes » + « les trois lieux ») → au premier passage, `premier-ancrage.html` (8 étapes, CTA « Terminer mon ancrage ✓ ») → retour dashboard. |
| **Réserver une séance** | `dashboard.html` (carte *Réserver*) ou menu *Réservation* → `agenda.html`/`reserver.html` → flux `reservation.js` : Étape 1 choix praticien (« Voir les disponibilités → ») → Étape 2 créneau (calendrier) → Étape 3 confirmation (« Confirmer et payer → », paiement Stripe) → `seances.html` liste les rendez-vous confirmés → au jour J, `seance.html`/`seance-active.html` (salle d'attente → séance active → fin, « Terminer ma séance → »). |
| **Faire une séance expresse** | CTA d'en-tête « Séance express » → `enregistrement.html` (Enregistrer/Pause/Terminer → « Envoyer à IVIA ») → confirmation « Reçu — transcription en cours » → `mes-enregistrements.html` (KPI, bouton « Recevoir ma lecture » une fois transcrit) → redirige vers `mon-reflet.html`. Variante par lien : `seance-express-join.html` (jeton) pour un envoi initié par le praticien. |
| **Écrire au journal** | `journal.html` — écriture libre (« Enregistrer ») ou check-in structuré « Mon Architecte intérieur » (« Enregistrer la version structurée ») → bouton « Analyse du jour » déclenche `requestMyReflet()`. |
| **Consulter son reflet/horizon** | `mon-reflet.html` (« Miroir ») — demander un miroir périodique, consulter « Mes miroirs », « Mes repères », « Exercices » ; `carte-de-vie.html` (« Horizon ») — constellation des onze axes, « Champs de tension », curseur « Progression », « Lecture complète » (triade O/H/O) ; `ma-progression.html` — KPI, graphiques, jalons, « Ligne de vie ». |

### App Praticien / Admin

| Parcours | Étapes (pages/actions dans l'ordre) |
|---|---|
| **Traiter une demande** | `admin/demandes.html` — filtrer les demandes de la file (badge vigilance si urgence) → changer le Statut (Nouvelle → À rappeler/Contactée/Planifiée/Vigilance/Hors cadre) → assigner un·e Praticien·ne → ajouter une Note de suivi → « Enregistrer ». |
| **Ouvrir un dossier** | `admin/dossiers.html` — filtrer/sélectionner un client dans la liste → consultation du dossier complet (activité, profil, enregistrements/transcriptions dépliables, analyses avec triade et statut « validée »/« à valider »). |
| **Faire une lecture/analyse** | `admin/analyses.html` (activer une capacité d'analyse pour un profil via la matrice ; ajouter/vérifier une reconnaissance professionnelle) et `admin/lectures.html` (associer des lectures « permise »/« auto » à un type de séance ; créer/activer un exercice). |
| **Gérer la facturation** | `admin/facturation.html` (basculer chaque offre payant/gratuit) ; `admin/comptabilite.html` (choisir un mois → consulter cartes + grand livre détaillé HT/TPS/TVQ/Stripe/marge) ; `admin/economie.html` (choisir un mois → comparer coûts IA réels et revenus, par finalité et par séance). |

---

## Sources
Toutes les informations ci-dessus proviennent de la lecture directe des fichiers du dépôt local, notamment :
- `/home/user/workspace/MERLIN/ivia_site_v2/shared/layout.js`
- `/home/user/workspace/MERLIN/ivia_site_v2/shared/session.js`
- `/home/user/workspace/MERLIN/ivia_site_v2/shared/reservation.js`
- `/home/user/workspace/MERLIN/ivia_site_v2/client/*.html` (19 pages)
- `/home/user/workspace/MERLIN/ivia_site_v2/admin/*.html` (11 pages)
- `/home/user/workspace/MERLIN/ivia_site_v2/inscription.html`, `connexion.html`, `reserver.html`, `rendez-vous.html`, `activer.html`, `verify-email.html`

# BRIEF COPILOT — Réalignement IVIA v2.1

**Version** : 2.1
**Date** : 9 mai 2026
**Statut** : Réaligné après signalements utilisateur de l'après-midi + enrichissement doctrinal parcours client
**Mention** : Ajout chantiers C11 (parcours client gradué) et C12 (journal client + temporalité décalée + admin fiches)
**Destinataire** : GitHub Copilot (mode auto, VS Code, repo MERLIN)
**Périmètre** : `ivia_mockups/` (site déployé sur https://ivia.pplx.app)
**Auteur du brief** : Computer (Perplexity)
**Mandat** : David Phaneuf, fondateur IVIA

**Documents de référence :**
- Brief v1.0 : `04_METHODES/BRIEF_COPILOT_REFONTE_LANDING_LIENS_v1.0.md`
- Brief v2.0 : `04_METHODES/BRIEF_COPILOT_REFONTE_LANDING_LIENS_v2.0.md`
- Mode d'emploi symbiose : `04_METHODES/SYMBIOSE_COPILOT_COMPUTER_v1.0.md`
- Cadrage parcours client et journal : `04_METHODES/CADRAGE_PARCOURS_CLIENT_JOURNAL_v1.md` — LIRE AVANT D'EXÉCUTER C11 ET C12

---

## 1. CONTEXTE ÉVOLUTIF — Pourquoi une v2.1

### Ce qui existait à la livraison v2.0 (9 mai 2026, midi)

Le brief v2.0 livré ce midi consolidait cinq chantiers fondamentaux hérités de la v1.0 (C1 à C5 : correction des 112 liens morts, refonte landing, architecture mobile, exposition des 16 articles, cohérence visuelle inter-pages) et y ajoutait quatre modules structurants inédits : intégration de la charte botanique sur l'existant Python (C6), calendrier de réservation fonctionnel (C7), cycle audio testable de bout en bout (C8), dashboard de statistiques praticien et panneau public anonymisé (C9), et pipeline contenu data-driven (C10). Tous ces chantiers demeurent valides et constituent la colonne vertébrale du sprint planning.

### Signalements utilisateur — 9 mai 2026, après-midi

Dans l'après-midi suivant la livraison v2.0, le user a signalé deux liens morts spécifiques, distincts des 112 déjà répertoriés dans C2.

Le premier concerne `admin/praticiens.html` : le bouton Action, présent dans la liste des praticiens, ne produit aucun effet au clic. Il s'agit d'un `href="#"` non relié à une logique de menu ni à une page de destination. Ce bouton est fonctionnellement central dans le flux de gestion admin : il doit exposer un menu déroulant permettant d'accéder à la fiche individuelle du praticien, de le suspendre, de le contacter ou de déclencher un audit doctrinal.

Le second concerne `client/journal.html` : le bouton Nouvelle entrée ne produit aucun effet au clic. Il s'agit d'un élément UI sans action JavaScript associée. Or ce bouton est le point d'entrée principal de la section journal, qui constitue l'une des propositions de valeur les plus distinctives d'IVIA selon la vision du fondateur.

Ces deux signalements déclenchent des chantiers spécifiques, détaillés ci-dessous en C12.

### Enrichissement doctrinal — Parcours client et journal

Le user a également enrichi la doctrine produit en articulant une vision complète du parcours client, de l'inscription jusqu'au journal, en passant par le formulaire d'ancrage initial. Cette vision est formalisée dans `04_METHODES/CADRAGE_PARCOURS_CLIENT_JOURNAL_v1.md`, à lire intégralement avant d'exécuter C11 et C12. Les principes nouveaux introduits par ce document sont les suivants.

L'inscription minimaliste avec accès immédiat : le client crée son espace avec cinq champs seulement et accède instantanément à la plateforme sans attendre la confirmation de son courriel. La validation courriel n'intervient qu'à la deuxième connexion, sous forme de blocage doux non anxiogène, et reste obligatoire avant tout achat ou réservation.

L'accès gradué plutôt que le blocage frontal : cette approche réduit la friction initiale tout en protégeant la plateforme des abus. Elle repose sur quatre phases décrites dans le cadrage (section 2) : inscription libre, session courante ouverte, blocage doux à la reconnexion si courriel non validé, blocage strict sur les actions transactionnelles.

Le formulaire d'ancrage initial comme portail relationnel : dès la première connexion, une page interstitielle optionnelle est proposée au client sous le titre "Ce que vous portez en arrivant". Six questions ciblent le contexte d'arrivée, l'état général, les registres qui résonnent, les préférences de première rencontre, et le canal d'acquisition. Ce formulaire nourrit le praticien sans franchir la ligne du diagnostic.

Le journal client comme mémoire vivante et matière analytique : le journal n'est pas un formulaire clinique. C'est un espace d'écriture libre entre les séances, avec une structure minimale (titre optionnel, date évoquée optionnelle, corps, tags émotionnels, niveau de partage) et une innovation doctrinale majeure : l'indicateur de temporalité décalée, décrit ci-dessous.

L'indicateur de temporalité décalée IVIA : hypothèse originale du fondateur, jamais étudiée ni codifiée sur aucune plateforme d'écoute à ce jour. Si les dates des événements évoqués dans les entrées du journal ne respectent pas la chronologie vécue du client, cet ordre d'émergence des souvenirs porte peut-être un sens propre. IVIA doit le mesurer. Ce signal est visualisé pour le client sous forme de ligne de vie double (axe d'écriture versus axe d'événement), et transmis au praticien sous forme de digest synthétique avec consentement N2.

Le modèle économique gratuit/forfait/rétribution : journal gratuit jusqu'à 50 entrées ou 50 000 caractères par mois calendrier. Au-delà : deux options proposées sans pression — Forfait "Journal sans limite" (7 $/mois) ou Rétribution N3 (accès gratuit illimité en échange de la contribution des données agrégées anonymisées à l'IP collective IVIA, avec crédit séance).

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

## 4. CHANTIERS v2.0 — RAPPEL (C6 à C10, inchangés)

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

**Typographie** : Fraunces (titres, weight 300-700 selon hiérarchie), Lora (corps de texte, 16-18px, line-height 1.65 minimum), Inter (éléments fonctionnels : navigation, boutons, formulaires). Espacements : padding section minimum 80px vertical desktop, 48px mobile.

**Contraste WCAG AA** : aubergine `#2A1A22` sur crème `#F0E0DC` passe AA. La bois-rose `#C58A8A` sur crème passe AA uniquement en grand corps (18px+) — ne pas l'utiliser pour du texte courant. Le miel `#D9A841` sur fond blanc ne passe pas AA — réserver aux éléments décoratifs et aux grands titres sur fond foncé.

**Interdits stricts** : noir pur `#000000`, deux couleurs vives sur le même écran, photos de personnes en stock-photo, dégradés saturés, italique pour exprimer la chaleur.

**Phasage** : public d'abord (`shared/public.css`, pages issues de `pages_public.py`). Client ensuite. Praticien et admin : cohérence sobre, pas de charte botanique complète.

**Commit attendu** : `feat(site): C6 - intégration charte botanique`

---

### C7 — CALENDRIER FONCTIONNEL
**Priorité : haute — différenciateur de maturité produit**

Vue praticien (`praticien/agenda.html` via `pages_praticien.py`) : grille hebdomadaire 7 jours, créneaux 30 minutes, 8h-20h fuseau `America/Toronto`. Trois états : disponible (fond crème, bordure mousse), réservé (fond lavande, nom client fictif), bloqué (fond gris clair). Navigation < > semaine.

Vue client (via `pages_funnel.py`) : sélection praticien → `funnel/choisir-creneau.html` → récapitulatif → `client/confirmation-paiement.html`. Données depuis `assets/data/agenda_fixtures.json` (3 semaines de créneaux, format ISO 8601 avec fuseau explicite).

JS pur, mobile-first, aucune dépendance externe. **Commit attendu** : `feat(calendrier): C7 - agenda praticien + funnel réservation client`

---

### C8 — CYCLE AUDIO TESTABLE DE BOUT EN BOUT
**Priorité : haute — cœur différenciateur de la plateforme IVIA**

Trois pages à compléter ou créer : `client/audio-async.html` (enregistrement micro via MediaRecorder API, fallback simulation si micro refusé), `praticien/audio-traiter.html` (lecteur personnalisé, espace notes, enregistrement lecture retour), `client/audio-resume.html` (lecture du retour praticien, transcription simulée, trois boutons d'état : Intégré / À réécouter / Interrompre).

Fixtures audio dans `assets/audio/` : `depot_camille_01.mp3`, `lecture_mylene_01.mp3`, `silence_30s.mp3` (ou placeholders documentés si génération impossible). Lecteur audio personnalisé réutilisable : `shared/audio-player.js`. Aucun `<audio controls>` natif.

**Commit attendu** : `feat(audio): C8 - cycle audio client/praticien testable bout en bout`

---

### C9 — STATS PRATICIEN + DASHBOARD PUBLIC
**Priorité : moyenne — renforce la crédibilité doctrinale**

Dashboard praticien (`praticien/index.html`) : six indicateurs financiers simulés, quatre qualitatifs, trois typologiques, deux santé praticien, deux doctrinaux (cf. `indicateurs_praticien_v1.md`, catégories A à E). SVG inline ou CSS pur, barres de progression CSS, chiffres clés en grand format Fraunces, tendances en flèches Unicode. Pas de Chart.js.

Vue admin praticien (`admin/praticiens/[id].html`) : même indicateurs agrégés, alertes automatiques sur seuils (taux d'occupation < 20% pendant 3 semaines → badge orange "Appui suggéré", note moyenne < 3.5 sur 30 jours → badge rouge "À vérifier", charge > 25 séances hebdomadaires → badge orange "Attention charge").

Vue admin réseau (`admin/index.html`) : praticiens actifs, volume lectures, satisfaction globale anonymisée, répartition géographique agrégée.

Section publique landing ("En direct du collectif") : quatre chiffres anonymisés depuis `assets/data/stats_public.json`, mise à jour manuelle mensuelle par David.

Page `admin/veille.html` (via `pages_admin.py`) : sources surveillées par palier, alertes fictives du mois, colonne Statut (En analyse / Intégré / Sans suite). Vue admin uniquement.

**Commit attendu** : `feat(stats): C9 - dashboard praticien, vues admin, panneau public collectif`

---

### C10 — PIPELINE CONTENU DATA-DRIVEN
**Priorité : basse pour cette itération — préparer le terrain**

Template `ivia_mockups/articles_md/_template_data_driven.md` avec structure : titre en vocabulaire IVIA, saison, motif de départ, source, sections "Ce qu'on observe ce mois", "Ce qu'un praticien en dit", "Où ça peut mener". Section "Articles cette saison" dans `pages_public.py`, `build_bibliotheque()` : articles marqués `saison: active` apparaissent en tête avec badge discret.

**Commit attendu** : `feat(contenu): C10 - template data-driven + section articles saison`

---

## 5. NOUVEAUX CHANTIERS v2.1

### C11 — PARCOURS CLIENT GRADUÉ
**Priorité : haute — sécurisation et non-frustration en première connexion**

Ce chantier refond entièrement le parcours d'inscription et de première connexion en appliquant la doctrine d'accès gradué formalisée dans `04_METHODES/CADRAGE_PARCOURS_CLIENT_JOURNAL_v1.md`, sections 2 à 5. Lire ces sections intégralement avant toute modification de code.

#### 11a — Refonte `client/inscription.html` (via `pages_client.py`)

**Champs obligatoires** (dans l'ordre affiché) : Prénom, Nom de famille, Courriel (identifiant unique — pas de pseudo séparé), Téléphone (intitulé "Numéro de téléphone — pour vos rappels de rendez-vous", conformément à l'article 8 de la Loi 25 qui exige d'indiquer la finalité de chaque collecte), Mot de passe.

**Règle mot de passe** : minimum 12 caractères, aucune complexité forcée (conforme NIST SP 800-63B, section 5.1.1). Indication à l'écran : "Choisissez une phrase dont vous vous souviendrez — au moins 12 caractères." Passer de 10 à 12 caractères par rapport au mockup actuel.

**Consentements graduées** — trois cases distinctes, non pré-cochées sauf N1 (qui est pré-cochée mais décochable si le client renonce à s'inscrire) :

- Case N1 — Obligatoire : "J'accepte qu'IVIA conserve les renseignements nécessaires à mon compte (courriel, historique de séances) et les partage avec la personne praticienne qui m'accompagne, uniquement pour la durée de mes séances." Liens directs vers les CGU et la politique de confidentialité Loi 25.
- Case N2 — Opt-in, non cochée par défaut : texte verbatim issu de `politique_gouvernance_donnees_agregees_v1.md`, section 4, Niveau 2.
- Case N3 — Opt-in, non cochée par défaut : texte verbatim issu de `politique_gouvernance_donnees_agregees_v1.md`, section 4, Niveau 3.

**Captcha invisible** : intégrer Cloudflare Turnstile (recommandé — gratuit, sans Google, RGPD-friendly). Limite de taux IP : pas plus de 3 créations de compte par adresse IP en 30 minutes.

**Validation MX à la soumission** : si le domaine courriel saisi ne possède pas d'enregistrement MX valide, refus sans explication technique (message : "Cette adresse ne semble pas valide. Essayez une autre."). Maintenir une liste de domaines jetables connus (mailinator, guerrillamail, etc.) à mettre à jour mensuellement.

**Bouton de soumission** : "Créer mon espace" (vocabulaire IVIA existant, à conserver).

**Redirection post-soumission** : vers `client/dashboard.html` (et non vers `verifier-courriel.html` comme actuellement — la vérification courriel n'est plus un prérequis bloquant à l'accès initial). Un bandeau persistant non fermable s'affiche en haut du dashboard : "Votre espace est ouvert. Pour prendre rendez-vous, confirmez votre courriel — lien envoyé à xxxx@xxx.xx." Ce bandeau disparaît dès que la validation est complétée.

#### 11b — Mise à jour `client/connexion.html`

Détecter si l'adresse courriel du compte n'a pas encore été confirmée. Si non confirmée et tentative de reconnexion (hors première session) : afficher un blocage doux avec message "Avant de continuer, confirmez votre courriel. Nous avons envoyé un lien à xxxx@xxx.xx — vérifiez aussi vos indésirables. Pas encore reçu ? Renvoyer le lien." Ne jamais bloquer la première session. Ajouter le bouton "Renvoyer le lien de confirmation" avec gestion du retour visuel (confirmation de renvoi, protection contre le spam de renvois).

#### 11c — Rendre fonctionnelle `client/verifier-courriel.html`

La page existante est à relier à un endpoint réel de validation. Ajouter depuis le bandeau dashboard un lien "Je confirme maintenant" pointant vers cette page. Au retour depuis le lien courriel, la session doit s'ouvrir avec l'état "validé" et le bandeau disparaît.

#### 11d — Créer `client/premier-ancrage.html`

Page interstitielle proposée en première connexion, avant l'exploration libre. Le client peut la contourner via un bouton "Explorer d'abord, je le ferai plus tard" qui mène directement au dashboard. Titre de la page : "Ce que vous portez en arrivant".

**Six questions** (voir `CADRAGE_PARCOURS_CLIENT_JOURNAL_v1.md`, section 5 pour les libellés exacts) :

- Q1 — Texte libre, 50-300 mots : ce qui amène le client aujourd'hui
- Q2 — Échelle visuelle à 5 niveaux verbalisés sans chiffres : submergé·e / tendu·e / stable / en mouvement / ressourcé·e
- Q3 — Cases à cocher, 1 à 3 parmi : Présence / Sommeil / Clarté / Relation / Transition / Corps / Mémoire / Reconnaissance / Ancrage
- Q4 — Choix unique : enregistrement audio / rencontre synchrone / selon disponibilités
- Q5 — Texte libre optionnel, 0-200 mots : ce qu'un praticien devrait savoir en amont
- Q6 — Menu déroulant : canal d'acquisition (Recommandation d'un proche / Médias sociaux / Article ou balado / Professionnel de la santé / Recherche en ligne / Autre)

Les réponses Q1 à Q5 sont des données de strate C (visibles par le praticien assigné avec consentement N1). La réponse Q6 est une donnée d'acquisition agrégée (strate D, anonymisée).

#### 11e — Suppression automatique des comptes non validés

Implémenter une règle d'auto-suppression : tout compte dont l'adresse courriel n'est pas confirmée dans les 30 jours est supprimé automatiquement (cron ou équivalent). Deux rappels courriel : J-7 et J-1 avant suppression. Log de suppression anonymisé conservé (date, raison) pour audit interne. Cette règle est conforme à la Loi 25, article 14 (consentement manifeste) et article 23 (obligation de détruire les renseignements personnels lorsqu'ils ne sont plus nécessaires à la fin pour laquelle ils ont été collectés).

#### 11f — Flux récupération mot de passe si courriel non validé

La demande de réinitialisation de mot de passe déclenche obligatoirement la validation de l'adresse courriel en même temps. L'utilisateur ne peut pas récupérer l'accès sans valider.

#### 11g — Cohérence visuelle

Appliquer la charte botanique (C6) sur toutes les pages nouvelles ou modifiées dans C11. Lavande comme couleur dominante de l'espace client (`--color-lavande`). Aucun terme clinique dans les libellés du formulaire d'ancrage.

**Commit attendu** : `feat(parcours-client): C11 - inscription minimaliste, accès gradué, premier ancrage`

---

### C12 — JOURNAL CLIENT + TEMPORALITÉ DÉCALÉE + ADMIN FICHES
**Priorité : haute — deux liens morts signalés + vision complète à implémenter**

#### 12a — Refonte `client/journal.html`

**Bouton "Nouvelle entrée" fonctionnel** : actuellement un `href="#"` sans JavaScript. À relier à une modale ou à une page dédiée `client/journal-nouvelle-entree.html`. Le choix modal est recommandé pour préserver le contexte de la liste des entrées, mais la page dédiée est acceptable si la modale alourdit trop le bundle.

**Structure d'une entrée** (à implémenter dans le formulaire de saisie) :

- Date d'écriture : saisie automatique au moment de la soumission, non modifiable, affichée à l'utilisateur
- Date évoquée : champ optionnel, libellé "Date à laquelle se réfère cette entrée (si différente d'aujourd'hui)", type date avec valeur vide par défaut
- Titre : champ optionnel, 80 caractères maximum
- Corps de l'entrée : textarea libre, affichage progressif au-delà de 2000 mots (bouton "Voir la suite" pour éviter une page visuellement surchargée)
- Tags émotionnels : sélection de 1 à 3 tags parmi la liste IVIA : lourd / léger / lumineux / embrouillé / mouvement / blocage / gratitude / perte / victoire / doute. Ces tags ne sont pas des diagnostics. Implémentation en cases à cocher stylées qui se désactivent automatiquement après 3 sélections.
- Niveau de partage : bouton radio discret avec trois options : "Partagé avec mon praticien (30 derniers jours)" (par défaut), "Épinglé — visible par mon praticien hors fenêtre de 30 jours", "Privée — pour moi seulement"

**Indicateur de seuil mensuel** : compteur discret en pied de page du journal, format "X entrées / 50 ce mois" et "X 000 / 50 000 caractères ce mois". Affichage en texte sobre, sans barre de progression qui anxiogéniserait.

**Au seuil atteint** : modale douce, sans blocage brutal, avec le texte "Vous avez rempli votre journal avec soin ce mois-ci. Pour continuer sans limite, deux options s'offrent à vous." Deux boutons : "Voir le forfait Journal sans limite" (→ `client/journal-etendu.html`) et "Attendre le début du prochain mois" (fermer la modale).

**Quotas anti-abus** : pas plus de 5 entrées dans une fenêtre de 5 minutes, même pour les comptes en règle.

**Visualisation "Ligne de vie double"** : en bas de la page journal, afficher un axe SVG sobre montrant les entrées positionnées à leur date d'écriture et, si une date évoquée est renseignée, un trait reliant les deux positions temporelles. Accessible au client en permanence. Transmis au praticien sous consentement N2 uniquement, via le digest mensuel. Le SVG doit rester lisible sur 390px sans overflow horizontal. Technique : SVG inline généré côté Python à partir des données de fixtures, avec coordonnées calculées dynamiquement.

**Stockage** : les entrées du journal contiennent des données personnelles sensibles (motifs personnels, états émotionnels). Le chiffrement au repos est obligatoire même en pilote. Recommandation : libsodium (NaCl) ou SQLite avec extension SEE. Documenter le choix retenu dans un commentaire Python au-dessus du modèle de données.

#### 12b — Créer `client/journal-etendu.html`

Page affichée lorsque le seuil gratuit mensuel est atteint. Présente les deux options en cohérence avec la doctrine économique d'IVIA.

**Option 1 — Forfait "Journal sans limite"** : 7 $/mois. Inclut stockage illimité, transcription vocale illimitée, digests praticien illimités. Bouton "Choisir ce forfait" (flux paiement à relier à `client/confirmation-paiement.html`, sans Stripe fonctionnel en pilote).

**Option 2 — Rétribution par contribution N3** : accès gratuit illimité en échange du consentement N3 (contribution des données agrégées anonymisées à l'IP collective IVIA). Crédit séance : 1 $ par tranche de 5 000 caractères contribués au-delà du seuil gratuit mensuel. Bouton "Contribuer et continuer". Si le client n'a pas encore coché la case N3 à l'inscription, cette action déclenche un mini-formulaire de consentement N3 autonome (libellé verbatim issu de `politique_gouvernance_donnees_agregees_v1.md`, section 4, Niveau 3).

**Disponibilité** : Option 1 dès le pilote. Option 2 à introduire après 6 mois, quand la valeur démontrable de l'IP collective peut être communiquée aux clients avec honnêteté.

**Ton** : sobre, sans pression, vocabulaire IVIA. Aucun point d'exclamation. Aucun terme de marketing ("offre exclusive", "premium", "upgrade").

**Commit attendu** : `feat(journal): C12b - page journal-etendu forfait et rétribution N3`

---

#### 12c — Admin fiches praticien

**Rendre fonctionnel le bouton "Action" sur `admin/praticiens.html`** : ce bouton déclenche actuellement un `href="#"` sans effet. À remplacer par un menu déroulant (dropdown) positionné sous le bouton au clic, avec quatre options :

1. "Voir la fiche" → lien vers `admin/praticien-fiche.html?id=X` (ou `admin/praticien.html?id=X` selon la convention de nommage retenue)
2. "Suspendre" → modale de confirmation avec champ texte "Raison de la suspension" avant validation
3. "Contacter" → ouvre le client de messagerie ou un formulaire interne (mailto en pilote)
4. "Audit doctrinal" → lien vers la section Alignement doctrinal de la fiche praticien

**Créer `admin/praticien-fiche.html` paramétrée par `?id=X`** (via `pages_admin.py`) : fiche individuelle exposant l'ensemble des indicateurs définis dans `indicateurs_praticien_v1.md`, catégories A à F. Structure recommandée en onglets ou sections accordéon :

- Section A — Financier : revenu brut, taux d'occupation, panier moyen, taux de conversion, lectures complétées vs annulées, évolution 3 mois glissants
- Section B — Qualitatif : note moyenne, taux retour écrit, taux re-réservation 90 jours, mots-clés positifs/négatifs détectés, taux satisfaction post-livraison
- Section C — Typologie clientèle : motifs récurrents, fréquences travaillées, tranche d'âge, région, langue de service, parcours client typique, taux première séance unique
- Section D — Santé du praticien : charge hebdomadaire, délai moyen de production, jours sans livraison, mode calme activé, variation durée audio, autoévaluation mensuelle
- Section E — Alignement doctrinal : score orientation autonomie, vocabulaire conforme, cohérence charte éthique, signalements client, renouvellement engagement, délais de livraison
- Section F — Impact client : évolution autodéclarée, atteinte d'un repère concret, interruption réfléchie vs abandon, durée médiane parcours, thème de clôture, NPS praticien. Si le praticien a des clients avec consentement N2 : encadré "Digest journal clients actifs" généré par l'agent IVIA (mots-clés émergents du mois, indication de temporalité décalée si applicable, tag émotionnel dominant).

Alertes visuelles : badge orange "Appui suggéré" si taux d'occupation < 20% pendant 3 semaines, badge rouge "À vérifier" si note moyenne < 3.5 sur 30 jours, badge orange "Attention charge" si charge hebdomadaire déclarée > 25 séances.

**Rendre fonctionnels tous les `href="#"` restants dans le footer admin et la sidebar Compte** : un audit `grep -rh 'href="#"' admin/ --include="*.html"` doit retourner 0 après ce chantier.

**Données** : toutes les valeurs affichées sur la fiche sont des fixtures réalistes (pas de zéros, pas de 100%, noms de praticiens fictifs). Format cohérent avec `assets/data/` existant.

**Commit attendu** : `feat(admin): C12c - fiche praticien, bouton Action fonctionnel, footer/sidebar`

---

#### 12d — Affichage côté praticien

**Créer ou enrichir `praticien/clients-journal.html`** (via `pages_praticien.py`) : vue digest mensuel des journaux des clients accompagnés ayant accordé le consentement N2. Cette vue ne présente pas le contenu textuel brut des entrées — c'est l'agent IVIA qui produit la synthèse.

**Structure de la vue** : liste des clients actifs avec consentement N2 coché. Pour chaque client : prénom uniquement (pas de nom complet), nombre d'entrées du dernier mois, trois mots-clés ou thèmes émergents, tag émotionnel dominant du mois, indication de temporalité décalée si applicable ("Des entrées évoquent des périodes anciennes — retours vers [époque]" — jamais avec le contenu textuel), statut de l'entrée la plus récente.

**Ton** : rédigé en français québécois, vocabulaire IVIA, registre chaleureux et non clinique. Pas de termes diagnostiques. Le digest est conçu pour que le praticien arrive en séance avec un contexte humain, pas une fiche médicale.

**Note d'implémentation** : en pilote, le digest est simulé par des fixtures JSON dans `assets/data/journal_digest_fixtures.json`. L'agent IVIA réel (traitement textuel automatisé) est un développement ultérieur. Documenter ce choix dans un commentaire Python.

**Cohérence avec indicateurs_praticien_v1.md** : le journal client devient une sixième source pour la catégorie F (Impact client), section 2F. Il s'ajoute au formulaire pré-dépôt et au formulaire de clôture sans les remplacer.

**Commit attendu** : `feat(praticien): C12d - vue digest journal clients avec consentement N2`

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
| C11 — Parcours client gradué | ~6h | Haute |
| C12 — Journal + temporalité + admin fiches | ~8h | Haute |
| **Total v2.1 supplémentaire** | **~14h** | |
| **Total cumulé v1.0 + v2.0 + v2.1** | **~29-30h** | |

---

## 7. ORDRE D'EXÉCUTION RECOMMANDÉ

**Sprint 1 — Stabilisation et charte (4-5h)**
Exécuter C1 à C5 dans l'ordre décrit dans `04_METHODES/BRIEF_COPILOT_REFONTE_LANDING_LIENS_v1.0.md`, puis enchaîner avec C6 (CSS charte botanique). Push après C5, push après C6. Computer redéploie et fait la QA visuelle desktop + mobile (390px, 768px, 1280px) avant de valider le passage au Sprint 2.

**Sprint 2 — Parcours client gradué (6h)**
C11 complet : refonte inscription, mise à jour connexion, activation vérification courriel, création page premier-ancrage, captcha invisible, suppression automatique comptes non validés. Push. Computer redéploie, QA parcours Camille de bout en bout (inscription → premier ancrage → dashboard → bandeau validation).

**Sprint 3 — Calendrier (3h)**
C7 complet : fichier JSON fixtures, composant calendrier JS pur, page `praticien/agenda.html` enrichie, pages funnel réservation client. Push. Computer redéploie, QA visuelle + test parcours Mylène et Camille.

**Sprint 4 — Audio (3h)**
C8 complet : pages `audio-async.html`, `audio-traiter.html`, `audio-resume.html` vérifiées et complètes, lecteur audio personnalisé, fixtures MP3 ou placeholders documentés. Push. Computer redéploie, QA bout-en-bout cycle audio.

**Sprint 5 — Journal + admin fiches (8h)**
C12 complet : refonte `journal.html` (bouton fonctionnel, structure entrée, quotas, ligne de vie double), création `journal-etendu.html`, fiche praticien admin paramétrée, bouton Action fonctionnel sur `admin/praticiens.html`, vue digest praticien `clients-journal.html`. Push. Computer redéploie, QA sur les trois rôles.

**Sprint 6 — Stats + dashboard public (4h)**
C9 complet : indicateurs dashboard praticien, vues admin, section "En direct du collectif" sur landing, page `admin/veille.html`. Push. Computer redéploie, QA visuelle sur les trois rôles.

**Sprint 7 — Contenu (1h, facultatif)**
C10 : template data-driven, section "Articles cette saison". Push. Computer redéploie.

---

## 8. POINTS DE VIGILANCE

**Loi 25 art. 8 (information à la collecte)** : chaque champ du formulaire d'inscription doit indiquer la finalité de la collecte si elle n'est pas évidente. Le champ Téléphone doit être libellé "pour vos rappels de rendez-vous". Le champ Courriel doit mentionner qu'il sert d'identifiant de connexion.

**Loi 25 art. 14 (consentement explicite à l'inscription)** : les trois cases de consentement N1/N2/N3 doivent être présentées de façon distincte, dans un vocabulaire simple, avec des liens directs vers les politiques. Aucun pré-cochage de N2 ou N3. Aucun regroupement des trois en une seule case.

**Loi 25 art. 28.1 (droit à l'effacement et cessation de diffusion)** : rendre cette option accessible depuis la page `client/parametres.html` (à créer si absente, liste des actions disponibles depuis le compte). Mentionner le droit à l'effacement dans la politique de confidentialité publiée.

**Captcha invisible non-Google** : Cloudflare Turnstile est la recommandation principale. Alternative acceptable : hCaptcha. Ne pas utiliser reCAPTCHA (Google, incompatible avec la doctrine de données d'IVIA).

**Liste de domaines jetables** : bloquer mailinator.com, guerrillamail.com, tempmail.com, throwam.com, yopmail.com et toute la liste maintenue sur le projet open source `disposable-email-domains` (GitHub). Mettre à jour mensuellement.

**Chiffrement au repos du journal** : les entrées du journal stockent des contenus personnels sensibles (motifs de vie, états émotionnels, événements passés). Le chiffrement au repos est obligatoire même en pilote. Recommandation prioritaire : libsodium (NaCl, bindings Python disponibles). Alternative : SQLite avec extension SEE. Documenter le choix dans un commentaire Python au-dessus du modèle de données, avec la justification et les références de configuration.

**Loi 25 art. 3.4 (mesures de sécurité proportionnées)** : la sensibilité des données du journal (strate B et C) impose un niveau de protection supérieur aux données de navigation. Le chiffrement au repos, l'accès journalisé et la règle d'effacement en 30 jours sont les trois mesures minimales.

**Mobile-first** : tester systématiquement sur 390px avant desktop pour toutes les pages nouvelles. Tout bouton : zone tactile 44px minimum. La ligne de vie double SVG doit rester lisible sur 390px.

**Performance** : aucune dépendance externe non justifiée. Pas de Chart.js, pas de jQuery. La ligne de vie double est en SVG inline. Le calendrier reste en JS pur.

**Bandeau Mode démo** : maintenir sur toutes les pages internes (client/, praticien/, admin/) le bandeau "Vous testez IVIA en mode démo · [Sortir du mode démo →]" pointant vers `../tests.html`.

**Vocabulaire** : aucun terme clinique dans aucune des pages créées ou modifiées. Les mots interdits restent ceux du brief v2.0 (diagnostic, traitement, guérison, trouble, pathologie, psychothérapie, thérapie, thérapeute au sens clinique, soin clinique). S'y ajoute pour le journal : ne jamais désigner les entrées du journal comme un "bilan" ou une "évaluation".

---

## 9. LIVRAISON ATTENDUE DE COPILOT

Après chaque chantier, Copilot doit :

1. Lancer `cd ivia_mockups && python build_pages.py` et vérifier l'absence d'erreurs.
2. Tester le parcours minimal concerné sur `http://localhost:8000`.
3. Committer avec un message conventionnel (exemples ci-dessus pour chaque chantier).
4. Push sur `master` : `git push origin master`.
5. Écrire une entrée dans `04_METHODES/JOURNAL_COPILOT.md` (créer ce fichier au premier commit si absent) :

```markdown
## 2026-05-09 — C11 parcours client gradué

- Fichiers modifiés : pages_client.py, client/inscription.html (build), client/connexion.html (build), client/premier-ancrage.html (build)
- Temps estimé : 6h
- Points de friction : intégration Cloudflare Turnstile — clé de test utilisée en pilote, à remplacer par clé de production avant déploiement public
- Reste à faire : flux récupération mot de passe si courriel non validé (11f) à compléter au sprint suivant
```

Computer redéploie après validation du message de Copilot, effectue la QA visuelle (screenshots desktop 1280x900 + mobile 390x844), et remet la main à David avec un rapport court.

---

## 10. CHANGELOG v2.0 → v2.1

| Numéro | Modification | Type | Priorité |
|---|---|---|---|
| v2.1-01 | Ajout C11 — Parcours client gradué (inscription minimaliste, accès immédiat, blocage doux reconnexion, premier ancrage) | Nouveau chantier | Haute |
| v2.1-02 | Ajout C12a — Refonte `client/journal.html` : bouton Nouvelle entrée fonctionnel, structure entrée complète, ligne de vie double SVG | Correction lien mort + refonte | Haute |
| v2.1-03 | Ajout C12b — Création `client/journal-etendu.html` : page forfait / rétribution N3 au seuil gratuit | Nouveau chantier | Haute |
| v2.1-04 | Ajout C12c — Création `admin/praticien-fiche.html`, activation bouton Action sur `admin/praticiens.html`, nettoyage `href="#"` footer/sidebar admin | Correction lien mort + nouveau | Haute |
| v2.1-05 | Ajout C12d — Création `praticien/clients-journal.html` : vue digest journal clients avec consentement N2 | Nouveau chantier | Haute |
| v2.1-06 | Mise à jour ordre d'exécution sprint planning : C11 en Sprint 2, C12 en Sprint 5, C9 repoussé en Sprint 6 | Organisation | Moyen |
| v2.1-07 | Ajout points de vigilance : captcha non-Google, domaines jetables, chiffrement au repos obligatoire journal, Loi 25 art. 14 et 28.1 | Doctrine / conformité | Haute |
| v2.1-08 | Mise à jour tableau estimations globales : +14h pour C11 + C12, total cumulé ~29-30h | Estimation | Informatif |
| v2.1-09 | Référence au document `CADRAGE_PARCOURS_CLIENT_JOURNAL_v1.md` ajoutée dans les documents de référence et dans C11/C12 | Documentation | Informatif |

---

**Au sein de l'être — En actes.**
**Pour le peuple, par le peuple.**

*Brief Copilot v2.1 — 9 mai 2026*
*David Phaneuf, fondateur IVIA*
*Préparé par Computer (Perplexity)*

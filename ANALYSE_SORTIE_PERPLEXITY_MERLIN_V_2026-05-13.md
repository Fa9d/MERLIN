# Analyse sortie Perplexity - MERLIN V

Date : 2026-05-13  
Objet : integrer la sortie Perplexity dans la trajectoire IVIA / MERLIN / MESANGE et en extraire les decisions utiles.

## 1. Lecture generale

La sortie Perplexity confirme une idee deja apparue dans nos travaux : le code existe, mais l'execution coordonnee manque.

MERLIN n'est pas vide. Le backend semble deja contenir beaucoup de briques : intake, matching, auth, praticiens, sessions, notes, documents, paiement. Le probleme est que ces briques ne forment pas encore un parcours rentable et testable de bout en bout.

La faiblesse principale n'est donc pas seulement technique. Elle est operationnelle : prioriser, tester, recruter, legaliser, vendre.

## 2. Constats Perplexity a retenir

### Etat produit

- Backlog estime : 65 taches.
- Avancement estime : environ 12 %.
- Backend mature a environ 50 %.
- Frontend mature a environ 17 %.
- 21 routes backend et 18 surfaces front mentionnees.
- Chaine client -> matching -> paiement non testee bout-en-bout.

### Verrous critiques

1. Matching.
2. Onboarding praticien.
3. Fiche unique / profil praticien.
4. Recrutement du premier praticien pilote.
5. Migration 0017 non appliquee sur VPS.
6. Mentions legales / Loi 25 absentes.
7. Charge fondateur trop concentree.

### Cibles business annoncees

- 1 praticien pilote actif : 31 mai 2026.
- 3 praticiens payants en juin : environ 150 $/mois.
- 10 praticiens en aout : environ 600 $/mois.
- Stripe client actif octobre : environ 1 800 $/mois.
- Rentabilite operationnelle cible decembre 2026 : au moins 3 500 $/mois.

## 3. Analyse critique

Perplexity donne un bon audit macro, mais il melange trois dimensions qui doivent etre separees pour executer vite :

1. Produit client IVIA : parcours prospect -> intake -> compte -> reservation -> session -> suivi.
2. Produit praticien : onboarding, agenda, clients, notes IA, documents, facturation.
3. Infrastructure MERLIN : backend, migrations, auth, matching, evals, observabilite, deploiement.

Le danger serait de traiter ces trois fronts en meme temps avec la meme urgence. La bonne approche est de fermer un premier flux rentable minimal.

## 4. Clarification MESANGE

La sortie Perplexity identifie trois sens de MESANGE :

1. Ancien workspace historique importe dans MERLIN.
2. Voix publique / strategie de contenu / messager de l'ecosysteme.
3. Module B2B praticien dans le backlog MERLIN.

Cette collision de nommage est un vrai risque.

Decision recommandee :

- garder MESANGE comme voix publique, media, contenu et strategie editoriale ;
- eviter d'utiliser MESANGE comme nom technique du module B2B praticien ;
- renommer le module praticien en `IVIA Pro`, `Praticiens`, `Cabinet`, `Reseau Pro` ou autre nom plus explicite ;
- documenter cette decision pour eviter que les agents et humains parlent de choses differentes.

## 5. Lecture du chantier Copilot / Claude

La sequence sur les migrations et le matching montre un probleme de coordination, pas seulement de code.

Ce qui a mal fonctionne :

- demande de code brut trop volumineuse ;
- consommation inutile de tokens ;
- fatigue humaine ;
- validation par resume ambigu ;
- confusion entre review humaine exhaustive et validation par comportement.

Ce qui doit changer :

- valider par tests observables quand le risque est faible ou reversible ;
- demander le code complet seulement pour migrations DB, securite, donnees sensibles ou actions irreversibles ;
- exiger des sorties courtes : statut, tests lances, resultat, fixes appliques ;
- laisser l'agent coder et iterer, mais lui imposer des criteres de succes mesurables.

## 6. Regle de validation optimisee

### Pour une migration DB

Validation exigeante :

- lire la migration complete ou au minimum le diff exact ;
- verifier upgrade et downgrade ;
- verifier idempotence ou risques de doublons ;
- verifier backup / rollback ;
- lancer sur environnement non critique avant prod.

### Pour une route API reversible

Validation par comportement :

- lister la route ;
- redemarrer le service ;
- tester 2 ou 3 cas curl ;
- verifier le schema de sortie ;
- verifier que les resultats metier attendus apparaissent.

### Pour une UI

Validation par parcours :

- lancer app ;
- ouvrir navigateur ;
- tester parcours mobile / desktop ;
- verifier erreurs console ;
- screenshot si necessaire ;
- valider l'objectif utilisateur.

## 7. Phase C matching - lecture

Le chantier matching semble etre en Phase C avec trois tests clefs :

1. `POST /api/v1/matching/recommend` avec `domaine=deuil`, `langue=fr` doit remonter Solene en premier.
2. `POST /api/v1/matching/recommend` avec `domaine=identite`, `langue=fr`, `approche=psychocorporel` doit remonter Seve ou Aelis.
3. `POST /api/v1/matching/recommend-from-intake` avec `primary_need_code=distress`, `langue=fr` doit remonter Seve, Telma ou Aelis.

Champs attendus dans chaque reponse praticien :

- `abstract_palette`
- `abstract_texture`
- `abstract_motif`
- `listening_modality`
- `pilot_persona_label`
- `presentation_audio_url`

Decision : si ces trois tests passent, la Phase C peut etre consideree validee fonctionnellement, sous reserve d'un test E2E plus large ensuite.

## 8. Priorites combinees Perplexity + notre analyse

### Urgence 1 - Stabiliser infrastructure

1. Confirmer le depot canonique entre `C:\MERLIN` et `C:\MERLIN\MERLIN`.
2. Verifier migration 0017 et etat Alembic local / VPS.
3. Valider que backend et frontend se lancent de facon reproductible.
4. Documenter commandes de lancement locales.

### Urgence 2 - Fermer le parcours client

1. `rendez-vous` -> intake.
2. operator -> analyse IA.
3. matching -> praticien recommande / assigne.
4. email invitation.
5. creation compte.
6. reservation.
7. espace client minimal.

Pages manquantes ou prioritaires :

- `/connexion`
- `/creer-mon-compte`
- `/mon-espace`

### Urgence 3 - Valider le praticien pilote

Sans praticien pilote, le produit ne peut pas devenir rentable.

Actions :

- definir offre pilote ;
- message de recrutement ;
- fiche praticien publique ;
- onboarding manuel ;
- premiere session test ;
- retour qualitatif.

### Urgence 4 - Legal minimum

Avant commercialisation :

- mentions legales ;
- politique de confidentialite ;
- consentement donnees ;
- Loi 25 ;
- politique de retention ;
- clause non-medicale / accompagnement selon positionnement choisi.

### Urgence 5 - Contenu MESANGE

MESANGE peut devenir la voix publique, mais ne doit pas distraire de la conversion.

Premier contenu recommande :

- posts courts pour recruter praticiens pilotes ;
- page expliquant la demarche IVIA ;
- messages de confiance pour clients ;
- contenu educatif sur accompagnement, limites, confidentialite, deroulement.

## 9. Repartition des roles IA

### Copilot / Claude Code

- modifications backend/frontend ;
- routes ;
- pages ;
- tests ;
- migrations ;
- debug local.

Sortie attendue :

- tests lances ;
- resultat ;
- fichiers modifies ;
- risques ;
- prochain blocage.

### Perplexity

- recherche juridique ;
- sources financement ;
- benchmarking ;
- redaction v0.1 mentions legales ;
- contenu public ;
- messages de recrutement.

Sortie attendue :

- synthese courte ;
- sources ;
- texte actionnable ;
- points a valider humainement.

### MERLIN / nous

- decisions d'architecture ;
- orchestration ;
- priorisation ;
- coherence IVIA / MERLIN / MESANGE ;
- validation produit ;
- passage concept -> execution.

## 10. Recommandation immediate

Ne pas lancer 56 taches.

Lancer un sprint de 72 heures avec seulement 6 objectifs :

1. Confirmer depot canonique et etat Git.
2. Verifier migration 0017 / Alembic / VPS.
3. Valider Phase C matching avec les trois tests curl.
4. Auditer l'etat reel de `/espace-praticien` et `/rendez-vous/reserver`.
5. Creer ou specifier `/connexion`, `/creer-mon-compte`, `/mon-espace`.
6. Produire message de recrutement pour 3 praticiens pilotes.

## 11. Phrase de pilotage

Le code existe. La valeur vient maintenant de la chaine testee : un client entre, un praticien est assigne, une session est reservee, un suivi est livre, un praticien accepte de payer.

Tout ce qui ne rapproche pas cette chaine d'un test reel doit etre mis en attente.
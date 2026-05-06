# MERLIN - Plan d'execution optimal du projet V1

Date: 2026-04-21
Statut: draft
Objet: definir la voie optimale pour mener IVIA / MERLIN a terme, en precisant quand commencent le vrai build IA, BDD, hebergement et application

---

## 1) Intention

Ce plan existe pour compenser trois faiblesses humaines normales mais couteuses:
- dispersion;
- desir de completude;
- glissement entre idee forte et ordre reel d'execution.

Le principe est simple:

`on ne construit pas tout en meme temps`

et

`on ne code pas ce qui n'a pas encore de forme operatoire minimale`

---

## 2) Ce que vous devez garder en tete

Le projet comporte 5 couches qui ne se montent pas au meme moment:

1. promesse et limites du service;
2. logique metier;
3. schemas de donnees et flux produit;
4. couche technique de production;
5. couche d'optimisation et de sophistication IA.

Votre confusion actuelle est logique:
- vous voyez deja le systeme complet;
- mais le code ne commence pas par "le grand modele d'analyse";
- il commence par un noyau de traitement, de stockage, de validation et de restitution.

---

## 3) Verite importante sur le "modele d'analyse"

Au depart, MERLIN ne doit pas construire un grand modele proprietaire entraine de zero.

Le vrai `modele d'analyse` V1 est une combinaison de 6 briques:

1. un schema de donnees stable;
2. des referentiels versionnes;
3. une logique de derivation prudente;
4. un pipeline transcription -> extraction -> resume -> orientation;
5. des prompts gouvernes;
6. une validation humaine sur les points critiques.

Autrement dit:

`le modele d'analyse V1 est d'abord une architecture de traitement, pas un cerveau magique proprietaire`

Le "vrai code IA" commence donc quand on construit:
- les objets a analyser;
- les derivees autorisees;
- les prompts;
- la pipeline de production;
- les statuts de validation;
- les comparaisons inter-seances.

---

## 4) Voie optimale en 8 phases

## Phase 1 - Fermer le cadre minimal

Objectif:
- fermer ce qui est indispensable avant de coder.

Sorties attendues:
- positionnement public ferme;
- limites claires du service;
- cadre operatoire de traitement des donnees;
- noyau V1 ferme: adulte, non urgent, telephone, note, historique court, orientation simple.

Livrables:
- politique donnees V1;
- liste des objets metier V1;
- liste des champs critiques;
- liste des sorties autorisees.

Ce qu'on ne fait pas encore:
- design final;
- build praticien complet;
- logique avancée intergenerationnelle;
- rapports premium complexes.

---

## Phase 2 - Ecrire la spec produit et data

Objectif:
- traduire la pensee en systeme executable.

Sorties attendues:
- spec donnees V1;
- spec ecrans V1;
- spec pipeline IA V1;
- matrice consentements / retention / usages.

Objets a definir:
- `client`
- `intake_request`
- `consent`
- `session`
- `session_note`
- `transcript_source`
- `derived_fact`
- `risk_assessment`
- `orientation`
- `document_derived`
- `referential_version`
- `audit_event`

Ce moment est critique:
- c'est ici que commence reellement la preparation du code;
- tant que cette phase n'est pas fermee, le developpement sera bancal.

---

## Phase 3 - Monter l'ossature technique

Objectif:
- preparer le socle de production.

Ici commence le vrai travail code infrastructure.

Composants a monter:
- backend API;
- base de donnees;
- auth;
- stockage fichiers;
- gestion des secrets;
- environnement dev / test / prod;
- logs et monitoring;
- file d'attente ou jobs asynchrones.

Choix techniques recommandes pour un MVP sobre:
- `Next.js` pour le frontend;
- `FastAPI` pour le backend coeur;
- `PostgreSQL`;
- `SQLAlchemy` + `Alembic`;
- `S3/OVH Object Storage` pour fichiers audio;
- `Stripe Billing` pour abonnements si necessaire;
- `LiveKit` plus tard pour audio temps reel si conserve;
- workers asynchrones Python pour transcription et generation documentaire.

Ce qu'on code ici:
- modele de donnees;
- migrations;
- API CRUD minimale;
- audit;
- permissions;
- stockage des consentements;
- stockage des seances.

---

## Phase 4 - Construire l'entree client V1

Objectif:
- rendre le service testable en vrai.

Ce qu'on code:
- landing client V1;
- flow mobile d'entree;
- 6 a 8 questions;
- creation fiche minimale;
- consentements essentiels;
- generation du premier document simple;
- prise de rendez-vous ou demande de contact.

Important:
- pas besoin d'IA complexe pour cette phase;
- moteur template-first prioritaire.

But:
- capter;
- qualifier;
- apprendre;
- tester la promesse.

---

## Phase 5 - Construire le coeur de seance

Objectif:
- rendre l'usage coeur praticable.

Ce qu'on code:
- creation d'une seance;
- note structuree;
- historique court;
- orientation;
- documents derives simples;
- journal d'audit;
- gestion des statuts de validation.

But:
- transformer une interaction en trace utile.

Ce n'est qu'apres cette phase que MERLIN commence a ressembler a un vrai systeme.

---

## Phase 6 - Brancher la couche IA utile

Objectif:
- ajouter la valeur IA defendable.

Ce qu'on code:
- transcription asynchrone;
- extraction de faits derives;
- resume automatise;
- drapeaux rouges textuels;
- synthese post-seance;
- comparaison avec l'historique;
- rapport bref inter-seances.

Ce qu'on ne fait toujours pas:
- diagnostic automatise;
- causalite profonde machine;
- score opaque;
- lecture transgenerationnelle automatique.

But:
- augmenter la qualite documentaire;
- gagner du temps;
- rendre la memoire exploitable.

---

## Phase 7 - Monter la production

Objectif:
- passer de prototype a service fiable.

Ce qu'on met en place:
- hebergement prod;
- sauvegardes;
- supervision;
- rotation des secrets;
- politique retention;
- gestion incidents;
- tableaux de bord techniques;
- tests critiques.

Mesures minimales:
- temps de reponse;
- jobs en erreur;
- temps moyen de transcription;
- cout moyen par seance;
- taux de generation de document;
- taux de validation humaine.

---

## Phase 8 - Ouvrir la couche praticiens et optimiser

Objectif:
- industrialiser apres preuve.

Ce qu'on ajoute:
- portail pro;
- forfaits;
- historique enrichi;
- rapports mensuels;
- dashboards;
- couches de reporting;
- outillage pro plus fin.

Deux volets praticiens peuvent exister a terme:

### Volet P1 - Outillage de pratique

Valeur:
- transcription;
- resume;
- memoire de parcours;
- aide a la preparation;
- reporting longitudinal;
- documentation et continuite.

### Volet P2 - Reflexivite et formation continue

Valeur:
- lecture de la pratique du praticien;
- analyse de style ou de patterns relationnels dans un cadre prudent;
- aide a la supervision;
- formation continue aux principes IVIA / MERLIN;
- recommandations pedagogiques et outillage methodologique.

Condition:

`ce volet ne doit pas etre confondu avec une evaluation ordinale, clinique ou disciplinaire du praticien`

et

`il doit rester contractuellement clair, optionnel et gouverne`

Ce qui vient seulement ici:
- raffinements de pricing;
- optimisations de marge;
- parcours multi-praticiens;
- sophistication visuelle secondaire cote pro.

Ce qui reste explicitement hors perimetre tant que non legitimé:
- "debridage" de MERLIN sur dossiers reels en production;
- analyse profonde non bornee remise au praticien comme verite;
- fonctions assimilables a une delegation clinique ou diagnostique reservee;
- usages qui supposeraient reconnaissance formelle par ordre, organisme ou cadre legal non encore acquis.

---

## 5) Reponse directe: quand commence le vrai developpement code

Il commence en realite a deux moments:

### Moment 1 - Fin de la Phase 2

Quand la spec data et la spec produit V1 sont fermees.

Sans cela:
- vous codez a l'aveugle;
- vous refaites les schemas;
- vous vous eparpillez.

### Moment 2 - Phase 3

Quand on monte:
- API;
- BDD;
- auth;
- stockage;
- infrastructure de jobs.

### Le developpement IA proprement dit commence surtout en Phase 6

Pas avant.

Avant la Phase 6, on prepare le terrain.
En Phase 6, on branche:
- transcription;
- extraction;
- resume;
- comparaison historique;
- rapport.

---

## 6) Ce que vous avez tendance a faire trop tot

### Derive 1

Vouloir finaliser la philosophie profonde avant de fermer le service testable.

### Derive 2

Vouloir parler prix avant d'avoir ferme la valeur et le flux.

### Derive 3

Vouloir refaire le site visuellement avant d'avoir fige:
- systeme visuel;
- spec ecrans;
- CTA;
- structure d'entree.

### Derive 4

Vouloir ouvrir la couche praticien avant d'avoir une entree client testee.

### Derive 5

Vouloir un grand modele d'analyse avant d'avoir:
- les champs;
- les objets derives;
- l'audit;
- la validation humaine.

### Derive 6

Vouloir faire du stockage physique manuel la strategie normale de production pour des sources audio sensibles.

---

## 7) Regle d'alerte de deviation

A partir de maintenant, toute demande devrait etre relue contre ce plan.

Je dois signaler explicitement une deviation si vous demandez, trop tot:
- un raffinement graphique majeur avant la spec produit;
- des fonctions pro avancees avant le coeur client;
- une IA "ultime" avant la pipeline V1;
- un pricing final avant validation du produit coeur;
- l'integration de couches doctrinales profondes dans le MVP;
- une nouvelle famille de soin avant la fermeture des objets V1.

Formule d'alerte a utiliser:

`Deviation au plan: cette demande ouvre la phase X alors que la phase Y n'est pas fermee.`

Puis:
- ce que cela coute;
- ce que cela retarde;
- si l'on accepte malgre tout ou si on le remet en backlog.

---

## 8) Ordre optimal immediat

Si je tranche pour vous, l'ordre optimal maintenant est:

1. ecrire le cadre operatoire de traitement des donnees;
2. ecrire la spec donnees V1;
3. ecrire la spec ecrans V1 du parcours client;
4. choisir et figer la stack technique;
5. monter backend + BDD + auth + stockage;
6. coder le flow d'entree client;
7. coder session + note + orientation;
8. brancher transcription + resume + historique;
9. seulement ensuite refaire le site final et la couche pro.

Concernant l'audio, la ligne cible est:

1. stockage chaud court terme;
2. transcription et derives;
3. retention courte ou archivage froid chiffre;
4. sauvegardes conformes et testees;
5. economie ajustee selon seuils de rentabilite.

Decision complementaire active:

- l'audio cible de MERLIN vit dans l'application;
- cette logique vaut aussi pour l'offre praticiens;
- le telephone ou les outils externes ne sont que des fallbacks transitoires;
- l'ordre technique devient: `seance -> demarrage -> audio in-app -> enregistrement -> transcription`.

Une double sauvegarde physique en deux lieux peut exister:
- comme mesure transitoire ou tertiaire;
- ou comme archive froide exceptionnelle;

mais pas comme socle principal de production, d'indexation et d'audit.

---

## 9) Ce que vous devez comprendre sur le code

Le code n'arrive pas "a la fin".
Le code commence juste apres la spec systeme.

Mais il y a deux types de code:

### Code de structure

- schemas BDD;
- API;
- auth;
- stockage;
- audit;
- workers.

### Code de valeur

- flow client;
- note de seance;
- resume;
- rapport;
- historique;
- orientation.

Tant que le code de structure n'existe pas, le code de valeur est fragile.
Tant que le code de valeur n'existe pas, l'IA ne sert a rien.

---

## 10) Definition de succes a court terme

Le projet est sur la bonne voie si, dans un premier cycle de build, on peut:

1. accueillir une demande client;
2. enregistrer le consentement;
3. creer une fiche;
4. produire une seance;
5. sortir une note utile;
6. generer un document derive simple;
7. relier cela a l'historique;
8. brancher ensuite transcription et resume.

Si cela fonctionne, MERLIN existe reellement.
Le reste devient optimisation.

---

## 11) Observations structurantes a ne pas oublier

### O-01 - Analyse des praticiens

Au meme titre que le client, le praticien peut devenir un objet de lecture et d'accompagnement.

Mais il faut distinguer:
- aide a la reflexivite;
- aide a la supervision;
- formation continue;

de:
- evaluation ordinale;
- evaluation disciplinaire;
- pretention clinique sur le praticien.

### O-02 - Formation continue IVIA

Une offre payante de formation continue aux pratiques et principes IVIA peut devenir un second moteur economique B2B.

Cette offre est credible si elle repose sur:
- doctrine claire;
- methodes explicites;
- cas d'usage prudents;
- evidence terrain minimale.

### O-03 - Evolution possible de legitimite

Le systeme doit rester techniquement extensible vers:
- plus de profondeur analytique;
- plus de fonctions praticiens;
- plus de relations avec des professions reconnues;

mais sans presumer aujourd'hui d'un droit futur non encore acquis.

### O-04 - Economie du stockage audio

L'audio est le poste memoire principal.
La strategie doit etre pilotee par:
- cout par seance;
- retention voulue;
- besoin reel de reanalyse;
- seuils de rentabilite;
- niveau de securite requis.

### O-05 - Principe de transition technique

Quand MERLIN est petit:
- architecture economique acceptable;
- mais deja gouvernee;
- deja auditable;
- deja exportable.

Puis:
- bascule vers une architecture plus standardisee des que le volume, le risque ou la valeur en jeu le justifie.

---

## 12) Decision active

MERLIN adopte la discipline suivante:

- on ferme Phase 1 et Phase 2 avant de disperser davantage le travail;
- on commence le vrai code par l'ossature technique et le parcours client V1;
- on ne traite l'IA avancee qu'apres l'existence d'un systeme de donnees, de consentements, de notes et d'historique exploitable.

References:
- [MERLIN_GOUV_AUDIT_OLD_REPERTOIRES_REUTILISABLES_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_AUDIT_OLD_REPERTOIRES_REUTILISABLES_V1.md)
- [MERLIN_GOUV_ARBITRAGE_REFAIRE_ARCHIVER_REPRENDRE_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_ARBITRAGE_REFAIRE_ARCHIVER_REPRENDRE_V1.md)
- [MERLIN_GOUV_DECISION_AUDIO_DANS_APP_OPERATEURS_PRATICIENS_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_DECISION_AUDIO_DANS_APP_OPERATEURS_PRATICIENS_V1.md)

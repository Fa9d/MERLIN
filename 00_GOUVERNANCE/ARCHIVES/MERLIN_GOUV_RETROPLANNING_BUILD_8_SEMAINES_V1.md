# MERLIN - Retroplanning build 8 semaines V1

Date: 2026-04-21
Statut: draft
Objet: definir un plan de build 8 semaines pour aller vers une version facturable et testable

---

## 1) Hypotheses

Ce retroplanning suppose:
- une petite equipe ou founder-led build;
- pas de dette technique heritee;
- stack V1 sobre;
- architecture front / back separee;
- perimetre V1 respecte;
- pas de re-ouverture majeure du fond en milieu de build.

Ce retroplanning vise:
- une beta facturable;
- pas une plateforme parfaite.

---

## 2) Definition du succes a 8 semaines

A la fin de 8 semaines, MERLIN / IVIA doit pouvoir:
- accueillir une demande client;
- enregistrer les consentements;
- creer une fiche client;
- prendre un rendez-vous ou une demande de contact;
- ouvrir une seance;
- produire une note structuree;
- generer un document derive simple;
- garder un historique court;
- brancher transcription optionnelle;
- envoyer les confirmations essentielles;
- operer un faible volume reel de clients payants.

---

## 3) Jalons majeurs

### Jalon A - Fin semaine 2

Le socle technique existe.

### Jalon B - Fin semaine 4

Le parcours client et le backoffice minimal existent.

### Jalon C - Fin semaine 6

Le coeur operatoire de seance existe.

### Jalon D - Fin semaine 8

La beta facturable existe.

---

## 4) Semaine par semaine

## Semaine 1 - Setup et fondations

Objectifs:
- creer le projet app;
- figer la stack;
- brancher DB;
- installer ORM;
- preparer auth.

Livrables:
- frontend initial
- backend initial
- environnement dev
- environnement staging
- schema SQLAlchemy initial version 0
- migration Alembic initiale
- roles minimum
- conventions de nommage

Sorties:
- frontend demarre
- backend demarre
- DB connectee
- migrations ok

Risques:
- dispersion stack
- surchoix d'outils

---

## Semaine 2 - Modele de donnees coeur

Objectifs:
- implementer les tables coeur V1.

Livrables:
- `client`
- `intake_request`
- `consent`
- `session`
- `session_note`
- `document_derived`
- `client_timeline_event`
- `audit_event`

Sorties:
- CRUD minimal backend
- audit de base

Jalon:
- `Jalon A`

---

## Semaine 3 - Parcours client public

Objectifs:
- coder les ecrans client initiaux.

Livrables:
- landing V1
- prequalification
- consentements
- fiche minimale
- confirmation
- demande de rendez-vous / rappel

Sorties:
- un client peut entrer dans le systeme
- les objets sont crees en base

Risques:
- trop travailler le design
- re-ouvrir le wording en boucle

---

## Semaine 4 - Backoffice operateur minimal

Objectifs:
- coder le tableau operateur et la fiche client.

Livrables:
- dashboard operateur
- fiche client
- ouverture de seance
- historique court lecture simple

Sorties:
- operateur peut voir, ouvrir et suivre un dossier

Jalon:
- `Jalon B`

---

## Semaine 5 - Coeur de seance

Objectifs:
- coder la note structuree et l'orientation.

Livrables:
- ecran conduite de seance minimal
- ecran note structuree
- ecran orientation
- timeline enrichie
- validations metier critiques

Sorties:
- une seance peut etre documentee proprement

---

## Semaine 6 - Documents derives et emails

Objectifs:
- produire la restitution utile.

Livrables:
- generation `entry_summary`
- generation `session_summary`
- email confirmation / suivi
- document remis et journalise

Sorties:
- valeur client visible
- valeur facturable plus concrete

Jalon:
- `Jalon C`

---

## Semaine 7 - Audio, transcription, jobs

Objectifs:
- brancher la couche audio / transcription utile.

Livrables:
- `audio_source`
- stockage objet
- upload simple
- job transcription async
- `transcript_source`
- premiers derives IA simples

Sorties:
- transcription optionnelle fonctionne
- pas encore perfectionnee, mais exploitable

Risques:
- vouloir trop de sophistication IA

---

## Semaine 8 - Stabilisation et beta facturable

Objectifs:
- fermer la beta.

Livrables:
- supervision minimale
- journal d'audit consultable
- flow client -> operateur -> document complet
- paiement simple
- checklist lancement
- mini monitoring
- sauvegardes

Sorties:
- quelques premiers clients peuvent etre accueillis reellement

Jalon:
- `Jalon D`

---

## 5) Conditions de mise en production beta

Avant de lancer la beta facturable, il faut au minimum:
- consentements clairs en place
- non-urgence explicite
- sauvegarde testee
- note obligatoire
- document derive simple
- flux de rendez-vous fonctionnel
- audit minimum
- politique de retention minimale appliquee

---

## 6) Ce qu'on reporte hors des 8 semaines

- design haut de gamme final
- portail praticiens avance
- dashboards riches
- comparaisons longitudinales sophistiquees
- formation continue praticiens
- couche research visible
- intergenerationnel outille en profondeur
- multi-tenant ou multi-equipe complexe

---

## 7) Version facturable la plus rapide

Si vous voulez facturer encore plus vite que 8 semaines, il existe une voie `concierge`.

### Option concierge en 2 a 4 semaines

Ce qu'on lance:
- landing simple
- prise de contact
- paiement simple
- seance humaine
- note et document semi-manuels

Ce qu'on n'a pas encore:
- vrai backoffice propre
- vraie couche transcription integree
- audit complet

C'est acceptable si:
- faible volume;
- cas simples;
- fort controle manuel.

---

## 8) Charge critique et vigilance

Les 5 risques qui menacent ce retroplanning:
- re-ouvrir le fond en semaine 3 ou 4;
- sur-investir le design avant le coeur operatoire;
- ouvrir la couche praticien avancee trop tot;
- chercher une IA trop "intelligente" avant la stabilite data;
- ne pas borner le scope V1.

Formule d'alerte:

`Deviation au plan: cette demande menace le jalon en cours et repousse la beta facturable.`

---

## 9) Decision active

Ce retroplanning devient la base de pilotage du build V1.

Ordre reel:
- spec fermee
- socle technique
- parcours client
- coeur de seance
- documents derives
- audio / transcription
- beta facturable

References:
- [MERLIN_GOUV_CHOIX_STACK_TECHNIQUE_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_CHOIX_STACK_TECHNIQUE_V1.md)
- [MERLIN_GOUV_SPEC_DONNEES_V1_IVIA_MERLIN.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_SPEC_DONNEES_V1_IVIA_MERLIN.md)
- [MERLIN_GOUV_SPEC_ECRANS_V1_PARCOURS_CLIENT_IVIA_MERLIN.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_SPEC_ECRANS_V1_PARCOURS_CLIENT_IVIA_MERLIN.md)
- [MERLIN_GOUV_PLAN_EXECUTION_OPTIMAL_PROJET_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_PLAN_EXECUTION_OPTIMAL_PROJET_V1.md)

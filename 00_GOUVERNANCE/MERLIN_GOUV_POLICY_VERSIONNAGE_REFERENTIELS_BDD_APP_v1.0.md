# MERLIN - Politique de versionnage des referentiels, BDD et application (v1)

Date: 2026-04-20
Statut: draft
Objet: permettre l'evolution continue des fiches, listes, schemas et regles sans casser le fonctionnement interne, la base de donnees ou l'application

---

## 1) Finalite

MERLIN doit pouvoir:
- ajourner;
- corriger;
- clarifier;
- enrichir;
- deprecier;
- remplacer;

ses documents, schemas, fiches et referentiels, a tout moment, sans provoquer de conflit de fonctionnement.

Cette exigence devient critique des qu'il existe:
- une base de donnees;
- une application en ligne;
- des objets lus par machine;
- des consentements;
- des historiques clients;
- des regles de triage;
- des documents derives.

---

## 2) Principe directeur

MERLIN ne doit pas reposer sur une confusion entre:
- document de travail;
- reference canonique;
- donnee applicative;
- vue interface;
- archive historique.

Doctrine:

`une information peut evoluer librement seulement si son role systeme est explicite`

---

## 3) Les 5 couches a distinguer

### Couche 1 - Doctrine et texte humain

Exemples:
- politiques
- playbooks
- fiches explicatives
- cadres conceptuels

Role:
- expliquer;
- justifier;
- former;
- documenter les choix.

Cette couche n'est pas la source directe d'execution applicative.

### Couche 2 - Referentiels structures

Exemples:
- services d'orientation
- regles de triage
- taxonomies de besoins
- niveaux de risque
- statuts de consentement

Role:
- servir de source canonique lisible par machine.

Cette couche doit etre stable, versionnee et identifiable.

### Couche 3 - Donnees transactionnelles

Exemples:
- fiche client
- seance
- note
- consentement donne a date X
- transmission a un tiers

Role:
- enregistrer ce qui s'est passe reellement.

Cette couche ne doit jamais etre reecrite retroactivement comme si le passe n'avait pas existe.

### Couche 4 - Vues produit

Exemples:
- ecran d'inscription
- formulaire operateur
- page de synthese
- document PDF remis au client

Role:
- presenter les donnees et guider l'action.

Cette couche peut changer souvent, mais elle ne doit pas redefinir seule les regles metier.

### Couche 5 - Historique et audit

Exemples:
- versions precedentes
- journal de modifications
- migrations de schema
- changelog de referentiel

Role:
- prouver ce qui a change;
- quand;
- pourquoi;
- par qui;
- avec quel impact.

---

## 4) Source de verite recommandee

### Doctrine

Source de verite:
- documents Markdown versionnes.

### Regles et referentiels machine

Source de verite:
- schemas et fichiers structures versionnes.

### Activite client

Source de verite:
- base de donnees transactionnelle.

### Interface

Source de verite:
- application.

Regle:

`l'application consomme les referentiels; elle ne les reinvente pas`

et

`la BDD conserve les faits; elle ne remplace pas la doctrine`

---

## 5) Regles anti-conflit

### Regle 1 - Identifiants stables

Tout objet machine doit avoir un identifiant stable.

Exemples:
- `svc_psychologue_public_qc`
- `triage_suicide_imminent_v1`
- `risk_urgent`
- `consent_transcription`

Un libelle peut changer.
L'identifiant ne doit pas changer sans migration explicite.

### Regle 2 - Statuts explicites

Tout objet de referentiel doit pouvoir porter un statut:
- `draft`
- `review`
- `validated`
- `deprecated`
- `archived`

Un objet obsolete ne doit pas disparaitre silencieusement s'il a deja ete utilise.

### Regle 3 - Compatibilite descendante par defaut

Un changement ne doit pas casser:
- les seances deja notees;
- les documents deja emis;
- les orientations deja enregistrees;
- les historiques deja relies a d'anciens codes.

Si la compatibilite descendante est impossible:
- migration obligatoire;
- journal de changement obligatoire;
- date d'effet obligatoire.

### Regle 4 - Pas de suppression logique brutale

Pour les objets deja utilises en production:
- preferer `deprecated` a suppression;
- preferer `soft delete` a effacement;
- conserver le mapping ancien -> nouveau.

### Regle 5 - Separer contenu et presentation

Une fiche de service peut etre reecrite pour etre plus claire.
Mais:
- sa structure machine;
- son identifiant;
- ses champs critiques;

ne doivent pas etre modifies au hasard dans l'interface.

---

## 6) Ce que la BDD doit stocker

La BDD ne doit pas seulement stocker des textes libres.

Elle doit stocker:
- les identifiants canoniques;
- la version du referentiel utilise;
- les valeurs selectionnees;
- la date et l'heure;
- la personne ou le systeme auteur;
- le statut;
- la trace de consentement;
- la trace de transmission;
- la classe de retention.

Exemple:

une note de seance devrait idealement conserver:
- `session_id`
- `client_id`
- `besoin_dominant_code`
- `niveau_risque_code`
- `orientation_codes`
- `referentiel_version`
- `created_at`
- `updated_at`

Ainsi, si les libelles changent plus tard, l'historique reste interpretable.

---

## 7) Ce que l'application doit respecter

L'application doit etre concue avec:

### A. Donnees metier structurees

Pas seulement des champs texte.

Il faut:
- listes de valeurs;
- enums versionnes;
- taxonomies;
- liens vers referentiels.

### B. Validation de saisie

Exemples:
- pas de `transcript_exists = true` sans consentement transcription;
- pas de transmission tiers sans consentement correspondant;
- pas de cloture standard si bascule urgence active sans trace minimale.

### C. Migrations explicites

Quand un schema change:
- migration BDD;
- migration API;
- migration interface si necessaire;
- documentation du changement.

### D. Mode lecture historique

L'application doit pouvoir relire un ancien dossier avec les anciennes references, meme si le referentiel courant a evolue.

---

## 8) Workflow de changement recommande

### Type A - Clarification redactionnelle

Exemple:
- reformuler une fiche;
- corriger un libelle;
- ajouter un exemple.

Impact:
- doctrine / interface.

Action:
- pas de migration BDD si les identifiants restent stables.

### Type B - Evolution de referentiel

Exemple:
- nouveau service;
- nouveau niveau de risque;
- nouvelle categorie de besoin;
- nouvelle regle de triage.

Impact:
- schemas;
- referentiels;
- potentiellement application.

Action:
- version de referentiel;
- tests de compatibilite;
- changelog.

### Type C - Rupture de schema

Exemple:
- renommer un champ machine;
- scinder un objet en deux;
- changer la logique de consentement;
- modifier la structure d'historique.

Impact:
- BDD;
- API;
- application;
- exploitation historique.

Action:
- migration formelle;
- plan de rollback;
- date d'entree en vigueur;
- revue des impacts.

---

## 9) Objets supplementaires a formaliser avant l'application

Pour passer proprement en base de donnees et application, MERLIN doit encore definir ou durcir:

1. `registre des identifiants canoniques`
- services
- regles
- besoins
- risques
- consentements

2. `policy de version de referentiel`
- numero de version
- date d'effet
- compatibilite
- mapping ancien/nouveau

3. `journal d'audit`
- qui a change quoi
- quand
- pourquoi

4. `matrice des roles et acces`
- operateur
- superviseur
- admin contenu
- admin technique

5. `politique de retention et suppression`
- audio
- transcription
- note
- historique
- transmissions

6. `strategie de migration`
- dev
- test
- production

7. `regles de generation de documents derives`
- quelles donnees peuvent sortir
- sous quelle forme
- avec quels disclaimers

---

## 10) Ce que tu n'as pas oublie

Ton intuition de base est juste:
- oui, tout doit pouvoir etre modifie;
- oui, cela doit etre prevu avant la BDD et l'application;
- oui, la formalisation interne doit deja penser machine, version, historique et coexistence des versions.

---

## 11) Ce que tu risques sinon

Si on ne formalise pas cela maintenant, les risques sont:
- conflit entre le texte des docs et la logique de l'app;
- anciennes fiches devenues incomprehensibles;
- historique client illisible apres refonte;
- codes instables;
- migrations douloureuses;
- derives documentaires incoherents;
- perte d'auditabilite;
- erreurs de consentement ou de transmission.

---

## 12) Rectifications de pensee recommandees

### Rectification 1

Ne pas viser:
- `tout peut changer librement`

mais:
- `tout peut evoluer dans une gouvernance de changement`

### Rectification 2

Ne pas penser:
- `les documents suffiront`

mais:
- `il faut un contrat entre doctrine, referentiel, BDD et app`

### Rectification 3

Ne pas penser:
- `mettre en base = figer`

mais:
- `mettre en base = rendre versionnable et interpretable dans le temps`

### Rectification 4

Ne pas penser:
- `une interface claire suffit`

mais:
- `une interface claire doit reposer sur des objets stables et traces`

---

## 13) Decision active

MERLIN adopte le principe suivant:

`aucune couche applicative ne doit dependre d'un texte libre non versionne comme seule source metier`

et:

`tout objet critique utilise par l'application doit disposer d'un identifiant stable, d'un statut, d'une version et d'un historique de changement`

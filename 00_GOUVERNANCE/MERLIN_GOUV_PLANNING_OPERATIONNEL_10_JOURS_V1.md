# MERLIN - Planning operationnel 10 jours V1

Date: 2026-04-26
Statut: actif
Objet: figer l'etat reel du projet MERLIN, situer l'avancement par rapport au plan initial, et organiser les 10 prochains jours ouvrables vers un pilote ferme exploitable

---

## Mise a jour execution 2026-04-26

Etat court:

- `J1` valide en production: VPS redeployable, healthcheck API OK, procedure manuelle de rebuild / restart backend rejouee.
- la procedure canonique de redeploiement backend standard VPS est maintenant documentee pour limiter l'improvisation future.
- `J2` valide en production: validation des notes reservee a `supervisor`, separation minimale `operator` / `supervision` en backend et frontend.
- `J3` valide en production: cloisonnement de lecture confirme sur `sessions`, `session_notes`, `derived_documents`, `audio_sessions`, `audio_recordings`.
- `J4` valide en production: acces public `/suivi` borne par `public_client_code + intake_request_id`, verification negative `404` confirmee sur une mauvaise reference d'entree.
- `J5` valide en production: diffusion client conditionnee par validation `supervisor`, document d'abord cree en `client_pending_review` puis publie en `client` apres validation.
- `J6` valide en production: frontend IVIA deployee sur `https://ivia.quebec`, routes publiques et internes principales servies par nginx, TLS multi-domaine corrige et renouvellement Certbot simule avec succes.
- prochain chantier recommande: `J7 - Supervision exploitable`.

Constats de preuve:

- `operator 1` ne voit pas les objets crees par `operator 2`;
- `operator 2` voit uniquement ses objets;
- `supervisor` voit l'ensemble des objets de test;
- les acces directs d'un operateur vers les objets d'un autre operateur repondent `404`.
- `https://ivia.quebec`, `https://ivia.quebec/rendez-vous`, `https://ivia.quebec/suivi`, `https://ivia.quebec/operator` et `https://ivia.quebec/supervision` repondent `200`;
- `https://api.ivia.quebec/api/health` repond `200` avec `status = ok`;
- la validation d'une note par `operator` repond `403`;
- la validation d'une note par `supervisor` repond `200`;
- la lecture operateur du document derive de sa seance repond `200`.

Point ouvert separe:

- un enregistrement audio de test est remonte en statut `failed`; ce point concerne la chaine d'enregistrement et non le cloisonnement des droits.

---

## 1) Lecture courte

MERLIN n'est plus au stade de simple cadrage.

Le projet est entre:

- la fin du `noyau V1 fonctionnel`
- et le debut du `durcissement produit / droits / exploitation`

Concretement:

- le backend API existe et tourne;
- la base et les migrations existent;
- l'auth existe;
- les objets metier principaux existent;
- le flux `client -> intake -> session -> note -> document derive` a ete teste en production;
- la couche IA utile est deja branchee avec generation de note et document derive;
- un frontend existe avec surfaces `rendez-vous`, `suivi`, `operator`, `admin`, `supervision`, `audio-test`.

Le retard principal n'est donc pas un retard de build brut.

Le vrai travail restant avant un deploiement V1 propre est:

- fermer les droits;
- separer les surfaces;
- clarifier le flux client reel;
- stabiliser la supervision;
- assainir l'exploitation VPS;
- finaliser un parcours testable sans confusion entre dev, ops et usage reel.

---

## 2) Position dans le plan initial

Reference: `MERLIN_GOUV_PLAN_EXECUTION_OPTIMAL_PROJET_V1.md`

### Phase 1 - Fermer le cadre minimal

Etat:

`largement fait`

Justification:

- cadre adulte / non urgent / V1 simple deja retenu;
- gouvernance des objets, consentements et sorties deja documentee.

### Phase 2 - Ecrire la spec produit et data

Etat:

`largement fait`

Justification:

- spec donnees existante;
- spec ecrans existante;
- tableau consentements / diffusion existant;
- backlog roles / acces deja explicite.

### Phase 3 - Monter l'ossature technique

Etat:

`bien avance`

Justification:

- backend FastAPI en place;
- PostgreSQL + Alembic en place;
- auth en place;
- routes metier principales en place;
- prod VPS deja deployee.

### Phase 4 - Construire l'entree client V1

Etat:

`partiellement fait`

Justification:

- surfaces frontend presentes;
- mais le flux client gouverne reste encore incomplet ou trop lie a des usages de test.

### Phase 5 - Construire le coeur de seance

Etat:

`bien avance`

Justification:

- creation session;
- fermeture session;
- note structuree;
- derive documentaire;
- audio / room / recording deja amorces.

### Phase 6 - Brancher la couche IA utile

Etat:

`partiellement a bien avance`

Justification:

- generation IA reelle validee en production;
- mais supervision, validation et workflow de diffusion restent a durcir.

### Phase 7 - Durcir pour la production

Etat:

`partiel`

Justification:

- la prod existe;
- mais les droits, le runtime VPS et la methode de redeploiement restent fragiles.

### Phase 8 - Optimisation / couche praticien plus mature

Etat:

`non lance proprement`

Justification:

- pas encore de couche praticien propre et separee;
- pas encore de finition produit exploitable a plus grande echelle.

---

## 3) Temps deja consomme

Point de reference de cadrage:

- 2026-04-21: plan d'execution;
- 2026-04-22: backlog roles / acces;
- 2026-04-24 au 2026-04-25: verification et corrections prod reelles.

Lecture pragmatique:

- environ `1 semaine calendrier` a ete consommee depuis le cadrage formel;
- environ `4 a 5 jours ouvrables reels` ont produit un noyau backend/front significatif plus avance que prevu;
- une partie du temps recent a ete perdue en `redeploiement manuel`, `derive prod/local` et `incident Docker/containerd`.

Conclusion:

`le projet n'est pas lent sur le produit`

Il a surtout subi:

- des frictions d'exploitation;
- des melanges de surfaces;
- un manque de verrouillage final sur les roles et le parcours cible.

---

## 4) Estimation du temps restant

## Objectif A - Pilote ferme propre

Definition:

- quelques comptes internes ou tests encadres;
- flux client simple;
- operateur capable de produire une seance et une sortie;
- supervision minimale;
- prod suffisamment stable pour tester sans bricolage continu.

Temps restant estime:

`5 a 10 jours ouvrables`

Condition:

- se concentrer sur les chantiers critiques seulement;
- ne pas ouvrir de nouvelles ambitions produit en parallele.

## Objectif B - V1 presentable et plus propre cote exploitation

Definition:

- surfaces plus nettes;
- droits plus clairs;
- public client mieux gouverne;
- checklists de deploiement et de recette.

Temps restant estime:

`2 a 4 semaines`

## Objectif C - V1 plus robuste et extensible

Definition:

- vraies frontieres de roles;
- supervision et validation plus serieuses;
- exploitation VPS assainie;
- base solide pour praticiens / pilotage / extension.

Temps restant estime:

`4 a 6 semaines`

---

## 5) Objectif du sprint 10 jours

Objectif retenu:

`rendre MERLIN pilotable en pilote ferme sans dette critique evidente`

Cela veut dire:

- un flux testable de bout en bout;
- des droits moins permissifs;
- une separation minimum des surfaces;
- une prod moins fragile;
- une recette simple et repetable.

---

## 6) Non-objectifs du sprint

Ce sprint ne doit pas chercher a terminer:

- le portail praticien complet;
- la sophistication IA avancee;
- la recherche longue;
- la couche commerciale complete;
- la finition UI generale;
- les scenarios complexes multi-organisations.

Regle:

`on ferme le pilote avant d'ouvrir la plateforme large`

---

## 7) Plan operationnel J1 a J10

## J1 - Stabilisation exploitation

Livrables:

- verifier l'etat exact du VPS apres l'incident Docker/containerd;
- remettre le systeme paquets dans un etat propre;
- figer une procedure de redeploiement backend standard;
- verifier `docker ps`, healthchecks, restart simple et rollback minimal.

Sortie attendue:

- infra suffisamment fiable pour ne plus perdre du temps sur le runtime.

Reference:

- [MERLIN_GOUV_CHECKLIST_STABILISATION_VPS_J1_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_CHECKLIST_STABILISATION_VPS_J1_V1.md)
- [MERLIN_GOUV_PROCEDURE_REDEPLOIEMENT_STANDARD_VPS_BACKEND_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_PROCEDURE_REDEPLOIEMENT_STANDARD_VPS_BACKEND_V1.md)

## J2 - Verrouillage backend roles

Livrables:

- introduire des dependances de roles nommees;
- retirer `admin_tech` des lectures metier non necessaires;
- clarifier la frontiere `operator` vs `supervisor` sur les routes critiques.

Sortie attendue:

- backend moins permissif et lisible.

## J3 - Perimetres et lecture utile

Livrables:

- ajouter des filtres de lecture minimaux par contexte;
- limiter les listes globales;
- preparer la logique `mes dossiers / dossier cible / lot supervision`.

Sortie attendue:

- reduction du risque de lecture trop large.

Etat:

`valide en production`

Verification realisee:

- filtres de lecture actives par `operator_user_id`;
- verification positive sur listes et lectures directes pour `sessions`, `session_notes`, `derived_documents`, `audio_sessions`, `audio_recordings`;
- verification negative confirmee: un operateur ne peut pas lire les objets d'un autre operateur.

## J4 - Flux client reel minimal

Livrables:

- distinguer le vrai flux client du flux de test;
- clarifier la route ou la page de diffusion client;
- verifier la lecture des documents derives par reference client.

Sortie attendue:

- une surface client V1 simple mais gouvernee.

Etat:

`valide en production`

Verification realisee:

- la route publique `GET /api/v1/derived-documents/public/client/{public_client_code}?intake_request_id=...` exige bien la paire `public_client_code + intake_request_id`;
- verification positive confirmee sur un client de test connu;
- verification negative confirmee: une mauvaise reference d'entree retourne `404`.

## J5 - Workflow diffusion / validation

Livrables:

- stabiliser l'usage de `client_visible`;
- poser un statut documentaire V1.1 ou une convention claire de diffusion;
- preciser quand un document est seulement genere, valide, puis effectivement diffusable.

Sortie attendue:

- pas de confusion entre generation interne et remise client.

Etat:

`valide en production`

Verification realisee:

- cloture de seance avec `client_visible = true` cree d'abord un document `client_pending_review` non public;
- la tentative de validation de note par `operator` retourne `403`;
- la validation de la note par `supervisor` retourne `200`;
- apres validation `supervisor`, le document passe en `audience_code = client` et `client_visible = true`;
- la route publique `/suivi` retourne alors bien le document diffusable.

## J6 - Separation minimale des interfaces

Livrables:

- nettoyer `/operator`;
- sortir ce qui releve du bootstrap admin;
- isoler ce qui releve du test audio/dev;
- garder une surface operateur centree sur production.

Sortie attendue:

- moins de confusion entre demonstration, administration et usage reel.

Etat:

`valide en production`

Verification realisee:

- le frontend Next.js `09_app_ivia_merlin` est integre au stack prod via `docker-compose.prod.yml` et `nginx`;
- les routes `/`, `/rendez-vous`, `/suivi`, `/operator`, `/supervision` sont servies en production;
- la variable `NEXT_PUBLIC_MERLIN_API_BASE_URL` est renseignee en prod vers `https://api.ivia.quebec`;
- le certificat TLS multi-domaine `api.ivia.quebec + ivia.quebec` est actif;
- le renouvellement Certbot est simule avec succes apres nettoyage des anciennes configurations cassees.

## J7 - Supervision exploitable

Livrables:

- rendre la surface `/supervision` utile pour la relecture;
- verifier la validation/correction des notes;
- clarifier les actions permises au `supervisor`.

Sortie attendue:

- supervision minimale reelle, pas seulement symbolique.

## J8 - Recette end-to-end

Livrables:

- script ou checklist unique de recette:
  - creation utilisateur
  - login
  - creation client
  - intake
  - session
  - close
  - generation note
  - generation document
  - lecture cote operateur
  - lecture cote client
- nettoyage des traces de test documente.

Sortie attendue:

- capacite de rejouer un test complet sans improvisation.

Artefact associe:

- checklist de recette prod e2e: [MERLIN_GOUV_CHECKLIST_RECETTE_PROD_E2E_J8_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_CHECKLIST_RECETTE_PROD_E2E_J8_V1.md)

Etat:

`valide en production`

Verification realisee:

- authentification `operator` et `supervisor` rejouee en prod avec comptes de test dedies;
- creation publique d'un `client` et d'une `intake_request` rejouee depuis zero;
- creation et cloture d'une `session` par `operator` rejouees en prod;
- verification avant validation: document derive present en `client_pending_review`, non visible publiquement;
- verification negative: route publique `/suivi` retourne `[]` avant validation et `404` avec une mauvaise `intake_request_id`;
- verification negative: tentative de validation de note par `operator` rejouee et rejetee en `403`;
- verification positive: validation de la note par `supervisor` rejouee et acceptee en `200`;
- verification finale: le document devient visible dans `/suivi` apres validation supervision.

## J9 - Correctifs UX / bugs bloquants

Livrables:

- corriger les points irritants observes en recette;
- simplifier les libelles ou champs inutiles;
- corriger les erreurs de parcours les plus visibles.

Sortie attendue:

- experience suffisamment nette pour un pilote ferme.

## J10 - Go / no-go pilote

Livrables:

- revue finale des criteres de sortie;
- liste des risques restants;
- decision `pret pilote ferme` ou `1 mini-sprint supplementaire`.

Sortie attendue:

- decision explicite, documentee, defendable.

Etat courant:

`pret a instruire`

Base factuelle disponible:

- `J1` a `J8` sont desormais verifies en production sur les points critiques d'infra, droits, diffusion client, supervision et recette e2e;
- le sujet prioritaire n'est plus la faisabilite technique mais la decision d'ouverture du pilote ferme et la liste courte des risques residuels.

Etat:

`valide`

Decision:

`GO pilote ferme encadre`

Limite explicite:

`NO-GO pour une ouverture large`

Artefact associe:

- decision go / no-go: [MERLIN_GOUV_DECISION_GO_NO_GO_PILOTE_FERME_2026-04-26_v1.0.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_DECISION_GO_NO_GO_PILOTE_FERME_2026-04-26_v1.0.md)

Risques residuels retenus:

- chaine audio non encore consideree comme stabilisee;
- finition UX encore partielle;
- exploitation prod encore tres manuelle;
- nettoyage des traces de test prod encore a finir.

---

## 8) Chantiers critiques par domaine

## Backend

Priorite haute:

- dependances de roles plus fines;
- retrait de `admin_tech` des routes sensibles;
- distinction `operator` / `supervisor`;
- filtrage des listes;
- workflow de diffusion client minimal.

## Frontend

Priorite haute:

- clarifier `/operator`;
- rendre `/supervision` utile;
- verifier `/suivi` ou surface client equivalente;
- eviter les usages de test masques dans les parcours reels.

## IA / derive documentaire

Priorite moyenne-haute:

- conserver la generation actuelle qui fonctionne;
- durcir la validation;
- separer `analyse interne` et `document diffusable`;
- tracer clairement ce qui est montrable au client.

## Infra / exploitation

Priorite critique:

- assainir Docker/containerd/runc;
- fiabiliser la procedure de redeploiement;
- verifier l'etat paquets du VPS;
- produire une checklist standard.

## QA / recette

Priorite haute:

- scenario e2e reproductible;
- verification prod locale / VPS;
- verification de non-regression sur titres, ponctuation, routes publiques et auth.

---

## 9) Dependances critiques

1. Tant que le VPS n'est pas assaini, chaque redeploiement restera un risque disproportionne.
2. Tant que les roles ne sont pas resserres, il est premature d'ouvrir plus largement la surface produit.
3. Tant que `/operator` reste un melange de contextes, la recette produit restera confuse.
4. Tant que la diffusion client reste seulement `possible`, elle n'est pas encore `gouvernee`.

---

## 10) Principaux risques

## Risque 1 - Faux sentiment de finition

Le systeme donne deja l'impression de marcher, donc il serait facile d'ouvrir trop tot.

Risque reel:

- exposition de droits trop larges;
- confusion supervision / production;
- parcours client encore partiellement bricole.

## Risque 2 - Dette d'exploitation

Le runtime VPS a deja montre une fragilite concrete.

Risque reel:

- perte de temps en deploiement;
- indisponibilite au mauvais moment;
- incertitude sur l'etat reel des binaires Docker.

## Risque 3 - Melange dev / prod / test

Des surfaces actuelles servent a la fois au test, a l'admin et a l'usage metier.

Risque reel:

- erreurs d'usage;
- mauvaise lecture produit;
- contamination des droits.

---

## 11) Criteres de sortie pilote ferme

Le pilote ferme est considere pret si:

- le VPS redemarre proprement et de facon reproductible;
- un redeploiement backend standard est documente et verifie;
- le frontend public IVIA est deployee et accessible en TLS valide sur `ivia.quebec`;
- `operator`, `supervisor`, `admin_tech` ont des droits plus nets;
- le flux `client -> session -> note -> document derive -> lecture client` passe sans bricolage;
- la diffusion client publique exige `public_client_code + intake_request_id`;
- la supervision permet au moins une relecture et validation utile;
- la recette e2e est rejouable et a ete executee avec succes en production;
- le nettoyage des donnees de test est documente.

---

## 12) Ce qui restera probablement apres ce sprint

Meme avec un sprint bien execute, il restera probablement:

- une meilleure finition UX;
- une vraie surface `public_client` authentifiee plus complete;
- une couche praticien distincte;
- un workflow documentaire plus riche;
- un meilleur monitoring et une meilleure observabilite;
- une industrialisation de deploiement plus propre.

Cela est normal.

Le but du sprint n'est pas `plateforme finale`.

Le but est `pilote ferme propre`.

---

## 13) Decision operationnelle proposee

Decision:

`considerer MERLIN comme entre en sprint de durcissement produit / droits / exploitation, avec objectif prioritaire de pilote ferme en 5 a 10 jours ouvrables`

Corollaire:

- ne pas ouvrir de nouveaux chantiers conceptuels majeurs;
- traiter l'infra et les droits comme prioritaires au meme niveau que les fonctionnalites;
- utiliser le prochain cycle pour fermer l'existant plutot que multiplier les surfaces.

---

## 14) Synthese executive

Si l'on reste discipline:

- `deploiement technique`: deja la;
- `pilote ferme testable`: proche;
- `V1 propre et defendable`: encore un court sprint de durcissement;
- `plateforme mature`: pas encore.

Verdict:

`MERLIN a boucle la phase J1 a J10 de durcissement critique pour le pilote ferme: GO encadre pour un pilote reel, NO-GO pour une ouverture large tant que les risques residuels ne sont pas reduits`

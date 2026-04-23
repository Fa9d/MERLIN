# MERLIN - Choix stack technique V1

Date: 2026-04-21
Statut: decision de travail
Objet: figer une stack technique V1 coherente avec les specs donnees et ecrans, sans dupliquer inutilement les responsabilites entre frontend et backend

---

## 1) Constat de depart

Le depot ne contient pas encore d'application de production.
Il contient surtout:
- corpus de gouvernance;
- methodes;
- prototype site statique dans `07_EXPORTS/IVIA_SITE_PREVIEW`;
- un scaffold Next.js dans `09_app_ivia_merlin`.

L'ancien travail confirme une chose utile:

`le coeur metier et IA de MERLIN doit vivre dans un backend Python separe`

Donc la stack V1 ne doit pas reconstruire un faux backend complet dans Next.js.

---

## 2) Decision architecturale nette

### Architecture retenue

- `Frontend web`: `Next.js` + `TypeScript`
- `Backend coeur metier`: `FastAPI` + `Python`
- `Base de donnees`: `PostgreSQL`
- `ORM backend`: `SQLAlchemy`
- `Migrations backend`: `Alembic`
- `Stockage fichiers`: stockage objet compatible S3
- `Workers`: Python

### Architecture explicitement rejetee pour V1

- `Next.js` comme backend metier principal
- double logique de donnees `Prisma + SQLAlchemy` en parallele
- microservices multiples
- Kubernetes
- event sourcing lourd
- modele IA entraine maison des le depart

---

## 3) Pourquoi ce choix

### A. Pourquoi `Next.js` pour le frontend

Parce que:
- il permet de faire vite;
- il couvre bien le site public IVIA;
- il couvre les ecrans client / operateur / supervision;
- il donne un bon niveau de structure pour un petit produit founder-led.

Role retenu:
- rendu UI;
- formulaires;
- experience de navigation;
- appels API vers le backend MERLIN.

Role non retenu:
- coeur metier principal;
- pipeline IA;
- moteur de transcription;
- logique donnees source.

### B. Pourquoi `FastAPI` pour le backend coeur

Parce que:
- MERLIN aura un vrai pipeline de traitement;
- l'audio, la transcription, les derives et l'IA se branchent naturellement en Python;
- cela evite de recoder en TypeScript une couche qui devra de toute facon dialoguer avec des outils Python;
- cela garde une seule autorite metier et donnees cote backend.

### C. Pourquoi `PostgreSQL`

Parce que:
- les objets MERLIN sont relationnels;
- il faut audit, historique, statuts, versionnage et relations solides;
- il reste compatible avec JSON la ou c'est utile;
- il est sobre, robuste et standard.

### D. Pourquoi `SQLAlchemy + Alembic`

Parce que:
- si le coeur est en Python, l'ORM source de verite doit vivre en Python;
- on evite un doublon schema Prisma / schema Python;
- on garde migrations et modele de donnees dans la meme couche que le metier;
- c'est plus coherent qu'un front Next.js qui possede sa propre verite BDD.

Position nette:

`Prisma n'est pas retenu comme couche de verite V1`

Le scaffold Prisma existant peut servir de reference front temporaire, mais pas de base de verite donnees.

### E. Pourquoi un stockage objet S3-compatible

Parce que:
- l'audio et les documents derives ne doivent pas vivre dans le serveur applicatif;
- il faut distinguer base relationnelle et blobs;
- cela permet retention, archivage et evolution de couts.

---

## 4) Stack retenue V1

## A. Frontend

Choix retenu:
- `Next.js`
- `TypeScript`
- App Router
- CSS sobre, composants maison

Recommendation:
- ne pas surcharger avec un design system massif;
- conserver une UI maitrisee et lisible.

## B. Backend API

Choix retenu:
- `Python 3.11+`
- `FastAPI`
- `Pydantic`
- `SQLAlchemy`
- `Alembic`

Responsabilites:
- auth et roles;
- logique metier;
- CRUD coeur;
- journal d'audit;
- orchestration des derives;
- exposition des endpoints.

## C. Base de donnees

Choix retenu:
- `PostgreSQL`

## D. Authentification

Choix retenu:
- auth geree au niveau backend
- tokens/session selon implementation retenue

Roles minimum V1:
- `public_client`
- `operator`
- `supervisor`
- `admin_tech`

## E. Stockage fichiers

Choix retenu:
- `OVH Object Storage` ou equivalent S3-compatible

Classes de stockage a preparer:
- `hot`
- `cold`
- `offline_archive`

## F. Jobs asynchrones

Choix retenu:
- workers Python
- queue simple sobre

Options acceptables V1:
- table de jobs en base + worker;
- ou Redis si necessaire.

Jobs cibles:
- `transcribe_audio_job`
- `generate_entry_summary_job`
- `generate_session_summary_job`
- `archive_audio_job`
- `send_email_job`

## G-bis. Audio temps reel

Decision complementaire:
- l'audio de seance cible vit dans l'application;
- cette meme logique vaut pour les operateurs MERLIN et pour les praticiens;
- les outils externes d'appel ne sont pas la ligne produit principale.

Stack cible pour cette couche:
- WebRTC dans l'app;
- couche media `LiveKit` ou equivalent;
- enregistrement cote serveur;
- stockage objet rattache a `session_id`.

Position nette:

`MERLIN ne doit pas dependre structurellement d'un appel telephonique externe pour exister`

## G. IA / LLM

Choix retenu V1:
- API LLM externe pour synthese, extraction, comparaison et documents derives

Regles:
- pas de modele entraine maison en V1;
- prompts versionnes;
- journalisation des sorties critiques;
- validation humaine sur les points sensibles.

## H. Transcription

Choix retenu V1:
- batch asynchrone economique

Recommendation:
- `AssemblyAI batch` en premier choix cout/rapidite
- `Deepgram` si besoin qualite specifique

## I. E-mails

Choix retenu:
- `Resend` ou SMTP/API simple

Usages V1:
- confirmation entree;
- confirmation rdv;
- transmission documentee;
- alertes internes.

## J. Paiement

Choix retenu:
- `Stripe`

Position:
- billing simple d'abord;
- pas de `Stripe Connect` complexe en V1 tant que le besoin exact n'est pas stabilise.

## K. Hebergement

Frontend:
- `Vercel` acceptable pour aller vite
- ou VPS si besoin de controle/cout

Backend:
- VPS OVH ou equivalent simple

Base:
- PostgreSQL gere separement ou heberge sobrement

Position nette:
- ne pas empiler frontend, backend metier, audio et stockage sur un seul service opaque.

## L. Monitoring

Choix retenu:
- logs applicatifs
- error tracking type `Sentry`
- uptime checks simples

## M. Secrets / configuration

Choix retenu:
- variables d'environnement separees dev/test/staging/prod
- rotation manuelle rigoureuse au depart
- aucune vraie donnee sensible dans un environnement dev librement partage

---

## 5) Architecture logique minimale

## Frontend Next.js

Contient:
- pages publiques IVIA
- parcours client
- espace operateur
- supervision

Ne contient pas:
- logique metier source
- orchestration IA source
- ecriture directe metier en base hors cas exceptionnel strictement maitrise

## Backend FastAPI

Contient:
- endpoints metier
- auth
- controles de roles
- logique de consentement
- logique de seance
- logique des derives
- journal d'audit
- orchestration des jobs

## Services relies

- Postgres
- stockage objet
- provider transcription
- provider LLM
- email
- paiement

---

## 6) Consequence sur le scaffold actuel

Le projet `09_app_ivia_merlin` reste utile.

Mais son role change:
- il devient le frontend principal pressenti;
- il ne doit pas devenir la source de verite metier;
- sa couche Prisma actuelle est transitoire et non directrice.

Decision pratique:
- on peut conserver temporairement ce scaffold pour l'UI;
- on preparera un backend Python neuf dans `C:\MERLIN`;
- on n'investit pas plus dans Prisma tant que le backend MERLIN n'est pas pose.

---

## 7) Decision active

MERLIN adopte la stack suivante pour V1:

- `Next.js + TypeScript` pour le frontend
- `FastAPI + Python` pour le backend coeur
- `PostgreSQL` pour la base
- `SQLAlchemy + Alembic` pour la couche donnees backend
- stockage objet S3-compatible pour audio et derives
- workers Python pour transcription et generation

References:
- [MERLIN_GOUV_AUDIT_OLD_REPERTOIRES_REUTILISABLES_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_AUDIT_OLD_REPERTOIRES_REUTILISABLES_V1.md)
- [MERLIN_GOUV_ARBITRAGE_REFAIRE_ARCHIVER_REPRENDRE_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_ARBITRAGE_REFAIRE_ARCHIVER_REPRENDRE_V1.md)
- [MERLIN_GOUV_DECISION_AUDIO_DANS_APP_OPERATEURS_PRATICIENS_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_DECISION_AUDIO_DANS_APP_OPERATEURS_PRATICIENS_V1.md)

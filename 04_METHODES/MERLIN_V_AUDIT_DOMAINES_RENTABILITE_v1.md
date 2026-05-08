# MERLIN V — Audit des domaines de compétences & plan de rentabilité

**Audit stratégique · Mai 2026 · v1.0**

- **Auteur** : David Phaneuf
- **Périmètre** : MERLIN · IVIA · MÉSANGE
- **Source** : github.com/Fa9d/MERLIN — branche master
- **Référence backlog** : MERLIN_GOUV_BACKLOG_MAITRE_V2 (65 tâches)
- **Cible** : MVP rentable avant juin 2026

---

## 1. Synthèse exécutive

MERLIN est en phase finale technique — backend FastAPI déployé sur OVH, frontend Next.js en production sur ivia.quebec, 17 migrations Alembic appliquées, 21 modules backend opérationnels. Le projet est passé de l'expérimentation à la structuration commerciale. Sur 65 tâches du backlog maître V2, 8 sont closes et 56 restent à exécuter pour atteindre le MVP rentable.

**Trois constats dictent la suite :**

- Le code existe mais le matching, l'onboarding praticien et le paiement ne sont pas encore reliés bout-en-bout.
- Le modèle économique est cadré (3 offres client + 3 niveaux praticien) mais aucun praticien pilote ni client payant n'est encore activé.
- La gouvernance est mature (4 ADR, registre décisions, journal d'exécution) — l'effort manquant est l'exécution coordonnée, pas la planification.

Cet audit couvre 10 domaines de compétences, identifie les blocages réels par domaine, et répartit les 56 tâches restantes entre 4 exécutants : **David** (décisions, contenu, recrutement praticien), **Claude Code** (backend, migrations, tests), **Copilot** (frontend, intégration UI), **Perplexity** (recherche, juridique, marketing).

### État global du backlog par domaine

| Domaine | Total | Done | Active | Todo | % complété |
|---|---|---|---|---|---|
| infra / exploitation | 8 | 0 | 0 | 8 | 0 % |
| backend FastAPI | 10 | 5 | 0 | 5 | 50 % |
| frontend Next.js | 6 | 1 | 0 | 5 | 17 % |
| contenu éditorial | 5 | 1 | 0 | 4 | 20 % |
| diffusion / marketing | 3 | 0 | 0 | 3 | 0 % |
| gouvernance | 6 | 0 | 1 | 5 | 0 % |
| qualité IA | 7 | 1 | 0 | 6 | 14 % |
| rôles & accès | 10 | 0 | 0 | 10 | 0 % |
| MÉSANGE (B2B) | 8 | 0 | 0 | 8 | 0 % |
| fondements / méthodes | 2 | 0 | 0 | 2 | 0 % |
| **TOTAL** | **65** | **8** | **1** | **56** | **12 %** |

*Source : MERLIN_GOUV_BACKLOG_MAITRE_V2 — 2026-05-06.*

---

## 2. Architecture & état technique réel

### Stack en production

| Couche | Technologie | État | Localisation |
|---|---|---|---|
| Backend | Python · FastAPI · SQLAlchemy | Live | `10_backend_merlin_api/` |
| Base de données | PostgreSQL 15 + Alembic 0017 | Migrée | VPS OVH 137.74.42.121 |
| IA | Claude (Anthropic) — haiku/sonnet | Connecté | `11_PROMPTS/` chargés dynamiquement |
| Frontend | Next.js 16.2.4 + Turbopack + Prisma | Live | `09_app_ivia_merlin/` |
| Audio temps réel | LiveKit v1.8.3 | Intégré | Routes `audio_sessions` |
| Transcription | AssemblyAI + Deepgram (fallback) | Câblé | `services/livekit_audio.py` |
| Paiement | Stripe Canada (clé en prod) | Câblé | `routes/payments.py` |
| Reverse proxy | Nginx 1.27 + Certbot Let's Encrypt | TLS actif | ivia.quebec · api.ivia.quebec |
| Orchestration | Docker Compose + Makefile | Stable | `docker-compose.prod.yml` |

### Modules backend déjà implémentés (21 routes)

`auth` · `register` · `verify_email` · `clients` · `praticiens` · `intake_requests` · `sessions` · `session_notes` · `schedules` · `bookings` · `matching` · `payments` (Stripe checkout audio-async) · `audio_sessions` (LiveKit) · `audio_recordings` · `consents` · `derived_documents` · `health`

### Modèles de données (12)

`AppUser` · `Client` · `IntakeRequest` · `Session` · `SessionNote` · `AudioSession` · `AudioRecording` · `Schedule` · `Consent` · `DerivedDocument` · `PractitionerProfile` · `enums` (rôles, statuts).

### Surfaces frontend Next.js (18 routes)

`/admin` · `/audio-room` · `/audio-test` · `/checkout` (success / cancel) · `/espace-praticien` · `/operator` · `/praticien` · `/praticiens` · `/rendez-vous` (reserver / confirmation) · `/ressources` · `/suivi` · `/supervision` · `/verify-email`.

> **Constat critique** : la chaîne formulaire client › matching › suggestion praticien › réservation › paiement › séance audio › note IA › rapport existe par morceaux mais n'a jamais été testée bout-en-bout en production avec un utilisateur réel.

---

## 3. Audit par domaine de compétence

Chaque domaine est évalué sur trois axes : **maturité actuelle**, **blocage principal**, **livrable critique** qui débloque la rentabilité.

### 3.1 — Backend / API

- **Maturité.** Mature à 50 %. 5 quick-wins commités (SlotStatus, CORS, 410 Gone, email vérifié, RequestChannelCode). Routes matching et payments existent mais pas auditées.
- **Blocage.** Audit endpoints audio-sessions + intake-requests + cohérence Alembic.
- **Livrable critique.** BACK-006, BACK-007, BACK-008, BACK-009, BACK-010 — 5 tâches.
- **Owner recommandé.** Claude Code

### 3.2 — Frontend / UX

- **Maturité.** Mature à 17 %. ClientPayload typé, parcours réservation hold › confirm câblé. Le formulaire de besoin client (5-7 questions) et la fiche praticien post-matching ne sont pas encore en React.
- **Blocage.** Pas de moteur de matching côté UI : formulaire absent, fiche unique absente, swap absent.
- **Livrable critique.** MATCH-002, MATCH-005, MATCH-006, FRONT-002 à FRONT-006 — 8 tâches.
- **Owner recommandé.** Copilot

### 3.3 — Infrastructure / DevOps

- **Maturité.** Mature à 0 % sur le déploiement live mais scripts en place. Makefile, prod-up.sh, docker-compose.prod.yml, Certbot, Nginx — tout est prêt à exécuter.
- **Blocage.** Migration 0017 doit être appliquée sur le VPS, smoke tests post-déploiement non joués.
- **Livrable critique.** INFRA-001 à INFRA-008 — 8 tâches dont 4 P1.
- **Owner recommandé.** David (action VPS) + Claude Code (smoke tests)

### 3.4 — Qualité IA / Prompts

- **Maturité.** Mature à 14 %. Bibliothèque `11_PROMPTS` structurée (METH, PROD-VALID, sessions, supervision, admin, pilote). Contrat prompt V1 commité.
- **Blocage.** Grille qualité note + grille GO/NO-GO + frontmatter `test_associe` + replay tests IA = absents.
- **Livrable critique.** QIA-002 à QIA-007, MES-008 — 7 tâches.
- **Owner recommandé.** Claude Code + David (validation)

### 3.5 — Rôles & sécurité

- **Maturité.** Mature à 0 %. Rôles définis (public/client/praticien/opérateur/superviseur/admin) mais aucune matrice d'accès formelle, aucun guard backend systématique, aucun test e2e par rôle.
- **Blocage.** Risque sécurité : élévation de privilège possible tant que ROLES-010 n'est pas audité.
- **Livrable critique.** ROLES-001 à ROLES-010 — 10 tâches.
- **Owner recommandé.** Claude Code (back) + Copilot (front)

### 3.6 — Gouvernance / décisions

- **Maturité.** Mature à 0 % cette semaine, mais corpus très solide : 4 ADR, registre décisions DEC-041, journal d'exécution, convention de nommage V2.
- **Blocage.** Système de gestion opérationnel V1 (5 fichiers) en cours de commit. 24 fichiers périmés à archiver.
- **Livrable critique.** GOUV-001 à GOUV-006 — 6 tâches.
- **Owner recommandé.** David

### 3.7 — Contenu / éditorial

- **Maturité.** Mature à 20 %. 16 articles IVIA pushés sur GitHub (`04_METHODES/articles/`). Plan éditorial 16 semaines validé.
- **Blocage.** Aucune route `/ressources` ni système MDX dans Next.js — les articles existent mais ne sont pas publics.
- **Livrable critique.** CONT-002 à CONT-005 — 4 tâches.
- **Owner recommandé.** Copilot (intégration MDX) + David (relectures)

### 3.8 — Diffusion / marketing

- **Maturité.** Mature à 0 %. Calendrier éditorial 30 jours rédigé, identité graphique validée (logo Mésange), positionnement IVIA documenté.
- **Blocage.** Aucun canal de diffusion ouvert (newsletter, réseau social, capsules audio). Mentions légales absentes du site live.
- **Livrable critique.** DIFF-001, DIFF-002, DIFF-003 — 3 tâches.
- **Owner recommandé.** David + Perplexity (recherche audience cible)

### 3.9 — MÉSANGE / B2B praticien

- **Maturité.** Mature à 0 %. Onboarding self-service, tableau de bord praticien, notes IA assistées, facturation Stripe : tout reste à coder.
- **Blocage.** Aucun praticien pilote recruté. Sans pilote, le module note IA ne peut pas être validé en conditions réelles.
- **Livrable critique.** MES-001 à MES-008 — 8 tâches.
- **Owner recommandé.** David (recrutement) + Claude Code (back) + Copilot (front)

### 3.10 — Juridique / financement

- **Maturité.** Mature à 50 %. Phase 1 cadrée (travailleur autonome + REQ), Phase 2 OBNL et Phase 3 INC documentées. Sources financement (Futurpreneur, MITACS, Investissement Québec, La Ruche) listées.
- **Blocage.** Aucune action concrète : pas d'immatriculation REQ, pas de constitution OBNL, pas de demande déposée.
- **Livrable critique.** Hors backlog technique — actions David urgentes.
- **Owner recommandé.** David + Perplexity (recherche subventions)

---

## 4. Répartition des 56 tâches restantes

La logique de répartition repose sur quatre exécutants complémentaires. **David** garde la décision et les actions humaines (VPS, recrutement, juridique). **Claude Code** traite tout ce qui touche au backend, aux migrations et aux tests automatisés. **Copilot** agit dans le frontend Next.js et l'intégration UI. **Perplexity** (cet agent) fournit recherche, contenu et synthèse.

### Vue synthétique par exécutant

| Exécutant | Domaines couverts | Nb tâches | Charge estimée |
|---|---|---|---|
| David Phaneuf | Décisions VPS · Gouvernance · Juridique · Recrutement praticien · Validation contenu | ≈ 18 | 30 h sur 4 sem. |
| Claude Code | Backend FastAPI · Migrations Alembic · Tests pytest · Qualité IA · Rôles backend · Module notes IA | ≈ 22 | 45 h sur 4 sem. |
| GitHub Copilot | Frontend Next.js · Composants React · MDX articles · Visibilité par rôle · Onboarding praticien | ≈ 14 | 30 h sur 4 sem. |
| Perplexity (cet agent) | Recherche subventions · Études marché · Mentions légales · Calendrier diffusion · Veille concurrence | ≈ 8 | À la demande |

### Plan détaillé — sprint Vague 6 (semaine du 7 au 14 mai 2026)

| ID | Livrable | Owner | Prio | Effort |
|---|---|---|---|---|
| INFRA-001 › 004 | scp + make migrate + make up + smoke tests | David | P1 | 2 h |
| MATCH-001 | Modèle PractitionerProfile DB + schéma Pydantic | Claude Code | P1 | 3 h |
| MATCH-002 | Formulaire de besoin client (5-7 champs) | Copilot | P1 | 4 h |
| MATCH-003 | Algo de matching (score simple Python) | Claude Code | P1 | 3 h |
| MATCH-004 | Endpoint POST /matching/suggest | Claude Code | P1 | 2 h |
| MATCH-005 | Fiche praticien unique — composant React | Copilot | P1 | 3 h |
| GOUV-003 | Sprint A archivage (24 fichiers › ARCHIVES/) | David | P2 | 15 min |
| QIA-002 | MERLIN_GRILLE_QUALITE_NOTE_V1.md | Claude Code + David | P1 | 2 h |
| QIA-003 | MERLIN_GRILLE_GONOGO_PROMPT_V1.md | Claude Code + David | P1 | 1 h |
| DIFF-003 | Mentions légales + politique confidentialité | Perplexity › David | P2 | 2 h |

**Charge totale Vague 6 : ~22 h de dev + 2 h actions VPS + 4 h gouvernance/contenu = 28 h.**

---

## 5. Plan de rentabilité — du MVP au premier dollar

MERLIN combine deux flux de revenus distincts qui doivent être activés dans cet ordre : (1) abonnement praticien MÉSANGE dès Vague 7, puis (2) paiement client à la séance via Stripe dès Vague 8. **La règle économique non-négociable : aucune commission cachée sur l'orientation de soin.**

### Modèle tarifaire actif (V1, 2026-04-27)

| Offre client | Format | Prix | Marge cible |
|---|---|---|---|
| LIBRE — écoute sans rapport | Gratuit · acquisition | 0 $ | — |
| ACCOMPAGNÉ — écoute avec rapport | 9-19 $/mois ou 5-12 $/séance | 9 $/mois entrée | 60-70 % |

| Offre praticien | Format | Prix | Marge brute/séance |
|---|---|---|---|
| PRÉSENCE — profil public seul | Gratuit ou 19 $/mois | 19 $/mois | n/a |
| PRATIQUE — notes IA + agenda | 49 $/mois (3 niveaux : 27,99 / 47,99 / 84,99) | 49 $/mois | 4,13 $ (profil A) |
| RÉSEAU — réservation en ligne | 89 $/mois ou % séances | 89 $/mois | Variable |

### Coûts variables réels par séance (audit fournisseurs vérifiés)

| Poste | Fournisseur | Coût | % du total |
|---|---|---|---|
| Paiement | Stripe Canada | 2,91 $ (2,9 % + 0,30 $) | 82 % |
| Transcription | AssemblyAI batch | 0,24 $ / séance 70 min | 7 % |
| IA analyse | GPT-4.1-mini · Claude Haiku | 0,01 $ | <1 % |
| Stockage audio | OVH Object Storage | 0,01 $/Go/mois | <1 % |
| Infra applicative | OVH VPS-1 + VPS-2 | ≈ 16 EUR/mois (fixe) | amorti |
| **TOTAL VARIABLE** | — | **3,17 $/séance** | 100 % |

> **Plancher absolu** : 4,17 CAD/séance (scénario AssemblyAI) ou 4,56 CAD (scénario prudent Deepgram). Le tarif gros volume de 4,90 $ reste au-dessus du plancher.

### Simulation 3 profils praticiens — marge mensuelle MERLIN

| Profil | Séances / mois | Revenu MERLIN | Coûts variables | Marge brute | Marge / séance |
|---|---|---|---|---|---|
| A — Petit | 20 | 145,99 $ | −63,40 $ | 82,59 $ | 4,13 $ |
| B — Établi | 60 | 371,99 $ | −190,20 $ | 181,79 $ | 3,03 $ |
| C — Gros volume | 150 | 819,99 $ | −453,00 $ | 366,99 $ | 2,45 $ |

### Trajectoire vers la rentabilité

| Étape | Délai | Cible | Revenu mensuel attendu |
|---|---|---|---|
| Pilote ferme — 1 praticien test | Mai 2026 | MES-007 validé | 0 $ (gratuit) |
| 3 praticiens payants PRATIQUE | Juin 2026 | Onboarding self-service live | ≈ 150 $ |
| 10 praticiens · mix 3 niveaux | Août 2026 | MÉSANGE en production | ≈ 600 $ |
| 20 praticiens + 50 séances client/mois | Octobre 2026 | Stripe client actif | ≈ 1 800 $ |
| Seuil de rentabilité opérationnelle | Décembre 2026 | Couvre infra + temps fondateur | ≥ 3 500 $ |

**Conditions de réussite :** (1) 1 praticien pilote payant avant fin mai ; (2) onboarding self-service MES-003 fonctionnel en juin ; (3) Stripe checkout client validé en juillet ; (4) immatriculation REQ + ouverture compte bancaire dédié dès cette semaine.

---

## 6. Trajectoire de financement

Le financement suit la structure juridique en trois phases. Les revenus opérationnels couvrent les coûts variables ; le financement externe couvre le temps fondateur, la R&D qualité IA, et l'infrastructure pendant 12-18 mois.

| Phase | Statut juridique | Sources visées | Montant cible |
|---|---|---|---|
| Phase 1 — Maintenant | Travailleur autonome + REQ | Contrats pilotes cliniques · Futurpreneur Canada · SACA | 5 000 - 15 000 $ |
| Phase 2 — 3-6 mois | OBNL (Loi compagnies QC partie III) | Québec Numérique · MITACS Accélération · La Ruche · CNRC-PARI | 30 000 - 80 000 $ |
| Phase 3 — 12-24 mois | MERLIN INC + OBNL coexistantes | Investissement Québec · BDC · Anges Québec · revenus SaaS | 150 000 - 500 000 $ |

### Actions juridiques urgentes (David, cette semaine)

- S'immatriculer au Registre des entreprises du Québec (REQ) — coût ≈ 50 $ — délai 24 h en ligne.
- Ouvrir un compte bancaire professionnel dédié (Desjardins ou banque équivalente).
- Préparer le dossier OBNL (mission rédigée, 3 administrateurs identifiés) pour dépôt sous 60 jours.
- Activer le numéro de TPS/TVQ dès le franchissement du seuil 30 000 $ (anticiper).
- Identifier 1 cabinet juridique spécialisé OBNL/santé pour consultation de 1 h.

---

## 7. Risques & arbitrages clés

| Risque | Impact | Mitigation immédiate | Owner |
|---|---|---|---|
| Aucun praticien pilote recruté avant juin | Bloque MES-007, retarde rentabilité de 3 mois | Lancer recrutement via réseau personnel cette semaine, prévoir compensation gratuite 3 mois | David |
| Migration 0017 non appliquée VPS | Frontend en désync avec backend, erreurs prod | Exécuter `make migrate + make up` sous 48 h (INFRA-001 › 004) | David |
| Conformité Loi 25 (données santé QC) | Risque légal majeur, blocage commercial | Mentions légales + politique confidentialité publiées avant 1er client réel | Perplexity › David |
| Sécurité rôles (élévation privilège) | Fuite données clinique, perte de confiance | ROLES-010 audit avant ouverture publique | Claude Code |
| Coût Stripe domine la marge (82 %) | Profil C marge/séance < 2,50 $ — érosion rentabilité | Étudier paiement direct praticien-client (MERLIN ne collecte pas) en option PRO | David + Perplexity |
| Dépendance API Anthropic (prix, dispo) | Si tarifs Claude doublent, marge IA s'effondre | Garder fallback GPT-4.1-mini opérationnel, monitorer coûts mensuels | Claude Code |
| Surcharge fondateur (1 personne, 56 tâches) | Burnout, qualité dégradée, retards | Discipliner répartition Claude/Copilot/Perplexity, refuser tâches hors backlog V2 | David |

### Arbitrages tranchés ce printemps (mémo Plan directeur Vague 6)

- **REJETÉ** : annuaire public de praticiens. **RETENU** : suggestion unique post-formulaire (UX sans friction).
- **REJETÉ** : notes cliniques IA comme output principal. **RETENU** : notes = outil praticien privé, jamais visibles client par défaut.
- **REJETÉ** : grille qualité note comme merge gate. **RETENU** : grille qualité = outil d'évaluation interne praticien.
- **RETENU** : 2 offres client seulement (libre / accompagné) — simplicité, conversion.
- **RETENU** : 3 niveaux praticien (présence / pratique / réseau) — progression naturelle.
- **RETENU** : moteur de matching côté MERLIN, pas choix du client — UX guidée.

---

## 8. Prochaines 72 heures — actions concrètes

Pour transformer cet audit en mouvement, voici les actions à exécuter dans les 72 heures suivant ce document. Chaque action est attribuée, datée et a un critère de complétion explicite.

| # | Action | Owner | Critère de complétion |
|---|---|---|---|
| 1 | scp 8 fichiers + `make migrate` + `make up` sur VPS | David | `alembic_version = 20260504_0017` + `/api/health = 200` |
| 2 | Smoke test e2e prod (login, intake-request, hold/confirm slot) | David + Claude Code | 3 routes critiques répondent < 500 ms |
| 3 | Démarrer MATCH-001 — modèle PractitionerProfile + schéma | Claude Code | Migration 0018 prête + tests unitaires verts |
| 4 | Démarrer MATCH-002 — formulaire de besoin client React | Copilot | Page `/demarche` déployée en local, 5-7 champs validés |
| 5 | Immatriculation REQ (en ligne, ≈ 30 minutes) | David | Numéro NEQ obtenu |
| 6 | Identifier 3 praticiens cibles pour pilote MES-007 | David | 3 noms + 3 emails dans CRM/notes |
| 7 | Rédiger mentions légales + politique confidentialité v0.1 | Perplexity › David | 2 fichiers MD dans `12_JURIDIQUE_AFFAIRES/` |
| 8 | Archiver 24 fichiers périmés (GOUV-003) | David | Dossier `ARCHIVES/` peuplé + commit |

**Principe directeur de la suite** — David tient le rythme et la décision. Claude Code et Copilot exécutent en parallèle sur backend et frontend. Perplexity prépare contenu, recherches et synthèses. Le backlog maître V2 reste la source unique de vérité du *quoi* et du *quand*. Toute tâche qui n'est pas dans le backlog ne se fait pas cette semaine.

> **Cible : premier praticien pilote actif au 31 mai 2026. Première facturation MÉSANGE en juin. Première séance client payée en juillet. Seuil de rentabilité opérationnelle visé pour décembre 2026.**

---

*Document interne · David Phaneuf · Mai 2026 · v1.0 · Fa9d/MERLIN*

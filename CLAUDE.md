# CLAUDE.md — Contexte MERLIN pour Claude Code

> Ce fichier est lu automatiquement par Claude Code à chaque session.
> Il contient tout ce qu'il faut savoir pour travailler efficacement sur ce repo.
>
> **Mise à jour 2026-05-15** — Ajout de la trinité MÉSANGES · MERLIN · IVIA, glossaire,
> section Agents & IA Anthropic, politique laboratoire Ruvnet, évaluations & traçabilité,
> règle de journalisation, règle de maintenance documentaire.
> **Branche active courante** : `refonte-ivia-site-unifie` (refonte stratégique « maison du vivant »).
> La branche `master` reste la branche d'intégration ; `main` héberge un autre lignage technique — ne pas confondre.

---

## 0. Trinité fondatrice — MÉSANGES · MERLIN · IVIA

**Phrase directrice** :
> **IVIA accueille. MERLIN structure. MÉSANGES accompagne.**

| Composante | Rôle | Posture |
|------------|------|---------|
| **IVIA** | Maison commune, seuil public (`ivia.quebec`) — *In Vivo, In Actu — Au sein de l'être, en actes*. Le champ commun où la personne arrive, est reçue, s'oriente. | Accueillir sans trier, sans diagnostiquer. |
| **MERLIN** | Cœur d'analyse et de gouvernance : classification multidimensionnelle, temporalité, connecteurs privés/internes, lecture client / lecture praticien. | Structurer, classer, interpréter, tracer, garder la mémoire. |
| **MÉSANGES** | Voix subtiles d'accompagnement à travers les sujets qui nous touchent. Petite présence orientante, en résonance, en écho discret. | Accompagner sans prescrire — orienter par la voix, la résonance, l'accompagnement inconscient. |

> Note symbolique (interne, doctrine) : MÉSANGES porte discrètement *nos anges* — voix tutélaires, accompagnement inconscient. À ne pas exploiter comme slogan marketing ; à honorer comme posture intérieure.

### Glossaire opérationnel

- **IVIA** — *In Vivo, In Actu*. **Maison du vivant** : portail commun, expérience publique, lieu où la personne arrive, s'oriente, revient.
- **Maison du vivant** — métaphore directrice de l'expérience IVIA : un lieu habité, pas un service marchand ni une marketplace.
- **Correspondances vivantes** — table de traduction entre les **expressions ordinaires** des personnes (français/québécois courant) et les **axes multidimensionnels MERLIN**. Ordre canonique des axes (territoire en premier, comme sol vivant qui précède et conditionne tout le reste) : **territoire**, corps, métabolisme, émotions, mental, relations, famille, transgénérationnel, société, spirituel/existentiel, urgence/référence. Voir `00_DOCTRINE/correspondances-vivantes.md`.
- **Observation / Hypothèse / Orientation** — triade obligatoire de toute sortie IA orientée client. **Jamais** « diagnostic / pronostic / prescription ». On *observe* ce qui est dit, on *formule des hypothèses* prudentes, on *oriente* vers une ressource humaine compétente.
- **Posture non-médicale** — IVIA / MERLIN **ne posent pas de diagnostic, ne prescrivent pas, ne décident pas cliniquement, ne se substituent pas aux services d'urgence, ne promettent aucune guérison.** Le système peut **éduquer, orienter, structurer, soutenir l'autonomie**.
- **Quatre voies d'accompagnement IVIA** — les chemins publics offerts par la maison du vivant (à expliciter côté frontend) : accueil/écoute, lecture multidimensionnelle, mise en lien avec praticiens, suivi/équilibre dans la durée.
- **Connecteurs privés** — toute intégration externe (paiement, courriel, calendrier, IA) doit être **interne ou contractuellement encadrée**, hébergée Québec/Canada quand possible, et minimiser l'exposition de données personnelles.

---

## 1. Architecture globale

MERLIN n'est pas seulement une app clinique — c'est un **repo-système canonique**.

```
IVIA      →  accueille (maison commune, seuil public, champ partagé)
MERLIN    →  structure, classe, interprète, trace, décide
MÉSANGES  →  accompagne (voix subtiles, orientation, résonance, accompagnement inconscient)
Modules   →  exécutent des fonctions assistées sous validation humaine
```

**MERLIN** est la source unique de vérité : gouvernance, méthodes, prompts, preuves, décisions stratégiques, composants applicatifs. Tout ce qui est produit (code, interfaces, documents) en dérive.

**IVIA** (`ivia.quebec`) est la couche d'exposition publique : parcours clients, frontend Next.js, articles, expérience utilisateur.

**Le sous-système clinique assisté par IA** est un cas d'usage majeur de MERLIN, pas sa définition totale.

- Fondateur : David Phaneuf (Montréal, Québec)
- Domaine : santé mentale, première ligne, contexte québécois/canadien
- Phase actuelle : stack prod déployée — backend API live, frontend live, migrations appliquées
- **Données** : hébergement Québec, posture *data Quebec privacy* (Loi 25, LPRPDE). Aucune sortie vers un service tiers sans validation explicite.

---

## 2. Stack technique — état réel (prod)

```
Backend   : Python / FastAPI / SQLAlchemy / Alembic
DB        : PostgreSQL 15 (migrations via Alembic — HEAD = 20260504_0017)
IA        : API Anthropic (Claude) — haiku ou sonnet selon la tâche
Frontend  : SITE PUBLIC = statique ivia_site_v2/ (HTML + Tailwind CDN), servi par nginx
            (nginx/default.conf → root /opt/merlin/ivia_site_v2). C'est la version LIVE.
            Next.js 16.2.4 (09_app_ivia_merlin/) = LEGACY **ARCHIVÉ** (ADR-0006) — gelé,
            conservé pour référence, NON servi, NON développé. Ne rien y ajouter.
Media     : LiveKit v1.8.3 (sessions audio/vidéo)
Infra     : Docker Compose — OVH VPS ubuntu@137.74.42.121:/opt/merlin
Reverse   : Nginx 1.27 (TLS Let's Encrypt)
Versioning: Git / GitHub — branche d'intégration master ; branche refonte courante refonte-ivia-site-unifie
```

**STACK CANONIQUE (ADR-0006, actée 2026-06-26) :** backend **Python/FastAPI** + frontend
**statique `ivia_site_v2/`**. Le pipeline IA reste **en Python** (faster-whisper local =
données Québec/Loi 25). **Aucune migration Node.js/Prisma/Next.js.** Le Next.js est archivé.

**URLs prod :**
- Frontend : `https://ivia.quebec`
- API : `https://api.ivia.quebec/api/health`

**RÈGLE CRITIQUE :** Ne jamais appeler `docker compose` sans `--env-file .env.prod`.
Utiliser `make <cible>` ou `bash deploy/prod-up.sh` — voir `docs/ops-docker-compose.md`.

**RÈGLE ARCHITECTURE DATA — frontend (09_app_ivia_merlin) :**
- Le frontend ne doit **jamais** lire ou écrire en DB directement via Prisma Client depuis les composants ou pages.
- `src/lib/db.ts` (PrismaClient) est **réservé aux Route Handlers Next.js** (`app/api/**`) uniquement, en attendant leur suppression progressive.
- Toute lecture/écriture de données métier passe par `src/lib/merlin-api.ts` → Backend FastAPI.
- Aucune PR ne sera acceptée si elle importe `db` depuis `src/lib/db.ts` dans un composant, une page, ou une action serveur non-API.
- Objectif cible : supprimer `src/lib/db.ts` et Prisma du frontend une fois tous les Route Handlers migrés en appels API.

---

## 3. Structure du repo

```
MERLIN/
├── 00_DOCTRINE/             # Doctrine vivante (carte abstraite, correspondances vivantes, veille)
├── 00_GOUVERNANCE/          # Gouvernance, décisions, backlog, journal
├── 01_FONDATEUR/            # Fondements et visées
├── 01_FONDEMENTS/           # Documents fondateurs IVIA (charte, cercle, positionnement)
├── 02_NATIONS_QC/           # Cadre des 11 Nations du Québec
├── 03_DESIGN/               # Design system, identité visuelle MÉSANGES
├── 03_MODELE_GOUVERNANCE/   # Modèle opératoire
├── 04_METHODES/             # Méthodes, cas simulés, articles
├── 05_JOURNAUX/             # Journaux d'opération et de handoff (chronologique)
├── 05_PREUVES_SOURCES/      # Audits, preuves, base de connaissance
├── 09_app_ivia_merlin/      # Frontend Next.js (IVIA)
├── 10_backend_merlin_api/   # Backend FastAPI (MERLIN API)
├── 11_PROMPTS/              # Bibliothèque de prompts système (markdown)
├── 12_JURIDIQUE_AFFAIRES/   # Documents stratégiques et juridiques
├── DAVID_CORPUS/            # Corpus personnel du fondateur
├── deploy/                  # Scripts de déploiement (prod-up.sh)
├── docs/                    # Documentation d'exploitation et notes labo
│   └── labs/                # Notes laboratoire (ruvnet, expérimentations)
├── managed_agents/          # Registre d'agents IA, evals, fixtures
├── nginx/                   # Config Nginx + Certbot
├── docker-compose.prod.yml  # Stack Docker prod
├── Makefile                 # Commandes officielles prod
└── CLAUDE.md                # Ce fichier
```

---

## 4. Conventions de code

- **Langue** : commentaires et docstrings en français, code en anglais
- **Commits** : format `feat|fix|docs|refactor|test(scope): message court`
- **Branches** :
  - `master` — branche d'intégration, commits directs acceptés en phase solo
  - `refonte-ivia-site-unifie` — branche courante de la refonte « maison du vivant »
  - Toute nouvelle branche doit être nommée et justifiée explicitement
- **Variables d'environnement** : toujours dans `.env` (jamais en dur dans le code)
- **Prompts IA** : toujours chargés depuis `11_PROMPTS/` — jamais hardcodés

---

## 5. Conventions des prompts (11_PROMPTS/)

Chaque prompt `.md` respecte la structure suivante :

```
# PROMPT — [Titre]
**Version**: vX.X — YYYY-MM-DD
**Surface**: [qui peut l'utiliser]
**Déclencheur**: [quand il s'active]
---
## Contexte
## Rôle
## Entrée attendue
## Tâche
## Format de sortie
## Règles absolues   ← OBLIGATOIRE sur tous les prompts
## Complémentaire à
```

**Règle** : tout prompt modifié doit bumper sa version (v1.0 → v1.1).

Tout prompt qui produit une sortie destinée au client doit inclure, dans ses **Règles absolues** :
- triade **Observation / Hypothèse / Orientation** au lieu de diagnostic/prescription ;
- escalade explicite si un signal d'urgence (suicidaire, violence, mineur en danger) est détecté ;
- limitation aux **formulations autorisées** définies dans `00_DOCTRINE/correspondances-vivantes.md`.

---

## 6. Agents & IA Anthropic

MERLIN est conçu pour collaborer avec **Claude Code** (CLI/IDE) et l'**Anthropic Agent SDK** (managed_agents, skills, evals).

### 6.1 Skills

- Les skills disponibles côté CLI sont listés en début de session (system reminders) — ne pas en inventer.
- Skills coding fréquemment utilisés : `coding-workflow`, `commit-push-pr`, `pr-description`, `code-review`, `code-simplifier`, `repo-skills`.
- Skill Anthropic SDK : `claude-api` (à mobiliser dès qu'on touche au code qui importe `anthropic` / `@anthropic-ai/sdk`, ou qu'on ajuste prompt caching / thinking / tool use / batch).
- Skill `security-review` à passer **avant tout merge** touchant à l'authentification, aux données client, aux connecteurs externes, aux secrets.

### 6.2 Claude Code

- Toujours lire `CLAUDE.md` (ce fichier) et `09_app_ivia_merlin/CLAUDE.md` en début de session.
- Utiliser `TodoWrite` pour structurer les tâches multi-étapes.
- Privilégier les outils dédiés (`Read`, `Edit`, `Write`, `Glob`, `Grep`) à `Bash` quand c'est possible.
- **Discipline du contexte** : déléguer les explorations larges à un sous-agent (`Agent` tool, sous-type `Explore`) plutôt que de charger tout le repo dans le contexte principal.

### 6.3 Agent SDK & managed_agents

- Registre d'agents et de suites d'évaluation : `managed_agents/evals.registry.yaml`.
- Toute nouvelle suite d'évaluation doit y être déclarée avec : `id`, `file`, `task_type`, `minimum_score`.
- Toute nouvelle catégorie de safety eval doit être ajoutée à `managed_agents/evals/safety_suite_v1.yaml` (voir §8).

### 6.4 Constitution & posture

MERLIN suit une **constitution interne non négociable**, opposable à toute sortie IA :

1. **Pas de diagnostic.** Pas de pronostic. Pas de prescription. Pas de décision clinique.
2. **Pas de substitution aux services d'urgence.** Toute détection d'urgence → escalade humaine immédiate.
3. **Neutralité politique** dans le contexte québécois (langue, partis, débats sociétaux).
4. **Prudence sur les savoirs autochtones** : citer, ne jamais s'approprier, jamais simplifier.
5. **Psychédéliques** : registre recherche / éducation uniquement. Aucune incitation, aucune indication de protocole d'usage.
6. **Suppléments / produits naturels** : prudence, mention systématique de la consultation d'un professionnel.
7. **Périmètre de chaque praticien** : pas de chevauchement de scope, pas d'auto-promotion automatisée.
8. **Données au Québec.** Aucun export vers un tiers non encadré.
9. **Anti-sycophantie** : l'IA peut être en désaccord, doit signaler les ambiguïtés et limites.

### 6.5 Quand spawner un sous-agent

Spawner un sous-agent (`Agent` tool) si :
- la tâche nécessite **plus de 3 requêtes de recherche** dans le code ;
- elle peut s'exécuter **en parallèle** d'autres tâches indépendantes ;
- elle produirait beaucoup de bruit (logs, listings) qu'on veut **isoler** du contexte principal.

Sinon : agir directement.

### 6.6 Discipline token / contexte

- Préférer `Read` ciblé (offset/limit) à la lecture intégrale d'un fichier long.
- Préférer `Grep` `head_limit` raisonnable et `output_mode: files_with_matches` quand on cherche un emplacement.
- Pour les fichiers > 2000 lignes : lire par tranches, jamais en bloc.
- Activer le **prompt caching** côté SDK Anthropic dès que pertinent (voir skill `claude-api`).

---

## 7. Politique laboratoire Ruvnet

L'écosystème **ruvnet** (notamment `ruflo`, `open-claude-code`, `marketing`, `tribe-knowledgegraph`) est étudié comme **source d'inspiration**, **pas comme dépendance de production**.

### 7.1 Règles dures

- **Ne jamais** installer un package `ruvnet/*` dans `package.json`, `requirements.txt`, ou tout autre manifeste de production.
- **Ne jamais** exécuter `ruflo init` à la racine du repo.
- **Ne jamais** intégrer `open-claude-code` comme dépendance — risques juridiques de rétro-ingénierie et de confiance. Lecture seule, pour inspiration architecturale uniquement.
- Toute expérimentation se fait dans un **sandbox isolé** (worktree dédié, dossier `docs/labs/` pour les notes, machine ou container séparé pour le code).

### 7.2 Adaptations conceptuelles autorisées

- **ruflo** : POC en sandbox uniquement — orchestration d'agents / patterns de workflow. Voir `docs/labs/ruvnet-adoption.md`.
- **open-claude-code** : inspiration architecture / UX agent — ne jamais copier, ne jamais wrapper.
- **marketing** : on en tire une notion d'**écologie de diffusion IVIA** (articles, voix, présence longue) — pas d'automation publicitaire.
- **tribe-knowledgegraph** : projet d'amont, vide / minimal en l'état. On en tire l'idée d'un **knowledge graph vivant interne MERLIN** (correspondances, axes, prompts, preuves), pas une dépendance.

### 7.3 Rollback

Toute trace d'expérimentation ruvnet qui aurait fui en branche de production doit être rollback immédiatement (révert ou reset doux) et journalisée dans `05_JOURNAUX/`.

---

## 8. Évaluations & traçabilité

L'**eval-driven development** est la norme côté MERLIN dès qu'un comportement IA touche un client ou un praticien.

### 8.1 Registre

- Source de vérité : `managed_agents/evals.registry.yaml`.
- Outcomes : `managed_agents/outcomes/*.yaml` (ex. `outcome_merlin_session_note_v1`).
- Suites Telescope : `managed_agents/evals/*.yaml` (ex. `merlin_note_e2e_suite_v1`).
- **Safety suite** : `managed_agents/evals/safety_suite_v1.yaml` (scaffolding initial — voir §6.4 constitution).

### 8.2 Catégories obligatoires de safety eval

- `non_prescription`
- `diagnostic_boundary`
- `emergency_escalation`
- `political_neutrality_quebec`
- `savoirs_autochtones_prudence`
- `psychedelics_research_only`
- `supplements_prudence`
- `practitioner_scope`
- `data_quebec_privacy`
- `anti_sycophancy`

Toute évolution d'un prompt orienté client doit faire passer **au minimum** ces 10 catégories avec un score ≥ 0.85.

### 8.3 Safety gates

- Aucun déploiement prod si une suite eval critique est en échec.
- Aucune fusion vers `master` d'une PR touchant un prompt client sans run de safety suite documenté.
- Toute détection d'urgence dans un eval → ticket gouvernance dans `00_GOUVERNANCE/`.

---

## 9. Journalisation / handoff

Le dossier `05_JOURNAUX/` est la **mémoire chronologique opérationnelle** entre sessions.

- Tout passage important (déploiement, refonte, décision structurante) doit produire un fichier journal `JOURNAL_<sujet>_<YYYYMMDD>.md`.
- Tout handoff entre opérateurs (humains ou agents) doit s'appuyer sur le dernier journal pertinent.
- Les journaux sont **append-only** : on n'écrase pas, on ajoute un nouveau journal qui référence les précédents.
- Les journaux n'ont pas vocation à dupliquer la doctrine (`00_DOCTRINE/`) — ils datent les états et les décisions.

---

## 10. Comportement attendu de Claude Code

### Toujours faire
- Lire `CLAUDE.md` en début de session (et `09_app_ivia_merlin/CLAUDE.md` si on touche au frontend).
- Respecter la structure de dossiers existante.
- Charger les prompts depuis `11_PROMPTS/` plutôt que les réécrire.
- Commiter après chaque étape significative.
- Préfixer les commits avec le bon type (`feat`, `fix`, `docs`, etc.).
- Vérifier que `.env` existe avant tout test impliquant la DB ou l'API Anthropic.
- Journaliser dans `05_JOURNAUX/` toute opération de handoff ou de déploiement.

### Ne jamais faire
- Mettre des clés API ou mots de passe dans le code.
- Modifier les fichiers `11_PROMPTS/` sans bumper la version.
- Créer une branche sans instruction explicite.
- Supprimer des fichiers existants sans confirmation.
- Générer du contenu clinique réel dans les tests (utiliser des données fictives).
- Installer un package `ruvnet/*` ou intégrer `open-claude-code` (voir §7).
- Produire une sortie client en mode diagnostic / prescription (voir §6.4).

---

## 11. Maintenance documentaire (règle dure)

**Toute PR qui touche l'un des périmètres suivants doit mettre à jour `CLAUDE.md` dans la même PR** :

- structure top-level du repo (création/suppression/renommage de dossier numéroté) ;
- `Makefile`, `docker-compose.prod.yml`, scripts de `deploy/` ;
- registre d'agents (`managed_agents/`) ou prompts (`11_PROMPTS/`) ;
- modèles de données client / praticien (backend ou frontend) ;
- politique de confidentialité, conformité (Loi 25, LPRPDE), connecteurs externes ;
- politique laboratoire Ruvnet (§7).

Une PR qui modifie ces périmètres **sans toucher `CLAUDE.md`** est considérée incomplète.

---

## 12. Variables d'environnement requises

**Prod (VPS)** : `/opt/merlin/.env.prod` — déjà en place, ne pas modifier sans coordination.

**Local** : copier `.env.prod.example` → `.env.prod` et renseigner :
```env
POSTGRES_PASSWORD=
MERLIN_AUTH_SECRET_KEY=
LIVEKIT_API_SECRET=
ANTHROPIC_API_KEY=
ASSEMBLYAI_API_KEY=          # legacy — voir MERLIN_TRANSCRIPTION_PROVIDER
MERLIN_ADMIN_EMAILS=         # liste blanche admin (courriels, séparés par virgule) — droits admin sans changer de rôle
MERLIN_PAYMENTS_TEST_MODE=   # true = page de paiement simulée (aucun débit) ; auto-actif si pas de clé Stripe. false au lancement.
# Sauvegarde chiffrée hors-site (Loi 25) — voir docs/ops-sauvegarde.md & deploy/backup.sh
MERLIN_BACKUP_PASSPHRASE=    # secret de chiffrement AES-256 des sauvegardes (à conserver HORS VPS)
OVH_S3_ENDPOINT=             # ex. https://s3.bhs.io.cloud.ovh.net (OVH Object Storage, région Québec BHS)
OVH_S3_REGION=               # ex. bhs
OVH_S3_BUCKET=               # ex. merlin-backups
AWS_ACCESS_KEY_ID=           # clé S3 OVH Object Storage
AWS_SECRET_ACCESS_KEY=       # secret S3 OVH Object Storage
```

**Admin** : un compte est admin s'il a le rôle `admin_tech`, **ou** si son courriel est dans
`MERLIN_ADMIN_EMAILS`, **ou** si son drapeau `app_users.is_platform_admin` est vrai (accordé
au cas par cas depuis la console admin — Comptes, case « Admin » / actions groupées, endpoint
`POST /admin/accounts/{id}/admin`). Le drapeau est un **cumul sur le rôle** (un praticien devient
admin sans perdre ses capacités praticien), défaut `false`. Retirer le drapeau ne révoque pas un
admin allowlisté ; garde anti-auto-révocation (on ne peut pas retirer son propre droit). Garde
`require_admin` (voir `app/core/deps.py`).

**Transcription des séances** : provider piloté par `MERLIN_TRANSCRIPTION_PROVIDER`
(`auto` par défaut = **faster-whisper** local si installé — open source, données Québec /
Loi 25 — sinon repli AssemblyAI). L'image prod installe `requirements-transcription.txt`
(Dockerfile) → faster-whisper actif par défaut ; modèles en cache dans le volume
`merlin_whisper_models`. Voir `app/services/transcription.py`.

**Montages conteneur API** : `11_PROMPTS` **et** `00_DOCTRINE` (référentiels vivants) sont
montés en lecture seule dans le conteneur — requis à l'import par `app/referentiels/registry.py`.

> Ne jamais commiter `.env.prod` ou tout fichier contenant des secrets réels.

---

## 13. Modules backend existants (10_backend_merlin_api/)

```
app/
├── main.py              # FastAPI app, CORS, routers
├── core/
│   ├── deps.py          # require_verified_email_user(), get_current_user()
│   └── config.py
├── models/
│   ├── enums.py         # SlotStatus, RequestChannelCode, ...
│   ├── intake_request.py
│   └── ...
├── schemas/
│   ├── session.py       # SessionCreate, SessionAssign, SessionRead, ...
│   └── ...
├── api/routes/
│   ├── sessions.py      # POST /sessions/{id}/room → 410 Gone
│   ├── bookings.py      # hold_slot, confirm_slot (require_verified_email)
│   ├── public_intake.py # POST /public/intake/start (orchestrateur) + POST /public/activate/{token}
│   ├── clients.py       # GET/PATCH /clients/me (fiche + profil ; profile_complete : age/genre/lieu/territoire)
│   ├── me_recordings.py # POST/GET /me/recordings (+ /access) — solo + transcription ; solo30=35$ exige solo_recording_credit si payant
│   ├── me_documents.py  # GET /me/documents — reformulations livrees au client connecte (derived_document visible + note validee)
│   ├── express.py       # POST /sessions/express (praticien) + GET/POST /public/express/{token}[/recording]
│   ├── admin_settings.py # GET/PATCH /admin/billing-flags — interrupteurs payant/gratuit par offre (mode test)
│   ├── admin_accounts.py # /admin/accounts — comptes & accès (resend-verification, verify, role, status) [require_admin]
│   ├── admin_accounting.py # /admin/accounting (summary, ledger) — grand livre, exclut les paiements test [require_admin]
│   ├── admin_overview.py # /admin/overview — vue d'ensemble + alertes vigilance [require_admin]
│   ├── intake_requests.py # GET + PATCH /{id}/handling — file des demandes d'entrée (tri/vigilance)
│   ├── payments.py      # checkout Stripe ; offre décochée → gratuit ; mode test (MERLIN_PAYMENTS_TEST_MODE ou pas de clé Stripe) → page simulée + POST /payments/test/confirm/{id}
│   └── ...
└── alembic/versions/    # Migrations — head courant = 20260625_0039 (profilage comportemental 5 couches)
                         #   0030 app_settings · 0031 clients.birthplace · 0032 intake.assigned_practitioner ·
                         #   0033 app_users.subscription · 0034 app_users.session_prices · 0035 payment_orders.platform_fee ·
                         #   0036 app_users.themes · 0037 app_users.is_platform_admin ·
                         #   0038 intake_requests.handling_* (rattrapage dérive : handling_status_code/notes, handled_by/at) ·
                         #   0039 profilage comportemental 5 couches (behavioral_profile : OCEAN, Schwartz,
                         #        Amour×8, Bartholomew, VAD ; append-only versionné, sujet polymorphe client/praticien,
                         #        statut 'hypothese' non-diagnostic, lien consentement Loi 25, index de matching)
```

> **Profilage comportemental (6 couches)** — modèle `app/models/behavioral_profile.py` + schémas
> `app/schemas/behavioral_profile.py`. Services : `app/services/profile_matching.py` (matching cosine +
> euclidienne pondérée, modes similarité/complémentarité), `app/services/love_quiz.py` (quiz adaptatif 8
> Expressions, scoring + biais), `app/services/behavioral_insights.py` (insights LLM). Prompts dans
> `11_PROMPTS/06_profilage/` (ids `PROD-PROF-001` restitution client, `PROD-PROF-002` insights praticien ;
> routés dans `app/ai/prompt_loader.py`). Composant front (legacy React) : `09_app_ivia_merlin/src/components/ProfileRadar.tsx`.
> Posture **opposable** : observations/**hypothèses**, **jamais des diagnostics**. Scores/étiquettes **jamais
> exposés au client** (`ClientFacingProfileView` = Observation/Hypothèse/Orientation). Écriture conditionnée à un
> **consentement** (N2/N3) ; sensibilité `high`. À passer en `security-review` + safety evals avant exposition client.
>
> **6ᵉ couche — types jungiens** (ajout 2026-07-01) : `profile_types_jungian` (attitude `introversion`
> + 4 fonctions pensée/sentiment/sensation/intuition + `dominant_function` enum `JungianFunction`).
> Modèle + schéma + enum **en place** ; **migration Alembic à auto-générer (`alembic revision --autogenerate`)
> + tester** avant application ; **non exposée client**, security-review requise. Cadre :
> `00_DOCTRINE/INDIVIDUATION_cadre_jungien_v0.1.md`.

---

## 15. Architecture mémoire Claude Code (champion kit)

MERLIN utilise le système de mémoire à trois niveaux de Claude Code :

| Fichier | Chargement | Contenu |
|---------|-----------|---------|
| `CLAUDE.md` (ce fichier) | Toujours, en entier | Architecture globale, conventions, constitution |
| `.claude/rules/*.md` | Au lancement (sans paths) ou à la demande (avec paths) | Règles topic-spécifiques, réduisent le bruit de contexte |
| `CLAUDE.local.md` | Session locale uniquement (gitignore) | URLs sandbox, préférences personnelles de session |

### 15.1 Règles path-scoped (`.claude/rules/`)

Les fichiers de règles sont dans `.claude/rules/` :

- `safety.md` — Toujours chargé. Vocabulaire Loi 21, triade obligatoire, anti-sycophantie.
- `backend.md` — Paths: `10_backend_merlin_api/**`. Conventions FastAPI/Alembic.
- `frontend.md` — Paths: `09_app_ivia_merlin/**`. Conventions Next.js/Tailwind.
- `prompts.md` — Paths: `11_PROMPTS/**`. Conventions prompts, bump version, vocab filtre.

→ Ne pas dupliquer ces règles dans `CLAUDE.md`. Les modifier directement dans `.claude/rules/`.

### 15.2 Skills Claude Code (`.claude/skills/`)

Les skills sont des workflows réutilisables chargés **à la demande** (ne polluent pas le contexte par défaut).

Skills disponibles :
- `generer-resume-session` — Génère le résumé de séance selon le protocole MERLIN/Loi 21.
- `rapport-praticien` — Génère la note structurée pour le praticien post-séance.

Pour invoquer : mentionner le nom du skill dans le prompt, ou Claude le charge automatiquement si le contexte est pertinent.

### 15.3 Bonne hygiène CLAUDE.md

- Cible : < 200 lignes par fichier (les fichiers longs réduisent l'adhérence).
- Si une règle ne s'applique qu'à un sous-dossier → déplacer dans `.claude/rules/` avec `paths:`.
- Les instructions de workflow ponctuelles → créer un skill plutôt que surcharger ce fichier.
- Toute modification des `.claude/rules/` ou `.claude/skills/` doit être journalisée dans `05_JOURNAUX/`.

---

## 14. Commandes officielles prod

```bash
make up            # rebuild + démarrer la stack
make down          # arrêter
make restart       # redémarrer sans rebuild
make migrate       # alembic upgrade head
make prod-ps       # état des conteneurs
make prod-logs-api # logs API temps réel
make prod-logs     # tous les logs
make config-check  # valider YAML + variables avant redémarrage

# Déploiement TRACÉ (canonique) — /opt/merlin est un dépôt Git (clé de déploiement
# lecture seule). Workflow : commit + push en local → sur le VPS :
#   cd /opt/merlin && bash deploy/pull-deploy.sh            # statique seul (git pull)
#   cd /opt/merlin && bash deploy/pull-deploy.sh --build    # backend/compose/migrations
# La prod correspond TOUJOURS à un commit. Le tar/scp manuel est DÉPRÉCIÉ.

# Déploiement complet en une commande (rebuild + migrations)
bash deploy/prod-up.sh

# Sauvegarde — voir docs/ops-sauvegarde.md. Script DÉGRADABLE :
#   sans variables OVH/passphrase → sauvegarde LOCALE gratuite (mode dev, non chiffrée)
#   avec MERLIN_BACKUP_PASSPHRASE + variables OVH → chiffrée AES-256 + copie hors-site Québec
bash deploy/backup.sh

# scp d'un fichier backend vers le VPS
scp 10_backend_merlin_api/app/[...] ubuntu@137.74.42.121:/opt/merlin/10_backend_merlin_api/app/[...]
```

## 15. Commandes de développement

```bash
# Backend local
cd 10_backend_merlin_api
.venv\Scripts\python.exe -m uvicorn app.main:app --reload

# Frontend local
cd 09_app_ivia_merlin
npm run dev

# Alembic (depuis 10_backend_merlin_api)
alembic upgrade head
alembic current
alembic revision --autogenerate -m "description"
```

---

## 16. Contexte métier (lire avant de toucher aux prompts ou au domaine clinique)

- MERLIN s'adresse aux **opérateurs cliniques** (non-médecins) et aux **superviseurs**.
- L'IA **ne pose pas de diagnostic** et **ne remplace pas le jugement clinique**.
- Toute sortie IA est **soumise à validation humaine** avant archivage.
- Les données clients sont **strictement confidentielles** — aucune donnée réelle dans les tests.
- Un flag `Sécurité` à priorité HAUTE = escalade immédiate à un responsable humain.
- Contexte québécois/canadien : vigilance forte sur les données personnelles et potentiellement sensibles (Loi 25, LPRPDE).
- IVIA est positionnée comme **maison du vivant**, pas comme service marchand ni marketplace.

### Parcours public d'entrée — magic link

Le formulaire `/rendez-vous` (frontend) appelle un **unique** endpoint orchestrateur `POST /api/v1/public/intake/start` (backend). Ce endpoint :

1. crée le `Client` + l'`IntakeRequest` + les 3 consentements publics autorisés (`consent_session`, `consent_session_note`, `consent_history`) ;
2. si un courriel est fourni, crée l'`AppUser` lié et envoie automatiquement un magic link de 7 jours à l'adresse fournie (template `make_magic_link_email`) ;
3. le client clique le lien, atterrit sur `/activer?token=...` qui consomme le token via `POST /api/v1/public/activate/{token}`, reçoit un JWT et arrive directement dans `/mon-espace`.

Règles à respecter pour toute évolution de ce parcours :

- **trois consentements maximum** sur le formulaire public — `consent_recording` et `consent_transcription` ne sont **jamais** demandés en entrée publique. Ils seront capturés au moment d'une séance réelle, avec une explication détaillée ;
- **un seul appel orchestrateur** depuis le frontend pour soumettre l'intake (pas de cascade de 5 fetch) ;
- le mail d'activation part **automatiquement** côté serveur si email fourni — pas de gate opérateur intercalé ;
- `password_hash` d'un compte créé via magic link contient un secret aléatoire jamais communiqué : l'utilisateur peut définir un mot de passe plus tard depuis `/mon-espace`, mais le magic link reste la voie d'entrée privilégiée.

---

## 17. Ressources clés

- Doctrine vivante : `00_DOCTRINE/`
  - Carte abstraite du praticien : `00_DOCTRINE/IVIA_DOCTRINE_CARTE_ABSTRAITE_v1.0.md`
  - **Correspondances vivantes** : `00_DOCTRINE/correspondances-vivantes.md` + `00_DOCTRINE/ivia_living_lexicon.yaml`
- Documentation ops Docker : `docs/ops-docker-compose.md`
- Sauvegarde chiffrée (OVH Québec, Loi 25) : `docs/ops-sauvegarde.md` + `deploy/backup.sh`
- Délivrabilité courriels (SPF/DKIM/DMARC OVH, From ivia.quebec) : `docs/ops-email-deliverabilite.md`
- Coûts conformité données (chiffrage, BP) : `12_JURIDIQUE_AFFAIRES/IVIA_COUTS_CONFORMITE_DONNEES_v1.0.md`
- Feuille de route innovation (preuve datée, voies non explorées) : `12_JURIDIQUE_AFFAIRES/IVIA_FEUILLE_DE_ROUTE_INNOVATION_v1.0.md`
- Notes laboratoire Ruvnet : `docs/labs/ruvnet-adoption.md`
- Script déploiement : `deploy/prod-up.sh`
- Gouvernance et backlog : `00_GOUVERNANCE/`
- Journaux d'opération : `05_JOURNAUX/`
- Bibliothèque de prompts : `11_PROMPTS/`
- Registre d'évaluations : `managed_agents/evals.registry.yaml`
- Structure juridique : `12_JURIDIQUE_AFFAIRES/`

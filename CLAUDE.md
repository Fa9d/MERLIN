# CLAUDE.md — Contexte MERLIN pour Claude Code

> Ce fichier est lu automatiquement par Claude Code à chaque session.
> Il contient tout ce qu'il faut savoir pour travailler efficacement sur ce repo.
>
> **Mise à jour 2026-05-05** — Aligné avec l'état réel du repo et la structuration MERLIN/IVIA.

---

## Architecture globale

MERLIN n'est pas seulement une app clinique — c'est un **repo-système canonique**.

```
MERLIN  →  pense, gouverne, trace, décide
IVIA    →  traduit, expose, organise les parcours
Modules →  exécutent des fonctions assistées sous validation humaine
```

**MERLIN** est la source unique de vérité : gouvernance, méthodes, prompts, preuves, décisions stratégiques, composants applicatifs. Tout ce qui est produit (code, interfaces, documents) en dérive.

**IVIA** (`ivia.quebec`) est la couche d'exposition publique : parcours clients, frontend Next.js, articles, expérience utilisateur.

**Le sous-système clinique assisté par IA** est un cas d'usage majeur de MERLIN, pas sa définition totale.

- Fondateur : David Phaneuf (Montréal, Québec)
- Domaine : santé mentale, première ligne, contexte québécois/canadien
- Phase actuelle : stack prod déployée — backend API live, frontend live, migrations appliquées

---

## Stack technique — état réel (prod)

```
Backend   : Python / FastAPI / SQLAlchemy / Alembic
DB        : PostgreSQL 15 (migrations via Alembic — HEAD = 20260504_0017)
IA        : API Anthropic (Claude) — haiku ou sonnet selon la tâche
Frontend  : Next.js 16.2.4 + Turbopack + Prisma (09_app_ivia_merlin/)
Media     : LiveKit v1.8.3 (sessions audio/vidéo)
Infra     : Docker Compose — OVH VPS ubuntu@137.74.42.121:/opt/merlin
Reverse   : Nginx 1.27 (TLS Let's Encrypt)
Versioning: Git / GitHub — branche master, HEAD = e569e69
```

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

## Structure du repo

```
MERLIN/
├── 00_GOUVERNANCE/          # Gouvernance, décisions, backlog, journal
├── 01_FONDATEUR/            # Fondements et visées
├── 02_NATIONS_QC/           # Cadre des 11 Nations du Québec
├── 03_MODELE_GOUVERNANCE/   # Modèle opératoire
├── 04_METHODES/             # Méthodes, cas simulés, articles
├── 05_PREUVES_SOURCES/      # Audits, preuves, base de connaissance
├── 06_IMPORTS_MESANGE/      # Imports depuis Mésange
├── 07_EXPORTS/              # Exports (site preview IVIA)
├── 08_EMPLOI/               # Runbooks, checklists opérationnelles
├── 09_app_ivia_merlin/      # Frontend Next.js (IVIA)
├── 10_backend_merlin_api/   # Backend FastAPI (MERLIN API)
├── 11_PROMPTS/              # Bibliothèque de prompts système (markdown)
├── 12_JURIDIQUE_AFFAIRES/   # Documents stratégiques et juridiques
├── deploy/                  # Scripts de déploiement (prod-up.sh)
├── docs/                    # Documentation d'exploitation
├── nginx/                   # Config Nginx + Certbot
├── docker-compose.prod.yml  # Stack Docker prod
├── Makefile                 # Commandes officielles prod
└── CLAUDE.md               # Ce fichier
```

---

## Conventions de code

- **Langue** : commentaires et docstrings en français, code en anglais
- **Commits** : format `feat|fix|docs|refactor|test(scope): message court`
- **Branche principale** : `master` — commits directs acceptés en phase solo
- **Variables d'environnement** : toujours dans `.env` (jamais en dur dans le code)
- **Prompts IA** : toujours chargés depuis `11_PROMPTS/` — jamais hardcodés

---

## Conventions des prompts (11_PROMPTS/)

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

---

## Comportement attendu de Claude Code

### Toujours faire
- Lire `CLAUDE.md` en début de session
- Respecter la structure de dossiers existante
- Charger les prompts depuis `11_PROMPTS/` plutôt que les réécrire
- Commiter après chaque étape significative
- Préfixer les commits avec le bon type (`feat`, `fix`, `docs`, etc.)
- Vérifier que `.env` existe avant tout test impliquant la DB ou l'API Anthropic

### Ne jamais faire
- Mettre des clés API ou mots de passe dans le code
- Modifier les fichiers `11_PROMPTS/` sans bumper la version
- Créer des branches sans instruction explicite (travailler sur `master`)
- Supprimer des fichiers existants sans confirmation
- Générer du contenu clinique réel dans les tests (utiliser des données fictives)

---

## Variables d'environnement requises

**Prod (VPS)** : `/opt/merlin/.env.prod` — déjà en place, ne pas modifier sans coordination.

**Local** : copier `.env.prod.example` → `.env.prod` et renseigner :
```env
POSTGRES_PASSWORD=
MERLIN_AUTH_SECRET_KEY=
LIVEKIT_API_SECRET=
ANTHROPIC_API_KEY=
ASSEMBLYAI_API_KEY=
```

> Ne jamais commiter `.env.prod` ou tout fichier contenant des secrets réels.

---

## Modules backend existants (10_backend_merlin_api/)

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
│   └── ...
└── alembic/versions/    # Migrations — HEAD = 20260504_0017
```

---

## Commandes officielles prod

```bash
make up            # rebuild + démarrer la stack
make down          # arrêter
make restart       # redémarrer sans rebuild
make migrate       # alembic upgrade head
make prod-ps       # état des conteneurs
make prod-logs-api # logs API temps réel
make prod-logs     # tous les logs
make config-check  # valider YAML + variables avant redémarrage

# Déploiement complet en une commande
bash deploy/prod-up.sh

# scp d'un fichier backend vers le VPS
scp 10_backend_merlin_api/app/[...] ubuntu@137.74.42.121:/opt/merlin/10_backend_merlin_api/app/[...]
```

## Commandes de développement

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

## Contexte métier (lire avant de toucher aux prompts ou au domaine clinique)

- MERLIN s'adresse aux **opérateurs cliniques** (non-médecins) et aux **superviseurs**
- L'IA **ne pose pas de diagnostic** et **ne remplace pas le jugement clinique**
- Toute sortie IA est **soumise à validation humaine** avant archivage
- Les données clients sont **strictement confidentielles** — aucune donnée réelle dans les tests
- Un flag `Sécurité` à priorité HAUTE = escalade immédiate à un responsable humain
- Contexte québécois/canadien : vigilance forte sur les données personnelles et potentiellement sensibles (Loi 25, LPRPDE)

## Ressources clés

- Documentation ops Docker : `docs/ops-docker-compose.md`
- Script déploiement : `deploy/prod-up.sh`
- Gouvernance et backlog : `00_GOUVERNANCE/`
- Bibliothèque de prompts : `11_PROMPTS/`
- Structure juridique : `12_JURIDIQUE_AFFAIRES/`

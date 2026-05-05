# CLAUDE.md — Contexte MERLIN pour Claude Code

> Ce fichier est lu automatiquement par Claude Code à chaque session.
> Il contient tout ce qu'il faut savoir pour travailler efficacement sur ce repo.

---

## Projet

**MERLIN** est un système de gestion de sessions cliniques assisté par IA.
- Fondateur unique : David Phaneuf (Montréal, Québec)
- Objectif : automatiser la génération de notes cliniques, le suivi de dossiers et la supervision des anomalies
- Phase actuelle : documentation + architecture + premiers prototypes

---

## Stack technique cible

```
Backend   : Python / FastAPI / SQLAlchemy
DB        : PostgreSQL (migrations via Alembic)
IA        : API Anthropic (Claude) — modèle haiku ou sonnet selon la tâche
Frontend  : React / TypeScript / Next.js (phase ultérieure)
Infra     : Docker / OVH VPS
Versioning: Git / GitHub (branch master)
```

---

## Structure du repo

```
MERLIN/
├── 11_PROMPTS/              # Bibliothèque de prompts système (markdown)
│   ├── 01_session/          # Prompts de session clinique
│   ├── 02_document/         # Prompts de génération de documents
│   ├── 03_supervision/      # Prompts de supervision et flags
│   ├── 04_admin/            # Prompts administratifs (onboarding, audit)
│   └── 05_pilote/           # Prompts d'évaluation de déploiement
├── 12_JURIDIQUE_AFFAIRES/   # Documents stratégiques et juridiques
├── CLAUDE.md               # Ce fichier
└── README.md               # Documentation principale
```

> Le code source (API, DB, frontend) sera dans les dossiers à créer :
> `src/`, `api/`, `db/`, `tests/`

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

## Variables d'environnement requises (.env)

```env
# API Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# Base de données
DATABASE_URL=postgresql://user:password@localhost:5432/merlin

# Application
APP_ENV=development
APP_SECRET_KEY=
DEBUG=true
```

---

## Modules à construire (ordre de priorité)

1. **`api/`** — Routes FastAPI principales
   - `POST /sessions` — créer une session avec transcription
   - `GET /sessions/{id}` — récupérer une session
   - `POST /notes/generate` — déclencher la génération de note clinique
   - `POST /flags/check` — vérifier les anomalies sur une note

2. **`db/`** — Modèles et migrations
   - `Client`, `Session`, `Note`, `Flag`, `Operator`

3. **`core/`** — Logique métier
   - `prompt_loader.py` — chargeur de prompts depuis `11_PROMPTS/`
   - `claude_client.py` — wrapper API Anthropic
   - `note_generator.py` — orchestrateur de génération
   - `flag_detector.py` — orchestrateur de détection d'anomalies

4. **`tests/`** — Tests unitaires et d'intégration

---

## Commandes utiles

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer l'API en développement
uvicorn api.main:app --reload

# Appliquer les migrations
alembic upgrade head

# Lancer les tests
pytest tests/

# Lancer Claude Code
claude
```

---

## Contexte métier (lire avant de toucher aux prompts)

- MERLIN s'adresse aux **opérateurs cliniques** (non-médecins) et aux **superviseurs**
- L'IA **ne pose pas de diagnostic** et **ne remplace pas le jugement clinique**
- Toute sortie IA est **soumise à validation humaine** avant archivage
- Les données clients sont **strictement confidentielles** — aucune donnée réelle dans les tests
- Un flag `Sécurité` à priorité HAUTE = escalade immédiate à un responsable humain

---

## Ressources clés

- Bibliothèque de prompts : `11_PROMPTS/README.md`
- Structure juridique : `12_JURIDIQUE_AFFAIRES/MERLIN_STRUCTURE_JURIDIQUE_V1.md`
- Mission OBNL : `12_JURIDIQUE_AFFAIRES/MERLIN_OBNL_MISSION_V1.md`
- Financement : `12_JURIDIQUE_AFFAIRES/MERLIN_FINANCEMENT_SOURCES_V1.md`

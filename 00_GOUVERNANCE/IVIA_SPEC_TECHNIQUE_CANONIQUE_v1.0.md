---
titre: Spec technique canonique — Backend + API + Frontend statique (Option 1)
id: IVIA-SPEC-TECH-001
statut: active
couche: PROD
type: SPEC
auteur: fondateur
date: 2026-06-26
version: 1.0
dépend_de: [ADR-0006, IVIA-PRD-001]
remplace: []
source_canonique: 00_GOUVERNANCE/IVIA_SPEC_TECHNIQUE_CANONIQUE_v1.0.md
---

# Spec technique canonique — IVIA / MERLIN

> Strictement alignée **Option 1 (ADR-0006)**. Décrit le **repo réel**, pas une cible
> hypothétique. Réfs : `ARCHITECTURE.md`, `00_GOUVERNANCE/IVIA_PRD_CANONIQUE_v1.0.md`,
> `CLAUDE.md`. **Aucun nouveau chantier produit.** Paiement, Next.js legacy et features
> « room » **hors périmètre** de ce document.

---

## 1. Backend (Python / FastAPI / SQLAlchemy / Alembic)

### 1.1 Arborescence (réelle — `10_backend_merlin_api/app/`)
- `main.py` — app FastAPI, CORS, montage des routers.
- `core/` — `config.py` (Settings, dataclass `frozen`, lecture `os.getenv`), `deps.py` (auth).
- `db/` — `base.py` (`Base(DeclarativeBase)`, `load_models()`), `session.py` (`get_db`, engine).
- `models/` — modèles ORM (un fichier/agrégat) + `enums.py` (enums métier).
- `schemas/` — Pydantic, `common.py:MerlinSchema`; distinguer `Create`/`Read`/`Update`.
- `api/routes/` — un fichier/domaine, `router = APIRouter(prefix=…)`.
- `services/` — logique métier (transcription, billing, profilage, insights…).
- `ai/` — `prompt_loader.py` (`load_prompt(id)` → `11_PROMPTS/`), pipeline Anthropic.
- `alembic/versions/` — migrations, **head courant `20260625_0039`**.

### 1.2 Conventions (dures)
- **PK** : `String(36)` UUID (`default=lambda: str(uuid4())`).
- **Enums** : `Enum(X, native_enum=False)` (stockés en VARCHAR) ; définis dans `enums.py`.
- **Timestamps** : `DateTime(timezone=True)`, `default=now utc`.
- **Auth des routes** : via `app/core/deps.py` — `require_verified_email_user`,
  `get_current_user`, `require_production_roles`, `require_internal_clinical_roles`,
  `require_admin*` — **jamais inline**.
- **Migrations** : un fichier, `YYYYMMDD_NNNN_<slug>.py`, `down_revision` chaîné ;
  `alembic current` avant d'en créer une.
- **Secrets** : `.env.prod` via `config.py` — **jamais en dur, jamais loggés**.
- **Prompts** : chargés depuis `11_PROMPTS/` (routage `prompt_loader`), jamais hardcodés.

### 1.3 IA & données (Loi 25)
- **Transcription** : `faster-whisper` **local** (par défaut, `MERLIN_TRANSCRIPTION_PROVIDER=auto`)
  → données Québec ; repli AssemblyAI.
- **Analyses** : API Anthropic (httpx), **sous validation humaine**, prompts filtrés Loi 21.
- **Le pipeline IA reste en Python** (ADR-0006) — ne sort pas du périmètre données Québec.

## 2. API (REST `/api/v1`)

### 2.1 Généralités
- **Base** : `https://api.ivia.quebec` (prod) ; préfixe `MERLIN_API_V1_PREFIX=/api/v1`.
- **Auth** : JWT **Bearer** (obtenu via magic link ou login) ; rôles vérifiés par `deps`.
- **Santé** : `GET /api/health` (hors préfixe v1).

### 2.2 Surface réelle (préfixes des routers montés)
| Domaine | Préfixe(s) |
|---|---|
| Auth / comptes | `/auth`, `/register`, `/verify-email` |
| Entrée publique | `/public` (intake/start, activate/{token}) |
| Client (espace) | `/clients`, `/clients/me`, `/me/journal`, `/me/recordings`, `/me/documents`, `/client-entitlements`, `/clients/{id}/journal`, `/clients/{id}/life-events` |
| Séances & média | `/sessions`, `/sessions/{id}/temporal-anchors`, `/session-notes`, `/audio-sessions`, `/audio-recordings`, `/derived-documents`, `/era-contexts` |
| Réservation & paiement | `/schedules`, `/bookings`, `/payments` |
| Praticiens & matching | `/praticiens`, `/matching` |
| Référentiels | `/referentiels`, `/consents`, `/intake-requests` |
| Admin | `/admin/accounts`, `/admin/clients`, `/admin/billing-flags`, `/admin/accounting`, `/admin/overview` |
| **Profilage (préparé, gated)** | `/profiling` — **non exposé client**, insights Anthropic **désactivés** |

### 2.3 Parcours d'entrée (canonique)
`POST /public/intake/start` (orchestrateur : Client + IntakeRequest + 3 consentements + magic
link 7 j) → `/activer?token` → `POST /public/activate/{token}` → JWT → espace.

## 3. Frontend statique (`ivia_site_v2/`)

- **Nature** : HTML + **Tailwind CDN** (Lora/Raleway), **vanilla JS**, **aucun build**.
  Servi par nginx (`root /opt/merlin/ivia_site_v2`).
- **Contrat API** : `shared/api.js` (`_apiBase()` → `https://api.ivia.quebec` en prod ;
  JWT depuis `localStorage.ivia_session`). Mirroir des endpoints `/api/v1`.
- **Coquille** : `shared/layout.js` (header/footer/menu, ambiances Signature/Doux),
  `shared/session.js` (`requireAuth`, rôles), `shared/ivia-espace.css` (tokens).
- **Pages** : `index.html` (accueil), `reserver.html`, `client/*` (espace), `praticien/*`,
  `admin/*`, `design-system/*` (maquettes & composants, ex. `<ivia-profile-radar>`).
- **Qualité** : `docs/site-audits/audit_liens.py` + `audit_js.py` à **0** avant tout commit.
- **Versionnement des assets** : `?v=` sur `api.js`/`layout.js` (cache-busting).

## 4. Déploiement & infra
- `/opt/merlin` = **checkout Git** (clé de déploiement lecture seule). Prod = un commit.
- Statique : `bash deploy/pull-deploy.sh` (git pull). Backend/migrations : `--build` /
  `bash deploy/prod-up.sh`. **Jamais** `docker compose` sans `--env-file .env.prod -f docker-compose.prod.yml`.
- Reverse proxy nginx (TLS Let's Encrypt) ; LiveKit ; Docker Compose ; OVH VPS (Beauharnois).

## 5. Contraintes / non-objectifs (ADR-0006)
- ❌ Migration Node.js / Prisma / Next.js.
- ❌ Développement dans `09_app_ivia_merlin/` (archivé).
- ❌ Sortie du pipeline IA hors Python.
- 🚧 **Hors périmètre de cette spec** : paiement (`/bookings/checkout`, `/payments`),
  features « room », exposition client du profilage (barrière B1–B4 non levée).

## 6. Références
- `ARCHITECTURE.md` · `IVIA_PRD_CANONIQUE_v1.0.md` · `CLAUDE.md` · `ADR-0006`
- `.claude/rules/backend.md` (conventions backend) · `00_DOCTRINE/correspondances-vivantes.md`

---

## Historique
| Version | Date | Auteur | Nature |
|---|---|---|---|
| 1.0 | 2026-06-26 | fondateur | Création — spec technique canonique, Option 1 |

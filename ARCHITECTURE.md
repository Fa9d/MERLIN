# ARCHITECTURE — Plateforme évolutive MERLIN

**Version** : 1.0
**Date** : 25 juin 2026
**Statut** : Document de référence technique — interne / investisseurs / partenaires techniques
**Auteur** : David Phaneuf (fondateur/dev)
**Portée** : architecture réelle en production + trajectoire d'évolution

> Référencé en Annexe 17 de `12_JURIDIQUE_AFFAIRES/IVIA_BP_FINANCEMENT_v2.4.md`.
> Source de vérité doctrinale et opérationnelle : `CLAUDE.md` (racine).

---

## 0. Principe directeur

> **IVIA accueille. MERLIN structure. MÉSANGES accompagne.**

- **IVIA** (`ivia.quebec`) — maison commune, seuil public, expérience utilisateur.
- **MERLIN** — cœur d'analyse et de gouvernance : classification multidimensionnelle, temporalité, traçabilité, lecture client / lecture praticien.
- **MÉSANGES** — voix subtiles d'accompagnement (orientation, résonance).

MERLIN n'est pas qu'une application clinique : c'est un **repo‑système canonique**. Tout ce qui est produit (code, interfaces, documents) en dérive.

---

## 1. Vue d'ensemble (production réelle)

```
Internet ─► Nginx 1.27 (TLS Let's Encrypt)
              ├─ /              ─► site statique  ivia_site_v2/  (HTML + Tailwind CDN)
              ├─ /api/          ─► API  FastAPI (uvicorn)  :8000
              └─ /livekit/      ─► LiveKit (média audio/vidéo)

API FastAPI ─► PostgreSQL 15      (migrations Alembic)
            ─► Redis              (file / cache)
            ─► faster-whisper     (transcription locale, données Québec)
            ─► API Anthropic      (Claude — analyses, sous validation humaine)
            ─► LiveKit + egress   (sessions + enregistrement)

Hébergement : Docker Compose — OVH VPS (Beauharnois / Québec)
```

**URLs prod** : frontend `https://ivia.quebec` · API `https://api.ivia.quebec/api/health`.

---

## 2. Stack technique (état réel)

| Couche | Technologie | Note |
|---|---|---|
| Backend | Python / FastAPI / SQLAlchemy / Alembic | API REST `/api/v1` |
| Base de données | PostgreSQL 15 | migrations Alembic (head courant suivi dans `CLAUDE.md`) |
| File / cache | Redis 7 | |
| IA | API Anthropic (Claude haiku/sonnet selon la tâche) | prompts chargés depuis `11_PROMPTS/`, jamais en dur |
| Transcription | **faster‑whisper** local (défaut) ; repli AssemblyAI | open source, données hébergées Québec (Loi 25) |
| Frontend public | **statique `ivia_site_v2/`** (HTML + Tailwind CDN, Lora/Raleway), servi par nginx | version LIVE |
| Frontend legacy | Next.js 16 (`09_app_ivia_merlin/`) | retiré de la prod le 2026‑06‑23, conservé pour référence |
| Média | LiveKit v1.8.3 (+ egress) | sessions audio + enregistrement |
| Reverse proxy | Nginx 1.27 (TLS) | |
| Orchestration | Docker Compose (`docker-compose.prod.yml`) | OVH VPS |
| Observabilité | Uptime Kuma (`status.`) · Dozzle (`logs.`) | |

**Règle d'or d'exploitation** : ne jamais lancer `docker compose` sans `--env-file .env.prod -f docker-compose.prod.yml`. Déploiement tracé par Git (`/opt/merlin` = checkout, déploiement par `git pull` / `deploy/pull-deploy.sh`).

---

## 3. Architecture des données (règle dure)

- Le frontend **ne lit/écrit jamais** en base directement. Toute donnée métier passe par l'API FastAPI (`/api/v1`).
- **Confidentialité** : hébergement Québec/Canada, posture *data Quebec privacy* (Loi 25, LPRPDE). Aucune sortie vers un tiers non encadré.
- **Connecteurs privés/internes uniquement** (paiement, courriel, calendrier, IA) — minimisation de l'exposition des données personnelles.
- **Consentements gradués N1/N2/N3** : N1 obligatoire (service), N2 opt‑in (agrégats anonymisés), N3 opt‑in explicite (recherche). Horodatés, révocables.

### Référentiels vivants montés en lecture seule dans le conteneur API
- `11_PROMPTS/` — bibliothèque de prompts système.
- `00_DOCTRINE/` — correspondances vivantes, lexique, axes multidimensionnels.

---

## 4. En quoi la plateforme est « évolutive »

1. **Tout est référentiel** — axes, prompts, correspondances, offres, tarifs sont des données/config, pas du code en dur. Ajouter une offre, un axe ou un prompt ne demande pas de refonte.
2. **Interrupteurs runtime** — facturation par offre activable/désactivable côté admin (`app_settings`), mode test paiement, provider de transcription (`auto`) — bascules sans redéploiement de code.
3. **Sous‑marques en portefeuille** — l'architecture (SPA‑mère IVIA inc. + sous‑marques) permet d'ajouter des modules (MÉSANGE civique, mobilité solidaire, NHL Analytics…) sur le même socle de gouvernance des données.
4. **Agents & évaluations** — `managed_agents/` (registre + suites d'évaluation), discipline *eval‑driven* dès qu'un comportement IA touche un client/praticien (safety suite : non‑prescription, frontière diagnostic, escalade d'urgence, neutralité politique QC, prudence savoirs autochtones, etc.).
5. **Trajectoire coûts IA** — transcription locale (coût ≈ 0) + modèles propriétaires à terme → réduction des coûts variables, marge qui s'améliore avec l'échelle.

---

## 5. Posture non‑médicale (opposable à toute sortie IA)

- Pas de diagnostic, pronostic, prescription, décision clinique.
- Triade obligatoire orientée client : **Observation → Hypothèse → Orientation**.
- Détection d'urgence (suicidaire, violence, mineur en danger) → **escalade humaine immédiate**, l'IA ne poursuit pas.
- Vocabulaire Loi 21 respecté (pas de « thérapie / diagnostic / traitement / guérison »).
- Toute sortie IA est **soumise à validation humaine** avant archivage/diffusion.

---

## 6. Sécurité & conformité

- Secrets hors code (`.env.prod`, jamais commité).
- Auth par JWT via le backend ; le frontend ne signe pas de tokens.
- Sauvegarde dégradable (locale gratuite, ou chiffrée AES‑256 + copie hors‑site OVH Québec selon configuration) — `deploy/backup.sh`, `docs/ops-sauvegarde.md`.
- Rôles : admin > superviseur > praticien > client (cumul de drapeau `is_platform_admin` possible).

---

## 7. Références

- Doctrine : `00_DOCTRINE/` · `CLAUDE.md`
- Backend : `10_backend_merlin_api/`
- Frontend public : `ivia_site_v2/`
- Ops Docker : `docs/ops-docker-compose.md`
- Prompts : `11_PROMPTS/` · Évaluations : `managed_agents/evals.registry.yaml`
- Plan d'affaires : `12_JURIDIQUE_AFFAIRES/IVIA_BP_FINANCEMENT_v2.4.md`

---

*Au sein de l'être — En actes.*
*Architecture v1.0 — 25 juin 2026 — David Phaneuf*

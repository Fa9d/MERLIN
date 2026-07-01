---
titre: Journal — Audit des routes (Phase 0, campagne « version propre et saine »)
id: JOURNAL-AUDIT-ROUTES-20260701
type: journal
couche: SYSTEME
date: 2026-07-01
auteur: fondateur + Claude Code (COS)
---

# Journal — Carte des routes (Phase 0) — 2026-07-01

> Livrable de la Phase 0 (audit) de la campagne de mise au propre. Inventaire **structurel** +
> états connus. L'état « sain/cassé » de chaque route se **teste** en Phase 2 (backend = DB + QA ;
> frontend = liens/JS + rendu).

## 1. Backend — API FastAPI (~35 routers, ~155 endpoints)

| Groupe | Routers | État |
|---|---|---|
| Auth / comptes | auth, register, verify_email | 🟢 (verify_email : 1 déprécié) |
| Client / moi | clients, client_entitlements, me_journal, me_recordings, me_documents | 🟢 à tester |
| Journal / vie | client_journal_entries, client_life_events, era_contexts, session_temporal_anchors | 🟢 à tester |
| Audio / séances | audio_recordings, audio_sessions, sessions, session_notes, express | ⚠️ **sessions.py : 4× `410 Gone`** (LiveKit retiré — mortes *volontaires*) |
| Profilage / matching | profiling, praticiens, matching | 🟢 (profiling : Jung 0040 à appliquer, non exposé) |
| Réservation / paiement | bookings, schedules, payments | 🟢 à tester |
| Admin | admin_accounts, admin_settings, admin_accounting, admin_overview, admin_clients | 🟢 à tester |
| Entrée publique | public_intake (1 déprécié), consents, intake_requests, derived_documents | 🟢 à tester |
| Référentiels | referentiels | 🟢 |
| Santé | health | 🟢 |

**🟠 Orphelin** : `organization_leads.py` (1 endpoint) **n'est PAS monté** dans `main.py`
→ décision Phase 1 : **le monter** (canal B2B GROWTH ?) **ou le supprimer**.

## 2. Frontend — ivia_site_v2 (87 pages HTML)

| Dossier | Pages | Rôle | État |
|---|---|---|---|
| **racine** | 14 | parcours public (index, rendez-vous, reserver, activer, connexion, inscription, confirmation, pourquoi, praticiens, cgu/confidentialite/mentions, verify-email, 404) | 🟡 **index = wip d'accueil non tranché** ; liens/JS à re-tester |
| client/ | 17 | espace client connecté | ⚪ à auditer |
| praticien/ | 19 | espace praticien | ⚪ à auditer |
| admin/ | 2 | console admin | ⚪ à auditer |
| checkout/ | 3 | paiement | ⚪ à auditer |
| ressources/ | 19 | les articles (empathie, autonomie…) | 🟢 |
| design-system/ | 10 | **docs internes** | 🟠 servies au public ? → sortir du site public |
| `_proto/` | protos | maquettes de travail | 🟠 à retirer (Phase 4) |

## 3. Décisions qui émergent pour la Phase 1 (STRAT)
- [ ] `organization_leads` : monter ou supprimer.
- [ ] `design-system/` : hors du site public.
- [ ] **wip d'accueil** (`index.html`) : finir ou jeter (cf. discours COMM v1.0).
- [ ] Divergence **prod ↔ git** (prod = refonte@a2903c5, 24 juin ; local en avance) à réconcilier (Lot 2).
- [ ] `sessions.py` 410 : garder tel quel (mortes assumées) ou supprimer les stubs.

## 4. Phase 2 — ce qui devra être testé (pas testable ici)
- Backend : `alembic upgrade head` (Jung 0040) puis tests QA de chaque endpoint (nécessite la DB).
- Frontend : audit liens + JS + rendu de chaque page ; cohérence avec le discours/design.

## Historique
| Date | Auteur | Nature |
|---|---|---|
| 2026-07-01 | fondateur + Claude Code (COS) | Phase 0 — carte des routes (backend + frontend) |

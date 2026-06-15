# Carte d'état des outils IVIA — base du benchmark

> Snapshot 2026-06-15. Régénérer le tableau frontend : `python docs/site-audits/etat_des_outils.py`
> Légende — **RÉEL** : branché API sans mock · **MIXTE** : API + repli mock · **FICTIF** : mock seulement · **STATIQUE** : contenu/placeholder sans donnée dynamique.

Cette carte sert de référence pour « tout connecter au réel » et de socle au benchmark
(qualité/sécurité via les suites d'éval, voir §4).

## 1. Frontend — `ivia_site_v2/` (41 pages)

**RÉEL 12 · MIXTE 2 · FICTIF 8 · STATIQUE 19**

### Espace client — l'essentiel est réel
| Page | État | API réelle | Mock restant |
|------|------|-----------|--------------|
| `connexion.html` | RÉEL | apiLogin | — |
| `inscription.html` | RÉEL | apiRegisterClient | — |
| `verify-email.html` | RÉEL | apiVerifyEmail | — |
| `reserver.html` | RÉEL | listPraticiens, getAvailableSlots, holdSlot, bookingCheckout, pilotBook | — |
| `client/dashboard.html` | RÉEL | apiMe, getMyBookings, getMyJournal | — |
| `client/compte.html` | RÉEL | apiMe, apiSetPassword | — |
| `client/journal.html` | RÉEL | getMyJournal, createMyJournalEntry | — |
| `client/seances.html` | RÉEL | getMyBookings, cancelSlot | — |
| `client/enregistrement.html` | RÉEL | uploadMyRecording | — |
| `client/mes-enregistrements.html` | RÉEL | getMyRecordings | — |
| `client/seance-express-join.html` | RÉEL | getExpressSession, uploadExpressRecording | — |
| `client/audio-resume.html` | **FICTIF** | — | getMockSeances |
| `client/ma-progression.html` | **FICTIF** | — | getMockProgression, getMockJalons |
| `client/carte-de-vie.html` | STATIQUE | — | (placeholder « Bientôt ») |

### Espace praticien — le grand chantier (presque tout fictif)
| Page | État | API réelle | Mock restant |
|------|------|-----------|--------------|
| `praticien/seance-express.html` | RÉEL | createExpressSession | — |
| `praticien/profil.html` | MIXTE | getMySchedule, createScheduleBlock, deleteScheduleBlock | getMockPratUser (infos publiques) |
| `praticien/agenda.html` | MIXTE | getAvailableSlots | getMockAgendaSlots (repli) |
| `praticien/dashboard.html` | **FICTIF** | — | getMockPratStats, getMockClients, getMockLivraisons |
| `praticien/livraisons.html` | **FICTIF** | — | getMockLivraisons |
| `praticien/seance-en-cours.html` | **FICTIF** | — | getMockClients, getMockCompteRendus, getMockPratUser |
| `praticien/analyse-seance.html` | **FICTIF** | — | getMockPratUser |
| `praticien/compte-rendu-seance.html` | **FICTIF** | — | getMockCompteRendu, getMockPratUser |
| `praticien/compte.html` | **FICTIF** | — | getMockPratUser |
| `praticien/clients-journal.html` | STATIQUE | — | (à câbler) |
| `praticien/fiche.html` | STATIQUE | — | (à câbler) |
| `praticien/carte-de-vie-demo.html` | STATIQUE | — | démo doctrine (données fictives assumées) |

### Pages de contenu (STATIQUE — normal, pas de données)
`index.html`, `pourquoi.html`, `confidentialite.html`, `cgu.html`, `mentions.html`,
`rendez-vous.html`, `confirmation.html`, `404.html`, `checkout/success|cancel.html`,
`client/{seance,seance-active,premier-ancrage,journal-nouvelle-entree,mot-de-passe-oublie}.html`.

## 2. Backend — `10_backend_merlin_api/` (réel, déployé, head migration `20260615_0029`)

Routers montés (`app/main.py`) : `auth`, `clients`, `client_entitlements`, `client_life_events`,
`client_journal_entries`, `me_journal`, `me_recordings`, `express`, `era_contexts`,
`intake_requests`, `consents`, `derived_documents`, `praticiens`, `referentiels`,
`public_intake`, `sessions`, `session_notes`, `session_temporal_anchors`, `audio_recordings`,
`audio_sessions`, `bookings`, `schedules`, `matching`, `register`, `verify_email`,
`organization_leads`, `payments`, `health`.

**Pipeline d'analyse IA** : `app/services/livekit_audio.py:run_post_recording_pipeline`
→ transcription (faster-whisper) → `app/ai/anthropic_session_note_pipeline` → note structurée
(production / client_delivery / supervision / research) + `transcript_text` persisté.
Déclenché après chaque enregistrement (solo, express). **Non encore exposé dans l'UI praticien.**

## 3. Écart principal pour « connecter au réel »

1. **Espace praticien** (8 pages FICTIF) — surtout : `dashboard`, `livraisons`,
   `seance-en-cours`, `analyse-seance`, `compte-rendu-seance`. C'est là que doit apparaître
   le résultat du pipeline d'analyse (les vrais entretiens enregistrés).
2. **Client** : `audio-resume` et `ma-progression` encore fictifs.
3. **Profil praticien** : infos publiques encore mock (les disponibilités sont réelles).

## 4. Benchmark qualité / sécurité (existant, à activer)

- `managed_agents/evals/safety_suite_v1.yaml` — 10 catégories obligatoires ≥ 0.85
  (non-prescription, frontière diagnostic, escalade urgence, neutralité Québec,
  savoirs autochtones, psychédéliques recherche, suppléments, périmètre praticien,
  données Québec, anti-sycophantie).
- Suites Telescope : `make telescope-note-e2e`, `make telescope-minimal`.
- Registre : `managed_agents/evals.registry.yaml`.

→ Le « benchmark de tous nos outils » = (a) cette carte d'état tenue à jour +
(b) un vrai entretien passé dans le pipeline + (c) les suites d'éval vertes sur cas réels.

## 5. Régénérer

```bash
python docs/site-audits/etat_des_outils.py     # tableau frontend réel/mock
python docs/site-audits/audit_liens.py         # 0 lien cassé
python docs/site-audits/audit_js.py            # fonctions appelées vs incluses
```

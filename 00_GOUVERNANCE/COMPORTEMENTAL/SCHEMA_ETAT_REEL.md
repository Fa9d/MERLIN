# MERLIN — Carte d'état réel du schéma PostgreSQL
**Généré le :** 29 juin 2026  
**Source :** `10_backend_merlin_api/app/models/` + migrations `0001–0027`  
**Head Alembic actuel :** `20260504_0017` (confirmé par Claude Code)

---

## ✅ Chaîne Alembic — état sain

Un seul head : `20260504_0017_add_request_channel_code_enum.py`  
Toute nouvelle migration part de ce head.

---

## Tables existantes — état complet

### `app_users`
Utilisateurs de la plateforme (praticiens + clients avec compte).

Champs clés : `email`, `password_hash`, `display_name`, `legal_name`, `role` (AppRole enum), `record_status`, `spoken_languages`, `email_verified_at`

---

### `clients`
Profil client (peut exister sans compte `app_users`).

Champs clés : `public_client_code`, `first_name_or_alias`, `email`, `phone`, `app_user_id` (FK nullable), `language_code`, `timezone`, `record_status`

Relations : → `sessions`, `intake_requests`, `consents`, `client_life_events`, `client_journal_entries`, `client_entitlements`, `payment_orders`

---

### `practitioner_profiles`
Profil praticien — **matching existant basé sur ce modèle**.

Champs clés : `user_id` (FK → app_users), `public_visible`, `accepting_clients`, `actif`  
Champs matching existants (ajoutés via migrations) : `domaines` (JSON), `approches` (JSON), `langues` (JSON), `disponibilites` (JSON)

⚠️ **Zone d'extension** : les champs comportementaux (Big Five, Schwartz, LEARY) seront ajoutés ici ou dans une table liée `profil_comportemental`.

---

### `sessions`
Séances entre praticien et client.

Champs clés : `client_id`, `intake_request_id`, `session_sequence_number`, `session_mode_code`, `session_channel_code`, `scheduled_start_at`, `actual_start_at`, `actual_end_at`, `praticien_id` (FK → app_users)

---

### `session_notes`
Notes structurées de séance — **principale source pour l'analyse comportementale NLP**.

Champs clés : `session_id`, `client_id`, `summary_text`, `observations_text`, `coeur_summary_text`, `axes_scores` (JSON — axes MERLIN existants), `risk_level_code`, `context_summary_text`, `hypotheses` (JSON)

⚠️ **Zone d'extension** : ajouter `big_five_scores` (JSON) et `leary_position` (JSON) via migration.

---

### `derived_documents`
Documents générés depuis les notes (rapports, synthèses).

Champs clés : `session_id`, `source_note_id`, `document_kind_code`, `audience_code` (praticien/client), `body_text`, `client_visible`

---

### `audio_sessions`
Sessions audio LiveKit.

Champs clés : `session_id` (FK), `room_name`, `recording_enabled`, `audio_session_status_code`

---

### `audio_recordings`
Enregistrements audio — **source pour la prosodie vocale**.

Champs clés : `audio_session_id` (FK), `provider_code`, `audio_recording_status_code`, `output_location`, `requested_by_user_id`

---

### `intake_requests`
Demandes d'admission — **source pour Schwartz Values et Ternary Plot**.

Champs clés : `client_id`, `request_channel_code`, `primary_need_code`, `perceived_urgency_code`, `requested_outcome_text`, `entry_summary_text`, `langues` (JSON), `domaines` (JSON), `approches` (JSON)

---

### `consents`
Consentements granulaires — **à étendre pour les analyses comportementales**.

Champs clés : `client_id`, `session_id`, `consent_type_code`, `consent_value`, `consent_version_code`

⚠️ **Action requise** : ajouter `consent_type_code` = `BEHAVIORAL_ANALYSIS` dans l'enum ConsentTypeCode.

---

### `client_life_events`
Événements de vie du client — **source pour Jungien et Enneagramme**.

Champs clés : `client_id`, `era_tag`, `life_stage`, `family_role`, `event_year_approx`, `significance_score`

---

### `client_journal_entries`
Journal client — **source textuelle secondaire pour NLP Big Five**.

Champs clés : `client_id`, `entry_type`, `body_text`, `emotional_tone`, `event_year_ref`

---

### `session_temporal_anchors`
Ancres temporelles extraites des séances — **source pour heatmap longitudinale**.

Champs clés : `session_id`, `session_note_id`, `client_id`, `life_event_id`, `verbatim_fragment`, `said_at_offset_sec`, `event_year_approx`, `temporal_model_code`

---

### `payment_orders` / `client_entitlements`
Paiements et droits — **source pour calcul LTV et ROI des modèles**.

---

### `booking_slots` / `practitioner_schedules` / `schedule_exceptions`
Disponibilités praticien — utilisées dans le matching actuel (critère `dispo`).

---

### `era_contexts`
Contextes d'époque (territorial, historique) — pertinent pour l'ancrage culturel québécois/autochtone.

---

## Service matching existant — état actuel

**Fichier :** `10_backend_merlin_api/app/services/matching.py`

**Algorithme actuel :** scoring pondéré sur 4 critères discrets
```python
WEIGHTS = {"domaine": 3, "approche": 2, "langue": 3, "dispo": 1}
```

**Ce qui manque pour le matching comportemental :**
- Vecteurs Big Five, Schwartz, LEARY dans `practitioner_profiles`
- Même vecteurs dans un profil client (à construire depuis `session_notes` + `intake_requests`)
- Cosine similarity sur ces vecteurs en complément du scoring pondéré actuel

---

## Nouvelles tables à créer

> Aucune de ces tables n'existe encore. Toutes partent du head `0017`.

| Table | Contenu | Migration |
|---|---|---|
| `profil_comportemental` | Vecteur comportemental par user (Big Five, Schwartz, LEARY, Ternary) | Post-0017 |
| `veille_configs` | Configuration des 10 domaines de veille (OFF par défaut) | Post-0017 |
| `veille_digests` | Résultats de veille stockés par domaine | Post-0017 |

---

## Champs à ajouter à des tables existantes

| Table | Champs à ajouter | Type | Migration |
|---|---|---|---|
| `session_notes` | `big_five_scores` | JSON nullable | Post-0017 |
| `session_notes` | `leary_position` | JSON nullable | Post-0017 |
| `practitioner_profiles` | `big_five_scores`, `schwartz_values`, `leary_position`, `ternary_values` | JSON nullable | Post-0017 |
| `consents` | Nouveau `consent_type_code` = `BEHAVIORAL_ANALYSIS` | Enum extension | Post-0017 |

---

## Routers existants

| Dossier/fichier | Fonction |
|---|---|
| `app/api/routes/` | Routes API principales |
| `app/services/matching.py` | Matching praticien-client (à étendre) |
| `app/services/intake_analysis.py` | Analyse des demandes d'admission |
| `app/services/transcription.py` | Transcription audio |
| `app/services/session_documents.py` | Documents de séance |
| `app/ai/anthropic_session_note_pipeline.py` | Pipeline IA existant (à étendre pour Big Five) |

**Nouveaux services à créer :**
- `app/services/behavioral_profile.py` — construction et mise à jour des profils comportementaux
- `app/services/veille.py` — module de veille admin

---

## Ordre d'implémentation recommandé pour Claude Code

```
1. Migration post-0017 :
   → Ajouter big_five_scores + leary_position dans session_notes
   → Ajouter big_five_scores + schwartz_values + leary_position + ternary_values dans practitioner_profiles
   → Créer table profil_comportemental

2. Extension app/services/matching.py :
   → Ajouter cosine similarity sur vecteurs comportementaux
   → Conserver le scoring pondéré existant (ne pas casser)
   → Score final = WEIGHTS existants + bonus cosine si vecteurs disponibles

3. Extension app/ai/anthropic_session_note_pipeline.py :
   → Ajouter extraction Big Five (JSON structuré) depuis observations_text
   → Ajouter position LEARY depuis dynamique relationnelle
   → Stocker dans session_notes.big_five_scores + session_notes.leary_position

4. Nouveau service app/services/behavioral_profile.py :
   → Agrégation des scores Big Five par client (moyenne pondérée sur N séances)
   → Construction du vecteur Ternary (Autonomie/Lien/Structure) depuis intake_requests
   → Mise à jour automatique de profil_comportemental après chaque session_note

5. Composants frontend (09_app_ivia_merlin) :
   → RadarProfile.tsx — 8 axes (Big Five + 3 valeurs IVIA)
   → TernaryPlot.tsx — triangle SVG (Autonomie / Lien / Structure)
   → LearyCircumplex.tsx — rosace 8 octants
   → Intégration dans la vue séance (onglet "Profil comportemental")
   → Intégration dans le dashboard praticien

6. Migration post-0017 (lot 2) :
   → Créer tables veille_configs + veille_digests

7. Nouveau service app/services/veille.py :
   → 10 domaines préconfigurés
   → Appel Perplexity API par domaine
   → Scoring pertinence MERLIN via Anthropic haiku
   → Stockage digest

8. Route admin veille :
   → GET /admin/veille/config
   → PATCH /admin/veille/config/{domaine}
   → POST /admin/veille/run/{domaine}
   → GET /admin/veille/digests

9. Dashboard rentabilité admin :
   → Coûts par modèle (CR hardcodé par modèle)
   → Nb séances avec modèle actif ce mois
   → ROI estimé par modèle
```

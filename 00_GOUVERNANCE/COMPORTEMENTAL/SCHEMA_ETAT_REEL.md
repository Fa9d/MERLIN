# MERLIN — Carte d'état réel du schéma (référence d'implémentation)

**Réécrit le :** 29 juin 2026 — **sur la branche canonique `refonte-ivia-site-unifie`**
**Source :** `10_backend_merlin_api/app/models/` (20 modèles) + 41 migrations
**Head Alembic réel :** **`20260625_0039`** (vérifié `alembic heads`) — *et non `0017`*

> ⛔ **Remplace la version périmée** (générée par Perplexity sur `master`, head 0017, qui
> proposait de créer des tables `profil_comportemental` **déjà existantes**). Toute nouvelle
> migration part de **`0039`**. Règle dure : **on étend l'existant, on ne le duplique pas.**

---

## 0. Le module comportemental EXISTE DÉJÀ (ne pas recréer)

| Brique | Fichier | État |
|---|---|---|
| Modèle 5 couches (OCEAN, Schwartz, 8 Expressions, Bartholomew, VAD) | `app/models/behavioral_profile.py` | ✅ append-only versionné, sujet polymorphe client/praticien, lien consentement, sensibilité `high` |
| Migration des tables | `alembic/versions/20260625_0039_…` | ✅ appliquée à la chaîne (head) |
| Matching | `app/services/profile_matching.py` | ✅ cosine + euclidienne pondérée, similarité/complémentarité, 0–100 + explication |
| Quiz 8 Expressions | `app/services/love_quiz.py` | ✅ adaptatif IRT, scoring + biais |
| Insights LLM | `app/services/behavioral_insights.py` | ✅ gated (`insights_enabled=False`), fallback, post-filtre Loi 21 |
| Vue radar | `ivia_site_v2/shared/profile-radar.js` (`<ivia-profile-radar>`) | ✅ web component statique |
| Routes | `app/api/routes/profiling.py` | ✅ câblées, **non exposées client** (B2/B3/B4) |

**Barrière safety/sécurité (ne pas franchir sans levée) :** B1 (cadre transfrontalier + consentement
avant Anthropic réel), B2 (consentement obligatoire à l'écriture), B3 (surface client sans scores),
B4 (post-filtre Loi 21 + triage urgence). Suite : `managed_agents/evals/profiling_safety_suite_v1.yaml`.
Revue : `05_PREUVES_SOURCES/SECURITY_REVIEW_PROFILAGE_v1.0.md`.

---

## 1. Tables réelles (20 modèles ORM)

`app_settings` · `app_users` · `audio_recordings` · `audio_sessions` · **`behavioral_profile`
(5 tables : ocean/schwartz/love/attachment/vad)** · `clients` · `client_entitlements` ·
`client_journal_entries` · `client_life_events` · `consents` · `derived_documents` ·
`era_contexts` · `intake_requests` · `payment_orders` · `practitioner_profiles` · `schedules` ·
`sessions` · `session_notes` · `session_temporal_anchors`
*(+ `enums.py` : énumérations métier, pas une table.)*

### Sources de données pour les modèles comportementaux (réutiliser, ne pas dupliquer)
- **`behavioral_profile`** — scores par couche, versionnés. **C'est ICI** que vivent OCEAN/Schwartz/
  Amour/Bartholomew/VAD. Toute nouvelle dimension = colonne/couche ici, pas une table parallèle.
- **`session_notes`** — `axes_scores` (axes MERLIN), `hypotheses`, `observations_text` : matière NLP.
- **`audio_recordings`** — source prosodie (transcription faster-whisper locale).
- **`intake_requests`** — `primary_need_code` : entrée du mapping besoin → domaine de matching.
- **`practitioner_profiles`** — profil praticien ; champs matching existants (`domaines`, `approches`,
  `langues`, `disponibilites`). *(Cf. intention « carte abstraite/persona » : voir
  `05_PREUVES_SOURCES/SALVAGE_CLONE_MERLIN_MATCHING_PERSONA_v1.0.md`.)*
- **`consents`** — N1/N2/N3 ; **toute écriture de profil exige un `consent_id`** (B2).

---

## 2. Ordre d'implémentation CORRIGÉ (étendre l'existant)

> Pré-requis : travailler sur `refonte-ivia-site-unifie`, head `0039`. Rien n'est exposé au
> client ni n'appelle Anthropic réel tant que la barrière B1–B4 n'est pas levée + validation
> humaine clinique/Loi 21.

1. **Lire l'existant** (`behavioral_profile.py`, `profile_matching.py`, `behavioral_insights.py`,
   `profiling_safety_suite_v1.yaml`) — ne rien recréer.
2. **Appliquer `0039`** sur une base de **test** (`alembic upgrade head`) + écrire les **tests DB**
   (bascule `is_current`, `record_layer` end-to-end, routes avec session réelle).
3. **N'ajouter QUE ce qui manque**, par migration > `0039` (jamais une table parallèle) :
   éventuels champs « carte abstraite/persona » sur `practitioner_profiles` (cf. salvage),
   mapping `NeedCode → Domaine` (déjà esquissé), vues ternary/Leary (en statique vanilla).
4. **Garder la barrière** : profilage/insights restent gated ; XAI (explication par score) obligatoire.
5. **Veille / ROI** (doc d'intention) : tout connecteur externe (Perplexity API…) = **egress
   transfrontalier** → à cadrer Loi 25 d'abord, ou hors-périmètre.

---

## 3. Références
- `ADR-0006` (stack), `ADR-0007` (dépôt + branche canoniques)
- `00_GOUVERNANCE/IVIA_SPEC_TECHNIQUE_CANONIQUE_v1.0.md`
- `MERLIN_modeles_comportementaux_v1.md` (intention, même dossier)
- `05_PREUVES_SOURCES/SECURITY_REVIEW_PROFILAGE_v1.0.md` · `SALVAGE_CLONE_MERLIN_MATCHING_PERSONA_v1.0.md`

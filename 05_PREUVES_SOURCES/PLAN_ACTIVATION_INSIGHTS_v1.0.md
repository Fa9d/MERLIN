# Plan d'activation — Insights LLM (Prompt 5)

**Version** : 1.0 — 2026-06-26
**Statut** : patchs réalisés et testés (offline) — **activation NON faite** (flag `insights_enabled=False`).
**Lié à** : `SECURITY_REVIEW_PROFILAGE_v1.0.md` (B1), `profiling_safety_suite_v1.yaml`.

> Aucun déploiement, aucune migration, aucun appel Anthropic réel déclenché par ce plan.

---

## 1. Intégration contrôlée (fait)
- L'appel réel reste piloté par **`settings.insights_enabled`** (défaut **False**) côté route
  (`/profiling/insights/generate`). Tant que False → l'entrée est préparée, **aucun appel**.
- Modèle/limites configurables : `MERLIN_INSIGHTS_MODEL` (défaut `claude-sonnet-4-6`),
  `MERLIN_INSIGHTS_MAX_TOKENS` (1100), `MERLIN_INSIGHTS_DAILY_CAP` (200).

## 2. Gestion des secrets (fait)
- `ANTHROPIC_API_KEY` lue depuis `settings`/`.env.prod`, **jamais en dur**, **jamais journalisée**
  ni renvoyée. Header `x-api-key` non loggé.
- À faire avant activation : **rotation** de clé, et idéalement un cadre **non‑rétention / DPA**
  Anthropic (lié à B1, transfrontalier).

## 3. Fallback en cas d'échec (fait)
- `generate_with_fallback` ne lève **jamais** : sur échec API / réponse non conforme / plafond →
  renvoie une **dégradation sûre** (`_FALLBACK`) avec `degraded=True` + `reason`.
- `_call_claude` : **retry** unique sur erreurs transitoires (429/5xx/réseau) + timeout borné.

## 4. Journalisation (fait)
- Succès : `model`, `input_tokens`, `output_tokens`, **coût estimé** — **jamais** le contenu ni le profil.
- Incidents : post‑filtre Loi 21 déclenché (formulation interdite du LLM), dégradations (raison).
- À faire : exporter ces logs vers le monitoring (Dozzle déjà en place ; alerte sur taux de dégradation).

## 5. Garde‑fous de formulation (fait — critique)
- **Post‑filtre déterministe Loi 21** (`loi21_filter`) appliqué à `resume_client` (sortie client) :
  si une formulation interdite passe le LLM → **refus** + journalisation + fallback.
- Le prompt `PROD-PROF-002` impose déjà la triade + le vocabulaire interdit ; le post‑filtre est le
  **filet de sécurité hors LLM**.

## 6. Limites de coûts & monitoring
- **Borne `max_tokens`** par appel + **plafond souple d'appels/jour** (mémoire process).
  ⚠️ Compteur **non persistant** (par process) → pour un vrai garde‑fou multi‑worker, **persister**
  (Redis/DB) — recommandé avant montée en charge.
- Estimation de coût par appel (tarifs indicatifs) journalisée → base d'un suivi budgétaire.
- À faire : tableau de bord coût/jour + alerte de seuil.

## 7. Checklist d'activation (à exécuter le moment venu — ordre)
1. **B1 levé** : cadre transfrontalier Anthropic (non‑rétention/DPA) + consentement N3 documentés.
2. **Safety eval** `profiling_safety_suite_v1` validée par une personne qualifiée (clinique/Loi 21).
3. Migration `0039` appliquée (tables de profils existent).
4. Câblage validé (B2/B3 actifs, permissions, journalisation).
5. Secret en place + rotation + (idéalement) compteur de coût persistant.
6. Mettre `MERLIN_INSIGHTS_ENABLED=true` **en dernier**, puis surveiller le taux de dégradation/coût.

## 8. Fichiers (patchs de ce Prompt 5)
- `app/services/behavioral_insights.py` — post‑filtre, fallback, retry, usage/coût, cap, modèle configurable.
- `app/api/routes/profiling.py` — route insights via `generate_with_fallback`.
- `app/core/config.py` — `insights_model`, `insights_max_tokens`, `insights_daily_cap`.
- `tests/test_behavioral_insights.py` — nominal, post‑filtre, fallback, cap, coût (8 tests offline).

## 9. Non fait (volontaire)
- `insights_enabled` reste **False** ; aucun appel Anthropic réel ; aucun déploiement ; aucune migration.

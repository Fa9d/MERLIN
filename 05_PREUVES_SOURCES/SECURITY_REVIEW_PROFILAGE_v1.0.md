# SECURITY REVIEW — Bloc profilage / matching / insights

**Version** : 1.0
**Date** : 2026-06-25
**Auteur** : Claude Code (audit) — à contre‑valider par un·e responsable humain·e
**Périmètre** : `app/models/behavioral_profile.py`, `app/schemas/behavioral_profile.py`,
`app/services/{profile_matching,love_quiz,behavioral_insights}.py`, prompts
`11_PROMPTS/06_profilage/`, vue `ClientFacingProfileView`, composant `ProfileRadar.tsx`.
**Barrière amont** : `managed_agents/evals/profiling_safety_suite_v1.yaml`.
**Contraintes** : aucun déploiement, aucune migration prod, aucun câblage dans cette revue.

> Échelle de sévérité : **BLOQUANT** (absolu) · **CRITIQUE** · **ÉLEVÉ** · **MOYEN** · **FAIBLE**.

---

## 0. Constats de base (vérifiés)
- ✅ **Aucune route n'importe le bloc** → **surface d'exposition actuelle = nulle**.
- ✅ **Migration `0039` non appliquée** → tables inexistantes en prod.
- ✅ Payload envoyé à Anthropic = **scores + `fiabilite` uniquement**, **aucun PII** (ni `client_id`, ni nom, ni courriel).
- ⚠️ `consent_id` **nullable** → le consentement n'est pas forcé au niveau base.
- ✅ `ANTHROPIC_API_KEY` lue depuis `settings`/`.env.prod`, **jamais en dur**.

---

## 1. Risques par axe (classés par sévérité)

### 1.1 Sécurité des données
- **F‑DATA‑1 — BLOQUANT.** L'appel `behavioral_insights → api.anthropic.com` réalise un
  **traitement transfrontalier (hors Québec/Canada)** de **données comportementales sensibles**.
  Même sans identifiant, un profil 5 couches est une **donnée personnelle** (Loi 25). Atténuation
  présente : aucun PII dans le payload. Manque : **consentement explicite (N3)**, **cadre
  contractuel Anthropic** (entente de traitement / non‑rétention), notice.
- **F‑DATA‑2 — CRITIQUE.** `consent_id` nullable → une écriture de profil **sans consentement**
  est possible. À rendre **obligatoire au service** d'écriture (refus sinon).
- **F‑DATA‑3 — ÉLEVÉ.** `raw_payload` (réponses brutes du quiz) = sensible. Prévoir
  **chiffrement au repos** / politique de **rétention + effacement** (`data_sensitivity_class=high`
  et `ondelete=CASCADE` déjà en place — bons appuis).

### 1.2 Confidentialité
- **F‑CONF‑1 — CRITIQUE.** Garantir **structurellement** que toute surface client ne sérialise que
  `ClientFacingProfileView` (jamais les `*Read` avec scores). À verrouiller par code + **test de
  non‑régression**.
- **F‑CONF‑2 — MOYEN.** Les logs ne doivent **jamais** contenir scores bruts / `raw_payload` en clair.

### 1.3 Sécurité applicative & routes
- **F‑APP‑1 — ÉLEVÉ (futur).** À l'écriture des routes : **auth par rôle** via `app/core/deps.py`
  (jamais inline), validation Pydantic (déjà prête), **rate‑limit** sur quiz/insights, garde
  « client ≠ scores ». *Aucune route n'existe encore → risque uniquement à venir.*

### 1.4 Surface d'exposition
- **F‑EXP‑1 — MOYEN.** `ProfileRadar` vit dans le **Next.js legacy non servi** → pas d'exposition
  front actuelle. Le jour de l'exposition : portage maîtrisé (Prompt 4).

### 1.5 Journalisation
- **F‑LOG‑1 — ÉLEVÉ.** **Aucune journalisation** des événements critiques (création profil,
  référence de consentement, génération d'insight, escalade d'urgence). À ajouter au câblage —
  tracer *qui / quand / consent_id / type d'événement*, **pas** les valeurs/scores.

### 1.6 Permissions
- **F‑PERM‑1 — CRITIQUE (futur).** Matrice à définir : écriture (praticien/admin + auto‑quiz client),
  lecture des scores (praticien/superviseur/admin), client = **vue restituée seulement**. Non implémenté.

### 1.7 Gestion des secrets (ANTHROPIC_API_KEY)
- **F‑SEC‑1 — MOYEN.** Clé hors code, envoyée en header `x-api-key` (TLS) — standard. Vérifier
  qu'**aucun log** ne dump les headers ; prévoir **rotation**.
- **F‑SEC‑2 — ÉLEVÉ.** Aucun **fallback**, **cap de coût/quota** ni monitoring sur l'appel insights
  → risque d'abus / dérive de coût (à traiter au Prompt 5).

### 1.8 Surinterprétation produit
- **F‑PROD‑1 — ÉLEVÉ.** Score 0‑100 et insights lisibles comme **verdict/prédiction**. Couvert par
  `profiling_safety_suite_v1`, mais exige un **post‑filtre déterministe** (anti‑termes Loi 21) +
  une UI prudente + le triage d'urgence des champs libres **avant** tout scoring. Non implémenté.

### 1.9 Dépendances bloquantes
- ✅ `numpy` présent ; `sklearn` non requis ; `recharts` non requis (radar SVG natif).
- ⏸️ Migration `0039` à appliquer — **après** la barrière.
- ⏸️ **Validation humaine** clinique / Loi 21 de la safety eval — avant exposition client.

---

## 2. Blocants absolus (avant toute exposition client / appel Anthropic réel)
- **B1 (F‑DATA‑1)** — Pas d'appel Anthropic sur **données client réelles** sans cadre transfrontalier
  + consentement N3.
- **B2 (F‑DATA‑2 / F‑PERM‑1)** — Écriture de profil **sans consentement** = interdite (`consent_id`
  obligatoire au service).
- **B3 (F‑CONF‑1)** — Surface client = `ClientFacingProfileView` **uniquement** (jamais de score),
  garanti par code + test.
- **B4 (F‑PROD‑1 + safety eval)** — Post‑filtre déterministe anti‑Loi 21 **et** triage d'urgence des
  champs libres **avant** scoring/insight/exposition.

## 3. Correctifs OBLIGATOIRES avant exposition
1. Implémenter B2 (consentement obligatoire) et B3 (surface client verrouillée + test).
2. Journalisation des événements critiques sans valeurs sensibles (F‑LOG‑1).
3. Matrice de permissions appliquée via `deps.py` (F‑PERM‑1, F‑APP‑1).
4. Post‑filtre Loi 21 + triage urgence avant toute sortie (B4).
5. Cadre transfrontalier + consentement avant tout appel Anthropic réel (B1).

## 4. Correctifs RECOMMANDÉS
- Chiffrement au repos de `raw_payload` + politique de rétention explicite (F‑DATA‑3).
- Rate‑limit + cap de coût + monitoring sur insights (F‑SEC‑2).
- Rotation de clé + vérif anti‑dump des headers (F‑SEC‑1).
- Notice/UX de prudence sur les scores (anti‑surinterprétation).

---

## 5. VERDICT
- **Câblage interne (Prompt 3)** — *sans exposition publique, sans appel Anthropic réel, sans
  migration prod* : **✅ PRÊT à préparer**, à condition d'implémenter **B2** (consentement) et **B3**
  (surface client) + la journalisation **dans** le câblage lui‑même.
- **Exposition client / appel Anthropic réel / migration prod** : **⛔ NON PRÊT** tant que **B1–B4**
  ne sont pas faits **et** qu'une **validation humaine clinique / Loi 21** n'a pas signé.

> En clair : on peut **préparer le câblage** (étape suivante) en y intégrant les blocants B2/B3 et la
> journalisation, mais **rien ne s'allume côté client ni côté Anthropic** avant B1–B4 + signature humaine.

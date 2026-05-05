---
titre: Plan de validation technique MERLIN/IVIA — Cartographie du moteur
id: PROD-VALID-001
statut: active
type: audit
couche: PROD
périmètre: moteur backend + prompts critiques + tests
auteur: fondateur
date: 2026-05-05
version: 1.0
dépend_de: [ADR-0002, MERLIN-AUDIT-PROMPTS-V1]
remplace: []
arbitrage_requis: non — rapport d'état
source_canonique: 11_PROMPTS/PROD-VALID-001-CARTOGRAPHIE_MOTEUR_V1.md
---

# MERLIN/IVIA — Validation technique pour finançabilité

> **Objectif** : cartographier le moteur actuel, identifier ce qui est testable, proposer un MVP démontrable
> **Audience** : fondateur + financeur technique
> **Horizon** : fin mai 2026
> **Date d'audit** : 2026-05-05

---

## SECTION 1 — Cartographie du moteur actuel

### 1.1 Structure générale

Le moteur IVIA/MERLIN est un backend FastAPI exposant un API REST en `v1` (`/v1/*`). Il gère le flux complet d'une session de santé mentale : de la prise en charge client jusqu'à la génération d'un document structuré.

**Stack technique confirmée** :
- Backend: FastAPI 0.110+ (Python 3.12)
- BDD: PostgreSQL 15 ou SQLite (développement)
- Auth: JWT + bcrypt
- IA: Anthropic Claude Sonnet 4 (2025-05-14)
- Temps réel: LiveKit (audio/video)
- Infrastructure: Nginx 1.27, uvicorn

### 1.2 Modules de base (app/)

| Module | Rôle | État |
|---|---|---|
| `api/routes/` | 15 routeurs REST | ✅ Actif |
| `models/` | 11 entités Doctrine ORM | ✅ Schémas stables |
| `schemas/` | Validateurs Pydantic | ✅ Validations strictes |
| `services/` | Logique métier isolée | ✅ Testable |
| `ai/` | Pipeline IA Anthropic | ✅ Moteur critique |
| `db/` | Couche BDD | ✅ Alembic actif |
| `core/` | Config + authentification | ✅ Robuste |

### 1.3 Routes API actives (v1)

**Cœur du flux métier (7 routes critiques)** :

| Endpoint | Méthode | Rôle | Dépendances |
|---|---|---|---|
| `/v1/clients` | POST | Créer/register client public | email + validation |
| `/v1/intake-requests` | POST | Dépôt demande (entry point) | analyse texte brut (regex) |
| `/v1/audio-sessions` | POST | Créer session (réserver room) | LiveKit API |
| `/v1/audio-recordings` | PUT | Clôturer session + récupérer audio | FileSystem ou S3 |
| `/v1/session-notes` | POST | Générer note (IA + structuration) | **Moteur Anthropic Claude** |
| `/v1/derived-documents` | POST | Générer document client | Jinja2 + templates |
| `/v1/audio-sessions/{id}` | GET | Lire état session | BDD |

**Routes de supervision (3)** :
- `POST /v1/session-notes/{id}/validate` — superviseur valide note
- `GET /v1/sessions` (list, filtrable) — vue opérateur/superviseur
- `PATCH /v1/sessions/{id}` — mise à jour état de session

**Routes administratives (5)** :
- `/v1/register` — enregistrement (client + praticien)
- `/v1/verify-email` — validation email
- `/v1/auth/login` — JWT
- `/v1/consents` — gestion consentements
- `/v1/schedules`, `/v1/praticiens` — référentiels

### 1.4 Flux critique de la session

```
PUBLIC FLOW:
  Client public
    ↓
  [POST /clients] → IntakeRequest (via demande texte libre)
    ↓
  [Analyse via intake_analysis.py] → risk/gap signals détectés
    ↓
  [POST /audio-sessions] → Réservation LiveKit (room name + tokens)
    ↓
  [Audio live] → Enregistrement on-the-fly
    ↓
  [PUT /audio-recordings?session_id=X] → Clôture + audio récupéré
    ↓
  [POST /session-notes] → MOTEUR: Anthropic Claude Sonnet 4
    ├─ Prompt: SESSION_NOTE_CERCLE_SYSTEM_PROMPT (METH-003)
    ├─ Contexte: hypothèses + signaux (METH-001, METH-002)
    └─ Output: JSON structuré (production_note, client_delivery, supervision, research, metadata)
    ↓
  [POST /derived-documents] → Document client générés depuis note
    ↓
  [Client voit résultat] via `/suivi/documents/[CODE]`

SUPERVISION FLOW:
  Superviseur voit liste sessions
    ↓
  [GET /sessions?status=pending_review]
    ↓
  [Lecture note + flags]
    ↓
  [POST /session-notes/{id}/validate?decision=approve/reject]
    ↓
  Si approve → derived_document passe en `client_visible=true`
  Si reject → retour opérateur pour correction
```

---

## SECTION 2 — Prompts critiques du moteur

### 2.1 État de l'externalisation (Vague 3 - Phase A)

**Tous les prompts critiques sont externalisés** dans `11_PROMPTS/02_METH/` depuis le 2026-05-05.

| ID | Fichier | Rôle | Couche | Modèle | Statut |
|---|---|---|---|---|---|
| METH-001 | `METH-001-quebec-context-hypotheses-v1.md` | 9 hypothèses contextuelles québécoises | METH | Sonnet 4 | ✅ Actif |
| METH-002 | `METH-002-quebec-context-signals-v1.md` | 12 signaux contextuels à détecter | METH | Sonnet 4 | ✅ Actif |
| METH-003 | `METH-003-session-note-cercle-system-prompt-v1.md` | Prompt système principal (la *persona* MERLIN) | METH | Sonnet 4 | ✅ CRITIQUE |

### 2.2 Composantes du prompt système METH-003

Le prompt système définit :
1. **Rôle** : "Tu es MERLIN, moteur documentaire d'IVIA"
2. **Grille d'analyse** : 4 dimensions (coeur/corps/esprit/etre) + contexte immédiat
3. **Contraintes absolues** :
   - ❌ Pas de diagnostic
   - ❌ Pas de traitement prescrit
   - ❌ Pas de spéculation métaphysique
   - ❌ Pas de citation de traditions autochtones (sauf contexte formel)
4. **Règles de diffusion** : ce qui va en production_note vs client_delivery vs supervision
5. **Contexte québécois** : hypothèses + signaux (injectés depuis METH-001/002)
6. **Format de sortie** : schéma JSON strictement défini

### 2.3 Chargement dynamique via prompt_loader.py

Depuis Vague 3:
- Les 3 prompts sont chargés depuis le disque via `load_prompt(prompt_id)`
- Cache mémoire simple (dict) pour éviter relecture disque répétée
- Erreur explicite `PromptNotFoundError` si fichier manquant
- Modification de prompt = modification fichier Markdown (traçable dans git)

**Impact fondateur** : les changeants au moteur IA passent désormais par `11_PROMPTS/`, pas par code Python.

### 2.4 Schéma de sortie du moteur

La note de séance générée par Claude respecte ce schéma JSON :

```
{
  "production_note": {
    "summary_text": "résumé court (~150 mots)",
    "observations_text": "lecture structurée",
    "coeur_summary_text": "dimension relationnelle/émotionnelle",
    "corps_summary_text": "dimension physique/somatique",
    "esprit_summary_text": "dimension cognitive/mentale",
    "etre_summary_text": "dimension existentielle/identitaire",
    "immediate_context_text": "environnement immédiat",
    "context_factors_json": [
      {
        "factor_family_code": "materiel|travail|logement|reseau|institutions|territoire",
        "impact_direction_code": "support|fragilite|contrainte",
        "summary_text": "..."
      }
    ],
    "context_hypotheses_json": [
      {
        "hypothesis_code": "pression_silence_et_minimisation|...",  // 9 codes possibles
        "summary_text": "...",
        "matched_signals": ["..."],
        "primary_dimension": "coeur|corps|esprit|etre",
        "confidence_code": "faible|moyen|eleve"
      }
    ],
    "identified_tensions_json": [
      {
        "tension_code": "tension_rythme|...",  // 10 codes possibles
        "description": "...",
        "dimensions_impactees": ["coeur", "corps", ...],
        "intensite_presumee": "faible|moderee|marquee",
        "niveau_de_confiance": "faible|moyen|eleve"
      }
    ],
    "vigilance_level_code": "non_urgent|watch|priority|urgent",  // CRITIQUE POUR SECURITE
    "vigilance_summary_text": "justification du niveau",
    "next_step_type_code": "continue_to_structure|clarify_major_point|stabilize_rhythm_and_load|mobilize_relational_resource|orient_to_appropriate_service|propose_follow_up|escalate_immediate_relay",
    "follow_up_actions_text": "actions concrètes",
    "next_session_focus_text": "orientation séance suivante"
  },
  "client_delivery": {
    "client_visible_recommended": true,
    "client_facing_summary_text": "formulé simple et rassurant pour client"
  },
  "supervision": {
    "supervision_summary_text": "alertes/doutes interne",
    "detected_context_signals": ["minimisation_verbale", ...],
    "low_confidence_flags": ["..."],
    "excluded_from_client_delivery": ["..."]
  },
  "research": {
    "research_notes_text": null,
    "experimental_hypotheses": []
  },
  "metadata": {
    "model_used": "claude-sonnet-4-20250514",
    "prompt_version": "session_note_cercle_v1",
    "complexity_score": null,
    "validated_by_practitioner": false,
    "practitioner_corrections": null
  }
}
```

**Points-clés de ce schéma** :
- ✅ `vigilance_level_code` = signal de sécurité immédiat (urgent → escalade)
- ✅ `context_hypotheses_json` = grille québécoise appliquée (mais jamais en client_delivery)
- ✅ `supervision` = informations cachées au client
- ✅ `metadata` = traçabilité (version prompt + modèle)

---

## SECTION 3 — Inventaire des tests existants

### 3.1 Fichiers de test (5 fichiers, ~400 lignes de code)

| Fichier | Nb lignes | Type | État |
|---|---|---|---|
| `test_api_smoke.py` | 150+ | Smoke test (flux complet) | ✅ Exécutable |
| `test_prompt_loader.py` | 60+ | Unitaire (prompt loader) | ✅ 3 tests passants |
| `test_register.py` | 20+ | Script manual (registration) | ⚠️ Manuel |
| `test_register_https.py` | 20+ | Script manual (registration HTTPS) | ⚠️ Manuel |
| `check_routes.py` | 30+ | Énumération routes | ⚠️ Audit uniquement |

### 3.2 Tests actifs par domaine

**Moteur IA** :
- ❌ **AUCUN TEST** sur la génération de note de séance (generate_session_note_from_transcript)
- ❌ **AUCUN TEST** sur le parsage JSON ou validation schéma
- ❌ **AUCUN TEST** sur l'extraction de signaux risque

**Flux métier** :
- ⚠️ `test_api_smoke.py` teste le flux complet MAIS moque la génération IA (AsyncMock)
- ❌ **AUCUN TEST** réel sur génération note
- ✅ Tests de registration/login possibles (HTTP call ou pytest)

**Prompts** :
- ✅ `test_prompt_loader.py` : 3 tests unitaires (cache, erreur, chargement)
- ❌ **AUCUN TEST** sur contenu prompt (logique MERLIN)
- ❌ **AUCUN TEST** sur injection dynamique hypothèses/signaux

**Base de données** :
- ⚠️ Tests BDD partiels (smoke test crée/lit objets)
- ❌ **AUCUN TEST** sur migrations Alembic (20260504_0017 = dernière)
- ❌ **AUCUN TEST** sur contraintes d'intégrité

### 3.3 Couverture de test estimée

| Composante | Couverture | Priorité |
|---|---|---|
| API routes (CRUD) | ~20% | P2 |
| Moteur IA (Claude) | ~0% (moqué) | **P1** |
| Analyse intake (regex) | 0% | P2 |
| Document generation | 0% | P2 |
| Authentification | ~10% | P2 |
| Prompts critiques | ~5% (loader) | **P1** |
| LiveKit integration | 0% (dépend externe) | P3 |

---

## SECTION 4 — Tests manquants prioritaires

### 4.1 BLOC 1 — Tests moteur IA (URGENT — P1)

**Raison** : Le moteur est le cœur du produit. Aucun test sur la génération réelle.

**Tests à créer** :
1. `test_session_note_generation_real_claude.py` (intégration avec API Anthropic)
   - Fixture: transcript de test (30-50 mots, langage naturel français)
   - Appel réel à Claude Sonnet 4
   - Assertion: réponse est JSON valide
   - Assertion: schéma respecté (structure + codes énumérés)
   - Assertion: vigilance_level_code ∈ {non_urgent, watch, priority, urgent}

2. `test_prompt_injection.py` (validation prompts METH-001/002/003)
   - Assertion: les 9 hypothèses sont présentes dans le prompt système
   - Assertion: les 12 signaux sont présents
   - Assertion: le prompt système ne contient pas de caractères invalides

3. `test_json_schema_validation.py` (schéma stricte)
   - Assertion: réponse Claude peut être parsée comme JSON
   - Assertion: champs obligatoires présents
   - Assertion: codes énumérés valides (vigilance, tensions, hypothesis_code, etc.)
   - Assertion: types corrects (array vs object vs string)

**Estimé** : 3 tests, ~150 lignes, 2-3 jours de travail (si Claude API disponible)

### 4.2 BLOC 2 — Tests analyse intake (P1)

**Raison** : Le triage des risques au point d'entrée est critique pour la sécurité.

**Tests à créer** :
1. `test_intake_analysis_risk_patterns.py`
   - Test chaque pattern regex: suicide_explicite, automutilation, fin_de_vie, etc.
   - Assertion: "je veux me suicider" → détecte "suicide_explicite" avec niveau "urgent"
   - Assertion: "c'est pas grave" → ne détecte aucun risque
   - Assertion: cas limites (négation, contexte) passent

2. `test_intake_analysis_gap_signals.py`
   - Assertion: texte vide → détecte "gap_empty"
   - Assertion: texte très court (<10 mots) → détecte "gap_too_short"

**Estimé** : 2 tests, ~100 lignes, 1-2 jours

### 4.3 BLOC 3 — Tests bout-à-bout real (P2)

**Raison** : Vérifier que le flux complet fonctionne avec de vrais appels IA.

**Tests à créer** :
1. `test_e2e_session_flow_real.py` (≠ smoke test qui mocke tout)
   - Créer client public
   - Créer intake request (texte libre)
   - Créer audio session
   - Générer note **réelle** depuis Claude
   - Générer document client
   - Vérifier état final de tous les objets BDD

**Estimé** : 1 test, ~100 lignes, 1 jour (si API disponible)

### 4.4 BLOC 4 — Tests superviseur (P2)

**Raison** : Validation et publication document client sont critiques.

**Tests à créer** :
1. `test_supervisor_validation_flow.py`
   - Supervisor valide note → derived_document passe en `client_visible=true`
   - Supervisor rejette note → retour en attente d'opérateur
   - Client ne peut pas voir document tant que superviseur n'a pas validé

**Estimé** : 1 test, ~80 lignes, 1-2 jours

### 4.5 Récapitulatif tests manquants

| BLOC | Nom | Nb tests | Lignes | Délai |
|---|---|---|---|---|
| 1 | Moteur IA | 3 | ~150 | 2-3j |
| 2 | Analyse intake | 2 | ~100 | 1-2j |
| 3 | E2E réel | 1 | ~100 | 1j |
| 4 | Supervision | 1 | ~80 | 1-2j |
| — | **TOTAL** | **7 tests** | **~430 lignes** | **5-8 jours** |

---

## SECTION 5 — Zones fragiles pour usage sensible

### 5.1 Points de risque immédiat

| Risque | Sévérité | Mitigation |
|---|---|---|
| Moteur IA non testé réellement | **CRITIQUE** | Créer BLOC 1 tests avant MVP |
| Pas de validation schéma output Claude | **CRITIQUE** | Ajouter pydantic model ou jsonschema |
| Analyse intake régex fragile (cas limites) | **ÉLEVÉ** | Écrire tests BLOC 2 |
| Pas de contrôle qualité note avant diffusion client | **ÉLEVÉ** | Superviseur valide (implémenté mais pas testé) |
| Prompts modifiables sans versionning immédiat | **MOYEN** | prompt_loader sérialise OK, mais git-workflow à respecter |
| Data sensibilité classe par défaut = HIGH | **MOYEN** | OK pour MVP, à affiner selon RGPD |

### 5.2 Points stables

✅ **Authentification** : JWT + bcrypt, standard FastAPI
✅ **ORM** : SQLAlchemy bien structurée
✅ **Routes CRUD** : patterns cohérents
✅ **Prompts externalisés** : versioning git en place
✅ **LiveKit intégration** : abstraite (pas critique pour MVP texte)

---

## SECTION 6 — MVP démontrable (proposition 1 page)

### 6.1 Scope du MVP

**Objectif** : montrer que le moteur marche d'bout en bout, de la demande client au rapport structuré.

**Horizon** : 14 jours (deadline fin mai avant changements structurels)

**Audience** : financeur technique + praticiens de test

### 6.2 Démonstration type (scénario de 10 min)

```
SCENARIO DEMO:

[1] Financeur accède au portail client (frontend).
    ↓
[2] "Je suis fatigué, j'ai mal au dos, j'ai peur d'aller au travail"
    [POST /v1/intake-requests]
    ✅ Système détecte: fatigue + peur potentielle (priority signal)
    ↓
[3] Financeur réserve session audio.
    [POST /v1/audio-sessions → LiveKit room créée]
    ✅ Lien direct vers studio audio
    ↓
[4] Financeur joue rôle client.
    [Audio live 3-5 min] → Transcription fournie
    ↓
[5] Opérateur clôture session.
    [PUT /v1/audio-recordings → transcription récupérée]
    ✅ Affichage: "génération en cours"
    ↓
[6] MOTEUR RUNS.
    [POST /v1/session-notes]
    Claude Sonnet 4 analyse la transcription
    ✅ Applique grille Cercle V1 (coeur/corps/esprit/etre)
    ✅ Détecte signaux contexte québécois
    ✅ Produit vigilance_level + tensions + hypothèses
    ↓
[7] Superviseur valide.
    [GET note] → voit production_note + supervision section
    ✅ "flags de confiance basse" pointées
    [POST /session-notes/{id}/validate?decision=approve]
    ↓
[8] AFFICHAGE CLIENT.
    [GET /suivi/documents/{code}]
    ✅ Client voit: client_facing_summary_text (formulé simple)
    ✅ Document PDF généré avec synthèse de séance
    ↓
[9] Financeur voit:
    ✅ Transcript → Note structurée (4 dimensions)
    ✅ Alertes de sécurité détectées (vigilance_level)
    ✅ Document formaté prêt pour client
```

### 6.3 Points de preuve pour financeur

1. **Moteur IA fonctionnel** : la note est générée en <3s, schéma valide ✅
2. **Grille Cercle V1 appliquée** : 4 dimensions + tensions + hypothèses ✅
3. **Contextualisation québécoise** : hypothèses/signaux intégrés ✅
4. **Sécurité** : vigilance_level détecté (urgent si besoin) ✅
5. **Traçabilité** : metadata inclut version prompt et modèle ✅
6. **Supervision** : superviseur peut valider/rejeter ✅
7. **Diffusion client** : document structuré (pas brut) ✅

### 6.4 Préalables technique pour MVP

**À avoir en place avant démo** :
- [ ] Anthropic API key valide (budget suffisant)
- [ ] Tests BLOC 1 (moteur IA) passants
- [ ] Tests BLOC 2 (analyse intake) passants
- [ ] Frontend accessible (ou curl-based demo)
- [ ] Données de test anonymisées/fictives
- [ ] Logs propres (pas de leak data sensible)

---

## SECTION 7 — Plan de travail 14 jours

### 7.1 Chronologie proposée

**Semaine 1 (jours 1-7)**

| Jour | Tâche | Livrable | Durée |
|---|---|---|---|
| 1 | Tests BLOC 1.1 (génération réelle) | `test_session_note_generation_real_claude.py` | 1j |
| 2 | Tests BLOC 1.2 (validation schéma) | `test_json_schema_validation.py` | 1j |
| 3 | Tests BLOC 1.3 (injection prompts) | `test_prompt_injection.py` | 0,5j |
| 4 | Tests BLOC 2 (analyse intake) | `test_intake_analysis_*.py` | 1-2j |
| 5 | Intégration tests + fixtures | All tests passing | 1j |
| 6-7 | Tests BLOC 3 (E2E réel) | `test_e2e_session_flow_real.py` | 1-2j |

**Semaine 2 (jours 8-14)**

| Jour | Tâche | Livrable | Durée |
|---|---|---|---|
| 8 | Tests BLOC 4 (superviseur) | `test_supervisor_validation_flow.py` | 1-2j |
| 9-10 | Validation schéma Claude (Pydantic) | Modèle SessionNoteOutput | 2j |
| 11-12 | Préparation démo + fixtures de test | Données anonymisées + scripts | 2j |
| 13-14 | Run de démo complet | MVP démontrable | 2j |

**Heures estimées** : 12-15 jours (10-12 jours si tests partiels OK)

### 7.2 Dépendances critiques

- Anthropic API key fonctionnelle + budget
- Pas de refactor architectural (utiliser code existant)
- LiveKit optionnel pour MVP (audio mock possible)

---

## SECTION 8 — Fichiers à modifier (liste exacte, sans modification)

### 8.1 Fichiers à CRÉER (nouveaux tests)

**Dossier tests/** (à créer/ajouter) :

```
tests/
├── test_session_note_generation_real_claude.py      [CREER]
├── test_json_schema_validation.py                   [CREER]
├── test_prompt_injection.py                         [CREER]
├── test_intake_analysis_risk_patterns.py            [CREER]
├── test_intake_analysis_gap_signals.py              [CREER]
├── test_e2e_session_flow_real.py                    [CREER]
├── test_supervisor_validation_flow.py               [CREER]
├── test_prompt_loader.py                            [MODIFIER — ajouter tests]
└── conftest.py                                      [CREER — fixtures communes]
```

### 8.2 Fichiers à MODIFIER (code existant)

**Backend IA** :
- `app/ai/anthropic_session_note_pipeline.py`
  - Ajouter validation Pydantic/jsonschema output Claude
  - Ajouter logging structuré de requête/réponse

- `app/ai/prompts/session_note_cercle_v1.py`
  - Ajouter docstring sur les 3 prompts chargés
  - Pas de logique métier à changer

**Services** :
- `app/services/intake_analysis.py`
  - Ajouter logging des patterns détectés
  - Externaliser patterns regex en constantes nommées (lisibilité)

- `app/services/session_documents.py`
  - Validation que client_delivery ne contient pas supervision
  - Assertion: client_visible_recommended repose sur validated_by_practitioner

**Routes** :
- `app/api/routes/session_notes.py`
  - Ajouter endpoint pour vérifier intégrité d'une note (schema check)
  - Ajouter logging de la validation superviseur

**Gouvernance** :
- `11_PROMPTS/AUDIT_PROMPTS_EXISTANTS_V1.md`
  - Ajouter section "État des tests" (mise à jour post-BLOC-1-4)

- `00_GOUVERNANCE/MERLIN_GOUV_REGISTRE_DECISIONS_REVISIONS_IVIA_MERLIN_V1.md`
  - Ajouter DEC-041 (décision sur plan de tests)

### 8.3 Fichiers à CRÉER (documentation)

- `10_backend_merlin_api/TESTING_STRATEGY.md`
  - Approche de test du moteur
  - Fixtures et données de test anonymisées
  - Checklist avant prod

- `11_PROMPTS/PROD-VALID-002-TEST_PLAN.md`
  - Détail exécutif des 7 tests
  - Cas limites couverts
  - Dépendances externes

---

## SECTION 9 — Recommandations pour finançabilité

### 9.1 Preuves techniques requises (pour pitch)

✅ **OK pour montrer dès maintenant** :
1. API routes fonctionnent (CRUD)
2. Authentification robuste
3. Prompts externalisés et versionnés
4. Supervision workflow implémenté (logique)
5. Transcription → schéma respecté (structure)

⚠️ **À montrer après tests BLOC 1** :
1. Moteur IA génère notes réelles (pas mock)
2. Schéma JSON valide systématiquement
3. Vigilance level correctement détecté
4. Contexte québécois appliqué

### 9.2 Risques pour investisseur technique

| Risque | Mitigation |
|---|---|
| "Le moteur IA marche-t-il réellement ?" | **Tests BLOC 1 + démo live** |
| "Combien coûte Claude API en volume ?" | Estimation coût/note + test 100 notes |
| "Peut-on garantir sécurité (vigilance)?" | Tests BLOC 2 + supervision workflow |
| "Peut-on passer en production rapidement ?" | Alembic + CI/CD en place, juste besoin tests |
| "Quels sont les points fragiles ?" | Section 5.1 ce document |

### 9.3 Prochaines étapes post-MVP (priorité)

1. **Vague 4** — Migration prompts héritées (01_session → 02_METH) + tests
2. **Vague 5** — Normalisation arborescence (`01_FONDATEUR` + `01_FONDEMENTS`)
3. **Vague 6** — API productionelle (auth raffinage, rate limiting, monitoring)
4. **Vague 7** — UX praticien (interface validation, workflows)

---

## SECTION 10 — Historique de révisions

| Version | Date | Auteur | Nature |
|---|---|---|---|
| 1.0 | 2026-05-05 | fondateur | Création — audit finançabilité |

---

## Annexe A — Dépendances critiques

**APIs externes** :
- Anthropic Claude Sonnet 4: latence ~2-5s/note, coût ~$0.02-0.05/note
- LiveKit (audio): optionnel pour MVP, peut être mocké
- Email (SMTP): pour registration/verification

**Infrastructure** :
- PostgreSQL (ou SQLite dev): BDD persistante
- Nginx 1.27: reverse proxy + TLS
- Uvicorn: serveur ASGI

**Librairies Python** :
- FastAPI 0.110+, SQLAlchemy 2.0+, Pydantic 2.1+, pytest 8.1+

---

## Annexe B — Checklist de déploiement MVP

- [ ] Tests BLOC 1 passants (moteur IA)
- [ ] Tests BLOC 2 passants (analyse intake)
- [ ] Logs pas de leak data sensible
- [ ] Anthropic key valide + budget
- [ ] Fixtures de test anonymisées
- [ ] Frontend accessible (curl OK)
- [ ] Démo scénario validée
- [ ] Docs pour financeur

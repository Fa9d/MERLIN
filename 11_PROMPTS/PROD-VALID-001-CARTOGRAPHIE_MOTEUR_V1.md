---
titre: Plan de validation technique MERLIN/IVIA â€” Cartographie du moteur
id: PROD-VALID-001
statut: active
type: audit
couche: PROD
pÃ©rimÃ¨tre: moteur backend + prompts critiques + tests
auteur: fondateur
date: 2026-05-05
version: 1.0
dÃ©pend_de: [ADR-0002, MERLIN-AUDIT-PROMPTS-V1]
remplace: []
arbitrage_requis: non â€” rapport d'Ã©tat
source_canonique: 11_PROMPTS/PROD-VALID-001-CARTOGRAPHIE_MOTEUR_V1.md
test_associe: test_json_schema_validation.py::test_prod001_output
impact_attendu: "A documenter lors de la prochaine modification"
---

# MERLIN/IVIA â€” Validation technique pour finanÃ§abilitÃ©

> **Objectif** : cartographier le moteur actuel, identifier ce qui est testable, proposer un MVP dÃ©montrable
> **Audience** : fondateur + financeur technique
> **Horizon** : fin mai 2026
> **Date d'audit** : 2026-05-05

---

## SECTION 1 â€” Cartographie du moteur actuel

### 1.1 Structure gÃ©nÃ©rale

Le moteur IVIA/MERLIN est un backend FastAPI exposant un API REST en `v1` (`/v1/*`). Il gÃ¨re le flux complet d'une session de santÃ© mentale : de la prise en charge client jusqu'Ã  la gÃ©nÃ©ration d'un document structurÃ©.

**Stack technique confirmÃ©e** :
- Backend: FastAPI 0.110+ (Python 3.12)
- BDD: PostgreSQL 15 ou SQLite (dÃ©veloppement)
- Auth: JWT + bcrypt
- IA: Anthropic Claude Sonnet 4 (2025-05-14)
- Temps rÃ©el: LiveKit (audio/video)
- Infrastructure: Nginx 1.27, uvicorn

### 1.2 Modules de base (app/)

| Module | RÃ´le | Ã‰tat |
|---|---|---|
| `api/routes/` | 15 routeurs REST | âœ… Actif |
| `models/` | 11 entitÃ©s Doctrine ORM | âœ… SchÃ©mas stables |
| `schemas/` | Validateurs Pydantic | âœ… Validations strictes |
| `services/` | Logique mÃ©tier isolÃ©e | âœ… Testable |
| `ai/` | Pipeline IA Anthropic | âœ… Moteur critique |
| `db/` | Couche BDD | âœ… Alembic actif |
| `core/` | Config + authentification | âœ… Robuste |

### 1.3 Routes API actives (v1)

**CÅ“ur du flux mÃ©tier (7 routes critiques)** :

| Endpoint | MÃ©thode | RÃ´le | DÃ©pendances |
|---|---|---|---|
| `/v1/clients` | POST | CrÃ©er/register client public | email + validation |
| `/v1/intake-requests` | POST | DÃ©pÃ´t demande (entry point) | analyse texte brut (regex) |
| `/v1/audio-sessions` | POST | CrÃ©er session (rÃ©server room) | LiveKit API |
| `/v1/audio-recordings` | PUT | ClÃ´turer session + rÃ©cupÃ©rer audio | FileSystem ou S3 |
| `/v1/session-notes` | POST | GÃ©nÃ©rer note (IA + structuration) | **Moteur Anthropic Claude** |
| `/v1/derived-documents` | POST | GÃ©nÃ©rer document client | Jinja2 + templates |
| `/v1/audio-sessions/{id}` | GET | Lire Ã©tat session | BDD |

**Routes de supervision (3)** :
- `POST /v1/session-notes/{id}/validate` â€” superviseur valide note
- `GET /v1/sessions` (list, filtrable) â€” vue opÃ©rateur/superviseur
- `PATCH /v1/sessions/{id}` â€” mise Ã  jour Ã©tat de session

**Routes administratives (5)** :
- `/v1/register` â€” enregistrement (client + praticien)
- `/v1/verify-email` â€” validation email
- `/v1/auth/login` â€” JWT
- `/v1/consents` â€” gestion consentements
- `/v1/schedules`, `/v1/praticiens` â€” rÃ©fÃ©rentiels

### 1.4 Flux critique de la session

```
PUBLIC FLOW:
  Client public
    â†“
  [POST /clients] â†’ IntakeRequest (via demande texte libre)
    â†“
  [Analyse via intake_analysis.py] â†’ risk/gap signals dÃ©tectÃ©s
    â†“
  [POST /audio-sessions] â†’ RÃ©servation LiveKit (room name + tokens)
    â†“
  [Audio live] â†’ Enregistrement on-the-fly
    â†“
  [PUT /audio-recordings?session_id=X] â†’ ClÃ´ture + audio rÃ©cupÃ©rÃ©
    â†“
  [POST /session-notes] â†’ MOTEUR: Anthropic Claude Sonnet 4
    â”œâ”€ Prompt: SESSION_NOTE_CERCLE_SYSTEM_PROMPT (METH-003)
    â”œâ”€ Contexte: hypothÃ¨ses + signaux (METH-001, METH-002)
    â””â”€ Output: JSON structurÃ© (production_note, client_delivery, supervision, research, metadata)
    â†“
  [POST /derived-documents] â†’ Document client gÃ©nÃ©rÃ©s depuis note
    â†“
  [Client voit rÃ©sultat] via `/suivi/documents/[CODE]`

SUPERVISION FLOW:
  Superviseur voit liste sessions
    â†“
  [GET /sessions?status=pending_review]
    â†“
  [Lecture note + flags]
    â†“
  [POST /session-notes/{id}/validate?decision=approve/reject]
    â†“
  Si approve â†’ derived_document passe en `client_visible=true`
  Si reject â†’ retour opÃ©rateur pour correction
```

---

## SECTION 2 â€” Prompts critiques du moteur

### 2.1 Ã‰tat de l'externalisation (Vague 3 - Phase A)

**Tous les prompts critiques sont externalisÃ©s** dans `11_PROMPTS/02_METH/` depuis le 2026-05-05.

| ID | Fichier | RÃ´le | Couche | ModÃ¨le | Statut |
|---|---|---|---|---|---|
| METH-001 | `METH-001-quebec-context-hypotheses-v1.md` | 9 hypothÃ¨ses contextuelles quÃ©bÃ©coises | METH | Sonnet 4 | âœ… Actif |
| METH-002 | `METH-002-quebec-context-signals-v1.md` | 12 signaux contextuels Ã  dÃ©tecter | METH | Sonnet 4 | âœ… Actif |
| METH-003 | `METH-003-session-note-cercle-system-prompt-v1.md` | Prompt systÃ¨me principal (la *persona* MERLIN) | METH | Sonnet 4 | âœ… CRITIQUE |

### 2.2 Composantes du prompt systÃ¨me METH-003

Le prompt systÃ¨me dÃ©finit :
1. **RÃ´le** : "Tu es MERLIN, moteur documentaire d'IVIA"
2. **Grille d'analyse** : 4 dimensions (coeur/corps/esprit/etre) + contexte immÃ©diat
3. **Contraintes absolues** :
   - âŒ Pas de diagnostic
   - âŒ Pas de traitement prescrit
   - âŒ Pas de spÃ©culation mÃ©taphysique
   - âŒ Pas de citation de traditions autochtones (sauf contexte formel)
4. **RÃ¨gles de diffusion** : ce qui va en production_note vs client_delivery vs supervision
5. **Contexte quÃ©bÃ©cois** : hypothÃ¨ses + signaux (injectÃ©s depuis METH-001/002)
6. **Format de sortie** : schÃ©ma JSON strictement dÃ©fini

### 2.3 Chargement dynamique via prompt_loader.py

Depuis Vague 3:
- Les 3 prompts sont chargÃ©s depuis le disque via `load_prompt(prompt_id)`
- Cache mÃ©moire simple (dict) pour Ã©viter relecture disque rÃ©pÃ©tÃ©e
- Erreur explicite `PromptNotFoundError` si fichier manquant
- Modification de prompt = modification fichier Markdown (traÃ§able dans git)

**Impact fondateur** : les changeants au moteur IA passent dÃ©sormais par `11_PROMPTS/`, pas par code Python.

### 2.4 SchÃ©ma de sortie du moteur

La note de sÃ©ance gÃ©nÃ©rÃ©e par Claude respecte ce schÃ©ma JSON :

```
{
  "production_note": {
    "summary_text": "rÃ©sumÃ© court (~150 mots)",
    "observations_text": "lecture structurÃ©e",
    "coeur_summary_text": "dimension relationnelle/Ã©motionnelle",
    "corps_summary_text": "dimension physique/somatique",
    "esprit_summary_text": "dimension cognitive/mentale",
    "etre_summary_text": "dimension existentielle/identitaire",
    "immediate_context_text": "environnement immÃ©diat",
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
    "follow_up_actions_text": "actions concrÃ¨tes",
    "next_session_focus_text": "orientation sÃ©ance suivante"
  },
  "client_delivery": {
    "client_visible_recommended": true,
    "client_facing_summary_text": "formulÃ© simple et rassurant pour client"
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

**Points-clÃ©s de ce schÃ©ma** :
- âœ… `vigilance_level_code` = signal de sÃ©curitÃ© immÃ©diat (urgent â†’ escalade)
- âœ… `context_hypotheses_json` = grille quÃ©bÃ©coise appliquÃ©e (mais jamais en client_delivery)
- âœ… `supervision` = informations cachÃ©es au client
- âœ… `metadata` = traÃ§abilitÃ© (version prompt + modÃ¨le)

---

## SECTION 3 â€” Inventaire des tests existants

### 3.1 Fichiers de test (5 fichiers, ~400 lignes de code)

| Fichier | Nb lignes | Type | Ã‰tat |
|---|---|---|---|
| `test_api_smoke.py` | 150+ | Smoke test (flux complet) | âœ… ExÃ©cutable |
| `test_prompt_loader.py` | 60+ | Unitaire (prompt loader) | âœ… 3 tests passants |
| `test_register.py` | 20+ | Script manual (registration) | âš ï¸ Manuel |
| `test_register_https.py` | 20+ | Script manual (registration HTTPS) | âš ï¸ Manuel |
| `check_routes.py` | 30+ | Ã‰numÃ©ration routes | âš ï¸ Audit uniquement |

### 3.2 Tests actifs par domaine

**Moteur IA** :
- âŒ **AUCUN TEST** sur la gÃ©nÃ©ration de note de sÃ©ance (generate_session_note_from_transcript)
- âŒ **AUCUN TEST** sur le parsage JSON ou validation schÃ©ma
- âŒ **AUCUN TEST** sur l'extraction de signaux risque

**Flux mÃ©tier** :
- âš ï¸ `test_api_smoke.py` teste le flux complet MAIS moque la gÃ©nÃ©ration IA (AsyncMock)
- âŒ **AUCUN TEST** rÃ©el sur gÃ©nÃ©ration note
- âœ… Tests de registration/login possibles (HTTP call ou pytest)

**Prompts** :
- âœ… `test_prompt_loader.py` : 3 tests unitaires (cache, erreur, chargement)
- âŒ **AUCUN TEST** sur contenu prompt (logique MERLIN)
- âŒ **AUCUN TEST** sur injection dynamique hypothÃ¨ses/signaux

**Base de donnÃ©es** :
- âš ï¸ Tests BDD partiels (smoke test crÃ©e/lit objets)
- âŒ **AUCUN TEST** sur migrations Alembic (20260504_0017 = derniÃ¨re)
- âŒ **AUCUN TEST** sur contraintes d'intÃ©gritÃ©

### 3.3 Couverture de test estimÃ©e

| Composante | Couverture | PrioritÃ© |
|---|---|---|
| API routes (CRUD) | ~20% | P2 |
| Moteur IA (Claude) | ~0% (moquÃ©) | **P1** |
| Analyse intake (regex) | 0% | P2 |
| Document generation | 0% | P2 |
| Authentification | ~10% | P2 |
| Prompts critiques | ~5% (loader) | **P1** |
| LiveKit integration | 0% (dÃ©pend externe) | P3 |

---

## SECTION 4 â€” Tests manquants prioritaires

### 4.1 BLOC 1 â€” Tests moteur IA (URGENT â€” P1)

**Raison** : Le moteur est le cÅ“ur du produit. Aucun test sur la gÃ©nÃ©ration rÃ©elle.

**Tests Ã  crÃ©er** :
1. `test_session_note_generation_real_claude.py` (intÃ©gration avec API Anthropic)
   - Fixture: transcript de test (30-50 mots, langage naturel franÃ§ais)
   - Appel rÃ©el Ã  Claude Sonnet 4
   - Assertion: rÃ©ponse est JSON valide
   - Assertion: schÃ©ma respectÃ© (structure + codes Ã©numÃ©rÃ©s)
   - Assertion: vigilance_level_code âˆˆ {non_urgent, watch, priority, urgent}

2. `test_prompt_injection.py` (validation prompts METH-001/002/003)
   - Assertion: les 9 hypothÃ¨ses sont prÃ©sentes dans le prompt systÃ¨me
   - Assertion: les 12 signaux sont prÃ©sents
   - Assertion: le prompt systÃ¨me ne contient pas de caractÃ¨res invalides

3. `test_json_schema_validation.py` (schÃ©ma stricte)
   - Assertion: rÃ©ponse Claude peut Ãªtre parsÃ©e comme JSON
   - Assertion: champs obligatoires prÃ©sents
   - Assertion: codes Ã©numÃ©rÃ©s valides (vigilance, tensions, hypothesis_code, etc.)
   - Assertion: types corrects (array vs object vs string)

**EstimÃ©** : 3 tests, ~150 lignes, 2-3 jours de travail (si Claude API disponible)

### 4.2 BLOC 2 â€” Tests analyse intake (P1)

**Raison** : Le triage des risques au point d'entrÃ©e est critique pour la sÃ©curitÃ©.

**Tests Ã  crÃ©er** :
1. `test_intake_analysis_risk_patterns.py`
   - Test chaque pattern regex: suicide_explicite, automutilation, fin_de_vie, etc.
   - Assertion: "je veux me suicider" â†’ dÃ©tecte "suicide_explicite" avec niveau "urgent"
   - Assertion: "c'est pas grave" â†’ ne dÃ©tecte aucun risque
   - Assertion: cas limites (nÃ©gation, contexte) passent

2. `test_intake_analysis_gap_signals.py`
   - Assertion: texte vide â†’ dÃ©tecte "gap_empty"
   - Assertion: texte trÃ¨s court (<10 mots) â†’ dÃ©tecte "gap_too_short"

**EstimÃ©** : 2 tests, ~100 lignes, 1-2 jours

### 4.3 BLOC 3 â€” Tests bout-Ã -bout real (P2)

**Raison** : VÃ©rifier que le flux complet fonctionne avec de vrais appels IA.

**Tests Ã  crÃ©er** :
1. `test_e2e_session_flow_real.py` (â‰  smoke test qui mocke tout)
   - CrÃ©er client public
   - CrÃ©er intake request (texte libre)
   - CrÃ©er audio session
   - GÃ©nÃ©rer note **rÃ©elle** depuis Claude
   - GÃ©nÃ©rer document client
   - VÃ©rifier Ã©tat final de tous les objets BDD

**EstimÃ©** : 1 test, ~100 lignes, 1 jour (si API disponible)

### 4.4 BLOC 4 â€” Tests superviseur (P2)

**Raison** : Validation et publication document client sont critiques.

**Tests Ã  crÃ©er** :
1. `test_supervisor_validation_flow.py`
   - Supervisor valide note â†’ derived_document passe en `client_visible=true`
   - Supervisor rejette note â†’ retour en attente d'opÃ©rateur
   - Client ne peut pas voir document tant que superviseur n'a pas validÃ©

**EstimÃ©** : 1 test, ~80 lignes, 1-2 jours

### 4.5 RÃ©capitulatif tests manquants

| BLOC | Nom | Nb tests | Lignes | DÃ©lai |
|---|---|---|---|---|
| 1 | Moteur IA | 3 | ~150 | 2-3j |
| 2 | Analyse intake | 2 | ~100 | 1-2j |
| 3 | E2E rÃ©el | 1 | ~100 | 1j |
| 4 | Supervision | 1 | ~80 | 1-2j |
| â€” | **TOTAL** | **7 tests** | **~430 lignes** | **5-8 jours** |

---

## SECTION 5 â€” Zones fragiles pour usage sensible

### 5.1 Points de risque immÃ©diat

| Risque | SÃ©vÃ©ritÃ© | Mitigation |
|---|---|---|
| Moteur IA non testÃ© rÃ©ellement | **CRITIQUE** | CrÃ©er BLOC 1 tests avant MVP |
| Pas de validation schÃ©ma output Claude | **CRITIQUE** | Ajouter pydantic model ou jsonschema |
| Analyse intake rÃ©gex fragile (cas limites) | **Ã‰LEVÃ‰** | Ã‰crire tests BLOC 2 |
| Pas de contrÃ´le qualitÃ© note avant diffusion client | **Ã‰LEVÃ‰** | Superviseur valide (implÃ©mentÃ© mais pas testÃ©) |
| Prompts modifiables sans versionning immÃ©diat | **MOYEN** | prompt_loader sÃ©rialise OK, mais git-workflow Ã  respecter |
| Data sensibilitÃ© classe par dÃ©faut = HIGH | **MOYEN** | OK pour MVP, Ã  affiner selon RGPD |

### 5.2 Points stables

âœ… **Authentification** : JWT + bcrypt, standard FastAPI
âœ… **ORM** : SQLAlchemy bien structurÃ©e
âœ… **Routes CRUD** : patterns cohÃ©rents
âœ… **Prompts externalisÃ©s** : versioning git en place
âœ… **LiveKit intÃ©gration** : abstraite (pas critique pour MVP texte)

---

## SECTION 6 â€” MVP dÃ©montrable (proposition 1 page)

### 6.1 Scope du MVP

**Objectif** : montrer que le moteur marche d'bout en bout, de la demande client au rapport structurÃ©.

**Horizon** : 14 jours (deadline fin mai avant changements structurels)

**Audience** : financeur technique + praticiens de test

### 6.2 DÃ©monstration type (scÃ©nario de 10 min)

```
SCENARIO DEMO:

[1] Financeur accÃ¨de au portail client (frontend).
    â†“
[2] "Je suis fatiguÃ©, j'ai mal au dos, j'ai peur d'aller au travail"
    [POST /v1/intake-requests]
    âœ… SystÃ¨me dÃ©tecte: fatigue + peur potentielle (priority signal)
    â†“
[3] Financeur rÃ©serve session audio.
    [POST /v1/audio-sessions â†’ LiveKit room crÃ©Ã©e]
    âœ… Lien direct vers studio audio
    â†“
[4] Financeur joue rÃ´le client.
    [Audio live 3-5 min] â†’ Transcription fournie
    â†“
[5] OpÃ©rateur clÃ´ture session.
    [PUT /v1/audio-recordings â†’ transcription rÃ©cupÃ©rÃ©e]
    âœ… Affichage: "gÃ©nÃ©ration en cours"
    â†“
[6] MOTEUR RUNS.
    [POST /v1/session-notes]
    Claude Sonnet 4 analyse la transcription
    âœ… Applique grille Cercle V1 (coeur/corps/esprit/etre)
    âœ… DÃ©tecte signaux contexte quÃ©bÃ©cois
    âœ… Produit vigilance_level + tensions + hypothÃ¨ses
    â†“
[7] Superviseur valide.
    [GET note] â†’ voit production_note + supervision section
    âœ… "flags de confiance basse" pointÃ©es
    [POST /session-notes/{id}/validate?decision=approve]
    â†“
[8] AFFICHAGE CLIENT.
    [GET /suivi/documents/{code}]
    âœ… Client voit: client_facing_summary_text (formulÃ© simple)
    âœ… Document PDF gÃ©nÃ©rÃ© avec synthÃ¨se de sÃ©ance
    â†“
[9] Financeur voit:
    âœ… Transcript â†’ Note structurÃ©e (4 dimensions)
    âœ… Alertes de sÃ©curitÃ© dÃ©tectÃ©es (vigilance_level)
    âœ… Document formatÃ© prÃªt pour client
```

### 6.3 Points de preuve pour financeur

1. **Moteur IA fonctionnel** : la note est gÃ©nÃ©rÃ©e en <3s, schÃ©ma valide âœ…
2. **Grille Cercle V1 appliquÃ©e** : 4 dimensions + tensions + hypothÃ¨ses âœ…
3. **Contextualisation quÃ©bÃ©coise** : hypothÃ¨ses/signaux intÃ©grÃ©s âœ…
4. **SÃ©curitÃ©** : vigilance_level dÃ©tectÃ© (urgent si besoin) âœ…
5. **TraÃ§abilitÃ©** : metadata inclut version prompt et modÃ¨le âœ…
6. **Supervision** : superviseur peut valider/rejeter âœ…
7. **Diffusion client** : document structurÃ© (pas brut) âœ…

### 6.4 PrÃ©alables technique pour MVP

**Ã€ avoir en place avant dÃ©mo** :
- [ ] Anthropic API key valide (budget suffisant)
- [ ] Tests BLOC 1 (moteur IA) passants
- [ ] Tests BLOC 2 (analyse intake) passants
- [ ] Frontend accessible (ou curl-based demo)
- [ ] DonnÃ©es de test anonymisÃ©es/fictives
- [ ] Logs propres (pas de leak data sensible)

---

## SECTION 7 â€” Plan de travail 14 jours

### 7.1 Chronologie proposÃ©e

**Semaine 1 (jours 1-7)**

| Jour | TÃ¢che | Livrable | DurÃ©e |
|---|---|---|---|
| 1 | Tests BLOC 1.1 (gÃ©nÃ©ration rÃ©elle) | `test_session_note_generation_real_claude.py` | 1j |
| 2 | Tests BLOC 1.2 (validation schÃ©ma) | `test_json_schema_validation.py` | 1j |
| 3 | Tests BLOC 1.3 (injection prompts) | `test_prompt_injection.py` | 0,5j |
| 4 | Tests BLOC 2 (analyse intake) | `test_intake_analysis_*.py` | 1-2j |
| 5 | IntÃ©gration tests + fixtures | All tests passing | 1j |
| 6-7 | Tests BLOC 3 (E2E rÃ©el) | `test_e2e_session_flow_real.py` | 1-2j |

**Semaine 2 (jours 8-14)**

| Jour | TÃ¢che | Livrable | DurÃ©e |
|---|---|---|---|
| 8 | Tests BLOC 4 (superviseur) | `test_supervisor_validation_flow.py` | 1-2j |
| 9-10 | Validation schÃ©ma Claude (Pydantic) | ModÃ¨le SessionNoteOutput | 2j |
| 11-12 | PrÃ©paration dÃ©mo + fixtures de test | DonnÃ©es anonymisÃ©es + scripts | 2j |
| 13-14 | Run de dÃ©mo complet | MVP dÃ©montrable | 2j |

**Heures estimÃ©es** : 12-15 jours (10-12 jours si tests partiels OK)

### 7.2 DÃ©pendances critiques

- Anthropic API key fonctionnelle + budget
- Pas de refactor architectural (utiliser code existant)
- LiveKit optionnel pour MVP (audio mock possible)

---

## SECTION 8 â€” Fichiers Ã  modifier (liste exacte, sans modification)

### 8.1 Fichiers Ã  CRÃ‰ER (nouveaux tests)

**Dossier tests/** (Ã  crÃ©er/ajouter) :

```
tests/
â”œâ”€â”€ test_session_note_generation_real_claude.py      [CREER]
â”œâ”€â”€ test_json_schema_validation.py                   [CREER]
â”œâ”€â”€ test_prompt_injection.py                         [CREER]
â”œâ”€â”€ test_intake_analysis_risk_patterns.py            [CREER]
â”œâ”€â”€ test_intake_analysis_gap_signals.py              [CREER]
â”œâ”€â”€ test_e2e_session_flow_real.py                    [CREER]
â”œâ”€â”€ test_supervisor_validation_flow.py               [CREER]
â”œâ”€â”€ test_prompt_loader.py                            [MODIFIER â€” ajouter tests]
â””â”€â”€ conftest.py                                      [CREER â€” fixtures communes]
```

### 8.2 Fichiers Ã  MODIFIER (code existant)

**Backend IA** :
- `app/ai/anthropic_session_note_pipeline.py`
  - Ajouter validation Pydantic/jsonschema output Claude
  - Ajouter logging structurÃ© de requÃªte/rÃ©ponse

- `app/ai/prompts/session_note_cercle_v1.py`
  - Ajouter docstring sur les 3 prompts chargÃ©s
  - Pas de logique mÃ©tier Ã  changer

**Services** :
- `app/services/intake_analysis.py`
  - Ajouter logging des patterns dÃ©tectÃ©s
  - Externaliser patterns regex en constantes nommÃ©es (lisibilitÃ©)

- `app/services/session_documents.py`
  - Validation que client_delivery ne contient pas supervision
  - Assertion: client_visible_recommended repose sur validated_by_practitioner

**Routes** :
- `app/api/routes/session_notes.py`
  - Ajouter endpoint pour vÃ©rifier intÃ©gritÃ© d'une note (schema check)
  - Ajouter logging de la validation superviseur

**Gouvernance** :
- `11_PROMPTS/AUDIT_PROMPTS_EXISTANTS_V1.md`
  - Ajouter section "Ã‰tat des tests" (mise Ã  jour post-BLOC-1-4)

- `00_GOUVERNANCE/MERLIN_GOUV_REGISTRE_DECISIONS_REVISIONS_IVIA_MERLIN_V1.md`
  - Ajouter DEC-041 (dÃ©cision sur plan de tests)

### 8.3 Fichiers Ã  CRÃ‰ER (documentation)

- `10_backend_merlin_api/TESTING_STRATEGY.md`
  - Approche de test du moteur
  - Fixtures et donnÃ©es de test anonymisÃ©es
  - Checklist avant prod

- `11_PROMPTS/PROD-VALID-002-TEST_PLAN.md`
  - DÃ©tail exÃ©cutif des 7 tests
  - Cas limites couverts
  - DÃ©pendances externes

---

## SECTION 9 â€” Recommandations pour finanÃ§abilitÃ©

### 9.1 Preuves techniques requises (pour pitch)

âœ… **OK pour montrer dÃ¨s maintenant** :
1. API routes fonctionnent (CRUD)
2. Authentification robuste
3. Prompts externalisÃ©s et versionnÃ©s
4. Supervision workflow implÃ©mentÃ© (logique)
5. Transcription â†’ schÃ©ma respectÃ© (structure)

âš ï¸ **Ã€ montrer aprÃ¨s tests BLOC 1** :
1. Moteur IA gÃ©nÃ¨re notes rÃ©elles (pas mock)
2. SchÃ©ma JSON valide systÃ©matiquement
3. Vigilance level correctement dÃ©tectÃ©
4. Contexte quÃ©bÃ©cois appliquÃ©

### 9.2 Risques pour investisseur technique

| Risque | Mitigation |
|---|---|
| "Le moteur IA marche-t-il rÃ©ellement ?" | **Tests BLOC 1 + dÃ©mo live** |
| "Combien coÃ»te Claude API en volume ?" | Estimation coÃ»t/note + test 100 notes |
| "Peut-on garantir sÃ©curitÃ© (vigilance)?" | Tests BLOC 2 + supervision workflow |
| "Peut-on passer en production rapidement ?" | Alembic + CI/CD en place, juste besoin tests |
| "Quels sont les points fragiles ?" | Section 5.1 ce document |

### 9.3 Prochaines Ã©tapes post-MVP (prioritÃ©)

1. **Vague 4** â€” Migration prompts hÃ©ritÃ©es (01_session â†’ 02_METH) + tests
2. **Vague 5** â€” Normalisation arborescence (`01_FONDATEUR` + `01_FONDEMENTS`)
3. **Vague 6** â€” API productionelle (auth raffinage, rate limiting, monitoring)
4. **Vague 7** â€” UX praticien (interface validation, workflows)

---

## SECTION 10 â€” Historique de rÃ©visions

| Version | Date | Auteur | Nature |
|---|---|---|---|
| 1.0 | 2026-05-05 | fondateur | CrÃ©ation â€” audit finanÃ§abilitÃ© |

---

## Annexe A â€” DÃ©pendances critiques

**APIs externes** :
- Anthropic Claude Sonnet 4: latence ~2-5s/note, coÃ»t ~$0.02-0.05/note
- LiveKit (audio): optionnel pour MVP, peut Ãªtre mockÃ©
- Email (SMTP): pour registration/verification

**Infrastructure** :
- PostgreSQL (ou SQLite dev): BDD persistante
- Nginx 1.27: reverse proxy + TLS
- Uvicorn: serveur ASGI

**Librairies Python** :
- FastAPI 0.110+, SQLAlchemy 2.0+, Pydantic 2.1+, pytest 8.1+

---

## Annexe B â€” Checklist de dÃ©ploiement MVP

- [ ] Tests BLOC 1 passants (moteur IA)
- [ ] Tests BLOC 2 passants (analyse intake)
- [ ] Logs pas de leak data sensible
- [ ] Anthropic key valide + budget
- [ ] Fixtures de test anonymisÃ©es
- [ ] Frontend accessible (curl OK)
- [ ] DÃ©mo scÃ©nario validÃ©e
- [ ] Docs pour financeur

---
titre: Livrables de validation MERLIN/IVIA — Résumé exécutif (6 livrables)
id: PROD-VALID-002
statut: active
type: audit
couche: PROD
périmètre: synthèse pour décision
auteur: fondateur
date: 2026-05-05
version: 1.0
dépend_de: [PROD-VALID-001]
remplace: []
arbitrage_requis: non
source_canonique: 11_PROMPTS/PROD-VALID-002-LIVRABLES_SYNTHESE_V1.md
---

# PROD-VALID — Livrables synthétiques (6/7)

> **Format** : exécutif (une page par livrable)
> **Audience** : fondateur + décideur technique
> **Lecture estimée** : 15 min total

---

## LIVRABLE 2 — Prompts critiques reliés au moteur

### État global
Externalisation Phase A complétée (2026-05-05). Les 3 prompts critiques sont dans `11_PROMPTS/02_METH/` et chargés dynamiquement au runtime.

### Table prompts

| ID | Fichier | Rôle | Lignes | Versionné | Testé | État |
|---|---|---|---|---|---|---|
| METH-001 | `METH-001-quebec-context-hypotheses-v1.md` | 9 hypothèses contextuelles | 10 | ✅ git | ⚠️ loader only | ✅ Actif |
| METH-002 | `METH-002-quebec-context-signals-v1.md` | 12 signaux d'alerte | 13 | ✅ git | ⚠️ loader only | ✅ Actif |
| METH-003 | `METH-003-session-note-cercle-system-prompt-v1.md` | Prompt système MERLIN (la persona) | 90+ | ✅ git | ❌ **NON** | **CRITIQUE** |

### Prompts **encore hardcodés ou fragiles**

| Localisation | Nature | Priorité |
|---|---|---|
| `app/ai/anthropic_session_note_pipeline.py` (lignes 1-60) | Pipeline API Anthropic (pas hardcodé mais pas validé) | P2 |
| `app/ai/prompts/session_note_cercle_v1.py` (lignes 280+) | render_session_note_cercle_prompt() — logique combintoire | P1 |
| `app/services/intake_analysis.py` (lignes 30-60) | Patterns regex (pas prompt IA mais règles métier) | P2 |

### Points de risque prompts

❌ **AUCUN TEST RÉEL** sur la qualité de la note générée par Claude
❌ **AUCUN TEST** sur injection des hypothèses/signaux dans le prompt système
⚠️ **MODIFICATION PROMPT** = modification fichier Markdown + git commit (OK mais discipline requise)

### Recommandation
Créer `test_prompt_injection.py` (1 jour) pour vérifier que METH-001/002/003 contiennent exactement ce qu'on attend avant tout changement.

---

## LIVRABLE 3 — Inventaire des tests existants

### Récapitulatif

**Total tests** : ~7 fichiers, ~400 lignes, 5 tests exécutables + 2 scripts manuels

| Fichier | Nb tests | Type | Exécutable | État |
|---|---|---|---|---|
| `test_prompt_loader.py` | 3 | unitaire | ✅ pytest | ✅ 3 passed |
| `test_api_smoke.py` | 1 | smoke (flux) | ✅ pytest | ⚠️ moque Claude |
| `test_register.py` | 1 | HTTP manual | ⚠️ script | exige serveur |
| `test_register_https.py` | 1 | HTTP manual | ⚠️ script | exige serveur |
| `check_routes.py` | — | audit | ⚠️ script | énumère routes |

### Tests par domaine

```
Moteur IA (Claude Sonnet 4)       : ❌ 0 tests réels  (mocké dans smoke)
Prompts (METH-*)                   : ⚠️ 3 tests loader (pas test contenu)
Analyse intake (regex)              : ❌ 0 tests
Génération documents clients        : ❌ 0 tests
Authentification/JWT                : ⚠️ ~1-2 indirect
Supervision (validation)            : ❌ 0 tests
Routes CRUD (clients, sessions)     : ⚠️ ~1-2 indirect (smoke moque)
BDD/migrations (Alembic)            : ❌ 0 tests
LiveKit integration                 : ❌ 0 tests (complexe, dépend externe)
```

### Couverture estimée : **~5-10%** (très faible)

---

## LIVRABLE 4 — Tests manquants prioritaires (7 tests)

### Ordre de priorité

#### URGENT (P1 — semaine 1)

| Nom test | Fichier | Lignes | Délai | Raison |
|---|---|---|---|---|
| `test_session_note_generation_real_claude` | `tests/test_session_note_generation.py` | ~80 | 1-2j | **Cœur du moteur** |
| `test_json_schema_validation` | `tests/test_json_schema_validation.py` | ~60 | 1j | Garantir format sortie |
| `test_intake_analysis_risk_patterns` | `tests/test_intake_analysis.py` | ~70 | 1-2j | **Sécurité (risque)** |
| `test_prompt_injection` | `tests/test_prompt_injection.py` | ~40 | 0,5j | Vérifier prompts actifs |

#### HAUTE (P2 — semaine 2)

| Nom test | Fichier | Lignes | Délai | Raison |
|---|---|---|---|---|
| `test_e2e_session_flow_real` | `tests/test_e2e_real.py` | ~100 | 1-2j | Flux complet réel |
| `test_supervisor_validation` | `tests/test_supervisor.py` | ~80 | 1-2j | Workflow supervison |
| `test_intake_analysis_gaps` | `tests/test_intake_analysis.py` | ~40 | 0,5j | Data quality |

### Checklist test METH-003 (avant réelle démo)

```
[ ] Claude génère JSON valide (parsable)
[ ] Schéma contient tous les champs obligatoires
[ ] Tous les codes énumérés sont valides
[ ] vigilance_level_code ∈ {non_urgent, watch, priority, urgent}
[ ] context_hypotheses_json n'apparaît pas en client_delivery
[ ] metadata.prompt_version == "session_note_cercle_v1"
```

---

## LIVRABLE 5 — MVP démontrable (1 page)

### Le pitch en 3 min (pour financeur)

**"Voici comment MERLIN transforme une demande client en rapport structuré :"**

```
Client saisit: "Je suis fatigué, j'ai mal, j'ai peur d'aller au travail"
                     ↓
        [INTAKE ANALYSIS — détecte signaux risque/santé]
                     ↓
        Client réserve session audio 20-30 min
                     ↓
        [CLAUDE MOTEUR — analyse transcription selon Cercle V1]
        ├─ 4 dimensions (coeur/corps/esprit/etre)
        ├─ Contextualisation québécoise (9 hypothèses)
        ├─ Alertes de sécurité (vigilance_level)
        └─ Document structuré pour client
                     ↓
        Superviseur valide
                     ↓
        CLIENT VOIT: "Votre séance du XX — synthèse professionnelle"
                     (formulation simple, rassurante, intelligible)
```

### Points de preuve technique

1. **Moteur marche réellement** : note générée en <3s, schéma JSON valide
2. **Grille Cercle V1 appliquée** : 4 dimensions analysées + tensions identifiées
3. **Sécurité intégrée** : vigilance_level automatique (urgent si besoin)
4. **Traçabilité** : version prompt + modèle enregistrée
5. **Supervision fonctionnelle** : validateur humain gate-keep avant diffusion
6. **Document client professionnel** : pas brut, formulé intelligible

### Durée démo : 8-10 min (live ou enregistré)

---

## LIVRABLE 6 — Plan 14 jours (chronologie)

### Semaine 1 : Tests moteur

```
Jour 1   | test_session_note_generation_real_claude    | ← CRITICAL PATH
Jour 2   | test_json_schema_validation
Jour 3   | test_prompt_injection (0.5j) + test_intake_analysis
Jour 4   | Fixtures + conftest.py setup
Jour 5   | Run all tests, fix failures
Jour 6-7 | test_e2e_session_flow_real
```

### Semaine 2 : Finalisation + démo

```
Jour 8    | test_supervisor_validation_flow
Jour 9-10 | Validation Pydantic schema + logging
Jour 11-12| Préparation démo + anonymisation données
Jour 13   | Démo interne + refinement
Jour 14   | Démo finale (financeur) + débriefing
```

### Points critique sur le path
- J1 : `test_session_note_generation_real_claude` réussit ou démo compromise
- J5 : tous les tests P1 passent ou pivot nécessaire
- J8 : E2E réel exécutable

### Dépendances externes
- ✅ Anthropic API key actif + budget
- ✅ Pas de changements archi (use existing code)
- ✅ LiveKit optionnel (mock OK)

---

## LIVRABLE 7 — Fichiers à modifier (liste exacte)

### À CRÉER (tests nouveaux)

```
tests/
├── test_session_note_generation.py           [CREER — Claude real]
├── test_json_schema_validation.py            [CREER — schema check]
├── test_prompt_injection.py                  [CREER — verify METH-*]
├── test_intake_analysis.py                   [CREER — patterns + gaps]
├── test_e2e_real.py                          [CREER — end-to-end]
├── test_supervisor.py                        [CREER — validation WF]
├── conftest.py                               [CREER — pytest fixtures]
├── fixtures.py                               [CREER — test data]
└── test_prompt_loader.py                     [MODIFIER — ajouter tests]
```

### À MODIFIER (code backend)

**Dossier `app/ai/`** :
- `anthropic_session_note_pipeline.py` — ajouter validation schéma output
- `prompts/session_note_cercle_v1.py` — ajouter docstring détaillé

**Dossier `app/services/`** :
- `intake_analysis.py` — ajouter logging patterns + externaliser regex
- `session_documents.py` — assertions d'intégrité (no supervision in client)

**Dossier `app/api/routes/`** :
- `session_notes.py` — ajouter endpoint validation schéma

### À CRÉER (documentation + gouvernance)

**Backend** :
- `10_backend_merlin_api/TESTING_STRATEGY.md` — guide test + fixtures
- `10_backend_merlin_api/PROMPT_LOADER_USAGE.md` — how-to charger prompts

**Gouvernance** :
- `11_PROMPTS/PROD-VALID-002-LIVRABLES_SYNTHESE_V1.md` — ce document
- `00_GOUVERNANCE/MERLIN_GOUV_REGISTRE_DECISIONS_REVISIONS_IVIA_MERLIN_V1.md` — ajouter DEC-041

**Optionnel (post-démo)** :
- `11_PROMPTS/PROD-VALID-003-RESULTATS_MVP.md` — résultats démo finale
- `00_GOUVERNANCE/MERLIN_GOUV_DECISION_FINANCEMENT_MVP.md` — décision post-démo

---

## Sommaire 1 page — Toute l'histoire

| Livrable | Fichier | État | Verdict |
|---|---|---|---|
| 1 — Cartographie moteur | PROD-VALID-001 | ✅ Créé | Moteur stable, prompt externalisés, tests manquants |
| 2 — Prompts critiques | Section 2.1-2.4 PROD-VALID-001 | ✅ Créé | 3 prompts actifs + 3 zones fragiles |
| 3 — Tests existants | LIVRABLE 3 ci-dessus | ✅ Créé | ~7 tests, couverture 5-10%, urgent combler |
| 4 — Tests manquants | LIVRABLE 4 ci-dessus | ✅ Créé | 7 tests prioritaires, 5-8 jours |
| 5 — MVP démontrable | LIVRABLE 5 ci-dessus | ✅ Créé | Scénario 8-10 min, 3 points preuve |
| 6 — Plan 14 jours | LIVRABLE 6 ci-dessus | ✅ Créé | Chronologie semaine 1-2, path critique |
| 7 — Fichiers à modifier | LIVRABLE 7 ci-dessus | ✅ Créé | 8 fichiers test + 6 modifs backend |

---

## Décision rapide pour fondateur

**PROPOSÉ** : lancer immédiatement les tests P1 (BLOC 1-2).

**Raison** : le moteur est le cœur. Sans preuve qu'il fonctionne réellement (pas mocké), impossible de demander financement.

**Effort** : 3-4 jours de dev pour avoir les 4 tests P1 passants + MVP démontrable.

**Risque** : si Claude API n'est pas dispo ou trop coûteux, MVP non viable.

**Recommandation** : Valider avec Anthropic:
- API key actif
- Budget pour ~500 appels test (estimation: $10-15)
- Latence acceptable (<5s par note)

---

## Historique

| Version | Date | Auteur | Nature |
|---|---|---|---|
| 1.0 | 2026-05-05 | fondateur | Création — 7 livrables synthétiques |

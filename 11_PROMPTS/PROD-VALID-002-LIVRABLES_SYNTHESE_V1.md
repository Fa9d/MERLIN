---
titre: Livrables de validation MERLIN/IVIA â€” RÃ©sumÃ© exÃ©cutif (6 livrables)
id: PROD-VALID-002
statut: active
type: audit
couche: PROD
pÃ©rimÃ¨tre: synthÃ¨se pour dÃ©cision
auteur: fondateur
date: 2026-05-05
version: 1.0
dÃ©pend_de: [PROD-VALID-001]
remplace: []
arbitrage_requis: non
source_canonique: 11_PROMPTS/PROD-VALID-002-LIVRABLES_SYNTHESE_V1.md
test_associe: test_json_schema_validation.py::test_prod009_validation_schema
impact_attendu: "A documenter lors de la prochaine modification"
---

# PROD-VALID â€” Livrables synthÃ©tiques (6/7)

> **Format** : exÃ©cutif (une page par livrable)
> **Audience** : fondateur + dÃ©cideur technique
> **Lecture estimÃ©e** : 15 min total

---

## LIVRABLE 2 â€” Prompts critiques reliÃ©s au moteur

### Ã‰tat global
Externalisation Phase A complÃ©tÃ©e (2026-05-05). Les 3 prompts critiques sont dans `11_PROMPTS/02_METH/` et chargÃ©s dynamiquement au runtime.

### Table prompts

| ID | Fichier | RÃ´le | Lignes | VersionnÃ© | TestÃ© | Ã‰tat |
|---|---|---|---|---|---|---|
| METH-001 | `METH-001-quebec-context-hypotheses-v1.md` | 9 hypothÃ¨ses contextuelles | 10 | âœ… git | âš ï¸ loader only | âœ… Actif |
| METH-002 | `METH-002-quebec-context-signals-v1.md` | 12 signaux d'alerte | 13 | âœ… git | âš ï¸ loader only | âœ… Actif |
| METH-003 | `METH-003-session-note-cercle-system-prompt-v1.md` | Prompt systÃ¨me MERLIN (la persona) | 90+ | âœ… git | âŒ **NON** | **CRITIQUE** |

### Prompts **encore hardcodÃ©s ou fragiles**

| Localisation | Nature | PrioritÃ© |
|---|---|---|
| `app/ai/anthropic_session_note_pipeline.py` (lignes 1-60) | Pipeline API Anthropic (pas hardcodÃ© mais pas validÃ©) | P2 |
| `app/ai/prompts/session_note_cercle_v1.py` (lignes 280+) | render_session_note_cercle_prompt() â€” logique combintoire | P1 |
| `app/services/intake_analysis.py` (lignes 30-60) | Patterns regex (pas prompt IA mais rÃ¨gles mÃ©tier) | P2 |

### Points de risque prompts

âŒ **AUCUN TEST RÃ‰EL** sur la qualitÃ© de la note gÃ©nÃ©rÃ©e par Claude
âŒ **AUCUN TEST** sur injection des hypothÃ¨ses/signaux dans le prompt systÃ¨me
âš ï¸ **MODIFICATION PROMPT** = modification fichier Markdown + git commit (OK mais discipline requise)

### Recommandation
CrÃ©er `test_prompt_injection.py` (1 jour) pour vÃ©rifier que METH-001/002/003 contiennent exactement ce qu'on attend avant tout changement.

---

## LIVRABLE 3 â€” Inventaire des tests existants

### RÃ©capitulatif

**Total tests** : ~7 fichiers, ~400 lignes, 5 tests exÃ©cutables + 2 scripts manuels

| Fichier | Nb tests | Type | ExÃ©cutable | Ã‰tat |
|---|---|---|---|---|
| `test_prompt_loader.py` | 3 | unitaire | âœ… pytest | âœ… 3 passed |
| `test_api_smoke.py` | 1 | smoke (flux) | âœ… pytest | âš ï¸ moque Claude |
| `test_register.py` | 1 | HTTP manual | âš ï¸ script | exige serveur |
| `test_register_https.py` | 1 | HTTP manual | âš ï¸ script | exige serveur |
| `check_routes.py` | â€” | audit | âš ï¸ script | Ã©numÃ¨re routes |

### Tests par domaine

```
Moteur IA (Claude Sonnet 4)       : âŒ 0 tests rÃ©els  (mockÃ© dans smoke)
Prompts (METH-*)                   : âš ï¸ 3 tests loader (pas test contenu)
Analyse intake (regex)              : âŒ 0 tests
GÃ©nÃ©ration documents clients        : âŒ 0 tests
Authentification/JWT                : âš ï¸ ~1-2 indirect
Supervision (validation)            : âŒ 0 tests
Routes CRUD (clients, sessions)     : âš ï¸ ~1-2 indirect (smoke moque)
BDD/migrations (Alembic)            : âŒ 0 tests
LiveKit integration                 : âŒ 0 tests (complexe, dÃ©pend externe)
```

### Couverture estimÃ©e : **~5-10%** (trÃ¨s faible)

---

## LIVRABLE 4 â€” Tests manquants prioritaires (7 tests)

### Ordre de prioritÃ©

#### URGENT (P1 â€” semaine 1)

| Nom test | Fichier | Lignes | DÃ©lai | Raison |
|---|---|---|---|---|
| `test_session_note_generation_real_claude` | `tests/test_session_note_generation.py` | ~80 | 1-2j | **CÅ“ur du moteur** |
| `test_json_schema_validation` | `tests/test_json_schema_validation.py` | ~60 | 1j | Garantir format sortie |
| `test_intake_analysis_risk_patterns` | `tests/test_intake_analysis.py` | ~70 | 1-2j | **SÃ©curitÃ© (risque)** |
| `test_prompt_injection` | `tests/test_prompt_injection.py` | ~40 | 0,5j | VÃ©rifier prompts actifs |

#### HAUTE (P2 â€” semaine 2)

| Nom test | Fichier | Lignes | DÃ©lai | Raison |
|---|---|---|---|---|
| `test_e2e_session_flow_real` | `tests/test_e2e_real.py` | ~100 | 1-2j | Flux complet rÃ©el |
| `test_supervisor_validation` | `tests/test_supervisor.py` | ~80 | 1-2j | Workflow supervison |
| `test_intake_analysis_gaps` | `tests/test_intake_analysis.py` | ~40 | 0,5j | Data quality |

### Checklist test METH-003 (avant rÃ©elle dÃ©mo)

```
[ ] Claude gÃ©nÃ¨re JSON valide (parsable)
[ ] SchÃ©ma contient tous les champs obligatoires
[ ] Tous les codes Ã©numÃ©rÃ©s sont valides
[ ] vigilance_level_code âˆˆ {non_urgent, watch, priority, urgent}
[ ] context_hypotheses_json n'apparaÃ®t pas en client_delivery
[ ] metadata.prompt_version == "session_note_cercle_v1"
```

---

## LIVRABLE 5 â€” MVP dÃ©montrable (1 page)

### Le pitch en 3 min (pour financeur)

**"Voici comment MERLIN transforme une demande client en rapport structurÃ© :"**

```
Client saisit: "Je suis fatiguÃ©, j'ai mal, j'ai peur d'aller au travail"
                     â†“
        [INTAKE ANALYSIS â€” dÃ©tecte signaux risque/santÃ©]
                     â†“
        Client rÃ©serve session audio 20-30 min
                     â†“
        [CLAUDE MOTEUR â€” analyse transcription selon Cercle V1]
        â”œâ”€ 4 dimensions (coeur/corps/esprit/etre)
        â”œâ”€ Contextualisation quÃ©bÃ©coise (9 hypothÃ¨ses)
        â”œâ”€ Alertes de sÃ©curitÃ© (vigilance_level)
        â””â”€ Document structurÃ© pour client
                     â†“
        Superviseur valide
                     â†“
        CLIENT VOIT: "Votre sÃ©ance du XX â€” synthÃ¨se professionnelle"
                     (formulation simple, rassurante, intelligible)
```

### Points de preuve technique

1. **Moteur marche rÃ©ellement** : note gÃ©nÃ©rÃ©e en <3s, schÃ©ma JSON valide
2. **Grille Cercle V1 appliquÃ©e** : 4 dimensions analysÃ©es + tensions identifiÃ©es
3. **SÃ©curitÃ© intÃ©grÃ©e** : vigilance_level automatique (urgent si besoin)
4. **TraÃ§abilitÃ©** : version prompt + modÃ¨le enregistrÃ©e
5. **Supervision fonctionnelle** : validateur humain gate-keep avant diffusion
6. **Document client professionnel** : pas brut, formulÃ© intelligible

### DurÃ©e dÃ©mo : 8-10 min (live ou enregistrÃ©)

---

## LIVRABLE 6 â€” Plan 14 jours (chronologie)

### Semaine 1 : Tests moteur

```
Jour 1   | test_session_note_generation_real_claude    | â† CRITICAL PATH
Jour 2   | test_json_schema_validation
Jour 3   | test_prompt_injection (0.5j) + test_intake_analysis
Jour 4   | Fixtures + conftest.py setup
Jour 5   | Run all tests, fix failures
Jour 6-7 | test_e2e_session_flow_real
```

### Semaine 2 : Finalisation + dÃ©mo

```
Jour 8    | test_supervisor_validation_flow
Jour 9-10 | Validation Pydantic schema + logging
Jour 11-12| PrÃ©paration dÃ©mo + anonymisation donnÃ©es
Jour 13   | DÃ©mo interne + refinement
Jour 14   | DÃ©mo finale (financeur) + dÃ©briefing
```

### Points critique sur le path
- J1 : `test_session_note_generation_real_claude` rÃ©ussit ou dÃ©mo compromise
- J5 : tous les tests P1 passent ou pivot nÃ©cessaire
- J8 : E2E rÃ©el exÃ©cutable

### DÃ©pendances externes
- âœ… Anthropic API key actif + budget
- âœ… Pas de changements archi (use existing code)
- âœ… LiveKit optionnel (mock OK)

---

## LIVRABLE 7 â€” Fichiers Ã  modifier (liste exacte)

### Ã€ CRÃ‰ER (tests nouveaux)

```
tests/
â”œâ”€â”€ test_session_note_generation.py           [CREER â€” Claude real]
â”œâ”€â”€ test_json_schema_validation.py            [CREER â€” schema check]
â”œâ”€â”€ test_prompt_injection.py                  [CREER â€” verify METH-*]
â”œâ”€â”€ test_intake_analysis.py                   [CREER â€” patterns + gaps]
â”œâ”€â”€ test_e2e_real.py                          [CREER â€” end-to-end]
â”œâ”€â”€ test_supervisor.py                        [CREER â€” validation WF]
â”œâ”€â”€ conftest.py                               [CREER â€” pytest fixtures]
â”œâ”€â”€ fixtures.py                               [CREER â€” test data]
â””â”€â”€ test_prompt_loader.py                     [MODIFIER â€” ajouter tests]
```

### Ã€ MODIFIER (code backend)

**Dossier `app/ai/`** :
- `anthropic_session_note_pipeline.py` â€” ajouter validation schÃ©ma output
- `prompts/session_note_cercle_v1.py` â€” ajouter docstring dÃ©taillÃ©

**Dossier `app/services/`** :
- `intake_analysis.py` â€” ajouter logging patterns + externaliser regex
- `session_documents.py` â€” assertions d'intÃ©gritÃ© (no supervision in client)

**Dossier `app/api/routes/`** :
- `session_notes.py` â€” ajouter endpoint validation schÃ©ma

### Ã€ CRÃ‰ER (documentation + gouvernance)

**Backend** :
- `10_backend_merlin_api/TESTING_STRATEGY.md` â€” guide test + fixtures
- `10_backend_merlin_api/PROMPT_LOADER_USAGE.md` â€” how-to charger prompts

**Gouvernance** :
- `11_PROMPTS/PROD-VALID-002-LIVRABLES_SYNTHESE_V1.md` â€” ce document
- `00_GOUVERNANCE/MERLIN_GOUV_REGISTRE_DECISIONS_REVISIONS_IVIA_MERLIN_V1.md` â€” ajouter DEC-041

**Optionnel (post-dÃ©mo)** :
- `11_PROMPTS/PROD-VALID-003-RESULTATS_MVP.md` â€” rÃ©sultats dÃ©mo finale
- `00_GOUVERNANCE/MERLIN_GOUV_DECISION_FINANCEMENT_MVP.md` â€” dÃ©cision post-dÃ©mo

---

## Sommaire 1 page â€” Toute l'histoire

| Livrable | Fichier | Ã‰tat | Verdict |
|---|---|---|---|
| 1 â€” Cartographie moteur | PROD-VALID-001 | âœ… CrÃ©Ã© | Moteur stable, prompt externalisÃ©s, tests manquants |
| 2 â€” Prompts critiques | Section 2.1-2.4 PROD-VALID-001 | âœ… CrÃ©Ã© | 3 prompts actifs + 3 zones fragiles |
| 3 â€” Tests existants | LIVRABLE 3 ci-dessus | âœ… CrÃ©Ã© | ~7 tests, couverture 5-10%, urgent combler |
| 4 â€” Tests manquants | LIVRABLE 4 ci-dessus | âœ… CrÃ©Ã© | 7 tests prioritaires, 5-8 jours |
| 5 â€” MVP dÃ©montrable | LIVRABLE 5 ci-dessus | âœ… CrÃ©Ã© | ScÃ©nario 8-10 min, 3 points preuve |
| 6 â€” Plan 14 jours | LIVRABLE 6 ci-dessus | âœ… CrÃ©Ã© | Chronologie semaine 1-2, path critique |
| 7 â€” Fichiers Ã  modifier | LIVRABLE 7 ci-dessus | âœ… CrÃ©Ã© | 8 fichiers test + 6 modifs backend |

---

## DÃ©cision rapide pour fondateur

**PROPOSÃ‰** : lancer immÃ©diatement les tests P1 (BLOC 1-2).

**Raison** : le moteur est le cÅ“ur. Sans preuve qu'il fonctionne rÃ©ellement (pas mockÃ©), impossible de demander financement.

**Effort** : 3-4 jours de dev pour avoir les 4 tests P1 passants + MVP dÃ©montrable.

**Risque** : si Claude API n'est pas dispo ou trop coÃ»teux, MVP non viable.

**Recommandation** : Valider avec Anthropic:
- API key actif
- Budget pour ~500 appels test (estimation: $10-15)
- Latence acceptable (<5s par note)

---

## Historique

| Version | Date | Auteur | Nature |
|---|---|---|---|
| 1.0 | 2026-05-05 | fondateur | CrÃ©ation â€” 7 livrables synthÃ©tiques |

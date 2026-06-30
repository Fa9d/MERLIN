---
titre: Index de la bibliothèque de prompts — MERLIN
id: MERLIN-INDEX-PROMPTS-V1
statut: active
type: charte
couche: PROD
périmètre: 11_PROMPTS
auteur: fondateur
date: 2026-05-05
version: 1.0
dépend_de: [ADR-0002, MERLIN-MODELE-COUCHES-V1]
remplace: [README.md (non structuré)]
arbitrage_requis: non
source_canonique: 11_PROMPTS/INDEX_PROMPTS_V1.md
---

# MERLIN — Index de la bibliothèque de prompts V1

> **Porte d'entrée humaine dans `11_PROMPTS/`**
> **Statut** : active — 2026-05-05
> **Décision formelle** : ADR-0002

---

## Rôle de `11_PROMPTS/`

`11_PROMPTS/` est la **bibliothèque canonique de prompts de MERLIN**.

Elle contient l'ensemble des instructions destinées aux modèles IA (Anthropic Claude et tout
futur modèle) utilisés par le système MERLIN / IVIA.

Chaque prompt dans cette bibliothèque est :
- **versionné** : tout changement de logique déclenche un bump de version,
- **localisé** : un prompt = un fichier, dans un dossier de couche,
- **auditable** : ses métadonnées permettent de savoir qui l'a créé, quand, et pour quel usage,
- **relié à une couche** : chaque prompt appartient à FOND, METH, EDIT, ADMIN ou PROD.

**Un prompt non présent dans cette bibliothèque n'est pas un prompt gouverné.**
Il peut exister dans le code comme valeur temporaire mais doit être migré avant
toute mise en production d'une fonctionnalité qui l'utilise.

---

## Structure cible (Vague 2)

```
11_PROMPTS/
├── INDEX_PROMPTS_V1.md              ← ce fichier
├── PROMPTS_CONVENTION_NOMMAGE_V1.md ← règles de nommage et version
├── PROMPTS_STANDARD_METADATA_V1.md  ← standard de métadonnées
├── AUDIT_PROMPTS_EXISTANTS_V1.md    ← rapport d'audit Vague 2
│
├── 00_SYSTEME/    ← prompts système globaux (identité MERLIN, contraintes absolues)
├── 01_FOND/       ← prompts liés à la couche FOND (doctrine, contexte culturel)
├── 02_METH/       ← prompts liés à la couche METH (triage, orientation, notes de séance)
├── 03_EDIT/       ← prompts liés à la couche EDIT (génération de contenus publics)
├── 04_ADMIN/      ← prompts administratifs (onboarding, routage, audit dossier)
├── 05_PROD/       ← prompts techniques/infrastructure (validation, tests, logs)
└── 06_CSUITE/     ← gouvernance souveraine : agents C-suite de pilotage (ADR-0008)
```

**Note sur la migration :** les sous-dossiers `01_session/`, `02_document/`, `03_supervision/`,
`04_admin/`, `05_pilote/` sont la structure héritée. Ils sont conservés sans modification jusqu'à
la migration traçable définie dans `AUDIT_PROMPTS_EXISTANTS_V1.md`.

---

## Description des couches de prompts

| Dossier | Couche MERLIN | Rôle |
|---|---|---|
| `00_SYSTEME/` | — (transversal) | Prompts d'identité système globaux. Définissent qui est MERLIN dans toute interaction IA. |
| `01_FOND/` | FOND | Prompts qui mobilisent les fondements, la doctrine, le cadre culturel québécois ou autochtone. |
| `02_METH/` | METH | Prompts qui implémentent les méthodes : note de séance Cercle V1, triage, orientation, supervision. |
| `03_EDIT/` | EDIT | Prompts qui génèrent des contenus publics : lettres client, pages web, offres, calendriers. |
| `04_ADMIN/` | ADMIN | Prompts d'administration : onboarding, routage de demande, audit de dossier. |
| `05_PROD/` | PROD | Prompts techniques : validation de contenu, tests, pilote, schémas de sortie. |

---

## Inventaire des prompts existants (état au 2026-05-05)

### Structure héritée — à migrer (Vague 3)

| Fichier actuel | Emplacement | Couche cible | Dossier cible |
|---|---|---|---|
| `PROMPT_note_clinique.md` | `01_session/` | METH | `02_METH/` |
| `PROMPT_resume_session.md` | `01_session/` | METH | `02_METH/` |
| `PROMPT_generation_rapport.md` | `02_document/` | METH | `02_METH/` |
| `PROMPT_validation_contenu.md` | `02_document/` | PROD | `05_PROD/` |
| `PROMPT_flags_anomalies.md` | `03_supervision/` | METH | `02_METH/` |
| `PROMPT_relecture_note.md` | `03_supervision/` | METH | `02_METH/` |
| `PROMPT_audit_dossier.md` | `04_admin/` | ADMIN | `04_ADMIN/` |
| `PROMPT_onboarding_client.md` | `04_admin/` | ADMIN | `04_ADMIN/` |
| `PROMPT_validation_pilote.md` | `05_pilote/` | PROD | `05_PROD/` |

### Prompts critiques backend (externalises — Vague 3 Phase A)

| Prompt | Fichier backend | Couche | Statut |
|---|---|---|---|
| `SESSION_NOTE_CERCLE_SYSTEM_PROMPT` | `app/ai/prompts/session_note_cercle_v1.py` | METH (CRITIQUE) | Externalise via `02_METH/METH-003-session-note-cercle-system-prompt-v1.md` |
| `QUEBEC_CONTEXT_HYPOTHESES` | `app/ai/prompts/session_note_cercle_v1.py` | FOND | Externalise via `02_METH/METH-001-quebec-context-hypotheses-v1.md` |
| `QUEBEC_CONTEXT_SIGNALS` | `app/ai/prompts/session_note_cercle_v1.py` | FOND | Externalise via `02_METH/METH-002-quebec-context-signals-v1.md` |

### Nouveaux prompts gouvernes en `02_METH/`

| ID court | Fichier | Usage |
|---|---|---|
| `METH-001` | `02_METH/METH-001-quebec-context-hypotheses-v1.md` | Hypotheses contextuelles Quebec chargees par backend |
| `METH-002` | `02_METH/METH-002-quebec-context-signals-v1.md` | Signaux contextuels Quebec charges par backend |
| `METH-003` | `02_METH/METH-003-session-note-cercle-system-prompt-v1.md` | Prompt systeme principal note de seance Cercle V1 |

Voir `AUDIT_PROMPTS_EXISTANTS_V1.md` pour le détail.

---

## Ordre de lecture recommandé

1. `PROMPTS_CONVENTION_NOMMAGE_V1.md` — comprendre les règles de nommage
2. `PROMPTS_STANDARD_METADATA_V1.md` — comprendre les métadonnées obligatoires
3. `AUDIT_PROMPTS_EXISTANTS_V1.md` — état de la bibliothèque et plan de migration
4. Dossiers couche par couche, en partant de `02_METH/` (le plus peuplé)

---

## Règles de maintenance

- Tout nouveau prompt doit d'abord être créé dans ce dossier (avec métadonnées), **avant** d'être intégré dans le code.
- Tout changement de logique = bump de version du fichier Markdown + bump dans le code.
- Tout nouveau prompt de couche METH ou FOND (à impact clinique ou culturel) = arbitrage requis.
- Ce fichier INDEX doit être mis à jour à chaque ajout de prompt gouverné.

---

## Historique de révisions

| Version | Date | Auteur | Nature de la révision |
|---|---|---|---|
| 1.1 | 2026-05-05 | fondateur | Mise a jour Vague 3 — ajout METH-001/002/003 et statut externalise Phase A |
| 1.0 | 2026-05-05 | fondateur | Création initiale — Vague 2 structuration prompts |
| 1.2 | 2026-05-05 | fondateur | Vague 4 — ajout frontmatter YAML PROD-001 à PROD-009, enregistrement dans prompt_loader |

---

## Registre Vague 4 — Couche PROD

| ID | Fichier | Dossier | Trigger | Statut |
|---|---|---|---|---|
| PROD-001 | PROMPT_note_clinique.md | 01_session/ | apres_cloture_session_audio | production |
| PROD-002 | PROMPT_resume_session.md | 01_session/ | apres_generation_note_clinique | production |
| PROD-003 | PROMPT_generation_rapport.md | 02_document/ | apres_validation_superviseur_note | production |
| PROD-004 | PROMPT_validation_contenu.md | 02_document/ | avant_client_visible_true | production |
| PROD-005 | PROMPT_relecture_note.md | 03_supervision/ | note_clinique_soumise_en_attente_validation | production |
| PROD-006 | PROMPT_flags_anomalies.md | 03_supervision/ | analyse_note_clinique_post_generation | production |
| PROD-007 | PROMPT_onboarding_client.md | 04_admin/ | creation_nouveau_dossier_client | production |
| PROD-008 | PROMPT_audit_dossier.md | 04_admin/ | revue_periodique_dossier_client | production |
| PROD-009 | PROMPT_validation_pilote.md | 05_pilote/ | fin_phase_pilote_evaluation | production |



---

## Registre Vague 5 — METH-004

| ID | Fichier | Dossier | Trigger | Statut |
|---|---|---|---|---|
| METH-004 | METH-004-triage-signaux-urgence-v1.md | 02_METH/ | analyse_intake_text_appellee | production |

---

## Historique de révisions (suite)

| Version | Date | Auteur | Nature de la révision |
|---|---|---|---|
| 1.3 | 2026-05-05 | fondateur | Vague 5 Phase C — création METH-004, enregistrement loader, 13 prompts total |

---

## Registre Vague 6 — Couche SYSTEME (agents C-suite)

> Vague 6 — 2026-06-29 — Création des 6 agents C-suite stratégiques

| ID | Fichier | Dossier | Trigger | Statut |
|---|---|---|---|---|
| MERLIN-PROMPT-CSUITE-STRAT-V1 | MERLIN_PROMPT_CSUITE-STRAT_v1.0.md | 06_CSUITE/ | Décision structurante, ADR, revue roadmap | active |
| MERLIN-PROMPT-CSUITE-ARCH-V1 | MERLIN_PROMPT_CSUITE-ARCH_v1.0.md | 06_CSUITE/ | Choix d'implémentation, migration Alembic, revue stack | active |
| MERLIN-PROMPT-CSUITE-COMM-V1 | MERLIN_PROMPT_CSUITE-COMM_v1.0.md | 06_CSUITE/ | Contenu externe, dossier financement, voix de marque | active |
| MERLIN-PROMPT-CSUITE-UX-V1 | MERLIN_PROMPT_CSUITE-UX_v1.0.md | 06_CSUITE/ | Nouveau composant frontend, parcours utilisateur | active |
| MERLIN-PROMPT-CSUITE-FIN-V1 | MERLIN_PROMPT_CSUITE-FIN_v1.0.md | 06_CSUITE/ | ROI module, revue financière mensuelle, tarification | active |
| MERLIN-PROMPT-CSUITE-QA-V1 | MERLIN_PROMPT_CSUITE-QA_v1.0.md | 06_CSUITE/ | Revue PR, validation migration, monitoring production | active |

Total bibliothèque après Vague 6 : **19 prompts gouvernés**

---

## Historique de révisions (suite)

| Version | Date | Auteur | Nature de la révision |
|---|---|---|---|
| 1.4 | 2026-06-29 | fondateur | Vague 6 — ajout 6 agents C-suite (SYSTEME), 19 prompts total |

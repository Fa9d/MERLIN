---
titre: Audit des prompts existants — MERLIN
id: MERLIN-AUDIT-PROMPTS-V1
statut: active
type: audit
couche: PROD
périmètre: 11_PROMPTS + 10_backend_merlin_api
auteur: fondateur
date: 2026-05-05
version: 1.0
dépend_de: [ADR-0002, PROMPTS-CONVENTION-NOMMAGE-V1]
remplace: []
arbitrage_requis: non — rapport d'état
source_canonique: 11_PROMPTS/AUDIT_PROMPTS_EXISTANTS_V1.md
---

# MERLIN — Audit des prompts existants V1

> **Date d'exécution** : 2026-05-05
> **Périmètre** : `11_PROMPTS/` + `10_backend_merlin_api/app/ai/`
> **Objectif** : identifier tous les prompts existants, leur état de gouvernance, et les risques immédiats.

---

## Synthèse exécutive

| Catégorie | Nb | Statut |
|---|---|---|
| Prompts externalisés dans `11_PROMPTS/` (structure héritée) | 9 | Partiellement gouvernés — sans métadonnées standard |
| Prompts critiques dans le backend Python | 3 | **Externalises** — Phase A completee le 2026-05-05 |
| Prompts référencés dans README mais absents | 2 | Fantômes documentaires |
| Prompts candidats à externalisation (services/analyse) | 1 | Règles regex — hors périmètre IA strict |

**Mise a jour 2026-05-05 (Vague 3 - Phase A)** : les 3 prompts critiques initialement hardcodes
dans `app/ai/prompts/session_note_cercle_v1.py` sont maintenant externalises dans
`11_PROMPTS/02_METH/` via le loader `app/ai/prompt_loader.py`.

---

## SECTION 1 — Prompts déjà externalisés dans `11_PROMPTS/`

Ces prompts existent dans des fichiers Markdown dans `11_PROMPTS/`. Ils ne sont pas encore
conformes au standard V1 (pas de YAML frontmatter, nommage hérité, pas d'ID) mais leur
contenu est accessible et lisible.

### `01_session/PROMPT_note_clinique.md`

| Attribut | Valeur |
|---|---|
| Version déclarée | v1.0 — 2026-05-05 |
| Surface | opérateur / backend MERLIN |
| Déclencheur | après clôture d'une session audio |
| Couche cible | METH |
| Dossier cible | `02_METH/` |
| Conformité standard V1 | ❌ — pas de YAML, nommage hérité |
| Lié au backend ? | Incertain — pas de `utilisé_par` documenté |
| Données sensibles | Oui — transcription audio et données de santé |
| Priorité migration | P1 |

**Contenu** : transformation de transcription brute en note clinique structurée (4 sections).
Instruction explicite : ne pas formuler de diagnostic. Longueur cible 150-300 mots.

### `01_session/PROMPT_resume_session.md`

| Attribut | Valeur |
|---|---|
| Version déclarée | v1.0 — 2026-05-05 |
| Surface | opérateur / tableau de bord MERLIN |
| Couche cible | METH |
| Dossier cible | `02_METH/` |
| Conformité standard V1 | ❌ — pas de YAML, nommage hérité |
| Lié au backend ? | Incertain |
| Données sensibles | Oui — résumé d'une note clinique |
| Priorité migration | P2 |

**Contenu** : génération d'un résumé de 3-5 phrases pour affichage dans la liste sessions opérateur.
Non transmis au client.

### `02_document/PROMPT_generation_rapport.md`

| Attribut | Valeur |
|---|---|
| Version déclarée | Non documentée (fichier sans entête structurée) |
| Couche cible | METH |
| Dossier cible | `02_METH/` |
| Conformité standard V1 | ❌ |
| Données sensibles | Oui — note clinique → document formel |
| Priorité migration | P2 |

### `02_document/PROMPT_validation_contenu.md`

| Attribut | Valeur |
|---|---|
| Version déclarée | Non documentée |
| Couche cible | PROD |
| Dossier cible | `05_PROD/` |
| Conformité standard V1 | ❌ |
| Données sensibles | Potentiellement — validation avant diffusion client |
| Priorité migration | P3 |

### `03_supervision/PROMPT_flags_anomalies.md`

| Attribut | Valeur |
|---|---|
| Version déclarée | v1.0 — 2026-05-05 |
| Surface | superviseur / système MERLIN |
| Couche cible | METH |
| Dossier cible | `02_METH/` |
| Conformité standard V1 | ❌ — pas de YAML |
| Données sensibles | Oui — analyse de note clinique |
| Priorité migration | P1 |

**Note** : ce prompt détecte des flags de sécurité (risque pour soi ou autrui).
Son impact est direct sur le parcours de supervision. Migration prioritaire.

### `03_supervision/PROMPT_relecture_note.md`

| Attribut | Valeur |
|---|---|
| Couche cible | METH |
| Dossier cible | `02_METH/` |
| Conformité standard V1 | ❌ |
| Données sensibles | Oui |
| Priorité migration | P2 |

### `04_admin/PROMPT_audit_dossier.md`

| Attribut | Valeur |
|---|---|
| Couche cible | ADMIN |
| Dossier cible | `04_ADMIN/` |
| Conformité standard V1 | ❌ |
| Données sensibles | Potentiellement — revue de dossier client |
| Priorité migration | P3 |

### `04_admin/PROMPT_onboarding_client.md`

| Attribut | Valeur |
|---|---|
| Couche cible | ADMIN |
| Dossier cible | `04_ADMIN/` |
| Conformité standard V1 | ❌ |
| Données sensibles | Oui — création de fiche client |
| Priorité migration | P2 |

### `05_pilote/PROMPT_validation_pilote.md`

| Attribut | Valeur |
|---|---|
| Couche cible | PROD |
| Dossier cible | `05_PROD/` |
| Conformité standard V1 | ❌ |
| Données sensibles | Non — évaluation de déploiement |
| Priorité migration | P3 |

---

## SECTION 2 — Prompts critiques backend (etat apres externalisation Phase A)

Ces prompts etaient entierement dans le code Python au debut de Vague 3.
Depuis le 2026-05-05, ils sont externalises et charges dynamiquement depuis `11_PROMPTS/`.

### PROMPT CRITIQUE 1 — `SESSION_NOTE_CERCLE_SYSTEM_PROMPT`

| Attribut | Valeur |
|---|---|
| Fichier source | `app/ai/prompts/session_note_cercle_v1.py` — ligne 101 |
| Variable Python | `SESSION_NOTE_CERCLE_SYSTEM_PROMPT` |
| Identifiant de version (code) | `SESSION_NOTE_CERCLE_PROMPT_VERSION = "session_note_cercle_v1"` |
| Couche | METH (couche dominante) + FOND (hypothèses contextuelles) |
| Modèle cible | `claude-sonnet-4-20250514` |
| En production | **Oui** |
| Données sensibles | **Oui** — traite des transcriptions de séances de santé mentale |
| Version Markdown | ✅ `11_PROMPTS/02_METH/METH-003-session-note-cercle-system-prompt-v1.md` |
| Statut migration | ✅ **Externalise — Phase A complete** |

**Contenu** : prompt système complet définissant MERLIN comme "moteur documentaire d'IVIA".
Contient les contraintes absolues (ne pas poser de diagnostic, ne pas citer des traditions),
les règles de diffusion (production_note / client_delivery / supervision / research),
et l'enrichissement contextuel québécois.

**Etat actuel** : le prompt est charge via `load_prompt("METH-003")`; les modifications
passent desormais par fichier Markdown versionne.

### PROMPT CRITIQUE 2 — `QUEBEC_CONTEXT_HYPOTHESES`

| Attribut | Valeur |
|---|---|
| Fichier source | `app/ai/prompts/session_note_cercle_v1.py` — lignes 10-20 |
| Variable Python | `QUEBEC_CONTEXT_HYPOTHESES` |
| Couche | **FOND** |
| En production | Oui — injecté dans SESSION_NOTE_CERCLE_SYSTEM_PROMPT |
| Données sensibles | Non — liste d'hypothèses génériques |
| Version Markdown | ✅ `11_PROMPTS/02_METH/METH-001-quebec-context-hypotheses-v1.md` |
| Statut migration | ✅ **Externalise — Phase A complete** |

**Contenu** : 9 hypothèses de pression contextuelle québécoise (pression_silence_et_minimisation,
pression_performance_travail, pression_isolement_relationnel, etc.).
C'est un document de couche FOND — il exprime une lecture culturelle structurée.
Il devrait exister dans `11_PROMPTS/01_FOND/` **et** dans `04_METHODES/`.

### PROMPT CRITIQUE 3 — `QUEBEC_CONTEXT_SIGNALS`

| Attribut | Valeur |
|---|---|
| Fichier source | `app/ai/prompts/session_note_cercle_v1.py` — lignes 22-35 |
| Variable Python | `QUEBEC_CONTEXT_SIGNALS` |
| Couche | **FOND** |
| En production | Oui — injecté dans SESSION_NOTE_CERCLE_SYSTEM_PROMPT |
| Données sensibles | Non — liste de signaux génériques |
| Version Markdown | ✅ `11_PROMPTS/02_METH/METH-002-quebec-context-signals-v1.md` |
| Statut migration | ✅ **Externalise — Phase A complete** |

**Contenu** : 12 signaux d'entretien québécois à détecter dans les transcriptions
(minimisation_verbale, humour_defensif, honte_de_demander, etc.).
Appartient à la couche FOND — c'est une grille d'observation culturelle.

---

## SECTION 3 — Prompts candidats à externalisation (périmètre élargi)

### `app/services/intake_analysis.py` — `_RISK_PATTERNS` et `_GAP_PATTERNS`

| Attribut | Valeur |
|---|---|
| Nature | Patterns regex d'analyse de texte libre |
| Couche | METH |
| En production | Oui |
| Données sensibles | Oui — analyse du motif de consultation client |
| Nature IA | Non — regex pur, pas d'appel à un modèle IA |
| Priorité externalisation | P3 (pas un prompt IA, mais une règle métier à documenter dans METH) |

**Recommandation** : ne pas externaliser dans `11_PROMPTS/`. Documenter comme
**règle métier METH** dans `04_METHODES/`. Créer un fichier
`MERLIN_METH_REGLES_TRIAGE_SIGNAUX_URGENCE_v1.0.md`.

---

## SECTION 4 — Prompts fantômes (référencés mais absents)

Le `README.md` de `11_PROMPTS/` liste des fichiers qui n'existent pas :

| Fichier référencé | Emplacement indiqué | Statut réel |
|---|---|---|
| `PROMPT_extraction_entites.md` | `01_session/` | **Absent** — jamais créé |
| `PROMPT_lettre_client.md` | `02_document/` | **Absent** — jamais créé |

**Action** : retirer ces références du README ou créer les fichiers selon le standard V1.

---

## SECTION 5 — Risques immédiats classés

| Risque | Niveau | Description | Action recommandée |
|---|---|---|---|
| Modification silencieuse du prompt de note de seance | **FAIBLE** | Prompt externalise via `METH-003` + loader en cache | Maintenir discipline de bump de version |
| Derive des regles de non-diagnostic | **MOYEN** | Le risque reste lie aux changements sans revue humaine | Exiger revue superviseur pour tout changement METH-003 |
| Perte de tracabilite du contexte quebecois | **FAIBLE** | Hypotheses/signaux externalises via `METH-001` et `METH-002` | Maintenir les liens d'ID dans la gouvernance |
| Prompts héritées sans métadonnées | **MOYEN** | 9 fichiers dans l'ancienne structure sans YAML, sans ID | Migrer en Vague 3 |
| Prompts fantômes dans README | **FAIBLE** | 2 fichiers référencés absents | Corriger le README |

---

## Plan de migration recommandé — Vague 3

### Phase A — Externalisation des prompts critiques backend (P1)

1. Créer `11_PROMPTS/00_SYSTEME/MERLIN_PROMPT_SYSTEME-IDENTITE_MERLIN_v1.0.md`
   — contenant le corps du prompt système MERLIN (persona, contraintes absolues, règles de diffusion).
2. Créer `11_PROMPTS/01_FOND/MERLIN_PROMPT_FOND-CONTEXTE_QUEBEC_v1.0.md`
   — contenant `QUEBEC_CONTEXT_HYPOTHESES` + `QUEBEC_CONTEXT_SIGNALS` en format documenté.
3. Créer `11_PROMPTS/02_METH/MERLIN_PROMPT_METH-NOTE_SEANCE_CERCLE_v1.0.md`
   — version Markdown complète du prompt de note de séance.
4. Bumper `SESSION_NOTE_CERCLE_PROMPT_VERSION` à `"session_note_cercle_v2"` dans le code
   pour marquer la transition vers la version gouvernée.

### Phase B — Migration de la structure héritée (P2/P3)

5. Migrer les 9 prompts héritées vers les nouveaux dossiers avec renommage et ajout des métadonnées.
6. Conserver les anciens fichiers avec un statut `superseded` pendant 1 mois.
7. Mettre à jour les références dans le code backend si nécessaire.

### Phase C — Documentation des règles METH (P3)

8. Créer `04_METHODES/MERLIN_METH_REGLES_TRIAGE_SIGNAUX_URGENCE_v1.0.md`
   — documenter les patterns `_RISK_PATTERNS` et `_GAP_PATTERNS` de `intake_analysis.py`.

---

## Historique de révisions

| Version | Date | Auteur | Nature de la révision |
|---|---|---|---|
| 1.1 | 2026-05-05 | fondateur | Mise a jour Vague 3 — Phase A complete (3 prompts critiques externalises) |
| 1.0 | 2026-05-05 | fondateur | Création initiale — audit Vague 2 |

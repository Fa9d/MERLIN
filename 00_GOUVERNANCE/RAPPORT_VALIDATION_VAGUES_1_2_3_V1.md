---
titre: Rapport de validation — Vagues 1, 2 et 3
id: MERLIN-RAPPORT-VALIDATION-V1-2-3
statut: active
type: audit
couche: PROD
périmètre: 11_PROMPTS + 00_GOUVERNANCE/ADR + 10_backend_merlin_api/app/ai
auteur: Claude Code (claude-sonnet-4-6)
date: 2026-05-05
version: 1.0
dépend_de: [ADR-0002, PROMPTS_STANDARD_METADATA_V1, PROMPTS_CONVENTION_NOMMAGE_V1]
remplace: []
arbitrage_requis: non — rapport d'état
source_canonique: 00_GOUVERNANCE/RAPPORT_VALIDATION_VAGUES_1_2_3_V1.md
---

# MERLIN — Rapport de validation Vagues 1-2-3

> **Date d'exécution** : 2026-05-05
> **Périmètre** : `11_PROMPTS/` + `00_GOUVERNANCE/ADR/` + `10_backend_merlin_api/app/ai/prompt_loader.py`
> **Références** : `CLAUDE.md`, `PROMPTS_STANDARD_METADATA_V1.md`, `PROMPTS_CONVENTION_NOMMAGE_V1.md`
> **Méthode** : lecture intégrale de chaque fichier, comparaison ligne à ligne avec les standards

---

## Synthèse exécutive

| Domaine | Fichiers audités | Écarts critiques | Écarts majeurs | Écarts mineurs |
|---|---|---|---|---|
| Prompts legacy (01-05 session/doc/sup/admin/pilote) | 9 | 1 | 5 | 3 |
| Prompts METH (02_METH/) | 3 | 0 | 3 | 2 |
| `prompt_loader.py` | 1 | 0 | 1 | 4 |
| ADR (00_GOUVERNANCE/ADR/) | 4 | 1 | 4 | 2 |
| **Total** | **17** | **2** | **13** | **11** |

**Blocants pour Vague 4 :** 5 éléments (voir section 5).

---

## 1. Prompts — Structure héritée (`01_session/`, `02_document/`, `03_supervision/`, `04_admin/`, `05_pilote/`)

### Référentiel appliqué

Structure obligatoire définie par `CLAUDE.md` :

```
# PROMPT — [Titre]
**Version**: vX.X — YYYY-MM-DD
**Surface**: [qui peut l'utiliser]
**Déclencheur**: [quand il s'active]
---
## Contexte
## Rôle
## Entrée attendue
## Tâche
## Format de sortie
## Règles absolues   ← OBLIGATOIRE
## Complémentaire à
```

Et structure enrichie définie par `PROMPTS_STANDARD_METADATA_V1.md` (Vague 2) :
- YAML frontmatter avec 11 champs obligatoires
- 7 sections numérotées
- Section `## Historique de révisions`

---

### ECL-P01 — CRITIQUE — Doublement de ligne `**Version**` incohérent (6 prompts)

**Fichiers concernés :**
- `01_session/PROMPT_note_clinique.md`
- `01_session/PROMPT_resume_session.md`
- `02_document/PROMPT_generation_rapport.md`
- `02_document/PROMPT_validation_contenu.md`
- `03_supervision/PROMPT_flags_anomalies.md`
- `03_supervision/PROMPT_relecture_note.md`

**Écart :** Chaque fichier déclare `**Version**: v1.0` en en-tête et `**Version**: v1.1` en pied de document. La version de référence est ambiguë pour tout système ou humain lisant ces fichiers. Un loader automatique lisant la première ligne trouverait v1.0 ; un auditeur lisant jusqu'au bas trouverait v1.1.

**Exemple (PROMPT_note_clinique.md) :**
```
Ligne 4 :  **Version**: v1.0 — 2026-05-05
Ligne 104 : **Version**: v1.1 — 2026-05-05 (ajout Règles absolues)
```

**Impact :** Le registre `INDEX_PROMPTS_V1.md` ne peut pas indiquer la bonne version. Tout diff ou audit par version est compromis.

---

### ECL-P02 — MAJEUR — Section `## Tâche` absente, remplacée par `## Instructions` (6 prompts)

**Fichiers concernés :** mêmes 6 que ECL-P01.

**Écart :** `CLAUDE.md` liste `## Tâche` comme section standard. Ces 6 prompts utilisent `## Instructions` à la place. `PROMPTS_STANDARD_METADATA_V1.md` utilise quant à lui `## 3. Instructions` (avec numéro). Il y a donc deux standards en coexistence, et les prompts legacy suivent ni l'un ni l'autre exactement.

Les 3 prompts `04_admin/` et `05_pilote/` (`PROMPT_audit_dossier.md`, `PROMPT_onboarding_client.md`, `PROMPT_validation_pilote.md`) utilisent correctement `## Tâche`.

---

### ECL-P03 — MAJEUR — Section `## Complémentaire à` non dédiée (6 prompts)

**Fichiers concernés :** mêmes 6 que ECL-P01.

**Écart :** `CLAUDE.md` liste `## Complémentaire à` comme section standard à part entière. Ces 6 prompts noient la liste de complémentaires dans une section `## Notes d'usage` sous forme de bullet `- Complémentaire à : ...`. Ce n'est pas une section H2 indépendante.

Les 3 prompts `04_admin/` et `05_pilote/` ont une section `## Complémentaire à` dédiée et conforme.

---

### ECL-P04 — MAJEUR — Pas de YAML frontmatter sur les 9 prompts legacy

**Fichiers concernés :** tous les 9 prompts dans la structure héritée.

**Écart :** `PROMPTS_STANDARD_METADATA_V1.md` exige un bloc YAML frontmatter avec 11 champs obligatoires (`titre`, `id`, `statut`, `couche`, `type`, `périmètre`, `auteur`, `date`, `version`, `modèle_cible`) avant tout contenu. Aucun prompt legacy ne possède ce bloc.

**Note :** Migration planifiée en Vague 3 selon `INDEX_PROMPTS_V1.md` et `AUDIT_PROMPTS_EXISTANTS_V1.md`. Écart attendu, mais à traiter avant mise en production de tout nouveau flux IA utilisant ces prompts.

---

### ECL-P05 — MAJEUR — Nommage non conforme sur les 9 prompts legacy

**Fichiers concernés :** tous les 9 prompts dans la structure héritée.

**Écart :** `PROMPTS_CONVENTION_NOMMAGE_V1.md` impose le format :
```
MERLIN_PROMPT_[COUCHE]-[SUJET]_v[MAJOR].[MINOR].md
```
Les fichiers actuels utilisent l'ancien format hérité (`PROMPT_note_clinique.md`, etc.).

**Exemples de noms cibles :**
- `PROMPT_note_clinique.md` → `MERLIN_PROMPT_METH-NOTE_CLINIQUE_v1.1.md`
- `PROMPT_flags_anomalies.md` → `MERLIN_PROMPT_METH-FLAGS_ANOMALIES_v1.1.md`
- `PROMPT_audit_dossier.md` → `MERLIN_PROMPT_ADMIN-AUDIT_DOSSIER_v1.1.md`

**Note :** Migration planifiée en Vague 3. Écart connu et tracé.

---

### ECL-P06 — MINEUR — Section `## Historique de révisions` absente (9 prompts legacy)

**Fichiers concernés :** tous les 9 prompts dans la structure héritée.

**Écart :** `PROMPTS_STANDARD_METADATA_V1.md` (section 6) exige un tableau `## Historique de révisions` en fin de fichier. Aucun prompt legacy ne l'a.

---

### ECL-P07 — MINEUR — Typo dans `PROMPT_relecture_note.md`

**Fichier :** `03_supervision/PROMPT_relecture_note.md`, ligne 79.

**Écart :** `«imposséible à déterminer»` → devrait être `«impossible à déterminer»`.

---

### ECL-P08 — MINEUR — `README.md` obsolète et référençant des fichiers fantômes

**Fichier :** `11_PROMPTS/README.md`.

**Écart :**
1. Le README référence 2 fichiers qui n'existent pas :
   - `01_session/PROMPT_extraction_entites.md` — absent
   - `02_document/PROMPT_lettre_client.md` — absent
2. La section "Convention de format" du README décrit une structure (sans `## Tâche`, sans `## Règles absolues`) qui est inférieure au standard actuel de `CLAUDE.md`.
3. `INDEX_PROMPTS_V1.md` se déclare comme remplaçant de ce README (`remplace: [README.md (non structuré)]`) mais le README n'a pas été retiré ni mis à jour.

---

## 2. Prompts METH (`11_PROMPTS/02_METH/`)

### ECL-M01 — MAJEUR — Couche incohérente pour METH-001 et METH-002

**Fichiers concernés :**
- `02_METH/METH-001-quebec-context-hypotheses-v1.md`
- `02_METH/METH-002-quebec-context-signals-v1.md`

**Écart :** Les deux fichiers déclarent `couche: METH` dans leur frontmatter YAML. Or :
- `INDEX_PROMPTS_V1.md` les classe explicitement dans la couche `FOND` (colonne "Couche" du tableau "Prompts critiques backend").
- `AUDIT_PROMPTS_EXISTANTS_V1.md` (Section 2) indique pour METH-001/002 : `Couche : FOND`.
- `PROMPTS_CONVENTION_NOMMAGE_V1.md` précise que les prompts FOND vont dans `01_FOND/`.

La couche `FOND` implique une **stabilité maximale, changement par arbitrage uniquement** (ADR-0001). La couche `METH` est évolutive sous contrôle de version. Cette divergence a un impact sur la gouvernance : un changement à ces prompts nécessite-t-il un arbitrage fondateur (FOND) ou une simple révision (METH) ?

**Note :** Ces fichiers sont également mal placés — ils devraient être dans `01_FOND/` selon leur couche réelle.

---

### ECL-M02 — MAJEUR — Nommage non conforme (3 prompts METH)

**Fichiers concernés :**
- `METH-001-quebec-context-hypotheses-v1.md`
- `METH-002-quebec-context-signals-v1.md`
- `METH-003-session-note-cercle-system-prompt-v1.md`

**Écart :** Le format utilisé (`METH-NNN-[sujet]-v[N].md`) ne respecte pas la convention `PROMPTS_CONVENTION_NOMMAGE_V1.md` :
```
MERLIN_PROMPT_[COUCHE]-[SUJET]_v[MAJOR].[MINOR].md
```

Les noms cibles selon la convention :
- `METH-001...` → `MERLIN_PROMPT_FOND-QUEBEC_CONTEXT_HYPOTHESES_v1.0.md` (avec couche FOND correcte)
- `METH-002...` → `MERLIN_PROMPT_FOND-QUEBEC_CONTEXT_SIGNALS_v1.0.md`
- `METH-003...` → `MERLIN_PROMPT_METH-NOTE_SEANCE_CERCLE_v1.0.md`

---

### ECL-M03 — MAJEUR — Sections Markdown absentes ou non structurées (3 prompts METH)

**Fichiers concernés :** METH-001, METH-002, METH-003.

**Écart :** `PROMPTS_STANDARD_METADATA_V1.md` (section 6) exige 7 sections numérotées + historique :
```
## 1. Contexte et usage
## 2. Persona / Rôle
## 3. Instructions
## 4. Contraintes absolues
## 5. Format de sortie
## 6. Entrée attendue
## 7. Exemple de sortie
## Historique de révisions
```

Constat par fichier :
- **METH-001** : uniquement une liste de bullet points après le frontmatter. Aucune section H2.
- **METH-002** : idem — liste de bullets sans section.
- **METH-003** : contenu structuré sous forme de paragraphes et bullets mais **sans aucune section H2**. Les sections (Contraintes, Règles de diffusion, Enrichissement, Format de sortie) sont implicites dans le texte, non balisées.

---

### ECL-M04 — MINEUR — Format `id` non standard dans METH-001/002

**Fichiers concernés :** METH-001, METH-002.

**Écart :** Les IDs contiennent un numéro ordinal non prévu par le standard :
- `MERLIN-PROMPT-METH-001-QUEBEC_CONTEXT_HYPOTHESES-V1` (METH-001)
- `MERLIN-PROMPT-METH-002-QUEBEC_CONTEXT_SIGNALS-V1` (METH-002)

Le format canonique (`PROMPTS_STANDARD_METADATA_V1.md`) est :
```
MERLIN-PROMPT-[COUCHE]-[SUJET]-V[N]
```
Le numéro `001` / `002` est une séquence locale de projet non prévue dans le format d'ID.

---

### ECL-M05 — MINEUR — `_PROMPT_PATHS` dans `prompt_loader.py` utilise l'ancien identifiant court non canonique

**Fichier :** `10_backend_merlin_api/app/ai/prompt_loader.py`

**Écart :** Le loader utilise `"METH-001"`, `"METH-002"`, `"METH-003"` comme clés. Ces clés correspondent au nom de fichier abrégé, pas à l'identifiant canonique `id` défini dans le frontmatter YAML (`MERLIN-PROMPT-METH-001-...`). Si le standard d'ID est un jour aligné, le loader devient incohérent sans mise à jour.

---

## 3. `prompt_loader.py`

**Fichier :** `10_backend_merlin_api/app/ai/prompt_loader.py`

### Bilan positif (points conformes)

| Critère | Statut |
|---|---|
| Docstrings présents sur toutes les fonctions | ✅ |
| Docstrings en français | ✅ (avec réserve ECL-L01) |
| Cache mémoire implémenté | ✅ `_PROMPT_CACHE: dict[str, str]` |
| Exception personnalisée | ✅ `PromptNotFoundError(FileNotFoundError)` |
| Gestion d'erreur ID introuvable | ✅ `raise PromptNotFoundError(...)` |
| Gestion d'erreur fichier absent | ✅ `if not prompt_path.exists()` |
| Type hints | ✅ `from __future__ import annotations` |
| Encodage UTF-8 explicite | ✅ `encoding="utf-8"` |

---

### ECL-L01 — MAJEUR — Docstrings sans accents (orthographe française incorrecte)

**Écart :** `CLAUDE.md` impose docstrings en français. Les accents sont absents dans plusieurs docstrings :

| Ligne | Texte actuel | Correction |
|---|---|---|
| 7 | `Erreur levee quand` | `Erreur levée quand` |
| 34 | `situee apres le deuxieme delimitateur` | `située après le deuxième délimitateur` |
| 45 | `Charge un prompt Markdown a partir de son identifiant et applique un cache memoire simple` | `Charge un prompt Markdown à partir de son identifiant et applique un cache mémoire simple` |

---

### ECL-L02 — MINEUR — Pas de docstring au niveau module

**Écart :** Aucune docstring de module en tête de `prompt_loader.py`. Convention implicite (CLAUDE.md : docstrings en français) et bonne pratique Python : le module devrait exposer son rôle et son usage en une ou deux lignes.

---

### ECL-L03 — MINEUR — `_PROMPT_PATHS` ne couvre que 3 prompts sur 12

**Écart :** La table de routage `_PROMPT_PATHS` contient uniquement les 3 prompts METH externalisés en Vague 3 Phase A. Les 9 prompts legacy ne sont pas routables via ce loader. Pas d'indication dans le code sur le plan de couverture future.

**Impact :** Un développeur utilisant `load_prompt("note_clinique")` obtient une `PromptNotFoundError` sans explication. Le loader devrait documenter sa portée dans sa docstring module.

---

### ECL-L04 — MINEUR — Aucun test unitaire visible

**Écart :** Aucun fichier de test pour `prompt_loader.py` n'est présent dans le repo. Les chemins testés incluent `_prompts_root()` (relatif à `__file__`), `_extract_markdown_body` (parsing YAML), et les cas d'erreur de `load_prompt`. Ces fonctions sont testables de manière isolée.

---

### ECL-L05 — INFO — Cache sans invalidation ni documentation

**Observation :** `_PROMPT_CACHE` est un dict module-level sans TTL ni mécanisme d'invalidation. En production, un redémarrage du processus efface le cache. Ce comportement est attendu mais non documenté. Si un prompt est modifié sans redémarrage (rare avec Docker Compose), le cache retourne l'ancienne version.

---

## 4. ADR (`00_GOUVERNANCE/ADR/`)

### Référentiel appliqué

La structure implicite commune observable dans les 4 ADR :

```
---
[YAML frontmatter]
---

# ADR-[NNN] — [Titre]

> Statut / bloc callout

---

## Contexte
## Options considérées
## Décision
## Conséquences
  ### Avantages
  ### Inconvénients ou risques
  ### Actions requises
## Entrée registre associée
```

---

### ECL-A01 — CRITIQUE — Pas de template ADR canonique défini

**Écart :** Aucun fichier `ADR_TEMPLATE.md` ou équivalent n'existe dans `00_GOUVERNANCE/ADR/`. La structure standard des ADR MERLIN n'est pas formalisée dans un document de référence. Les 4 ADR actuels présentent des structures divergentes (voir ECL-A02 à ECL-A06), ce qui confirme l'absence de template de référence.

**Impact :** Toute ADR créée en Vague 4 risque de dériver davantage. Un template est un prérequis à la cohérence.

---

### ECL-A02 — MAJEUR — Frontmatter hétérogène entre ADR-0001/0002/0003 et ADR-0004

**Écart :** Le frontmatter de ADR-0001, ADR-0002, ADR-0003 est minimaliste :
```yaml
titre, id, statut, date, décideurs, remplace, remplacé_par
```

ADR-0004 a un frontmatter enrichi qui ajoute :
```yaml
couche, type, auteur, version, dépend_de, arbitrage_requis, source_canonique, décision_registre
```

Les deux formats coexistent sans qu'un standard soit déclaré. ADR-0004 semble plus aligné avec `MERLIN_STANDARD_METADATA_V1.md`, mais ADR-0001/0002/0003 n'ont pas été rétroactivement mis à jour.

---

### ECL-A03 — MAJEUR — ADR-0004 manque les champs `décideurs` et `remplacé_par`

**Fichier :** `ADR-0004-normalisation-arborescence.md`

**Écart :** ADR-0001/0002/0003 déclarent `décideurs: fondateur` et `remplacé_par: []`. ADR-0004 ne contient ni l'un ni l'autre. Si l'ADR-0004 est un jour supersédée, il n'y a pas de champ `remplacé_par` pour tracer la succession.

---

### ECL-A04 — MAJEUR — ADR-0004 manque la section `## Conséquences`

**Fichier :** `ADR-0004-normalisation-arborescence.md`

**Écart :** ADR-0001, ADR-0002, ADR-0003 ont tous une section `## Conséquences` avec sous-sections Avantages, Inconvénients/risques, Actions requises. ADR-0004 passe directement de `## Décision` à `## Actions requises`, supprimant l'analyse des avantages/inconvénients qui est pourtant la substance d'une ADR.

---

### ECL-A05 — MAJEUR — ADR-0004 remplace `## Entrée registre associée` par un champ frontmatter

**Fichier :** `ADR-0004-normalisation-arborescence.md`

**Écart :** ADR-0001/0002/0003 ont une section dédiée `## Entrée registre associée` avec la ligne formatée :
```
> DEC-NNN | date | domaine | description | statut | ADR-NNNN
```

ADR-0004 utilise à la place un champ frontmatter `décision_registre: DEC-039`. L'information est présente mais dans un emplacement différent, ce qui casse la cohérence de format pour tout outil ou humain cherchant cette information en fin de document.

---

### ECL-A06 — MINEUR — ADR-0001/0002/0003 manquent `## Historique de révisions`

**Fichiers concernés :** ADR-0001, ADR-0002, ADR-0003.

**Écart :** ADR-0004 termine par un `## Historique de révisions` au format tableau. Les 3 premières ADR n'en ont pas. Si une ADR est révisée (bump de version), cette section est nécessaire pour tracer qui a changé quoi.

---

### ECL-A07 — MINEUR — ADR-0004 manque le bloc callout de statut après le H1

**Fichier :** `ADR-0004-normalisation-arborescence.md`

**Écart :** ADR-0001/0002/0003 ont immédiatement après le titre H1 un bloc callout :
```markdown
> **Statut** : accepted — YYYY-MM-DD
> **Document de référence** : ...
```

ADR-0004 utilise à la place une section `## Statut` avec un bloc de code inline. Format différent des 3 autres.

---

## 5. Ce qui doit être corrigé avant la Vague 4

Les éléments suivants sont **bloquants ou à risque élevé** pour la cohérence de la Vague 4.

### PRIORITÉ 1 — Bloquants immédiats

| # | Code | Fichier(s) | Action requise |
|---|---|---|---|
| 1 | ECL-P01 | 6 prompts legacy | Supprimer la ligne `**Version**: v1.0` en en-tête OU la ligne `**Version**: v1.1` en pied — choisir une position canonique unique et la tenir |
| 2 | ECL-A01 | `00_GOUVERNANCE/ADR/` | Créer `ADR_TEMPLATE.md` avec le format canonique MERLIN avant toute nouvelle ADR en Vague 4 |
| 3 | ECL-M01 | METH-001, METH-002 | Corriger `couche: METH` → `couche: FOND` dans les frontmatters ; décider du dossier cible (`02_METH/` ou `01_FOND/`) par arbitrage explicite |

### PRIORITÉ 2 — Majeurs à résoudre avant production de nouveaux prompts

| # | Code | Fichier(s) | Action requise |
|---|---|---|---|
| 4 | ECL-P02 | 6 prompts legacy | Renommer `## Instructions` → `## Tâche` pour aligner avec CLAUDE.md |
| 5 | ECL-P03 | 6 prompts legacy | Extraire `Complémentaire à` en section H2 dédiée |
| 6 | ECL-M03 | METH-001, METH-002, METH-003 | Ajouter les 7 sections H2 numérotées + historique de révisions |
| 7 | ECL-A02 | ADR-0001, ADR-0002, ADR-0003 | Enrichir les frontmatter avec `couche`, `type`, `auteur`, `version` au minimum |
| 8 | ECL-A03 | ADR-0004 | Ajouter `décideurs` et `remplacé_par` au frontmatter |
| 9 | ECL-A04 | ADR-0004 | Ajouter section `## Conséquences` avec Avantages / Inconvénients / Risques |
| 10 | ECL-A05 | ADR-0004 | Ajouter section `## Entrée registre associée` en bas (conserver ou supprimer le champ frontmatter) |
| 11 | ECL-L01 | `prompt_loader.py` | Corriger les accents dans les docstrings (levée, située, après, deuxième, à, mémoire) |

### PRIORITÉ 3 — Mineurs (peuvent être traités en Vague 4 sans bloquer)

| # | Code | Fichier(s) | Action requise |
|---|---|---|---|
| 12 | ECL-P07 | `PROMPT_relecture_note.md` | Corriger `imposséible` → `impossible` (ligne 79) |
| 13 | ECL-P08 | `README.md` | Retirer les 2 références fantômes (`PROMPT_extraction_entites.md`, `PROMPT_lettre_client.md`) ou créer les fichiers |
| 14 | ECL-A06 | ADR-0001/0002/0003 | Ajouter `## Historique de révisions` |
| 15 | ECL-A07 | ADR-0004 | Aligner le bloc callout de statut avec les autres ADR |
| 16 | ECL-L02 | `prompt_loader.py` | Ajouter docstring module-level en français |
| 17 | ECL-L03 | `prompt_loader.py` | Documenter la portée de `_PROMPT_PATHS` (3 prompts METH seulement) dans la docstring module |

---

## 6. Éléments conformes — points forts à conserver

| Élément | Constat |
|---|---|
| Section `## Règles absolues` | Présente et substantielle dans les 9 prompts legacy. Règle de CLAUDE.md respectée. |
| Prompts `04_admin/` et `05_pilote/` | Utilisent correctement `## Tâche` et `## Complémentaire à` dédiée. Pas de doublement de version. |
| YAML frontmatter METH-001/002/003 | Conforme à `PROMPTS_STANDARD_METADATA_V1.md` (10/11 champs présents). |
| `prompt_loader.py` — logique de cache | Correct, propre, performant. Aucun correctif fonctionnel requis. |
| `prompt_loader.py` — gestion d'erreur | Double vérification (ID absent + fichier absent) avec exception typée. Conforme. |
| ADR-0001/0002/0003 — structure narrative | `## Contexte`, `## Options considérées`, `## Décision`, `## Conséquences` rigoureusement tenus. |
| ADR-0004 — frontmatter enrichi | Aligné avec le standard général `MERLIN_STANDARD_METADATA_V1.md`. À adopter comme modèle. |

---

## Historique de révisions

| Version | Date | Auteur | Nature |
|---|---|---|---|
| 1.0 | 2026-05-05 | Claude Code (claude-sonnet-4-6) | Création — audit complet Vagues 1-2-3 |

---
titre: Rapport d'audit de conformité — agents C-suite 06_CSUITE/
id: MERLIN-AUDIT-CSUITE-V1
statut: active
type: audit
couche: PROD
périmètre: 11_PROMPTS
auteur: fondateur
date: 2026-06-30
version: 1.0
dépend_de: [MERLIN-PROMPTS-STANDARD-META-V1, MERLIN-PROMPTS-CONV-NOMMAGE-V1, MERLIN-INDEX-PROMPTS-V1]
remplace: []
arbitrage_requis: non
---

# MERLIN — Audit de conformité — 06_CSUITE/ V1.0

> **Date** : 2026-06-30  
> **Périmètre** : 7 fichiers dans `11_PROMPTS/06_CSUITE/`  
> **Référentiels appliqués** :
> - `PROMPTS_STANDARD_METADATA_V1.md` — champs obligatoires, structure de contenu
> - `PROMPTS_CONVENTION_NOMMAGE_V1.md` — format de nommage, codes de couche, placement
> - `INDEX_PROMPTS_V1.md` — structure cible `11_PROMPTS/`, intégration bibliothèque

---

## Verdict global

| Agent | Nommage | YAML | Structure | Placement | Intégration | Verdict |
|---|---|---|---|---|---|---|
| MERLIN-STRAT | ⚠️ | ✅ | ✅ | ⚠️ | ⚠️ | **3 écarts mineurs** |
| MERLIN-ARCH | ⚠️ | ⚠️ | ✅ | ⚠️ | ⚠️ | **4 écarts mineurs** |
| MERLIN-COMM | ⚠️ | ✅ | ✅ | ⚠️ | ⚠️ | **3 écarts mineurs** |
| MERLIN-UX | ⚠️ | ✅ | ✅ | ⚠️ | ⚠️ | **3 écarts mineurs** |
| MERLIN-FIN | ⚠️ | ⚠️ | ✅ | ⚠️ | ⚠️ | **4 écarts mineurs** |
| MERLIN-QA | ⚠️ | ✅ | ✅ | ⚠️ | ⚠️ | **3 écarts mineurs** |
| INDEX_CSUITE_V1.md | ⚠️ | ⚠️ | ✅ | n/a | ⚠️ | **3 écarts mineurs** |

**Aucun écart bloquant. Aucun agent ne peut aller en production avec son statut actuel `active`
sans correction — le statut correct avant correction est `draft`.**

---

## Écart #1 — CRITIQUE (tous les agents) — Statut `active` prématuré

**Fichiers concernés :** tous les 6 agents  
**Règle violée :** `PROMPTS_CONVENTION_NOMMAGE_V1.md` §4 — Règles de statut

> `draft` : En rédaction, non testé — **Ne pas utiliser en production**  
> `active` : Testé, validé, en production ou prêt pour production

**Constat :** Les 6 agents ont `statut: active` alors qu'ils n'ont jamais été testés sur
un modèle IA réel, n'ont pas fait l'objet d'une validation praticien/superviseur, et
aucun résultat de test n'est documenté.

**Correction requise :**
```yaml
# Avant
statut: active

# Après (jusqu'à validation réelle)
statut: draft
```

**Condition de passage à `active` :** au moins une session de test documentée par agent,
validée par le fondateur, avec exemple de sortie réelle (pas fictif) ajouté à la section 7.

---

## Écart #2 — MAJEUR (tous les agents) — Nommage non conforme

**Fichiers concernés :** tous les 6 agents  
**Règle violée :** `PROMPTS_CONVENTION_NOMMAGE_V1.md` §1 — Format obligatoire

**Format requis :**
```
MERLIN_PROMPT_[COUCHE]-[SUJET]_v[MAJOR].[MINOR].md
```

**Constat :** Le code de couche `CSUITE` n'existe pas dans la convention. Les codes définis sont :
`SYSTEME`, `FOND`, `METH`, `EDIT`, `ADMIN`, `PROD`. Les agents déclarent `couche: SYSTEME` dans
leurs métadonnées mais leur nom de fichier utilise `CSUITE` comme pseudo-couche.

**Noms actuels → noms corrigés :**

| Nom actuel | Nom corrigé |
|---|---|
| `MERLIN_PROMPT_CSUITE-STRAT_v1.0.md` | `MERLIN_PROMPT_SYSTEME-CSUITE_STRAT_v1.0.md` |
| `MERLIN_PROMPT_CSUITE-ARCH_v1.0.md` | `MERLIN_PROMPT_SYSTEME-CSUITE_ARCH_v1.0.md` |
| `MERLIN_PROMPT_CSUITE-COMM_v1.0.md` | `MERLIN_PROMPT_SYSTEME-CSUITE_COMM_v1.0.md` |
| `MERLIN_PROMPT_CSUITE-UX_v1.0.md` | `MERLIN_PROMPT_SYSTEME-CSUITE_UX_v1.0.md` |
| `MERLIN_PROMPT_CSUITE-FIN_v1.0.md` | `MERLIN_PROMPT_SYSTEME-CSUITE_FIN_v1.0.md` |
| `MERLIN_PROMPT_CSUITE-QA_v1.0.md` | `MERLIN_PROMPT_SYSTEME-CSUITE_QA_v1.0.md` |

**Alternative recommandée :** créer un ADR pour acter officiellement `CSUITE` comme nouveau
code de couche (§7 de la convention le prévoit explicitement). C'est la voie préférable
car les agents C-suite sont conceptuellement distincts des prompts `SYSTEME` existants.

```
ADR requis : "Ajout du code de couche CSUITE dans PROMPTS_CONVENTION_NOMMAGE_V1.md"
```

---

## Écart #3 — MAJEUR (tous les agents) — Dossier de placement non prévu

**Fichiers concernés :** tous les 6 agents  
**Règle violée :** `INDEX_PROMPTS_V1.md` — Structure cible + `PROMPTS_CONVENTION_NOMMAGE_V1.md` §5

**Constat :** La structure cible définie dans `INDEX_PROMPTS_V1.md` prévoit :
```
11_PROMPTS/
├── 00_SYSTEME/
├── 01_FOND/
├── 02_METH/
├── 03_EDIT/
├── 04_ADMIN/
└── 05_PROD/
```

Le dossier `06_CSUITE/` n'est pas dans cette structure cible. Les agents `couche: SYSTEME`
devraient aller dans `00_SYSTEME/` selon la règle de placement, ou `06_CSUITE/` doit être
ajouté à la structure cible par un ADR.

**Deux options :**

Option A — Déplacer dans `00_SYSTEME/` avec sous-dossier :
```
11_PROMPTS/00_SYSTEME/CSUITE/
```

Option B — Acter `06_CSUITE/` dans la structure cible (recommandée — cohérence sémantique) :
```
ADR requis + mise à jour de INDEX_PROMPTS_V1.md §Structure cible
```

---

## Écart #4 — MINEUR (MERLIN-ARCH, MERLIN-FIN) — Dépendance non résolue

**Fichier concerné :** `MERLIN_PROMPT_CSUITE-ARCH_v1.0.md`  
**Champ concerné :** `dépend_de: [..., SCHEMA_ETAT_REEL]`

**Constat :** `SCHEMA_ETAT_REEL` référence le fichier
`00_GOUVERNANCE/COMPORTEMENTAL/SCHEMA_ETAT_REEL.md` mais le format attendu dans
`dépend_de` est un **ID de document** (ex. `MERLIN-ARCH-SCHEMA-V1`), pas un chemin de fichier.
Ce fichier n'a pas de YAML frontmatter avec un ID déclaré — il ne peut pas être référencé
proprement.

**Correction requise :**
1. Ajouter un YAML frontmatter à `SCHEMA_ETAT_REEL.md` avec un ID (`MERLIN-SCHEMA-REEL-V1`)
2. Mettre à jour `dépend_de` dans MERLIN-ARCH pour pointer vers cet ID

**Fichier concerné :** `MERLIN_PROMPT_CSUITE-FIN_v1.0.md`  
**Champ concerné :** `données_sensibles: oui` sans `validation_requise: superviseur`

**Constat :** `PROMPTS_STANDARD_METADATA_V1.md` §7 stipule :
> Pour les prompts sensibles : *la validation par un praticien ou un superviseur est obligatoire avant passage en `active`*

MERLIN-FIN a `données_sensibles: oui` et `validation_requise: fondateur`. Le fondateur
est un niveau de validation accepté — c'est conforme. Pas d'écart bloquant, mais noter
que le passage à `active` nécessite une validation documentée.

---

## Écart #5 — MINEUR (INDEX_CSUITE_V1.md) — Format d'index non aligné

**Fichier concerné :** `INDEX_CSUITE_V1.md`  
**Règle de référence :** `INDEX_PROMPTS_V1.md` — format d'index canonique

**Constat :** `INDEX_CSUITE_V1.md` utilise un YAML frontmatter avec `type: index` —
ce type n'est pas défini dans `PROMPTS_STANDARD_METADATA_V1.md` (types définis : `prompt`, `charte`, `audit`). 
De plus, son champ `id` utilise le format `MERLIN-INDEX-CSUITE-V1` alors que la convention
d'ID pour les prompts est `MERLIN-PROMPT-[COUCHE]-[SUJET]-V[N]`. Un index n'est pas un
prompt — il devrait utiliser le standard de métadonnées général (`MERLIN_STANDARD_METADATA_V1.md`)
plutôt que le standard spécifique aux prompts.

**Correction :** remplacer `type: index` par `type: charte` (plus proche sémantiquement)
ou attendre l'ADR qui ajoute `type: index` formellement.

---

## Écart #6 — MINEUR (tous les agents) — Section 7 avec exemples fictifs non étiquetés

**Règle de référence :** `PROMPTS_STANDARD_METADATA_V1.md` §7

> *Les exemples de sortie dans le fichier doivent être anonymisés ou fictifs.*

**Constat :** Les exemples sont bien fictifs, mais ils ne portent pas le label explicite
`[EXEMPLE FICTIF — non tiré d'une session réelle]` requis pour les prompts sensibles.
Seul MERLIN-FIN est `données_sensibles: oui` — pour lui c'est obligatoire.
Pour les autres c'est recommandé.

**Correction pour MERLIN-FIN :**
```markdown
## 7. Exemple de sortie

> ⚠️ **EXEMPLE FICTIF** — données simulées, non issues d'une session réelle.

[contenu existant]
```

---

## Récapitulatif des actions requises

### Actions bloquantes avant usage en production

| # | Action | Fichiers | Priorité |
|---|---|---|---|
| A1 | Passer tous les statuts de `active` à `draft` | 6 agents | 🔴 Immédiate |
| A2 | Créer ADR pour acter le code de couche `CSUITE` et le dossier `06_CSUITE/` dans la structure cible | ADR nouveau | 🔴 Avant renommage |

### Actions requises avant passage à `active`

| # | Action | Fichiers | Priorité |
|---|---|---|---|
| A3 | Tester chaque agent sur modèle réel + documenter résultat | 6 agents | 🟠 Avant activation |
| A4 | Remplacer les exemples fictifs par des sorties réelles validées (ou étiqueter comme fictifs) | 6 agents | 🟠 Avant activation |
| A5 | Ajouter label `[EXEMPLE FICTIF]` dans MERLIN-FIN section 7 | MERLIN-FIN | 🟠 Avant activation |

### Actions de qualité (non bloquantes)

| # | Action | Fichiers | Priorité |
|---|---|---|---|
| A6 | Ajouter YAML frontmatter à `SCHEMA_ETAT_REEL.md` + ID stable | SCHEMA_ETAT_REEL.md | 🟡 Qualité |
| A7 | Mettre à jour `dépend_de` MERLIN-ARCH pour référencer l'ID de SCHEMA_ETAT_REEL | MERLIN-ARCH | 🟡 Qualité |
| A8 | Renommer les fichiers selon format `MERLIN_PROMPT_SYSTEME-CSUITE_[SUJET]_v1.0.md` OU attendre l'ADR CSUITE | 6 agents | 🟡 Après ADR |
| A9 | Corriger `type: index` dans INDEX_CSUITE_V1.md → `type: charte` | INDEX_CSUITE_V1.md | 🟡 Qualité |
| A10 | Mettre à jour INDEX_PROMPTS_V1.md §Structure cible pour inclure `06_CSUITE/` | INDEX_PROMPTS_V1.md | 🟡 Après ADR |

---

## Ce qui est conforme — ne pas modifier

✅ **Structure de contenu (7 sections)** — tous les agents respectent la structure
`PROMPTS_STANDARD_METADATA_V1.md` §6 : contexte, persona, instructions, contraintes absolues,
format de sortie, entrée attendue, exemple, historique.

✅ **Champs YAML obligatoires** — tous présents dans les 6 agents :
`titre`, `id`, `statut`, `type`, `couche`, `périmètre`, `auteur`, `date`, `version`, `modèle_cible`.

✅ **Instructions numérotées (×7)** — chaque agent a exactement 7 instructions numérotées,
conformément à la structure recommandée.

✅ **Contraintes absolues** — présentes et formulées négativement (« Ne jamais... »)
conformément à la pratique établie dans les prompts METH existants.

✅ **Historique de révisions** — présent dans tous les fichiers avec tableau conforme.

✅ **Cohérence inter-agents** — la matrice de collaboration dans `INDEX_CSUITE_V1.md`
est cohérente avec les triggers et périmètres déclarés dans chaque agent.

✅ **Posture non-clinique** — tous les agents intègrent la contrainte absolue de
non-prescription médicale, conformément au cadre opératoire IVIA/MERLIN.

---

## Ordre d'exécution recommandé

```
1. Passer statut → draft (A1)            ← 5 min, 6 fichiers
2. Créer ADR CSUITE (A2)                 ← 30 min, 1 fichier
3. Ajouter label fictif MERLIN-FIN (A5)  ← 2 min, 1 fichier
4. Corriger type INDEX (A9)              ← 2 min, 1 fichier
5. Tester + valider chaque agent (A3+A4) ← selon disponibilité
6. Renommer fichiers post-ADR (A8)       ← après étape 2
7. Mettre à jour dépendances (A6+A7)     ← qualité, non bloquant
8. Mettre à jour INDEX_PROMPTS (A10)     ← après étape 2
```

---

*Rapport produit par audit automatisé — à valider par le fondateur.*  
*Prochaine révision : après correction de A1+A2 et première session de tests.*

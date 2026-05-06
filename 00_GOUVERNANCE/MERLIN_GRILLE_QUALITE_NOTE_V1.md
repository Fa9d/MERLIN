# MERLIN_GRILLE_QUALITE_NOTE_V1

**Version:** 1.0  
**Statut:** ACTIF  
**Date:** 2026-05-06  
**Décision associée:** DEC-040  
**Dépend de:** MERLIN_CONTRAT_PROMPT_V1  

---

## 1. Objectif

Définir les **critères de qualité métier** d'une note clinique générée par MERLIN. Ces critères servent à évaluer les sorties de MERLIN sur le fond clinique, et pas uniquement sur la validité JSON.

Ils s'appliquent à :
- La validation humaine lors des sessions pilotes (PROD-009)
- Les tests d'évaluation qualité (ROD-TEST-001-A Journée 3+)
- Les audits de régression entre versions de prompts

---

## 2. Les 7 critères de qualité

### Critère 1 — Clarté (QUAL-001)

**Définition :** La note est compréhensible par un praticien non impliqué dans la session, sans ambiguïté de sens.

| Score | Description |
|---|---|
| 5 | Phrases courtes, langage professionnel accessible, aucune ambiguïté |
| 4 | Compréhensible avec effort minimal |
| 3 | Quelques formulations ambiguës mais le sens global est clair |
| 2 | Plusieurs sections nécessitent interprétation |
| 1 | Incompréhensible ou contradictoire |

**Test automatisable :** Longueur moyenne des phrases < 25 mots, aucun mot de plus de 3 syllabes non défini.

---

### Critère 2 — Non-jugement (QUAL-002)

**Définition :** La note ne contient aucune formulation évaluative négative sur le client, ni diagnostic implicite.

| Score | Description |
|---|---|
| 5 | Entièrement observationnel, zéro évaluation du client |
| 4 | Une formulation limite mais rectifiable |
| 3 | Ton neutre mais une inférence non étayée |
| 2 | Plusieurs jugements implicites |
| 1 | Ton pathologisant ou condescendant |

**Test automatisable :** Scan regex des termes interdits (voir liste MERLIN_CONTRAT_PROMPT_V1 §4) + modèle de classification de sentiment négatif.

---

### Critère 3 — Sécurité (QUAL-003)

**Définition :** Les signaux d'urgence (idéation suicidaire, violence, maltraitance) sont correctement identifiés, ni sur-détectés ni sous-détectés.

| Score | Description |
|---|---|
| 5 | Détection précise, citations directes, protocole METH-004 déclenché si nécessaire |
| 4 | Signal identifié mais citation manquante |
| 3 | Signal mentionné sans niveau de confiance |
| 2 | Signal ignoré ou sous-évalué |
| 1 | Faux positif grave ou omission d'un signal critique |

**Règle absolue :** Un score de 1 sur QUAL-003 = **rejet immédiat de la sortie**, indépendamment des autres scores.

---

### Critère 4 — Actionnabilité (QUAL-004)

**Définition :** Les recommandations sont concrètes, réalisables lors de la prochaine session, et liées aux faits observés.

| Score | Description |
|---|---|
| 5 | Actions spécifiques, liées à des faits, réalisables dans le prochain contact |
| 4 | Actions claires mais génériques |
| 3 | Orientations présentes mais vagues |
| 2 | Recommandations non liées aux faits de la session |
| 1 | Aucune recommandation ou recommandations inapplicables |

---

### Critère 5 — Fidélité au transcript (QUAL-005)

**Définition :** Le contenu de la note reflète fidèlement ce qui a été dit, sans ajout, déformation ou omission majeure.

| Score | Description |
|---|---|
| 5 | Chaque fait est vérifiable dans le transcript (timestamps présents) |
| 4 | Fidèle dans l'ensemble, un léger écart de paraphrase |
| 3 | Quelques inférences sans citation directe |
| 2 | Plusieurs éléments non vérifiables |
| 1 | Hallucination confirmée (contenu absent du transcript) |

**Test automatisable :** Alignement cosinus entre fragments de note et segments du transcript (seuil > 0.75).

---

### Critère 6 — Traçabilité des sources (QUAL-006)

**Définition :** Chaque fait est accompagné d'un timestamp ou d'une référence au transcript qui permet la vérification.

| Score | Description |
|---|---|
| 5 | 100% des faits avec timestamp ou citation |
| 4 | >80% des faits tracés |
| 3 | 50-80% des faits tracés |
| 2 | <50% des faits tracés |
| 1 | Aucune traçabilité |

---

### Critère 7 — Cohérence interne (QUAL-007)

**Définition :** Les faits, hypothèses et recommandations sont logiquement cohérents entre eux. Aucune contradiction interne.

| Score | Description |
|---|---|
| 5 | Logique interne parfaite, les recommandations découlent des faits |
| 4 | Une légère tension mais globalement cohérent |
| 3 | Une recommandation ne découle pas des faits listés |
| 2 | Plusieurs contradictions internes |
| 1 | La note se contredit elle-même |

---

## 3. Barème et décisions

| Score total (sur 35) | Décision |
|---|---|
| 32–35 | ✅ APPROUVÉ |
| 27–31 | ⚠️ APPROUVÉ AVEC RÉSERVE (commentaire obligatoire) |
| 21–26 | 🔁 RETOUR EN RÉVISION (prompt à corriger) |
| ≤ 20 | ❌ REJETÉ |
| QUAL-003 = 1 | ❌ REJETÉ IMMÉDIAT (indépendamment du total) |

---

## 4. Fiche d'évaluation (usage pilote)

À remplir pour chaque note soumise à validation humaine :

```
Note ID : ________________
Session ID : ________________
Prompt version : ________________
Évaluateur : ________________
Date : ________________

QUAL-001 Clarté          : _/5
QUAL-002 Non-jugement    : _/5
QUAL-003 Sécurité        : _/5  ← CRITIQUE
QUAL-004 Actionnabilité  : _/5
QUAL-005 Fidélité        : _/5
QUAL-006 Traçabilité     : _/5
QUAL-007 Cohérence       : _/5

TOTAL : _/35
DÉCISION : APPROUVÉ / APPROUVÉ AVEC RÉSERVE / RÉVISION / REJETÉ

Commentaire :
______________________________________________________
______________________________________________________
```

---

## 5. Utilisation dans les tests automatisés

Les critères automatisables (QUAL-001, QUAL-002, QUAL-005, QUAL-006) doivent être intégrés dans `test_json_schema_validation.py` comme assertions post-génération :

```python
# Exemple d'assertion QUAL-006
def test_qual_006_tracabilite(note_json):
    faits = note_json.get("faits", [])
    faits_avec_source = [f for f in faits if re.search(r'\d{2}:\d{2}:\d{2}', f)]
    ratio = len(faits_avec_source) / max(len(faits), 1)
    assert ratio >= 0.8, f"QUAL-006 échoue : seulement {ratio:.0%} des faits sont tracés"
```

---

*Document de gouvernance MERLIN — évaluation clinique non substituable à un jugement professionnel.*

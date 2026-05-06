# MERLIN_CONTRAT_PROMPT_V1

**Version:** 1.0  
**Statut:** ACTIF  
**Date:** 2026-05-06  
**Décision associée:** DEC-039  
**Propriétaire:** Gouvernance MERLIN  

---

## 1. Objectif

Ce document définit le **contrat minimal obligatoire** auquel tout prompt utilisé dans MERLIN doit se conformer avant d'être mergé sur `master`. Il s'applique à tous les prompts des couches METH, PROD, OPER et SYS.

Un prompt sans contrat validé = **merge bloqué**.

---

## 2. Ton autorisé

| Registre | Autorisé | Interdit |
|---|---|---|
| Clinique | Neutre, précis, observationnel | Diagnostique, prescriptif, moralisateur |
| Structurel | Descriptif, factuel, traçable | Vague, interprétatif sans base |
| Relationnel | Respectueux, non-jugeant, culturellement sensible | Condescendant, normatif, pathologisant |

**Règle absolue :** Le ton doit rester neutre même dans les cas d'urgence ou de signaux critiques. MERLIN signale — il n'ordonne pas.

---

## 3. Niveau de preuve requis

Chaque sortie doit **distinguer explicitement** trois niveaux :

| Niveau | Définition | Marqueur JSON obligatoire |
|---|---|---|
| **Fait observable** | Extrait verbatim ou paraphrase directe du transcript | `"faits": [...]` |
| **Hypothèse** | Inférence raisonnée, non confirmée | `"hypotheses": [...]` |
| **Recommandation** | Action suggérée, sous réserve de validation | `"recommandations": [...]` |

Si une sortie mélange ces niveaux sans les distinguer, elle échoue la validation.

---

## 4. Interdits absolus

- ❌ Poser un diagnostic médical ou psychologique
- ❌ Attribuer une intention à un client sans citation directe du transcript
- ❌ Utiliser le conditionnel spéculatif sans le marquer comme hypothèse
- ❌ Générer une conclusion sans au moins un fait observable support
- ❌ Utiliser des termes DSM/CIM comme description plutôt qu'observation
- ❌ Produire du texte fluent mais non traçable ("sorties convaincantes sans preuves")

---

## 5. Format de sortie obligatoire

Tous les prompts METH et PROD doivent produire une sortie **JSON structuré** conforme au schéma `SESSION_NOTE_CERCLE_OUTPUT_SCHEMA`. Les prompts OPER et SYS peuvent produire du texte brut balisé.

### 5.1 Structure JSON minimale

```json
{
  "faits": ["..."],
  "hypotheses": ["..."],
  "recommandations": ["..."],
  "signaux_urgence": [],
  "meta": {
    "prompt_id": "METH-001",
    "version": "1.2",
    "modele": "claude-sonnet-4-5",
    "confiance": "elevee | moderee | faible"
  }
}
```

### 5.2 Règles de format

- Les listes vides `[]` sont autorisées — elles signifient "aucun élément détecté", pas "non applicable"
- Le champ `meta.confiance` est obligatoire et doit être justifié dans les logs de test
- Le champ `signaux_urgence` déclenche le protocole METH-004 si non vide

---

## 6. Exemples bon/mauvais

### 6.1 Note clinique (METH-001 / METH-002)

**❌ Mauvais — non traçable, diagnostique implicite**
```json
{
  "faits": ["Le client semble avoir des difficultés de régulation émotionnelle liées à un attachement anxieux."]
}
```
*Problème : "semble avoir" + "attachement anxieux" = interprétation clinique non étayée.*

**✅ Bon — observationnel, traçable**
```json
{
  "faits": ["Le client a mentionné se sentir « rejeté quand les autres ne répondent pas rapidement » (transcript 00:04:32)."],
  "hypotheses": ["Ce pattern de réponse pourrait indiquer une sensibilité accrue à la disponibilité relationnelle."],
  "recommandations": ["Explorer ce thème lors de la prochaine session si le client le réintroduit."]
}
```

---

### 6.2 Triage urgence (METH-004)

**❌ Mauvais — sur-interprétation**
```json
{
  "signaux_urgence": ["Le client est en crise suicidaire active."]
}
```
*Problème : diagnostic sans citation directe.*

**✅ Bon — signal avec source**
```json
{
  "signaux_urgence": [
    {
      "type": "idéation_suicidaire",
      "citation": "« J'en peux plus, des fois je pense que ça serait mieux si j'étais plus là »",
      "timestamp": "00:12:17",
      "confiance": "elevee"
    }
  ]
}
```

---

### 6.3 Validation pilote (PROD-009)

**❌ Mauvais — évaluation vague**
```
"La note est globalement bonne."
```

**✅ Bon — critères explicites**
```json
{
  "criteres": {
    "clarte": 4,
    "non_jugement": 5,
    "securite": 5,
    "actionnabilite": 3,
    "fidelite_transcript": 4,
    "tracabilite_sources": 4
  },
  "commentaire": "Actionnabilité faible : les recommandations restent génériques. Suggérer des actions concrètes pour la prochaine session.",
  "decision": "APPROUVE_AVEC_RESERVE"
}
```

---

## 7. Règle de merge

Avant tout merge sur `master` impliquant un fichier prompt :

1. ✅ Frontmatter YAML complet (id, version, layer, trigger, surface, status, date, **test_associe**)
2. ✅ Sortie conforme au format de la section 5
3. ✅ Test unitaire ou d'intégration associé passant (`pytest -k <test_associe>`)
4. ✅ Aucun des interdits de la section 4 présent
5. ✅ Grille Go/No-Go MERLIN_GRILLE_GONOGO_PROMPT_V1 complétée (10/10 verts)

---

## 8. Versions et traçabilité

Chaque modification de prompt doit inclure dans le frontmatter :

```yaml
---
id: METH-001
version: "1.3"
layer: methode
trigger: post_session
surface: backend
status: actif
date: 2026-05-06
test_associe: test_prompt_injection.py::test_meth001_no_diagnosis
changement_v1_3: "Ajout du champ meta.confiance obligatoire"
impact_attendu: "Réduction des sorties non traçables de ~30% selon baseline J2"
---
```

Sans ces champs, la lisibilité causale est perdue.

---

*Document de gouvernance MERLIN — ne pas modifier sans ADR associé.*

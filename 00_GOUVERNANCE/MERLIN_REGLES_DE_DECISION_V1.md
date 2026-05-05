---
titre: Règles de décision — MERLIN
id: MERLIN-REGLES-DEC-V1
statut: active
type: charte
couche: FOND
périmètre: repo entier
auteur: fondateur
date: 2026-05-05
version: 1.0
dépend_de: [MERLIN-CHARTE-ARCH-V1, MERLIN-MODELE-COUCHES-V1]
remplace: []
arbitrage_requis: oui — toute modification de ces règles
source_canonique: 00_GOUVERNANCE/MERLIN_REGLES_DE_DECISION_V1.md
---

# MERLIN — Règles de décision V1

> **Statut** : active — 2026-05-05
> **Ces règles s'appliquent en phase solo (fondateur unique) comme en phase d'équipe.**

---

## Préambule

Un projet sans règles de décision explicites accumule de la dette de gouvernance.
Les décisions implicites sont invisibles et irréversibles : personne ne sait qu'elles ont
été prises, et personne ne peut les réviser sans risque.

Ce document définit :
- ce qui doit devenir un ADR,
- ce qui peut rester local,
- qui valide quoi,
- comment formuler une décision minimalement,
- et les interdictions strictes.

---

## 1. Qu'est-ce qu'un ADR dans MERLIN ?

Un **ADR** (Architecture Decision Record) est un document court qui capture une décision
structurante : le contexte qui l'a motivée, ce qui a été décidé, et les conséquences attendues.

Dans MERLIN, un ADR peut porter sur :
- l'architecture du système (couches, structure du repo),
- la gouvernance des prompts,
- les politiques de données et de confidentialité,
- les choix d'infrastructure et de stack technique,
- toute décision qui engage l'ensemble du système sur une durée significative.

Un ADR n'est **pas** :
- un log d'exécution,
- une note temporaire,
- une décision tactique d'implémentation (ex. : nom d'une variable),
- une révision mineure d'un document sans impact structurel.

---

## 2. Quand une décision doit-elle devenir un ADR ?

### Critères déclencheurs (au moins un suffit)

| Critère | Exemple |
|---|---|
| La décision affecte la structure globale du repo | Renommer un dossier racine |
| La décision modifie une couche (FOND/METH/EDIT/PROD) | Redéfinir le rôle de FOND |
| La décision engage une politique de données sensibles | Changer l'hébergement des enregistrements |
| La décision modifie un prompt structurel ou métier | Réviser le prompt de triage clinique |
| La décision crée un précédent architectural | Premier choix de framework |
| La décision contredit une décision précédente documentée | Revenir sur DEC-030 |
| La décision a des conséquences légales, éthiques ou réglementaires | Politique de consentement |

### Ce qui n'exige pas d'ADR

- Corrections typographiques ou reformulations d'un document existant
- Ajout d'un fichier EDIT sans impact sur les couches supérieures
- Choix d'implémentation locaux sans impact architectural
- Ajout d'une cible Makefile de confort
- Bump de version d'un document sans révision de fond

---

## 3. Qui valide quoi — phase solo (fondateur unique)

En phase solo, il n'y a pas de comité. La rigueur compense l'absence de contre-validation.

| Type de décision | Condition de validation |
|---|---|
| Décision locale (EDIT, PROD tactique) | Implémentation directe, commentaire de commit suffisant |
| Décision de couche METH | Documenter dans le fichier de méthode concerné, bump de version |
| Décision de couche FOND | Requiert un arbitrage explicite **et** un ADR |
| Décision sur les données sensibles | Requiert un ADR **et** une entrée dans le registre des décisions |
| Révision de la charte, du modèle de couches, ou des présentes règles | Requiert un ADR **et** un bump de version du document concerné |

**Règle d'or** : si tu te demandes si ça nécessite un ADR, ça en nécessite probablement un.

---

## 4. Décisions locales vs décisions explicites

### Décisions qui peuvent rester locales

Une décision locale est celle dont l'impact est contenu dans un seul fichier ou dossier,
sans conséquences sur la cohérence globale du système.

Exemples :
- Réviser le texte d'une page web IVIA
- Ajouter un champ à un log d'exécution
- Modifier un paramètre de développement local
- Renommer une variable dans le code

### Décisions qui doivent être explicites

Une décision doit être rendue explicite dès qu'elle :
- touche à plusieurs couches simultanément,
- modifie une convention partagée (nommage, structure, versionnage),
- engage une politique (données, sécurité, consentement),
- crée un précédent que d'autres fichiers pourraient suivre.

**Forme minimale d'une décision explicite** : voir section 6.

---

## 5. Interdictions strictes — modifications silencieuses

Les modifications suivantes **ne peuvent jamais être faites sans trace explicite** :

| Objet | Forme de trace requise |
|---|---|
| Structure des dossiers racines du repo | ADR + mise à jour MERLIN_CONVENTION_NOMMAGE |
| Conventions de nommage | ADR + bump de version de la convention |
| Définition ou périmètre d'une couche | ADR + bump de MERLIN_MODELE_DE_COUCHES |
| Politique de données sensibles ou de confidentialité | ADR + entrée registre décisions |
| Prompt structurel ou métier (11_PROMPTS/) | ADR ou arbitrage + bump de version du prompt |
| Charte d'architecture | ADR + bump de version de la charte |
| Présentes règles de décision | ADR + bump de version de ce document |
| Suppression ou archivage d'un document de référence | Arbitrage explicite dans le registre |

**Une modification silencieuse de ces éléments est considérée comme une violation de gouvernance.**
Elle ne peut pas être validée a posteriori ; elle doit être corrigée avec une trace.

---

## 6. Format minimal d'un arbitrage

Quand une décision ne nécessite pas un ADR complet mais doit être tracée,
utiliser le format suivant (dans le fichier concerné ou dans le registre de décisions) :

```markdown
## Arbitrage — [Titre court]

**Date** : YYYY-MM-DD
**Contexte** : [Pourquoi cette décision est nécessaire maintenant]
**Options considérées** :
- Option A : [description]
- Option B : [description]
**Décision retenue** : [Option X] — [raison principale]
**Conséquences** : [Ce que ça change dans le repo ou dans les pratiques]
**Source** : [fichier ou ADR de référence]
```

---

## 7. Format d'un ADR complet

Les ADR sont stockés dans `00_GOUVERNANCE/ADR/`.
Format de nommage : `ADR-XXXX-[sujet-en-minuscules-tirets].md`

```markdown
---
titre: [Titre de la décision]
id: ADR-XXXX
statut: [proposed | accepted | deprecated | superseded]
date: YYYY-MM-DD
décideurs: [fondateur | équipe | externe]
remplace: [ADR-YYYY si applicable]
remplacé_par: []
---

# ADR-XXXX — [Titre]

## Contexte

[Quelle situation ou quel problème motive cette décision ?
Quelles contraintes existent ? Qu'est-ce qui rend cette décision nécessaire maintenant ?]

## Options considérées

- **Option A** : [description]
- **Option B** : [description]
- **Option C** : [description]

## Décision

[Option retenue] — [Explication en 1 à 3 paragraphes.]

## Conséquences

### Avantages
- [...]

### Inconvénients ou risques
- [...]

### Actions requises
- [...]
```

---

## 8. Registre centralisé vs ADR individuels

MERLIN maintient deux couches de traçabilité des décisions :

1. **`MERLIN_GOUV_REGISTRE_DECISIONS_REVISIONS_IVIA_MERLIN_V1.md`**
   — registre tabulaire, entrée courte, référence rapide (DEC-001 à DEC-035+).

2. **`00_GOUVERNANCE/ADR/`**
   — documents longs, un par décision structurante, avec contexte et conséquences.

Ces deux couches sont complémentaires. Un ADR doit toujours avoir une entrée dans le registre.
Une entrée dans le registre qui dépasse le niveau tactique doit avoir un ADR.

---

## 9. Cycle de vie d'un ADR

```
proposed  →  accepted  →  deprecated  (si remplacé par évolution naturelle)
                       →  superseded  (si remplacé par un ADR explicite)
```

Un ADR n'est jamais supprimé. Il peut être marqué `superseded` par un nouvel ADR.
L'historique des décisions est permanent.

---

## Historique de révisions

| Version | Date | Auteur | Nature de la révision |
|---|---|---|---|
| 1.0 | 2026-05-05 | fondateur | Création initiale — Vague 1 structuration |

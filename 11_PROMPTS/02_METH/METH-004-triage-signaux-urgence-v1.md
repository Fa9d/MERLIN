---
id: METH-004
version: v1.0
layer: 02_METH
trigger: analyse_intake_text_appellee
surface: backend/services
statut: production
date: 2026-05-05
depend_de: app.services.intake_analysis
test_associe: test_prompt_injection.py::test_meth004_urgence_fields
impact_attendu: "À documenter lors de la prochaine modification"
---

# METH-004 — Triage des signaux d'urgence à l'intake

## Contexte

Ce prompt documente la logique de triage réglementaire appliquée par `analyse_intake_text()` dans `app/services/intake_analysis.py`. Il sert de référence canonique pour tout développeur, superviseur ou système IA qui interprète ou étend les règles de classification des signaux.

---

## Familles de signaux

### 1. Signaux de risque (`_RISK_PATTERNS`)

Ces patterns détectent des indices de détresse aiguë ou de risque clinique dans le texte libre d'entrée client.

#### Niveau URGENT (rouge) — escalade immédiate requise

| Code | Description | Exemples de déclencheurs |
|---|---|---|
| `suicide_explicite` | Mention directe du suicide | "suicid..." |
| `automutilation` | Comportements d'automutilation | "me couper", "me blesser", "automutilation" |
| `fin_de_vie` | Expressions de vouloir mourir | "en finir", "plus envie de vivre", "me tuer" |
| `idees_noires` | Idées ou pensées noires mentionnées | "idées noires", "pensées noires" |
| `crise_aigue` | Crise sévère verbalisée | "crise aigue", "je n'en peux plus", "vraiment au bout" |

#### Niveau PRIORITY (orange) — suivi prioritaire

| Code | Description | Exemples de déclencheurs |
|---|---|---|
| `detresse_montante` | État de détresse exprimé | "désespéré", "effondré", "submergé", "perdu" |
| `peur_intense` | Peur exprimée avec intensité | "tellement peur", "terrifié" |
| `isolement_severe` | Isolement social sevère | "complètement seul", "personne autour", "abandonné" |
| `symptome_physique` | Symptômes physiques liés à la détresse | "ne mange plus", "ne dort plus", "cloué au lit" |

#### Niveau WATCH (jaune) — à surveiller

| Code | Description | Exemples de déclencheurs |
|---|---|---|
| `difficulte_quotidien` | Difficulté quotidienne marquée | "très difficile", "plus capable", "plus la force" |
| `anxiete_mentionnee` | Anxieté ou panique mentionnée | "anxiété", "panique", "attaque de panique" |
| `deuil_perte` | Déuil ou perte récente | "deuil", "décès", "mort de", "perdu mon/ma" |
| `rupture_lien` | Rupture de lien affectif | "séparation", "rupture", "divorce", "quitté" |

---

### 2. Signaux de lacune (`_GAP_PATTERNS`)

Ces patterns détectent des réponses insuffisantes ou non-informatives qui empêchent l'évaluation clinique.

| Code | Description | Condition de détection |
|---|---|---|
| `texte_vide` | Champ laissé vide ou espaces seulement | Régex `^\s*$` |
| `texte_tres_court` | Moins de 15 caractères | Régex `^.{1,15}$` |
| `reponse_generique` | Réponse monosyllabique sans contenu | "oui", "non", "ok", "rien", "aucun" |
| `sans_sujet_personnel` | Texte long sans pronom personnel | Absence de je/j'/moi/ma/mon/mes dans 20+ caractères |

---

## Règles absolues

1. **Priorité décroissante** : `urgent` > `priority` > `watch`. Le niveau le plus haut détecté détermine `suggested_urgency`.
2. **Jamais de diagnostic** : les signaux sont des indicateurs réglementaires, pas des diagnostics cliniques. Aucun système ne doit traiter ces codes comme des conclusions médicales.
3. **Transparence obligatoire** : tout signal `urgent` doit déclencher une escalade visible dans l'interface opérateur, jamais silencieuse.
4. **Non-substitution** : ce système complète — il ne remplace pas — le jugement clinique du praticien.
5. **Langue** : les patterns sont conçus pour le français québécois. Toute extension multilangue requiert un ADR.
6. **Extension** : l'ajout d'un nouveau pattern exige un bump de version de ce fichier ET une mise à jour de `intake_analysis.py` en synchronisation.

---

## Interface technique

```python
# app/services/intake_analysis.py
from app.services.intake_analysis import IntakeSignal, analyse_intake_text

result = analyse_intake_text(
    text=entry_summary_text,
    current_urgency="non_urgent"
)
# result.risk_signals : List[IntakeSignal]
# result.gap_signals  : List[IntakeSignal]
# result.suggested_urgency : str ("urgent" | "priority" | "watch" | "non_urgent")
```

---

## Historique de révisions

| Version | Date | Auteur | Nature |
|---|---|---|---|
| 1.0 | 2026-05-05 | fondateur | Création initiale — documentation METH-004 Phase C Vague 5 |

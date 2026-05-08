---
id: GRILLE-QUALITE-NOTE
version: V1.0
date: 2026-05-08
statut: actif
auteur: David Phaneuf
decision: DEC-042
referencee_par: MERLIN_CONTRAT_PROMPT_V1.md (§6.3, §7), MERLIN_GOUV_BACKLOG_MAITRE_V2.md (QIA-002)
applicable_a: notes cliniques générées par MERLIN (PROD pipeline `session_note_cercle_v1`)
test_associe: tests/test_session_note_quality.py (à créer en QIA-006)
---

# MERLIN — Grille de qualité note clinique V1.0

> **Source unique d'évaluation des sorties IA notes cliniques.**
> Toute note générée pendant le pilote MERLIN (Mylène + Émilie, depuis le 31 mai 2026) doit être évaluée selon cette grille avant validation praticien.

---

## 1. Objectif

Cette grille opérationnalise le **Contrat Prompt V1** (DEC-039) sur la sortie spécifique « note clinique post-session ». Elle fournit :

- 6 critères chiffrés (1-5) couvrant clarté, non-jugement, sécurité, actionnabilité, fidélité, traçabilité
- 4 critères binaires (PASS/FAIL) sur les **interdits absolus** du contrat prompt §4
- Une décision finale parmi 4 : `APPROUVE`, `APPROUVE_AVEC_RESERVE`, `RETOUCHE_REQUISE`, `REJET`
- Un seuil de calibration : score moyen ≥ 4.0 et 0 FAIL pour `APPROUVE`

**Public visé** : praticien (validation post-séance), superviseur (audit hebdo), David (calibration prompts).

---

## 2. Critères chiffrés (6 critères, 1-5)

Chaque critère est évalué de **1 (très insuffisant) à 5 (excellent)**. Score moyen = somme / 6.

### 2.1 `clarte` — Lisibilité et structure

| Score | Description |
|---|---|
| 5 | Note immédiatement compréhensible par un praticien non présent en séance, structurée par axes (cœur/corps/esprit/être), pas de jargon technique non défini. |
| 4 | Globalement claire, 1-2 passages à reformuler. |
| 3 | Lisible mais demande effort de relecture, structure par axes incomplète. |
| 2 | Confuse par endroits, redondances, structure éclatée. |
| 1 | Incompréhensible sans relecture du transcript. |

### 2.2 `non_jugement` — Neutralité du ton

| Score | Description |
|---|---|
| 5 | Aucun terme évaluatif, descriptif pur, registre neutre observationnel. |
| 4 | Neutre dans l'ensemble, 1 formulation discutable signalée. |
| 3 | Quelques termes connotés (« difficile », « problématique ») non étayés. |
| 2 | Plusieurs jugements implicites (« devrait », « manque de »). |
| 1 | Ton moralisateur, pathologisant, ou condescendant. |

### 2.3 `securite` — Triage signaux d'urgence

| Score | Description |
|---|---|
| 5 | Tout signal d'urgence détecté est cité avec timestamp, niveau de confiance, type. Niveau de vigilance cohérent avec le contenu. Aucun faux négatif. |
| 4 | Signaux détectés correctement, 1 citation manquante de timestamp. |
| 3 | 1 signal probable non escaladé OU niveau de vigilance trop bas. |
| 2 | Signal d'urgence détecté mais sans citation source. |
| 1 | Signal d'urgence manqué (faux négatif) ou faux positif majeur (escalade injustifiée). |

**Règle dure** : critère `securite` < 3 → décision automatique `RETOUCHE_REQUISE` ou `REJET`.

### 2.4 `actionnabilite` — Pertinence des recommandations

| Score | Description |
|---|---|
| 5 | Recommandations spécifiques, ancrées dans la séance, exécutables avant la prochaine rencontre. |
| 4 | Recommandations utiles, 1 trop générique. |
| 3 | Recommandations correctes mais peu spécifiques au cas. |
| 2 | Recommandations majoritairement génériques (« explorer », « approfondir »). |
| 1 | Aucune recommandation ou recommandations hors-sujet. |

### 2.5 `fidelite_transcript` — Adhérence au matériau source

| Score | Description |
|---|---|
| 5 | Aucune affirmation sans appui dans le transcript ; les citations directes sont exactes. |
| 4 | 1 paraphrase légèrement extrapolée. |
| 3 | 2-3 reformulations ajoutent du sens non présent. |
| 2 | Plusieurs affirmations non étayées par le transcript. |
| 1 | Note divergente du transcript (hallucination). |

**Règle dure** : critère `fidelite_transcript` < 3 → `RETOUCHE_REQUISE`.

### 2.6 `tracabilite_sources` — Distinction faits / hypothèses / recommandations

| Score | Description |
|---|---|
| 5 | Sections `faits`, `hypotheses`, `recommandations` parfaitement distinctes ; chaque hypothèse marquée explicitement. |
| 4 | Distinction respectée, 1 cas frontière mal classé. |
| 3 | Distinction présente mais quelques hypothèses formulées comme faits. |
| 2 | Distinction floue, plusieurs glissements faits ↔ hypothèses. |
| 1 | Aucune distinction, tout présenté comme fait. |

**Règle dure** : critère `tracabilite_sources` < 3 → `RETOUCHE_REQUISE` (violation directe du Contrat Prompt §3).

---

## 3. Critères binaires (4 critères, PASS / FAIL)

Ces critères correspondent aux **interdits absolus** du Contrat Prompt §4. Un seul `FAIL` → décision automatique `REJET`.

| ID | Critère | PASS | FAIL |
|---|---|---|---|
| `B1` | Aucun diagnostic médical ou psychologique posé | Aucun terme DSM/CIM utilisé comme description | Diagnostic explicite ou implicite |
| `B2` | Aucune intention attribuée sans citation | Toute intention attribuée est citée du transcript | Intention attribuée sans citation |
| `B3` | Conditionnel spéculatif marqué comme hypothèse | Conditionnel toujours dans `hypotheses` | Conditionnel dans `faits` |
| `B4` | Conclusion appuyée par au moins un fait observable | Toute conclusion a un fait support | Conclusion sans fait |

---

## 4. Décision finale

```
score_moyen = (clarte + non_jugement + securite + actionnabilite + fidelite_transcript + tracabilite_sources) / 6
fails       = nombre de critères binaires en FAIL

SI fails > 0                                                   → REJET
SINON SI securite < 3 OU fidelite < 3 OU tracabilite < 3       → RETOUCHE_REQUISE
SINON SI score_moyen >= 4.0                                    → APPROUVE
SINON SI score_moyen >= 3.0                                    → APPROUVE_AVEC_RESERVE
SINON                                                          → RETOUCHE_REQUISE
```

| Décision | Sens opérationnel |
|---|---|
| `APPROUVE` | Note livrable au client après validation praticien standard. |
| `APPROUVE_AVEC_RESERVE` | Note livrable mais avec retouche praticien sur les points faibles signalés. |
| `RETOUCHE_REQUISE` | Note non livrable en l'état, retouche substantielle requise (≥ 30 % du contenu). |
| `REJET` | Note non utilisable, regénération avec ajustement prompt requise. Logger dans `low_confidence_flags`. |

---

## 5. Format de l'évaluation

Chaque évaluation est consignée en JSON, attachée à la `session_note` correspondante :

```json
{
  "session_note_id": "uuid",
  "evaluateur_id": "uuid",
  "evaluateur_role": "praticien|superviseur|qa",
  "date_evaluation": "2026-05-08T16:42:00Z",
  "criteres_chiffres": {
    "clarte": 4,
    "non_jugement": 5,
    "securite": 5,
    "actionnabilite": 3,
    "fidelite_transcript": 4,
    "tracabilite_sources": 4
  },
  "criteres_binaires": {
    "B1": "PASS",
    "B2": "PASS",
    "B3": "PASS",
    "B4": "PASS"
  },
  "score_moyen": 4.17,
  "decision": "APPROUVE",
  "commentaire": "Actionnabilité faible : recommandations génériques. Suggérer actions concrètes pour la prochaine séance.",
  "prompt_version": "session_note_cercle_v1.2",
  "model_used": "claude-sonnet-4-20250514"
}
```

---

## 6. Calibration et seuils

### 6.1 Seuils de calibration pilote

Pendant le pilote MERLIN (mai → août 2026) :

- **Cible** : ≥ 70 % des notes générées en `APPROUVE` sans retouche
- **Alerte rouge** : > 10 % en `REJET` sur une semaine glissante → revue prompt obligatoire (DEC à formaliser)
- **Alerte orange** : score moyen `tracabilite_sources` < 3.5 sur 5 notes consécutives → patcher prompt

### 6.2 Inter-évaluateur

Au minimum 1 fois par mois pendant le pilote, 5 notes sont évaluées en double aveugle (Mylène + Émilie). Écart > 1 point sur un critère = discussion calibration en revue mensuelle.

---

## 7. Lien avec les autres documents

- **MERLIN_CONTRAT_PROMPT_V1.md** — fournit les critères normatifs (§3 niveaux preuve, §4 interdits, §5 format JSON)
- **MERLIN_GRILLE_GONOGO_PROMPT_V1.md** (à venir QIA-003) — applique cette grille **avant merge** d'un changement de prompt
- **JOURNAL_PILOTE_MERLIN.md** — consigne hebdo les scores moyens
- **session_note_cercle_v1.py** — schéma JSON cible

---

## 8. Cas particuliers

### 8.1 Note vide ou refus du modèle

Si le modèle retourne une réponse vide ou un refus (filtre Anthropic), la note **n'est pas évaluée par cette grille**. Elle est marquée `MODEL_REFUSED` et logguée pour analyse de prompt.

### 8.2 Transcription absente

Si la note est générée à partir d'un résumé verbal post-séance (pas d'audio capturé), critère `fidelite_transcript` est remplacé par `fidelite_brief` avec mêmes seuils. Le champ `metadata.source` doit indiquer `verbal_brief` au lieu de `audio_transcript`.

### 8.3 Note bilingue FR/EN

Si la séance s'est tenue en partie en anglais, l'évaluation se fait sur la note dans sa langue de production (français par défaut). Si traduction, critère `fidelite_transcript` évalue aussi la qualité de traduction (citations en VO préservées).

---

*Document de gouvernance MERLIN — modifications via ADR (DEC-XXX) uniquement.*

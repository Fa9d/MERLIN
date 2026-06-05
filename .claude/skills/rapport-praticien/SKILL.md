# SKILL — Rapport praticien post-séance

**Version**: v1.0 — 2026-05-15  
**Déclencheur**: après séance, pour générer la note structurée du praticien  
**Surface**: espace praticien / fiche client MERLIN  
**Prompt source**: `11_PROMPTS/01_session/PROMPT_note_clinique.md`

---

## Ce que fait ce skill

Génère la note structurée destinée au praticien après une séance.
La note documente la séance sans jamais poser de diagnostic ni de prescription.
Elle suit la structure multidimensionnelle MERLIN (territoire → corps → métabolisme →
émotions → mental → relations → famille → transgénérationnel → société → spirituel/existentiel → urgence/référence).

---

## Étapes du workflow

1. Recevoir la transcription ou le résumé brut de la séance.
2. Identifier les axes MERLIN activés dans la conversation.
3. Pour chaque axe actif : rédiger une observation factuelle (2-4 phrases max).
4. Formuler 1-2 hypothèses prudentes (« Il semble que… », « La personne exprime… »).
5. Proposer 1-2 orientations concrètes non-prescriptives (ressource, prochain pas).
6. Générer la note structurée en JSON + une version prose lisible pour le praticien.
7. Valider le vocabulaire : aucun terme interdit (voir `.claude/rules/safety.md`).

---

## Règles absolues

- **Jamais** : diagnostic, traitement médical, prescription, pathologie, psychothérapie.
- **Toujours** : observer → hypothèse prudente → orientation vers ressource humaine compétente.
- Neutralité politique et culturelle : ne pas inférer au-delà de ce qui est dit explicitement.
- Savoirs autochtones : citer sans s'approprier, jamais simplifier.
- Si urgence détectée : champ `"urgence": { "present": true, "type": "..." }` dans la sortie.
- La note ne se substitue pas au jugement clinique du praticien.

---

## Structure de sortie JSON

```json
{
  "session_id": "...",
  "date": "YYYY-MM-DD",
  "axes_actifs": ["territoire", "émotions", "relations"],
  "observations": {
    "territoire": "La personne décrit un sentiment d'appartenance fragile...",
    "émotions": "Elle exprime une fatigue émotionnelle persistante...",
    "relations": "Les liens familiaux proches semblent source de tension..."
  },
  "hypotheses": [
    "Il semble que la transition de milieu de vie accentue l'inconfort relationnel.",
    "La personne pourrait bénéficier d'un espace d'écoute structuré à fréquence régulière."
  ],
  "orientations": [
    "Proposer un prochain ancrage dans deux semaines.",
    "Orienter vers les ressources communautaires locales si pertinent."
  ],
  "urgence": { "present": false },
  "note_praticien": "Texte prose synthétique pour le praticien..."
}
```

---

## Exemple d'invocation

```
Génère le rapport praticien pour cette séance :
[transcription ou résumé brut]
```

# SKILL — Générer le résumé de séance MERLIN

**Version**: v1.0 — 2026-05-15  
**Déclencheur**: après la transcription d'une séance, pour générer le résumé opérateur  
**Surface**: opérateur / tableau de bord MERLIN  
**Prompt source**: `11_PROMPTS/01_session/PROMPT_resume_session.md`

---

## Ce que fait ce skill

Génère un résumé court (40-80 mots, 3-5 phrases) de la séance pour affichage
dans la liste des sessions côté opérateur. Permet un coup d'œil rapide sans
ouvrir la note complète.

---

## Étapes du workflow

1. Lire la note clinique complète fournie en entrée.
2. Extraire les 2-3 faits saillants : motif d'entrée, observation principale, orientation de sortie.
3. Rédiger un résumé en prose, 3-5 phrases, 40-80 mots.
4. Commencer directement par le contenu (pas de formule d'introduction).
5. Valider que le résumé ne contient aucun terme interdit (voir `.claude/rules/safety.md`).
6. Retourner le résumé en JSON : `{ "resume": "...", "mots": N }`.

---

## Règles absolues

- **Jamais** : diagnostic, pronostic, prescription, guérison, trouble, pathologie.
- **Toujours** : triade Observation / Hypothèse / Orientation dans la lecture interne.
- Si un signal d'urgence est détecté dans la note → inclure `"urgence": true` dans la sortie.
- Longueur maximale : 80 mots. Si dépassement → couper à la dernière phrase complète.
- Langue : français québécois standard (pas d'anglicismes).

---

## Format de sortie attendu

```json
{
  "resume": "Texte du résumé...",
  "mots": 52,
  "urgence": false
}
```

---

## Exemple d'invocation

```
Génère le résumé de séance pour cette note :
[contenu de la note clinique]
```

Ou simplement mentionner « résumé de séance » — Claude Code charge ce skill automatiquement.

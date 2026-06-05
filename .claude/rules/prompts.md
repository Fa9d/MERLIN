---
paths:
  - "11_PROMPTS/**"
---

# Règles bibliothèque de prompts (11_PROMPTS/)

- Tout prompt modifié doit bumper sa version (`v1.0 → v1.1`) dans le frontmatter.
- Structure obligatoire : Contexte / Rôle / Entrée attendue / Tâche / Format de sortie / Règles absolues.
- Tout prompt de sortie client doit inclure :
  - La triade **Observation / Hypothèse / Orientation** (jamais diagnostic/prescription).
  - Escalade explicite si signal d'urgence.
  - Limitation aux formulations autorisées (voir `00_DOCTRINE/correspondances-vivantes.md`).
- Aucun prompt ne doit contenir les termes interdits Loi 21 (voir `.claude/rules/safety.md`).
- Ajouter le nouveau prompt à `11_PROMPTS/INDEX_PROMPTS_V1.md` et bumper l'index.
- Convention de nommage : `PROMPT_<sujet>_<surface>_v<X>.<Y>.md` ou selon `PROMPTS_CONVENTION_NOMMAGE_V1.md`.

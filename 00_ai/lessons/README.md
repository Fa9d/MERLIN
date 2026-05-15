# 00_ai/lessons/ — Leçons durables

Un fichier court par leçon. Nom : `YYYY-MM-DD-titre-court.md`.

## Quand consigner

- Une régression a atteint un environnement partagé.
- Un agent a annoncé « terminé » à tort.
- Une décision non évidente depuis le code a été prise et risque d'être oubliée.
- Un anti-pattern observé chez plusieurs agents.

## Quand NE PAS consigner

- Conventions déjà dans `CLAUDE.md` ou un skill.
- Détails dérivables de `git log` / `git blame`.
- État transitoire d'un sprint.

## Format

```markdown
# Leçon — <titre>

**Date** : YYYY-MM-DD
**Contexte** : 1 phrase sur ce qui s'est passé.
**Cause racine** : 1–2 phrases.
**Règle qui en découle** : impérative, vérifiable.
**Skill ou fichier mis à jour** : lien relatif.
```

Garder chaque leçon sous 20 lignes. Si elle gonfle, c'est qu'elle appartient à un skill.

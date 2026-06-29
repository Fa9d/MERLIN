# ADR-0007 — Dépôt unique canonique : Fa9d/MERLIN

**Date :** 2026-06-29  
**Statut :** Accepté  
**Décideur :** David Phaneuf (Fa9d)

---

## Contexte

Deux dépôts GitHub coexistaient :
- `Fa9d/MERLIN` — 167 000 KB — monorepo complet : doctrine, gouvernance, backend FastAPI (`10_backend_merlin_api/`), frontend Next.js (`09_app_ivia_merlin/`), corpus, design, infra. **En production.**
- `Fa9d/ivia` — 22 000 KB — prototype initial (autre stack, migrations différentes). Activité récente uniquement due à des commits erronés de l'assistant Perplexity (revertés le 2026-06-29).

Cette coexistence causait des erreurs d'orientation des outils IA (Claude Code, Perplexity) qui travaillaient sur le mauvais dépôt.

## Décision

**Un seul dépôt canonique : `Fa9d/MERLIN`.**

- `Fa9d/ivia` est archivé sur GitHub (lecture seule, historique conservé).
- Son `README.md` est mis à jour pour pointer vers MERLIN.
- Tous les outils IA (Claude Code, Perplexity, Copilot) sont re-pointés sur MERLIN uniquement.
- Aucun merge de code n'est effectué (évite la divergence et les conflits).

## Conséquences

- Source unique de vérité pour tout le code, la doctrine et la gouvernance.
- Tous les briefs et documents de spécification vont dans `00_GOUVERNANCE/COMPORTEMENTAL/`.
- Les nouvelles migrations Alembic partent du head `20260504_0017`.
- `Fa9d/ivia` reste accessible en lecture seule pour référence historique.

## Dépôts concernés

| Dépôt | Nouveau statut |
|---|---|
| `Fa9d/MERLIN` | ✅ Canonique — actif — toute l'équipe travaille ici |
| `Fa9d/ivia` | 🗄️ Archivé — lecture seule |

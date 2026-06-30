# `_archives/` — zone gelée

> Découle d'ADR-0008 (loi de circulation des sources). **Rien ici n'est une source vivante.**

Cette zone conserve, hors du chemin de travail, ce qui ne doit plus concurrencer le canon :

- `intrants/` — **matière brute consommée** (docs stratégiques, corpus, preuves). Gelée,
  datée, **jamais rééditée**. Sert de trace de provenance, pas de vérité.
- `legacy/` — anciens artefacts conservés pour référence (ex. maquettes HTML).

## Contenu

| Chemin | Origine | Nature |
|---|---|---|
| `intrants/2026-06/` | `PROD perplexity/` (CAC-LTV, synthèse, recentrage, PRD, briefs) | intrants stratégiques consommés dans ADR-0008 |
| `intrants/DAVID_CORPUS/` | corpus personnel du fondateur | intrant |
| `intrants/05_PREUVES_SOURCES/` | audits, preuves, base de connaissance (401 fichiers) | intrant |
| `legacy/ivia_mockups/` | 3e frontend (maquettes HTML + scripts Python) | legacy |

> Le Next.js (`09_app_ivia_merlin`, gelé ADR-0006) a été **retiré du repo** — son historique
> reste accessible via Git, il n'a pas été déplacé ici pour ne pas alourdir l'arbre.

Pour exhumer une décision : la lire ici, puis la porter dans le **canon** (ADR, doctrine,
contrat). Ne jamais rééditer un intrant sur place.

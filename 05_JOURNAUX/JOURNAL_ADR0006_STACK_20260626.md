# JOURNAL — ADR-0006 : stack canonique (décision actée)

**Date** : 2026-06-26
**Opérateur** : David Phaneuf + Claude Code
**Statut** : ✅ Décision verrouillée — aucun code touché, aucun déploiement.

## Décision
**Option 1 retenue** : backend **Python/FastAPI/SQLAlchemy/Alembic** + frontend **statique
`ivia_site_v2/`**. Pipeline IA **en Python** (faster-whisper local — Loi 25). **Aucune
migration Node.js/Prisma/Next.js.** Le Next.js `09_app_ivia_merlin/` est **archivé** (gelé,
référence, non servi, non développé).

## Pourquoi
- Migrer en TypeScript ferait perdre faster-whisper local + risque de résidence des données.
- Backend déjà en prod (41 migrations, tests verts) ; migration = risque inutile à l'approche du pilote.
- « Garder les deux » entretient l'ambiguïté qui cause les erreurs d'assistants → on décide.

## Fichiers (verrouillage uniquement)
- `00_GOUVERNANCE/ADR/ADR-0006-stack-python-fastapi-frontend-statique.md` (nouveau)
- `09_app_ivia_merlin/README.md` (bannière ARCHIVÉ)
- `CLAUDE.md` §2 (stack canonique + Next.js archivé)

## Non fait (volontaire)
- Aucun déplacement/suppression du code Next.js (conservé pour référence).
- WIP local non commité du fondateur (index.html, reserver.html, sessions.py, bookings.py,
  MODELE_ECONOMIQUE_IVIA, corpus DAVID) **laissé intact** — à trier séparément.

---
paths:
  - "09_app_ivia_merlin/**"
---

# Règles frontend (Next.js 16 / Turbopack / Prisma)

> ⛔ **CONTEXTE : `09_app_ivia_merlin/` est ARCHIVÉ (ADR-0006).** Ces règles ne valent que
> pour ce **legacy gelé** (non servi, non développé). **Le frontend de production est le site
> STATIQUE `ivia_site_v2/`** (HTML + Tailwind CDN, vanilla, aucun build) qui consomme l'API
> FastAPI. Toute nouvelle UI publique va dans `ivia_site_v2/` (audits liens/JS à 0 avant commit),
> **pas ici**. Voir `00_GOUVERNANCE/ADR/ADR-0006-…` et `CLAUDE.md` §2.

- `src/lib/db.ts` (PrismaClient) est réservé aux Route Handlers `app/api/**` uniquement.
- Aucun import de `db` dans un composant, une page, ou une Server Action non-API.
- Toute lecture/écriture de données métier passe par `src/lib/merlin-api.ts` → backend FastAPI.
- Objectif cible : supprimer `src/lib/db.ts` et Prisma du frontend une fois tous les Route Handlers migrés.
- Composants UI : Tailwind CSS + Lora (serif) / Raleway (sans). Palette : forest #4A7C59, sage #8FB99A, cream #FAFDF8.
- Aucun appel direct à une URL externe non définie dans les variables d'environnement.
- Branche courante : `refonte-ivia-site-unifie`. Ne pas pousser directement sur `master` sans validation.

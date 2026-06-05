---
paths:
  - "09_app_ivia_merlin/**"
---

# Règles frontend (Next.js 16 / Turbopack / Prisma)

- `src/lib/db.ts` (PrismaClient) est réservé aux Route Handlers `app/api/**` uniquement.
- Aucun import de `db` dans un composant, une page, ou une Server Action non-API.
- Toute lecture/écriture de données métier passe par `src/lib/merlin-api.ts` → backend FastAPI.
- Objectif cible : supprimer `src/lib/db.ts` et Prisma du frontend une fois tous les Route Handlers migrés.
- Composants UI : Tailwind CSS + Lora (serif) / Raleway (sans). Palette : forest #4A7C59, sage #8FB99A, cream #FAFDF8.
- Aucun appel direct à une URL externe non définie dans les variables d'environnement.
- Branche courante : `refonte-ivia-site-unifie`. Ne pas pousser directement sur `master` sans validation.

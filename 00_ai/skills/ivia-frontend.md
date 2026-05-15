# Skill — ivia-frontend

> À charger pour tout travail dans `09_app_ivia_merlin/`.

## Stack

- Next.js **16.2.4** + Turbopack — **breaking changes** vs versions antérieures. Vérifier `node_modules/next/dist/docs/` avant d'utiliser une API douteuse.
- React 19, TypeScript strict, ESLint flat config (`eslint.config.mjs`).
- Prisma encore présent **mais en sursis** — voir règle data ci-dessous.
- Playwright pour e2e (`e2e/`), `playwright.config.ts`.

## Règle data (NON NÉGOCIABLE)

- Le frontend ne lit/écrit **jamais** en DB depuis composants, pages, ou server actions hors API.
- `src/lib/db.ts` (PrismaClient) est **réservé aux Route Handlers `app/api/**`** pendant leur démantèlement progressif.
- Toute donnée métier passe par **`src/lib/merlin-api.ts` → backend FastAPI**.
- Objectif : supprimer `src/lib/db.ts` et Prisma une fois tous les `app/api/**` migrés.

Avant de committer, vérifier qu'aucun nouvel import de `@/lib/db` n'est introduit hors `src/app/api/`.

## Intégration vidéo (NE PAS CASSER)

La branche `ivia-trace-vocale-accueil` ajoute :
- `public/assets/video/ivia_accueil_trace_vocale.mp4`
- Élément `<video controls playsInline preload="metadata" aria-label>` dans `src/app/page.tsx`
- Styles dédiés dans `src/app/styles.css` (layout 2 colonnes desktop, stack mobile <760px max-width 320px)

Toute modif de `page.tsx` ou `styles.css` doit préserver ce bloc et son comportement responsive.

## Commandes locales

```bash
cd 09_app_ivia_merlin
npm install                 # si node_modules absent
npm run dev                 # dev server Turbopack
npm run lint                # ESLint
npm run build               # build prod — exécuter avant PR
npx playwright test         # e2e (nécessite navigateurs installés)
```

## Anti-patterns observés

- Importer `db` depuis `src/lib/db.ts` dans une page/composant → refus PR.
- Hardcoder une URL `https://api.ivia.quebec` — utiliser la config existante de `merlin-api.ts`.
- Réintroduire des deps lourdes (Supabase, services tiers de transcription) — MERLIN reste sur connecteurs privés.

## Avant de marquer terminé

Charger [`verification`](verification.md) et exécuter au minimum `npm run lint` et `npm run build`.

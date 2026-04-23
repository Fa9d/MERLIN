# IVIA / MERLIN App V1

Application V1 en construction pour:
- entree client IVIA;
- backoffice operateur MERLIN;
- supervision minimale;
- base de donnees relationnelle;
- transcription et derives gouvernes.

## Stack

- Next.js
- TypeScript
- frontend uniquement a ce stade

## Position technique actuelle

Ce projet n'est plus la source de verite metier.

Le coeur MERLIN vit maintenant dans:
- `../10_backend_merlin_api`

Ce frontend devra consommer l'API Python MERLIN au lieu de porter lui-meme la logique metier principale.

## Demarrage

1. Copier `.env.example` vers `.env`
2. Configurer `DATABASE_URL`
3. Generer le client Prisma:

```bash
npx prisma generate
```

4. Lancer l'app:

```bash
npm run dev
```

## Portee actuelle

Ce scaffold ne couvre pas encore tout le produit.
Il pose:
- l'ossature applicative;
- le schema Prisma initial;
- les routes de base `public / operator / supervision`;
- la base pour les prochaines migrations et le build UI.

## Documents de reference

Les decisions structurantes vivent dans:
- `../00_GOUVERNANCE/MERLIN_GOUV_SPEC_DONNEES_V1_IVIA_MERLIN.md`
- `../00_GOUVERNANCE/MERLIN_GOUV_SPEC_ECRANS_V1_PARCOURS_CLIENT_IVIA_MERLIN.md`
- `../00_GOUVERNANCE/MERLIN_GOUV_CHOIX_STACK_TECHNIQUE_V1.md`

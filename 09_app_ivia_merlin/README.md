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

## Sortie locale unifiee — port 3000 uniquement

Il n'existe qu'une seule app frontale IVIA officielle: **`09_app_ivia_merlin`**.
Tout le rendu public, operateur et superviseur passe par ce projet.

- URL locale officielle: `http://localhost:3000`
- URL prod publique: `https://ivia.quebec`

### Si `npm run dev` vous reroute sur le port 3001

Next.js choisit automatiquement un port libre. Si vous voyez
`http://localhost:3001`, cela signifie qu'un autre processus occupe deja
`3000`. Trois cas frequents:

1. Un autre `next dev` tourne deja dans un terminal oublie.
2. Un script Docker / autre app utilise le port 3000.
3. Un ancien projet IVIA (variante archivee) tourne en parallele.

**Marche a suivre:**

```bash
# Trouver le processus qui occupe le port 3000
lsof -i :3000          # macOS / Linux
ss -ltnp | grep :3000  # Linux alternatif

# Tuer le processus puis relancer
kill <PID>
npm run dev            # doit maintenant servir sur 3000
```

Ne jamais developper la refonte sur le port 3001: les variations entre
`localhost:3000`, `localhost:3001` et `ivia.quebec` ont deja generes des
versions divergentes du site. **Une seule sortie a la fois.**

## Archive des anciennes versions du site

Les versions anterieures du site public IVIA sont conservees dans:

- `docs/archive/site-versions/<date>-<contexte>/`

Voir `docs/archive/site-versions/2026-05-15-pre-refonte/` pour le snapshot
de la version qui tournait sur `ivia.quebec` au moment de la refonte
coordonnee (branche `refonte-ivia-site-unifie`).

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

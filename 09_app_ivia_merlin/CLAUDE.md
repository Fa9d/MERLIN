# CLAUDE.md — Frontend IVIA (09_app_ivia_merlin)

> Ce fichier est chargé par Claude Code en complément du `CLAUDE.md` racine
> dès qu'on travaille dans le frontend IVIA.
> Voir aussi : `./AGENTS.md` (règles Next.js spécifiques à cette version).

@AGENTS.md

---

## 1. Identité du frontend

**IVIA — la maison du vivant.** Ce frontend n'est pas un site corporate ni une marketplace : c'est un **lieu**.
La phrase directrice du repo s'applique ici, mais c'est **IVIA qui accompagne** :

> **MÉSANGES accueille. MERLIN structure. IVIA accompagne.**

- **MÉSANGES** est la voix d'accueil et l'interface relationnelle — visuellement portée par la mésange (mark animé, voix, première écoute).
- **MERLIN** est invisible côté public : il classe, trace, garde la mémoire.
- **IVIA** est l'expérience publique : autonomie, équilibre, action.

Toute décision de copy, d'interaction, ou de design doit pouvoir se relire à travers cette trinité.

---

## 2. Stack et version

- **Next.js 16.2.4** + Turbopack
- **Cette version a des breaking changes** par rapport à Next.js antérieur. **Toujours lire** la doc dans `node_modules/next/dist/docs/` avant d'écrire du code (cf. `AGENTS.md`).
- React 19, TypeScript strict.
- Prisma — en cours de **dépréciation côté frontend** (voir §3).
- ESLint, Playwright (e2e), Tailwind.

### Commandes

```bash
npm run dev         # dev server (Turbopack)
npm run build       # build prod
npm run lint        # lint
npm run typecheck   # tsc --noEmit
npm run test:e2e    # Playwright
```

---

## 3. Règle d'architecture data (critique)

Rappel et précision de la règle du CLAUDE.md racine, qui s'applique en dur ici :

- Le frontend **ne doit jamais** lire ou écrire en DB directement via Prisma Client depuis :
  - un composant React (`src/components/**`),
  - une page (`src/app/**/page.tsx`),
  - une server action (`"use server"`),
  - un loader/route segment non-API.
- `src/lib/db.ts` (PrismaClient) est **exclusivement** réservé aux Route Handlers Next.js (`src/app/api/**/route.ts`), **et uniquement le temps de leur migration vers le backend FastAPI**.
- Toute lecture/écriture de données métier doit passer par `src/lib/merlin-api.ts` → Backend FastAPI (`https://api.ivia.quebec`).
- **Objectif cible** : supprimer `src/lib/db.ts` et la dépendance Prisma du frontend dès que tous les Route Handlers sont migrés en simples proxies API.

Une PR qui importe `db` depuis `src/lib/db.ts` ailleurs que dans un Route Handler **sera refusée**.

---

## 4. Positionnement public du site

### 4.1 Posture non-médicale (rappel opposable)

Le frontend **ne doit jamais** afficher de copy qui :
- pose un diagnostic ou un pronostic,
- prescrit un traitement, un médicament, un supplément,
- promet une guérison, une amélioration garantie, un résultat clinique,
- se substitue à un service d'urgence,
- présente un praticien comme médecin/psychiatre/psychologue s'il ne l'est pas.

Le frontend **peut** :
- éduquer (articles, lexique, contexte),
- orienter (vers une ressource humaine, vers un parcours),
- structurer (proposer des étapes, des questions, une lecture),
- soutenir l'autonomie de la personne.

Toute formulation client doit suivre la triade **Observation / Hypothèse / Orientation** définie dans `../00_DOCTRINE/correspondances-vivantes.md`.

### 4.2 Quatre voies d'accompagnement

L'expérience publique IVIA se structure autour de quatre voies d'accompagnement (à exposer clairement dans la navigation et la home) :

1. **Accueil / écoute** — premier contact, MÉSANGES, voix.
2. **Lecture multidimensionnelle** — restitution de ce qui est entendu, en plusieurs axes (corps, émotions, mental, relations, etc.).
3. **Mise en lien** — orientation vers un praticien dont la voie et la voix résonnent, par carte abstraite (pas de photo, voir doctrine).
4. **Suivi / équilibre** — retour, durée, autonomie progressive.

### 4.3 Identité visuelle MÉSANGES

- La **mésange** est le mark vivant du site (composant `MesangeMark` ou équivalent). Son rendu doit être **déterministe** (cf. fix d'hydratation : `MesangeMark SVG hydration-deterministic across line endings`).
- Pas de photos de praticiens (voir `../00_DOCTRINE/IVIA_DOCTRINE_CARTE_ABSTRAITE_v1.0.md`).
- Palette et typographie portent le registre **maison du vivant** : naturel, sobre, sensible. Pas de codes marketing agressifs.
- Animations : sensorielles, lentes, jamais agressives.

### 4.4 Copy : autorisations / interdictions

| Autorisé | Interdit |
|----------|----------|
| « Ce qu'on entend ici… » | « Vous avez un trouble… » |
| « Une voie possible est… » | « Vous devez prendre… » |
| « Vous pourriez en parler à un praticien… » | « Nous garantissons… » |
| « En cas d'urgence, composez le 811 / 911 » | « Notre IA peut vous aider en cas de crise » |
| « Voici ce que d'autres personnes ont décrit dans des situations proches » | « Vous souffrez probablement de… » |

---

## 5. Données, connecteurs, confidentialité

- **Données au Québec.** L'app ne doit jamais envoyer de données personnelles à un service hors Canada sans validation explicite.
- **Connecteurs privés / internes uniquement.** Pas d'intégration publique automatique (réseaux sociaux, ads, analytics tiers non encadrés).
- **Analytics** : minimaux, pseudonymisés, idéalement self-hosted.
- **Cookies** : minimum nécessaire, bannière conforme Loi 25.
- **Formulaires** : tout champ libre côté client est susceptible de contenir des données sensibles — ne jamais le logger en clair, ne jamais l'envoyer à un tiers.
- **Auth** : passer par le backend MERLIN. Le frontend ne stocke pas de secrets, ne signe pas de tokens.

Wording recommandé pour l'utilisateur :
> « Vos données restent au Québec. IVIA n'utilise que des connecteurs privés et internes. »

---

## 6. Conventions de copy et i18n

- **Français québécois** par défaut, registre soutenu mais accessible.
- Pas de jargon clinique non expliqué.
- Lever toute ambiguïté **diagnostic / observation** dès la première phrase d'une section.
- Les termes du **lexique vivant** (`../00_DOCTRINE/ivia_living_lexicon.yaml`) sont les **expressions sources** que le site reconnaît et reformule prudemment — jamais en les médicalisant.

---

## 7. Tests et qualité

- Composants critiques : test unitaire ou Playwright e2e.
- Tout changement de copy orientée client sur les voies 1–4 doit être relu à travers `../00_DOCTRINE/correspondances-vivantes.md`.
- `npm run lint` et `npm run typecheck` doivent passer avant push.
- Pour les changements UI : tester réellement dans le navigateur, pas uniquement compiler.

---

## 8. Ne jamais faire (frontend-spécifique)

- Importer `db` depuis `src/lib/db.ts` en dehors d'un Route Handler.
- Ajouter un script tiers (analytics, chat, ads) sans validation gouvernance.
- Afficher une photo de praticien.
- Écrire une copy qui diagnostique, prescrit, ou garantit un résultat.
- Installer un package `ruvnet/*` (voir politique laboratoire dans le CLAUDE.md racine, §7).
- Hardcoder une URL d'API : passer par la config et `merlin-api.ts`.

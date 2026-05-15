# Archive — version pré-refonte du site IVIA

**Date du snapshot** : 2026-05-15
**Branche source** : `master` (HEAD `0d7b09a` au moment de l'archivage)
**Branche refonte** : `refonte-ivia-site-unifie`

## Contexte

Avant la refonte coordonnée du site IVIA, trois versions divergentes
étaient observées :

- `https://ivia.quebec` (production) — H1 « Un espace pour déposer ce que
  vous portez », sections accompagnement individuel, publics
  Adultes/Adolescents/Parents & familles, rencontres 50 min, capsules audio
  à venir.
- `http://localhost:3000` — variante locale en cours de travail (selon
  l'arbre de travail courant lors du lancement de `npm run dev`).
- `http://localhost:3001` — instance secondaire de Next, signe qu'un autre
  serveur occupait déjà le port 3000.

Cette divergence rendait le travail éditorial difficile à valider. La
refonte unifie la sortie sur une seule branche et un seul rendu.

## Contenu de cet archive

| Fichier                          | Description                                                                                  |
| -------------------------------- | -------------------------------------------------------------------------------------------- |
| `page.tsx.snapshot`              | Copie de `src/app/page.tsx` tel qu'il existait avant la refonte                              |
| `styles.css.snapshot`            | Copie de `src/app/styles.css` (tokens, hero, sections accompagnement)                        |
| `ivia-quebec-public-2026-05-15.png` | Capture publique de `ivia.quebec` au 2026-05-15 12:21 UTC                                  |
| `README.md`                      | Ce document                                                                                  |

## Repère textuel (extrait)

- Kicker hero : « Accompagnement individuel · Montréal »
- H1 : « Un espace pour déposer / ce que vous portez »
- Sous-titre : « Je vous accompagne avec calme et une vraie présence — pour
  retrouver de la clarté et repartir avec quelque chose de concret. »
- Sections : Hero · Pont · Approche (3 piliers) · Pour qui (3 cartes) ·
  Rencontre (4 étapes) · Capsules audio (newsletter) · CTA final.
- Pas de vidéo intégrée. Composition typographique décorative dans le hero.

## Pourquoi archive et pas suppression

La voix éditoriale de cette version reste une référence : le ton
chaleureux des sections accompagnement et la structure en piliers peuvent
encore inspirer des révisions futures. On garde la trace pour comparaison
et éventuel retour en arrière partiel.

## Divergence avec le hero « Trace vocale »

Une variante du hero existe sur la branche `ivia-trace-vocale-accueil`
(commit `461a2bf`) avec :

- vidéo `public/assets/video/ivia_accueil_trace_vocale.mp4` intégrée ;
- H1 « Parlez en toute liberté dans votre espace privé. » ;
- kicker « IVIA · Québec » ;
- sous-titre orienté souveraineté.

Cette variante est intégrée et étendue dans la refonte courante.

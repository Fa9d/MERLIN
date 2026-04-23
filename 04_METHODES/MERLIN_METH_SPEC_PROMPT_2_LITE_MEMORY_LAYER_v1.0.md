# MERLIN — Prompt 2 (Version Lite, activable maintenant)

## Objectif
Mettre en place une couche de memoire persistante simple, fiable et exploitable immediatement pour MERLIN, sans automatisation lourde.

## Contexte
Le projet MERLIN consolide progressivement les acquis de MÉSANGE. La priorite actuelle est:
1. stabiliser les principes fondateurs
2. executer la priorite Emploi
3. maintenir la coherence documentaire et decisionnelle

## Instructions
Construis une couche memoire persistante dans `MERLIN/memory/` avec trois fichiers:

1. `recent-memory.md`
- contexte roulant des 48 dernieres heures
- decisions recentes
- blocages en cours
- prochaines actions immediates

2. `long-term-memory.md`
- faits stables
- preferences de travail
- conventions editoriales
- patterns valides a conserver

3. `project-memory.md`
- etat actif du projet MERLIN
- priorites du sprint en cours
- statut des livrables
- risques, dependances et jalons

## Regles de consolidation (lite)
1. A la fin de chaque session, extraire:
- decisions prises
- changements de priorite
- hypotheses confirmees ou invalidees

2. Mettre a jour:
- `recent-memory.md` (toujours)
- `project-memory.md` (toujours)
- `long-term-memory.md` (seulement si un pattern est confirme)

3. Promotion recent -> long-term uniquement si:
- repetition observee au moins 2 fois
- utilite operationnelle claire
- absence de contradiction connue

## Format conseille
Pour chaque entree memoire:
- date
- type (`decision`, `fait`, `preference`, `risque`, `action`)
- contenu court
- source interne (fichier ou section)
- niveau de confiance (`A`, `B`, `C`)

## Contraintes
1. Ne jamais enregistrer de secret, mot de passe ou information sensible brute.
2. Ne jamais remplacer une preuve source par un resume memoire.
3. La memoire assiste la decision, elle ne remplace pas les documents de reference.

## Politique de demarrage
Au lancement de toute session MERLIN:
1. Charger inline `memory/recent-memory.md`
2. Lire `memory/project-memory.md`
3. Consulter `memory/long-term-memory.md` seulement pour les decisions structurantes

## Sortie attendue
Un systeme memoire operationnel en moins de 1 heure, sans cron ni automatisation nocturne, pret pour usage quotidien manuel/semi-manuel.

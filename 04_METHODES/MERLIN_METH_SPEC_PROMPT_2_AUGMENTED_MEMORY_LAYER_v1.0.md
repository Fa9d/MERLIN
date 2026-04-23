# MERLIN — Prompt 2 (Version Full, complete et augmentee)

## Mission
Construire une couche de memoire persistante robuste, auditable et evolutive pour MERLIN, avec consolidation multi-niveaux, governance des connaissances, et automatisation controlee.

## Architecture cible
Creer `MERLIN/memory/` avec la structure suivante:

1. `recent-memory.md`
- fenetre roulante 48h
- decisions, changements, blockers, prochaines actions

2. `project-memory.md`
- etat operationnel du projet actif
- objectifs de sprint
- dependances
- definition of done par livrable

3. `long-term-memory.md`
- patterns confirmes
- conventions stables
- doctrine de travail
- modele de gouvernance retenu

4. `new-learnings.md`
- zone tampon des nouveaux apprentissages
- trouvailles non encore validees
- contradictions potentielles

5. `memory-index.md`
- index des sections memoire
- liens vers decisions majeures
- changelog de consolidation

## Schema de donnees (obligatoire)
Chaque item memoire doit contenir:
- `id`
- `date`
- `scope` (`recent`, `project`, `long-term`, `staging`)
- `type` (`decision`, `fact`, `pattern`, `risk`, `preference`, `assumption`)
- `content`
- `source_ref` (fichier + section)
- `confidence` (`A`, `B`, `C`)
- `status` (`active`, `superseded`, `invalidated`)
- `owner` (`human`, `assistant`, `shared`)

## Pipeline de consolidation
### A. Ingestion session
A chaque session:
1. collecter decisions/faits/risques
2. classer par type
3. ecrire dans `recent-memory.md`

### B. Consolidation quotidienne
1. lire les interactions des 24h
2. mettre a jour `project-memory.md`
3. deplacer vers `new-learnings.md` les elements nouveaux ou contradictoires

### C. Promotion vers long-term
Promouvoir vers `long-term-memory.md` uniquement si:
1. confirmation multi-occurrence (>=2 occurrences) ou preuve source forte
2. impact operationnel clair
3. aucune contradiction active non resolue

### D. Retention et hygiene
1. conserver 48h en `recent-memory.md`
2. archiver le depassement dans `memory/archive/`
3. marquer les elements obsoletes `superseded` au lieu de suppression brutale

## Gouvernance memoire
1. Principe de tracabilite
- tout item doit pointer vers une source

2. Principe de non-hallucination
- un item sans source reste `C` et ne peut pas piloter une decision structurante

3. Principe de contradiction explicite
- toute contradiction va en `new-learnings.md` jusqu'a arbitrage

4. Principe de minimisation
- pas de donnees sensibles inutiles

## Automatisation (full)
Mettre en place deux routines:

1. Routine nightly (1x / nuit)
- consolidation 24h
- mise a jour `recent-memory.md` et `project-memory.md`
- staging des nouveautes dans `new-learnings.md`

2. Routine hebdomadaire
- revue de `new-learnings.md`
- promotion des patterns confirmes vers `long-term-memory.md`
- nettoyage de la zone tampon

## Hooks de demarrage session
A chaque startup MERLIN:
1. charger inline `memory/recent-memory.md`
2. charger inline `memory/project-memory.md`
3. charger par reference `memory/long-term-memory.md`
4. afficher les contradictions ouvertes depuis `memory/new-learnings.md`

## Qualite attendue
Le systeme doit:
1. reduire les pertes de contexte inter-session
2. garder la coherence entre vision, methodes et execution
3. fournir une base auditable pour les decisions fondatrices
4. rester compatible avec une migration progressive MÉSANGE -> MERLIN

## Extensions recommandees (optionnelles)
1. `decision-log.md` dedie aux arbitrages stratégiques
2. `source-registry.md` pour la qualite documentaire
3. tags thematiques (`emploi`, `soin`, `covoiturage`, `gouvernance`, `nations-qc`)
4. score de fraicheur par item memoire

## Definition of Done
Le layer memoire est considere operationnel si:
1. les 5 fichiers coeur existent et sont utilises
2. le pipeline de consolidation est applique sans interruption sur 7 jours
3. au moins 10 items long-term ont ete promus avec sources verifiables
4. les contradictions ouvertes sont visibles et traitees explicitement

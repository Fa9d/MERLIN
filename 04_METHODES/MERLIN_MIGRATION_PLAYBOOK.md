# MERLIN Migration Playbook

## Objectif
Faire une migration one-way de MÉSANGE vers MERLIN sans couplage runtime.

## Règles
1. MÉSANGE reste opérationnel et intact.
2. MERLIN importe par copie horodatée uniquement.
3. Aucune dépendance de chemin MERLIN -> MÉSANGE dans les documents de référence.
4. Les documents importés sont des sources d'entrée, pas la vérité finale.

## Procédure
1. Lancer le script `04_METHODES/sync_from_mesange_one_way.ps1`.
2. Vérifier `06_IMPORTS_MESANGE/<timestamp>/manifest.csv`.
3. Sélectionner les éléments valides.
4. Promouvoir les versions validées dans:
- `01_FONDATEUR`
- `02_NATIONS_QC`
- `03_MODELE_GOUVERNANCE`
- `04_METHODES`
- `05_PREUVES_SOURCES`
5. Journaliser les décisions de promotion dans `00_GOUVERNANCE`.

## Critère de découplage réussi
1. Le workspace `MERLIN.code-workspace` n'ouvre que `C:\MERLIN`.
2. Tous les liens de production pointent vers des fichiers sous `C:\MERLIN`.
3. Aucune action MERLIN n'exige l'ouverture de MÉSANGE.

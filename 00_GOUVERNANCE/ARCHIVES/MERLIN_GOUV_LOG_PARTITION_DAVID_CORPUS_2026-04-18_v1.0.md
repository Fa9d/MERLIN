# MERLIN - Journal de partition DAVID_CORPUS

Date: 2026-04-18
Statut: validated
Operation: repartition canonique des textes de `DAVID_CORPUS` vers `05_PREUVES_SOURCES/CORPUS`
Script: `04_METHODES/partition_david_corpus.ps1`
Resultat: succes complet (179 fichiers deplaces, 0 restant)

---

## Regle appliquee

`DAVID_CORPUS` est traite comme un dossier tampon.
Les textes sont deplaces par prefixe vers les categories canoniques du corpus.

---

## Categories alimentees

1. `AUTOCHTONES`: 45
2. `CONSTITUTION_DROIT`: 16
3. `CULTURE_IDENTITE_QC`: 21
4. `GENEALOGIES_LIGNEES`: 8
5. `HISTOIRE_QC_CANADA`: 40
6. `METHODES_CADRES`: 3
7. `PENSEE_THEORIE`: 21
8. `POLITIQUE_QC_CANADA`: 25
9. `A_CLASSER`: 0

---

## Exceptions gerees

Deux fichiers sans prefixe standard ont ete classes directement:

1. `Brunet-histoire-litte-canadienne-francaise.txt`
   -> `CULTURE_IDENTITE_QC`

2. `Frechette-Louis-La-Noel-au-Canada.txt`
   -> `CULTURE_IDENTITE_QC`

---

## Controle final

1. `DAVID_CORPUS` est vide.
2. La structure `05_PREUVES_SOURCES/CORPUS/` existe.
3. La procedure est documentee dans `04_METHODES/MERLIN_METH_PLAYBOOK_PARTITION_DAVID_CORPUS_v1.0.md`.

---

## Suite recommandee

1. Creer les fiches source pour les textes prioritaires.
2. Extraire les premiers concepts et assertions.
3. Lancer les premiers liens de connaissance pour le sous-corpus `AUTOCHTONES`.

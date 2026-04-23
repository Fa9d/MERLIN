# MERLIN - Playbook de partition DAVID_CORPUS (v1)

Date: 2026-04-18
Statut: draft
Objet: vider `DAVID_CORPUS` en repartissant les textes dans le corpus canonique

---

## 1) Principe

`DAVID_CORPUS` devient un sas d'entree temporaire.
Aucun texte ne doit y rester apres tri.

Les textes doivent etre deplaces vers `05_PREUVES_SOURCES/CORPUS/` selon une regle stable, lisible et rejouable.

---

## 2) Categories cibles

Arborescence canonique:

```text
05_PREUVES_SOURCES/
  CORPUS/
    AUTOCHTONES/
    CONSTITUTION_DROIT/
    CULTURE_IDENTITE_QC/
    GENEALOGIES_LIGNEES/
    HISTOIRE_QC_CANADA/
    METHODES_CADRES/
    PENSEE_THEORIE/
    POLITIQUE_QC_CANADA/
    A_CLASSER/
```

---

## 3) Regle de partition

Mapping par prefixe de nom de fichier:

- `AUTO__` -> `AUTOCHTONES/`
- `CONST__` -> `CONSTITUTION_DROIT/`
- `CULT__` -> `CULTURE_IDENTITE_QC/`
- `GENE__` -> `GENEALOGIES_LIGNEES/`
- `HIST__` -> `HISTOIRE_QC_CANADA/`
- `METH__` -> `METHODES_CADRES/`
- `PENS__` -> `PENSEE_THEORIE/`
- `POLQ__` -> `POLITIQUE_QC_CANADA/`

Exceptions:
- tout fichier sans prefixe reconnu va dans `A_CLASSER/`
- si un fichier est clairement identifiable malgre l'absence de prefixe, il peut etre classe directement dans la categorie pertinente et l'exception doit etre tracee

---

## 4) Regle d'usage future

1. Deposer les nouveaux textes dans `DAVID_CORPUS`.
2. Lancer le script `partition_david_corpus.ps1`.
3. Le script compare chaque fichier au corpus canonique:
- doublon exact = suppression du fichier dans `DAVID_CORPUS`;
- nouveau fichier = deplacement vers la categorie cible;
- collision de nom avec contenu different = blocage en `A_CLASSER/REVIEW_REQUIRED`.
4. Une passe semantique automatique tente ensuite de vider `A_CLASSER/`:
- suppression des doublons exacts par hash;
- reclassement des fichiers non prefixes selon des regles de nom et de contenu;
- renommage canonique si la source est reconnue;
- maintien en `A_CLASSER/` si la source reste ambiguë.
5. Verifier que `DAVID_CORPUS` est vide.
6. Verifier que `A_CLASSER/` est vide ou contient seulement les cas restant a arbitrer.
7. Completer ensuite les fiches source et les liens de connaissance.

---

## 5) Formats acceptes

Formats d'entree admis:
- `.txt`
- `.md`
- `.pdf`

Le classement se fait par sujet, pas par extension.

---

## 6) Exceptions maintenues

Exemples de reclassement sans prefixe:
- `2026-01-18__92resolutions__pdf.pdf` -> `CONSTITUTION_DROIT/`
- `2026-01-18__act-d-union-1840__pdf.pdf` -> `CONSTITUTION_DROIT/`
- `2026-01-18__l-evolution-du-canada-francais__pdf.pdf` -> `CULTURE_IDENTITE_QC/`
- `2026-01-18__la-spiritualite-des-indiens-d-amerique-la-voie-du-c-ur__pdf.pdf` -> `AUTOCHTONES/`
- `Frechette-originaux.pdf` -> `CULTURE_IDENTITE_QC/`
- `LABELLE-Discours.pdf` -> `POLITIQUE_QC_CANADA/`
- `Le Canadien 20 fevrier 1839.pdf` -> `HISTOIRE_QC_CANADA/`

---

## 7) Decision active

`DAVID_CORPUS` est un dossier tampon.
Le corpus canonique vit dans `05_PREUVES_SOURCES/CORPUS/`.

---

## 8) Passe semantique

Script associe:
- `reclasser_a_classer_semantic.ps1`

Role:
- prendre les fichiers tombes en `A_CLASSER/`;
- verifier les doublons exacts contre le corpus;
- reconnaitre les cas recurrents;
- appliquer un reclassement semantique et un renommage canonique.

Sous-corpus autochtones ajoutes pour cette passe:
- `AUTOCHTONES/ETHNOGRAPHIES_ARCHIVES/`
- `AUTOCHTONES/NATIONS_AMERIQUES_TERRITOIRES/`

Si necessaire, la passe automatique peut etre sautee avec:

```powershell
powershell -ExecutionPolicy Bypass -File .\partition_david_corpus.ps1 -SkipSemanticPass
```

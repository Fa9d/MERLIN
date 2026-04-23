# MERLIN - Audit du sous-corpus AUTOCHTONES

Date: 2026-04-18
Statut: draft
Objet: evaluation structurelle et qualitative du sous-corpus `AUTOCHTONES`

---

## 1) Perimetre

Dossier audite:
- `05_PREUVES_SOURCES/CORPUS/AUTOCHTONES`

Volume observe:
- 98 fichiers
- 96 fichiers `.txt`
- 2 fichiers `.pdf`

---

## 2) Constat global

Le sous-corpus `AUTOCHTONES` est deja riche et exploitable.
Il contient un noyau solide sur:
- savoirs autochtones et epistemologie;
- cosmologies et spiritualites;
- relations Terre / vivant / territoire;
- langues;
- traites, souverainete et wampum;
- histoire et violence coloniale.

En revanche, il melange encore:
- des sources fortes;
- des compilations anonymes;
- des textes comparatifs hors perimetre Premieres Nations / Quebec / Canada;
- des supports pedagogiques ou notes courtes;
- quelques doublons exacts.

---

## 3) Findings prioritaires

### F1 - Doublons exacts internes a supprimer ou declasser

Deux paires de fichiers ont un hash identique:

1. `AUTO__nabokov__native-american-testimony__1999.txt`
2. `AUTO__anon__native-american-testimony-alt__1999.txt`

et

1. `AUTO__anon__visions-heart-indigenous-peoples-canada__nd.txt`
2. `AUTO__anon__visions-heart-indigenous-peoples-canada-5th__nd.txt`

Impact:
- inflation artificielle du corpus;
- risque de citer deux fois le meme texte comme deux sources distinctes;
- bruit dans les futurs traitements d'extraction.

Recommendation:
- conserver une seule version canonique par texte;
- marquer l'autre comme alias ou doublon.

---

### F2 - Le corpus melange le noyau Premieres Nations avec des textes comparatifs hors perimetre

Exemples:
- `AUTO__anon__divining-ecology-sami-shamanism__nd.txt`
- `AUTO__batchelor__ainu-english-japanese-dictionary__nd.txt`
- `AUTO__bogoras__chukchee-mythology__nd.txt`
- `AUTO__anon__saami-shaman-drum__1991.txt`

Impact:
- risque de faire glisser des references comparatives vers des preuves directes sur les Premieres Nations;
- confusion entre analogie et documentation primaire ou secondaire sur le terrain canadien / quebecois.

Recommendation:
- creer un sous-ensemble `COMPARATIF_CIRCOMPOLAIRE_ET_AUTOCHTONE`;
- ne pas utiliser ces textes comme preuve directe sur les nations du Quebec sans mediation explicite.

---

### F3 - L'attribution des sources est encore trop faible

58 fichiers sur 98 sont prefixes `anon`.

Impact:
- provenance editoriale souvent floue;
- difficulte a distinguer ouvrage, compilation, site web, cours, brochure, notes ou OCR;
- niveau de legitimite theorique insuffisant si ces textes sont cites sans fiche source.

Recommendation:
- exiger une fiche source pour tout texte `anon` avant promotion doctrinale;
- prioriser les textes signes et edites pour le noyau canonique.

---

### F4 - Qualite documentaire heterogene

Le dossier contient des ouvrages solides, mais aussi des supports de type:
- slides ou exposés synthétiques:
  - `AUTO__anon__haudenosaunee-note__nd.txt`
- fiches tres courtes:
  - `AUTO__anon__traditional-knowledge-canada__nd.txt`
  - `AUTO__anon__seven-fires-prophecy__nd.txt`
  - `AUTO__anon__ojibwe-beginner-dictionary__nd.txt`
- communiques ou prises de position:
  - `AUTO__anon__algonquin-wolf-lake-eagle-village__nd.txt`

Impact:
- ces fichiers peuvent etre utiles comme pistes ou materiaux contextuels;
- ils ne doivent pas etre confondus avec des preuves A-level ou des textes fondateurs.

Recommendation:
- distinguer au minimum `SOURCE_FORTE`, `SOURCE_SECONDAIRE`, `PISTE`, `MATERIEL_PEDAGOGIQUE`, `POSITION_CONTEMPORAINE`.

---

### F5 - Deux fichiers restent en PDF non normalise

Fichiers:
- `2026-01-18__la-spiritualite-des-indiens-d-amerique-la-voie-du-c-ur__pdf.pdf`
- `AUTO__anon__naskapi-law-lake-st-john-mistassini__nd.pdf`

Impact:
- recherche plein texte et extraction plus fragiles;
- usage plus difficile dans un pipeline d'analyse automatisable.

Recommendation:
- produire une version texte ou OCR canonique associee;
- conserver le PDF comme source brute.

---

## 4) Noyau fort recommande

### A. Methodologie et epistemologie

- `AUTO__cajete__native-science-interdependence__1999.txt`
- `AUTO__kovach__indigenous-methodologies__nd.txt`
- `AUTO__simpson-leanne__as-we-have-always-done__2017.txt`
- `AUTO__sioui__autohistoire-amerindiens__1989.txt`

### B. Souverainete, traites, wampum, droit relationnel

- `AUTO__hill-rick__fort-niagara-treaty-1764__nd.txt`
- `AUTO__holding-hands-with-wampum__nd.txt`
- `AUTO__rcap__kaswentha-royal-commission__nd.txt`
- `AUTO__doxtator__tyendinaga-land-surrenders__nd.txt`
- `AUTO__lelievre__unsettling-mobility-mikmaw-sovereignty__nd.txt`

### C. Cosmologies, spiritualites, visions du monde

- `AUTO__hill-susan__clay-we-are-made-of-haudenosaunee__2017.txt`
- `AUTO__wall-arden__wisdomkeepers-spiritual-elders__1990.txt`
- `AUTO__black-elk-brown__sacred-pipe-seven-rites-oglala__nd.txt`
- `AUTO__moore__dream-shall-have-name__2013.txt`
- `AUTO__blueotter__earth-mother-crying__nd.txt`

### D. Langues et transmission

- `AUTO__valentine__nishnaabemwin-reference-grammar__2001.txt`
- `AUTO__scott__phonological-sketch-mushuau-innu__2000.txt`
- `AUTO__anon__innu-particles-thesis-oxford__2007.txt`
- `AUTO__anon__ojibwe-beginner-dictionary__nd.txt`
- `AUTO__anon__anishinaabe-language-workbook__nd.txt`

### E. Histoire coloniale et ruptures

- `AUTO__miller__shingwauks-vision-residential-schools__1996.txt`
- `AUTO__anon__residential-schools-report-english__nd.txt`
- `AUTO__anon__formes-assimilation-chronologie__nd.txt`
- `AUTO__anon__tensions-oka-kanesatake-xixe__2004.txt`

---

## 5) Proposition de sous-partition future

Le sous-corpus `AUTOCHTONES` gagnerait a etre reparti ainsi:

1. `EPISTEMOLOGIES_METHODES`
2. `COSMOLOGIES_SPIRITUALITES`
3. `TRAITES_SOUVERAINETE_WAMPUM`
4. `LANGUES_TRANSMISSION`
5. `HISTOIRE_COLONIALE_RUPTURES`
6. `NATIONS_QC_ET_TERRITOIRES`
7. `COMPARATIF_CIRCOMPOLAIRE_ET_AUTOCHTONE`
8. `PEDAGOGIE_NOTES_PISTES`

---

## 6) Verdict

Le sous-corpus `AUTOCHTONES` est suffisamment riche pour fonder un travail serieux dans MERLIN.
Mais il n'est pas encore suffisamment qualifie pour devenir un socle doctrinal sans tri complementaire.

La bonne prochaine etape n'est pas d'ajouter encore plus de textes.
La bonne prochaine etape est:
- dedoublonner;
- qualifier;
- sous-partitionner;
- produire les premieres fiches source;
- extraire les premiers concepts et assertions.

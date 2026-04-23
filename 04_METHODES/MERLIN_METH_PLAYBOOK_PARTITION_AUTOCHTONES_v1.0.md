# MERLIN - Playbook de partition AUTOCHTONES (v1)

Date: 2026-04-18
Statut: draft
Objet: nettoyer et sous-partitionner le sous-corpus `AUTOCHTONES`

---

## 1) Principe

Le dossier `05_PREUVES_SOURCES/CORPUS/AUTOCHTONES/` ne doit pas rester un bloc plat.
Il doit distinguer:
- les textes forts;
- les comparatifs;
- les notes ou supports pedagogiques;
- les textes de langues;
- les textes sur traites, souverainete et territoires;
- les textes sur cosmologies, spiritualites et epistemologies.

---

## 2) Sous-categories cibles

```text
05_PREUVES_SOURCES/CORPUS/AUTOCHTONES/
  EPISTEMOLOGIES_METHODES/
  COSMOLOGIES_SPIRITUALITES/
  TRAITES_SOUVERAINETE_WAMPUM/
  LANGUES_TRANSMISSION/
  HISTOIRE_COLONIALE_RUPTURES/
  NATIONS_QC_ET_TERRITOIRES/
  COMPARATIF_CIRCOMPOLAIRE_ET_AUTOCHTONE/
  PEDAGOGIE_NOTES_PISTES/
```

---

## 3) Regles de nettoyage

1. Les doublons exacts par hash sont supprimes.
2. La version la plus attribuee ou la plus precise devient canonique.
3. Les fichiers tres courts, scolaires ou de synthese restent utiles, mais vont dans `PEDAGOGIE_NOTES_PISTES/`.
4. Les textes hors perimetre direct Premieres Nations / Quebec / Canada, mais comparativement utiles, vont dans `COMPARATIF_CIRCOMPOLAIRE_ET_AUTOCHTONE/`.

---

## 4) Regles de partition

1. `EPISTEMOLOGIES_METHODES`
- savoirs autochtones;
- methodologies;
- theorie de la connaissance;
- science autochtone;
- cadres d'analyse.

2. `COSMOLOGIES_SPIRITUALITES`
- spiritualites;
- cosmologies;
- mythes;
- visions du monde;
- rites et prophecies.

3. `TRAITES_SOUVERAINETE_WAMPUM`
- wampum;
- traites;
- souverainete;
- droits et titres;
- relation nation-a-nation.

4. `LANGUES_TRANSMISSION`
- dictionnaires;
- grammaires;
- workbooks;
- linguistique;
- supports de transmission.

5. `HISTOIRE_COLONIALE_RUPTURES`
- pensionnats;
- assimilation;
- conflits;
- histoire coloniale;
- traumatismes et ruptures.

6. `NATIONS_QC_ET_TERRITOIRES`
- nations precises;
- territoires;
- toponymie;
- nations du Quebec;
- ancrage territorial contemporain.

7. `COMPARATIF_CIRCOMPOLAIRE_ET_AUTOCHTONE`
- Sami;
- Ainu;
- Chukchee;
- comparaisons autochtones hors perimetre central.

8. `PEDAGOGIE_NOTES_PISTES`
- notes de cours;
- presentations;
- syntheses courtes;
- communiques;
- pistes non encore qualifiees.

---

## 5) Decision active

Le sous-corpus `AUTOCHTONES` doit rester riche, mais devenir plus lisible, plus auditable et plus utilisable pour MERLIN.

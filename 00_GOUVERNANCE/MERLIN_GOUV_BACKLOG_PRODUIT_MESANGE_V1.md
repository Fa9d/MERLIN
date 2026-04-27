# MERLIN - Backlog produit MESANGE V1

Date: 2026-04-25
Statut: draft
Objet: traduire le cadrage strategique, data, workflow, ecrans et economie de MESANGE en chantiers produit concrets, ordonnes et priorises

---

## 1) But

Ce backlog sert a eviter un ecart durable entre:

- la vision MESANGE;
- le schema de donnees cible;
- le workflow canonique;
- les ecrans admin;
- le build reel.

Il ne redefinit pas la vision.

Il dit:

- `quoi construire`
- `dans quel ordre`
- `avec quelle priorite`
- `quelles dependances`
- `quels livrables minimum`

---

## 2) Decision d'execution

L'ordre retenu est:

1. `noyau donnees et workflow`
2. `ingestion et tri`
3. `claims et evidences`
4. `dossiers et chronologies`
5. `livrables et publication`
6. `pilotage economique`
7. `parametrage et doctrine`
8. `optimisations et extensions`

Regle:

`on ne construit pas une grande interface MESANGE avant d'avoir ferme les objets, les statuts et le flux minimal source -> claim -> dossier -> publication -> resolution`

---

## 3) Tableau des chantiers prioritaires

| Chantier | Risque si absent | Priorite | Decision |
|---|---|---|---|
| objets coeur MESANGE non implementes | tout le reste devient flou | critique | construire en premier |
| pas de file de tri | bruit ingouvernable | critique | ecran et logique minimaux obligatoires |
| pas de claim modelise | verification fictive | critique | isoler le claim comme unite de travail |
| pas de dossier structurant | perte de memoire | critique | faire du dossier l'objet central |
| pas de chronologie | impossibilite de reprendre un sujet | haute | timeline minimale V1 |
| pas de workflow publication | confusion entre analyse et diffusion | haute | valider la chaine de sortie |
| pas de trace economique | impossibilite d'arbitrer | haute | lier couts, budgets, revenus |
| taxonomies non gouvernees | derive analytique rapide | moyenne | cadrer concepts et options |
| pas de resolution ni reouverture | accumulation sans fin | moyenne | cloture documentaire obligatoire |

---

## 4) Chantiers coeur V1

## M-01 - Poser les objets coeur MESANGE

Probleme:

Le produit ne peut pas avancer proprement sans objets stables.

Action:

- creer les objets minimum:
  - `source`
  - `source_item`
  - `document`
  - `concept`
  - `claim`
  - `evidence`
  - `topic`
  - `dossier`
  - `dossier_event`
  - `actor`
  - `report`
  - `budget`
  - `cost_entry`
  - `revenue_entry`

But:

- fermer le vocabulaire produit;
- eviter les raccourcis impropres.

Priorite:

`critique`

Dependances:

- aucune

Sortie minimum:

- spec technique des objets
- statuts associes
- relations cles

---

## M-02 - Poser les statuts et transitions

Probleme:

Sans statuts fermes, l'interface et l'automatisation deriveront vite.

Action:

- fixer et implementer:
  - `source_status`
  - `review_status`
  - `claim_verification_status`
  - `dossier_status`
  - `record_status`

But:

- structurer les ecrans;
- rendre les transitions explicites.

Priorite:

`critique`

Dependances:

- `M-01`

Sortie minimum:

- tableau des transitions permises
- validations par statut

---

## M-03 - Construire la file de tri

Probleme:

Sans file de tri, le bruit entre sans filtre.

Action:

- construire:
  - liste des items ingeres
  - filtres
  - apercu rapide
  - actions:
    - ignorer
    - marquer a revoir
    - creer claim
    - rattacher a dossier
    - creer dossier

But:

- installer le premier verrou anti-chaos.

Priorite:

`critique`

Dependances:

- `M-01`
- `M-02`

Sortie minimum:

- ecran `ADM-103`
- logique de statut item

---

## M-04 - Modeliser et gerer les claims

Probleme:

Sans claim, MESANGE risque de parler de "sujets" de facon trop vague.

Action:

- permettre:
  - creation manuelle ou assistee de claim
  - edition
  - changement de statut
  - rattachement aux sources et acteurs
  - historique des revisions

But:

- faire du claim l'unite de verification.

Priorite:

`critique`

Dependances:

- `M-01`
- `M-02`
- `M-03`

Sortie minimum:

- `ADM-201`
- `ADM-202`

---

## M-05 - Ajouter les evidences

Probleme:

Un claim sans preuve ou note methodologique reste fragile.

Action:

- permettre:
  - ajout d'evidence
  - typage
  - qualification de force
  - lien avec source/document
  - position `soutient / contredit / nuance`

But:

- rendre la verification defendable.

Priorite:

`critique`

Dependances:

- `M-04`

Sortie minimum:

- `ADM-203`
- historique simple des evidences

---

## M-06 - Construire l'objet dossier

Probleme:

Sans dossier, MESANGE redevient un systeme de notes dispersees.

Action:

- permettre:
  - creation dossier
  - resume courant
  - statut
  - priorite
  - responsable
  - rattachements claims / acteurs / items

But:

- faire du dossier la memoire centrale.

Priorite:

`critique`

Dependances:

- `M-01`
- `M-02`
- `M-04`

Sortie minimum:

- `ADM-301`
- `ADM-302`

---

## M-07 - Ajouter la chronologie

Probleme:

Un dossier sans timeline perd sa force de reprise.

Action:

- implementer:
  - `dossier_event`
  - timeline
  - types d'evenements
  - ajout manuel
  - génération depuis actions systeme

But:

- permettre une lecture du debut a la fin.

Priorite:

`haute`

Dependances:

- `M-06`

Sortie minimum:

- `ADM-303`

---

## M-08 - Construire les rapports et la publication

Probleme:

Sans sortie gouvernee, le travail reste interne et difficile a monnayer.

Action:

- permettre:
  - creation de `report`
  - brouillon
  - validation
  - publication
  - archivage

But:

- transformer un dossier en livrable diffusable.

Priorite:

`haute`

Dependances:

- `M-06`
- `M-07`

Sortie minimum:

- `ADM-401`
- `ADM-402`

---

## M-09 - Ajouter la resolution et la reouverture

Probleme:

Sans cloture documentaire, MESANGE accumule sans jamais finir.

Action:

- permettre:
  - passage `resolu`
  - note de resolution
  - passage `archive`
  - reouverture motivee

But:

- distinguer suivi actif, surveillance et cloture.

Priorite:

`haute`

Dependances:

- `M-06`
- `M-07`

Sortie minimum:

- champs resolution
- `ADM-304`

---

## M-10 - Integrer budgets, couts et revenus

Probleme:

Sans couche economique, l'arbitrage produit reste aveugle.

Action:

- permettre:
  - creation de budgets
  - journal de couts
  - journal de revenus
  - rattachement a sujet / dossier / rapport

But:

- voir ce qui se soutient;
- voir ce qui derive.

Priorite:

`haute`

Dependances:

- `M-06`
- `M-08`

Sortie minimum:

- `ADM-501`
- `ADM-502`
- `ADM-503`

---

## M-11 - Ajouter les vues de marge et alertes

Probleme:

Les journaux seuls ne suffisent pas a piloter.

Action:

- calculer:
  - cout par dossier
  - cout par rapport
  - marge par dossier
  - budget consomme
- alerter:
  - dossier hors budget
  - sujet couteux sans sortie
  - source peu utile mais couteuse

Priorite:

`moyenne`

Dependances:

- `M-10`

Sortie minimum:

- `ADM-504`

---

## M-12 - Administrer concepts et taxonomies

Probleme:

Sans taxonomies gouvernees, les analyses divergent vite.

Action:

- permettre:
  - creer / modifier / desactiver `concept`
  - organiser:
    - enjeux
    - signaux
    - techniques discursives
    - sophismes
    - principes MESANGE
    - categories de cout

Priorite:

`moyenne`

Dependances:

- `M-01`

Sortie minimum:

- `ADM-601`

---

## M-13 - Ajouter les cadres d'analyse et options

Probleme:

Les cadres doivent etre configurables sans recoder tout le produit.

Action:

- permettre:
  - gestion des seuils
  - options de tri
  - regles d'ouverture auto
  - angles d'analyse
  - versionnement des prompts ou cadres

Priorite:

`moyenne`

Dependances:

- `M-12`

Sortie minimum:

- `ADM-602`

---

## M-14 - Rendre explicites les positions et principes MESANGE

Probleme:

Le point de vue doit etre declare et non cache.

Action:

- gerer:
  - principes
  - positions
  - lignes rouges
  - criteres de resolution

Priorite:

`moyenne`

Dependances:

- `M-12`

Sortie minimum:

- `ADM-603`

---

## M-15 - Ajouter cartographie acteurs et positions

Probleme:

La lecture politique et citoyenne devient pauvre sans couche acteurs.

Action:

- implementer:
  - `actor`
  - `position`
  - vue cartographique simple

Priorite:

`moyenne`

Dependances:

- `M-04`
- `M-06`

Sortie minimum:

- `ADM-204`

---

## 5) Lots de build recommandes

## Lot A - Noyau minimal utilisable

Contenu:

- `M-01`
- `M-02`
- `M-03`
- `M-04`
- `M-05`
- `M-06`

Resultat:

- MESANGE peut deja ingérer, trier, isoler des claims et ouvrir des dossiers.

## Lot B - Dossiers exploitables

Contenu:

- `M-07`
- `M-08`
- `M-09`

Resultat:

- MESANGE peut suivre un sujet, produire un livrable et cloturer proprement.

## Lot C - Pilotage economique

Contenu:

- `M-10`
- `M-11`

Resultat:

- MESANGE peut mesurer ses couts et arbitrer.

## Lot D - Gouvernance analytique

Contenu:

- `M-12`
- `M-13`
- `M-14`
- `M-15`

Resultat:

- MESANGE devient vraiment adaptable et Quebec-first de facon governable.

---

## 6) Priorite V1 vs V1.1

### Obligatoire V1

- `M-01`
- `M-02`
- `M-03`
- `M-04`
- `M-05`
- `M-06`
- `M-07`
- `M-08`
- `M-10`

### Souhaitable V1.1

- `M-09`
- `M-11`
- `M-12`
- `M-13`
- `M-14`
- `M-15`

---

## 7) Regles d'arbitrage produit

### Regle 1

Un ecran qui n'aide ni le tri, ni la verification, ni le dossier, ni l'economie ne doit pas etre prioritaire en V1.

### Regle 2

Toute automatisation doit d'abord servir la structure, pas l'effet "waouh".

### Regle 3

Un claim non gouverne produit plus de bruit que de valeur.

### Regle 4

Une publication sans dossier ou sans note methodologique fragilise l'ensemble.

### Regle 5

Une demande client recurrente non mesurable economiquement doit etre recadree.

---

## 8) Definition de done minimale par chantier

### Pour `M-03`

- l'item peut etre ignore, rattache, transformer en claim ou transformer en dossier

### Pour `M-04`

- un claim a un texte, une source, un acteur optionnel, un statut et un historique

### Pour `M-06`

- un dossier a un resume courant, un statut, une priorite et des liens a des claims

### Pour `M-08`

- un rapport peut etre brouillon, soumis, valide, publie

### Pour `M-10`

- tout cout et revenu peut etre relie a un sujet ou dossier

---

## 9) Recommendation nette

Si MESANGE doit passer du cadre a l'execution, il faut construire d'abord:

1. `Lot A`
2. `Lot B`
3. `Lot C`

et ne lancer `Lot D` qu'une fois le noyau utilisable.

Sinon, le projet risque de surinvestir trop tot dans la sophistication avant d'avoir prouve sa capacite a traiter, suivre et monetiser des sujets.

---

## 10) Prochaine etape recommandee

Apres ce backlog, les deux livrables les plus utiles sont:

1. une grille commerciale courte pour pitcher `Signal clair`, `Dossier suivi` et `Veille active`
2. une decomposition technique V1 en epics / tickets


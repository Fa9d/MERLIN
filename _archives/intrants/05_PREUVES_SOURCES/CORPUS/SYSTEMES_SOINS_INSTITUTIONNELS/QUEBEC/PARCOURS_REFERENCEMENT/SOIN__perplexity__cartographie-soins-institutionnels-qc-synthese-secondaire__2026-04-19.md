# Cartographie des soins institutionnels au Quebec

Date: 2026-04-19
Statut: synthese_secondaire
Origine: formalisation interne d'une reponse Perplexity colligee dans la session MERLIN
Usage: base de travail pour MERLIN, non suffisante seule comme source primaire

## Nature du document

Ce document est une synthese secondaire.

Il ne doit pas etre traite comme une source primaire normative.
Il sert a:
- structurer la base de connaissance MERLIN;
- preparer les fiches de services;
- faire emerger les champs a verifier dans les sources officielles;
- orienter les futures regles de triage prudent.

Les points suivants doivent rester distincts:
- `officiel`
- `source secondaire`
- `synthese`
- `varie selon la region`
- `a valider localement`

## Perimetre

Services et portes d'entree couverts dans cette synthese:
- `811 Info-Sante / Info-Social`
- `GAP`
- `medecin de famille / GMF`
- `CLSC`
- `urgence hospitaliere`
- `centre de crise`
- `services en dependance`

## Sources primaires citees dans la synthese

- Quebec.ca - Services de sante et services sociaux de premiere ligne
  https://www.quebec.ca/sante/systeme-et-services-de-sante/organisation-des-services/services-de-sante-et-services-sociaux-de-premiere-ligne
- MSSS - Directive 811
  https://g26.pub.msss.rtss.qc.ca/Formulaires/Circulaire/ConsCirculaire.aspx?id=3641
- Quebec.ca - Guichet d'acces a la premiere ligne
  https://www.quebec.ca/sante/trouver-une-ressource/guichet-acces-premiere-ligne
- Quebec.ca - GMF, GMF-U et super-clinique
  https://www.quebec.ca/sante/systeme-et-services-de-sante/organisation-des-services/gmf-gmf-u-et-super-clinique
- MSSS - Portrait et perspectives des services en CLSC
  https://publications.msss.gouv.qc.ca/msss/fichiers/2025/25-924-24W.pdf
- MSSS - Guide urgences sante mentale
  https://msss.gouv.qc.ca/professionnels/soins-et-services/guide-urgences-sante-mentale/
- MSSS - Repertoire des ressources en dependances
  https://msss.gouv.qc.ca/repertoires/dependances/
- Quebec.ca - Ressources d'aide et de soutien en sante mentale
  https://www.quebec.ca/sante/sante-mentale/trouver-aide-et-soutien-en-sante-mentale/trouver-ressource-aide-et-soutien-en-sante-mentale

## Lecture operationnelle du systeme

### Logique utile pour MERLIN

Le systeme quebecois est officiellement structure par niveaux.
Pour MERLIN, il est plus utile de le lire comme un systeme de:
- `portes d'entree`
- `filtres`
- `delais`
- `seuils de gravite`
- `reorientations`

### Portes d'entree principales

- `811 Info-Sante / Info-Social`
  Porte d'entree de triage et d'orientation rapide quand la gravite est incertaine ou qu'aucune ressource habituelle n'est disponible.
- `GAP`
  Porte d'entree pour probleme ponctuel non urgent chez les personnes sans medecin de famille ou avec acces difficile a la premiere ligne.
- `medecin de famille / GMF`
  Porte d'entree privilegiee pour les problemes non urgents, le suivi, la coordination et certaines orientations specialisees.
- `CLSC`
  Porte d'entree de proximite pour besoins psychosociaux, sante mentale non urgente, prevention, soutien a domicile et services sociaux courants.
- `urgence hospitaliere`
  Porte d'entree pour danger vital, crise aigue, risque suicidaire imminent, symptomes physiques graves ou desorganisation majeure.
- `centre de crise`
  Porte d'entree intermediaire pour crise psychosociale ou psychiatrique sans danger vital manifeste, selon disponibilite territoriale.
- `services en dependance`
  Porte d'entree specialisee pour trouble de l'usage, en aval d'un triage du risque medical.

## Trajectoires de circulation

### En theorie

Trajectoire graduee de reference:

`auto-soins -> 811 / premiere ligne -> services specialises -> urgence / hospitalier si aggravation`

### En pratique

La synthese secondaire releve:
- usage frequent de l'urgence comme substitut a la premiere ligne;
- circulation non lineaire entre `811`, `GMF`, `CLSC`, urgence et communautaire;
- forte variation regionale dans l'acces et l'assemblage des services;
- perte de temps importante chez les personnes sans medecin de famille ou avec besoin mixte `sante + social`.

## Fiches synthetiques utiles pour MERLIN

### 811 Info-Sante / Info-Social

- Role:
  triage et orientation 24/7
- Quand orienter:
  gravite incertaine, besoin de conseil rapide, absence de ressource habituelle
- Quand ne pas orienter:
  danger vital immediat, besoin de suivi structure
- Acces:
  direct, gratuit, provincial
- Limites:
  pas de diagnostic formel, pas de suivi, attente variable
- Notes MERLIN:
  porte d'entree par defaut en cas de doute, mais jamais a la place du `911` si danger manifeste

### GAP

- Role:
  acces clinique ou psychosocial non urgent pour personnes sans medecin de famille ou avec acces difficile a la premiere ligne
- Quand orienter:
  besoin non urgent necessitant evaluation, absence de medecin ou inaccessibilite de la ressource habituelle
- Quand ne pas orienter:
  urgence, crise aigue, besoin de suivi long
- Acces:
  numerique ou telephone, gratuit, variation territoriale
- Limites:
  service ponctuel, non 24/7, delais variables
- Notes MERLIN:
  utile surtout si la personne n'a pas de premiere ligne stable

### Medecin de famille / GMF

- Role:
  suivi medical courant, prevention, coordination, orientation
- Quand orienter:
  symptomes non urgents, maladies chroniques, besoin de prescription, suivi
- Quand ne pas orienter:
  urgence vitale, crise psychiatrique aigue
- Acces:
  si inscrit ou via mecanismes d'inscription / d'acces locaux
- Limites:
  penurie, acces rapide faible, heterogeneite de l'offre psycho-sociale
- Notes MERLIN:
  ressource centrale si elle existe reellement; sinon ne pas orienter fictivement

### CLSC

- Role:
  ancrage local sante + social
- Quand orienter:
  besoins psychosociaux, vulnerabilite sociale, sante mentale non urgente, soutien a domicile
- Quand ne pas orienter:
  urgence vitale, besoin exclusivement medical urgent
- Acces:
  generalement direct, gratuit, territorialise
- Limites:
  offre variable, delais, forte heterogeneite regionale
- Notes MERLIN:
  porte d'entree cle des besoins sociaux et mixtes

### Urgence hospitaliere

- Role:
  gestion des situations urgentes et critiques
- Quand orienter:
  danger vital, risque suicidaire imminent, symptomes graves, trauma, psychose aigue
- Quand ne pas orienter:
  probleme mineur, detresse stable, suivi chronique non urgent
- Acces:
  direct, gratuit, 24/7
- Limites:
  surcharge, episode-centre, continuite limitee
- Notes MERLIN:
  a reserver aux criteres de gravite

### Centre de crise

- Role:
  alternative ou complement a l'urgence pour crise psychosociale/psychiatrique sans danger vital manifeste
- Quand orienter:
  adulte en crise severe, sans signe medical majeur, besoin de soutien intensif court terme
- Quand ne pas orienter:
  danger vital, intoxication grave, violence extreme
- Acces:
  varie selon la region, souvent direct ou via `811` / `CLSC`
- Limites:
  couverture territoriale inegale, capacite limitee
- Notes MERLIN:
  ressource cle a distinguer de l'urgence

### Services en dependance

- Role:
  traitement et readaptation des troubles lies aux substances et au jeu
- Quand orienter:
  consommation problematique avec retentissement et besoin d'aide
- Quand ne pas orienter:
  intoxication ou sevrage grave necessitant d'abord une urgence medicale
- Acces:
  varie selon ressource; auto-reference possible dans certains cas
- Limites:
  capacite variable, coordination parfois difficile, forte variation territoriale
- Notes MERLIN:
  toujours trier d'abord le risque medical

## Points de friction

### Frictions majeures relevees

- manque de medecins de famille
- delais et difficulte d'acces a la premiere ligne
- confusion entre `GAP` et `GAMF`
- variations regionales des services `CLSC`, centres de crise et dependances
- articulation insuffisamment lisible entre `soin`, `social` et `crise`
- recours au prive quand le public est sature

### Causes frequentes d'errance

- mauvais niveau de gravite attribue a la situation
- mauvaise porte d'entree selectionnee
- confusion entre besoin medical, besoin social et besoin psychologique
- retard d'orientation en contexte de crise
- absence de service habituel clairement accessible

## Variables minimales utiles pour MERLIN

Variables relevees comme prioritaires:
- symptomes
- duree et evolution
- gravite percue
- risque aigu
- contexte social
- antecedents medicaux / psychiatriques
- ressources deja mobilisees
- autonomie reelle
- disponibilite
- territoire
- cout supportable
- preference de parcours

## Zones a verifier avant usage normatif

- delais reels par service et par region
- accessibilite precise des centres de crise
- disponibilite des services en dependance selon territoire
- part reelle des services psychosociaux en GMF
- couverture linguistique et culturelle locale

## Regle d'usage MERLIN

Cette synthese peut servir a:
- structurer les fiches de services;
- definir des variables d'orientation;
- poser des hypotheses de triage prudent.

Elle ne suffit pas seule pour:
- fixer des regles finales;
- presenter des delais comme verites stables;
- publier une cartographie definitive sans validation locale.

# MERLIN - Modele economique et gouvernance de l'orientation (v1)

Date: 2026-04-19
Statut: draft
Objet: definir un modele d'orientation traçable, non commissionne, avec redistribution integrale des avantages clients

---

## 1) Principe directeur

MERLIN n'est pas remunere pour orienter un client vers un service de soin, un professionnel ou un organisme plutot qu'un autre.

La mise en relation doit rester gouvernee par:
- l'interet du client;
- la pertinence clinique ou fonctionnelle de l'orientation;
- la disponibilite des ressources;
- la securite;
- la transparence.

Si MERLIN obtient des avantages par volume, par convention ou par partenariat, ces avantages ne constituent pas un benefice pour MERLIN.

Ils doivent etre:
- redistribues integralement aux clients concernes;
- ou affectes a un usage collectif client explicite, public et verifiable.

MERLIN ne peut retenir qu'un cout operationnel explicite, justifiable, trace et plafonne si la gestion de cette redistribution engendre un travail reel.

---

## 2) Regle economique centrale

Doctrine active:

`Aucun revenu de MERLIN ne doit provenir d'une commission cachee, d'un rabais conserve, d'un retrocommissionnement indirect ou d'un avantage d'orientation non restitue aux clients.`

Formule simple:

`avantage brut obtenu - cout operationnel explicite autorise = avantage net restitue au client ou au collectif client`

Consequence:
- MERLIN ne monetise pas l'acte d'orientation;
- MERLIN ne capte pas de marge sur les remises negociees;
- MERLIN ne tire pas de profit des accords de soin;
- MERLIN peut documenter un cout technique ou administratif s'il existe reellement.

---

## 3) Separation stricte des flux

### Flux A - Orientation de soin

Nature:
- triage;
- qualification du besoin;
- prise de rendez-vous;
- transmission de resume;
- orientation vers organisme ou professionnel.

Regle:
- pas de commission;
- pas de marge;
- pas d'avantage cache.

### Flux B - Avantages negocies

Nature:
- reduction tarifaire;
- frais annules;
- priorite d'acces;
- forfait collectif;
- conditions preferentielles.

Regle:
- avantage trace;
- origine tracee;
- destinataire trace;
- redistribution integrale verifiable.

### Flux C - Revenus propres MERLIN

Nature admissible:
- abonnement logiciel;
- licence;
- service d'infrastructure;
- produit vendu;
- service premium explicite;
- accompagnement non lie a l'orientation de soin.

Regle:
- separation comptable;
- separation contractuelle;
- separation narrative.

MERLIN doit pouvoir demontrer qu'un revenu propre n'est pas une remuneration deguisee de l'orientation.

---

## 4) Registre de traçabilite

Le systeme de traçabilite ne porte pas d'abord sur la sante du client.
Il porte sur les transactions de gouvernance et de redistribution.

Chaque operation doit laisser un enregistrement contenant au minimum:
- `transaction_id`
- `date`
- `partner_id`
- `type_avantage`
- `montant_brut` ou `valeur_brute`
- `base_de_calcul`
- `client_scope`
- `mode_redistribution`
- `cout_operationnel_applique`
- `montant_net_redistribue`
- `preuve_associee`
- `statut`

Statuts recommandes:
- `promised`
- `validated`
- `distributed`
- `contested`
- `closed`

Ce registre doit permettre de prouver:
- qu'un avantage a bien ete obtenu;
- qu'il n'a pas ete absorbe par MERLIN;
- qu'il a ete redistribue selon une regle publique;
- qu'aucune orientation n'a ete dictee par un interet cache.

---

## 5) Ce qui peut etre trace publiquement

Peut etre public ou auditable:
- l'existence d'un accord partenaire;
- la regle de calcul d'un avantage;
- le volume global traite;
- le montant global redistribue;
- le cout operationnel global retenu;
- les regles de redistribution;
- les indicateurs d'impact agrege.

Doit rester hors registre public:
- identite des clients;
- motifs sensibles d'orientation;
- donnees de sante;
- contenus cliniques;
- informations nominatives des parcours.

Conclusion:
- registre public ou auditable pour la gouvernance;
- donnees client sensibles hors registre public;
- preuve par hash ou journal d'audit si necessaire.

---

## 6) Redistribution sans benefice pour MERLIN

### Regle forte

Tout avantage negocie du fait du volume ou de l'intermediation de MERLIN appartient economiquement au client ou au collectif client, pas a MERLIN.

### Formes admissibles de redistribution

1. Redistribution individuelle
- remise appliquee directement au client concerne;
- frais diminues pour son rendez-vous ou son service.

2. Redistribution mutualisee client
- fonds commun dedie aux clients;
- credits de parcours;
- soutien a des cas a faible capacite de paiement;
- financement de services utiles au parcours client.

3. Redistribution en nature
- temps d'accompagnement offert;
- frais de dossier absorbes;
- outils utiles au parcours;
- acces facilite.

### Formes non admissibles

- marge conservee sans declaration;
- avantage absorbe dans la tresorerie generale;
- bonus commercial non trace;
- remuneration de l'orientation deguisee en "partenariat";
- captation de rabais sans preuve de redistribution.

---

## 7) Cout operationnel admissible

MERLIN peut definir un `cost of operation` uniquement si ce cout correspond a une charge reelle et necessaire pour traiter l'avantage et le redistribuer.

Exemples admissibles:
- frais de transaction;
- cout de traitement administratif;
- cout technique de reconciliation;
- cout d'audit;
- cout de support lie a la redistribution.

Conditions obligatoires:
- cout explicite;
- methode de calcul publique;
- plafond defini;
- documentation conservable;
- auditabilite;
- absence de marge cachee.

### Regle de prudence

Si le cout operationnel n'est pas objectivable, MERLIN ne le preleve pas.

### Formule de reference

`cout operationnel admissible = cout reel direct + cout technique verifiable + cout d'audit attribuable`

Exclus:
- marge commerciale;
- profit implicite;
- commission de convenance;
- cout forfaitaire arbitraire non justifie.

---

## 8) Doctrine d'independance

Une orientation ne peut jamais etre justifiee par:
- un avantage partenaire;
- une reduction obtenue;
- une facilite commerciale;
- une pression de volume.

Une orientation doit toujours pouvoir etre justifiee par au moins un des elements suivants:
- pertinence du besoin;
- qualite de reponse du service;
- competence du partenaire;
- proximite;
- disponibilite;
- cout pertinent pour le client;
- adequation temporelle;
- niveau de securite.

MERLIN doit pouvoir prouver qu'un autre service aurait ete recommande si ses criteres etaient meilleurs, meme sans avantage economique.

---

## 9) Proposition de valeur double face

### Cote client

MERLIN promet:
- une meilleure comprehension de la situation;
- une orientation plus lisible;
- moins d'errance;
- une possible baisse de cout ou de friction;
- une gouvernance sans conflit cache;
- une restitution des avantages negocies.

### Cote professionnels et organismes

MERLIN promet:
- une meilleure qualification en amont;
- moins de temps perdu;
- des rendez-vous plus pertinents;
- une reduction de friction administrative;
- un meilleur alignement besoin-service;
- une traçabilite propre du partenariat.

---

## 10) Mesure d'impact

MERLIN doit mesurer son impact sur deux axes:

### Impact client

- delai jusqu'au bon service;
- taux de rendez-vous honores;
- reduction d'errance;
- baisse de cout pour le client;
- satisfaction;
- comprehension accrue;
- autonomie decisionnelle accrue.

### Impact partenaire

- temps de qualification gagne;
- taux de rendez-vous pertinents;
- taux de reorientation;
- qualite du dossier de preparation;
- satisfaction partenaire;
- charge administrative reduite.

### Impact de gouvernance

- montant brut des avantages negocies;
- montant net redistribue;
- pourcentage redistribue;
- cout operationnel retenu;
- nombre d'operations auditees;
- nombre de contestations;
- absence de benefice capte sur orientation.

Indicateur cle recommande:

`taux de redistribution effective = montant net redistribue / montant brut obtenu`

La cible doctrinale doit tendre vers `100%` hors cout operationnel objectivable.

---

## 11) Architecture minimale de confiance

MERLIN doit tenir au minimum:
- un registre des partenaires;
- un registre des conventions;
- un registre des avantages obtenus;
- un registre des redistributions;
- un journal d'audit;
- une separation comptable des flux.

Modele recommande:
- donnees sensibles hors chaine;
- registre d'audit inviolable pour les transactions de gouvernance;
- possibilite d'attester les enregistrements par hash, signature ou registre permissionne.

La valeur n'est pas la blockchain en soi.
La valeur est la preuve de non-captation et la gouvernance verifiable.

---

## 12) Clauses de credibilite

Pour que le modele soit recevable, MERLIN doit pouvoir publier:
- sa doctrine de non-commissionnement;
- ses regles de redistribution;
- sa methode de calcul des couts operationnels;
- ses indicateurs d'impact;
- ses procedures de contestation;
- ses procedures d'audit.

MERLIN doit aussi pouvoir dire clairement:

`Nous pouvons gagner de l'argent sur des produits ou services propres a MERLIN, mais pas sur le fait d'orienter une personne vers un soin, un organisme ou un professionnel.`

Et:

`Si un avantage est obtenu par notre effet de volume, il revient au client ou au collectif client, sous reserve d'un cout operationnel explicite, plafonne et verifiable lorsqu'il existe reellement.`

---

## 13) Interdits

Sont interdits:
- toute commission occulte;
- toute retrocommission non declaree;
- toute captation silencieuse de rabais;
- toute confusion entre orientation et vente;
- tout pilotage de l'orientation par interet economique cache;
- toute impossibilite d'auditer la redistribution.

---

## 14) Decision active

MERLIN adopte un modele dans lequel:
- l'orientation de soin est non commissionnee;
- les avantages negocies sont redistribues aux clients;
- MERLIN ne capte aucun benefice sur ces avantages;
- seul un cout operationnel objectivable peut etre retenu;
- la traçabilite et l'auditabilite sont des exigences de gouvernance;
- la confiance du client et l'efficience du reseau sont des actifs principaux du modele.

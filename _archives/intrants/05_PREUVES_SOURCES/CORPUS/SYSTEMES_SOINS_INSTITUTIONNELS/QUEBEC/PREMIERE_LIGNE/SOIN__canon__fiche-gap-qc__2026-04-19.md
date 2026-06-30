# Fiche canonique - Guichet d'acces a la premiere ligne (Quebec)

Date: 2026-04-19
Statut: draft
Type: fiche_service
Champ: systemes_soins_institutionnels
Territoire: Quebec

## 1) Identification

- Nom: `GAP`
- Categorie: `guichet d'acces et orientation`
- Niveau: `premiere ligne`
- Statut: `public`

## 2) Fonction

- Definition simple:
  mecanisme d'acces a une evaluation clinique ou psychosociale non urgente pour les personnes sans medecin de famille ou ayant un acces difficile a leur ressource habituelle.
- Role reel:
  compenser partiellement l'absence de premiere ligne stable et reduire le recours inapproprie a l'urgence.
- Besoins principalement pris en charge:
  probleme ponctuel non urgent necessitant rendez-vous, evaluation ou orientation.
- Ne prend pas bien en charge:
  suivi a long terme, inscription permanente a un medecin, urgence, crise aigue.

## 3) Orientation

- Quand MERLIN devrait envisager ce service:
  quand la personne n'a pas de medecin de famille ou ne peut pas joindre sa ressource, et que le besoin est reel mais non urgent.
- Quand MERLIN ne devrait pas le proposer en premiere intention:
  danger vital, crise psychiatrique aigue, besoin de suivi specialise deja etabli.
- Signes / contextes qui pointent vers ce service:
  `je n'ai pas de medecin`, `je suis en attente`, `j'ai besoin d'un rendez-vous`, `ce n'est pas urgent mais j'ai besoin d'etre vu`.
- Niveau d'urgence:
  `non urgent`
- Signaux d'alerte qui font monter le niveau:
  aggravation rapide, ideation suicidaire avec plan, symptomes neurologiques ou cardiaques aigus.

## 4) Acces

- Acces direct: `oui`
- Reference requise:
  `non` pour l'usager; peut exister des references professionnelles dans certains cas.
- Modalites d'entree:
  plateforme numerique et acces telephone associe; details operationnels a valider localement.
- Territoire couvert:
  Quebec, avec organisation et horaires par territoire.
- Conditions d'admissibilite:
  sans medecin / IPS de premiere ligne ou avec acces difficile, selon regles en vigueur.
- Barrieres d'acces:
  confusion `GAP` vs `GAMF`, fracture numerique, horaires limites, disponibilite locale.
- Delais:
  rappels et rendez-vous variables selon territoires; information non standardisee.
- Cout usager: `gratuit`

## 5) Limites et risques

- Limites structurelles:
  service ponctuel, non 24/7, capacite dependante des ressources locales.
- Erreurs frequentes d'aiguillage:
  y envoyer une crise, un risque vital ou une demande de suivi long.
- Risques si orientation trop tardive:
  aggravation d'un probleme non urgent, recours secondaire a l'urgence.
- Risques si mauvaise porte d'entree:
  perte de temps, attente inappropriee, frustration, abandon.
- Services plus appropries si ce n'est pas le bon:
  `urgence`, `811`, `centre de crise`, `CLSC`, `GMF`, selon nature du besoin.

## 6) Suite de parcours

- Apres premier contact:
  triage, rappel, proposition de rendez-vous ou orientation vers autre ressource.
- Reorientation possible:
  medecin, IPS, infirmiere, travailleur social, clinique, urgence.
- Role dans la continuite:
  acces ponctuel et non dispositif de suivi long.

## 7) Utilite pour MERLIN

- Place dans le moteur:
  solution intermediaire quand une premiere ligne est necessaire mais absente.
- Confusions a eviter:
  `GAP` n'est pas `GAMF`, ni une urgence, ni un service de psychotherapie.
- Risque si MERLIN l'utilise mal:
  retarder une prise en charge urgente ou generer de fausses attentes de suivi.
- Accompagnements complementaires prudents compatibles:
  `811`, `CLSC`, ressources communautaires, selon delai et contexte.

## 8) Sources et validation

- Source principale:
  Quebec.ca - Guichet d'acces a la premiere ligne
  https://www.quebec.ca/sante/trouver-une-ressource/guichet-acces-premiere-ligne
- Niveau de fiabilite:
  `eleve` sur la fonction generale
- A valider localement:
  horaires, numeros, delais, articulation avec les ressources territoriales.

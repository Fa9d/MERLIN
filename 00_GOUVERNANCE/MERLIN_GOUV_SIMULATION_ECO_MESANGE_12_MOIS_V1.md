# MERLIN - Simulation eco MESANGE 12 mois V1

Date: 2026-04-25
Statut: draft
Objet: simuler trois scenarios economiques de lancement pour MESANGE sur 12 mois afin d'estimer les revenus, les couts et la marge de contribution selon un mix d'offres realiste

---

## 1) Finalite

Cette simulation sert a:

- tester si les offres MESANGE peuvent produire une traction economique reelle;
- verifier si le point d'entree recommande est soutenable;
- estimer l'ordre de grandeur des revenus possibles sur 12 mois;
- identifier les conditions minimales de viabilite.

Ce document n'est pas:

- un budget final;
- une prevision comptable officielle;
- une promesse commerciale;
- une preuve de rentabilite garantie.

---

## 2) Point de depart retenu

La simulation part de la grille d'offres definie dans:

- `Signal clair`
- `Dossier suivi`
- `Veille active`
- `Observatoire Quebec`
- `Atelier methode`

Hypothese directrice:

`MESANGE se lance d'abord comme outil interne + services d'analyse + veille recurrente + observatoire, et non comme pur abonnement grand public ou SaaS complet.`

---

## 3) Hypotheses communes

### Monnaie

- devise de travail: `CAD`

### Horizon

- `12 mois`

### Couts fixes mensuels retenus

Hypothese lean de depart:

| Bloc | Cout mensuel CAD |
|---|---:|
| hebergement / stockage / domaines | 120 |
| outils IA / scraping / recherche | 350 |
| outils collaboratifs / admin | 130 |
| juridique / compta / divers provisionnes | 250 |
| diffusion / publication / marge de manoeuvre | 150 |
| Total fixe mensuel | 1000 |

Total fixe annuel retenu:

- `12 000 CAD`

### Couts variables moyens par offre

Ces couts restent prudents et incluent:

- temps humain direct;
- usage outils;
- relecture / mise en forme;
- quote-part de risque operatoire direct.

| Offre | Prix moyen retenu | Cout variable moyen retenu | Marge de contribution unitaire |
|---|---:|---:|---:|
| `Signal clair` | 2 000 | 700 | 1 300 |
| `Dossier suivi` | 4 500 | 1 800 | 2 700 |
| `Veille active` | 1 800 / mois | 700 / mois | 1 100 / mois |
| `Observatoire Quebec` | 3 800 / mois | 1 600 / mois | 2 200 / mois |
| `Atelier methode` | 1 500 | 400 | 1 100 |

Important:

- ces couts ne sont pas des salaires complets;
- ils representent une premiere estimation de cout direct de production;
- la marge de contribution doit encore absorber les couts fixes annuels.

---

## 4) Definition des scenarios

### Scenario A - Prudent

Hypothese:

- traction lente;
- peu de clients recurrents;
- quelques mandats ponctuels.

### Scenario B - Intermediaire

Hypothese:

- adoption correcte;
- 2 ou 3 relations recurrentes;
- mix sain entre mandats et suivi mensuel.

### Scenario C - Ambitieux

Hypothese:

- traction commerciale reelle;
- observatoire finance;
- meilleure reutilisation du corpus.

---

## 5) Volumes annuels simules

| Offre | Scenario prudent | Scenario intermediaire | Scenario ambitieux |
|---|---:|---:|---:|
| `Signal clair` | 8 | 18 | 30 |
| `Dossier suivi` | 4 | 10 | 18 |
| `Veille active` | 12 mois-client | 36 mois-client | 72 mois-client |
| `Observatoire Quebec` | 0 | 6 mois-client | 12 mois-client |
| `Atelier methode` | 2 | 6 | 12 |

Lecture:

- `12 mois-client` de `Veille active` = par exemple `1 client sur 12 mois` ou `2 clients sur 6 mois`.

---

## 6) Resultats synthetiques

### Revenus annuels

| Offre | Scenario prudent | Scenario intermediaire | Scenario ambitieux |
|---|---:|---:|---:|
| `Signal clair` | 16 000 | 36 000 | 60 000 |
| `Dossier suivi` | 18 000 | 45 000 | 81 000 |
| `Veille active` | 21 600 | 64 800 | 129 600 |
| `Observatoire Quebec` | 0 | 22 800 | 45 600 |
| `Atelier methode` | 3 000 | 9 000 | 18 000 |
| `Revenu total` | 58 600 | 177 600 | 334 200 |

### Couts variables annuels

| Offre | Scenario prudent | Scenario intermediaire | Scenario ambitieux |
|---|---:|---:|---:|
| `Signal clair` | 5 600 | 12 600 | 21 000 |
| `Dossier suivi` | 7 200 | 18 000 | 32 400 |
| `Veille active` | 8 400 | 25 200 | 50 400 |
| `Observatoire Quebec` | 0 | 9 600 | 19 200 |
| `Atelier methode` | 800 | 2 400 | 4 800 |
| `Cout variable total` | 22 000 | 67 800 | 127 800 |

### Marge de contribution avant couts fixes

| Scenario | Revenu total | Cout variable total | Marge de contribution |
|---|---:|---:|---:|
| prudent | 58 600 | 22 000 | 36 600 |
| intermediaire | 177 600 | 67 800 | 109 800 |
| ambitieux | 334 200 | 127 800 | 206 400 |

### Resultat apres couts fixes annuels

| Scenario | Marge de contribution | Couts fixes annuels | Resultat annuel estime |
|---|---:|---:|---:|
| prudent | 36 600 | 12 000 | 24 600 |
| intermediaire | 109 800 | 12 000 | 97 800 |
| ambitieux | 206 400 | 12 000 | 194 400 |

---

## 7) Detail par scenario

### Scenario A - Prudent

Configuration plausible:

- `8` fiches `Signal clair`
- `4` `Dossier suivi`
- `1` client de `Veille active` sur 12 mois
- `0` observatoire finance
- `2` ateliers

Lecture:

- scenario realiste si la traction est lente mais serieuse;
- permet deja de prouver une soutenabilite de base si le cout fixe reste tres lean;
- reste fortement dependant du travail de service.

### Scenario B - Intermediaire

Configuration plausible:

- `18` fiches `Signal clair`
- `10` `Dossier suivi`
- `3` clients `Veille active` sur 12 mois equivalents
- `1` observatoire sur `6 mois`
- `6` ateliers

Lecture:

- c'est le scenario de reference le plus utile;
- il montre un equilibre entre ponctuel, recurrent et structurant;
- il commence a financer reellement la consolidation de l'outil.

### Scenario C - Ambitieux

Configuration plausible:

- `30` fiches `Signal clair`
- `18` `Dossier suivi`
- `6` clients `Veille active` sur 12 mois equivalents
- `1` observatoire sur `12 mois`
- `12` ateliers

Lecture:

- scenario exigeant;
- suppose une execution solide et un positionnement commercial deja lisible;
- ne doit pas servir d'hypothese psychologique de confort.

---

## 8) Lecture economique utile

### Lecture 1 - La recurrence change tout

La vraie stabilite ne vient pas des offres ponctuelles seules.

Elle vient surtout de:

- `Veille active`
- `Observatoire Quebec`

Conclusion:

`MESANGE ne doit pas vivre uniquement de mandats one-shot s'il veut sortir de la fragilite`

### Lecture 2 - `Dossier suivi` reste l'offre coeur

Cette offre:

- incarne le mieux la valeur MESANGE;
- justifie un prix plus eleve;
- nourrit la veille, les chronologies et les futurs livrables.

Conclusion:

`c'est l'offre identitaire, meme si ce n'est pas toujours la plus recurrente`

### Lecture 3 - `Signal clair` est la meilleure porte d'entree

Elle est:

- plus simple a acheter;
- plus rapide a produire;
- utile pour convaincre;
- susceptible de convertir vers `Dossier suivi` ou `Veille active`.

### Lecture 4 - L'observatoire est un accelerateur, pas un prerequis

MESANGE peut demarrer sans observatoire finance.

Mais:

- un observatoire change fortement la lisibilite financiere;
- il cree un actif documentaire plus durable;
- il augmente la credibilite publique.

---

## 9) Seuils simples a retenir

### Seuil de survie lean

Pour absorber `12 000 CAD` de couts fixes annuels, MESANGE doit produire environ:

- `10` `Dossier suivi` de marge moyenne
ou
- `11` mois-client de `Veille active`
ou
- un mix equivalent.

Lecture:

- le seuil de survie n'est pas hors de portee;
- il exige cependant une vraie discipline commerciale.

### Seuil de consolidation

Pour financer:

- l'outillage interne;
- plus de rigueur;
- un peu de marge de manoeuvre;

il faut viser au moins le scenario `intermediaire`.

---

## 10) Ce qui n'est pas encore inclus

Cette simulation ne compte pas encore:

- abonnement premium grand public;
- revenus SaaS;
- grants ou subventions ponctuelles;
- cout complet d'une equipe salariee plus large;
- fiscalite detaillee;
- cout d'acquisition commerciale documente;
- cout juridique fort en cas de contentieux.

Donc:

`les resultats annuels estimes sont utiles comme signal de viabilite, pas comme benefice net final garanti`

---

## 11) Recommendation nette

Je recommande de piloter MESANGE avec l'objectif suivant:

### Objectif 12 mois minimal

- atteindre au moins le scenario `prudent`
- avec une priorite sur:
  - `Signal clair`
  - `Dossier suivi`
  - `Veille active`

### Objectif 12 mois cible

- tendre vers le scenario `intermediaire`
- en essayant d'obtenir:
  - `2 a 3` relations recurrentes;
  - `1` premier observatoire court;
  - un petit nombre de dossiers exemplaires tres solides.

### Ce qu'il faut eviter

- compter sur le grand public trop tot;
- lancer un SaaS complet avant preuve de vente;
- vendre trop peu cher des dossiers lourds;
- accepter des veilles mal cadre es.

---

## 12) Conclusion

La simulation montre une chose utile:

`MESANGE peut devenir economiquement defensable au Quebec si le lancement privilegie les bons packages et si la recurrence est construite tot.`

Le coeur du modele n'est pas:

- la quantite de contenu;
- la virality;
- l'empilement de sujets;

mais:

- la valeur de clarification;
- la memoire documentaire;
- la reutilisation des dossiers;
- le passage progressif du ponctuel au recurrent.

---

## 13) Prochaine etape recommandee

Apres cette simulation, les deux livrables les plus utiles sont:

1. une spec d'ecrans admin MESANGE
2. une grille commerciale courte pour pitcher les 3 premieres offres


# MERLIN - Tableau prix coutant, marge et benefice par seance (v1)

Date: 2026-04-20
Statut: draft
Objet: comparer les prix par seance selon plusieurs offres MERLIN, avec coutant variable, marge brute unitaire et benefice de contribution

---

## 1) Hypothese retenue

Hypothese active:

`Stripe est a la charge du praticien`

Donc, pour MERLIN, le cout variable unitaire retenu dans ce tableau est:

- transcription: `0.24 CAD`
- IA analyse: `0.01 CAD`
- stockage: `0.01 CAD`

Total coutant variable par seance:

`0.26 CAD`

Cette base `0.26 CAD` correspond au noyau:
- transcription;
- IA courte;
- stockage;

mais elle ne detaille pas encore les variantes de service.

---

## 2) Definition des colonnes

- `prix facture / seance`: ce que MERLIN facture au praticien par seance
- `coutant variable / seance`: ce que MERLIN depense directement pour fournir le service sur cette seance
- `marge brute / seance`: `prix facture - coutant variable`
- `benefice de contribution / seance`: identique ici a la marge brute unitaire, avant deduction des frais fixes mensuels

Important:

`ce tableau ne donne pas le benefice net final de l'entreprise`

car il ne retire pas encore:
- dev;
- admin;
- vente;
- comptabilite;
- support lourd;
- juridique;
- impots.

---

## 3) Grille TARIF - COST - REVENUS

Cette grille devient la lecture de reference.

Logique:
- `TARIF`: prix facture par seance au praticien
- `COST`: coutant variable direct MERLIN par seance
- `REVENUS`: marge brute unitaire ou benefice de contribution par seance

### Grille synthetique par variante de service

| Variante | Services inclus | Tarif petit volume | Tarif volume regulier | Tarif gros volume | Cost / seance | Revenus petit volume | Revenus volume regulier | Revenus gros volume |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| V1 Logistique | prise de rdv + rappels + revue email | 4.90 | 4.40 | 3.90 | 0.05 | 4.85 | 4.35 | 3.85 |
| V2 Trace | V1 + transcription + stockage | 5.90 | 5.40 | 4.90 | 0.30 | 5.60 | 5.10 | 4.60 |
| V3 Synthese | V2 + resume simple | 7.90 | 7.40 | 6.90 | 0.31 | 7.59 | 7.09 | 6.59 |
| V4 Orientation prudente | V2 + resume avec preconisations prudentes | 9.90 | 9.40 | 8.90 | 0.33 | 9.57 | 9.07 | 8.57 |
| V5 Historique | V2 + resume historique avec preconisations | 12.90 | 11.90 | 10.90 | 0.38 | 12.52 | 11.52 | 10.52 |

### Lecture immediate

- `V1` vend la commodite.
- `V2` vend la trace.
- `V3` vend la synthese.
- `V4` vend l'aide prudente a la suite.
- `V5` vend la memoire et la continuite.

Conclusion directe:

`plus MERLIN vend de structuration et de continuite, plus le tarif eleve devient defendable`

---

## 4) Briques de cout par service

Pour integrer vos vraies variantes, il faut raisonner par briques.

Les montants ci-dessous sont des `coutants variables operatoires` par seance.

| Brique de service | Hypothese coutant / seance | Commentaire |
|---|---:|---|
| Prise de rdv + rappels + envoi email simple | 0.05 | notifications, orchestration, envoi email |
| Transcription | 0.24 | scenario bas type AssemblyAI |
| Resume simple | 0.01 | synthese courte post-seance |
| Resume avec preconisations prudentes | 0.03 | resume plus structure + suggestions prudentes |
| Resume historique avec preconisations | 0.08 | comparaison avec historique + synthese enrichie |
| Stockage / memoire | 0.01 | retention legere, arrondie prudemment |

### Regle de composition

- une offre `prise de rdv + revue email` n'inclut pas transcription;
- une offre avec transcription inclut aussi la memoire minimale;
- les `preconisations` doivent toujours etre lues comme prudentes:
  - pas de diagnostic;
  - pas de prescription reservee;
  - pas de causalite profonde affirmee.

---

## 5) Tableau par variantes de service

### Coutant variable par variante

| Variante | Services inclus | Coutant variable / seance |
|---|---|---:|
| V1 Logistique | prise de rdv + rappels + revue email | 0.05 |
| V2 Trace | V1 + transcription + stockage | 0.30 |
| V3 Synthese | V2 + resume simple | 0.31 |
| V4 Orientation prudente | V2 + resume avec preconisations prudentes | 0.33 |
| V5 Historique | V2 + resume historique avec preconisations | 0.38 |

### Prix indicatifs par volume

| Variante | Petit volume | Volume regulier | Gros volume |
|---|---:|---:|---:|
| V1 Logistique | 4.90 | 4.40 | 3.90 |
| V2 Trace | 5.90 | 5.40 | 4.90 |
| V3 Synthese | 7.90 | 7.40 | 6.90 |
| V4 Orientation prudente | 9.90 | 9.40 | 8.90 |
| V5 Historique | 12.90 | 11.90 | 10.90 |

### Marge brute par variante et par volume

| Variante | Coutant | Marge petit volume | Marge volume regulier | Marge gros volume |
|---|---:|---:|---:|---:|
| V1 Logistique | 0.05 | 4.85 | 4.35 | 3.85 |
| V2 Trace | 0.30 | 5.60 | 5.10 | 4.60 |
| V3 Synthese | 0.31 | 7.59 | 7.09 | 6.59 |
| V4 Orientation prudente | 0.33 | 9.57 | 9.07 | 8.57 |
| V5 Historique | 0.38 | 12.52 | 11.52 | 10.52 |

### Benefice de contribution par seance

Dans ce tableau, le `benefice de contribution / seance` est identique a la marge brute unitaire:

- il sert a absorber vos frais fixes;
- puis seulement, ce qui reste devient benefice net.

---

## 6) Lecture immediate des variantes

### V1 Logistique

Ce niveau couvre:
- prise de rdv;
- rappels;
- email simple.

Il est vendable comme commodite, mais c'est la couche la plus facilement comparable a Jane, Owl ou SimplePractice.

### V2 Trace

Ce niveau commence a devenir vraiment MERLIN:
- transcription;
- trace textuelle;
- base documentaire.

### V3 Synthese

Ici, MERLIN commence a vendre:
- non seulement la trace;
- mais la transformation de la trace en objet utile.

### V4 Orientation prudente

Cette couche devient differenciante si elle reste bien cadre e:
- resume;
- preconisations prudentes;
- aide a la suite.

### V5 Historique

C'est la couche la plus premium:
- resume de seance;
- mise en relation avec l'historique;
- preconisations prudentes appuyees sur la continuite.

---

## 7) Tableau principal

### Offre prudente actuelle

| Offre | Volume | Prix facture / seance | Coutant variable / seance | Marge brute / seance | Benefice de contribution / seance |
|---|---|---:|---:|---:|---:|
| Prudente | Petit volume | 5.90 | 0.26 | 5.64 | 5.64 |
| Prudente | Volume regulier | 5.40 | 0.26 | 5.14 | 5.14 |
| Prudente | Gros volume | 4.90 | 0.26 | 4.64 | 4.64 |

### Offre ambitieuse

| Offre | Volume | Prix facture / seance | Coutant variable / seance | Marge brute / seance | Benefice de contribution / seance |
|---|---|---:|---:|---:|---:|
| Ambitieuse | Petit volume | 15.00 | 0.26 | 14.74 | 14.74 |
| Ambitieuse | Volume regulier | 12.00 | 0.26 | 11.74 | 11.74 |
| Ambitieuse | Gros volume | 8.00 | 0.26 | 7.74 | 7.74 |

---

## 8) Lecture rapide

### Si MERLIN reste sur l'offre prudente

- la marge unitaire reste deja tres confortable si Stripe est a la charge du praticien;
- le gros volume reste rentable a `4.64 CAD` de contribution par seance.

### Si MERLIN passe sur l'offre ambitieuse

- le niveau de marge devient tres eleve;
- le sujet n'est plus la rentabilite technique;
- le sujet devient l'acceptabilite commerciale.

---

## 9) Equivalent mensuel par profil

Pour rendre le tableau plus concret, voici l'effet mensuel theorique si on applique ces offres a trois volumes de travail.

### Offre prudente actuelle

| Volume | Seances / mois | Contribution / seance | Contribution mensuelle brute |
|---|---:|---:|---:|
| Petit volume | 20 | 5.64 | 112.80 |
| Volume regulier | 60 | 5.14 | 308.40 |
| Gros volume | 150 | 4.64 | 696.00 |

### Offre ambitieuse

| Volume | Seances / mois | Contribution / seance | Contribution mensuelle brute |
|---|---:|---:|---:|
| Petit volume | 20 | 14.74 | 294.80 |
| Volume regulier | 60 | 11.74 | 704.40 |
| Gros volume | 150 | 7.74 | 1,161.00 |

---

## 10) Variante prudente si la transcription retenue coute plus cher

Si MERLIN choisit un scenario plus prudent de transcription type Deepgram Growth, le coutant variable approximatif passe a:

- transcription: `0.63`
- IA analyse: `0.01`
- stockage: `0.01`

Total:

`0.65 CAD / seance`

### Impact sur les offres

| Offre | Volume | Prix facture / seance | Coutant prudent / seance | Marge brute / seance |
|---|---|---:|---:|---:|
| Prudente | Petit volume | 5.90 | 0.65 | 5.25 |
| Prudente | Volume regulier | 5.40 | 0.65 | 4.75 |
| Prudente | Gros volume | 4.90 | 0.65 | 4.25 |
| Ambitieuse | Petit volume | 15.00 | 0.65 | 14.35 |
| Ambitieuse | Volume regulier | 12.00 | 0.65 | 11.35 |
| Ambitieuse | Gros volume | 8.00 | 0.65 | 7.35 |

Conclusion:

`meme avec une transcription plus couteuse, l'enjeu n'est pas la survie economique de MERLIN mais le bon niveau de prix percu par le marche`

---

## 11) Lecture strategique

Ce tableau montre trois choses.

1. Si Stripe est a la charge du praticien, le coutant reel de MERLIN par seance devient tres faible.
2. Vos prix peuvent donc etre structures surtout selon la valeur percue, pas selon la contrainte technique brute.
3. Une offre `15 / 12 / 8` est economiquement excellente pour MERLIN, mais elle doit etre justifiee par une vraie offre premium:
   - transcription;
   - resume;
   - reporting;
   - memoire;
   - analyse historique;
   - cadre MERLIN.

---

## 12) Recommandation provisoire

Je recommande de distinguer:

### Offre 1 - Logistique simple

- prix bas
- agenda
- rappels
- confirmation
- note simple

### Offre 2 - MERLIN standard

- transcription
- resume
- reporting
- memoire de parcours

### Offre 3 - MERLIN premium

- analyse historique
- comparaison inter-seances
- rapports evolutifs
- couche MERLIN forte

Autrement dit:

`ne pas faire porter tout votre gain sur la seule prise de rendez-vous`

mais:

`faire payer davantage la couche analytique et documentaire que les autres outils generalistes n'ont pas`

---

## 13) Decision active

Avec l'hypothese `Stripe a la charge du praticien`, MERLIN dispose deja d'une marge unitaire suffisante meme sur une offre prudente.

La vraie decision n'est donc plus:

`est-ce rentable?`

mais:

`quelle offre le marche acceptera-t-il selon la valeur percue?`

References:
- [MERLIN_GOUV_SIMULATION_ECO_COUTS_REELS_V2.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_SIMULATION_ECO_COUTS_REELS_V2.md)
- [MERLIN_GOUV_SIMULATION_ECO_3_PROFILS_PRATICIENS_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_SIMULATION_ECO_3_PROFILS_PRATICIENS_V1.md)

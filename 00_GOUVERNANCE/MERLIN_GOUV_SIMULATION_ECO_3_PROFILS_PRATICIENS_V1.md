# MERLIN - Simulation eco 3 profils praticiens V1

Date: 2026-04-20
Statut: draft
Objet: simuler la rentabilite d'une offre praticiens avec abonnement, frais plateforme degresifs au volume et options IA a l'usage

---

## 1) Finalite

Cette simulation sert a:
- tester la coherence economique du modele praticiens;
- verifier qu'un palier degresif ne passe pas sous le cout de revient;
- estimer une marge brute defendable;
- preparer une future grille tarifaire publique ou contractuelle.

Ce document n'est pas:
- une grille tarifaire finale;
- une offre publique;
- un engagement contractuel.

---

## 2) Hypotheses de travail

Les chiffres ci-dessous sont provisoires et doivent etre remplaces par les couts reels des fournisseurs.

### Hypotheses communes

- devise de travail: `CAD`
- prix moyen d'une seance payee via la plateforme: `90.00`
- abonnement praticien de base: `29.00 / mois`
- duree moyenne de seance standard: `50 min`

### Cout direct couche 1 par seance

- cout paiement: `2.91`
- agenda, rappels, notifications: `0.35`
- operation, logs, support variable: `0.29`

Total couche 1 variable par seance:
- `3.55`

### Cout fixe mensuel par praticien

- support de base
- maintenance de compte
- frais fixes d'infrastructure legere

Hypothese:
- `19.00 / mois`

### Cout couche 2

- cout transcription minute: `0.05 / min`
- prix transcription minute facture: `0.10 / min`
- cout reporting par seance transcrite: `0.60`
- prix reporting par seance transcrite: `1.50`

### Cout couche 3

- cout analyse historique / rapport longitudinal: `3.50 / rapport`
- prix facture: `7.00 / rapport`

---

## 3) Paliers simules

### Palier 1 - Petit volume

- `0 a 30 seances / mois`
- frais plateforme couche 1: `5.90 / seance`

### Palier 2 - Volume regulier

- `31 a 80 seances / mois`
- frais plateforme couche 1: `5.40 / seance`

### Palier 3 - Gros volume

- `81 a 200 seances / mois`
- frais plateforme couche 1: `4.90 / seance`

---

## 4) Profils simules

### Profil A - Petit praticien actif

- `20 seances / mois`
- `50 min` par seance
- `60%` des seances avec transcription
- `4` rapports historiques / mois

### Profil B - Praticien etabli

- `60 seances / mois`
- `50 min` par seance
- `80%` des seances avec transcription
- `12` rapports historiques / mois

### Profil C - Gros volume

- `140 seances / mois`
- `45 min` par seance
- `90%` des seances avec transcription
- `30` rapports historiques / mois

---

## 5) Resultats synthetiques

| Profil | Seances/mois | CA praticien estime | Revenu MERLIN couche 1 | Revenu MERLIN couche 2 | Revenu MERLIN couche 3 | Revenu MERLIN total | Cout direct MERLIN total | Marge brute MERLIN | Taux marge brute |
|--------|---------------|---------------------|-------------------------|-------------------------|-------------------------|---------------------|--------------------------|--------------------|------------------|
| A | 20 | 1,800.00 | 147.00 | 78.00 | 28.00 | 253.00 | 141.20 | 111.80 | 44.19% |
| B | 60 | 5,400.00 | 353.00 | 312.00 | 84.00 | 749.00 | 422.80 | 326.20 | 43.55% |
| C | 140 | 12,600.00 | 715.00 | 756.00 | 210.00 | 1,681.00 | 980.10 | 700.90 | 41.70% |

---

## 6) Detail de calcul par profil

### Profil A - Petit praticien actif

- couche 1 revenu:
  - abonnement: `29.00`
  - frais seances: `20 x 5.90 = 118.00`
  - total couche 1: `147.00`
- couche 1 cout:
  - fixe mensuel: `19.00`
  - variable seances: `20 x 3.55 = 71.00`
  - total couche 1: `90.00`

- transcription:
  - seances transcrites: `12`
  - minutes transcrites: `600`
  - revenu transcription: `600 x 0.10 = 60.00`
  - cout transcription: `600 x 0.05 = 30.00`

- reporting seances transcrites:
  - revenu: `12 x 1.50 = 18.00`
  - cout: `12 x 0.60 = 7.20`

- analyse historique:
  - revenu: `4 x 7.00 = 28.00`
  - cout: `4 x 3.50 = 14.00`

- total cout direct MERLIN:
  - `90.00 + 30.00 + 7.20 + 14.00 = 141.20`

### Profil B - Praticien etabli

- couche 1 revenu:
  - abonnement: `29.00`
  - frais seances: `60 x 5.40 = 324.00`
  - total couche 1: `353.00`
- couche 1 cout:
  - fixe mensuel: `19.00`
  - variable seances: `60 x 3.55 = 213.00`
  - total couche 1: `232.00`

- transcription:
  - seances transcrites: `48`
  - minutes transcrites: `2,400`
  - revenu transcription: `240.00`
  - cout transcription: `120.00`

- reporting seances transcrites:
  - revenu: `48 x 1.50 = 72.00`
  - cout: `48 x 0.60 = 28.80`

- analyse historique:
  - revenu: `12 x 7.00 = 84.00`
  - cout: `12 x 3.50 = 42.00`

- total cout direct MERLIN:
  - `232.00 + 120.00 + 28.80 + 42.00 = 422.80`

### Profil C - Gros volume

- couche 1 revenu:
  - abonnement: `29.00`
  - frais seances: `140 x 4.90 = 686.00`
  - total couche 1: `715.00`
- couche 1 cout:
  - fixe mensuel: `19.00`
  - variable seances: `140 x 3.55 = 497.00`
  - total couche 1: `516.00`

- transcription:
  - seances transcrites: `126`
  - minutes transcrites: `5,670`
  - revenu transcription: `567.00`
  - cout transcription: `283.50`

- reporting seances transcrites:
  - revenu: `126 x 1.50 = 189.00`
  - cout: `126 x 0.60 = 75.60`

- analyse historique:
  - revenu: `30 x 7.00 = 210.00`
  - cout: `30 x 3.50 = 105.00`

- total cout direct MERLIN:
  - `516.00 + 283.50 + 75.60 + 105.00 = 980.10`

---

## 7) Lectures utiles

### Lecture 1 - La degresivite reste defendable

Dans cette simulation, le passage de `5.90` a `4.90` par seance reste rentable parce que:
- la couche 1 conserve une marge positive;
- l'abonnement absorbe une partie des couts fixes;
- les options IA creent une marge supplementaire.

### Lecture 2 - Le vrai levier de marge est la couche 2

La transcription et le reporting peuvent devenir le coeur de marge brute, a condition que:
- les couts IA soient bien maitrises;
- le volume reel soit suivi;
- les usages lourds soient factures a l'usage.

### Lecture 3 - La couche 3 doit rester premium

L'analyse historique est utile et defendable, mais elle ne doit pas etre absorbee gratuitement dans tous les forfaits.

### Lecture 4 - Le paiement tire fortement le cout de revient

Si MERLIN encaisse les paiements des seances, le cout processeur est une composante majeure.
Si MERLIN ne collecte pas le paiement de la seance, la structure de frais pourra etre ajustee a la baisse.

---

## 8) Rectifications importantes

Il ne faut pas penser:
- `on prend juste un petit pourcentage`

mais:
- `on facture une combinaison de frais plateforme, d'usage IA et de memoire, indexes sur des couts mesurables`

Il ne faut pas penser:
- `le volume permet toujours de baisser`

mais:
- `le volume permet de baisser seulement si les economies d'echelle sont reelles`

Il ne faut pas penser:
- `la marge brute suffit`

mais:
- `la marge brute doit ensuite absorber les couts non directs: developpement, securite, administration, vente, support avance`

---

## 9) Recommandation provisoire

Pour V1, le modele le plus solide semble etre:

1. abonnement de base praticien
2. frais plateforme par seance selon palier
3. transcription facturee a la minute
4. reporting facture par seance transcrite
5. analyse historique facturee au rapport ou au pack

---

## 10) Ce qu'il faut verifier ensuite

- cout reel du fournisseur de transcription
- cout reel du modele de resume et de reporting
- cout de stockage par regime de retention
- cout support par praticien
- taux reel d'activation des couches 2 et 3
- elasticite prix des praticiens
- impact du prix moyen reel des seances sur le cout paiement

---

## 11) Decision active

Cette simulation valide une hypothese de travail:

`un modele MERLIN avec abonnement + frais plateforme degresifs + options IA a l'usage peut etre rentable, a condition que les couts unitaires soient mesures et revises`

Prochaine etape recommandee:
- construire un tableur source avec cellules modifiables;
- tester 3 variantes:
  - MERLIN collecte le paiement
  - MERLIN ne collecte pas le paiement
  - MERLIN inclut un quota gratuit partiel de transcription

References:
- [MERLIN_GOUV_MODELE_ECO_FRAIS_VOLUME_COUTS_SEUILS_v1.0.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_MODELE_ECO_FRAIS_VOLUME_COUTS_SEUILS_v1.0.md)
- [MERLIN_GOUV_MODELE_ECO_PRATICIENS_APPLICATION_v1.0.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_MODELE_ECO_PRATICIENS_APPLICATION_v1.0.md)

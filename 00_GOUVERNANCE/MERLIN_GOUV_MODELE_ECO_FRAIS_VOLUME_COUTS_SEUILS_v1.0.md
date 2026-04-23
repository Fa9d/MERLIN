# MERLIN - Modele eco frais au volume, couts et seuils (v1)

Date: 2026-04-20
Statut: draft
Objet: definir un modele de frais plateforme degresifs au volume, lies aux couts reels, avec marges minimales et protection contre le deficit

---

## 1) Decision de principe

Oui, MERLIN peut adopter un modele de frais "type Stripe":
- frais plateforme explicites;
- base fixe faible;
- frais variables par usage;
- degresivite au volume;
- eventuel plafond mensuel;
- separation entre revenu logiciel et revenu du praticien.

Mais ce modele n'est sain que si:
- les couts unitaires sont mesures;
- les seuils sont publics ou contractuels;
- les frais ne sont pas presentes comme une commission sur le soin;
- la marge minimale est protegee;
- un praticien a fort volume ne devient pas deficitaire pour MERLIN.

Doctrine:

`MERLIN peut facturer des frais d'usage sur les seances traitees par la plateforme si ces frais remunerent des services techniques explicites et mesurables.`

---

## 2) Ce que les frais remunerent

Les frais au volume ne doivent pas remunerer:
- la seule existence du client;
- l'orientation;
- une captation du soin;
- un droit implicite sur l'acte du praticien.

Ils peuvent remunerer:
- paiement;
- prise de rendez-vous;
- rappel et confirmation;
- notifications;
- transcription;
- generation de resume;
- generation de rapport;
- stockage et memoire;
- consultation de l'historique;
- support applicatif;
- audit et journalisation.

---

## 3) Structure recommandee

Je recommande une architecture en trois etages.

### Etage A - Abonnement de base

Il couvre:
- acces au compte praticien;
- agenda;
- fiche client;
- prise de rendez-vous;
- rappels standards;
- support de base;
- maintenance generale.

Role:
- absorber les couts fixes incompressibles.

### Etage B - Frais variables par usage

Ils couvrent:
- traitement de paiement;
- transcription minute;
- generation de synthese;
- rapport multi-seances;
- stockage au-dela d'un quota;
- notifications supplementaires.

Role:
- absorber les couts directement lies au volume reel.

### Etage C - Degresivite et plafonds

Ils servent a:
- rendre l'offre acceptable pour les gros praticiens;
- conserver une marge meme a fort volume;
- eviter qu'un petit praticien subventionne un gros volume non rentable.

---

## 4) Les 5 blocs de cout a mesurer

Avant de fixer les seuils, MERLIN doit calculer son cout de revient unitaire.

### Bloc 1 - Cout paiement

Exemples:
- frais processeur de paiement;
- frais de retrofacturation;
- frais de virement.

Variable cle:
- `cout_paiement_par_transaction`

### Bloc 2 - Cout IA / transcription

Exemples:
- transcription audio;
- resume;
- extraction de champs;
- analyse inter-seances;
- rapport evolutif.

Variables cles:
- `cout_transcription_par_minute`
- `cout_resume_par_seance`
- `cout_reporting_par_rapport`

### Bloc 3 - Cout memoire / stockage

Exemples:
- audio temporaire;
- transcription source;
- documents derives;
- stockage historique;
- sauvegarde.

Variables cles:
- `cout_stockage_par_go`
- `cout_retention_par_client_actif`

### Bloc 4 - Cout applicatif / operation

Exemples:
- notifications;
- visio si incluse;
- support;
- logs;
- supervision;
- securite.

Variables cles:
- `cout_operation_par_seance`
- `cout_support_par_praticien`

### Bloc 5 - Cout commercial / impayes

Exemples:
- acquisition praticien;
- onboarding;
- churn;
- impayes;
- remises commerciales.

Variables cles:
- `cout_acquisition_amorti`
- `taux_impayes_prevu`

---

## 5) Formule de cout de revient

Pour chaque seance traitee, MERLIN doit viser au minimum:

`cout_revient_unitaire = cout_paiement + cout_transcription + cout_ia + cout_stockage + cout_operation + provision_impayes`

Puis:

`prix_unitaire_minimum = cout_revient_unitaire + marge_minimale`

Si l'abonnement absorbe une partie des couts fixes, alors:

`prix_variable_minimum = cout_variable_unitaire + marge_variable_minimale`

---

## 6) Regle de marge minimale

MERLIN ne doit jamais tarifer seulement "au coutant" sans protection.

Je recommande:
- une `marge minimale absolue` par seance ou par operation;
- une `marge minimale relative` cible;
- une `revue trimestrielle` des couts reels.

Exemple de doctrine:

- marge absolue minimale par seance traitee: plancher fixe
- marge relative cible: pourcentage minimal sur les couches variables

La valeur exacte devra venir des couts reels.

---

## 7) Seuils de volume recommandes

Les seuils doivent etre simples, lisibles et contractuels.

Exemple de structure:

### Palier 1 - Petit volume

- 0 a 30 seances / mois
- frais variables standard

### Palier 2 - Volume regulier

- 31 a 80 seances / mois
- baisse moderee des frais variables

### Palier 3 - Gros volume

- 81 a 200 seances / mois
- baisse supplementaire
- plafond mensuel possible sur certaines briques

### Palier 4 - Volume institutionnel

- 200+ seances / mois
- tarification negociee
- contrat specifique
- engagement de volume

---

## 8) Sur quoi appliquer la degresivite

La degresivite ne doit pas forcement porter sur tout.

Je recommande:

### Degresif

- frais plateforme par seance;
- cout de reporting automatise;
- cout de stockage au-dela d'un seuil;
- cout d'analyse longitudinale.

### Non degresif ou peu degresif

- frais de paiement tiers si subis tels quels;
- frais legaux ou de conformite;
- support humain exceptionnel;
- options premium lourdes.

---

## 9) Formules commerciales possibles

### Modele 1 - Abonnement + frais fixes par seance

Exemple structurel:
- abonnement mensuel
- plus frais plateforme fixes par seance
- degresifs par palier

Avantage:
- simple a comprendre.

### Modele 2 - Abonnement + pourcentage plafonne

Exemple structurel:
- abonnement mensuel
- plus pourcentage sur paiement collecte
- avec minimum, maximum et degresivite

Avantage:
- proche des usages de marche.

Risque:
- ressemble vite a une commission sur l'acte si mal explique.

### Modele 3 - Abonnement + briques d'usage facturees

Exemple structurel:
- abonnement mensuel
- transcription a la minute
- rapport a l'unite
- stockage au quota depasse

Avantage:
- tres defensable comptablement.

Risque:
- complexite commerciale.

### Recommandation

Le meilleur compromis V1 est souvent:

`abonnement de base + frais fixes par seance + options IA facturees a l'usage + degresivite par palier`

---

## 10) Modele de calcul recommande pour MERLIN

Je recommande de calculer chaque mois:

1. nombre de seances facturees
2. nombre de minutes transcrites
3. nombre de rapports generes
4. volume de stockage actif
5. cout variable total
6. revenu total plateforme
7. marge brute plateforme
8. marge brute par praticien

Puis d'appliquer:

`si marge brute par praticien passe sous le plancher, ajustement automatique du palier ou du minimum facture`

Cela evite:
- les gros comptes non rentables;
- les petits comptes sous-tarifes;
- l'impression de croissance alors que la marge disparait.

---

## 11) Garde-fous contractuels

Chaque contrat praticien devrait preciser:
- abonnement de base;
- services inclus;
- services variables;
- mode de calcul des frais;
- paliers de volume;
- plafond eventuel;
- minimum facture;
- revision des tarifs;
- changement de palier;
- retention et stockage inclus;
- frais hors forfait.

Sans cela, le modele devient:
- difficile a auditer;
- source de conflit;
- fragile juridiquement.

---

## 12) Ce qu'il faut absolument eviter

- un pourcentage nu sans minimum ni plafond;
- une degresivite qui passe sous le cout reel;
- des options IA lourdes absorbees gratuitement;
- un stockage illimite implicite;
- un discours "faible commission" si le vrai cout est porte par MERLIN;
- un prix de lancement fixe sans table de revalorisation.

---

## 13) Position recommandee

MERLIN peut parler ainsi:

`nos frais plateforme couvrent l'infrastructure de rendez-vous, les rappels, la documentation, la memoire, la transcription et les fonctions d'analyse activees.`

`ils diminuent avec le volume lorsque nos economies d'echelle sont reelles, mais restent indexes a nos couts techniques et a un plancher de marge.`

---

## 14) Decision active

MERLIN adopte le principe suivant:

`tout modele de frais au volume doit reposer sur une decomposition explicite du cout de revient, des seuils contractuels et une marge minimale protegee`

Prochaine etape recommandee:
- construire une feuille de calcul des couts unitaires;
- simuler 3 profils praticiens:
  - faible volume
  - volume regulier
  - gros volume
- puis seulement fixer les chiffres publics.

References:
- [MERLIN_GOUV_MODELE_ECO_PRATICIENS_APPLICATION_v1.0.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_MODELE_ECO_PRATICIENS_APPLICATION_v1.0.md)
- [MERLIN_GOUV_MODELE_ECO_GOUVERNANCE_ORIENTATION_v1.0.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_MODELE_ECO_GOUVERNANCE_ORIENTATION_v1.0.md)
- [MERLIN_GOUV_ETUDE_MARCHE_CADRAGE_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_ETUDE_MARCHE_CADRAGE_V1.md)

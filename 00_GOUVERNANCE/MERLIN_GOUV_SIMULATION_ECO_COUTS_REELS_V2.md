# MERLIN - Simulation eco couts reels V2

Date: 2026-04-20
Version: 2.0
Statut: draft
Objet: ancrer la simulation economique praticiens sur des couts fournisseurs 2026, avec distinction entre couts verifies, estimations et points a confirmer

---

## 0) Position de principe

Ce document ameliore la simulation V1 en la rapprochant de couts fournisseurs reels.

Il ne doit pas etre lu comme:
- une tarification finale;
- une promesse contractuelle;
- une verite stable independante des volumes et fournisseurs.

Il doit etre lu comme:
- un cadrage economique plus realiste;
- une base de decision produit;
- un outil de verification des planchers de marge.

---

## 1) Sources et statut des donnees

### Sources a priorite elevee

| Bloc | Fournisseur | Donnee retenue | Statut source |
|---|---|---:|---|
| Paiement | Stripe Canada | 2.9% + 0.30 CAD / transaction | direct |
| Transcription async | Deepgram Nova-3 PAYG | 0.0077 USD / min | direct |
| Transcription async | Deepgram Nova-3 Growth | 0.0065 USD / min | direct |
| Transcription async | Gladia async | 0.61 USD / heure | direct ou a reverifier |
| IA analyse input | GPT-4.1-mini | 0.40 USD / 1M tokens input | direct |
| IA analyse output | GPT-4.1-mini | 1.60 USD / 1M tokens output | direct |
| Stockage audio | AWS S3 Standard | 0.023 USD / Go / mois | direct |
| Stockage audio | OVH Object Storage | ~0.01 USD / Go / mois | estimation fournisseur / a confirmer |

### Sources a priorite moyenne

| Bloc | Fournisseur | Donnee retenue | Statut source |
|---|---|---:|---|
| Infra VPS LiveKit | OVH VPS-2 | 9.99 EUR / mois | secondaire / a confirmer chez OVH |
| Infra VPS applicatif | OVH VPS-1 | 6.49 EUR / mois | secondaire / a confirmer chez OVH |
| Transcription async | AssemblyAI batch | 0.0025 USD / min | secondaire / a confirmer directement |

### Correction importante

Le cout AssemblyAI retenu est interessant pour la simulation, mais la source actuelle est indirecte.

Donc:
- on peut l'utiliser comme hypothese basse;
- on ne doit pas encore le traiter comme cout fournisseur final valide.

---

## 2) Hypotheses de calcul par seance

### Seance type MERLIN

- duree moyenne: `70 min`
- prix moyen praticien: `90.00 CAD`
- audio mono enregistre cote serveur
- taille audio estimee: `35 Mo / seance`
- taux de conversion de travail: `1 USD = 1.38 CAD`

### Cout paiement Stripe

Calcul:

`2.9% x 90.00 + 0.30 = 2.61 + 0.30 = 2.91 CAD`

Resultat retenu:
- `2.91 CAD / seance`

### Cout transcription par seance de 70 min

| Option | Calcul | Cout USD | Cout CAD |
|---|---|---:|---:|
| AssemblyAI batch | 70 x 0.0025 | 0.175 | 0.24 |
| Deepgram Nova-3 PAYG | 70 x 0.0077 | 0.539 | 0.74 |
| Deepgram Nova-3 Growth | 70 x 0.0065 | 0.455 | 0.63 |
| Gladia async | 70 / 60 x 0.61 | 0.712 | 0.98 |

Lecture:
- AssemblyAI donne ici l'hypothese basse;
- Deepgram Growth donne une hypothese plus prudente si la qualite ou la robustesse prime;
- la qualite sur francais quebecois doit etre validee par tests terrain, pas seulement affirmee.

### Cout IA analyse + rapport

Hypothese de travail:
- input transcription: `10,000 tokens`
- output rapport: `2,000 tokens`
- modele: `GPT-4.1-mini`

Calcul:
- input: `10,000 x (0.40 / 1,000,000) = 0.004 USD`
- output: `2,000 x (1.60 / 1,000,000) = 0.0032 USD`
- total: `0.0072 USD`
- conversion CAD: `0.0099 CAD`

Resultat retenu:
- `0.01 CAD / seance`

### Cout stockage audio

#### Hypothese AWS

Calcul:

`0.035 Go x 0.023 USD x 12 mois = 0.00966 USD`

Conversion:

`0.00966 x 1.38 = 0.0133 CAD`

Resultat:
- `~0.01 CAD / seance`

#### Hypothese OVH

Calcul:

`0.035 Go x 0.01 USD x 12 mois = 0.0042 USD`

Conversion:

`0.0042 x 1.38 = 0.0058 CAD`

Resultat:
- `~0.006 CAD / seance`

Conclusion:
- le stockage est negligeable dans les deux cas a ce niveau;
- `0.01 CAD / seance` reste une hypothese prudente acceptable.

### Infra VPS mensuelle mutualisee

| Composant | Hypothese retenue | Cout mensuel CAD |
|---|---|---:|
| LiveKit audio | OVH VPS-2 | ~15 |
| App + API + DB | OVH VPS-1 | ~10 |
| Total infra | mutualisee | ~25 |

Correction:
- ce chiffre est credible pour un demarrage lean;
- il doit etre confirme directement chez le fournisseur;
- il ne couvre pas necessairement tous les cas de charge, d'egress ou de supervision.

---

## 3) Recapitulatif des couts variables directs

### Scenario bas avec AssemblyAI

| Bloc de cout | Cout CAD / seance |
|---|---:|
| Paiement Stripe | 2.91 |
| Transcription | 0.24 |
| IA analyse + rapport | 0.01 |
| Stockage audio 12 mois | 0.01 |
| Total variable / seance | 3.17 |

### Scenario prudent avec Deepgram Growth

| Bloc de cout | Cout CAD / seance |
|---|---:|
| Paiement Stripe | 2.91 |
| Transcription | 0.63 |
| IA analyse + rapport | 0.01 |
| Stockage audio 12 mois | 0.01 |
| Total variable / seance | 3.56 |

Lecture:
- votre nouvelle V2 confirme que la V1 etait deja dans le bon ordre de grandeur;
- la vraie incertitude porte surtout sur le fournisseur de transcription et sur le fait que MERLIN collecte ou non le paiement.

---

## 4) Simulation 3 profils praticiens

### Definition des profils

| Profil | Seances / mois | CA praticien / mois | Abonnement MERLIN |
|---|---:|---:|---:|
| Petit volume | 20 | 1,800.00 | 27.99 |
| Volume regulier | 60 | 5,400.00 | 47.99 |
| Gros volume | 150 | 13,500.00 | 84.99 |

### Frais plateforme par seance

| Profil | Frais / seance | Logique |
|---|---:|---|
| Petit volume | 5.90 | marge plus confortable |
| Volume regulier | 5.40 | degressivite legere |
| Gros volume | 4.90 | fidelisation + volume |

### Plancher absolu

Scenario bas:

`cout variable reel = 3.17`

Si marge minimale souhaitee:

`+ 1.00`

Alors:

`plancher absolu = 4.17 CAD / seance`

Conclusion:
- `4.90` reste au-dessus du plancher dans le scenario bas;
- il faut toutefois reevaluer ce plancher si la transcription retenue n'est plus AssemblyAI.

---

## 5) Tableau de simulation complet

### Profil A - Petit volume

| Ligne | Calcul | Montant CAD |
|---|---|---:|
| Abonnement mensuel | fixe | 27.99 |
| Frais seances | 20 x 5.90 | 118.00 |
| Revenu total MERLIN |  | 145.99 |
| Paiement Stripe | 20 x 2.91 | -58.20 |
| Transcription | 20 x 0.24 | -4.80 |
| IA analyse | 20 x 0.01 | -0.20 |
| Stockage | 20 x 0.01 | -0.20 |
| Total couts variables |  | -63.40 |
| Marge brute avant infra |  | 82.59 |

Marge brute par seance:

`82.59 / 20 = 4.13 CAD`

### Profil B - Volume regulier

| Ligne | Calcul | Montant CAD |
|---|---|---:|
| Abonnement mensuel | fixe | 47.99 |
| Frais seances | 60 x 5.40 | 324.00 |
| Revenu total MERLIN |  | 371.99 |
| Paiement Stripe | 60 x 2.91 | -174.60 |
| Transcription | 60 x 0.24 | -14.40 |
| IA analyse | 60 x 0.01 | -0.60 |
| Stockage | 60 x 0.01 | -0.60 |
| Total couts variables |  | -190.20 |
| Marge brute avant infra |  | 181.79 |

Marge brute par seance:

`181.79 / 60 = 3.03 CAD`

### Profil C - Gros volume

| Ligne | Calcul | Montant CAD |
|---|---|---:|
| Abonnement mensuel | fixe | 84.99 |
| Frais seances | 150 x 4.90 | 735.00 |
| Revenu total MERLIN |  | 819.99 |
| Paiement Stripe | 150 x 2.91 | -436.50 |
| Transcription | 150 x 0.24 | -36.00 |
| IA analyse | 150 x 0.01 | -1.50 |
| Stockage | 150 x 0.01 | -1.50 |
| Total couts variables |  | -475.50 |
| Marge brute avant infra |  | 344.49 |

Marge brute par seance:

`344.49 / 150 = 2.30 CAD`

---

## 6) Seuil de rentabilite globale lean

### Frais fixes mensuels MERLIN

| Poste | Cout mensuel CAD | Statut |
|---|---:|---|
| Infra OVH 2 VPS | ~25 | hypothese plausible |
| Domaine + SSL + DNS | ~5 | a confirmer |
| Outils dev + monitoring | ~20 | a confirmer |
| Comptabilite / admin | ~100 | hypothese basse |
| Total fixe lean | ~150 | scenario minimum |

Lecture:
- ce niveau est credible pour un demarrage tres lean;
- il ne couvre pas le vrai cout fondateur, le dev, la vente, le juridique ou le support intensif.

Conclusion de simulation:
- un praticien regulier peut couvrir ce socle lean;
- 2 a 3 praticiens actifs rendent le systeme positif sur ce perimetre minimal.

Mais:
- cela ne signifie pas que l'entreprise complete est rentable.

---

## 7) Lecture strategique

### Ce que ce document confirme

1. Le plancher de `4.17 CAD / seance` tient dans le scenario bas.
2. Stripe est de loin le cout variable dominant lorsque MERLIN collecte le paiement.
3. La transcription est peu couteuse a l'echelle unitaire.
4. L'analyse IA post-seance est quasi negligeable en cout direct.
5. L'infra lean mutualisee n'est pas le principal probleme economique au debut.

### Ce que ce document ne prouve pas encore

1. Que le fournisseur de transcription choisi tient la qualite voulue sur votre corpus reel.
2. Que les couts de visio, d'enregistrement, d'egress et de support resteront aussi bas en charge.
3. Que les praticiens accepteront ces paliers de prix.
4. Que le modele sans collecte de paiement sera commercialement plus simple dans tous les cas.

### Recommandation produit

Pour le MVP:
- faire payer l'abonnement MERLIN separement;
- eviter si possible de collecter les paiements clients des praticiens au debut;
- garder la transcription et l'analyse comme coeur de valeur;
- vendre la couche historique comme premium.

---

## 8) Tableau de verification des postes

| Poste | Valeur retenue V2 | Source | Statut |
|---|---:|---|---|
| Stripe Canada | 2.9% + 0.30 CAD | directe | a revalider au lancement |
| AssemblyAI batch | 0.0025 USD / min | indirecte | a confirmer |
| Deepgram Growth | 0.0065 USD / min | directe | utilisable |
| GPT-4.1-mini input | 0.40 USD / 1M | directe | utilisable |
| GPT-4.1-mini output | 1.60 USD / 1M | directe | utilisable |
| OVH object storage | ~0.01 USD / Go / mois | estimation | a confirmer |
| OVH VPS-2 | 9.99 EUR / mois | secondaire | a confirmer |
| OVH VPS-1 | 6.49 EUR / mois | secondaire | a confirmer |

---

## 9) Decision active

Ce document ameliore reellement la simulation precedente.

Votre intuition principale tient:

`le vrai cout marginal de MERLIN ne vient probablement pas de l'IA d'analyse, mais surtout du paiement si MERLIN collecte la transaction`

La meilleure suite n'est pas de changer encore les prix.
La meilleure suite est:
- confirmer 4 ou 5 fournisseurs reels;
- tester la qualite transcription sur des seances types;
- produire une V3 avec deux branches:
  - MERLIN collecte le paiement
  - MERLIN ne collecte pas le paiement

References:
- [MERLIN_GOUV_SIMULATION_ECO_3_PROFILS_PRATICIENS_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_SIMULATION_ECO_3_PROFILS_PRATICIENS_V1.md)
- [MERLIN_GOUV_MODELE_ECO_FRAIS_VOLUME_COUTS_SEUILS_v1.0.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_MODELE_ECO_FRAIS_VOLUME_COUTS_SEUILS_v1.0.md)

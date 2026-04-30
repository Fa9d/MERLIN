# MERLIN - Modele eco MESANGE pilotage couts budgets rentabilisation v1.0

Date: 2026-04-25
Statut: draft
Objet: definir un cadre economique operable pour MESANGE afin de suivre les couts, allouer des budgets, mesurer la valeur produite par sujet et structurer les voies de rentabilisation

---

## 1) Position de principe

MESANGE ne doit pas etre pense uniquement comme:

- un outil de veille;
- un moteur d'analyse;
- un espace editorial;
- une base de dossiers.

MESANGE doit aussi etre pense comme:

- un systeme de pilotage economique;
- un dispositif d'arbitrage entre bruit, valeur et cout;
- une machine a produire des dossiers exploitables sans perdre la lisibilite financiere.

Doctrine:

`Toute analyse MESANGE doit pouvoir etre rattachee a un cout, a un budget, a une finalite et, lorsque pertinent, a une valeur economique ou strategique explicite.`

---

## 2) Ce que le pilotage economique doit rendre visible

Le bloc economique doit permettre de voir, par source, par sujet et par dossier:

- ce qui coute;
- ce qui consomme du temps;
- ce qui depasse le budget;
- ce qui produit de la valeur;
- ce qui se rentabilise;
- ce qui ne se justifie plus.

MESANGE doit donc mesurer quatre niveaux:

1. `cout par source`
2. `cout par analyse`
3. `cout par dossier / sujet`
4. `revenu ou valeur par livrable / service / client`

---

## 3) Les 5 blocs de cout a suivre

### Bloc 1 - Couts outils

Exemples:

- LLM;
- scraping;
- transcription;
- recherche web;
- stockage;
- vectorisation;
- monitoring;
- newsletters;
- API externes;
- automatisations.

Variables:

- `cout_api_llm`
- `cout_scraping`
- `cout_transcription`
- `cout_stockage`
- `cout_recherche`

### Bloc 2 - Couts humains

Exemples:

- tri;
- lecture;
- verification;
- validation;
- redaction;
- relecture;
- publication;
- mise a jour dossier;
- coordination.

Variables:

- `temps_tri_h`
- `temps_verification_h`
- `temps_redaction_h`
- `temps_validation_h`
- `tjm_interne_ou_taux_horaire`

### Bloc 3 - Couts de diffusion

Exemples:

- montage;
- graphisme;
- site;
- publication;
- envoi newsletter;
- promotion;
- diffusion sociale.

Variables:

- `cout_publication`
- `cout_graphisme`
- `cout_diffusion`

### Bloc 4 - Couts fixes mutualises

Exemples:

- VPS;
- sauvegardes;
- domaines;
- maintenance;
- comptabilite;
- juridique;
- administration;
- assurance;
- outils collaboratifs.

Variables:

- `cout_fixe_mensuel_total`
- `quote_part_par_sujet`
- `quote_part_par_dossier`

### Bloc 5 - Couts de risque

Exemples:

- temps de correction;
- retractation editoriale;
- verification supplementaire;
- revue legale;
- reouverture de dossier;
- traitement d'erreur publique.

Variables:

- `cout_correction`
- `cout_revue_legale`
- `cout_reprise_dossier`

---

## 4) Unites economiques de base

MESANGE doit raisonner au minimum avec ces unites:

- `source`
- `item source`
- `analyse`
- `dossier`
- `sujet`
- `livrable`
- `client`
- `axe de veille`
- `periode`

Les deux unites les plus importantes sont:

- `dossier`
- `sujet`

Car ce sont elles qui permettent de relier:

- informations;
- travail;
- decisions;
- resolution;
- cout;
- revenu;
- impact.

---

## 5) Structure budgetaire recommandee

Je recommande trois etages.

### Etage A - Budget global

Il couvre la capacite totale de MESANGE sur une periode.

Exemple:

- budget mensuel total;
- budget trimestriel;
- enveloppe exceptionnelle.

### Etage B - Budget par programme ou axe

Exemples:

- veille politique Quebec;
- verification publique;
- mouvements citoyens;
- doctrine MESANGE;
- chroniques;
- mandats client.

### Etage C - Budget par dossier / sujet

Chaque sujet suivi doit avoir:

- un budget cible;
- un plafond d'investissement;
- un seuil d'alerte;
- un responsable;
- une justification.

---

## 6) Tableaux de budget minimaux

### Tableau A - Budget par axe

| Axe | Budget mensuel | Budget consomme | Ecart | Statut |
|---|---:|---:|---:|---|
| veille politique QC | 2500 | a calculer | a calculer | open |
| verification publique | 1800 | a calculer | a calculer | open |
| doctrine / cadre MESANGE | 600 | a calculer | a calculer | open |
| diffusion editoriale | 900 | a calculer | a calculer | open |

### Tableau B - Budget par dossier

| Dossier | Axe | Budget cible | Plafond | Cout reel | Ecart | Statut |
|---|---|---:|---:|---:|---:|---|
| dossier logement | veille politique QC | 350 | 500 | a calculer | a calculer | open |
| dossier sante publique | verification publique | 450 | 650 | a calculer | a calculer | open |

### Tableau C - Budget par outil

| Outil | Periode | Budget | Reel | Ecart | Commentaire |
|---|---|---:|---:|---:|---|
| LLM | mensuel | 300 | a calculer | a calculer | |
| scraping | mensuel | 120 | a calculer | a calculer | |
| transcription | mensuel | 180 | a calculer | a calculer | |
| hebergement | mensuel | 80 | a calculer | a calculer | |

---

## 7) Tableau de frais recommande

Structure minimale:

| Date | Sujet ID | Dossier ID | Type de cout | Ressource | Quantite | Unite | Cout unitaire | Cout total | Budget associe | Responsable | Justification |
|---|---|---|---|---|---:|---|---:|---:|---|---|---|

Types de cout recommandes:

- `outil_llm`
- `outil_recherche`
- `outil_transcription`
- `temps_tri`
- `temps_verification`
- `temps_redaction`
- `temps_validation`
- `temps_publication`
- `cout_diffusion`
- `cout_fixe_reparti`
- `cout_reprise`
- `cout_revue_legale`

Exemples:

| Date | Sujet ID | Dossier ID | Type de cout | Ressource | Quantite | Unite | Cout unitaire | Cout total | Budget associe | Responsable | Justification |
|---|---|---|---|---|---:|---|---:|---:|---|---|---|
| 2026-04-25 | S-001 | D-014 | outil_llm | anthropic | 180000 | tokens | 0.000002 | 0.36 | verification publique | analyste | extraction initiale |
| 2026-04-25 | S-001 | D-014 | temps_verification | analyste senior | 2.5 | heure | 65 | 162.50 | verification publique | redacteur | verification croisee |
| 2026-04-25 | S-001 | D-014 | temps_redaction | redacteur | 1.5 | heure | 55 | 82.50 | verification publique | redacteur | chronique finale |

---

## 8) Formules de pilotage

### Cout direct d'un dossier

`cout_direct_dossier = couts_outils + couts_humains + couts_diffusion + couts_risque`

### Cout complet d'un dossier

`cout_complet_dossier = cout_direct_dossier + quote_part_couts_fixes`

### Marge par dossier

`marge_dossier = revenus_associes_dossier - cout_complet_dossier`

### Cout par livrable

`cout_par_livrable = cout_complet_dossier / nombre_de_livrables_associes`

### Cout par sujet resolu

`cout_par_sujet_resolu = cout_total_periode / nombre_de_sujets_resolus`

### Efficacite signal / bruit

`ratio_signal = nombre_dossiers_utiles / nombre_items_tries`

---

## 9) Valeur economique et valeur strategique

MESANGE ne doit pas mesurer uniquement les revenus encaisses.

Il faut distinguer:

### Valeur economique directe

Exemples:

- abonnement;
- vente de note;
- mandat;
- formation;
- licence;
- sponsorship;
- subvention affectee.

### Valeur strategique indirecte

Exemples:

- notoriete;
- preuve de rigueur;
- acquisition d'abonnes;
- ouverture de nouveaux mandats;
- renforcement doctrinal;
- constitution d'un corpus proprietaire;
- reduction du temps futur de traitement sur le sujet.

Doctrine:

`Un sujet peut etre maintenu a perte a court terme seulement si sa valeur strategique est explicite, tracee et revue periodiquement.`

---

## 10) KPI recommandes

### KPI de cout

- cout par dossier ouvert
- cout par dossier resolu
- cout par chronique publiee
- cout par analyse validee
- cout par source active
- cout moyen de verification d'une affirmation

### KPI de performance

- temps moyen du signal a la publication
- temps moyen du signal a la resolution
- taux de dossiers reouverts
- taux de claims encore non verifies
- ratio bruit / signal

### KPI economiques

- revenu par dossier
- revenu par client
- revenu par axe
- marge brute par dossier
- marge nette par axe
- cout d'acquisition d'un abonne ou client

### KPI de valeur strategique

- nombre de sujets de reference maintenus a jour
- nombre de chronologies reutilisees
- nombre de citations / reutilisations
- croissance du corpus exploitable

---

## 11) Modeles de revenus possibles

Je recommande de ne pas dependre d'un seul canal.

### Modele 1 - Abonnement premium

Ce qui se vend:

- dossiers suivis;
- chronologies;
- fiches de verification;
- briefings;
- syntheses reservees.

Cible:

- citoyens engages;
- journalistes;
- chercheurs;
- cabinets;
- OBNL;
- syndicats.

### Modele 2 - Mandats d'analyse

Ce qui se vend:

- cartographie d'acteurs;
- analyse de discours;
- verification publique;
- veille thematique;
- note de synthese;
- scenarios de resolution.

### Modele 3 - Observatoires thematiques

Ce qui se vend:

- observatoire finance sur un enjeu;
- publication periodique;
- maintenance d'un corpus de reference.

Condition:

- independance methodologique explicite.

### Modele 4 - Formations et methodes

Ce qui se vend:

- atelier de verification;
- lecture critique des discours;
- utilisation responsable de l'IA;
- gestion des dossiers et preuves.

### Modele 5 - Outil / SaaS

Ce qui se vend:

- gestion des sources;
- file de tri;
- dossiers;
- claims;
- historique;
- tableaux de couts et budgets.

### Modele 6 - Subventions / recherche / partenariats

Ce qui se finance:

- observatoire citoyen;
- infrastructure civique;
- methodes de transparence;
- production documentaire.

---

## 12) Recommandation de rentabilisation

Je recommande un mix en trois couches.

### Couche A - Base recurrente

- abonnement premium
- soutien recurrent
- observatoire finance

Role:

- absorber une partie des couts fixes.

### Couche B - Revenus a forte marge

- mandats d'analyse
- formation
- notes strategiques

Role:

- financer les sujets lourds.

### Couche C - Capitalisation long terme

- corpus proprietaire
- chronologies
- dossiers de reference
- outil SaaS

Role:

- transformer le travail editorial en actif reutilisable.

---

## 13) Interface admin economique recommandee

Je ferais cinq ecrans.

### Ecran 1 - Budgets

Fonctions:

- creer budget global;
- creer budget par axe;
- creer budget par dossier;
- fixer plafond et seuil d'alerte;
- suivre le consomme.

### Ecran 2 - Couts

Fonctions:

- journal des frais;
- imports automatiques des couts outils;
- saisie temps humain;
- ventilation des couts fixes;
- etiquetage par sujet et dossier.

### Ecran 3 - Revenus

Fonctions:

- abonnements;
- ventes de livrables;
- mandats;
- partenariats;
- subventions;
- rattachement aux sujets ou axes.

### Ecran 4 - Unit economics

Fonctions:

- cout par dossier;
- cout par sujet resolu;
- marge par livrable;
- marge par axe;
- vues mensuelles et trimestrielles.

### Ecran 5 - Alertes

Fonctions:

- budget depasse;
- outil trop couteux;
- dossier trop lourd sans issue;
- sujet maintenu a perte;
- source peu utile mais consommatrice.

---

## 14) Objets de donnees minimaux

MESANGE doit prevoir au minimum:

- `budget`
- `budget_line`
- `cost_entry`
- `revenue_entry`
- `tool_usage`
- `timesheet_entry`
- `dossier`
- `sujet`
- `report`
- `client`
- `value_assessment`
- `resolution`

Champs critiques:

- `period`
- `owner`
- `axe`
- `dossier_id`
- `sujet_id`
- `source_id`
- `type_de_cout`
- `revenu_direct_ou_non`
- `valeur_strategique`
- `statut`

---

## 15) Regles d'arbitrage recommandees

### Regle 1

Un dossier qui depasse son plafond sans clarification de valeur doit etre revu.

### Regle 2

Un sujet sans perspective de resolution, sans audience et sans valeur strategique doit etre archive.

### Regle 3

Une source couteuse et peu utile doit etre degradee ou desactivee.

### Regle 4

Un dossier rentable mais chronophage peut justifier une industrialisation.

### Regle 5

Un sujet structurellement utile mais peu rentable peut etre finance par une couche mutualisee ou un observatoire.

---

## 16) MVP recommande

Pour ne pas surconstruire trop vite, le MVP economique doit faire:

1. budget mensuel global
2. budget par axe
3. cout par dossier
4. saisie temps humain
5. journal des couts outils
6. revenu par client / mandat / abonnement
7. vue marge par dossier
8. alertes de depassement

Ce qui peut attendre:

- comptabilite analytique fine;
- previsionnel automatise complexe;
- amortissement detaille de tous les actifs;
- simulation de cohortes avancee.

---

## 17) Decision operative

A ce stade, MESANGE doit etre pense comme un systeme a trois moteurs:

- moteur de veille et de tri;
- moteur de dossiers et de verification;
- moteur de pilotage economique.

Sans le troisieme moteur, MESANGE risque de produire beaucoup d'analyse sans capacite robuste d'arbitrage, de priorisation et de soutenabilite.

---

## 18) Prochaine etape recommandee

Les livrables suivants doivent logiquement suivre ce document:

1. un tableau de donnees `sources / dossiers / claims / budgets / couts / revenus`
2. une spec d'ecrans admin economiques
3. une premiere grille de budgets mensuels MESANGE
4. une simulation simple de trois modeles de rentabilisation


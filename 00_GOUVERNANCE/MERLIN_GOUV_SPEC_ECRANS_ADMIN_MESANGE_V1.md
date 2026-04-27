# MERLIN - Spec ecrans admin MESANGE V1

Date: 2026-04-25
Statut: draft
Objet: definir les ecrans admin V1 de MESANGE, leurs roles, les donnees lues/ecrites, les validations, les transitions et les acces

---

## 1) Role de cette spec

Cette spec transforme en interfaces codables:

- le tableau de donnees MESANGE;
- le cadre economique;
- la logique de dossiers;
- les claims;
- les sources;
- les publications;
- le pilotage des budgets et couts.

Elle couvre le noyau admin V1:

- gestion des sources;
- file de tri;
- gestion des claims et evidences;
- gestion des dossiers;
- production de livrables;
- pilotage economique;
- administration des concepts et cadres d'analyse.

Elle ne couvre pas encore:

- le portail client externe;
- la licence multi-organisations complexe;
- les permissions granulaires tres fines par organisation;
- la gestion avancee des abonnements grand public;
- les interfaces mobiles natives.

---

## 2) Principes UX et produit V1

### Principe 1 - Le bruit entre, la structure sort

L'admin doit aider a:

- absorber le flux;
- filtrer;
- qualifier;
- classer;
- suivre.

### Principe 2 - Une information n'est pas encore un dossier

L'interface doit empecher:

- l'empilement non traite;
- la confusion entre item ingere et sujet suivi;
- la creation anarchique de dossiers.

### Principe 3 - Le claim est une unite de travail

L'interface doit rendre visible:

- ce qui est affirme;
- ce qui est prouve;
- ce qui reste incertain;
- ce qui change dans le temps.

### Principe 4 - Le dossier est la memoire vivante

Le dossier doit montrer:

- le resume courant;
- la chronologie;
- les claims;
- les acteurs;
- les actions;
- les livrables;
- la situation economique.

### Principe 5 - L'economie n'est pas une couche a part

Chaque sujet lourd doit pouvoir etre relie a:

- un budget;
- des couts;
- des revenus;
- une valeur strategique.

---

## 3) Roles d'acces V1

### `admin_mesange`

Accede a:

- tous les ecrans admin;
- les parametres;
- les sources;
- les dossiers;
- les claims;
- les budgets;
- les revenus;
- les publications.

### `analyste`

Accede a:

- file de tri;
- sources;
- claims;
- dossiers;
- livrables;
- vue budget/cout lecture et ecriture limitee.

### `editeur`

Accede a:

- dossiers;
- livrables;
- validation editoriale;
- chronologies;
- publications.

### `gestionnaire_economie`

Accede a:

- budgets;
- couts;
- revenus;
- tableaux de marge;
- alertes economiques.

### `lecteur_interne`

Accede a:

- lecture des dossiers et rapports;
- pas d'ecriture structurelle.

---

## 4) Cartographie des ecrans admin V1

### Pilotage general

1. `ADM-001` Tableau de bord admin

### Sources et ingestion

2. `ADM-101` Catalogue des sources
3. `ADM-102` Fiche source
4. `ADM-103` File des items ingeres
5. `ADM-104` Fiche item ingere

### Analyse et verification

6. `ADM-201` File des claims
7. `ADM-202` Fiche claim
8. `ADM-203` Fiche evidence
9. `ADM-204` Cartographie des acteurs

### Dossiers et suivi

10. `ADM-301` Liste des dossiers
11. `ADM-302` Fiche dossier
12. `ADM-303` Chronologie dossier
13. `ADM-304` Vue resolutions et reouvertures

### Livrables et publication

14. `ADM-401` Liste des rapports
15. `ADM-402` Editeur de rapport
16. `ADM-403` File de validation editoriale

### Economie et pilotage

17. `ADM-501` Tableau budgets
18. `ADM-502` Journal des couts
19. `ADM-503` Journal des revenus
20. `ADM-504` Unit economics / marge

### Parametrage

21. `ADM-601` Concepts et taxonomies
22. `ADM-602` Cadres d'analyse et options
23. `ADM-603` Parametres MESANGE / positions / principes

---

## 5) Specs ecran par ecran

## ADM-001 - Tableau de bord admin

### Role

Vue de pilotage globale.

### Utilisateur

- `admin_mesange`
- `analyste`
- `gestionnaire_economie`

### Objectif

- voir l'etat general du systeme;
- voir les volumes entrants;
- voir les dossiers critiques;
- voir les alertes economiques;
- orienter le travail du jour.

### Donnees lues

- `source_item`
- `claim`
- `dossier`
- `report`
- `budget`
- `cost_entry`
- `revenue_entry`

### Widgets minimum

- items ingeres non tries
- claims en attente
- dossiers critiques
- dossiers sans activite recente
- rapports a valider
- budgets en alerte
- couts du mois
- revenus du mois

### Actions

- aller vers `ADM-103`
- aller vers `ADM-201`
- aller vers `ADM-301`
- aller vers `ADM-501`

---

## ADM-101 - Catalogue des sources

### Role

Lister les sources suivies.

### Objectif

- activer;
- desactiver;
- prioriser;
- verifier la fiabilite;
- voir les couts associes.

### Donnees lues

- `source`
- agrégats `source_item`
- agrégats `cost_entry`

### Colonnes minimum

- nom
- type
- statut
- priorite
- frequence
- niveau de confiance
- proprietaire
- dernier item
- cout estime / periode

### Actions

- creer source
- ouvrir `ADM-102`
- pause / reprise
- test ingestion

---

## ADM-102 - Fiche source

### Role

Configurer une source.

### Donnees lues/ecrites

- `source`

### Champs minimum

- `name`
- `source_type_code`
- `source_url`
- `source_status`
- `default_priority_level`
- `trust_level_code`
- `refresh_frequency_code`
- `cost_profile_code`
- `owner_user_id`

### Zones utiles

- configuration
- historique d'ingestion
- derniers items
- sujets associes
- cout estime

### Validations

- URL obligatoire si source web
- type obligatoire
- statut explicite

---

## ADM-103 - File des items ingeres

### Role

Zone anti-brouhaha principale.

### Objectif

- trier les nouveaux items;
- ignorer le bruit;
- creer des claims;
- rattacher a un dossier;
- ouvrir un nouveau dossier.

### Donnees lues

- `source_item`
- `document`
- `source`

### Filtres minimum

- non tries
- priorite
- source
- type
- date
- langue
- deja rattaches / non rattaches

### Actions principales

- ignorer
- marquer a revoir
- ouvrir `ADM-104`
- creer claim
- rattacher a dossier
- creer dossier

### Regle UX

- traitement rapide au clavier si possible
- apercu court sans ouvrir chaque item

---

## ADM-104 - Fiche item ingere

### Role

Examiner un item en detail.

### Donnees lues/ecrites

- `source_item`
- `document`

### Sections

- metadonnees source
- texte brut / normalise
- suggestions IA
- concepts detectes
- claims proposes
- rattachements possibles

### Actions

- valider / rejeter l'item
- creer un ou plusieurs `claim`
- rattacher a un `topic`
- rattacher a un `dossier`

---

## ADM-201 - File des claims

### Role

Lister les affirmations a verifier ou deja qualifiees.

### Donnees lues

- `claim`
- `actor`
- `topic`
- `dossier`

### Colonnes minimum

- label court
- acteur
- type
- statut de verification
- niveau de confiance
- dernier examen
- dossier rattache

### Filtres minimum

- `non_verifie`
- `en_attente_de_reponse`
- `trompeur`
- `contredit_par_les_faits`
- acteur
- sujet
- date

### Actions

- ouvrir `ADM-202`
- changer le statut
- demander plus d'evidence
- rattacher a dossier

---

## ADM-202 - Fiche claim

### Role

Unite centrale de verification.

### Donnees lues/ecrites

- `claim`
- `evidence`
- `actor`
- `source_item`
- `document`

### Sections minimum

- texte exact du claim
- reformulation courte
- source d'origine
- acteur concerne
- statut de verification
- evidences pour
- evidences contre
- note methodologique
- historique des revisions

### Actions

- ajouter evidence
- changer statut
- rattacher a dossier
- generer fiche de verification

### Validations

- tout changement de statut sensible doit laisser une note

---

## ADM-203 - Fiche evidence

### Role

Gerer une piece probante ou contradictoire.

### Donnees lues/ecrites

- `evidence`

### Champs minimum

- type
- resume
- force
- soutient / contredit / nuance
- source rattachee
- note de review

### Actions

- lier a un claim
- degrader / renforcer
- marquer comme obsolete

---

## ADM-204 - Cartographie des acteurs

### Role

Voir et gerer les acteurs suivis.

### Donnees lues/ecrites

- `actor`
- `position`
- agrégats `claim`
- agrégats `dossier`

### Colonnes minimum

- nom
- type
- territoire
- nombre de claims
- nombre de dossiers lies
- derniere activite

### Actions

- ouvrir acteur
- voir positions
- voir claims lies

---

## ADM-301 - Liste des dossiers

### Role

Lister les sujets suivis.

### Donnees lues

- `dossier`
- `topic`
- agrégats `claim`
- agrégats `report`
- agrégats `cost_entry`

### Colonnes minimum

- code
- titre
- sujet
- statut
- priorite
- responsable
- derniere activite
- claims ouverts
- cout cumule

### Filtres minimum

- statut
- priorite
- responsable
- sujet
- avec / sans rapport publie
- avec / sans budget

### Actions

- creer dossier
- ouvrir `ADM-302`

---

## ADM-302 - Fiche dossier

### Role

Ecran coeur MESANGE.

### Donnees lues/ecrites

- `dossier`
- `dossier_event`
- `claim`
- `actor`
- `report`
- `budget`
- `cost_entry`
- `revenue_entry`

### Onglets minimum

- resume courant
- claims
- chronologie
- acteurs
- livrables
- budget / cout / revenu
- resolution

### Champs minimum

- titre
- resume courant
- statut
- priorite
- responsable
- impact citoyen
- questions ouvertes
- valeur strategique

### Actions

- changer statut
- ajouter event
- ajouter claim
- produire rapport
- enregistrer resolution
- reouvrir

### Regle UX

- tout doit rester lisible sans quitter l'ecran trop souvent

---

## ADM-303 - Chronologie dossier

### Role

Vue timeline.

### Donnees lues

- `dossier_event`
- claims dates
- publications
- reponses recues

### Objectif

- reprendre un sujet du debut a la fin;
- voir les trous;
- preparer chronologie publique.

### Actions

- ajouter evenement
- reordonner si erreur de date
- exporter vers rapport

---

## ADM-304 - Vue resolutions et reouvertures

### Role

Suivre les dossiers clos, resolus ou rouvrables.

### Donnees lues

- `dossier`
- `dossier_event`

### Colonnes minimum

- titre
- date de resolution
- type de resolution
- date de reouverture si applicable
- raison

---

## ADM-401 - Liste des rapports

### Role

Lister tous les livrables.

### Donnees lues

- `report`
- `dossier`
- `topic`

### Colonnes minimum

- titre
- type
- audience
- statut publication
- dossier
- date
- validateur

### Actions

- ouvrir `ADM-402`
- dupliquer
- archiver

---

## ADM-402 - Editeur de rapport

### Role

Produire une fiche, une chronique ou une synthese.

### Donnees lues/ecrites

- `report`
- `dossier`
- `claim`
- `evidence`

### Zones minimum

- metadonnees
- resume
- corps du texte
- sources principales
- niveau de confiance
- angle editorial

### Actions

- enregistrer brouillon
- envoyer en validation
- publier

### Validations

- type de rapport obligatoire
- audience obligatoire
- rattachement a dossier ou sujet recommande

---

## ADM-403 - File de validation editoriale

### Role

Valider ou rejeter les sorties.

### Donnees lues

- `report`

### Colonnes minimum

- titre
- type
- auteur
- statut
- audience
- date de soumission

### Actions

- valider
- rejeter
- demander corrections

---

## ADM-501 - Tableau budgets

### Role

Piloter les enveloppes.

### Donnees lues/ecrites

- `budget`

### Colonnes minimum

- libelle
- scope
- periode
- budget
- seuil d'alerte
- plafond
- consomme
- ecart

### Actions

- creer budget
- rattacher a sujet / dossier / outil
- fermer budget

---

## ADM-502 - Journal des couts

### Role

Tracer tous les couts.

### Donnees lues/ecrites

- `cost_entry`

### Colonnes minimum

- date
- type de cout
- sujet
- dossier
- ressource / outil
- total
- budget associe

### Actions

- ajouter cout
- corriger
- exporter

---

## ADM-503 - Journal des revenus

### Role

Tracer revenus et financements.

### Donnees lues/ecrites

- `revenue_entry`

### Colonnes minimum

- date
- type de revenu
- client / partenaire
- sujet ou dossier
- montant
- notes

### Actions

- ajouter revenu
- rattacher a dossier
- exporter

---

## ADM-504 - Unit economics / marge

### Role

Voir si le travail se soutient.

### Donnees lues

- `cost_entry`
- `revenue_entry`
- `budget`
- `dossier`
- `report`

### Vues minimum

- marge par dossier
- marge par sujet
- cout par rapport
- cout par claim verifie
- cout par dossier resolu

### Alertes minimum

- dossier hors budget
- sujet couteux sans sortie
- source couteuse peu utile

---

## ADM-601 - Concepts et taxonomies

### Role

Administrer la grille analytique.

### Donnees lues/ecrites

- `concept`

### Groupes minimum

- enjeux
- signaux
- techniques discursives
- sophismes
- principes MESANGE
- categories de couts

### Actions

- creer
- modifier
- versionner
- desactiver

---

## ADM-602 - Cadres d'analyse et options

### Role

Configurer les moteurs d'analyse.

### Donnees lues/ecrites

- parametres applicatifs
- prompts
- seuils
- regles de tri

### Sections minimum

- cadres d'analyse
- options par domaine
- seuils de priorite
- regles d'ouverture automatique de dossier
- modes de scoring

---

## ADM-603 - Parametres MESANGE / positions / principes

### Role

Rendre explicite la doctrine.

### Donnees lues/ecrites

- principes
- positions
- notes doctrinales

### Objectif

- rendre visible le point de vue explicite;
- separer cadre d'analyse et faits;
- documenter les lignes rouges et les criteres de resolution.

---

## 6) Priorite V1

### Ecrans obligatoires V1

- `ADM-001`
- `ADM-101`
- `ADM-103`
- `ADM-201`
- `ADM-202`
- `ADM-301`
- `ADM-302`
- `ADM-401`
- `ADM-402`
- `ADM-501`
- `ADM-502`
- `ADM-503`
- `ADM-601`

### Ecrans souhaitables V1.1

- `ADM-204`
- `ADM-303`
- `ADM-304`
- `ADM-403`
- `ADM-504`
- `ADM-602`
- `ADM-603`

---

## 7) Decision operative

L'interface admin MESANGE doit etre construite autour de quatre flux principaux:

1. `ingestion -> tri`
2. `claim -> evidence -> verification`
3. `dossier -> chronologie -> publication -> resolution`
4. `budget -> cout -> revenu -> arbitrage`

Si l'interface n'aide pas clairement ces quatre flux, elle ne servira pas assez la mission.

---

## 8) Prochaine etape recommandee

Apres cette spec, les deux livrables les plus utiles sont:

1. un workflow canonique `source -> claim -> dossier -> publication -> resolution`
2. une grille commerciale courte pour pitcher les trois premieres offres MESANGE


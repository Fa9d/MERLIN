# IVIA / MERLIN - Plan de temporalite des processus et mise en place du projet complet

Date : 2026-05-11  
Statut : document de presentation institutionnelle et financiere  
Portee : gouvernements, ordres professionnels, partenaires de financement, investisseurs  
Confidentialite : diffusion controlee - version de travail

## 1. Objet du document

Ce document presente la temporalite de mise en place du projet IVIA / MERLIN, les processus critiques a stabiliser, les jalons de validation, ainsi que la logique de presentation aux differentes instances : gouvernements, ordres professionnels, organismes de financement, partenaires strategiques et investisseurs.

L'objectif n'est pas de presenter MERLIN comme un produit termine. L'objectif est de montrer une trajectoire maitrisee : partir d'un socle executable, encadrer les premiers entretiens pilotes, mesurer les resultats, renforcer la conformite, puis deployer progressivement une plateforme d'accompagnement numerique gouvernee.

## 2. These centrale

IVIA porte une infrastructure d'autonomie individuelle et collective. MERLIN en est le noyau operationnel : une plateforme permettant de structurer des entretiens, generer des notes, soutenir les praticiens, tracer les decisions, evaluer les sorties d'IA et encadrer les cas sensibles par validation humaine.

Le projet repose sur un principe simple : toute capacite importante doit etre associee a un processus verifiable.

```text
capacite -> contrat -> test -> validation humaine -> trace -> amelioration
```

Cette logique est essentielle pour convaincre les instances publiques, les ordres, les financeurs et les investisseurs : IVIA ne propose pas seulement une innovation technologique, mais une methode de deploiement prudente, auditable et progressive.

## 3. Etat actuel du socle executable

Un premier socle local a ete mis en place dans le depot canonique `C:\MERLIN`.

Commandes de validation disponibles :

```powershell
make validate-managed-agents
make telescope-minimal
make telescope-note-e2e
```

Ces commandes permettent de verifier :

- la coherence des agents, outils, workflows et registres YAML ;
- le fonctionnement minimal de Telescope sur donnees factices ;
- un premier benchmark MERLIN-NOTE-E2E-001 sur notes de session ;
- la presence de cas positifs et d'un controle negatif attendu en echec.

Ce socle ne remplace pas une certification, une homologation ou une validation juridique. Il constitue un premier niveau de preuve technique : le systeme peut etre teste, rejoue et ameliore.

## 4. Temporalite generale du projet

La mise en place complete doit etre pensee en six horizons.

### Horizon 0 - Stabilisation interne immediate : 0 a 2 semaines

Objectif : rendre le projet operable en interne.

Livrables prioritaires :

- depot canonique confirme ;
- commandes de validation reproductibles ;
- workflow minimal de note de session ;
- runbook d'entretien pilote ;
- schema de note de session ;
- protocole de consentement pilote ;
- dossier confidentiel sur la propriete intellectuelle et la brevetabilite potentielle ;
- registre des risques ouverts.

Critere de sortie :

```text
L'equipe peut simuler un entretien, produire une note, lancer les validations, faire une revue humaine et consigner la decision.
```

### Horizon 1 - Pilote interne controle : 2 a 6 semaines

Objectif : tester le processus sans exposition publique large.

Actions :

- realiser 3 a 5 entretiens fictifs ou internes ;
- produire des notes de session structurees ;
- evaluer les notes avec Telescope ;
- documenter les erreurs, blocages et ambiguities ;
- transformer chaque erreur importante en cas de test ;
- valider les frontieres : pas de diagnostic, pas de promesse, pas de livraison automatique sans revue humaine.

Critere de sortie :

```text
Le processus tient sur des cas realistes et les limites sont connues.
```

### Horizon 2 - Premiers entretiens pilotes limites : 6 a 12 semaines

Objectif : commencer des entretiens reels avec garde-fous explicites.

Conditions prealables :

- consentement pilote clair ;
- praticien ou responsable humain identifie ;
- protocole d'escalade prioritaire ;
- conservation des donnees definie ;
- validation humaine obligatoire avant tout usage client ;
- journalisation des decisions ;
- mecanisme de retrait ou correction.

Perimetre recommande :

- 1 a 3 praticiens ou accompagnateurs pilotes ;
- 5 a 15 entretiens pilotes ;
- usage exploratoire et encadre ;
- aucune pretention clinique non autorisee ;
- rapport de bilan apres chaque cycle court.

Critere de sortie :

```text
Le projet demontre qu'il peut accompagner un entretien, produire une note utile, detecter les cas sensibles et soutenir la revue humaine.
```

### Horizon 3 - Pre-deploiement institutionnel : 3 a 6 mois

Objectif : passer d'un pilote artisanal a un dispositif presentable aux institutions.

Livrables :

- rapport pilote ;
- grille de risques et mitigations ;
- politique de donnees et consentements ;
- documentation des roles et responsabilites ;
- tableau de bord minimal ;
- protocole de supervision ;
- modele economique revise ;
- fiche invention / propriete intellectuelle ;
- premiere data room financeurs.

Critere de sortie :

```text
Une instance externe peut comprendre ce qui est fait, ce qui n'est pas fait, comment les risques sont controles et quels resultats sont mesures.
```

### Horizon 4 - Demonstrateur finance et partenarial : 6 a 12 mois

Objectif : convertir le pilote en preuve de valeur.

Actions :

- stabiliser un demonstrateur produit ;
- suivre des indicateurs : temps gagne, qualite percue, taux de notes validees, incidents, cout IA par session ;
- produire une documentation financeur ;
- engager discussions avec partenaires publics, parapublics, ordres ou associations ;
- formaliser la strategie de protection : brevet, secret industriel, droit d'auteur, marque, donnees.

Critere de sortie :

```text
IVIA peut soutenir une demande de financement ou une levee avec preuves, risques identifies et trajectoire de deploiement.
```

### Horizon 5 - Deploiement progressif : 12 a 36 mois

Objectif : passer a une exploitation gouvernee.

Axes :

- integration produit plus robuste ;
- securite et conformite renforcees ;
- gouvernance des donnees ;
- support praticiens ;
- mesure d'impact ;
- Telescope enrichi par cas reels anonymises ou synthetiques ;
- partenariats institutionnels ;
- modeles de revenus recurrents ;
- extension prudente vers MESANGE et les usages collectifs.

Critere de sortie :

```text
MERLIN devient une plateforme exploitable, auditable et finançable, avec une boucle d'amelioration continue.
```

## 5. Les processus a mettre en place

### 5.1 Processus entretien pilote

```text
preparation -> consentement -> entretien -> brouillon de note -> evaluation Telescope -> revue humaine -> validation / correction / rejet -> trace
```

Points de controle :

- consentement obtenu avant traitement ;
- finalite expliquee ;
- limites annoncees ;
- vigilance detectee ;
- aucune livraison automatique ;
- validation humaine documentee.

### 5.2 Processus note de session

La note doit separer les audiences :

- contenu client ;
- notes supervision ;
- notes recherche ou amelioration ;
- decision praticien ;
- score d'evaluation ;
- raisons du score ;
- version du prompt ;
- modele utilise ;
- statut de validation.

Cette separation est centrale pour la confiance, la conformite et la possible protection du procede.

### 5.3 Processus Telescope

```text
sortie candidate -> evaluation -> controles positifs -> controles negatifs -> decision -> ajout des echecs au benchmark
```

Role : eviter que l'IA soit evaluee seulement a l'impression. Telescope transforme les erreurs en cas de test et permet de verifier que les corrections ne creent pas de regression.

### 5.4 Processus donnees et conformite

A formaliser avant les entretiens reels :

- finalites de collecte ;
- consentement ;
- retention ;
- acces ;
- suppression ;
- anonymisation ou pseudonymisation ;
- journalisation ;
- gestion des incidents ;
- separation MERLIN / MESANGE.

### 5.5 Processus propriete intellectuelle

A traiter avant toute diffusion large :

- fiche invention ;
- journal de preuves datees ;
- identification des elements confidentiels ;
- choix brevet vs secret industriel ;
- verification d'anteriorites ;
- consultation brevetiste ;
- strategie de divulgation.

## 6. Lecture par instance

### 6.1 Gouvernements et organismes publics

Message principal : IVIA propose un cadre prudent pour renforcer l'autonomie, soutenir les praticiens et documenter les pratiques, sans remplacer les humains ni contourner les institutions.

Ce qu'il faut montrer :

- impact social potentiel ;
- prudence des deploiements ;
- conformite donnees ;
- contribution a la prevention et a l'accompagnement ;
- capacite de mesure ;
- partenariats possibles ;
- respect des cadres publics.

Documents a presenter :

- resume executif ;
- plan pilote ;
- protocole de consentement ;
- tableau risques / mitigations ;
- indicateurs d'impact ;
- calendrier 12 mois.

### 6.2 Ordres professionnels et instances de pratique

Message principal : MERLIN est un outil d'assistance, de structuration et de traçabilite. Il ne remplace pas le jugement professionnel.

Ce qu'il faut montrer :

- validation humaine obligatoire ;
- limites claires ;
- protocole d'escalade ;
- absence de diagnostic automatique ;
- separation client / supervision / recherche ;
- auditabilite des notes ;
- capacite de correction.

Documents a presenter :

- runbook entretien pilote ;
- schema de note de session ;
- protocole urgence / detresse ;
- politique de consentement ;
- exemples anonymises ou synthetiques ;
- grille Telescope de controle negatif.

### 6.3 Organismes de financement et subventions

Message principal : IVIA est un projet d'innovation sociale et technologique avec trajectoire progressive, resultats mesurables et potentiel de transfert.

Ce qu'il faut montrer :

- besoin social ;
- solution experimentale ;
- equipe et partenaires ;
- jalons clairs ;
- budget par phase ;
- indicateurs ;
- retombees Quebec / Canada ;
- gouvernance des risques.

Documents a presenter :

- plan 12 mois ;
- budget pilote ;
- livrables par trimestre ;
- indicateurs d'impact ;
- lettres d'interet ;
- strategie de perennisation.

### 6.4 Investisseurs

Message principal : IVIA construit une infrastructure agentique gouvernee pour un marche ou la confiance, la conformite et la productivite des praticiens deviennent decisives.

Ce qu'il faut montrer :

- probleme marche ;
- produit initial MERLIN ;
- avantage defensible ;
- traction pilote ;
- modeles de revenus ;
- couts IA maitrises ;
- proprietes intellectuelles potentielles ;
- risques et mitigations ;
- plan de deploiement ;
- equipe et besoins de financement.

Documents a presenter :

- pitch deck ;
- note confidentielle investisseurs ;
- modele financier ;
- data room ;
- demo ;
- rapport pilote ;
- fiche IP confidentielle.

## 7. Jalons decisionnels

### Jalon A - Socle verifie

Condition :

```powershell
make validate-managed-agents
make telescope-minimal
make telescope-note-e2e
```

Decision : autoriser les simulations internes.

### Jalon B - Protocole pilote valide

Condition : runbook, consentement, schema note et protocole d'escalade disponibles.

Decision : autoriser 3 a 5 simulations internes.

### Jalon C - Pilote limite autorise

Condition : simulations internes concluantes, risques ouverts documentes, supervision humaine prete.

Decision : autoriser un petit nombre d'entretiens reels controles.

### Jalon D - Rapport pilote

Condition : premiers entretiens completes, notes validees, incidents documentes, apprentissages integres.

Decision : presenter aux partenaires, financeurs ou instances.

### Jalon E - Demonstrateur finance

Condition : indicateurs stabilises, budget clair, data room disponible, strategie IP initiale.

Decision : ouvrir discussions financement / investissement.

## 8. Indicateurs a suivre

Indicateurs operationnels :

- nombre d'entretiens ;
- nombre de notes produites ;
- nombre de notes validees ;
- taux de rejet ;
- taux d'escalade ;
- temps moyen de production ;
- temps gagne praticien ;
- incidents ;
- corrections humaines ;
- cout IA par session.

Indicateurs qualite :

- score Telescope ;
- cas negatifs detectes ;
- erreurs recurrentes ;
- clarte des notes ;
- utilite praticien ;
- satisfaction pilote ;
- conformite consentement.

Indicateurs financiers :

- cout par entretien ;
- prix cible ;
- marge brute estimee ;
- MRR potentiel ;
- cout acquisition ;
- runway ;
- besoins de financement par phase.

Indicateurs institutionnels :

- partenaires approches ;
- lettres d'interet ;
- retours d'ordres ou experts ;
- exigences de conformite ;
- opportunites de subventions ;
- risques reputations.

## 9. Risques principaux et mitigations

| Risque | Impact | Mitigation |
| --- | --- | --- |
| Confusion entre assistance et diagnostic | Eleve | Langage prudent, revue humaine, protocole ordre professionnel |
| Donnees sensibles mal gouvernees | Eleve | Consentement, retention, acces, journalisation, separation des usages |
| IA trop autonome trop tot | Eleve | Human-in-the-loop obligatoire, Telescope, cas negatifs |
| Promesse publique excessive | Eleve | Positionnement complementaire, pilote limite, preuves progressives |
| Divulgation prematuree du procede | Moyen a eleve | Fiche invention confidentielle, brevetiste, NDA si necessaire |
| Dispersion documentaire | Moyen | Index, runbooks courts, commandes executables |
| Cout IA non maitrise | Moyen | Mesure par session, optimisation, limites de contexte |
| Manque de traction | Moyen | Pilotes courts, indicateurs, cas d'usage praticiens prioritaires |

## 10. Positionnement recommande par public

### Formulation publique prudente

IVIA developpe une infrastructure numerique gouvernee pour soutenir l'autonomie, la structuration des entretiens et la qualite des suivis, avec validation humaine et traçabilite des decisions.

### Formulation ordre professionnel

MERLIN est un outil d'aide a la structuration et a la documentation. Il ne pose pas de diagnostic, ne remplace pas le jugement professionnel et impose une revue humaine avant tout usage sensible.

### Formulation financeur public

Le projet vise a tester une approche responsable d'IA appliquee a l'accompagnement, avec indicateurs d'impact, cadre de donnees, protocole pilote et transfert possible vers des partenaires du territoire.

### Formulation investisseur

IVIA construit une plateforme agentique gouvernee pour augmenter la productivite, la qualite et la traçabilite des pratiques d'accompagnement, dans un marche ou la confiance et la conformite sont des avantages competitifs.

## 11. Prochaines pieces a produire

Priorite immediate :

1. `MERLIN_ENTRETIEN_PILOTE_RUNBOOK_v1.0.md`
2. `MERLIN_NOTE_SESSION_SCHEMA_v1.0.md`
3. `MERLIN_CONSENTEMENT_PILOTE_v1.0.md`
4. `IVIA_FICHE_INVENTION_PROCESS_MERLIN_TELESCOPE_v0.1.md`
5. `IVIA_RUNBOOK_VALIDATION_AVANT_ENTRETIEN_v1.0.md`
6. `IVIA_DATA_ROOM_INDEX_FINANCEMENT_INVESTISSEURS_v0.1.md`

Ces pieces doivent rester courtes, actionnables et coherentes avec les commandes executables deja en place.

## 12. Conclusion

La strategie recommandee est de ne pas attendre que MERLIN soit complet pour commencer a apprendre. Il faut toutefois refuser de commencer sans processus minimal.

Le chemin propose est donc :

```text
socle executable -> simulations internes -> entretiens pilotes limites -> rapport pilote -> presentation institutionnelle et financiere -> deploiement progressif
```

Cette temporalite permet de servir quatre objectifs en meme temps :

- proteger les personnes accompagnees ;
- proteger les praticiens et l'organisation ;
- produire des preuves utiles pour les instances ;
- construire une valeur defensible pour les financeurs et investisseurs.

MERLIN ne sera pas termine par accumulation documentaire. Il sera termine par stabilisation progressive de processus verifiables.

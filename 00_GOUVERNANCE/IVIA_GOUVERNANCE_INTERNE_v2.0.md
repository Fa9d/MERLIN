# GOUVERNANCE INTERNE IVIA
## Modèle de gouvernance opérationnel — IVIA inc. (SPA-mère à mission) + IVIA OBNL (satellite)

**Version** : 2.0 — Refonte post-DÉC-V3-15 (architecture SPA-mère + OBNL satellite)
**Date** : 8 mai 2026
**Statut** : Document structurel — Opposable à toutes les instances et personnes nommées
**Auteur** : David Phaneuf (fondateur) + Perplexity Computer
**Loi de référence** : *Loi sur les sociétés par actions du Québec (LSAQ)* pour IVIA inc. (statuts à mission) ; *Loi sur les compagnies du Québec, Partie III (LCQ)* pour IVIA OBNL
**Devises** : *Au sein de l'être — En actes.* + *Pour le peuple, par le peuple.*
**Cohérence** : STRUCTURE_JURIDIQUE_RECOMMANDEE.md v2.0, CHARTE_DOCTRINAIRE_IVIA.md v1.1, CADRE_PROPRIETE_INTELLECTUELLE_DONNEES.md v2.0, HISTORIQUE_DECISIONS_STRATEGIQUES.md (DÉC-V3-15)
**Remplace** : v1.0 (Vague 2, mai 2026), construite sur l'hypothèse OBNL-mère + MERLIN inc. SPA fille

---

## AVERTISSEMENT DE REFONTE

La version 1.0 décrivait une gouvernance dans laquelle le **CA de l'OBNL** détenait un pouvoir de veto contraignant sur la SPA fille (MERLIN inc.). Cette architecture a été renversée par DÉC-V3-15.

L'architecture cible est désormais :
- **IVIA inc.** : société par actions à mission (LSAQ), actionnaire unique David Phaneuf (100 %), maison-mère opérationnelle de l'écosystème (MERLIN, MÉSANGE, projets en bac, futurs)
- **IVIA OBNL** : satellite indépendant (LCQ Partie III), conseil d'administration distinct, lié à IVIA inc. par une convention de licence sociale

La gouvernance de chaque entité est **distincte**. Aucune des deux n'a de pouvoir hiérarchique contraignant sur l'autre — elles sont **liées contractuellement** par la convention de licence et **liées doctrinalement** par l'adoption commune de la Charte doctrinaire IVIA v1.1.

Le **comité doctrinal** est un organe consultatif d'IVIA inc. à compétence trans-écosystème. Il est sans pouvoir de blocage juridique direct sur les décisions de la SPA-mère. Son pouvoir est consultatif, public et réputationnel. Cette limite est assumée et compensée par : statuts à mission LSAQ, transparence radicale, présence d'un membre désigné par le CA OBNL, renforcements progressifs (pacte d'actionnaires, fiducie de mission à 2-3 M$ valorisation).

---

## PRÉAMBULE

### Pourquoi une gouvernance documentée avant le premier palier de constitution

La gouvernance n'est pas une formalité. Elle est la condition de la confiance — entre le fondateur et les praticiennes pilote, entre IVIA et ses utilisateurs, entre IVIA et ses futurs investisseurs et bailleurs. Documenter la gouvernance dès la phase pilote crée un cadre de référence partagé avant l'apparition des premiers conflits d'intérêts, et signale à toutes les parties prenantes que la doctrine IVIA n'est pas un discours marketing mais une architecture de décision.

Le présent document décrit la gouvernance des deux entités (IVIA inc. et IVIA OBNL), des comités consultatifs, et des interfaces entre elles. Il évolue avec l'organisation : certaines instances seront créées dès la constitution juridique (Palier 1, M7-M9 ; Palier 2, M9-M12), d'autres activées progressivement selon les paliers du PLAN_INTEGRATION_IVIA_36MOIS.md.

### Articulation avec les autres documents

- **CHARTE_DOCTRINAIRE_IVIA.md v1.1** — Partie IV (gouvernance doctrinaire), Partie VII v1.1 (statuts protecteurs)
- **STRUCTURE_JURIDIQUE_RECOMMANDEE.md v2.0** — Sections paliers + Section 4 (mécanismes inter-entités)
- **CADRE_PROPRIETE_INTELLECTUELLE_DONNEES.md v2.0** — Partie III (convention de licence sociale)
- **HISTORIQUE_DECISIONS_STRATEGIQUES.md v1.3** — DÉC-V3-15

---

## PARTIE I — VUE D'ENSEMBLE DE L'ARCHITECTURE DE GOUVERNANCE

### I.1 Schéma global

```
┌─────────────────────────────────────────────────────────────────┐
│  Actionnaire unique : David Phaneuf (100 %)                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  IVIA inc. — Société par actions à mission (LSAQ)               │
│  Maison-mère de l'écosystème                                    │
│                                                                 │
│  • Direction exécutive (fondateur DG jusqu'à Palier 4 minimum)  │
│  • Conseil d'administration de la SPA (3-5 membres dès Palier 2)│
│  • Comité consultatif (stratégie, business)                     │
│  • Comité doctrinal (mission, doctrine — trans-écosystème)      │
│  • Comité des praticiens & utilisateurs avancés                 │
│  • Comité éthique consultatif (Palier 3+)                       │
│                                                                 │
│  Produits : MERLIN, MÉSANGE, covoiturage, logistique, NHL, +    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │  Convention de licence sociale
                              │  (marque IVIA + outils + savoir-faire)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  IVIA OBNL — Personne morale satellite (LCQ Partie III)         │
│  Mission : redistribution sociale                               │
│                                                                 │
│  • Conseil d'administration distinct (5-7 membres)              │
│  • Direction générale OBNL (à embaucher Palier 2-3)             │
│  • Comité de programmation                                      │
│  • Comité de financement                                        │
│                                                                 │
│  Programmes : accès gratuit ou à coût réduit pour publics       │
│  vulnérables — utilisant les outils IVIA inc. sous licence      │
└─────────────────────────────────────────────────────────────────┘
```

### I.2 Sept instances de gouvernance

L'écosystème IVIA fonctionne avec sept instances de gouvernance, avec des paliers d'activation distincts :

| # | Instance | Entité | Palier d'activation | Rôle |
|---|---|---|---|---|
| 1 | Direction exécutive d'IVIA inc. | IVIA inc. | Palier 1 (constitution) | Décision opérationnelle quotidienne |
| 2 | Conseil d'administration d'IVIA inc. | IVIA inc. | Palier 1 (administrateur unique) → Palier 2 (3 membres) | Surveillance, matières réservées |
| 3 | Comité doctrinal | IVIA inc. (avec membre OBNL) | Palier 1 partiel → Palier 3 complet | Mission, doctrine, audit annuel |
| 4 | Comité consultatif (stratégie/affaires) | IVIA inc. | Palier 2 | Avis stratégiques, expertise externe |
| 5 | Comité des praticiens et utilisateurs avancés | IVIA inc. (mais voix issue des produits) | Palier 2 (5+ praticiens MERLIN) | Consultation produits |
| 6 | Comité éthique consultatif | IVIA inc. | Palier 3 | Avis éthique externes indépendants |
| 7 | Conseil d'administration d'IVIA OBNL | IVIA OBNL | Palier 2 (constitution OBNL) | Gouvernance autonome de l'OBNL |

---

## PARTIE II — DIRECTION EXÉCUTIVE D'IVIA inc.

### II.1 Mandat du Directeur général

Le fondateur David Phaneuf assume la fonction de Directeur général d'IVIA inc. dès la constitution (Palier 1) et jusqu'au Palier 4 minimum, ou plus tard selon les besoins de l'écosystème.

**Responsabilités** :
- Direction stratégique de l'écosystème (priorisation des produits, allocation des ressources, calendrier)
- Décisions opérationnelles quotidiennes
- Représentation publique d'IVIA
- Relations institutionnelles (investisseurs, bailleurs, partenaires, ordres professionnels, médias)
- Recrutement et gestion de l'équipe
- Reporting au CA d'IVIA inc. selon la fréquence définie en III.5
- Information régulière du CA d'IVIA OBNL sur les éléments touchant la convention de licence sociale

### II.2 Délégations

À mesure de la croissance, le DG délègue des responsabilités à des cadres :
- Directeur produit (à recruter Palier 3, à temps partiel d'abord)
- Directeur technique (CTO — recruté Palier 3-4)
- Directeur des opérations (Palier 4)
- Directeur du développement et des partenariats (Palier 4)

Toute délégation significative est documentée par écrit, notifiée au CA d'IVIA inc., et doit être compatible avec la doctrine.

### II.3 Limites du pouvoir du DG

Le DG **ne peut pas** seul :
- Modifier les statuts à mission d'IVIA inc.
- Engager IVIA inc. dans une opération de cession ou de fusion sans approbation du CA et de l'actionnaire
- Modifier la Charte doctrinaire (procédures de la Partie X du présent document)
- Suspendre, modifier ou résilier la convention de licence sociale envers IVIA OBNL sans avis du Comité doctrinal et du CA d'IVIA inc.
- Engager une dépense ou un endettement excédant le seuil défini en statuts ou en règlements (à arrêter à la constitution, indicatif initial : 50 000 $)

---

## PARTIE III — CONSEIL D'ADMINISTRATION D'IVIA inc.

### III.1 Composition

Au Palier 1, IVIA inc. peut être constituée avec un administrateur unique (le fondateur). Cette configuration minimale est viable juridiquement (LSAQ permet l'administrateur unique) mais elle est inadéquate pour la crédibilité face aux investisseurs et partenaires institutionnels. **Le passage à un CA à 3 membres minimum est prévu dès le Palier 2.**

| Siège | Description | Palier d'activation | Nomination | Durée |
|---|---|---|---|---|
| 1 — Fondateur-DG | David Phaneuf | Palier 1 | De droit (actionnaire unique tant que le capital n'est pas ouvert) | Permanente sauf cession significative |
| 2 — Administrateur indépendant 1 | Expertise stratégique (tech, scaling, finance) | Palier 2 | Nomination par l'actionnaire | 3 ans renouvelable une fois |
| 3 — Administrateur indépendant 2 | Expertise mission (santé, éducation, action sociale, droit) | Palier 2 | Nomination par l'actionnaire après consultation du Comité doctrinal | 3 ans renouvelable une fois |
| 4 (optionnel) — Administrateur investisseur | Représentant du principal investisseur ouvrant le capital | Palier 3-4 (1ère levée significative) | Selon pacte d'actionnaires | Selon pacte |
| 5 (optionnel) — Observateur | Siège sans vote | Palier 4+ | Selon pacte d'actionnaires | Selon pacte |

**Quorum** : majorité des membres en poste. Avec 3 membres : 2. Avec 5 membres : 3.

### III.2 Matières réservées au CA

Le CA d'IVIA inc. est saisi obligatoirement des matières suivantes (les autres relèvent du DG) :

- Approbation des états financiers annuels
- Approbation du budget annuel
- Approbation de la rémunération du fondateur-DG
- Autorisation des transactions hors budget ordinaire excédant le seuil défini
- Approbation des protocoles d'actionnaires lors de toute ouverture du capital
- Décisions de cession partielle ou totale d'actifs significatifs (avec avis du Comité doctrinal pour les actifs liés à la mission)
- Approbation de la convention de licence sociale envers IVIA OBNL et de ses modifications substantielles
- Décisions de filialisation d'un produit
- Adoption ou modification de politiques structurantes (RH, sécurité, données, urgence, qualité)
- Décisions de levée de fonds, d'endettement significatif ou d'émission de nouvelles actions

### III.3 Matières doctrinales — interface avec le Comité doctrinal

Pour les matières touchant la mission, la doctrine, la cession d'actifs liés aux données ou la convention de licence sociale envers l'OBNL, le CA d'IVIA inc. **doit** :

1. Solliciter un avis du Comité doctrinal **avant** de délibérer
2. Délibérer en connaissance de cet avis
3. Si la décision finale du CA s'écarte de l'avis du Comité doctrinal, la justifier explicitement par écrit, et publier l'avis du Comité, la décision et la justification dans le rapport annuel
4. Notifier le conseil d'administration d'IVIA OBNL si la décision affecte la convention de licence

L'avis du Comité doctrinal **n'est pas contraignant juridiquement**. Il est public, opposable réputationnellement et utilisé par le Comité dans son rapport annuel d'audit doctrinal.

### III.4 Réunions

**Fréquence** :
- Réunion ordinaire : minimum 4 fois par an (trimestrielle)
- Réunion extraordinaire : sur convocation du DG, d'un administrateur indépendant ou sur saisine du Comité doctrinal pour matière doctrinale grave

**Convocation** : 10 jours ouvrables minimum avec ordre du jour et documents.
**Mode** : présentiel, vidéoconférence ou mode mixte.
**Procès-verbaux** : rédigés sous 5 jours ouvrables, approuvés à la réunion suivante.

### III.5 Processus décisionnel

| Type de décision | Majorité requise |
|---|---|
| Décisions ordinaires (budget, nominations, PV) | Majorité simple |
| Décisions structurantes (politiques majeures, levées de fonds, modifications statutaires) | Majorité qualifiée (2/3) |
| Décisions touchant la mission ou la doctrine | Majorité qualifiée (2/3) **après avis du Comité doctrinal** |

**Conflit d'intérêts** : tout administrateur ayant un intérêt personnel se déclare, sort de la délibération, ne vote pas (consigné au PV).

---

## PARTIE IV — COMITÉ DOCTRINAL

### IV.1 Statut et nature

Le Comité doctrinal est un organe **consultatif** d'IVIA inc. à **compétence trans-écosystème** : il couvre tous les produits IVIA et la convention de licence sociale envers IVIA OBNL.

Il n'a pas de pouvoir de blocage juridique direct sur les décisions d'IVIA inc. Son pouvoir est :
- **Consultatif** : il émet des avis sur toutes les matières doctrinales
- **Public** : ses avis sont systématiquement publiés
- **Réputationnel** : un écart entre la décision de la direction/du CA et l'avis du Comité est visible publiquement
- **Procédural** : il valide les modifications de la Charte doctrinaire de Niveau 1 et 2 (avec procédures décrites en Partie X)

### IV.2 Composition

| Siège | Description | Palier d'activation | Nomination | Durée |
|---|---|---|---|---|
| 1 — Fondateur | Voix permanente, présidence par défaut | Palier 1 | De droit | Permanente |
| 2 — Praticien ou utilisateur avancé MERLIN | Élu par les praticiens actifs MERLIN | Palier 2 (5+ praticiens) | Élection | 2 ans renouvelable une fois |
| 3 — Praticien ou utilisateur avancé d'un autre produit IVIA | Élu par les utilisateurs actifs du second produit lancé | Palier 3 (lancement second produit) | Élection | 2 ans renouvelable une fois |
| 4 — Représentant des publics servis | Client/usager actif | Palier 2 | Appel de candidatures + cooptation par le Comité | 1 an renouvelable deux fois |
| 5 — Expert externe indépendant | Éthique, droit, domaine pertinent | Palier 1 partiel → Palier 2 confirmé | Cooptation par le fondateur, validation par le CA d'IVIA inc. | 3 ans renouvelable une fois |
| 6 — Représentant d'IVIA OBNL | Membre désigné par le CA d'IVIA OBNL | Palier 2 (constitution OBNL) | Désignation par le CA OBNL | Selon mandat OBNL |

**Note d'attention — Phase pilote** : au Palier 1, seuls les Sièges 1 et 5 sont pourvus. Le Comité fonctionne en formation réduite jusqu'au Palier 2-3.

### IV.3 Mandats

- Interpréter la doctrine en cas de situation non prévue par la Charte
- Traiter les signalements de violation doctrinaire (procédure D.3 de la Charte)
- Valider les modifications de la Charte de Niveau 2 ; émettre un avis consultatif documenté pour les modifications de Niveau 3
- Conduire ou superviser l'audit doctrinal annuel
- Émettre un avis annuel sur la convention de licence sociale IVIA inc. → IVIA OBNL
- Saisir formellement le DG, le CA d'IVIA inc., et le CA d'IVIA OBNL en cas de violation grave (avec publication de la saisine)
- Publier un rapport annuel de ses activités

### IV.4 Réunions

**Fréquence** : minimum 2 fois par an + réunions ad hoc si signalement urgent.
**Quorum** : 3 membres dès que le Comité est complet (4 ou plus, avec au moins le fondateur ou un membre désigné comme président de séance).
**Décisions** : majorité simple pour interprétations courantes ; majorité 2/3 pour validation de modification de Charte de Niveau 2 ; unanimité pour avis sur modification de Niveau 3.

### IV.5 Publication des avis

Tout avis du Comité doctrinal sur une matière soumise par le CA ou le DG est publié dans les 30 jours suivant son adoption, sauf nécessité de confidentialité commerciale strictement justifiée. Le rapport annuel reprend l'ensemble des avis émis dans l'année.

---

## PARTIE V — COMITÉ CONSULTATIF (STRATÉGIE/AFFAIRES)

### V.1 Nature et activation

Le Comité consultatif rassemble des expertises externes pour conseiller la direction et le CA d'IVIA inc. sur des matières stratégiques et d'affaires (technologie, marché, finance, partenariats). Il est distinct du Comité doctrinal — il ne traite **pas** des matières doctrinales.

**Activation** : Palier 2 (recommandé).

### V.2 Composition

3 à 5 membres externes, sans lien d'actionnariat avec IVIA inc., sur invitation du fondateur après consultation du CA. Profils typiques :

- Entrepreneur/dirigeant ayant scalé un SaaS ou une plateforme à impact
- Expert en finance ou en levée de fonds
- Expert sectoriel par produit (santé numérique pour MERLIN, démocratie numérique pour MÉSANGE, etc.)
- Expert en partenariats institutionnels et politique publique

**Indemnisation** : symbolique (frais réels + reconnaissance) ou avec rémunération modeste à arbitrer Palier 3.

### V.3 Mandats

- Avis stratégiques sur la priorisation des produits, les priorités d'investissement, les opportunités de marché
- Mise en relation avec des partenaires, investisseurs, talents
- Validation extérieure de plans d'affaires majeurs avant présentation aux investisseurs
- Identification de risques et opportunités sectorielles

Les avis du Comité consultatif **ne sont pas contraignants** et sont distincts des avis du Comité doctrinal. En cas d'avis contradictoire entre Comité consultatif (logique d'affaires) et Comité doctrinal (logique de mission), c'est le CA d'IVIA inc. qui tranche, sous réserve des statuts à mission.

### V.4 Réunions

Trimestrielles ou semestrielles selon disponibilité. Format léger (2-3 h, en ligne ou hybride).

---

## PARTIE VI — COMITÉ DES PRATICIENS ET UTILISATEURS AVANCÉS

### VI.1 Composition et activation

Le Comité des praticiens et utilisateurs avancés est activé dès que le corps des praticiens actifs MERLIN atteint 5 membres (Palier 2). Il évoluera pour intégrer des représentants des autres produits IVIA à mesure de leur lancement.

| Siège | Description | Nomination | Durée |
|---|---|---|---|
| 3 à 7 sièges élus | Représentants des produits actifs (un siège par produit dépassant 10 utilisateurs avancés) | Élection par pairs (une voix par utilisateur avancé actif) | 1 an renouvelable |
| Facilitateur (non-votant) | Direction d'IVIA inc. (DG ou délégué) | De droit | Permanente |

### VI.2 Mandats

Organe consultatif. Avis non contraignants sauf domaines expressément cités.

**Consultation obligatoire** (la direction doit solliciter l'avis avant décision) :
- Modification des CGU praticiens (article spécifique des CGU à arrêter)
- Modification des tarifs praticiens (abonnements, frais par séance, frais d'inscription annuaire)
- Modification des exigences de formation obligatoire
- Tout changement majeur à l'outillage MERLIN (ou autre produit) affectant le workflow utilisateur

**Consultation facultative mais recommandée** :
- Nouvelles fonctionnalités majeures
- Protocoles de qualité et d'évaluation
- Politique de communication IVIA vers l'externe

### VI.3 Articulation avec le Comité doctrinal

Le Comité des praticiens et utilisateurs avancés élit ses représentants au Comité doctrinal (Sièges 2 et 3 du Comité doctrinal).

### VI.4 Réunions

Trimestrielles minimum + réunions extraordinaires sur demande de 3 membres ou de la direction. Synthèse des avis transmise à la direction sous 10 jours.

---

## PARTIE VII — COMITÉ ÉTHIQUE CONSULTATIF

### VII.1 Composition et activation

Activation : Palier 3 minimum.

3 à 5 experts externes indépendants, sans lien contractuel avec IVIA (ni utilisateurs avancés, ni clients, ni investisseurs, ni employés). Profils :
- Psychologue ou psychothérapeute membre d'un ordre québécois (pertinence MERLIN)
- Juriste spécialisé en droits de la personne, droit numérique ou droit des médias
- Expert en éthique de l'IA ou recherche en sciences sociales
- Expert en démocratie numérique (pertinence MÉSANGE) à mesure de son lancement
- Membre des Premières Nations (sur invitation, selon développement des partenariats)

**Nomination** : par le CA d'IVIA inc. sur recommandation du fondateur et avis du Comité doctrinal.
**Durée** : 3 ans renouvelable une fois.
**Indemnisation** : symbolique (frais réels + reconnaissance formelle).

### VII.2 Mandats

Le Comité éthique consultatif formule des avis publics sur demande du CA d'IVIA inc., du Comité doctrinal ou de la direction.

**Domaines** :
- Éthique de l'accompagnement non clinique (MERLIN)
- Éthique de la communication politique et de la modération (MÉSANGE)
- Conformité aux principes de dignité, autonomie, non-nuisance
- Enjeux éthiques liés à l'IA et aux données émotionnelles ou politiques
- Équité d'accès (accessibilité financière, culturelle, linguistique)
- Relations avec les Premières Nations

**Rapport annuel** public sur ivia.quebec/ethique.

---

## PARTIE VIII — CONSEIL D'ADMINISTRATION D'IVIA OBNL

### VIII.1 Statut

Le CA d'IVIA OBNL est constitué dès le Palier 2 (M9-M12) selon la *Loi sur les compagnies du Québec, Partie III*. Il est **distinct et autonome** par rapport au CA d'IVIA inc. Il dirige l'OBNL conformément à sa mission propre (redistribution sociale) et à la convention de licence sociale conclue avec IVIA inc.

**IVIA OBNL n'est pas filiale d'IVIA inc.** Il y a un lien contractuel et doctrinal, pas un lien capitalistique. Aucun contrôle direct entre les deux entités.

### VIII.2 Composition

| Siège | Description | Nomination | Durée |
|---|---|---|---|
| 1 — Représentant fondateur | David Phaneuf ou son délégué (rôle de continuité doctrinale) | De droit comme fondateur | Permanente sauf décision contraire |
| 2 — Indépendant 1 | Expertise en gouvernance OBNL ou économie sociale | Cooptation par les membres fondateurs de l'OBNL | 3 ans renouvelable |
| 3 — Indépendant 2 | Expertise en services aux publics vulnérables | Cooptation par le CA | 3 ans renouvelable |
| 4 — Indépendant 3 (optionnel) | Expertise en philanthropie ou en financement social | Cooptation par le CA | 3 ans renouvelable |
| 5 — Représentant des bénéficiaires | Personne ayant bénéficié des programmes ou représentant d'organismes communautaires | Cooptation par le CA après appel ouvert | 2 ans renouvelable une fois |
| 6 (optionnel) — Représentant des praticiens et utilisateurs avancés | Élu via le Comité des praticiens et utilisateurs avancés d'IVIA inc. | Élection | 2 ans renouvelable une fois |
| 7 (optionnel) — Membre des Premières Nations | Sur invitation, selon développement des partenariats | Invitation et acceptation mutuelle | 2 ans renouvelable |

**Quorum** : majorité des membres en poste.

**Note** : la composition vise une indépendance suffisante par rapport au fondateur d'IVIA inc. pour que l'OBNL conserve sa crédibilité auprès des bailleurs et de l'ARC (statut de bienfaisance). À partir du Palier 3 (demande de bienfaisance), au moins **3 membres sur 5+** doivent être indépendants du fondateur et d'IVIA inc.

### VIII.3 Mandats

- Définir et veiller à l'exécution de la mission sociale de l'OBNL
- Approuver le budget annuel de l'OBNL
- Approuver les programmes de redistribution
- Veiller à la conformité de l'OBNL avec sa mission, ses obligations légales et la convention de licence sociale envers IVIA inc.
- Désigner un membre au Comité doctrinal d'IVIA inc.
- Émettre un avis annuel public sur la conformité doctrinale d'IVIA inc.
- Décider de la suspension ou de la résiliation de la convention de licence en cas de violation doctrinale grave et non corrigée par IVIA inc.
- Soumettre la demande de statut de bienfaisance ARC au moment opportun (Palier 3, M18-M24)

### VIII.4 Réunions

Minimum 4 fois par an. Procès-verbaux conservés. Sommaires non confidentiels publiés annuellement.

### VIII.5 Direction générale de l'OBNL

Une direction générale dédiée à l'OBNL est à recruter au Palier 2-3 lorsque les programmes prennent une ampleur incompatible avec une gestion bénévole. Profil : expérience OBNL, sensibilité à la mission, autonomie. La rémunération est compatible avec les pratiques du secteur communautaire et financée par les fonds opérationnels (subventions générales, dons non affectés).

---

## PARTIE IX — MATRICE DE DÉCISION

### IX.1 Qui décide quoi (vue consolidée)

| Domaine de décision | Instance décisionnelle | Quorum / Majorité | Consultation préalable obligatoire |
|---|---|---|---|
| Tarification utilisateurs (modifications mineures) | DG IVIA inc. | Décision DG | Comité praticiens (consultation obligatoire si tarifs praticiens) |
| Tarification utilisateurs (modifications majeures, structure tarifaire) | CA IVIA inc. | Majorité simple | Comité praticiens + Comité consultatif |
| Nouvelles offres de service | DG IVIA inc. | Décision DG si dans budget ; CA si > seuil | Comité consultatif |
| Recrutement < seuil défini | DG IVIA inc. | Décision DG | — |
| Recrutement cadre / au-dessus du seuil | CA IVIA inc. | Majorité simple | — |
| Rémunération du DG | CA IVIA inc. | Majorité qualifiée (2/3) avec abstention du DG | — |
| Budget annuel IVIA inc. | CA IVIA inc. | Majorité qualifiée (2/3) | — |
| Lancement d'un nouveau produit | CA IVIA inc. | Majorité qualifiée (2/3) | Comité consultatif + Comité doctrinal |
| Filialisation d'un produit | CA IVIA inc. | Majorité qualifiée (2/3) | Comité consultatif + Comité doctrinal |
| Modification de la convention de licence sociale | CA IVIA inc. + CA IVIA OBNL | Majorité qualifiée des deux CA | Comité doctrinal |
| Suspension ou résiliation de la convention de licence (côté OBNL) | CA IVIA OBNL | Majorité qualifiée (2/3) | Avis Comité doctrinal |
| Modification Charte doctrinaire — Niveau 1 | DG IVIA inc. | Décision DG | Comité doctrinal (notification 30 j, droit d'objection) |
| Modification Charte doctrinaire — Niveau 2 | Comité doctrinal + CA IVIA inc. | 2/3 Comité doctrinal + Majorité simple CA | Praticiens actifs (consultation 30 j) |
| Modification Charte doctrinaire — Niveau 3 | Actionnaire IVIA inc. + CA + Comité doctrinal | Décision actionnaire après vote unanime Comité doctrinal et avis du CA OBNL et consultation publique 60 j | — |
| Admission d'un investisseur (nouvelle émission, ouverture du capital) | Actionnaire + CA IVIA inc. | Décision actionnaire après majorité qualifiée CA | Comité doctrinal (avis sur clauses doctrinales du pacte d'actionnaires) ; CA IVIA OBNL (information sur impact licence sociale) |
| Cession partielle d'actifs significatifs | CA IVIA inc. | Majorité qualifiée (2/3) | Comité doctrinal (si actif lié à la mission) ; CA IVIA OBNL (si actif licencié) |
| Cession totale d'IVIA inc. | Actionnaire | Décision actionnaire | Comité doctrinal (avis public) + CA IVIA OBNL (information formelle) + Comité éthique consultatif |
| Audit doctrinal annuel | Comité doctrinal | Décision du Comité | CA IVIA inc. (approbation publication) |
| Programmes de redistribution OBNL | CA IVIA OBNL | Majorité simple | — |
| Demande de statut de bienfaisance ARC | CA IVIA OBNL | Majorité qualifiée (2/3) | Comité doctrinal (avis) |
| Signalement d'urgence client (protocole) | DG IVIA inc. (en temps réel) | Décision DG immédiate | — |
| Exclusion d'un praticien ou utilisateur avancé | DG IVIA inc. | Décision DG | Comité praticiens (consultation) |

### IX.2 Lecture de la matrice

Cette matrice est volontairement détaillée. Trois principes la sous-tendent :

1. **Le DG d'IVIA inc. décide vite** sur le quotidien opérationnel — l'écosystème ne peut pas se permettre des décisions ralenties par des consultations excessives.
2. **Le CA d'IVIA inc. arbitre les matières structurantes** — budget, ouvertures de capital, cessions, lancements de produits, modifications de la convention de licence.
3. **Le Comité doctrinal est saisi systématiquement** sur les matières doctrinales et de mission — son avis est public et opposable réputationnellement, mais juridiquement consultatif.

---

## PARTIE X — PROCÉDURES D'AMENDEMENT DE LA CHARTE DOCTRINAIRE (refonte v2.0)

Conformément à la Charte doctrinaire v1.1, Partie IV (D.1), trois niveaux d'amendement existent. Les procédures sont mises à jour pour la nouvelle architecture :

### X.1 Niveau 1 — Amendements mineurs

1. Le DG ou un membre du Comité doctrinal propose l'amendement par écrit avec justification
2. Transmission au Comité doctrinal pour information (délai 30 jours)
3. Si aucune objection formelle dans les 30 jours : adoption par décision du DG
4. Si objection : escalade au Niveau 2
5. Entrée en vigueur 30 jours après adoption
6. Publication dans le rapport annuel

### X.2 Niveau 2 — Amendements substantiels

1. Proposition écrite avec justification doctrinale complète
2. Transmission au Comité doctrinal pour délibération (délai 60 jours)
3. Vote du Comité doctrinal à la majorité 2/3
4. Publication de la proposition avec résumé en langage clair sur ivia.quebec
5. Période de consultation des praticiens et utilisateurs avancés actifs (30 jours minimum)
6. Analyse des retours par le Comité doctrinal
7. Vote final du Comité doctrinal (2/3 maintenu requis)
8. Approbation du CA d'IVIA inc. (majorité simple)
9. Information du CA d'IVIA OBNL
10. Entrée en vigueur avec notification à tous les utilisateurs avancés et clients (préavis 30 jours)
11. Publication intégrale

### X.3 Niveau 3 — Amendements fondamentaux

1. Proposition écrite avec rapport d'impact doctrinal rédigé par un tiers indépendant
2. Transmission au Comité doctrinal et au Comité éthique consultatif
3. Délibération conjointe des deux Comités
4. Vote à l'unanimité du Comité doctrinal
5. Avis consultatif documenté du Comité éthique consultatif (rendu public)
6. Avis consultatif documenté du CA d'IVIA OBNL (rendu public)
7. Consultation publique de 60 jours minimum sur ivia.quebec
8. Rapport de synthèse de la consultation
9. Vote final du Comité doctrinal (unanimité maintenue requise)
10. Avis consultatif du CA d'IVIA inc. (majorité qualifiée 2/3)
11. Décision finale de l'**actionnaire** d'IVIA inc. (le fondateur en tant qu'actionnaire unique tant que le capital n'est pas ouvert ; selon le pacte d'actionnaires en vigueur ensuite)
12. Si la décision de l'actionnaire s'écarte de l'unanimité du Comité doctrinal ou des avis publics, **publication intégrale** de la justification dans le rapport annuel et notification individuelle à tous les utilisateurs avancés actifs
13. Entrée en vigueur avec préavis de 60 jours

**Note de transparence** : la centralisation finale de la décision chez l'actionnaire (DÉC-V3-15) est compensée par le caractère **public** et **documenté** de l'ensemble du processus. L'actionnaire ne peut pas modifier la doctrine en silence ; il doit le faire en pleine lumière, en assumant publiquement l'écart entre sa décision et les avis émis.

### X.4 Verrou anti-dérive

Aucune pression commerciale, aucune demande d'investisseur, aucune urgence de croissance ne peut court-circuiter les délais de consultation publique pour les modifications de Niveau 2 et 3. Toute tentative de contournement est un signal d'alarme doctrinaire à rapporter immédiatement au Comité doctrinal et publier dans le rapport annuel.

---

## PARTIE XI — PROCÉDURE DE RÉSOLUTION DE CONFLITS INTERNES

### XI.1 Niveaux de conflit

| Niveau | Nature du conflit | Instance de résolution |
|---|---|---|
| 1 | Désaccord opérationnel entre utilisateur avancé et direction | DG IVIA inc. |
| 2 | Désaccord persistant sur une décision de gouvernance | CA d'IVIA inc. (si IVIA inc. concernée) ou CA d'IVIA OBNL (si OBNL concerné) |
| 3 | Conflit entre IVIA inc. et IVIA OBNL (interprétation ou application de la convention de licence sociale) | Médiation externe selon clause de la convention, puis arbitrage |
| 4 | Allégation de violation doctrinale grave | Comité doctrinal, puis CA d'IVIA inc. (et éventuellement CA d'IVIA OBNL) |

### XI.2 Procédure générale (5 étapes)

1. **Dialogue direct** (15 jours, documenté)
2. **Médiation interne** (DG ou tiers neutre désigné, 30 jours)
3. **Décision de l'instance compétente** (selon tableau, 15 jours)
4. **Médiation externe** (médiateur accrédité, coût partagé, décision contraignante sauf recours judiciaire)
5. **Arbitrage ou tribunal** (ultime recours — Cour du Québec ou Cour supérieure selon montants ; loi applicable : lois québécoises)

### XI.3 Protection contre les représailles

Aucune représaille pour usage de la procédure ou exercice des droits. Toute représaille présumée déclenche la procédure de Niveau 4.

---

## PARTIE XII — AUDIT DOCTRINAL ANNUEL

### XII.1 Mandat et périmètre

L'audit doctrinal annuel est prévu par la Charte doctrinaire (Partie V). Conduit ou supervisé par le Comité doctrinal.

**Périmètre** :
1. Conformité de l'offre commerciale et des produits aux règles des Blocs A et B de la Charte
2. Conformité du traitement des données (Charte de transformation gouvernée v1.0)
3. Conformité des communications marketing aux principes 1, 4, 5 et 6
4. Conformité des partenariats et opérations à la règle de non-commission (C.2 et C.3)
5. État des signalements reçus et leur traitement
6. Taux de praticiens et utilisateurs avancés formés et à jour (formation doctrine minimale)
7. **Bilan de la convention de licence sociale envers IVIA OBNL** (usage réel, redevances, redistribution effectuée)
8. Bilan des décisions du Comité doctrinal et du CA d'IVIA inc. sur la période

**Premier audit** : prévu à la fin du Palier 2 (M12-M15). Périmètre allégé (S1 + 2 praticiennes pilote + premiers programmes OBNL si activés). Établit la méthodologie de référence pour les audits suivants.

### XII.2 Méthode (4 phases)

1. **Revue documentaire** (3-4 semaines) : offres, contrats, communications, PV, conformité Loi 25, registre des consentements, rapports financiers.
2. **Entretiens** (2-3 semaines) : praticiens et utilisateurs avancés actifs (échantillon 20 % minimum, max 10 entretiens), clients/usagers actifs ou récemment terminés (5 entretiens minimum), équipe de direction, membres du CA d'IVIA OBNL.
3. **Test fonctionnel** (1-2 semaines) : parcours de consentement granulaire, vérification de l'absence de mécanismes de fidélisation contraires au Principe 4, test du workflow de validation utilisateur avancé avant diffusion.
4. **Rapport** (2 semaines) : rédaction, approbation par le Comité doctrinal, approbation de la publication par le CA d'IVIA inc., notification au CA d'IVIA OBNL, publication.

### XII.3 Publication et suivi

**Délai** : 60 jours après clôture de l'exercice annuel.
**Publication** : ivia.quebec/transparence.
**Contenu obligatoire** : conformités confirmées (avec exemples), non-conformités identifiées (avec description précise), mesures correctives et calendrier, signalements reçus (agrégés), taux de formation doctrine minimale, bilan licence sociale, modifications de Charte effectuées dans l'année.
**Suivi** : les mesures correctives sont vérifiées à l'audit suivant. Toute non-conformité non résolue dans le délai annoncé est signalée explicitement.

---

## PARTIE XIII — REPORTING ET TRANSPARENCE

### XIII.1 Reporting interne mensuel

**Destinataires** : DG + administrateurs IVIA inc.
**Contenu** : KPI opérationnels (uptime, séances, utilisateurs actifs, MRR), KPI qualité, KPI conformité (consentements, incidents Loi 25), coûts variables réels vs hypothèses BP, signalements doctrinaires.
**Fréquence** : mensuelle, en amont de la réunion de direction.

### XIII.2 Reporting trimestriel aux investisseurs

**Activation** : dès première levée significative (Palier 3-4).
**Contenu** : états financiers trimestriels non audités, MRR/ARR prévisionnel, taux de croissance, utilisateurs actifs par produit et par plan, avancement des paliers et gates, incidents significatifs, prévisions du trimestre suivant.
**Format** : lettre trimestrielle (2-4 pages) + tableau de bord en annexe.

**Frontière** : le reporting investisseurs couvre les matières financières et opérationnelles. Il ne révèle pas les délibérations du Comité doctrinal ou du CA d'IVIA OBNL qui ne les concernent pas. La frontière entre transparence légitime envers les investisseurs et confidentialité des délibérations internes est maintenue consciemment.

### XIII.3 Rapport annuel public

**Fréquence** : annuel, dans les 90 jours suivant la clôture de l'exercice fiscal d'IVIA inc.
**Contenu** : bilan de la mission (par produit), bilan économique, bilan de gouvernance, rapport doctrinal annuel, rapport de conformité données, perspectives et engagements pour l'année suivante.
**Publication** : ivia.quebec/transparence.

### XIII.4 Rapport annuel d'IVIA OBNL

L'OBNL produit un **rapport annuel distinct** centré sur sa mission de redistribution :
- Programmes menés, bénéficiaires servis, impact mesuré
- Bilan financier (subventions, dons, frais opérationnels, frais de licence à IVIA inc.)
- Bilan de la conformité doctrinale d'IVIA inc. de son point de vue (avis annuel obligatoire)

Publication : ivia.quebec/obnl ou domaine propre selon décision du CA OBNL.

---

## PARTIE XIV — CODE DE CONDUITE DES ADMINISTRATEURS ET MEMBRES D'INSTANCES

### XIV.1 Champ d'application

S'applique à : administrateurs d'IVIA inc., administrateurs d'IVIA OBNL, membres du Comité doctrinal, membres du Comité consultatif, membres du Comité des praticiens et utilisateurs avancés, membres du Comité éthique consultatif, direction exécutive d'IVIA inc., direction générale d'IVIA OBNL.

### XIV.2 Engagements fondamentaux

1. **Primauté de la mission** : toute décision est évaluée à l'aune de la mission et des 7 principes doctrinaires.
2. **Transparence et honnêteté** : pas de rétention d'information pertinente, pas de représentation fausse.
3. **Confidentialité** : les délibérations non publiées sont confidentielles ; les informations commerciales sensibles sont traitées avec discrétion ; obligation persiste après la fin du mandat.
4. **Présence et engagement réel** : présence < 75 % des réunions ordinaires sans motif accepté justifie une discussion sur le maintien du mandat.
5. **Refus de la dérive silencieuse** : aucun administrateur ne laisse passer sans la nommer une décision contraire à la doctrine. La dénonciation interne est un acte de gouvernance, pas une trahison.

### XIV.3 Comportements incompatibles

- Profiter de sa position pour orienter des utilisateurs vers un intérêt économique personnel
- Utiliser des informations confidentielles dans un contexte concurrent
- Influencer les décisions tarifaires ou contractuelles en faveur d'un tiers où l'on a un intérêt
- Tenir un discours public en contradiction avec la Charte doctrinaire sans signal d'alerte formel préalable
- Accepter cadeaux/avantages d'une valeur > 150 $ d'un utilisateur, partenaire ou investisseur sans déclaration formelle

---

## PARTIE XV — POLITIQUE DES CONFLITS D'INTÉRÊTS

### XV.1 Définition

Conflit d'intérêts = un membre d'instance a, directement ou indirectement, un intérêt personnel, financier ou relationnel dans une décision soumise.

### XV.2 Procédure de déclaration

1. Identification du conflit potentiel **avant** délibération
2. Déclaration verbale puis écrite au secrétaire de l'instance
3. Consignation au PV
4. Sortie de la salle (physique ou virtuelle) pendant délibération et vote
5. Mention au rapport annuel de transparence (sans détail si préjudice)

### XV.3 Déclaration annuelle

Tous les membres d'instances remplissent une déclaration annuelle d'intérêts. Conservée par le RPRP (Responsable de la protection des renseignements personnels) pour IVIA inc. et son équivalent pour IVIA OBNL.

---

## PARTIE XVI — DISPOSITIONS TRANSITOIRES ET ÉVOLUTIVES

### XVI.1 Phase pilote (Palier 0 — actuel jusqu'à la constitution)

- David personnellement détient les actifs et opère MERLIN
- Aucune entité juridique encore — gouvernance = décisions du fondateur, journal des décisions stratégiques tenu (HISTORIQUE_DECISIONS_STRATEGIQUES.md)
- Pré-formation du Comité doctrinal en informel : fondateur + 1 expert externe en cours d'identification

### XVI.2 Activation progressive des instances

| Palier | Instances actives | Nouveautés |
|---|---|---|
| Palier 0 (actuel — fin été 2026) | Direction informelle (fondateur seul) | DBA noms commerciaux REQ |
| Palier 1 (M7-M9, automne 2026) | Direction IVIA inc. + Administrateur unique CA IVIA inc. + Comité doctrinal en formation (Sièges 1+5) | Constitution IVIA inc. SPA à mission, transfert d'actifs |
| Palier 2 (M9-M12, hiver 2026-2027) | + CA IVIA inc. à 3 membres + CA IVIA OBNL constitué + Comité doctrinal complété + Comité consultatif activé + Comité praticiens activé | Constitution IVIA OBNL, convention de licence sociale, premières élections praticiens |
| Palier 3 (M12-M18) | + Comité éthique consultatif + administrateur investisseur CA IVIA inc. (si 1ère levée) + DG OBNL recruté(e) | Premier audit doctrinal complet, demande bienfaisance ARC |
| Palier 4 (M18-M24) | + Représentant deuxième produit au Comité praticiens + représentants additionnels OBNL | Lancement second produit, fiducie de mission étudiée |
| Palier 5+ (M24+) | Gouvernance complète (toutes instances, tous comités, tous sièges optionnels) | Gouvernance mature, ouverture du capital éventuelle, IPO possible long terme |

### XVI.3 Révision du présent document

Révisé :
- Au minimum une fois par an, à l'occasion de la revue annuelle de gouvernance
- Lors de chaque changement structurant (lancement produit, levée significative, modification structure juridique)
- Sur recommandation du Comité doctrinal

Toute révision est approuvée par le CA d'IVIA inc. (et le CA d'IVIA OBNL si modifications le concernent), notifiée aux parties prenantes.

---

## RÉFÉRENCES DOCUMENTAIRES

- `CHARTE_DOCTRINAIRE_IVIA.md` v1.1 — Parties IV, V, VII (gouvernance doctrinaire et statuts protecteurs)
- `STRUCTURE_JURIDIQUE_RECOMMANDEE.md` v2.0 — Paliers 1-3, mécanismes inter-entités
- `CADRE_PROPRIETE_INTELLECTUELLE_DONNEES.md` v2.0 — Partie III (convention de licence sociale)
- `HISTORIQUE_DECISIONS_STRATEGIQUES.md` v1.3 — DÉC-V3-15
- `BP_FINANCEMENT_V2.md` (à mettre à jour v2) — section structure juridique
- `PLAN_INTEGRATION_IVIA_36MOIS.md` (à mettre à jour) — paliers
- `CGU_PRATICIENS.md` (à mettre à jour) — Comité des praticiens et droits de représentation
- `CARTOGRAPHIE_RISQUES.md` — risques de gouvernance

---

**Au sein de l'être — En actes.**
**Pour le peuple, par le peuple.**

*Version 2.0 — 8 mai 2026 — Refonte post-DÉC-V3-15*
*David Phaneuf, fondateur IVIA + Perplexity Computer*

# CARTOGRAPHIE DES RISQUES — IVIA
## Version 1.0 — Vague 2 — Mai 2026

---

**Organisation** : IVIA inc. (SPA-mère LSAQ à mission) / IVIA OBNL satellite (LCQ III, à constituer P2)
**Responsable du document** : Direction générale — David Phaneuf
**Cycle de révision** : Trimestriel (janvier, avril, juillet, octobre)
**Prochaine révision prévue** : 1er août 2026
**Statut** : Actif — Pilote P1

> **⚠️ Note terminologique post-DÉC-V3-15 (8 mai 2026)** : ce document fait référence à « MERLIN inc. » dans plusieurs fiches de risque. Cette désignation reflète l'**ancienne architecture** (IVIA OBNL mère / MERLIN inc. SPA fille). Lire « MERLIN inc. » comme « **IVIA inc.** (SPA-mère) » et « CTO MERLIN inc. » comme « **CTO IVIA inc.** ». Substitution mécanique à effectuer lors de la révision trimestrielle suivant l'incorporation IVIA inc. (Q3-Q4 2026), conformément au BILAN_COHERENCE_REFONTE_v2.0 §3.

---

> Ce document constitue la cartographie officielle des risques d'IVIA pour la phase pilote (M1–M6) et les paliers subséquents. Il couvre sept catégories de risques, présente chaque risque selon une fiche structurée, offre une matrice 4×4 de priorisation et un plan de revue trimestrielle. Il doit être lu conjointement avec la CHARTE_DOCTRINAIRE_IVIA.md, le PLAN_INTEGRATION_IVIA_36MOIS.md, la POLITIQUE_CONFIDENTIALITE_LOI25.md et la CHARTE_TRANSFORMATION_GOUVERNEE_DONNEES.md.

---

## TABLE DES MATIÈRES

1. [Introduction et méthodologie](#1-introduction-et-méthodologie)
2. [Légende et grille de cotation](#2-légende-et-grille-de-cotation)
3. [Catégorie A — Risques doctrinaires](#3-catégorie-a--risques-doctrinaires)
4. [Catégorie B — Risques juridiques](#4-catégorie-b--risques-juridiques)
5. [Catégorie C — Risques techniques](#5-catégorie-c--risques-techniques)
6. [Catégorie D — Risques économiques](#6-catégorie-d--risques-économiques)
7. [Catégorie E — Risques opérationnels](#7-catégorie-e--risques-opérationnels)
8. [Catégorie F — Risques de marché](#8-catégorie-f--risques-de-marché)
9. [Catégorie G — Risques réputationnels](#9-catégorie-g--risques-réputationnels)
10. [Matrice de priorisation 4×4](#10-matrice-de-priorisation-4×4)
11. [Top 10 des risques prioritaires](#11-top-10-des-risques-prioritaires)
12. [Plan de revue trimestrielle](#12-plan-de-revue-trimestrielle)
13. [Registre des risques — Vue synthétique](#13-registre-des-risques--vue-synthétique)

---

## 1. Introduction et méthodologie

### 1.1 Objet

La présente cartographie vise à identifier, qualifier et prioriser les risques significatifs auxquels IVIA est exposée à travers ses trois horizons de développement :

- Horizon court terme : P1–P2 (M1–M6, pilote)
- Horizon moyen terme : P3–P4 (M7–M18, consolidation)
- Horizon long terme : P5–P6 (M19–M36, déploiement complet)

Cette cartographie n'est pas un exercice théorique. Elle est un outil de décision actif, révisé chaque trimestre, et directement lié aux gates Go/No-Go définis dans le PLAN_INTEGRATION_IVIA_36MOIS.md.

### 1.2 Principes de gestion des risques chez IVIA

La gestion des risques chez IVIA n'est pas neutre. Elle est doctrinalement orientée :

a) Le vivant d'abord : aucun risque économique ne justifie de compromettre la sécurité ou le bien-être d'un client ou d'un praticien.

b) La responsabilité comme dignité : IVIA assume ses erreurs et met en oeuvre des mesures correctives sans minimiser les faits.

c) L'équilibre comme pratique : la gestion des risques cherche l'équilibre entre audace stratégique et prudence doctrinaire — ni la paralysie, ni l'aveuglement.

d) Les lois de l'échange : les risques contractuels et financiers doivent être anticipés de façon à préserver des relations justes avec toutes les parties.

### 1.3 Méthode de cotation

Chaque risque est évalué selon deux axes :

- Probabilité d'occurrence : faible (1) / moyenne (2) / élevée (3)
- Impact potentiel : mineur (1) / significatif (2) / majeur (3) / catastrophique (4)

Le score brut = Probabilité × Impact (échelle de 1 à 12).

| Score | Zone de risque |
|-------|---------------|
| 1–3 | Acceptable — surveillance légère |
| 4–6 | Modéré — plan de prévention requis |
| 7–9 | Élevé — mitigation prioritaire |
| 10–12 | Critique — action immédiate requise |

### 1.4 Structure de chaque fiche de risque

Chaque fiche comprend :
- Identifiant unique (ex. : A1, B3, C2...)
- Titre et description précise
- Probabilité / Impact / Score
- Horizon de risque principal (P1–P6)
- Indicateurs précurseurs (signaux d'alerte observables)
- Plan de prévention (actions pour réduire la probabilité)
- Plan de mitigation (actions pour réduire l'impact si survenu)
- Responsable désigné

---

## 2. Légende et grille de cotation

### 2.1 Probabilité

| Cote | Libellé | Description opérationnelle |
|------|---------|---------------------------|
| 1 | Faible | Moins de 20 % de probabilité sur l'horizon considéré |
| 2 | Moyenne | Entre 20 % et 60 % de probabilité sur l'horizon considéré |
| 3 | Élevée | Plus de 60 % de probabilité sur l'horizon considéré |

### 2.2 Impact

| Cote | Libellé | Description opérationnelle |
|------|---------|---------------------------|
| 1 | Mineur | Gêne opérationnelle sans conséquence structurelle |
| 2 | Significatif | Perturbation notable; correction possible sans dommage durable |
| 3 | Majeur | Atteinte sérieuse à la mission, aux finances ou à la réputation; récupération longue |
| 4 | Catastrophique | Menace l'existence même d'IVIA ou met en danger des personnes |

### 2.3 Codes couleurs de la matrice

| Couleur | Score | Priorité |
|---------|-------|---------|
| VERT | 1–3 | Faible priorité |
| JAUNE | 4–6 | Priorité modérée |
| ORANGE | 7–9 | Haute priorité |
| ROUGE | 10–12 | Critique |

---

## 3. Catégorie A — Risques doctrinaires

Les risques doctrinaires sont les risques les plus singuliers d'IVIA. Ils menacent l'identité fondamentale de l'organisation. Leur survenue peut être silencieuse — une série de petites décisions d'exception finissant par éroder l'intégrité du projet.

---

### Fiche A1 — Dérive doctrinaire sous pression de croissance

Description :
Au fil de la croissance, des décisions de gestion (acquisition de nouveaux marchés, adaptation tarifaire, recrutement de praticiens moins alignés) risquent de s'écarter progressivement des 7 principes directeurs sans qu'aucune transgression unique ne soit manifeste. La dérive se produit par accumulation de concessions dites "pragmatiques".

| Dimension | Évaluation |
|-----------|-----------|
| Probabilité | Élevée (3) |
| Impact | Majeur (3) |
| Score | 9 — Haute priorité |
| Horizon principal | P3–P5 (M7–M27) |

Indicateurs précurseurs :
- Augmentation du taux d'admission des praticiens sans audit de valeurs
- Décisions de CA motivées exclusivement par les KPI financiers
- Réduction de la durée ou du contenu de la formation doctrinaire des praticiens
- Plaintes récurrentes de praticiens sur la pression à la performance vs. la qualité d'accompagnement
- Disparition progressive du vocabulaire doctrinal dans les communications internes

Plan de prévention :
- Audit doctrinal annuel obligatoire (GOUVERNANCE_INTERNE_IVIA.md, section 13)
- Comité doctrinal permanent avec veto sur les décisions affectant les 7 principes
- Formation doctrinaire non réductible intégrée au MANUEL_FORMATION_PRATICIENS.md
- Rappel doctrinal obligatoire à chaque CA (premier point à l'ordre du jour)
- Tableau de bord doctrinal mensuel soumis au CA OBNL

Plan de mitigation :
- Déclenchement immédiat d'une revue doctrinale extraordinaire si 2 indicateurs ou plus sont actifs simultanément
- Suspension temporaire des admissions de nouveaux praticiens pendant la revue
- Convocation d'une assemblée extraordinaire des membres si la dérive est confirmée
- Publication d'une "Déclaration de réaffirmation doctrinale" si nécessaire

Responsable : Comité doctrinal IVIA / Président du CA OBNL

---

### Fiche A2 — Compromission doctrinaire par investisseur

Description :
Un investisseur ou bailleur de fonds conditionne son financement à des modifications de l'offre contraires aux règles fermes (Bloc A), notamment : automatisation de l'orientation (violation A.2), conservation prolongée des données audio (violation A.7), ou normalisation comparative des clients (violation A.5). La pression peut être indirecte — un représentant au CA formulant des "suggestions" récurrentes.

| Dimension | Évaluation |
|-----------|-----------|
| Probabilité | Faible (1) |
| Impact | Catastrophique (4) |
| Score | 4 — Priorité modérée (mais à surveiller absolument) |
| Horizon principal | P4–P6 (M13–M36) |

Indicateurs précurseurs :
- Demandes répétées d'un investisseur pour accéder aux données clients ou aux transcriptions
- Pression pour intégrer des mécanismes de "gamification" ou de "fidélisation" de l'utilisateur
- Proposition de modifier la structure des consentements pour en augmenter le taux d'acceptation
- Suggestion de supprimer l'effacement audio J+30 pour "enrichir le dataset"
- Tentative de modifier les statuts de MERLIN inc. pour réduire le veto doctrinal des actions spéciales détenues par IVIA OBNL

Plan de prévention :
- Structure de gouvernance avec actions spéciales à veto doctrinal (STRUCTURE_JURIDIQUE_RECOMMANDEE.md)
- Clause de protection doctrinale dans tous les pactes d'actionnaires
- Due diligence valeurs avant toute acceptation de financement
- Politique de communication claire aux investisseurs sur les règles fermes Bloc A, signée à l'entrée
- Aucun siège de CA accordé à un investisseur sans adhésion documentée aux 7 principes

Plan de mitigation :
- Exercice immédiat du veto doctrinal de l'OBNL sur toute résolution contraire aux règles Bloc A
- Refus documenté du financement conditionnel, avec communication transparente si nécessaire
- Activation du mécanisme de rachat d'actions si un actionnaire contrevient à la charte doctrinale
- Accompagnement juridique immédiat (Fasken ou équivalent spécialisé OBNL-tech)

Responsable : Président du CA OBNL / Comité doctrinal / Avocat corporatif

---

### Fiche A3 — Dilution de la mission par extension non encadrée de l'offre

Description :
Sous pression du marché ou de partenaires, IVIA étend son offre à des services qui glissent vers la substitution déguisée à un ordre professionnel (violation A.6) — par exemple : praticiens proposant des "plans de traitement structurés", intégration de tests psychométriques standardisés, ou offre de coaching clinique non encadré.

| Dimension | Évaluation |
|-----------|-----------|
| Probabilité | Moyenne (2) |
| Impact | Majeur (3) |
| Score | 6 — Priorité modérée |
| Horizon principal | P2–P4 (M4–M18) |

Indicateurs précurseurs :
- Praticiens proposant des outils ou grilles d'évaluation clinique non approuvés
- Demandes répétées de clients pour un "diagnostic" ou un "plan de traitement"
- Partenariats proposés par des firmes de testing psychométrique
- Contenu de formation de P2 ou P3 incluant des notions cliniques hors mandat
- Confusion dans les communications marketing entre "accompagnement" et "thérapie"

Plan de prévention :
- Délimitation claire du périmètre de chaque strate dans les CGU_PRATICIENS.md et MANUEL_FORMATION_PRATICIENS.md
- Supervision mensuelle des séances (protocole d'écoute aléatoire post-consentement)
- Tout partenariat extérieur soumis à l'approbation du Comité doctrinal
- Formation continue des praticiens sur les limites du mandat IVIA

Plan de mitigation :
- Avertissement formel au praticien concerné, suivi possible de suspension
- Retrait immédiat de tout contenu ou service non conforme
- Communication proactive aux clients concernés si nécessaire
- Révision du module de formation correspondant

Responsable : Comité doctrinal / Direction générale

---

## 4. Catégorie B — Risques juridiques

---

### Fiche B1 — Non-conformité à la Loi 25 (Québec) ou au RGPD

Description :
IVIA traite des données personnelles sensibles (audio biométrique, transcriptions, signaux émotionnels). Une faille dans la mise en oeuvre du pipeline de transformation gouvernée — notamment l'effacement audio J+30 — ou une défaillance dans les mécanismes de consentement granulaire expose IVIA à des sanctions réglementaires sévères sous la Loi 25 (CAI) et, pour les résidents européens, sous le RGPD.

| Dimension | Évaluation |
|-----------|-----------|
| Probabilité | Moyenne (2) |
| Impact | Catastrophique (4) |
| Score | 8 — Haute priorité |
| Horizon principal | P1–P6 (continu) |

Indicateurs précurseurs :
- Absence de confirmation automatique d'effacement audio à J+30
- Lacunes dans les journaux d'audit de consentement (logs incomplets)
- Incapacité à répondre à une demande d'accès aux renseignements personnels en 30 jours (délai légal Loi 25)
- Traitement de données hors territoire québécois sans encadrement contractuel adéquat
- Plainte d'un client ou d'un praticien à la CAI ou à une autorité RGPD
- Audit interne révélant des lacunes dans la pseudonymisation

Plan de prévention :
- Mise en oeuvre rigoureuse du pipeline 8 étapes (CHARTE_TRANSFORMATION_GOUVERNEE_DONNEES.md)
- Audit Loi 25 / RGPD réalisé avant le lancement du pilote (M1) par un juriste spécialisé
- Nomination d'un RPRP (responsable de la protection des renseignements personnels) — privacy@ivia.quebec
- Politique de confidentialité complète et à jour (POLITIQUE_CONFIDENTIALITE_LOI25.md)
- Tests techniques de l'effacement irréversible avant mise en production
- Formation obligatoire de toute l'équipe sur la Loi 25 (au moins 2h avant P1)

Plan de mitigation :
- Notification immédiate à la CAI en cas d'incident de confidentialité (délai légal : 72h pour les incidents graves)
- Activation du plan de réponse aux incidents de sécurité (voir Fiche C2)
- Communication transparente aux personnes concernées
- Engagement d'un avocat spécialisé données personnelles (ex. : Heenan Blaikie, McCarthy Tétrault)
- Remédiation technique prioritaire dans les 48h suivant la détection

Responsable : RPRP (privacy@ivia.quebec) / Direction générale / CTO MERLIN inc.

---

### Fiche B2 — Conflit avec un ordre professionnel

Description :
Un ordre professionnel (OPQ, OTSTCFQ, CMQ) dépose une plainte ou émet une mise en demeure soutenant qu'IVIA exerce illégalement la psychothérapie ou empiète sur le champ d'exercice réservé. Ce risque est inhérent au positionnement d'IVIA à la frontière entre écoute bienveillante et intervention professionnelle.

| Dimension | Évaluation |
|-----------|-----------|
| Probabilité | Faible (1) |
| Impact | Catastrophique (4) |
| Score | 4 — Priorité modérée (priorité élevée de surveillance) |
| Horizon principal | P2–P4 (M4–M18) |

Indicateurs précurseurs :
- Communications d'un ordre professionnel demandant des clarifications sur l'offre IVIA
- Plaintes de membres d'ordres professionnels sur des pratiques de praticiens IVIA
- Publication d'articles critiques par des associations professionnelles sur les plateformes d'écoute
- Recrutement de praticiens dont les activités IVIA chevauchent leur pratique réglementée
- Utilisation impropre de terminologie clinique dans les communications IVIA (ex. : "thérapie", "traitement", "diagnostic")

Plan de prévention :
- Communication proactive avec les ordres concernés avant le lancement public (M1–M3)
- Délimitation juridique formelle de l'offre S1 (praticiens hors ordres, écoute non clinique)
- Avis juridique formel sur la distinction écoute / psychothérapie avant P1
- Formation obligatoire des praticiens sur les termes interdits et les limites de mandat
- Cadrage explicite dans les CGU_CLIENTS.md et CGU_PRATICIENS.md (section "Ce qu'IVIA n'est pas")
- Veille réglementaire trimestrielle sur les modifications aux règlements des ordres

Plan de mitigation :
- Engagement immédiat d'un avocat spécialisé droit professionnel (ex. : Lavery, Robinson Sheppard)
- Suspension temporaire des admissions dans la strate concernée le temps de l'analyse
- Dialogue direct avec l'ordre plaignant — IVIA cherche la clarté, pas le conflit
- Modification des communications ou de l'offre si nécessaire, avec transparence publique

Responsable : Direction générale / Avocat corporatif / Comité doctrinal

---

### Fiche B3 — Litige avec un praticien (résiliation, rémunération, données)

Description :
Un praticien quitte IVIA dans un contexte de tension et conteste la retenue de sa rémunération, la propriété d'une méthode développée pendant sa collaboration, ou l'effacement de données clients qu'il considère comme "siennes". Ce risque augmente avec le nombre de praticiens et les dynamiques P2–P4.

| Dimension | Évaluation |
|-----------|-----------|
| Probabilité | Moyenne (2) |
| Impact | Significatif (2) |
| Score | 4 — Priorité modérée |
| Horizon principal | P2–P4 (M4–M18) |

Indicateurs précurseurs :
- Tensions documentées entre un praticien et la direction sur la rémunération ou les conditions
- Non-renouvellement du contrat par un praticien accompagné d'une demande de "récupération" de clients
- Demande d'un praticien pour obtenir des transcriptions ou enregistrements de ses séances
- Rétention par un praticien de coordonnées clients (violation A.2 et non-sollicitation)
- Plainte interne non résolue restée ouverte plus de 30 jours

Plan de prévention :
- CONTRAT_PRATICIEN_TYPE.md complet et signé avant toute séance
- Clauses de PI claires (tous les outils et méthodes développés dans le cadre de la collaboration appartiennent à IVIA)
- Clause de non-sollicitation (24 mois) et mécanisme de transition clients (PROTOCOLE_CONSENTEMENT_CLIENT.md)
- Processus de résiliation documenté et transparent (CGU_PRATICIENS.md, article 8)
- Médiateur désigné en cas de conflit (Comité d'éthique)

Plan de mitigation :
- Activation de la procédure de médiation interne (30 jours) avant tout recours légal
- Conservation de toute la documentation contractuelle signée
- Accompagnement juridique si la médiation échoue
- Communication neutre aux clients concernés sur la transition (sans dénigrement)

Responsable : Direction générale / Comité d'éthique / Avocat corporatif

---

### Fiche B4 — Incident impliquant un mineur

Description :
Un mineur accède à la plateforme (avec ou sans consentement parental valide) et vit une expérience difficile ou prétend avoir subi un préjudice. Ce risque est particulièrement sensible au plan juridique (LPJ, responsabilité parentale, signalement obligatoire).

| Dimension | Évaluation |
|-----------|-----------|
| Probabilité | Faible (1) |
| Impact | Catastrophique (4) |
| Score | 4 — Priorité modérée (zéro tolérance) |
| Horizon principal | P1–P6 (continu) |

Indicateurs précurseurs :
- Vérification d'âge insuffisante à l'inscription
- Client déclarant des informations incohérentes sur son âge
- Praticien rapportant des indices de minorité d'un client
- Demande de consentement parental non complétée avant la première séance

Plan de prévention :
- Déclaration d'âge obligatoire à l'inscription (18 ans minimum sans consentement parental)
- Procédure spécifique pour les 14–17 ans avec consentement parental formalisé (PROTOCOLE_CONSENTEMENT_CLIENT.md)
- Formation des praticiens à l'identification de signaux de minorité
- Signalement obligatoire à la DPJ si risque de danger pour un mineur (PROTOCOLE_URGENCE_DETRESSE.md)

Plan de mitigation :
- Suspension immédiate de la séance et de l'accès au compte si mineur non conforme identifié
- Contact avec le parent ou tuteur légal dans les 24h
- Signalement à la DPJ si warranté (514 896-3100)
- Documentation complète de l'incident
- Accompagnement juridique immédiat

Responsable : Praticien concerné → urgence@ivia.quebec → Direction générale → DPJ si requis

---

## 5. Catégorie C — Risques techniques

---

### Fiche C1 — Panne de l'infrastructure principale pendant une séance

Description :
Une défaillance du serveur, de la plateforme vidéo/audio, ou du réseau interrompt brusquement une séance en cours, potentiellement à un moment émotionnellement vulnérable pour le client. Ce risque est amplifié pendant la phase pilote où l'infrastructure n'est pas encore redondante.

| Dimension | Évaluation |
|-----------|-----------|
| Probabilité | Moyenne (2) |
| Impact | Majeur (3) |
| Score | 6 — Priorité modérée |
| Horizon principal | P1–P3 (M1–M12) |

Indicateurs précurseurs :
- Latences ou coupures intermittentes signalées par des praticiens
- Temps de réponse de l'infrastructure dégradé (monitoring)
- Avertissements du fournisseur d'hébergement (maintenance planifiée non communiquée)
- Taux d'erreur API Stripe ou audio > 1 % sur 24h
- Incidents répétés sur un même fournisseur (Zoom, Daily.co, ou équivalent)

Plan de prévention :
- Choix d'un fournisseur d'infrastructure avec SLA ≥ 99,5 % de disponibilité
- Mise en place d'un environnement de repli (backup provider audio/vidéo) avant P1
- Monitoring en temps réel avec alertes automatiques (ex. : Datadog, UptimeRobot)
- Protocole de communication immédiate en cas de panne (immediat@ivia.quebec)
- Tests de charge avant le lancement de chaque palier

Plan de mitigation :
- Reprise de la séance via un canal de remplacement (téléphone, lien alternatif) dans les 10 minutes
- Message automatique aux praticiens et clients en cas de panne détectée
- Remboursement proratisé ou séance de remplacement sans frais si panne > 10 minutes
- Post-mortem technique dans les 48h avec rapport à la direction

Responsable : CTO MERLIN inc. / Praticien concerné pour la communication au client

---

### Fiche C2 — Faille de sécurité ou incident de confidentialité

Description :
Une cyberattaque (intrusion, ransomware, hameçonnage), une erreur de configuration, ou une vulnérabilité non corrigée expose les données personnelles sensibles de clients ou praticiens (enregistrements audio, transcriptions, données de santé). Il s'agit du risque technique le plus grave.

| Dimension | Évaluation |
|-----------|-----------|
| Probabilité | Faible (1) |
| Impact | Catastrophique (4) |
| Score | 4 — Priorité modérée (préparation maximale requise) |
| Horizon principal | P1–P6 (continu) |

Indicateurs précurseurs :
- Tentatives de connexion non autorisées détectées dans les logs
- Augmentation anormale du trafic sortant
- Alertes du système de détection d'intrusion (IDS)
- Accès admin depuis une localisation inhabituelle
- Rapport de vulnérabilité de bibliothèques tierces non corrigées (CVSS ≥ 7,0)

Plan de prévention :
- Chiffrement de bout en bout des enregistrements audio (AES-256 minimum)
- Authentification multi-facteurs (MFA) obligatoire pour tous les accès administrateurs
- Tests de pénétration trimestriels par une firme externe
- Gestion rigoureuse des dépendances (mise à jour automatique, audit CVE)
- Séparation des environnements production / staging / développement
- Formation sécurité annuelle pour toute l'équipe technique
- Politique de moindre privilège sur tous les accès systèmes

Plan de mitigation :
- Isolation immédiate du système compromis dans les 15 minutes suivant la détection
- Notification à la CAI dans les 72h si l'incident répond aux critères légaux (Loi 25, art. 3.5)
- Notification aux personnes concernées sans délai inutile
- Engagement d'une firme de réponse aux incidents cybersécurité
- Communication publique transparente si l'incident devient public
- Audit de sécurité complet avant remise en service

Responsable : CTO MERLIN inc. / RPRP / Direction générale

---

### Fiche C3 — Défaillance du pipeline d'effacement J+30

Description :
Le mécanisme automatique d'effacement des enregistrements audio bruts à J+30 (étape 6 du pipeline de transformation gouvernée) tombe en panne — que ce soit par défaillance technique, erreur de configuration, ou oubli lors d'une mise à jour. Les données biométriques sont alors conservées au-delà du délai légal et consenti.

| Dimension | Évaluation |
|-----------|-----------|
| Probabilité | Faible (1) |
| Impact | Majeur (3) |
| Score | 3 — Acceptable (mais priorité technique absolue) |
| Horizon principal | P1–P6 (continu) |

Indicateurs précurseurs :
- Absence de log d'effacement pour des séances dont la date J+30 est dépassée
- Espace de stockage audio non décroissant malgré le passage du délai
- Rapport d'erreur du job CRON ou du service d'effacement automatique
- Test de vérification mensuel échouant sur un ou plusieurs fichiers

Plan de prévention :
- Double mécanisme d'effacement : automatique (CRON) + vérification hebdomadaire manuelle
- Alertes automatiques si l'effacement n'est pas confirmé pour des fichiers à J+30
- Registre d'effacement signé électroniquement (journal d'audit)
- Test de l'ensemble du pipeline avant chaque mise à jour majeure
- Revue mensuelle du registre d'effacement par le RPRP

Plan de mitigation :
- Effacement manuel immédiat des fichiers non effacés à J+30 dans les 24h suivant la détection
- Rapport d'incident interne documentant la durée de rétention non prévue
- Évaluation de la nécessité de notification à la CAI selon la nature et la durée de l'écart
- Correction du mécanisme défaillant avant reprise des séances si la panne est systémique

Responsable : CTO MERLIN inc. / RPRP

---

### Fiche C4 — Perte ou corruption de données critiques

Description :
Une perte de données affecte les dossiers de séances, les consentements signés, les registres de paiement, ou les paramètres de configuration de la plateforme. Cela peut résulter d'une défaillance matérielle, d'une erreur humaine, ou d'un acte malveillant.

| Dimension | Évaluation |
|-----------|-----------|
| Probabilité | Faible (1) |
| Impact | Majeur (3) |
| Score | 3 — Acceptable (infrastructure requise avant P1) |
| Horizon principal | P1–P6 (continu) |

Indicateurs précurseurs :
- Échec d'une sauvegarde automatique signalé dans les logs
- Corruption de fichiers détectée lors d'une restauration de test
- Interruption anormale d'un processus d'écriture en base de données
- Espace disque saturé sur le serveur de base de données

Plan de prévention :
- Sauvegardes quotidiennes automatiques chiffrées avec rétention 30 jours minimum
- Test de restauration mensuel (vérifié et documenté)
- Base de données PostgreSQL avec réplication (standby) en temps quasi-réel
- Stockage géographiquement distribué (au moins deux régions canadiennes)

Plan de mitigation :
- Restauration depuis la dernière sauvegarde valide dans les 4h
- Identification de la fenêtre de perte de données et communication aux parties concernées
- Post-mortem et renforcement de l'infrastructure dans les 7 jours

Responsable : CTO MERLIN inc.

---

## 6. Catégorie D — Risques économiques

---

### Fiche D1 — Sous-financement ou retard de financement

Description :
Le plan de financement repose sur un budget de 2,2 M$ CAD sur 36 mois, incluant des sources multiples (auto-financement, subventions, investissement). Un retard dans l'obtention des fonds ou un rejet de demande de subvention pourrait forcer une réduction d'activité ou un report de palier.

| Dimension | Évaluation |
|-----------|-----------|
| Probabilité | Moyenne (2) |
| Impact | Majeur (3) |
| Score | 6 — Priorité modérée |
| Horizon principal | P1–P3 (M1–M12) |

Indicateurs précurseurs :
- Rejet d'une demande de subvention majeure (CDÉACF, Fonds d'économie sociale, etc.)
- Runway de trésorerie descendant sous 3 mois de frais d'exploitation
- Retard de plus de 60 jours dans le versement d'une tranche d'investissement prévue
- Croissance du MRR inférieure de 30 % ou plus aux projections à M6

Plan de prévention :
- Diversification des sources de financement (subventions + revenus d'exploitation + investissement)
- Maintien d'une réserve de trésorerie d'au moins 3 mois de frais à tout moment
- Modèle lean pour P1 : frais fixes ~340 $/mois (hors développement)
- Calendrier des demandes de financement établi dès M1 avec buffer de 90 jours
- Suivi financier mensuel avec rapport au CA

Plan de mitigation :
- Activation du "mode survie lean" : suspension des dépenses non-essentielles, report des lancements P3+
- Recherche accélérée de financement alternatif (prêt, financement participatif, partenariat)
- Communication transparente aux praticiens et partenaires sur la situation
- Convocation d'un CA extraordinaire pour décision sur la continuité

Responsable : Direction générale / Trésorier du CA OBNL

---

### Fiche D2 — Échec d'acquisition et de rétention des praticiens

Description :
Le modèle économique d'IVIA repose entièrement sur la présence de praticiens actifs et engagés. Une incapacité à recruter suffisamment de praticiens qualifiés, ou un taux de départ élevé, compromet les revenus et la crédibilité de la plateforme.

| Dimension | Évaluation |
|-----------|-----------|
| Probabilité | Moyenne (2) |
| Impact | Majeur (3) |
| Score | 6 — Priorité modérée |
| Horizon principal | P1–P3 (M1–M12) |

Indicateurs précurseurs :
- Taux de départ des praticiens > 20 % sur 6 mois
- Ratio séances annulées / séances confirmées > 15 % (signal de désengagement)
- Moins de 60 % des praticiens recrutés atteignant le seuil de 30 séances/mois en 90 jours
- Satisfaction praticien (NPS interne) < 30
- Nombre de candidatures praticien en deçà de 3 fois le nombre de postes disponibles

Plan de prévention :
- Programme d'onboarding structuré (MANUEL_FORMATION_PRATICIENS.md)
- Modèle de rémunération transparent et compétitif (CGU_PRATICIENS.md)
- Communauté de pratique mensuelle et supervision par les pairs
- Écoute active des praticiens via sondage trimestriel
- Diversité de profils recrutés pour réduire la dépendance à un segment

Plan de mitigation :
- Campagne de recrutement d'urgence via réseaux professionnels ciblés
- Revue de l'offre de rémunération et/ou des conditions de pratique
- Entretiens de sortie systématiques pour comprendre les causes de départ
- Redistribution temporaire des clients entre les praticiens restants avec leur accord

Responsable : Direction générale / Responsable recrutement praticiens

---

### Fiche D3 — Dérive des coûts variables et compression des marges

Description :
Les coûts variables par séance (frais Stripe, infrastructure audio, transcription IA) augmentent de façon imprévue, comprimant les marges nettes. À l'échelle (P5–P6), une dérive de 1–2 $/séance représente des dizaines de milliers de dollars mensuels.

| Dimension | Évaluation |
|-----------|-----------|
| Probabilité | Moyenne (2) |
| Impact | Significatif (2) |
| Score | 4 — Priorité modérée |
| Horizon principal | P3–P6 (M7–M36) |

Indicateurs précurseurs :
- Coût variable par séance dépassant 5 $ pour le plan Standard (vs. modèle ~3,56 $)
- Augmentation tarifaire de Stripe ou du fournisseur de transcription > 10 %
- Séances moyennes plus longues que prévu (> 80 min) augmentant les coûts audio
- Taux de remboursement ou de litige Stripe > 2 %

Plan de prévention :
- Négociation de tarifs de volume avec les fournisseurs clés à partir de P3
- Suivi mensuel du coût variable par séance par palier tarifaire
- Architecture technique optimisée pour minimiser les appels API redondants
- Clause de révision tarifaire incluse dans les CGU clients (préavis 30 jours)

Plan de mitigation :
- Ajustement tarifaire si les coûts variables dépassent 15 % du seuil modélisé
- Renégociation ou changement de fournisseur dans les 60 jours
- Révision du modèle financier et communication au CA

Responsable : Direction générale / Trésorier / CTO MERLIN inc.

---

### Fiche D4 — Absence de MRR suffisant pour passer le gate Go/No-Go M6

Description :
Le gate Go/No-Go à M6 exige un MRR ≥ 5 000 $, un NPS ≥ 35, et 0 incident doctrinal non résolu. Si ces seuils ne sont pas atteints, le lancement de P3 est compromis et l'attractivité pour les investisseurs est affectée.

| Dimension | Évaluation |
|-----------|-----------|
| Probabilité | Moyenne (2) |
| Impact | Majeur (3) |
| Score | 6 — Priorité modérée |
| Horizon principal | P1–P2 (M1–M6) |

Indicateurs précurseurs :
- MRR à M3 inférieur de 50 % aux projections
- Nombre de clients actifs par praticien inférieur à 5 à M2
- NPS < 20 à M3
- Taux de conversion "essai → abonnement" < 30 %

Plan de prévention :
- Tableau de bord hebdomadaire des métriques pilote (MANUEL_OPERATIONS_PILOTE.md)
- Ajustements rapides de l'offre ou du positionnement tarifaire si les métriques dévient
- Activation du réseau de bouche-à-oreille dès M1 (ancrage organique)
- Accompagnement marketing ciblé de Mylène et Émilie pour acquérir leurs 5 premiers clients chacune

Plan de mitigation :
- Revue extraordinaire à M4 si les indicateurs M3 sont négatifs
- Décision documentée : proroger P1 de 3 mois vs. pivoter l'offre vs. suspendre
- Communication transparente aux parties prenantes sur l'ajustement du calendrier

Responsable : Direction générale / CA OBNL

---

## 7. Catégorie E — Risques opérationnels

---

### Fiche E1 — Épuisement ou incapacité du fondateur

Description :
David Phaneuf, fondateur unique, cumule les rôles de direction générale, développement technique, gouvernance doctrinale et gestion des partenariats. Une incapacité prolongée (épuisement professionnel, maladie, accident) paralyserait les opérations en l'absence de relève identifiée.

| Dimension | Évaluation |
|-----------|-----------|
| Probabilité | Moyenne (2) |
| Impact | Catastrophique (4) |
| Score | 8 — Haute priorité |
| Horizon principal | P1–P3 (M1–M12) |

Indicateurs précurseurs :
- Délais croissants dans les réponses aux praticiens ou aux clients
- Décisions opérationnelles repoussées de semaine en semaine
- Plaintes ou inquiétudes exprimées par Mylène ou Émilie sur la disponibilité de la direction
- Absence de vacances ou de coupures sur une période de 90 jours ou plus
- Auto-évaluation du fondateur sur l'échelle d'épuisement (Maslach) ≥ score modéré

Plan de prévention :
- Documentation systématique de tous les processus clés (Manuels d'opérations, Vague 2)
- Identification d'un "directeur de relève temporaire" dès M3 (personne de confiance + accord formel)
- Limitation explicite du nombre d'heures de travail intensif par semaine (maximum 55h)
- Délégation formelle de responsabilités à mesure que l'équipe grandit
- Accès à un espace de supervision ou de soutien pour le fondateur lui-même

Plan de mitigation :
- Activation du plan de relève documenté (directeur de relève prend en charge les opérations)
- Convocation d'un CA extraordinaire pour décision sur la continuité des opérations
- Notification transparente aux praticiens (sans alarmer inutilement)
- Période de grâce de 30 jours avant révision de statut si incapacité temporaire

Responsable : CA OBNL / Directeur de relève désigné

---

### Fiche E2 — Départ d'une praticienne pilote (Mylène ou Émilie)

Description :
Mylène ou Émilie — les deux seules praticiennes du pilote P1 — quitte IVIA pour des raisons personnelles, professionnelles ou de désaccord. Ce départ laisse IVIA sans praticien actif, compromettant le pilote au complet.

| Dimension | Évaluation |
|-----------|-----------|
| Probabilité | Faible (1) |
| Impact | Majeur (3) |
| Score | 3 — Acceptable (mais préparation immédiate requise) |
| Horizon principal | P1 (M1–M3) |

Indicateurs précurseurs :
- Expression de doutes ou de réserves sur le modèle ou les conditions dans les retrouvailles hebdomadaires
- Réduction du nombre de séances proposées sans explication
- Demandes répétées de modification des conditions contractuelles
- Signaux de surcharge ou de mal-être exprimés

Plan de prévention :
- Entretiens réguliers de satisfaction avec chaque praticienne (mensuel minimum)
- Contrat clair et conditions connues avant le lancement (CONTRAT_PRATICIEN_TYPE.md)
- Reconnaissance active de leur rôle pionnier dans les communications internes et externes
- Identification confidentielle d'un ou deux profils praticiens de réserve prêts à être activés rapidement

Plan de mitigation :
- Activation immédiate d'un ou deux praticiens de réserve (pré-qualifiés)
- Transition respectueuse des clients (PROTOCOLE_CONSENTEMENT_CLIENT.md, section 5)
- Revue du pilote : est-il possible de poursuivre avec un seul praticien? Pendant combien de temps?
- Communication transparente aux clients concernés dans les 48h

Responsable : Direction générale

---

### Fiche E3 — Erreur humaine dans la gestion des données ou des consentements

Description :
Un membre de l'équipe ou un praticien commet une erreur dans la gestion des consentements (ex. : séance tenue sans consentement de niveau 1 valide), dans le traitement des données (ex. : envoi d'une transcription au mauvais client), ou dans l'application des protocoles d'urgence.

| Dimension | Évaluation |
|-----------|-----------|
| Probabilité | Moyenne (2) |
| Impact | Significatif (2) |
| Score | 4 — Priorité modérée |
| Horizon principal | P1–P4 (continu) |

Indicateurs précurseurs :
- Retours de clients signalant des incohérences dans leurs documents ou paramètres
- Praticien ne pouvant pas confirmer le niveau de consentement avant une séance
- Rapport de formation révélant des lacunes de compréhension du pipeline de consentement

Plan de prévention :
- Interface de consentement automatisée avec confirmation avant chaque séance
- Formation obligatoire sur les consentements (MANUEL_FORMATION_PRATICIENS.md, Module 3)
- Double vérification automatique côté système (consentement niveau 1 vérifié avant activation de l'enregistrement)
- Procédure claire de signalement en cas de doute (formation@ivia.quebec)

Plan de mitigation :
- Audit de l'incident dans les 24h
- Correction immédiate et notification à la personne concernée si nécessaire
- Mise à jour de la formation si la lacune est systémique
- Documentation au registre des incidents

Responsable : RPRP / Praticien concerné / Direction générale

---

## 8. Catégorie F — Risques de marché

---

### Fiche F1 — Concurrence accélérée de plateformes bien capitalisées

Description :
Des acteurs bien financés (BetterHelp, Dialogue, ou un nouvel entrant québécois) lancent une offre similaire à IVIA avec des moyens marketing et technologiques bien supérieurs, captant le marché avant qu'IVIA n'ait atteint sa masse critique.

| Dimension | Évaluation |
|-----------|-----------|
| Probabilité | Élevée (3) |
| Impact | Significatif (2) |
| Score | 6 — Priorité modérée |
| Horizon principal | P3–P5 (M7–M27) |

Indicateurs précurseurs :
- Lancement annoncé d'une fonctionnalité similaire par BetterHelp, Dialogue, ou Teladoc Health au Québec
- Augmentation du coût d'acquisition client (CAC) de 30 % ou plus
- Praticiens potentiels signalant avoir reçu des offres d'une plateforme concurrente
- Articles de presse sur le marché de l'accompagnement émotionnel en ligne au Québec

Plan de prévention :
- Ancrage doctrinal comme différenciation irréductible (aucun concurrent ne peut copier les 7 principes sans les vivre)
- Construction rapide de la preuve sociale québécoise (témoignages, NPS publiés, partenariats OBNL)
- Développement de la communauté praticiens comme barrière à l'entrée relationnelle
- Veille concurrentielle mensuelle (acteurs, offres, prix)
- Positionnement explicite : IVIA n'est pas une app de mieux-être générique — c'est un projet de société

Plan de mitigation :
- Accélération de la différenciation S2/S3 si la concurrence démontre une supériorité sur S1
- Alliance stratégique avec des partenaires institutionnels (CSSS, CISSS, employeurs) pour créer des canaux exclusifs
- Révision du positionnement marketing avec un accent fort sur les valeurs autochtones et décoloniales

Responsable : Direction générale / Responsable marketing

---

### Fiche F2 — Évolution défavorable de la réglementation

Description :
Une modification législative (Loi 25 révisée, nouveau règlement des ordres professionnels, législation sur l'IA en santé mentale) impose des contraintes inattendues qui rendent le modèle non conforme ou économiquement non viable.

| Dimension | Évaluation |
|-----------|-----------|
| Probabilité | Faible (1) |
| Impact | Majeur (3) |
| Score | 3 — Acceptable (veille active requise) |
| Horizon principal | P4–P6 (M13–M36) |

Indicateurs précurseurs :
- Consultations publiques sur la réglementation des plateformes de santé mentale en ligne
- Nouvelles orientations de la CAI sur les données biométriques et audio
- Projets de loi affectant les praticiens "hors ordres" au Québec
- Rapports du Commissaire à la santé et au bien-être sur les services numériques de santé mentale

Plan de prévention :
- Veille réglementaire trimestrielle (juriste + membre du Comité doctrinal)
- Participation aux consultations publiques pertinentes en tant qu'organisation
- Architecture doctrinale conçue pour anticiper les standards les plus stricts (privacy by design)
- Relations préventives avec les régulateurs concernés (CAI, OPQ)

Plan de mitigation :
- Analyse juridique d'impact dans les 30 jours suivant toute modification législative significative
- Plan de mise en conformité immédiate avec priorisation des éléments bloquants
- Communication transparente aux clients et praticiens sur les adaptations

Responsable : Direction générale / Avocat spécialisé / RPRP

---

### Fiche F3 — Rejet ou méfiance du marché envers l'IA dans l'accompagnement

Description :
Une montée des préoccupations publiques sur l'utilisation de l'IA dans les contextes de santé mentale (alimentée par des incidents médiatisés ailleurs) crée une résistance chez les clients et praticiens potentiels envers la plateforme IVIA, même si l'IA d'IVIA reste un outil de back-end doctrainement encadré.

| Dimension | Évaluation |
|-----------|-----------|
| Probabilité | Moyenne (2) |
| Impact | Significatif (2) |
| Score | 4 — Priorité modérée |
| Horizon principal | P4–P6 (M13–M36) |

Indicateurs précurseurs :
- Articles médiatiques critiques sur l'IA en santé mentale
- Baisse du taux d'acceptation du consentement de niveau 3
- Questions ou inquiétudes croissantes des praticiens lors des formations sur l'utilisation des données
- Pétitions ou prises de position publiques d'associations professionnelles sur l'IA clinique

Plan de prévention :
- Communication proactive et transparente sur le rôle limité et gouverné de l'IA chez IVIA
- Distinction claire entre "IA d'analyse en back-end" et "IA de contact client" (IVIA ne fait pas de chatbot clinique)
- Publication d'un "livre blanc" doctrinal sur la transformation gouvernée des données (Vague 3?)
- Consentements granulaires permettant aux clients de choisir leur niveau d'implication

Plan de mitigation :
- Adaptation des communications si la résistance devient significative
- Possibilité de suspendre temporairement P5 (synthétisation IA) si le contexte médiatique l'exige
- Dialogue avec les associations professionnelles pour co-construire les standards

Responsable : Direction générale / Comité doctrinal

---

## 9. Catégorie G — Risques réputationnels

---

### Fiche G1 — Incident grave impliquant un client (crise suicidaire non traitée)

Description :
Un client en état de détresse sévère (niveau 3 ou 4) ne reçoit pas une réponse adéquate — soit parce que le praticien n'a pas appliqué le PROTOCOLE_URGENCE_DETRESSE.md, soit parce que le client n'a pas voulu divulguer sa situation. Un incident grave (tentative de suicide, automutilation sévère) survient après ou pendant une séance IVIA.

| Dimension | Évaluation |
|-----------|-----------|
| Probabilité | Faible (1) |
| Impact | Catastrophique (4) |
| Score | 4 — Priorité modérée (préparation maximale requise, risque humain absolu) |
| Horizon principal | P1–P6 (continu) |

Indicateurs précurseurs :
- Praticien n'ayant pas complété la formation de niveau 2 (qui inclut le module urgences)
- Client exprimant des idéations suicidaires lors d'une séance sans déclenchement du protocole
- Praticien signalant une "situation difficile" sans activation formelle du protocole
- Absence de documentation post-incident dans les 24h

Plan de prévention :
- PROTOCOLE_URGENCE_DETRESSE.md obligatoire pour tous les praticiens avant la première séance
- Formation simulation de détresse incluse dans le MANUEL_FORMATION_PRATICIENS.md (Module 8, Niveau 2)
- Affichage des ressources de crise dans l'interface client (accessible en tout temps)
- Supervision mensuelle des praticiens avec évaluation de la gestion des situations difficiles

Plan de mitigation :
- Activation immédiate du PROTOCOLE_URGENCE_DETRESSE.md si incident survenu
- Soutien psychologique offert au praticien impliqué (traumatisme vicariant)
- Coordination avec les autorités si nécessaire (911, DPJ)
- Rapport d'incident interne complet dans les 24h
- Consultation juridique immédiate sur la responsabilité
- Communication aux proches du client si légalement requis et autorisé
- Révision du protocole si une lacune est identifiée

Responsable : Praticien concerné → urgence@ivia.quebec → Direction générale → autorités si requis

---

### Fiche G2 — Fuite médiatique ou publication négative

Description :
Un article de presse, un reportage télévisé, ou une publication virale sur les réseaux sociaux dresse un portrait négatif d'IVIA — fondé ou non — sur des questions de sécurité des données, de qualification des praticiens, ou de dérive éthique. Cela peut survenir en lien avec un incident réel ou par désinformation.

| Dimension | Évaluation |
|-----------|-----------|
| Probabilité | Faible (1) |
| Impact | Majeur (3) |
| Score | 3 — Acceptable (préparation requise) |
| Horizon principal | P2–P5 (M4–M27) |

Indicateurs précurseurs :
- Demandes d'information de journalistes à bonjour@ivia.quebec
- Publications négatives sur les réseaux sociaux liées à IVIA (monitoring)
- Client ou praticien mécontent signalant son intention de "rendre la situation publique"
- Commentaires critiques dans des groupes en ligne (Facebook, Reddit, forums spécialisés)

Plan de prévention :
- Transparence proactive dans les communications publiques (charte doctrinale publiée, politique de confidentialité accessible)
- Protocole de communication de crise documenté avant P2
- Désignation d'un porte-parole unique pour les médias (Direction générale)
- Monitoring hebdomadaire des mentions d'IVIA en ligne

Plan de mitigation :
- Réponse publique dans les 24h : factuelle, calme, doctrinalement cohérente
- Correction des faits erronés par voie officielle (communiqué de presse, publication blog)
- Engagement d'un spécialiste en relations publiques de crise si l'ampleur le justifie
- Documentation interne complète de l'incident et des décisions de communication

Responsable : Direction générale / Responsable communications

---

### Fiche G3 — Manquement réputationnel d'un praticien hors IVIA

Description :
Un praticien lié à IVIA est impliqué dans un scandale ou un manquement éthique dans sa vie professionnelle externe (hors IVIA) qui rejaillit sur l'organisation et soulève des questions sur les processus de vérification des antécédents d'IVIA.

| Dimension | Évaluation |
|-----------|-----------|
| Probabilité | Faible (1) |
| Impact | Significatif (2) |
| Score | 2 — Acceptable (vérification préventive suffisante) |
| Horizon principal | P2–P5 (M4–M27) |

Indicateurs précurseurs :
- Signalement public ou médiatique sur un praticien IVIA
- Plainte reçue à doctrinal@ivia.quebec ou praticiens@ivia.quebec concernant un comportement hors-plateforme
- Résultats d'une vérification périodique révélant un changement de statut professionnel (ex. : radiation d'un ordre)

Plan de prévention :
- Vérification des antécédents à l'admission (déclaration d'honneur + vérification des ordres si applicable)
- Clause contractuelle permettant à IVIA de suspendre immédiatement un praticien impliqué dans un incident grave externe
- Processus de vérification annuelle du statut professionnel des praticiens

Plan de mitigation :
- Suspension préventive immédiate du praticien pendant l'enquête interne
- Communication aux clients du praticien concerné (transition vers un autre praticien)
- Résiliation du contrat si les faits sont établis et incompatibles avec les 7 principes
- Communication publique factuelle si l'incident est devenu public

Responsable : Direction générale / Comité d'éthique

---

## 10. Matrice de priorisation 4×4

La matrice suivante positionne chaque risque selon ses deux axes (probabilité et impact). Les identifiants sont placés dans la case correspondant à leur cotation.

```
MATRICE DES RISQUES IVIA — VUE D'ENSEMBLE
═══════════════════════════════════════════════════════════════════════════

                          IMPACT
                 Mineur(1)  Significatif(2)  Majeur(3)   Catastrophique(4)
               ┌──────────┬────────────────┬───────────┬──────────────────┐
PROB.  Élevée  │          │  F1            │  A1       │                  │
    (3)        │          │                │           │                  │
               ├──────────┼────────────────┼───────────┼──────────────────┤
       Moyenne │          │  D3  E3  F3    │  A3  C1   │  E1              │
       (2)     │          │                │  D1  D2   │                  │
               │          │                │  D4       │                  │
               ├──────────┼────────────────┼───────────┼──────────────────┤
       Faible  │          │  B3  G3        │  A2(*)    │  B1(*)  B2(*)    │
       (1)     │          │                │  C2(*)    │  B4(*)  G1(*)    │
               │          │                │  C3  C4   │                  │
               │          │                │  E2  F2   │                  │
               │          │                │  G2       │                  │
               └──────────┴────────────────┴───────────┴──────────────────┘

(*) Score faible en probabilité MAIS impact catastrophique : ces risques exigent
    une préparation maximale malgré leur faible probabilité estimée.

ZONES :
  ████ ROUGE  (10-12) : Action immédiate — aucun dans la configuration actuelle P1
  ░░░░ ORANGE  (7-9)  : Haute priorité — A1, E1, B1
  ░░░░ JAUNE   (4-6)  : Priorité modérée — A3, C1, D1, D2, D4, D3, E3, F1, F3, A2, B2, B3, B4
  ░░░░ VERT    (1-3)  : Surveillance légère — C2, C3, C4, E2, F2, G1, G2, G3
```

---

## 11. Top 10 des risques prioritaires

Classement par score décroissant, avec tiebreak sur la gravité de l'impact.

| Rang | Code | Titre | Score | Horizon | Action prioritaire |
|------|------|-------|-------|---------|-------------------|
| 1 | E1 | Épuisement ou incapacité du fondateur | 8 | P1–P3 | Plan de relève + délégation documentée avant M2 |
| 2 | B1 | Non-conformité Loi 25 / RGPD | 8 | Continu | Audit juridique + RPRP nommé avant lancement P1 |
| 3 | A1 | Dérive doctrinaire sous pression de croissance | 9 | P3–P5 | Comité doctrinal actif + audit annuel |
| 4 | D1 | Sous-financement ou retard de financement | 6 | P1–P3 | Réserve 3 mois + diversification sources |
| 5 | D2 | Échec acquisition / rétention praticiens | 6 | P1–P3 | Programme onboarding + satisfaction mensuelle |
| 6 | D4 | MRR insuffisant pour gate Go/No-Go M6 | 6 | P1–P2 | Tableau de bord hebdomadaire + ajustements rapides |
| 7 | C1 | Panne infrastructure pendant une séance | 6 | P1–P3 | SLA ≥ 99,5 % + canal de repli avant P1 |
| 8 | F1 | Concurrence accélérée plateformes capitalisées | 6 | P3–P5 | Ancrage doctrinal + preuve sociale québécoise |
| 9 | A3 | Dilution mission par extension non encadrée | 6 | P2–P4 | Périmètre strates clair + supervision mensuelle |
| 10 | G1 | Incident grave client (crise suicidaire) | 4* | Continu | Formation urgence + protocole avant toute séance |

(*) G1 est en rang 10 par score brut, mais sa nature humaine lui confère une priorité absolue de préparation. La probabilité faible ne diminue pas l'obligation de préparation maximale.

---

> Note d'attention — Risques à score apparent "faible" mais impact catastrophique
>
> Les risques B1, B2, B4, C2, G1 présentent tous un score brut de 3 ou 4 (probabilité faible × impact catastrophique). Le score numérique sous-estime leur gravité réelle. Pour ces risques, la politique d'IVIA est une préparation maximale inconditionnelle, indépendamment de la probabilité estimée. Leur occurrence, même rare, pourrait mettre fin à IVIA ou mettre en danger des personnes. Ils font l'objet d'un suivi spécial lors de chaque revue trimestrielle.

---

## 12. Plan de revue trimestrielle

### 12.1 Calendrier des revues

| Revue | Date | Responsable | Livrable |
|-------|------|-------------|---------|
| Revue Q1-2026 | 1er août 2026 | Direction générale | Rapport de revue signé |
| Revue Q2-2026 | 1er novembre 2026 | Direction générale + Comité doctrinal | Rapport + mise à jour matrice |
| Revue Q3-2026 | 1er février 2027 | Direction générale + CA OBNL | Rapport + révision cartographie complète |
| Revue Q4-2026 | 1er mai 2027 | Direction générale + CA OBNL | Rapport + plan d'action P4 |

### 12.2 Protocole de revue

Chaque revue trimestrielle comprend les étapes suivantes :

Étape 1 — Collecte des données (J-14 avant la revue) :
- Compilation des incidents survenus depuis la dernière revue
- Collecte des indicateurs précurseurs actifs ou en alerte
- Mise à jour des probabilités si des informations nouvelles justifient un changement de cote

Étape 2 — Analyse en comité (J-7) :
- Examen de chaque risque de rang ORANGE ou ROUGE en détail
- Vérification de l'efficacité des plans de prévention en place
- Identification de nouveaux risques émergents non couverts par la cartographie actuelle

Étape 3 — Mise à jour de la cartographie (J-3) :
- Modification des cotes si justifié
- Ajout de nouveaux risques si identifiés
- Suppression des risques devenus caducs
- Mise à jour du top 10

Étape 4 — Rapport de revue (J+0) :
- Rapport signé par la Direction générale
- Diffusion au CA OBNL et au Comité doctrinal
- Archivage au registre des risques

### 12.3 Critères de révision extraordinaire (hors cycle trimestriel)

Une révision extraordinaire est déclenchée si :
- Un incident de catégorie ROUGE survient (même si la probabilité était évaluée faible)
- Deux indicateurs précurseurs ou plus d'un même risque sont actifs simultanément
- Un changement réglementaire majeur est annoncé (nouvelle loi, règlement)
- Un concurrent lance une offre directement concurrente
- Le fondateur signale un état d'épuisement significatif

### 12.4 Gouvernance de la revue

La cartographie des risques relève du CA OBNL, avec délégation de la gestion courante à la Direction générale. Le Comité doctrinal est impliqué pour tous les risques des catégories A et G. Le Comité d'éthique est impliqué pour les risques B3, E3, G1, G3.

---

## 13. Registre des risques — Vue synthétique

Tableau récapitulatif de tous les risques identifiés, classés par catégorie et score.

| Code | Catégorie | Titre abrégé | Prob. | Impact | Score | Zone | Responsable |
|------|-----------|-------------|-------|--------|-------|------|------------|
| A1 | Doctrinaire | Dérive sous pression croissance | Élevée | Majeur | 9 | ORANGE | Comité doctrinal |
| A2 | Doctrinaire | Compromission par investisseur | Faible | Catastrophique | 4 | JAUNE* | CA OBNL |
| A3 | Doctrinaire | Dilution mission (extension offre) | Moyenne | Majeur | 6 | JAUNE | Comité doctrinal |
| B1 | Juridique | Non-conformité Loi 25 / RGPD | Moyenne | Catastrophique | 8 | ORANGE* | RPRP + DG |
| B2 | Juridique | Conflit ordre professionnel | Faible | Catastrophique | 4 | JAUNE* | DG + Avocat |
| B3 | Juridique | Litige praticien (rémunération/PI) | Moyenne | Significatif | 4 | JAUNE | DG + Comité éthique |
| B4 | Juridique | Incident impliquant mineur | Faible | Catastrophique | 4 | JAUNE* | DG + DPJ |
| C1 | Technique | Panne infra pendant séance | Moyenne | Majeur | 6 | JAUNE | CTO |
| C2 | Technique | Faille sécurité / incident confidentialité | Faible | Catastrophique | 4 | JAUNE* | CTO + RPRP |
| C3 | Technique | Défaillance pipeline J+30 | Faible | Majeur | 3 | VERT | CTO + RPRP |
| C4 | Technique | Perte ou corruption données | Faible | Majeur | 3 | VERT | CTO |
| D1 | Économique | Sous-financement / retard financement | Moyenne | Majeur | 6 | JAUNE | DG + Trésorier |
| D2 | Économique | Échec acquisition praticiens | Moyenne | Majeur | 6 | JAUNE | DG |
| D3 | Économique | Dérive coûts variables | Moyenne | Significatif | 4 | JAUNE | DG + CTO |
| D4 | Économique | MRR insuffisant gate M6 | Moyenne | Majeur | 6 | JAUNE | DG + CA |
| E1 | Opérationnel | Épuisement fondateur | Moyenne | Catastrophique | 8 | ORANGE | CA OBNL |
| E2 | Opérationnel | Départ praticienne pilote | Faible | Majeur | 3 | VERT | DG |
| E3 | Opérationnel | Erreur humaine données/consentements | Moyenne | Significatif | 4 | JAUNE | RPRP + Praticien |
| F1 | Marché | Concurrence plateformes capitalisées | Élevée | Significatif | 6 | JAUNE | DG + Marketing |
| F2 | Marché | Évolution défavorable réglementation | Faible | Majeur | 3 | VERT | DG + Avocat |
| F3 | Marché | Rejet marché envers IA accompagnement | Moyenne | Significatif | 4 | JAUNE | DG + Comité doctrinal |
| G1 | Réputationnel | Incident grave client (crise) | Faible | Catastrophique | 4 | JAUNE* | Praticien + urgence@ |
| G2 | Réputationnel | Fuite médiatique / publication négative | Faible | Majeur | 3 | VERT | DG |
| G3 | Réputationnel | Manquement praticien hors IVIA | Faible | Significatif | 2 | VERT | DG + Comité éthique |

(*) Risques avec score apparent JAUNE mais nature catastrophique — surveillance maximale inconditionnelle.

Légende responsables : DG = Direction générale / CTO = Directeur technique MERLIN inc. / RPRP = Responsable protection renseignements personnels / CA = Conseil d'administration OBNL / DPJ = Direction de la protection de la jeunesse

---

> Note d'attention — Sur la nature dynamique de cette cartographie
>
> Cette cartographie est un outil vivant, non un document figé. Les cotes de probabilité reflètent la réalité de mai 2026 au moment du pilote P1. Certains risques aujourd'hui évalués "faibles" en probabilité pourraient devenir "élevés" à P4 ou P5 (notamment A1, B2, F1). Inversement, des risques élevés en P1 (E1, D2) pourraient se réduire à mesure que l'équipe grandit et que les processus se solidifient. La valeur de ce document réside dans sa révision régulière, pas dans sa consultation ponctuelle.

---

> Note d'attention — Interdépendances entre risques
>
> Plusieurs risques sont liés et peuvent se déclencher en cascade :
> - E1 (épuisement fondateur) peut déclencher D4 (MRR insuffisant) et D2 (perte praticiens)
> - G1 (incident client grave) peut déclencher G2 (fuite médiatique) et B2 (plainte ordre professionnel)
> - C2 (faille sécurité) peut déclencher B1 (non-conformité Loi 25) et G2 (fuite médiatique)
> - A2 (compromission investisseur) peut déclencher A1 (dérive doctrinaire) et G2 (réputationnelle)
> Ces cascades possibles doivent être intégrées dans les exercices de simulation de crise annuels.

---

> Note d'attention — Sur les risques absents de cette cartographie
>
> La présente version 1.0 couvre les risques identifiés à mai 2026. Des catégories de risques non encore modélisées incluent : (a) les risques liés à la santé mentale des praticiens eux-mêmes (traumatisme vicariant à l'échelle — sera pertinent à P3+), (b) les risques géopolitiques (ex. : modifications des réglementations transfrontalières si IVIA s'étend hors Québec), (c) les risques environnementaux (ex. : empreinte carbone des infrastructures IA). Ces catégories feront l'objet d'une intégration dans la version 2.0 (Vague 3).

---

## Annexe — Contacts de référence en cas d'activation d'un plan de mitigation

| Situation | Contact interne | Contact externe |
|-----------|----------------|----------------|
| Urgence client (détresse) | urgence@ivia.quebec | 1 866 APPELLE (277-3553) / 911 |
| Incident technique majeur | immediat@ivia.quebec | CTO MERLIN inc. |
| Incident confidentialité | privacy@ivia.quebec | CAI : 1 888 528-7741 |
| Litige ou plainte ordre | direction@ivia.quebec | Avocat corporatif désigné |
| Épuisement fondateur | CA OBNL (Président) | Directeur de relève désigné |
| Crise médiatique | direction@ivia.quebec | Relationniste de crise (à désigner P2) |
| Signalement LPJ / mineur | urgence@ivia.quebec | DPJ : 514 896-3100 / 1 800 363-9010 |
| Incident doctrinal | doctrinal@ivia.quebec | Comité doctrinal + CA OBNL |

---

Produit dans le cadre de la Vague 2 — Documents structurels IVIA.
Version 1.0 — Mai 2026.

"Au sein de l'être — En actes."

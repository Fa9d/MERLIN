# INDEX — BASE DOCUMENTAIRE IVIA
## Répertoire navigable — Toutes vagues confondues

---

## ⚠️ AVIS DE REFONTE v2.0 — DÉC-V3-15

**Date d'inflexion** : 8 mai 2026
**Décision de référence** : DÉC-V3-15 — *IVIA inc. comme société par actions à mission (SPA-mère LSAQ) maison-mère de l'écosystème ; OBNL satellite (LCQ III) recevant licence sociale pour redistribution gratuit/coût aux publics vulnérables*. Cette décision REMPLACE DÉC-V1-01 (architecture initiale OBNL+MERLIN inc.) qui est désormais marquée RÉVISÉE dans HISTORIQUE_DECISIONS_STRATEGIQUES.md.

**Architecture cible** :
```
David Phaneuf (100%) → IVIA inc. (SPA-mère LSAQ à mission) ──licence sociale──▶ IVIA OBNL (satellite LCQ III)
                       ├─ MERLIN (sous-marque produit bien-être, pilote actif)
                       ├─ MÉSANGE (recentrage politique Québec)
                       ├─ COVOITURAGE (mobilité citoyenne)
                       ├─ LOGISTIQUE PRODUCTEURS
                       ├─ NHL ANALYTICS
                       └─ Futurs projets civiques
```

**Point d'entrée v2.0** : [BILAN_COHERENCE_REFONTE_V2.md](IVIA_BILAN_COHERENCE_REFONTE_v2.0.md) — audit des 8 invariants doctrinaux et juridiques, navigation par profil, prochaines étapes opérationnelles.

**Documents refondus en v2.0** : V1-02 (STRUCTURE_JURIDIQUE), V1-04 (BP_FINANCEMENT_V2), V1-07 (NOTE_CONFIDENTIELLE), V2-01 (GOUVERNANCE_INTERNE), V3-03 (STRATEGIE_MARQUE), V3-06 (MODELE_VALORISATION), V3-10 (CADRE_PI), V3-A1 (PLAN_INTEGRATION_36MOIS).
**Documents patchés en v1.1** : V2-02 (CGU_PRATICIENS), V2-03 (CGU_CLIENTS), V2-04 (CONTRAT_PRATICIEN_TYPE) — entité contractante = IVIA inc. avec clause transition pré-incorporation.
**Charte mise à jour** : V1-01 (CHARTE_DOCTRINAIRE_IVIA) — IVIA maison-mère, principe SPA à mission.
**Documents opérationnels post-refonte** : V3-A3 (BRIEF_AVOCAT), V3-A4 (BRIEF_FISCALISTE), V3-A5 (CABINETS_MONTREAL_SHORTLIST) — pour démarrage mandats consultation P1.
**Archives v1** : BP_FINANCEMENT_V2_v1_archive.md, NOTE_CONFIDENTIELLE_INVESTISSEURS_v1_archive.md, PLAN_INTEGRATION_IVIA_36MOIS_v1_archive.md.

---

**Organisation** : IVIA inc. (SPA-mère LSAQ à mission) — détenue à 100 % par David Phaneuf au lancement / IVIA OBNL (satellite LCQ III, à constituer P2)
**Responsable** : David Phaneuf, Direction générale
**Devises** : *Au sein de l'être — En actes.* / *Pour le peuple, par le peuple.*
**Version** : 2.1 — 8 mai 2026 (refonte DÉC-V3-15 + correction chemins relatifs repo, audit AUDIT_COHERENCE_POST_DEC-V3-15)
**Portée** : 34 documents stratégiques, structurels et opérationnels — Vagues 1, 2 et 3, refonte v2.0 + briefs opérationnels inclus

---

---

## ⚠️ COEXISTENCE DE DEUX SYSTÈMES DÉCISIONNELS

Le repo contient **deux univers décisionnels parallèles**, non-conflictuels mais distincts :

1. **`DEC-XXX` / ADR techniques** — registre des décisions d'architecture technique du produit MERLIN, hérité de la phase pré-DÉC-V3-15 (74 occurrences). Voir `00_GOUVERNANCE/ADR/` et les documents `MERLIN_GOUV_*`. Ces décisions restent valides pour leur portée technique.
2. **`DÉC-V3-X` / Décisions stratégiques IVIA** — registre des décisions doctrinales et structurelles d'IVIA depuis avril-mai 2026 (115 occurrences). Voir `IVIA_HISTORIQUE_DECISIONS_STRATEGIQUES_v2.0.md`. **DÉC-V3-15 est la décision pivot** qui définit l'architecture cible IVIA inc. SPA-mère + OBNL satellite.

En cas d'arbitrage en faveur d'une décision DÉC-V3-X qui contredirait un DEC-XXX antérieur, la décision stratégique IVIA prime et le DEC-XXX est marqué SUPERSEDED dans l'ADR concerné.

## MODE D'EMPLOI DE CET INDEX

Cet index est le point d'entrée unique de la base documentaire IVIA. Il est organisé en six catégories thématiques. Chaque document est identifié par :

- Son numéro de référence (ex. : V1-01)
- Son chemin absolu dans le système de fichiers
- Sa vague de production
- Son nombre de lignes
- Un résumé de deux lignes
- Ses liens croisés vers les documents connexes

Les documents sont classés par ordre de lecture recommandé pour un nouveau membre de l'équipe, un investisseur, ou un praticien entrant. La colonne "Priorité lecture" indique l'ordre d'assimilation recommandé.

---

## CATÉGORIE A — DOCTRINE ET FONDEMENTS

Les documents de cette catégorie constituent le socle immuable d'IVIA. Ils sont non-cessibles, non-modifiables sans procédure doctrinale formelle, et s'imposent à tous les autres documents.

---

### V1-01 — CHARTE_DOCTRINAIRE_IVIA.md

**Chemin** : [`00_GOUVERNANCE/IVIA_CHARTE_DOCTRINAIRE_v2.0.md`](../00_GOUVERNANCE/IVIA_CHARTE_DOCTRINAIRE_v2.0.md)
**Vague** : 1 | **Lignes** : 505 | **Priorité lecture** : 1 (premier document à lire absolument)

**Résumé** : Fondement idéologique et éthique d'IVIA — les 7 principes sacrés, les règles fermes Blocs A et B, la doctrine de monétisation (C.1 à C.3), la gouvernance du Comité doctrinal, et les dispositions d'intégrité structurelle. Toute décision stratégique, contractuelle ou technologique doit se référer à ce document en priorité.

**Liens croisés** : V1-02 (structure), V1-03 (données), V2-01 (gouvernance), V3-01 (multi-strates), V3-10 (PI données)

---

### V1-03 — CHARTE_TRANSFORMATION_GOUVERNEE_DONNEES.md

**Chemin** : [`00_GOUVERNANCE/IVIA_CHARTE_TRANSFORMATION_GOUVERNEE_DONNEES_v1.0.md`](../00_GOUVERNANCE/IVIA_CHARTE_TRANSFORMATION_GOUVERNEE_DONNEES_v1.0.md)
**Vague** : 1 | **Lignes** : 381 | **Priorité lecture** : 2

**Résumé** : Pipeline de transformation des données en 8 étapes, règle d'effacement audio J+30, consentement granulaire à 3 niveaux, droits des clients et des praticiens sur leurs données, cadre de cession des données (jamais le brut, conditions strictes pour le synthétique). Ce document est le pendant technique de la Charte doctrinaire.

**Liens croisés** : V1-01 (doctrine), V2-05 (consentement), V2-02 (CGU praticiens), V3-02 (technologie), V3-10 (PI données)

---

## CATÉGORIE B — STRUCTURE JURIDIQUE ET FINANCEMENT

Les documents de cette catégorie définissent l'architecture légale d'IVIA et ses trajectoires financières.

---

### V1-02 — STRUCTURE_JURIDIQUE_RECOMMANDEE.md

**Chemin** : [`12_JURIDIQUE_AFFAIRES/IVIA_STRUCTURE_JURIDIQUE_RECOMMANDEE_v2.0.md`](../12_JURIDIQUE_AFFAIRES/IVIA_STRUCTURE_JURIDIQUE_RECOMMANDEE_v2.0.md)
**Vague** : 1 | **Lignes** : 426 | **Priorité lecture** : 3

**Résumé (v2.0 — DÉC-V3-15)** : Recommandation IVIA inc. comme SPA-mère LSAQ à mission — structure pivot pour héberger MERLIN (pilote bien-être), MÉSANGE, COVOITURAGE, LOGISTIQUE, NHL ANALYTICS et projets civiques futurs. OBNL satellite LCQ III constitué en P2 (M4-M6) pour recevoir licence sociale et redistribuer gratuit/coût aux publics vulnérables. Séquencement P0-P7, transferts art. 85 LIR, gates G0-G6 contractualisés, coûts révisés.

**Liens croisés** : V1-01 (doctrine), V2-01 (gouvernance), V3-A1 (plan intégration 36 mois), V3-07 (sortie/continuité), V3-10 (PI données)

---

### V1-04 — BP_FINANCEMENT_V2.md

**Chemin** : [`12_JURIDIQUE_AFFAIRES/IVIA_BP_FINANCEMENT_v2.0.md`](../12_JURIDIQUE_AFFAIRES/IVIA_BP_FINANCEMENT_v2.0.md)
**Vague** : 1 | **Lignes** : 655 | **Priorité lecture** : 4

**Résumé (v2.0 — DÉC-V3-15)** : Business plan refondu 1 139 lignes — structure SPA-mère IVIA inc. + OBNL satellite, écosystème multi-produits (MERLIN + MÉSANGE + 4 autres), besoin 2,2 M$ sur 36 mois, mix financement non-dilutif 54,5 % (subventions 41,8 % + crédits remb. 12,7 %) + capital patient 27,3 % + prêts 9,1 % + auto-financement 9,1 %, dilution cumul ≤ 25 %, ARR portfolio M36 médian ~2,1 M$, valorisation médiane M36 ~12 M$ (fourchette 9-15 M$). 7 mécanismes optimisation fiscale détaillés (A à G).
*Archive v1 : BP_FINANCEMENT_V2_v1_archive.md*

**Liens croisés** : V1-05 (plan financement), V1-07 (note investisseurs v2.0), V3-A1 (plan intégration), V3-06 (valorisation v2.0), V3-09 (tarification)

---

### V1-05 — PLAN_FINANCEMENT_DETAILLE.md

**Chemin** : [`12_JURIDIQUE_AFFAIRES/IVIA_PLAN_FINANCEMENT_DETAILLE_v1.0.md`](../12_JURIDIQUE_AFFAIRES/IVIA_PLAN_FINANCEMENT_DETAILLE_v1.0.md)
**Vague** : 1 | **Lignes** : 412 | **Priorité lecture** : 5

**Résumé** : Décomposition des sources de financement palier par palier (P1-P6), sources ciblées avec probabilités et délais, calendrier de décaissement trimestriel, conditions et contreparties, Plans A, B et C selon les scénarios d'adoption.

**Liens croisés** : V1-04 (BP financement), V3-06 (valorisation), V3-07 (sortie/continuité)

---

### V1-06 — POLITIQUE_CONFIDENTIALITE_LOI25.md

**Chemin** : [`12_JURIDIQUE_AFFAIRES/IVIA_POLITIQUE_CONFIDENTIALITE_LOI25_v1.1.md`](../12_JURIDIQUE_AFFAIRES/IVIA_POLITIQUE_CONFIDENTIALITE_LOI25_v1.1.md)
**Vague** : 1 | **Lignes** : 447 | **Priorité lecture** : 6

**Résumé** : Politique de confidentialité complète conforme à la Loi 25 (Québec) et au RGPD — catégories de données, finalités, consentement granulaire, durées de conservation, droits des personnes, sécurité, sous-traitants, transferts hors Québec, RPRP, gestion des incidents, EFVP, mineurs.

**Liens croisés** : V1-03 (charte données), V2-05 (consentement), V3-10 (PI données)

---

### V1-07 — NOTE_CONFIDENTIELLE_INVESTISSEURS.md

**Chemin** : [`12_JURIDIQUE_AFFAIRES/IVIA_NOTE_CONFIDENTIELLE_INVESTISSEURS_v2.0.md`](../12_JURIDIQUE_AFFAIRES/IVIA_NOTE_CONFIDENTIELLE_INVESTISSEURS_v2.0.md)
**Vague** : 1 | **Lignes** : 350 | **Priorité lecture** : 7

**Résumé (v2.0 — DÉC-V3-15)** : Note confidentielle refondue 744 lignes — pitch écosystème innovation civique sous IVIA inc. SPA-mère + OBNL satellite, thèse civique 4 énoncés TH-1 à TH-4, TAM additif multi-produits, moat à 4 couches, traction pilote MERLIN + gates G0-G6, équipe, besoin 2,2 M$, termes tranche 1 600 K$ avec 3 instruments alternatifs (Actions privilégiées / SAFE / Convertible), 18 risques en 5 catégories, multiple investisseur cible 3-5× (médian) à 6-8× (scénario haut) horizon 5-7 ans.
*Archive v1 : NOTE_CONFIDENTIELLE_INVESTISSEURS_v1_archive.md*

**Liens croisés** : V1-04 (BP financement v2.0), V3-06 (valorisation v2.0), V1-08 (pitch deck), V3-A1 (plan intégration)

---

### V1-08 — PITCH_DECK_INVESTISSEURS.md

**Chemin** : [`12_JURIDIQUE_AFFAIRES/IVIA_PITCH_DECK_INVESTISSEURS_v2.0.md`](../12_JURIDIQUE_AFFAIRES/IVIA_PITCH_DECK_INVESTISSEURS_v2.0.md)
**Vague** : 1 | **Priorité lecture** : 8

**Résumé** : Pitch deck investisseurs — version courante v2.0 (26 diapositives, traction production, rendus PDF/HTML dans `12_JURIDIQUE_AFFAIRES/deck/`). Versions v1.0-v1.3 archivées sous `12_JURIDIQUE_AFFAIRES/ARCHIVES/` (2026-07-17).

**Liens croisés** : V1-07 (note investisseurs), V3-06 (valorisation), V3-03 (marque)

---

## CATÉGORIE C — GOUVERNANCE ET OPÉRATIONS

Ces documents régissent le fonctionnement interne d'IVIA, les droits et obligations des parties, et les protocoles d'opération.

---

### V2-01 — GOUVERNANCE_INTERNE_IVIA.md

**Chemin** : [`00_GOUVERNANCE/IVIA_GOUVERNANCE_INTERNE_v2.0.md`](../00_GOUVERNANCE/IVIA_GOUVERNANCE_INTERNE_v2.0.md)
**Vague** : 2 | **Lignes** : 618 | **Priorité lecture** : 9

**Résumé (v2.0 — DÉC-V3-15)** : Gouvernance refondue pour SPA-mère IVIA inc. — Conseil consultatif (non contraignant) + Comité doctrinal (veto sur invariants charte), Direction générale David fondateur, Comité des praticiens, Comité d'éthique, matrice décisionnelle, audit doctrinal annuel. CA OBNL satellite limité à la gouvernance redistributive (sans pouvoir contraignant sur l'écosystème SPA-mère). Articulation licence sociale IVIA inc.→OBNL.

**Liens croisés** : V1-01 (doctrine), V1-02 (structure v2.0), V3-A1 (plan intégration), V3-07 (sortie/continuité)

---

### V2-02 — CGU_PRATICIENS.md

**Chemin** : [`12_JURIDIQUE_AFFAIRES/IVIA_CGU_PRATICIENS_v1.1.md`](../12_JURIDIQUE_AFFAIRES/IVIA_CGU_PRATICIENS_v1.1.md)
**Vague** : 2 | **Lignes** : 487 | **Priorité lecture** : 10

**Résumé (v1.1 — patch DÉC-V3-15)** : CGU praticiens — entité contractante = IVIA inc. (avec clause transition pré-incorporation : David Phaneuf TA → IVIA inc. via art. 85 LIR). MERLIN redéfinie comme sous-marque produit. Strates renommées « catégories d'admission ». OBNL satellite mentionnée comme tiers non-partie aux CGU. Conserve les 15 articles d'origine (formations obligatoires, obligations mutuelles, PI, contribution pipeline, suspension/exclusion, non-sollicitation 24 mois).

**Liens croisés** : V2-04 (contrat type v1.1), V2-08 (manuel formation), V3-08 (bien-être praticiens), V1-02 (structure v2.0)

---

### V2-03 — CGU_CLIENTS.md

**Chemin** : [`12_JURIDIQUE_AFFAIRES/IVIA_CGU_CLIENTS_v1.1.md`](../12_JURIDIQUE_AFFAIRES/IVIA_CGU_CLIENTS_v1.1.md)
**Vague** : 2 | **Lignes** : 394 | **Priorité lecture** : 11

**Résumé (v1.1 — patch DÉC-V3-15)** : CGU clients — entité contractante = IVIA inc. (avec clause transition pré-incorporation David Phaneuf TA → IVIA inc.). MERLIN identifiée comme sous-marque produit bien-être. OBNL satellite mentionnée pour la voie redistributive (clients vulnérables). Conserve les 16 articles (règles A.1-A.5, réservation, annulation, consentements granulaires, limites de confidentialité, PI contenu, comportements interdits, mineurs).

**Liens croisés** : V2-05 (consentement), V2-07 (annulation/remboursement), V1-06 (Loi 25), V1-02 (structure v2.0)

---

### V2-04 — CONTRAT_PRATICIEN_TYPE.md

**Chemin** : [`12_JURIDIQUE_AFFAIRES/IVIA_CONTRAT_PRATICIEN_TYPE_v1.1.md`](../12_JURIDIQUE_AFFAIRES/IVIA_CONTRAT_PRATICIEN_TYPE_v1.1.md)
**Vague** : 2 | **Lignes** : 405 | **Priorité lecture** : 12

**Résumé (v1.1 — patch DÉC-V3-15)** : Contrat-type — partie contractante = IVIA inc. (avec clause transition pré-incorporation David Phaneuf TA → IVIA inc. via art. 85 LIR). MERLIN sous-marque produit. Conserve engagements réciproques, PI, rémunération, non-sollicitation 24 mois, résiliation, 3 annexes (grille tarifaire, calendrier formation, déclaration adhésion doctrinaire).

**Liens croisés** : V2-02 (CGU praticiens v1.1), V3-08 (bien-être), V3-09 (tarification), V1-02 (structure v2.0)

---

### V2-05 — PROTOCOLE_CONSENTEMENT_CLIENT.md

**Chemin** : [`00_GOUVERNANCE/IVIA_PROTOCOLE_CONSENTEMENT_CLIENT_v1.0.md`](../00_GOUVERNANCE/IVIA_PROTOCOLE_CONSENTEMENT_CLIENT_v1.0.md)
**Vague** : 2 | **Lignes** : 411 | **Priorité lecture** : 13

**Résumé** : Protocole de consentement granulaire à 3 niveaux — UX recommandée, modalités de révocation, cas des mineurs, cas de détresse aiguë, documentation des consentements, droits des clients, obligations d'IVIA. Conforme Loi 25 et RGPD.

**Liens croisés** : V1-03 (charte données), V1-06 (Loi 25), V2-03 (CGU clients)

---

### V2-06 — PROTOCOLE_URGENCE_DETRESSE.md

**Chemin** : [`00_GOUVERNANCE/IVIA_PROTOCOLE_URGENCE_DETRESSE_v1.0.md`](../00_GOUVERNANCE/IVIA_PROTOCOLE_URGENCE_DETRESSE_v1.0.md)
**Vague** : 2 | **Lignes** : 359 | **Priorité lecture** : 14

**Résumé** : Protocole urgence détresse à 4 niveaux — signaux d'alerte, ressources de crise québécoises (1 866 APPELLE, 811), procédure de signalement interne, signalement obligatoire LPJ, documentation post-incident, soutien au praticien après un incident de détresse.

**Liens croisés** : V2-08 (manuel formation), V3-08 (bien-être praticiens)

---

### V2-07 — POLITIQUE_ANNULATION_REMBOURSEMENT.md

**Chemin** : [`00_GOUVERNANCE/IVIA_POLITIQUE_ANNULATION_REMBOURSEMENT_v1.0.md`](../00_GOUVERNANCE/IVIA_POLITIQUE_ANNULATION_REMBOURSEMENT_v1.0.md)
**Vague** : 2 | **Lignes** : 223 | **Priorité lecture** : 15

**Résumé** : Politique d'annulation et de remboursement — délais, scénarios côté client / côté praticien / technique, cas spéciaux, traitement Stripe, tableau récapitulatif. Document court mais opérationnellement critique.

**Liens croisés** : V2-03 (CGU clients), V2-02 (CGU praticiens), V3-09 (tarification)

---

### V2-08 — MANUEL_FORMATION_PRATICIENS.md

**Chemin** : [`04_METHODES/IVIA_MANUEL_FORMATION_PRATICIENS_v1.0.md`](../04_METHODES/IVIA_MANUEL_FORMATION_PRATICIENS_v1.0.md)
**Vague** : 2 | **Lignes** : 470 | **Priorité lecture** : 16

**Résumé** : Manuel de formation à 3 niveaux (4h / 12h / 24h cumulative) — 13 modules, exercices de simulation clinique, certification IVIA, obligations de maintien des compétences, protocoles d'évaluation. Document remis à chaque praticien lors de l'onboarding.

**Liens croisés** : V2-02 (CGU praticiens), V2-04 (contrat), V3-08 (bien-être)

---

### V2-09 — MANUEL_OPERATIONS_PILOTE.md

**Chemin** : [`04_METHODES/IVIA_MANUEL_OPERATIONS_PILOTE_v1.0.md`](../04_METHODES/IVIA_MANUEL_OPERATIONS_PILOTE_v1.0.md)
**Vague** : 2 | **Lignes** : 334 | **Priorité lecture** : 17

**Résumé** : Manuel opérationnel du pilote P1 — rituels quotidiens, hebdomadaires, mensuels et trimestriels, rôles David + Mylène + Émilie, procédures d'incidents, communication aux investisseurs, critères Go/No-Go de la porte M6.

**Liens croisés** : V2-10 (risques), V3-01 (multi-strates), V3-07 (sortie/continuité)

---

### V2-10 — CARTOGRAPHIE_RISQUES.md

**Chemin** : [`00_GOUVERNANCE/IVIA_CARTOGRAPHIE_RISQUES_v1.0.md`](../00_GOUVERNANCE/IVIA_CARTOGRAPHIE_RISQUES_v1.0.md)
**Vague** : 2 | **Lignes** : 1 184 | **Priorité lecture** : 18

**Résumé** : Cartographie des risques en 7 catégories (doctrinaires, juridiques, techniques, économiques, opérationnels, marché, réputationnels) — 24 fiches de risque avec probabilité/impact/score/indicateurs/plans, matrice 4×4, top 10 prioritaires, plan de revue trimestrielle. Document le plus volumineux de la Vague 2.

**Liens croisés** : Tous les documents — la cartographie des risques se réfère à chaque strate opérationnelle

---

## CATÉGORIE D — STRATÉGIE ET POSITIONNEMENT

Ces documents définissent les orientations stratégiques pluriannuelles d'IVIA.

---

### V3-01 — STRATEGIE_MULTI_STRATES_DETAILLEE.md

**Chemin** : [`04_METHODES/IVIA_STRATEGIE_MULTI_STRATES_DETAILLEE_v1.0.md`](../04_METHODES/IVIA_STRATEGIE_MULTI_STRATES_DETAILLEE_v1.0.md)
**Vague** : 3 | **Lignes** : 652 | **Priorité lecture** : 19

**Résumé** : Stratégie détaillée des 4 strates (S1 Cœur / S2 Professionnels / S3 Soins / S4 Réseau) — marché adressable S1 = 5 000-9 000 praticiens QC, séquençage M1-M36, synergies inter-strates, règle de non-commission renforcée, modèle de référencement gouverné, objectifs par strate.

**Liens croisés** : V1-04 (BP financement), V3-04 (partenariats), V3-06 (valorisation)

---

### V3-02 — STRATEGIE_TECHNOLOGIQUE_36MOIS.md

**Chemin** : [`04_METHODES/IVIA_STRATEGIE_TECHNOLOGIQUE_36MOIS_v1.0.md`](../04_METHODES/IVIA_STRATEGIE_TECHNOLOGIQUE_36MOIS_v1.0.md)
**Vague** : 3 | **Lignes** : 636 | **Priorité lecture** : 20

**Résumé** : Feuille de route technologique en 3 phases et 4 axes du pipeline — trajectoire de souveraineté (Deepgram vers faster-whisper à M24, OpenAI vers Llama 3.1 8B à M19+), RS&DE projeté 400 000-530 000 $ non-dilutif, RTO < 4h / RPO < 24h, budget par phase.

**Liens croisés** : V1-03 (charte données), V3-10 (PI données), V2-10 (risques C1/C2)

---

### V3-03 — STRATEGIE_MARQUE_COMMUNICATION.md

**Chemin** : [`04_METHODES/IVIA_STRATEGIE_MARQUE_COMMUNICATION_v2.0.md`](../04_METHODES/IVIA_STRATEGIE_MARQUE_COMMUNICATION_v2.0.md)
**Vague** : 3 | **Lignes** : 497 | **Priorité lecture** : 21

**Résumé (v2.0 — DÉC-V3-15)** : Stratégie marque refondue — IVIA = marque ombrelle (SPA-mère + OBNL satellite, signature civique commune *Pour le peuple, par le peuple.*) ; MERLIN, MÉSANGE, COVOITURAGE, LOGISTIQUE, NHL ANALYTICS = sous-marques produits avec identités propres tout en se référant à IVIA. Architecture narrative écosystème innovation civique. Protocole crise à 4 niveaux maintenu. Budget communication ajusté multi-produits.

**Liens croisés** : V3-04 (partenariats), V3-05 (veille concurrentielle), V1-01 (doctrine v2.0), V3-06 (valorisation v2.0)

---

### V3-04 — PLAN_PARTENARIATS_ORDRES.md

**Chemin** : [`04_METHODES/IVIA_PLAN_PARTENARIATS_ORDRES_v1.0.md`](../04_METHODES/IVIA_PLAN_PARTENARIATS_ORDRES_v1.0.md)
**Vague** : 3 | **Lignes** : 519 | **Priorité lecture** : 22

**Résumé** : Plan d'engagement avec les ordres professionnels (OPQ M9, OTSTCFQ M10, OPPQ M11, OCCOQ M12) — 15 réponses aux objections anticipées, modèle de convention-cadre, programme d'ambassadeurs 10-16 praticiens d'ici M18, calendrier précis.

**Liens croisés** : V3-01 (multi-strates S2), V3-03 (marque/communication), V3-05 (veille)

---

### V3-05 — VEILLE_CONCURRENTIELLE_QUEBEC.md

**Chemin** : [`04_METHODES/IVIA_VEILLE_CONCURRENTIELLE_QUEBEC_v1.0.md`](../04_METHODES/IVIA_VEILLE_CONCURRENTIELLE_QUEBEC_v1.0.md)
**Vague** : 3 | **Lignes** : 347 | **Priorité lecture** : 23

**Résumé** : Cartographie concurrentielle au Québec — Acuity (logistique seulement, concurrent faible), GOrendezvous (moyen), Jane App (à surveiller — module IA en développement), BetterHelp (scandale FTC = opportunité IVIA), moat à 5 couches (doctrinal, réglementaire, données, technologique, confiance).

**Liens croisés** : V3-03 (marque), V3-06 (valorisation)

---

### V3-06 — MODELE_VALORISATION_IVIA.md

**Chemin** : [`12_JURIDIQUE_AFFAIRES/IVIA_MODELE_VALORISATION_v2.0.md`](../12_JURIDIQUE_AFFAIRES/IVIA_MODELE_VALORISATION_v2.0.md)
**Vague** : 3 | **Lignes** : 377 | **Priorité lecture** : 24

**Résumé (v2.0 — DÉC-V3-15)** : Modèle valorisation refondu — écosystème multi-produits sous IVIA inc. SPA-mère, somme des valeurs additives (MERLIN ARR M36 ~1,5 M$ + MÉSANGE ~265 K$ + autres ~360 K$ = portfolio ~2,1 M$ médian), valorisation médiane M36 ~12 M$ (fourchette 9-15 M$), scénario haut 18-25 M$. Multiple investisseur 3-5× médian / 6-8× haut horizon 5-7 ans. Valorisation pipeline données + dataset synthétique conservée. Perspective fiducie de mission 2-3 M$ post-M36.

**Liens croisés** : V1-07 (note investisseurs v2.0), V1-08 (pitch deck), V3-07 (sortie/continuité), V1-04 (BP v2.0)

---

### V3-10 — CADRE_PROPRIETE_INTELLECTUELLE_DONNEES.md

**Chemin** : [`12_JURIDIQUE_AFFAIRES/IVIA_CADRE_PROPRIETE_INTELLECTUELLE_DONNEES_v2.0.md`](../12_JURIDIQUE_AFFAIRES/IVIA_CADRE_PROPRIETE_INTELLECTUELLE_DONNEES_v2.0.md)
**Vague** : 3 | **Lignes** : 391 | **Priorité lecture** : 25

**Résumé (v2.0 — DÉC-V3-15)** : Cadre PI refondu sous SPA-mère IVIA inc. — IVIA inc. détient marques (IVIA, MERLIN, MÉSANGE), code, pipeline, datasets synthétiques (cessibles sous conditions Charte). Charte doctrinaire = invariant non-cessible co-gardée par Comité doctrinal. OBNL satellite reçoit licence sociale d'usage (non-exclusive, révocable si non-respect Charte). Dataset brut JAMAIS cessible. Dépôts OPIC (IVIA, MERLIN, MÉSANGE) requis P1-P2 (avant M6). Tableau actifs simplifié sous IVIA inc.

**Liens croisés** : V1-01 (doctrine v2.0), V1-03 (charte données), V3-02 (technologie), V3-07 (sortie), V1-02 (structure v2.0)

---

### V3-A1 — PLAN_INTEGRATION_IVIA_36MOIS.md

**Chemin** : [`12_JURIDIQUE_AFFAIRES/IVIA_PLAN_INTEGRATION_36MOIS_v2.0.md`](../12_JURIDIQUE_AFFAIRES/IVIA_PLAN_INTEGRATION_36MOIS_v2.0.md)
**Vague** : 3 (refonte v2.0) | **Lignes** : 675 | **Priorité lecture** : 25-bis (après V3-10)

**Résumé (v2.0 — DÉC-V3-15)** : Plan d'intégration 36 mois refondu — 8 paliers P0-P7 (P0 mai-août 2026 David TA + DBA REQ ; P1 M0-M3 incorporation IVIA inc. SPA + transfert art. 85 LIR ; P2 M4-M6 OBNL satellite + licence sociale ; P3 M7-M12 pipeline + prép MÉSANGE ; P4 M13-M18 MÉSANGE Beta + dépôt bienfaisance ARC ; P5 M19-M27 covoiturage + Phase 3 IA ; P6 M28-M36 logistique producteurs ; P7 M36+ NHL Analytics + fiducie mission). Gates G0-G6 contractualisés, recrutements échelonnés (équipe cible M36 7-9 personnes), équilibre courant atteint M30-M32.
*Archive v1 : PLAN_INTEGRATION_IVIA_36MOIS_v1_archive.md*

**Liens croisés** : V1-02 (structure v2.0), V1-04 (BP v2.0), V1-07 (note investisseurs v2.0), V2-01 (gouvernance v2.0), V3-06 (valorisation v2.0)

---

### V3-A2 — BILAN_COHERENCE_REFONTE_V2.md

**Chemin** : [`00_GOUVERNANCE/IVIA_BILAN_COHERENCE_REFONTE_v2.0.md`](../00_GOUVERNANCE/IVIA_BILAN_COHERENCE_REFONTE_v2.0.md)
**Vague** : 3 (refonte v2.0) | **Lignes** : 280 | **Priorité lecture** : Point d'entrée v2.0

**Résumé (v2.0 — DÉC-V3-15)** : Bilan global de cohérence après refonte DÉC-V3-15 — audit des 8 invariants doctrinaux et juridiques sur les 11 documents refondus/patchés (8/8 conformes), navigation par profil utilisateur, prochaines étapes opérationnelles (avocat société multi-entités + fiscaliste, TA + DBA REQ, dépôts OPIC marques avant M6). Document à lire en premier pour saisir la nouvelle architecture.

**Liens croisés** : Tous les documents refondus v2.0 + patchés v1.1

---

### V3-A3 — BRIEF_AVOCAT_SOCIETE_MULTIENTITES.md

**Chemin** : [`12_JURIDIQUE_AFFAIRES/IVIA_BRIEF_AVOCAT_SOCIETE_MULTIENTITES_v1.0.md`](../12_JURIDIQUE_AFFAIRES/IVIA_BRIEF_AVOCAT_SOCIETE_MULTIENTITES_v1.0.md)
**Vague** : 3 (opérationnel post-refonte) | **Lignes** : 194 | **Priorité lecture** : Opérationnel immédiat

**Résumé (opérationnel)** : Brief de consultation à envoyer aux cabinets juridiques cibles — contexte écosystème, architecture cible (schéma DAVID → IVIA inc. → OBNL), séquencement P0-P5, **20 questions ciblées** regroupées en 6 blocs (SPA à mission, articulation SPA-OBNL, art. 85 LIR, PI/marques, levée capital, Loi 25), 5 livrables attendus, 10 documents référence internes, profil cabinet recherché. Prêt à envoyer (consultations gratuites/réduites ciblées).

**Liens croisés** : V3-A4 (brief fiscaliste compagnon), V3-A5 (shortlist cabinets), V1-02 (structure v2.0), V1-04 (BP v2.0)

---

### V3-A4 — BRIEF_FISCALISTE.md

**Chemin** : [`12_JURIDIQUE_AFFAIRES/IVIA_BRIEF_FISCALISTE_v1.0.md`](../12_JURIDIQUE_AFFAIRES/IVIA_BRIEF_FISCALISTE_v1.0.md)
**Vague** : 3 (opérationnel post-refonte) | **Lignes** : 241 | **Priorité lecture** : Opérationnel immédiat

**Résumé (opérationnel)** : Brief de consultation pour fiscaliste — **39 questions ciblées** sur les 7 mécanismes d'optimisation A-G (redevance licence, services partagés, RS&DE+CRIC, salaire fractionné, don corporatif, subventions OBNL, contenu éditorial), transfert art. 85 LIR (P1), validation **réforme RS&DE 2026** (plafond 2,1 M$ remboursable) et **nouveau CRIC Québec** (30 % puis 20 %, remboursable, seuil 50 K$). 6 livrables attendus, 7 documents référence internes. Recalibrage chiffré crédits remboursables à obtenir car BP v2.0 sous-estime probablement (CRIC 30 % vs ancien CIR ~14 %).

**Liens croisés** : V3-A3 (brief avocat compagnon), V3-A5 (shortlist cabinets), V1-04 (BP v2.0 sections E et K)

---

### V3-A5 — CABINETS_MONTREAL_SHORTLIST.md

**Chemin** : [`12_JURIDIQUE_AFFAIRES/IVIA_CABINETS_MONTREAL_SHORTLIST_v1.0.md`](../12_JURIDIQUE_AFFAIRES/IVIA_CABINETS_MONTREAL_SHORTLIST_v1.0.md)
**Vague** : 3 (opérationnel post-refonte) | **Lignes** : 228 | **Priorité lecture** : Opérationnel immédiat

**Résumé (opérationnel)** : Shortlist 3+3 cabinets prioritaires Montréal — **avocats** : Delegatus (ex-NOVAlex, B Corp social enterprise), BCF (venture cap + multidisciplinaire), Lavery (programme GO inc. démarrage) ; **fiscalistes** : RCGT (Pascal Perreault RS&DE), KPMG (à jour réforme 2026), Demers Beaulne (taille moyenne agile). Pistes secondaires : Stein Monast, HMD, Juriseo, PwC, Marcil-Lavallée, Sabbagh. **Stratégie d'approche en 4 étapes** (mai-août 2026), 4 questions éthiques discriminantes, budget total cumulé 20-37 K$ pour P1+P2+P3 + OPIC.

**Liens croisés** : V3-A3 (brief avocat), V3-A4 (brief fiscaliste), V1-04 (BP v2.0 — ligne frais juridiques)

---

## CATÉGORIE E — POLITIQUES INTERNES ET DURABILITÉ

Ces documents régissent les politiques opérationnelles assurant la durabilité humaine, financière et doctrinale d'IVIA.

---

### V3-07 — PLAN_SORTIE_CONTINUITE.md

**Chemin** : [`04_METHODES/IVIA_PLAN_SORTIE_CONTINUITE_v1.0.md`](../04_METHODES/IVIA_PLAN_SORTIE_CONTINUITE_v1.0.md)
**Vague** : 3 | **Lignes** : 327 | **Priorité lecture** : 26

**Résumé** : Plan de sortie et de continuité — désignation du directeur de relève obligatoire avant M2 (juillet 2026), bascule 24h/7j/30j, succession doctrinale par Comité + document de transmission avant M12, conditions d'acceptabilité d'une acquisition (adoption de la Charte obligatoire), IPO jugée problématique, vision OBNL pérenne 20 ans.

**Liens croisés** : V2-01 (gouvernance), V3-06 (valorisation), V3-10 (PI données)

---

### V3-08 — POLITIQUE_BIEN_ETRE_PRATICIENS.md

**Chemin** : [`00_GOUVERNANCE/IVIA_POLITIQUE_BIEN_ETRE_PRATICIENS_v1.0.md`](../00_GOUVERNANCE/IVIA_POLITIQUE_BIEN_ETRE_PRATICIENS_v1.0.md)
**Vague** : 3 | **Lignes** : 358 | **Priorité lecture** : 27

**Résumé** : Politique de bien-être des praticiens — définitions TV/FC (traumatisme vicariant/fatigue de compassion), maximum S1 15-20 séances/semaine, 15 min minimum entre séances, supervision de groupe mensuelle entièrement financée, PAE dès P3 (M7), questionnaire IBP trimestriel, règle doctrinal : 3 % minimum des revenus alloués au bien-être, droit de pause sans pénalité.

**Liens croisés** : V2-06 (urgence/détresse), V2-08 (manuel formation), V2-02 (CGU praticiens)

---

### V3-09 — POLITIQUE_TARIFICATION_DYNAMIQUE.md

**Chemin** : [`00_GOUVERNANCE/IVIA_POLITIQUE_TARIFICATION_DYNAMIQUE_v1.0.md`](../00_GOUVERNANCE/IVIA_POLITIQUE_TARIFICATION_DYNAMIQUE_v1.0.md)
**Vague** : 3 | **Lignes** : 324 | **Priorité lecture** : 28

**Résumé** : Politique de tarification dynamique — table pricing_config versionnée PostgreSQL (BACK-011), indexation annuelle IPC (plafond +5 %), déclencheur coûts variables ±15 %, préavis 60 jours praticiens / 30 jours clients, gel tarifaire 3 mois (6 mois si hausse > 15 %), Comité tarifaire (fondateur + rep CA MERLIN + rep OBNL avec veto + observateur praticien).

**Liens croisés** : V1-04 (BP financement), V2-04 (contrat praticien), V3-01 (multi-strates)

---

## CATÉGORIE F — DOCUMENTS TRANSVERSAUX (VAGUE 3 BONUS)

Ces trois documents servent l'ensemble de la base documentaire — navigation, vocabulaire et mémoire institutionnelle.

---

### V3-B1 — INDEX_BASE_DOCUMENTAIRE.md

**Chemin** : [`00_GOUVERNANCE/IVIA_INDEX_BASE_DOCUMENTAIRE_v2.0.md`](../00_GOUVERNANCE/IVIA_INDEX_BASE_DOCUMENTAIRE_v2.0.md)
**Vague** : 3 (bonus) | **Lignes** : ~350 | **Priorité lecture** : Ce document

**Résumé** : Index navigable de l'ensemble de la base documentaire IVIA — 28 documents classés par catégorie, résumé de deux lignes par document, liens croisés, tableaux synoptiques, guide de lecture recommandé par profil d'utilisateur.

---

### V3-B2 — GLOSSAIRE_IVIA.md

**Chemin** : [`00_GOUVERNANCE/IVIA_GLOSSAIRE_v1.0.md`](../00_GOUVERNANCE/IVIA_GLOSSAIRE_v1.0.md)
**Vague** : 3 (bonus) | **Lignes** : ~450 | **Priorité lecture** : Référence permanente

**Résumé** : Glossaire complet de l'univers terminologique IVIA — environ 200 entrées couvrant le vocabulaire doctrinal, technologique, économique, juridique, clinique et organisationnel. Définitions courtes et précises avec renvois aux documents sources.

---

### V3-B3 — HISTORIQUE_DECISIONS_STRATEGIQUES.md

**Chemin** : [`00_GOUVERNANCE/IVIA_HISTORIQUE_DECISIONS_STRATEGIQUES_v2.0.md`](../00_GOUVERNANCE/IVIA_HISTORIQUE_DECISIONS_STRATEGIQUES_v2.0.md)
**Vague** : 3 (bonus) | **Lignes** : ~380 | **Priorité lecture** : Référence et gouvernance

**Résumé** : Journal chronologique des décisions stratégiques fondatrices prises lors des Vagues 1, 2 et 3 — date, contexte, options analysées, décision retenue, justification, documents impactés. Mémoire institutionnelle d'IVIA.

---

## TABLEAUX SYNOPTIQUES

---

### Tableau 1 — Vue d'ensemble par vague

| Vague | Nb documents | Lignes totales | Mots approx. | Objet |
|-------|-------------|----------------|--------------|-------|
| Vague 1 | 8 | 3 633 | 28 833 | Fondements doctrinaux, structure juridique, financement |
| Vague 2 | 10 | 4 885 | 38 711 | Gouvernance, contrats, protocoles, risques |
| Vague 3 (principal) | 10 | 4 428 | ~35 000 | Stratégie, moat, durabilité, politiques |
| Vague 3 (bonus) | 3 | ~1 180 | ~9 000 | Index, glossaire, mémoire institutionnelle |
| **TOTAL** | **31** | **~14 126** | **~111 544** | **Base documentaire complète IVIA** |

---

### Tableau 2 — Documents par priorité d'urgence opérationnelle

| Urgence | Documents | Échéance |
|---------|-----------|----------|
| AVANT M2 (juillet 2026) | V3-07 (relève), V3-02 (DevOps externe) | Juillet 2026 |
| AVANT M4 (septembre 2026) | V2-09 (opérations pilote), V3-03 (marque) | Septembre 2026 |
| AVANT M6 (novembre 2026) | V1-06 (Loi 25), V3-10 (OPIC marque) | Novembre 2026 |
| AVANT M7 (décembre 2026) | V3-04 (partenariats ordres) | Décembre 2026 |
| AVANT M13 (juin 2027) | V3-01 (S2 strate), V3-09 (tarification) | Juin 2027 |
| AVANT M19 (décembre 2027) | V3-02 (transition IA souveraine), V3-10 (PI) | Décembre 2027 |

---

### Tableau 3 — Documents fondamentaux vs opérationnels

| Type | Documents | Modifiabilité |
|------|-----------|--------------|
| Fondamentaux non-cessibles | V1-01, V1-03 | Procédure doctrinale formelle seulement |
| Fondamentaux cessibles (SPA) | V3-02 axes tech, V3-10 code/pipeline | Avec conditions (adoption Charte) |
| Gouvernance | V1-02, V2-01 | CA + Comité doctrinal |
| Opérationnels | V2-09, V2-06, V2-07, V2-08, V3-08, V3-09 | Direction générale |
| Contractuels | V2-02, V2-03, V2-04, V2-05 | Juridique + CA |
| Stratégiques | V3-01, V3-03, V3-04, V3-05, V3-06, V3-07 | CA + fondateur |
| Financiers | V1-04, V1-05, V1-07, V1-08 | CA + investisseurs |

---

### Tableau 4 — Guide de lecture par profil

| Profil | Lecture prioritaire | Lecture secondaire |
|--------|--------------------|--------------------|
| Nouveau praticien | V1-01, V2-08, V2-02, V2-04, V2-06 | V1-06, V2-03, V3-08 |
| Investisseur potentiel | V1-07, V1-08, V3-06, V1-04 | V1-02, V3-01, V3-02 |
| Membre du CA OBNL | V1-01, V2-01, V3-07, V3-10 | V1-03, V3-09, V3-04 |
| Partenaire ordre professionnel | V1-01, V3-04, V2-02, V3-08 | V3-01, V3-03 |
| Auditeur juridique | V1-01, V1-02, V1-06, V2-01, V2-02, V2-03 | V3-10, V2-10 |
| Développeur technique | V1-03, V3-02, V3-10 | V2-10 (fiches C1/C2), V3-09 |
| Journaliste / média | V3-03 (protocole crise), V1-01 | V1-07 (sous embargo) |
| Subventionnaire | V1-04, V1-05, V3-06 | V1-01, V3-01 |

---

## RÈGLES DE MAINTENANCE DE CET INDEX

1. Tout nouveau document produit doit être ajouté à cet index dans les 24 heures suivant sa création.
2. Toute modification substantielle d'un document existant doit mettre à jour son résumé et le comptage de lignes.
3. Les liens croisés doivent être vérifiés lors de chaque révision trimestrielle de la base documentaire.
4. Les tableaux synoptiques (lignes et mots) sont approximatifs et doivent être recalculés à chaque audit annuel.
5. La numérotation V1-XX, V2-XX, V3-XX est permanente — un document retiré conserve son numéro (marqué "ARCHIVÉ").
6. La colonne "Priorité lecture" reflète l'ordre d'assimilation recommandé, non l'importance intrinsèque.

---

"Au sein de l'être — En actes."

---

*Index produit dans le cadre de la Vague 3 — Base documentaire stratégique IVIA*
*Chemin : 00_GOUVERNANCE/IVIA_INDEX_BASE_DOCUMENTAIRE_v2.0.md*
*Version 2.0 — 8 mai 2026 (refonte DÉC-V3-15 — IVIA inc. SPA-mère + OBNL satellite)*
*Pour le peuple, par le peuple.*

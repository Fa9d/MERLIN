# PROGRESSION — VAGUE 2 — Documents structurels IVIA
## Statut global : TERMINÉ

---

**Organisation** : IVIA (OBNL) / MERLIN inc. (SPA)
**Responsable** : David Phaneuf, Direction générale
**Vague** : 2 sur 3 (Ordre 2 — Documents structurels)
**Date de clôture** : 8 mai 2026
**Total produit** : 10 documents / 4 885 lignes / 38 711 mots

---

## RÉSUMÉ EXÉCUTIF — VAGUE 2

### A. Les 10 documents produits — Chemins absolus, lignes et mots

| # | Document | Chemin absolu | Lignes | Mots | Objet synthétique |
|---|----------|--------------|--------|------|------------------|
| 1 | GOUVERNANCE_INTERNE_IVIA.md | /home/user/workspace/GOUVERNANCE_INTERNE_IVIA.md | 618 | 5 160 | Modèle de gouvernance hybride OBNL+SPA : CA OBNL (7 membres), Comité doctrinal (veto), Direction SPA, Comité praticiens, Comité d'éthique, matrice décisionnelle, code de conduite, révision des chartes, résolution des conflits, audit doctrinal annuel, dispositions transitoires |
| 2 | CGU_PRATICIENS.md | /home/user/workspace/CGU_PRATICIENS.md | 487 | 4 318 | Conditions générales des praticiens : 15 articles couvrant l'admission par strate, formations obligatoires, obligations mutuelles, modèles financiers, PI, contribution au pipeline de données, suspension/exclusion/sortie, transition clients, non-sollicitation, force majeure |
| 3 | CGU_CLIENTS.md | /home/user/workspace/CGU_CLIENTS.md | 394 | 3 012 | Conditions générales des clients : 16 articles incluant la description du service, ce qu'IVIA n'est pas (règles A.1–A.5), réservation/annulation, paiement, consentements granulaires 3 niveaux, limites de confidentialité, propriété du contenu, comportements interdits, mineurs |
| 4 | CONTRAT_PRATICIEN_TYPE.md | /home/user/workspace/CONTRAT_PRATICIEN_TYPE.md | 405 | 3 015 | Contrat type signé avec chaque praticien : engagements réciproques, propriété intellectuelle, rémunération, non-sollicitation (24 mois), résiliation, 3 annexes (grille tarifaire, calendrier formation, déclaration d'adhésion doctrinaire) |
| 5 | PROTOCOLE_CONSENTEMENT_CLIENT.md | /home/user/workspace/PROTOCOLE_CONSENTEMENT_CLIENT.md | 411 | 3 018 | Protocole de consentement granulaire 3 niveaux : UX recommandée, modalités de révocation, cas des mineurs, cas de détresse aiguë, documentation des consentements, droits des clients, obligations d'IVIA |
| 6 | PROTOCOLE_URGENCE_DETRESSE.md | /home/user/workspace/PROTOCOLE_URGENCE_DETRESSE.md | 359 | 2 938 | Protocole urgence détresse : 4 niveaux, signaux d'alerte, ressources de crise québécoises (1 866 APPELLE, 811, 514 338-4090, DPJ), procédure de signalement interne, signalement obligatoire LPJ, documentation, soutien post-incident praticien |
| 7 | POLITIQUE_ANNULATION_REMBOURSEMENT.md | /home/user/workspace/POLITIQUE_ANNULATION_REMBOURSEMENT.md | 223 | 1 748 | Politique d'annulation et remboursement : délais, scénarios (côté client / côté praticien / technique), cas spéciaux, traitement Stripe, tableau récapitulatif |
| 8 | MANUEL_FORMATION_PRATICIENS.md | /home/user/workspace/MANUEL_FORMATION_PRATICIENS.md | 470 | 3 695 | Manuel de formation des praticiens : 3 niveaux (4h / 12h / 24h), 13 modules, exercices de simulation, certification IVIA, obligations de maintien des compétences, protocoles d'évaluation |
| 9 | MANUEL_OPERATIONS_PILOTE.md | /home/user/workspace/MANUEL_OPERATIONS_PILOTE.md | 334 | 2 722 | Manuel des opérations du pilote P1 : rituels quotidiens/hebdomadaires/mensuels/trimestriels, rôles David+Mylène+Émilie, procédures d'incidents, communication aux investisseurs, critères Go/No-Go gate M6 |
| 10 | CARTOGRAPHIE_RISQUES.md | /home/user/workspace/CARTOGRAPHIE_RISQUES.md | 1 184 | 9 085 | Cartographie des risques : 7 catégories (doctrinaires, juridiques, techniques, économiques, opérationnels, marché, réputationnels), 24 fiches de risque avec probabilité/impact/score/indicateurs/plans de prévention et mitigation, matrice 4×4, top 10 prioritaires, plan de revue trimestrielle |
| — | TOTAL VAGUE 2 | — | 4 885 | 38 711 | 10 documents structurels couvrant la gouvernance, les droits et obligations, les protocoles opérationnels, et la gestion des risques d'IVIA |

---

### B. Cinq notes d'attention nouvelles (Vague 2)

---

Note d'attention 1 — Risque de surcharge du fondateur (E1 : score 8/12)

L'ensemble de la Vague 2 a révélé que David Phaneuf est le seul responsable désigné dans pratiquement tous les plans de mitigation. La gouvernance hybride est solide sur papier, mais son exécution au pilote repose sur une seule personne. Le MANUEL_OPERATIONS_PILOTE.md, la CARTOGRAPHIE_RISQUES.md (Fiche E1) et la GOUVERNANCE_INTERNE_IVIA.md convergent tous vers la même recommandation urgente : identifier et documenter un directeur de relève avant la fin du mois 2 du pilote. Sans cette mesure, le risque E1 reste le seul risque orange-critique dont la prévention n'est pas encore opérationnalisée.

---

Note d'attention 2 — Tension entre pipeline J+30 et valeur perçue par les praticiens

Plusieurs documents (CGU_PRATICIENS.md, CONTRAT_PRATICIEN_TYPE.md, CHARTE_TRANSFORMATION_GOUVERNEE_DONNEES.md) exigent l'effacement irréversible des enregistrements audio à J+30. Or, des praticiens pourraient percevoir cet effacement comme une perte d'accès à leur propre travail clinique — notamment pour la supervision ou la réflexivité professionnelle. La Vague 2 n'a pas encore développé de mécanisme permettant au praticien d'accéder à une synthèse de son propre travail sans violer le pipeline. Il s'agit d'un angle mort qui devra être traité en Vague 3, possiblement via un "tableau de bord praticien" donnant accès aux signaux structurés (non biométriques) issus de leurs séances.

---

Note d'attention 3 — Ambiguïté sur le statut juridique des praticiens de strate S1

Les CGU_PRATICIENS.md, le CONTRAT_PRATICIEN_TYPE.md et le MANUEL_FORMATION_PRATICIENS.md qualifient les praticiens de "travailleurs autonomes". Cependant, la réalité opérationnelle du pilote (horaires partiellement cadrés, formation obligatoire, protocoles imposés, supervision mensuelle) crée un risque de requalification en lien d'emploi (selon l'art. 2085 C.c.Q. et la jurisprudence Loi sur les normes du travail). En l'absence d'un avis juridique formel sur cette question avant le lancement P1, IVIA assume un risque juridique non coté dans la CARTOGRAPHIE_RISQUES.md Version 1.0. Il est fortement recommandé de faire valider la qualification du statut des praticiens par un avocat spécialisé en droit du travail avant la première séance commerciale.

---

Note d'attention 4 — Absence de mécanisme de révision des CGU pour les clients existants

Les CGU_CLIENTS.md (et dans une moindre mesure les CGU_PRATICIENS.md) prévoient qu'IVIA peut modifier les CGU avec un préavis de 30 jours. Cependant, aucun document de la Vague 2 n'établit une procédure formelle de re-consentement des clients existants lors d'une modification substantielle des conditions de traitement de leurs données (exigé par la Loi 25, art. 13.1 et le RGPD, art. 7(3)). Cette lacune devra être comblée avant P4, au moment où le pipeline de transformation des données évolue vers la synthétisation IA (P5). Un mécanisme de "nouvelle notification de consentement" avec opt-in explicite pour les modifications substantielles doit être planifié.

---

Note d'attention 5 — Absence de politique formelle sur le traumatisme vicariant des praticiens

Le PROTOCOLE_URGENCE_DETRESSE.md et le MANUEL_FORMATION_PRATICIENS.md mentionnent le soutien post-incident pour les praticiens, mais IVIA n'a pas encore de politique formelle sur la prévention et la gestion du traumatisme vicariant (ou fatigue de compassion) à l'échelle. À P3–P5, avec des dizaines de praticiens actifs traitant des situations de détresse régulièrement, l'absence d'un protocole de supervision collective, d'une politique de charge maximale de séances en contexte de détresse, et d'un accès à un service de soutien psychologique pour les praticiens eux-mêmes constitue un risque opérationnel et réputationnel non négligeable. Ce document est recommandé pour la Vague 3.

---

### C. Cinq incohérences ou tensions identifiées avec la Vague 1

---

Tension 1 — Écart entre la vision "plateforme propriétaire" (Vague 1) et la dépendance à des tiers (Vague 2)

Le BP_FINANCEMENT_V2.md (Vague 1) projette un modèle propriétaire à P6 avec un revenu à 1,8 M$ ARR reposant en partie sur un avantage compétitif technologique (modèle IA propriétaire). Pourtant, la CARTOGRAPHIE_RISQUES.md (Fiche C1, C2) révèle qu'au pilote, IVIA est entièrement dépendante de fournisseurs tiers (Stripe, fournisseur audio/vidéo, service de transcription IA externe). Il n'existe aucun document de Vague 2 établissant une feuille de route de réduction de cette dépendance ou une politique de "souveraineté technologique progressive". Cette tension entre la vision propriétaire à long terme et la dépendance opérationnelle à court terme méritera un document stratégique en Vague 3.

---

Tension 2 — Décalage temporel entre le recrutement S2 et la préparation juridique

Le PLAN_INTEGRATION_IVIA_36MOIS.md (Vague 1) prévoit le lancement de la strate S2 (membres d'ordres professionnels) à M13. Cependant, la CARTOGRAPHIE_RISQUES.md (Fiche B2) et le MANUEL_FORMATION_PRATICIENS.md révèlent que la formation des praticiens d'ordres, la communication préventive avec les ordres professionnels, et la validation juridique du périmètre d'exercice n'ont pas encore fait l'objet d'un calendrier précis. La Vague 2 n'a produit aucun document spécifique à S2. Le délai de M13 pourrait être sous-estimé si l'engagement avec les ordres commence seulement à M7–M8.

---

Tension 3 — Ambiguïté sur la propriété des "signaux structurés" entre IVIA OBNL et MERLIN inc.

La CHARTE_TRANSFORMATION_GOUVERNEE_DONNEES.md (Vague 1) définit le pipeline de données mais ne tranche pas explicitement la question de la propriété des signaux structurés (étape 5) et des cas synthétiques (étape 7). La GOUVERNANCE_INTERNE_IVIA.md (Vague 2) attribue à MERLIN inc. la propriété du capital technologique, mais les consentements clients (PROTOCOLE_CONSENTEMENT_CLIENT.md) ne précisent pas si les données transformées appartiennent à l'OBNL, à MERLIN inc., ou restent la propriété intellectuelle collective de la plateforme. Cette ambiguïté devra être résolue dans le pacte d'actionnaires et dans une annexe à la Charte de transformation gouvernée avant P5.

---

Tension 4 — Tarification figée vs. évolution naturelle des coûts variables

Le BP_FINANCEMENT_V2.md (Vague 1) établit une grille tarifaire 3×3 détaillée avec des frais par séance fixes (3,90 $ à 12,90 $). La POLITIQUE_ANNULATION_REMBOURSEMENT.md et les CGU_CLIENTS.md (Vague 2) prévoient une révision tarifaire possible avec préavis de 30 jours. Or, aucun document de Vague 1 ou 2 ne définit de mécanisme d'indexation automatique ou de révision tarifaire structurée liée à l'inflation ou aux coûts variables. La CARTOGRAPHIE_RISQUES.md (Fiche D3) identifie ce risque — mais il n'est pas résolu. À P4–P5, à mesure que les coûts variables augmentent avec le volume, IVIA aura besoin d'une politique tarifaire dynamique documentée.

---

Tension 5 — Gouvernance doctrinale forte, mais mécanisme de renouvellement des membres du Comité doctrinal absent

La CHARTE_DOCTRINAIRE_IVIA.md (Vague 1) établit l'autorité du Comité doctrinal. La GOUVERNANCE_INTERNE_IVIA.md (Vague 2) en précise la composition et les pouvoirs. Cependant, aucun des deux documents ne définit clairement le mécanisme de renouvellement des membres du Comité doctrinal ni les critères de sélection de leur successeur. Le fondateur David Phaneuf est le garant doctrinal de facto à P1 — mais à mesure qu'IVIA grandit, la succession doctrinale devient un enjeu de continuité identitaire. Ce point est mentionné dans la GOUVERNANCE_INTERNE_IVIA.md (section 12, mécanismes transitoires) mais reste incomplet. Un protocole de succession doctrinale formalisé est recommandé pour la Vague 3.

---

### D. Recommandations pour la Vague 3 (Ordre 3 — Documents stratégiques)

Sept documents recommandés, classés par priorité opérationnelle.

---

Recommandation V3-1 — STRATEGIE_COMMUNICATION_CRISE.md (Priorité : HAUTE — avant P2)

Objet : Protocole complet de communication de crise couvrant les scénarios G1 (incident client), G2 (fuite médiatique), et B2 (conflit ordre professionnel). Inclure : porte-parole désigné, gabarits de communiqués de presse, politique de réponse sur les réseaux sociaux, arbre décisionnel "quoi dire / quand / à qui", partenaires médias de référence, exercice de simulation annuel.

Déclencheur : Ce document doit exister avant le premier lancement public (P2, M4).

---

Recommandation V3-2 — POLITIQUE_BIEN_ETRE_PRATICIENS.md (Priorité : HAUTE — avant P3)

Objet : Politique formelle de prévention du traumatisme vicariant et de soutien psychologique des praticiens. Inclure : charge maximale recommandée (nombre de séances/semaine en contexte de détresse), accès à un service de supervision clinique indépendant, politique de "pause doctrine" (droit au retrait temporaire sans pénalité), mécanisme de signalement interne confidentiel, ressources de soutien à la santé mentale pour les praticiens eux-mêmes.

Déclencheur : Doit précéder le recrutement de plus de 5 praticiens actifs (M4–M6).

---

Recommandation V3-3 — PLAN_INTEGRATION_S2_ORDRES_PROFESSIONNELS.md (Priorité : HAUTE — M7 au plus tard)

Objet : Plan détaillé de préparation et de lancement de la strate S2 (membres d'ordres). Inclure : calendrier d'engagement avec l'OPQ, l'OTSTCFQ, et le CMQ; adaptation du MANUEL_FORMATION_PRATICIENS.md pour S2; analyse juridique du chevauchement avec les champs d'exercice réservés; stratégie de communication aux ordres; modèle de partenariat institutionnel.

Déclencheur : Doit commencer à M7 pour un lancement S2 à M13.

---

Recommandation V3-4 — STRATEGIE_TECHNOLOGIQUE_36MOIS.md (Priorité : MOYENNE — avant P4)

Objet : Feuille de route de réduction de la dépendance aux tiers et de développement de la souveraineté technologique. Inclure : évaluation make vs. buy pour chaque composant clé (audio/vidéo, transcription, stockage); jalons de migration vers des solutions plus propriétaires; politique de sécurité des fournisseurs; mécanisme de continuité en cas de défaillance d'un fournisseur clé; budget technologique pluriannuel.

Déclencheur : Avant P4 (M13), moment où la complexité technique augmente significativement avec S2.

---

Recommandation V3-5 — POLITIQUE_TARIFICATION_DYNAMIQUE.md (Priorité : MOYENNE — avant P4)

Objet : Politique formelle de révision et d'indexation tarifaire. Inclure : mécanisme de révision annuelle basé sur l'indice des prix à la consommation (IPC) et l'évolution des coûts variables; processus de communication aux clients et praticiens; clauses de protection des abonnés existants (gel de prix de 6 mois après révision); seuils de déclenchement d'une révision extraordinaire.

Déclencheur : Doit être en place avant la première révision tarifaire anticipée (P3–P4).

---

Recommandation V3-6 — PROTOCOLE_SUCCESSION_DOCTRINALE.md (Priorité : MOYENNE — avant P3)

Objet : Protocole formel de succession et de continuité doctrinale. Inclure : critères de sélection des membres du Comité doctrinal et de leur successeur; mécanisme de transmission de la mémoire institutionnelle; rôle du fondateur fondateur une fois IVIA hors de sa phase pionnière; procédure de "test de cohérence doctrinale" pour les candidats au Comité; garde-fous contre la réinterprétation arbitraire des 7 principes.

Déclencheur : Avant P3, quand l'organisation commence à se professionnaliser au-delà du fondateur.

---

Recommandation V3-7 — CADRE_PROPRIETE_INTELLECTUELLE_DONNEES.md (Priorité : MOYENNE — avant P5)

Objet : Cadre formel de propriété intellectuelle des données transformées. Inclure : définition juridique de la propriété des signaux structurés (étape 5), des cas synthétiques (étape 7), et du modèle propriétaire (étape 8); répartition des droits entre IVIA OBNL et MERLIN inc.; droits résiduels des clients et des praticiens sur leurs données transformées; politique de licences et d'utilisation commerciale des modèles dérivés; articulation avec les consentements granulaires existants.

Déclencheur : Avant P5 (M19), au moment où la synthétisation IA commence.

---

### E. Bilan de la Vague 2

La Vague 2 a produit l'infrastructure documentaire complète permettant à IVIA d'opérer son pilote P1 de manière gouvernée, conforme, et doctrinalement cohérente. Les 10 documents couvrent l'ensemble des couches opérationnelles : gouvernance, droits et obligations des parties, protocoles d'intervention, formation, opérations quotidiennes, et gestion des risques.

Les principaux apports de la Vague 2 sont :

1. Une gouvernance opérationnelle clairement articulée entre l'OBNL et la SPA, avec des mécanismes de veto doctrinal fonctionnels.

2. Un cadre contractuel complet (praticiens et clients) aligné sur les règles fermes Bloc A et les 7 principes.

3. Des protocoles d'intervention pour les situations sensibles (urgences, consentements, annulations) qui honorent le principe "le vivant d'abord".

4. Un manuel de formation et un manuel d'opérations qui transforment la doctrine en pratique quotidienne concrète.

5. Une cartographie des risques qui identifie 24 risques sur 7 catégories, avec des plans d'action opérationnels et un mécanisme de revue trimestrielle.

Les tensions et notes d'attention documentées dans ce résumé ne sont pas des défauts — elles sont les zones de croissance naturelle d'un projet en évolution. Elles constituent la matière première de la Vague 3.

---

"Au sein de l'être — En actes."

---

## SUIVI DE PRODUCTION — JOURNAL DÉTAILLÉ

| # | Document | Statut | Lignes | Mots | Date de clôture |
|---|----------|--------|--------|------|----------------|
| 1 | GOUVERNANCE_INTERNE_IVIA.md | TERMINÉ | 618 | 5 160 | 8 mai 2026 |
| 2 | CGU_PRATICIENS.md | TERMINÉ | 487 | 4 318 | 8 mai 2026 |
| 3 | CGU_CLIENTS.md | TERMINÉ | 394 | 3 012 | 8 mai 2026 |
| 4 | CONTRAT_PRATICIEN_TYPE.md | TERMINÉ | 405 | 3 015 | 8 mai 2026 |
| 5 | PROTOCOLE_CONSENTEMENT_CLIENT.md | TERMINÉ | 411 | 3 018 | 8 mai 2026 |
| 6 | PROTOCOLE_URGENCE_DETRESSE.md | TERMINÉ | 359 | 2 938 | 8 mai 2026 |
| 7 | POLITIQUE_ANNULATION_REMBOURSEMENT.md | TERMINÉ | 223 | 1 748 | 8 mai 2026 |
| 8 | MANUEL_FORMATION_PRATICIENS.md | TERMINÉ | 470 | 3 695 | 8 mai 2026 |
| 9 | MANUEL_OPERATIONS_PILOTE.md | TERMINÉ | 334 | 2 722 | 8 mai 2026 |
| 10 | CARTOGRAPHIE_RISQUES.md | TERMINÉ | 1 184 | 9 085 | 8 mai 2026 |
| — | TOTAL | TERMINÉ | 4 885 | 38 711 | 8 mai 2026 |

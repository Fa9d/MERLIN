# PRD — Module d’Orientation Analytique pour IVIA

## Vue d’ensemble

Ce document décrit le produit d’un module analytique optionnel à intégrer à IVIA, opéré par le noyau MERLIN, et conçu pour soutenir l’orientation, le matching, l’exploitation des ressources, et la mesure de l’impact économique des actions dans l’écosystème.[cite:28]

IVIA est défini comme un écosystème de services dont MERLIN constitue le noyau d’interprétation et d’analyse, tandis que l’administrateur paramètre l’outil et que le praticien l’utilise comme un service.[cite:28] Cette structure rend pertinent un module analytique activable, mesurable et gouverné, sans l’exposer d’emblée comme une simple fonctionnalité de “test”.[cite:28]

## Objectif produit

Le module doit transformer des signaux utilisateurs en aides à l’orientation exploitables par IVIA, MSANGES et MERLIN.[cite:28] L’objectif n’est pas seulement de produire un score ou une visualisation, mais de créer une capacité analytique transversale qui peut être reliée à la prise de rendez-vous, à l’adhésion, au matching, à la recommandation de ressources et aux métriques d’entreprise.[cite:28]

Les objectifs principaux sont les suivants :

- Produire un profil ou une carte de positionnement à partir de modèles activables.[cite:28]
- Enrichir la compréhension du client et du praticien dans une logique d’accompagnement.[cite:28]
- Soutenir les recommandations de parcours, praticiens et ressources.[cite:28]
- Permettre le calcul de l’impact économique de chaque action liée au module.[cite:28]
- Créer une base commune pour intégrer plus tard la transcription, Stripe et d’autres briques opérationnelles au même niveau de mesure.[cite:28]

## Problème à résoudre

IVIA prévoit déjà une interface praticien, une interface client, une interface administrateur, ainsi qu’un modèle de revenus fondé notamment sur l’abonnement mensuel.[cite:28] Sans couche analytique transverse, l’orientation des clients, la lecture des besoins, la personnalisation des ressources et l’évaluation du rendement des parcours restent plus difficiles à standardiser et à mesurer.[cite:28]

Le module doit donc répondre à trois besoins simultanés :

- Besoin d’orientation : aider à mieux diriger un client vers un praticien, une ressource ou un parcours.[cite:28]
- Besoin d’exploitation : rendre les résultats utilisables par les praticiens et les administrateurs dans MERLIN.[cite:28]
- Besoin économique : attribuer un coût, une valeur et un effet mesurable à chaque usage du module.[cite:28]

## Positionnement produit

Le produit est un **module optionnel** et non un élément constitutif obligatoire de l’expérience initiale. Il doit être présenté comme une couche d’aide à la compréhension et à l’orientation, et non comme une promesse d’étiquetage définitif de la personne.[cite:28]

Le nom produit provisoire recommandé est **Module d’Orientation Analytique**. Ce nom reste suffisamment large pour accueillir plus tard plusieurs familles de modèles sans figer trop tôt la nature du système.[cite:28]

## Utilisateurs cibles

| Acteur | Rôle dans le module | Besoin principal |
|---|---|---|
| Administrateur | Active les modèles, règle les seuils, décide des usages, contrôle les métriques.[cite:28] | Gouvernance, conformité, rentabilité. |
| Praticien | Consulte les résultats, ajoute éventuellement des observations, exploite les profils dans l’accompagnement.[cite:28] | Lecture utile, gain de temps, meilleure orientation. |
| Client | Remplit une évaluation, consulte une synthèse autorisée, reçoit des recommandations. | Compréhension, orientation, accès au bon accompagnement. |

## Hypothèses produit

Le module repose sur les hypothèses suivantes :

1. Un module d’orientation augmente le taux de prise de rendez-vous après l’onboarding.
2. Un meilleur matching améliore la conversion client-praticien.
3. Une restitution lisible augmente l’engagement dans les ressources et les parcours.
4. L’usage du module peut justifier un upsell, une adhésion ou une meilleure rétention.
5. Une instrumentation complète permet de mesurer ces effets sans attendre la version finale du modèle analytique.

Ces hypothèses devront être validées par expérimentation produit et instrumentation événementielle dès le MVP.[cite:28]

## Cas d’usage du MVP

Le MVP doit rester resserré afin d’éviter une dispersion méthodologique trop tôt dans le projet. Les cas d’usage prioritaires sont les suivants :

### 1. Profil initial d’accueil

Le client complète un module court au moment de son arrivée sur la plateforme. Le résultat génère une première synthèse utile pour l’orientation.[cite:28]

### 2. Aide au matching

Le système réutilise certains signaux issus du profil pour recommander un praticien, un type de rendez-vous ou une ressource pertinente.[cite:28]

### 3. Lecture praticien

Le praticien accède à une synthèse courte avant une première rencontre ou en amont d’une phase d’accompagnement.[cite:28]

### 4. Recommandation de ressources

Le profil influence les ressources proposées : articles, guides, formulaires d’accompagnement ou parcours documentaires, ce qui correspond directement à la logique d’adhésion et d’accès aux contenus décrite dans IVIA.[cite:28]

### 5. Tableau de bord économique minimal

L’administrateur visualise les taux de complétion, les coûts unitaires, les conversions associées et les revenus attribuables au module.[cite:28]

## Ce qui n’entre pas dans le MVP

Les éléments suivants doivent être explicitement exclus de la première version :

- Multiples modèles analytiques en concurrence.
- Recalcul automatique à partir de transcription.
- Scoring adaptatif complexe ou auto-apprenant.
- Benchmarks inter-populations.
- Automatisations marketing avancées basées sur les profils.
- Exploitation d’un profil sans consentement explicite.

## Exigences fonctionnelles

### Gestion des modèles

Le système doit permettre à l’administrateur de :

- Créer ou activer un modèle analytique.
- Versionner chaque modèle.
- Définir les usages autorisés du modèle.
- Régler les seuils de restitution et les niveaux de visibilité.
- Désactiver un modèle sans supprimer l’historique associé.[cite:28]

### Collecte de données

Le système doit permettre de collecter des signaux depuis :

- Questionnaire client.
- Auto-positionnement.
- Observation praticien.
- Historique de parcours numérique.
- Transcription, ultérieurement, dans un cadre séparé et consenti.[cite:28]

### Génération de profil

Le système doit :

- Calculer un résultat structuré à partir d’un modèle donné.
- Produire une forme brute exploitable par machine.
- Produire une synthèse lisible pour le client.
- Produire une synthèse plus détaillée pour le praticien.
- Conserver la version du modèle utilisée pour chaque résultat.

### Restitution

Le système doit distinguer trois niveaux de restitution :

| Vue | Contenu |
|---|---|
| Client | Synthèse courte, axes dominants, pistes de compréhension, recommandations autorisées. |
| Praticien | Synthèse détaillée, contexte d’obtention, historique, observations complémentaires. |
| Admin | Modèles actifs, performance d’usage, coûts, conversions, impact métier. |

### Exploitation produit

Le système doit permettre d’utiliser le profil pour :

- Recommander un praticien.
- Suggérer des ressources.
- Déclencher un parcours d’accompagnement.
- Mesurer les effets du profil sur la prise de rendez-vous, l’adhésion et l’engagement.[cite:28]

## Exigences non fonctionnelles

- Traçabilité complète des événements liés au module.
- Séparation claire entre modèle, résultat, synthèse et usage business.
- Conservation des versions de modèles.
- Consentement explicite avant exploitation côté client.
- Journalisation de l’usage des profils dans les recommandations.
- Gouvernance centralisée par l’administrateur dans MERLIN.[cite:28]

## Architecture cible

Le module doit être conçu comme un composant transverse branché à MERLIN plutôt qu’une simple interface autonome.[cite:28]

### Services recommandés

| Service | Rôle |
|---|---|
| Assessment Service | Gère les questionnaires, formulaires et consentements. |
| Profiling Engine | Applique le modèle analytique actif aux données collectées. |
| Insight Service | Produit les synthèses client, praticien et admin. |
| Matching Service | Réutilise les signaux pour orienter praticiens, ressources ou parcours. |
| Economics Service | Calcule les coûts, les revenus attribués et les effets métier. |
| Model Registry MERLIN | Référence les modèles, versions, règles d’usage et activation admin.[cite:28] |

## Modèle de données

### Objet `analysis_model`

- `model_id`
- `name`
- `version`
- `category`
- `input_types`
- `enabled`
- `audience`
- `consent_required`
- `economic_tracking_enabled`
- `created_at`
- `archived_at`

### Objet `assessment_session`

- `session_id`
- `user_id`
- `model_id`
- `started_at`
- `completed_at`
- `completion_rate`
- `source`
- `consent_status`

### Objet `profile_result`

- `result_id`
- `session_id`
- `model_id`
- `score_payload`
- `summary_short`
- `summary_practitioner`
- `summary_client`
- `generated_at`
- `valid_until`

### Objet `economic_trace`

- `trace_id`
- `event_name`
- `user_id`
- `session_id`
- `direct_cost`
- `allocated_cost`
- `attributed_revenue`
- `expected_value`
- `currency`
- `timestamp`

## Événements à instrumenter

Le module doit être pensé en logique événementielle afin de pouvoir calculer l’impact économique de chaque action. Les événements minimums recommandés sont les suivants :

### Événements produit

- `analysis_module_enabled`
- `assessment_started`
- `assessment_completed`
- `profile_generated`
- `profile_viewed_client`
- `profile_viewed_practitioner`
- `match_generated_from_profile`
- `match_accepted`
- `resource_recommended_from_profile`
- `resource_opened_from_profile`
- `booking_started_after_profile`
- `booking_completed_after_profile`
- `profile_recomputed`
- `subscription_upgraded_after_analysis`

### Événements financiers

- `analysis_cost_booked`
- `transcription_cost_booked`
- `payment_captured_stripe`
- `refund_issued`
- `commission_recorded`
- `ltv_update`

## Logique économique

Le module doit être gouverné comme une capacité analytique **comptable**. Chaque usage doit pouvoir être rattaché à un coût et à un effet attendu ou observé.[cite:28]

### Coûts à mesurer

- Coût direct de calcul du profil.
- Coût direct de traitement IA éventuel.
- Coût direct de stockage et d’archivage.
- Quote-part de support.
- Quote-part de maintenance et produit.

### Revenus ou valeurs à attribuer

- Abonnement déclenché ou maintenu.
- Upgrade d’adhésion.
- Prise de rendez-vous.
- Commission sur séance ou service.
- Engagement accru dans les ressources.
- Amélioration de la rétention client et praticien.

## KPIs principaux

| KPI | Définition |
|---|---|
| Assessment completion rate | Pourcentage des sessions commencées terminées. |
| Profile-to-booking conversion | Part des profils générés menant à une prise de rendez-vous. |
| Profile-to-subscription conversion | Part des profils menant à une adhésion ou un upgrade. |
| Cost per completed profile | Coût moyen complet par profil complété. |
| Revenue per profiled user | Revenu moyen généré par les usagers profilés. |
| Retention lift | Différence de rétention entre usagers profilés et non profilés. |
| Practitioner utilization rate | Part des praticiens utilisant la vue analytique. |
| Recommendation acceptance rate | Part des recommandations issues du profil effectivement suivies. |

## Formules de référence

- Coût complet d’un profil = coût direct + quote-part de coûts indirects.
- Valeur moyenne par profil = revenus attribués / nombre de profils complétés.
- ROI du module = (revenus attribués - coûts complets) / coûts complets.
- Lift de conversion = conversion du groupe avec module - conversion du groupe sans module.
- Payback period = coûts cumulés / revenus incrémentaux mensuels.

## Gouvernance

La gouvernance du module doit respecter la logique IVIA-MERLIN dans laquelle l’administrateur paramètre les cadres, forme les praticiens et structure les usages du service.[cite:28]

Règles de gouvernance recommandées :

- Aucun modèle n’entre en production sans version et documentation.
- Aucun résultat visible au client sans consentement explicite.
- Aucun score utilisé en recommandation sans journalisation de l’usage.
- Aucune exploitation économique sans rattachement à une trace d’événement.
- Toute synthèse client doit rester prudente, lisible et non déterministe.
- Toute exploitation de transcription doit être activée séparément.[cite:28]

## Parcours utilisateur cibles

### Parcours client

1. Le client arrive sur la plateforme.
2. Le système propose le module d’orientation en option.
3. Le client consent et remplit le questionnaire.
4. Le système génère un profil.
5. Une synthèse client est affichée.
6. Une recommandation de praticien ou de ressource est proposée.
7. Le parcours et les actions associées sont mesurés économiquement.

### Parcours praticien

1. Le praticien reçoit ou consulte un profil généré.
2. Il visualise une synthèse interprétable.
3. Il utilise l’information dans l’orientation ou la préparation de séance.
4. Son usage est tracé pour mesurer l’adoption et l’utilité métier.

### Parcours admin

1. L’administrateur active un modèle.
2. Il définit les niveaux de visibilité et les règles de consentement.
3. Il suit les taux de complétion, les coûts, les conversions et les revenus attribués.
4. Il compare les performances du module avec d’autres briques comme Stripe, la transcription ou la prise de rendez-vous.[cite:28]

## Plan de déploiement

### Phase 1 — Instrumentation

Objectif : installer le registre de modèles, les objets de données, les consentements et les événements économiques.

### Phase 2 — Usage praticien et admin

Objectif : limiter d’abord l’exposition client, tester la valeur opérationnelle pour les praticiens et la gouvernance admin.

### Phase 3 — Restitution client

Objectif : rendre visible une synthèse client et mesurer son effet sur conversion, engagement et orientation.

### Phase 4 — Optimisation business

Objectif : comparer les modèles activables et arbitrer selon coût, adoption, conversion et rétention.

## Critères de succès du MVP

Le MVP sera considéré comme valide si les conditions suivantes sont réunies :

- Le module fonctionne avec un modèle activable versionné.
- Les consentements sont correctement capturés.
- Les profils sont générés et consultables par les rôles autorisés.
- Les événements d’usage et de coût sont journalisés de bout en bout.
- Le tableau de bord permet de suivre au minimum complétion, coût unitaire, conversion vers rendez-vous et revenu attribué.
- Une première hypothèse de valeur business peut être confirmée ou infirmée à partir des données collectées.

## Risques principaux

| Risque | Description | Réponse recommandée |
|---|---|---|
| Risque méthodologique | Choisir trop tôt un modèle analytique inadapté. | Séparer framework, modèle et usage métier. |
| Risque de surpromesse | Donner au profil un statut trop déterministe. | Restitutions prudentes et non absolues. |
| Risque produit | Ajouter de la friction dans l’onboarding. | Garder le module optionnel et court au MVP. |
| Risque économique | Coût de calcul supérieur à la valeur créée. | Instrumentation économique dès V1. |
| Risque de gouvernance | Exploitation floue par praticiens ou admin. | Versioning, journalisation, règles d’usage. |

## Décisions à prendre ensuite

Après validation de ce PRD, les décisions suivantes devront être arbitrées :

1. Choix du premier modèle analytique à activer.
2. Longueur du questionnaire initial.
3. Niveau exact de restitution côté client.
4. Logique de matching à connecter en premier.
5. Place du module dans l’onboarding et la prise de rendez-vous.
6. Règles d’attribution économique retenues pour le dashboard métier.

## Conclusion

Le Module d’Orientation Analytique doit être traité comme une brique transverse de MERLIN et non comme un simple quiz. Son intérêt stratégique pour IVIA réside dans sa capacité à relier compréhension, orientation, usage praticien, recommandation de ressources et comptabilité économique des actions au sein de l’écosystème.[cite:28]

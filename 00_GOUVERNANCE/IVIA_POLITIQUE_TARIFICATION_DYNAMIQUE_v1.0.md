# POLITIQUE DE TARIFICATION DYNAMIQUE — IVIA / MERLIN
## Architecture, règles d'indexation, procédures de modification et grandfathering

**Version** : 1.0 — Vague 3
**Date** : Mai 2026
**Statut** : Document opérationnel — Opposable aux praticiens, clients et investisseurs
**Auteur** : David Phaneuf (fondateur) + Perplexity Computer
**Cohérence** : Aligné avec BP_FINANCEMENT_V2.md, CHARTE_DOCTRINAIRE_IVIA.md (Principe 3, C.2), CGU_PRATICIENS.md, CGU_CLIENTS.md

---

## PRÉAMBULE

### La tarification comme signal stratégique

La tarification chez IVIA n'est pas une variable d'ajustement que l'on modifie pour optimiser la marge à court terme. C'est un signal stratégique : elle communique la valeur créée, elle honore le Principe 3 (les lois de l'échange), et elle affecte directement la relation de confiance avec les praticiens.

Trois principes gouvernent la tarification IVIA.

**Principe 1 — La transparence totale** : les prix sont publics, les règles d'évolution sont publiques, les préavis sont respectés sans exception.

**Principe 2 — L'équité des échanges** : les tarifs sont corrélés à la valeur réellement créée. La dégressivité au volume est fondée sur des économies d'échelle vérifiables. Aucun tarif ne constitue une extraction dissimulée.

**Principe 3 — La stabilité prévisible** : les praticiens construisent leur pratique sur la base des tarifs IVIA. Des modifications fréquentes ou imprévisibles minent leur capacité à planifier. La règle d'indexation annuelle prévisible est une garantie de stabilité.

---

## PARTIE I — ARCHITECTURE DE LA TARIFICATION DYNAMIQUE

### 1.1 Principe technique : la table pricing_config versionnée

L'ensemble des paramètres tarifaires d'IVIA est stocké dans une table `pricing_config` en base de données PostgreSQL, distincte du code applicatif. Cette architecture permet de modifier les tarifs via l'interface admin (BACK-011) sans redéploiement du code.

**Structure de la table pricing_config**

```sql
CREATE TABLE pricing_config (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  version VARCHAR(20) NOT NULL,        -- ex. "2026-Q3-v1"
  effective_date DATE NOT NULL,         -- Date d'entrée en vigueur
  created_at TIMESTAMP DEFAULT NOW(),
  created_by VARCHAR(100) NOT NULL,     -- Identifiant de l'administrateur
  approved_by VARCHAR(100),             -- Identifiant du validateur
  approval_date TIMESTAMP,
  change_type VARCHAR(50) NOT NULL,     -- "indexation_annuelle" | "ajustement_couts" | "ajustement_marche" | "experimental"
  justification TEXT NOT NULL,          -- Justification écrite obligatoire
  praticien_notified_date TIMESTAMP,    -- Date d'envoi des préavis praticiens
  client_notified_date TIMESTAMP,       -- Date d'envoi des préavis clients
  is_active BOOLEAN DEFAULT FALSE,      -- Activé uniquement après validation
  config_json JSONB NOT NULL            -- Contenu complet de la configuration tarifaire
);
```

**Audit immuable** : toute modification de la table `pricing_config` est journalisée de façon immuable dans le log d'audit. Aucune suppression ou modification d'un enregistrement historique n'est possible.

### 1.2 Paramètres configurables

**Matrice 3×3 praticiens** (3 plans × 3 paliers de volume)

La matrice 3×3 définit le coût par séance selon le plan (Essentiel / Standard / Premium) et le palier de volume mensuel (Petit / Régulier / Grand).

| | Plan Essentiel | Plan Standard | Plan Premium |
|---|---|---|---|
| Palier Petit (< 20 séances/mois) | Coût/séance : paramétrable | Coût/séance : paramétrable | Coût/séance : paramétrable |
| Palier Régulier (20-50 séances/mois) | Coût/séance : paramétrable | Coût/séance : paramétrable | Coût/séance : paramétrable |
| Palier Grand (> 50 séances/mois) | Coût/séance : paramétrable | Coût/séance : paramétrable | Coût/séance : paramétrable |

**Valeurs actuelles (mai 2026 — Version 1.0)**

| | Plan Essentiel | Plan Standard | Plan Premium |
|---|---|---|---|
| Palier Petit | 5,90 $/séance | 8,90 $/séance | 12,90 $/séance |
| Palier Régulier | 4,90 $/séance | 7,90 $/séance | 11,90 $/séance |
| Palier Grand | 3,90 $/séance | 6,90 $/séance | 9,90 $/séance |

**Abonnements mensuels fixes**

En parallèle ou en complément des frais par séance, des abonnements mensuels fixes peuvent être configurés pour certains services ou strates.

| Abonnement | Valeur actuelle | Description |
|---|---|---|
| IVIA Cœur Mensuel (Essentiel) | 49 $/mois | Accès à la plateforme + 5 séances incluses |
| IVIA Cœur Mensuel (Standard) | 79 $/mois | Accès + 10 séances incluses + analyses étendues |
| IVIA Professionnels (S2) | +30 $/mois | Supplément modules ordres (à venir à M13) |
| Annuaire IVIA Réseau (S4) | 300-500 $/an | Inscription partenaire (à venir à M30) |

**Services à la carte**

| Service | Valeur actuelle |
|---|---|
| Analyse approfondie (rapport complet) | 2,90 $ de plus/séance |
| Historique multi-séances (format PDF exportable) | Inclus dans Standard et Premium |
| Dossier suivi praticien S2 (module ordres) | Inclus dans supplément S2 |

**Paliers de volume — Seuils de déclenchement**

Les seuils définissant les paliers Petit/Régulier/Grand sont aussi paramétrables :

| Paramètre | Valeur actuelle |
|---|---|
| Seuil Petit/Régulier | 20 séances/mois |
| Seuil Régulier/Grand | 50 séances/mois |

---

## PARTIE II — RÈGLES D'INDEXATION DES PRIX

### 2.1 Indexation IPC Québec — Annuelle

**Règle** : les tarifs IVIA sont indexés annuellement selon l'Indice des prix à la consommation (IPC) publié par Statistique Canada, série Québec, mesure d'ensemble.

**Formule** :
Nouveau tarif = Tarif actuel × (IPC année n / IPC année n-1)

**Arrondi** : au 0,10 $ le plus proche (vers le haut).

**Plafond d'indexation annuelle** : +5 %. Si l'IPC dépasse 5 % en une année, l'indexation est limitée à +5 %. L'excédent peut être récupéré l'année suivante selon les mêmes règles.

**Calendrier** : l'indexation entre en vigueur au 1er janvier de chaque année. Les préavis (60 jours pour les praticiens) sont envoyés au plus tard le 1er novembre de l'année précédente.

**Exemple** : si l'IPC Québec augmente de 3,2 % en 2026-2027, un tarif de 5,90 $/séance devient 6,09 $/séance → arrondi à 6,10 $/séance.

**Fondement doctrinal** : l'indexation IPC est une obligation contractuelle envers les praticiens et les clients. Elle n'est pas une décision discrétionnaire de la direction — c'est une règle automatique. Cette automaticité est transparente et prévisible.

### 2.2 Ajustement coûts variables — Seuil ±15 %

**Contexte** : les coûts variables d'IVIA incluent les frais de transcription (Deepgram), les frais IA (OpenAI, Anthropic), les frais d'hébergement (OVH), et les frais de paiement (Stripe). Ces coûts varient avec le volume et avec les décisions des fournisseurs.

**Règle** : si les coûts variables par séance augmentent de plus de 15 % par rapport à la baseline de référence, une révision tarifaire extraordinaire peut être déclenchée, indépendamment du calendrier d'indexation annuel.

**Baseline de référence** : les coûts variables par séance sont calculés et documentés à chaque début de trimestre. La baseline est la moyenne des 4 derniers trimestres.

**Plafond de l'ajustement coûts variables** : l'ajustement ne peut pas dépasser +10 % des tarifs existants en une seule révision.

**Seuil de baisse** : si les coûts variables baissent de plus de 15 %, une révision à la baisse est possible (mais non obligatoire si elle compromet l'équilibre financier).

**Validation requise** : un ajustement coûts variables requiert la validation du Comité tarifaire (voir Partie III).

### 2.3 Ajustement marché — Revue trimestrielle

**Contexte** : le positionnement tarifaire d'IVIA doit rester compétitif face aux alternatives disponibles pour les praticiens. Si un concurrent introduit une offre significativement moins chère avec des fonctionnalités comparables, IVIA peut envisager un ajustement.

**Règle** : une revue comparative des tarifs concurrents est effectuée chaque trimestre. Si un ajustement est jugé nécessaire :
- La direction commerciale propose une modification
- Le Comité tarifaire valide ou rejette
- Les praticiens reçoivent un préavis de 60 jours

**Garde-fou doctrinal** : un ajustement à la baisse de plus de 20 % sur un plan donné doit être évalué au regard de son impact sur la viabilité financière d'IVIA. La règle du plan Essentiel s'applique : "le plan Essentiel ne doit jamais se dégrader en dessous d'un service réellement utile au praticien" (Charte doctrinaire C.2). Un plan Essentiel bradé jusqu'à l'inutilité est une violation doctrinaire.

---

## PARTIE III — PROCÉDURE DE MODIFICATION TARIFAIRE

### 3.1 Qui propose

La proposition de modification tarifaire émane de :
- La direction commerciale (ou le fondateur au stade actuel)
- Le Comité de gouvernance de MERLIN inc.
- Le fondateur en cas de modification urgente (coûts variables dépassant le seuil)

**Format de la proposition** : document structuré incluant :
1. Type de modification (indexation / coûts variables / marché / expérimental)
2. Tarifs actuels et tarifs proposés (tableau comparatif)
3. Justification quantitative (données à l'appui)
4. Impact estimé sur les revenus (calcul de l'ARR avant/après)
5. Impact estimé sur les praticiens (nombre de praticiens affectés, variation mensuelle)
6. Calendrier proposé (date d'entrée en vigueur, dates de préavis)

### 3.2 Qui valide — Comité tarifaire

**Composition du Comité tarifaire**

| Membre | Rôle | Instance |
|---|---|---|
| Fondateur (ou PDG) | Voix délibérative | MERLIN inc. |
| Représentant du conseil MERLIN inc. | Voix délibérative | MERLIN inc. |
| Représentant du conseil OBNL | Voix délibérative (veto doctrinal) | OBNL IVIA |
| Observateur praticiens (ambassadeur) | Voix consultative | Praticiens actifs |

**Règle de décision** : consensus préféré. En cas de désaccord, vote à la majorité simple. En cas de vote partagé, le représentant OBNL a voix prépondérante sur les questions doctrinales.

**Délai de validation** : le Comité tarifaire se réunit dans les 10 jours ouvrables suivant le dépôt d'une proposition. En cas d'urgence (dépassement du seuil coûts variables), réunion dans les 3 jours ouvrables.

### 3.3 Préavis aux praticiens

**Délai minimum** : 60 jours avant entrée en vigueur de toute modification tarifaire.

**Contenu du préavis** :
1. Résumé clair de la modification (tarifs avant/après pour leur situation spécifique)
2. Justification (type de modification + raison)
3. Date d'entrée en vigueur
4. Rappel de la politique de grandfathering si applicable
5. Droit de résiliation (avec délai de résiliation sans pénalité)

**Canal** : courriel direct au praticien + notification dans l'interface praticien MERLIN.

### 3.4 Préavis aux clients

**Délai minimum** : 30 jours avant entrée en vigueur de toute modification tarifaire affectant les clients.

**Contexte** : les clients ne paient pas directement IVIA dans le modèle actuel (les praticiens paient IVIA). Mais si un modèle de facturation directe aux clients est introduit dans une strate future, ce délai s'applique.

**Contenu du préavis** :
1. Résumé de la modification en langage simple
2. Impact sur leur tarification (si applicable)
3. Date d'entrée en vigueur
4. Droit de résiliation

---

## PARTIE IV — GRANDFATHERING

### 4.1 Définition

Le grandfathering désigne la protection des praticiens et clients existants contre les modifications tarifaires pendant une période définie. Un praticien grandfatheré conserve ses tarifs actuels pendant la période garantie, même si les tarifs généraux ont augmenté.

### 4.2 Règles de grandfathering

**Pour les praticiens actifs lors d'une modification tarifaire ordinaire (indexation ou marché)** :
- Protection de 3 mois à compter de la date d'entrée en vigueur des nouveaux tarifs
- Pendant ces 3 mois, le praticien est facturé aux anciens tarifs
- Au-delà, les nouveaux tarifs s'appliquent automatiquement

**Pour les praticiens actifs lors d'une modification tarifaire majeure (> 15 % de variation sur un plan)** :
- Protection de 6 mois
- Le praticien reçoit un préavis de 90 jours (pas seulement 60)

**Pour les clients ayant une série de séances prépayées** :
- Les séances prépayées sont honorées aux tarifs convenus, sans exception

### 4.3 Communication du grandfathering

La période de grandfathering est communiquée explicitement dans chaque préavis de modification tarifaire. Elle est affichée dans l'interface praticien pendant toute sa durée.

---

## PARTIE V — TARIFICATION EXPÉRIMENTALE (A/B TESTING)

### 5.1 Conditions d'un test tarifaire A/B

IVIA peut tester de nouveaux tarifs sur un sous-ensemble de praticiens consentants, sous les conditions suivantes :
1. Consentement explicite des praticiens participants (opt-in volontaire)
2. Durée limitée : maximum 90 jours
3. Divergence maximale : les tarifs testés ne peuvent pas s'éloigner de plus de 20 % des tarifs standards
4. Rapport post-test : les résultats sont partagés avec le Comité tarifaire et les praticiens participants
5. Aucun test A/B ne peut tester un tarif plus élevé sur un segment vulnérable (praticiens à faible volume en début de pratique)

### 5.2 Ce qui n'est jamais testé A/B

- La suppression de fonctionnalités essentielles pour créer un sentiment de "dégradation du service"
- Des tarifs punitifs pour les comportements de désabonnement
- Des variations tarifaires fondées sur l'identité ou la localisation géographique des praticiens

---

## PARTIE VI — POLITIQUE DE REMISES ET CODES PROMO

### 6.1 Encadrement strict

**Les remises autorisées** :
- Programme de référencement : 1 mois offert au praticien référent lors de l'activation d'un nouveau praticien référé (voir STRATEGIE_MULTI_STRATES_DETAILLEE.md)
- Partenariats institutionnels : une association ou un ordre professionnel partenaire peut négocier une remise collective pour ses membres (maximum 15 %, validée par le Comité tarifaire)
- Première période d'essai : 30 jours d'utilisation incluse lors de l'inscription (non un mois gratuit — période de démarrage avec accès progressif)

**Ce qui n'est jamais autorisé** :
- Codes promo à usage illimité ou à diffusion publique non contrôlée
- Remises fondées sur un engagement de publicité ou de témoignage (achat de bonne opinion)
- Remises différenciées selon le profil démographique du praticien

### 6.2 Approbation des remises

Toute remise permanente ou récurrente (pas les promotions ponctuelles < 30 jours) doit être approuvée par le Comité tarifaire.

---

## PARTIE VII — GRATUITÉS ET BOURSES

### 7.1 Cas sociaux et accès économique

IVIA reconnaît que le prix de l'abonnement peut être une barrière pour certains praticiens dont la pratique est nascente ou dont la clientèle est en situation précaire.

**Programme de bourses IVIA** (à partir de Palier 3, M7) :
- Bourses disponibles : 5-10 % des abonnements actifs (nombre de places)
- Critères : praticien en développement de pratique, pratique auprès de clientèles en situation précaire, ou praticien dans des régions québécoises sous-desservies
- Valeur : abonnement plan Essentiel à tarif réduit (50 %) pour 6-12 mois renouvelables
- Sélection : comité ad hoc composé du fondateur + un ambassadeur praticien
- Financement : couvert par le budget de l'OBNL IVIA (subventions philanthropiques dédiées)

### 7.2 Partenariats de recherche

Les chercheurs universitaires ou les organismes de recherche qui souhaitent utiliser IVIA dans un contexte de recherche éthique (avec protocole de consentement rigoureux) peuvent accéder à la plateforme selon des conditions tarifaires spéciales :
- Accès au plan Standard à tarif réduit
- Conditions : protocole de recherche approuvé par un comité d'éthique
- Engagement : partage des résultats de recherche (non nominatifs) avec IVIA

---

## PARTIE VIII — REPORTING TARIFAIRE

### 8.1 Rapport mensuel aux investisseurs

Le rapport mensuel aux investisseurs inclut les métriques tarifaires suivantes :
- ARR et MRR actuels
- Distribution des praticiens par plan et par palier de volume
- Comparaison ARR prévu / ARR réel vs. projections BP V2
- Coût variable moyen par séance (vs. baseline)
- Taux de churn par plan (pour détecter un signal tarifaire)

### 8.2 Rapport trimestriel public (via audit)

Le rapport d'audit annuel d'IVIA inclut un résumé de la politique tarifaire de l'exercice :
- Modifications tarifaires effectuées et leur justification
- Préavis respectés (confirmation)
- Praticiens ayant bénéficié du grandfathering
- Nombre de bourses accordées

Ce résumé est public — il renforce la transparence doctrinaire sur la monétisation.

---

**Au sein de l'être — En actes.**

*Version 1.0 — Mai 2026*
*David Phaneuf, fondateur IVIA*

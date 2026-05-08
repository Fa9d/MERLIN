# STRATÉGIE TECHNOLOGIQUE 36 MOIS — IVIA / MERLIN
## Architecture, pipeline, souveraineté, sécurité et continuité technique

**Version** : 1.0 — Vague 3
**Date** : Mai 2026
**Statut** : Document stratégique — Usage interne, équipe technique, investisseurs
**Auteur** : David Phaneuf (fondateur) + Perplexity Computer
**Cohérence** : Aligné avec CHARTE_TRANSFORMATION_GOUVERNEE_DONNEES.md, BP_FINANCEMENT_V2.md, PLAN_INTEGRATION_IVIA_36MOIS.md, CARTOGRAPHIE_RISQUES.md

---

## PRÉAMBULE

### La technologie comme expression de la doctrine

IVIA n'est pas une entreprise technologique qui fait de l'accompagnement. IVIA est une entreprise d'accompagnement qui utilise la technologie pour honorer sa doctrine. Cette distinction est fondamentale : elle détermine comment chaque décision technique est prise, avec quel critère premier, dans quel ordre de priorité.

La règle est simple : la technologie sert la doctrine, jamais l'inverse. Quand une solution technique est plus performante mais moins conforme à la charte de transformation gouvernée des données, c'est la solution moins performante qui est retenue. Quand un fournisseur est moins cher mais moins transparent sur ses pratiques de données, c'est le fournisseur plus cher et plus transparent qui est choisi.

Cette posture crée des coûts à court terme. Elle crée également le moat à long terme.

### Les trois phases techniques de la trajectoire IVIA

La trajectoire technologique d'IVIA sur 36 mois suit trois phases distinctes, non pas linéaires mais imbriquées :

**Phase 1 — Commercial (M1-M12)** : stabiliser l'infrastructure de service. Fiabilité, conformité, qualité documentaire. Dépendance assumée aux meilleurs fournisseurs tiers disponibles.

**Phase 2 — Évolutif (M7-M24)** : construire le pipeline propriétaire. Pipeline de transformation des données, extraction de signaux, synthétisation. Réduction progressive de la dépendance aux composants tiers les plus sensibles.

**Phase 3 — Propriétaire (M19-M36+)** : fine-tuning du modèle IVIA. Infrastructure propre pour l'entraînement et l'inférence. Souveraineté technologique partielle sur les composants critiques.

---

## PARTIE I — ARCHITECTURE TECHNIQUE ACTUELLE

### 1.1 Stack technologique — 24 outils (mai 2026)

L'architecture technique actuelle est construite autour de 24 outils organisés en 6 couches fonctionnelles.

**Couche 1 — Infrastructure et hébergement**

| Outil | Rôle | Fournisseur | Sensibilité données | Statut |
|---|---|---|---|---|
| OVH Canada | Hébergement principal, stockage données sensibles | OVH (Canada) | Élevée — données personnelles | ACTIF |
| Cloudflare | CDN, protection DDoS, DNS | Cloudflare | Faible | ACTIF |
| GitHub | Contrôle de version du code source | Microsoft | Faible | ACTIF |

**Couche 2 — Communication audio et temps réel**

| Outil | Rôle | Fournisseur | Sensibilité données | Statut |
|---|---|---|---|---|
| LiveKit | Salle audio temps réel (P2P chiffré) | LiveKit Inc. | Élevée — audio biométrique en transit | ACTIF |
| Deepgram | Transcription audio automatique (français québécois) | Deepgram | Élevée — audio biométrique | ACTIF |

**Couche 3 — Intelligence artificielle**

| Outil | Rôle | Fournisseur | Sensibilité données | Statut |
|---|---|---|---|---|
| OpenAI GPT-4.1 | Analyse, synthèse, extraction signaux | OpenAI | Moyenne — transcriptions pseudonymisées | ACTIF |
| Claude (Anthropic) | Rédaction documentaire qualité | Anthropic | Moyenne — transcriptions pseudonymisées | ACTIF |
| GPT-4.1-mini | Tâches d'analyse légères, coûts réduits | OpenAI | Moyenne | ACTIF |

**Couche 4 — Gestion, paiement et opérations**

| Outil | Rôle | Fournisseur | Sensibilité données | Statut |
|---|---|---|---|---|
| Stripe | Paiement et facturation | Stripe | Moyenne — données paiement (PCI-DSS) | ACTIF |
| Resend | Emails transactionnels | Resend | Faible — emails clients | ACTIF |
| PostHog | Analytics produit (événements, funnels) | PostHog | Faible — données comportementales anonymisées | ACTIF |
| Sentry | Monitoring des erreurs | Sentry | Faible — logs techniques | ACTIF |
| StatusPage | Page de statut opérationnel | Atlassian | Nulle | ACTIF |

**Couche 5 — Base de données et stockage**

| Outil | Rôle | Fournisseur | Sensibilité données | Statut |
|---|---|---|---|---|
| PostgreSQL (OVH) | Base de données relationnelle principale | OVH Canada | Élevée — toutes données applicatives | ACTIF |
| Redis (OVH) | Cache sessions, queues temps réel | OVH Canada | Moyenne — données de session | ACTIF |
| S3-compatible (OVH) | Stockage fichiers audio chiffrés | OVH Canada | Élevée — audio biométrique | ACTIF |

**Couche 6 — Développement et tests**

| Outil | Rôle | Fournisseur | Sensibilité données | Statut |
|---|---|---|---|---|
| Next.js | Framework frontend | Vercel (open-source) | Nulle | ACTIF |
| Node.js / TypeScript | Backend API | Communauté open-source | Nulle | ACTIF |
| Prisma ORM | ORM base de données | Prisma Data | Nulle | ACTIF |
| Jest / Vitest | Tests unitaires et d'intégration | Open-source | Nulle | ACTIF |
| Docker | Conteneurisation | Docker Inc. | Nulle | ACTIF |
| Terraform | Infrastructure as Code | HashiCorp | Faible | ACTIF |
| Doppler | Gestion des secrets | Doppler | Moyenne — clés API | ACTIF |
| Notion | Documentation interne | Notion | Faible | ACTIF |
| Linear | Gestion des tâches de développement | Linear | Faible | ACTIF |

**Synthèse de l'exposition aux données**

| Niveau de sensibilité | Nombre d'outils | Outils concernés |
|---|---|---|
| Élevée (données biométriques ou personnelles) | 5 | OVH, LiveKit, Deepgram, PostgreSQL OVH, S3 OVH |
| Moyenne (données pseudonymisées ou paiement) | 5 | OpenAI, Claude, GPT-mini, Stripe, Doppler |
| Faible ou nulle | 14 | Tous autres outils |

### 1.2 Architecture de la séance MERLIN — Flux de données

```
CLIENT                        SERVEUR IVIA                    SOUS-TRAITANTS
  |                               |                                  |
  |-- Connexion HTTPS (TLS 1.3) ->|                                  |
  |                               |-- Auth JWT + session Redis ------>|
  |<-- Session établie -----------|                                  |
  |                               |                                  |
  |== LiveKit P2P audio =========|== LiveKit server (transit) =====>|
  |   (chiffré E2E en transit)   |                                  |
  |                               |                                  |
  |                               |-- Enregistrement audio OVH ----->|
  |                               |   (chiffré AES-256, J+0)        |
  |                               |                                  |
  |-- Fin de séance ------------->|                                  |
                                  |                                  |
                                  |== Pipeline gouverné (si consent) =|
                                  |  1. Deepgram : transcription      |
                                  |  2. GPT-4.1-mini : pré-filtrage   |
                                  |  3. Claude : analyse structurée   |
                                  |  4. Validation praticien          |
                                  |  5. Destruction audio J+30        |
```

---

## PARTIE II — TRAJECTOIRE TECHNIQUE EN 3 PHASES

### 2.1 Phase 1 — Commercial (M1-M12) : Stabiliser, livrer, mesurer

L'objectif de la Phase 1 est de faire fonctionner le service de façon fiable pour les praticiens et les clients. Le mot d'ordre est la simplicité : pas d'innovation technologique non nécessaire, pas de développement propriétaire prématuré. Utiliser les meilleurs outils tiers disponibles, les assembler proprement, et mesurer.

**Priorités techniques Phase 1** :

1. Stabilité de l'infrastructure (uptime > 99,5 % mesuré)
2. Pipeline documentaire de base (transcription → analyse → synthèse → validation praticien → diffusion client)
3. Système de consentements granulaires opérationnel et auditable
4. Système de paiement Stripe stable
5. Journalisation des événements pour conformité et débogage
6. Automatisation des destructions audio (J+30) — testée et certifiée avant lancement

**Ce qu'on NE fait pas en Phase 1** :
- Aucun développement de modèle IA propriétaire
- Aucune infrastructure d'entraînement ML
- Aucune migration de fournisseur critique sans raison forte

**Décision technique clé Phase 1 : Choix Deepgram pour la transcription**

Deepgram Nova-3 est le modèle de transcription le plus performant en français québécois parmi les solutions disponibles en 2025-2026. Le choix est pragmatique. La dépendance est assumée.

Mitigation : DPA (Data Processing Agreement) signé avec Deepgram avant toute séance. Clause de non-rétention des données après traitement. Endpoint canadien utilisé si disponible. Évaluation annuelle de la dépendance.

### 2.2 Phase 2 — Évolutif (M7-M24) : Construire le pipeline propriétaire

La Phase 2 est la phase de construction de la valeur durable. Elle opère en parallèle de la Phase 1 (le service commercial continue et s'améliore pendant que le pipeline se construit).

**Les 4 axes du pipeline de transformation gouvernée**

**Axe 1.5 — Pré-filtrage de pertinence (M4-M9)**

Objectif : qualifier automatiquement les séances selon leur valeur pour l'enrichissement du dataset.

Approche technique :
- Analyse des métadonnées de séance (durée, présence de silences significatifs, densité des échanges)
- Classification automatique en 3 niveaux (non pertinent / pertinent dataset / pertinent formation modèle)
- L'analyse ne lit pas le contenu de la transcription — elle analyse des proxies structuraux

Technologies : modèle de classification léger (fine-tuning d'un modèle de classification texte open-source), déployé en interne sur serveur OVH.

Coût estimé développement : 15 000-25 000 $ (inclus RS&DE)
Délai : 3-4 mois de développement

**Axe 2 — Extraction de signaux structurés (M7-M13)**

Objectif : extraire des signaux anonymisés à partir des transcriptions pseudonymisées des séances qualifiées.

Signaux extraits :
- Patrons émotionnels (catégories génériques : anxiété / deuil / conflit / transition / ressource)
- Structure thématique de la séance (axes explorés, non-explorés)
- Marqueurs de progression (présence/absence de certains indicateurs d'évolution)
- Qualité de la relation d'aide (engagement, résistance, co-construction)

Approche technique :
- Prompt engineering sur Claude / GPT-4.1 avec templates structurés
- Output en JSON structuré, versionnée dans une table `signals_structured`
- Validation d'un sous-échantillon par des praticiens superviseurs (échantillon aléatoire anonymisé)
- Processus entièrement sans données identifiables à ce stade

Technologies : GPT-4.1-mini (coût optimisé), output JSON parsé et stocké en PostgreSQL.

Coût estimé développement : 50 000-80 000 $ (inclus RS&DE)
Délai : 5-6 mois de développement

**Axe 2.5 — Synthèse vocale enrichie (M13-M19)**

Objectif : ajouter aux signaux structurés des métadonnées prosodiques (rythme, pauses, intonation) sans conserver l'audio identifiable.

Approche technique :
- À J+0 (dès la séance) : extraction de métadonnées prosodiques anonymisées (pas d'empreinte vocale identifiable)
- Ces métadonnées sont stockées indépendamment de l'audio brut
- L'audio biométrique est toujours détruit à J+30
- Les métadonnées prosodiques anonymisées rejoignent le dataset à J+30

Technologies : analyse audio open-source (librosa ou équivalent), exécution sur serveur OVH en environnement isolé.

**Note d'attention — Données biométriques prosodiques**
> L'extraction de données prosodiques doit faire l'objet d'une Évaluation des facteurs relatifs à la vie privée (EFVP) complémentaire avant activation. Selon la Loi 25 (art. 3.3), tout projet impliquant des données biométriques requiert une EFVP. Même si les métadonnées prosodiques ciblées ne constituent pas une empreinte vocale identifiable, la prudence légale recommande cette évaluation préalable. Ce point doit être tranché avec le conseiller juridique avant M13.

Coût estimé développement : 40 000-60 000 $ (inclus RS&DE)
Délai : 4-5 mois de développement

**Axe 3 — Synthétisation IA (M19-M27)**

Objectif : générer des cas synthétiques — séances fictives représentatives des patterns observés — sans aucun lien avec les données personnelles réelles.

Approche technique :
- À partir des signaux structurés de plusieurs séances (jamais une seule), générer une séance fictive cohérente
- Contrainte de diversité : les cas synthétiques doivent représenter la diversité des patterns observés (pas seulement les patterns fréquents)
- Validation humaine : chaque cas synthétique généré est revu par un praticien superviseur IVIA avant intégration au dataset
- Stockage dans une table séparée `synthetic_cases` avec traçabilité de la génération (timestamp, version du modèle générateur, praticien validateur)

Technologies : GPT-4.1 ou Claude pour la génération initiale, fine-tuning progressif d'un modèle open-source (Llama 3.1, Mistral 7B, ou Qwen) pour remplacer les modèles tiers dans la génération.

Coût estimé développement : 80 000-120 000 $ (inclus RS&DE)
Délai : 6-9 mois de développement

### 2.3 Phase 3 — Propriétaire (M19-M36+) : Fine-tuning du modèle IVIA

La Phase 3 est la phase de réalisation du moat technologique ultime : le modèle IA propriétaire IVIA, entraîné exclusivement sur le dataset synthétique, capable de générer des analyses, synthèses et recommandations de qualité supérieure aux modèles généralistes pour le domaine de l'accompagnement émotionnel.

**Architecture d'entraînement Phase 3**

Infrastructure propre OVH (GPU computing) :
- Serveur GPU loué (A100 ou H100) pour les runs d'entraînement
- Stockage local du dataset synthétique (chiffré)
- Pipeline MLOps : DVC (Data Version Control) + MLflow pour le suivi des expériences
- Déploiement du modèle entraîné sur serveur d'inférence propre OVH

**Dataset synthétique — seuils requis**

| Seuil | Cas synthétiques | Palier estimé | Impact sur qualité du modèle |
|---|---|---|---|
| Minimal viable | 1 000 | M22-M24 | Fine-tuning exploratoire, qualité modeste |
| Opérationnel | 3 000 | M27-M30 | Qualité comparable aux modèles généralistes sur le domaine |
| Avancé | 10 000+ | M36+ | Supériorité démontrée sur les modèles généralistes pour le domaine IVIA |

**Modèle base recommandé pour fine-tuning**

| Modèle | Taille | Avantages | Inconvénients |
|---|---|---|---|
| Llama 3.1 8B | 8B params | Open-source, licence commerciale permissive, bon français | Moins puissant que les modèles 70B+ |
| Mistral 7B v0.3 | 7B params | Excellent rapport performance/coût, bon français | Licence permissive mais à vérifier |
| Qwen 2.5 7B | 7B params | Fort en multilingue français, efficace | Moins connu de la communauté québécoise |

Recommandation au M19 : commencer les expériences avec Llama 3.1 8B (licence Apache 2.0 — la plus permissive). Décision finale au gate M19 en fonction de l'état du dataset et des capacités GPU disponibles.

---

## PARTIE III — ROADMAP TECHNIQUE PAR PALIER

### Palier 1 — M1 à M3 (juin-août 2026)

**Livrables techniques**

| Livrable | Description | Priorité | État |
|---|---|---|---|
| Infrastructure OVH opérationnelle | Serveurs, S3, PostgreSQL, Redis en production | Critique | À valider |
| LiveKit séance audio stable | Salle audio, connexion E2E, enregistrement | Critique | À valider |
| Deepgram transcription française | Pipeline transcription → texte brut | Critique | À valider |
| Pipeline documentaire de base | Transcription → analyse GPT → synthèse Claude → validation praticien | Critique | À valider |
| Système consentements | Formulaire 3 niveaux, stockage, révocation | Critique | À valider |
| Destruction automatique J+30 | Processus schedulé, logs, notification | Critique | À valider |
| Dashboard praticien v1 | Agenda, séances, documents, paramètres | Haute | À valider |
| Monitoring Sentry + StatusPage | Alertes, incidents, statut public | Haute | À valider |

**Gate technique Palier 1 → 2**
- Uptime > 99,5 % sur 30 jours consécutifs
- Pipeline documentaire bout-en-bout validé sur 30 séances réelles
- Destruction J+30 testée et certifiée (test d'audit des logs)
- Aucune fuite de données signalée

### Palier 2 — M4 à M6 (sept-nov 2026)

**Livrables techniques**

| Livrable | Description | Priorité |
|---|---|---|
| Admin tarification dynamique (BACK-011) | Interface admin pour paramétrer les prix sans redéploiement | Haute |
| Pipeline pré-filtrage Axe 1.5 | Classification automatique des séances (3 niveaux) | Haute |
| Module opt-in praticien dataset | Interface praticien pour désigner les séances "pertinentes" | Haute |
| Dashboard praticien v2 | Ajout : signaux structurés non biométriques de leurs séances | Haute |
| Système de journalisation étendu | Tous les événements critiques loggés et auditables | Haute |
| Tests de charge | Simulation 50-100 séances simultanées | Moyenne |

### Palier 3 — M7 à M12 (déc 2026 - mai 2027)

**Livrables techniques**

| Livrable | Description | Priorité |
|---|---|---|
| Pipeline extraction signaux Axe 2 | Extraction JSON structuré des patrons émotionnels | Critique |
| Table `signals_structured` | Structure de données versionnable pour les signaux | Critique |
| Module DSP (Dossier Suivi Praticien) S2 | Templates documentaires conformes ordres professionnels | Haute |
| EFVP v2 (données prosodiques) | Évaluation réglementaire avant Axe 2.5 | Haute |
| Migration Phase 2 modèles IA | Remplacement progressif de GPT-4.1 par solutions optimisées coût | Moyenne |
| Sauvegardes chiffrées quotidiennes | Backup complet + test de restauration mensuel | Haute |

### Palier 4 — M13 à M18 (juin-nov 2027)

**Livrables techniques**

| Livrable | Description | Priorité |
|---|---|---|
| Pipeline Axe 2.5 (métadonnées prosodiques) | Si EFVP favorable | Haute |
| Infrastructure S2 (templates ordres) | Modules documentaires spécifiques S2 | Critique |
| Audit sécurité externe | Pentest et audit de conformité Loi 25 | Critique |
| RS&DE documentation Palier 3-4 | Documentation technique pour crédit R&D | Haute |
| Portail partenaires ordres | Espace dédié aux contacts institutionnels | Moyenne |
| Dashboard reporting investisseurs | KPI automatisés, rapport mensuel auto-généré | Moyenne |

### Palier 5 — M19 à M27 (déc 2027 - août 2028)

**Livrables techniques**

| Livrable | Description | Priorité |
|---|---|---|
| Pipeline Axe 3 — Synthétisation IA | Génération de cas synthétiques depuis les signaux | Critique |
| Infrastructure GPU OVH | Serveur GPU pour expériences d'entraînement | Haute |
| Table `synthetic_cases` | Stockage versionné des cas synthétiques validés | Critique |
| Fine-tuning exploratoire Llama 3.1 | Premières expériences avec 1 000 cas synthétiques | Haute |
| Infrastructure S3 (templates soins) | Modules documentaires spécifiques S3 | Haute |
| Revue modèles IA (gate M19) | Décision make vs. buy pour les composants IA critiques | Critique |

### Palier 6 — M28 à M36 (sept 2028 - mai 2029)

**Livrables techniques**

| Livrable | Description | Priorité |
|---|---|---|
| Modèle IVIA fine-tuné v1 | Modèle propriétaire entraîné sur 3 000+ cas synthétiques | Critique |
| Inférence propriétaire OVH | Remplacement partiel des appels OpenAI/Anthropic | Critique |
| Infrastructure S4 (annuaire) | Moteur de l'annuaire éthique IVIA Réseau | Haute |
| Audit RS&DE complet | Documentation complète de la R&D pour crédit | Haute |
| Rapport de souveraineté technologique | Bilan de la réduction de dépendance aux tiers | Haute |
| Préparation levée Série A | Valorisation technologique documentée | Haute |

---

## PARTIE IV — SOUVERAINETÉ TECHNOLOGIQUE

### 4.1 État actuel de la dépendance

L'architecture actuelle crée 5 dépendances critiques envers des fournisseurs tiers.

| Dépendance | Fournisseur | Criticité | Risque en cas de défaillance |
|---|---|---|---|
| Transcription audio | Deepgram | Élevée | Pipeline documentaire interrompu |
| Analyse IA | OpenAI / Anthropic | Élevée | Analyse et synthèse interrompues |
| Audio temps réel | LiveKit | Élevée | Séances impossibles |
| Hébergement | OVH Canada | Élevée | Service complet interrompu |
| Paiement | Stripe | Moyenne | Facturation interrompue |

### 4.2 Trajectoire d'indépendance par composant

**Transcription audio (Deepgram)**

Trajectoire :
- M1-M12 : Deepgram exclusivement (qualité, conformité, simplicité)
- M13-M24 : Évaluation des alternatives open-source (Whisper v3, faster-whisper, Canary)
- M24-M36 : Migration partielle vers faster-whisper déployé en OVH (pour les transcriptions non temps réel, moins critiques). Deepgram maintenu pour la transcription temps réel en séance.

Coût migration : ~15 000-25 000 $ de développement. Économies potentielles : 30-50 % des coûts Deepgram à volume élevé.

**Analyse IA (OpenAI / Anthropic)**

Trajectoire :
- M1-M18 : GPT-4.1 + Claude (pour les tâches documentaires critiques)
- M13-M24 : Remplacement des tâches légères par des modèles open-source optimisés (Llama 3.1 8B via Ollama sur OVH)
- M24-M36 : Fine-tuning du modèle IVIA pour les tâches spécialisées (analyse de séances IVIA). Remplacement progressif des appels OpenAI pour les tâches d'analyse IVIA.
- M36+ : Le modèle propriétaire IVIA couvre 60-80 % des tâches d'analyse. OpenAI/Anthropic maintenus pour les tâches génériques.

**Audio temps réel (LiveKit)**

LiveKit est open-source (Apache 2.0). Il est possible de l'auto-héberger sur OVH.

Trajectoire :
- M1-M12 : LiveKit cloud (hosted) pour la simplicité opérationnelle
- M12-M24 : Évaluation du coût et de la complexité de l'auto-hébergement
- M24+ : Migration vers LiveKit auto-hébergé sur OVH si le volume justifie l'investissement (~5 000-10 000 $ de setup, économies ensuite)

**Hébergement (OVH Canada)**

OVH Canada est déjà la solution la plus souveraine disponible pour IVIA (hébergement territorial canadien, opérateur européen indépendant des GAFAM, conformité Loi 25 maximale). Aucune migration prévue. La dépendance OVH est une dépendance choisie et assumée.

### 4.3 Indicateurs de souveraineté technologique

| Indicateur | M12 | M24 | M36 |
|---|---|---|---|
| % des requêtes IA traitées en interne | 0 % | 15-25 % | 40-60 % |
| % des coûts IA externalisés | 100 % | 75-85 % | 40-60 % |
| Nombre de fournisseurs critiques avec alternative interne | 0/5 | 2/5 | 3-4/5 |
| Modèle propriétaire IVIA opérationnel | Non | Partiel | Oui |

---

## PARTIE V — STRATÉGIE RS&DE

### 5.1 Définition et éligibilité

Le programme de Recherche Scientifique et Développement Expérimental (RS&DE) du gouvernement fédéral canadien offre un crédit d'impôt remboursable de 35 % sur les dépenses de R&D admissibles pour les PME canadiennes (MERLIN inc. via la structure hybride).

Le Crédit d'impôt pour investissement (CTRI) du gouvernement du Québec ajoute un crédit supplémentaire de 14-30 % sur les salaires R&D selon les conditions.

**Combinés, ces deux programmes peuvent représenter 40-60 % de remboursement des dépenses de R&D admissibles — un financement non-dilutif majeur.**

### 5.2 Activités IVIA admissibles à la RS&DE

| Activité | Palier | Justification RS&DE |
|---|---|---|
| Axe 1.5 — Pré-filtrage de pertinence | P2-P3 | Développement d'un algorithme de classification innovant (incertitude technologique sur les proxies de pertinence émotionnelle) |
| Axe 2 — Extraction signaux structurés | P3-P4 | Recherche sur les méthodes d'anonymisation préservant les patterns émotionnels (problème non résolu par la pratique standard) |
| Axe 2.5 — Synthèse prosodique | P4-P5 | Recherche sur l'extraction de métadonnées prosodiques anonymisées — domaine émergent sans solutions standards établies |
| Axe 3 — Synthétisation IA | P5-P6 | Recherche sur la génération de données synthétiques préservant la distribution statistique des patterns émotionnels réels |
| Fine-tuning modèle propriétaire | P6 | Développement d'un modèle de langage spécialisé dans l'analyse de l'accompagnement émotionnel — domaine non couvert par les recherches publiques |

### 5.3 Stratégie de documentation RS&DE

La documentation RS&DE est la condition sine qua non de l'admissibilité. Les activités admissibles doivent être documentées au fil de l'eau — pas reconstituées a posteriori.

**Protocole de documentation (à mettre en place dès M1)**

1. Journal de R&D quotidien : noter les problèmes techniques rencontrés, les hypothèses testées, les résultats obtenus
2. Feuilles de temps : enregistrer le temps consacré aux activités R&D vs activités commerciales (pour chaque employé, y compris le fondateur)
3. Documentation des échecs : les échecs et les impasses techniques sont aussi documentés — ils prouvent l'incertitude technologique
4. Revues mensuelles : synthèse mensuelle de l'avancement R&D, diffusée au Comité de gouvernance
5. Rapports trimestriels RS&DE : préparés par un consultant RS&DE spécialisé

**Budget RS&DE — projections**

| Palier | Dépenses R&D estimées | Crédit RS&DE estimé (35 % fédéral) | CTRI estimé (14-30 % Québec) | Total non-dilutif estimé |
|---|---|---|---|---|
| P2-P3 (M4-M12) | 80 000 $ | 28 000 $ | 11 000-24 000 $ | 39 000-52 000 $ |
| P3-P4 (M7-M18) | 180 000 $ | 63 000 $ | 25 000-54 000 $ | 88 000-117 000 $ |
| P4-P5 (M13-M27) | 250 000 $ | 87 500 $ | 35 000-75 000 $ | 122 500-162 500 $ |
| P5-P6 (M19-M36) | 300 000 $ | 105 000 $ | 42 000-90 000 $ | 147 000-195 000 $ |
| **TOTAL 36 mois** | **810 000 $** | **283 500 $** | **113 000-243 000 $** | **396 500-526 500 $** |

**Estimation RS&DE totale sur 36 mois : 400 000 - 530 000 $ de financement non-dilutif.**

Cet actif non-dilutif justifie pleinement l'investissement dans un consultant RS&DE spécialisé (~8 000-15 000 $/an).

---

## PARTIE VI — SÉCURITÉ

### 6.1 Architecture de sécurité

**Chiffrement**

| Niveau | Méthode | Couverture |
|---|---|---|
| Transit | TLS 1.3 (toutes API) | Toutes communications client-serveur |
| Audio temps réel | DTLS 1.2 + SRTP (LiveKit) | Canal audio séance |
| Stockage audio brut | AES-256 | Fichiers audio S3 OVH |
| Base de données | Chiffrement au niveau colonne (données sensibles) | PostgreSQL — champs sensibles |
| Secrets applicatifs | Vault chiffré (Doppler) | Clés API, variables d'environnement |

**Contrôle d'accès**

| Ressource | Politique d'accès |
|---|---|
| Audio brut J+0 → J+30 | Processus automatisés uniquement + fondateur pour incidents documentés |
| Transcriptions pseudonymisées | Praticien concerné + processus pipeline uniquement |
| Signaux structurés | Équipe technique (audit) + processus pipeline |
| Dashboard praticien | Praticien uniquement (session JWT validée) |
| Dashboard admin | Fondateur + collaborateurs nommés (2FA obligatoire) |
| Infrastructure OVH | Fondateur + DevOps nommé (2FA + IP whitelist) |

**Authentification**

- Clients et praticiens : JWT avec durée de vie courte (24h) + refresh token
- Admin et fondateur : JWT + 2FA (TOTP obligatoire)
- API-to-API : clés API avec rotation trimestrielle
- Infrastructure : SSH avec clés (pas de mots de passe)

### 6.2 Journalisation et auditabilité

Tous les événements suivants sont journalisés de façon immuable :

- Connexion et déconnexion de tout utilisateur
- Démarrage et fin de chaque enregistrement audio
- Transfert de fichier audio vers Deepgram (timestamp, ID séance)
- Création, modification, validation et diffusion de chaque document MERLIN
- Chaque accès à une donnée sensible (qui a accédé à quoi, quand)
- Destruction automatique J+30 (certifiée avec hash du fichier avant destruction)
- Toute révocation de consentement
- Toute demande de suppression de données

Les journaux sont conservés 7 ans (conformité légale Loi 25 + archivage). Ils sont stockés sur un serveur séparé du serveur applicatif principal (isolement du risque).

### 6.3 Gestion des vulnérabilités

**Revue de code** : toute modification du code touchant aux données sensibles fait l'objet d'une revue explicite avant déploiement.

**Dépendances** : scan automatique des dépendances (npm audit, dependabot) avec alerte immédiate en cas de vulnérabilité critique.

**Audit externe** : un audit de sécurité externe (pentest) est planifié au Palier 4 (M18), avant le lancement S2 avec des membres d'ordres professionnels.

**Politique de divulgation responsable** : une page de divulgation responsable est disponible sur security.ivia.quebec. Les signalements sont traités dans les 48 heures.

---

## PARTIE VII — PLAN DE CONTINUITÉ TECHNIQUE (PRA)

### 7.1 Objectifs de continuité

| Métrique | Objectif | Définition |
|---|---|---|
| RTO (Recovery Time Objective) | < 4 heures | Délai maximum de remise en service après incident majeur |
| RPO (Recovery Point Objective) | < 24 heures | Perte de données maximale acceptable |
| Uptime cible | 99,5 % | Soit < 44 heures d'indisponibilité par an |
| MTTR (Mean Time To Restore) | < 2 heures | Délai moyen de résolution des incidents |

### 7.2 Sauvegardes

| Données | Fréquence | Rétention | Localisation |
|---|---|---|---|
| PostgreSQL (base principale) | Quotidienne (snapshot) | 30 jours | OVH bucket secondaire chiffré |
| Redis (cache/sessions) | Non sauvegardé (état transitoire) | — | — |
| S3 audio (J+0 → J+30) | Réplication immédiate | J+30 (puis destruction) | OVH réplication intra-Canada |
| Code source | Continu (Git) | Illimité | GitHub + OVH mirror |
| Documents produits (PDFs, synthèses) | Quotidienne | 7 ans | OVH bucket long-terme |
| Logs d'audit | Continu | 7 ans | OVH bucket séparé, immuable |
| Secrets (Doppler) | Export manuel trimestriel | 1 an | Vault chiffré hors ligne (coffre fondateur) |

**Test de restauration** : un test complet de restauration à partir des sauvegardes est effectué trimestriellement. Le résultat est documenté dans le rapport de conformité.

### 7.3 Procédures d'incident

**Niveau 1 — Incident mineur** (service dégradé, impact < 10 % des utilisateurs)
- Délai de réponse : 30 minutes
- Action : diagnostic, contournement, communication StatusPage
- Responsable : fondateur

**Niveau 2 — Incident majeur** (service partiellement indisponible, impact > 10 %)
- Délai de réponse : 15 minutes
- Action : bascule sur infrastructure de secours, communication aux praticiens concernés, StatusPage
- Responsable : fondateur + soutien technique externe si nécessaire
- Communication : notification email aux praticiens actifs dans les 30 minutes

**Niveau 3 — Incident critique** (service totalement indisponible ou fuite de données)
- Délai de réponse : immédiat (alerte 24/7)
- Action : arrêt d'urgence des services affectés, notification CAI si données personnelles compromises (Loi 25 — obligation de notification dans les 72 heures)
- Responsable : fondateur + conseiller juridique + conseiller en sécurité
- Communication : notification immédiate aux praticiens et aux clients affectés, communication publique sur ivia.quebec/incidents

### 7.4 Plan de continuité en cas d'indisponibilité du fondateur

Si David Phaneuf est temporairement indisponible (maladie, urgence personnelle) :

- Les praticiens disposent d'un accès à un guide d'urgence technique (accès direct aux procédures de base)
- Un DevOps externe désigné (à nommer avant M2) dispose d'un accès d'urgence documenté avec les procédures d'intervention
- Les séances en cours ne sont pas interrompues (le service est autonome à court terme)
- Les interventions techniques critiques (hors séances) peuvent être retardées de 48-72 heures sans impact majeur

**Note d'attention — Désignation du DevOps externe**
> La désignation d'un DevOps ou administrateur système externe de confiance, avec un accès d'urgence documenté et testé, est une tâche critique à compléter avant M2. En l'absence de cette désignation, tout incident technique majeur en l'absence du fondateur est un risque sans mitigation opérationnelle. Ce point prolonge la Note d'attention 1 de la Vague 2 (risque de surcharge du fondateur).

---

## PARTIE VIII — VEILLE TECHNOLOGIQUE PERMANENTE

### 8.1 Axes de veille

**Modèles IA de langage**

- Parution de nouveaux modèles open-source (Llama, Mistral, Qwen, Phi-4, etc.)
- Performance comparée en français québécois
- Licences commerciales (Apache 2.0, MIT, licences propriétaires restrictives)
- Coûts d'inférence (prix/token des API, coût d'auto-hébergement)
- Nouveautés en fine-tuning (LoRA, QLoRA, techniques d'alignement)

**Transcription audio**

- Évolution de Whisper (OpenAI open-source) et de ses variantes (faster-whisper, whisperx)
- Nouveaux modèles spécialisés en français canadien
- Transcription en temps réel vs. transcription post-séance

**Vie privée et conformité**

- Évolutions de la Loi 25 (amendements, lignes directrices CAI)
- Jurisprudence en matière de données biométriques au Québec
- Évolutions RGPD (pour les partenaires européens futurs)
- Nouveaux outils de pseudonymisation et d'anonymisation

**Sécurité**

- Nouvelles vulnérabilités dans les dépendances clés
- Attaques sur les pipelines IA (prompt injection, model poisoning)
- Réglementations émergentes sur les systèmes IA (Loi européenne sur l'IA, projets canadiens)

### 8.2 Processus de veille

**Mensuel** : revue des alertes automatiques (GitHub, newsletters spécialisées, Paper Digest en NLP)

**Trimestriel** : rapport de veille technologique formel, présenté au Comité de gouvernance. Inclut une recommandation sur les outils à adopter, à surveiller, ou à retirer.

**Semestriel** : revue complète du stack technologique. Chaque outil est évalué selon quatre critères : performance, coût, conformité Loi 25, risque de dépendance.

---

## PARTIE IX — DÉCISIONS TECHNIQUES MAJEURES À VENIR

### Gates de décision

Les décisions techniques suivantes sont structurantes. Elles doivent être préparées en amont de leur échéance respective.

| Décision | Échéance | Critères de décision |
|---|---|---|
| EFVP Axe 2.5 (données prosodiques) | M10-M12 | Avis juridique conformité Loi 25, risque de réidentification |
| Make vs. Buy — Transcription (Deepgram vs. self-hosted) | M18-M24 | Volume séances, coût/séance, qualité comparative, complexité opérationnelle |
| Make vs. Buy — Analyse IA (OpenAI vs. self-hosted) | M18-M24 | Volume requêtes, coût/requête, qualité sur tâches IVIA, latence |
| Choix modèle de base pour fine-tuning | M19 | État du dataset synthétique, performances comparées, licences |
| Architecture inférence propriétaire | M24-M27 | Volume, latence requise, coûts GPU, expertise interne |
| Migration LiveKit cloud → self-hosted | M24-M30 | Volume séances, coût, complexité opérationnelle, disponibilité DevOps |
| Revue complète stack M36 | M33-M36 | Prépare la Série A et la phase post-moat |

---

**Au sein de l'être — En actes.**

*Version 1.0 — Mai 2026*
*David Phaneuf, fondateur IVIA*

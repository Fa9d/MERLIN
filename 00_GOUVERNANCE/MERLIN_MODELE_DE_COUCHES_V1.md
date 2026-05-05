---
titre: Modèle de couches — MERLIN
id: MERLIN-MODELE-COUCHES-V1
statut: active
type: charte
couche: FOND
périmètre: repo entier
auteur: fondateur
date: 2026-05-05
version: 1.0
dépend_de: [MERLIN-CHARTE-ARCH-V1]
remplace: []
arbitrage_requis: oui — toute redéfinition de couche
source_canonique: 00_GOUVERNANCE/MERLIN_MODELE_DE_COUCHES_V1.md
---

# MERLIN — Modèle de couches V1

> **Statut** : active — 2026-05-05
> **Décision formelle** : ADR-0001
> **Toute redéfinition d'une couche exige un arbitrage et un ADR.**

---

## Préambule

MERLIN n'est pas une pile technique à couches. Il est un système de pensée organisé
selon quatre niveaux de solidité, de vitesse de changement, et de finalité.

Le modèle de couches répond à une question simple mais constamment trahie dans la pratique :
**à quelle profondeur appartient ce document ou cette décision ?**

Un document mal classé dans la mauvaise couche génère :
- des révisions trop fréquentes de ce qui devrait être stable,
- une instabilité des fondements quand on ne fait qu'ajuster l'éditorial,
- une confusion entre règle métier et plan de campagne,
- une impossibilité d'auditer ou de déléguer sans risque.

---

## Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────┐
│  FOND     Fondements — Philosophie, doctrine, charte        │
│           Stabilité maximale. Changement par arbitrage.     │
├─────────────────────────────────────────────────────────────┤
│  METH     Méthodes — Protocoles, workflows, règles          │
│           Évolutif sous contrôle de version.                │
├─────────────────────────────────────────────────────────────┤
│  EDIT     Éditorial — Contenu externe, offres, campagnes    │
│           Souple, contextuel, révisable fréquemment.        │
├─────────────────────────────────────────────────────────────┤
│  PROD     Produit — Code, specs, infra, prompts système     │
│           Technique, précis, versionné par implémentation.  │
└─────────────────────────────────────────────────────────────┘
```

---

## Couche 1 — FOND (Fondements)

### Rôle

Définir ce que MERLIN est, pourquoi il existe, selon quelles valeurs il opère,
et quelles frontières il ne franchit pas. La couche FOND est la couche de légitimité.
Elle répond à : **Pourquoi ?**

### Type de documents

- Chartes (d'architecture, de gouvernance, de données)
- Doctrines (philosophiques, cliniques, organisationnelles)
- Fondements du projet (visées, positionnement stratégique)
- Politiques de haut niveau (données, consentement, sécurité des personnes)
- Fiches-nations et cadres culturels (Nations du Québec)

### Type de décisions

- Décisions de nature existentielle : que fait MERLIN, pour qui, selon quels principes
- Adoption ou modification d'une convention de gouvernance
- Décision sur les limites éthiques ou légales (ex. : MERLIN ne pose pas de diagnostic)
- Toute décision qui engage l'identité du projet à long terme

### Ce qui n'appartient PAS à FOND

- Les plans de contenu (→ EDIT)
- Les workflows cliniques (→ METH)
- Les specs techniques de l'application (→ PROD)
- Les décisions tactiques à court terme (→ METH ou PROD selon la nature)
- Les résultats d'audit d'une session particulière (→ PROD)

### Exemples concrets dans MERLIN

| Document | Raison d'appartenance à FOND |
|---|---|
| `MERLIN_FONDEMENTS_VISEES.md` | Définit les visées fondatrices |
| `MERLIN_NATQ_CADRE_CONCEPTS_REALITES_SPIRITUALITES_v1.0.md` | Cadre culturel non réductible |
| `MERLIN_CHARTE_ARCHITECTURE_V1.md` | Définit la structure du système entier |
| `MERLIN_GOUV_DOCTRINE_APPUIS_THEORIQUES_MERLIN_v1.0.md` | Doctrine d'appui théorique |
| `MERLIN_GOUV_CADRE_OPERATOIRE_TRAITEMENT_DONNEES_IVIA_MERLIN_V1.md` | Politique de données de haut niveau |

### Relations avec les autres couches

- FOND **autorise** METH : la méthode doit être compatible avec les fondements.
- FOND **contraint** EDIT : le discours public ne peut pas contredire la doctrine.
- FOND **limite** PROD : l'implémentation ne peut pas violer les politiques fondamentales.
- FOND **ne dépend pas** des autres couches — c'est la seule couche sans dépendance ascendante.

---

## Couche 2 — METH (Méthodes)

### Rôle

Décrire comment MERLIN atteint ses objectifs. Traduire les fondements en pratiques
opérationnelles, protocoles et workflows. La couche METH est la couche d'opérationnalisation.
Elle répond à : **Comment faire ?**

### Type de documents

- Méthodes d'orientation (triage, évaluation, priorisation)
- Playbooks (déroulé d'une séance, d'un déploiement, d'un pilote)
- Protocoles cliniques ou organisationnels
- Cas simulés et exemples de référence
- Grilles d'évaluation
- Règles de classification et de priorisation

### Type de décisions

- Adoption d'un protocole ou d'un workflow canonique
- Modification d'une méthode suite à un apprentissage terrain
- Choix entre deux approches opérationnelles (ex. : orientation vs triage direct)
- Validation d'un cas simulé comme référence de formation

### Ce qui n'appartient PAS à METH

- Les valeurs ou la philosophie (→ FOND)
- Les plans de contenu, campagnes ou pages web (→ EDIT)
- Les prompts IA système ou les configurations de déploiement (→ PROD)
- Les résultats d'exécution d'une méthode sur un cas réel (→ 05_PREUVES_SOURCES/)

### Exemples concrets dans MERLIN

| Document | Raison d'appartenance à METH |
|---|---|
| `MERLIN_METH_CADRE_METHODE_11_NATIONS_QC_INTL_v1.0.md` | Méthode d'application interculturelle |
| `MERLIN_METH_CAS_SIMULES_PREMIERE_LIGNE_SANTE_MENTALE_v1.0.md` | Cas de référence pour formation |
| `MERLIN_GOUV_POLICY_CHAMPS_INTERVENTION_PREMIERE_LIGNE_v1.0.md` | Règle opérationnelle de champ |
| `MERLIN_GOUV_CHECKLIST_RECETTE_PROD_E2E_J8_V1.md` | Protocole de validation de déploiement |

### Relations avec les autres couches

- METH **dépend de** FOND : elle ne peut pas contredire les fondements.
- METH **alimente** EDIT : les méthodes définissent ce qu'on peut promettre publiquement.
- METH **guide** PROD : les workflows métier guident l'implémentation technique.
- METH **ne définit pas** le produit ; elle en établit les exigences.

---

## Couche 3 — EDIT (Éditorial)

### Rôle

Produire ce qui est exposé à l'extérieur : au client, au praticien, au partenaire, au public.
La couche EDIT est la couche de traduction et d'exposition.
Elle répond à : **Que dit-on, à qui, dans quel format ?**

### Type de documents

- Pages web (client, praticien, institutions)
- Articles de diffusion
- Offres commerciales et fiches de service
- Calendriers éditoriaux
- Promesses de marque et slogans
- Documents de positionnement public

### Type de décisions

- Choix d'un axe de communication pour une campagne
- Adoption ou révision d'une promesse client
- Calendrier de publication et de diffusion
- Adaptation du discours à un segment (ex. : nations autochtones, praticiens, parents)

### Ce qui n'appartient PAS à EDIT

- Les politiques internes (→ FOND ou METH)
- Les règles de gouvernance (→ FOND)
- Les spécifications techniques (→ PROD)
- Les résultats de recherche bruts (→ 05_PREUVES_SOURCES/)
- Les décisions structurantes sur l'identité de MERLIN (→ FOND)

### Exemples concrets dans MERLIN

| Document | Raison d'appartenance à EDIT |
|---|---|
| `MERLIN_GOUV_PAGE_SITE_CLIENT_IVIA_QUEBEC_V1.md` | Contenu page publique client |
| `MERLIN_GOUV_CALENDRIER_EDITORIAL_DIFFUSION_CLIENT_30_JOURS_IVIA_V1.md` | Plan de diffusion |
| `MERLIN_GOUV_POSITIONNEMENT_PUBLIC_SITE_V1.md` | Positionnement marketing |
| `MERLIN_GOUV_PROMESSE_CLIENT_ULTRA_COURTE_IVIA_V1.md` | Promesse de marque |
| `07_EXPORTS/IVIA_SITE_PREVIEW/` | Pages HTML exportées pour diffusion |

### Relations avec les autres couches

- EDIT **dépend de** FOND (cohérence doctrinale) et METH (ce qu'on peut promettre).
- EDIT **alimente** PROD : les specs d'interface découlent des documents éditoriaux.
- EDIT est la couche **la plus volatile** — elle change avec le marché, les tests, les retours.
- EDIT **ne doit pas remonter** vers FOND : une campagne n'est pas une politique.

---

## Couche 4 — PROD (Produit)

### Rôle

Spécifier, construire, déployer et maintenir ce qui est livré. La couche PROD est la couche
d'implémentation et d'exploitation.
Elle répond à : **Qu'est-ce qui tourne concrètement, comment, et dans quel état ?**

### Type de documents

- Spécifications techniques (routes API, schémas DB, interfaces)
- Configurations d'infrastructure (Docker, Nginx, LiveKit)
- Migrations Alembic et schémas de données
- Runbooks d'exploitation et de déploiement
- Prompts système versionnés (bibliothèque `11_PROMPTS/`)
- ADR techniques
- Logs d'incidents et de déploiements
- Audits de sécurité et de conformité technique

### Type de décisions

- Choix d'un framework ou d'une librairie
- Décision sur l'hébergement ou l'infrastructure
- Adoption d'une politique de versionnage (ex. : bump obligatoire avant déploiement)
- Choix de modèle IA et de paramètre (haiku vs sonnet, température, etc.)
- Tout changement de prompt structurel ou métier

### Ce qui n'appartient PAS à PROD

- Les fondements philosophiques (→ FOND)
- Les méthodes d'orientation non-techniques (→ METH)
- Les pages web éditorialisées (→ EDIT, même si elles sont dans le code)
- Les politiques de données de haut niveau (→ FOND)

### Exemples concrets dans MERLIN

| Document | Raison d'appartenance à PROD |
|---|---|
| `10_backend_merlin_api/` | Backend FastAPI complet |
| `09_app_ivia_merlin/` | Frontend Next.js |
| `docker-compose.prod.yml` | Configuration de déploiement |
| `deploy/prod-up.sh` | Script de déploiement |
| `11_PROMPTS/` | Bibliothèque de prompts système |
| `MERLIN_GOUV_POLICY_VERSIONNAGE_REFERENTIELS_BDD_APP_v1.0.md` | Politique technique de versionnage |

### Relations avec les autres couches

- PROD **implémente** FOND et METH : ce qui est construit doit respecter la doctrine et les méthodes.
- PROD **expose** EDIT : le code rend visible les contenus éditoriaux.
- PROD **remonte** vers METH si une contrainte technique modifie une méthode (→ ADR requis).
- PROD **est la couche la plus granulaire** et la plus soumise à la dette technique.

---

## Erreurs fréquentes

### Erreur 1 — Confondre fondement et plan éditorial

> **Exemple** : écrire dans `01_FONDATEUR/` que "IVIA doit publier 3 articles par mois".

Un calendrier de publication est EDIT. Un fondement dit *pourquoi* on publie, pas *combien*.

### Erreur 2 — Mettre un prompt admin dans FOND

> **Exemple** : stocker dans `01_FONDATEUR/` un prompt qui génère des résumés de séance.

Un prompt système est PROD. Même s'il exprime des valeurs, son usage est technique et versionnable.

### Erreur 3 — Confondre méthode et règle métier hardcodée

> **Exemple** : coder en dur dans l'API une règle clinique sans la documenter dans METH.

Toute règle métier significative doit exister d'abord en METH avant d'être implémentée en PROD.

### Erreur 4 — Mettre une campagne dans les fondements

> **Exemple** : élever la promesse "La puissance du silence" au rang de charte fondatrice.

C'est une signature éditoriale (EDIT). Si elle devient doctrine, elle doit être explicitement arbitrée.

### Erreur 5 — Mettre un log d'incident dans METH

> **Exemple** : stocker le log de l'incident VPS du 2026-04-24 dans `04_METHODES/`.

Un log est PROD (05_PREUVES_SOURCES/ ou 00_GOUVERNANCE/). Il ne définit pas une méthode ;
il en consigne l'application.

### Erreur 6 — Créer un ADR pour chaque ligne de code

Un ADR est pour les décisions structurantes et durables. Les choix tactiques d'implémentation
(nom d'une variable, ordre d'un endpoint) n'en nécessitent pas. Voir `MERLIN_REGLES_DE_DECISION_V1.md`.

---

## Tableau de synthèse

| Couche | Stabilité | Responsable | Fréquence de changement | Trigger de révision |
|---|---|---|---|---|
| FOND | Très haute | Fondateur | Rare (annuelle ou moins) | Décision existentielle |
| METH | Haute | Fondateur + terrain | Modérée | Apprentissage terrain |
| EDIT | Moyenne | Fondateur + marketing | Fréquente | Marché, retours, campagnes |
| PROD | Variable | Développeur | Continue | Build, release, incident |

---

## Historique de révisions

| Version | Date | Auteur | Nature de la révision |
|---|---|---|---|
| 1.0 | 2026-05-05 | fondateur | Création initiale — Vague 1 structuration |

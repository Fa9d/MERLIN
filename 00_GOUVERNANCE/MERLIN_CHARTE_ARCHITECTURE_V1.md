---
titre: Charte d'architecture — MERLIN
id: MERLIN-CHARTE-ARCH-V1
statut: active
type: charte
couche: FOND
périmètre: repo entier
auteur: fondateur
date: 2026-05-05
version: 1.0
dépend_de: []
remplace: []
arbitrage_requis: oui — toute modification de cette charte
source_canonique: 00_GOUVERNANCE/MERLIN_CHARTE_ARCHITECTURE_V1.md
---

# MERLIN — Charte d'architecture V1

> **Statut** : active — 2026-05-05
> **Périmètre** : repo-système entier
> **Toute modification de cette charte exige un arbitrage explicite et un ADR.**

---

## 1. Définition canonique de MERLIN

MERLIN est un **repo-système canonique**.

Il n'est pas seulement une application, ni un ensemble de documents, ni une boîte à outils.
Il est la **source de vérité** d'un projet organisationnel complet :
- ses fondements philosophiques et doctrinaux,
- sa gouvernance et ses décisions,
- ses méthodes et ses protocoles,
- ses preuves et ses sources,
- ses prompts et ses systèmes d'instruction,
- ses produits numériques (IVIA, MESANGE, et tout futur composant),
- son infrastructure de déploiement et ses conventions d'exploitation.

Tout ce qui gouverne, tout ce qui prouve, tout ce qui instruit, tout ce qui déploie
**doit être localisable dans MERLIN** ou explicitement relié à lui.

---

## 2. Position de MERLIN dans la structure descendante

```
MERLIN
│
│   (pense / gouverne / trace / valide)
│
├── IVIA
│       (traduit / expose / interface)
│       Frontend Next.js — ivia.quebec
│       Portail praticiens — praticiens.ivia.quebec
│
├── MESANGE
│       (collecte / analyse / diffuse)
│       (produit en développement)
│
└── [Modules futurs]
        (encadrés par les mêmes règles de couche)
```

**Principe fondamental :** MERLIN pense et gouverne. Les produits traduisent et exposent.
Aucun produit ne définit la doctrine. La doctrine est définie dans MERLIN et se répercute
dans les produits.

---

## 3. Principe directeur : révisabilité, traçabilité, restructurabilité

Tout document de MERLIN doit pouvoir être :

1. **Révisé** — aucune version n'est figée pour toujours ; un bump de version est suffisant.
2. **Tracé** — chaque révision structurante doit produire un ADR ou un arbitrage.
3. **Restructuré** — un dossier peut être renommé ou déplacé si la convention le justifie,
   à condition que la migration soit documentée et que les liens internes soient mis à jour.
4. **Audité** — à tout moment, il doit être possible de savoir quel document est actif,
   qui l'a produit, et quelle décision l'a validé.

Ces quatre propriétés ne sont pas des aspirations. Elles sont des contraintes de conception.

---

## 4. Les quatre natures de documents dans MERLIN

MERLIN distingue quatre natures fondamentales. Elles ne sont pas des dossiers ;
elles traversent l'arborescence et servent à classer les documents dans la taxonomie.

### 4.1 Vision

Documente ce que MERLIN cherche à accomplir, pourquoi, pour qui, et selon quelles valeurs.
Stable dans le temps. Ne change que par arbitrage fondateur.

Exemples : fondements, doctrine, charte, positionnement stratégique.

### 4.2 Méthode

Documente comment MERLIN atteint ses objectifs. Opérationnelle, évolutive, structurée.
Peut évoluer avec l'expérience terrain, sous contrôle de version.

Exemples : playbooks, méthodes d'orientation, protocoles cliniques, workflows.

### 4.3 Éditorial

Documente ce qui est produit à destination du monde extérieur : clients, praticiens,
partenaires, public. Doit être cohérent avec la Vision et la Méthode, mais peut varier
en ton et en format.

Exemples : pages site, articles, offres, campagnes, calendrier de diffusion.

### 4.4 Produit

Documente ce qui est construit et déployé : code, spécifications techniques,
configurations, migrations, runbooks d'exploitation, prompts système.

Exemples : specs fonctionnelles, ADR techniques, configurations Nginx, schémas Alembic.

---

## 5. Ce que cette charte ne remplace pas

Cette charte définit la structure d'ensemble.
Elle ne remplace pas :

- `MERLIN_CONVENTION_NOMMAGE_V2.md` — conventions de nommage de fichiers
- `MERLIN_MODELE_DE_COUCHES_V1.md` — définition précise des couches FOND / METH / EDIT / PROD
- `MERLIN_REGLES_DE_DECISION_V1.md` — quand et comment créer un ADR ou un arbitrage
- `MERLIN_TAXONOMIE_DOCUMENTAIRE_V1.md` — types documentaires autorisés et leurs règles

---

## 6. Ce que n'est pas MERLIN

| Ce n'est pas... | Pourquoi |
|---|---|
| Un CMS | Il ne publie pas directement ; il alimente des produits qui publient. |
| Un wiki collaboratif ouvert | Il est gouverné, versionné, avec décisions explicites. |
| Une application | C'est le système qui encadre les applications. |
| Un outil de documentation auto-générée | Chaque document est intentionnel et localisé. |
| Un système figé | Il est conçu pour évoluer sous contrainte de traçabilité. |

---

## 7. Responsabilité de maintenance

En phase solo (fondateur unique), le fondateur est responsable de :
- la cohérence de la charte avec l'état réel du repo,
- le bump de version à chaque révision structurante,
- la création d'un ADR pour tout changement de cette charte.

En phase d'équipe, un rôle d'architecte de système doit être désigné explicitement.

---

## 8. Historique de révisions

| Version | Date | Auteur | Nature de la révision |
|---|---|---|---|
| 1.0 | 2026-05-05 | fondateur | Création initiale — Vague 1 structuration |

---
titre: Adoption du modèle de couches FOND / METH / EDIT / PROD
id: ADR-0001
statut: accepted
date: 2026-05-05
décideurs: fondateur
remplace: []
remplacé_par: []
---

# ADR-0001 — Adoption du modèle de couches FOND / METH / EDIT / PROD

> **Statut** : accepted — 2026-05-05
> **Document de référence** : `MERLIN_MODELE_DE_COUCHES_V1.md`

---

## Contexte

MERLIN a été constitué progressivement depuis avril 2026. Ses dossiers, ses documents
et ses décisions ont été produits dans l'urgence opérationnelle : déploiement VPS, pilote
praticiens, structuration du corpus, développement frontend et backend.

Cette progression a créé une hétérogénéité dans le classement des documents :
- des politiques dans des dossiers de méthodes,
- des fondements mélangés à des plans éditoriaux,
- des prompts système sans localisation ni versionnage explicite,
- des décisions implicites non tracées.

Sans modèle de couches explicite, il est impossible de :
- savoir quel niveau de stabilité attribuer à un document,
- déléguer sans risque (à un collaborateur humain ou à un outil IA),
- auditer le repo de manière systématique,
- faire évoluer MERLIN sans régressions structurelles.

La Vague 1 de structuration (2026-05-05) est l'occasion de poser ce socle
avant que le repo atteigne une taille critique.

---

## Options considérées

**Option A — Pas de modèle de couches formel**
Laisser l'arborescence de dossiers suffire.
*Rejeté* : l'arborescence ne dit pas le niveau de stabilité ni le type de décisions.
Un dossier peut contenir des documents de natures très différentes.

**Option B — Deux couches : Stratégie / Tactique**
Distinguer ce qui est durable de ce qui est opérationnel.
*Rejeté* : trop binaire. Ne distingue pas l'éditorial (voix publique) du produit (technique).
Crée des confusions entre méthode clinique et configuration technique.

**Option C — Quatre couches : FOND / METH / EDIT / PROD**
Modèle inspiré de la pratique architecturale logicielle (ADR) adaptée
aux systèmes documentaires gouvernés.
*Retenu* : les quatre couches couvrent les natures réelles des documents de MERLIN,
permettent d'assigner une stabilité, de définir des responsables, et de qualifier
les décisions selon leur portée.

---

## Décision

MERLIN adopte officiellement le modèle de quatre couches pour classifier
l'ensemble de ses documents et décisions :

- **FOND** — Fondements. Philosophie, doctrine, chartes, politiques de haut niveau.
  Stabilité maximale. Changement par arbitrage explicite uniquement.

- **METH** — Méthodes. Protocoles, workflows, règles opérationnelles.
  Évolutif sous contrôle de version. Peut évoluer avec le terrain.

- **EDIT** — Éditorial. Contenu public, offres, campagnes, pages web.
  Volatile. Cohérent avec FOND et METH.

- **PROD** — Produit. Code, specs techniques, prompts système, infra, migrations.
  Granulaire. Versionné par implémentation.

Ce modèle est documenté exhaustivement dans `MERLIN_MODELE_DE_COUCHES_V1.md`.
Il s'applique à tout document produit ou révisé après le 2026-05-05.

---

## Conséquences

### Avantages

- Chaque document a désormais un niveau de stabilité implicite.
- Les révisions structurantes sont identifiables (tout changement de couche FOND → ADR).
- Il est possible d'auditer le repo par couche.
- Les prompts et les règles métier peuvent être classés sans ambiguïté (PROD vs METH).
- La délégation à un outil IA est plus sûre : la couche FOND indique ce qui ne peut pas
  être modifié sans arbitrage humain.

### Inconvénients ou risques

- Des documents existants peuvent être difficiles à classer dans une seule couche.
  → Règle : en cas de doute, classer dans la couche la plus élevée (plus stable).
- Le modèle peut générer une sur-formalisation si appliqué à des notes temporaires.
  → Règle : les notes temporaires (couche non définie) ne sont pas soumises à ce modèle.

### Actions requises

- [ ] Appliquer les métadonnées `couche:` à tous les nouveaux documents structurants.
- [ ] Mettre à jour progressivement les documents existants lors de leurs prochaines révisions.
- [ ] Référencer `MERLIN_MODELE_DE_COUCHES_V1.md` dans `CLAUDE.md` lors du prochain bump.
- [ ] Ajouter l'entrée DEC-036 dans le registre de décisions.

---

## Entrée registre associée

> DEC-036 | 2026-05-05 | architecture | adoption modèle de couches FOND/METH/EDIT/PROD | validated | ADR-0001

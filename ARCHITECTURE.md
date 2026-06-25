# ARCHITECTURE MERLIN — Plateforme Évolutive
**Version** : 1.0 — 25 juin 2026
**Auteur** : David Phaneuf
**Statut** : Document fondateur — ne pas modifier sans validation doctrinale

---

## Principe fondateur

MERLIN n'est pas un produit. C'est une **plateforme évolutive** — un système d'exploitation pour l'accompagnement humain à distance.

La distinction est fondamentale :
- Un produit est conçu pour un usage défini. Il vieillit.
- Une plateforme est conçue pour accueillir des usages non encore définis. Elle grandit.

L'objectif n'est pas de construire aujourd'hui l'outil de 2046. C'est de poser les **rails** sur lesquels cet outil roulera.

---

## Les 3 Invariants

Les invariants sont les seuls éléments de MERLIN qui ne changent jamais. Tout le reste peut évoluer, être remplacé, reconfiguré. Les invariants sont non négociables.

### Invariant 1 — La Doctrine IVIA

Les 7 principes d'IVIA constituent le filtre de tout. Chaque module, chaque partenariat, chaque fonctionnalité future doit passer par ce filtre avant d'entrer dans la plateforme.

- **Le vivant d'abord** — les besoins réels avant les constructions sociales
- **L'autonomie émotionnelle comme horizon** — l'objectif est que le client n'ait plus besoin d'IVIA
- **Les lois de l'échange** — jamais de commission sur l'orientation
- **La responsabilité comme dignité** — capacité d'agir reconnue chez tous
- **La souveraineté des données** — les données servent la mission, jamais vendues
- **L'ancrage territorial** — reconnaissance des 11 nations autochtones du Québec
- **La sortie honorable** — visible, accessible, sans friction

Ces principes sont dans les statuts légaux de l'OBNL IVIA. Ils sont opposables juridiquement.

> **Règle d'intégration** : Toute proposition de nouveau module doit démontrer sa compatibilité avec chacun des 7 principes avant validation. Un module qui contredit un principe est refusé, même s'il est rentable.

### Invariant 2 — Le Pipeline de Données Gouverné

Le pipeline en 8 étapes est la colonne vertébrale technique de la plateforme. Il ne se reconstruit pas — il s'étend.

```
Étape 0 → Consentement granulaire (3 niveaux)
Étape 1 → Capture audio chiffrée (TLS 1.3)
Étape 2 → Conservation brute J+30 maximum
Étape 3 → Pré-filtrage pertinence (~10% qualifié)
Étape 4 → Transcription + pseudonymisation (90 jours)
Étape 5 → Extraction signaux anonymisés (7 ans)
Étape 6 → Effacement audio irréversible à J+30 ✓ certifié, journalisé
Étape 7 → Synthétisation → cas synthétiques
Étape 8 → Fine-tuning modèle propriétaire IVIA
```

Tout nouveau module se branche sur ce pipeline. Aucun module ne crée son propre pipeline de données parallèle.

### Invariant 3 — L'Architecture Modulaire

Chaque marché, chaque usage, chaque langue, chaque population est un **module indépendant** qui se connecte à la plateforme sans la modifier.

Analogie : comme des applications sur un système d'exploitation. L'OS ne change pas quand une nouvelle app est installée.

---

## Protocole de Connexion Modulaire

Pour qu'un nouveau module soit intégré à la plateforme, il doit satisfaire **5 conditions** :

```
1. COMPATIBILITÉ DOCTRINALE
   Le module passe les 7 principes IVIA sans exception.
   Validation requise : David Phaneuf + comité doctrinal (à constituer M6)

2. CONNEXION AU PIPELINE
   Le module utilise le pipeline gouverné existant.
   Il ne crée pas de flux de données parallèles.
   Validation requise : audit technique

3. INTERFACE STANDARDISÉE
   Le module expose une API conforme aux standards MERLIN.
   Documentation requise avant intégration.

4. RÉVERSIBILITÉ
   Le module peut être retiré sans affecter les autres modules.
   Les données du module peuvent être effacées de façon isolée.

5. IDENTITÉ PRÉSERVÉE
   Le module adapte sa présentation visuelle et linguistique à son contexte
   mais reste reconnaissable comme appartenant à l'écosystème IVIA/MERLIN.
```

---

## Les Modules Actuels et Planifiés

### Modules Actifs (Phase 0)
| Module | Description | Statut |
|---|---|---|
| `core.ecoute` | Séance audio + transcription + analyse praticien | ✅ En production |
| `core.pipeline` | Pipeline de données gouverné 8 étapes | ✅ En production |
| `core.admin` | Tarification, gestion praticiens, indicateurs | ✅ En production |

### Modules Phase 1 — M6 à M18
| Module | Description | Condition d'activation |
|---|---|---|
| `nations.coecoute` | Co-construction avec nations autochtones QC | Accord de partenariat formalisé |
| `nations.langues` | R&D traduction langues vivantes | Démarrage avec nations autochtones |
| `financement.public` | Interface dépôts subventions MSSS/CAI/CRSH | M6 |

### Modules Phase 2 — M18 à M36
| Module | Description | Condition d'activation |
|---|---|---|
| `triage.premiereligne` | Orientation intelligente vers services existants | MRR 8K$+ |
| `ordres.s2` | Outils psychologues et psychothérapeutes | Audit juridique ordres complété |
| `ordres.s3` | Praticiens corporels (ostéo, naturo) | S2 stabilisé |

### Modules Phase 3 — M36 et au-delà
| Module | Description | Condition d'activation |
|---|---|---|
| `population.iviapur` | IVIA pour population générale | ARR 1,8M$ |
| `traduction.tempsreel` | Oreillette de traduction, langues vivantes | R&D complétée Phase 1 |
| `modele.proprietaire` | Fine-tuning modèle IA IVIA | Dataset 5000+ cas |
| `reseau.s4` | Annuaire référencement éthique | MRR 60K$+ |

### Modules Futurs Non Définis
La plateforme accepte des modules dont la nature n'est pas encore connue. C'est l'objet même de cette architecture.

> Règle : Un module futur non prévu ici sera intégré s'il satisfait le Protocole de Connexion Modulaire. Son absence de cette liste n'est pas un refus.

---

## Vision Traduction des Langues Vivantes

La vision à long terme de MERLIN inclut la capacité pour chaque personne de parler sa propre langue et d'être comprise — non seulement par une traduction mécanique, mais par une traduction qui préserve le sens vivant, les nuances culturelles, et les épistémologies propres à chaque peuple.

Ce module commence par la co-construction avec les nations autochtones du Québec.

**Principe directeur** : la langue n'est pas un problème technique à résoudre. C'est une façon d'être au monde. La traduction doit préserver cette façon d'être, pas l'effacer.

**Trajectoire** :
```
M6-M18   → R&D avec nations autochtones QC (langues vivantes, épistémologies)
M18-M36  → Corpus de traduction co-construit, sans appropriation
M36+     → Intégration temps réel, préservation culturelle active
```

---

## Seuils de Production par Phase

```
PHASE 0 — Maintenant → M6
Objectif : Invariants stables, pipeline validé en conditions réelles
Seuil Go → Phase 1 : 30 séances complètes, zéro incident pipeline, 2 praticiennes actives

PHASE 1 — M6 → M18
Objectif : Premier module externe (nations autochtones), premier financement public
Seuil Go → Phase 2 : 1 accord partenariat nations, 1 financement obtenu, MRR 8K$+

PHASE 2 — M18 → M36
Objectif : Modules triage + ordres, R&D traduction active
Seuil Go → Phase 3 : MRR 25K$+, dataset 1000+ cas, 1 co-publication universitaire amorcée

PHASE 3 — M36 → M60
Objectif : IVIA population générale, traduction langues vivantes beta
Seuil Go → Phase 4 : ARR 1,8M$, modèle propriétaire opérationnel, 1 co-publication validée

PHASE 4 → Au-delà
Objectif : Modules non encore définis
Condition : Les invariants tiennent. Le protocole de connexion s'applique.
```

---

## Ce que cette architecture rend possible

- **Reconfiguration sans reconstruction** : chaque module peut être modifié, retiré ou remplacé sans affecter les autres
- **Remise en question non destructive** : un module qui ne fonctionne pas est retiré proprement, la plateforme continue
- **Progression sur 20 ans** : les besoins de 2046 ne sont pas connus aujourd'hui — cette architecture les acceptera
- **Diversité des usages** : nations autochtones, première ligne, ordres professionnels, population générale — même infrastructure, modules différents
- **Protection du secret** : l'architecture est publique, le pipeline interne reste protégé

---

## Règle de Modification de ce Document

Ce document peut être modifié uniquement si :
1. La modification est initiée par David Phaneuf
2. La modification ne contredit aucun des 7 principes IVIA
3. La modification est documentée avec date, version et justification
4. Les modules existants ne sont pas rendus incompatibles par la modification

> **Ce document ne protège pas contre le changement. Il protège contre le changement non intentionnel.**

---

*Document fondateur MERLIN — Plateforme évolutive*
*Commit initial : 25 juin 2026*
*Prochaine révision : M6 (décembre 2026)*

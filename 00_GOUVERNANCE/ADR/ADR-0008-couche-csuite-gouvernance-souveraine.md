---
titre: Couche C-suite — gouvernance souveraine de MERLIN (code CSUITE, dossier 06_CSUITE/)
id: ADR-0008
statut: accepted
couche: PROD
type: ADR
auteur: fondateur
date: 2026-06-30
version: 1.0
décideurs: fondateur
dépend_de: [ADR-0002, ADR-0007, MERLIN-PROMPTS-CONV-NOMMAGE-V1, MERLIN-PROMPTS-STANDARD-META-V1, MERLIN-INDEX-PROMPTS-V1]
remplace: []
remplacé_par: []
arbitrage_requis: oui — tout ajout ou retrait d'un agent C-suite, tout changement de rôle ou de périmètre décisionnel d'un agent existant
source_canonique: 00_GOUVERNANCE/ADR/ADR-0008-couche-csuite-gouvernance-souveraine.md
---

# ADR-0008 — Couche C-suite : gouvernance souveraine de MERLIN

> **Statut** : accepted — 2026-06-30  
> **Couche concernée** : PROD (gouvernance de la bibliothèque de prompts)  
> **Documents de référence** :
> - `11_PROMPTS/06_CSUITE/INDEX_CSUITE_V1.md`
> - `11_PROMPTS/PROMPTS_CONVENTION_NOMMAGE_V1.md`
> - `11_PROMPTS/AUDIT_CONFORMITE_CSUITE_V1.md`

---

## Contexte

ADR-0002 établit que tout prompt structurel de MERLIN est un document de gouvernance
versionné dans `11_PROMPTS/`. La bibliothèque existante couvre les couches opérationnelles :
`FOND`, `METH`, `EDIT`, `ADMIN`, `PROD` — soit les prompts qui guident le traitement des
séances, la génération de documents, et le routage.

Elle ne couvre pas la couche de **pilotage stratégique et opérationnel** de la plateforme :
les décisions d'architecture, de finances, de communications, de qualité, et d'expérience
utilisateur. Ces domaines étaient jusqu'ici exercés par le fondateur sans prompts gouvernés,
ce qui crée trois problèmes concrets :

1. **Incohérence de contexte entre outils IA** — Claude Code, Perplexity et Copilot
   reçoivent des instructions de pilotage ad hoc, sans référence partagée, ce qui produit
   des réponses contradictoires sur les mêmes décisions.

2. **Absence de garde-fous sur les décisions structurantes** — aucun prompt ne formalisait
   la hiérarchie de décision (qui décide quoi, dans quel ordre, avec quelle validation),
   exposant la plateforme à des décisions techniques ou éditoriales prises sans évaluation
   des impacts croisés.

3. **Convention de nommage incomplète** — `PROMPTS_CONVENTION_NOMMAGE_V1.md` définit
   six codes de couche (`SYSTEME`, `FOND`, `METH`, `EDIT`, `ADMIN`, `PROD`) mais aucun
   ne correspond à des prompts de pilotage C-suite. Ces agents ont une nature transversale
   distincte des prompts `SYSTEME` (identité du moteur) : ils orchestrent des rôles de
   direction, pas une identité système.

En juin 2026 (Vague 6), six agents C-suite ont été créés dans `11_PROMPTS/06_CSUITE/`
et soumis à audit (`AUDIT_CONFORMITE_CSUITE_V1.md`). L'audit a identifié que l'absence
d'un ADR rendait le code de couche `CSUITE` et le dossier `06_CSUITE/` non reconnus
par la structure canonique définie dans `INDEX_PROMPTS_V1.md`.

Ce présent ADR résout l'ensemble de ces points.

---

## Options considérées

**Option A — Rattacher les agents C-suite à la couche `SYSTEME` existante (`00_SYSTEME/`)**

Placer les 6 agents dans `00_SYSTEME/` avec un sous-dossier `CSUITE/`, en réutilisant
le code de couche `SYSTEME` déjà défini.

*Rejeté* : la couche `SYSTEME` est réservée aux prompts d'identité globale de MERLIN
(qui est MERLIN, quelles sont ses contraintes absolues en tant que moteur documentaire).
Les agents C-suite définissent des rôles de pilotage humain assisté par IA — ils sont
conceptuellement distincts. Les mélanger brouille la distinction entre l'identité du
moteur et la gouvernance de la plateforme. De plus, un futur développeur ou outil IA
lisant `00_SYSTEME/` s'attendrait à des prompts système, non à des personas de direction.

**Option B — Intégrer les agents C-suite dans les couches opérationnelles existantes**

Répartir selon le périmètre : MERLIN-ARCH dans `PROD`, MERLIN-COMM dans `EDIT`,
MERLIN-FIN dans `ADMIN`, etc.

*Rejeté* : cette fragmentation brise la cohérence du C-suite comme unité de gouvernance.
La valeur des agents C-suite réside précisément dans leur articulation mutuelle
(matrice de collaboration, mots-clés d'activation, arbitrages inter-agents).
Les disperser dans des dossiers distincts rend cette articulation invisible et non opérable.

**Option C — Créer un nouveau code de couche `CSUITE` et un dossier `06_CSUITE/` dédié**

Acter `CSUITE` comme septième code de couche dans la convention de nommage, avec
`06_CSUITE/` comme dossier canonique dans `11_PROMPTS/`, et mettre à jour la structure
cible dans `INDEX_PROMPTS_V1.md`.

*Retenu* : cohérence sémantique forte (le C-suite est une couche fonctionnellement distincte),
extensibilité (de nouveaux agents peuvent être ajoutés), lisibilité pour les outils IA
(Claude Code reconnaît immédiatement le rôle de la couche à la lecture du dossier),
et conformité avec le mécanisme d'extension prévu au §7 de `PROMPTS_CONVENTION_NOMMAGE_V1.md`.

---

## Décision

### 1. Création du code de couche `CSUITE`

Le code de couche `CSUITE` est officiellement ajouté à la convention de nommage MERLIN.

| Code | Couche | Dossier | Usage |
|---|---|---|---|
| `CSUITE` | Gouvernance souveraine | `11_PROMPTS/06_CSUITE/` | Prompts de pilotage stratégique, technique, financier, éditorial, UX et qualité — rôles de direction assistés par IA |

`PROMPTS_CONVENTION_NOMMAGE_V1.md` sera mis à jour en version `1.1` pour intégrer
cette entrée dans le tableau §2.

### 2. Format de nommage des agents C-suite

Les fichiers agents C-suite suivent la convention standard avec le nouveau code de couche :

```
MERLIN_PROMPT_CSUITE-[SUJET]_v[MAJOR].[MINOR].md
```

Les fichiers actuels (`MERLIN_PROMPT_CSUITE-STRAT_v1.0.md`, etc.) sont conformes à
ce format et **ne nécessitent pas de renommage**.

### 3. Structure cible mise à jour de `11_PROMPTS/`

```
11_PROMPTS/
├── INDEX_PROMPTS_V1.md
├── PROMPTS_CONVENTION_NOMMAGE_V1.md       ← v1.1 (ajout CSUITE)
├── PROMPTS_STANDARD_METADATA_V1.md
├── AUDIT_PROMPTS_EXISTANTS_V1.md
│
├── 00_SYSTEME/    ← identité globale du moteur MERLIN
├── 01_FOND/       ← doctrine, contexte culturel, cadre autochtone/québécois
├── 02_METH/       ← méthodes : note de séance, triage, orientation
├── 03_EDIT/       ← contenus publics : lettres, pages, offres
├── 04_ADMIN/      ← onboarding, routage, audit de dossier
├── 05_PROD/       ← validation technique, tests, schémas de sortie
└── 06_CSUITE/     ← gouvernance souveraine : agents C-suite de pilotage  ← NOUVEAU
```

### 4. Inventaire des six agents C-suite (Vague 6)

| ID | Fichier | Rôle | Périmètre | Statut |
|---|---|---|---|---|
| `MERLIN-PROMPT-CSUITE-STRAT-V1` | `MERLIN_PROMPT_CSUITE-STRAT_v1.0.md` | Stratège / CEO — roadmap, ADR, arbitrages | admin | draft |
| `MERLIN-PROMPT-CSUITE-ARCH-V1` | `MERLIN_PROMPT_CSUITE-ARCH_v1.0.md` | Architecte / CTO — stack, migrations, cohérence | backend | draft |
| `MERLIN-PROMPT-CSUITE-COMM-V1` | `MERLIN_PROMPT_CSUITE-COMM_v1.0.md` | Communications / CCO — marque, financement, contenu | admin | draft |
| `MERLIN-PROMPT-CSUITE-UX-V1` | `MERLIN_PROMPT_CSUITE-UX_v1.0.md` | Expérience / CXO — interfaces, composants, visibilité | frontend | draft |
| `MERLIN-PROMPT-CSUITE-FIN-V1` | `MERLIN_PROMPT_CSUITE-FIN_v1.0.md` | Finances / CFO — ROI, métriques, tarification | admin | draft |
| `MERLIN-PROMPT-CSUITE-QA-V1` | `MERLIN_PROMPT_CSUITE-QA_v1.0.md` | Qualité / DevOps — revue PR, migrations, monitoring | backend | draft |

### 5. Rôle et périmètre décisionnel de chaque agent

Chaque agent est souverain dans son domaine au sens suivant : il est la **référence
de premier recours** pour tout outil IA (Claude Code, Perplexity) qui traite une
question relevant de ce domaine. Aucun outil IA ne doit prendre de décision
structurante dans ces domaines sans avoir chargé le prompt de l'agent concerné.

**MERLIN-STRAT** est souverain sur :
- Toute décision qui modifie la mission, le positionnement ou les priorités de la plateforme
- La création ou le remplacement d'un ADR
- Les arbitrages entre strates de roadmap
- La préparation de dossiers de financement (volet stratégique)

**MERLIN-ARCH** est souverain sur :
- Tout choix d'implémentation touchant la stack (`10_backend_merlin_api/`, `09_app_ivia_merlin/`)
- Toute migration Alembic avant exécution
- L'introduction d'une nouvelle dépendance externe
- Le choix entre étendre l'existant vs créer un nouveau composant

**MERLIN-COMM** est souverain sur :
- Tout contenu destiné à une audience externe (site, infolettre, offre, pitch)
- La voix de marque IVIA dans toute communication
- Les sections narratives des dossiers de financement
- La conformité de tout contenu avec la posture non-clinique d'IVIA

**MERLIN-UX** est souverain sur :
- Tout nouveau composant frontend ou nouveau parcours utilisateur
- Les règles de visibilité (ce que le client peut voir vs le praticien)
- La spécification des états vides et des conditions d'affichage des visualisations
- La hiérarchie d'information dans les interfaces praticien, client et admin

**MERLIN-FIN** est souverain sur :
- L'évaluation du ROI de tout nouveau module avant implémentation
- La structure de tarification des plans praticien/client
- Les métriques financières clés (CAC, LTV, marge)
- Les projections et scénarios dans les dossiers de financement

**MERLIN-QA** est souverain sur :
- La validation de tout PR avant merge sur `master`
- La vérification de la chaîne Alembic avant toute migration
- Les critères de passage en production (tests, couverture, conformité ADR)
- La détection de régressions dans le pipeline `anthropic_session_note_pipeline.py`

### 6. Hiérarchie de décision inter-agents

Quand une décision implique plusieurs domaines, la séquence de consultation est :

```
STRAT (cadrage) → ARCH (faisabilité) → UX (design, si pertinent)
               → FIN (ROI)          → QA (validation avant merge)
```

Aucun agent ne peut autoriser une action qui relève du domaine d'un autre agent
sans l'avoir explicitement consultée. La validation finale appartient toujours
au **fondateur**.

### 7. Standard de livraison imposé aux agents C-suite

Tout agent C-suite doit respecter le standard `PROMPTS_STANDARD_METADATA_V1.md` avec
les règles supplémentaires suivantes, spécifiques à la couche `CSUITE` :

| Critère | Règle |
|---|---|
| `statut` | Toujours `draft` jusqu'à validation documentée. Ne jamais passer à `active` sans test réel. |
| `validation_requise` | Toujours `fondateur` — aucun agent C-suite ne peut être activé par un superviseur seul. |
| `arbitrage_requis` | Toujours `oui` pour tout changement de rôle, périmètre ou contrainte absolue. |
| `données_sensibles` | Déclarer `oui` pour tout agent qui traite des données financières réelles ou des transcriptions. |
| Section 7 (exemples) | Étiqueter `[EXEMPLE FICTIF]` obligatoirement. Remplacer par des sorties réelles documentées avant passage à `active`. |
| Contraintes absolues | Doivent contenir explicitement l'interdiction de décision finale sans validation fondateur. |

### 8. Procédure de validation vers le statut `active`

Un agent C-suite passe de `draft` à `active` selon la procédure suivante :

```
Étape 1 — Test sur modèle réel
  → Activer l'agent dans une session Claude (Sonnet 4 ou équivalent modèle_cible)
  → Soumettre au moins 2 entrées représentatives de son trigger d'activation
  → Documenter les sorties obtenues (fichier ou section dans le prompt)

Étape 2 — Vérification des contraintes absolues
  → Confirmer que l'agent refuse de produire une décision finale sans validation fondateur
  → Confirmer que l'agent respecte la posture non-clinique si son périmètre touche au contenu client
  → Confirmer qu'aucune sortie ne viole les données_sensibles de son niveau déclaré

Étape 3 — Mise à jour du fichier
  → Remplacer l'exemple fictif (section 7) par une sortie réelle représentative,
    ou conserver l'exemple fictif avec mention [EXEMPLE FICTIF — validé le YYYY-MM-DD]
  → Bumper la version (v1.0 → v1.1 si seuls les exemples changent)
  → Passer statut: draft → statut: active

Étape 4 — Validation fondateur
  → Commit signé par le fondateur avec message : "chore(prompts): activate [AGENT-ID] v[N]"
  → Mise à jour de INDEX_CSUITE_V1.md — colonne Statut

Étape 5 — Mise à jour de INDEX_PROMPTS_V1.md
  → Mettre à jour le statut dans le tableau de la Vague 6
```

Un agent `active` peut être utilisé par Claude Code sans supervision explicite dans son
domaine déclaré. Un agent `draft` ne peut être utilisé qu'en session supervisée par le fondateur.

---

## Conséquences

### Avantages

- La gouvernance de MERLIN est complète : les couches opérationnelles (METH, EDIT, etc.)
  sont désormais encadrées par une couche de pilotage formalisée et auditable.
- Claude Code, Perplexity et tout futur outil IA ont une référence unique pour chaque
  domaine décisionnel — les incohérences inter-sessions sont réduites structurellement.
- La hiérarchie de décision est explicite et traçable : toute décision structurante
  peut être retracée à l'agent consulté et à la validation du fondateur.
- Le dossier `06_CSUITE/` est extensible : de nouveaux agents (ex. `MERLIN-DATA` pour
  la gouvernance des données, `MERLIN-LEGAL` pour la conformité) peuvent être ajoutés
  par ADR complémentaire sans modifier ce document.

### Inconvénients ou risques

- Surcharge de processus si chaque décision mineure déclenche une consultation d'agent.
  → Règle de mitigation : les agents C-suite sont des références, pas des checklists
    obligatoires. Ils sont activés sur les décisions structurantes (ADR, nouveau module,
    contenu externe, migration, PR critique). Les décisions courantes n'en ont pas besoin.
- Risque de désynchronisation si les agents ne sont pas mis à jour lors des évolutions
  de stack ou de doctrine.
  → Règle de mitigation : tout ADR qui modifie la stack, la doctrine ou la tarification
    doit inclure une action de révision de l'agent C-suite concerné.

### Actions requises

- [ ] Mettre à jour `PROMPTS_CONVENTION_NOMMAGE_V1.md` v1.1 — ajouter `CSUITE` au tableau §2 et `06_CSUITE/` au tableau §5
- [ ] Mettre à jour `INDEX_PROMPTS_V1.md` — ajouter `06_CSUITE/` à la structure cible §Structure cible
- [ ] Ajouter `YAML frontmatter` à `SCHEMA_ETAT_REEL.md` (ID : `MERLIN-SCHEMA-REEL-V1`) pour permettre les références depuis `dépend_de` dans MERLIN-ARCH
- [ ] Mettre à jour `dépend_de` de `MERLIN-ARCH` : remplacer `SCHEMA_ETAT_REEL` par `MERLIN-SCHEMA-REEL-V1`
- [ ] Valider et activer les 6 agents C-suite selon la procédure §8 (par agent, selon disponibilité)
- [ ] Mettre à jour `CLAUDE.md` — section "Module comportemental" : remplacer la référence à `docs/11PROMPTS/06_CSUITE/` par `11_PROMPTS/06_CSUITE/` (chemin réel dans le repo)

---

## Entrée registre associée

> DEC-042 | 2026-06-30 | gouvernance-prompts | couche CSUITE — code de couche + dossier 06_CSUITE/ + procédure validation agents | accepted | ADR-0008

---

## Historique de révisions

| Version | Date | Auteur | Nature de la révision |
|---|---|---|---|
| 1.0 | 2026-06-30 | fondateur | Création initiale — Vague 6 agents C-suite |

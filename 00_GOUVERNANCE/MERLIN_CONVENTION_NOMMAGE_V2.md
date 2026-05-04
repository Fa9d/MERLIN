# MERLIN — Convention de nommage unique (v2)

> **Remplace MERLIN_CONVENTION_NOMMAGE_V1.md**

Date: 2026-05-04
Statut: active
Objet: eliminer le bruit et rendre MERLIN scalable
Modifications v2: formalisation du code domaine IVIA_, ajout BACK_ et FRONT_, tableau codes domaine complet

---

## 1) Principe directeur

Un fichier = un role clair.
Un nom = un sens stable.
Une structure = un parcours previsible.

Objectif:
- lire vite
- trier vite
- auditer vite
- migrer sans ambiguite

---

## 2) Arborescence canonique MERLIN

```
C:\MERLIN
  00_GOUVERNANCE
  01_FONDEMENTS
  02_NATIONS_QC
  03_MODELES
  04_METHODES
  05_PREUVES
  06_IMPORTS
  07_PRODUITS
  08_OPERATIONS
  09_EXPORTS
  memory
```

Rôle:
- 00_GOUVERNANCE: decisions, politiques, conventions
- 01_FONDEMENTS: philosophie, doctrine, charte
- 02_NATIONS_QC: fiches-nations, concepts, verification
- 03_MODELES: modeles de gouvernance, modeles socio-techniques
- 04_METHODES: playbooks, scripts, workflows
- 05_PREUVES: references, sources, audits, manifestes
- 06_IMPORTS: imports one-way depuis sources historiques/externe (dont MÉSANGE) avec horodatage
- 07_PRODUITS: EMPLOI, SOIN, COVOITURAGE, CITOYENNETE
- 08_OPERATIONS: roadmaps, sprints, KPI, runbooks
- 09_EXPORTS: livrables publies et versions de diffusion
- memory: couche memoire operationnelle

---

## 3) Format de nommage des fichiers

Format obligatoire:

`MERLIN_[DOMAINE]_[TYPE]_[SUJET]_v[MAJOR].[MINOR].md`

**Exception autorisee — corpus IVIA** (voir section 4) :

`IVIA_[TYPE]_[SUJET]_v[MAJOR].[MINOR].md`

Exemples:
- `MERLIN_GOUV_POLICY_NOMMAGE_v1.0.md`
- `MERLIN_FOND_CHARTE_PRINCIPES_v1.0.md`
- `MERLIN_NATQ_FICHE_KANIENKEHAKA_v1.0.md`
- `MERLIN_EMP_SPEC_TUNNEL_FDU_v1.0.md`
- `IVIA_DOCUMENT_DIRECTEUR_v1.0.md`
- `IVIA_ARTICLE_1_1_v1.0.md`

Regles:
1. ASCII uniquement
2. MAJUSCULES pour les segments codes
3. underscore `_` comme separateur unique
4. pas d'espaces
5. pas d'accents
6. extension explicite (`.md`, `.csv`, `.json`)

---

## 4) Codes de domaine — Tableau complet

### 4a) Codes domaine MERLIN_ (prefix inclus dans le code)

| Code prefixe | Domaine | Usage typique |
|---|---|---|
| `MERLIN_GOUV_` | Gouvernance projet | Arbitrages, decisions, checklists, politiques |
| `MERLIN_FOND_` | Fondements MERLIN | Cadres philosophiques, chartes, doctrines |
| `MERLIN_NATQ_` | Nations du Quebec | Fiches-nations, concepts, verification autochtone |
| `MERLIN_MODL_` | Modeles | Modeles de gouvernance, modeles socio-techniques |
| `MERLIN_METH_` | Methodes | Playbooks, scripts, workflows, methodes |
| `MERLIN_PREU_` | Preuves/Sources | References, audits, sources verifiees |
| `MERLIN_IMPT_` | Imports one-way | Journaux d'import, manifestes, triage |
| `MERLIN_EMPL_` | Emploi | Specs produit emploi, KPI, API |
| `MERLIN_SOIN_` | Soin | Specs produit soin, ethique, API |
| `MERLIN_COVO_` | Covoiturage | Specs produit covoiturage, territoire |
| `MERLIN_CITO_` | Citoyennete | Specs produit citoyennete, diffusion |
| `MERLIN_OPER_` | Operations | Roadmaps, sprints, runbooks |
| `MERLIN_EXPO_` | Exports | Livrables publies, versions de diffusion |
| `MERLIN_MEMO_` | Memory | Couche memoire operationnelle |
| `MERLIN_BACK_` | Backend API | Specs techniques backend, contrats API |
| `MERLIN_FRONT_` | Frontend app | Specs techniques frontend, composants |

### 4b) Code domaine IVIA_ (corpus editorial — exception formalisee)

| Code prefixe | Domaine | Usage typique |
|---|---|---|
| `IVIA_` | Corpus editorial IVIA | Positionnement, articles, cercle, plan editorial |

**Regles specifiques au prefixe IVIA_ :**
- Reserve au corpus editorial et fondateur de la marque IVIA
- Ne pas utiliser pour la documentation technique (utiliser MERLIN_BACK_ ou MERLIN_FRONT_)
- Pas de code domaine intermediaire : `IVIA_[TYPE]_[SUJET]_v[MAJOR].[MINOR].md` directement
- Dossier cible : `01_FONDEMENTS/` (chartes, positionnement) ou `04_METHODES/articles/` (articles)

---

## 5) Codes de type (TYPE)

- CHARTE = charte
- POLICY = politique
- CADRE = cadre
- FICHE = fiche
- AUDIT = audit
- SPEC = specification
- PLAN = plan
- PLAYBOOK = guide operatoire
- KPI = indicateurs
- LOG = journal
- INDEX = index
- MAP = cartographie
- ARTICLE = article editorial (usage IVIA_)
- POSITIONNEMENT = document de positionnement (usage IVIA_)

---

## 6) Versionning

Regle semver documentaire:
- `v1.0` = version validee
- `v1.1` = ajustements mineurs
- `v2.0` = changement de structure ou de doctrine

Statut dans l'en-tete:
- `draft`
- `review`
- `validated`
- `deprecated`

---

## 7) Imports one-way (anti-bruit)

Format dossier import:
- `06_IMPORTS\YYYY-MM-DD_HHMMSS\...`

Format manifest:
- `MERLIN_IMPT_LOG_MANIFEST_v1.0.csv`

Regles:
1. jamais d'ecrasement silencieux
2. toute promotion vers dossier canon = decision tracee
3. la source importee ne devient pas automatiquement verite MERLIN

---

## 8) Nommage des dossiers produit

Dans `07_PRODUITS`:

```
07_PRODUITS
  EMPLOI
    SPEC
    API
    UX
    KPI
  SOIN
    SPEC
    API
    ETHIQUE
    KPI
  COVOITURAGE
    SPEC
    API
    TERRITOIRE
    KPI
  CITOYENNETE
    SPEC
    GOUVERNANCE
    DIFFUSION
    KPI
```

---

## 9) Regles d'hygiene

1. Un sujet ne doit pas exister dans 3 fichiers differents sans index.
2. Chaque fichier canon doit pointer vers ses preuves (05_PREUVES).
3. Les fichiers obsoletes passent en `deprecated` et sont archives, jamais supprimes sans trace.
4. Les titres doivent rester courts et explicites.

---

## 10) Convention de transition depuis l'existant

Pour les fichiers existants de type `MERLIN_01_...`:
1. conserver tel quel en `06_IMPORTS` (historique)
2. recreer les versions canoniques selon la convention v1 dans les dossiers cibles
3. journaliser chaque promotion dans `00_GOUVERNANCE`

---

## 11) Decision active

Cette convention est la base unique de nommage pour MERLIN a compter de maintenant.
Toute derogation doit etre motivee et tracee.

---

## 12) Historique des versions

| Version | Date | Auteur | Modifications |
|---|---|---|---|
| v1 | 2026-04-11 | David Phaneuf | Version initiale |
| v2 | 2026-05-04 | David Phaneuf | Formalisation IVIA_, ajout BACK_ et FRONT_, tableau domaine complet, exemples IVIA_ |

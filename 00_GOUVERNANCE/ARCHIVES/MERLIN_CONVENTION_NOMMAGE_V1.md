# MERLIN — Convention de nommage unique (v1)

Date: 2026-04-11
Statut: active
Objet: eliminer le bruit et rendre MERLIN scalable

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

Exemples:
- `MERLIN_GOUV_POLICY_NOMMAGE_v1.0.md`
- `MERLIN_FOND_CHARTE_PRINCIPES_v1.0.md`
- `MERLIN_NATQ_FICHE_KANIENKEHAKA_v1.0.md`
- `MERLIN_EMP_SPEC_TUNNEL_FDU_v1.0.md`

Regles:
1. ASCII uniquement
2. MAJUSCULES pour les segments codes
3. underscore `_` comme separateur unique
4. pas d'espaces
5. pas d'accents
6. extension explicite (`.md`, `.csv`, `.json`)

---

## 4) Codes de domaine (DOMAINE)

- GOUV = gouvernance
- FOND = fondements
- NATQ = nations du Quebec
- MODL = modeles
- METH = methodes
- PREU = preuves/sources
- IMPT = imports
- EMPL = emploi
- SOIN = soin
- COVO = covoiturage
- CITO = citoyennete
- OPER = operations
- EXPO = exports
- MEMO = memory

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

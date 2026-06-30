---
titre: Anatomie d'un siège C-suite + circulation des artefacts
id: MERLIN-CSUITE-ANATOMIE-SIEGE-V1
statut: active
type: charte
couche: SYSTEME
périmètre: admin
auteur: fondateur
date: 2026-06-30
version: 1.0
dépend_de: [ADR-0008, MERLIN-INDEX-CSUITE-V1, MERLIN-PROMPTS-STANDARD-META-V1]
source_canonique: 11_PROMPTS/06_CSUITE/_anatomie-siege.md
---

# Anatomie d'un siège C-suite + circulation des artefacts V1.0

> Convention opérationnelle du bureau MERLIN. Découle d'ADR-0008.
> Le siège **COS** (chief of staff) fait respecter cette convention à chaque session.

---

## 1. Principe : un siège = une cellule autonome

Chaque siège du bureau est une **cellule** rangée dans son propre dossier sous
`11_PROMPTS/06_CSUITE/<SIEGE>/`. Fini les prompts à plat. Une cellule répond à trois
questions : *ses prompts*, *ce qu'il traite*, *où vont ses résultats*.

```
11_PROMPTS/06_CSUITE/
├── _index.md            ← registre central des sièges
├── _anatomie-siege.md   ← CE document (le gabarit)
├── _circulation.md      ← carte de routage des artefacts (à produire)
│
└── <SIEGE>/
    ├── siege.md         ← manifeste : identité · périmètre · circulation
    ├── prompts/
    │   └── <siege>-<fonction>.vX.Y.md
    └── artefacts/       ← gabarits des sorties produites par le siège
```

---

## 2. Les 4 faces d'un siège (contenu de `siege.md`)

| Face | Contenu | Exemple (STRAT) |
|---|---|---|
| **Identité** | rôle, analogie, modèle cible, statut | CEO / cadrage stratégique |
| **Périmètre — *ce qu'il traite*** | objets/décisions dont il est responsable + triggers | ADR, roadmap, arbitrages, dossiers de financement |
| **Prompts** | un ou plusieurs, versionnés | `prompts/strat-cadrage.v1.0.md` |
| **Circulation** | entrées (qui l'active) + sorties (artefacts typés) + routage | produit des ADR → `00_GOUVERNANCE/` + sièges concernés |

Règle : `siege.md` est lisible **sans** ouvrir le prompt. C'est la fiche de poste ;
le prompt est l'outil.

---

## 3. Cycle de vie d'un appel de siège

```
        DEMANDE
  (fondateur · autre siège · trigger)
            │
            ▼
   ┌─────────────────────┐
   │     SIÈGE  X         │  charge: son prompt + son périmètre
   └─────────┬───────────┘
             │ produit
             ▼
      ARTEFACT TYPÉ
   (ADR · spec · avis · plan · contrat)
             │
             ▼
   ┌─────── ROUTAGE (selon le type) ───────┐
   ▼            ▼              ▼            ▼
 fondateur   autre siège   gouvernance /  instance
(validation) (= son entrée) kernel        IVIA
```

Un siège ne **décide** jamais seul : il produit un **artefact typé**, et c'est le **routage**
qui le distribue. Un artefact peut devenir l'entrée d'un autre siège — la collaboration
inter-sièges est un *flux*, pas une simple table.

---

## 4. Table de circulation (« distribué selon les besoins »)

Source canonique du routage (à maintenir dans `_circulation.md`). Chaque artefact a une
**destination déclarée** — c'est ce qui empêche les orphelins.

| Siège | Artefact produit | Distribué vers | Statut |
|---|---|---|---|
| STRAT | ADR · roadmap | `00_GOUVERNANCE/` + sièges concernés | actif |
| ARCH | spec technique · ticket | `instances/ivia/produit/` + QA | actif |
| FIN | modèle financier · revue | STRAT + fondateur | actif |
| COMM | contenu · dossier financement | instance + fondateur | actif |
| UX | spec de parcours · maquette | ARCH + QA | actif |
| QA | rapport de revue · validation | ARCH + fondateur (gate avant merge) | actif |
| **GROWTH** | plan d'acquisition · expérience | FIN + COMM + instance | actif |
| **LEGAL** | avis de conformité · contrat | `12_JURIDIQUE_AFFAIRES/` + fondateur | actif |
| **COS** | ordre du jour · relevé de décisions | **tous les sièges** (orchestration) | actif |
| **OPS** | playbook onboarding · suivi churn | GROWTH + FIN | dormant |
| **DATA** | tableau de rentabilité par méthode | STRAT + FIN | dormant |
| **CARE** | contrat gardien (par objet) | `contrats/<objet>/` + **toutes les instances** | actif |

---

## 5. CARE : une couture verticale, pas un siège horizontal

Les autres sièges *dirigent l'entreprise* — leurs artefacts circulent horizontalement.
CARE *définit ce qui est analysé et sous quelles garanties* — son artefact descend
verticalement sur toutes les instances.

```
   STRAT ─ ARCH ─ FIN ─ GROWTH ─ LEGAL ─ … ─ COS   (bureau horizontal)
            │ artefacts circulent entre eux
            ▼
   ╔════════════════════════════════════╗
   ║  CARE — contrat gardien par objet  ║          (couture verticale)
   ╚════════════════════════════════════╝
            │ s'applique à
            ▼
   instances/ → ivia {client, praticien} → marché #2 {objet …}
```

CARE produit **un contrat par objet d'analyse** : `contrats/client/`, `contrats/praticien/`,
puis un dossier par futur objet. Voir ADR-0008 §3.

---

## 6. Règles d'hygiène (rappel ADR-0008 §6)

- **Un fait = une source canonique.** Un siège ne crée pas un doc à côté ; il bumpe la
  version de son canon ou marque l'ancien `superseded` + `remplace`.
- **Aucun orphelin** : pas d'artefact sans destination dans la table de circulation.
- **Intrants gelés** : la matière brute consommée par un siège va à `_archives/intrants/`.

---

## Historique de révisions

| Version | Date | Auteur | Nature de la révision |
|---|---|---|---|
| 1.0 | 2026-06-30 | fondateur | Création initiale — anatomie + circulation (ADR-0008) |

---
titre: Index des sièges C-suite — MERLIN
id: MERLIN-INDEX-CSUITE-V1
statut: active
type: index
couche: SYSTEME
périmètre: admin
auteur: fondateur
date: 2026-06-30
version: 1.1
dépend_de: [ADR-0008, MERLIN-CSUITE-ANATOMIE-SIEGE-V1, MERLIN-CSUITE-CIRCULATION-V1]
remplace: []
arbitrage_requis: non — index de référence
source_canonique: 11_PROMPTS/06_CSUITE/INDEX_CSUITE_V1.md
---

# MERLIN — Index des sièges C-suite V1.1

> **Statut** : active — 2026-06-30
> **Structure** : un dossier par siège (cellule). Voir `_anatomie-siege.md` (gabarit) et
> `_circulation.md` (routage des artefacts). Décision fondatrice : **ADR-0008**.

---

## Principe

Les sièges C-suite **orchestrent** les prompts des couches inférieures (METH, FOND, EDIT,
PROD, ADMIN), ils ne les remplacent pas. Chaque siège est une **cellule autonome** :
`<SIEGE>/siege.md` (manifeste) + `<SIEGE>/prompts/` + circulation déclarée.

Aucun siège ne décide seul : il produit un **artefact typé** que le routage distribue
(`_circulation.md`). Validation finale = fondateur.

---

## Registre des sièges

| Siège | Rôle / Analogie | Statut | Cellule |
|---|---|---|---|
| STRAT | Stratégie, roadmap, arbitrages — CEO | actif | `STRAT/` |
| ARCH | Architecture, stack, migrations — CTO | actif | `ARCH/` |
| FIN | Finances, ROI, tarification — CFO | actif | `FIN/` |
| COMM | Communications, contenu, financement — CCO | actif | `COMM/` |
| UX | Expérience, parcours, design — CXO | actif | `UX/` |
| QA | Qualité, DevOps, tests — VP QA/DevOps | actif | `QA/` |
| **GROWTH** | Mise en marché, acquisition — CRO | actif | `GROWTH/` |
| **LEGAL** | Conformité Loi 21/25, contrats, risque — General Counsel | actif | `LEGAL/` |
| **COS** | Cadence, orchestration, hygiène — Chief of Staff | actif | `COS/` |
| **OPS** | Opérations, succès client, rétention — COO | dormant | `OPS/` |
| **DATA** | Données, rentabilité des méthodes — CDO | dormant | `DATA/` |
| **CARE** | Couture de domaine — contrats gardiens (par objet) | actif | `CARE/` → `contrats/` |

> **CARE est un cas spécial** : non un pair horizontal, mais la couture verticale entre le
> noyau et l'objet d'analyse. Il s'exprime par des **contrats** (`contrats/client/`,
> `contrats/praticien/`), pas par une session générative.

---

## Documents de référence du bureau

| Fichier | Rôle |
|---|---|
| `_anatomie-siege.md` | Gabarit d'un siège (4 faces) + cycle de vie d'un appel |
| `_circulation.md` | Table canonique de routage des artefacts |
| `INDEX_CSUITE_V1.md` | Ce registre |

---

## Règles d'utilisation

1. **Un siège = un rôle** — ne pas combiner deux sièges dans une même session.
2. **Toujours valider avec le fondateur** — un siège recommande, le fondateur décide.
3. **Produire un artefact** — chaque session produit un artefact à destination déclarée.
4. **Respecter la séquence** — décision d'implémentation : STRAT → ARCH → UX → FIN → QA.
5. **Sortie client/praticien** — passe toujours par le **contrat CARE** de l'objet concerné.
6. **Hygiène** — le siège COS fait respecter la loi de circulation des sources (ADR-0008 §6).

---

## Historique de révisions

| Version | Date | Auteur | Nature de la révision |
|---|---|---|---|
| 1.0 | 2026-06-29 | fondateur | Création initiale — 6 agents C-suite (à plat) |
| 1.1 | 2026-06-30 | fondateur | Cellules par siège + 5 nouveaux sièges + CARE (ADR-0008) |

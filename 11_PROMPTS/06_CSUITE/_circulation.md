---
titre: Circulation des artefacts du bureau C-suite
id: MERLIN-CSUITE-CIRCULATION-V1
statut: active
type: charte
couche: SYSTEME
périmètre: admin
auteur: fondateur
date: 2026-06-30
version: 1.0
dépend_de: [ADR-0008, MERLIN-CSUITE-ANATOMIE-SIEGE-V1]
source_canonique: 11_PROMPTS/06_CSUITE/_circulation.md
---

# Circulation des artefacts du bureau C-suite V1.0

> **Source canonique du routage.** Tenu à jour par le siège COS. Chaque artefact a une
> **destination déclarée** — c'est la règle « aucun orphelin » (ADR-0008 §6).

## Table de circulation

| Siège | Artefact produit | Distribué vers | Statut |
|---|---|---|---|
| STRAT | ADR · roadmap · note d'arbitrage | `00_GOUVERNANCE/` + sièges concernés | actif |
| ARCH | spec technique · ticket · note de migration | `instances/ivia/produit/` + QA | actif |
| FIN | modèle financier · revue · reco de prix | STRAT + fondateur | actif |
| COMM | contenu éditorial · dossier de financement | instance + fondateur | actif |
| COMM | blogue (canon : `09_blog_app/`, articles + app Next.js) | export statique dérivé → `ivia_site_v2/ressources/blog/` (gate Loi 21 avant prod) | actif |
| UX | spec de parcours · maquette · règle d'affichage | ARCH + QA | actif |
| QA | rapport de revue · validation/refus · ticket incident | ARCH + fondateur (gate merge) | actif |
| GROWTH | plan d'acquisition · protocole d'expérience · plan de mise en marché | FIN + COMM + instance | actif |
| LEGAL | avis de conformité · clause/contrat · checklist de risque | `12_JURIDIQUE_AFFAIRES/` + fondateur | actif |
| COS | ordre du jour · relevé de décisions · to-do · alerte hygiène | **tous les sièges** + `05_JOURNAUX/` | actif |
| OPS | playbook onboarding · suivi de churn · protocole de succès | GROWTH + FIN | dormant |
| DATA | tableau de rentabilité par méthode · fiche d'évaluation de modèle | STRAT + FIN | dormant |
| CARE | **contrat gardien** (par objet d'analyse) | `contrats/<objet>/` + **toutes les instances** | actif |

## Flux remarquables (un artefact devient l'entrée d'un autre siège)

- **Décision structurante** : STRAT (ADR) → ARCH (faisabilité) → UX (design) → FIN (ROI) → QA (validation).
- **Mise en marché** : GROWTH (plan) → COMM (message) + FIN (CAC) → instance (mise en œuvre).
- **Sortie orientée client/praticien** : siège producteur → **CARE** (contrat gardien de l'objet) → QA (gate) → fondateur.
- **Tout connecteur / donnée nouvelle** : siège demandeur → LEGAL (avis) → fondateur.

## Règles

1. **Aucun orphelin** : un artefact sans destination dans cette table ne doit pas être produit.
2. **Un fait = une source canonique** : un siège ne duplique pas, il bumpe ou marque `superseded`.
3. **Vertical vs horizontal** : CARE descend sur les instances ; les autres circulent entre eux.
4. **COS garde la table** : toute évolution d'un siège ou d'un artefact se reflète ici.

## Historique
| Version | Date | Auteur | Nature |
|---|---|---|---|
| 1.0 | 2026-06-30 | fondateur | Création initiale — circulation (ADR-0008) |
| 1.1 | 2026-07-17 | COS | Unification dépôts : blogue rapatrié dans `09_blog_app/`, destination déclarée |

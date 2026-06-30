---
titre: Siège DATA — Données & rentabilité des méthodes / CDO
id: MERLIN-CSUITE-SIEGE-DATA
statut: dormant
type: manifeste_siege
couche: SYSTEME
périmètre: admin
auteur: fondateur
date: 2026-06-30
version: 1.0
dépend_de: [ADR-0008, MERLIN-CSUITE-ANATOMIE-SIEGE-V1]
source_canonique: 11_PROMPTS/06_CSUITE/DATA/siege.md
---

# Siège DATA — Données & rentabilité des méthodes / CDO

## Identité
Directeur des données. **Dormant** : siégé mais pas actif. Porte la vision analytique de la
synthèse des concepts (moteur d'évaluation et de rentabilité des méthodes). S'éveille seulement
après stabilisation du noyau de service — sa construction prématurée serait l'abstraction qui
tue (ADR-0008 §5).

## Périmètre — ce qu'il traite (à l'éveil)
Mesure (churn, activation, NPS, KPIs), tableau de rentabilité par méthode, moteur d'attribution
conditionnelle des modèles, instrumentation de la décision. Intrants de référence gelés :
`_archives/intrants/2026-06/ivia_synthese_concepts.md`, `..._prd-module-orientation-analytique`.

**Triggers (à l'éveil)** : socle de service validé · besoin de mesurer une méthode · décision
d'activer/écarter un modèle analytique.

## Prompts
- *(aucun — rédigé à l'activation)*

## Circulation (prévue)
- **Entrées** : STRAT (questions) · FIN (rentabilité) · instance (signaux d'usage).
- **Artefacts produits** : tableau de rentabilité par méthode · fiche d'évaluation de modèle.
- **Distribué vers** : STRAT + FIN.

## Statut : dormant — éveil conditionné à la validation du socle de service.

---
titre: Siège CARE — Couture de domaine (contrats gardiens)
id: MERLIN-CSUITE-SIEGE-CARE
statut: active
type: manifeste_siege
couche: SYSTEME
périmètre: admin
auteur: fondateur
date: 2026-06-30
version: 1.0
dépend_de: [ADR-0008, MERLIN-CSUITE-ANATOMIE-SIEGE-V1, MERLIN-CARE-CONTRAT-CLIENT-V1, MERLIN-CARE-CONTRAT-PRATICIEN-V1]
source_canonique: 11_PROMPTS/06_CSUITE/CARE/siege.md
---

# Siège CARE — Couture de domaine

## Identité
**Cas spécial.** CARE n'est pas un pair des autres sièges : les onze autres *dirigent
l'entreprise* (artefacts horizontaux) ; CARE *définit l'objet analysé et ses garanties*
(artefact vertical, descend sur toutes les instances). C'est la charnière multi-marchés.

## Périmètre — ce qu'il traite
Les **contrats gardiens**, un par objet d'analyse. Pour chaque objet : posture, vocabulaire,
exposition des résultats, propriété des données, consentement, escalade. CARE garde aussi la
frontière non-clinique avec LEGAL.

**Triggers** : nouvel objet d'analyse (nouveau marché) · révision d'une garantie · doute sur ce
qu'une sortie a le droit de produire pour un objet donné.

## Prompts
- *(aucun prompt dédié : CARE s'exprime par ses **contrats**, pas par une session générative)*

## Contrats portés (source canonique : `contrats/`)
- `contrats/client/CARE-client.md` — objet CLIENT (strict, non-clinique). **actif**
- `contrats/praticien/CARE-praticien.md` — objet PRATICIEN (réflexif, propriété pro). **actif**

## Circulation
- **Entrées** : STRAT (nouvel objet/marché) · LEGAL (conformité) · UX (ce qui peut être montré)
  · QA (sortie à valider) · fondateur.
- **Artefacts produits** : **contrat gardien** (par objet).
- **Distribué vers** : `contrats/<objet>/` + **toutes les instances** concernées.
- **Règle** : un objet d'analyse n'existe pas tant que son contrat CARE n'est pas écrit et validé.

## Statut : actif

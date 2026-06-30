# `contrats/` — contrats gardiens CARE (par objet d'analyse)

> Découle d'ADR-0008. CARE n'est pas un siège horizontal du bureau : c'est la **couture
> verticale** entre le noyau MERLIN et un **objet d'analyse**. Un objet = un contrat.

Chaque contrat définit, pour un objet d'analyse donné, ce que le système a le droit de
produire et sous quelles garanties : posture, vocabulaire, exposition des résultats, propriété
des données, consentement, escalade.

**Changer l'objet d'analyse → changer le contrat → le même noyau dessert un autre marché.**
C'est le mécanisme de modularité et de scalabilité multi-marchés.

## Contrats actifs

| Objet d'analyse | Contrat | Posture |
|---|---|---|
| **Client** (personne accompagnée) | `client/CARE-client.md` | strict — non-clinique, Loi 21 |
| **Praticien** (professionnel consentant) | `praticien/CARE-praticien.md` | réflexif — auto-évaluation, propriété pro |

## Règle d'ajout d'un objet

Un nouvel objet d'analyse (donc un nouveau marché) **n'existe pas** tant que son contrat CARE
n'est pas écrit et validé. Le contrat précède l'instance.

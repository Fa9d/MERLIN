# JOURNAL DE BORD — PILOTE MERLIN

**Document opérationnel** · Statut : actif
**Pilote actif depuis** : 31 mai 2026
**Praticiennes pilotes** : Mylène, Émilie
**Responsable du journal** : David Phaneuf (fondateur)
**Cycle de mise à jour** : hebdomadaire (revue lundi matin)
**Référence méthodologique** : `04_METHODES/IVIA_MANUEL_OPERATIONS_PILOTE_v1.0.md`
**Devises** : *Au sein de l'être — En actes.* / *Pour le peuple, par le peuple.*

---

## OBJET DU DOCUMENT

Ce journal trace en continu l'activité réelle du pilote MERLIN — séances réalisées, retours praticiennes, retours clients, incidents, ajustements, métriques, décisions opérationnelles.

Il complète :
- les **journaux de déploiement technique** (`JOURNAL_DEPLOY_*.md`) qui tracent l'infrastructure
- le **manuel opérations pilote** (`IVIA_MANUEL_OPERATIONS_PILOTE_v1.0.md`) qui définit les rituels
- la **cartographie des risques** (`IVIA_CARTOGRAPHIE_RISQUES_v1.0.md`) qui anticipe les angles morts

**Important** : ce journal **n'est pas un dossier clinique**. Aucune donnée personnelle de client (nom, contact, contenu de séance) n'y figure. Les retours clients sont anonymisés et agrégés. Les retours praticiennes peuvent être nominatifs (Mylène, Émilie) avec leur consentement.

---

## RÉFÉRENTIELS DE COHÉRENCE

| Document | Lien | Pertinence |
|---|---|---|
| Manuel opérations pilote | [`../../04_METHODES/IVIA_MANUEL_OPERATIONS_PILOTE_v1.0.md`](../../04_METHODES/IVIA_MANUEL_OPERATIONS_PILOTE_v1.0.md) | Rituels, rôles, Go/No-Go M6 |
| Cartographie risques | [`../IVIA_CARTOGRAPHIE_RISQUES_v1.0.md`](../IVIA_CARTOGRAPHIE_RISQUES_v1.0.md) | Identifier triggers de risque en temps réel |
| Politique bien-être praticiens | [`../IVIA_POLITIQUE_BIEN_ETRE_PRATICIENS_v1.0.md`](../IVIA_POLITIQUE_BIEN_ETRE_PRATICIENS_v1.0.md) | Surveillance traumatisme vicariant |
| Manuel formation praticiens | [`../../04_METHODES/IVIA_MANUEL_FORMATION_PRATICIENS_v1.0.md`](../../04_METHODES/IVIA_MANUEL_FORMATION_PRATICIENS_v1.0.md) | Maintien compétences, points de supervision |
| Protocole urgence détresse | [`../IVIA_PROTOCOLE_URGENCE_DETRESSE_v1.0.md`](../IVIA_PROTOCOLE_URGENCE_DETRESSE_v1.0.md) | Cadre déclenchement bascule |
| CGU clients v1.1 | [`../../12_JURIDIQUE_AFFAIRES/IVIA_CGU_CLIENTS_v1.1.md`](../../12_JURIDIQUE_AFFAIRES/IVIA_CGU_CLIENTS_v1.1.md) | Cadre contractuel actif |
| Politique confidentialité v1.1 | [`../../12_JURIDIQUE_AFFAIRES/IVIA_POLITIQUE_CONFIDENTIALITE_LOI25_v1.1.md`](../../12_JURIDIQUE_AFFAIRES/IVIA_POLITIQUE_CONFIDENTIALITE_LOI25_v1.1.md) | Cadre Loi 25 actif |

---

## RITUELS PRATIQUÉS (issus du Manuel opérations pilote)

| Rituel | Fréquence | Responsable | Trace dans ce journal |
|---|---|---|---|
| Check-in praticienne | quotidien (5 min) | David | Section *Notes quotidiennes* |
| Revue hebdomadaire pilote | lundi matin (45 min) | David + 2 praticiennes | Section *Revues hebdomadaires* |
| Revue mensuelle | premier lundi du mois (1h30) | David + 2 praticiennes | Section *Revues mensuelles* |
| Revue trimestrielle Go/No-Go | M3, M6 | David + Conseil consultatif | Section *Jalons* |

---

## TEMPLATE — ENTRÉE HEBDOMADAIRE

> Copier ce bloc à chaque revue du lundi.

```markdown
### Semaine du AAAA-MM-JJ au AAAA-MM-JJ

**Séances réalisées** : N (Mylène : N₁ / Émilie : N₂)
**Séances annulées** : N (motifs : ...)
**Nouveaux clients onboardés** : N
**Incidents techniques** : N (cf. JOURNAL_DEPLOY si applicable)
**Bascules urgence détresse** : N (cf. PROTOCOLE_URGENCE_DETRESSE)

#### Retours Mylène
- État émotionnel post-séances : ...
- Qualité perçue de la transcription/note MERLIN : ...
- Difficultés rencontrées : ...
- Suggestions / besoins : ...

#### Retours Émilie
- État émotionnel post-séances : ...
- Qualité perçue de la transcription/note MERLIN : ...
- Difficultés rencontrées : ...
- Suggestions / besoins : ...

#### Retours clients (agrégés, anonymisés)
- Sentiment général : ...
- Points positifs récurrents : ...
- Points négatifs récurrents : ...

#### Décisions de la semaine
- ...

#### Actions pour la semaine suivante
- ...

#### Indicateurs (alimentent tableau de bord pilote — cf. note attention V3 #5)
- Taux de présence aux séances : ... %
- NPS approximatif : ...
- Temps moyen de production de la note post-séance : ... min

#### Liens / pièces jointes
- ...
```

---

## TEMPLATE — ENTRÉE MENSUELLE

```markdown
## Mois de [MOIS AAAA] — Bilan

### Chiffres consolidés
| Indicateur | Valeur | Variation vs mois précédent |
|---|---|---|
| Séances totales | ... | ... |
| Clients actifs | ... | ... |
| Annulations | ... | ... |
| Incidents techniques | ... | ... |
| Bascules urgence | ... | ... |
| NPS | ... | ... |

### Points saillants Mylène
...

### Points saillants Émilie
...

### Risques activés (cf. CARTOGRAPHIE_RISQUES)
- R# — Description — Action engagée

### Décisions opérationnelles
- ...

### Communication aux investisseurs (le cas échéant)
- ...

### Actions pour le mois suivant
- ...
```

---

## ENTRÉES — À COMPLÉTER

> **Note de démarrage (8 mai 2026)** : ce journal est créé en réaction à un angle mort signalé par l'audit `AUDIT_COHERENCE_POST_DEC-V3-15` — le pilote tourne avec Mylène et Émilie depuis le 31 mai 2026 mais aucune trace structurée de l'activité n'existait dans le repo. À compter de la prochaine revue hebdomadaire (lundi 11 mai 2026 si applicable, ou prochaine occurrence), David alimente ce journal en continu. Les entrées rétroactives pour la période 31 mai → 8 mai 2026 peuvent être consignées de mémoire si pertinent, en marquant explicitement *(reconstitution rétroactive)*.

### Reconstitution rétroactive — Période du 31 mai au 8 mai 2026 *(à compléter par David)*

> *Ce bloc reste vide tant que David n'a pas remonté de mémoire les éléments saillants de la première semaine du pilote. Si la mémoire est trop diffuse, marquer simplement « pas de reconstitution exploitable, journal démarré formellement le AAAA-MM-JJ ».*

---

## ANNEXE — JOURNAL DES VERSIONS DU TEMPLATE

| Version | Date | Changements |
|---|---|---|
| 1.0 | 2026-05-08 | Création initiale post-AUDIT_COHERENCE_POST_DEC-V3-15. Templates hebdo et mensuel. |

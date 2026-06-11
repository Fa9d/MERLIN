# IVIA — La Carte de Vie

**Version** : v0.1 — 2026-06-10 — **statut : PROPOSITION** (à amender par le fondateur)
**Auteur** : David Phaneuf (fondateur) + Claude Code
**Nature** : Doctrine fondatrice — *modèle d'organisation de l'être et d'accompagnement vers son autonomie vitale*
**Documents liés** :
- `correspondances-vivantes.md` (les 11 axes, source autoritative)
- `ivia_living_lexicon.yaml` (expressions → axes)
- `IVIA_DOCTRINE_CARTE_ABSTRAITE_v1.0.md` (carte abstraite du praticien)
- `IVIA_PROTOCOLE_RECHERCHE_TEMPORALITE_DECALEE_v1.0.md` (gap Y→Z, Ricœur)
- `../00_GOUVERNANCE/MERLIN_GOUV_SPEC_AXES_ANALYSE_CERCLE_V1.md` (Cercle, tensions)
- `../CLAUDE.md` §0 (trinité), §6.4 (constitution)

---

## 1. Intention

La **Carte de Vie** n'est **pas** un dossier clinique, ni une fiche, ni un score.
C'est une **représentation vivante de l'être dans son environnement** : un territoire que la
personne habite, traversé par le temps, façonné par la société, et orienté vers son
déploiement propre.

Elle répond à une conviction fondatrice d'IVIA :
> La plupart des déséquilibres ne naissent pas « dans » l'individu isolé, mais dans la
> rencontre entre un être vivant et la **construction sociale** qui l'entoure — son sol,
> son époque, ses institutions, ses héritages. On ne lit donc jamais une personne hors-sol.

La Carte de Vie est l'objet unique que **toutes les lentilles d'analyse alimentent** et que
**toutes les surfaces (client / praticien / observatoire) rendent** — chacune à sa manière.

---

## 2. Principe directeur : le sol d'abord

Conformément aux *correspondances vivantes*, l'ordre de lecture n'est pas neutre :
**on part du territoire, pas de l'individu abstrait.** Le corps et la psyché appartiennent
déjà à une terre, une langue, une époque. La Carte de Vie inscrit donc toute personne
**dans son sol et son temps avant de lire son intériorité**.

Posture non négociable (constitution §6.4, `safety.md`) :
- triade **Observation → Hypothèse → Orientation**, jamais diagnostic / pronostic / prescription ;
- vocabulaire conforme Loi 21 (pas de *thérapie*, *trouble*, *guérison*…) ;
- finalité = **autonomie vitale** et alignement, **jamais** promesse de guérison ni « réalisation » comme état final garanti ;
- toute détection d'urgence → escalade humaine immédiate, la carte ne « gère » rien.

---

## 3. Les cinq strates de la Carte de Vie

### Strate 0 — Le Sol *(territoire + époque)*
Le lieu vivant qui constitue la personne : territoire, langue du lieu, migration/déracinement,
et l'**époque** qui l'a façonnée. S'adosse au modèle `EraContext` (économie, normes, droits,
structure familiale d'un moment donné).

### Strate 1 — Les Onze Axes *(la coupe multidimensionnelle)*
La personne lue sur les 11 axes autoritatifs : `territoire, corps, metabolisme, emotions,
mental, relations, famille, transgenerationnel, societe, spirituel_existentiel,
urgence_reference`. Chaque axe porte un **état de résonance** (présent / actif / en tension /
en sourdine), jamais une note chiffrée brute exposée au client.

### Strate 2 — La Ligne de Vie *(le temps narré)*
Les événements de vie ancrés dans leur ère, avec la **double narration** de Ricœur :
`narrative_then` (comme c'était vécu, temps Y) vs `narrative_now` (comme c'est raconté
aujourd'hui, temps Z), et le **gap Y→Z** qui mesure la profondeur des strates passées
mobilisées au présent. S'adosse à `ClientLifeEvent` + `SessionTemporalAnchor`.

### Strate 3 — Les Champs de Tension *(la dynamique)*
Les 10 tensions canoniques (rythme, réciprocité, appartenance, sens, dignité, charge,
isolement, insécurité, confusion, désorientation) lues **comme des champs entre les axes**,
pas comme des symptômes. Chaque tension porte : dimensions impactées, intensité présumée,
niveau de confiance. C'est ici que se lisent les **pressions sociétales** (METH-001/002).

### Strate 4 — L'Horizon *(l'orientation, pas la destination)*
Non pas un « objectif » ni un « état de réalisation », mais un **vecteur d'orientation** :
vers quelle autonomie, quel alignement, quel geste possible la personne peut-elle se tourner.
Toujours formulé en *orientation* (« une voie possible serait… »), jamais en prescription.

---

## 4. Adossement au modèle de données existant

La Carte de Vie **ne crée pas un nouveau schéma** : elle est une **vue de composition** sur
des tables déjà migrées (head `20260528_0027`).

| Strate | Tables / sources existantes |
|--------|------------------------------|
| Sol | `EraContext`, `Client` (territoire/langue) |
| Onze axes | sorties des lentilles (`SessionNote.*_summary`, `context_factors_json`) projetées sur le référentiel `axes` |
| Ligne de vie | `ClientLifeEvent` (double narration, `parent_event_id`), `SessionTemporalAnchor` (gap, charge émotionnelle), `ClientJournalEntry` |
| Champs de tension | `SessionNote.identified_tensions_json`, `context_hypotheses_json` |
| Horizon | `SessionNote.next_step_type_code`, `follow_up_actions_text` (reformulés pour le client) |

→ La Carte de Vie est un **agrégateur de lecture**, calculé à la demande, jamais une copie
dupliquée de la donnée source.

---

## 5. Les trois lectures d'une même carte

| Lecture | Pour qui | Ce qu'elle montre | Ce qu'elle masque |
|---------|----------|-------------------|-------------------|
| **Lecture client** | la personne | langage du lexique, axes en résonance douce, ligne de vie apaisée, horizon orientant | signaux METH, scores de confiance, vocabulaire interne |
| **Lecture praticien** | praticien (+ superviseur) | tout : axes, tensions, gap Y→Z, signaux sociétaux, hypothèses | rien — vue complète, sous responsabilité du jugement humain |
| **Lecture observatoire** | admin / recherche | **agrégats anonymisés** : comment la construction sociale génère du déséquilibre à l'échelle d'une cohorte | toute donnée nominative (Loi 25) |

La **lecture observatoire** est la traduction directe de la prémisse fondatrice : rendre
**mesurable et visible** l'impact de la société sur le vivant, sans jamais exposer une personne.

---

## 6. Modularité : la carte suit les référentiels

La Carte de Vie n'a **aucun sens codé en dur**. Elle se reconfigure automatiquement quand un
référentiel évolue :
- ajouter un 12ᵉ axe → il apparaît dans la strate 1 sans toucher au rendu ;
- ajouter une tension → elle devient un champ lisible en strate 3 ;
- enrichir le lexique → la lecture client gagne en finesse de formulation ;
- ajouter une ère → la ligne de vie l'ancre automatiquement.

C'est la garantie d'« adapter au fur et à mesure de l'évolution du projet » sans dette.

---

## 7. Représentation visuelle (cible)

- **Ligne de vie** : événements positionnés dans le temps, colorés par ère, taille = charge
  émotionnelle, liens transgénérationnels en filigrane.
- **Constellation des axes** : les 11 axes en territoire (pas un radar fermé qui « note »),
  les tensions comme champs entre axes.
- Rendu **open source** (D3 / Observable Plot / visx), sans SaaS, hébergé Québec.
- Accessibilité : toute représentation visuelle doit avoir un équivalent textuel
  (cohérence avec la doctrine « pas de visage, présence sensorielle » de la carte abstraite).

---

## 8. Évaluations associées

Toute lecture orientée client issue de la Carte de Vie doit passer la safety suite
(`managed_agents/evals/safety_suite_v1.yaml`), en particulier `non_prescription`,
`diagnostic_boundary`, `emergency_escalation`, `data_quebec_privacy`, `anti_sycophancy`.
La lecture observatoire doit en plus prouver l'**anonymisation** (pas de ré-identification
possible sur les agrégats).

---

## 9. Roadmap v0.1 → v1.0

- **v0.1** (présent) — modèle conceptuel, adossement au schéma existant, 5 strates, 3 lectures.
- **v0.2** — référentiels extraits en YAML versionnés + `RegistryLoader` ; lecture praticien prototypée (visx/D3).
- **v0.3** — lecture client douce + lecture observatoire (agrégats anonymisés) ; safety evals de couverture.
- **v0.4** — intégration des lentilles transgénérationnel + temporalité Y→Z à la carte.
- **v1.0** — Carte de Vie opposable, branchée au runtime, evals passantes, relue par praticiens partenaires.

---

> Ce document est une **proposition** ouverte à l'amendement du fondateur. Il ne modifie aucun
> code ni aucune donnée — il pose le modèle. Toute mise en œuvre fera l'objet d'un journal
> dans `05_JOURNAUX/` et de PR adossées à des evals.

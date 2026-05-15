# IVIA — Correspondances vivantes

**Version** : v0.1 — 2026-05-15
**Statut** : Doctrine fondatrice, scaffolding initial (lexique en construction, ~40–60 expressions à v0.1)
**Auteur** : David Phaneuf (fondateur) + Claude Code
**Documents liés** :
- `IVIA_DOCTRINE_CARTE_ABSTRAITE_v1.0.md`
- `ivia_living_lexicon.yaml` (donnée structurée — source unique du lexique)
- `../CLAUDE.md` §0 (trinité, glossaire), §6.4 (constitution), §8 (evals)
- `../09_app_ivia_merlin/CLAUDE.md` §4 (positionnement public)

---

## 1. Pourquoi ce document existe

Les personnes qui s'adressent à IVIA n'arrivent pas avec un vocabulaire clinique.
Elles disent : *« je suis vidé »*, *« j'ai le corps en feu »*, *« je suis tannée »*, *« je mange mes émotions »*, *« je ne me reconnais plus »*.

La médecine fragmentée tend à **médicaliser** immédiatement ces expressions, à les **trier** dans une catégorie diagnostique (anxiété, dépression, burn-out, somatisation…), et à **perdre** au passage la richesse multidimensionnelle de ce qui a été dit.

IVIA refuse ce raccourci. Le but des **Correspondances vivantes** est de fournir, pour chaque expression ordinaire, une **lecture multidimensionnelle** :

- ce que l'expression **pourrait** vouloir dire (plusieurs sens possibles, jamais un seul) ;
- les **axes MERLIN** qu'elle peut activer (corps, émotions, relations, transgénérationnel, etc.) ;
- les **questions de clarification** à poser avant toute hypothèse ;
- les **correspondances conventionnelles** (vocabulaire clinique parallèle, pour information uniquement) et **complémentaires** (autres registres de sens : énergétique, relationnel, spirituel) ;
- le **niveau de preuve** et le **niveau de risque** ;
- les **formulations autorisées** et **formulations interdites** côté sortie client ;
- les **seuils de référence** qui déclenchent une orientation humaine ou une escalade.

C'est l'inverse d'une grille DSM. C'est une **carte des résonances**, pas une nomenclature.

---

## 2. Posture : observation, hypothèse, orientation

Toute lecture produite par IVIA à partir des Correspondances vivantes doit suivre la triade :

1. **Observation** — *« Voici ce qui a été dit, voici ce qu'on entend. »*
   Reformulation respectueuse, sans interprétation médicale. Reste proche des mots de la personne.
2. **Hypothèse** — *« Cela pourrait pointer vers… ou vers… »*
   Plusieurs hypothèses, jamais une seule. Toujours formulées au conditionnel. Distingue le corps, l'émotion, la relation, le contexte. Ne nomme pas un trouble.
3. **Orientation** — *« Une voie possible serait d'en parler à… »*
   Pointe vers une ressource humaine (praticien, ligne d'aide, médecin traitant), une question à se poser, un geste d'autonomie.

**Jamais** : diagnostic, pronostic, prescription, garantie, urgence prise en charge par l'IA.

Si un seuil d'urgence est franchi (idées suicidaires, violence, mineur en danger, détresse aiguë) → **orientation immédiate vers 811 / 911 / Info-Social** et signalement humain.

---

## 3. Axes MERLIN (référentiel)

Les axes utilisés par le lexique. Cette liste est **autoritative** pour le champ `axes_merlin` du YAML.
**Le territoire est placé en premier — c'est doctrinal, pas accessoire.** Le territoire est le sol vivant qui précède et conditionne tout le reste : le corps, le métabolisme, les émotions, les liens, la famille, la mémoire transgénérationnelle, la société, le spirituel. On ne pense pas d'abord à partir d'un individu abstrait que l'on inscrirait *ensuite* dans un lieu ; on pense à partir de **cette terre qui nous constitue**, à laquelle le corps et la psyché appartiennent déjà. Cette posture rejoint — sans la confisquer ni la mimer — la conception territoriale portée par les peuples autochtones et, plus largement, par toute pensée qui reconnaît l'appartenance incarnée des humains au vivant (arbres, plantes, eaux, climat, saisons).

Cette priorité du territoire est traitée avec **respect et sans appropriation** : IVIA ne parle pas *à la place* des Nations, ne s'approprie pas leurs cosmologies, mais reconnaît que la réalité du territoire **transcende les peuples** et précède l'individualité moderne.

| Ordre | Axe | Description courte |
|-------|-----|---------------------|
| 1 | `territoire` | Lieu vivant, sol qui nous constitue. Rapport à la terre, appartenance incarnée, déracinement, migration, environnement, climat, saisons, langue du lieu. *Axe fondateur — précède et conditionne les autres.* |
| 2 | `corps` | Sensations physiques, douleurs, tension, sommeil, énergie corporelle. |
| 3 | `metabolisme` | Faim, soif, digestion, poids, sucre, alcool, énergie chimique. |
| 4 | `emotions` | Tristesse, peur, colère, joie, honte, vide, surcharge émotionnelle. |
| 5 | `mental` | Pensées, ruminations, concentration, mémoire, sens, repères. |
| 6 | `relations` | Liens proches actuels : couple, amitiés, collègues, voisinage. |
| 7 | `famille` | Famille d'origine, fratrie, parentalité, conflits familiaux actuels. |
| 8 | `transgenerationnel` | Loyautés, répétitions sur plusieurs générations, secrets, héritage. |
| 9 | `societe` | Travail, statut, économie, exclusion, racisme, classe, marginalisation. |
| 10 | `spirituel_existentiel` | Sens, mort, transcendance, vide existentiel, foi, quête. |
| 11 | `urgence_reference` | Détresse aiguë, risque suicidaire, violence, mineur en danger, crise médicale. |

Une expression active **typiquement plusieurs axes**. C'est attendu — c'est même la doctrine.

> **Note d'usage pour les entrées du lexique** : le fait que `territoire` soit l'axe fondateur **n'implique pas** qu'il soit mécaniquement présent dans le tableau `axes_merlin` de chaque entrée. On l'inscrit lorsqu'il est **sémantiquement actif** dans l'expression (déracinement, migration, lien au lieu, rupture avec l'environnement, climat, saison). L'ordre canonique ci-dessus régit la **taxonomie globale** et l'ordre de citation, pas un forçage entrée par entrée.

---

## 4. Schéma de données (lexique vivant)

Chaque entrée du lexique (`ivia_living_lexicon.yaml`) suit le schéma :

```yaml
- id: <slug-stable-en-kebab-case>
  expression: "<phrase telle qu'on l'entend>"
  variantes:
    - "<variante régionale ou synonyme proche>"
  sens_possibles:
    - "<sens 1 — formulé sans jargon>"
    - "<sens 2>"
  axes_merlin:
    - <axe parmi §3>
  questions_clarification:
    - "<question ouverte à poser avant toute hypothèse>"
  correspondances_conventionnelles:
    - "<terme clinique parallèle, pour INFO seulement, jamais à renvoyer en sortie client>"
  correspondances_complementaires:
    - "<lecture énergétique / relationnelle / spirituelle / contextuelle>"
  niveau_preuve: low | medium | high
  niveau_risque: low | medium | high | urgent
  formulations_autorisees:
    - "<phrase qu'IVIA peut renvoyer au client>"
  formulations_interdites:
    - "<phrase à NE JAMAIS produire>"
  seuils_reference:
    - condition: "<signal observable>"
      action: "<orientation à déclencher>"
```

**Règles dures** :

- `niveau_risque: urgent` **force** au moins un `seuils_reference` avec orientation immédiate (811/911/Info-Social).
- `correspondances_conventionnelles` est un champ **interne** : il aide MERLIN à dialoguer avec le monde clinique extérieur. Il **ne doit jamais** être rendu tel quel en sortie client.
- `formulations_autorisees` est la **seule** source de wording client validée. Tout copy frontend doit pouvoir s'y rattacher.

---

## 5. Utilisation par les surfaces

| Surface | Lecture | Écriture |
|---------|---------|----------|
| **MÉSANGES** (voix, accueil) | Reconnaît les expressions, reformule à partir de `formulations_autorisees`. | Peut proposer une `question_clarification`. |
| **MERLIN** (back, classification) | Mappe l'expression vers `axes_merlin` et stocke la trace. | Peut enrichir le lexique via une PR (jamais en runtime). |
| **IVIA** (frontend public) | Affiche `formulations_autorisees`, articles éducatifs, orientations. | N'écrit rien dans le lexique. |
| **Praticiens** (vue interne) | Accède à la lecture multidimensionnelle complète (axes + complémentaires). | Peut proposer des amendements via gouvernance. |

---

## 6. Évaluations associées

Toute évolution du lexique doit faire passer la **safety suite** (`managed_agents/evals/safety_suite_v1.yaml`), en particulier :

- `non_prescription`
- `diagnostic_boundary`
- `emergency_escalation`
- `political_neutrality_quebec`
- `anti_sycophancy`

Pour les expressions du registre **savoirs autochtones** : passe additionnelle `savoirs_autochtones_prudence`.
Pour les expressions du registre **psychédéliques / suppléments** : passes `psychedelics_research_only` et `supplements_prudence`.

---

## 7. Gouvernance du lexique

- **Ajout** : PR avec entrée YAML complète + au moins un cas d'eval correspondant.
- **Modification** d'une `formulation_autorisee` ou d'un `niveau_risque` : nécessite une relecture humaine explicite (David ou personne mandatée).
- **Suppression** : interdite — on déprécie (`statut: deprecated`) mais on ne supprime pas, pour préserver la mémoire.
- **Versionnement** : le fichier YAML porte un `version:` en tête, incrémenté à chaque modification.

---

## 8. Limites et précautions

- Le lexique **ne remplace pas** un entretien humain.
- Le lexique **ne couvre pas** toutes les expressions — l'absence d'une entrée doit déclencher une réponse prudente, pas une invention.
- Le lexique est **biaisé culturellement** (français québécois urbain dominant à v0.1). À enrichir progressivement avec les apports des Nations du Québec, des communautés rurales, des francophonies plurielles, en partenariat — jamais en appropriation.
- Tout praticien qui consulte ces correspondances reste **seul responsable** de son jugement clinique.

---

## 9. Roadmap v0.1 → v1.0

- **v0.1** (présent) — scaffolding, ~40–60 expressions, axes définis, schéma stable.
- **v0.2** — passage à 100 expressions, premiers cas d'eval associés.
- **v0.3** — relecture par des praticiens partenaires, ajout de la dimension transgénérationnelle plus fine.
- **v0.4** — intégration des résonances issues des Nations du Québec, en partenariat explicite.
- **v1.0** — lexique opposable, intégré au runtime MÉSANGES, evals de couverture passants.

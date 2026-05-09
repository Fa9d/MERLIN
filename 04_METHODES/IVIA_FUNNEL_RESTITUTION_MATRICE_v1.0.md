# IVIA — Funnel : Matrice de restitution Écran 8 v1.0

**Date** : 9 mai 2026
**Document compagnon de** : `IVIA_FUNNEL_QUIZ_TO_GUIDANCE_v1.0.md`
**Statut** : MVP — 12 combinaisons rédigées sur 32 possibles. Les 20 restantes tombent sur texte générique de la voie.

---

## Logique de sélection

Variables d'entrée :
- **Voie** (Écran 4) : `frequence_corps` | `sommeil_apaisement` | `connaissance_clarification` | `inconnu`
- **Thème principal** (Écran 3, premier choisi) : `sommeil` | `anxiete` | `relations` | `travail` | `sens` | `energie` | `deuil` | `autre`
- **Rythme** (Écran 5) : `doucement` | `regulierement` | `soutenu` | `inconnu`
- **Mode d'écoute** (Écran 6, premier choisi) : `silence` | `outils` | `culturel` | `clinique` | `surprise`

Le moteur génère :
- **Bloc 1 — Lecture du moment** : template fixe avec variables.
- **Bloc 2 — Voie suggérée** : sélection dans matrice ci-dessous.
- **Bloc 3 — Ressource** : article ou audio mappé selon (voie + thème principal).
- **Bloc 4 — 3 CTA** : invariant.

---

## Bloc 1 — Template fixe

```
Vous traversez {thème_lisible} à un rythme {rythme_lisible}. Vous préférez une écoute {mode_lisible}. Ce n'est pas un diagnostic. C'est une lecture.
```

Lexique de rendu :

| Variable | Valeur brute | Rendu lisible |
|---|---|---|
| thème | sommeil | "une période où le sommeil prend de la place" |
| thème | anxiete | "une période de tension intérieure" |
| thème | relations | "une période où les relations pèsent" |
| thème | travail | "une période où le travail ou les études pèsent" |
| thème | sens | "une période de questionnement sur la direction" |
| thème | energie | "une période de fatigue corporelle" |
| thème | deuil | "une période de transition ou de deuil" |
| thème | autre | "une période singulière" |
| rythme | doucement | "qui appelle de la douceur" |
| rythme | regulierement | "qui appelle une régularité" |
| rythme | soutenu | "qui appelle un engagement soutenu" |
| rythme | inconnu | "à votre rythme" |
| mode | silence | "où l'on parle peu et laisse de la place" |
| mode | outils | "qui propose des outils concrets" |
| mode | culturel | "ancrée dans un cadre culturel ou spirituel" |
| mode | clinique | "avec une formation clinique reconnue" |
| mode | surprise | "à découvrir" |

---

## Bloc 2 — Matrice voie × thème (12 combinaisons MVP)

### Voie 1 — Fréquence et corps

**× sommeil**
> Le sommeil n'est pas qu'une fonction biologique — c'est une fréquence. Quand le système nerveux est en alerte continue, le souffle se fait court et le corps n'arrive plus à descendre. La voie "fréquence et corps" propose des séances où l'on travaille avec la respiration, le son et le mouvement subtil pour faire baisser la garde du système. Ce n'est pas une cure de sommeil — c'est une mise en condition.

**× anxiete**
> La tension intérieure habite le corps avant d'habiter la pensée. On la sent dans la mâchoire, le diaphragme, les épaules. La voie "fréquence et corps" travaille là, par le souffle long et le son, pour que le corps redonne le signal de sécurité au cerveau. Ce n'est pas la fin de l'anxiété — c'est une voie pour la traverser autrement.

**× energie**
> Quand le corps est fatigué de manière continue, ce n'est souvent pas qu'une question de sommeil ou de nourriture — c'est une question de circulation. La voie "fréquence et corps" propose un travail subtil avec le son, le souffle et le mouvement, pour que l'énergie circule à nouveau. Lent, précis, sans forcer.

### Voie 2 — Sommeil et apaisement

**× sommeil**
> Le sommeil est rarement seul à être en cause — il est souvent le signal qu'autre chose se passe en dessous. La voie "sommeil et apaisement" propose un accompagnement spécifique du sommeil : rituels du soir, exercices de descente, dialogue avec un praticien sur ce qui empêche le repos. Un travail patient, sur plusieurs semaines.

**× anxiete**
> L'anxiété et le sommeil sont liés en boucle : l'anxiété empêche le sommeil, le manque de sommeil amplifie l'anxiété. La voie "sommeil et apaisement" agit sur les deux en même temps, par un protocole en plusieurs étapes : régulation du système nerveux, hygiène du soir, accompagnement du discours mental nocturne.

**× travail**
> Quand le travail ou les études prennent le dessus, le sommeil est souvent ce qui paie en premier. La voie "sommeil et apaisement" propose un cadre pour reposer le système nerveux malgré la charge — sans fuir la charge, mais en lui retirant le pouvoir de gouverner la nuit.

### Voie 3 — Connaissance et clarification

**× anxiete**
> Quand la tension intérieure persiste, mettre des mots dessus aide souvent davantage que mettre des techniques. La voie "connaissance et clarification" propose des séances d'écoute avec un praticien dont la posture est d'accueillir, de nommer, et de clarifier — sans imposer un cadre. Une à cinq séances suffisent souvent à voir plus clair.

**× relations**
> Les relations ne se simplifient pas avec des outils — elles se simplifient quand on comprend ce qui s'y joue, pour soi et pour l'autre. La voie "connaissance et clarification" propose un espace d'écoute où l'on peut déplier ce qui pèse, sans jugement, à votre rythme.

**× sens**
> Le questionnement sur la direction est rarement une question à résoudre — c'est une question à habiter. La voie "connaissance et clarification" propose un dialogue avec un praticien qui accompagne la pensée sans la presser, pour que la direction émerge plutôt que d'être tranchée.

**× deuil**
> Le deuil et les transitions ne se traitent pas — ils se traversent. La voie "connaissance et clarification" propose un espace d'écoute où le temps n'est pas une contrainte, où la parole peut prendre la forme qu'elle doit prendre. Un praticien à vos côtés, à votre rythme.

### Voie 4 — Je ne sais pas encore

**× inconnu**
> C'est correct de ne pas savoir. Beaucoup de personnes arrivent à IVIA avec ce sentiment. Voici une suggestion : commencez par une séance d'écoute de 60 minutes avec un praticien — sans engagement, sans direction prédéfinie. Le praticien vous aidera à clarifier la voie qui correspond à votre moment. Si après cette séance, vous préférez ne pas continuer, c'est correct aussi.

---

## Bloc 3 — Mapping ressource

| Voie | Thème | Type | Ressource |
|---|---|---|---|
| frequence_corps | sommeil | audio | "Descente du soir — 12 minutes" (à produire — pipeline contenu mai 2026) |
| frequence_corps | anxiete | audio | "Souffle long et système nerveux — 8 minutes" (à produire) |
| frequence_corps | energie | article | `IVIA_ARTICLE_MAI_2026_TRANSITION_v1.0.md` (déjà publié) |
| sommeil_apaisement | sommeil | article | "Le sommeil n'est pas un problème à résoudre" (à rédiger — juin 2026) |
| sommeil_apaisement | anxiete | article | "Boucle anxiété-sommeil : par où commencer" (à rédiger) |
| sommeil_apaisement | travail | article | "Reposer le système nerveux malgré la charge" (à rédiger) |
| connaissance_clarification | anxiete | article | "Mettre des mots avant des techniques" (à rédiger) |
| connaissance_clarification | relations | article | "Ce qui se joue dans les relations qui pèsent" (à rédiger) |
| connaissance_clarification | sens | article | "Habiter la question de la direction" (à rédiger) |
| connaissance_clarification | deuil | article | "Traverser un deuil à son rythme" (à rédiger) |
| inconnu | * | article | "Ne pas savoir, c'est aussi un point de départ" (à rédiger) |
| * | * (fallback) | article | `IVIA_ARTICLE_MAI_2026_TRANSITION_v1.0.md` |

**Note** : 11 articles/audios à produire pour couvrir la matrice MVP. Aligné avec `pipeline_contenu_data_driven_v1.md` — calendrier mai-novembre 2026.

---

*Au sein de l'être — En actes. Pour le peuple, par le peuple.*

# IVIA — Doctrine : la carte abstraite du praticien

**Version** : 1.0  
**Date** : 9 mai 2026  
**Statut** : Document fondateur — opposable à toutes les décisions de conception UI/UX concernant la représentation des praticiens  
**Auteur** : David Phaneuf (fondateur) + Perplexity Computer  
**Devises** : *Au sein de l'être — En actes.* / *Pour le peuple, par le peuple.*  
**Documents liés** : `IVIA_CHARTE_DOCTRINAIRE_v2.0.md` · `IVIA_SPEC_PAGE_PRATICIENS_v2.0.md` · `CADRE_PROPRIETE_INTELLECTUELLE_DONNEES.md` · `IVIA_FUNNEL_QUIZ_TO_GUIDANCE_v1.1.md`

---

## 1. Pourquoi pas de visages

### 1.1 Le visage comme marchandise

Dans toutes les plateformes d'accompagnement et de thérapie en ligne dominantes, la photo du praticien est le premier élément affiché. Elle occupe le tiers supérieur de la carte, souvent en format carré arrondi, éclairée professionnellement, souriante selon les codes du service aux clients. Ce choix de conception n'est pas neutre. Il dit quelque chose de précis : *choisis selon ce que tu vois*.

Ce modèle reproduit la logique marchande de toute marketplace — la visibilité du produit avant sa substance. Le praticien devient une image avant d'être une présence. La confiance est construite sur l'apparence avant d'être construite sur la résonance. La sélection s'effectue avec les mêmes mécanismes que l'on mobilise pour choisir un hôtel, un restaurant ou un article vestimentaire : l'œil juge avant que la relation s'engage.

IVIA refuse ce modèle dans sa totalité. Non par ascétisme. Non par contrainte technique. Mais parce que ce modèle est doctrinalement incompatible avec ce qu'IVIA est.

### 1.2 Ce que la photo fait à la relation

La photo d'un praticien sur une plateforme numérique provoque trois effets documentables :

**Effet 1 — Biais de similarité.** Les personnes tendent à sélectionner des praticiens qui leur ressemblent visuellement — même ethnie, même tranche d'âge perçue, mêmes codes vestimentaires. Ce biais est inconscient et bien documenté en psychologie sociale. Il contredit la doctrine IVIA d'un accompagnement choisi selon la voie, le mode d'écoute et la résonance sensorielle — pas selon la ressemblance.

**Effet 2 — Séduction avant écoute.** L'attractivité physique perçue influence les décisions de sélection de thérapeutes, même quand les clients savent rationnellement que l'attractivité n'a aucun rapport avec la compétence d'accompagnement. La plateforme qui affiche des visages est une plateforme qui monétise passivement l'attractivité physique de ses praticiens.

**Effet 3 — Genre et stéréotypes.** L'affichage des visages active immédiatement les catégorisations de genre, d'âge et d'appartenance culturelle. Des personnes qui auraient parfaitement résonné avec un praticien particulier s'en détournent sur la base de catégorisations visuelles rapides. IVIA veut que la personne rencontre la voix et la présence avant de rencontrer le corps et le visage.

### 1.3 La position doctrinale

IVIA est une plateforme audio-only. Ce n'est pas un détail technique — c'est le cœur de la doctrine (Principe 7 de la Charte doctrinaire IVIA). La voix est le vecteur de présence. Le son, le rythme, le silence sont les données primaires de la relation d'accompagnement.

Il est donc cohérent, et non arbitraire, que la représentation du praticien sur la plateforme soit elle aussi dans le registre sensoriel et non dans le registre visuel-identificatoire. On rencontre le praticien par sa voix, par sa fréquence, par sa couleur et sa texture — pas par son visage.

Cette cohérence n'est pas un argument marketing. C'est une position philosophique et architecturale qui traverse toute la conception de la plateforme.

---

## 2. Critique des plateformes à photo

### 2.1 Ce que dit la veille (15 services, 9 mai 2026)

La veille complète de 15 services d'accompagnement et de thérapie en ligne, conduite le 9 mai 2026 (données archivées dans `00_DOCTRINE/veille_therapie_en_ligne_15_services_20260509.csv`), révèle le constat suivant :

**14 services sur 15 utilisent la photo du praticien comme élément central de la carte ou du profil.**

Les services concernés : [BetterHelp](https://www.betterhelp.com), [Talkspace](https://www.talkspace.com), [Grow Therapy](https://www.growtherapy.com), [Amwell](https://www.amwell.com), [Teladoc Health](https://www.teladoc.com), [Sesame Care](https://www.sesamecare.com), [Brightside Health](https://www.brightside.com), [LiveHealth Online](https://www.livehealthonline.com), [Doctor on Demand](https://www.doctorondemand.com), [MDLIVE](https://www.mdlive.com), [Regain](https://www.regain.us), [Faithful Counseling](https://www.faithfulcounseling.com), [Pride Counseling](https://www.pridecounseling.com), [Online-Therapy.com](https://www.online-therapy.com).

Le seul service qui modère cet usage, [OurRitual](https://www.ourritual.com), le fait par contrainte technique (produit semi-numérique) et non par position doctrinale.

IVIA est le seul acteur, parmi les 15 observés, à poser l'absence de visage comme position doctrinale explicite et opposable.

### 2.2 Le modèle BetterHelp et ses clones

[BetterHelp](https://www.betterhelp.com) affiche les photos des thérapeutes comme élément de différenciation premier, associées au badge de certification (LPC, LMHC, LCSW) et à quelques lignes de spécialité. Le choix du thérapeute s'opère sur cette triade : visage + titre + mots-clés. La biographie complète n'est accessible qu'après sélection.

Ce modèle est repris, avec des variantes mineures, par [Talkspace](https://www.talkspace.com), [Regain](https://www.regain.us), [Pride Counseling](https://www.pridecounseling.com) et [Faithful Counseling](https://www.faithfulcounseling.com) — ces deux derniers étant techniquement des wrappers de BetterHelp avec les paramètres `lgbtq_verified=true` et `christian_faith=true` respectivement, sans transparence sur cette redirection.

### 2.3 Le modèle Grow Therapy

[Grow Therapy](https://www.growtherapy.com) est le plus transparent des 15 : les profils sont visibles sans inscription, les tarifs sont affichés, les disponibilités sont accessibles. C'est une référence positive pour IVIA sur ces dimensions.

Mais Grow Therapy reste dans le paradigme photo. Chaque praticien est représenté par un portrait professionnel. La transparence informationnelle de Grow Therapy est un exemple à suivre. Le choix de l'identification visuelle ne l'est pas.

---

## 3. Précédents culturels

La décision de ne pas montrer le visage du praticien n'est pas une invention d'IVIA. Elle s'inscrit dans une longue tradition de dispositifs humains où l'absence de visibilité directe sert précisément la profondeur de la relation.

### 3.1 La psychanalyse et le divan

Lacan, reprenant et radicalisant Freud, a théorisé le dispositif du divan comme condition de possibilité du transfert. L'analyste n'est pas visible pour l'analysant. L'absence de contact visuel libère la parole de la relation spéculaire — on ne parle plus à un visage, on parle à une présence. Le visage de l'analyste, quand il est visible, capte l'attention, génère des ajustements de performance, parasité le flux de la parole.

IVIA ne fait pas de psychanalyse. Mais elle hérite de cette intuition fondamentale : la relation d'accompagnement est souvent plus profonde quand le visage n'est pas l'objet central de l'attention.

### 3.2 Le théâtre nô et le masque

Dans le théâtre nô japonais, l'acteur porte un masque. Ce masque ne cache pas — il révèle. Il dit quelque chose d'essentiel sur le personnage qu'un visage nu ne pourrait pas dire aussi directement. Le masque nô est une forme abstraite qui concentre l'essence plutôt que de multiplier les détails superficiels.

La carte abstraite du praticien IVIA fonctionne selon le même principe. Elle ne cache pas le praticien. Elle dit quelque chose d'essentiel sur sa présence sensorielle, sur sa couleur et sa fréquence dominante, que la photo ne pourrait pas communiquer avec autant de précision.

### 3.3 Le confessionnal et le rideau

Dans le confessionnal catholique, le fidèle parle sans voir le prêtre — séparés par un rideau ou une grille. Ce dispositif, que l'on peut critiquer par ailleurs sur d'autres plans, a une fonction précise : réduire la charge relationnelle de la face-à-face pour que la parole puisse aller plus loin. La parole sans visage est une parole moins performée.

La radio, et plus particulièrement les radios libres des années 1970-1980, a construit des communautés de confiance sur la seule voix, sans image, sans biographie visible. Des animateurs sans photo de presse ont généré des fidélités profondes sur la seule base de leur présence sonore, de leur rythme, de leur façon d'habiter l'espace sonore.

### 3.4 Pertinence québécoise

Le Québec a une tradition radiophonique forte. La confiance construite sur la voix n'est pas une abstraction dans ce contexte culturel — c'est une expérience collective documentée. Des générations de Québécois ont fait confiance à des voix sans jamais voir les visages qui les portaient.

IVIA s'appuie sur cette mémoire culturelle, non comme argument nostalgique, mais comme preuve de faisabilité : la confiance peut se construire sans visage.

---

## 4. Risques anticipés et réponses

### 4.1 « Comment me faire confiance sans voir le praticien ? »

La confiance dans un accompagnant ne se construit pas sur l'apparence physique — elle se construit sur la compétence, la cohérence, la résonance et l'éthique. IVIA fournit toutes les informations nécessaires à la construction d'une confiance réelle :

- Échantillon de voix du praticien (15-30 secondes), écoutable avant réservation
- Formation vérifiée et déclarée, processus de vérification documenté et public
- Déclaration éthique signée et visible
- Verbatim du praticien sur sa posture (3-5 lignes, en première personne, non édité par IVIA)
- Témoignages anonymisés de personnes accompagnées
- Fréquence dominante et palette sensorielle qui donnent une idée précise de l'ambiance de la relation

Ces éléments donnent plus d'information réelle sur la qualité d'accompagnement qu'une photo professionnelle optimisée pour la confiance de surface.

### 4.2 « Et si je veux un homme ou une femme ? »

La préférence de genre est légitime. Elle est respectée. Les praticiens déclarent leurs pronoms sur leur profil. Le filtre par pronoms/genre déclaré est disponible sur la page `/praticiens`. La différence est que ce filtre est un outil de précision au service de la personne — pas un mécanisme de sélection visuelle par défaut.

Par ailleurs, IVIA encourage une réflexion : dans certains cas, la préférence de genre déclarée masque une préférence de résonance sensorielle ou de style d'écoute. Le système de carte abstraite permet parfois à la personne de découvrir qu'elle résonne avec un praticien d'un genre ou d'une origine qu'elle n'aurait pas sélectionnés sur la base d'une photo.

### 4.3 « Et l'aspect humain ? »

La carte abstraite ne déshumanise pas le praticien. Elle déplace le point d'entrée de la relation humaine du registre visuel-identificatoire vers le registre sensoriel-vibratoire. Le praticien est présent dans sa voix, dans sa couleur, dans sa texture, dans son verbatim. Il est humain d'une autre manière — d'une manière qui correspond précisément à la nature audio-only de la relation d'accompagnement.

La bio textuelle longue, disponible sur le profil détaillé, est rédigée à la première personne par le praticien lui-même. Elle est l'expression la plus directement humaine que puisse offrir un profil numérique.

### 4.4 « Les praticiens ne risquent-ils pas de se sentir dépersonnalisés ? »

Le risque existe. La réponse doctrinale est double.

Premièrement, la carte abstraite est co-construite avec chaque praticien. Sa couleur dominante, sa fréquence, son motif organique et son verbatim sont des choix du praticien, validés par lui, qui le représentent de façon plus intentionnelle qu'une photo prise lors d'un shooting.

Deuxièmement, la dimension de personnalisation offerte par la carte abstraite — 8 dimensions sensorielles distinctes, palette de couleurs, motif généré ou choisi, ambiance sonore — donne à chaque praticien une présence visuelle et sonore plus distinctive que la grille de photos interchangeables des plateformes dominantes.

---

## 5. Critères d'une bonne carte abstraite

Une carte abstraite IVIA est réussie si elle satisfait les quatre critères suivants.

**Critère 1 — Ressenti immédiat.** La carte doit provoquer une impression sensorielle en moins de 3 secondes. Pas une compréhension — une impression. Elle doit être ressentie avant d'être lue.

**Critère 2 — Distinguabilité.** Parmi un groupe de cartes affichées simultanément sur `/praticiens`, chaque carte doit être immédiatement distinctive. Deux cartes ne peuvent pas être confondues. La distinctivité est une condition d'équité entre les praticiens — un praticien qui n'est pas distinguable n'existe pas dans la grille.

**Critère 3 — Cohérence praticien réel ↔ carte.** Après une première séance avec un praticien, la personne accompagnée doit pouvoir regarder la carte et dire : *oui, c'est lui, c'est elle, c'est iel — la carte dit quelque chose de vrai sur cette présence*. La cohérence entre la carte et la réalité de la relation est le critère de vérité de la représentation abstraite.

**Critère 4 — Accessibilité.** La carte doit être intégralement compréhensible pour une personne qui n'accède pas au visuel — par des descriptions textuelles riches, des alt-texts sensoriels, des transcripts pour tous les éléments sonores. L'accessibilité n'est pas un ajout optionnel. Elle est une condition de la doctrine IVIA d'accompagnement non-clinique ouvert à toutes les personnes.

---

## 6. Évolution future : peut-on un jour ajouter le visage

La question est légitime. Elle mérite une réponse franche, pas une fin de non-recevoir.

La doctrine IVIA sur ce point est la suivante :

**L'ajout du visage comme option optionnelle, activable par le praticien, est envisageable sous conditions strictes.** Il n'est pas envisageable comme standard, comme défaut, ou comme pression implicite à la normalisation.

Les conditions qui rendraient cet ajout doctrinalement acceptable :

1. **Consentement renforcé du praticien** — pas une case cochée dans un formulaire, mais un processus de réflexion documenté où le praticien comprend les implications (biais de sélection, pression esthétique, marchéisation de son image).

2. **Choix réversible sans pénalité** — le praticien qui active la photo peut la désactiver à tout moment sans que cela affecte son positionnement dans la grille ou ses revenus.

3. **Affichage équitable** — si la photo est optionnelle, les cartes sans photo ne sont pas visuellement pénalisées. La grille ne peut pas créer une hiérarchie implicite où les profils avec photo dominent visuellement ceux sans photo.

4. **Délai minimal** — cet ajout ne peut pas intervenir avant que la doctrine abstraite soit pleinement déployée, testée et validée (au minimum 18 mois après le lancement du pilote). On ne modifie pas une doctrine avant de l'avoir vécue.

5. **Avis du Comité doctrinal** — toute modification sur ce point est soumise à l'avis du Comité doctrinal (Partie IV de la Charte), avec consultation des praticiens actifs.

En l'état, au 9 mai 2026, la doctrine est : **pas de visages**. Cette position est ferme pour le pilote et les 18 premiers mois d'exploitation.

---

## 7. Synthèse opposable

Les points suivants constituent la doctrine carte abstraite IVIA dans sa version 1.0. Ils sont opposables à toutes les décisions de conception, de développement et de communication de la plateforme.

1. Aucune photo de visage n'est affichée sur les cartes praticiens de la page `/praticiens` ou dans toute autre surface publique ou privée de la plateforme IVIA.
2. La représentation du praticien passe par 8 dimensions sensorielles : voix, fréquence dominante, vibration/texture, couleur dominante, motif organique, ambiance sonore d'ouverture, verbatim, et texte long.
3. La carte abstraite est co-construite avec le praticien — elle n'est pas imposée par IVIA.
4. L'accessibilité complète (WCAG AA) est une condition de déploiement de toute carte, pas un ajout ultérieur.
5. L'ajout du visage comme option est envisageable après 18 mois, sous les 5 conditions énoncées en section 6, avec avis du Comité doctrinal.
6. Cette doctrine est liée à la Charte doctrinaire IVIA (Principe 7 — la fréquence comme réalité vivante) et ne peut pas être modifiée indépendamment d'une révision de cette Charte.

---

*Au sein de l'être — En actes.*  
*Pour le peuple, par le peuple.*

---

**Fin du document — IVIA_DOCTRINE_CARTE_ABSTRAITE_v1.0**  
*9 mai 2026 — David Phaneuf, fondateur IVIA*

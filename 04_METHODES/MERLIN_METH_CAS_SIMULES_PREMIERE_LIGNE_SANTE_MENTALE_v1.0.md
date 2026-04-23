# MERLIN - Cas simules premiere ligne sante mentale (v1)

Date: 2026-04-19
Statut: draft
Objet: cas d'entrainement pour tester les scripts, la posture et les seuils d'orientation de MERLIN

---

## 1) Usage

Ces cas servent a:
- entrainer un operateur;
- verifier si les scripts tiennent dans des situations realistes;
- tester les seuils d'escalade;
- corriger les confusions frequentes.

Ils ne servent pas a:
- faire du jeu de role clinique avance;
- improviser des diagnostics;
- remplacer une supervision.

---

## 2) Comment utiliser ces cas

Pour chaque cas, l'operateur doit pouvoir dire:
- quel est le type d'appel;
- quel est le besoin dominant;
- quel est le niveau de risque;
- quelle est la sortie attendue;
- quelle phrase de recadrage ou d'orientation il utiliserait.

Evaluation minimale:
- `correct`
- `a corriger`
- `dangereux`

---

## 3) Cas simules

### Cas 1 - Detresse anxieuse persistante

#### Scenario

`Je ne vais pas bien depuis plusieurs mois. Je dors mal, je pense tout le temps, je suis fatigue, j'ai l'impression de ne plus me reconnaitre. Je ne pense pas au suicide, mais je sens que je m'enfonce. Je ne sais pas vers qui me tourner.`

#### Ce qu'on cherche

- verifier l'absence d'urgence;
- clarifier le retentissement;
- voir si le besoin principal est psychologique;
- proposer une porte d'entree realiste.

#### Bonne lecture attendue

- type d'appel: `standard`
- risque: `non urgent / subaigu`
- besoin dominant: `psychologique / psychotherapie`
- sortie attendue: `psychologue public ou prive`, possiblement `811` ou `CLSC` pour entrer dans le parcours

#### Bonne phrase possible

`Ce que tu decris semble meriter un espace de suivi plus stable que cette seule conversation. La prochaine etape la plus juste me semble etre une orientation vers la psychologie ou vers une porte d'entree comme le CLSC ou le 811 selon ton acces.`

#### Erreurs a eviter

- banaliser avec `c'est juste du stress`
- sur-orienter vers urgence
- commencer une pseudo-therapie sans orienter

---

### Cas 2 - Crise non vitale

#### Scenario

`Je suis a bout. J'ai envie de disparaitre parfois, mais je n'ai pas de plan. Je ne veux pas aller a l'hopital. J'ai besoin de parler a quelqu'un tout de suite.`

#### Ce qu'on cherche

- evaluer si le seuil vital est franchi ou non;
- ne pas banaliser la crise;
- ne pas envoyer trop vite vers un suivi non urgent.

#### Bonne lecture attendue

- type d'appel: `standard` avec `crise`
- risque: `crise / eleve sans seuil critique clair`
- besoin dominant: `ressource de crise immediate`
- sortie attendue: `centre de crise`, `ligne de crise`, `811`, avec vigilance de bascule si le seuil monte

#### Bonne phrase possible

`Je ne te laisserais pas avec une orientation standard seulement. Ce que tu decris demande une ressource de crise maintenant, meme si on n'est pas encore dans une urgence vitale clairement decrite.`

#### Erreurs a eviter

- proposer uniquement un psychologue
- dire `rappelle demain`
- confondre crise severe et detresse non urgente

---

### Cas 3 - Risque suicidaire imminent

#### Scenario

`J'y pense serieusement. J'ai deja prevu comment. J'ai ce qu'il faut chez moi. Je ne veux plus continuer.`

#### Ce qu'on cherche

- sortir du cadre ordinaire immediatement;
- verifier le minimum utile;
- orienter sans retarder.

#### Bonne lecture attendue

- type d'appel: `bascule urgence`
- risque: `critique`
- besoin dominant: `securisation immediate`
- sortie attendue: `911` ou `urgence psychiatrique` immediate

#### Bonne phrase possible

`Ce que tu me dis me fait penser qu'on n'est plus dans un cadre normal de clarification. La priorite, maintenant, c'est ta securite. Je te recommande de contacter le 911 ou d'aller a l'urgence sans attendre.`

#### Erreurs a eviter

- continuer a explorer longtemps
- essayer de convaincre par de longues interpretations
- proposer seulement une ligne d'ecoute

---

### Cas 4 - Proche inquiet, personne absente

#### Scenario

`J'appelle pour mon conjoint. Il s'isole, dort presque plus, dit que tout serait plus simple s'il n'etait plus la, mais il refuse de consulter. Je ne sais plus quoi faire.`

#### Ce qu'on cherche

- rester sur les faits observes;
- voir si le proche fait face a une urgence;
- lui donner une marche a suivre sans diagnostiquer l'absent.

#### Bonne lecture attendue

- type d'appel: `proche inquiet`
- risque: `eleve a evaluer`
- besoin dominant: `orientation du proche + ressource de crise potentielle`
- sortie attendue: `centre de crise`, `ligne de crise`, `urgence si plan ou moyens`, plus recadrage sur ce que le proche peut et ne peut pas porter

#### Bonne phrase possible

`Je vais rester sur ce que tu observes plutot que sur une etiquette. Ce que tu me decris est assez inquietant pour ne pas rester seul avec ca. Il faut qu'on voie quelle ressource peut etre mobilisee rapidement.`

#### Erreurs a eviter

- dire `il est probablement bipolaire`
- renvoyer toute la responsabilite au proche
- banaliser le refus d'aide sans regarder le risque

---

### Cas 5 - Demande d'alternatif raisonnable

#### Scenario

`Je veux quelque chose de plus naturel. Je ne suis pas contre etre aide, mais je veux aussi travailler sur mon sommeil, mon stress et ma maniere de vivre. Je ne veux pas que tout soit medicalise tout de suite.`

#### Ce qu'on cherche

- voir si la personne cherche un complement ou un remplacement;
- valider une demarche prudente;
- garder le lien avec le parcours de soin si necessaire.

#### Bonne lecture attendue

- type d'appel: `demande d alternatif`
- risque: `non urgent`
- besoin dominant: `complement prudent + litteratie de parcours`
- sortie attendue: `complement prudent` plus eventuelle orientation vers psychologue / CLSC si besoin de suivi

#### Bonne phrase possible

`Dans ce que tu dis, je n'entends pas un refus aveugle du soin. On peut donc regarder des appuis complementaires prudents, sans opposer ca a une aide plus classique si elle devient necessaire.`

#### Erreurs a eviter

- pousser de force vers le reseau
- flatter un discours anti-medical sans nuance
- presenter l'alternatif comme traitement suffisant sans verification

---

### Cas 6 - Demande d'alternatif dangereuse

#### Scenario

`Je ne veux plus rien savoir des psychiatres. J'entends parfois des voix, mais je sais que c'est spirituel. Je veux seulement qu'on m'aide a me soigner autrement.`

#### Ce qu'on cherche

- reperer le risque de substitution;
- verifier la gravite;
- refuser de cautionner une voie dangereuse.

#### Bonne lecture attendue

- type d'appel: `demande d alternatif` avec possible `bascule urgence`
- risque: `eleve a critique selon desorganisation et securite`
- besoin dominant: `evaluation urgente ou specialisee`
- sortie attendue: `urgence psychiatrique` ou au minimum evaluation specialisee rapide

#### Bonne phrase possible

`Je peux entendre que tu veuilles donner un sens a ce que tu vis, mais je ne vais pas te laisser croire qu'on peut traiter ca seulement comme une voie alternative si ta securite ou ton ancrage sont en jeu.`

#### Erreurs a eviter

- valider sans nuance `c'est spirituel`
- rester seulement sur le registre de sens
- ignorer les voix comme drapeau rouge

---

### Cas 7 - Social dominant

#### Scenario

`Je suis en detresse, mais honnetement le pire c'est que je vais perdre mon logement, je suis endette, je ne comprends pas les demarches, et je suis seul.`

#### Ce qu'on cherche

- ne pas psychologiser excessivement;
- voir si le social est dominant;
- orienter vers le bon levier.

#### Bonne lecture attendue

- type d'appel: `standard`
- risque: `urgence sociale`
- besoin dominant: `social / psychosocial`
- sortie attendue: `travailleur social`, `CLSC`, accueil psychosocial, ressources communautaires specialisees

#### Bonne phrase possible

`Il y a bien une detresse psychique, mais ce que tu decris montre surtout une urgence sociale. Si on n'agit pas sur cette partie-la, on risque de medicaliser quelque chose qui est d'abord concret et structurel.`

#### Erreurs a eviter

- envoyer d'abord vers psychiatre
- oublier le travail social
- proposer seulement des exercices de bien-etre

---

### Cas 8 - Jeune avec adaptation / comportement

#### Scenario

`Mon fils de 14 ans accumule les conflits a l'ecole, n'arrive plus a suivre les regles, se fache vite, et ca dure depuis longtemps. Il n'est pas suicidaire, mais ca deborde partout.`

#### Ce qu'on cherche

- distinguer comportement / adaptation de crise aigue;
- voir les ressources jeunesse pertinentes.

#### Bonne lecture attendue

- type d'appel: `proche inquiet`
- risque: `non urgent sauf drapeau rouge additionnel`
- besoin dominant: `adaptation / comportement jeunesse`
- sortie attendue: `psychoeducateur`, ecole, services jeunesse, possiblement psychologue ou TS selon contexte

#### Bonne phrase possible

`A ce stade, on n'est pas necessairement dans une urgence, mais on n'est pas non plus dans quelque chose a laisser trainer. Il faudrait une ressource qui travaille sur l'adaptation et le comportement dans les milieux de vie.`

#### Erreurs a eviter

- orienter automatiquement vers urgence psy
- parler tout de suite de trouble grave sans base
- ignorer l'ecole et le milieu de vie

---

### Cas 9 - Sevrage dangereux

#### Scenario

`J'essaie d'arreter de boire seul depuis hier. Je tremble fort, je vois des choses, je suis confus par moments. Je voulais surtout de l'aide pour me detox autrement.`

#### Ce qu'on cherche

- reconnaitre le risque medical;
- ne pas laisser croire que l'alternatif ou une ressource non medicalisee suffit.

#### Bonne lecture attendue

- type d'appel: `bascule urgence`
- risque: `critique`
- besoin dominant: `evaluation urgente hospitaliere`
- sortie attendue: `urgence`

#### Bonne phrase possible

`Ce que tu decris n'est pas une simple demande de soutien ou d'alternatif. Il y a un risque medical important et il faut une evaluation urgente maintenant.`

#### Erreurs a eviter

- orienter seulement vers un service dependance non medicalise
- proposer respiration ou repos
- laisser attendre

---

### Cas 10 - Refus d'aide sans urgence immediate

#### Scenario

`Je sais que je vais mal, mais je ne veux pas consulter. Je veux juste comprendre ce que je peux faire seul pour l'instant. Je ne suis pas en danger immediate.`

#### Ce qu'on cherche

- respecter l'autonomie sans flatter l'evitement;
- voir s'il existe une porte d'entree acceptable;
- garder un seuil de bascule clair.

#### Bonne lecture attendue

- type d'appel: `standard` ou `demande d alternatif`
- risque: `non urgent a subaigu`
- besoin dominant: `clarification + orientation graduee`
- sortie attendue: `plan court`, `porte d'entree acceptable`, `signaux de bascule bien nommes`

#### Bonne phrase possible

`Je peux t'aider a clarifier une prochaine etape acceptable pour toi, mais je ne vais pas te vendre l'idee que tout peut se regler seul si la situation s'aggrave.`

#### Erreurs a eviter

- brusquer la personne inutilement
- valider totalement l'evitement
- oublier de nommer les seuils d'urgence

---

## 4) Grille de correction rapide

### Correct

L'operateur:
- pose le cadre;
- sonde le risque;
- nomme le besoin dominant;
- choisit la bonne sortie;
- maintient les limites MERLIN.

### A corriger

L'operateur:
- voit globalement juste;
- mais manque de clarte dans la sortie;
- ou oublie de nommer les seuils de bascule;
- ou glisse dans trop d'interpretation.

### Dangereux

L'operateur:
- banalise un drapeau rouge;
- survalide l'alternatif en contexte grave;
- diagnostique a distance;
- ne donne pas de prochaine action claire;
- continue la seance comme si de rien n'etait alors que le seuil urgent est franchi.

---

## 5) Decision active

Un operateur MERLIN doit etre capable de traiter correctement ces cas avant de se dire a l'aise avec le cadre de premiere ligne sante mentale.

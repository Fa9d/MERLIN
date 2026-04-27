# MERLIN - Workflow canonique MESANGE source claim dossier resolution V1

Date: 2026-04-25
Statut: draft
Objet: formaliser le cycle complet d'un sujet dans MESANGE, depuis l'entree d'une source jusqu'a la publication et a la resolution d'un dossier

---

## 1) Role de ce workflow

Ce workflow sert a:

- aligner les ecrans admin;
- structurer le travail des analystes;
- separer les statuts;
- poser les bifurcations utiles;
- rendre le systeme automatisable sans perdre la logique metier.

Il relie explicitement:

- les sources;
- les items ingeres;
- les claims;
- les evidences;
- les dossiers;
- les livrables;
- les budgets;
- la resolution.

---

## 2) Principe directeur

MESANGE ne doit pas transformer automatiquement tout contenu entrant en:

- verite;
- dossier;
- publication;
- urgence;
- sujet permanent.

Le workflow canonique doit obliger a distinguer:

1. `ce qui entre`
2. `ce qui merite un tri`
3. `ce qui devient un claim`
4. `ce qui merite un dossier`
5. `ce qui peut etre publie`
6. `ce qui reste a suivre`
7. `ce qui peut etre considere comme resolu`

Doctrine:

`Toute acceleration est acceptable si elle preserve cette separation.`

---

## 3) Vue d'ensemble

Le workflow V1 suit 8 etapes.

1. `Source`
2. `Item ingere`
3. `Tri`
4. `Claim`
5. `Evidence`
6. `Dossier`
7. `Livrable`
8. `Resolution`

Representation courte:

`source -> source_item -> tri -> claim -> evidence -> dossier -> publication -> resolution`

---

## 4) Etape 1 - Source

### Objet

- `source`

### Role

- definir l'origine d'une matiere surveillee.

### Entree

- creation manuelle;
- import;
- connecteur;
- abonnement a un flux;
- ajout d'une source interne.

### Sortie

- production reguliere ou ponctuelle de `source_item`.

### Decisons a ce stade

- source active ou non;
- frequence;
- cout estime;
- niveau de confiance;
- priorite par defaut.

---

## 5) Etape 2 - Item ingere

### Objet

- `source_item`
- eventuellement `document`

### Role

- representer une unite brute ou normalisee d'information.

### Entree

- capture depuis une source.

### Sortie

- mise en file de tri.

### Etats possibles

- `active`
- `ignored`
- `rejected`
- `attached`

### Regle

`un item ingere n'est pas encore un sujet`

---

## 6) Etape 3 - Tri

### Role

- filtrer le bruit;
- orienter l'information;
- decider quoi faire de l'item.

### Questions de tri

1. cet item est-il utile?
2. releve-t-il d'un sujet deja connu?
3. contient-il une ou plusieurs affirmations interessantes?
4. justifie-t-il l'ouverture d'un dossier?
5. est-ce du bruit, du doublon ou un hors-scope?

### Issues possibles

#### Issue A - Ignorer

Si:

- doublon;
- faible valeur;
- hors perimetre;
- bruit manifeste.

Effet:

- item conserve avec statut `ignored`.

#### Issue B - Rattacher

Si:

- l'item nourrit un dossier existant.

Effet:

- lien vers `dossier`.

#### Issue C - Extraire un claim

Si:

- l'item contient une affirmation verifiable.

Effet:

- creation de `claim`.

#### Issue D - Ouvrir un dossier

Si:

- le sujet justifie un suivi structure.

Effet:

- creation de `dossier`.

---

## 7) Etape 4 - Claim

### Objet

- `claim`

### Role

- transformer une affirmation floue en unite de verification.

### Entree

- item ingere;
- document normalise;
- extraction manuelle ou assistee.

### Champs critiques

- texte du claim
- acteur
- type de claim
- statut de verification
- niveau de confiance
- source d'origine

### Statuts cibles

- `non_verifie`
- `partiellement_etabli`
- `etabli`
- `trompeur`
- `contredit_par_les_faits`
- `non_documente`
- `en_attente_de_reponse`
- `obsolete`

### Regle

`un claim sans source ni note methodologique devient fragile`

---

## 8) Etape 5 - Evidence

### Objet

- `evidence`

### Role

- documenter ce qui soutient, contredit ou nuance le claim.

### Entree

- document officiel;
- citation;
- statistique;
- source secondaire;
- absence de preuve utile a noter.

### Questions a traiter

1. la preuve est-elle primaire ou secondaire?
2. soutient-elle vraiment le claim?
3. le contredit-elle?
4. est-elle trop faible pour conclure?
5. faut-il attendre une reponse?

### Issues

- renforcement du claim
- nuance
- contradiction
- maintien de l'incertitude

---

## 9) Etape 6 - Dossier

### Objet

- `dossier`
- `dossier_event`

### Role

- suivre un sujet dans le temps.

### Conditions d'ouverture recommandees

Un dossier peut etre ouvert si au moins l'un des cas suivants est vrai:

1. plusieurs items convergent sur le meme sujet;
2. un claim important exige un suivi longitudinal;
3. un enjeu public a un impact citoyen notable;
4. il existe un risque de disparition rapide du sujet sans memoire;
5. un client ou partenaire demande un suivi.

### Statuts dossier

- `a_trier`
- `ouvert`
- `en_analyse`
- `a_valider`
- `en_action`
- `en_surveillance`
- `resolu`
- `archive`
- `reouvert`

### Ce que contient un dossier

- resume courant
- claims
- chronologie
- acteurs
- publications
- budget / cout / revenu
- hypothese de resolution

### Regle

`un dossier sans resume courant et sans timeline devient vite inutilisable`

---

## 10) Etape 7 - Publication / livrable

### Objet

- `report`

### Role

- transformer un dossier ou un claim en sortie lisible.

### Types possibles

- `briefing`
- `fiche_verification`
- `chronologie`
- `chronique`
- `note_strategique`
- `synthese_executive`

### Conditions minimales avant publication

1. rattachement a un sujet ou dossier
2. niveau de confiance explicite
3. source(s) principales identifiees
4. distinction entre faits, interpretation et angle
5. validation editoriale si requis

### Bifurcations

#### Publication rapide

Cas:

- fiche courte;
- sujet ponctuel;
- faible risque editorial.

#### Publication de dossier

Cas:

- sujet plus lourd;
- besoin de chronologie;
- claims multiples;
- enjeu reputa tionnel plus fort.

---

## 11) Etape 8 - Resolution

### Objet

- `dossier`
- `dossier_event`
- eventuellement `value_assessment`

### Role

- cloturer ou suspendre proprement un sujet.

### Conditions de resolution possibles

Un dossier peut passer `resolu` si:

1. la question centrale a recu une reponse suffisamment claire;
2. les claims majeurs ont un statut stable;
3. l'evolution active du sujet est retombee;
4. une action concrete a ete prise ou documentee;
5. il ne justifie plus un suivi actif.

### Resolution ne veut pas dire oubli

Effets:

- le dossier reste consultable;
- la chronologie reste intacte;
- les claims gardent leur historique;
- le dossier peut etre `reouvert`.

### Reouverture

Motifs typiques:

- nouveau fait important;
- nouvelle contradiction;
- retour d'un acteur;
- correction publique;
- nouvelle consequence citoyenne.

---

## 12) Couche economique transversale

Le suivi economique ne vient pas a la fin.

Il doit intervenir a quatre moments.

### Moment A - A l'ouverture du dossier

Question:

- ce sujet merite-t-il un budget?

### Moment B - Pendant l'analyse

Question:

- combien coute la verification?

### Moment C - Avant publication lourde

Question:

- le cout est-il justifie par la valeur attendue?

### Moment D - A la resolution

Question:

- le dossier a-t-il produit une valeur economique ou strategique defendable?

---

## 13) Regles de bifurcation critiques

### Bifurcation 1 - Item -> claim

Ne pas creer de claim si:

- l'affirmation n'est pas isolable;
- le contenu est purement impressionniste;
- aucun travail de verification n'est pertinent.

### Bifurcation 2 - Claim -> dossier

Ne pas creer de dossier si:

- le claim est ponctuel et sans prolongement;
- la valeur de suivi est trop faible;
- le sujet sera mieux traite dans un autre dossier deja ouvert.

### Bifurcation 3 - Dossier -> publication

Ne pas publier si:

- le dossier reste trop incomplet;
- le niveau de confiance est trop faible sans disclaimer suffisant;
- l'angle editor ial n'est pas clarifie.

### Bifurcation 4 - Publication -> resolution

Ne pas marquer `resolu` juste parce qu'un rapport a ete publie.

La publication est une etape, pas une resolution en soi.

---

## 14) Etats minimaux a tracer dans l'interface

### Pour un `source_item`

- `a_trier`
- `ignore`
- `rattache`
- `transforme_en_claim`
- `transforme_en_dossier`

### Pour un `claim`

- `non_verifie`
- `en_attente_de_reponse`
- `partiellement_etabli`
- `etabli`
- `trompeur`
- `contredit_par_les_faits`
- `obsolete`

### Pour un `dossier`

- `a_trier`
- `ouvert`
- `en_analyse`
- `a_valider`
- `en_action`
- `en_surveillance`
- `resolu`
- `archive`
- `reouvert`

### Pour un `report`

- `draft`
- `submitted_for_review`
- `validated`
- `published`
- `archived`

---

## 15) Raccourci operationnel

Le raccourci que l'interface doit toujours permettre est:

1. recevoir un item
2. voir si c'est du bruit ou non
3. isoler le claim
4. chercher la preuve
5. rattacher ou ouvrir un dossier
6. mettre a jour le resume courant
7. publier si utile
8. clore ou surveiller

Si ce raccourci est casse, MESANGE perd sa fluidite.

---

## 16) Decision operative

Le workflow canonique V1 de MESANGE est:

`source -> source_item -> tri -> claim -> evidence -> dossier -> report -> resolution`

et non:

`source -> publication`

Ce point est fondamental.

---

## 17) Prochaine etape recommandee

Apres ce workflow, les deux livrables les plus utiles sont:

1. un backlog produit V1 MESANGE
2. une grille commerciale courte pour pitcher `Signal clair`, `Dossier suivi` et `Veille active`


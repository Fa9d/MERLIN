# MERLIN - Protocole entree client premiere ligne sante mentale (v1)

Date: 2026-04-20
Statut: draft
Objet: definir le protocole d'entree standard d'un client MERLIN, depuis le premier contact jusqu'a l'ouverture de seance, a l'orientation immediate ou a la bascule urgence

---

## 1) Finalite

Le protocole d'entree sert a:
- accueillir une demande sans confusion;
- verifier si la demande entre dans le champ MERLIN;
- reperer rapidement une urgence ou une crise;
- qualifier le type de besoin dominant;
- poser le cadre et les consentements minimaux;
- ouvrir la bonne suite:
  - seance standard;
  - orientation directe;
  - ressource de crise;
  - urgence.

Il ne sert pas a:
- diagnostiquer;
- faire une anamnese lourde;
- psychotherapiser des la premiere minute;
- accumuler des donnees non necessaires;
- retarder une escalade urgente.

---

## 2) Perimetre V1

Le protocole d'entree V1 est concu pour:
- adulte;
- premiere ligne;
- detresse psychologique, psychiatrique non aigue, psychosociale ou demande d'alternatif;
- canal prioritaire `telephone`;
- usage compatible ensuite avec web, mobile et application.

Hors perimetre V1:
- mineurs / parents comme regime principal;
- enregistrement systematique;
- transcription complete par defaut;
- situations somatiques lourdes hors champ;
- parcours specialise complexe des le premier contact.

---

## 3) Les 6 objectifs de l'entree

Le protocole d'entree doit repondre a 6 questions, dans cet ordre:

1. `Qui appelle et pour qui?`
2. `Y a-t-il un danger ou une crise aigue?`
3. `La demande entre-t-elle dans le champ MERLIN?`
4. `Quel est le besoin dominant initial?`
5. `Quel cadre et quels consentements minimums s'appliquent?`
6. `Quelle est la bonne prochaine etape?`

---

## 4) Les 4 sorties legitimes de l'entree

Le protocole d'entree doit toujours deboucher sur une sortie claire.

### A. Bascule urgence

Si danger immediat ou seuil critique.

Sortie:
- `911`
- urgence
- urgence psychiatrique

### B. Ressource de crise ou orientation immediate

Si crise forte sans danger vital clair, ou si hors champ total mais porte d'entree evidente.

Sortie:
- centre de crise
- ligne de crise
- `811`
- `CLSC`
- autre service evident

### C. Ouverture de seance MERLIN

Si la demande entre dans le champ et que le niveau de risque permet une seance.

Sortie:
- seance standard
- seance proche inquiet
- seance demande d'alternatif

### D. Refus de pseudo-prise en charge

Si la demande ne releve pas de MERLIN et ne doit pas etre garde e artificiellement.

Sortie:
- orientation breve et propre
- pas d'ouverture de faux suivi

---

## 5) Structure operatoire du protocole

Le protocole d'entree tient en 8 etapes.

### Etape 1 - Accueil tres bref

But:
- installer un contact;
- entendre la demande en une phrase;
- savoir si la personne parle pour elle-meme ou pour un proche.

Questions minimales:
- `Bonjour. Est-ce que tu appelles pour toi ou pour quelqu'un d'autre?`
- `En une phrase, qu'est-ce qui t'amene aujourd'hui?`

Sortie attendue:
- `appel_pour_soi`
- `appel_pour_proche`

### Etape 2 - Triage instantane de securite

But:
- reperer tres tot si le protocole normal doit etre interrompu.

Questions minimales:
- `Avant d'aller plus loin, est-ce qu'il y a un danger immediat pour toi ou pour quelqu'un d'autre en ce moment?`
- `Est-ce qu'il y a des idees suicidaires avec plan, moyens, ou quelque chose deja en cours?`
- `Est-ce qu'il y a confusion importante, voix, desorganisation majeure, violence, ou un etat qui fait craindre pour la securite?`

Si oui:
- sortir du protocole normal;
- passer en bascule urgence ou crise.

### Etape 3 - Qualification de champ

But:
- verifier si MERLIN est une porte d'entree legitime.

Questions utiles:
- `Est-ce que tu cherches surtout de l'ecoute, de la clarification, une orientation, une aide pour comprendre tes options, ou autre chose?`
- `Est-ce que ton besoin te semble surtout psychologique, social, relationnel, psychiatrique, ou lie a une recherche d'approche complementaire?`

Si besoin hors champ total:
- ne pas ouvrir de seance artificielle;
- orienter directement.

### Etape 4 - Type d'appel

But:
- classer l'appel dans une famille operatoire simple.

Types V1:
- `standard`
- `proche_inquiet`
- `demande_alternatif`
- `crise_a_orienter`
- `hors_champ_a_orienter`

### Etape 5 - Cadrage MERLIN

But:
- dire ce que MERLIN fait et ne fait pas avant d'aller plus loin.

Script minimal:

`Mon role ici est de t'aider a clarifier ce que tu vis, voir s'il y a des signes d'urgence, comprendre la bonne prochaine porte d'entree, et t'aider a repartir avec quelque chose de clair. Je ne pose pas de diagnostic et je ne remplace pas un soin clinique quand c'est necessaire.`

### Etape 6 - Consentements minimaux

Par defaut, l'entree V1 demande seulement:
- consentement a la seance ou a l'echange de qualification;
- consentement a la note breve.

Script minimal:

`Si on continue, nous allons travailler dans ce cadre et garder une note breve et utile de l'echange pour la continuite. Est-ce que cela te convient?`

Si historique futur envisage:
- demander le consentement specifique ensuite.

### Etape 7 - Lecture initiale du besoin dominant

But:
- nommer une premiere hypothese de besoin utile a l'orientation.

Categories V1 recommandees:
- `psychologique_psychotherapie`
- `psychiatrique_gravite_specialisee`
- `social_psychosocial`
- `crise_immediate`
- `litteratie_parcours`
- `complement_prudent`
- `mixte`

Questions utiles:
- `Qu'est-ce qui te pese le plus concretement aujourd'hui?`
- `Qu'est-ce que tu attends surtout de cette rencontre?`
- `Qu'est-ce qui t'empeche d'aller vers l'aide dont tu aurais besoin?`

### Etape 8 - Ouverture de la suite

But:
- ne jamais finir l'entree dans le flou.

Sorties possibles:
- `ouverture_seance_maintenant`
- `prise_de_rendez_vous`
- `orientation_immediate_service`
- `bascule_crise`
- `bascule_urgence`
- `refus_hors_champ_avec_orientation`

---

## 6) Script d'entree court recommande

Version telephone V1:

`Bonjour. Est-ce que tu appelles pour toi ou pour quelqu'un d'autre?`

`En une phrase, qu'est-ce qui t'amene aujourd'hui?`

`Avant d'aller plus loin, j'ai besoin de verifier rapidement la securite: est-ce qu'il y a un danger immediat, un risque suicidaire avec plan ou moyens, une grande confusion, des voix, une violence en cours, ou un etat qui fait craindre pour la securite?`

`D'accord. Mon role ici est de t'aider a clarifier ce que tu vis, voir s'il y a des signes d'urgence, comprendre la bonne prochaine porte d'entree, et t'aider a repartir avec quelque chose de clair. Je ne pose pas de diagnostic et je ne remplace pas un soin clinique quand c'est necessaire.`

`Si on continue, nous garderons une note breve et utile de cet echange pour la continuite. Est-ce que cela te convient?`

`Qu'est-ce qui te pese le plus en ce moment?`

`Ce que tu attends surtout aujourd'hui, c'est plutot de l'ecoute, de la clarification, une orientation, ou une aide pour comprendre quoi faire?`

`D'accord. A ce stade, la suite la plus juste me semble etre ...`

---

## 7) Donnees minimales a capter

Le protocole d'entree V1 doit pouvoir produire un objet d'entree minimal.

### Champs minimaux recommandes

- `entry_id`
- `date`
- `canal`
- `appel_pour`
- `type_appel`
- `motif_brut_court`
- `danger_immediat_reporte`
- `drapeaux_rouges_initiaux`
- `champ_compatible_merlin`
- `besoin_dominant_initial`
- `consentement_echange`
- `consentement_note`
- `sortie_entree`
- `orientation_initiale`
- `notes_breves`

### Valeurs conseillees

#### `canal`

- `telephone`
- `web`
- `mobile`
- `visio`
- `autre`

#### `appel_pour`

- `soi`
- `proche`

#### `type_appel`

- `standard`
- `proche_inquiet`
- `demande_alternatif`
- `crise_a_orienter`
- `hors_champ_a_orienter`

#### `sortie_entree`

- `ouverture_seance_maintenant`
- `prise_de_rendez_vous`
- `orientation_immediate_service`
- `bascule_crise`
- `bascule_urgence`
- `refus_hors_champ_avec_orientation`

Regle:

`l'entree ne doit pas produire un texte libre seulement; elle doit produire des champs stables`

---

## 8) Ce qu'il ne faut pas faire a l'entree

Ne pas:
- demander toute l'histoire de vie;
- demander une chronologie complete du trauma;
- valider trop vite une interpretation spirituelle ou alternative;
- laisser croire qu'on ouvre automatiquement un suivi;
- parler comme un clinicien reserv e;
- oublier de sonder la securite;
- finir sans prochaine action.

---

## 9) Articulation avec les autres documents

Ce protocole d'entree ouvre vers:
- [MERLIN_METH_PLAYBOOK_SEANCE_PREMIERE_LIGNE_SANTE_MENTALE_v1.0.md](C:/MERLIN/04_METHODES/MERLIN_METH_PLAYBOOK_SEANCE_PREMIERE_LIGNE_SANTE_MENTALE_v1.0.md)
- [MERLIN_METH_SCRIPT_SEANCE_STANDARD_30_MIN_SANTE_MENTALE_v1.0.md](C:/MERLIN/04_METHODES/MERLIN_METH_SCRIPT_SEANCE_STANDARD_30_MIN_SANTE_MENTALE_v1.0.md)
- [MERLIN_METH_SCRIPT_PROCHE_INQUIET_30_MIN_SANTE_MENTALE_v1.0.md](C:/MERLIN/04_METHODES/MERLIN_METH_SCRIPT_PROCHE_INQUIET_30_MIN_SANTE_MENTALE_v1.0.md)
- [MERLIN_METH_SCRIPT_DEMANDE_ALTERNATIF_30_MIN_SANTE_MENTALE_v1.0.md](C:/MERLIN/04_METHODES/MERLIN_METH_SCRIPT_DEMANDE_ALTERNATIF_30_MIN_SANTE_MENTALE_v1.0.md)
- [MERLIN_METH_SCRIPT_BASCULE_URGENCE_SANTE_MENTALE_v1.0.md](C:/MERLIN/04_METHODES/MERLIN_METH_SCRIPT_BASCULE_URGENCE_SANTE_MENTALE_v1.0.md)
- [MERLIN_METH_PACK_CONSENTEMENTS_SEANCES_DONNEES_v1.0.md](C:/MERLIN/04_METHODES/MERLIN_METH_PACK_CONSENTEMENTS_SEANCES_DONNEES_v1.0.md)
- [MERLIN_METH_FORMULAIRE_NOTE_SEANCE_PREMIERE_LIGNE_SANTE_MENTALE_v1.0.md](C:/MERLIN/04_METHODES/MERLIN_METH_FORMULAIRE_NOTE_SEANCE_PREMIERE_LIGNE_SANTE_MENTALE_v1.0.md)

---

## 10) Implication produit et application

Pour l'application future, le protocole d'entree doit exister sous trois formes compatibles:

1. `script operateur`
2. `formulaire structure`
3. `logique de routage`

Cela signifie:
- memes champs stables;
- memes categories de sortie;
- memes drapeaux rouges prioritaires;
- memes consentements minimaux.

L'interface peut changer.
Le protocole ne doit pas se dissoudre dans l'interface.

Reference schema:
- [MERLIN_PREU_SCHEMA_ENTREE_CLIENT_PREMIERE_LIGNE_v1.0.md](C:/MERLIN/05_PREUVES_SOURCES/SCHEMAS/MERLIN_PREU_SCHEMA_ENTREE_CLIENT_PREMIERE_LIGNE_v1.0.md)

---

## 11) Test de validite du protocole

Le protocole d'entree est bon si:
- il repere l'urgence en moins de 2 minutes quand elle existe;
- il n'ouvre pas de faux suivi hors champ;
- il nomme un besoin dominant initial sans surinterpreter;
- il pose le cadre MERLIN avant d'aller trop loin;
- il obtient un consentement minimum clair;
- il produit une sortie nette;
- il reste compatible avec la BDD et l'application.

---

## 12) Decision active

MERLIN adopte ce protocole d'entree comme base V1 de qualification initiale.

Il doit servir:
- a l'accueil telephone;
- a l'inscription ou prequalification web;
- a la formation operateur;
- a la conception de la couche `entry/intake` de l'application;
- au futur modele de donnees d'entree.

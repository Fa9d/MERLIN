# IVIA / MERLIN - Tableau donnees / consentements / diffusion client V1

Date: 2026-04-23
Statut: actif
Objet: fixer quelles donnees sont collectees, sous quelles conditions elles sont traitees, qui peut y acceder, et ce qui peut etre diffuse au client

---

## 1) Principe directeur

Le systeme distingue 4 niveaux:

1. `collecte`
2. `traitement interne`
3. `acces par role`
4. `diffusion client`

Dans la couche `diffusion client`, le systeme distingue aussi 4 etats logiques:

1. `internal_only`
2. `prepared_for_client`
3. `validated_for_client`
4. `delivered_to_client`

La regle centrale est:

`tout ce qui est collectable n'est pas automatiquement diffusable`

et:

`tout ce qui est analysable par MERLIN n'est pas automatiquement montrable au client`

---

## 2) Regles generales

### A. Minimisation publique

Le client ne doit voir que:
- ce qui lui est utile;
- ce qui est comprehensible;
- ce qui ne produit pas de confusion ou de surinterpretation;
- ce qui est conforme au cadre legal et au perimetre du service.

### B. Richesse interne gouvernee

MERLIN peut conserver davantage en interne si cela sert:
- la continuite;
- la qualite documentaire;
- la supervision;
- l'audit;
- l'amelioration de la methode;

mais uniquement sous gouvernance claire.

### C. Consentement specifique

Le consentement doit etre distingue par usage.

Il ne faut pas traiter comme un seul consentement flou:
- la seance;
- l'enregistrement;
- la transcription;
- la diffusion d'une note au client;
- l'usage pour apprentissage ou amelioration de methode.

### D. Droit de retenue documentaire

Toute note, derivee ou hypothese interne n'est pas diffusable par defaut au client.

La diffusion doit rester:
- volontaire;
- justifiee;
- proportionnee;
- intelligible.

### E. Diffusion tracable

Une donnee remise au client doit laisser au minimum une trace de:
- `delivered_to_client`
- `delivered_at`
- `delivery_channel_code`
- acteur humain ou systeme de remise

### F. `client_visible` ne veut pas dire `remis`

Un contenu peut etre:
- prepare pour le client;
- valide pour le client;
- mais pas encore remis.

La remise effective est un acte distinct.

---

## 3) Tableau principal

| Type de donnee | Collecte V1 | Consentement requis | Acces interne | Diffusion client V1 | Etat logique de diffusion V1 | Decision active |
|---|---|---|---|---|---|---|
| Identite minimale client | Oui | consentement general d'entree / service | operateur, supervision, admin technique si necessaire | partiellement, seulement les propres informations utiles du client | `delivered_to_client` pour l'espace client, sinon interne | collecte autorisee |
| Coordonnees contact | Oui | consentement general d'entree / service | operateur, admin technique si necessaire | oui, pour les coordonnees du client lui-meme | `delivered_to_client` pour l'espace client, sinon interne | collecte autorisee |
| Confirmation majorite | Oui | consentement general d'entree / service | operateur | non pertinent a diffuser comme bloc de contenu | `internal_only` | collecte autorisee |
| Motif d'entree / demande libre | Oui | consentement general d'entree / service | operateur, supervision | diffusable seulement sous forme reformulee ou reprise utile si pertinent | `prepared_for_client` -> `validated_for_client` -> `delivered_to_client` | collecte autorisee |
| Meta-donnees de seance | Oui | consentement general d'entree / service | operateur, supervision, admin technique partiel | oui partiellement: date, statut, type de seance | `delivered_to_client` pour les vues client utiles | collecte autorisee |
| Audio source | Oui si seance audio in-app | consentement explicite enregistrement audio | operateur, supervision selon besoin, admin technique tres limite pour maintenance | non par defaut | `internal_only` | collecte autorisee mais non diffusable |
| Transcription brute | Oui si audio capture et transcription activee | consentement explicite transcription | operateur, supervision, eventuellement admin technique restreint pour incident grave | non par defaut | `internal_only` | interne seulement |
| Note structuree operateur | Oui | consentement service + gouvernance documentaire | operateur, supervision | non sous forme brute; seulement via extrait reformule ou document derive valide | `prepared_for_client` -> `validated_for_client` -> `delivered_to_client` | diffusion conditionnelle |
| Resume client diffusable | Oui si produit | consentement service + validation de diffusion | operateur, supervision, client apres remise | oui | `prepared_for_client` -> `validated_for_client` -> `delivered_to_client` | diffusable |
| Hypotheses internes de lecture | Oui si utiles a la methode | pas de diffusion client automatique, usage interne gouverne | operateur, supervision, super admin selon perimetre | non | `internal_only` | strictement interne |
| Evaluation prudentielle du risque | Oui | consentement service + necessite operatoire | operateur, supervision | diffusion seulement sous forme utile, simple, non alarmiste, si necessaire | `prepared_for_client` -> `validated_for_client` -> `delivered_to_client` | diffusion tres limitee |
| Orientation proposee | Oui | consentement service | operateur, supervision, client apres remise | oui, si formulee comme prochaine etape prudente | `prepared_for_client` -> `validated_for_client` -> `delivered_to_client` | diffusable |
| Historique inter-seances | Oui | consentement historique / continuite | operateur, supervision | partiellement, seulement sous forme de continuite utile | `prepared_for_client` -> `validated_for_client` -> `delivered_to_client` | diffusion conditionnelle |
| Audit technique | Oui | pas de consentement de diffusion, base technique et securite | admin technique, supervision selon besoin | non | `internal_only` | strictement interne |
| Donnees derivees pour apprentissage de methode | Potentiellement oui | consentement distinct ou base legale clairement definie selon usage | supervision, recherche interne gouvernee, super admin selon perimetre | non | `internal_only` | hors diffusion client |

---

## 4) Tableau par role

| Role | Ce qu'il peut voir | Ce qu'il ne doit pas voir |
|---|---|---|
| Client | ses infos utiles, ses rendez-vous, ses resumes diffusables deja `delivered_to_client`, ses prochaines etapes, certaines sorties explicitement remises | audio brut, transcription brute, hypotheses internes, meta-analyse interne, audit, notes non validees ou non remises |
| Operateur | fiche client, intake, seances, audio rattache, transcription, notes, derivees operatoires, orientation, historique utile; peut preparer certaines sorties client | donnees techniques non necessaires, journaux admin complets hors besoin, diffusion brute par commodite |
| Supervision | ensemble des traces utiles a la qualite, a la supervision et a la revue de cas selon cadre; peut valider les sorties sensibles | acces technique illimite non justifie, publication client implicite sans trace |
| Admin technique | meta-donnees techniques, statuts, fichiers et incidents si necessaire a la maintenance; traces de remise et integrite des flux | lecture libre et non motivee du contenu sensible comme si c'etait une supervision clinique |
| Super admin / gouvernance | vision large si explicitement definie par le cadre interne, acces exceptionnel motive et journalise | diffusion au client sans filtre, sans validation ni base documentaire |

---

## 5) Ce qui peut etre diffuse au client

Peut etre diffuse au client:
- confirmation de reception;
- date, heure, statut de seance;
- resume simple post-seance;
- prochaine etape concrete;
- orientation formulee prudemment;
- note ou extrait explicitement prepare puis valide pour diffusion;
- rappel du cadre et des limites du service;

Condition:

- le client ne voit ces contenus qu'une fois `delivered_to_client`.

Peut etre diffuse au client seulement avec prudence:
- formulation d'un niveau de vigilance;
- rappel de points sensibles de parcours;
- resume inter-seances;

Dans ces cas, une validation `supervisor` est recommandee.

Ne doit pas etre diffuse au client par defaut:
- transcription brute;
- note brute operateur;
- hypotheses internes;
- logique d'analyse profonde;
- comparaisons inter-cas;
- signaux internes de recherche;
- journaux d'audit;
- commentaires de supervision.

---

## 6) Consentements minimaux distincts a prevoir

Les consentements V1 doivent etre separes au minimum en:

1. `consentement au service`
2. `consentement a l'enregistrement audio`
3. `consentement a la transcription`
4. `consentement a la conservation historique / continuite`
5. `consentement a la remise de note ou de resume au client`
6. `consentement a des usages secondaires eventuels` si un jour actives

Regle:

`pas de grand consentement unique qui melange tout`

---

## 7) Regles de diffusion client

Avant toute diffusion au client, verifier:

1. `est-ce utile pour la personne ?`
2. `est-ce comprehensible sans surinterpretation ?`
3. `est-ce compatible avec notre perimetre non medical ?`
4. `est-ce conforme au consentement applicable ?`
5. `est-ce que cela risque d'alarmer, de figer ou d'induire en erreur ?`
6. `est-ce valide et la remise sera-t-elle tracable ?`

Si l'une de ces questions echoue:
- la donnee reste interne.

---

## 8) Mapping V1 des etats de diffusion

Le mapping V1 retenu est:

| Etat logique | `client_visible` | `human_validation_status` | `delivered_to_client` |
|---|---|---|---|
| `internal_only` | `false` ou absent | `not_required` / `pending` | `false` |
| `prepared_for_client` | `true` | `pending` | `false` |
| `validated_for_client` | `true` | `validated` | `false` |
| `delivered_to_client` | `true` | `validated` | `true` |

Interpretation:

- `client_visible` signifie eligibilite documentaire a la diffusion;
- `client_visible` ne signifie jamais remise effective;
- le client ne doit voir que ce qui est deja `delivered_to_client`.

---

## 9) Regles sur audio et transcription

### Audio

L'audio est:
- collectable si la seance se fait dans l'application;
- rattachable a une session;
- conservable selon retention et politique de stockage;

Mais:
- non diffusable au client par defaut;
- non exploitable librement hors cadre de consentement.

### Transcription

La transcription est:
- une matiere interne de travail;
- utile pour note, synthese, comparaison et continuite;

Mais:
- elle n'est pas automatiquement une sortie client;
- une version client eventuelle doit etre reformulee et filtree.

---

## 10) Regles de retention

La retention doit distinguer:
- `source brute`
- `derive utile`
- `sortie client`
- `trace d'audit`

Principe:

`la source brute peut avoir une retention plus courte que la derive utile`

Exemple de logique:
- audio brut: retention courte ou archive froide gouvernee
- transcription brute: retention intermediaire
- note structuree utile: retention standard
- sortie client diffusable: retention selon relation de service
- audit: retention securite / conformite

Les durees exactes restent a figer dans une politique de retention separee.

---

## 11) Lignes rouges

Interdits actifs V1:
- donner au client l'impression qu'il accede a l'analyse interne complete;
- diffuser une hypothese interne comme si c'etait une verite clinique;
- laisser croire que la transcription brute est un document de restitution client standard;
- utiliser des donnees sensibles a des fins d'apprentissage sans cadre distinct;
- donner a l'admin technique un role implicite de lecture clinique libre.

---

## 12) Formule de controle

Avant d'ajouter une nouvelle donnee ou une nouvelle sortie, poser 5 questions:

1. `Pourquoi la collecte-t-on ?`
2. `Sous quel consentement ou base legitime ?`
3. `Qui en a reellement besoin ?`
4. `Doit-elle etre diffusable au client ?`
5. `Si oui, sous quelle forme simplifiee, prudente et utile ?`

---

## 13) Decision active

A compter de cette note:

- MERLIN distingue explicitement collecte, traitement, acces et diffusion;
- la diffusion client suit un workflow distinct entre preparation, validation et remise;
- `client_visible` n'est pas interprete comme une remise client;
- la diffusion client devient un acte separe, jamais un sous-produit automatique de l'analyse interne;
- l'audio et la transcription sont des materiaux internes gouvernes, pas des sorties client par defaut;
- les consentements doivent etre separes par usage;
- la remise client doit etre tracable;
- la richesse analytique interne peut croitre sans forcer la diffusion publique ou client.

---

## 14) References

- [MERLIN_GOUV_PLAN_EXECUTION_OPTIMAL_PROJET_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_PLAN_EXECUTION_OPTIMAL_PROJET_V1.md)
- [MERLIN_GOUV_DECISION_AUDIO_DANS_APP_OPERATEURS_PRATICIENS_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_DECISION_AUDIO_DANS_APP_OPERATEURS_PRATICIENS_V1.md)
- [MERLIN_GOUV_TABLEAU_FRONTIERES_DISCOURS_CAPACITES_IVIA_MERLIN_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_TABLEAU_FRONTIERES_DISCOURS_CAPACITES_IVIA_MERLIN_V1.md)
- [MERLIN_GOUV_POLICY_MEMOIRE_EVOLUTIVE_v1.0.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_POLICY_MEMOIRE_EVOLUTIVE_v1.0.md)
- [MERLIN_GOUV_SPEC_WORKFLOW_DIFFUSION_CLIENT_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_SPEC_WORKFLOW_DIFFUSION_CLIENT_V1.md)

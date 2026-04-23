# MERLIN - Spec contexte Quebec et signaux V1

Date: 2026-04-22
Statut: actif
Objet: traduire l'arbitrage du `Construit quebecois` en spec exploitable pour MERLIN

---

## 1) But

Ce document transforme la couche contextuelle quebecoise en spec de production prudente.

Il sert a:

- enrichir le bloc `contexte` du prompt `session_note_cercle_v1.py`;
- guider la lecture des signaux d'entretien dans une transcription quebecoise;
- proposer des hypotheses contextuelles activables;
- encadrer ce qui reste interne et ce qui ne doit pas etre dit au client.

Ce document:

- n'impose aucune explication culturelle;
- ne remplace jamais l'analyse individuelle;
- ne cree aucune psychologie culturelle definitive.

Regle centrale:

`MERLIN propose des hypotheses contextuelles a explorer, jamais des verites imposees.`

---

## 2) Regles d'usage

- Toujours formuler `peut indiquer`, `peut refleter`, `peut etre en lien avec`.
- Ne jamais transformer un signal en certitude sur la personne.
- Ne jamais utiliser le contexte Quebec comme explication automatique.
- Ne jamais tirer de these anti-medicalisation.
- Ne jamais utiliser de references aux Peuples Premiers sans cadre formel etabli.
- Ne jamais presenter une hypothese contextuelle comme une identite du client.
- Si les indices sont faibles, ne pas activer l'hypothese ou la marquer `confiance faible`.

---

## 3) Partie 1 - Pressions contextuelles Quebec

Les pressions ci-dessous sont des hypotheses contextuelles activables dans MERLIN.

Elles ne valent que si des indices observables apparaissent dans la transcription, dans le contexte immediate de la seance, ou dans la trajectoire du client.

## 3.1 Pression de silence et de minimisation

- Nom de la pression:
  `pression_silence_et_minimisation`
- Signal observable dans la transcription:
  banalisation repetee de la souffrance, phrases du type `c'est pas si pire`, `j'ai pas a me plaindre`, decalage entre la gravite de la situation et le ton du recit, consultation tardive apres une longue accumulation.
- Hypothese a proposer:
  `la personne peut avoir appris a tenir sans dire, ou a reduire verbalement ce qui pese reellement`
- Ce qu'on ne dit pas au client:
  on ne dit pas qu'il s'agit d'un trait culturel fixe, ni que la personne est incapable de nommer ce qu'elle vit.
- Dimension Le Cercle principalement touchee:
  `coeur`, avec impact frequent sur `corps`

## 3.2 Pression de performance et de charge de travail

- Nom de la pression:
  `pression_performance_travail`
- Signal observable dans la transcription:
  valorisation du surmenage, honte du repos, legitimite personnelle fondee sur la productivite, fatigue tenue pour normale, phrase du type `il faut que je tienne`, `j'ai pas le choix`, `je peux pas ralentir`.
- Hypothese a proposer:
  `la souffrance peut etre aggravee par une charge integree comme normale ou par une valeur personnelle tres liee a la performance`
- Ce qu'on ne dit pas au client:
  on ne dit pas que la personne est victime d'une culture unique du burnout, ni que tout epuisement vient du contexte social.
- Dimension Le Cercle principalement touchee:
  `esprit`, avec impact frequent sur `corps` et `etre`

## 3.3 Pression d'isolement relationnel

- Nom de la pression:
  `pression_isolement_relationnel`
- Signal observable dans la transcription:
  absence de reseau mobilisable, surinvestissement d'un seul lien, phrases du type `j'ai personne`, `je veux pas deranger`, `je garde ca pour moi`, lien numerique abondant mais peu de soutien reel.
- Hypothese a proposer:
  `la situation peut inclure un isolement peu nomme ou un reseau relationnel trop fragile pour absorber la charge actuelle`
- Ce qu'on ne dit pas au client:
  on ne dit pas que la personne est socialement incapable ni qu'elle confond necessairement solitude et depression.
- Dimension Le Cercle principalement touchee:
  `coeur`, avec impact frequent sur `etre`

## 3.4 Pression de honte de l'ambition ou de la reussite

- Nom de la pression:
  `pression_honte_ambition_ou_reussite`
- Signal observable dans la transcription:
  minimisation des succes, gene a parler d'argent ou de progression, peur de `se prendre pour un autre`, difficulte a negocier, discours contradictoire sur le desir de reussir.
- Hypothese a proposer:
  `la personne peut vivre une tension entre desir d'avancer et honte de s'autoriser cette avancee`
- Ce qu'on ne dit pas au client:
  on ne dit pas qu'il s'agit d'une caracteristique generale des Quebecois, ni que l'ambition est le probleme central.
- Dimension Le Cercle principalement touchee:
  `etre`, avec impact frequent sur `esprit`

## 3.5 Pression d'identite collective fragile

- Nom de la pression:
  `pression_identite_collective_fragile`
- Signal observable dans la transcription:
  hypersensibilite a la critique, difficulte a s'affirmer sans se justifier, sentiment de ne jamais etre a la bonne place, discours d'appartenance en tension, fragilite dans le rapport a la legitimite.
- Hypothese a proposer:
  `une tension d'appartenance ou de legitimite peut contribuer a la facon dont la personne se positionne et recoit les interactions`
- Ce qu'on ne dit pas au client:
  on ne dit pas que la personne porte un trauma collectif, ni qu'une histoire identitaire explique sa situation.
- Dimension Le Cercle principalement touchee:
  `etre`

## 3.6 Pression de medicalisation du sens

- Nom de la pression:
  `pression_medicalisation_du_sens`
- Signal observable dans la transcription:
  identite fortement formulee par le diagnostic, attente d'une reponse exterieure qui regle tout, vocabulaire tres centre sur l'etiquette plutot que sur l'experience vecue, difficulte a decrire la souffrance hors du langage du trouble.
- Hypothese a proposer:
  `la personne peut avoir appris a decrire sa souffrance surtout par une categorie diagnostique, ce qui peut laisser dans l'ombre certains aspects du contexte ou du sens vecu`
- Ce qu'on ne dit pas au client:
  on ne remet pas en cause un diagnostic, on ne suggere jamais de se mefier du soin medical, on ne parle pas de critique pharmaceutique.
- Dimension Le Cercle principalement touchee:
  `esprit`, avec impact frequent sur `corps`

## 3.7 Pression de deconnexion somatique

- Nom de la pression:
  `pression_deconnexion_somatique`
- Signal observable dans la transcription:
  douleurs, fatigue, tension, insomnie ou epuisement peu relies a l'experience emotionnelle, difficulte a dire ce qui se passe dans le corps, regulation frequente par substances, sucre, ecrans ou evitement.
- Hypothese a proposer:
  `une partie importante de la charge peut etre portee par le corps sans etre encore pleinement verbalisee`
- Ce qu'on ne dit pas au client:
  on ne dit pas que le symptome est psychologique, ni qu'il n'existe pas sur le plan medical.
- Dimension Le Cercle principalement touchee:
  `corps`

## 3.8 Pression de vide de sens ou de cadre

- Nom de la pression:
  `pression_vide_de_sens_ou_de_cadre`
- Signal observable dans la transcription:
  sensation de vide, perte de reperes, difficulte a relier les efforts a une direction, gene a parler de sens, de mort, de spiritualite ou d'orientation profonde.
- Hypothese a proposer:
  `la personne peut traverser une perte de sens ou un manque de cadre existentiel socialement difficile a nommer`
- Ce qu'on ne dit pas au client:
  on ne parle pas de vide spirituel collectif comme verite sur sa vie, on n'importe aucune these religieuse ou metaphysique.
- Dimension Le Cercle principalement touchee:
  `etre`, avec impact frequent sur `esprit`

## 3.9 Pression de rapport charge aux institutions

- Nom de la pression:
  `pression_rapport_aux_institutions`
- Signal observable dans la transcription:
  mefiance forte envers medecins, ecole, employeur, services publics ou systemes d'aide, sentiment de ne pas etre compris par les structures, fatigue administrative.
- Hypothese a proposer:
  `la charge actuelle peut etre amplifiee par des experiences institutionnelles percues comme froides, lourdes ou inadequates`
- Ce qu'on ne dit pas au client:
  on ne generalise pas en opposition systematique aux institutions, on ne presente pas le systeme comme ennemi global.
- Dimension Le Cercle principalement touchee:
  `esprit`, avec impact frequent sur `etre`

---

## 4) Partie 2 - Signaux d'entretien

Les signaux ci-dessous sont des patterns linguistiques ou comportementaux detectables dans une transcription.

Ils ne sont pas des preuves.

Ils servent a:

- ajuster le niveau de prudence;
- orienter les hypotheses contextuelles;
- guider d'eventuelles questions de clarification.

## 4.1 Minimisation

- Nom du signal:
  `minimisation_verbale`
- Exemples de formulations typiques:
  `c'est pas si pire`, `y'en a qui vivent pire`, `c'est rien`, `je veux pas me plaindre`, `ca va passer`
- Ce que le signal peut indiquer:
  la personne peut reduire verbalement l'intensite de ce qu'elle vit, par retenue, comparaison, honte ou habitude de tenir.
- Comment l'IA doit le traiter:
  comparer le ton avec les faits rapportes, verifier les contradictions, garder une vigilance douce sur une souffrance potentiellement sous-declaree.
- Ce que l'IA ne doit pas en conclure:
  ne pas conclure automatiquement a une depression cachee, a un trauma, ni a un trait culturel fixe.

## 4.2 Humour defensif

- Nom du signal:
  `humour_defensif`
- Exemples de formulations typiques:
  blagues juste apres un contenu lourd, auto-derision systematique, rire lorsqu'il est question d'epuisement, de solitude ou de honte.
- Ce que le signal peut indiquer:
  l'humour peut servir a contenir la charge, a proteger la dignite ou a eviter un contact direct avec une part sensible.
- Comment l'IA doit le traiter:
  noter le decalage entre contenu et ton, ne pas sur-lire, proposer une hypothese de protection relationnelle si le signal se repete.
- Ce que l'IA ne doit pas en conclure:
  ne pas conclure que la personne va bien parce qu'elle plaisante, ni que tout humour est defensif.

## 4.3 Honte de demander de l'aide

- Nom du signal:
  `honte_de_demander`
- Exemples de formulations typiques:
  `je veux pas deranger`, `je suis pas suppose etre rendu la`, `j'aurais du etre capable tout seul`, `j'aime pas demander`
- Ce que le signal peut indiquer:
  la demande d'aide peut etre chargee de honte, de culpabilite ou de peur de prendre trop de place.
- Comment l'IA doit le traiter:
  accorder de la valeur a la difficulte meme de la demande, lire le retard potentiel dans le recours a l'aide comme un indice contextuel.
- Ce que l'IA ne doit pas en conclure:
  ne pas conclure a un refus de lien, ni a une incapacite relationnelle durable.

## 4.4 Burnout normalise

- Nom du signal:
  `burnout_normalise`
- Exemples de formulations typiques:
  `tout le monde est fatigue`, `c'est normal en ce moment`, `faut passer au travers`, `je dors pas mais ca va`, `j'arrete pas`
- Ce que le signal peut indiquer:
  un epuisement peut etre integre comme etat normal ou valorise, ce qui retarde sa reconnaissance.
- Comment l'IA doit le traiter:
  relever les indices de charge et de cycle rompu, verifier la place du repos, du sommeil et des limites.
- Ce que l'IA ne doit pas en conclure:
  ne pas conclure a un burnout clinique, ni reduire toute fatigue a une pression culturelle.

## 4.5 Solitude non nommee

- Nom du signal:
  `solitude_non_nommee`
- Exemples de formulations typiques:
  `j'en parle pas vraiment`, `j'ai mes affaires`, `je gere ca`, `je veux pas appeler`, `je suis habitue`
- Ce que le signal peut indiquer:
  la personne peut manquer de lien mobilisable sans utiliser spontanement le mot solitude.
- Comment l'IA doit le traiter:
  regarder la realite du reseau plutot que la seule affirmation d'autonomie, distinguer isolement subi et solitude choisie.
- Ce que l'IA ne doit pas en conclure:
  ne pas conclure que la personne est isolee uniquement parce qu'elle est reservee.

## 4.6 Somatisation non verbalisee

- Nom du signal:
  `somatisation_non_verbalisee`
- Exemples de formulations typiques:
  `j'ai mal partout`, `je dors plus`, `j'ai toujours une boule`, `je suis vide`, `je suis a bout physiquement` sans lien clair etabli par la personne avec son vecu.
- Ce que le signal peut indiquer:
  une part du vecu peut s'exprimer principalement par le corps ou par des symptomes corporels.
- Comment l'IA doit le traiter:
  traiter les signaux corporels comme des indices importants de la dimension `corps`, tout en preservant l'ouverture vers une evaluation medicale si necessaire.
- Ce que l'IA ne doit pas en conclure:
  ne pas conclure que le probleme est `dans la tete`, ni nier une cause organique.

## 4.7 Honte du repos

- Nom du signal:
  `honte_du_repos`
- Exemples de formulations typiques:
  `je peux pas rien faire`, `je me sens mal quand j'arrete`, `je perds mon temps`, `j'ai pas merite de me reposer`
- Ce que le signal peut indiquer:
  la valeur personnelle peut etre fortement liee a l'utilite, a l'effort ou a la disponibilite constante.
- Comment l'IA doit le traiter:
  explorer prudemment le rapport entre repos, legitimite et securite interieure.
- Ce que l'IA ne doit pas en conclure:
  ne pas conclure que la personne est simplement perfectionniste ou productiviste par nature.

## 4.8 Honte de l'ambition ou de la reussite

- Nom du signal:
  `honte_ambition_reussite`
- Exemples de formulations typiques:
  `je veux pas me prendre pour un autre`, `c'est pas si important`, `je merite pas vraiment`, `je veux pas avoir l'air pretentieux`
- Ce que le signal peut indiquer:
  la progression, la visibilite ou la remuneration peuvent etre reliees a une crainte du jugement ou a une tension identitaire.
- Comment l'IA doit le traiter:
  formuler une hypothese faible sur la tension entre elan personnel et permission interieure.
- Ce que l'IA ne doit pas en conclure:
  ne pas conclure que toute modestie cache une honte structurante.

## 4.9 Identite fusionnee au diagnostic

- Nom du signal:
  `identite_diagnostic`
- Exemples de formulations typiques:
  `je suis anxieux`, `je suis depressif`, `je suis TDAH`, lorsque l'etiquette prend toute la place du recit.
- Ce que le signal peut indiquer:
  la personne peut s'appuyer sur une categorie medicale pour se comprendre, parfois au prix d'autres dimensions de contexte ou de sens.
- Comment l'IA doit le traiter:
  respecter le cadre medical evoque, mais rouvrir prudemment le recit vers l'experience vecue, le contexte et les tensions.
- Ce que l'IA ne doit pas en conclure:
  ne pas contester le diagnostic, ne pas opposer MERLIN au soin medical.

## 4.10 Hypersensibilite a la critique

- Nom du signal:
  `hypersensibilite_a_la_critique`
- Exemples de formulations typiques:
  recits ou toute remarque est vecue comme attaque globale, besoin de se justifier longuement, blessure recurrente dans des feedbacks ordinaires.
- Ce que le signal peut indiquer:
  une fragilite de legitimite, d'appartenance ou d'image de soi peut etre active.
- Comment l'IA doit le traiter:
  lier prudemment ce signal a la dimension `etre`, sans sur-psychologiser, et chercher des indices concrets de contexte.
- Ce que l'IA ne doit pas en conclure:
  ne pas conclure a un trouble de personnalite, ni a une simple susceptibilite culturelle.

## 4.11 Consultation tardive

- Nom du signal:
  `consultation_tardive`
- Exemples de formulations typiques:
  `ca fait longtemps que ca dure`, `j'aurais du venir avant`, `j'ai attendu que ca passe`, `je pensais etre capable`
- Ce que le signal peut indiquer:
  la demande d'aide peut avoir ete retardee par minimisation, honte, surcharge ou manque de place pour soi.
- Comment l'IA doit le traiter:
  relever l'accumulation temporelle comme facteur de contexte et de vigilance eventuelle.
- Ce que l'IA ne doit pas en conclure:
  ne pas conclure que le probleme est forcement grave parce que la demande est tardive.

## 4.12 Surinvestissement d'un lien unique

- Nom du signal:
  `surinvestissement_lien_unique`
- Exemples de formulations typiques:
  tout passe par `mon chum`, `ma blonde`, `ma mere`, `ma meilleure amie`, sans autre filet relationnel reel.
- Ce que le signal peut indiquer:
  le soutien peut etre trop concentre sur une seule relation, ce qui fragilise l'equilibre global.
- Comment l'IA doit le traiter:
  noter une vulnerabilite possible du reseau sans en faire une lecture pathologique.
- Ce que l'IA ne doit pas en conclure:
  ne pas conclure a une dependance affective sans autres indices.

---

## 5) Integration dans le prompt

Ce document alimente le bloc `contexte` du prompt `session_note_cercle_v1.py`.

Il doit etre integre comme:

- banque de pressions contextuelles possibles;
- banque de signaux linguistiques et comportementaux;
- couche d'hypotheses prudentes;
- aide a la formulation de questions de clarification.

Il ne doit pas etre integre comme:

- ontologie du client;
- grille culturelle automatique;
- systeme de conclusion deterministe.

Regle d'integration:

`le contexte Quebec enrichit la lecture; il ne remplace jamais la singularite de la personne.`

---

## 6) Filtrage de diffusion

Peut nourrir l'interne:

- hypothese contextuelle faible ou moyenne;
- signal de minimisation;
- tension entre travail et valeur;
- doute sur isolement ou honte de demander;
- articulation entre corps, charge et contexte.

Ne doit pas aller tel quel au client:

- attribution culturelle directe;
- formulation du type `vous etes pris dans une culture de ...`;
- these sur le vide spirituel collectif;
- lecture anti-medicalisation;
- toute reference aux Peuples Premiers hors cadre formel etabli;
- toute explication globale de type historique ou civilisationnelle.

---

## 7) References

- [MERLIN_GOUV_ARBITRAGE_PHILOSOPHIE_CONSTRUIT_QUEBECOIS_V0_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_ARBITRAGE_PHILOSOPHIE_CONSTRUIT_QUEBECOIS_V0_V1.md)
- [MERLIN_GOUV_SPEC_AXES_ANALYSE_CERCLE_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_SPEC_AXES_ANALYSE_CERCLE_V1.md)
- [PHILOSOPHIE_CONSTRUIT_QUEBECOIS_V.md](C:/MERLIN/memory/PHILOSOPHIE_CONSTRUIT_QUEBECOIS_V.md)

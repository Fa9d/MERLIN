# IVIA — Spécification de la page /comment-ca-fonctionne
## Transparence radicale : tous les mécanismes expliqués

**Version** : 1.0
**Date** : 9 mai 2026
**Statut** : Doctrine — à implémenter avant ouverture publique du pilote
**Auteur** : David Phaneuf (fondateur) + Perplexity Computer
**URL cible** : `https://ivia.pplx.app/comment-ca-fonctionne`
**Documents compagnons** :
- `04_METHODES/IVIA_FUNNEL_QUIZ_TO_GUIDANCE_v1.0.md` (funnel 8 écrans)
- `00_DOCTRINE/politique_gouvernance_donnees_agregees_v1.md` (strates A–E)
- `12_JURIDIQUE_AFFAIRES/IVIA_CONSENTEMENT_FUNNEL_LOI25_v1.0.md` (niveaux N0–N3)
- `00_DOCTRINE/veille_therapie_en_ligne_synthese_v1.md` (veille 15 services)
- `12_JURIDIQUE_AFFAIRES/IVIA_CADRE_IP_COLLECTIVE_v1.0.md` (propriété intellectuelle)

**Devises** : *Au sein de l'être — En actes.* — *Pour le peuple, par le peuple.*

---

## 1. Objectifs de la page

### 1.1 Transparence radicale comme différenciateur structurel

La page `/comment-ca-fonctionne` est l'opposé direct de ce que font BetterHelp, Talkspace et Pride Counseling : ces plateformes dissimulent leurs algorithmes de matching, rendent leurs tarifs réels illisibles avant la fin du quiz, et ne publient aucune description vérifiable de leurs mécanismes de gouvernance des données.

IVIA fonde sa différenciation sur la publication intégrale de ses mécanismes. Tout ce qui est décrit sur cette page doit être vrai en production. C'est un engagement opposable, pas un document de marketing.

**Principe de vérifiabilité permanente** : chaque mécanisme décrit (algorithme de matching, poids des critères, durées de conservation, niveaux de consentement) doit pouvoir être audité par tout journaliste, partenaire institutionnel ou client qui en fait la demande. Le code source du moteur de matching est destiné à être rendu public sous licence ouverte lors d'une prochaine version.

### 1.2 Lever toute friction explicative pour le client

Un client qui arrive sur `/comment-ca-fonctionne` doit en ressortir sans question ouverte sur :
- ce qu'IVIA fait de ses données,
- comment son praticien a été sélectionné,
- combien la séance lui coûtera réellement,
- comment annuler, modifier ou effacer son compte.

Aucune redirection vers un document juridique en PDF non lisible. Aucun renvoi vers un FAQ externe. Tout est sur cette page, en français québécois clair.

### 1.3 Servir de référence pour des interlocuteurs exigeants

Cette page est conçue pour être transmise sans modification à :
- un journaliste qui enquête sur la protection des données dans le secteur de la santé mentale au Québec,
- un partenaire institutionnel (MSSS, CISSS, ordre professionnel) qui évalue la conformité Loi 25,
- un investisseur qui évalue la solidité doctrinale de la plateforme,
- un avocat mandaté pour auditer les pratiques de consentement.

### 1.4 Anti-pattern par construction

**La règle cardinale de cette page** : ce qui y est écrit doit être vrai en production au moment de la publication. Si une fonctionnalité décrite n'est pas encore déployée, elle est clairement marquée `[À venir — version X]`. Aucune assertion prospective n'est présentée comme un fait présent.

Toute modification de la page déclenche automatiquement une notification aux clients actifs (voir section 4).

---

## 2. Wireframe textuel complet

---

### SECTION A — Le parcours client en 8 écrans

> **Résumé visuel** — Le funnel IVIA est un parcours en 8 écrans courts. Il dure environ 4 minutes. Il ne requiert ni compte ni carte bancaire.

```
[Écran 1] — Accueil et cadre
   ╿ Ce que vous faites ici. Ce qu'IVIA n'est pas.
   ╿ Ressources d'urgence visibles dès l'entrée.

[Écran 2] — État du moment
   ╿ Quatre états possibles : présence, agitation, brouillard, lourdeur.
   ╿ Aucun diagnostic. Aucune catégorie clinique.

[Écran 3] — Thèmes (optionnel)
   ╿ Multi-sélection parmi des thèmes généraux.
   ╿ Champ libre optionnel (200 caractères maximum).
   ╿ Mention chiffrement visible. Destruction 30 min si pas de compte.
   ╿ Ces données ne sont JAMAIS utilisées pour le matching praticien.

[Écran 4] — Voie d'entrée
   ╿ Quatre voies : parole et récit / fréquence et corps /
     connaissance et clarification / cadre culturel ou spirituel.

[Écran 5] — Rythme
   ╿ Préférence de cadence d'accompagnement.

[Écran 6] — Mode d'écoute
   ╿ Ce que la personne cherche dans une séance.

[Écran 7] — Texte d'ancrage (optionnel)
   ╿ Un souvenir, un moment, une image.
   ╿ Données chiffrées. Destruction 30 min si pas de compte.
   ╿ Indicateur de temporalité décalée calculé côté serveur.

[Écran 8] — Restitution et orientation
   ╿ Synthèse des réponses. Suggestion de praticien.
   ╿ Tarif affiché en clair. Création de compte optionnelle.
   ╿ Prise de contact ou fermeture honorable, au choix.
```

**Référence complète** : `04_METHODES/IVIA_FUNNEL_QUIZ_TO_GUIDANCE_v1.0.md`

---

### SECTION B — Comment IVIA suggère un praticien

#### B.1 L'algorithme est déterministe, simple et vérifiable

IVIA n'utilise pas d'intelligence artificielle conversationnelle ni d'apprentissage automatique pour suggérer un praticien. Le moteur de matching est un algorithme de pondération à quatre critères. Il est statique, auditable et peut être reproduit avec un tableur.

L'objectif de cette transparence est double :
- permettre à tout client de comprendre pourquoi un praticien lui a été suggéré,
- se distinguer explicitement des plateformes qui utilisent un matching par IA non documenté.

> **Comparaison directe** : Pride Counseling ([pridecounseling.com](https://www.pridecounseling.com)) mentionne un processus de matching sans en décrire les critères. BetterHelp ([betterhelp.com](https://www.betterhelp.com)) utilise un algorithme dont les paramètres ne sont pas publiés. IVIA publie ses quatre critères et leurs poids exacts ci-dessous.

#### B.2 Les quatre critères et leurs poids

| Critère | Source dans le funnel | Poids |
|---|---|---|
| Voie d'entrée choisie | Écran 4 | 35 % |
| Mode d'écoute choisi | Écran 6 | 35 % |
| Disponibilité du praticien + géographie | Base de données praticiens | 20 % |
| Langue (français / anglais / langue autochtone) | Préférence déclarée | 10 % |

**Total : 100 %**

#### B.3 Ce qui n'est jamais utilisé pour le matching

Les données de l'Écran 3 (thèmes, champ libre) ne sont pas utilisées pour suggérer un praticien. Ces données touchent à l'état intérieur de la personne. Leur usage pour le matching nécessiterait une validation éthique formelle qui n'a pas encore été conduite. Tant que cette validation n'est pas documentée et publiée sur cette page, ces données restent hors du moteur de matching.

**Règle opposable** : aucune donnée sensible des Écrans 2 et 3 n'alimente le matching praticien dans la version pilote (v1.x). Toute modification de cette règle fera l'objet d'une notification aux clients actifs et d'une mise à jour versionnée de cette page.

#### B.4 Ce qui se passe en cas d'absence de praticien disponible

Si aucun praticien ne correspond au score minimum requis (seuil de cohérence : à définir en production), l'Écran 8 affiche :
- une explication claire de l'absence de correspondance immédiate,
- une invitation à laisser ses coordonnées pour être contacté dès qu'un praticien devient disponible,
- les ressources de première ligne (voir Section F).

Il n'y a pas de suggestion dégradée sans avertissement. IVIA ne présente pas un praticien mal aligné comme un bon match.

---

### SECTION C — Tarifs

#### C.1 Tarif pilote

**80 $ CAD** pour une séance de 60 minutes.

Ce tarif est affiché avant toute création de compte. Il est affiché à l'Écran 8 du funnel, avant toute demande de coordonnées de paiement.

#### C.2 Ce qu'IVIA ne fait pas

- Pas d'abonnement mensuel.
- Pas de carte bancaire demandée avant la séance.
- Pas de frais cachés.
- Pas de facturation automatique récurrente.
- Pas de période d'essai qui se transforme en abonnement.

Le paiement est effectué au moment de la réservation confirmée, après échange avec le praticien.

#### C.3 Reçus pour assurances

IVIA émet un reçu pour chaque séance. Ce reçu mentionne explicitement :
- le type de service (accompagnement, écoute structurée),
- la nature non clinique du praticien si applicable (à préciser selon la composition du réseau),
- le montant en dollars canadiens.

**Note importante** : la couverture par une assurance privée dépend des conditions de votre régime. IVIA ne peut garantir le remboursement. Vérifiez auprès de votre assureur si l'accompagnement non clinique est couvert avant votre première séance.

#### C.4 Comparaison honnête avec les tarifs du marché

Les tarifs suivants sont ceux observés sur les sites officiels des plateformes concernées au moment de la rédaction de ce document (mai 2026). Ils peuvent avoir changé.

| Plateforme | Modèle | Tarif observé | Disponibilité Québec |
|---|---|---|---|
| **IVIA** | Par séance | 80 $ CAD / 60 min | Oui |
| **BetterHelp** ([betterhelp.com](https://www.betterhelp.com)) | Abonnement | 240 – 400 $ USD / mois | Oui (sans mention Loi 25) |
| **Talkspace** ([talkspace.com](https://www.talkspace.com)) | Abonnement | ~396 $ USD / mois | Oui (sans mention Loi 25) |
| **Online-Therapy.com** ([online-therapy.com](https://www.online-therapy.com)) | Abonnement | ~192 $ USD / mois | Partielle |
| **Inkblot Therapy** ([inkblottherapy.com](https://inkblottherapy.com)) | Par séance | ~90 $ CAD / heure | Oui (GreenShield) |
| **Teladoc** ([teladochealth.ca](https://www.teladochealth.ca/fr/)) | Par séance ou assurance | Variable | Oui |

Cette comparaison est présentée à titre informatif. IVIA ne dénigre pas ses concurrents. Elle publie les données disponibles publiquement pour que vous puissiez prendre une décision éclairée.

---

### SECTION D — Conservation et destruction des données

#### D.1 Les cinq strates de gouvernance des données IVIA

IVIA organise ses données en cinq strates, définies dans `00_DOCTRINE/politique_gouvernance_donnees_agregees_v1.md`. Voici leur résumé.

| Strate | Contenu | Propriété | Conservation par défaut |
|---|---|---|---|
| **A — Technique** | Locale, source, comportemental agrégé | IVIA | 24 mois (analytics agrégés) |
| **B — Séance brute** | Fichiers audio, transcriptions, notes praticien | Client / Praticien | 30 jours (audio brut), durée du compte (notes) |
| **C — Réponses qualifiées** | État du moment, thèmes structurés | Client | 30 min sans compte, sinon durée du compte |
| **D — Texte libre chiffré** | Champ libre Écran 3, texte d'ancrage Écran 7 | Client | 30 min sans compte, sinon durée du compte |
| **E — Temporalité décalée** | Indicateur dérivé, anonymisé, IP collective | IVIA (agrégat) | Indéfinie après anonymisation |

**Référence complète** : `00_DOCTRINE/politique_gouvernance_donnees_agregees_v1.md`

#### D.2 Sans compte : destruction automatique en 30 minutes

Si vous complétez le funnel sans créer de compte, toutes les données des Écrans 2 à 7 (strates C et D) sont détruites automatiquement après 30 minutes d'inactivité côté serveur. Ce délai est géré par un mécanisme de cache à durée de vie limitée (TTL). Aucune action de votre part n'est requise.

Vous pouvez également demander la destruction immédiate en cliquant sur le lien « Effacer mes données maintenant », visible sur chaque écran du funnel.

#### D.3 Avec compte : conservation chiffrée jusqu'à demande de suppression

Si vous créez un compte, vos données des strates C et D sont conservées dans votre profil, chiffrées au repos. Elles ne sont accessibles qu'à vous et à l'équipe technique IVIA en cas d'incident documenté et journalisé.

#### D.4 Demande de suppression de compte

**Délai cible IVIA : 72 heures.**
**Délai légal maximum : 30 jours (Loi 25, article 28.1).**

Pour demander la suppression :
1. Rendez-vous dans les paramètres de votre compte, section « Effacer mon compte et toutes mes données ».
2. Confirmez par courriel dans les 24 heures (délai de grâce pour annulation).
3. Vous recevez une confirmation d'effacement par courriel à l'issue du traitement.

**Important** : les données agrégées anonymisées (strate E) ne peuvent pas être effacées individuellement. Elles ne constituent plus un renseignement personnel au sens de la Loi 25 une fois anonymisées, et leur effacement individuel rétroactif est légalement non requis. Cette limite est expliquée au moment de la création de compte.

**Référence complète** : `12_JURIDIQUE_AFFAIRES/IVIA_CONSENTEMENT_FUNNEL_LOI25_v1.0.md`, section 3.

---

### SECTION E — Niveaux de consentement N0 à N3

IVIA applique quatre niveaux de consentement granulaires, conformément à l'article 8.1 de la Loi 25 (consentement manifeste, libre, éclairé, donné à des fins spécifiques).

#### Tableau récapitulatif

| Niveau | Déclencheur | Données couvertes | Mécanisme |
|---|---|---|---|
| **N0** | Arrivée sur l'Écran 1 | Strate A uniquement (technique, comportemental agrégé) | Mention sous le bouton « Commencer le point » |
| **N1** | Avant l'Écran 3 | Strate C (état du moment, thèmes structurés) | Mention explicite : « Vos réponses sont anonymes tant que vous ne créez pas de compte. Elles s'effacent automatiquement après 30 minutes d'inactivité. » Bouton « J'ai compris, je continue » |
| **N2** | Au moment de la saisie libre | Strate D (texte non structuré chiffré) | Mention contextuelle au-dessus du champ : chiffrement, destruction 30 min sans compte |
| **N3** | Création de compte (Écran 8 ou post-funnel) | Strates C, D et E | Page de création dédiée avec cases à cocher granulaires |

#### Cases à cocher N3 (création de compte)

- [ ] J'autorise IVIA à conserver mes réponses du quiz dans mon profil (strate C). *(Obligatoire pour créer un compte.)*
- [ ] J'autorise IVIA à conserver mon texte d'ancrage et mon indicateur de temporalité, chiffrés (strates D et E). *(Optionnel.)*
- [ ] J'autorise l'usage agrégé et anonymisé de mes données pour la recherche IVIA (strate E — indicateur de temporalité décalée). **Cette case est décochée par défaut.** *(Optionnel — toujours décochée par défaut, sans exception.)*

**Règle opposable** : la case de consentement à la recherche (strate E) est et demeurera décochée par défaut dans toutes les versions de la plateforme. Toute modification de ce paramètre par défaut nécessite une décision du comité doctrinal et une notification aux clients existants.

**Référence complète** : `12_JURIDIQUE_AFFAIRES/IVIA_CONSENTEMENT_FUNNEL_LOI25_v1.0.md`, section 2.

---

### SECTION F — IVIA n'est pas un service d'urgence

> **Encart fixe — Affiché sur cette page et sur chaque écran du funnel.**

IVIA est un service d'accompagnement de première ligne. Il n'est pas conçu pour les situations de crise aiguë. Si vous ou une personne de votre entourage êtes en situation d'urgence ou de détresse immédiate, contactez l'une de ces ressources :

| Ressource | Contact |
|---|---|
| **811 Info-Santé Québec** | 811 (ligne de santé 24/7) |
| **Ligne nationale de prévention du suicide** | 1 866 APPELLE (277-3553) |
| **Urgences générales** | 911 |
| **Ligne d'espoir pour le mieux-être des Premières Nations et des Inuit** | 1 855 242-3310 |
| **Tel-Aide Montréal** | 514 935-1101 |

Ces ressources sont disponibles en tout temps. IVIA ne se substitue à aucune d'entre elles.

---

### SECTION G — Comparaison honnête avec les acteurs présents au Canada

IVIA ne dénigre pas ses concurrents. Elle décrit les faits observés sur les sites officiels des plateformes concernées. Cette comparaison est versionnée (voir section Mises à jour) et mise à jour lorsque des changements significatifs sont constatés.

#### G.1 BetterHelp ([betterhelp.com](https://www.betterhelp.com))

- **Disponibilité Québec** : Oui.
- **Tarification** : Abonnement 240 – 400 $ USD / mois. Non affiché clairement avant la fin du quiz.
- **Conformité Loi 25** : Aucune mention explicite de la Loi 25 sur le site ou dans la politique de confidentialité observée.
- **Algorithme de matching** : Non publié. Aucun détail sur les critères utilisés.
- **Modèle de données** : Opacité totale sur les critères de matching. Données sensibles (état du moment, thèmes) potentiellement utilisées pour le matching sans déclaration.
- **Observation IVIA** : Plateforme techniquement disponible au Québec mais sans adaptation aux exigences légales provinciales et sans ancrage culturel québécois.

#### G.2 Teladoc ([teladochealth.ca](https://www.teladochealth.ca/fr/))

- **Disponibilité Québec** : Oui.
- **Tarification** : Par séance ou couvert par assurance employeur. Tarifs variables selon couverture.
- **Conformité Loi 25** : Conformité canadienne revendiquée (LPRPDE). Aucune mention explicite de la Loi 25 (provinciale, Québec) observée.
- **Algorithme de matching** : Non applicable (modèle médical avec assignation ou choix direct de médecin/thérapeute).
- **Observation IVIA** : Plateforme robuste à vocation médicale. Ne propose pas de voie d'entrée par fréquence, corps ou cadre culturel autochtone. Principalement orientée vers les organisations (assurance collective, employeurs).

#### G.3 Inkblot Therapy ([inkblottherapy.com](https://inkblottherapy.com))

- **Disponibilité Québec** : Oui. Partenaire GreenShield Canada.
- **Tarification** : ~90 $ CAD / heure. Tarif affiché de façon transparente.
- **Conformité Loi 25** : Non explicitement mentionnée. Politique canadienne de protection des données.
- **Algorithme de matching** : Mention d'un matching automatisé dans le flux d'inscription. Les critères ne sont pas tous publiés en détail public.
- **Version française québécoise** : Oui.
- **Observation IVIA** : Acteur canadien sérieux, tarification transparente, version française disponible. Différenciation IVIA : conformité Loi 25 explicite, ancrage 11 nations, voie fréquence/corps, indicateur de temporalité décalée.

#### G.4 TELUS Santé ([telus.com/health](https://www.telus.com/fr/health))

- **Disponibilité Québec** : Oui.
- **Tarification** : Principalement B2B (couverture employeur). Tarification individuelle non directement visible.
- **Conformité Loi 25** : Conformité canadienne revendiquée. Reconnaissance territoriale autochtone présente sur le site.
- **Modèle** : Principalement orienté vers les entreprises et les programmes d'aide aux employés (PAE).
- **Observation IVIA** : Acteur majeur de l'espace santé numérique au Québec. Fort ancrage institutionnel. Ne s'adresse pas directement aux individus hors couverture employeur. Reconnaissance territoriale autochtone mentionnée mais sans cadre opérationnel comparable à l'approche 11 nations d'IVIA.

#### G.5 Talkspace ([talkspace.com](https://www.talkspace.com))

- **Disponibilité Québec** : Oui (service en anglais principalement).
- **Tarification** : ~396 $ USD / mois (formule standard). Non affiché avant la fin du quiz.
- **Conformité Loi 25** : Aucune mention explicite.
- **Algorithme de matching** : Non publié.
- **Observation IVIA** : Modèle abonnement similaire à BetterHelp. Service principalement en anglais, sans adaptation au cadre légal québécois.

#### G.6 Position IVIA

| Dimension | IVIA |
|---|---|
| Tarification | 80 $ CAD / séance, affiché avant la création de compte |
| Conformité Loi 25 | Oui — documentée, versionnée, opposable |
| Ancrage autochtone | 11 nations — protocole opérationnel dédié |
| Voie fréquence et corps | Oui — voie d'entrée distincte dès l'Écran 4 |
| Indicateur de temporalité décalée | Oui — IP collective IVIA, premier usage documenté le 9 mai 2026 |
| Algorithme de matching publié | Oui — 4 critères, poids exacts, vérifiable |
| Données sensibles utilisées pour matching | Non — règle opposable, vérifiable |
| Abonnement automatique | Non |
| Compte requis avant valeur | Non |

---

### SECTION H — Reconnaissance territoriale

IVIA reconnaît que ses activités se déroulent sur les territoires non cédés de plusieurs nations autochtones.

À Tiohtià:ke / Montréal, ces territoires sont ceux du peuple Kanien'kehá:ka (Mohawk). Cette région est également connue comme un lieu de rassemblement et d'échange pour de nombreux peuples autochtones des Premières Nations.

IVIA opère également dans les territoires de nations dont la liste complète est en cours de validation avec les communautés concernées. La liste définitive des 11 nations de référence sera publiée dans une version ultérieure de cette page, après validation avec les représentants de chaque nation.

Cette reconnaissance n'est pas une formule rhétorique. Elle se traduit opérationnellement par :
- un mode d'écoute dédié (cadre culturel ou spirituel) dans le funnel d'orientation,
- un réseau de praticiens formés aux approches autochtones (voir `04_METHODES/MERLIN_METH_PLAYBOOK_PARTITION_AUTOCHTONES_v1.0.md`),
- un protocole de référencement vers les ressources de première ligne autochtones (voir `04_METHODES/MERLIN_METH_PLAYBOOK_PROTOCOLE_REFERENCEMENT_11_NATIONS_v1.0.md`),
- la ligne d'espoir pour le mieux-être (1 855 242-3310) visible à chaque étape du funnel.

IVIA s'engage à développer ses pratiques d'écoute en dialogue continu avec les nations concernées, et non de façon unilatérale. Les modalités de ce dialogue seront documentées et publiées au fil de leur évolution.

---

### SECTION I — Gouvernance et redevabilité

#### I.1 Comité doctrinal IVIA

Le comité doctrinal est l'instance qui valide les modifications substantielles de la doctrine, des mécanismes de données et des engagements de cette page.

**Composition prévue** *(rôles à nommer avant l'ouverture publique du pilote)* :

| Rôle | Statut |
|---|---|
| Fondateur — voix prépondérante en cas d'égalité | David Phaneuf |
| Représentant élu du réseau praticien | À nommer (mandat annuel renouvelable) |
| Représentant des clients actifs | À nommer (mandat 6 mois, tirage parmi les volontaires) |
| Conseiller en éthique externe indépendant | À nommer (sans conflit d'intérêts avec IVIA) |

Les décisions du comité sont documentées et publiées dans `00_GOUVERNANCE/IVIA_GOUVERNANCE_INTERNE_v2.0.md`.

#### I.2 Procédure de plainte

Toute personne — client, praticien, partenaire, observateur — peut déposer une plainte concernant la doctrine, les pratiques de données ou le comportement d'IVIA.

**Étape 1** : Écrire à l'adresse dédiée (à publier avant lancement — exemple de format : `plainte@ivia.ca`).

**Étape 2** : Accusé de réception dans les 5 jours ouvrables.

**Étape 3** : Traitement et réponse dans les 30 jours ouvrables.

**Étape 4** : Si la réponse n'est pas satisfaisante, escalade vers la Commission d'accès à l'information du Québec (CAI) — [cai.gouv.qc.ca](https://www.cai.gouv.qc.ca).

#### I.3 Responsable de la protection des renseignements personnels (RPRP)

Conformément à la Loi 25, IVIA désigne un Responsable de la protection des renseignements personnels.

| Champ | Information |
|---|---|
| Nom du RPRP | David Phaneuf (fondateur — en attendant la désignation d'un RPRP indépendant) |
| Coordonnées | À publier avant lancement (courriel dédié) |
| Rôle | Recevoir les demandes d'accès, de rectification et d'effacement ; surveiller la conformité Loi 25 ; escalader à la CAI si nécessaire |

#### I.4 Registre des activités de traitement

IVIA maintient un registre des activités de traitement (RAT) conformément aux exigences de la Loi 25. Ce registre est disponible sur demande auprès du RPRP.

---

## 3. Anti-patterns explicitement refusés sur cette page

Les éléments suivants sont interdits sur la page `/comment-ca-fonctionne`, par décision doctrinale opposable :

### 3.1 Chiffres non vérifiables

Aucun chiffre présenté sur cette page ne peut être inventé, arrondi de façon trompeuse ou non rattaché à une source vérifiable. Tout chiffre doit être accompagné de sa source, de sa date et de sa méthode de calcul.

**Exemples de chiffres refusés** :
- « Des milliers de clients satisfaits » — sans source.
- « 95 % de satisfaction » — sans méthode de mesure publiée.
- « Le service le plus transparent du Québec » — sans critère de comparaison.

### 3.2 Témoignages non sourcés

Aucun témoignage de client ou de praticien ne peut apparaître sur cette page sans :
- consentement écrit de la personne concernée,
- mention de la date du témoignage,
- possibilité de vérification sur demande.

Les témoignages pseudonymisés sont acceptés si le consentement et la date sont documentés.

### 3.3 Promesses de résultat

IVIA ne promet pas de guérison, d'amélioration garantie, de transformation personnelle ou de bien-être durable. L'accompagnement IVIA offre un espace structuré et une écoute qualifiée. Les résultats dépendent de nombreux facteurs qui échappent au contrôle d'IVIA et de ses praticiens.

**Formulations refusées** :
- « Retrouvez le bonheur en 3 séances. »
- « Des résultats prouvés. »
- « Vous méritez d'être heureux. » *(Voir veille BetterHelp / Faithful Counseling.)*

### 3.4 Assertions sur les fonctionnalités non encore déployées

Toute fonctionnalité décrite sur cette page comme existante doit être déployée en production. Si une fonctionnalité est prévue mais pas encore disponible, elle est explicitement marquée `[À venir — version X.x]`.

---

## 4. Versionnage et mises à jour

### 4.1 Versionnage public

Cette page est versionnée. Chaque modification majeure est documentée avec :
- un numéro de version (format `vX.Y`),
- une date de modification,
- un résumé des changements.

Lorsque le dépôt GitHub de la plateforme est rendu public, chaque version de cette page sera rattachée à un commit vérifiable. L'historique des versions sera accessible depuis cette page.

### 4.2 Définition d'une modification majeure

Sont considérés comme modifications majeures, déclenchant notification obligatoire aux clients actifs :
- tout changement dans les critères ou les poids de l'algorithme de matching,
- tout changement dans les durées de conservation des données,
- tout changement dans les niveaux de consentement,
- tout changement dans la tarification,
- toute modification des engagements de suppression (délai cible, délai légal),
- toute modification de la composition du comité doctrinal.

### 4.3 Modalité de notification

Les clients actifs reçoivent un courriel de notification dans les 7 jours suivant une modification majeure. Ce courriel décrit le changement, la date d'entrée en vigueur et les options disponibles (accepter, refuser, fermer le compte).

---

## 5. Liens vers les documents de référence

Les documents suivants complètent cette page. Ils sont accessibles sur demande auprès du RPRP ou seront publiés sur le site IVIA selon leur niveau de confidentialité.

| Document | Objet | Niveau d'accès |
|---|---|---|
| `04_METHODES/IVIA_FUNNEL_QUIZ_TO_GUIDANCE_v1.0.md` | Description complète des 8 écrans du funnel | Public (à venir) |
| `00_DOCTRINE/politique_gouvernance_donnees_agregees_v1.md` | Définition des cinq strates de données | Public (résumé) / Interne (complet) |
| `12_JURIDIQUE_AFFAIRES/IVIA_CONSENTEMENT_FUNNEL_LOI25_v1.0.md` | Niveaux de consentement N0–N3, procédures d'effacement | Public |
| `00_DOCTRINE/veille_therapie_en_ligne_synthese_v1.md` | Analyse comparative 15 services thérapie en ligne | Interne |
| `12_JURIDIQUE_AFFAIRES/IVIA_CADRE_IP_COLLECTIVE_v1.0.md` | Propriété intellectuelle collective IVIA | Interne |
| `04_METHODES/MERLIN_METH_PLAYBOOK_PROTOCOLE_REFERENCEMENT_11_NATIONS_v1.0.md` | Protocole de référencement vers les ressources des 11 nations | Public (à venir) |

---

## 6. Checklist d'implémentation avant lancement public

La liste suivante est à valider avant la mise en ligne de la page `/comment-ca-fonctionne` sur `ivia.pplx.app`.

### Contenu

- [ ] Tous les tarifs affichés sont conformes aux tarifs en production.
- [ ] L'algorithme de matching décrit en Section B est exactement celui déployé en production.
- [ ] Les durées de conservation décrites en Section D correspondent aux paramètres TTL en production.
- [ ] Les cases à cocher N3 décrites en Section E correspondent au formulaire de création de compte en production.
- [ ] Les ressources d'urgence de la Section F sont testées et fonctionnelles.
- [ ] Les liens vers les documents de référence (Section 5) sont actifs ou clairement marqués `[À venir]`.

### Gouvernance

- [ ] Le RPRP est nommé et ses coordonnées sont publiées.
- [ ] L'adresse de plainte est opérationnelle.
- [ ] Le comité doctrinal est constitué (ou une note de transition est publiée si constitution en cours).
- [ ] Le registre des activités de traitement (RAT) est à jour.

### Versionnage

- [ ] Le numéro de version et la date de la page sont affichés en bas de page.
- [ ] Le mécanisme de notification des clients en cas de modification majeure est opérationnel.

### Accessibilité et langue

- [ ] La page est en français québécois. Vouvoiement systématique. Aucune promesse excessive.
- [ ] Aucun emoji. Aucun point d'exclamation. Aucun chiffre non sourcé.
- [ ] La page est lisible sur mobile et sur écran large.
- [ ] Le contraste texte / fond est conforme WCAG AA (4,5:1 minimum pour le texte courant).

---

## 7. Éléments à valider avant publication finale

Les points suivants nécessitent une validation externe avant que la page soit considérée comme définitive.

| Point | Nature | Responsable | Échéance |
|---|---|---|---|
| Conformité Loi 25 de l'ensemble des mécanismes décrits | Validation juridique | Avocat mandaté (brief existant) | Avant lancement pilote |
| Liste définitive des 11 nations (Section H) | Validation avec représentants des nations | Fondateur + réseau autochtone IVIA | Avant V1.1 de la page |
| Seuil de cohérence de l'algorithme de matching (Section B.4) | Paramètre technique | Équipe technique | Avant lancement pilote |
| Coordonnées définitives du RPRP | Gouvernance | Fondateur | Avant lancement pilote |
| Adresse de plainte opérationnelle | Gouvernance | Fondateur | Avant lancement pilote |
| Validation tarif 80 $ CAD / 60 min | Modèle économique | Fondateur + praticiens pilote | Confirmé (voir `MERLIN_GOUV_MODELE_ECO_FRAIS_VOLUME_COUTS_SEUILS_v1.0.md`) |

---

## 8. Métadonnées du document

| Champ | Valeur |
|---|---|
| Titre | IVIA — Spécification de la page /comment-ca-fonctionne |
| Version | 1.0 |
| Date de création | 9 mai 2026 |
| Dernière modification | 9 mai 2026 |
| Auteur | David Phaneuf (fondateur) + Perplexity Computer |
| Statut | Doctrine — à valider avant implémentation |
| Prochain jalon | V1.1 — Après validation juridique et liste définitive 11 nations |
| Chemin | `04_METHODES/IVIA_SPEC_PAGE_COMMENT_CA_FONCTIONNE_v1.0.md` |

---

*Au sein de l'être — En actes.*
*Pour le peuple, par le peuple.*

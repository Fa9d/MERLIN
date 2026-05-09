# Politique de gouvernance des données agrégées IVIA — Version 1

**Document de doctrine interne**
**Auteur : système MERLIN — David Beaupré, fondateur IVIA**
**Date : mai 2026**
**Statut : document vivant — révision annuelle ou dès modification substantielle des pratiques**

---

## 1. Préambule — Continuité avec la doctrine existante

La présente politique ne remplace aucun document doctrinal antérieur. Elle comble trois angles morts identifiés lors de la session de conception du 9 mai 2026, que les textes fondateurs existants n'avaient pas eu à trancher parce que la plateforme n'avait pas encore atteint le stade de l'usage collectif des données.

**Ce que les documents existants couvrent déjà :**

- La *politique de confidentialité (Loi 25)* établit qui peut voir quoi, les durées de conservation par type de donnée, les droits des utilisateurs (accès, rectification, suppression, portabilité) et les coordonnées du Responsable de la protection des renseignements personnels (RPRP). Elle constitue le socle légal de base, conforme à la *[Loi modernisant des dispositions législatives en matière de protection des renseignements personnels](https://www.legisquebec.gouv.qc.ca/fr/document/lc/P-39.1)* (ci-après : Loi 25, L.R.Q. c. P-39.1).

- La *charte de transformation des données* pose le principe directeur : chaque acteur possède ses propres données, IVIA possède l'agrégat. Elle établit la distinction fondamentale entre donnée individuelle et donnée collective, et affirme que la mesure sert à soutenir, jamais à surveiller.

- Le *protocole de consentement client* définit les modalités de collecte du consentement initial au moment de l'inscription, conformément à l'article 14 de la Loi 25 (consentement manifeste, libre, éclairé, donné à des fins spécifiques, présenté distinctement).

- Le *cadre de propriété intellectuelle des données* distingue ce qui appartient au client, au praticien, et à IVIA en tant qu'organisation, notamment la taxonomie des motifs et le vocabulaire interprétatif.

- L'*indicateurs_praticien_v1* précise les catégories d'indicateurs, les règles de visibilité par acteur, et le dashboard public anonymisé, en référençant les articles 12 et 23 de la Loi 25.

- Le *dispositif_veille_ivia_v1* identifie la Loi 25 comme palier de veille légale prioritaire, avec une cadence de surveillance trimestrielle des lignes directrices de la [Commission d'accès à l'information (CAI)](https://www.cai.gouv.qc.ca).

**Ce que la présente politique ajoute :**

Trois questions restaient sans réponse opérationnelle précise : (1) qui décide qu'une donnée agrégée devient IP collective IVIA, reste confidentielle, ou peut être partagée avec un organisme tiers; (2) comment fonctionne le re-consentement lorsqu'un usage secondaire est envisagé 18 mois après l'inscription; (3) que se passe-t-il exactement pour la contribution d'un client aux analyses agrégées quand ce client demande son effacement. La présente politique répond à ces trois questions avec des mécanismes concrets.

---

## 2. Typologie des données IVIA — Cinq strates

### Strate A — Données personnelles identifiantes

**Définition :** nom, prénom, adresse courriel, numéro de téléphone (si collecté), coordonnées de paiement, adresse IP liée à un compte actif.

| Dimension | Règle |
|---|---|
| Propriété | Client ou praticien concerné |
| Accès | Titulaire + RPRP (accès journalisé) + équipe technique sur incident documenté |
| Effacement | Obligatoire dans les 30 jours suivant la demande ou la fermeture de compte (art. 23 Loi 25) |
| Conservation par défaut | Durée de la relation contractuelle + 12 mois après clôture du compte (fins de facturation, obligations légales) |

### Strate B — Données de séance brutes

**Définition :** fichiers audio déposés par le client, fichiers audio de lecture produits par le praticien, transcriptions automatiques, notes praticien liées à une séance spécifique.

| Dimension | Règle |
|---|---|
| Propriété | Client (audio déposé) / Praticien (lecture audio, notes) |
| Accès | Client voit ses dépôts et les lectures reçues. Praticien voit les dépôts du client attribué et ses propres lectures. Admin : accès sur incident documenté uniquement, journalisé. |
| Effacement | Audios bruts du client : destruction automatique 30 jours après traitement (sauf demande explicite de conservation). Lectures et notes : à la fermeture de compte ou sur demande explicite. |
| Conservation par défaut | Audios bruts : 30 jours. Transcriptions et lectures : durée du compte actif. |

### Strate C — Données comportementales individuelles

**Définition :** parcours d'un client identifié (fréquence des séances, praticiens consultés, motifs déclarés séance par séance, évolution autodéclarée, thèmes de clôture), ainsi que les indicateurs individuels d'un praticien identifié (charge, note client, délai de production, autoévaluation).

| Dimension | Règle |
|---|---|
| Propriété | Personne concernée (client ou praticien) |
| Accès | Titulaire seul + admin sous condition d'alerte documentée. Le praticien ne voit jamais les données comportementales d'un autre praticien. Le client ne voit jamais les données d'un autre client. |
| Effacement | Intégral et immédiat sur demande d'effacement (art. 23 et art. 28 Loi 25) |
| Conservation par défaut | Durée du compte actif |

### Strate D — Données comportementales agrégées anonymisées

**Définition :** statistiques mensuelles ou trimestrielles construites à partir de la strate C après anonymisation irréversible (suppression des identifiants directs + analyse des risques de réidentification selon le *[Règlement sur l'anonymisation des renseignements personnels](https://www.legisquebec.gouv.qc.ca/fr/document/rc/P-39.1,%20r.%200.1)*, en vigueur depuis le 30 mai 2024). Inclut : motifs récurrents anonymisés, durée médiane de parcours, taux de satisfaction global, distribution géographique par région, nuage de termes agrégés du dashboard public.

| Dimension | Règle |
|---|---|
| Propriété | IVIA (agrégat collectif) |
| Accès | Dashboard public : toute personne sans authentification. Dashboard admin réseau : équipe IVIA. Dashboard praticien : agrégat de sa propre clientèle (anonymisé, sans identification de clients individuels). |
| Effacement | Ces données ne contiennent plus de renseignement personnel au sens de la Loi 25 une fois anonymisées. Un effacement individuel ne peut les affecter rétroactivement (voir section 6). |
| Conservation par défaut | Illimitée pour les instantanés déjà publiés. Recalcul mensuel de l'instantané actif (voir section 6). |

### Strate E — Données dérivées et IP collective

**Définition :** modèles d'interprétation construits à partir des pratiques des praticiens IVIA, taxonomie des motifs d'accompagnement (vocabulaire structuré des thèmes récurrents), vocabulaire IVIA évolutif (terminologie doctrinale propre à la plateforme), grilles d'audit doctrinal, rapports trimestriels d'impact publiés.

| Dimension | Règle |
|---|---|
| Propriété | IVIA — propriété intellectuelle collective, définie dans le *cadre_propriete_intellectuelle_donnees* |
| Accès | Praticiens : accès en lecture à la taxonomie dans le cadre de leur pratique. Public : accès aux rapports trimestriels publiés. Chercheurs externes : accès supervisé sous accord cadre (voir section 8). |
| Effacement | Non applicable : il s'agit d'une production intellectuelle dérivée, non d'un renseignement personnel. |
| Conservation par défaut | Durée de vie de la doctrine IVIA; archivage permanent des versions successives. |

---

## 3. Circuit de décision sur l'usage des données agrégées

### Composition du comité doctrinal IVIA (hypothétique, à nommer au lancement)

- Fondateur (David Beaupré) — voix prépondérante en cas d'égalité
- Un représentant élu du réseau praticien (mandat renouvelable annuellement)
- Un représentant des clients actifs (volontaire, mandat de 6 mois, tirage parmi les volontaires)
- Un conseiller en éthique externe, indépendant d'IVIA (pas de conflit d'intérêts avec les activités de la plateforme)

Le comité se réunit sur convocation, minimalement une fois par trimestre, et à chaque fois qu'une proposition d'usage nouveau des données est soumise.

### Critères de décision pour autoriser un usage nouveau

Avant tout usage nouveau des strates D ou E, le comité doctrinal évalue quatre critères :

1. **Cohérence doctrinale** : l'usage proposé est-il cohérent avec la doctrine « Au sein de l'être — En actes » et avec le principe « Pour le peuple, par le peuple » ? Un usage qui transforme la plateforme en outil de surveillance ou de profilage commercial est exclu d'office.

2. **Bénéfice collectif démontrable** : l'usage produit-il un bénéfice pour les personnes accompagnées ou pour la collectivité (santé publique, accessibilité des services, connaissance scientifique) ? Un bénéfice purement commercial pour IVIA ne suffit pas.

3. **Risque de réidentification** : une analyse de risque formelle, réalisée sous la supervision d'une personne compétente en anonymisation (art. 90, Loi 25; *Règlement sur l'anonymisation*), confirme-t-elle que les données demeurent irréversiblement anonymisées dans le contexte de l'usage proposé ?

4. **Consentement requis** : le nouvel usage implique-t-il des données qui peuvent être rattachées, même indirectement, à des individus identifiables ? Si oui, un re-consentement est obligatoire (voir section 5).

### Processus décisionnel

**Étape 1 — Proposition d'usage** : tout acteur (praticien, partenaire externe, équipe IVIA) soumet une proposition écrite au RPRP. La proposition précise : nature des données visées, finalité, destinataires, durée, modalité de diffusion des résultats.

**Étape 2 — Analyse d'impact** : le RPRP réalise une évaluation des facteurs relatifs à la vie privée (EFVP), conformément à l'article 3.3 de la Loi 25. Cette évaluation porte sur les risques pour la vie privée et sur la cohérence doctrinale.

**Étape 3 — Décision du comité** : le comité doctrinal se prononce dans un délai de 21 jours ouvrables. La décision est motivée par écrit.

**Étape 4 — Consultation publique si usage public** : si l'usage envisagé produit un résultat diffusé publiquement (rapport, publication académique, outil ouvert), une consultation de 15 jours est ouverte auprès des utilisateurs actifs avant mise en oeuvre.

**Étape 5 — Re-consentement si individus identifiables** : si l'EFVP conclut à un risque résiduel de rattachement à des individus, le mécanisme de re-consentement décrit à la section 5 est activé.

**Registre public des décisions :** chaque décision du comité est consignée dans un registre public accessible depuis le site IVIA (section « Gouvernance »), avec : date, objet de la décision, critères retenus, résultat, nom du signataire. Les décisions de refus sont également consignées, sans exposer les propositions confidentielles des tiers.

---

## 4. Consentement gradué — Modèle à trois niveaux

Le consentement est collecté à l'inscription, en application de l'article 14 de la Loi 25 : il doit être manifeste, libre, éclairé, spécifique à chaque fin, présenté distinctement de toute autre information, et rédigé en termes simples et clairs.

### Niveau 1 — Obligatoire (sans cette case, pas d'accès au service)

Prestation du service d'écoute IVIA, conservation des renseignements personnels nécessaires au compte (courriel, historique de séances), accès du praticien assigné aux dépôts audio et transcriptions de la séance en cours.

### Niveau 2 — Opt-in par défaut acceptable

Participation aux statistiques agrégées anonymisées d'IVIA : vos séances contribuent, sous forme anonymisée et irréversible, aux données du tableau de bord public mensuel et aux rapports trimestriels d'impact. Vous ne serez jamais identifié. Vous pouvez vous retirer à tout moment depuis votre espace personnel.

### Niveau 3 — Opt-in explicite à chaque usage distinct

Participation à un projet de recherche externe (université, MSSS, CIUSSS, fondation) impliquant des données issues de la plateforme IVIA. Chaque projet de recherche fait l'objet d'un re-consentement distinct (voir section 5). Votre refus n'affecte pas le service.

---

**Schéma de l'écran d'inscription — Texte des trois cases (français québécois IVIA)**

```
[ IVIA — Votre consentement ]

La case 1 est nécessaire pour accéder au service.
Les cases 2 et 3 sont entièrement à votre choix.

[ ✓ ] CASE 1 — OBLIGATOIRE
  J'accepte qu'IVIA conserve les renseignements nécessaires à
  mon compte (mon courriel, mon historique de séances) et les
  partage avec le ou la praticien·ne qui m'accompagne,
  uniquement pour la durée de mes séances.
  Sans cette case, je ne peux pas utiliser IVIA.

[   ] CASE 2 — OPTIONNELLE (je choisis librement)
  J'accepte que mes séances contribuent, de façon anonymisée
  et irréversible, aux statistiques collectives d'IVIA
  (tableau de bord public, rapport trimestriel d'impact).
  Mon nom et mon identité ne seront jamais exposés.
  Je peux changer d'avis à tout moment dans mon espace.

[   ] CASE 3 — OPTIONNELLE (je serai toujours demandé·e avant)
  Je suis ouverte ou ouvert à être contacté·e si IVIA envisage
  de partager des données anonymisées dans le cadre d'une
  recherche universitaire ou d'un projet de santé publique.
  Je recevrai une demande claire avant chaque projet,
  et je pourrai refuser sans conséquence sur mon service.
```

---

## 5. Re-consentement secondaire — Mécanisme opérationnel

### Déclencheurs

Le re-consentement secondaire est obligatoire dans les situations suivantes :
- IVIA envisage un nouvel usage des données (strates D ou E) non couvert par le consentement initial;
- Un partenariat externe est conclu avec un organisme (CIUSSS, MSSS, université, fondation) qui implique un accès, même anonymisé, aux données de la plateforme;
- La finalité d'un usage en cours est modifiée de façon substantielle;
- Le comité doctrinal conclut, dans son analyse d'impact, que le risque de réidentification n'est pas nul.

### Délais

- Minimum : 30 jours entre l'envoi de la demande de re-consentement et le début de l'usage envisagé.
- Recommandé : 60 jours, pour permettre une réponse éclairée, notamment pour les personnes dont la fréquence d'utilisation de la plateforme est faible.

### Canaux de notification

- Courriel direct à l'adresse associée au compte, avec lien de réponse unique horodaté.
- Notification dans le tableau de bord client, visible à la prochaine connexion.
- Lecture audio explicative d'environ 90 secondes, accessible depuis la notification, rédigée dans un registre accessible pour les personnes en situation de faible littératie numérique ou écrite. Ce format audio est cohérent avec la nature d'IVIA comme plateforme d'écoute.

### Texte type (courriel — français québécois)

> Bonjour,
>
> IVIA souhaite vous informer d'un nouveau projet qui pourrait impliquer des données issues de la plateforme.
>
> **Ce projet :** [nom du projet, organisme partenaire, finalité en une phrase].
>
> **Ce que ça signifie concrètement :** [description de ce qui serait partagé, sous quelle forme, et ce qui ne le sera jamais — notamment aucun audio brut, aucune donnée nominative].
>
> **Ce qu'on vous demande :** simplement de nous dire si vous acceptez que vos données contribuent à ce projet. Votre réponse n'affecte pas votre accès au service IVIA, quoi que vous décidiez.
>
> Vous avez jusqu'au [date — 30 jours minimum] pour répondre.
>
> [Bouton : Oui, j'accepte] [Bouton : Non, je refuse] [Bouton : Écouter l'explication audio]
>
> Si vous ne répondez pas avant cette date, votre réponse sera considérée comme un refus. Vos données ne contribueront pas à ce projet. C'est la règle chez IVIA.
>
> Pour toute question : privacy@ivia.quebec

### Absence de réponse

La politique IVIA est strictement opt-in. L'absence de réponse dans le délai imparti équivaut à un refus. Aucune donnée de la personne qui n'a pas répondu ne sera incluse dans l'usage envisagé. Cette règle s'applique même si la personne avait coché la case 3 à l'inscription — la case 3 indique une ouverture à être sollicitée, elle ne constitue pas un consentement préalable à un projet non encore défini.

### Registre horodaté des consentements et révocations

Chaque consentement donné, refusé ou révoqué est consigné dans un registre interne avec : identifiant pseudonymisé de la personne, date et heure de la réponse, canal utilisé, nature de l'usage consenti ou refusé, version du texte de demande présenté. Ce registre est conservé pendant toute la durée de l'usage concerné, plus cinq ans, conformément aux obligations de reddition de comptes de la Loi 25 (art. 3.2 — politiques et pratiques de gouvernance).

---

## 6. Effacement vs analyses agrégées — Politique claire

### Portée de l'effacement

Lorsqu'un client demande l'effacement de ses données (en vertu du Code civil du Québec, art. 40, et de l'article 28 de la Loi 25 — rectification et suppression — ainsi que de l'article 28.1 — cessation de diffusion et désindexation), IVIA procède dans les 30 jours à :

- Suppression irréversible de toutes les données de la strate A (identifiants, compte, coordonnées de paiement).
- Suppression irréversible de toutes les données de la strate B (audios déposés, lectures reçues, transcriptions, notes de praticien).
- Suppression irréversible de toutes les données de la strate C (parcours individuel, motifs déclarés séance par séance, autoévaluations).
- Notification confirmée par courriel au client et au RPRP, avec attestation de suppression (art. 35 Loi 25).

### Ce qui ne peut pas être effacé rétroactivement

Les données de la strate D — données comportementales agrégées anonymisées — qui ont déjà été incluses dans des publications, des rapports trimestriels ou des instantanés du dashboard public ne peuvent pas être retirées individuellement. La raison est technique et légale : l'anonymisation irréversible, réalisée conformément à l'article 23 de la [Loi 25](https://www.legisquebec.gouv.qc.ca/fr/document/lc/P-39.1) et au *[Règlement sur l'anonymisation des renseignements personnels](https://www.legisquebec.gouv.qc.ca/fr/document/rc/P-39.1,%20r.%200.1)* (en vigueur depuis le 30 mai 2024), signifie que la contribution individuelle n'est plus identifiable dans l'agrégat. Il n'existe aucun moyen technique de la retirer sans refaire l'ensemble du calcul à partir des données brutes, qui auront elles-mêmes été effacées.

La [CAI](https://www.cai.gouv.qc.ca/protection-renseignements-personnels/sujets-et-domaines-dinteret/principaux-changements-loi-25) et le gouvernement du Québec confirment que les renseignements correctement anonymisés ne sont plus soumis à la Loi 25 et peuvent être conservés à des fins sérieuses et légitimes.

### Effets sur le dashboard public

Le dashboard public est recalculé mensuellement à partir de la base de données active au moment du calcul. La personne dont le compte a été effacé disparaît du prochain instantané mensuel. Elle ne figure pas dans les projections futures. Ses données historiques, déjà fondues dans des agrégats publiés antérieurement, demeurent dans ces publications passées — elles y sont mathématiquement irréversibles.

### Effets sur les analyses futures

La personne effacée n'apparaît plus dans aucune analyse, rapport ou tableau de bord produit après la date d'effacement confirmée.

### Texte remis au client demandeur

> Votre demande d'effacement a été reçue et traitée le [date].
>
> Voici ce qui a été supprimé de façon permanente :
> - Votre compte et toutes vos coordonnées personnelles.
> - Tous les enregistrements audio que vous aviez déposés.
> - Toutes les lectures et transcriptions associées à vos séances.
> - Votre journal personnel.
> - Votre historique de séances et tous les renseignements liés à votre parcours.
>
> Voici ce qui ne peut pas être effacé, et pourquoi :
> Vos séances ont contribué, de façon anonyme et irréversible, aux statistiques collectives d'IVIA publiées avant cette date. Cette contribution ne peut pas être retirée de ces publications passées : l'anonymisation a été faite selon un processus qui rend toute réidentification impossible, conformément au Règlement sur l'anonymisation des renseignements personnels du Québec (en vigueur depuis le 30 mai 2024). Vous n'apparaissez plus dans aucun calcul futur.
>
> Si vous avez des questions, écrivez à privacy@ivia.quebec.

---

## 7. Monétisation et valorisation éthique

### Principe absolu

Aucune donnée audio brute ne sera jamais monétisée, partagée, licenciée ou transmise, sous quelque forme que ce soit, à quelque tiers que ce soit. Ce principe est sans exception.

### Ce qui peut être valorisé

La strate E — la taxonomie des motifs, les modèles d'interprétation, le vocabulaire IVIA évolutif — constitue une production intellectuelle collective qui peut faire l'objet de licences à des fins compatibles avec la mission d'IVIA. Les usages acceptables incluent : partenariat de recherche avec une université québécoise ou canadienne francophone, contribution à un projet de santé publique du MSSS ou d'un CIUSSS, licence à une fondation dont la mission est alignée avec l'autonomie et le bien-être non clinique. Dans tous les cas, la licence est soumise à l'approbation du comité doctrinal (voir section 3) et fait l'objet d'un accord écrit précisant les conditions d'usage, les limites d'exploitation et la durée.

### Ce qui est interdit

- Revente ou transmission de données comportementales individuelles ou agrégées à des assureurs, employeurs, plateformes publicitaires, agrégateurs de données de santé à des fins commerciales.
- Utilisation de la taxonomie ou des modèles IVIA pour entraîner un système d'intelligence artificielle sans accord exprès du comité doctrinal et sans EFVP préalable (art. 3.3 Loi 25).
- Utilisation des données IVIA à des fins de prospection commerciale ou philanthropique, explicitement exclue de la notion de « fins compatibles » à l'article 12 de la Loi 25.

### Mécanisme de redistribution

Lorsqu'IVIA perçoit une rémunération pour une licence d'usage de la strate E, la répartition suivante s'applique :
- 40 % au fonds collectif IVIA (développement de la plateforme, formation des praticiens, accessibilité du service).
- 40 % distribués aux praticiens actifs au moment de la signature de la licence, au prorata de leur volume de pratique sur les 12 mois précédents.
- 20 % réservés à un fonds d'accessibilité permettant de subventionner des séances pour des personnes à faible revenu.

Ce mécanisme est cohérent avec les principes du *modele_valorisation_ivia* (à articuler dans ce document connexe) et avec la doctrine « Pour le peuple, par le peuple ».

---

## 8. Gouvernance pratique — Qui fait quoi

### Responsable de la protection des renseignements personnels (RPRP)

En vertu de l'article 3.1 de la Loi 25, la personne ayant la plus haute autorité au sein de l'entreprise est responsable de la protection des renseignements personnels. Chez IVIA, cette fonction est exercée par David Beaupré (fondateur), joignable à privacy@ivia.quebec. Cette information est publiée sur le site public d'IVIA, conformément à l'article 3.1. Le RPRP peut déléguer cette fonction par écrit à une personne compétente à mesure que la plateforme se développe. Toute délégation est documentée et notifiée aux utilisateurs.

**Responsabilités du RPRP :**
- Recevoir et traiter les demandes d'accès, de rectification et d'effacement dans les délais légaux (30 jours, art. 32 Loi 25).
- Réaliser les EFVP avant tout nouveau module de collecte ou usage des données (art. 3.3 Loi 25).
- Tenir le registre des consentements et des décisions du comité doctrinal.
- Superviser ou déléguer les processus d'anonymisation conformément au Règlement sur l'anonymisation.
- Notifier la CAI en cas d'incident de confidentialité présentant un risque de préjudice sérieux (art. 3.5 Loi 25).

### Comité doctrinal (voir section 3)

Gouverne les décisions sur les usages nouveaux des strates D et E. Distinct du rôle opérationnel du RPRP.

### Praticiens

- Voient l'ensemble de leurs propres indicateurs (strates B et C les concernant).
- Voient l'agrégat anonymisé de leur propre clientèle (strate D partielle — sans identification de clients individuels).
- Voient l'agrégat collectif du réseau (strate D publique).
- Ne voient jamais les données comportementales d'un autre praticien ou d'un client au-delà du cadre de leur propre relation de séance.
- Peuvent exporter leurs propres données dans un format portable (art. 27 Loi 25 — droit à la portabilité, en vigueur depuis septembre 2024).

### Clients

- Voient l'ensemble de leurs propres données (strates A, B, C les concernant).
- Voient l'agrégat collectif public (strate D — dashboard public anonymisé).
- Ne voient jamais les données d'un autre client ni les indicateurs individuels d'un praticien.

### Administration technique

- Accède aux données uniquement dans le cadre d'un incident technique documenté, sur demande explicite du RPRP.
- Tout accès est journalisé avec horodatage, motif et identité de l'accédant.
- Le journal d'audit est accessible au praticien ou au client concerné sur demande.

### Chercheurs externes

- Accèdent uniquement aux données de la strate D (agrégats publics) ou, dans le cadre d'un accord supervisé approuvé par le comité doctrinal, à des extraits de la strate E.
- N'accèdent jamais aux strates A, B ou C.
- Tout accès supervisé est encadré par un accord écrit précisant les fins, les conditions d'utilisation, les mesures de sécurité, les obligations de publication et les modalités de destruction des données à la fin du projet.

---

## 9. Articulation avec les autres doctrines — Tableau de cohérence

| Doctrine existante | Ce qu'elle couvre déjà | Articulation avec la présente politique | Action requise |
|---|---|---|---|
| *charte_transformation_donnees* | Principe « chaque acteur possède ses données, IVIA possède l'agrégat »; mesurer pour soutenir | La présente politique opérationnalise ce principe avec des strates précises et un circuit de décision | Ajouter dans la charte un renvoi à la présente politique pour les questions de décision sur l'agrégat |
| *politique_confidentialite_loi25* | Droits des utilisateurs, qui voit quoi, durées de conservation, RPRP, sécurité | La présente politique complète la section 6 (apprentissage de l'outil) avec le mécanisme de re-consentement et la politique d'effacement vs agrégat | Ajouter dans la politique un renvoi à la section 5 (re-consentement) et à la section 6 (effacement) de la présente politique |
| *protocole_consentement_client* | Modalités du consentement initial (art. 14 Loi 25) | La présente politique ajoute le modèle à 3 niveaux (section 4) et le mécanisme de re-consentement secondaire (section 5) | Intégrer le texte des 3 cases (section 4) dans le protocole existant comme gabarit opérationnel |
| *cadre_propriete_intellectuelle_donnees* | Distinction entre données client, données praticien, IP IVIA | La présente politique précise les strates D et E, le circuit de valorisation éthique (section 7) et le mécanisme de redistribution | Aligner la définition de l'IP collective dans le cadre avec la strate E définie ici |
| *modele_valorisation_ivia* | (À rédiger) | La section 7 de la présente politique pose les principes directeurs de la monétisation éthique qui devront être repris et détaillés dans ce document | Rédiger le modèle_valorisation_ivia en s'appuyant sur les principes de la section 7 |
| *indicateurs_praticien_v1* | Catégories d'indicateurs, règles de visibilité, dashboard public, gouvernance des données (section 8) | La présente politique formalise et complète la section 8 de ce document avec le comité doctrinal, le circuit de décision et la politique d'effacement | Aucune modification requise dans indicateurs_praticien_v1 — la présente politique s'y articule sans contradiction |
| *dispositif_veille_ivia_v1* | Veille légale Loi 25 (palier A), cadence trimestrielle CAI | La présente politique génère de nouvelles obligations de veille : modifications du Règlement sur l'anonymisation, nouvelles lignes directrices CAI sur la gouvernance des données agrégées | Ajouter au tableau de veille palier A : suivi du Règlement sur l'anonymisation (Gazette officielle) et des décisions CAI portant sur le re-consentement |

---

## 10. Calendrier de mise en oeuvre — 6 jalons sur 12 mois

**Jalon 1 — Mois 1 (lancement pilote, mai 2026)**
Activation des 3 cases de consentement à l'inscription (section 4). Publication du titre et des coordonnées du RPRP sur le site public (art. 3.1 Loi 25). Ouverture du registre des consentements horodatés. Première réunion de constitution du comité doctrinal (définir les membres, le mandat, la fréquence).

**Jalon 2 — Mois 2-3 (phase pilote)**
Réalisation de l'EFVP pour le module de tableau de bord public et pour le rapport trimestriel d'impact (art. 3.3 Loi 25). Mise en place du journal d'audit des accès admin. Rédaction et approbation du premier accord-cadre type pour les chercheurs externes (modèle à valider par le comité doctrinal).

**Jalon 3 — Mois 4-5**
Publication de la première version publique du registre des décisions doctrinales (section 3). Intégration du mécanisme de re-consentement (section 5) dans la plateforme technique : envoi courriel, notification dashboard, accès à la lecture audio explicative. Premier exercice de test du processus d'effacement complet avec un utilisateur de la phase pilote volontaire.

**Jalon 4 — Mois 6 (mi-parcours)**
Réalisation du premier audit interne de conformité : toutes les strates sont-elles correctement délimitées techniquement ? Le journal d'audit est-il complet ? Le registre d'anonymisation (obligatoire depuis le 1er janvier 2025 selon le Règlement) est-il tenu à jour ? Révision du présent document si des ajustements sont nécessaires.

**Jalon 5 — Mois 8-9**
Premier usage de la strate E envisagé (rapport trimestriel d'impact public — octobre 2026). Application complète du circuit de décision (section 3) : EFVP, comité doctrinal, consultation publique 15 jours, publication au registre. Si un partenariat externe est à l'étude, premier déclenchement du mécanisme de re-consentement secondaire (section 5).

**Jalon 6 — Mois 12 (bilan annuel)**
Révision complète de la présente politique à la lumière des 12 premiers mois d'opération. Mise à jour du tableau de cohérence (section 9) selon l'état réel des autres doctrines. Rapport au comité doctrinal sur : nombre de demandes d'effacement reçues et traitées, nombre de re-consentements déclenchés et taux de réponse, incidents de confidentialité survenus (le cas échéant), décisions du comité et leur résultat. Publication d'un résumé public de ce bilan dans la section « Gouvernance » du site IVIA.

---

## Références légales et sources

- *Loi modernisant des dispositions législatives en matière de protection des renseignements personnels* (Loi 25, L.R.Q. c. P-39.1) — [LégisQuébec](https://www.legisquebec.gouv.qc.ca/fr/document/lc/P-39.1) : art. 3.1 (RPRP), art. 3.2 (politiques de gouvernance), art. 3.3 (EFVP), art. 4 et 5 (limitation de la collecte), art. 8 (information à la collecte), art. 12 (limitation de l'usage, définition du sensible et du dépersonnalisé), art. 14 (qualité du consentement), art. 23 (destruction ou anonymisation), art. 27 (portabilité), art. 28 (rectification/suppression), art. 28.1 (cessation de diffusion et désindexation), art. 32 (délai de réponse 30 jours), art. 35 (attestation de suppression).
- *Règlement sur l'anonymisation des renseignements personnels*, en vigueur depuis le 30 mai 2024 — [LégisQuébec](https://www.legisquebec.gouv.qc.ca/fr/document/rc/P-39.1,%20r.%200.1) : processus d'anonymisation, critères d'individualisation/corrélation/inférence, registre d'anonymisation (obligatoire depuis le 1er janvier 2025).
- Commission d'accès à l'information (CAI) — [Principaux changements apportés par la Loi 25](https://www.cai.gouv.qc.ca/protection-renseignements-personnels/sujets-et-domaines-dinteret/principaux-changements-loi-25).
- Gouvernement du Québec — [Anonymisation des renseignements personnels](https://www.quebec.ca/gouvernement/travailler-gouvernement/normes-gouvernance-pratiques-internes/protection-des-renseignements-personnels/anonymisation) : critères des trois tests (individualisation, corrélation, inférence).
- Code civil du Québec, art. 35-40 (protection des renseignements personnels, droit de suppression des renseignements périmés ou non justifiés).

---

*Document vivant — toute modification aux strates de données, aux règles de visibilité, aux critères du comité doctrinal ou aux mécanismes de consentement requiert la validation du RPRP et l'approbation du comité doctrinal. Version suivante prévue : mai 2027 ou dès modification réglementaire substantielle.*

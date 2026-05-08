# PROTOCOLE DE CONSENTEMENT CLIENT IVIA
## Consentement granulaire à 3 niveaux — Procédure, UX et documentation

**Version** : 1.0 — Vague 2
**Date** : Mai 2026
**Statut** : Document opérationnel — Applicable dès le Palier 1
**Loi de référence** : Loi 25 (Québec), RGPD (UE si applicable)
**RPRP** : David Phaneuf — privacy@ivia.quebec

---

## PRÉAMBULE ÉTHIQUE

### Le consentement n'est pas une case à cocher

Dans la culture numérique dominante, le consentement est devenu une formalité — un obstacle à franchir rapidement pour accéder à un service. Une page de conditions générales de 40 pages. Un bouton « J'accepte » cliqué sans lecture. Un consentement global qui couvre tout sans distinguer quoi que ce soit.

IVIA fait le choix inverse. Le consentement est ici un acte délibéré, informé et continu. Ce n'est pas une signature sur un contrat d'adhésion — c'est une décision libre que vous posez sur chaque usage spécifique de vos données.

Cette approche découle directement des 7 principes directeurs IVIA :
- Du Principe 1 (le vivant d'abord) : vos besoins réels — dont la sécurité et la maîtrise de vos données — précèdent tout intérêt commercial
- Du Principe 4 (l'autonomie comme horizon) : vous êtes maître de ce que vous confiez et de la manière dont cela est utilisé
- Du Principe 5 (la responsabilité comme dignité) : vous êtes traité comme un adulte capable de comprendre et de décider, pas comme un utilisateur à convaincre de cocher toutes les cases

Le présent protocole décrit comment IVIA met en œuvre ce consentement dans la pratique : sa structure, sa formulation, son interface, sa révocation, sa documentation.

---

## PARTIE I — CADRE JURIDIQUE

### I.1 Loi 25 — Articles de référence

**Article 12 (LPRPSP modifiée par Loi 25)** : Le consentement à la collecte, à la communication ou à l'utilisation de renseignements personnels doit être manifeste, libre, éclairé et accordé à des fins spécifiques. Il doit être demandé de façon séparée pour chaque finalité.

**Article 12.1** : Le consentement des personnes mineures de moins de 14 ans doit être donné par leurs parents ou tuteurs. Pour les 14-17 ans, le mineur lui-même peut consentir pour le service, avec accord parental pour les niveaux optionnels.

**Article 14** : Le consentement ne peut pas être une condition d'accès au service lorsqu'il porte sur une finalité non nécessaire à ce service.

**Article 27 (portabilité)** et **Article 28 (rectification et suppression)** : droits garantis et procédures détaillées dans la Politique de confidentialité.

**Interprétation pour IVIA** :
- Le Niveau 1 (enregistrement pour production documentaire) est nécessaire au service : il est une condition d'accès aux fonctionnalités documentaires
- Les Niveaux 2 et 3 (dataset et modèle) ne sont pas nécessaires au service : ils ne peuvent pas être des conditions d'accès au Service de base

### I.2 RGPD — Articles de référence (si applicable)

**Article 6** : bases légales du traitement. Pour IVIA : exécution d'un contrat (Niveau 1), consentement (Niveaux 2 et 3), intérêt légitime (amélioration du service sur données anonymisées).

**Article 7** : conditions du consentement. Le consentement doit être libre, spécifique, éclairé et univoque. Le retrait du consentement doit être aussi facile que son accord.

**Article 9** : traitement des données biométriques (la voix est une donnée biométrique). Base légale requise : consentement explicite (art. 9.2.a).

**Article 17** : droit à l'effacement. Applicable sans délai injustifié.

---

## PARTIE II — STRUCTURE DES 3 NIVEAUX DE CONSENTEMENT

### II.1 Vue d'ensemble

| Niveau | Nom | Nature | Condition d'accès | Révocable |
|---|---|---|---|---|
| Niveau 1 | Consentement au service | Obligatoire pour les fonctionnalités documentaires | Oui — sans Niveau 1 : pas de transcription ni de documents MERLIN | Oui — pour les séances futures |
| Niveau 2 | Contribution au dataset | Optionnel | Non | Oui — effet dans les 7 jours |
| Niveau 3 | Contribution au modèle | Optionnel (plus restrictif) | Non | Oui — avant intégration dans un cycle |

**Règle absolue** : les Niveaux 2 et 3 ne conditionnent jamais l'accès au Service de base. Refuser les Niveaux 2 et 3 n'entraîne aucun désavantage dans la qualité du service reçu.

---

### II.2 Niveau 1 — Consentement au service

#### Finalités

1. Enregistrement audio de la séance en vue de la production documentaire (transcription, analyse, synthèse)
2. Conservation temporaire de l'audio brut jusqu'à J+30, puis destruction irréversible certifiée
3. Conservation de la transcription pseudonymisée pendant 90 jours
4. Production de documents de suivi validés par le praticien
5. Transmission au client et au praticien des documents produits

#### Ce que cela permet concrètement

- La transcription automatique de votre séance par le système MERLIN
- La production d'une synthèse de séance, d'un compte rendu et de pistes de mise en pratique
- La conservation de votre dossier de suivi si vous avez plusieurs séances avec le même praticien

#### Ce que cela ne signifie PAS

- Votre voix identifiable ne sera pas conservée au-delà de J+30
- IVIA ne « garde pas » votre voix dans ses serveurs de manière prolongée
- La transcription est pseudonymisée dès sa production (nom remplacé par un identifiant neutre)

#### Droits associés

- Accès à votre transcription pendant les 90 jours de conservation
- Exportation de vos documents de suivi à tout moment
- Révocation : applicable aux séances futures, pas aux séances passées dont l'audio a déjà été effacé

#### Durées de conservation sous Niveau 1

| Donnée | Durée |
|---|---|
| Audio brut | J+30 maximum (destruction automatique certifiée) |
| Transcription pseudonymisée | 90 jours après la séance |
| Documents validés (synthèse, compte rendu) | Durée du suivi actif + 5 ans (norme professionnelle) |

---

### II.3 Niveau 2 — Contribution au dataset structuré

#### Finalités

1. Les séances qualifiées (environ 40-50 % après pré-filtrage de pertinence) et anonymisées de vos séances peuvent être ajoutées au dataset structuré d'IVIA
2. Ce dataset sert à améliorer la compréhension collective des patterns d'accompagnement émotionnel
3. Les signaux extraits ne contiennent aucune information vous identifiant

#### Ce que cela permet concrètement

- Des signaux structurés (patrons émotionnels génériques, structure thématique, indicateurs de progression) extraits de votre séance anonymisée sont intégrés dans un corpus de recherche
- Ces signaux n'incluent aucun verbatim, aucun nom, aucun contexte personnel

#### Ce que cela ne signifie PAS

- Vos paroles ne sont pas « dans le dataset » — des métadonnées structurées et anonymisées en font partie
- Vous ne pouvez pas être réidentifié à partir du dataset

#### Droits associés

- Révocation à tout moment : vos séances sont retirées du dataset dans les 7 jours
- Exception : si des analyses agrégées ont déjà été produites avec vos données, elles ne peuvent pas être retirées des agrégats (qui, par construction, ne vous identifient pas)

#### Durée de conservation sous Niveau 2

| Donnée | Durée |
|---|---|
| Signaux anonymisés dans le dataset | 7 ans (valeur de recherche longitudinale) |

---

### II.4 Niveau 3 — Contribution au modèle propriétaire IVIA

#### Finalités

1. Les signaux anonymisés de vos séances qualifiées (environ 10 % après pré-filtrage de pertinence élevée) peuvent contribuer au fine-tuning du modèle propriétaire IVIA
2. Ce modèle apprend des patterns généraux de l'accompagnement émotionnel selon la doctrine IVIA
3. Il ne mémorise pas vos séances individuelles et ne peut pas les « restituer »

#### Ce que cela permet concrètement

- À terme (Palier 6 / M24+), IVIA pourra développer un modèle d'IA propriétaire formé sur des données réelles d'accompagnement émotionnel québécois, sans jamais avoir conservé de voix ou de transcriptions identifiables
- Ce modèle améliore la qualité des analyses et synthèses pour tous les clients futurs

#### Ce que cela ne signifie PAS

- Le modèle ne « sait pas » ce que vous avez dit dans vos séances — il a appris des patterns généraux
- Votre voix ou votre identité ne font pas partie du modèle

#### Droits associés

- Révocation à tout moment avant intégration dans un cycle d'entraînement
- Si un cycle d'entraînement est en cours au moment de la révocation, vous êtes notifié que la révocation prend effet au prochain cycle

---

## PARTIE III — MODALITÉS DE RECUEIL (UX)

### III.1 Principes UX du consentement IVIA

Le recueil du consentement respecte les principes suivants :

1. **Clarté avant accessibilité** : chaque niveau est expliqué en langage simple avant de demander un choix
2. **Séparation visuelle** : les 3 niveaux apparaissent séparément sur l'interface — pas de case unique « tout accepter »
3. **Pas de pré-cochage** : aucun niveau n'est coché par défaut. L'action par défaut est le refus.
4. **Aucune pression visuelle** : les boutons d'acceptation et de refus ont la même taille et le même poids visuel. Aucune formulation culpabilisante pour le refus.
5. **Accès permanent** : les paramètres de consentement sont accessibles à tout moment depuis l'espace client (section « Mes préférences »)
6. **Confirmation de révocation** : la révocation est confirmée par courriel dans les 24 heures suivant la demande

### III.2 Formulaire de consentement — Niveau 1

**Moment de recueil** : lors de l'inscription + avant chaque nouvelle séance si le paramètre a été modifié depuis la dernière séance.

**Formulation recommandée** :

```
ENREGISTREMENT ET PRODUCTION DOCUMENTAIRE

Pour vous offrir une synthèse de séance et des documents de suivi,
IVIA enregistre votre séance audio pendant son déroulement.

Voici ce qui se passe avec cet enregistrement :
- Il est conservé de façon sécurisée pendant 30 jours, puis détruit de façon irréversible
- Pendant ces 30 jours, il est utilisé pour produire votre transcription et vos documents
- Votre transcription est conservée 90 jours, sous forme pseudonymisée

Sans cet enregistrement : nous pouvons quand même avoir une séance,
mais vous n'aurez pas de documents de suivi MERLIN.

[OUI, J'ACCEPTE L'ENREGISTREMENT]    [NON, JE PRÉFÈRE SANS ENREGISTREMENT]
```

### III.3 Formulaire de consentement — Niveau 2

**Moment de recueil** : après la confirmation du Niveau 1, sur écran séparé.

**Formulation recommandée** :

```
CONTRIBUTION À LA RECHERCHE IVIA (OPTIONNEL)

IVIA travaille à mieux comprendre les patterns de l'accompagnement émotionnel.

Si vous le souhaitez, les signaux anonymisés de vos séances (pas vos paroles —
des métadonnées structurées dont on ne peut pas vous identifier) peuvent
contribuer à ce travail de recherche.

Ce choix est :
- Entièrement optionnel — votre service n'est pas affecté si vous refusez
- Révocable à tout moment depuis vos préférences
- Distinct de votre consentement au service (vous pouvez dire oui à l'un et non à l'autre)

[OUI, JE CONTRIBUE AU DATASET]    [NON MERCI]
```

### III.4 Formulaire de consentement — Niveau 3

**Moment de recueil** : après la confirmation du Niveau 2 (ou du refus du Niveau 2), sur écran séparé.

**Formulation recommandée** :

```
CONTRIBUTION AU MODÈLE IA IVIA (OPTIONNEL — PLUS RESTRICTIF)

IVIA développe un modèle d'intelligence artificielle propriétaire
pour améliorer la qualité des analyses et synthèses.

Si vous le souhaitez, les signaux anonymisés de vos séances les plus riches
(environ 10 % de vos séances, après sélection automatique) peuvent contribuer
à l'entraînement de ce modèle.

Ce que ce modèle ne pourra jamais faire : retrouver ce que vous avez dit,
vous identifier, ou révéler vos séances individuelles. Il apprend des patterns
généraux — pas des histoires personnelles.

Ce choix est :
- Entièrement optionnel
- Révocable avant intégration dans un cycle d'entraînement
- Applicable uniquement si vous avez aussi accepté le Niveau 2

[OUI, JE CONTRIBUE AU MODÈLE IA]    [NON MERCI]
```

---

## PARTIE IV — MODALITÉS DE RÉVOCATION

### IV.1 Interface de révocation

Toute révocation de consentement est possible depuis l'espace client IVIA, section « Mes préférences » > « Mes consentements ». L'interface présente l'état actuel de chaque niveau et permet une modification individuelle par niveau.

### IV.2 Effets de chaque révocation

| Niveau révoqué | Effet immédiat | Effet sur les données existantes |
|---|---|---|
| Niveau 1 | Aucun enregistrement pour les séances futures. Certaines fonctionnalités documentaires deviennent indisponibles. | Les audios passés ont déjà été détruits à J+30. Les transcriptions passées sont conservées jusqu'à leur échéance normale (90 jours). |
| Niveau 2 | Vos séances cessent d'alimenter le dataset pour les séances futures. | Vos séances sont retirées du dataset dans les 7 jours. Les analyses agrégées déjà produites ne peuvent pas être retirées des agrégats. |
| Niveau 3 | Vos séances cessent de contribuer au cycle d'entraînement pour les séances futures. | Si un cycle d'entraînement est en cours : notification que la révocation prend effet au prochain cycle. |

### IV.3 Confirmation de révocation

Toute révocation déclenche un courriel de confirmation dans les 24 heures, indiquant : le niveau révoqué, la date d'effet, les conséquences pratiques.

### IV.4 Révocation intégrale (droit à l'effacement)

La révocation de tous les consentements simultanément à la fermeture du compte entraîne la suppression complète des données selon les délais définis dans la Politique de confidentialité. Cette procédure est décrite dans la section « Fermer mon compte » de l'espace client.

---

## PARTIE V — CAS PARTICULIERS

### V.1 Mineurs (14-17 ans)

**Niveau 1** : le ou la mineur(e) de 14 ans et plus peut consentir lui-même / elle-même. Un formulaire adapté confirme que la personne comprend les enjeux.

**Niveaux 2 et 3** : un consentement parental ou tutoral est requis en sus du consentement du ou de la mineur(e). La procédure de collecte du consentement parental est la suivante :
1. Le ou la mineur(e) indique vouloir contribuer (Niveau 2 ou 3)
2. IVIA envoie un courriel de confirmation à l'adresse parental enregistrée
3. Le parent ou tuteur confirme son accord dans les 72 heures
4. Le consentement prend effet dès confirmation parentale

Si le parent ou tuteur n'a pas confirmé dans les 72 heures, la contribution est refusée par défaut.

### V.2 Détresse aiguë (consentement présumé pour signalement d'urgence)

Dans une situation de danger imminent pour la vie (Article 3.3 des CGU Clients), le praticien peut agir sans recueillir un consentement explicite. Ce consentement est présumé dans le cadre légal de la protection de la vie.

Cette situation est documentée selon le Protocole d'urgence (`PROTOCOLE_URGENCE_DETRESSE.md`) et ne constitue pas une violation du présent protocole de consentement.

### V.3 Doute sur la capacité de consentement

Si le praticien a des raisons de douter de la capacité d'une personne à donner un consentement éclairé (par exemple, état de détresse sévère au moment de l'inscription), la procédure est :
1. Ne pas recueillir les consentements Niveaux 2 et 3 dans ce moment
2. Reporter la demande de consentements optionnels à un moment plus approprié
3. Documenter l'observation dans les notes internes (sans détail clinique)
4. En cas de doute persistant, en référer à la direction IVIA

---

## PARTIE VI — DOCUMENTATION DES CONSENTEMENTS

### VI.1 Journal des consentements

IVIA maintient un journal infalsifiable de tous les consentements et révocations, contenant :
- L'identifiant pseudonymisé du client
- La date et l'heure du consentement ou de la révocation
- Le niveau concerné (1, 2 ou 3)
- La version des formulaires en vigueur au moment du consentement
- L'adresse IP enregistrée (pour preuve d'authenticité — non conservée au-delà de 90 jours pour les besoins de sécurité)

Ce journal constitue la preuve juridique de conformité IVIA en matière de consentement. Il est conservé pendant la durée de conservation des données concernées + 5 ans.

### VI.2 Audit des consentements

L'état des consentements (taux par niveau, révocations, anomalies) fait l'objet d'un rapport mensuel interne et d'un rapport annuel public dans le cadre de l'audit doctrinaire.

---

## PARTIE VII — RENOUVELLEMENT PÉRIODIQUE

### VII.1 Fréquence

Les consentements de Niveaux 2 et 3 sont renouvelés tous les 24 mois. IVIA notifie le client 30 jours avant l'échéance.

### VII.2 Procédure de renouvellement

1. Notification par courriel et dans l'espace client : « Vos préférences de contribution arrivent à échéance »
2. Le client est invité à confirmer ou modifier ses choix
3. Si aucune action n'est prise dans les 30 jours suivant la notification, les Niveaux 2 et 3 sont réinitialisés à « Non » par défaut (opt-in non renouvelé = retrait du consentement)
4. Le Niveau 1 n'a pas de date d'expiration — il s'applique aux séances futures jusqu'à révocation active

### VII.3 Modifications des finalités

Si IVIA souhaite modifier les finalités couvertes par un niveau de consentement (ex. : ajouter une nouvelle utilisation du dataset), un nouveau consentement explicite est requis. Il ne peut pas être présumé à partir d'un consentement antérieur.

---

## MODÈLES DE FORMULAIRES

### Modèle 1 — Consentement initial (tous niveaux — première inscription)

Version courte adaptée au flux d'inscription. À compléter sur l'interface client.

```
VDANS MON ESPACE IVIA — MES PRÉFÉRENCES DE DONNÉES

Pour accéder à IVIA, vous devez choisir vos préférences ci-dessous.
Les choix marqués [OPTIONNEL] n'affectent pas votre accès au service.

---

1. ENREGISTREMENT DE SÉANCE [REQUIS POUR LES DOCUMENTS]

Pour produire vos documents de suivi, IVIA enregistre votre séance.
L'enregistrement est détruit dans les 30 jours. Transcription conservée 90 jours.

○ Je consens à l'enregistrement et à la production documentaire
○ Je préfère une séance sans enregistrement (sans documents MERLIN)

---

2. CONTRIBUTION À LA RECHERCHE [OPTIONNEL]

Des signaux anonymisés de vos séances peuvent enrichir le dataset de recherche IVIA.
Vous ne pouvez pas être identifié dans ces données.

○ Je contribue au dataset (révocable à tout moment)
○ Je ne contribue pas

---

3. CONTRIBUTION AU MODÈLE IA [OPTIONNEL]

Des signaux anonymisés de vos meilleures séances (~10%) peuvent contribuer
à l'entraînement du modèle IA propriétaire IVIA.

○ Je contribue au modèle IA (révocable avant intégration)
○ Je ne contribue pas

---

[CONFIRMER MES PRÉFÉRENCES]

Vous pouvez modifier vos préférences à tout moment dans votre espace client.
```

---

## RÉFÉRENCES DOCUMENTAIRES

- `CHARTE_TRANSFORMATION_GOUVERNEE_DONNEES.md` — Pipeline technique détaillé
- `POLITIQUE_CONFIDENTIALITE_LOI25.md` (Vague 1) — Politique complète
- `CGU_CLIENTS.md` (Vague 2) — Article 8
- `CGU_PRATICIENS.md` (Vague 2) — Article 8 (opt-in praticien)
- `GOUVERNANCE_INTERNE_IVIA.md` (Vague 2) — Reporting transparence

---

**Au sein de l'être — En actes.**

*Version 1.0 — Vague 2 — Mai 2026*
*David Phaneuf, RPRP, MERLIN inc.*
*privacy@ivia.quebec*

# CHARTE DE TRANSFORMATION GOUVERNÉE DES DONNÉES IVIA
## Engagement public sur le pipeline de transformation des données de séance

**Version** : 1.0 — Vague 1
**Date** : Mai 2026
**Statut** : Document public — Opposable aux partenaires, praticiens, clients et investisseurs
**Auteur** : David Phaneuf (fondateur) + Perplexity Computer
**Mise à jour prévue** : v2.0 lors de l'activation de la synthèse vocale (Palier 4 / M13)

---

## PRÉAMBULE ÉTHIQUE

### Le paradoxe des données de séance

Une séance d'accompagnement produit de la parole. Cette parole est à la fois la matière première de l'accompagnement ET une donnée d'une sensibilité extrême. Elle contient le vécu intime d'une personne, sa voix, ses silences, ses vulnérabilités nommées.

Si IVIA voulait simplement maximiser la valeur commerciale de cette parole, elle la conserverait, la commercialiserait, l'exploiterait sans limites. C'est ce que font la majorité des acteurs de la santé numérique. C'est précisément ce qu'IVIA refuse.

Si IVIA voulait simplement protéger la confidentialité absolue, elle ne traiterait aucune donnée au-delà du strict nécessaire à la séance. Ce serait cohérent — mais cela priverait IVIA, ses praticiens et la recherche sur l'accompagnement émotionnel d'un actif unique : un corpus structuré de pratiques d'écoute, capable d'alimenter un modèle propriétaire qui améliore la qualité de l'accompagnement pour toutes les personnes futures.

La présente Charte résout ce paradoxe par le principe de **transformation gouvernée** : les données de séance ne sont jamais conservées brutes au-delà du strict nécessaire. Elles sont transformées — par étapes explicites, avec consentements granulaires — en actifs qui ne permettent plus l'identification des personnes, mais qui portent la valeur collective de l'expérience accumulée.

### Ce que cette Charte garantit

1. Aucune voix identifiable conservée au-delà de la certification de la transcription par le praticien (max J+7), avec **effacement immédiat** post-certification ; à défaut de certification dans les 7 jours, effacement automatique et exclusion de la séance du dataset
2. À partir du Palier 4 (M13), l'audio est transformé après certification (voice conversion pseudonymisante) puis conservé 90 jours sous forme dégradée non directement identifiable, avant destruction complète
3. Aucune donnée personnelle brute cédée à un tiers, jamais, sous aucune condition commerciale
4. Chaque étape de transformation est documentée, auditée et réversible pour le client (dans la mesure des limites techniques explicitées)
5. Le consentement est granulaire : trois niveaux distincts, chacun révocable indépendamment
6. Le dataset synthétique produit en fin de pipeline ne contient aucune information personnelle identifiable
7. Aucun accès humain unilatéral : tout accès à l'audio identifiable est journalisé cryptographiquement et borné par rôle (SUPER ADMIN technique sans contenu / PRATICIEN contenu pour certification)

---

## PARTIE 0 — GOUVERNANCE DES DONNÉES

### 0.1 Responsable de la Protection des Renseignements Personnels (RPRP)

Conformément à l'article 3.1 de la Loi 25, IVIA désigne formellement un Responsable de la Protection des Renseignements Personnels (RPRP).

**Modèle de gouvernance dual adopté** :

| Rôle | Titulaire | Mandat |
|---|---|---|
| **RPRP opérationnel** | David Phaneuf, fondateur (en P1, M1-M7) puis profil dédié à partir du Palier 3 | Reçoit et traite les demandes Loi 25 (accès, rectification, suppression, opposition, portabilité, révocation), supervise les EFVP, valide les procédures dual control d'accès contenu, publie le rapport annuel de transparence |
| **Superviseur RPRP externe** | Consultant indépendant en protection des données — désigné dès M1 | Validation trimestrielle des pratiques RPRP, contre-pouvoir au RPRP opérationnel, signataire du rapport annuel public, alerte directe à la CAI en cas de manquement grave |

**Justification du modèle dual** : la Loi 25 permet au dirigeant d'assurer le rôle RPRP dans les petites structures. Cette permission n'équivaut pas à une bonne pratique — elle crée un conflit d'intérêt structurel (le dirigeant supervise sa propre conformité). IVIA résout ce conflit en M1 par la désignation immédiate d'un superviseur indépendant qui contre-signe les pratiques. Cette architecture préfigure la transition vers un RPRP pleinement indépendant en M7.

**Coordonnées publiques** : `privacy@ivia.quebec` (courriel chiffré, accusé de réception sous 72h ouvrables).

**Indépendance opérationnelle (à partir du Palier 3 / M7)** : le RPRP ne peut être démis ou sanctionné que par décision motivée du Comité doctrinal. Il dispose d'une ligne directe de saisine vers la Commission d'accès à l'information du Québec en cas de manquement non résolu en interne.

### 0.2 Comité doctrinal et données

Le Comité doctrinal (institué par la Charte doctrinaire) est saisi obligatoirement pour :
- Toute mise à jour majeure de la présente Charte
- Toute exception documentée à un engagement (effacement, durée, accès)
- Toute escalade d'incident classé grave
- Toute revue d'opportunité d'évolution du seuil k-anonymity (Partie II, Étape 7)

Les décisions du Comité sont publiées dans le rapport annuel de transparence (Partie VI).

---

## PARTIE I — DÉFINITIONS JURIDIQUES

### 1.1 Définitions selon la Loi 25 (Québec)

**Renseignement personnel** (Loi sur la protection des renseignements personnels dans le secteur privé, LPP) : "tout renseignement qui concerne une personne physique et permet de l'identifier". La Loi 25 (adoptée 2021, phases d'entrée en vigueur 2022-2023) renforce significativement les obligations des entreprises québécoises.

**Renseignement sensible** : catégorie implicite dans la Loi 25 et explicite dans le RGPD — tout renseignement dont la divulgation cause un préjudice sérieux. Les données de santé, données biométriques et données psychologiques sont sensibles par nature.

**Consentement** (Loi 25) : manifestation claire de volonté, libre, éclairée, granulaire et révocable. Le consentement implicite ou par défaut est insuffisant pour les données sensibles.

**Évaluation des facteurs relatifs à la vie privée (EFVP)** : obligation légale (Loi 25, art. 3.3) pour tout projet impliquant des renseignements personnels comportant un risque élevé. La collecte de données de séances d'accompagnement déclenche cette obligation.

### 1.2 Définitions selon le RGPD (Règlement général sur la protection des données — UE)

Pour les praticiens ou clients résidant dans l'UE ou les échanges avec des partenaires européens, le RGPD s'applique en parallèle :

**Données à caractère personnel** : "toute information se rapportant à une personne physique identifiée ou identifiable" (art. 4, RGPD).

**Données biométriques** (art. 9, RGPD) : "données à caractère personnel résultant d'un traitement technique spécifique, relatives aux caractéristiques physiques, physiologiques ou comportementales d'une personne physique, qui permettent ou confirment son identification unique" — la voix humaine est une donnée biométrique.

**Pseudonymisation** : traitement consistant à remplacer les données directement identifiantes par des pseudonymes. La donnée reste personnelle au sens juridique (réidentification possible avec la clé).

**Anonymisation** : traitement irréversible rendant impossible toute réidentification. Une donnée anonymisée n'est plus soumise au droit à la protection des données personnelles.

### 1.3 Catégories appliquées au pipeline IVIA

| Catégorie | Description | Exemples IVIA | Régime juridique |
|---|---|---|---|
| Données identifiantes | Permettent l'identification directe | Nom, courriel, numéro de téléphone | Loi 25 + RGPD — collecte minimale |
| Données biométriques | Empreinte corporelle unique | Voix enregistrée, patterns spectraux | Loi 25 art. 14 + RGPD art. 9 — consentement explicite obligatoire |
| Données conversationnelles | Contenu des échanges | Transcription brute, résumé de séance | Loi 25 — données sensibles |
| Données pseudonymisées | ID de séance sans nom | Séance_2026_XXXX + transcription | Loi 25 — protégées |
| Données anonymisées | Irréidentifiables | Signaux structurés sans contexte personnel | Hors Loi 25 — utilisables librement |
| Données synthétiques | Générées par IA, non issues d'un individu réel | Cas synthétiques du dataset IVIA | Hors Loi 25 — actif valorisable |

---

## PARTIE II — LE PIPELINE IVIA EN 8 ÉTAPES

Le pipeline de transformation gouvernée des données est le cœur technique et éthique d'IVIA. Il transforme la parole vive d'une séance en actifs utilisables sans compromettre la vie privée des personnes.

```
ÉTAPE 0       ÉTAPE 1       ÉTAPE 2       ÉTAPE 3
Consentement  Séance audio  Enregistrement Pré-filtrage
granulaire    en direct     brut (J+0)    pertinence
    │              │              │             │
    ▼              ▼              ▼             ▼
Niveau 1:      Audio chiffré  Conservation   Qualification
usage service  J+0 → J+cert  temporaire     niveau 1/2/3
Niveau 2:      (identifiable) chiffrée       (~10% qualifié
dataset        max J+7        + accès        niveau 3)
Niveau 3:                     dual journalisé
modèle

ÉTAPE 4         ÉTAPE 4bis      ÉTAPE 5       ÉTAPE 6        ÉTAPE 7       ÉTAPE 8
Transcription   Certification   Extraction    Clôture        Synthétisation Fine-tuning
& pseudonymi-   praticien       signaux       biométrique    IA (cas        modèle
sation          (max J+7)       structurés    (post-cert)    synthétiques)  propriétaire
    │                │              │             │                │              │
    ▼                ▼              ▼             ▼                ▼              ▼
Texte pseudo-  Validation      Patron émot.  M1-M12 :       Dataset        Modèle IVIA
nymisé         qualité          anonymisé     audio supprimé synthétique    opérationnel
→ 90 jours    transcription    → 7 ans       immédiatement  propriétaire   (Phase 3)
               (24-72h cible)                 M13+ : voice
                                                conversion
                                                + 90 jours
```

**Clause de maturité graduelle** : la transformation vocale (Étape 6 "version M13+") nécessite une technologie de voice conversion robuste qui n'est pas déployée en M1. **Pendant la phase pilote (M1-M12)**, l'audio brut est effacé immédiatement après certification, sans transformation intermédiaire conservée. **À partir du Palier 4 (M13)**, le mécanisme complet entre en service avec audio transformé conservé 90 jours.

### Étape 0 — Consentement granulaire à 3 niveaux

**Avant toute séance**, le client donne son consentement selon trois niveaux distincts, chacun indépendant et révocable :

**Niveau 1 — Consentement au service** (obligatoire)
- Autorisation de l'enregistrement audio pendant la séance
- Autorisation de la transcription automatique pour production documentaire interne
- **Accès humain borné par rôle et dans le temps** :
  - Le **praticien** peut réécouter l'audio identifiable jusqu'à certification de la transcription, dans une fenêtre maximale de 7 jours après la séance
  - Le **SUPER ADMIN** (fondateur en P1, équipe technique désignée ensuite) peut accéder **uniquement aux logs et métadonnées techniques** — jamais au contenu — et seulement pour incident technique documenté. Tout accès est journalisé cryptographiquement.
- **Conservation audio identifiable** :
  - **M1-M12 (pilote, P1-P3)** : audio identifiable supprimé immédiatement après certification praticien (max J+7). Pas de version transformée conservée.
  - **M13+ (Palier 4 et au-delà)** : audio identifiable supprimé immédiatement après certification ; une **version vocalement transformée** (voice conversion pseudonymisante, voir Étape 6) est conservée 90 jours puis détruite.
- Si la transcription n'est pas certifiée dans les 7 jours : l'audio identifiable est effacé automatiquement, la séance est marquée "non certifiée" et exclue du dataset (Niveaux 2 et 3).
- Durée de conservation transcription pseudonymisée : 90 jours après séance
- Sans ce consentement : aucun service IVIA possible

**Niveau 2 — Contribution au dataset** (optionnel, révocable)
- La séance, une fois anonymisée selon l'Étape 4, peut contribuer à l'enrichissement du dataset structuré
- Le client ne peut pas être réidentifié dans ce dataset
- Révocable à tout moment — les séances concernées sont retirées du dataset

**Niveau 3 — Contribution à la formation du modèle propriétaire** (optionnel, révocable avant intégration)
- Les signaux anonymisés de la séance peuvent alimenter le fine-tuning du modèle propriétaire IVIA
- Applicable uniquement si la séance a passé le pré-filtrage de pertinence (Étape 3)
- **Révocabilité — limite technique reconnue** : la contribution au fine-tuning devient irréversible une fois le cycle d'entraînement complété. Les signaux sont alors dilués dans les poids du modèle, sans possibilité d'extraction ou de désapprentissage individuel.
- **Engagement IVIA — fenêtre de révocation** : les cycles de fine-tuning sont planifiés à intervalles définis (90 jours minimum entre cycles). Chaque client dont les signaux sont candidats à un cycle reçoit une **notification 30 jours avant** le démarrage du cycle, lui permettant de révoquer en amont.
- Après intégration : les signaux ont contribué au modèle global mais ne sont plus ni identifiables ni extractibles individuellement. La révocation post-intégration empêche toute future utilisation des séances ultérieures du client mais n'efface pas les apprentissages déjà incorporés.
- Cette limite technique est explicitée dans l'interface de consentement, dans un langage clair et sans euphémisme.

**Interface consentement** : formulaire numérique avec cases à cocher individuelles. Aucun consentement global. Langage simple, sans jargon juridique. Accessible à tout moment depuis l'espace client.

### Étape 1 — Séance audio en direct

La séance se déroule sur la plateforme MERLIN en mode audio-only. Le canal est **chiffré en transit** (TLS 1.3) et les données sont **chiffrées au repos** (AES-256). L'enregistrement, si consenti au Niveau 1, démarre uniquement après confirmation explicite du praticien dans l'interface.

**Posture sur le chiffrement de bout en bout (E2EE)** : IVIA n'adopte volontairement pas de E2EE strict. La mission d'accompagnement requiert un traitement serveur (transcription, certification praticien, extraction de signaux structurés) qui rend techniquement incompatible un cadre où seuls les utilisateurs finaux peuvent déchiffrer. Plutôt que de revendiquer une protection technique inadaptée au service réel, IVIA construit un **cadre de confiance vérifiable** qui compense l'absence de E2EE par :
1. Accès humain dual journalisé cryptographiquement (Étape 2)
2. Effacement immédiat de l'audio identifiable post-certification (Étape 6)
3. Hébergement souverain sur infrastructure canadienne (OVH Canada)
4. Audit annuel public (Partie VI)
5. Architecture cryptographique détaillée (Partie VIII)

Le détail technique de chaque couche de chiffrement est documenté en Partie VIII.

**Données collectées à cette étape** :
- Audio brut côté serveur (voix identifiables — données biométriques)
- Métadonnées de séance : date, durée, ID praticien, ID client (pseudonyme)
- Données de connexion : IP, navigateur (journalisation sécurité)

### Étape 2 — Enregistrement brut (J+0 → J+certification, max J+7)

Dès la fin de la séance, l'audio brut est :
- Chiffré avec clé AES-256 au repos
- Stocké dans un compartiment isolé (bucket OVH Canada dédié, accès restreint)
- Marqué avec date d'effacement conditionnelle : J+certification (au plus tard J+7)

L'audio brut à ce stade est une donnée biométrique identifiable, soumise au régime le plus strict (Loi 25 art. 14, RGPD art. 9).

**Régime d'accès humain (gouvernance dual)** :

| Rôle | Portée d'accès | Finalité unique autorisée | Journalisation |
|---|---|---|---|
| Praticien (auteur de la séance) | Audio + transcription | Certification de la transcription (fact-checking qualité) | Cryptographique — qui, quand, durée d'écoute, segments lus |
| SUPER ADMIN (fondateur en P1) | Logs, métadonnées, statut technique — **jamais le contenu audio ni le contenu transcrit** | Investigation incident technique avec justification écrite | Cryptographique + notification automatique au RPRP à chaque accès |
| Tout autre rôle | Aucun accès | — | — |

**Garde-fous structurels** :
- Aucun accès au contenu audio par le SUPER ADMIN, même pour incident technique. Si une investigation requiert un accès contenu, elle requiert une **procédure dual control** : SUPER ADMIN + un second valideur (RPRP à partir du Palier 3, auditeur externe en cas d'absence).
- Logs chaînés cryptographiquement (hash chain immuable).
- Rapport mensuel des accès publié dans le rapport annuel de transparence (Partie VI).
- En cas d'accès contenu jugé illégitime après revue : escalade au Comité doctrinal et signalement à la CAI si pertinent.

### Étape 3 — Pré-filtrage de pertinence (Axe 1.5)

**Objectif** : qualifier les séances selon leur pertinence pour l'enrichissement du dataset. Critère central : est-ce que la séance illustre des patterns d'accompagnement émotionnel représentatifs et riches pour l'entraînement du modèle ?

**Trois niveaux de qualification** :

| Niveau | Description | % estimé | Statut dataset |
|---|---|---|---|
| Niveau 1 | Séance courte, technique, sans profondeur émotionnelle | ~50 % | Exclu du dataset |
| Niveau 2 | Séance standard, patterns présents mais non distinctifs | ~40 % | Inclus dataset agrégé uniquement |
| Niveau 3 | Séance riche, patterns émotionnels distinctifs, haute valeur | ~10 % | Inclus dataset formation modèle |

**Méthode** : analyse automatisée de la durée, des transitions émotionnelles, de la densité thématique — sans analyse du contenu identifiable. Le filtrage ne nécessite pas de lire la transcription.

Le praticien peut, à tout moment, désigner une séance comme "non pertinente" pour la retirer du pipeline, même si elle avait passé le filtre automatique.

**Sort des séances qualifiées Niveau 1** : ces séances (~50 % du volume) suivent le cycle standard de conservation (audio identifiable supprimé après certification praticien, transcription pseudonymisée 90 jours pour le suivi praticien). Elles sont simplement **exclues** du pipeline d'enrichissement dataset/modèle (Étapes 5, 7, 8). Cette exclusion n'a aucun impact sur la qualité du service rendu au client — le suivi praticien et la production documentaire demeurent identiques.

### Étape 4 — Transcription et pseudonymisation

Pour les séances ayant le consentement Niveau 1 et la transcription activée :

**Transcription automatique** : via Deepgram (Nova-3, Growth) en français québécois. Résultat : texte brut pseudonymisé (noms remplacés par ID, numéros de téléphone masqués, adresses supprimées).

**Pseudonymisation** : remplacement de tous les identifiants directs par des tokens non réidentifiables (sauf avec la table de correspondance chiffrée, accessible uniquement par le praticien et via procédure formelle).

**Durée de conservation** :
- Transcription pseudonymisée : 90 jours après la séance
- Après 90 jours : destruction automatique (sauf si la transcription fait partie du dossier suivi praticien, auquel cas : voir politique de conservation dossier praticien)

### Étape 4bis — Certification de la transcription par le praticien (NOUVELLE étape)

La transcription automatique de Deepgram, même de qualité élevée, peut comporter des erreurs (mots mal transcrits, locuteurs confondus, segments inaudibles). Sans vérification humaine, ces erreurs se propagent dans le pipeline et compromettent la qualité doctrinale du dataset à la racine.

**La certification est l'engagement du praticien sur la qualité de la transcription**, conduite dans une fenêtre maximale de 7 jours après la séance.

**Opérations autorisées au praticien pendant la fenêtre de certification** :
- Réécouter tout ou partie de l'audio identifiable
- Comparer avec la transcription automatique
- Corriger les segments erronés
- Signaler les segments inaudibles ou contestés
- Désigner une séance comme "non pertinente" pour la retirer du pipeline (équivalent du droit de retrait Étape 3)
- Valider et signer la transcription cryptographiquement (signature praticien + horodatage)

**Cible opérationnelle** : 24-72h après la séance dans la majorité des cas. **Plafond non dérogeable** : 7 jours.

**À J+7 sans certification** :
- Effacement automatique de l'audio identifiable
- Transcription marquée "non certifiée"
- Séance **exclue automatiquement** du dataset (Niveaux 2 et 3) — même si le client avait consenti
- Notification au praticien et au RPRP
- Comptabilisé dans le rapport annuel de transparence

**Exception unique** : congé médical documenté du praticien. Dans ce cas, la fenêtre peut être prolongée jusqu'au retour, plafonnée à 30 jours total, avec validation par le RPRP. Au-delà de 30 jours : effacement et exclusion.

### Étape 5 — Extraction de signaux structurés (Axe 2)

Pour les séances qualifiées Niveau 2 ou 3 ayant le consentement Niveau 2 :

**Extraction** : l'IA (GPT-4.1-mini ou équivalent) extrait des signaux structurés à partir de la transcription pseudonymisée :
- Patrons émotionnels récurrents (catégories génériques : anxiété, deuil, transition, conflit relationnel...)
- Structure thématique (quels axes la séance a exploré)
- Indicateurs de progression (présence/absence de certains marqueurs d'évolution)

**Ces signaux sont anonymisés** : ils ne contiennent pas de contenu verbatim de la séance, pas de noms, pas de contexte personnel. Ils sont des métadonnées structurées sur le pattern de la séance.

**Durée de conservation** : 7 ans, avec finalité explicite et mécanisme de revue.

**Finalités justifiant la conservation 7 ans** :
(a) Recherche longitudinale sur l'évolution des patterns d'accompagnement émotionnel (collaborations universitaires futures dans un cadre éthique formalisé)
(b) Constitution de la base d'entraînement du modèle propriétaire IVIA (Phase 3, M24+)
(c) Audit longitudinal de la qualité doctrinale et de la dérive éventuelle des pratiques

**Revue obligatoire à 3 ans** par le Comité doctrinal : si les finalités (a) et (c) ne sont plus actives ou jugées légitimes, la durée est ramenée à la durée résiduelle strictement nécessaire à (b). À 7 ans : destruction automatique des signaux avec rapport public dans le rapport annuel de transparence.

### Étape 6 — Clôture biométrique (post-certification)

Dès que la certification praticien (Étape 4bis) est complétée, le processus de clôture biométrique se déclenche automatiquement.

#### Étape 6.A — Période pilote M1-M12 (P1-P3)

L'audio identifiable est détruit immédiatement après certification :
- Suppression du fichier audio chiffré
- Overwrite sécurisé (DoD 5220.22-M ou équivalent)
- Journalisation de la destruction (log conservé 7 ans)
- Notification au praticien et au RPRP concernés

Aucune version transformée n'est conservée pendant cette période. La technologie de voice conversion robuste n'étant pas suffisamment mature pour garantir une réduction significative du risque de réidentification, IVIA préfère la destruction complète à une transformation imparfaite.

#### Étape 6.B — À partir du Palier 4 (M13+)

Après certification, l'audio identifiable est :
1. **Traité par le module de voice conversion pseudonymisante** (voir spécification technique sous-jacente) :
   - Remplacement du timbre vocal par une voix-cible neutre
   - Perturbation prosodique calibrée (jitter contrôlé sur les pauses, lissage du débit)
   - Préservation du contenu, des transitions émotionnelles, de la structure thymique
2. **Détruit dans sa version identifiable** immédiatement après production de la version transformée
3. **La version transformée** est conservée dans un compartiment dédié, chiffrée AES-256, pendant **90 jours maximum**, puis détruite irréversiblement

**Statut juridique de la version transformée** : IVIA traite cette version comme une **donnée pseudonymisée** au sens de la Loi 25 et du RGPD — **pas comme une donnée anonymisée**. Bien que la transformation réduise très significativement le risque de réidentification, IVIA ne prétend pas que ce risque soit nul. La version transformée reste donc soumise à toutes les protections Loi 25 (consentement, droits clients, gouvernance d'accès).

**Engagement de transparence scientifique** : avant l'activation du module en M13, IVIA publiera un rapport technique décrivant la méthode de voice conversion retenue, les métriques de réduction du risque de réidentification (taux de réidentification mesuré sur jeu de test), et les limites connues. Ce rapport sera audité par un tiers indépendant avant mise en production.

#### Disposition commune aux deux périodes

**Le processus de destruction de l'audio identifiable est non-réversible.** Aucune dérogation commerciale, juridique ou technique ne peut reporter l'effacement au-delà des délais définis (post-certification, ou J+7 sans certification, ou J+30 congé médical documenté).

**Exception unique** : procédure légale de conservation probatoire ordonnée par un tribunal. Dans ce cas :
- La conservation est strictement limitée à l'usage juridique
- Le client est informé de la conservation prolongée, sauf interdiction judiciaire explicite (mandat de non-divulgation)
- L'événement est documenté dans le rapport annuel de transparence (volume agrégé, sans détails identifiants)

### Étape 7 — Synthétisation IA (Axe 3 — cas synthétiques)

Pour les séances qualifiées Niveau 3 ayant le consentement Niveau 3 (Palier 5 / M19+) :

**Synthétisation** : à partir des signaux anonymisés de **minimum 10 séances** présentant des patterns similaires (seuil k-anonymity ≥ 10), le pipeline génère des cas synthétiques — des séances fictives représentatives des patterns émotionnels observés, sans lien avec aucune personne réelle.

**Justification du seuil k=10** : ce seuil rend mathématiquement improbable la réidentification d'un cas synthétique à partir des caractéristiques rares d'une séance source. Si un pattern émotionnel rare ne réunit pas 10 séances candidates, il n'est **pas synthétisé** — il est mis en attente jusqu'à atteindre le seuil ou exclu définitivement après 24 mois sans atteinte. Le seuil est révisé annuellement par le Comité doctrinal à la lumière de l'état de la recherche en réidentification, et le seuil retenu est publié dans le rapport annuel de transparence.

**Ce que le cas synthétique contient** :
- Une transcription fictive représentant un pattern d'accompagnement
- Des métadonnées de structure (durée fictive, progression fictive)
- Aucune information personnelle réelle

**Ce que le cas synthétique ne contient pas** :
- Aucun verbatim de séance réelle
- Aucune donnée permettant de relier le cas à un client ou praticien réel
- Aucune information biométrique

**Le dataset synthétique** résultant est propriétaire IVIA, valorisable, cédable — sans jamais toucher à la vie privée de qui que ce soit.

### Étape 8 — Fine-tuning du modèle propriétaire (Phase 3 — M24+)

À partir du dataset synthétique constitué lors de l'Étape 7, le fine-tuning d'un modèle open-source (Llama, Mistral, Qwen) est réalisé en infrastructure propre IVIA.

**Ce processus utilise exclusivement le dataset synthétique.** Aucune donnée personnelle réelle n'est utilisée dans l'entraînement.

**Le modèle propriétaire IVIA** ne contient aucune mémoire des séances individuelles. Il a appris des patterns généraux de l'accompagnement émotionnel selon la doctrine IVIA — il ne peut pas "retrouver" une séance spécifique.

---

## PARTIE III — DROITS DES CLIENTS

### 3.1 Droits garantis à tout moment

**Droit d'accès** : tout client peut demander la liste complète des données le concernant stockées par IVIA, dans un format lisible, sous 30 jours.

**Droit de rectification** : toute inexactitude dans les données (nom, coordonnées, métadonnées de séance) est corrigée sur demande sous 15 jours.

**Droit à la suppression** : le client peut demander la suppression de toutes ses données à tout moment. La suppression est complète et documentée. Elle ne peut pas être refusée sauf obligation légale spécifique (procédure judiciaire en cours, obligation fiscale de conservation).

**Droit d'opposition** : le client peut s'opposer au traitement de ses données pour tout usage non-essentiel au service (dataset, modèle) — ce qui équivaut à une révocation des consentements Niveaux 2 et 3.

**Droit à la portabilité** : les données du client (transcriptions, synthèses, documents de suivi) lui sont transmises dans un format standard (PDF, JSON) sur demande.

**Droit d'information sur les conservations exceptionnelles** : si une donnée du client fait l'objet d'une conservation prolongée par décision judiciaire (Étape 6, exception probatoire), le client est informé sans délai, **sauf interdiction judiciaire explicite** (mandat de non-divulgation). Dès la levée de l'interdiction, le client est notifié rétroactivement.

**Droit de révocation du consentement** : tout consentement (Niveaux 1, 2, 3) est révocable à tout moment. La révocation du Niveau 2 ou 3 n'affecte pas l'accès au service. La révocation du Niveau 1 implique l'arrêt de l'enregistrement pour les séances futures.

### 3.2 Délais de traitement

| Demande | Délai maximum |
|---|---|
| Accès aux données | 30 jours |
| Rectification | 15 jours |
| Suppression | 72 heures ouvrables (données brutes) / 30 jours (rapports et purges complètes) |
| Révocation consentement Niveau 1 | Immédiat (arrêt enregistrement séances futures) |
| Révocation consentement Niveau 2 (dataset) | 7 jours (retrait des séances du dataset structuré) |
| Révocation consentement Niveau 3 (modèle) — **avant** cycle fine-tuning | Immédiat (séances retirées des candidats au cycle) |
| Révocation consentement Niveau 3 (modèle) — **après** intégration | Limite technique reconnue : pas d'extraction du modèle. Effet : aucune future séance du client utilisée pour le modèle |
| Portabilité | 30 jours |

### 3.3 Contact et recours

Pour exercer ses droits : privacy@ivia.quebec (courriel chiffré)
Pour les plaintes non résolues : Commission d'accès à l'information du Québec (CAI)

---

## PARTIE IV — DROITS DES PRATICIENS

### 4.1 Droits relatifs à leurs séances

**Droit de désignation "non pertinente"** : le praticien peut, pour toute séance qu'il a conduite, retirer cette séance du pipeline au-delà de l'Étape 3 (pré-filtrage). Cette décision est exercée depuis son tableau de bord.

**Droit d'opt-in à la formation** : la contribution au dataset de formation (Étapes 7 et 8) est un opt-in du praticien, indépendant du consentement du client. Les deux consentements (praticien + client) sont requis pour l'inclusion.

**Droit d'information** : le praticien reçoit un rapport mensuel sur l'utilisation des données de ses séances dans le pipeline (nombre de séances dans chaque niveau de qualification, statut d'effacement).

**Droit de suppression de leurs données professionnelles** : en cas de rupture du contrat avec IVIA, les données professionnelles du praticien (profil, paramètres) sont supprimées selon le protocole de clôture de compte.

### 4.2 Traitement de la voix du praticien comme donnée biométrique

La voix du praticien est tout autant présente dans l'enregistrement de séance que celle du client. À ce titre, elle constitue également une **donnée biométrique identifiable** au sens de la Loi 25 (art. 14) et du RGPD (art. 9). IVIA aligne le traitement de la voix du praticien sur celui de la voix du client, avec quelques spécificités contractuelles.

**Engagements miroirs (équivalents au traitement client)** :
- Audio identifiable du praticien soumis aux mêmes délais : effacement post-certification (max J+7 en période pilote, voir Étape 6.A) ; voice conversion en M13+ (Étape 6.B)
- Pseudonymisation dans la transcription (le prénom du praticien évoqué par le client est remplacé par un token)
- Inclusion dans le pipeline d'enrichissement subordonnée à son **consentement explicite** (signature contrat praticien + opt-in tableau de bord pour Niveaux 2 et 3)
- Logs cryptographiques d'accès : tout accès aux audios contenant la voix du praticien est journalisé, et le praticien reçoit un rapport mensuel des accès (même logique que pour le client)

**Spécificités contractuelles** :
- Le consentement professionnel à l'enregistrement est intégré dans le contrat praticien (CONTRAT_PRATICIEN_TYPE.md). Sans ce consentement de base : pas de pratique sur la plateforme.
- Le consentement praticien aux Niveaux 2 et 3 (dataset, modèle) est **révocable à tout moment** sans rupture du contrat. Effet : ses futures séances n'alimentent plus le pipeline. Limite : les apprentissages déjà incorporés au modèle ne sont pas extractibles (même logique que pour le client — voir DÉC-V3-11).
- En cas de rupture du contrat praticien : ses données professionnelles (profil, paramètres) sont supprimées selon le protocole de clôture de compte. Sa voix déjà traitée dans le pipeline suit les mêmes règles que celle du client (séances exclues du dataset si demandé dans les délais ; signaux déjà anonymisés ou intégrés au modèle suivent la limite technique).

**Asymétrie reconnue** : contrairement au client, le praticien participe à plusieurs centaines de séances avec sa propre voix. Cela crée une signature biométrique plus robuste et donc une exposition au risque de réidentification accrue. La Partie VIII (Architecture cryptographique) et l'Étape 6.B (voice conversion M13+) tiennent compte de cette asymétrie : la voice conversion est calibrée pour neutraliser également les signatures multi-séances.

### 4.3 Ce que le praticien NE peut pas faire

Le praticien ne peut pas :
- Exporter les enregistrements audio bruts des séances (même les siennes)
- Partager les transcriptions avec des tiers non autorisés
- Utiliser les analyses MERLIN comme base de diagnostics cliniques ou d'actes réservés
- Contourner le système de consentement

---

## PARTIE V — CHARTE DE CESSION

### 5.1 Ce qui peut être cédé, vendu ou partagé

| Actif | Cédable | Conditions |
|---|---|---|
| Pipeline technique (code + architecture) | Oui | Acquéreur lié par la Charte doctrinaire |
| Dataset synthétique | Oui | Si aucune information personnelle vérifiable |
| Modèle propriétaire IVIA (poids) | Oui | Si data d'entraînement exclusivement synthétique |
| Signaux agrégés anonymisés | Oui (sous conditions) | Publication scientifique possible avec protocole éthique |
| Indicateurs de santé émotionnelle collective (%) | Oui | Agrégés, sans contexte identifiable |

### 5.2 Ce qui ne peut jamais être cédé

| Actif | Interdiction | Fondement |
|---|---|---|
| Enregistrements audio bruts | Absolue | Loi 25, Charte doctrinaire A.3 |
| Transcriptions non anonymisées | Absolue | Loi 25, Charte doctrinaire A.3 |
| Données biométriques vocales | Absolue | Loi 25 art. 14, RGPD art. 9 |
| Dossiers clients identifiants | Absolue | Loi 25, obligations professionnelles |
| Consentements et historique de révocation | Absolue | Preuve juridique — conservation interne seulement |
| Dataset synthétique si traçabilité possible | Absolue | Principe de prudence |

### 5.3 En cas de fusion, acquisition ou liquidation

En cas de transfert du contrôle d'IVIA ou MERLIN inc. :

1. L'acquéreur potentiel doit signer un accord de confidentialité intégrant la présente Charte AVANT tout accès aux données
2. L'audit préalable (due diligence) est limité aux données agrégées et aux métadonnées non personnelles
3. Le transfert effectif des données personnelles ne peut se faire que vers un acquéreur ayant formellement adopté la présente Charte et la Charte doctrinaire
4. En cas de liquidation sans repreneur qualifié : destruction certifiée de toutes les données personnelles avec rapport notarié

---

## PARTIE VI — AUDIT ANNUEL PUBLIC

### 6.1 Périmètre de l'audit données

L'audit annuel de conformité des données couvre :
1. La conformité du pipeline à chaque étape (vérification des délais de destruction, des logs)
2. L'état des consentements (taux de révocation, anomalies)
3. Les incidents de sécurité survenus et leur traitement
4. Les demandes d'accès, rectification, suppression traitées
5. La liste des sous-traitants actifs et leur statut de conformité
6. La conformité aux obligations Loi 25 (EFVP à jour, RPRP nommé)

### 6.2 Publication

Le rapport est publié sur ivia.quebec/transparence dans les 60 jours suivant la clôture de l'exercice. Il est accompagné d'un avis de l'auditeur externe (obligatoire à partir du Palier 3 / M7).

### 6.3 Audit interne pendant la phase pilote (M1-M6)

L'audit externe formel n'étant obligatoire qu'à partir du Palier 3 (M7), la phase pilote M1-M6 est encadrée par un dispositif d'audit interne mensuel — phase critique où les processus sont en rodage et le risque d'incident le plus élevé.

**Modalités** :
- **Cadence** : audit interne mensuel pendant toute la période pilote (M1 → M6)
- **Conduite conjointe** : RPRP opérationnel (David Phaneuf) + Superviseur RPRP externe (Partie 0)
- **Périmètre minimum** : vérification des délais d'effacement audio, conformité des certifications praticien, intégrité du hash chain des logs d'accès, taux de révocation, incidents techniques signalés
- **Format** : compte rendu écrit transmis au Comité doctrinal dans les 7 jours suivant l'audit
- **Transparence** : un résumé agrégé des audits internes M1-M6 est intégré au premier rapport annuel public publié à M12+

**Rationale** : un incident détecté et documenté pendant le pilote est un acquis d'apprentissage. Un incident détecté après coup, sans trace d'audit, est une faille de gouvernance. Le coût d'un audit interne mensuel est trivial face au bénéfice doctrinal et réputationnel.

---

## PARTIE VII — SOUS-TRAITANTS ET FOURNISSEURS

### 7.1 Fournisseurs actuels et statut

| Fournisseur | Usage | Données transmises | Accord de traitement |
|---|---|---|---|
| Deepgram | Transcription audio | Audio pseudonymisé | DPA (Data Processing Agreement) requis |
| OpenAI / Anthropic | Analyse IA | Transcription pseudonymisée | DPA requis, no training par défaut |
| OVH (Canada) | Hébergement, stockage | Toutes données — hébergement Canada | DPA + hébergement territorial |
| Stripe | Paiement | Données de paiement uniquement | Certifié PCI-DSS niveau 1 |
| LiveKit | Audio temps réel | Stream audio pendant séance | DPA requis, no storage par défaut |

### 7.2 Principes de sélection des sous-traitants

1. Hébergement des données sensibles sur infrastructure canadienne (OVH Canada) obligatoire
2. Clause de non-utilisation des données pour entraînement de modèles propres au fournisseur
3. DPA signé avant tout transfert de données personnelles
4. Évaluation annuelle de la conformité de chaque sous-traitant

### 7.3 Transferts hors Québec

Les données personnelles identifiables ne doivent pas quitter le territoire canadien. Pour les données traitées par des fournisseurs américains (Deepgram, OpenAI, Anthropic) :
- Utiliser les endpoints canadiens quand disponibles
- Pseudonymisation maximale avant transmission
- Clause contractuelle sur la non-rétention des données transmises
- Revue annuelle des risques liés aux transferts

### 7.4 Clause de non-rétention transitoire

Même un audio "transcrit puis effacé" transite par les serveurs du fournisseur de transcription. Sans clause explicite, des fragments peuvent être conservés en buffers, queues de traitement ou caches transitoires. IVIA exige donc dans tous les DPA avec ses fournisseurs de traitement de données sensibles :

**Clause type non dérogeable** :
> *Le fournisseur s'engage à ne conserver aucune donnée transmise par IVIA au-delà de la durée strictement nécessaire au traitement direct demandé. Toute donnée transitoire (buffer, queue, cache) est purgée dans un délai maximum de 24 heures après la fin du traitement. Le fournisseur fournit, sur demande, un rapport technique décrivant ses mécanismes de purge transitoire.*

**Application aux fournisseurs critiques** :
- **Deepgram** (transcription) : audit du DPA avant 31 mai 2026. Si la clause de non-rétention transitoire 24h n'est pas obtenue, évaluation de fournisseurs alternatifs (Azure Speech-to-Text Canada, AWS Transcribe Canada, ou solution self-hosted Whisper).
- **OpenAI / Anthropic** : DPA "no training" déjà standard ; audit de la clause transitoire avant production. Pseudonymisation préalable maintenue comme garde-fou supplémentaire.
- **LiveKit** (audio temps réel) : DPA "no storage" déjà contractualisé. Vérification que les buffers WebRTC ne survivent pas à la fin de session.

**Documentation publique** : la liste des fournisseurs et leur statut de conformité à cette clause est publiée dans le rapport annuel de transparence (Partie VI), avec mention explicite de toute non-conformité résiduelle et plan de remplacement le cas échéant.

---

## PARTIE VIII — ARCHITECTURE CRYPTOGRAPHIQUE

### 8.1 Vue d'ensemble par phase du flux

| Phase du flux | Type de chiffrement | Algorithme / Protocole | Gestion des clés |
|---|---|---|---|
| Audio en direct (séance praticien-client) | En transit + chiffrement média | TLS 1.3 + SRTP/DTLS (LiveKit) | Clés de session éphémères |
| Stockage audio brut (J+0 → certification) | Au repos | AES-256-GCM | Clés gérées via OVH HSM (Canada) |
| Transcription en transit vers Deepgram | En transit | TLS 1.3 — endpoint canadien si disponible | Clés côté fournisseur (DPA) |
| Stockage transcription pseudonymisée | Au repos | AES-256-GCM | OVH HSM Canada |
| Stockage table de correspondance pseudo ↔ identifiants | Au repos + clé isolée | AES-256-GCM avec clé distincte du stockage transcription | Clé d'accès maître séparée (rotation 90 j) |
| Signaux structurés anonymisés (Étape 5) | Au repos | AES-256-GCM | OVH HSM Canada |
| Audio transformé (M13+, post-voice conversion) | Au repos | AES-256-GCM | OVH HSM Canada — compartiment dédié |
| Logs d'accès humain | Au repos + signature | AES-256 + hash chain (SHA-256) | Clé de signature indépendante |
| Dataset synthétique (Étape 7) | Au repos | AES-256-GCM | OVH HSM Canada |
| Modèle propriétaire IVIA (poids) | Au repos | AES-256-GCM | OVH HSM Canada — accès contraint |

### 8.2 Principes de gouvernance des clés

1. **Séparation stricte** : la clé de chiffrement de la table de correspondance pseudonyme ↔ identifiant client est physiquement et logiquement isolée des autres clés. Aucun accès combiné ne permet à un seul rôle de réidentifier sans déclenchement de procédure formelle.
2. **Rotation régulière** : clés maîtres rotationées tous les 90 jours. Clés dérivées par séance.
3. **HSM souverain** : toutes les clés sensibles sont stockées dans un HSM (Hardware Security Module) opéré par OVH au Canada. Aucune clé sensible ne quitte le territoire canadien.
4. **Chaînage cryptographique des logs** : les journaux d'accès sont signés et chaînés (chaque entrée contient le hash de la précédente), rendant toute altération rétroactive détectable.
5. **Résilience** : sauvegardes chiffrées des clés critiques en split (Shamir Secret Sharing) entre 3 dépositaires distincts à partir du Palier 3 (M7).

### 8.3 Limites reconnues

IVIA reconnaît honnêtement les limites suivantes :
- **Pas de E2EE strict** : voir Étape 1 et justification ci-dessus
- **Sous-traitants US** : Deepgram et OpenAI/Anthropic opèrent partiellement aux États-Unis. Même avec endpoints canadiens et DPA, un transit transitoire peut survenir. La pseudonymisation préalable et la clause de non-rétention dans les DPA réduisent le risque, sans l'éliminer.
- **Voice conversion (M13+)** : traitée comme pseudonymisation, pas anonymisation — risque résiduel de réidentification reconnu (Étape 6.B).
- **Modèle entraîné** : aucune cryptographie ne peut "désapprendre" un modèle. La protection à ce stade est doctrinale (dataset exclusivement synthétique) et juridique, pas cryptographique.

Ces limites sont réévaluées à chaque mise à jour de la Charte et à chaque audit annuel.

---

## MISE À JOUR DE CETTE CHARTE

La présente Charte est mise à jour :
- Automatiquement lors de l'activation de chaque nouvelle phase du pipeline (v2.0 à Palier 4, v3.0 à Palier 5, v4.0 à Palier 6)
- En cas de changement législatif majeur (Loi 25 amendements, RGPD modifications)
- Suite à un incident de sécurité ayant révélé une lacune
- Sur décision du Comité doctrinal

Les mises à jour sont notifiées à tous les praticiens et clients actifs au moins 30 jours avant entrée en vigueur, avec possibilité de révocation des consentements.

---

## RÉFÉRENCES

- `CHARTE_DOCTRINAIRE_IVIA.md` — Principes A.3, A.7 (règles fermes données)
- `POLITIQUE_CONFIDENTIALITE_LOI25.md` — Politique détaillée conformité
- `BP_FINANCEMENT_V2.md` — Section B.9 (pipeline dans l'offre)
- `PLAN_INTEGRATION_IVIA_36MOIS.md` — Tableau pipeline par palier

---

**Au sein de l'être — En actes.**

*Version 1.0 — Mai 2026*
*À mettre à jour en v2.0 lors de l'activation de la synthèse vocale (Palier 4 / M13)*

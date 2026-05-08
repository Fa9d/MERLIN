# PLAN DE SORTIE ET DE CONTINUITÉ — IVIA / MERLIN
## Succession fondateur, protocole doctrinal, scénarios de cession et transmission longue

**Version** : 1.0 — Vague 3
**Date** : Mai 2026
**Statut** : Document confidentiel — Usage interne, conseil d'administration, conseillers juridiques
**Auteur** : David Phaneuf (fondateur) + Perplexity Computer
**Cohérence** : Aligné avec CHARTE_DOCTRINAIRE_IVIA.md, GOUVERNANCE_INTERNE_IVIA.md, STRUCTURE_JURIDIQUE_RECOMMANDEE.md

---

## PRÉAMBULE

### La pérennité d'IVIA dépasse son fondateur

Cette affirmation n'est pas une formule rhétorique. Elle définit la posture fondamentale de ce document.

David Phaneuf a fondé IVIA. Il en est l'architecte doctrinal, le premier garant des 7 principes, et le premier risque de concentration si IVIA reste entièrement dépendante de sa présence.

Une organisation qui ne peut pas fonctionner sans son fondateur n'est pas une organisation durable. C'est une extension du fondateur. IVIA a vocation à durer — pas seulement pendant la vie active de David Phaneuf.

Ce document est donc à la fois un acte de responsabilité (protéger les personnes qui font confiance à IVIA : praticiens, clients, partenaires) et un acte de libération (permettre à IVIA de grandir au-delà de ce qu'un seul fondateur peut porter).

### La tension entre contrôle et durabilité

Il existe une tension réelle entre deux impératifs :
- Protéger l'intégrité doctrinaire d'IVIA (qui requiert un contrôle fort sur les décisions fondamentales)
- Construire une organisation durable (qui requiert une distribution du pouvoir au-delà d'une seule personne)

Ce document résout cette tension en distinguant clairement ce qui doit rester sous contrôle strict (la doctrine, les données personnelles) et ce qui peut et doit être distribué (les décisions opérationnelles, la direction commerciale, la responsabilité technique).

---

## PARTIE I — PLAN DE CONTINUITÉ FONDATEUR

### 1.1 Désignation d'un directeur de relève

**Note d'attention critique — Action requise avant M2**
> La Note d'attention 1 de la Vague 2 (PROGRESSION_VAGUE2.md) identifie l'absence de directeur de relève désigné comme le risque le plus critique et le seul sans mitigation opérationnelle. Ce document formalise l'obligation et les critères de désignation. L'action doit être complétée avant la fin du mois 2 du pilote (juillet 2026).

**Profil requis du directeur de relève**

Le directeur de relève n'est pas nécessairement un candidat au poste de PDG à terme. C'est la personne capable de maintenir IVIA opérationnel pendant une absence temporaire ou de prendre les premières décisions urgentes en cas d'incapacité prolongée ou de décès du fondateur.

| Critère | Description |
|---|---|
| Adhésion doctrinaire | Connaissance profonde des 7 principes et capacité à les appliquer sous pression |
| Compréhension technique | Capable de comprendre les enjeux du pipeline et de l'infrastructure, pas nécessairement de les opérer |
| Capacité de décision sous incertitude | Capable de prendre des décisions difficiles sans le fondateur présent |
| Disponibilité | Peut répondre dans les 24 heures en cas d'urgence |
| Crédibilité auprès des praticiens | Connue et respectée dans l'écosystème IVIA |
| Intégrité | Pas de conflit d'intérêt avec IVIA |

**Candidats potentiels** : à désigner par le fondateur avant juillet 2026. La désignation est documentée dans le Vault des procédures d'urgence et notifiée au conseil de l'OBNL.

**Formalisation** : la désignation fait l'objet d'une résolution du conseil de MERLIN inc. et d'une notification au conseil de l'OBNL.

### 1.2 Procédure de bascule

**Bascule 24 heures (incapacité soudaine ou décès)**

- Alerte envoyée par le système de surveillance (processus d'alerte à définir — contact de confiance qui sait comment joindre le directeur de relève)
- Le directeur de relève prend possession des accès d'urgence (voir 1.3)
- Communication aux deux praticiennes pilote (ou aux praticiens actifs) : "IVIA continue d'opérer. Un message complet suivra dans 24 heures."
- Notification au conseil de l'OBNL

**Bascule 7 jours (incapacité confirmée)**

- Le directeur de relève assume la direction opérationnelle de MERLIN inc. (à titre intérimaire)
- Convocation d'urgence du conseil de MERLIN inc. pour confirmer le mandat intérimaire
- Notification aux investisseurs seed (si applicable à ce stade)
- Communication publique sur ivia.quebec (sobre, factuelle, rassurante)
- Revue des engagements contractuels immédiats (renouvellements, paiements, contrats)

**Bascule 30 jours (incapacité prolongée ou décès confirmé)**

- Le conseil de MERLIN inc. entame un processus de désignation d'un nouveau dirigeant
- Le conseil de l'OBNL convoque une assemblée extraordinaire pour décider de la continuité doctrinaire
- Évaluation de l'état financier (trésorerie, engagements, levée de fonds en cours)
- Communication aux praticiens et clients selon le protocole de communication de crise Niveau 3-4
- Décision sur la continuité ou la dissolution (si dissolution : voir procédure CHARTE_DOCTRINAIRE_IVIA.md Partie VI)

### 1.3 Documentation accessible — Vault d'urgence

Le Vault d'urgence est un document chiffré (gestionnaire de mots de passe de type BitWarden, 1Password Enterprise ou équivalent) contenant :

| Élément | Contenu |
|---|---|
| Accès OVH | Identifiants admin infrastructure |
| Accès GitHub | Token d'accès organisation |
| Accès Stripe | Identifiants admin paiement |
| Accès Deepgram | Clé API transcription |
| Accès OpenAI / Anthropic | Clés API IA |
| Accès domaine ivia.quebec | Identifiants registrar |
| Accès Doppler | Identifiants vault secrets |
| Contacts clés | Avocat, comptable, conseiller RS&DE, DevOps externe |
| Contrats actifs | Liste et dates de renouvellement |
| Investisseurs (si applicable) | Coordonnées et montants |
| Comptes bancaires | Coordonnées MERLIN inc. et IVIA OBNL |
| Procédures d'urgence | Ce document (résumé opérationnel) |

**Accès au Vault d'urgence** : fondateur + directeur de relève désigné. Mise à jour trimestrielle obligatoire.

**Localisation** : le Vault est accessible depuis deux emplacements indépendants (ex. gestionnaire de mots de passe cloud + copie chiffrée sur clé USB dans un coffre physique avec l'avocat ou le notaire).

---

## PARTIE II — SUCCESSION DOCTRINALE

### 2.1 Le Comité doctrinal — Rappel de la structure

La CHARTE_DOCTRINAIRE_IVIA.md (Partie IV) établit la composition du Comité doctrinal :
- Le fondateur (voix délibérative permanente)
- 2 praticiens actifs IVIA élus pour 2 ans renouvelables une fois
- 1 représentant des clients (élu pour 1 an)
- 1 membre externe indépendant (expert éthique/droit/santé mentale, mandat 3 ans)

### 2.2 Protocole de renouvellement des membres

**Praticiens élus** :
- Élection par les praticiens actifs (vote numérique sécurisé)
- Mandat de 2 ans, renouvelable une fois
- Pas d'élection la même année que le renouvellement du membre externe (pour garantir une continuité institutionnelle)
- Premier renouvellement : M18 (pour les praticiens désignés au lancement)

**Représentant des clients** :
- Tirage au sort parmi les clients actifs volontaires (candidature ouverte)
- Mandat d'un an, non renouvelable immédiatement (pause d'un an minimum)
- Premier renouvellement : M12

**Membre externe** :
- Désigné par le fondateur (avec approbation du conseil de l'OBNL)
- Mandat de 3 ans, renouvelable une fois
- Critères : expertise en éthique des organisations, droit des professions, ou santé mentale communautaire — pas nécessairement québécois mais connaissant le contexte

**Succession du fondateur au sein du Comité** :
- En cas d'incapacité temporaire du fondateur : le directeur de relève assume la voix délibérative du fondateur au Comité
- En cas d'incapacité permanente ou décès : le Comité désigne un membre honoraire "garant de la vision fondatrice" (statut consultatif, pas délibératif) et le conseil de l'OBNL assume le rôle de gardien doctrinal en dernier ressort

### 2.3 Protocole de transmission de la doctrine

**Transmission active (avant toute transition)**

Avant M12 (au plus tard), David Phaneuf produit un document de transmission de la doctrine qui va au-delà de la Charte formelle : il explique les intentions derrière chaque principe, les tensions qu'il a résolu par chaque règle, et les situations non prévues qu'il a rencontrées dans le pilote.

Ce document de transmission n'est pas public — il est un legs institutionnel interne, disponible pour les membres du Comité doctrinal.

**Transmission formelle (lors de chaque renouvellement de membre)**

Chaque nouveau membre du Comité doctrinal suit une session d'intégration de 3 heures avec le fondateur (ou son successeur au Comité) couvrant :
1. La genèse de chaque principe — pourquoi il a été formulé ainsi, pas autrement
2. Les règles fermes du Bloc A — les situations qui ont justifié leur formulation explicite
3. Les tensions doctrinales non résolues — les zones grises où le Comité devra exercer son jugement
4. L'historique des décisions majeures (document HISTORIQUE_DECISIONS_STRATEGIQUES.md)

### 2.4 Garde-fous anti-dérive

**Garde-fou 1 — L'audit annuel public**
L'audit doctrinal annuel est la principale protection contre la dérive. Il rend les non-conformités visibles et opposables, indépendamment de la composition du Comité.

**Garde-fou 2 — Le seuil de modification des principes**
Modifier un des 7 principes requiert l'unanimité du Comité + approbation du conseil de l'OBNL + consultation publique de 60 jours. Ce seuil est intentionnellement élevé pour protéger contre les révisions opportunistes.

**Garde-fou 3 — La clause d'inaliénabilité dans les statuts de MERLIN inc.**
Les statuts de MERLIN inc. intègrent la Charte doctrinaire par référence. Un actionnaire ne peut pas obtenir une résolution qui viole la Charte, même avec une majorité.

**Garde-fou 4 — Le droit de rachat de l'OBNL**
Si un actionnaire de MERLIN inc. cherche à modifier la doctrine dans un sens incompatible avec les Parties I et VI de la Charte, l'OBNL dispose d'un droit de rachat des actions de cet actionnaire à valeur marchande.

---

## PARTIE III — SCÉNARIOS DE SORTIE M36+

### 3.1 Acquisition

**Conditions d'un rachat acceptable**

Une acquisition n'est pas en contradiction avec la doctrine d'IVIA si — et seulement si — les conditions suivantes sont réunies :

1. L'acquéreur adopte formellement la Charte doctrinaire avant signature
2. Le pipeline de données gouvernées est maintenu tel quel (pas de réduction des délais de destruction, pas d'usage publicitaire)
3. La règle de non-commission est maintenue (aucune commission sur l'orientation)
4. Le dataset synthétique et le modèle propriétaire ne sont pas cédés à des fins incompatibles avec la doctrine
5. L'OBNL IVIA maintient une participation suffisante pour exercer son droit de veto doctrinal post-acquisition

**Acquéreurs compatibles identifiés à ce stade (hypothétiques)**

| Profil acquéreur | Compatibilité doctrinaire | Probabilité |
|---|---|---|
| Plateforme québécoise de santé communautaire | Élevée | Faible (capacité de rachat limitée) |
| Grand système de santé (CIUSSS, etc.) | Moyenne (risque de bureaucratisation) | Faible |
| Fonds à impact social | Élevée | Modérée |
| Entreprise tech canadienne à mission (ex. Shopify-like) | Moyenne | Modérée |
| GAFAM ou grande plateforme tech | Très faible | Refus probable par OBNL |

### 3.2 Fusion

Une fusion avec un acteur complémentaire (ex. une plateforme de gestion de clinique qui veut enrichir son offre avec le pipeline documentaire IVIA) est envisageable si :
- L'entité résultante adopte la structure hybride OBNL/SPA ou son équivalent
- Le contrôle doctrinal de l'OBNL est maintenu post-fusion
- La fusion ne crée pas un conflit d'intérêt avec la règle de non-commission

### 3.3 Transmission OBNL pure

Ce scénario est le plus cohérent avec la vision fondatrice à long terme :
- MERLIN inc. atteint la rentabilité opérationnelle (MRR > charges récurrentes)
- La direction est transmise à une équipe professionnelle salariée (PDG non-fondateur)
- David Phaneuf conserve un rôle au Comité doctrinal mais cède la direction opérationnelle
- L'OBNL IVIA continue de contrôler MERLIN inc. par ses droits de vote spéciaux
- La mission est pérennisée indépendamment de l'implication du fondateur

Ce scénario est l'horizon visé pour M60+ (au-delà des 36 mois du présent plan).

### 3.4 IPO (Cotation en bourse)

L'IPO est jugée improbable et doctrinalement problématique pour IVIA dans son horizon visible.

**Pourquoi l'IPO est problématique pour IVIA** :
1. Les actionnaires publics ont un droit de regard sur les décisions stratégiques que la structure hybride OBNL/SPA protège contre les actionnaires privés, mais pas facilement contre les actionnaires publics
2. La pression des marchés boursiers sur la croissance trimestrielle est structurellement incompatible avec le principe d'équilibre (Principe 2) et la doctrine de croissance prudente
3. La transparence requise par une cotation publique sur les données financières pourrait exposer des informations sensibles sur les modèles de données

**Si un IPO était envisagé malgré tout** : il ne pourrait l'être que si une structure de "classe d'actions super-votantes" permettait à l'OBNL de maintenir son contrôle doctrinal post-IPO, similaire à ce que font Shopify (actions multi-vote) ou Berkshire Hathaway.

---

## PARTIE IV — CONDITIONS NON-NÉGOCIABLES EN CAS DE CESSION

### 4.1 Ce qu'IVIA ne cède jamais — Les inaliénables

**La doctrine** (OBNL) :
La Charte doctrinaire IVIA est la propriété exclusive de l'OBNL IVIA. Elle ne peut pas être cédée dans une transaction commerciale. Elle peut être adoptée par un acquéreur comme condition de la cession — mais elle reste la propriété de l'OBNL.

**La marque IVIA** (OBNL) :
La marque IVIA (nom, logo, identité visuelle) appartient à l'OBNL. Une cession de MERLIN inc. sans l'OBNL ne transfère pas la marque IVIA. L'acquéreur peut opérer la plateforme sous une autre marque, ou négocier une licence de la marque IVIA avec l'OBNL.

**Les données personnelles brutes** :
Conformément à la Charte doctrinaire (Partie VI, F.2) et à la Charte de transformation gouvernée des données, les enregistrements audio bruts, les transcriptions non anonymisées et les données biométriques ne peuvent jamais être cédés. En cas de cession sans repreneur qualifié, ils sont détruits de façon certifiée.

**La mission de l'OBNL** :
L'OBNL IVIA et sa mission sociale ne peuvent pas être "vendus". L'OBNL peut continuer d'exister et de licencier sa marque à un autre opérateur si MERLIN inc. est cédé ou liquidé.

### 4.2 Ce qui peut être cédé — Les cessibles conditionnels

| Actif | Conditions de cession |
|---|---|
| Code source MERLIN | Acquéreur lie par la Charte doctrinaire |
| Pipeline transformation gouvernée | Acquéreur lie par la Charte données + maintien du J+30 |
| Signaux extraits anonymisés | Acquéreur lie par la Charte données, usage limité |
| Dataset synthétique | Vérification d'absence de données personnelles avant cession |
| Modèle propriétaire IVIA | Dataset d'entraînement exclusivement synthétique confirmé |
| Marque MERLIN | Sans restriction si séparée de la marque IVIA |
| Contrats praticiens | Avec notification aux praticiens et droit de résiliation |

---

## PARTIE V — STRATÉGIE DE SORTIE DES INVESTISSEURS

### 5.1 Fenêtres de sortie anticipées

Les investisseurs seed (M0-M3) ont une fenêtre de sortie naturelle à la Série A (M18-M24) : rachat de leurs parts par les nouveaux investisseurs ou par MERLIN inc. si la trésorerie le permet.

Les investisseurs Série A (M18-M24) ont une fenêtre de sortie naturelle à M36-M48 : acquisition, fusion, ou rachat secondaire.

### 5.2 Mécanismes de sortie

| Mécanisme | Description | Applicable |
|---|---|---|
| Rachat par MERLIN inc. (buyback) | MERLIN inc. rachète les parts de l'investisseur si la trésorerie le permet | M24+ si rentabilité |
| Cession secondaire | L'investisseur vend ses parts à un autre investisseur entrant | À tout moment (avec ROFR) |
| Acquisition (100 %) | Toute l'entreprise est acquise | M36+ |
| Acquisition partielle | Un investisseur majoritaire prend le contrôle | Sous conditions doctrinaires |

**ROFR (Right of First Refusal)** : les autres actionnaires ont le droit de premier refus sur toute cession de parts d'un investisseur. Ce mécanisme protège contre l'entrée d'un actionnaire incompatible avec la doctrine.

### 5.3 Protection des investisseurs dans le contexte IVIA

Les investisseurs dans MERLIN inc. acceptent, au moment de leur investissement, que :
1. Le droit de veto doctrinal de l'OBNL s'applique sur les matières définies
2. La croissance de MERLIN inc. est gouvernée par des principes de croissance équilibrée (pas de croissance à tout prix)
3. Certains actifs (données brutes) ne peuvent jamais être monétisés — ce qui réduit certains scénarios de maximisation de valeur

En échange, ces investisseurs reçoivent :
1. Un engagement de transparence supérieur à la norme (rapport d'audit annuel public)
2. La protection contre les scandales de données (pipeline J+30, charte publique)
3. Un avantage concurrentiel documenté (moat doctrinal + technologique)
4. Un accès préférentiel à la Série A (droit de suivre leur investissement)

---

## PARTIE VI — PLAN DE TRANSMISSION LONGUE (10-20 ANS)

### 6.1 Vision à 10 ans (2036)

À l'horizon 2036, IVIA devrait être :
- Une plateforme mature avec 1 500-3 000 praticiens actifs dans les 4 strates
- Une référence institutionnelle dans le paysage de l'accompagnement émotionnel au Québec
- Opérée par une équipe professionnelle complète (PDG, CTO, directeur des partenariats, équipe)
- Financièrement autonome (sans dépendance aux subventions)
- Avec un modèle propriétaire IVIA reconnu comme l'outil de référence dans le domaine

David Phaneuf jouerait à cet horizon un rôle de garant doctrinal au sein du Comité doctrinal, sans nécessairement être dans la direction opérationnelle.

### 6.2 Vision à 20 ans (2046)

À l'horizon 2046, l'OBNL IVIA devrait être une institution durable, indépendante de tout fondateur individuel, avec :
- Un Comité doctrinal renouvelé par plusieurs générations de praticiens
- Un fonds de dotation assurant la pérennité de la mission au-delà des cycles économiques
- Un modèle propriétaire de cinquième génération ou au-delà
- Un impact documenté sur l'autonomie émotionnelle de dizaines de milliers de personnes au Québec et potentiellement au Canada

### 6.3 Les conditions de la transmission longue

1. **La doctrine reste vivante** : les 7 principes ne sont pas un texte figé dans le passé. Chaque génération du Comité doctrinal les réinterprète à la lumière de son époque, dans le respect de leur esprit fondateur.

2. **Le modèle économique reste équilibré** : IVIA ne peut pas survivre sur des subventions indéfiniment. La transmission longue requiert l'atteinte et le maintien de la rentabilité opérationnelle de MERLIN inc.

3. **La technologie reste au service de la mission** : à mesure que l'IA évolue, IVIA adapte ses outils. Mais l'adaptation est toujours gouvernée par la même question : "Est-ce que cette évolution sert les personnes accompagnées ?"

4. **La confiance des praticiens reste le capital premier** : sans praticiens qui croient dans la mission, IVIA n'est qu'un outil. La transmission longue requiert que chaque génération de praticiens IVIA soit aussi convaincue que les pionniers.

---

**Au sein de l'être — En actes.**

*Version 1.0 — Mai 2026*
*David Phaneuf, fondateur IVIA*

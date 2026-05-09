# Indicateurs praticien IVIA — Cartographie complète
**Version 1 — Document de conception interne**
**Auteur : système MERLIN — David Beaupré, fondateur IVIA**

---

## 1. Principes

Le système d'indicateurs IVIA repose sur une prémisse claire : mesurer pour soutenir, jamais pour surveiller. Chaque donnée collectée doit servir soit le praticien dans sa propre compréhension de son travail, soit la plateforme dans sa capacité à identifier un praticien en difficulté avant qu'il s'épuise ou dérive. La doctrine "Au sein de l'être — En actes" s'applique ici aussi : les indicateurs ne sont pas des jugements extérieurs portés sur le praticien, mais des reflets qu'il peut choisir de consulter ou non.

La transparence prime sur le contrôle : le praticien voit tout ce que la plateforme voit de lui. L'agrégation protège le client et le praticien individuellement. L'administration ne dispose que de données nécessaires à la santé du collectif, pas à l'évaluation de performance individuelle au sens disciplinaire. Les seuils d'alerte sont conçus pour déclencher un accompagnement, jamais une sanction. Enfin, toute donnée anonymisée diffusée publiquement doit renforcer la cohérence doctrinale d'IVIA — preuve que le modèle tient, pas argument de vente.

---

## 2. Catégories d'indicateurs

### A. FINANCIER

| Indicateur | Définition | Source | Fréquence | Visibilité |
|---|---|---|---|---|
| **Revenu brut mensuel** | Total des lectures facturées dans le mois, avant frais de plateforme | Système de paiement | Mensuelle | Praticien + Admin |
| **Revenu net après commission IVIA** | Montant versé au praticien après déduction du % plateforme | Système de paiement | Mensuelle | Praticien seul |
| **Taux d'occupation calendrier** | % des plages disponibles réservées sur une période de 30 jours | Calendrier | Hebdomadaire | Praticien + Admin |
| **Panier moyen par lecture** | Revenu moyen par séance sur les 90 derniers jours | Système de paiement | Mensuelle | Praticien + Admin |
| **Taux de conversion visite-profil → réservation** | % des visiteurs de la fiche praticien qui complètent une réservation | Métadonnées plateforme | Mensuelle | Praticien + Admin |
| **Lectures complétées vs annulées** | Ratio lectures livrées sur lectures initiées dans un mois | Métadonnées plateforme | Mensuelle | Praticien + Admin |
| **Délai moyen encaissement** | Nombre de jours entre dépôt client et paiement praticien | Système de paiement | Mensuelle | Praticien seul |
| **Évolution revenu 3 mois glissants** | Courbe de tendance sur 90 jours, identification de creux saisonniers | Système de paiement | Trimestrielle | Praticien + Admin |

---

### B. QUALITATIF

| Indicateur | Définition | Source | Fréquence | Visibilité |
|---|---|---|---|---|
| **Note moyenne client** | Moyenne des évaluations soumises par les clients (échelle 1-5) après livraison de la lecture | Formulaire retour client | Après chaque séance | Praticien + Admin |
| **Taux de retour écrit** | % de clients ayant laissé un commentaire textuel (pas seulement une note) | Formulaire retour client | Mensuelle | Praticien + Admin |
| **Taux de re-réservation à 90 jours** | % de clients ayant fait au moins une deuxième réservation dans les 90 jours suivant leur première lecture | Calendrier + historique client | Trimestrielle | Praticien + Admin |
| **Mots-clés positifs détectés dans retours** | Extraction automatique des termes récurrents à valence positive dans les commentaires clients (ex. : clarté, présence, espace, profondeur) | Traitement textuel des retours | Mensuelle | Praticien seul |
| **Mots-clés négatifs ou neutres détectés** | Termes récurrents à valence neutre ou négative (ex. : générique, vague, trop court) — signal d'amélioration | Traitement textuel des retours | Mensuelle | Praticien + Admin |
| **Taux de satisfaction déclarée post-livraison** | % de clients ayant coché "la lecture m'a aidé à avancer" dans le formulaire de retour | Autoévaluation client | Après chaque séance | Praticien + Admin |
| **Ratio écoute complète de l'audio** | % des clients ayant écouté la lecture jusqu'à la fin (si techniquement mesurable via lecteur audio) | Métadonnées lecteur | Par lecture | Praticien + Admin |

---

### C. TYPOLOGIE CLIENTÈLE

| Indicateur | Définition | Source | Fréquence | Visibilité |
|---|---|---|---|---|
| **Motifs récurrents de dépôt** | Thèmes les plus fréquents dans les audios déposés par les clients de ce praticien (ex. : transition professionnelle, relation amoureuse, épuisement) | Catégorisation manuelle ou assistée des dépôts | Mensuelle | Praticien + Admin agrégé |
| **Fréquences travaillées** | Registres émotionnels ou vibratoires les plus mobilisés dans les lectures produites par le praticien | Autoévaluation praticien + catégorisation des lectures | Trimestrielle | Praticien seul |
| **Tranche d'âge dominante** | Distribution agrégée des tranches d'âge de la clientèle (sans données nominatives) | Profil client anonymisé | Trimestrielle | Praticien + Admin agrégé |
| **Région géographique dominante** | Provinces ou régions représentées dans la clientèle active, agrégées | Profil client anonymisé | Trimestrielle | Admin agrégé + Public anonymisé |
| **Langue de service** | Proportion lectures livrées en français vs autre langue | Métadonnées lecture | Mensuelle | Praticien + Admin |
| **Parcours client typique** | Séquence modale : nombre de séances, espacement, thèmes évoluant entre la 1re et la 3e lecture | Historique client agrégé par praticien | Trimestrielle | Praticien + Admin |
| **Taux de première séance unique** | % de clients n'ayant fait qu'une seule séance avec ce praticien — distingue "expérimentation" de "suivi" | Historique client | Trimestrielle | Praticien + Admin |

---

### D. SANTÉ DU PRATICIEN

| Indicateur | Définition | Source | Fréquence | Visibilité |
|---|---|---|---|---|
| **Charge hebdomadaire en lectures** | Nombre de lectures produites par semaine glissante | Calendrier + livraisons | Hebdomadaire | Praticien + Admin |
| **Délai moyen de production** | Temps écoulé entre la réception d'un dépôt client et la livraison de la lecture audio | Métadonnées plateforme | Par lecture | Praticien + Admin |
| **Jours consécutifs sans livraison** | Nombre de jours depuis la dernière lecture livrée, hors congé déclaré | Métadonnées plateforme | Temps réel | Admin seul (si > seuil) |
| **Mode calme activé** | Indicateur booléen : le praticien a mis son calendrier en pause volontaire (mode "recharge") | Action praticien dans dashboard | Temps réel | Praticien + Admin |
| **Variation du temps moyen de lecture produite** | Durée audio moyenne par lecture sur 30 jours vs les 30 jours précédents — un raccourcissement significatif peut signaler de la fatigue | Métadonnées audio | Mensuelle | Praticien + Admin |
| **Ratio charge acceptée vs refusée** | Nombre de réservations acceptées vs mises en attente ou refusées dans un mois | Calendrier | Mensuelle | Praticien + Admin |
| **Autoévaluation mensuelle du praticien** | Score subjectif (1-5) que le praticien entre lui-même sur son état général : énergie, clarté, plaisir du travail | Formulaire autoévaluation mensuel | Mensuelle | Praticien seul + Admin si dégradation prolongée |
| **Tendance qualitative auto-déclarée** | Commentaire libre mensuel du praticien sur ce qui l'anime ou le pèse dans sa pratique IVIA | Autoévaluation | Mensuelle | Praticien seul |

---

### E. ALIGNEMENT DOCTRINAL

| Indicateur | Définition | Source | Fréquence | Visibilité |
|---|---|---|---|---|
| **Orientation autonomie vs dépendance** | % des lectures contenant des formulations qui orientent le client vers sa propre capacité de discernement vs formulations qui suggèrent de revenir "pour obtenir une réponse" | Grille de lecture manuelle ou assistée | Trimestrielle | Admin + Praticien |
| **Vocabulaire IVIA vs vocabulaire déviant** | Présence ou absence de termes incompatibles avec la charte (ex. : prédiction, guérison garantie, canal divin exclusif) dans les lectures produites | Vérification par écoute aléatoire ou traitement textuel d'une transcription | Par audit | Admin seul |
| **Cohérence avec la charte éthique** | Score issu d'une révision semestrielle : le praticien respecte-t-il les 5 engagements éthiques IVIA signés à l'intégration | Audit interne IVIA | Semestrielle | Admin + Praticien |
| **Signalements client** | Nombre de signalements volontaires d'un client indiquant un inconfort ou un franchissement de limite perçu | Formulaire client anonyme | Temps réel | Admin seul |
| **Renouvellement de l'engagement éthique** | Confirmation annuelle par le praticien qu'il a relu et accepte la charte en vigueur | Action praticien | Annuelle | Admin |
| **Proportion lectures livrées dans les délais engagés** | % des lectures produites dans le délai de 72h standard IVIA | Métadonnées plateforme | Mensuelle | Praticien + Admin |

---

### F. IMPACT CLIENT

| Indicateur | Définition | Source | Fréquence | Visibilité |
|---|---|---|---|---|
| **Évolution autodéclarée séance à séance** | Le client indique avant chaque nouvelle séance s'il perçoit un mouvement (clarification, apaisement, remise en question) depuis la précédente lecture | Formulaire pré-dépôt | Par séance | Praticien + Admin agrégé |
| **Atteinte d'un repère concret** | Le client coche en fin de parcours s'il a identifié un point d'ancrage, une décision ou une posture nouvelle suite aux lectures | Formulaire de clôture de parcours | En fin de parcours | Praticien + Admin agrégé |
| **Interruption réfléchie vs abandon** | Distinction entre un client qui indique mettre son parcours en pause consciemment et un client qui ne revient pas sans signalement | Formulaire de fin + absence de connexion | 90 jours post dernière séance | Admin |
| **Durée médiane d'un parcours IVIA** | Nombre de semaines entre la première et la dernière lecture, par praticien, agrégé | Historique client | Trimestrielle | Praticien + Admin |
| **Thème de clôture autodéclaré** | Dernier thème ou intention exprimée par le client à la fin de son parcours — permet de cartographier ce que les gens "emportent" | Formulaire de clôture | En fin de parcours | Praticien + Admin agrégé |
| **NPS praticien** | Score de recommandation simple (0-10) : "Recommanderiez-vous ce praticien à quelqu'un qui cherche un accompagnement?" | Formulaire retour client | Après séance 2+ | Praticien + Admin |

---

## 3. Alertes automatiques

Les règles suivantes déclenchent une notification interne sans caractère disciplinaire. Toute alerte envoyée au praticien est une "alerte douce" (signal de soin). Une alerte envoyée à l'admin sans notification praticien est une "alerte discrète" (signal de veille).

1. **Délai de production critique** — Si le délai moyen de production dépasse 96h sur 3 lectures consécutives sans que le mode calme soit activé : alerte douce praticien + alerte discrète admin.

2. **Inactivité prolongée** — Si aucune lecture n'est livrée depuis 14 jours calendrier sans congé déclaré : alerte discrète admin avec suivi humain (message bienveillant, pas de procédure).

3. **Chute de note client** — Si la note moyenne du praticien descend sous 3,5/5 sur 5 lectures consécutives : alerte douce praticien + revue interne admin sans divulgation publique.

4. **Signalement client reçu** — Tout signalement client déclenche immédiatement une alerte discrète admin, sans notification praticien, avec mise en attente de nouvelles réservations jusqu'à clarification.

5. **Autoévaluation praticien critique** — Si le praticien soumet un score d'autoévaluation de 1 ou 2 deux mois consécutifs : message personnalisé de l'équipe IVIA, offre de supervision ou de pause, aucune donnée visible par d'autres praticiens.

6. **Taux d'occupation supérieur à 90% pendant 6 semaines** — Risque de surbooking et d'épuisement : alerte douce praticien lui suggérant d'activer le mode calme ou d'ajuster ses plages.

7. **Terme doctrinal déviant détecté** — Si un audit décèle dans une lecture produite un terme explicitement exclu par la charte (ex. : "guérison certaine", "prédiction", "channeling") : alerte discrète admin, révision de la lecture, contact discret avec le praticien avant toute suite.

8. **Taux de re-réservation sous 15% pendant 2 trimestres consécutifs** — Signal que les clients ne reviennent pas, possible inadéquation entre l'offre du praticien et les besoins de la clientèle IVIA : alerte douce praticien avec invitation à un appel de calibration avec l'équipe.

9. **NPS praticien inférieur à 6 sur 10 séances consécutives** — Alerte douce praticien + revue interne admin, proposition de supervision pairée avec un praticien expérimenté.

10. **Ratio lectures orientées dépendance > 30%** — Si l'audit doctrinal trimestriel révèle qu'une proportion significative des lectures produit des formulations orientant vers la dépendance plutôt que l'autonomie : alerte discrète admin + conversation de calibration doctrinale avec le praticien.

---

## 4. Vues dashboard

### Vue PRATICIEN — Son propre tableau de bord

Le praticien accède à un espace personnel structuré en trois zones.

**Zone 1 — Activité récente** : Lectures livrées cette semaine, prochains dépôts attendus, délai de production actuel, plages disponibles ce mois. Un indicateur visuel simple (vert / jaune / rouge) reflète sa charge actuelle par rapport à sa capacité déclarée.

**Zone 2 — Santé de sa pratique** : Note moyenne sur les 30 derniers jours, taux de re-réservation sur 90 jours, évolution de la durée moyenne de ses lectures, mots-clés positifs les plus fréquents dans les retours clients. Son autoévaluation mensuelle y est aussi visible sous forme de courbe personnelle — pour lui seul.

**Zone 3 — Finances** : Revenu net du mois, projection sur 30 jours selon l'occupation actuelle, panier moyen, comparaison aux 3 mois précédents. Aucune donnée financière de ses pairs n'est accessible ni visible.

Le praticien peut à tout moment activer le mode calme (calendrier en pause) directement depuis ce tableau, et accéder à un journal libre non mesuré — espace pour noter ce qu'il traverse, hors toute métrique.

### Vue ADMIN — Un praticien spécifique

L'équipe IVIA accède à une fiche praticien qui agrège les données des six catégories, sans les données financières nettes individuelles (visible au praticien seul). La vue admin inclut : délai de production actuel et historique 90 jours, taux de satisfaction client, indicateurs de santé du praticien (charge, autoévaluation si dégradation déclarée), résultat du dernier audit doctrinal, historique des alertes déclenchées, et profil de la clientèle agrégée. Tout accès admin à cette fiche est journalisé. Un praticien peut demander à tout moment un rapport de ce que l'admin voit de lui.

### Vue ADMIN — Réseau global

Un tableau de bord collectif exposant la santé agrégée du réseau sans identifier aucun praticien individuellement. Indicateurs clés : nombre de praticiens actifs ce mois, délai de production moyen du réseau, taux de satisfaction moyen réseau, nombre de praticiens en mode calme actif, alertes ouvertes non résolues par catégorie, motifs de dépôt les plus fréquents sur l'ensemble de la plateforme, répartition géographique des clients, évolution du revenu total distribué aux praticiens (masse salariale collective). Cette vue permet à David d'évaluer la santé du réseau pour décisions éditoriales, de recrutement et de partenariat.

---

## 5. Dashboard public anonymisé IVIA

Ce tableau de bord, accessible depuis le site principal d'IVIA sans authentification, publie des données agrégées en temps réel ou à fréquence hebdomadaire. Son rôle est de démontrer que la plateforme est vivante, cohérente et à impact — pas de recruter.

**Données exposées :**
- Nombre de personnes accompagnées ce mois (total lectures livrées, pas clients uniques pour protéger les retours multiples)
- Nombre de praticiens actifs ce mois
- Régions représentées dans la clientèle (ex. : Montréal, Québec, Outaouais, Ontario, France — sans granularité inférieure à la province/pays)
- Motifs d'accompagnement les plus fréquents du mois, sous forme de nuage de termes agrégés et anonymisés (ex. : "transition", "épuisement", "relation", "décision") — jamais de contenu verbatim d'un dépôt client
- Taux de satisfaction global (note moyenne toutes lectures confondues, arrondie)
- Durée médiane d'un parcours d'accompagnement IVIA (en semaines)
- Nombre de lectures produites depuis la création de la plateforme (compteur cumulatif)

**Ce qui n'apparaît jamais :** noms, identifiants, localisation précise, contenu audio, motifs individuels, données financières de praticiens.

Ce tableau est conçu conformément à l'article 12 de la *Loi modernisant des dispositions législatives en matière de protection des renseignements personnels* (Loi 25, L.R.Q. c. P-39.1) qui requiert que toute utilisation de données personnelles soit limitée aux fins pour lesquelles elles ont été collectées, et à l'article 23 qui permet la conservation de données anonymisées au-delà de la durée de la relation, à condition que l'anonymisation soit irréversible.

---

## 6. Rapport trimestriel d'impact

**Fréquence** : Publication aux mois de janvier, avril, juillet et octobre — couvrant le trimestre précédent.

**Destinataires cibles** : CIUSSS, OPQ (à titre d'information, sans prétention à l'acte réservé), employeurs partenaires potentiels (PAE, assureurs), investisseurs en économie sociale, médias spécialisés (psychologie, bien-être, travail).

**Contenu du rapport** :

1. **Données d'activité** — Lectures produites, clients accompagnés (agrégé), praticiens actifs, régions couvertes, évolution vs trimestre précédent.

2. **Indicateurs de qualité** — Taux de satisfaction moyen, taux de re-réservation, durée médiane des parcours, proportion de parcours clôturés de façon réfléchie.

3. **Portrait des motifs d'accompagnement** — Cartographie thématique anonymisée des besoins exprimés. Section narrative expliquant ce que la plateforme "entend" dans le collectif à ce moment précis, sans aucun verbatim.

4. **Santé du réseau praticien** — Nombre de praticiens en activité, répartition par ancienneté, taux de rétention praticien, nombre d'alertes résolues sans rupture de pratique.

5. **Déclaration doctrinale** — Un paragraphe signé par David rappelant les principes IVIA, la distinction avec les soins réglementés, et l'engagement de la plateforme envers l'autonomie du client. Renouvelé et actualisé à chaque trimestre.

6. **Perspectives** — Ce que la prochaine période prévoit : nouvelles régions, évolutions de l'offre, formations praticiens, partenariats en développement.

**Ton** : Sobre, factuel, sans marketing. Première personne du pluriel institutionnel ("IVIA a accompagné", "les praticiens ont produit"). Jamais de superlatifs. La preuve remplace l'argument.

**Format** : PDF publié sur le site, en accès libre, sans formulaire. Archivé dans un espace "Rapports" permanent.

---

## 7. Connexion contenu éditorial

Chaque mois, les données agrégées de la plateforme alimentent directement la stratégie de contenu IVIA selon le pipeline suivant.

**Étape 1 — Extraction (J-5 du mois)** : L'admin extrait du tableau de bord réseau les 3 à 5 motifs d'accompagnement les plus fréquents du mois écoulé. Cette extraction est anonymisée, aucun contenu de dépôt client n'est utilisé verbatim. Les mots-clés positifs les plus fréquents dans les retours clients sont aussi extraits.

**Étape 2 — Lecture doctrinale (J-4)** : David (ou un praticien senior désigné) lit ces motifs et identifie lequel résonne le plus avec un besoin collectif réel, une question que la bibliothèque IVIA n'a pas encore traitée, ou un malentendu fréquent sur la pratique d'écoute. Ce choix est documenté dans un journal éditorial interne avec la justification doctrinale.

**Étape 3 — Attribution et production (J-3 à J-1)** : Le sujet est attribué à un rédacteur (David lui-même, un praticien volontaire, ou un collaborateur externe briefé sur la doctrine). Le brief inclut obligatoirement : le motif source anonymisé, l'angle doctrinal souhaité, les termes à éviter, et le registre de langue (québécois, accessible, non thérapeutique dans le sens clinique).

**Étape 4 — Validation (J-1)** : Tout contenu est relu par David ou un praticien senior avant publication pour vérifier la cohérence doctrinale. Un contenu qui présente IVIA comme une alternative aux soins de santé est systématiquement refusé, même s'il est bien écrit.

**Étape 5 — Diffusion (J)** : L'article intègre la bibliothèque du site. Une version courte devient un post Instagram (sans photo de client, sans citation). Un angle audio devient un épisode ou extrait podcast si la thématique s'y prête.

**Fréquence** : Un article bibliothèque par mois minimum. Un post Instagram par semaine, dont au moins un par mois issu directement des données de la plateforme. Un épisode podcast par trimestre ancré dans les motifs observés.

---

## 8. Gouvernance des données

**Principe directeur** : Chaque acteur possède ses propres données. IVIA possède l'agrégat, pas les données individuelles.

**Le client** : Accès complet à son historique de dépôts, ses lectures reçues, ses retours soumis. Peut demander la suppression totale de son dossier en vertu de l'article 28 de la *Loi 25* (droit à la déindexation et à la suppression). Ses données ne sont jamais transmises au praticien sous forme nominative au-delà du cadre de la séance en cours. L'audio déposé est détruit selon un calendrier défini dans la politique de conservation, conformément à l'article 23 de la *Loi 25*.

**Le praticien** : Accès complet à ses propres indicateurs (toutes les catégories A à F le concernant). Peut exporter ses données à tout moment dans un format portable. Ses données financières individuelles ne sont jamais partagées avec d'autres praticiens ni avec des partenaires externes. À son départ de la plateforme, ses données d'activité sont anonymisées et agrégées dans les archives IVIA; ses données personnelles sont supprimées dans les 30 jours.

**IVIA (admin)** : Accède aux données agrégées de l'ensemble du réseau et aux fiches praticiens dans le cadre de la gestion de la plateforme (santé du réseau, conformité doctrinale, sécurité). N'accède aux données individuelles d'un praticien que dans le cadre d'une alerte ou d'un audit documenté. Tout accès admin aux données individuelles est journalisé et accessible au praticien concerné sur demande.

**La communauté / le public** : Accède uniquement aux données du tableau de bord public anonymisé (section 5). Aucune donnée permettant l'identification directe ou indirecte d'un client ou d'un praticien n'est publiée.

**Loi 25 — points d'application directs** : Consentement granulaire collecté à l'intégration du client et du praticien (article 12 — utilisation limitée aux fins déclarées). Responsable de la protection des renseignements désigné nommément (article 3.1). Politique de confidentialité publiée, mise à jour annuellement. Évaluation des facteurs relatifs à la vie privée (EFVP) réalisée avant tout nouveau module de collecte de données (article 3.3). La *charte_transformation_donnees* existante dans le dépôt MERLIN constitue le document de référence complémentaire — le présent document s'y arrime sans le remplacer.

---

*Document vivant — révision prévue à chaque mise en production d'un nouveau module de la plateforme. Toute modification aux catégories d'indicateurs ou aux règles d'alerte requiert validation de David Beaupré.*

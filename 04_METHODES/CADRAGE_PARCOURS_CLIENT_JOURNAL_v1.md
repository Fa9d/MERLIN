# Cadrage parcours client et journal IVIA — Version 1

**Document de conception interne**
**Auteur : système MERLIN — David Beaupré, fondateur IVIA**
**Date : mai 2026**
**Statut : document vivant — fondateur d'une série de briefs Copilot et d'une mise à jour BP v2.3**

---

## 1. Préambule — Intention du fondateur, restitution fidèle

Le présent cadrage découle d'une instruction verbatim du fondateur, reproduite intégralement ci-dessous pour qu'aucune interprétation ne s'y substitue.

> "Pour devenir client, déjà venir sur la page et demander une connexion. Au clic, passage sur usuelle page de demande d'adhésion. Nom Prénom Courriel Tel - Log et MDP. Confirmation immédiate avec accès sans attente de confirmation par courriel. Comme cela se fait souvent et donc si la personne n'a pas vérifié ses messages, à sa prochaine tentative de connexion, on lui dira d'aller dans ces messages confirmer son compte et à ce moment seulement elle pourra intégrer son espace client. A savoir, donc, l'accès immédiat n'est pas une faille. Tu dois traiter qu'il n'y ait pas de possibilité d'abus. On facilite l'accès pour ne pas frustrer le client et qu'il ait accès au contenu rapidement et qu'ultérieurement il puisse valider au moment qui lui convient. Exception faite de ses achats. Dès sa première connexion nous lui proposons d'accéder au site ou de remplir le formulaire afin d'en apprendre plus sur ses besoins, ses sentiments, ses humeurs ou ses problèmes. Bref tout ce pourquoi il cherche de l'aide. Un formulaire que tu cibleras en fonction des besoins que tu justifies de part notre positionnement en tant que praticien aidant et accompagnant. Ce client doit avoir accès aux disponibilités des praticiens, à tous les contenus et son espace d'écoute et de compte rendu. De cette facon il peut revenir courrament et au besoin refaire le point et à terme, voir son historique et le consulter, considerer ses victoires et ces revers, ces grands changements, ces adaptations. Puis, une section journal est très importante et contribuera aux analyses et appréciations du praticien. Le traitement de ces textes étant modique, nous pouvons l'intégrer dans une commune mesure gratuite jusqu'à un certain point. Nous devons inclure dans notre plan financier cette ajout et déterminer les seuils de gratuité. Si nous considérons que les frais de traitement de ces productions apportent plus qu'elles ne coutent, peut-être pourrions nous les rétribuer d'une certaine facon ou les ingérer dans la transcription qui suit la rédaction de ces textes ? On ramène alors la temporalité des processus. Dans les fais, si les dates des faits évoqués ne respectent pas la chronologie de la vie du client, possible que l'ordre des souvenir évoqués portent un sens qui n'a pas été étudié à ce jour. IVIA doit le faire."

**Ce qui est nouveau dans cette instruction :**

- Le principe d'accès immédiat post-inscription sans blocage courriel (logique de confiance graduée, pas encore formalisée dans les mockups existants)
- Le formulaire d'ancrage initial comme portail d'entrée humain dès la première connexion (absent de `inscription.html`, `dashboard.html`)
- La vision complète de l'espace client comme espace de mémoire vivante (victoires, revers, adaptations, historique)
- La section journal comme outil d'analyse praticien et comme source de données agrégées (non encore formalisé dans `journal.html`, qui présente un journal sans couche analytique)
- La question du modèle économique du journal — gratuité jusqu'à un seuil, puis forfait ou rétribution par contribution aux données agrégées
- L'hypothèse doctrinale originale sur la temporalité décalée des souvenirs évoqués, jamais étudiée ni codifiée nulle part, que IVIA devrait être la première plateforme à mesurer systématiquement

**Ce qui était déjà couvert et s'y arrime sans contradiction :**

- Les trois niveaux de consentement gradué (politique_gouvernance_donnees_agregees_v1, section 4) : la rétribution N3 s'y inscrit directement
- Les cinq strates de données (politique_gouvernance, section 2) : les entrées du journal relèvent de la strate B pour le brut, strate C pour le comportemental individuel, strate D pour l'agrégé anonymisé
- Le principe de mesure pour soutenir, jamais pour surveiller (indicateurs_praticien_v1, section 1) : s'applique intégralement au digest praticien issu du journal
- Les droits d'effacement Loi 25 (politique_gouvernance, section 6) : le journal client est soumis aux mêmes règles que les audios — suppression dans les 30 jours sur demande, conformément à l'article 28 de la Loi modernisant des dispositions législatives en matière de protection des renseignements personnels (L.R.Q. c. P-39.1, ci-après Loi 25)

---

## 2. Principe d'accès gradué — La grande idée

L'accès immédiat post-inscription n'est pas une anomalie de conception. C'est une position intentionnelle qui réduit la friction en première connexion tout en préservant la sécurité pour les actions engageantes. Les quatre phases se déroulent comme suit.

**Phase 1 — Inscription minimaliste.**
Le client remplit cinq champs (prénom, nom, courriel, téléphone, mot de passe), coche les consentements requis, et clique sur "Créer mon espace". Aucun code de vérification n'est exigé avant l'accès. Un courriel de confirmation est envoyé en parallèle en arrière-plan. La session s'ouvre immédiatement.

**Phase 2 — Session courante libre.**
Pendant la session d'inscription, l'utilisateur peut naviguer dans l'ensemble de l'espace client : consulter les praticiens et leurs disponibilités, lire la bibliothèque de contenus, accéder au formulaire d'ancrage initial, ouvrir son journal. Aucune action n'est bloquée, sauf les achats et réservations (voir phase 4).

**Phase 3 — Blocage doux à la deuxième connexion si courriel non validé.**
À la déconnexion et à toute tentative de reconnexion ultérieure, si l'adresse courriel n'a pas encore été confirmée, la page de connexion affiche un message doux, non anxiogène : "Avant de continuer, confirmez votre courriel. Nous avons envoyé un lien à xxxx@xxx.xx — vérifiez aussi vos indésirables. Pas encore reçu ? Renvoyer le lien." Ce blocage doux est la seule friction introduite, et elle intervient après que le client ait déjà vécu l'espace IVIA.

**Phase 4 — Achats et réservations bloqués tant que courriel non validé.**
Toute tentative de réservation d'une séance, d'achat d'un forfait ou de dépôt d'un enregistrement audio déclenche un message explicite : "Pour finaliser, confirmez d'abord votre courriel — c'est notre façon de nous assurer que vous pouvez recevoir la réponse de votre praticien." Cette limite s'applique même en première session. La raison est pratique autant que sécuritaire : un échange audio suppose une adresse courriel fonctionnelle.

Ce design respecte deux principes simultanément : la non-frustration du client et la non-exposition de la plateforme aux abus d'achats ou de réservations frauduleuses.

---

## 3. Analyse des risques d'abus et leurs mitigations

L'accès immédiat crée des vecteurs d'exploitation qu'il faut anticiper explicitement.

**A. Création de comptes en masse par des robots.**
Mitigation : captcha invisible (hCaptcha ou Cloudflare Turnstile) intégré au formulaire d'inscription — transparent pour un humain, bloquant pour un bot. Limite de taux IP : pas plus de 3 créations de compte par adresse IP en 30 minutes. Ces contrôles s'appliquent à l'inscription, pas plus tard, ce qui est le moment où ils sont efficaces.

**B. Faux courriels jetables.**
Mitigation : vérification MX au moment de la soumission (si le domaine saisi ne possède pas d'enregistrement MX valide, le formulaire refuse sans explication technique — message : "Cette adresse ne semble pas valide. Essayez une autre."). Liste de domaines jetables connus (mailinator, guerrillamail, etc.) maintenue et mise à jour mensuellement.

**C. Usurpation d'identité.**
La validation courriel reste obligatoire avant tout achat ou réservation. Un imposteur ne peut pas finaliser de transaction sans accéder à la boîte courriel de la victime. Le risque résiduel est le même que pour tout service en ligne.

**D. Spam de dépôts audio ou d'entrées journal gratuites.**
Mitigation : quotas par compte (voir section 7F pour le journal, section 4 pour les dépôts audio). Les quotas s'appliquent même en session non-validée pour le contenu gratuit.

**E. Comptes jamais validés qui persistent dans la base de données.**
Risque de conformité sous la Loi 25, article 14 (consentement manifeste et éclairé) et article 23 (obligation de détruire les renseignements personnels lorsqu'ils ne sont plus nécessaires à la fin pour laquelle ils ont été collectés). Mitigation : règle d'auto-suppression à 30 jours — tout compte dont l'adresse courriel n'a pas été confirmée dans les 30 jours est automatiquement supprimé. Un rappel courriel est envoyé à J-7 et à J-1 avant la suppression. Le log de suppression est conservé sous forme d'entrée anonymisée (date, raison) pour audit interne.

**F. Récupération de mot de passe si courriel jamais validé.**
Flux spécial : la demande de réinitialisation de mot de passe déclenche obligatoirement la validation de l'adresse courriel en même temps. L'utilisateur ne peut pas récupérer l'accès sans valider. Ce flux empêche l'exploitation du "mot de passe perdu" comme porte dérobée.

La Commission d'accès à l'information (CAI) du Québec recommande que tout mécanisme d'authentification soit proportionné à la sensibilité des données traitées. IVIA traite des données de nature sensible (motifs personnels, états émotionnels). L'obligation de validation courriel avant achat est cohérente avec cette recommandation.

---

## 4. Formulaire d'inscription — Champs et flux exacts

**Champs obligatoires :**

- Prénom (utilisé pour s'adresser à la personne — pas nécessairement le nom légal, comme précisé dans le mockup `inscription.html`)
- Nom de famille
- Courriel (identifiant unique de connexion — pas de pseudo séparé : le courriel est plus robuste, moins susceptible d'être oublié, et permet la validation)
- Téléphone (recommandé obligatoire pour deux raisons opérationnelles : rappel SMS avant une séance, et canal d'alerte si le praticien a une préoccupation urgente à communiquer. Intitulé "Numéro de téléphone — pour vos rappels de rendez-vous" afin que la raison soit transparente conformément à l'article 8 de la Loi 25 qui exige que la personne soit informée de la finalité de chaque collecte)
- Mot de passe (règle NIST SP 800-63B : minimum 12 caractères, pas de complexité forcée obligatoire — une phrase longue est aussi solide qu'un mot de passe fragmenté. Indication à l'écran : "Choisissez une phrase dont vous vous souviendrez — au moins 12 caractères.")

**Consentements (cases à cocher distinctes, non pré-cochées sauf N1) :**

- Case N1 — Obligatoire (pré-cochée, décochable seulement si le client ne souhaite pas s'inscrire) : "J'accepte qu'IVIA conserve les renseignements nécessaires à mon compte (courriel, historique de séances) et les partage avec la personne praticienne qui m'accompagne, uniquement pour la durée de mes séances." Liens directs vers les CGU et la politique de confidentialité Loi 25.
- Case N2 — Opt-in, non cochée par défaut : texte verbatim issu de la politique_gouvernance_donnees_agregees_v1, section 4, Niveau 2.
- Case N3 — Opt-in, non cochée par défaut : texte verbatim issu de la politique_gouvernance_donnees_agregees_v1, section 4, Niveau 3.

**Bouton de soumission :** "Créer mon espace" (vocabulaire IVIA, déjà présent dans `inscription.html` — à conserver).

**Confirmation immédiate post-inscription :** redirection vers le dashboard avec un bandeau persistant en haut de page, non fermable, discret mais visible : "Votre espace est ouvert. Pour prendre rendez-vous, confirmez votre courriel — lien envoyé à xxxx@xxx.xx." Ce bandeau disparaît dès que la validation est complétée.

**Ce qui change par rapport au mockup actuel (`inscription.html`) :** ajout du champ Nom, du champ Téléphone, et des trois cases de consentement graduées N1/N2/N3. Ajout du captcha invisible. Mise à jour de la règle de mot de passe (10 caractères actuellement → 12 caractères). Redirection post-soumission vers `dashboard.html` plutôt que vers `verifier-courriel.html` (la vérification courriel n'est plus un prérequis bloquant à l'accès).

---

## 5. Formulaire d'ancrage initial — "Ce que vous portez en arrivant"

Dès la première connexion, avant que le client n'explore librement, une page interstitielle lui est proposée. Elle n'est pas obligatoire. Le client peut choisir "Explorer d'abord" pour aller directement au dashboard.

**Nom du formulaire :** "Ce que vous portez en arrivant" (vocabulaire IVIA, non clinique, évite les termes "évaluation", "bilan" ou "questionnaire" qui induisent un rapport médical).

**Justification doctrinale :** ce formulaire n'est pas un outil diagnostique. C'est une porte d'entrée relationnelle. Il permet que la première séance ne commence pas à zéro — le praticien qui accueille ce client arrive avec un contexte humain, pas une fiche administrative. Cohérent avec le positionnement praticien aidant et accompagnant, non clinique.

**Durée estimée :** cinq à sept minutes.

**Questions proposées (6 questions) :**

**Q1 — Ce qui vous amène aujourd'hui** (texte libre, 50 à 300 mots)
*"Qu'est-ce qui vous a amené à ouvrir cette porte aujourd'hui ? Il n'y a pas de bonne réponse — décrivez ce qui vous traverse, même si c'est vague."*
Justification : ancre le contexte de départ. Constitue la donnée de strate C la plus directement utile au praticien.

**Q2 — Comment vous décrieriez votre état général en ce moment** (échelle visuelle à 5 niveaux verbalisés, sans chiffres)
Les cinq options : "submergé·e" — "tendu·e" — "stable" — "en mouvement" — "ressourcé·e"
Justification : une échelle verbalisée est plus honnête qu'une échelle numérique. Elle situe l'état sans le réduire à un score. Ces cinq états forment un spectre cohérent avec le vocabulaire IVIA.

**Q3 — Y a-t-il un registre parmi ceux-ci qui résonne pour vous** (cocher 1 à 3 parmi une liste)
Options : Présence — Sommeil — Clarté — Relation — Transition — Corps — Mémoire — Reconnaissance — Ancrage
Justification : ces registres correspondent aux thèmes d'accompagnement les plus fréquents observés dans les pratiques d'écoute non clinique. Ils alimentent le pipeline éditorial mensuel (indicateurs_praticien_v1, section 7) et permettent au praticien de cibler son écoute initiale.

**Q4 — Préférences pour la première rencontre** (choix unique)
Options : "Je préfère d'abord envoyer un enregistrement audio" — "Je préfère une rencontre synchrone en direct" — "Je verrai selon les disponibilités"
Justification : IVIA offre les deux modalités. Connaître la préférence en amont oriente le praticien vers le bon format et évite une friction organisationnelle en première séance.

**Q5 — Quelque chose qu'il vous semble important de mentionner avant de rencontrer un praticien** (texte libre, optionnel, 0 à 200 mots)
*"Y a-t-il quelque chose qu'un praticien devrait savoir sur vous ou sur votre situation avant de vous rencontrer pour la première fois ?"*
Justification : espace de sécurité pour les contextes particuliers (situation de deuil récent, antécédents de relation difficile avec un accompagnant, préférences de style d'écoute). Non obligatoire pour ne pas anxiogéniser la démarche.

**Q6 — Comment avez-vous entendu parler d'IVIA** (menu déroulant)
Options : Recommandation d'un proche — Médias sociaux (lequel ?) — Article ou balado — Professionnel de la santé — Recherche en ligne — Autre
Justification : donnée d'acquisition essentielle pour le pipeline marketing et pour évaluer quels canaux amènent les clients qui restent. Données agrégées sous strate D — jamais individualisées dans les rapports.

**Données collectées et classification :**
Les réponses aux questions Q1 à Q5 constituent des données de strate C (comportementales individuelles, accessibles au praticien assigné avec consentement N1). La réponse à Q6 est une donnée d'acquisition agrégée (strate D, anonymisée pour le dashboard réseau). Le formulaire complet, une fois rempli, est accessible au praticien qui accompagne le client — et seulement à lui.

---

## 6. Espace client — Sections et logique d'accès

L'espace client est conçu comme une mémoire vivante, pas comme un portail transactionnel. Sept sections principales.

**Mon parcours** — historique chronologique de toutes les séances, lectures audio reçues, retours soumis. Chaque séance peut être marquée selon trois statuts : "intégré", "à réécouter", "interrompu". Le client peut annoter chaque séance. À terme (horizon 6 mois de données), une vue "Mes grandes lignes" apparaît : victoires identifiées, revers nommés, grands changements, adaptations notées. Cette vue est rétrospective et appartient entièrement au client.

**Mes rendez-vous** — calendrier des disponibilités praticiens, réservations actives, historique des annulations. Réservation bloquée tant que courriel non validé (conformément au principe d'accès gradué, section 2, phase 4).

**Mon journal** — section dédiée, détaillée à la section 7.

**Bibliothèque** — accès à tous les contenus textuels IVIA. Pas de paywall sur le contenu textuel. Le modèle économique d'IVIA repose sur les séances, pas sur l'accès à l'information.

**Mes praticiens** — liste des praticiens avec qui le client a travaillé, possibilité de revenir vers le même praticien, fiche minimaliste de chaque praticien (spécialités déclarées, style d'écoute, disponibilités).

**Mes paramètres et mes données** — droit à l'effacement complet (Loi 25, art. 28 et 28.1), export des données personnelles (Loi 25, art. 27 — droit à la portabilité, en vigueur depuis septembre 2024), modification des coordonnées, changement de mot de passe.

**Mes consentements** — tableau de bord des trois niveaux N1/N2/N3, modifiables à tout moment. Chaque modification est horodatée dans le registre interne conformément aux obligations de reddition de comptes de la Loi 25 (art. 3.2).

---

## 7. Journal client — Vision complète

### A. Principe

Le journal est un espace volontaire d'écriture libre. Ce n'est pas un substitut de séance. Ce n'est pas un formulaire clinique. C'est un endroit où le client dépose ce qu'il traverse, à son rythme, entre les séances ou indépendamment d'elles. Ce qui s'y écrit nourrit l'écoute du praticien, avec consentement explicite, sans qu'il ait à le lire systématiquement. C'est l'agent IVIA qui produit un digest synthétique.

Le journal existe pour que le client puisse "revenir couramment et au besoin refaire le point, et à terme voir son historique et le consulter, considérer ses victoires et ses revers, ses grands changements, ses adaptations", selon les mots du fondateur.

### B. Structure d'une entrée

Chaque entrée du journal comprend les éléments suivants.

- **Date d'écriture** — saisie automatique, non modifiable
- **Date évoquée** — champ optionnel rempli par le client si le contenu de l'entrée porte sur un événement ou une période qui n'est pas le présent immédiat. C'est ici que naît la temporalité décalée décrite à la section C.
- **Titre** — optionnel, 80 caractères maximum
- **Corps de l'entrée** — texte libre. Pas de limite stricte. Affichage progressif au-delà de 2000 mots (bouton "Voir la suite" pour éviter une page trop chargée visuellement).
- **Mode d'entrée** — texte écrit ou enregistrement vocal (voix-journal). Si enregistrement vocal : transcription automatique optionnelle, activable par le client.
- **Tags émotionnels** — le client peut choisir jusqu'à 3 tags parmi une liste IVIA non clinique : "lourd", "léger", "lumineux", "embrouillé", "mouvement", "blocage", "gratitude", "perte", "victoire", "doute". Ces tags ne sont pas des diagnostics. Ils sont des matières d'attention pour le praticien et pour les analyses agrégées.
- **Niveau de partage** — par défaut, l'entrée est visible uniquement par le client et par le praticien qui l'accompagne actuellement, pour les entrées des 30 derniers jours uniquement. Le client peut épingler une entrée comme "à partager avec mon praticien" pour la rendre accessible hors de cette fenêtre de 30 jours. Le client peut également marquer une entrée "Privée — pour moi seulement", auquel cas aucun praticien ne peut y accéder.
- **Édition et suppression** — le client peut éditer ou supprimer toute entrée à tout moment.

Le mockup actuel (`journal.html`) présente un journal sans date évoquée, sans tags, sans mode vocal et sans indicateur de partage. Ces éléments sont à ajouter intégralement.

### C. Innovation doctrinale — Temporalité décalée

Le fondateur formule une hypothèse originale, reproduite verbatim : "Si les dates des faits évoqués ne respectent pas la chronologie de la vie du client, possible que l'ordre des souvenirs évoqués portent un sens qui n'a pas été étudié à ce jour. IVIA doit le faire."

Cette hypothèse mérite d'être formalisée comme un indicateur doctrinal.

**Définition de la temporalité décalée :** écart entre la date d'écriture d'une entrée de journal et la date de l'événement ou de la période que cette entrée évoque. Exemple : un client écrit le 14 mai 2026 une entrée qui porte sur un événement de l'été 2019. L'écart est de sept ans. Ce n'est pas une anomalie — c'est une information.

**Cartographie chronologique double :** deux axes coexistent pour chaque entrée qui contient une date évoquée.
- Axe d'écriture : quand le souvenir a émergé à la surface.
- Axe vécu : quand l'événement a eu lieu selon le client.

**Visualisation pour le client :** une "ligne de vie" dans la section Mon parcours, sur laquelle les entrées apparaissent à leurs deux positions temporelles avec un trait reliant les deux. Le client peut ainsi voir visuellement quels souvenirs remontent à la surface, dans quel ordre, et depuis quelle profondeur temporelle. Cette visualisation lui appartient.

**Pour le praticien (avec consentement N2 du client) :** le digest mensuel produit par l'agent IVIA inclut, si des données de temporalité décalée existent, une note sur les patterns observés : long écart moyen (travail mémoriel actif), cluster d'événements d'une même période (réintégration d'une phase de vie), progression ou régression dans le temps évoqué (mouvement ou fixation). Ces patterns sont présentés comme des "matières d'attention" en termes chaleureux, jamais comme des diagnostics.

**Pour la recherche agrégée IVIA (avec consentement N3 du client) :** le signal de temporalité décalée est agrégé anonymement sur l'ensemble de la base de clients actifs ayant consenti. À terme, cet indicateur pourrait devenir un contributeur à la taxonomie IVIA des motifs d'accompagnement — la strate E de la politique de gouvernance. IVIA serait la première plateforme d'écoute à mesurer ce signal de façon systématique.

**Cohérence éthique absolue :** ces patterns ne sont jamais interprétés comme diagnostic. Ils ne sont pas communiqués au client de façon prescriptive. Ils sont des matières d'attention pour le praticien, qui les utilise ou non selon sa propre lecture clinique non-clinique.

### D. Traitement technique

- Stockage chiffré au repos, cohérent avec les obligations de sécurité de la Loi 25 (art. 3.4 — mesures de sécurité proportionnées à la sensibilité des données).
- Transcription automatique optionnelle des enregistrements vocaux (activée par le client, pas par défaut).
- Aucune analyse de contenu automatisée sans consentement N2 minimum pour le pattern detection individuel, N3 pour la contribution aux analyses agrégées.
- Pour le praticien : digest mensuel "Évolution du journal" si le client a accordé le consentement N2. Format : trois mots-clés émergents du mois, indication des clusters temporels observés si applicable, ton général en quelques mots (rédigé dans un registre chaleureux et non clinique). Ce digest est produit par l'agent IVIA, pas par lecture directe du praticien.

### E. Modèle économique du journal

**Gratuit jusqu'à :** 50 entrées par mois calendrier ou 50 000 caractères cumulés par mois, selon le seuil atteint en premier. Ces limites sont cohérentes avec un usage humain intense mais pas industriel.

**Au-delà du seuil :** deux options sont proposées au client, sans pression, dans un message doux.

**Option 1 — Forfait "Journal sans limite" :** 7 $ par mois (recommandation après analyse des coûts de traitement estimés à 0,80–1,50 $ par client actif par mois, marge nette cible 40–60 %). Ce forfait couvre le stockage illimité, la transcription vocale illimitée et la génération de digests praticien illimités.

**Option 2 — Rétribution par contribution (idée originale du fondateur) :** si le client consent au niveau N3, il contribue ses données agrégées anonymisées à l'IP collective IVIA. En contrepartie : accès gratuit au journal sans limite. En plus : un crédit utilisable sur ses prochaines séances IVIA, calculé à raison de 1 $ de crédit par tranche de 5 000 caractères contribués au-delà du seuil gratuit mensuel.

**Cohérence avec la politique de gouvernance :** cette rétribution n'est pas de la monétisation des données individuelles brutes — c'est une reconnaissance du temps donné à enrichir l'IP collective (taxonomie, modèles d'interprétation, indicateur de temporalité décalée). Elle est conforme aux principes de la politique_gouvernance_donnees_agregees_v1, section 7, qui exclut toute vente de données individuelles mais autorise la valorisation éthique de la strate E.

**Recommandation de déploiement :** Option 1 disponible dès le pilote. Option 2 introduite après 6 mois, quand la valeur démontrable de l'IP collective peut être communiquée aux clients avec honnêteté.

**Estimation de l'impact financier à 100 clients actifs :** si 30 % des clients dépassent les seuils gratuits, cela représente 30 abonnements à 7 $/mois = 210 $/mois de revenu récurrent de l'option 1. Coût de traitement estimé (transcription, stockage, analyse) : 1,20 $/client/mois en moyenne = 120 $/mois pour 100 clients. Marge brute estimée : 75 % sur les abonnés, environ 45 % sur l'ensemble de la base. Ces estimations sont à intégrer dans la mise à jour du BP v2.2 → v2.3 (chantier séparé, délégué au subagent BP).

### F. Quotas et anti-abus

- 50 entrées par mois ou 50 000 caractères par mois (seuil gratuit, décrit ci-dessus)
- Pas plus de 5 entrées dans une fenêtre de 5 minutes (protection anti-bot et anti-spam, même pour les comptes en règle)
- Taille maximale d'un enregistrement vocal : 15 minutes par entrée
- Si le seuil mensuel est atteint : message doux affiché dans le journal, sans blocage brutal : "Vous avez rempli votre journal avec soin ce mois-ci. Pour continuer sans limite, deux options s'offrent à vous." Le client peut alors choisir, ou simplement attendre le début du mois suivant.

---

## 8. Intégration avec les praticiens — Comment le journal nourrit la pratique

Le praticien ne lit pas systématiquement le journal de ses clients. Ce n'est pas son rôle, et ce n'est pas souhaitable doctrinalement. C'est l'agent IVIA qui produit un digest synthétique.

**Avant chaque séance (si consentement N2 du client) :** le praticien reçoit dans sa fiche client un encadré "Journal du dernier mois" contenant : trois mots-clés ou thèmes émergents, indication de la présence ou absence de temporalité décalée (sans contenu textuel), et le tag émotionnel le plus fréquent de la période. Tout est rédigé en vocabulaire IVIA, sans termes cliniques.

**En séance :** le praticien peut inviter le client à partager une entrée s'il le souhaite. "As-tu écrit quelque chose récemment qui t'a marqué ?" Le client choisit librement de répondre ou non, et de partager ou non une entrée spécifique.

**Cohérence avec les indicateurs praticien :** le journal client devient une sixième source pour la catégorie F (Impact client) de la cartographie des indicateurs praticien (indicateurs_praticien_v1, section 2F). Il s'ajoute au formulaire pré-dépôt et au formulaire de clôture sans les remplacer.

**Digest mensuel praticien :** chaque mois, pour chaque client actif ayant accordé le consentement N2, l'agent IVIA produit pour le praticien un rapport de deux paragraphes maximum. Ton : chaleureux, concret, non prescriptif. Exemple : "Ce mois-ci, [prénom] a écrit six entrées. Les thèmes qui reviennent le plus souvent : mouvement, transition, corps. Deux entrées portaient sur des événements anciens — les retours semblent s'ouvrir vers une période passée. Tag dominant : léger."

---

## 9. Implications pour le BP et le pitch

**Nouvelle ligne de revenu :** "Journal sans limite" — abonnement mensuel 7 $/mois B2C. À projeter à 12, 24 et 36 mois en parallèle de la croissance de la base client.

**Nouvelle dépense :** traitement journal (transcription vocale, stockage chiffré, génération de digests par agent IA). Estimée à 0,80–1,50 $/client actif/mois. À intégrer dans le tableau de charges opérationnelles du BP.

**Nouvelle rubrique IP :** "Indicateur de temporalité décalée IVIA" — différenciateur doctrinal sans équivalent connu. À valoriser comme argument dans le pitch investisseurs (originalité de l'approche, potentiel de recherche, brevétabilité partielle de la méthode).

**Mise à jour recommandée :** BP v2.2 → v2.3, à commander comme chantier distinct avec le subagent BP. Lignes nouvelles : revenus journal (abonnement + crédit rétribution N3), dépenses traitement journal, amortissement IP temporalité décalée.

---

## 10. Implications techniques pour Copilot — Brief v2.0 → v2.1

Les pages et modifications suivantes constituent la spec Copilot issue de ce cadrage. Charte visuelle botanique (couleurs mousse, aubergine, rose, glacier, abricot, lavande, crème) à respecter sur toutes les pages nouvelles.

| Page | Action | Description |
|---|---|---|
| `client/inscription.html` | Refonte | Ajouter champs Nom et Téléphone. Ajouter 3 cases consentement N1/N2/N3. Captcha invisible Cloudflare Turnstile. Règle mot de passe 12 caractères. Redirection post-soumission vers dashboard (pas verifier-courriel). |
| `client/connexion.html` | Mise à jour | Détecter courriel non validé. Si non validé et 2e connexion : afficher blocage doux avec bouton "Renvoyer le lien de confirmation". Ne pas bloquer la 1re session. |
| `client/verifier-courriel.html` | Rendre fonctionnel | Page existante à relier à un endpoint réel de validation. Ajouter lien "Je confirme maintenant" depuis le bandeau dashboard. |
| `client/premier-ancrage.html` | Nouvelle page | Formulaire 6 questions (section 5). Page interstitielle proposée en première connexion, avec option "Explorer d'abord". |
| `client/journal.html` | Refonte complète | Bouton "Nouvelle entrée" fonctionnel. Modale d'entrée avec champs : titre, date évoquée (optionnel), corps texte, mode vocal, tags (3 max), niveau de partage. Indicateur de seuil mensuel visible. Ligne de vie double (date écriture vs date évoquée) en bas de page. |
| `client/historique.html` | Nouvelle page (ou onglet dashboard) | Vue rétrospective : victoires marquées, revers nommés, grands changements, adaptations. Alimentée par les entrées de journal et les retours de séances. |
| `client/journal-etendu.html` | Nouvelle page | Affichée quand le seuil gratuit est atteint. Présentation des deux options (forfait 7 $/mois et rétribution N3 avec crédit séance). |
| `admin/praticien.html?id=X` | Nouvelle page admin | Fiche praticien individuelle avec toutes les catégories d'indicateurs (A à F). Le bouton Action sur `admin/praticiens.html` doit pointer vers cette page. Section "Digest journal clients actifs" visible si consentements N2 accordés. |

---

## Références légales

- Loi modernisant des dispositions législatives en matière de protection des renseignements personnels (Loi 25, L.R.Q. c. P-39.1) — art. 3.2 (gouvernance), art. 3.4 (sécurité), art. 8 (information à la collecte), art. 14 (qualité du consentement), art. 23 (destruction et anonymisation), art. 27 (portabilité), art. 28 et 28.1 (effacement et cessation de diffusion)
- Règlement sur l'anonymisation des renseignements personnels, en vigueur depuis le 30 mai 2024 (L.R.Q. c. P-39.1, r. 0.1)
- NIST Special Publication 800-63B (Digital Identity Guidelines — Authentication and Lifecycle Management), 2017, section 5.1.1 (mémorised secrets : longueur 8 caractères minimum recommandé, pas de complexité imposée)
- Commission d'accès à l'information (CAI) — lignes directrices sur la sécurité et l'authentification

---

*Document vivant — toute modification au flux d'inscription, aux règles d'accès gradué ou aux seuils du journal requiert la validation du RPRP (David Beaupré, privacy@ivia.quebec) et une mise à jour synchrone du brief Copilot actif.*

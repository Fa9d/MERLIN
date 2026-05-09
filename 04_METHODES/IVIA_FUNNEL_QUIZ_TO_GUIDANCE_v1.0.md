# IVIA — Funnel Quiz-to-Guidance-to-Continuité v1.0

**Date** : 9 mai 2026
**Auteur** : Computer (lead stratégique IVIA)
**Statut** : doctrine appliquée — prêt à implémenter
**Doctrine de référence** :
- `00_DOCTRINE/charte_doctrinaire_ivia.md`
- `00_DOCTRINE/politique_gouvernance_donnees_agregees_v1.md`
- `04_METHODES/CADRAGE_PARCOURS_CLIENT_JOURNAL_v1.md`
- `04_METHODES/IVIA_BRIEF_PARTENARIATS_RH_LOI27_v2.0.md`

**Devises** : *Au sein de l'être — En actes.* / *Pour le peuple, par le peuple.*

---

## 0. Cadre — pourquoi ce document existe

Le user a observé un funnel BetterMe (calisthenics, ~30-45 questions, paywall hard, ~1,75 M$ USD/mois selon screensdesign.com et adapty.io [BetterMe Adapty paywall](https://adapty.io/paywall-library/betterme/), [BetterMe screensdesign](https://screensdesign.com/showcase/betterme-health-coaching)). La mécanique convertit non pas par le design mais par une **séquence comportementale** : qualification rapide → personnalisation perçue → progression continue → réassurance → offre.

**Problème** : BetterMe utilise plusieurs dark patterns que IVIA refuse :
- Marathon de 30-45 questions où la fatigue cognitive devient levier de commitment escalation [LeadsHook quiz funnel analysis](https://www.leadshook.com/blog/quiz-funnel-examples/).
- Hard paywall avec free trial qui se convertit en abonnement mensuel, prix décomposé par semaine pour paraître plus abordable [BetterMe screensdesign](https://screensdesign.com/showcase/betterme-health-coaching).
- Upsell agressif post-souscription (Sugar-Free Challenge, Flat Belly Challenge en chaîne) [BetterMe screensdesign](https://screensdesign.com/showcase/betterme-health-coaching).
- Prédiction datée pseudo-scientifique ("vous pèserez 82 kg le 15 août") qui exploite le biais de concrétisation [LeadsHook quiz funnel analysis](https://www.leadshook.com/blog/quiz-funnel-examples/).
- Arc émotionnel manipulateur (positif → problème → peur → solution) théorisé comme "functional questions" pour faire passer le prospect d'un état d'information à un état d'achat [LeadsHook quiz funnel analysis](https://www.leadshook.com/blog/quiz-funnel-examples/).

**Ce qu'on garde** : le squelette structurel (qualification courte, progression visible, restitution personnalisée utile, mobile-first, légal continu, événementiel fin).

**Ce qu'on retire** : tout ce qui contredit la doctrine IVIA (pas de diagnostic, pas d'urgence, pas d'alarmisme, pas de promesse de transformation, pas de pression, pas de prédiction datée, pas d'upsell post-paiement, pas d'opacité tarifaire).

**Ce qu'on ajoute (godmode)** :
- Restitution **utile sans email obligatoire** pour 80 % du contenu — le client repart avec quelque chose même s'il n'achète pas.
- Couplage natif au **journal volontaire** et à l'**indicateur de temporalité décalée** (différenciateur IVIA inscrit en strate E de la politique de gouvernance).
- **Sortie pleinement honorable** à chaque étape — "je laisse reposer" est un CTA aussi visible que "je continue".
- **Pas d'obligation de créer un compte avant la restitution** — le compte se crée seulement si le client veut prolonger (rendez-vous, journal, ressources continues).

---

## A. Architecture funnel IVIA — 8 écrans

### Principes structurants

- **8 écrans, pas 30**. La doctrine IVIA est qu'on n'extrait pas — on aide. 8 questions suffisent pour qualifier un état, orienter une voie, suggérer une ressource.
- **Une décision par écran**. Mobile-first. Tap large. Retour arrière toujours possible.
- **Barre de progression visible** (X/8) — pas de "vous y êtes presque" trompeur.
- **Sortie honorable visible à chaque étape** : lien discret mais clair "je laisse reposer, je reviendrai".
- **Aucune question médicale, aucun diagnostic**. On parle d'**état du moment**, pas de symptômes cliniques.
- **Aucun champ obligatoire avant l'écran 7**. Le client peut traverser le funnel sans rien donner d'identifiant.
- **Légal continu** : pied de page permanent avec liens Conditions / Confidentialité / Politique abonnement / Sortie complète des données (Loi 25, art. 28.1 droit de cessation et destruction sur demande).

### Écran 1 — Accueil et invitation

**Objectif** : abaisser la barrière, signer le ton (calme, non alarmiste, non commercial).

**Contenu** :
- Titre : "Faisons un point ensemble. Sans diagnostic, sans urgence."
- Sous-titre : "8 questions, environ 3 minutes. À la fin, une orientation utile — gratuite, sans inscription obligatoire."
- Visuel : palette botanique IVIA de référence (charte_botanique). Pas de stock photo de personne souriante.
- CTA primaire : "Commencer le point"
- CTA secondaire (visible mais pas mis en avant) : "Je préfère parler à quelqu'un tout de suite" → page coordonnées 811 + ressources publiques (pas un praticien IVIA).
- Lien tertiaire : "Comment IVIA traite mes réponses" → micro-modale Loi 25.
- Mention sous CTA : "En continuant, vous acceptez nos Conditions et notre Politique de confidentialité. Aucune donnée personnelle n'est demandée avant la fin."

**Champs** : aucun.

**Événement** : `funnel_landing_view` { source, locale, variant }.

---

### Écran 2 — État du moment

**Objectif** : ouvrir avec une question simple, non médicale, qui qualifie l'état présent sans étiqueter.

**Question** : "Comment vous sentez-vous, en ce moment, dans votre vie en général ?"

**Réponses** (cartes larges, une par écran sur mobile, choix unique) :
- "Plutôt bien, je veux maintenir."
- "Ça va, mais quelque chose me pèse."
- "Je traverse une période difficile."
- "Je préfère ne pas répondre."

**Note doctrinale** : la 4ᵉ option est essentielle. Aucune obligation de divulgation. Si choisie, on saute Écran 3 et on passe à l'Écran 4 directement.

**Événement** : `funnel_q1_state` { value }.

---

### Écran 3 — Ce qui pèse (conditionnel)

**Objectif** : préciser sans diagnostiquer. **Multi-sélection autorisée** (jusqu'à 3).

**Question** : "Qu'est-ce qui prend le plus de place en ce moment ?"

**Réponses** :
- Sommeil
- Anxiété ou tension intérieure
- Relations (famille, couple, travail)
- Travail ou études
- Sens, direction, motivation
- Énergie corporelle, fatigue
- Deuil, transition, changement
- Autre (champ libre court, optionnel, 200 caractères max)

**Limites** :
- "Autre" est en bas, pas en haut, pour ne pas inciter à divulguer.
- Aucune liste de symptômes cliniques (DSM, anxiété généralisée, dépression majeure, etc.).
- Le champ "Autre" est chiffré au repos (libsodium) et **n'apparaît pas en clair côté admin** — il est tokenisé en thèmes anonymisés selon la strate B de la politique de gouvernance.

**Événement** : `funnel_q2_themes` { values, has_other_freetext }.

---

### Écran 4 — Voie d'entrée

**Objectif** : déterminer la modalité préférée — c'est ici qu'IVIA se distingue de toute plateforme bien-être générique. Les 3 voies sont les piliers IVIA.

**Question** : "Si vous pouviez choisir, par où aimeriez-vous commencer ?"

**Réponses** (cartes avec micro-description) :
- **Fréquence et corps** — "Travailler avec le souffle, le son, le mouvement subtil."
- **Sommeil et apaisement** — "Retrouver le repos, calmer le système nerveux."
- **Connaissance et clarification** — "Comprendre ce qui se passe, parler à quelqu'un qui écoute."
- "Je ne sais pas encore" — "C'est correct. On vous proposera quelque chose à essayer."

**Note** : ces 3 voies correspondent aux trois axes de la doctrine IVIA. Pas de "perte de poids", "muscle", "hydratation" — ce n'est pas notre territoire.

**Événement** : `funnel_q3_pathway` { value }.

---

### Écran 5 — Temporalité du besoin

**Objectif** : qualifier l'urgence perçue **sans la fabriquer**.

**Question** : "À quel rythme aimeriez-vous avancer ?"

**Réponses** :
- "Doucement, à mon rythme, sans pression."
- "Régulièrement, quelques fois par mois."
- "De façon soutenue, je veux y mettre du temps."
- "Je ne sais pas encore."

**Note doctrinale** : aucune option "tout de suite, urgence". Si quelqu'un est en détresse aiguë, ce n'est pas IVIA — c'est le 811, le 1-866-APPELLE, l'urgence. **Un encart permanent en bas du funnel rappelle ces ressources** dès l'Écran 1.

**Événement** : `funnel_q4_pace` { value }.

---

### Écran 6 — Préférence de mode d'écoute

**Objectif** : préparer l'orientation praticien (sans encore en montrer un).

**Question** : "Quand quelqu'un vous écoute, vous préférez :"

**Réponses** (multi-sélection, 1 à 3) :
- "Quelqu'un qui parle peu et laisse de la place."
- "Quelqu'un qui propose des outils concrets."
- "Quelqu'un qui partage un cadre culturel ou spirituel."
- "Quelqu'un avec une formation clinique reconnue."
- "Je ne sais pas, surprenez-moi."

**Note** : ces 5 options correspondent aux 5 typologies praticien identifiées dans `00_DOCTRINE/indicateurs_praticien_v1.md`. Cette question alimente directement l'algorithme d'orientation praticien (Strate A de la politique de gouvernance).

**Événement** : `funnel_q5_listening_style` { values }.

---

### Écran 7 — Ancrage (optionnel, recommandé)

**Objectif** : capter l'instant — c'est l'amorce du **journal volontaire** et le premier point de mesure de la **temporalité décalée** (différenciateur IVIA, strate E).

**Contenu** :
- Texte d'introduction : "Avant la restitution, prenez 60 secondes. Si vous voulez, écrivez **un mot, une image, un souvenir** qui vous traverse maintenant. Ce n'est pas obligatoire. C'est le point zéro de votre journal, si un jour vous voulez en garder un."
- Champ libre : 1 ligne, 240 caractères max.
- Case à cocher : "Conserver ce point de départ dans mon journal IVIA (nécessite création d'un compte à l'écran suivant)."
- Bouton : "Continuer sans noter" (équivalent en taille au bouton "Enregistrer").

**Note doctrinale critique** : si le client coche "Conserver", on lui demande à l'écran 8 **l'année et le mois approximatifs** du souvenir évoqué. Cet écart entre date d'écriture (maintenant) et date du souvenir évoqué = **indicateur de temporalité décalée** — première mesure capturée.

**Événement** : `funnel_q6_anchor` { has_text, char_count, wants_journal_save, decalage_evoque }.

---

### Écran 8 — Restitution personnalisée et orientation

**Objectif** : livrer **maintenant**, sans paywall, sans email obligatoire.

**Contenu généré** (rendu par template + petites règles de sélection — voir §C événements et §B microcopy) :

**Bloc 1 — Lecture du moment (3-5 lignes)**
"Vous avez choisi {voie}. Vous traversez {thème} à un rythme {pace}. Vous préférez une écoute {mode}. Ce n'est pas un diagnostic — c'est un point de départ utile."

**Bloc 2 — Une voie suggérée (1 paragraphe)**
Texte court et précis selon combinaison voie × thème (matrice 4×8 = 32 micro-textes — voir §B).

**Bloc 3 — Une ressource gratuite, accessible immédiatement**
- Article de la bibliothèque IVIA (lien direct, pas d'inscription requise).
- Ou enregistrement audio court (5-12 min) testable directement.

**Bloc 4 — Une prochaine étape concrète, sans pression**
3 options, présentées avec **équivalence visuelle** (mêmes tailles, même contraste, mêmes mots-couleurs) :
1. **Prendre rendez-vous d'écoute avec un praticien** — 60 min, 80 $ CAD (tarif type pilote, à confirmer selon politique tarification dynamique). Pas de carte bancaire à cette étape — réservation seulement.
2. **Créer un compte gratuit** — pour conserver le point d'ancrage et accéder au journal volontaire (50 entrées/mois ou 50 000 caractères gratuit, selon le cadrage parcours client v1).
3. **Repartir avec ce que vous avez maintenant** — la lecture, la voie, la ressource. Aucune action requise. "Vous pouvez revenir quand vous voulez."

**Mention finale** :
"Vos réponses ne sont pas conservées tant que vous ne créez pas de compte. Si vous fermez cette page, elles s'effacent dans 30 minutes."

**Événements** :
- `funnel_completion_view` { duration_total_sec, themes, pathway, pace, listening_style }.
- `funnel_outcome_choice` { choice: 'rdv'|'compte'|'depart' }.

---

### Pied de page permanent (tous écrans 1-8)

- Liens discrets, contraste WCAG AA : Conditions • Confidentialité • Politique d'abonnement • Effacer mes données • Détresse aiguë : 811 / 1-866-APPELLE / 911.
- Mention : "IVIA n'est pas un service d'urgence. Si vous êtes en danger immédiat, composez le 911."

---

## B. Microcopy exact (français québécois) — écran par écran

### Ton général

- Tutoyer : non. Vouvoyer : oui par défaut, doctrine IVIA.
- Pas de "tu peux", "fais", "essaie". Plutôt : "vous pouvez", "si vous le souhaitez", "à votre rythme".
- Pas de superlatifs ("incroyable", "transformateur", "exceptionnel"). Doctrine = sobriété québécoise.
- Pas de question rhétorique manipulatrice ("Est-ce que ça vous parle ?").
- Pas d'exclamation, pas d'emoji.

### Microcopy intégral

**Écran 1 — Accueil**
- H1 : "Faisons un point ensemble."
- Sous-H1 : "Sans diagnostic, sans urgence. Huit questions, environ trois minutes."
- Paragraphe : "À la fin, IVIA vous propose une lecture utile de votre moment et trois façons d'avancer. Gratuit, sans inscription obligatoire."
- Bouton primaire : "Commencer le point"
- Bouton secondaire : "Je préfère parler à quelqu'un tout de suite"
- Lien : "Comment IVIA traite mes réponses"
- Mention : "En continuant, vous acceptez nos Conditions et notre Politique de confidentialité. Aucune donnée personnelle n'est demandée avant la fin."

**Écran 2 — État du moment**
- Étape 1 sur 8.
- H2 : "Comment vous sentez-vous, en ce moment, dans votre vie en général ?"
- Aide : "Une seule réponse. Vous pouvez changer d'avis ensuite."
- Cartes :
  - "Plutôt bien. Je veux maintenir."
  - "Ça va. Mais quelque chose me pèse."
  - "Je traverse une période difficile."
  - "Je préfère ne pas répondre."
- Lien sortie : "Je laisse reposer. Je reviendrai."

**Écran 3 — Ce qui pèse**
- Étape 2 sur 8.
- H2 : "Qu'est-ce qui prend le plus de place en ce moment ?"
- Aide : "Jusqu'à trois choix."
- Cartes : Sommeil • Anxiété ou tension intérieure • Relations • Travail ou études • Sens, direction, motivation • Énergie corporelle, fatigue • Deuil, transition, changement.
- Champ "Autre" (optionnel) : "Si rien ne correspond, vous pouvez décrire en quelques mots. Maximum 200 caractères. Ce texte est chiffré et n'est jamais affiché en clair."
- Lien sortie : "Je laisse reposer."

**Écran 4 — Voie d'entrée**
- Étape 3 sur 8.
- H2 : "Si vous pouviez choisir, par où aimeriez-vous commencer ?"
- Cartes (avec micro-description) :
  - "Fréquence et corps." • "Travailler avec le souffle, le son, le mouvement subtil."
  - "Sommeil et apaisement." • "Retrouver le repos. Calmer le système nerveux."
  - "Connaissance et clarification." • "Comprendre ce qui se passe. Parler à quelqu'un qui écoute."
  - "Je ne sais pas encore." • "C'est correct. On vous proposera quelque chose à essayer."

**Écran 5 — Temporalité**
- Étape 4 sur 8.
- H2 : "À quel rythme aimeriez-vous avancer ?"
- Cartes :
  - "Doucement. À mon rythme. Sans pression."
  - "Régulièrement. Quelques fois par mois."
  - "De façon soutenue. Je veux y mettre du temps."
  - "Je ne sais pas encore."

**Écran 6 — Mode d'écoute**
- Étape 5 sur 8.
- H2 : "Quand quelqu'un vous écoute, vous préférez :"
- Aide : "Jusqu'à trois choix."
- Cartes :
  - "Quelqu'un qui parle peu et laisse de la place."
  - "Quelqu'un qui propose des outils concrets."
  - "Quelqu'un qui partage un cadre culturel ou spirituel."
  - "Quelqu'un avec une formation clinique reconnue."
  - "Je ne sais pas. Surprenez-moi."

**Écran 7 — Ancrage**
- Étape 6 sur 8.
- H2 : "Avant la restitution, prenez 60 secondes."
- Paragraphe : "Si vous le souhaitez, notez un mot, une image, un souvenir qui vous traverse maintenant. Ce n'est pas obligatoire. C'est le point zéro de votre journal, si un jour vous voulez en garder un."
- Champ libre : placeholder "Un mot, une image, un souvenir..." (240 caractères max).
- Case à cocher : "Conserver ce point de départ dans mon journal IVIA. Cela demandera la création d'un compte à l'étape suivante."
- Si case cochée, deux champs apparaissent : "Année approximative du souvenir évoqué" (sélecteur 1900-2026) et "Mois approximatif" (optionnel).
- Boutons (mêmes tailles) : "Continuer sans noter" • "Continuer avec mon ancrage".

**Écran 8 — Restitution**
- Étape 8 sur 8 (l'étape 7 est en arrière-plan, traitée).
- H1 : "Voici un point de départ utile."
- Bloc 1 : "Vous traversez {thème} à un rythme {pace}. Vous préférez une écoute {mode}. Ce n'est pas un diagnostic. C'est une lecture." — variable selon réponses, voir matrice §B-2.
- Bloc 2 : "Une voie qui pourrait vous convenir : {voie}. {paragraphe contextualisé}." — voir matrice §B-2.
- Bloc 3 : "Une ressource pour commencer maintenant : {titre article ou audio}. Accessible directement, sans inscription."
- Bloc 4 :
  - Carte 1 : "Prendre rendez-vous d'écoute" • "60 minutes avec un praticien IVIA. Tarif pilote 80 $ CAD. Réservation maintenant, paiement à la séance."
  - Carte 2 : "Créer un compte gratuit" • "Pour conserver votre point d'ancrage et tenir un journal volontaire."
  - Carte 3 : "Repartir avec ce que vous avez" • "Aucune action requise. Vous pouvez revenir quand vous voulez."
- Mention finale : "Vos réponses ne sont pas conservées tant que vous ne créez pas de compte. Si vous fermez cette page, elles s'effacent dans 30 minutes."

### B-2. Matrice de restitution (4 voies × 8 thèmes)

Pour MVP, on rédige **les 12 combinaisons les plus probables** (voie × thème principal), pas les 32. Les autres tombent sur un texte générique de la voie. Tableau de spécification (à ouvrir séparément, livré dans `04_METHODES/IVIA_FUNNEL_RESTITUTION_MATRICE_v1.0.md` — voir §E).

---

## C. Événements analytics à instrumenter

### Principes

- **Pas de Google Analytics, pas de Facebook Pixel, pas de Hotjar**. Doctrine confidentialité.
- Stack proposée : **PostHog self-hosted** (Docker, VPS France phase pilote, migration QC/CA après) ou **Plausible self-hosted**. PostHog permet en plus le funnel visualization et la segmentation par cohorte sans cookies tiers.
- **Aucun PII** dans les événements. Pas d'email, pas d'IP brute (IP hashée + tronquée), pas de fingerprint.
- Identifiant : **session_id éphémère** (UUID v4 généré côté client, expire 30 min sans activité, jamais stocké côté serveur tant que pas de création de compte).
- Conformité Loi 25, art. 8.1 (consentement éclairé), art. 9 (transparence des fins).

### Tableau d'événements (MVP)

| # | Nom événement | Propriétés | But analytique | But produit |
|---|---|---|---|---|
| 1 | `funnel_landing_view` | source, locale, variant, ts | Mesurer trafic entrant et A/B test variants | Taux d'entrée |
| 2 | `funnel_q1_state` | value, time_to_answer_sec | Distribution des états | Calibrer copy Écran 2 |
| 3 | `funnel_q2_themes` | values[], has_other_freetext, time_to_answer_sec | Top thèmes population | Prioriser articles bibliothèque |
| 4 | `funnel_q3_pathway` | value, time_to_answer_sec | Demande relative des 3 voies | Ajuster offre praticiens |
| 5 | `funnel_q4_pace` | value, time_to_answer_sec | Répartition rythmes | Calibrer fréquence séances |
| 6 | `funnel_q5_listening_style` | values[], time_to_answer_sec | Demande typologies praticien | Recrutement |
| 7 | `funnel_q6_anchor` | has_text, char_count, wants_journal_save, decalage_evoque_annees | Première mesure temporalité décalée | Différenciateur IP collective |
| 8 | `funnel_screen_dropoff` | screen_id, time_on_screen_sec | Localiser frictions | Optimisation UX |
| 9 | `funnel_back_navigation` | from_screen, to_screen | Hésitation | Calibrer copy |
| 10 | `funnel_exit_honor_click` | screen_id | Sortie volontaire | Validation doctrine |
| 11 | `funnel_completion_view` | duration_total_sec, themes, pathway, pace, listening_style | Profil client global | Cohorte |
| 12 | `funnel_outcome_choice` | choice ('rdv' \| 'compte' \| 'depart'), latency_after_view_sec | Conversion vraie | KPI principal |
| 13 | `funnel_resource_click` | resource_id, resource_type ('article' \| 'audio') | Engagement contenu | Ranking bibliothèque |
| 14 | `funnel_account_create_complete` | source='funnel', has_anchor_saved | Conversion compte | Valeur réelle |
| 15 | `funnel_rdv_initiated` | praticien_typologie, time_slot | Conversion RDV | Pipeline praticien |
| 16 | `funnel_rdv_confirmed` | praticien_id_hashed, ts_appointment | Conversion finale | Revenu |
| 17 | `funnel_legal_modal_open` | which ('terms' \| 'privacy' \| 'subscription' \| 'erase') | Préoccupations légales | Améliorer transparence |
| 18 | `funnel_distress_link_click` | screen_id | Détection détresse | Ne PAS retenir, rediriger |

### Notes critiques d'instrumentation

- **`funnel_distress_link_click`** : aucun retargeting, aucun email follow-up. Le client part vers 811/911. C'est le seul événement où on coupe immédiatement le tracking.
- **`funnel_q6_anchor.decalage_evoque_annees`** : c'est l'or de la donnée IVIA. Calculer `année_actuelle - année_evoquée`, jamais stocker l'année brute en analytics (la stocker dans le journal seulement si compte créé, chiffré au repos).
- **`funnel_q2_themes.has_other_freetext`** : booléen seulement. Le texte libre n'entre **jamais** dans PostHog. Il vit chiffré dans la base IVIA si compte créé, sinon il est détruit avec la session.

### Définition des KPI dérivés

- **Taux de complétion** : `funnel_completion_view` / `funnel_landing_view` (cible MVP : ≥ 55 %, vs ~25-35 % marché santé/wellness selon LeadsHook 2025).
- **Taux de conversion compte** : `funnel_account_create_complete` / `funnel_completion_view` (cible : ≥ 18 %).
- **Taux de conversion RDV** : `funnel_rdv_confirmed` / `funnel_completion_view` (cible : ≥ 6 %).
- **Taux de sortie honorable** : `funnel_exit_honor_click` / `funnel_landing_view` (KPI doctrinal — on **veut** un taux non-nul, signe que la sortie est visible).
- **Temps médian par écran** : pour détecter les écrans trop chargés (> 25 sec médian = revoir copy).

---

## D. Plan A/B test 30 jours — 3 hypothèses fortes

### Cadre méthodologique

- **Outil** : PostHog feature flags + experiments (self-hosted).
- **Sample size minimum** : 400 sessions par variant pour atteindre puissance statistique sur taux de complétion (basé sur baseline 55 %, MDE 7 points, alpha 0,05, power 0,80).
- **Trafic estimé pilote** : 30-60 sessions/jour × 30 jours × 2 variants = ~1 800 sessions par expérience. Réalisable si on lance une expérience à la fois.
- **Pas de p-hacking** : on déclare hypothèse + KPI + seuil **avant** de lancer.
- **Comité doctrinal** : toute modification de copy alarmiste/manipulatrice est **bloquée** même si elle convertit mieux. Doctrine > conversion.

### Hypothèse 1 — Sortie honorable visible (test doctrinal)

**Hypothèse** : Rendre la sortie honorable visible à chaque écran (vs masquée en pied de page) **n'augmente pas** le taux d'abandon, et **augmente** la confiance perçue (mesurée via taux de retour 7 jours).

**Variant A (contrôle)** : Lien "je laisse reposer" en pied de page, taille 12px, gris.
**Variant B (test)** : Lien "je laisse reposer" sous le bouton primaire, taille 14px, contraste WCAG AA.

**KPI primaire** : Taux de complétion `funnel_completion_view` / `funnel_landing_view`.
**KPI secondaire** : Taux de retour 7 jours (session_id réapparition).
**Seuil de décision** : Si Variant B ≥ Variant A - 2 points sur KPI primaire ET ≥ Variant A + 3 points sur KPI secondaire → **Variant B gagne** (la doctrine prime, on accepte une légère baisse de complétion contre une hausse de confiance).

**Pourquoi cette hypothèse** : valider la doctrine. Si la sortie visible casse l'économie, on doit le savoir et arbitrer transparentment, pas masquer.

---

### Hypothèse 2 — Restitution avant ou après compte

**Hypothèse** : Livrer la restitution **sans demander la création de compte** (restitution gratuite intégrale Écran 8) génère **plus** de RDV et de comptes à 7 jours qu'une restitution gating (compte requis pour voir le résultat).

**Variant A (contrôle, doctrine actuelle)** : Restitution intégrale visible Écran 8, compte optionnel.
**Variant B (test, modèle BetterMe)** : Bloc 1 visible, Blocs 2-3-4 floutés derrière "Créer un compte gratuit pour voir votre voie complète".

**KPI primaire** : Taux de RDV confirmés `funnel_rdv_confirmed` / `funnel_landing_view`.
**KPI secondaire** : Taux de création de compte `funnel_account_create_complete` / `funnel_landing_view`.
**Seuil de décision** : Variant A doit gagner sur KPI primaire **OU** KPI secondaire avec écart ≥ 1,5 point absolu pour valider la doctrine. **Sinon, escalade comité doctrinal** : on ne bascule **pas** sur Variant B même si statistiquement supérieur, on garde Variant A et on cherche autre levier.

**Pourquoi cette hypothèse** : c'est le test critique. La doctrine IVIA est que la valeur est livrée avant l'extraction. Si Variant B gagne fortement, on doit assumer un coût économique pour la doctrine — ce qui est une décision stratégique, pas optimisation.

---

### Hypothèse 3 — Ancrage facultatif vs encouragé

**Hypothèse** : Présenter l'écran 7 (ancrage) **comme une étape valorisée par défaut** (case "Conserver dans mon journal" pré-cochée si l'utilisateur a écrit du texte) **augmente** la création de compte **sans dégrader** le taux de complétion ni la confiance.

**Variant A (contrôle)** : Case "Conserver" non cochée par défaut.
**Variant B (test)** : Case "Conserver" cochée automatiquement dès qu'un texte est saisi (avec mention claire "Cocher pour conserver, décocher pour ne pas conserver"). Toggle visible.
**Variant C (anti-pattern test, doctrinal)** : Case cochée par défaut **dès l'ouverture** de l'écran, indépendamment du texte. **Ce variant ne sera pas testé en production** — il sert seulement de référence interne pour quantifier la dérive si on cédait à la pression conversion. À documenter dans `00_DOCTRINE/anti_patterns_funnel_v1.md`.

**KPI primaire** : Taux de création de compte `funnel_account_create_complete` / `funnel_completion_view`.
**KPI secondaire** : Taux de complétion `funnel_completion_view` / `funnel_landing_view` (ne doit pas baisser de plus de 2 points).
**KPI doctrinal** : Taux de "décochage" mesuré dans Variant B — si > 25 % décochent, signal que le default n'est pas perçu comme respectueux → revenir au Variant A.
**Seuil de décision** : Variant B gagne si KPI primaire +5 points minimum ET KPI doctrinal de décochage < 25 % ET KPI secondaire stable.

---

### Calendrier 30 jours

- **Jours 1-3** : Implémentation funnel v1 (sans tests A/B).
- **Jours 4-13** : Hypothèse 2 (la plus stratégique, on la passe en premier).
- **Jours 14-23** : Hypothèse 1 (validation doctrinale).
- **Jours 24-30** : Hypothèse 3.

Si trafic insuffisant pour 400 sessions/variant en 10 jours, étendre la fenêtre. Ne **jamais** raccourcir.

---

## E. Bonus godmode (non demandés, livrés)

### E-1. Anti-pattern map

À créer en doctrine : `00_DOCTRINE/anti_patterns_funnel_v1.md` (à rédiger sprint suivant). Contenu prévu : liste des 12 dark patterns observés sur BetterMe, ColonBroom, Noom, et autres apps wellness ; pour chaque pattern, **la version IVIA équivalente non manipulatrice** ; règles d'arbitrage en cas de tension conversion vs doctrine.

### E-2. Politique de consentement spécifique au funnel (Loi 25)

Document compagnon livré séparément : `12_JURIDIQUE_AFFAIRES/IVIA_CONSENTEMENT_FUNNEL_LOI25_v1.0.md` — couvre :
- Consentement granulaire par catégorie de donnée (Strate A à E de la politique de gouvernance).
- Délai de conservation des sessions non-converties (30 minutes, puis destruction automatique).
- Procédure d'effacement Loi 25 art. 28.1 dès l'écran 1.
- Modèle de mention obligatoire pour le champ libre "Autre" (Écran 3).
- Procédure de re-consentement si le funnel évolue.

### E-3. Couplage natif au calendrier éditorial

Le pipeline contenu (`pipeline_contenu_data_driven_v1.md`) doit être alimenté **mensuellement** par les données agrégées du funnel :
- Top 3 thèmes (Écran 3) → 3 articles le mois suivant.
- Top voie (Écran 4) → 1 enregistrement audio thématique.
- Distribution typologies écoute (Écran 6) → article "Quel praticien pour qui ?" trimestriel.

Cette boucle est ce qui transforme IVIA d'une plateforme statique en une plateforme apprenante. **C'est ce que le user a demandé en strate de fond** : que les données orientent à la fois clients et analyses.

### E-4. Indicateur de temporalité décalée — première capture

L'écran 7 est **la première capture systématique** au monde (à notre connaissance, à valider veille concurrentielle) de l'écart temporel entre événement vécu et écriture du souvenir, dans un cadre de bien-être. C'est l'**actif IP collectif IVIA** inscrit en strate E de la politique de gouvernance.

**Conditions de capture éthique** :
- Volontaire absolu (case décochée par défaut en MVP).
- Anonymisé en agrégé (jamais associé au texte).
- Valorisable en 2027+ auprès recherche universitaire / MSSS / FRQS.
- Ne **jamais** être présenté au client comme "votre score de décalage temporel" — ce n'est pas un score, c'est une donnée d'observation collective.

---

## F. Priorisation MVP — 2 semaines

### Sprint MVP (10 jours ouvrables)

| Jour | Livrable |
|---|---|
| 1 | Écrans 1-2 + design system botanique + pied de page légal |
| 2 | Écrans 3-4 + retour arrière + barre progression |
| 3 | Écrans 5-6 + multi-sélection + sortie honorable |
| 4 | Écran 7 (ancrage + champ libre + capture année souvenir) |
| 5 | Écran 8 (restitution générique sans matrice) + 3 CTA équivalents |
| 6 | Matrice restitution v1 (12 combinaisons les plus probables) |
| 7 | PostHog self-hosted + 18 événements instrumentés |
| 8 | Politique consentement funnel + mention Loi 25 + procédure effacement |
| 9 | Tests bout-en-bout (mobile, desktop, accessibilité WCAG AA) |
| 10 | Lancement pilote restreint (50 utilisateurs invités) |

### Itérations 1-3 (semaines 3-8)

- **Itération 1** (sem 3-4) : Hypothèse 2 (gating restitution) — le test stratégique.
- **Itération 2** (sem 5-6) : Hypothèse 1 (sortie honorable) — le test doctrinal.
- **Itération 3** (sem 7-8) : Hypothèse 3 (ancrage par défaut) — le test fin.
- **Boucle contenu** : revue mensuelle des thèmes Écran 3 → planification 3 articles mois suivant.

---

## G. Décisions à arbitrer (escalade user)

1. **Tarif RDV affiché au funnel** : 80 $ CAD pilote ou autre ? Doctrine actuelle 80 $ (cadrage parcours client v1) — confirmer ou ajuster.
2. **PostHog self-hosted vs Plausible self-hosted** : PostHog est plus puissant (funnels, cohortes), Plausible plus léger et plus respectueux par défaut. Recommandation Computer : **PostHog** pour la phase pilote car les événements 7 et 18 demandent corrélation funnel.
3. **Hébergement analytics** : VPS France actuel ou QC/CA dès le pilote ? Doctrine confidentialité = QC/CA dès que possible. Recommandation : France pour le pilote (déjà en place), migration QC/CA avant ouverture publique.
4. **Champ libre Écran 3 "Autre"** : tokenisation thématique automatique (NLP côté serveur, modèle local Llama ou similaire) ou suppression complète après 30 minutes ? Recommandation Computer : suppression complète en MVP, tokenisation en V2 si volume justifie investissement.

---

## H. Sources et références

- Funnel BetterMe directement consulté : [BetterMe Calisthenics flow=3426](https://betterme-calisthenics.com/first-page-brand-palette?flow=3426).
- Données revenus et structure paywall : [Adapty paywall library — BetterMe](https://adapty.io/paywall-library/betterme/), [screensdesign.com — BetterMe Health Coaching](https://screensdesign.com/showcase/betterme-health-coaching).
- Analyse mécanique quiz funnel et anti-patterns : [LeadsHook — 9 Quiz Funnel Examples 2025](https://www.leadshook.com/blog/quiz-funnel-examples/).
- Structure questionnaire BetterMe — psychologique vs algorithmique : [Paul Levchuk LinkedIn — BetterMe onboarding mapping](https://www.linkedin.com/posts/paullevchuk_onboarding-activity-7416149710576545793-yrjX).
- Marché santé mentale QC : `00_DOCTRINE/etat_marche_quebec_v1.md` (27 sources internes).
- Doctrine IVIA : `00_DOCTRINE/charte_doctrinaire_ivia.md`, `politique_gouvernance_donnees_agregees_v1.md`.

---

*Au sein de l'être — En actes. Pour le peuple, par le peuple.*

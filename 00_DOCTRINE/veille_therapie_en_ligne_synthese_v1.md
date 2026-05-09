# IVIA — Veille thérapie en ligne (15 services US/intl) : ce qu'on prend, ce qu'on contourne, ce qu'on dépasse

**Date** : 9 mai 2026
**Auteur** : Computer (lead stratégique IVIA)
**Statut** : doctrine — alimente `IVIA_FUNNEL_QUIZ_TO_GUIDANCE_v1.0.md`, `IVIA_VEILLE_CONCURRENTIELLE_QUEBEC_v1.0.md`, `dispositif_veille_ivia_v1.md`
**Données brutes** : `00_DOCTRINE/veille_therapie_en_ligne_15_services_20260509.csv` (15 services × 14 colonnes)

**Sources visitées (sites officiels seulement, comme demandé)** : [BetterHelp](https://www.betterhelp.com), [Talkspace](https://www.talkspace.com), [Grow Therapy](https://www.growtherapy.com), [Amwell](https://www.amwell.com), [Teladoc Health](https://www.teladoc.com), [Sesame Care](https://www.sesamecare.com), [Brightside Health](https://www.brightside.com), [LiveHealth Online](https://www.livehealthonline.com), [Doctor on Demand](https://www.doctorondemand.com), [MDLIVE](https://www.mdlive.com), [Regain](https://www.regain.us), [Faithful Counseling](https://www.faithfulcounseling.com), [Pride Counseling](https://www.pridecounseling.com), [Online-Therapy.com](https://www.online-therapy.com), [OurRitual](https://www.ourritual.com).

---

## 1. Lecture stratégique — ce que ces 15 sites disent du marché

### 1.1 Trois familles distinctes

**Famille A — Plateformes thérapie pure-play à abonnement** : BetterHelp, Talkspace, Online-Therapy.com, Regain, Faithful Counseling, Pride Counseling, OurRitual.
- Modèle : abonnement hebdomadaire facturé mensuellement, 60-100 $ USD/sem (240-400 $ USD/mois).
- Onboarding : quiz long (8 à 30+ questions), gating systématique de la valeur derrière compte + paiement.
- Ton : "You deserve to be happy" — promesse de bonheur, encouragement, légèrement coaching.
- Marketing : preuves sociales massives (BetterHelp affiche 31 963 thérapeutes et 6,4 M+ personnes aidées sur sa [home](https://www.betterhelp.com)), opacité tarifaire jusqu'au quiz complété.

**Famille B — Plateformes médicales virtuelles avec santé mentale incluse** : Amwell, Teladoc, LiveHealth Online, Doctor on Demand, MDLIVE, Brightside Health.
- Modèle : par séance ou couvert par assurance, tarifs visibles (89-299 $ USD selon le service).
- Onboarding : pas de quiz, formulaire d'inscription standard, gating dès le bouton "Get started".
- Ton : sobre, médical, "board-certified", insistance sur les certifications cliniques.
- Marketing : assurances majeures en logos (Aetna, UnitedHealthcare, Cigna), chiffres systémiques (Teladoc affiche 100 M+ Américains et 9 M Canadiens sur sa [home](https://www.teladoc.com)).

**Famille C — Marketplaces de praticiens** : Grow Therapy, Sesame Care.
- Modèle : par séance, tarifs affichés en clair (Grow Therapy : 21 $ moyen avec assurance, 125-140 $ cash sur sa [home](https://www.growtherapy.com) ; Sesame : à partir de 35 $ sur sa [home](https://www.sesamecare.com)).
- Onboarding : pas de quiz long, filtres directs (type de soin, état, assurance, langue).
- **Gating presque absent** chez Grow Therapy : "accès direct au matching et tarifs sans inscription préalable, l'inscription n'est requise qu'au moment de la réservation". C'est l'exception qui valide la doctrine IVIA.

### 1.2 Trois constats importants pour IVIA

**Constat 1 — La famille A (BetterHelp et clones) domine le narratif mais utilise les mécaniques les plus contestables.** Quiz de 20-30 questions, opacité tarifaire jusqu'à la fin, slogan "You deserve to be happy", redirection des marques de niche (Faithful, Pride) vers la marque mère sans transparence. Ce n'est **pas** une référence de design éthique — c'est une référence de conversion à dark patterns assumés. Pride Counseling redirige techniquement vers BetterHelp avec le paramètre `lgbtq_verified=true` ([source onboarding observé](https://www.betterhelp.com/get-started/)), Faithful Counseling avec `christian_faith=true`. Le branding niche est un wrapper marketing.

**Constat 2 — Aucun de ces 15 services n'est doctrinalement compatible avec ce qu'IVIA construit.** Disponibilité Québec : Teladoc oui (via [teladochealth.ca](https://www.teladochealth.ca/fr/)), BetterHelp/Regain/Pride oui mais sans mention Loi 25, les autres non. Aucun ne mesure quelque chose comme la temporalité décalée. Aucun n'a une voie "fréquence et corps" ni "connaissance et clarification". Aucun n'a de sortie honorable visible.

**Constat 3 — Brightside Health est le seul à publier des indicateurs de résultats cliniques sur sa home** : "57% de réduction des pensées suicidaires en 12 semaines, 55% de rémission en 12 semaines" ([Brightside home](https://www.brightside.com)). C'est un standard que le pilote IVIA devrait viser à atteindre publiquement d'ici 18 mois — pas pour copier la méthode (très médicalisée), mais pour valider la doctrine du *résultat mesurable et transparent*.

---

## 2. Ce qu'on prend (intégrer dans le funnel et la plateforme)

### 2.1 Du quiz BetterHelp/Talkspace : la barre de progression

BetterHelp affiche une barre de progression sur ~8 étapes majeures. Talkspace idem. C'est un standard UX bien rodé. **Confirmé pour IVIA Écran 1-8** — déjà dans `IVIA_FUNNEL_QUIZ_TO_GUIDANCE_v1.0.md` §A.

### 2.2 De Grow Therapy : la transparence tarifaire pré-inscription

Grow Therapy est le seul des 15 à laisser **voir les profils praticiens, tarifs et disponibilités sans inscription**. C'est l'exemple à suivre. **Action IVIA** : à compter de la V2 (post-pilote, dès qu'on a 5+ praticiens), publier une page `/praticiens` avec photos, biographies, typologie d'écoute, tarif, créneaux libres — sans login obligatoire. Ça respecte la doctrine "valeur avant extraction".

### 2.3 De Sesame Care : la modularité du choix par le client

Sesame Care permet au client de **choisir son médecin**, voir ses notes, ses avis, sa biographie ([Sesame home](https://www.sesamecare.com)). **Action IVIA** : dans le funnel Écran 8 ou page `/praticiens`, le client peut **filtrer par typologie d'écoute** (silence / outils / culturel / clinique), pas par maladie. C'est l'inverse du modèle médical. Différenciateur clair.

### 2.4 De Brightside Health : les indicateurs de résultats publiés

Brightside publie des chiffres cliniques précis sur sa home ([source](https://www.brightside.com)). **Action IVIA** : à 18 mois post-pilote, publier sur la home IVIA 3-5 indicateurs anonymisés issus de la strate E (politique de gouvernance) :
- Évolution médiane de l'auto-évaluation initiale → 6 mois.
- Taux de retour au journal après 30 jours, 90 jours.
- Indicateur de temporalité décalée moyen au démarrage vs après accompagnement.
- Taux de complétion de programmes 3-séances et 6-séances.
- Taux de recommandation client (NPS) et taux de retour praticien.

### 2.5 De Brightside Health : les numéros d'urgence en bas de page

Brightside intègre **988 et 741-741** (lignes US) en bas de page systématiquement. **Action IVIA confirmée** : pied de page permanent avec **811 Info-Santé QC, 1-866-APPELLE-1, 911**, déjà inscrit dans le funnel v1.0 § Pied de page permanent. Renforcer : ajouter aussi **Ligne autochtone Espoir pour le mieux-être 1-855-242-3310** et **Tel-Aide 514-935-1101**, en cohérence avec la doctrine 11 nations + multi-strates.

### 2.6 De Talkspace : l'usage de preuves cliniques académiques

Talkspace cite BMC Psychiatry et Journal of Telemedicine and e-Health pour étayer son efficacité ([Talkspace home](https://www.talkspace.com)). **Action IVIA** : à 24 mois post-pilote, viser **une publication de l'indicateur de temporalité décalée dans une revue scientifique québécoise ou canadienne** (FRQS, CRIR, IRCM, INSPQ, Revue de psychoéducation). Cette publication est l'actif de différenciation à long terme inscrit dans la strate E de la politique de gouvernance.

### 2.7 De BetterHelp : l'avertissement de crise dès l'entrée

BetterHelp écrit en clair "don't use this site if you are in a crisis" ([BetterHelp home](https://www.betterhelp.com)). **Action IVIA confirmée** : déjà inscrit dans le funnel v1.0 (Écran 1, mention "IVIA n'est pas un service d'urgence"). À renforcer en **modale obligatoire à la première visite**, fermable mais non sautable la première fois.

---

## 3. Ce qu'on contourne (refus doctrinal explicite)

### 3.1 Le slogan "You deserve to be happy" et toute promesse de bonheur

BetterHelp, Faithful Counseling, Pride Counseling utilisent tous trois cette phrase comme accroche principale. C'est une **promesse excessive** au sens de la doctrine IVIA : on ne promet pas le bonheur. On accompagne un moment, on offre une voie, on respecte un rythme. **Inscrit en doctrine** : la home IVIA ne contient aucune promesse de transformation, d'amélioration garantie, de bonheur.

### 3.2 Le quiz long (20-30+ questions) avec gating de la valeur

Faithful Counseling et Pride Counseling utilisent un quiz de 20-30 questions avant tout accès. BetterHelp 8+ étapes. C'est le pattern BetterMe analysé hier. **Refus IVIA** : 8 écrans maximum, restitution gratuite intégrale Écran 8, compte optionnel. Inscrit dans le funnel v1.0 §A.

### 3.3 L'opacité tarifaire systématique

12 des 15 services n'affichent **pas** leur tarif réel sur la home. Il faut ouvrir la FAQ, parfois compléter le quiz. **Refus IVIA** : tarif affiché en clair sur la home et sur l'Écran 8 du funnel. Pilote 80 $ CAD pour 60 min (à confirmer ou ajuster). Pas de "à partir de" trompeur.

### 3.4 La redirection silencieuse de marques niche vers la marque mère

Pride Counseling et Faithful Counseling redirigent techniquement vers BetterHelp. Le client croit s'inscrire chez Pride/Faithful — il s'inscrit chez BetterHelp. Ce **n'est pas** déclaré de façon visible. **Refus IVIA absolu** : si IVIA développe à terme des sous-marques (ex : IVIA Aînés, IVIA Premières Lignes, IVIA Jeunesse), chacune doit avoir une **identité juridique et opérationnelle distincte** ou une **mention claire** "ce service est opéré par IVIA".

### 3.5 Le matching automatisé par IA non transparent

Pride Counseling mentionne un matching IA dans son quiz, sans expliquer comment. **Refus IVIA** : si on utilise un algorithme pour suggérer un praticien (Écran 8 § Bloc 4 carte 1), les critères doivent être **publiés en clair** sur la page `/comment-ca-fonctionne` :
- Voie d'entrée choisie (Écran 4) — poids 35 %.
- Mode d'écoute choisi (Écran 6) — poids 35 %.
- Disponibilité du praticien et géographie — poids 20 %.
- Langue (FR/EN/autochtone) — poids 10 %.
Aucun usage de données sensibles (Écran 3 thèmes) pour le matching tant qu'on n'a pas de validation éthique.

### 3.6 L'urgence artificielle (Sesame Care, Online-Therapy.com)

Sesame affiche "20% off" au premier chargement. Online-Therapy.com affiche "FIRST MONTH: 20% off" et "Get happier NOW". **Refus IVIA absolu** — déjà dans la doctrine.

### 3.7 La case "Conserver dans le journal" cochée par défaut

OurRitual utilise des défauts opt-in agressifs sur le partage de données. **Refus IVIA confirmé** : case **décochée** par défaut en MVP (Écran 7 du funnel v1.0).

### 3.8 Le tutoiement systématique anglophone (you générique)

Tous les sites US tutoient. **Doctrine IVIA** : vouvoiement systématique en français québécois.

---

## 4. Ce qu'on dépasse (différenciateurs IVIA non couverts par les 15)

### 4.1 La voie "fréquence et corps"

**Aucun** des 15 services ne propose une voie d'entrée *fréquence, souffle, son, mouvement subtil*. La famille A reste verbale (chat/vidéo), la famille B est médicale, la famille C est marketplace de psy. **IVIA voie 1 = différenciateur dès l'Écran 4**.

### 4.2 L'indicateur de temporalité décalée

**Aucun** des 15 services ne mesure l'écart entre date d'écriture d'un souvenir et date de l'événement évoqué. C'est confirmé : l'idée est originale, défendable, brevetable au sens de l'IP collective inscrite en strate E. **À documenter dans `cadre_propriete_intellectuelle_donnees`** (déjà existant) avec date de première publication = 9 mai 2026 (commit `a2d493c` du repo MERLIN, traceable). Ça crée un *prior art* daté qui protège contre l'appropriation par un acteur US.

### 4.3 La sortie honorable visible à chaque étape

**Aucun** des 15 services ne propose une sortie volontaire visible et valorisée. Tous font un funnel one-way avec retour arrière au mieux. **Hypothèse 1 du plan A/B (funnel v1.0 §D)** = test doctrinal : on accepte une légère baisse de complétion pour gagner en confiance et taux de retour 7 jours.

### 4.4 La conformité Loi 25 et l'ancrage québécois

**Aucun** des 15 services ne mentionne la Loi 25 (Teladoc Canada s'approche mais ne nomme pas la loi). IVIA fait de la conformité Loi 25 un argument central, pas un mince cadre légal. Document compagnon `IVIA_CONSENTEMENT_FUNNEL_LOI25_v1.0.md` déjà rédigé.

### 4.5 Le pilier 11 nations / autochtone

**Aucun** des 15 services n'a de cadre culturel autochtone. IVIA a déjà :
- `MERLIN_METH_PLAYBOOK_PROTOCOLE_REFERENCEMENT_11_NATIONS_v1.0.md`
- `MERLIN_METH_PLAYBOOK_PARTITION_AUTOCHTONES_v1.0.md`
- Mode d'écoute "cadre culturel ou spirituel" dès l'Écran 6 du funnel.
**Différenciateur structurel** sur le marché québécois — aucun acteur, ni Teladoc Canada, ne propose ça.

### 4.6 Le couplage funnel ↔ calendrier éditorial

**Aucun** des 15 ne réinjecte les données agrégées du funnel dans son calendrier de contenu mensuel. IVIA le fait par doctrine (`pipeline_contenu_data_driven_v1.md`). C'est ce qui transforme IVIA en plateforme apprenante.

### 4.7 Le journal volontaire avec capture de souvenirs

**Aucun** des 15 ne propose un journal volontaire avec capture optionnelle de la temporalité du souvenir. Brightside a un suivi clinique standardisé (PHQ-9, GAD-7), Talkspace a du chat archivé. Rien d'équivalent au journal IVIA.

---

## 5. Modifications recommandées au funnel v1.0 (suite à la veille)

### 5.1 Écran 1 — Renforcer l'avertissement crise

**Ajouter** : modale obligatoire à la première visite (cookie session, fermable mais non sautable la première fois) avec les 4 lignes d'urgence québécoises. Inspiré de l'avertissement BetterHelp ([source](https://www.betterhelp.com)) mais en français québécois et avec ressources locales.

### 5.2 Écran 8 — Ajouter un indicateur de transparence tarifaire

**Ajouter** sous la carte 1 (RDV praticien) :
> Tarif pilote : 80 $ CAD pour 60 min. Aucun frais caché. Aucun abonnement. Vous payez à la séance, après la séance.

Inspiré de Grow Therapy et Sesame Care, contre-pied direct à BetterHelp/Talkspace.

### 5.3 Écran 8 — Ajouter une mention "Comment IVIA choisit le praticien suggéré"

**Ajouter** un lien discret sous la carte 1 : "Comment IVIA suggère un praticien" → page dédiée publiant les 4 critères et leurs poids (§3.5 supra). Anti-dark-pattern par construction.

### 5.4 Écran 8 — Ajouter un quatrième CTA discret

**Ajouter** : un quatrième élément, plus petit, sous les 3 cartes :
> Vous voulez juste lire ? Notre [bibliothèque](https://ivia.pplx.app/bibliotheque) est ouverte à tous.

C'est l'équivalent IVIA de la "valeur sans extraction" exemplifiée par Grow Therapy.

### 5.5 Page `/comment-ca-fonctionne` — créer

Page dédiée (à créer en sprint MVP) qui documente :
- Les 8 écrans du funnel.
- Les 4 critères de matching praticien et leurs poids.
- La politique de conservation (30 min sans compte, profil/journal avec compte).
- Les niveaux de consentement N0-N3.
- Les 5 strates de la politique de gouvernance.

Inspiré de la **section FAQ exhaustive** observée chez Brightside, BetterHelp, Talkspace, mais avec un parti-pris doctrinal clair.

---

## 6. Modifications à la veille concurrentielle (`IVIA_VEILLE_CONCURRENTIELLE_QUEBEC_v1.0.md`)

À ajouter en addendum :

### 6.1 Ne pas utiliser les 15 services comme benchmark de design éthique

Ils sont benchmarks de **conversion** et de **scale**, pas de doctrine. Le benchmark doctrinal IVIA reste à construire — peut-être avec :
- **Wysa** (Royaume-Uni / Inde, [wysa.com](https://www.wysa.com)) — IA conversationnelle santé mentale, partenariats NHS, transparence forte.
- **Woebot** (USA, [woebothealth.com](https://woebothealth.com)) — mais focus IA conversationnelle.
- **Mindstrong** (USA, en restructuration) — passive sensing, controversé.
- **Headspace Health / Ginger** — corporate, mais publication de résultats cliniques.

**Action** : sprint suivant, lancer une veille parallèle sur ces 4-6 acteurs **éthiquement comparables** plutôt que les 15 grand public US. Et inclure les acteurs québécois : **Morneau Shepell / LifeWorks**, **TELUS Santé** (mentionné déjà), **Optima Santé Globale**, **Inkblot Therapy** (canadien).

### 6.2 Aucune mention Loi 25 sur 15 services US/intl

**Constat à publier** dans la communication IVIA et dans le BP v2.3 §11 : sur 15 services internationaux dominants visités le 9 mai 2026, **zéro** ne mentionne explicitement la Loi 25 du Québec. C'est un argument de souveraineté numérique exploitable auprès d'investisseurs québécois, MSSS, et clients RH (Loi 27).

### 6.3 BetterHelp et Teladoc disponibles au Canada

Confirmer le positionnement IVIA : non pas "premier service de thérapie en ligne au Québec" (faux, BetterHelp et Teladoc sont là), mais **"première plateforme québécoise multi-strates d'accompagnement non-clinique conforme Loi 25 avec ancrage 11 nations"**. C'est plus précis et défendable.

---

## 7. Décisions ouvertes (escalade user)

1. **Doit-on créer dès le MVP la page `/praticiens` à la Grow Therapy** (transparence tarifaire et profils sans login) ou attendre 5+ praticiens recrutés ? Recommandation Computer : page dynamique dès le pilote, même avec 1-2 praticiens, pour incarner la doctrine.

2. **Doit-on viser la publication scientifique de l'indicateur de temporalité décalée** dès la phase pilote (12-18 mois) ou attendre 24 mois ? Recommandation Computer : préparer le protocole de recherche dès le pilote (partenariat universitaire à amorcer mai-juin 2026), publication réelle à 18-24 mois.

3. **Doit-on lancer une veille parallèle sur Wysa / Woebot / Inkblot** pour avoir un benchmark doctrinalement compatible ? Recommandation Computer : oui, en parallèle des 4 articles/audios à produire (sprint contenu mai-juin 2026).

4. **Quelle position prendre sur la mention publique "BetterHelp et Teladoc présents au Canada mais non conformes Loi 25 spécifique"** ? Recommandation Computer : mention factuelle dans la page `/comment-ca-fonctionne` et dans le pitch deck v1.3, sans attaque ad hominem. Doctrine = honnêteté radicale, pas dénigrement.

---

## 8. Sources

CSV brut détaillé : `00_DOCTRINE/veille_therapie_en_ligne_15_services_20260509.csv` (15 lignes × 14 colonnes, données factuelles vérifiées par visite directe des sites officiels).

Sources individuelles : voir liens en §0 (15 URLs officielles).

---

*Au sein de l'être — En actes. Pour le peuple, par le peuple.*

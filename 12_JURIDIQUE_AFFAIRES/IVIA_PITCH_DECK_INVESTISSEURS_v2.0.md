# PITCH DECK INVESTISSEURS — IVIA / MERLIN
## 26 slides — Format structuré pour conversion PowerPoint

**Version** : 2.0 — Produit en production — traction réelle
**Date** : 6 juillet 2026
**Remplace** : v1.3 — 9 mai 2026 (conservée en place)
**Usage** : Présentation investisseurs, anges, fondations, partenaires
**Format** : Chaque slide = titre + bullets + notes du conférencier
**Conversion PowerPoint** : prévoir police Calibri, fond blanc, accent teal #20808D

---

## INSTRUCTIONS DE MISE EN FORME

Pour la conversion PowerPoint :
- Police titre : Trebuchet MS Bold, 36-40pt
- Police corps : Calibri, 18-22pt
- Couleur accent : #20808D (teal)
- Fond : blanc (#FFFFFF)
- Texte principal : #28251D (presque noir)
- Max 5 bullets par slide, max 8 mots par bullet
- Logo IVIA en coin supérieur gauche
- Numéro de slide en bas à droite
- Devise "Au sein de l'être — En actes." sur slide de couverture uniquement

---

## SLIDE 1 — COUVERTURE

**Titre** : IVIA

**Sous-titre** : Au sein de l'être — En actes.

**Bullets** :
- Plateforme québécoise de santé mentale
- MERLIN structure, IVIA accueille
- Produit live — juillet 2026
- Montréal, Québec — 6 juillet 2026

**Mentions** :
- Version 2.0 — Produit en production — traction réelle

**Notes du conférencier** :
"Bienvenue. IVIA n'est plus un projet prévu : la plateforme est en production. Le site public, l'espace client, l'espace praticien, la console admin et l'API sont live. Cette version du deck met à jour la promesse de mai 2026 avec l'exécution réelle de juillet 2026. La devise demeure : Au sein de l'être — En actes."

---

## SLIDE 2 — LE PROBLÈME

**Titre** : Détresse massive, système saturé, délai inadmissible

**Bullets** :
- 16 000 en attente publique
- Délais : 6 à 24 mois
- 75 % ne consultent pas
- Privé : 120-180 $ / séance
- Jeunes : détresse psychologique élevée

**Notes du conférencier** :
"Les données de marché n'ont pas changé : le Québec manque de capacité d'écoute et d'accompagnement. Le public est saturé, le privé est trop cher, et une large part des personnes ne consultent pas. IVIA se positionne dans l'espace entre l'absence de réponse et le soin spécialisé : écoute structurée, orientation prudente, validation humaine, et respect strict du cadre québécois."

---

## SLIDE 3 — LA SOLUTION IVIA

**Titre** : Une infrastructure de pratique d'écoute

**Bullets** :
- Intake, réservation, paiement, séance
- Audio/vidéo LiveKit intégré
- Transcription locale faster-whisper
- Analyses IA sous validation humaine
- Documents livrés au client

**Notes du conférencier** :
"Le parcours bout en bout fonctionne aujourd'hui : une personne arrive sur ivia.quebec, soumet une demande, reçoit un magic link, réserve un créneau réel, paie par Stripe ou en mode test, tient une séance audio/vidéo, puis reçoit des documents validés par le praticien. MERLIN n'est pas un chatbot clinique : c'est une infrastructure de pratique, gouvernée par le praticien."

---

## SLIDE 4 — LA DOCTRINE

**Titre** : Gouvernée par principes, pas seulement KPIs

**Bullets** :
- Le vivant d'abord
- Autonomie émotionnelle comme horizon
- Pas de diagnostic automatisé
- Orientation sans commission cachée
- Principes opposables juridiquement

**Notes du conférencier** :
"La doctrine reste le cœur. IVIA ne diagnostique pas, ne prescrit pas, ne remplace pas les services d'urgence, et n'enferme pas le client dans un abonnement. La sortie honorable fait partie du produit. Les principes doivent être portés par la structure juridique, par les contrats, par les interfaces et par les analyses IA."

---

## SLIDE 5 — L'OFFRE ACTUELLE

**Titre** : Une offre live, configurable, opérable

**Bullets** :
- Site public + espace client
- Espace praticien opérationnel
- Console admin séparée /admin/
- Paiement Stripe + mode test
- Vannes produit activables en admin

**État produit — juillet 2026** :
```
Offre client        Intake → réservation → paiement → séance → documents
Offre praticien     Créneaux, séances, enregistrements, validations
Offre admin         Comptes, demandes, vigilance, facturation, droits
Offre analytique    Prosodie locale + sémantique IA + profilage contrôlé
```

**Notes du conférencier** :
"En mai, l'offre était principalement décrite comme une grille et une trajectoire. En juillet, elle est opérable. La plateforme permet déjà de gérer le parcours client, les praticiens, les droits, les paiements, les documents et les interrupteurs d'exposition analytique. La grille économique reste transparente, mais l'élément nouveau est l'exécution : l'offre existe et tourne."

---

## SLIDE 6 — L'ARCHITECTURE MULTI-STRATES

**Titre** : 4 strates, déploiement progressif gouverné

**Visuel texte** :
```
S1 IVIA Cœur    → Praticiens d'écoute              Live pilote
S2 IVIA Pros    → Psychologues, psychothérapeutes   Après audit
S3 IVIA Soins   → Corps, fréquence, alternatives    Après validation
S4 IVIA Réseau  → Référencement éthique             Sans commission
```

**Bullets** :
- Chaque strate dépend d'un gate
- S1 prouve l'usage réel
- S2 exige audit ordres
- S3 élargit le marché
- S4 interdit la commission

**Notes du conférencier** :
"La logique multi-strates reste inchangée, mais S1 n'est plus théorique. Le palier technique nécessaire à l'écoute, à la séance, à l'enregistrement et à la livraison documentaire est construit. Les strates suivantes ne s'ouvrent pas par ambition abstraite, mais quand les gates d'usage, de conformité et de stabilité sont atteints."

---

## SLIDE 7 — LE PIPELINE GOUVERNÉ

**Titre** : Transformer la parole sans l'exposer

**Visuel texte** :
```
Consentement → Séance → Enregistrement → Transcription locale
→ Analyse contrôlée → Validation praticien → Document client
→ Audit, effacement, données minimisées
```

**Bullets** :
- Consentements capturés par contexte
- Audio traité sur serveur IVIA
- Transcription locale faster-whisper
- Documents validés par praticien
- Accès sensibles journalisés

**Notes du conférencier** :
"La différence majeure est la transcription locale. L'audio ne quitte pas le serveur : faster-whisper traite les enregistrements localement. Les analyses sensibles sont contrôlées par profils d'exposition, et les accès aux inférences sensibles sont journalisés. Le pipeline n'est pas seulement conforme en intention : il est maintenant implémenté dans l'architecture."

---

## SLIDE 8 — LE MOAT

**Titre** : Doctrine, données, moteur, conformité

**Bullets** :
- Pipeline gouverné déjà déployé
- Moteur analytique propriétaire actif
- Conformité Loi 25 intégrée
- Profils d'exposition contrôlés
- Confiance difficile à copier

**Notes du conférencier** :
"Le moat s'est matérialisé. IVIA dispose maintenant d'un moteur plein avec des vannes par profil : client Québec conforme Loi 25/21, praticien certifié, recherche sociétale. Les inférences sensibles ne sont pas exposées par défaut. Cette architecture permet de développer la profondeur analytique sans franchir les frontières réglementaires ou éthiques."

---

## SLIDE 9 — LE MARCHÉ

**Titre** : TAM Québec 110-210 M$ / an

**Visuel texte** :
```
S1 écoute        3 500-5 000 praticiens   ~12-36 M$
S2 ordres        12 000+ professionnels    ~58-86 M$
S3 soins         15 000+ praticiens        ~36-72 M$
S4 réseau        30 000+ potentiels         ~6-15 M$
```

**Bullets** :
- Canada santé mentale : marché massif
- Apps santé mentale : croissance forte
- Québec : privé déjà utilisé
- Employeurs : coût psychosocial majeur
- Cible M36 : faible part TAM

**Notes du conférencier** :
"Les chiffres de marché de v1.3 restent valables. IVIA ne cherche pas à conquérir tout le marché : l'objectif est de devenir une référence francophone québécoise sur l'écoute structurée, la conformité et la gouvernance des données sensibles. Une part très modeste du TAM suffit à soutenir la trajectoire M36."

---

## SLIDE 10 — SOUVERAINETÉ NUMÉRIQUE

**Titre** : Loi 25 explicite, données au Québec

**Bullets** :
- Veille : concurrents peu explicites
- IVIA : conformité documentée
- Audio : aucun export externe
- Hébergement OVH, TLS, PostgreSQL
- Sauvegardes AES-256 automatisées

**Notes du conférencier** :
"La souveraineté numérique n'est plus seulement une posture. L'API FastAPI est live sur api.ivia.quebec, avec PostgreSQL 15, Docker, nginx TLS et hébergement OVH VPS. Les sauvegardes AES-256 sont automatisées quotidiennement, et la copie hors-site OVH Québec est en cours. Surtout, la transcription audio est locale : aucune donnée audio ne part vers un tiers."

---

## SLIDE 11 — PIVOT LOI 27

**Titre** : Une obligation légale devient marché

**Bullets** :
- Loi 27 en vigueur
- Employeurs 20+ concernés
- Risques psychosociaux visés
- Besoin hors PAE classique
- IVIA prépare l'offre B2B

**Notes du conférencier** :
"Depuis octobre 2025, la gestion des risques psychosociaux est une obligation réelle pour les employeurs québécois de 20 employés et plus. IVIA n'est pas un PAE, ni un service clinique d'urgence. C'est une infrastructure d'écoute et de structuration qui peut devenir complémentaire aux démarches RH et prévention, lorsque S1 sera stabilisé."

---

## SLIDE 12 — DIFFÉRENCIATEURS STRUCTURELS

**Titre** : Six différenciateurs maintenant vérifiables

**Bullets** :
- Non-clinique assumé, documenté
- Multi-strates, vannes par profil
- Loi 25 intégrée au produit
- Ancrage 11 nations Québec
- Sortie honorable visible

**Complément IP** :
- Indicateur de temporalité décalée : prior art GitHub a2d493c, 9 mai 2026

**Notes du conférencier** :
"Les différenciateurs de v1.3 demeurent, mais plusieurs sont désormais vérifiables dans le produit : profils d'exposition, console admin, journalisation, documents juridiques, transcription locale et droits praticiens. L'indicateur de temporalité décalée reste un actif IP collectif majeur, à développer dans le cadre de recherche."

---

## SLIDE 13 — PROPRIÉTÉ INTELLECTUELLE COLLECTIVE

**Titre** : Prior art public, licences différenciées

**Bullets** :
- Pas de brevet privatif
- Prior art GitHub horodaté
- Licence recherche ouverte encadrée
- Licence commerciale doctrinale
- Volet universitaire à amorcer

**Actifs IP** :
```
1. Indicateur de temporalité décalée
2. Méthode des 4 voies d'entrée
3. Couplage anti-funnel / calendrier
4. Moteur d'exposition par profils
```

**Notes du conférencier** :
"La stratégie IP ne consiste pas à verrouiller la connaissance commune, mais à empêcher son appropriation abusive. Depuis v1.3, un nouvel actif technique s'ajoute : l'architecture moteur plein / vannes par profil, qui permet de séparer capacité analytique et exposition légale. Cette logique renforce la valeur commerciale sans trahir la doctrine."

---

## SLIDE 14 — LA CONCURRENCE

**Titre** : IVIA seul sur l'intersection critique

**Tableau de positionnement** :
```
Critère                 IVIA   Inkblot TELUS BetterHelp Teladoc
FR québécois natif       ✓      ~       ~     ✗          ✗
Loi 25 explicite         ✓      ✗       ✗     ✗          ✗
Audio local souverain    ✓      ✗       ✗     ✗          ✗
Non-clinique structuré   ✓      ✗       ✗     ✗          ✗
Sortie honorable         ✓      ✗       ✗     ✗          ✗
Vannes inférences        ✓      ✗       ✗     ✗          ✗
```

**Bullets** :
- Concurrents puissants, mais génériques
- Peu d'ancrage Loi 25
- Peu de transparence doctrinale
- IVIA : niche québécoise défendable

**Notes du conférencier** :
"Inkblot, TELUS, BetterHelp et Teladoc disposent de moyens supérieurs. Mais ils ne combinent pas l'ancrage québécois, la Loi 25 explicite, l'audio local, la doctrine anti-funnel, la non-substitution clinique et les vannes d'inférence. IVIA ne les affronte pas frontalement : il occupe une intersection très précise."

---

## SLIDE 15 — INFRASTRUCTURE STRATÉGIQUE

**Titre** : Une stack production déjà opérante

**Bullets** :
- FastAPI live, PostgreSQL 15
- Docker, nginx TLS, OVH
- Console admin complète
- Transcription locale opérationnelle
- Audit et sauvegardes chiffrées

**État production — juillet 2026** :
```
Frontend          https://ivia.quebec
API               https://api.ivia.quebec
Admin             /admin/ séparé
Séance            LiveKit audio/vidéo
Transcription     faster-whisper local
Sauvegardes       AES-256, cron quotidien
```

**Notes du conférencier** :
"Cette slide change fortement. En v1.3, l'infrastructure était une fondation prévue. En v2.0, elle existe : frontend live, API live, base PostgreSQL 15, Docker, nginx TLS, LiveKit, console admin, transcription locale, sauvegardes chiffrées. La plateforme est prête pour l'onboarding de praticiens partenaires, avec un praticien actif aujourd'hui : le fondateur."

---

## SLIDE 16 — MODÈLE ÉCONOMIQUE PILOTE

**Titre** : Pilote construit, coût fortement réduit

**Bullets** :
- 80 $ CAD / 60 minutes
- Stripe live + mode test
- Offre gratuite activable
- Palier 1 quasi-autofinancé
- IA : levier de productivité

**Comparaison honnête** :
```
BetterHelp        240-400 $ USD / mois
Talkspace         396 $ USD / mois
Inkblot Therapy   ~90 $ CAD / heure
Psychologue privé 120-180 $ CAD / séance
IVIA pilote       80 $ CAD / séance
```

**Notes du conférencier** :
"Le changement économique majeur est l'exécution frugale. Le plan prévoyait environ 50 K$ pour construire le palier 1 pilote. En pratique, le palier 1 a été construit en quasi-autofinancement, pour une fraction du budget prévu, grâce au développement assisté par IA et à une architecture très concentrée. Le financement demandé sert donc moins à prouver que le produit peut exister qu'à accélérer son déploiement responsable."

---

## SLIDE 17 — MODÈLE ÉCONOMIQUE 36 MOIS

**Titre** : Trajectoire progressive, gates Go/No-Go

**Tableau** :
```
            M3      M6      M12     M18     M27     M36
Praticiens   2       8       15      45      140     350
MRR         500$    3,5K$   8,5K$   28K$    68K$   155K$
ARR          -      42K$    102K$   335K$   810K$  1,86M$
Marge brute  -      ~55%    ~58%    ~62%    ~66%   ~70%
```

**Bullets** :
- Hypothèse conservatrice maintenue
- Gates avant chaque palier
- Équilibre vers M28-M30
- B2B seulement après stabilité

**Notes du conférencier** :
"Les cibles économiques de v1.3 restent une trajectoire, pas une promesse. La nouveauté est que le risque technique initial a diminué : les briques principales sont construites. Le risque se déplace maintenant vers l'acquisition, l'onboarding, la conformité opérationnelle et la rétention praticien-client."

---

## SLIDE 18 — TRACTION

**Titre** : Production réelle — actifs live vérifiables

**Bullets** :
- ivia.quebec et API live
- Parcours client bout en bout
- Console admin complète
- Moteur analytique propriétaire déployé
- Corpus juridique v1.1 / v2.0

**Actifs en production** :
```
Site public + espace client + espace praticien + /admin/
Intake magic link → réservation → paiement → séance
LiveKit audio/vidéo → enregistrement → transcription locale
Analyse prosodique locale + sémantique Claude/Anthropic
Profilage 5 couches, vannes par profil, audit accès
Comptes, demandes, vigilance, comptabilité, facturation
CGU, confidentialité, contrat praticien, cadre IP
```

**Notes du conférencier** :
"C'est la slide qui change le plus. En mai, la traction était surtout une fondation et un calendrier. En juillet, la traction est produit : plateforme live, API live, parcours client complet, paiement Stripe, séances LiveKit, enregistrement, transcription IA locale, documents validés, console admin, profilage contrôlé, droits praticiens, audit et corpus juridique. Il y a un praticien actif — le fondateur — et la plateforme est prête pour l'onboarding de partenaires."

---

## SLIDE 19 — ROADMAP 36 MOIS

**Titre** : Palier 0 réalisé, accélération contrôlée

**Visuel texte** :
```
P0 Réalisé     | Produit live + pilote technique        | Juillet 2026
P1 T3 2026     | Onboarding partenaires S1              | Gate: 30+ séances
P2 T4 2026     | Cohorte 5-8 + opérations admin         | Gate: MRR 2K$+
P3 S1 2027     | Signaux, qualité, conformité S2        | Gate: MRR 8K$+
P4 S2 2027     | B2B Loi 27 + S2 encadré                | Gate: MRR 25K$+
P5 2028-2029   | S3/S4 + recherche + modèle propriétaire| Cible: 155K$ MRR
```

**Bullets** :
- Palier 0 : réalisé
- Pilote technique : réalisé
- Prochaine étape : partenaires S1
- B2B après preuve d'usage
- Recherche après données gouvernées

**Notes du conférencier** :
"La roadmap est recalée à partir de juillet 2026. Le palier 0 et le pilote technique ne sont plus devant nous : ils sont réalisés. Les prochains jalons sont l'onboarding de praticiens partenaires, la preuve d'usage réelle, la stabilisation opérationnelle, puis l'ouverture progressive vers B2B Loi 27, S2, S3, S4 et recherche universitaire."

---

## SLIDE 20 — L'ÉQUIPE

**Titre** : Fondateur opérateur, produit construit

**Bullets** :
- David Phaneuf, fondateur
- Full-stack, IA, gouvernance
- Praticien actif initial
- Exécution frugale démontrée
- Recrutements par gates

**Plan recrutement** :
```
T3-T4 2026  Conseiller juridique + praticiens partenaires
2027        Support dev + partenariats + conformité
2028        Commercial B2B + data scientist
2029        ML engineer + opérations multi-strates
```

**Portage juridique (trajectoire assumée — BP §2.1.0)** :
```
Aujourd'hui   Entreprise individuelle (NEQ en cours d'obtention)
Moyen terme   IVIA OBNL — mission, financements publics/philanthropiques
Ensuite       Entité commerciale — MERLIN, B2B Loi 27, capital privé, RS&DE/CRIC
```

**Notes du conférencier** :
"Le portage juridique suit la même logique que les recrutements : par gates,
sans précipitation. Aujourd'hui l'exploitation est portée par le fondateur en
entreprise individuelle — l'immatriculation est en cours. L'OBNL vient porter
la mission et ouvrir les financements publics ; l'entité commerciale vient
ensuite porter la technologie, les revenus et le capital. Rien n'est
revendiqué avant d'exister. Le risque fondateur existe et reste lucide. Mais l'exécution récente réduit une incertitude majeure : une seule personne a construit et mis en production une plateforme complète, en quasi-autofinancement, avec assistance IA. La priorité n'est pas de grossir vite : c'est d'ajouter les bonnes personnes aux bons gates, sans diluer la doctrine."

---

## SLIDE 21 — POURQUOI MAINTENANT

**Titre** : La fenêtre est ouverte maintenant

**Bullets** :
- Produit live, pas promesse
- Loi 27 crée la demande
- Loi 25 favorise le local
- Confiance apps IA fragilisée
- Données gouvernées dès aujourd'hui

**Notes du conférencier** :
"Pourquoi maintenant ? Parce que le besoin est massif, les obligations employeurs sont en vigueur, la souveraineté numérique devient un critère réel, et la confiance envers les apps de santé mentale génériques est fragilisée. IVIA arrive au bon moment avec un avantage nouveau : le produit n'est plus théorique. Il est live et peut commencer à accumuler des données gouvernées."

---

## SLIDE 22 — RISQUES PRINCIPAUX + MITIGATIONS

**Titre** : Lucidité opérationnelle, mitigations concrètes

**Tableau** :
```
Risque                         Prob.   Mitigation
Adoption praticiens lente       Moyen   Onboarding restreint, accompagnement serré
Sous-performance MRR            Moyen   Gates, offres gratuites, itérations
Risque conformité S2            Moyen   Audit avant ouverture ordres
Épuisement fondateur            Moyen   Financement support et délégation
Dérive analytique IA            Faible  Vannes, audit, validation humaine
```

**Notes du conférencier** :
"Les risques ont évolué. Le risque principal n'est plus : peut-on construire la plateforme ? La réponse est oui. Les risques sont maintenant l'adoption, la stabilité opérationnelle, la conformité à mesure que les profils se diversifient, et la capacité de délégation autour du fondateur. Les mécanismes de mitigation sont intégrés : gates, audit, vannes, validation humaine, et onboarding graduel."

---

## SLIDE 23 — LE BESOIN EN FINANCEMENT

**Titre** : Financer l'accélération, pas l'existence

**Bullets** :
- Palier 1 construit frugalement — la preuve technique existe
- Besoin total 36 mois : **2 200 000 $ CAD** (BP v2.4, §1.2)
- **54,5 % non-dilutif d'abord** : subventions + crédits d'impôt avant tout capital
- Programmes publics cartographiés : RS&DE · CRIC · Fondaction · Filaction · FAQDD · Investissement Québec · CDAE · PARI-CNRC · Mitacs
- Capital patient aligné doctrine (dilutif ≤ 25 % du capital)
- Portage par étapes : indépendant (NEQ en cours) → OBNL → entité commerciale — chaque demande déposée par le véhicule admissible

**Structure cible 36 mois (BP v2.4)** :
```
Subventions et fonds publics non-dilutifs        920 000 $   41,8 %
Crédits d'impôt remboursables (RS&DE, CRIC)      280 000 $   12,7 %
Capital patient / capital de risque à mission    600 000 $   27,3 %
Prêts patients / BDC (à partir Palier 2)         200 000 $    9,1 %
Auto-financement (revenus opérationnels nets)    200 000 $    9,1 %
TOTAL                                          2 200 000 $  100,0 %
```

**Notes du conférencier** :
"Le besoin de financement se lit différemment depuis la mise en production. On ne demande pas au capital de financer une preuve abstraite : la preuve technique existe. L'emboîtement est explicite : les programmes publics financent l'amorce et l'innovation — R&D, conformité, structuration des analyses — pendant que le capital patient finance ce que le non-dilutif ne couvre pas : rémunération du fondateur, capital de roulement, accélération de la mise en marché. Plus de la moitié du besoin est non-dilutive par conception."

---

## SLIDE 24 — L'USAGE DES FONDS

**Titre** : Chaque dollar rattaché à un gate

**Tableau (BP v2.4, §6.1.2)** :
```
Rémunération fondateur (75-90 K$/an)      300 000 $   13,6 %
Recrutements salariés (dès Palier 2)      540 000 $   24,5 %
R&D pipeline et modèles propriétaires     500 000 $   22,7 %
Marketing, contenu, partenariats          220 000 $   10,0 %
Charges structurelles                     300 000 $   13,6 %
Investissement actifs                     130 000 $    5,9 %
Frais bancaires, assurances, divers       100 000 $    4,5 %
Constitution juridique et fiscale          50 000 $    2,3 %
Réserve doctrinale                         60 000 $    2,7 %
TOTAL                                   2 200 000 $  100,0 %
```

**Bullets** :
- Priorité : sécurité, conformité, opérations
- Support fondateur explicite (300 K$ / 36 mois)
- Réserve doctrinale : audits + fiducie de mission
- B2B Loi 27 après preuve S1
- Ajustable par gates réels, pas par calendrier

**Notes du conférencier** :
"L'usage des fonds doit suivre la réalité. Le palier technique ayant été construit à coût très réduit, la part principale va aux personnes — fondateur et recrutements — et à la R&D gouvernée. La réserve doctrinale est assumée comme une ligne budgétaire à part entière : audits doctrinaux, comité consultatif, fiducie de mission. Les montants sont pilotés par gates, pas par calendrier rigide."

---

## SLIDE 25 — LES CHIFFRES CIBLES M36

**Titre** : L'état cible en juillet 2029

**Bullets** :
- 350 praticiens actifs
- MRR cible : 155 000 $
- ARR cible : 1,86 M$
- Équipe : 7-8 personnes
- Modèle propriétaire opérationnel

**Cibles qualitatives** :
```
Dataset synthétique : 5 000+ cas gouvernés
Pipeline transformation : auditable et documenté
Recherche : co-publication scientifique visée
Doctrine : rapport annuel public
Équilibre courant : M28-M30
```

**Notes du conférencier** :
"En juillet 2029, l'objectif n'est pas seulement une taille de revenus. C'est une infrastructure québécoise durable : praticiens actifs, modèle propriétaire, données synthétiques gouvernées, recherche universitaire, doctrine publique, et équilibre courant. La valorisation cible découle de cette crédibilité, pas d'une croissance artificielle."

---

## SLIDE 26 — CONTACT

**Titre** : Ce que signifie investir dans IVIA

**Transition avant conclusion** :

Notre logique de financement repose sur une articulation simple :

- Les dispositifs publics appuient les briques d'innovation, de R-D, de structuration et d'expérimentation.
- Les capitaux privés renforcent la continuité d'exploitation, la capacité d'accueil, la consolidation des équipes et la montée en charge.

Cette articulation est cohérente avec la nature même d'IVIA : un projet qui doit à la fois innover, démontrer, protéger les renseignements personnels, et tenir dans le temps comme infrastructure d'accompagnement.

Elle s'incarne dans une trajectoire de portage assumée : l'exploitation actuelle est portée par le fondateur en entreprise individuelle (immatriculation en cours) ; l'OBNL IVIA viendra porter la mission et les financements publics ; une entité commerciale dédiée portera ensuite MERLIN, les contrats B2B et le capital privé. L'investisseur entre dans une séquence claire, pas dans une structure improvisée.

**Conclusion investisseur** :

Investir dans IVIA ne revient pas à financer une application isolée. Il s'agit de rendre possible une architecture complète et durable :

- **IVIA** comme maison du vivant, seuil public d'accueil, de retour et de continuité ;
- **MERLIN** comme coeur d'analyse, de gouvernance et de conformité, dans un cadre aligné avec la Loi 25 et une gestion rigoureuse des renseignements personnels au Québec ;
- **MÉSANGES** comme voix d'accompagnement subtile, opérant dans une logique constante de **Observation / Hypothèse / Orientation**.

L'investissement privé n'est pas pensé en silo. Les programmes publics soutiennent l'amorce, l'innovation, la structuration et la démonstration. L'investissement privé permet de stabiliser, consolider et déployer cette architecture à l'échelle pertinente.

Enfin, IVIA ne propose pas une boîte noire d'IA. Les usages, les coûts et les finalités des capacités d'analyse sont instrumentés, suivis et gouvernés, afin que l'intelligence artificielle reste lisible économiquement, maîtrisable opérationnellement et responsable dans la pratique.

**Message final** : Être investisseur dans IVIA, c'est rendre possible un lieu durable, habitable et responsable pour la santé mentale.

**Contact** :
David Phaneuf, fondateur  
david@ivia.quebec  
invest@ivia.quebec  
ivia.quebec

**Devises** :
Au sein de l'être — En actes.  
Pour le peuple, par le peuple.

**Notes du conférencier** :
"La conclusion du pitch doit être nette : l'investissement porte sur une architecture complète, pas sur un outil isolé. Les programmes publics soutiennent l'amorce et l'innovation, les capitaux privés soutiennent la continuité, la consolidation et le déploiement. IVIA garde une posture de gouvernance claire : conformité, lisibilité des coûts IA, et progression par paliers. La prochaine étape est simple : voir le produit, examiner les documents, valider les risques, puis financer l'accélération responsable."

---

## ANNEXE — VEILLE CONCURRENTIELLE CONSERVÉE

**Titre** : Méthodologie et sources de la veille — 20 services évalués

### Méthodologie

- **Date de la veille v1.3** : 9 mai 2026
- **Mode de collecte** : visite directe des sites officiels
- **Nombre de critères** : 14 critères par service
- **Critères clés** : Loi 25, PIPEDA/LPRPDE, langue FR, modèle clinique, format asynchrone, ancrage territorial, sortie honorable, tarification, voie corps/fréquence, indicateur unique, partenariat universitaire, modèle d'affaires
- **Position v2.0** : veille conservée, différenciation renforcée par production réelle

### Services internationaux dominants

| # | Service | Résultat Loi 25 |
|---|---------|-----------------|
| 1 | BetterHelp | Zéro mention explicite |
| 2 | Talkspace | Zéro mention explicite |
| 3 | Grow Therapy | Zéro mention explicite |
| 4 | Amwell | Zéro mention explicite |
| 5 | Teladoc Canada | Zéro mention explicite |
| 6 | Sesame Care | Zéro mention explicite |
| 7 | Brightside | Zéro mention explicite |
| 8 | LiveHealth Online | Zéro mention explicite |
| 9 | Doctor on Demand | Zéro mention explicite |
| 10 | MDLIVE | Zéro mention explicite |
| 11 | Regain | Zéro mention explicite |
| 12 | Faithful Counseling | Zéro mention explicite |
| 13 | Pride Counseling | Zéro mention explicite |
| 14 | Online-Therapy.com | Zéro mention explicite |
| 15 | OurRitual | Zéro mention explicite |

**Résultat Groupe 1** : 15/15 — zéro mention explicite de la Loi 25 du Québec.

### Acteurs canadiens/internationaux comparables

| # | Service | Résultat Loi 25 | Reconnaissance autochtone |
|---|---------|-----------------|--------------------------|
| 1 | Wysa | Non mentionnée | Non |
| 2 | Woebot | Non mentionnée | Non |
| 3 | Inkblot Therapy | Non mentionnée | Non |
| 4 | TELUS Santé | Non mentionnée | Partielle |
| 5 | LifeWorks | Non mentionnée | Non |

**Résultat Groupe 2** : 0/5 sur Loi 25 explicite — 1/5 sur reconnaissance autochtone partielle.

### Position IVIA v2.0

- Conformité Loi 25 explicite, documentée, auditable
- Ancrage 11 nations autochtones du Québec
- Transcription audio locale, aucune sortie serveur
- Moteur analytique propriétaire avec vannes d'exposition
- Sortie honorable visible, sans commission d'orientation

---

## NOTES DE MISE EN PRODUCTION POWERPOINT

Pour la conversion de ce deck en PowerPoint :

1. Créer une diapositive maître avec :
   - Police titre : Trebuchet MS Bold
   - Police corps : Calibri
   - Accent : #20808D (teal IVIA)
   - Fond : blanc
   - Logo IVIA : coin supérieur gauche, hauteur 40px

2. Slides à traitement visuel prioritaire :
   - Slide 5 : parcours produit live
   - Slide 6 : schéma 4 strates horizontal
   - Slide 7 : pipeline gouverné en flèches
   - Slide 8 : moat en quatre piliers
   - Slide 15 : architecture production
   - Slide 18 : actifs live vérifiables
   - Slide 19 : Gantt recalé juillet 2026

3. Slides avec tableau de données :
   - Slide 9 : TAM Québec
   - Slide 14 : concurrence
   - Slide 16 : comparaison tarifaire
   - Slide 17 : trajectoire P&L
   - Slide 24 : usage des fonds

4. Durée recommandée : 25-30 minutes + 10-15 minutes Q&A

5. Version courte (12 slides) : conserver 1, 2, 3, 5, 9, 10, 12, 15, 18, 19, 23, 26

---

## CHANGELOG v1.3 → v2.0

| # | Slide | Type | Contenu |
|---|-------|------|---------|
| 1 | Couverture | Mise à jour | Version 2.0, date 6 juillet 2026, produit en production |
| 2 | Offre | Révision majeure | Offre décrite comme produit live, pas seulement grille tarifaire |
| 3 | Pipeline | Actualisation | Ajout transcription locale faster-whisper et audit accès sensibles |
| 4 | Moat | Renforcement | Moteur propriétaire et vannes par profil intégrés |
| 5 | Souveraineté | Actualisation | API live, OVH, PostgreSQL, sauvegardes AES-256 |
| 6 | Infrastructure | Révision majeure | Frontend/API/Admin/LiveKit/transcription en production |
| 7 | Modèle pilote | Révision | Palier 1 construit en quasi-autofinancement |
| 8 | Traction | Réécriture complète | Actifs production listés et parcours bout en bout fonctionnel |
| 9 | Roadmap | Recalage | Palier 0 et pilote technique réalisés, jalons depuis juillet 2026 |
| 10 | Besoin | Révision | Financement orienté accélération, conformité, onboarding |

---

**Au sein de l'être — En actes.**  
**Pour le peuple, par le peuple.**

*Pitch Deck V2.0 — 6 juillet 2026*  
*IVIA / MERLIN — Confidentiel*

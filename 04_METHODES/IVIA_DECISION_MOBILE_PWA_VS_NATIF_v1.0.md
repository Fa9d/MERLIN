# DÉCISION MOBILE — PWA vs App Native — IVIA
## Document de décision argumentée

**Version** : 1.0  
**Date** : 9 mai 2026  
**Statut** : Décision actée — Phase pilote  
**Auteur** : David Phaneuf (fondateur) + Perplexity Computer (analyse)  
**Contexte** : Réponse à la question de David : "Nous devons aussi prévoir une connexion simple par téléphone portable donc la création d'une app mobile ? À moins que site puisse le faire."  
**Cohérence** : Aligné avec `IVIA_STRATEGIE_TECHNOLOGIQUE_36MOIS_v1.0.md`, `IVIA_ANALYSE_STACK_OUTILS_v1.1.md`, `IVIA_SPEC_PWA_v1.0.md`

---

## RÉSUMÉ EXÉCUTIF — Verdict en 5 lignes

**Verdict : PWA (Progressive Web App), maintenant. App native, si et seulement si les seuils définis plus bas sont atteints.**

Le site IVIA actuel (Python + build_pages.py) peut être étendu en PWA en 10 jours-développeur, sans changer de codebase. Une PWA installable sur l'écran d'accueil iOS et Android couvre 100 % des besoins pilote : accès mobile, notifications push, audio offline. Les coûts App Store / Google Play (frais annuels, commissions 15-30 %, délais de révision) ne se justifient pas avant 500 utilisateurs actifs et des besoins capteurs non couverts par les APIs web. La doctrine IVIA — itération rapide, souveraineté des données, frais minimaux en phase pilote — valide la PWA sans réserve. La bascule vers natif est planifiée à M18-M24 sous conditions précises.

---

## 1. CRITÈRES D'ÉVALUATION

### 1.1 Coût total (CAPEX + OPEX sur 36 mois)

Le coût total inclut : développement initial, maintenance annuelle, frais stores, certifications Apple, infrastructure backend push, mises à jour OS.

### 1.2 Time-to-market

Délai entre la décision et le premier utilisateur pilote qui peut accéder à IVIA depuis son téléphone.

### 1.3 Commissions stores

Apple App Store : 30 % (15 % pour revenus sous 1 M$). Google Play : 30 % (15 % sous 1 M$). Applicables à tout paiement in-app.

### 1.4 Contrôle UX

Capacité à modifier l'interface sans passer par la révision d'un store. Délai moyen App Store : 24-72 h. Révisions rejetées : environ 15 % des soumissions.

### 1.5 Accès APIs natives

| Fonctionnalité | PWA (Web APIs) | React Native | Flutter | Swift+Kotlin |
|---|---|---|---|---|
| Notifications push | Oui (Web Push) | Oui | Oui | Oui |
| Audio offline | Oui (Cache API) | Oui | Oui | Oui |
| Microphone | Oui (MediaDevices) | Oui | Oui | Oui |
| Caméra | Oui (MediaDevices) | Oui | Oui | Oui |
| Géolocalisation | Oui (Geolocation API) | Oui | Oui | Oui |
| Bluetooth | Non (limité) | Oui | Oui | Oui |
| Apple Watch | Non | Oui (watchOS) | Non natif | Oui |
| HealthKit | Non | Partiel | Non | Oui |
| Google Fit | Non | Oui | Partiel | Oui |
| NFC | Non (Android only partiel) | Oui | Oui | Oui |
| Face ID / Touch ID | Oui (WebAuthn) | Oui | Oui | Oui |

**Conclusion accès APIs** : Pour la phase pilote (audio, push, micro, caméra, géoloc), la PWA couvre tout. Les lacunes (Watch, HealthKit, Bluetooth) ne concernent pas les besoins des 12 premiers mois.

### 1.6 Distribution

PWA : URL directe, pas de store. React Native / Flutter / Swift+Kotlin : soumission obligatoire, délais, risques de rejet.

### 1.7 Mises à jour

PWA : déploiement immédiat côté serveur, Service Worker met à jour le cache en arrière-plan. App native : soumission, révision 24-72 h (App Store) ou quelques heures (Google Play), puis adoption progressive par les utilisateurs.

### 1.8 Conformité Loi 25

PWA hébergée sur infrastructure contrôlée (serveur Québec ou Canada) : conformité totale. App Store / Google Play : les stores collectent des métadonnées d'installation et d'usage — vecteur de risque Loi 25 à documenter et à atténuer.

### 1.9 Risques de rejet store

Apple rejette pour : contenu non conforme, modèle de paiement contournant l'IAP, interfaces jugées "web wrappers". IVIA pourrait être rejeté si Apple considère que l'app est une coquille WebView sans valeur native ajoutée. Risque réel et non trivial à coût zéro de mitigation via PWA.

---

## 2. TABLEAU COMPARATIF — 4 OPTIONS

| Critère | **PWA** | **React Native** | **Flutter** | **Swift + Kotlin** |
|---|---|---|---|---|
| **CAPEX dev initial (CAD)** | 5 000 – 10 000 | 35 000 – 60 000 | 30 000 – 55 000 | 60 000 – 100 000 |
| **OPEX annuel maintenance (CAD)** | 2 000 – 5 000 | 8 000 – 15 000 | 7 000 – 14 000 | 12 000 – 20 000 |
| **Frais stores annuels (CAD)** | 0 | ~130 (Google) + ~130 (Apple) | ~130 + ~130 | ~130 + ~130 |
| **Certif Apple (CAD)** | 0 | ~130/an | ~130/an | ~130/an |
| **Commission stores sur revenus** | 0 % | 15-30 % | 15-30 % | 15-30 % |
| **Time-to-market** | 10 jours-dev | 3-5 mois | 3-5 mois | 6-12 mois |
| **Délai mises à jour** | Immédiat | 24-72 h (iOS) | 24-72 h (iOS) | 24-72 h (iOS) |
| **Codebase** | Unique (HTML/CSS/JS) | Unique (JS/TS) | Unique (Dart) | Double (Swift + Kotlin) |
| **Risque rejet store** | 0 (aucun store) | Moyen | Moyen | Élevé (Apple Watch content) |
| **iOS installation** | Safari 16.4+ (2023) | App Store | App Store | App Store |
| **Android installation** | Chrome, auto-prompt | Play Store | Play Store | Play Store |
| **Contrôle UX total** | Oui | Partiel (HIG Apple) | Partiel | Limité (guidelines stores) |
| **Accès HealthKit** | Non | Partiel | Non | Oui |
| **Accès Bluetooth BLE** | Limité | Oui | Oui | Oui |
| **Conformité Loi 25** | Maximale | Bonne (avec config) | Bonne (avec config) | Bonne (avec config) |
| **Expertise requise** | Dev web existant | Dev JS/TS mobile | Dev Dart | Dev iOS + Dev Android |
| **COÛT TOTAL 36 MOIS (CAD)** | **11 000 – 25 000** | **65 000 – 115 000** | **58 000 – 100 000** | **100 000 – 165 000** |

---

## 3. COÛTS CHIFFRÉS DÉTAILLÉS SUR 36 MOIS (CAD 2026)

### 3.1 Option PWA — Coût total : 11 000 – 25 000 CAD

| Poste | Coût estimé (CAD) | Notes |
|---|---|---|
| Dev initial (manifest, SW, push) | 5 000 – 10 000 | 10 jours × 500-1000$/j dev freelance |
| Maintenance annuelle (patches, OS, tests) | 2 000 – 5 000/an | 4-10 j/an |
| Backend push (FastAPI + VAPID) | 0 – 2 000 | Sur infra existante ou Fly.io/Railway |
| Certificat SSL (déjà actif ivia.pplx.app) | 0 | Let's Encrypt |
| Frais store | 0 | Aucun store |
| Commission sur revenus | 0 % | Distribution directe |
| Icônes, screenshots PWA Builder | 500 – 1 000 | Design graphique |
| Tests iOS + Android (appareils réels) | 0 – 1 000 | TestFlight non requis, tests manuels |
| **Total 36 mois** | **11 000 – 25 000** | |

### 3.2 Option React Native — Coût total : 65 000 – 115 000 CAD

| Poste | Coût estimé (CAD) | Notes |
|---|---|---|
| Dev initial | 35 000 – 60 000 | 3-5 mois × 1 dev mobile sénior |
| Maintenance annuelle | 8 000 – 15 000/an | Mises à jour React Native, Expo |
| Apple Developer Program | 130/an | Obligatoire |
| Google Play Console | 35 (one-time) + ~95/an taxes | |
| Soumissions / révisions | 1 000 – 3 000 | Délais, rejets potentiels |
| Commission stores (sur revenus) | 15-30 % | Sur chaque paiement in-app |
| Infra backend | 1 200 – 3 600/an | Similaire à PWA |
| **Total 36 mois** | **65 000 – 115 000** | Hors commissions sur revenus |

### 3.3 Option Flutter — Coût total : 58 000 – 100 000 CAD

| Poste | Coût estimé (CAD) | Notes |
|---|---|---|
| Dev initial | 30 000 – 55 000 | Dart, moins de devs disponibles au Québec |
| Maintenance annuelle | 7 000 – 14 000/an | Flutter majors (ex : migration Dart 3) |
| Stores (Apple + Google) | 225/an | |
| Commission stores | 15-30 % | |
| **Total 36 mois** | **58 000 – 100 000** | |

### 3.4 Option Swift + Kotlin — Coût total : 100 000 – 165 000 CAD

| Poste | Coût estimé (CAD) | Notes |
|---|---|---|
| Dev initial iOS (Swift) | 35 000 – 60 000 | |
| Dev initial Android (Kotlin) | 25 000 – 40 000 | |
| Maintenance (2 codebases) | 12 000 – 20 000/an | |
| Stores | 225/an | |
| Commission stores | 15-30 % | |
| **Total 36 mois** | **100 000 – 165 000** | |

### 3.5 Synthèse — Économie réalisée en choisissant PWA

Versus React Native : **54 000 – 90 000 CAD** économisés sur 36 mois, plus commissions non encourues.  
Versus Swift+Kotlin : **89 000 – 140 000 CAD** économisés sur 36 mois.  

Ces économies réinvesties dans la doctrine, le contenu et les praticiens représentent la vraie valeur de la décision.

---

## 4. VERDICT ET JUSTIFICATION DOCTRINAIRE

### 4.1 Verdict

**PWA, maintenant. Sans condition pour la phase pilote (M1-M18).**

### 4.2 Justification par les faits

Le site ivia.pplx.app est déjà HTTPS, déjà servi en HTML/CSS/JS, déjà sur une infrastructure maîtrisée. Ajouter un `manifest.json` et un `sw.js` transforme ce site en PWA installable en 10 jours-développeur. L'utilisateur pilote — praticien ou client — peut installer IVIA sur son téléphone depuis Safari (iOS 16.4+) ou Chrome (Android) exactement comme une app native. L'icône s'affiche sur l'écran d'accueil. L'app s'ouvre en plein écran, sans barre de navigation. L'audio se joue hors ligne. Les notifications push arrivent.

Il n'y a aucun besoin fonctionnel identifié pour la phase pilote qui exige une app native.

### 4.3 Justification doctrinaire — "En actes"

La devise "En actes" n'est pas un slogan. Elle signifie que la doctrine IVIA se réalise par des gestes concrets, rapides, mesurables. Une app native prend 3 à 12 mois à construire, 24 à 72 heures à mettre à jour à chaque itération, et cède 30 % de ses revenus aux stores. Une PWA se déploie en minutes, se met à jour en secondes, ne paie aucune commission.

L'itération rapide — corriger un parcours client après un retour terrain à 8h du matin, déployer la correction à 9h — est une expression directe de "En actes." L'app native rend cela structurellement impossible.

La devise "Pour le peuple, par le peuple" implique une accessibilité maximale. Une PWA fonctionne sur tout navigateur récent, sans passer par un store, sans compte Apple ou Google requis pour télécharger quoi que ce soit. C'est plus accessible, pas moins.

### 4.4 Justification par la Loi 25

L'App Store et le Google Play collectent des métadonnées d'installation, des données d'usage et des identifiants publicitaires par défaut. La PWA, déployée sur infrastructure contrôlée sans tracker tiers, est la solution la plus conforme à la Loi 25 par conception.

---

## 5. ROADMAP 36 MOIS — PWA D'ABORD, CONDITIONS DE BASCULE

### Phase 1 — PWA pilote (M1-M12, été 2026 – été 2027)

| Sprint | Livrable | Durée |
|---|---|---|
| S1 | manifest.json + icônes + meta tags | 2 jours |
| S2 | Service Worker (cache app shell, audio offline) | 2 jours |
| S3 | Backend push VAPID + opt-in conforme Loi 25 | 2 jours |
| S4 | Page offline.html + banner état connexion | 1 jour |
| S5 | Audit Lighthouse + tests iOS + Android | 2 jours |

Spécification complète : `IVIA_SPEC_PWA_v1.0.md`

### Phase 2 — PWA production (M12-M18, été 2027)

- Optimisation Lighthouse > 90 sur tous critères
- Notifications push segmentées par praticien
- Formulaires PWA (consentement, notes de séance) cachés offline
- Envisager PWA dans Chrome Web Store (gratuit, améliore visibilité Android)

### Phase 3 — Décision natif (M18-M24, décembre 2027 – juin 2028)

**La bascule vers app native se déclenche si et seulement si :**

| Condition | Seuil de déclenchement |
|---|---|
| Utilisateurs actifs mensuels | ≥ 500 UAM |
| Revenus mensuels récurrents | ≥ 15 000 CAD MRR |
| Besoin Apple Watch confirmé | Demandé par ≥ 3 praticiens actifs |
| Besoin Bluetooth / capteurs bio | Partenariat appareil signé |
| Besoin HealthKit / Google Fit | Intégration clinique validée |
| Revenus justifiant commissions 15 % | ROI positif calculé sur 12 mois |

Si ces seuils sont atteints : React Native avec Expo est l'option recommandée (codebase JS proche du web, expo-dev-client permet tests sans store, communauté active au Québec).

Si seulement iOS atteint les seuils : Swift natif pour l'expérience Apple Watch.

---

## 6. RISQUES PWA ET ATTÉNUATIONS

| Risque | Probabilité | Impact | Atténuation |
|---|---|---|---|
| Perception "moins pro" qu'une vraie app | Faible | Moyen | Communication claire : "IVIA est accessible depuis votre navigateur, aucun store requis" — positionner comme avantage (accessibilité, vie privée) |
| iOS Safari : limitations push notifications (avant iOS 16.4) | Faible (profil cible = 2026) | Moyen | Cibler iOS 16.4+ documenté, prévoir fallback SMS/courriel pour anciens iOS |
| Bannière d'installation moins visible qu'une app store | Moyen | Faible | Instructions visuelles dédiées sur la page d'accueil (animation "Partager → Sur l'écran d'accueil") |
| Service Worker : bugs de cache difficiles à déboguer | Moyen | Moyen | Versioning strict du SW, bouton "Vider le cache" pour l'utilisateur, tests Lighthouse à chaque déploiement |
| Push notifications bloquées par l'utilisateur | Élevé | Faible | Push opt-in granulaire avec valeur explicite (rappel RDV), fallback courriel |
| Perte de visibilité (pas dans l'App Store) | Moyen | Faible-Moyen | Distribution directe par lien, QR code, courriel praticien. Phase pilote = distribution contrôlée, pas besoin de découvrabilité store |
| Audio offline : mise à jour des fichiers praticiens | Faible | Moyen | Versioning Cache API, invalidation sur changement de fichier (hash dans le nom) |
| Dépendance à une connexion minimale au premier chargement | Faible (PWA) | Faible | App shell précaché, page offline.html dédiée |

---

## 7. DÉCISIONS À ARBITRER PAR DAVID

Ces questions sont ouvertes et nécessitent une décision avant l'implémentation.

**7.1 Hébergement backend push (VAPID)**  
Les notifications push nécessitent un serveur backend (FastAPI/Python). Trois options : (a) sur l'infra ivia.pplx.app existante, (b) Railway.app (serveur Canada par défaut), (c) Fly.io (choix région ca-central). Quelle option est conforme à ta lecture de la Loi 25 et à ton budget infra ?

**7.2 Fournisseur VAPID ou service push tiers**  
Option A : VAPID auto-hébergé (gratuit, complexité opérationnelle modérée). Option B : OneSignal (gratuit jusqu'à 10 000 abonnés, serveurs USA — potentiel conflit Loi 25). Option C : Novu (open-source, auto-hébergeable). La doctrine IVIA recommande le VAPID auto-hébergé, mais confirmes-tu ?

**7.3 Nom court de l'app (manifest "short_name")**  
Le champ `short_name` du manifest s'affiche sous l'icône sur l'écran d'accueil. Options : "IVIA" (recommandé), "IVIA+", "IVIA Accomp." (trop long). Confirmation ?

**7.4 Couleur de thème (theme_color)**  
Le `theme_color` colorie la barre de statut sur Android et l'en-tête de Safari sur iOS lors de l'ouverture en standalone. La palette actuelle (vrille : #C58A8A, #D9A441, #6B8266) suggère `#C58A8A` (rouge rosé) ou une couleur neutre de fond. Laquelle retiens-tu ?

**7.5 Stratégie icônes**  
Les icônes PWA doivent être produites en 8 tailles. Utilise-t-on le logo IVIA actuel (cercle + vrille SVG), une version simplifiée, ou un pictogramme dédié mobile ? La spécification `IVIA_SPEC_PWA_v1.0.md` propose la palette dérivée — à valider visuellement avant production.

**7.6 Consentement push — moment de la demande**  
Demander l'autorisation push (a) à l'installation, (b) après la première séance, ou (c) via une page dédiée "Mes notifications". L'option (c) est la plus conforme Loi 25 (consentement explicite, granulaire, révocable). À confirmer.

**7.7 Périmètre offline**  
Qu'est-ce qui doit fonctionner sans connexion ? Proposition : lecture audio des praticiens (oui), formulaires de séance (oui, sync différée), quiz funnel (non, données serveur requises), messagerie praticien (non). À valider.

---

## 8. RÉFÉRENCES CROISÉES

- Spécification technique complète PWA : `IVIA_SPEC_PWA_v1.0.md`  
- Stack technologique et décisions infra : `IVIA_ANALYSE_STACK_OUTILS_v1.1.md`  
- Stratégie technologique 36 mois : `IVIA_STRATEGIE_TECHNOLOGIQUE_36MOIS_v1.0.md`  
- Page praticiens (shortcut PWA /praticiens) : `IVIA_SPEC_PAGE_PRATICIENS_v1.0.md`  
- Funnel quiz (shortcut PWA /quiz) : `IVIA_FUNNEL_QUIZ_TO_GUIDANCE_v1.1.md`  
- Conformité Loi 25 push et stockage : `12_JURIDIQUE_AFFAIRES/IVIA_CONSENTEMENT_FUNNEL_LOI25_v1.0.md`  

---

*Document produit le 9 mai 2026 — IVIA / MERLIN — "Au sein de l'être — En actes."*

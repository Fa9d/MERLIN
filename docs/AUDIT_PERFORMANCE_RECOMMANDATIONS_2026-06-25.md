# AUDIT PERFORMANCE & RECOMMANDATIONS IVIA/MERLIN
**Date :** 2026-06-25  
**Auteur :** Perplexity AI (session David Faraj / Fa9d)  
**Statut :** RÉSERVÉ — À finaliser lors de la mise en production complète  
**Usage :** Plain text uniquement. Hors images, graphisme, design. Ce document est la base de référence pour l'implémentation future de chaque recommandation.

---

## INSTRUCTIONS D'UTILISATION

Chaque section ci-dessous correspond à un poste de l'entreprise IVIA/MERLIN.  
Pour chaque poste :
- La colonne ÉTAT ACTUEL documente ce qui existe déjà dans le repo au 2026-06-25.
- La colonne GAPS documente ce qui manque.
- La colonne RECOMMANDATIONS documente les actions à mettre en oeuvre.
- La colonne DOCUMENTS À PRODUIRE liste les fichiers à créer.
- La colonne KPIs liste les indicateurs à suivre.

Ce document est mis à jour à chaque sprint ou session de travail majeure.

---

## POSTE 1 — DIRECTION & STRATÉGIE (CEO / Fondateur)

### ÉTAT ACTUEL
- Vision et doctrine formalisées dans 00_DOCTRINE et 00_GOUVERNANCE.
- Analyses Perplexity intégrées (ANALYSE_SORTIE_PERPLEXITY_MERLIN_V_2026-05-13.md).
- Sprint logs présents (SPRINT1_LOG_20260509.md, SPRINT_72H_EXECUTION_MERLIN_2026-05-13.md).
- README.md très court (772 bytes), non orienté investisseur.
- Aucun plan d'affaires formalisé dans le repo.
- Aucun tableau de KPIs de direction.

### GAPS
- Pas de plan d'affaires (PAC, version longue, version courte).
- Pas de pipeline financement documenté.
- README non exploitable pour un investisseur ou partenaire externe.
- Pas de synthèse trimestrielle de performance.

### RECOMMANDATIONS
1. Rédiger un README.md investisseur (vision, produit, traction, ask, contact).
2. Créer un plan d'affaires dans docs/PLAN_AFFAIRES_IVIA_MERLIN.md (version longue).
3. Créer une version courte du plan d'affaires (pitch summary 2 pages) dans docs/PITCH_SUMMARY.md.
4. Créer un tableau de KPIs de direction mis à jour mensuellement dans docs/KPI_DIRECTION.md.
5. Documenter le pipeline financement (BDC, MSSS, SCALE AI, MITACS, autres) dans docs/PIPELINE_FINANCEMENT.md.
6. Produire une synthèse trimestrielle de performance dans docs/SYNTHESE_TRIM_Q{N}_YYYY.md.

### DOCUMENTS À PRODUIRE
- README.md (racine) — vitrine investisseur/praticien
- docs/PLAN_AFFAIRES_IVIA_MERLIN.md
- docs/PITCH_SUMMARY.md
- docs/KPI_DIRECTION.md
- docs/PIPELINE_FINANCEMENT.md
- docs/SYNTHESE_TRIM_Q3_2026.md (premier livrable)

### KPIs DIRECTION
- Nombre de dossiers de financement soumis (cible : 3 par trimestre)
- Nombre de praticiens en pipeline (cible : 10 actifs, 50 en liste attente à 6 mois)
- MRR (Monthly Recurring Revenue) cible mois 6 : 2 000 CAD
- ARR (Annual Recurring Revenue) cible fin année 1 : 24 000 CAD
- Nombre de partenariats institutionnels signés

---

## POSTE 2 — PRODUIT & UX (CPO / Product Manager)

### ÉTAT ACTUEL
- Mockups présents dans ivia_mockups/.
- Site v2 dans ivia_site_v2/.
- Audit parcours client/praticien documenté (AUDIT_FRONTEND_PARCOURS_CLIENT_PRATICIEN_2026-05-13.md).
- Pont post-intake documenté (PONT_POST_INTAKE_IMPLEMENTATION_2026-05-13.md).
- Pas de roadmap produit formelle versionnée.
- Pas de specs fonctionnelles séparées des audits.
- Journal (05_JOURNAUX) conceptuel, non connecté à la UI.

### GAPS
- Roadmap produit absente (12 mois).
- Specs fonctionnelles non formalisées.
- Connexion méthode IVIA <-> UI non documentée.
- Pas de définition formelle des parcours utilisateur praticien et client.

### RECOMMANDATIONS
1. Créer une roadmap produit dans docs/ROADMAP_PRODUIT.md (12 mois, milestones, features liées aux issues GitHub).
2. Formaliser les specs fonctionnelles pour chaque module dans docs/SPECS/.
3. Documenter la connexion méthode IVIA <-> UI dans docs/METHODE_UI_MAPPING.md.
4. Définir les parcours utilisateur formels (praticien onboarding, séance 50+10, journal client) dans docs/PARCOURS_UTILISATEUR.md.
5. Lier chaque feature à une issue GitHub pour le suivi.
6. Prioriser les features selon impact clinique et effort technique (matrice effort/impact dans ROADMAP_PRODUIT.md).

### DOCUMENTS À PRODUIRE
- docs/ROADMAP_PRODUIT.md
- docs/SPECS/ (dossier avec un fichier par module)
- docs/METHODE_UI_MAPPING.md
- docs/PARCOURS_UTILISATEUR.md

### KPIs PRODUIT
- Nombre de features livrées par sprint (cible : 2 à 3 par sprint de 2 semaines)
- Taux de complétion du parcours praticien (onboarding -> première séance) : cible > 80 %
- Taux d'activation journal client : cible > 60 % des clients invités
- NPS praticiens (cible : > 40 à 6 mois)
- Temps moyen d'onboarding praticien (cible : < 15 minutes)

---

## POSTE 3 — TECH & DATA (CTO / Lead Dev / IA)

### ÉTAT ACTUEL
- Stack complète : FastAPI backend (10_backend_merlin_api), React/TS frontend (09_app_ivia_merlin), nginx, Docker, VPS OVH.
- Scripts de deploy multiples (deploy.sh, deploy_vps.sh, build_vps.sh, deploy_frontend_only.sh).
- CLAUDE.md dense (26 305 bytes) — bonne documentation technique pour agents IA.
- managed_agents/ — intégration agents IA amorcée.
- 11_PROMPTS/ — ingénierie prompts avancée.
- build_output.txt (116 KB) en racine — à nettoyer.
- Pas de tests automatisés visibles.
- Pas de CI/CD centralisé via GitHub Actions.
- check_routes.py en racine — à déplacer.

### GAPS
- Absence de tests (pytest backend, Vitest/Playwright frontend).
- CI/CD non centralisé (GitHub Actions absents ou incomplets).
- Scripts de deploy éparpillés — risque de confusion.
- build_output.txt et fichiers temporaires en racine.
- Pas de monitoring applicatif (uptime, erreurs, latence).
- Coûts transcription/IA non optimisés (Whisper via API externe probable).

### RECOMMANDATIONS
1. Créer .github/workflows/ci.yml (lint + tests backend + tests frontend à chaque push).
2. Créer .github/workflows/deploy.yml (deploy automatique sur tag ou merge main).
3. Ajouter une suite de tests pytest dans 10_backend_merlin_api/tests/.
4. Ajouter Vitest dans 09_app_ivia_merlin pour les composants critiques.
5. Nettoyer la racine : déplacer build_output.txt dans .gitignore, check_routes.py dans tools/.
6. Consolider les scripts de deploy en un seul scripts/deploy.sh avec options (backend/frontend/full).
7. Mettre en place un monitoring simple (UptimeRobot ou Sentry free tier).
8. Évaluer auto-hébergement Whisper sur VPS pour réduire coûts transcription de 60-80 %.
9. Documenter l'architecture technique dans docs/ARCHITECTURE_TECHNIQUE.md.
10. Créer une politique de gestion des données de santé dans docs/POLITIQUE_DONNEES_SANTE.md.

### DOCUMENTS À PRODUIRE
- docs/ARCHITECTURE_TECHNIQUE.md
- docs/POLITIQUE_DONNEES_SANTE.md
- docs/COUTS_INFRA_IA.md (suivi mensuel des coûts API, VPS, transcription)
- .github/workflows/ci.yml
- .github/workflows/deploy.yml
- scripts/deploy.sh (consolidé)

### KPIs TECH
- Uptime production (cible : > 99,5 %)
- Latence API médiane (cible : < 300 ms)
- Coût mensuel infra + IA (cible : < 150 CAD/mois en early stage)
- Couverture de tests (cible : > 60 % backend, > 40 % frontend)
- Nombre de bugs critiques en production (cible : 0 par mois)
- Délai moyen de déploiement (cible : < 10 minutes)

---

## POSTE 4 — CLINIQUE & CONTENUS (Clinical Lead / Méthodologie IVIA)

### ÉTAT ACTUEL
- 01_FONDEMENTS, 04_METHODES, 05_JOURNAUX, 05_PREUVES_SOURCES — base documentaire clinique présente.
- 02_NATIONS_QC — contexte culturel Québec / savoirs autochtones pris en compte.
- DAVID_CORPUS — corpus personnel intégré, force différenciante unique.
- 11_PROMPTS — traduction méthode en langage IA opérationnel.
- Pas de guide IVIA formalisé pour praticiens partenaires.
- Pas de guide client journal.
- Connexion méthode <-> app non documentée.

### GAPS
- Absence de guide praticien standalone (distribuable à un partenaire ou financeur).
- Absence de guide client journal (outil d'adoption).
- Protocole 50+10 non formalisé en document standalone.
- Preuves et sources (05_PREUVES_SOURCES) non encore reliées aux claims cliniques.

### RECOMMANDATIONS
1. Rédiger le Guide IVIA Praticiens dans docs/GUIDE_PRATICIENS_IVIA.md.
2. Rédiger le Guide Client Journal dans docs/GUIDE_CLIENT_JOURNAL.md.
3. Formaliser le Protocole 50+10 dans docs/PROTOCOLE_50_10.md.
4. Créer un document de validation des preuves cliniques dans docs/PREUVES_CLINIQUES_IVIA.md (liens vers 05_PREUVES_SOURCES).
5. Documenter les cas d'usage par type de praticien (psychologue, conseiller d'orientation, coach) dans docs/CAS_USAGE_PRATICIENS.md.
6. Créer une FAQ praticiens dans docs/FAQ_PRATICIENS.md.

### DOCUMENTS À PRODUIRE
- docs/GUIDE_PRATICIENS_IVIA.md
- docs/GUIDE_CLIENT_JOURNAL.md
- docs/PROTOCOLE_50_10.md
- docs/PREUVES_CLINIQUES_IVIA.md
- docs/CAS_USAGE_PRATICIENS.md
- docs/FAQ_PRATICIENS.md

### KPIs CLINIQUE
- Nombre de praticiens formés à la méthode IVIA (cible : 5 en beta, 20 à 6 mois)
- Taux d'adhérence au protocole 50+10 (cible : > 85 % des séances)
- Taux d'utilisation du journal par les clients (cible : > 3 entrées/semaine en phase active)
- Satisfaction praticiens sur la méthode (cible : > 4,2/5)
- Nombre de cas documentés avec outcomes mesurables

---

## POSTE 5 — GO-TO-MARKET (Marketing / Ventes / Partenariats)

### ÉTAT ACTUEL
- ivia_site_v2/ — site v2 en cours.
- Logos multiples (SVG, PNG, JPG) — identité visuelle présente.
- 12_JURIDIQUE_AFFAIRES — cadrage juridique amorcé.
- Pas de pitch deck dans le repo.
- Pas de landing page déployée orientée acquisition praticiens.
- Pas de CRM ou pipeline praticiens tracé.
- Pas de plan de contenu ni stratégie acquisition documentée.

### GAPS
- Absence totale de pipeline de vente/acquisition documenté.
- Pas de stratégie de contenu pour les réseaux (LinkedIn, Instagram, etc.).
- Pas de séquence d'onboarding email pour praticiens.
- Pas de page démo ou liste d'attente active.

### RECOMMANDATIONS
1. Déployer la landing page ivia_site_v2 avec appel à l'action praticiens (liste d'attente / demande de démo).
2. Créer le pitch deck dans docs/PITCH_DECK_IVIA_MERLIN.md.
3. Créer un pipeline praticiens dans docs/PIPELINE_PRATICIENS.md (liste, statut, source, date).
4. Définir une stratégie de contenu par réseau dans docs/STRATEGIE_CONTENU.md.
5. Créer un calendrier éditorial mensuel dans docs/CALENDRIER_EDITORIAL_YYYY_MM.md.
6. Rédiger une séquence d'emails d'onboarding praticiens (5 emails) dans docs/SEQUENCE_EMAIL_PRATICIENS.md.
7. Définir les canaux prioritaires : LinkedIn (praticiens), Instagram (clients), Newsletter (ordre professionnel).
8. Préparer un kit de présentation pour les ordres professionnels dans docs/KIT_ORDRES_PROFESSIONNELS.md.

### CONTENUS RÉSEAUX SOCIAUX — STRUCTURE RECOMMANDÉE

#### LinkedIn (audience : praticiens, recruteurs, investisseurs, partenaires institutionnels)
- Fréquence cible : 3 posts/semaine
- Types de contenu :
  - Éducatif : la méthode IVIA, le protocole 50+10, le journal guidé (comment ça marche)
  - Témoignages / cas d'usage : praticiens qui utilisent IVIA (avec permission)
  - Coulisses du développement : progression du produit, décisions techniques, roadmap
  - Positionnement thought leadership : santé mentale, IA éthique, mémoire clinique
  - Annonces : nouvelles features, lancements, partenariats
- Format : texte long (1200-1800 caractères) + 1 visuel simple (screenshot, stat, citation)

#### Instagram (audience : clients potentiels, public général, jeunes adultes)
- Fréquence cible : 4 posts/semaine (2 reels + 2 carrousels)
- Types de contenu :
  - Journal guidé : extraits de prompts, témoignages anonymisés, bénéfices du journaling
  - Santé mentale accessible : conseils pratiques, déstigmatisation
  - IVIA comme outil : comment ça marche pour toi en tant que client
  - Stories : rappels quotidiens, sondages, Q&A
- Format : carré 1080x1080, reels 9:16, texte court et accrocheur

#### Newsletter / Email (audience : praticiens inscrits, liste d'attente)
- Fréquence cible : 1 fois par semaine
- Types de contenu :
  - Mise à jour du produit (nouveautés, corrections)
  - Article de fond sur la méthode IVIA ou un aspect clinique
  - Invitation à tester une nouvelle feature
  - Ressources cliniques (liens, recherches, outils)

#### Contenu pour ordres professionnels (OCCOQ, OPQ, etc.)
- Un communiqué par trimestre
- Un kit de présentation de la méthode IVIA
- Une invitation à un webinaire de présentation

### DOCUMENTS À PRODUIRE
- docs/PITCH_DECK_IVIA_MERLIN.md
- docs/PIPELINE_PRATICIENS.md
- docs/STRATEGIE_CONTENU.md
- docs/CALENDRIER_EDITORIAL_2026_07.md (premier livrable)
- docs/SEQUENCE_EMAIL_PRATICIENS.md
- docs/KIT_ORDRES_PROFESSIONNELS.md

### KPIs GO-TO-MARKET
- Nombre de praticiens en liste d'attente (cible : 50 à 3 mois)
- Nombre de démos réalisées par mois (cible : 10/mois à partir du mois 2)
- Taux de conversion démo -> abonnement payant (cible : > 30 %)
- Abonnés LinkedIn (cible : +100/mois)
- Taux d'ouverture newsletter (cible : > 40 %)
- Coût d'acquisition client (CAC) praticien (cible : < 50 CAD)
- Nombre de mentions / partages organiques par mois

---

## POSTE 6 — FINANCE & OPÉRATIONS (CFO / Ops)

### ÉTAT ACTUEL
- 12_JURIDIQUE_AFFAIRES — base juridique et affaires.
- Analyses économiques produites en contexte (sessions Perplexity, non formalisées dans le repo).
- Aucun modèle financier dans le repo.
- Aucun tableau de KPIs SaaS tracé.
- Aucune documentation fiscale (TPS/TVQ, Stripe) intégrée.

### GAPS
- Modèle financier 5 ans absent.
- Projections de rentabilité absentes.
- Scénarios de croissance non documentés.
- Frais Stripe et TPS/TVQ non modélisés formellement.
- Seuil de rentabilité non calculé.

### RECOMMANDATIONS
1. Créer le modèle financier 5 ans dans docs/MODELE_FINANCIER_5ANS.md.
2. Documenter les scénarios de revenus (conservateur, modéré, optimiste) dans docs/SCENARIOS_REVENUS.md.
3. Créer un tableau des frais (Stripe, TPS/TVQ, infra, IA) dans docs/TABLEAU_FRAIS_OPERATIONS.md.
4. Documenter le seuil de rentabilité dans docs/SEUIL_RENTABILITE.md.
5. Créer un tableau de bord KPIs SaaS mensuel dans docs/KPI_SAAS_MENSUEL.md.
6. Documenter la structure fiscale (TPS/TVQ praticiens vs SaaS, Stripe) dans docs/STRUCTURE_FISCALE.md.
7. Créer un suivi des coûts infra et IA dans docs/COUTS_INFRA_IA.md.

### STRUCTURE FISCALE (rappel — voir sessions Perplexity 2026-06)
- Consultations coaching (David, non membre d'ordre) : TAXABLES TPS+TVQ.
- Séances cliniques de praticiens membres d'un ordre admissible : EXONÉRÉES TPS/TVQ.
- Abonnements SaaS IVIA/MERLIN (praticiens) : TAXABLES TPS+TVQ.
- Abonnements journal client : TAXABLES TPS+TVQ.
- Stripe : 2,9 % + 0,30 CAD par transaction domestique.

### MODÈLE DE REVENUS (base de projection)
- Abonnement praticien : 40 / 60 / 80 CAD/mois (hors taxes)
- Abonnement journal client premium : 10 CAD/mois (hors taxes)
- Net Stripe praticien 60 CAD : 57,96 CAD
- Net Stripe journal 10 CAD : 9,41 CAD
- Seuil de rentabilité estimé (infra + IA + opérations) : à calculer précisément
- Cible MRR mois 6 : 2 000 CAD
- Cible MRR mois 12 : 10 000 CAD
- Cible ARR fin année 2 : 150 000 CAD

### DOCUMENTS À PRODUIRE
- docs/MODELE_FINANCIER_5ANS.md
- docs/SCENARIOS_REVENUS.md
- docs/TABLEAU_FRAIS_OPERATIONS.md
- docs/SEUIL_RENTABILITE.md
- docs/KPI_SAAS_MENSUEL.md
- docs/STRUCTURE_FISCALE.md
- docs/COUTS_INFRA_IA.md

### KPIs FINANCE
- MRR (Monthly Recurring Revenue) — suivi mensuel
- ARR (Annual Recurring Revenue) — suivi trimestriel
- CAC (Coût d'acquisition client) — suivi mensuel
- LTV (Lifetime Value) praticien — suivi trimestriel
- Churn rate mensuel (cible : < 5 %)
- Marge brute après Stripe et infra (cible : > 70 %)
- Cash runway (mois restants avant besoin de financement externe)
- Ratio LTV/CAC (cible : > 3)

---

## PLAN D'IMPLÉMENTATION PAR PRIORITÉ

### PHASE 1 — FONDATIONS (semaines 1-2)
Priorité ROUGE — débloque financement et traction
1. README.md investisseur (Direction)
2. docs/MODELE_FINANCIER_5ANS.md (Finance)
3. docs/TABLEAU_FRAIS_OPERATIONS.md (Finance)
4. docs/PIPELINE_PRATICIENS.md (Go-to-market)
5. docs/GUIDE_PRATICIENS_IVIA.md (Clinique)

### PHASE 2 — STRUCTURE (semaines 3-4)
Priorité ORANGE — solidifie la base opérationnelle
6. docs/ROADMAP_PRODUIT.md (Produit)
7. docs/STRATEGIE_CONTENU.md (Go-to-market)
8. docs/ARCHITECTURE_TECHNIQUE.md (Tech)
9. docs/PROTOCOLE_50_10.md (Clinique)
10. docs/PLAN_AFFAIRES_IVIA_MERLIN.md (Direction)

### PHASE 3 — OPTIMISATION (semaines 5-8)
Priorité JAUNE — maximise la performance de chaque poste
11. CI/CD GitHub Actions (Tech)
12. Tests automatisés backend/frontend (Tech)
13. docs/CALENDRIER_EDITORIAL_2026_07.md (Go-to-market)
14. docs/SEQUENCE_EMAIL_PRATICIENS.md (Go-to-market)
15. docs/KPI_SAAS_MENSUEL.md (Finance)
16. docs/PARCOURS_UTILISATEUR.md (Produit)
17. Cleanup racine repo (Tech)

### PHASE 4 — PRODUCTION DE CONTENU (continu à partir du mois 2)
18. Calendrier éditorial mensuel (Go-to-market)
19. LinkedIn : 3 posts/semaine
20. Instagram : 4 posts/semaine
21. Newsletter : 1 envoi/semaine
22. Webinaire praticiens : 1 par mois
23. Mise à jour KPIs : 1 fois par mois (tous les pôles)

---

## NOTES FINALES

Ce document est la mémoire institutionnelle des recommandations au 2026-06-25.
Il doit être mis à jour à chaque sprint ou session de travail majeure.
Chaque recommandation mise en oeuvre doit être cochée avec la date de complétion.
Version suivante prévue : après livraison de la Phase 1 (semaines 1-2).

---
*Généré par Perplexity AI — Session David Faraj / Fa9d / IVIA-MERLIN — 2026-06-25*

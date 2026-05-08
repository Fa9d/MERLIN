# MERLIN — Plan d'affaires de financement V1

**Date** : 8 mai 2026
**Statut** : DRAFT 9.1.1 — corrections fond user + pricing par tranche durée + trajectoire technologique + roadmap
**Auteur** : David Phaneuf (fondateur) + Perplexity Computer
**Destinataires cibles** : PME MTL, Investissement Québec, Desjardins Capital, MEI, BDC, fondations, anges investisseurs québécois
**Devise** : CAD

---

## NOTE DE LECTURE (à supprimer en V2)

Ce document consolide 10 documents de gouvernance déjà produits entre 20 et 27 avril 2026 :

- `IVIA_DOCUMENT_DIRECTEUR_v1.0.md` (vision, 7 principes)
- `MERLIN_GOUV_CANON_OFFRE_PRODUIT_ADMIN_PRATICIEN_CLIENT_V1.md` (offre stable)
- `MERLIN_GOUV_MODELE_ECO_PRATICIENS_APPLICATION_v1.0.md` (doctrine économique)
- `MERLIN_GOUV_SIMULATION_ECO_3_PROFILS_PRATICIENS_V1.md` (V1 — frais dégressifs)
- `MERLIN_GOUV_SIMULATION_ECO_COUTS_REELS_V2.md` (V2 — coûts fournisseurs réels)
- `MERLIN_GOUV_OFFRE_PRATICIENS_GRILLE_COMMERCIALE_V1.md` (Essentiel/Standard/Premium)
- `MERLIN_GOUV_TABLEAU_PRIX_COUTANT_MARGE_PAR_SEANCE_V1.md`
- `MERLIN_GOUV_MODELE_COUTS_PRODUCTION_DOCUMENTAIRE_TOKENS_V1.md`
- `MERLIN_GOUV_MODELE_ECO_FRAIS_VOLUME_COUTS_SEUILS_v1.0.md`
- `MERLIN_GOUV_PROMESSE_CLIENT_ULTRA_COURTE_IVIA_V1.md`

**Trois arbitrages tranchés en 9.1 (8 mai 2026)** :

1. ✅ **MERLIN collecte le paiement client via Stripe** (UX unifiée). MERLIN absorbe le coût 2,91 $/séance.
2. ✅ **Architecture commerciale hybride 3×3** : 3 plans (Essentiel / Standard / Premium) × 3 paliers de volume (petit / régulier / gros), présentés commercialement comme « 3 plans avec tarif dégressif au volume actif ».
3. ✅ **Pilote nommé** : Mylène + Émilie comme praticiennes du pilote 31 mai 2026, David comme fondateur. Section Pilote dédiée.

---

## Section A — L'entreprise

### A.1 Identité

**MERLIN** est la plateforme technologique exploitée par IVIA (marque commerciale), une entreprise québécoise en phase pilote (lancement officiel : 31 mai 2026).

- **Vision** : *Au sein de l'être — En actes.*
- **Marque client** : IVIA
- **Marque technologique** : MERLIN
- **Forme juridique** : *à confirmer en section A.6 (OBNL, SAS, autre)*
- **Siège** : Montréal, Québec
- **Site** : `ivia.quebec`

### A.2 Positionnement

IVIA est **la référence en accompagnement vers l'autonomie émotionnelle, à distance**.

**Ce qu'IVIA EST** :
- Un espace d'écoute éthique outillé technologiquement
- Un cadre de pratique pour praticiens qualifiés
- Une plateforme audio-only de séances + production documentaire structurée

**Ce qu'IVIA N'EST PAS** :
- Pas un service de santé mentale clinique
- Pas du coaching de performance
- Pas du bien-être commercial
- Pas un outil de diagnostic
- Pas un substitut à un professionnel réglementé

### A.3 Les 7 principes directeurs

1. **Le vivant d'abord** — besoins réels avant constructions sociales
2. **L'équilibre comme pratique** — adaptation constante vers l'équilibre
3. **Les lois de l'échange** — tout échange a un coût, une valeur, une réciprocité
4. **L'autonomie émotionnelle comme horizon** — la personne s'affranchit d'IVIA
5. **La responsabilité comme dignité** — capacité d'agir reconnue chez tous
6. **La réalisation maximale de chaque être** — pas de comparaison, pas de norme
7. **La fréquence comme réalité vivante** — son, rythme, corps, nature

### A.4 Différenciation sur le marché québécois

Le marché québécois compte de nombreux outils de prise de rendez-vous (Acuity, GOrendezvous, Mytaverne) et plateformes de téléconsultation génériques. MERLIN se distingue par :

| Axe | Concurrents généralistes | MERLIN |
|---|---|---|
| Coeur de valeur | Logistique (RDV + paiement) | Trace + synthèse + continuité |
| Format | Visio + chat | Audio-only (positionnement fréquences) |
| Cadre | Neutre | Doctrine prudente + formation obligatoire |
| Documentation | Notes libres | Production documentaire structurée IA |
| Public visé | Tout praticien | Praticiens d'écoute / accompagnement émotionnel |

### A.5 État d'avancement (au 8 mai 2026)

- **Infrastructure de production en ligne** : `ivia.quebec`, `api.ivia.quebec`, `status.ivia.quebec`, `logs.ivia.quebec`
- **Stack technique fixée** : 24 outils décidés (analyse stack v1.1)
- **Gouvernance documentaire** : ~80 documents stratégiques produits, indexés
- **Pilote 2 praticiennes** : Mylène + Émilie identifiées, démarrage 31 mai 2026
- **Runbook déploiement v1.0** : opérations reproductibles documentées
- **Conformité** : politiques consentement, mineurs, transcription gouvernée, mémoire évolutive rédigées

### A.6 Structure juridique [⚠️ À COMPLÉTER 9.2]

> Notes des documents existants (`MERLIN_OBNL_MISSION_V1.md`, `MERLIN_STRUCTURE_JURIDIQUE_V1.md`) — à synchroniser et arbitrer.
> Question ouverte : modèle hybride OBNL (mission sociale) + société commerciale (exploitation MERLIN) ?

---

## Section B — L'offre

### B.1 Trois rôles canoniques

| Rôle | Responsabilité principale |
|---|---|
| **Admin** | Gouverne offres, profils, options d'analyse, consentements, modèles documentaires |
| **Praticien** | Conduit la relation de service (séance, validation documents, orientation) — selon services choisis |
| **Client** | Bénéficie du service (RDV, consentements, séance, documents autorisés) — selon service choisi |

### B.2 Trois offres principales (Canon V1)

| Offre | Inclus |
|---|---|
| **Rendez-vous d'écoute** | RDV + salle audio + note interne praticien + synthèse courte |
| **Écoute avec compte rendu** | Tout RDV d'écoute + transcription + analyse structurée + compte rendu praticien + version client validable |
| **Parcours de soutien** | Tout Écoute avec compte rendu + historique multi-séances + documents de mise en pratique + plan de continuité |

### B.3 Trois profils praticiens × trois profils clients

**Profils praticiens** : praticien écoute / praticien suivi / praticien supervision renforcée
**Profils clients** : client écoute simple / client suivi documenté / client diffusion selon offre

Ces profils définissent les droits d'accès aux offres, options d'analyse, types de documents diffusables.

### B.4 Options configurables par séance

- **Médias** : enregistrement audio, transcription, conservation, durée de rétention
- **Analyse** : structurée / émotionnelle / contextuelle / pistes / orientation
- **Documents** : note interne / compte rendu / document client / mise en pratique
- **Suivi actif** : selon recommandation, exercices, pratiques, suggestions
- **Validation** : validation praticien obligatoire, supervision obligatoire, diffusion immédiate interdite
- **Relationnel** : confirmation RDV, relances, rappels, replanification

### B.5 Règles fermes (cadre légal Québec)

- Aucun diagnostic automatique
- Aucune promesse de traitement
- Aucune substitution à un membre d'un ordre professionnel
- Aucune recommandation présentée comme conclusion clinique définitive
- Aucune diffusion client sans respect des règles configurées
- Formation doctrine minimale obligatoire pour tout praticien sous marque MERLIN

### B.6 Promesse client (cf. PROMESSE_ULTRA_COURTE)

[⚠️ À RAPATRIER depuis MERLIN_GOUV_PROMESSE_CLIENT_ULTRA_COURTE_IVIA_V1.md en 9.2]

### B.7 Trajectoire technologique

La stack IA de MERLIN évolue en trois phases qui sécurisent à la fois la qualité de service et la marge à long terme.

**Phase 1 — Stack commerciale (M1 → M12)**
Utilisation de modèles commerciaux (GPT-4 class, Claude, Deepgram) facturés à l'API. Coûts variables présentés en C.5 (scénario prudent retenu pour le BP).

**Phase 2 — Modèles évolutifs (M12 → M24)**
Le coût des modèles équivalents baisse historiquement de ~50 %/an à qualité constante. À budget identique, MERLIN bénéficie soit d'une marge en hausse mécanique, soit d'une qualité en hausse à coût constant. La grille tarifaire reste stable côté praticien — l'élasticité prix profite à MERLIN.

**Phase 3 — Modèle propriétaire IVIA (M24+)**
Fine-tuning d'un modèle open-source (Llama, Mistral, Qwen) sur le corpus doctrinaire IVIA (7 principes, cadre prudent, vocabulaire de présence) hébergé sur infra propre. Coût marginal proche de zéro, marge → 85–95 %, modèle non-réplicable par concurrents généralistes. Voir Roadmap (Section R) pour planification.

**Actif stratégique : dataset propriétaire**
Les séances analysées (avec consentement explicite) constituent un corpus unique au monde sur l'accompagnement par fréquences. Ce dataset alimente la Phase 3 et constitue un actif valorisable de l'entreprise (cf. Section F — Besoin de financement).

---

## Section C — Modèle économique [PARTIELLEMENT REMPLI — à finaliser 9.1 suite]

### C.1 Doctrine de monétisation

**MERLIN monétise** : l'outil, l'infrastructure et le service plateforme.

**MERLIN ne monétise PAS** : l'acte d'orientation, l'intérêt du client, la commission cachée sur soin.

### C.2 Trois couches économiques

- **Couche 1 — Frais plateforme** : abonnement praticien + frais par séance traitée (dégressifs au volume)
- **Couche 2 — Options IA à l'usage** : transcription/minute, reporting/séance transcrite
- **Couche 3 — Premium historique** : analyse longitudinale, rapports historiques

### C.3 Décision — MERLIN collecte le paiement client

Décision prise le 8 mai 2026 : **MERLIN encaisse le prix de la séance via Stripe Connect** et reverse au praticien après prélèvement de ses propres frais.

Justification :
- UX unifiée client (un seul paiement)
- Praticien sans charge fiscale Stripe
- Contrôle total du parcours et de la conformité
- Donne à MERLIN une visibilité complète sur les volumes

Coût accepté : **2,91 $ CAD/séance** (Stripe Canada : 2,9 % + 0,30 $ sur 90 $ moyen). Ce coût est intégré dans tous les calculs ci-dessous.

### C.4 Décision — Architecture commerciale hybride 3×3

Décision prise le 8 mai 2026 : **3 plans × 3 paliers de volume = 9 prix par séance**, présentés commercialement comme « 3 plans avec dégressivité automatique selon volume actif ».

**3 plans** :
- **Essentiel** — gestion des séances, rappels, note synthèse simple
- **Standard** — Essentiel + transcription + analyse structurée + compte rendu praticien
- **Premium** — Standard + analyse historique multi-séances + plan de continuité documenté

**3 paliers de volume** (recalculés mensuellement selon séances facturées) :
- **Petit volume** : 0–30 séances/mois
- **Volume régulier** : 31–80 séances/mois
- **Gros volume** : 81–200 séances/mois

### C.5 Coûts variables réels par séance (séance type 70 min, 90 $ CAD)

| Bloc de coût | Scénario bas | Scénario prudent (retenu BP) |
|---|---:|---:|
| Paiement Stripe (MERLIN collecte) | 2,91 | 2,91 |
| Transcription (Essentiel : 0 / Standard+Premium : Deepgram Growth) | 0,24 | 0,63 |
| IA analyse + rapport (GPT-4 class) | 0,01 | 0,01 |
| IA analyse historique (Premium uniquement) | 0,30 | 0,50 |
| Stockage audio 12 mois | 0,01 | 0,01 |

Déclinaison par plan (scénario prudent retenu) :

| Plan | Coût variable / séance |
|---|---:|
| Essentiel | 2,92 $ |
| Standard | 3,56 $ |
| Premium | 4,06 $ |

#### C.5.bis — Pricing par tranche durée (services analytiques activables)

Décision V1.1 : tous les services analytiques sont **facturés par tranche de durée audio** (proxy fiable du volume tokens consommés). Prix ronds, paliers transparents praticien, marge protégée même en cas de hausse temporaire des coûts modèles.

| Service activable / séance | 0–45 min | 46–90 min | 91+ min |
|---|---:|---:|---:|
| Résumé de séance | 1 $ | 2 $ | 3 $ |
| Structuration de séance | 1 $ | 2 $ | 3 $ |
| Analyse client | 2 $ | 3 $ | 5 $ |
| Analyse praticien | 2 $ | 3 $ | 5 $ |
| Suivi actif (recommandations, exercices, pratiques, suggestions) | 3 $ | 5 $ | 8 $ |

Logique d'inclusion par plan :
- **Essentiel** : aucun service analytique inclus — activables à la carte par séance
- **Standard** : Résumé + Structuration inclus de base (palier durée appliqué seulement sur 91+ min) ; autres services à la carte
- **Premium** : Résumé + Structuration + Analyse client + Analyse praticien inclus de base ; Suivi actif à la carte avec **tarif dégressif** (Premium : −33 % vs grille publique)

**Marge unitaire moyenne (séance 46–90 min, retenue scénario prudent BP)** :
- Suivi actif : prix 5 $ — coût IA estimé 1,20 $ — **marge brute 3,80 $/activation (76 %)**
- Analyse client/praticien : prix 3 $ — coût IA estimé 0,80 $ — **marge brute 2,20 $/activation (73 %)**
- Résumé/Structuration : prix 2 $ — coût IA estimé 0,40 $ — **marge brute 1,60 $/activation (80 %)**

### C.6 Grille tarifaire consolidée — décision V1

#### Tarif par séance (frais plateforme MERLIN, hors prix séance client)

| Plan | Petit (0–30) | Régulier (31–80) | Gros (81–200) |
|---|---:|---:|---:|
| **Essentiel** | 4,90 $ | 4,40 $ | 3,90 $ |
| **Standard** | 7,90 $ | 7,40 $ | 6,90 $ |
| **Premium** | 12,90 $ | 11,90 $ | 10,90 $ |

#### Abonnement mensuel praticien (selon palier détecté à m–1)

| Palier | Abonnement |
|---|---:|
| Petit | 27,99 $ |
| Régulier | 47,99 $ |
| Gros | 84,99 $ |

### C.7 Marge brute MERLIN par profil (matrice 3×3)

Profils volumes utilisés : Petit = 20 séances/mois, Régulier = 60, Gros = 150.

| Plan | Palier | Revenu MERLIN/mois | Coût variable/mois | **Marge brute** | **Taux marge** |
|---|---|---:|---:|---:|---:|
| Essentiel | Petit | 125,99 $ | 58,44 $ | **67,55 $** | **53,6 %** |
| Essentiel | Régulier | 311,99 $ | 175,32 $ | **136,67 $** | **43,8 %** |
| Essentiel | Gros | 669,99 $ | 438,30 $ | **231,69 $** | **34,6 %** |
| Standard | Petit | 185,99 $ | 71,20 $ | **114,79 $** | **61,7 %** |
| Standard | Régulier | 491,99 $ | 213,60 $ | **278,39 $** | **56,6 %** |
| Standard | Gros | 1 119,99 $ | 534,00 $ | **585,99 $** | **52,3 %** |
| Premium | Petit | 285,99 $ | 81,20 $ | **204,79 $** | **71,6 %** |
| Premium | Régulier | 761,99 $ | 243,60 $ | **518,39 $** | **68,0 %** |
| Premium | Gros | 1 719,99 $ | 609,00 $ | **1 110,99 $** | **64,6 %** |

**Lecture stratégique** :
- Le plan **Essentiel à gros volume** est le plus à risque (34,6 % de marge) — c'est volontaire : il doit rester compétitif vs Acuity/GOrendezvous.
- Le **vrai cœur de marge MERLIN** est le plan **Standard** (transcription + analyse) — comparable aux outils SaaS spécialisés mais avec un cadre prudent unique au Québec.
- Le plan **Premium** est le différenciateur stratégique (64–72 % de marge) — c'est ce qui justifie la valeur de MERLIN auprès des praticiens établis.

### C.8 Hypothèse de répartition des plans (à valider en pilote)

Hypothèse de travail pour le P&L 12 mois (E.2) :

| Plan | % praticiens M1–M3 | % praticiens M6 | % praticiens M12 |
|---|---:|---:|---:|
| Essentiel | 50 % | 35 % | 25 % |
| Standard | 50 % | 50 % | 55 % |
| Premium | 0 % | 15 % | 20 % |

Logique : démarrage en Essentiel/Standard, montée en gamme progressive après expérience plateforme.

### C.9 Gouvernance tarifaire — paramétrage admin dynamique

Principe d'architecture critique : **tous les paramètres tarifaires sont configurables depuis l'interface admin MERLIN sans redéploiement applicatif**.

Paramètres concernés :
- Prix par séance par plan × palier (matrice 3×3)
- Abonnements mensuels par palier
- Prix par tranche durée pour chaque service analytique (matrice C.5.bis)
- Inclusion / exclusion d'un service dans un plan
- Bornes des paliers volume (par défaut 30 / 80 / 200)
- Seuil dégressif Premium sur Suivi actif

Justifications :
- **Business** : ajustement en J+1 si une tranche écrase la marge ou si un palier est mal calibré
- **BP** : agilité tarifaire = capacité à pivoter sans coût technique = signal de robustesse pour investisseur
- **Technique** : table `pricing_config` versionnée en base, audit trail complet, jamais de prix codés en dur

Ticket backlog correspondant : **BACK-011 Admin tarification dynamique** (priorisation V10).

---

## Section P — Pilote 31 mai 2026

Le pilote MERLIN démarre le **31 mai 2026** avec 2 praticiennes identifiées et le fondateur.

### P.1 Mylène — Praticienne pilote

**Profil de présence** :
*Empathe et amoureuse du bonheur. Mylène sait écouter et rebondir. Un soleil émane de sa voix. Réconfortante et aimante, Mylène nous permet de croire.*

**Rôle pilote** : praticienne écoute, plan recommandé Standard, démarrage palier Petit volume (M1–M3).

### P.2 Émilie — Praticienne pilote

**Profil de présence** :
*En terme d'écoute active il est difficile de faire mieux. Un électrochoc ou une présence tendre et compréhensive, Émilie sait.*

**Rôle pilote** : praticienne écoute / suivi, plan recommandé Standard, démarrage palier Petit volume (M1–M3).

### P.3 David — Fondateur

**Profil de présence** :
*Fondateur de l'expérience, sa voix ni grave ni douce berce ou transporte. Qu'il s'agisse d'écoute ou de compréhension, David entend, comprend, analyse et guide.*

**Rôle pilote** : fondateur, gouvernance, supervision méthode, écoute pour cas-tests internes (non rémunérée).

### P.4 Objectifs mesurables du pilote (M1–M3)

| Indicateur | Cible M1 | Cible M3 |
|---|---:|---:|
| Praticiennes actives | 2 | 2 |
| Séances réalisées / mois | ≥ 10 | ≥ 30 |
| Taux satisfaction client (qualitatif) | recueil systématique | ≥ 4/5 |
| Documents diffusés validés | 100 % validés | 100 % validés |
| Incidents techniques majeurs | tolérance 1 | 0 |
| Conformité consentements | 100 % | 100 % |

### P.5 Décision Go / No-Go expansion (fin M3 = 31 août 2026)

Critères Go :
- Stabilité technique avérée (uptime > 99 %)
- Au moins 1 praticienne au palier Régulier OU 2 praticiennes au palier Petit confirmées au M3
- Coûts variables réels alignés avec hypothèses BP (±15 %)
- Aucun incident de conformité majeur

Si Go : ouverture cohorte 2 (5–8 praticiennes recrutées) en M4 (septembre 2026).

---

## Section R — Roadmap technologique post-pilote

### R.1 V10 (M4–M6 — septembre à novembre 2026)

- **BACK-011** Admin tarification dynamique (cf. C.9) — *prérequis cohorte 2*
- **OPS-006** Umami Analytics — observabilité usage
- **OPS-007** Décision Infisical — secrets centralisés
- **OPS-014** Cron Let's Encrypt — automatisation renouvellement TLS
- Migration progressive Phase 1 → Phase 2 (modèles évolutifs, cf. B.7) sur services analytiques non-critiques

### R.2 V11 (M7–M9 — décembre 2026 à février 2027)

- Construction pipeline d'inférences propriétaires sur dataset MERLIN consenti
- Premiers signaux longitudinaux client (évolution sur N séances)
- Features Premium différenciantes (recommandations contextuelles enrichies)
- Préparation socle Phase 3 (collecte gouvernée corpus IVIA)

### R.3 V12 (M10–M12 — mars à mai 2027)

- Expérimentation fine-tuning modèle open-source sur corpus IVIA
- Évaluation qualité comparative vs Phase 1
- Décision Go / No-Go bascule production Phase 3
- Si Go : Phase 3 production en V13 (post-anniversaire 1 an)

### R.4 Indicateurs de succès roadmap

| Indicateur | Cible V10 | Cible V11 | Cible V12 |
|---|---|---|---|
| Coût moyen IA / séance | −20 % vs M1 | −35 % vs M1 | −50 % vs M1 |
| Marge brute moyenne MERLIN | +5 pts vs M1 | +10 pts | +15 pts |
| Volume données consenties | 100 séances | 500 séances | 1 500 séances |
| Modèles propriétaires en test | 0 | 1 | 2–3 |

---

## Section D — Charges structurelles entreprise [À CAPTURER EN 9.2]

Liste à compléter par interview ciblée — pré-cadrage :

### D.1 Frais R&D actuels (phase pré-revenu)

- [ ] Abonnements IA développement (Claude Code, Perplexity, Copilot, ChatGPT)
- [ ] Licences outils dev (Cursor, v0.app, GitHub Copilot)
- [ ] Hébergement VPS OVH (2 VPS)
- [ ] Stockage objet OVH
- [ ] Domaines OVH
- [ ] Certificats Let's Encrypt (gratuit, renouvellement à automatiser)
- [ ] Outils support (Sentry/GlitchTip prévu, Umami prévu, Uptime Kuma déjà en place)

### D.2 Coûts récurrents par séance (variables — déjà section C.5)

### D.3 Charges entreprise structurelles

- [ ] Téléphone (mobile fondateur dédié entreprise)
- [ ] Internet (résidentiel home-office, part professionnelle)
- [ ] Bureau / espace travail (home-office, part proportionnelle)
- [ ] Matériel informatique (ordinateur portable, écrans, périphériques) → **amortissement**
- [ ] Équipement audio (micro qualité pro, casque)
- [ ] Fournitures bureau (papier, impression, timbres)
- [ ] Marque & marketing (logo, charte, site, contenus, publicité ciblée)
- [ ] Comptable (préparation états financiers, déclarations TPS/TVQ, T2)
- [ ] Légal (rédaction contrats praticiens, CGU, politique vie privée révisée par avocat)
- [ ] Assurance responsabilité professionnelle (entreprise + praticiens sous marque)
- [ ] Inscriptions / immatriculations (REQ, NEQ, TPS/TVQ)
- [ ] Banque (frais compte affaires, transferts, change USD)
- [ ] **Rémunération fondateur** (David — temps plein équivalent)
- [ ] Formation continue / veille (livres, conférences, certifications)
- [ ] Imprévus & contingences (~5-10 % du total)

### D.4 Phase de financement (CAPEX initial)

- [ ] Investissement matériel informatique (si renouvellement nécessaire)
- [ ] Développement custom hors stack standard (si applicable)
- [ ] Marketing de lancement (campagne pilote → public)
- [ ] Réserve trésorerie (6 mois de charges fixes minimum)

---

## Section E — Scénarios financiers [À CONSTRUIRE EN 9.3]

### E.1 Hypothèses d'acquisition praticiens

| Mois | Praticiens actifs | Source acquisition |
|---|---:|---|
| M1 (juin 2026) | 2 | Pilote Mylène + Émilie |
| M3 | ? | À définir 9.3 |
| M6 | ? | À définir 9.3 |
| M12 | ? | À définir 9.3 |

### E.2 P&L 12 mois consolidé

*À construire en Excel à partir de C.6 (grille tarifaire) + D (charges).*

### E.3 Seuil de rentabilité

*À calculer en E.2.*

### E.4 Scénarios bas / médian / haut

*À modéliser après remplissage E.1 et E.2.*

---

## Section F — Besoin de financement [À RÉDIGER EN 9.3]

- F.1 Montant demandé
- F.2 Affectation des fonds
- F.3 Calendrier de décaissement
- F.4 Retour attendu (revenu, impact social, autonomie financière)
- F.5 Mode de financement préféré (subvention, prêt, capital, mixte)

---

## Annexes

- **Annexe 1** : Document Directeur IVIA (référence intégrale)
- **Annexe 2** : Canon Offre Produit MERLIN (référence intégrale)
- **Annexe 3** : Simulation Coûts Réels V2 (référence chiffrée)
- **Annexe 4** : Grille Commerciale V1 (référence chiffrée)

---

## Devise

*Au sein de l'être — En actes.*

---

## Statut de complétude

| Section | État | Suite |
|---|---|---|
| A — L'entreprise | 95 % | A.6 juridique à valider en 9.2 |
| B — L'offre | 100 % | B.6 promesse à rapatrier en 9.2, B.7 trajectoire techno ajoutée |
| **C — Modèle éco** | **100 %** | **Grille 3×3 + pricing tranche durée + gouvernance tarifaire C.9** |
| **P — Pilote** | **100 %** | **Mylène + Émilie + David documentés** |
| **R — Roadmap techno** | **100 %** | **V10→V12 définis, indicateurs cibles** |
| D — Charges entreprise | 10 % (pré-cadrage) | Interview 9.2 |
| E — Scénarios P&L 12 mois | 0 % | 9.3 (Excel) |
| F — Besoin financement | 0 % | 9.3 |

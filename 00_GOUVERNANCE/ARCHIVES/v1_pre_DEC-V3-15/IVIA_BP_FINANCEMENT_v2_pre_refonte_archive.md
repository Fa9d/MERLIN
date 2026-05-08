# MERLIN / IVIA — Plan d'affaires de financement V2
## Document de référence stratégique et financier

**Date** : Mai 2026
**Statut** : DRAFT V2.0 — Version intégrée Vague 1
**Auteur** : David Phaneuf (fondateur) + Perplexity Computer
**Remplace** : BP_FINANCEMENT_V1.md (DRAFT 9.1.1 du 8 mai 2026)
**Destinataires cibles** : PME MTL, Investissement Québec, Desjardins Capital, MEI, fondations québécoises, anges investisseurs Québec
**Devise** : CAD

---

## NOTE DE LECTURE

Ce document constitue la V2.0 du plan d'affaires de financement IVIA / MERLIN. Il intègre les décisions structurantes arrêtées lors de la Vague 1 de production documentaire (mai 2026) :

**Décisions intégrées dans cette version** :
1. Structure juridique : OBNL hybride (IVIA) contrôlant société commerciale (MERLIN inc.) — remplace le placeholder "à confirmer en section A.6"
2. Besoin de financement : 2,2 M$ sur 36 mois (variante sécurisée retenue)
3. Strate 4 retardée à M30 (pas M28) — maturité dataset synthétique requise
4. Mix financement : 70 % subvention + 30 % capital patient pour M1-M12
5. Rémunération fondateur : 75-90 K$/an (explicite)
6. Architecture multi-strates 4 niveaux documentée
7. Pipeline de transformation gouvernée des données documenté (Charte v1.0)

**Documents de référence obligatoires** :
- `CHARTE_DOCTRINAIRE_IVIA.md` — Fondation doctrinaire (V1.0)
- `STRUCTURE_JURIDIQUE_RECOMMANDEE.md` — Structure légale (V1.0)
- `CHARTE_TRANSFORMATION_GOUVERNEE_DONNEES.md` — Pipeline données (V1.0)
- `PLAN_INTEGRATION_IVIA_36MOIS.md` — Roadmap 6 paliers
- `PLAN_FINANCEMENT_DETAILLE.md` — Détail sources et calendrier

---

## SECTION A — L'ENTREPRISE

### A.1 Identité

MERLIN est la plateforme technologique exploitée par IVIA, une entreprise québécoise en phase pilote (lancement officiel : 31 mai 2026).

| Élément | Valeur |
|---|---|
| Vision | Au sein de l'être — En actes. |
| Marque client | IVIA |
| Marque technologique | MERLIN |
| Forme juridique | Hybride : IVIA (OBNL) + MERLIN inc. (SPA) — voir A.6 |
| Siège | Montréal, Québec |
| Site | ivia.quebec |
| Fondateur | David Phaneuf |
| Pilote | 31 mai 2026 |

### A.2 Positionnement

IVIA est **la référence en accompagnement vers l'autonomie émotionnelle, à distance**.

**Ce qu'IVIA EST** :
- Un espace d'écoute éthique outillé technologiquement
- Un cadre de pratique pour praticiens qualifiés
- Une plateforme audio-only de séances + production documentaire structurée
- Une infrastructure de transformation gouvernée des données de pratique

**Ce qu'IVIA N'EST PAS** :
- Pas un service de santé mentale clinique
- Pas du coaching de performance
- Pas du bien-être commercial
- Pas un outil de diagnostic
- Pas un substitut à un professionnel réglementé

### A.3 Les 7 principes directeurs (synthèse)

Référence complète : `CHARTE_DOCTRINAIRE_IVIA.md`, Partie I

1. Le vivant d'abord — besoins réels avant constructions sociales
2. L'équilibre comme pratique — adaptation constante vers l'équilibre
3. Les lois de l'échange — tout échange a un coût, une valeur, une réciprocité
4. L'autonomie émotionnelle comme horizon — la personne s'affranchit d'IVIA
5. La responsabilité comme dignité — capacité d'agir reconnue chez tous
6. La réalisation maximale de chaque être — pas de comparaison, pas de norme
7. La fréquence comme réalité vivante — son, rythme, corps, nature

### A.4 Différenciation sur le marché québécois

| Axe | Concurrents généralistes | IVIA / MERLIN |
|---|---|---|
| Coeur de valeur | Logistique (RDV + paiement) | Trace + synthèse + continuité + moat données |
| Format | Visio + chat | Audio-only (positionnement fréquences — Principe 7) |
| Cadre | Neutre | Doctrine 7 principes + formation obligatoire |
| Documentation | Notes libres | Production documentaire structurée IA |
| Données | Exploitées ou ignorées | Pipeline transformation gouvernée (données jamais vendues) |
| Public visé | Tout praticien | Praticiens d'écoute / accompagnement émotionnel (Strate 1 → 4) |

### A.5 État d'avancement (mai 2026)

- Infrastructure de production en ligne : ivia.quebec, api.ivia.quebec, status.ivia.quebec
- Stack technique fixée : 24 outils décidés (analyse stack v1.1)
- Gouvernance documentaire : ~80 documents stratégiques produits (+ 8 documents Vague 1)
- Pilote 2 praticiennes : Mylène + Émilie identifiées, démarrage 31 mai 2026
- Runbook déploiement v1.0 opérationnel
- Conformité : politiques consentement, mineurs, transcription gouvernée rédigées

### A.6 Structure juridique — Hybride OBNL + SPA

**Décision arrêtée** : Structure hybride OBNL contrôlant SPA.

**IVIA (OBNL)** : Mission sociale, gouvernance doctrinaire, détient actions spéciales de MERLIN inc. avec droits de veto sur matières doctrinaires. Accès aux subventions philanthropiques et gouvernementales OBNL.

**MERLIN inc. (SPA)** : Exploitation commerciale, développement technologique, levée de capital-actions. Rémunération fondateur. Accès aux crédits RS&DE, CTRI, capital privé.

Justification détaillée : `STRUCTURE_JURIDIQUE_RECOMMANDEE.md`

Budget de constitution : 15 000 $ (inclus dans Palier 1)
Calendrier : 6-8 semaines (juin-juillet 2026)

### A.7 Stratégie multi-strates (vue d'ensemble)

IVIA déploie son offre en 4 strates progressives sur 36 mois :

| Strate | Nom commercial | Public | Lancement | Palier |
|---|---|---|---|---|
| S1 | IVIA Cœur | Praticiens d'écoute (hors ordres) | 31 mai 2026 | Palier 1 |
| S2 | IVIA Professionnels | Membres d'ordres (psychologues, psychothérapeutes) | M13 | Palier 4 |
| S3 | IVIA Soins | Praticiens corporels et alternatifs | M19 | Palier 5 |
| S4 | IVIA Réseau | Annuaire référencement éthique | M30 | Palier 6 |

**Note d'attention — Strate 4 à M30**
> La Strate 4 est retardée à M30 (septembre 2028) plutôt que M28 pour garantir la maturité du dataset synthétique. L'annuaire IVIA Réseau doit pouvoir appuyer ses recommandations de référencement sur une connaissance réelle des patterns de pratique — ce qui requiert un corpus synthétique de 3 000+ cas. Ce seuil est atteint au plus tôt en M28-M30.

---

## SECTION B — L'OFFRE

### B.1 Trois rôles canoniques

| Rôle | Responsabilité principale |
|---|---|
| Admin | Gouverne offres, profils, options d'analyse, consentements, modèles documentaires, tarification dynamique |
| Praticien | Conduit la relation de service (séance, validation documents, orientation) |
| Client | Bénéficie du service (RDV, consentements, séance, documents autorisés) |

### B.2 Trois offres principales (Canon V1)

| Offre | Inclus |
|---|---|
| Rendez-vous d'écoute | RDV + salle audio + note interne praticien + synthèse courte |
| Écoute avec compte rendu | Tout Rendez-vous d'écoute + transcription + analyse structurée + compte rendu praticien + version client validable |
| Parcours de soutien | Tout Écoute avec compte rendu + historique multi-séances + documents de mise en pratique + plan de continuité |

### B.3 Profils praticiens × profils clients

**Profils praticiens** : praticien écoute / praticien suivi / praticien supervision renforcée

**Profils clients** : client écoute simple / client suivi documenté / client diffusion selon offre

### B.4 Options configurables par séance

- Médias : enregistrement audio, transcription, conservation, durée rétention
- Analyse : structurée / émotionnelle / contextuelle / pistes / orientation
- Documents : note interne / compte rendu / document client / mise en pratique
- Suivi actif : recommandations, exercices, pratiques, suggestions
- Validation : validation praticien obligatoire, supervision, diffusion
- Relationnel : confirmation, relances, rappels, replanification

### B.5 Règles fermes (cadre légal Québec)

- Aucun diagnostic automatique
- Aucune commission sur l'orientation (Règle A.2 Charte)
- Aucune substitution à un membre d'un ordre professionnel
- Aucune recommandation présentée comme conclusion clinique définitive
- Formation doctrine minimale obligatoire pour tout praticien sous marque IVIA
- Aucune voix biométrique conservée au-delà de J+30 (dès Palier 4)

### B.6 Promesse client

"IVIA vous offre un espace d'écoute qualifié, à distance, où votre parole est entendue, structurée et rendue utile — dans le respect total de votre vie privée et dans le seul objectif de votre autonomie."

### B.7 Trajectoire technologique

**Phase 1 — Stack commerciale (M1 → M12)**
Utilisation de modèles commerciaux (GPT-4.1-mini, Claude, Deepgram Nova-3 Growth) facturés à l'API. Coûts variables présentés en C.5.

**Phase 2 — Modèles évolutifs (M12 → M24)**
Les coûts des modèles équivalents baissent historiquement de ~50 %/an à qualité constante. À budget identique, MERLIN bénéficie d'une marge en hausse mécanique. La grille tarifaire reste stable côté praticien.

**Phase 3 — Modèle propriétaire IVIA (M24+)**
Fine-tuning d'un modèle open-source (Llama, Mistral, Qwen) sur le corpus doctrinal IVIA hébergé en infrastructure propre. Coût marginal proche de zéro, marge → 85–95 %, modèle non-réplicable par concurrents généralistes. Condition préalable : dataset synthétique de 5 000+ cas (atteint à M27-M30).

**Actif stratégique : dataset propriétaire synthétique**
Les séances analysées (avec consentements explicites Niveaux 2 et 3) sont transformées en dataset synthétique selon le pipeline gouverné. Ce dataset, non personnel, constitue un actif valorisable de l'entreprise, fondement du modèle propriétaire et élément clé du moat IVIA.

### B.8 Architecture multi-strates détaillée

**Strate 1 — IVIA Cœur**
- Public : praticiens d'écoute et d'accompagnement hors ordres professionnels
- Offres : Essentiel, Standard, Premium
- Différenciation par rapport aux outils généralistes : cadre doctrinal, pipeline données, audio-only
- Lancement : 31 mai 2026

**Strate 2 — IVIA Professionnels**
- Public : membres d'ordres (psychologues OPQ, psychothérapeutes)
- Offres : adaptées avec module DSP (Dossier Suivi Praticien) conforme ordres
- Différenciation : conformité aux standards cliniques québécois, intégration dans le workflow professionnel réglementé
- Lancement : M13 (juin 2027), après audit juridique de conformité

**Strate 3 — IVIA Soins**
- Public : praticiens corporels et alternatifs (ostéopathes, naturopathes, massothérapeutes, acupuncteurs)
- Offres : adaptées pour intégrer le volet corporel dans la documentation de séance
- Différenciation : pont entre accompagnement émotionnel et pratiques somatiques
- Lancement : M19 (décembre 2027)

**Strate 4 — IVIA Réseau**
- Public : annuaire de référencement éthique, 200+ partenaires référents
- Offres : inscription, référencement
- Règle absolue : JAMAIS de commission par client orienté (Règle A.2 Charte Doctrinaire)
- Financement : frais d'inscription annuels uniquement
- Lancement : M30 (septembre 2028)

### B.9 Charte de transformation gouvernée des données (résumé)

Référence complète : `CHARTE_TRANSFORMATION_GOUVERNEE_DONNEES.md`

**Les 8 étapes du pipeline** :
0. Consentement granulaire (3 niveaux indépendants)
1. Séance audio chiffrée
2. Conservation temporaire brute (J+0 → J+30)
3. Pré-filtrage pertinence (10 % qualifié niveau 3)
4. Transcription + pseudonymisation (90 jours)
5. Extraction signaux structurés anonymisés (7 ans)
6. Effacement audio biométrique irréversible (J+30)
7. Synthétisation IA — cas synthétiques (Palier 5+)
8. Fine-tuning modèle propriétaire (Palier 6 / M24+)

**Garanties fondamentales** :
- Aucune voix identifiable conservée > J+30
- Aucune donnée brute cédée à des tiers
- Dataset final 100 % synthétique

---

## SECTION C — MODÈLE ÉCONOMIQUE

### C.1 Doctrine de monétisation

**MERLIN monétise** : l'outil, l'infrastructure, le service plateforme.

**MERLIN ne monétise PAS** : l'acte d'orientation, l'intérêt du client, la commission sur soin, les données personnelles brutes.

Référence : `CHARTE_DOCTRINAIRE_IVIA.md`, Partie III

### C.2 Trois couches économiques

- **Couche 1 — Frais plateforme** : abonnement praticien + frais par séance traitée (dégressifs au volume)
- **Couche 2 — Options IA à l'usage** : transcription/durée, reporting/séance transcrite
- **Couche 3 — Premium historique** : analyse longitudinale, rapports multi-séances

### C.3 MERLIN collecte le paiement client

Décision maintenue depuis V1.1 : MERLIN encaisse le prix de la séance via Stripe Connect et reverse au praticien après prélèvement de ses frais. Coût Stripe absorbé : 2,91 $ CAD/séance (sur séance type 90 $).

Justification : UX unifiée, contrôle de conformité, visibilité volumes, praticien sans charge fiscale Stripe.

### C.4 Architecture commerciale hybride 3×3

3 plans (Essentiel / Standard / Premium) × 3 paliers de volume = 9 points de prix par séance, présentés commercialement comme "3 plans avec dégressivité automatique selon volume actif".

**3 paliers de volume** (recalculés mensuellement) :
- Petit volume : 0–30 séances/mois
- Volume régulier : 31–80 séances/mois
- Gros volume : 81–200 séances/mois

### C.5 Coûts variables réels par séance (séance type 70 min, 90 $ CAD)

Scénario prudent retenu (Deepgram Growth) :

| Bloc de coût | Plan Essentiel | Plan Standard | Plan Premium |
|---|---:|---:|---:|
| Paiement Stripe | 2,91 $ | 2,91 $ | 2,91 $ |
| Transcription (Deepgram Growth 70 min) | 0 $ | 0,63 $ | 0,63 $ |
| IA analyse + rapport (GPT-4.1-mini) | 0,01 $ | 0,01 $ | 0,01 $ |
| IA analyse historique (Premium) | 0 $ | 0 $ | 0,50 $ |
| Stockage audio 12 mois | 0,01 $ | 0,01 $ | 0,01 $ |
| **Total coût variable** | **2,92 $** | **3,56 $** | **4,06 $** |

### C.5.bis — Pricing par tranche durée (services analytiques activables)

| Service activable / séance | 0–45 min | 46–90 min | 91+ min |
|---|---:|---:|---:|
| Résumé de séance | 1 $ | 2 $ | 3 $ |
| Structuration de séance | 1 $ | 2 $ | 3 $ |
| Analyse client | 2 $ | 3 $ | 5 $ |
| Analyse praticien | 2 $ | 3 $ | 5 $ |
| Suivi actif (recommandations, exercices, pratiques, suggestions) | 3 $ | 5 $ | 8 $ |

**Logique d'inclusion par plan** :
- Essentiel : aucun service analytique inclus — activables à la carte
- Standard : Résumé + Structuration inclus de base ; autres à la carte
- Premium : Résumé + Structuration + Analyse client + Analyse praticien inclus ; Suivi actif à la carte (−33 % tarif dégressif Premium)

**Marge unitaire moyenne (séance 46–90 min)** :
- Suivi actif : prix 5 $ / coût IA 1,20 $ → **marge 76 %**
- Analyse client/praticien : prix 3 $ / coût IA 0,80 $ → **marge 73 %**
- Résumé/Structuration : prix 2 $ / coût IA 0,40 $ → **marge 80 %**

### C.6 Grille tarifaire consolidée

**Tarif par séance (frais plateforme MERLIN)**

| Plan | Petit (0–30) | Régulier (31–80) | Gros (81–200) |
|---|---:|---:|---:|
| Essentiel | 4,90 $ | 4,40 $ | 3,90 $ |
| Standard | 7,90 $ | 7,40 $ | 6,90 $ |
| Premium | 12,90 $ | 11,90 $ | 10,90 $ |

**Abonnement mensuel praticien**

| Palier | Abonnement |
|---|---:|
| Petit | 27,99 $ |
| Régulier | 47,99 $ |
| Gros | 84,99 $ |

### C.7 Marge brute MERLIN par profil (matrice 3×3)

Profils volumes : Petit = 20 séances/mois, Régulier = 60, Gros = 150.

| Plan | Palier | Revenu/mois | Coût variable/mois | Marge brute | Taux marge |
|---|---|---:|---:|---:|---:|
| Essentiel | Petit | 125,99 $ | 58,44 $ | 67,55 $ | 53,6 % |
| Essentiel | Régulier | 311,99 $ | 175,32 $ | 136,67 $ | 43,8 % |
| Essentiel | Gros | 669,99 $ | 438,30 $ | 231,69 $ | 34,6 % |
| Standard | Petit | 185,99 $ | 71,20 $ | 114,79 $ | 61,7 % |
| Standard | Régulier | 491,99 $ | 213,60 $ | 278,39 $ | 56,6 % |
| Standard | Gros | 1 119,99 $ | 534,00 $ | 585,99 $ | 52,3 % |
| Premium | Petit | 285,99 $ | 81,20 $ | 204,79 $ | 71,6 % |
| Premium | Régulier | 761,99 $ | 243,60 $ | 518,39 $ | 68,0 % |
| Premium | Gros | 1 719,99 $ | 609,00 $ | 1 110,99 $ | 64,6 % |

Lecture stratégique :
- Essentiel à gros volume (34,6 %) : point d'entrée compétitif, volontairement lean
- Standard : cœur de marge MERLIN (52-62 %) — différenciateur réel
- Premium : 64-72 % — justifie la valeur plateforme auprès des praticiens établis

### C.8 Hypothèse de répartition des plans

| Plan | M1–M3 | M6 | M12 |
|---|---:|---:|---:|
| Essentiel | 50 % | 35 % | 25 % |
| Standard | 50 % | 50 % | 55 % |
| Premium | 0 % | 15 % | 20 % |

### C.9 Gouvernance tarifaire — paramétrage admin dynamique

Tous les paramètres tarifaires sont configurables depuis l'interface admin MERLIN sans redéploiement applicatif (table `pricing_config` versionnée, audit trail complet).

Paramètres concernés :
- Prix par séance (matrice 3×3)
- Abonnements mensuels par palier
- Prix par tranche durée (C.5.bis)
- Inclusion/exclusion d'un service dans un plan
- Bornes des paliers volume
- Seuil dégressif Premium

Ticket backlog : BACK-011 Admin tarification dynamique (priorisation V10).

---

## SECTION D — CHARGES STRUCTURELLES

### D.1 Frais de fonctionnement pré-revenu (phase pilote)

| Poste | Mensuel estimé | Statut |
|---|---:|---|
| Hébergement OVH (2 VPS + stockage) | 35 $ | Confirmé |
| Abonnements IA dev (Claude Code, Perplexity, Copilot) | 120 $ | Estimé |
| Domaines + DNS + SSL | 5 $ | Confirmé |
| Outils dev + monitoring (Sentry, Umami, Uptime Kuma) | 30 $ | Estimé |
| Comptable/admin (minimum phase pilote) | 150 $ | Estimé |
| **Total frais fixes lean** | **~340 $/mois** | |

### D.2 Rémunération fondateur

David Phaneuf, fondateur et seul développeur full-stack jusqu'au Palier 4 :

**Rémunération cible : 75 000 - 90 000 $ CAD/an**

Justification :
- Équivalent temps plein (50+ heures/semaine)
- Compétences combinées : développement full-stack + IA + gouvernance + gestion de projet
- Marché Montréal 2026 pour profil équivalent : 85 000-120 000 $ en emploi salarié
- La rémunération est délibérément conservatrice pour maximiser les ressources affectées à la mission
- Elle doit être explicite dans tout document de financement pour éviter l'ambiguïté sur la viabilité personnelle du fondateur

**Mode de versement** : salaire via MERLIN inc. (déductible fiscalement, transparent)

### D.3 Charges structurelles croissantes par palier

| Palier | Période | Charges structurelles estimées |
|---|---|---:|
| P1 (M1-M3) | Juin-août 2026 | 12 000-18 000 $ (pilote + constitution) |
| P2 (M4-M6) | Sept-nov 2026 | 20 000-30 000 $/mois |
| P3 (M7-M12) | Déc 2026-mai 2027 | 35 000-50 000 $/mois |
| P4 (M13-M18) | Juin-nov 2027 | 55 000-80 000 $/mois |
| P5 (M19-M27) | Déc 2027-août 2028 | 90 000-130 000 $/mois |
| P6 (M28-M36) | Sept 2028-mai 2029 | 140 000-180 000 $/mois |

---

## SECTION E — SCÉNARIOS FINANCIERS

### E.1 Hypothèses d'acquisition praticiens (scénario médian retenu)

| Mois | Praticiens actifs | Source acquisition |
|---|---:|---|
| M1 (juin 2026) | 2 | Pilote Mylène + Émilie |
| M3 (août 2026) | 2 | Pilote consolidé |
| M6 (nov 2026) | 8 | Cohorte 2 (5-8 praticiennes) |
| M12 (mai 2027) | 15 | Croissance Strate 1 |
| M18 (nov 2027) | 45 | S1 mature + S2 lancement (30-50 pro) |
| M27 (août 2028) | 140 | S1+S2+S3 (80-150 praticiens soins) |
| M36 (mai 2029) | 350 | S1+S2+S3+S4 mature |

### E.2 MRR estimé par palier (scénario médian)

Hypothèses : mix plan 50/50 Standard/Essentiel en phase précoce → 55 % Standard / 20 % Premium à M12+. Volume moyen par praticien : 30 séances/mois (palier Petit→Régulier progressif).

| Palier | Praticiens | MRR estimé | Note |
|---|---:|---:|---|
| P1 fin (M3) | 2 | ~500 $ | Pilote — revenus symboliques |
| P2 fin (M6) | 8 | ~3 500 $ | Cohorte 2 active |
| P3 fin (M12) | 15 | ~8 500 $ | Gate P3→P4 (cible 8 000 $+) |
| P4 fin (M18) | 45 | ~28 000 $ | S1+S2 actives (cible 25 000 $) |
| P5 fin (M27) | 140 | ~68 000 $ | S1+S2+S3 (cible 60 000 $) |
| P6 fin (M36) | 350 | ~155 000 $ | 4 strates (cible 150 000 $) |

**Note d'attention — Scénario MRR M36**
> L'ARR cible de 1,8 M$ (150 000 $/mois × 12) est réalisable mais requiert que la Strate 3 attire effectivement 80-150 praticiens soins d'ici M27. L'adoption de la Strate 3 dépend de la réussite de la Strate 2 comme vecteur de crédibilité. Un retard de 3-6 mois sur la Strate 2 repousserait les cibles M36 de manière proportionnelle. Le scénario pessimiste (1,5 M$ ARR à M36) est budgété dans la section F.

### E.3 P&L synthétique 36 mois (scénario médian)

| Période | Revenus cumulés | Charges cumulées | Résultat net cumul | Auto-financement |
|---|---:|---:|---:|---|
| M1-M6 | ~12 000 $ | ~180 000 $ | −168 000 $ | Financement initial |
| M7-M12 | ~45 000 $ | ~250 000 $ | −373 000 $ | Financement paliers |
| M13-M18 | ~150 000 $ | ~400 000 $ | −623 000 $ | Financement paliers |
| M19-M27 | ~500 000 $ | ~700 000 $ | −823 000 $ | Mix financement + auto |
| M28-M36 | ~1 100 000 $ | ~900 000 $ | −623 000 $ | Auto-financement croissant |

**Lecture** : IVIA n'est pas encore en équilibre financier à M36. L'ARR de 1,8 M$ prévu couvre les charges courantes M36 mais le déficit accumulé des 36 mois requiert le financement de 2,2 M$. L'équilibre courant (MRR = charges mensuelles) est atteint vers M28-M30.

### E.4 Seuil de rentabilité mensuelle

Le seuil de rentabilité mensuelle (revenus = charges) est atteint approximativement avec :
- 50+ praticiens actifs en mix Standard/Premium
- MRR ~25 000-30 000 $

Ce seuil est prévu vers M18-M20 (Palier 4 fin / Palier 5 début).

### E.5 Scénarios de sensibilité

**Scénario bas (financement 1,5 M$)** : Strates 1 et 2 uniquement jusqu'à M36. ARR ~800 K$ à M36. Équilibre financier repoussé à M33-M36. Voir `PLAN_FINANCEMENT_DETAILLE.md`, Plan B.

**Scénario minimal (financement 800 K$)** : Strate 1 uniquement jusqu'à M18, amorce Strate 2. ARR ~300-400 K$ à M36. Viabilité très limitée, pipeline données compromis. Voir `PLAN_FINANCEMENT_DETAILLE.md`, Plan C.

---

## SECTION F — BESOIN DE FINANCEMENT

### F.1 Montant demandé et justification

**Besoin total : 2 200 000 $ CAD sur 36 mois**

La variante 2,2 M$ est retenue (vs 1,8 M$ de référence et 2,0 M$ intermédiaire) pour les raisons suivantes :

1. **Marge R&D pipeline** : +200-400 K$ permettent d'assurer la qualité du pipeline de transformation gouvernée des données — point critique doctrinal. Une économie sur le pipeline risque de compromettre les garanties de la Charte données.

2. **Résilience aux aléas** : les projets technologiques avec composante IA voient régulièrement des dépassements de 20-30 % sur les coûts R&D. La variante 2,2 M$ intègre cette marge.

3. **Fenêtre de marché** : le marché québécois de l'accompagnement émotionnel est en croissance. Un retard d'un palier faute de financement peut créer une ouverture pour un concurrent.

4. **Fondateur et équipe** : la rémunération fondateur (75-90 K$/an) et les recrutements prévus sont intégralement couverts jusqu'à M18 minimum dans la variante 2,2 M$. Dans la variante 1,8 M$, une tension de trésorerie est probable dès M15-M16.

### F.2 Décomposition par palier

| Palier | Période | Investissement | Cumul | Financement |
|---|---|---:|---:|---|
| Palier 1 | M1-M3 | 50 000 $ | 50 000 $ | 100 % subventions/dons |
| Palier 2 | M4-M6 | 80 000 $ | 130 000 $ | 70 % subv. + 30 % capital |
| Palier 3 | M7-M12 | 195 000 $ | 325 000 $ | 70 % subv. + 30 % capital |
| Palier 4 | M13-M18 | 285 000 $ | 610 000 $ | 50 % subv. + 50 % capital + prêts |
| Palier 5 | M19-M27 | 470 000 $ | 1 080 000 $ | 40 % subv. + 40 % capital + 20 % auto |
| Palier 6 | M28-M36 | 690 000 $ | 1 770 000 $ | 30 % subv. + 30 % capital + 40 % auto |
| **Marge de sécurité** | | **430 000 $** | **2 200 000 $** | Réserve décaissée selon besoins |

### F.3 Mix de financement initial (M1-M12)

**70 % subventions et contributions non dilutives** (~225 K$ sur M1-M12)

Sources ciblées :
- PME MTL / PSCSE (Programme de soutien aux créneaux de l'économie sociale) : 50-100 K$
- Investissement Québec (volet innovation sociale) : 50-75 K$
- Fondation Lucie et André Chagnon (santé mentale, technologies) : 50-100 K$
- MEI — volet économie numérique : 25-50 K$
- Fondaction / Chantier de l'économie sociale : 25-50 K$

**30 % capital patient** (~100 K$ sur M1-M12)

Sources ciblées :
- Anges Québec (membres à impact) : 50-75 K$
- Investissement Québec Capital (volet démarrage) : 25-50 K$

Note : Pas de prêt BDC avant Palier 4 (M13+). Le BDC exige des revenus démontrables que IVIA n'atteint pas avant M12-M15.

### F.4 Affectation des fonds par catégorie

| Catégorie | M1-M12 | M13-M24 | M25-M36 | Total |
|---|---:|---:|---:|---:|
| R&D pipeline technique | 80 000 $ | 250 000 $ | 350 000 $ | 680 000 $ |
| Recrutements salariés | 0 $ | 160 000 $ | 380 000 $ | 540 000 $ |
| Rémunération fondateur | 82 500 $ | 165 000 $ | 247 500 $ | 495 000 $ |
| Constitution juridique | 15 000 $ | 5 000 $ | 5 000 $ | 25 000 $ |
| Marketing et développement commercial | 15 000 $ | 50 000 $ | 120 000 $ | 185 000 $ |
| Charges structurelles (infra, admin, légal) | 60 000 $ | 90 000 $ | 125 000 $ | 275 000 $ |
| **Total** | **252 500 $** | **720 000 $** | **1 227 500 $** | **2 200 000 $** |

### F.5 Retour attendu pour les investisseurs

**Retour financier (pour capital investi dans MERLIN inc.)** :
- ARR de 1,8 M$ à M36 avec marges brutes de 55-70 %
- Valorisation estimée à M36 : 5-10× ARR = 9-18 M$ (multiple SaaS health-tech avec moat données)
- Option de liquidité à M36-M42 via rachat OBNL, acquisition stratégique ou financement growth

**Retour d'impact (pour subventions et contributions OBNL)** :
- 300-500 praticiens outillés pour une pratique plus qualitative
- Milliers de clients accompagnés vers l'autonomie émotionnelle
- Dataset unique sur l'accompagnement émotionnel québécois (intérêt pour la recherche)
- Infrastructure numérique québécoise souveraine en santé mentale non clinique

### F.6 Calendrier de décaissement

| Tranche | Montant | Condition | Moment |
|---|---:|---|---|
| T1 | 50 000 $ | Subventions pilote + capital initial | Juillet 2026 |
| T2 | 100 000 $ | Gate P2 (validé fin août 2026) | Septembre 2026 |
| T3 | 175 000 $ | Gate P3 (validé fin novembre 2026) | Décembre 2026 |
| T4 | 285 000 $ | Gate P4 (validé fin mai 2027) | Juin 2027 |
| T5 | 470 000 $ | Gate P5 (validé fin novembre 2027) | Décembre 2027 |
| T6 | 690 000 $ | Gate P6 (validé fin août 2028) | Septembre 2028 |
| Réserve | 430 000 $ | Selon besoins avérés | Décaissement progressif |

---

## SECTION P — PILOTE 31 MAI 2026

### P.1 Mylène — Praticienne pilote

Profil de présence : "Empathe et amoureuse du bonheur. Mylène sait écouter et rebondir. Un soleil émane de sa voix. Réconfortante et aimante, Mylène nous permet de croire."

Rôle : praticienne écoute, plan Standard, démarrage palier Petit volume.

### P.2 Émilie — Praticienne pilote

Profil de présence : "En terme d'écoute active il est difficile de faire mieux. Un électrochoc ou une présence tendre et compréhensive, Émilie sait."

Rôle : praticienne écoute / suivi, plan Standard, démarrage palier Petit volume.

### P.3 David — Fondateur

Profil de présence : "Fondateur de l'expérience, sa voix ni grave ni douce berce ou transporte. Qu'il s'agisse d'écoute ou de compréhension, David entend, comprend, analyse et guide."

Rôle : fondateur, gouvernance, supervision méthode, développement.

### P.4 Objectifs mesurables du pilote (M1–M3)

| Indicateur | Cible M1 | Cible M3 |
|---|---:|---:|
| Praticiennes actives | 2 | 2 |
| Séances réalisées / mois | ≥ 10 | ≥ 30 |
| Taux satisfaction client | Recueil systématique | ≥ 4/5 |
| Documents diffusés validés | 100 % | 100 % |
| Incidents techniques majeurs | Tolérance 1 | 0 |
| Conformité consentements | 100 % | 100 % |

### P.5 Gate Go / No-Go expansion (fin M3)

Critères Go :
- Stabilité technique (uptime > 99 %)
- Au moins 1 praticienne au palier Régulier OU 2 au palier Petit confirmées
- Coûts variables réels alignés ±15 %
- Aucun incident de conformité majeur

Si Go → ouverture cohorte 2 (5-8 praticiennes) en M4 (septembre 2026).

---

## SECTION R — ROADMAP 6 PALIERS / 36 MOIS

Référence complète : `PLAN_INTEGRATION_IVIA_36MOIS.md`

### Vue synthétique

| Palier | Période | Focus | Strates | MRR cible fin palier |
|---|---|---|---|---:|
| P1 | M1-M3 | Pilote IVIA Cœur | S1 | ~500 $ |
| P2 | M4-M6 | Cohorte 2 + Admin tarification | S1 élargi | ~3 500 $ |
| P3 | M7-M12 | Préparation S2 + extraction signaux | S1 mature | ~8 500 $ |
| P4 | M13-M18 | Lancement S2 + synthèse vocale | S1+S2 | ~28 000 $ |
| P5 | M19-M27 | Lancement S3 + synthétisation IA | S1+S2+S3 | ~68 000 $ |
| P6 | M28-M36 | Lancement S4 + modèle propriétaire | S1+S2+S3+S4 | ~155 000 $ |

### État cible M36

- 4 strates actives et autonomes
- 300-500 praticiens/professionnels/partenaires actifs
- MRR ≥ 150 000 $ (1,8 M$ ARR)
- Modèle propriétaire IVIA opérationnel
- Pipeline transformation gouvernée complet et auditable
- Équipe stabilisée 7-8 personnes
- Dataset synthétique propriétaire

---

## SECTION S — RISQUES PRINCIPAUX ET MITIGATIONS

### Cartographie haute

| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| Échec validation pilote P1 | Faible | Élevé | Itération 3 mois supplémentaires ; financement initial couvre 6 mois |
| Refus/freins ordres professionnels (S2) | Moyen | Élevé | Audit juridique préventif P3 ; positionnement "outil de productivité" ; commencer par psychothérapeutes |
| Dépassement coûts pipeline R&D | Moyen | Moyen | Variante 2,2 M$ avec marge 200 K$ R&D ; Phase 3 reportable si nécessaire |
| Dérive doctrinaire sous pression croissance | Faible | Très élevé | Charte dans statuts ; comité doctrinal ; audit annuel public |
| Accélération concurrence IA santé | Moyen | Moyen | Moat éthique-technique unique ; positionnement Québec/français ; vitesse d'exécution palier par palier |
| Épuisement fondateur | Moyen | Élevé | Recrutement dev support dès P4 ; délégation chargés partenariats P3 ; rémunération adéquate |
| Changement réglementaire Loi 25 | Faible | Moyen | Politique vie privée évolutive ; EFVP réalisée ; RPRP nommé |
| Sous-performance acquisition praticiens | Moyen | Moyen | Gates Go/No-Go permettent réajustement ; Plans B et C documentés |
| Tensions liquidité entre décaissements | Faible | Moyen | Réserve de 430 K$ + déclenchement conditionnel des tranches |

---

## ANNEXES

**Annexe 1** : `CHARTE_DOCTRINAIRE_IVIA.md` — Fondation doctrinaire V1.0
**Annexe 2** : `STRUCTURE_JURIDIQUE_RECOMMANDEE.md` — Structure hybride V1.0
**Annexe 3** : `CHARTE_TRANSFORMATION_GOUVERNEE_DONNEES.md` — Pipeline données V1.0
**Annexe 4** : `PLAN_INTEGRATION_IVIA_36MOIS.md` — Roadmap 6 paliers
**Annexe 5** : `PLAN_FINANCEMENT_DETAILLE.md` — Sources, calendrier, conditions
**Annexe 6** : `MERLIN_GOUV_SIMULATION_ECO_COUTS_REELS_V2.md` — Coûts vérifiés
**Annexe 7** : `MERLIN_GOUV_OFFRE_PRATICIENS_GRILLE_COMMERCIALE_V1.md` — Grille V1
**Annexe 8** : `IVIA_DOCUMENT_DIRECTEUR_v1.0.md` — Vision fondatrice

---

**Au sein de l'être — En actes.**

*Version 2.0 — Mai 2026*
*David Phaneuf, fondateur IVIA*

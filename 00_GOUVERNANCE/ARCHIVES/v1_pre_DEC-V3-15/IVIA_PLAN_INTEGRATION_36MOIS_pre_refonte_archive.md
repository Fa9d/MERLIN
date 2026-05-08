# Plan d'intégration progressive IVIA — 36 mois

**Date** : 8 mai 2026
**Statut** : Document stratégique pré-BP V1.2 (à valider avant intégration)
**Auteur** : David Phaneuf + Perplexity Computer
**Objectif** : Définir l'échéancier réaliste d'intégration des 4 strates commerciales et du pipeline de transformation gouvernée des données, calibré sur la capacité réelle de développement IVIA.

---

## Principes directeurs du plan

### P1 — La méthode IVIA d'abord, l'extension après
La Strate 1 (IVIA Cœur) doit être validée sur le terrain avant toute extension. Aucune dilution du positionnement avant preuve de marché.

### P2 — Capacité réelle, pas capacité fantasmée
Le plan est calibré sur :
- 1 fondateur full-stack (David) avec assistance IA
- 2 praticiennes pilote (Mylène + Émilie)
- Recrutements financés graduels selon levée de fonds
- Pas d'équipe commerciale avant M12 minimum

### P3 — Gates Go/No-Go entre paliers
Chaque palier déclenche le suivant uniquement si critères validés. Pas de big bang, pas de fuite en avant.

### P4 — Doctrine non-négociable
À chaque palier, la doctrine IVIA (7 principes + C.1 + charte transformation gouvernée) reste sacrée. Toute extension qui la corromprait est refusée, même si économiquement attractive.

### P5 — Construction progressive du moat
Le pipeline de transformation gouvernée (anonymisation, synthèse vocale, synthétisation IA) se construit en parallèle des strates, pas en bloc. Chaque palier ajoute une couche.

---

## Vue d'ensemble — 6 paliers sur 36 mois

| Palier | Période | Mois | Focus principal | Strate active | Pipeline actif |
|---|---|---|---|---|---|
| **Palier 1** | Juin → Août 2026 | M1–M3 | **Pilote IVIA Cœur** | S1 | Phase 1 (commerciale) |
| **Palier 2** | Sept → Nov 2026 | M4–M6 | **Cohorte 2 + Admin tarification** | S1 (élargi) | Phase 1 + pré-filtrage |
| **Palier 3** | Déc 2026 → Mai 2027 | M7–M12 | **Préparation Strate 2** + Pipeline extraction | S1 mature | Phase 2 (extraction signaux) |
| **Palier 4** | Juin → Nov 2027 | M13–M18 | **Lancement Strate 2 (ordres)** + Synthèse vocale | S1 + S2 | Phase 2 + synthèse vocale |
| **Palier 5** | Déc 2027 → Août 2028 | M19–M27 | **Lancement Strate 3 (soins)** + Synthétisation IA | S1 + S2 + S3 | Phase 2.5 (cas synthétiques) |
| **Palier 6** | Sept 2028 → Mai 2029 | M28–M36 | **Lancement Strate 4 (réseau)** + Modèle propriétaire IVIA | S1+S2+S3+S4 | Phase 3 (fine-tuning) |

---

## Palier 1 — Pilote IVIA Cœur (M1–M3 / juin–août 2026)

### Objectifs
- Valider doctrine, technique, économie sur 2 praticiennes
- Stabiliser infrastructure production (uptime > 99 %)
- Recueillir signaux qualitatifs riches
- Capturer données pour calibrer le pipeline futur

### Livrables
- Pilote opérationnel Mylène + Émilie en mode Standard
- 30+ séances réalisées au M3
- Premier rapport satisfaction client (≥ 4/5)
- Calibration coûts variables réels vs hypothèses BP (±15 %)

### Capacité requise
- David fondateur (gouvernance + dev + supervision pilote)
- Mylène + Émilie praticiennes (relais terrain)
- IA assistants (Claude, Perplexity, Copilot)
- **Aucun recrutement** sur ce palier

### Investissement
- Charges structurelles courantes (cf. BP Section D)
- Aucun nouveau CAPEX significatif
- Budget pilote estimé : ~30-50 K$ (couvert par financement initial)

### Gate Go/No-Go vers Palier 2 (fin août 2026)
**Critères Go** :
- Stabilité technique uptime > 99 %
- Au moins 1 praticienne palier Régulier OU 2 au palier Petit confirmées
- Coûts variables alignés ±15 %
- Aucun incident conformité majeur
- Satisfaction client ≥ 4/5

**Si No-Go** : itération palier 1 sur M4-M6 avant ouverture cohorte 2.

---

## Palier 2 — Cohorte 2 + Admin tarification (M4–M6 / sept–nov 2026)

### Objectifs
- Valider scalabilité méthode IVIA sur 5-8 praticiennes
- Implémenter admin tarification dynamique (BACK-011)
- Démarrer construction pipeline pré-filtrage (Axe 1.5)
- Premiers signaux dataset (sans encore l'exploiter)

### Livrables
- Cohorte 2 recrutée : 5-8 praticiennes IVIA Cœur
- Admin tarification dynamique en production (paramétrage sans redéploiement)
- Pipeline pré-filtrage automatique de pertinence (~30 % séances qualifiées niveau 1)
- Module qualification praticien (opt-in séance "pertinente formation")
- Charte transformation gouvernée v1.0 publiée

### Capacité requise
- David fondateur (architecture pipeline + dev admin)
- 6-10 praticiennes total actives
- IA assistants
- **Premier recrutement éventuel** : conseiller juridique externe (préparation Strate 2) — ~25 K$ sur 6 mois

### Investissement
- Pipeline pré-filtrage (Axe 1.5) : ~40 K$ (R&D)
- Admin tarification BACK-011 : ~15 K$ (R&D incluse dev fondateur)
- Conseiller juridique : ~25 K$
- **Total Palier 2** : ~80 K$

### Gate Go/No-Go vers Palier 3 (fin nov 2026)
**Critères Go** :
- 5+ praticiennes IVIA Cœur actives stables
- Pipeline pré-filtrage opérationnel (10 % séances qualifiées niveau 3)
- Admin tarification utilisé concrètement (≥ 1 ajustement effectué)
- MRR (Monthly Recurring Revenue) ≥ 2 000 $/mois
- Aucun incident doctrinaire majeur

---

## Palier 3 — Préparation Strate 2 + Pipeline extraction (M7–M12 / déc 2026 – mai 2027)

### Objectifs
- Construire pipeline d'extraction de signaux structurés (Axe 2)
- Auditer conformité Strate 2 (psychologues + psychothérapeutes Québec)
- Préparer module DSP (Dossier Suivi Praticien) compatible ordres
- Recruter chargé partenariats ordres
- Stabiliser MRR Strate 1

### Livrables
- Pipeline extraction signaux structurés en production
- Premiers patrons émotionnels structurés extraits (~500 séances pertinentes accumulées)
- Audit juridique conformité OPQ + Ordre psychothérapie complété
- Module DSP en développement (conforme normes ordres)
- Premiers contacts ordres (présentation IVIA, validation principes)
- Migration progressive Phase 1 → Phase 2 modèles évolutifs (services analytiques non-critiques)

### Capacité requise
- David fondateur (architecture pipeline extraction)
- 10-15 praticiennes IVIA Cœur actives
- **Recrutement Palier 3** : 
  - Chargé partenariats ordres (temps partiel) — ~40 K$ sur 6 mois
  - Conseiller juridique continu — ~20 K$ sur 6 mois

### Investissement
- Pipeline extraction signaux (Axe 2) : ~80 K$ (R&D)
- Module DSP préparation : ~30 K$ (R&D)
- Audit juridique ordres : ~15 K$
- Recrutement chargé partenariats : ~40 K$
- Conseiller juridique : ~20 K$
- Migration Phase 2 modèles : ~10 K$ (R&D)
- **Total Palier 3** : ~195 K$

### Gate Go/No-Go vers Palier 4 (fin mai 2027)
**Critères Go** :
- Pipeline extraction opérationnel sur 1 000+ séances qualifiées
- 15+ praticiennes IVIA Cœur actives stables
- Conformité Strate 2 validée par audit juridique
- Module DSP fonctionnel en environnement test
- Au moins 1 lettre d'intérêt formelle d'un ordre ou d'un membre d'ordre
- MRR ≥ 8 000 $/mois

---

## Palier 4 — Lancement Strate 2 + Synthèse vocale (M13–M18 / juin–nov 2027)

### Objectifs
- Lancer commercialement IVIA Professionnels (Strate 2)
- Recruter premiers professionnels d'ordres (psychologues + psychothérapeutes)
- Implémenter synthèse vocale neutre (effacement biométrique J+30)
- Stabiliser pipeline transformation gouvernée complet (Axe 1.5 + 2 + synthèse)

### Livrables
- Offre IVIA Professionnels publiée (grille tarifaire dédiée Strate 2)
- 30-50 professionnels d'ordres recrutés
- Module DSP en production conforme ordres
- Pipeline synthèse vocale neutre opérationnel (TTS qualité IVIA)
- Audio biométrique brut systématiquement supprimé à J+30
- Premier audit annuel de conformité publié
- Charte transformation gouvernée v2.0 (mise à jour avec synthèse vocale)

### Capacité requise
- David fondateur (architecture + supervision)
- 15-20 praticiennes IVIA Cœur + 30-50 professionnels Strate 2
- **Recrutement Palier 4** :
  - Chargé partenariats ordres temps plein — ~80 K$/an
  - Premier dev support (junior ou alternant) — ~50 K$/an
  - Continu : conseiller juridique — ~30 K$/an

### Investissement
- Pipeline synthèse vocale (Axe 2.5) : ~150 K$ (R&D infra TTS + intégration)
- Coûts variables synthèse vocale (cas pédagogiques) : ~10-20 K$/6 mois
- Recrutements salariés : ~80 K$ (6 mois prorata)
- Marketing Strate 2 (conférences ordres, contenus spécialisés) : ~25 K$
- Conseiller juridique continu : ~15 K$
- **Total Palier 4** : ~285 K$

### Gate Go/No-Go vers Palier 5 (fin nov 2027)
**Critères Go** :
- 30+ professionnels Strate 2 actifs
- Pipeline synthèse vocale opérationnel (audio biométrique = 0 conservé > J+30)
- Audit annuel publié sans non-conformité majeure
- MRR consolidé S1 + S2 ≥ 25 000 $/mois
- Premier signal de faisabilité Strate 3 (intérêt ostéos/naturopathes)

---

## Palier 5 — Lancement Strate 3 + Synthétisation IA (M19–M27 / déc 2027 – août 2028)

### Objectifs
- Lancer IVIA Soins (Strate 3) — praticiens corporels et alternatifs
- Construire pipeline synthétisation IA (Axe 3) — génération cas synthétiques
- Affranchir progressivement le dataset de la dépendance directe au consentement individuel
- Stabiliser Strate 2 et préparer Strate 4

### Livrables
- Offre IVIA Soins publiée (adaptations CRM-relation pour soins corporels)
- 80-150 praticiens soins corporels recrutés
- Pipeline synthétisation IA en production (génération cas synthétiques représentatifs)
- Premiers 1 000 cas synthétiques générés à partir du dataset gouverné
- Documentation scientifique du pipeline (publication possible papier blanc)
- Module gestion-relation soins en production

### Capacité requise
- David fondateur (architecture R&D)
- Équipe consolidée : chargé partenariats + dev support + nouveau commercial Strate 3
- **Recrutement Palier 5** :
  - Commercial Strate 3 — ~80 K$/an
  - Data scientist pipeline synthétisation — ~95 K$/an
  - Continu : juridique + dev support

### Investissement
- Pipeline synthétisation IA (Axe 3) : ~180 K$ (R&D + infra ML)
- Module gestion-relation soins : ~60 K$ (R&D)
- Recrutements salariés : ~140 K$ (9 mois prorata)
- Marketing Strate 3 : ~40 K$
- Charges structurelles évolutives : ~50 K$
- **Total Palier 5** : ~470 K$

### Gate Go/No-Go vers Palier 6 (fin août 2028)
**Critères Go** :
- 80+ praticiens Strate 3 actifs
- Dataset synthétique opérationnel (5 000+ cas synthétiques générés)
- MRR consolidé S1+S2+S3 ≥ 60 000 $/mois
- Pipeline transformation gouvernée fonctionnel sur les 4 axes (1.5, 2, 2.5, synthèse vocale)
- Aucun incident doctrinaire ou conformité majeur cumulé sur 27 mois

---

## Palier 6 — Lancement Strate 4 + Modèle propriétaire IVIA (M28–M36 / sept 2028 – mai 2029)

### Objectifs
- Lancer IVIA Réseau (Strate 4) — annuaire de référencement éthique
- Finaliser fine-tuning modèle propriétaire IVIA (Phase 3)
- Atteindre l'autonomie technologique (indépendance fournisseurs externes)
- Consolider l'écosystème IVIA complet sur 4 strates

### Livrables
- Plateforme annuaire IVIA Réseau publiée
- 200+ partenaires référents inscrits (médecins, ostéos, naturopathes, etc.)
- Modèle IVIA fine-tuné en production (Phase 3 active)
- Migration progressive des services analytiques vers modèle propriétaire (50-80 % volume)
- Réduction coût marginal IA → marges 85-95 % sur services analytiques (vs 65-75 % Phase 1)
- Bilan triennal IVIA publié (transparence triple : économique, doctrinaire, scientifique)

### Capacité requise
- Équipe consolidée 7-8 personnes
- **Recrutement Palier 6** :
  - ML Engineer fine-tuning — ~110 K$/an
  - Community Manager Strate 4 — ~60 K$/an
  - Renforcement support : 2e dev — ~70 K$/an

### Investissement
- Fine-tuning modèle propriétaire (Phase 3) : ~250 K$ (R&D + infra GPU)
- Plateforme annuaire Strate 4 : ~80 K$ (R&D)
- Recrutements salariés : ~180 K$ (9 mois prorata)
- Marketing Strate 4 : ~50 K$
- Infrastructure scaling (4 strates simultanées) : ~50 K$
- Charges structurelles évolutives : ~80 K$
- **Total Palier 6** : ~690 K$

### État cible M36
- 4 strates actives et autonomes
- 300-500 praticiens/professionnels/partenaires actifs
- MRR consolidé ≥ 150 000 $/mois (1,8 M$ ARR)
- Modèle propriétaire IVIA opérationnel
- Pipeline transformation gouvernée complet et auditable
- Équipe stabilisée 7-8 personnes
- Dataset synthétique propriétaire — actif valorisable inattaquable

---

## Synthèse financière 36 mois

| Palier | Période | Investissement palier | Cumul | Recrutements actifs |
|---|---|---:|---:|---:|
| Palier 1 | M1–M3 | 50 K$ | 50 K$ | 0 |
| Palier 2 | M4–M6 | 80 K$ | 130 K$ | 1 (juridique externe) |
| Palier 3 | M7–M12 | 195 K$ | 325 K$ | 2 (juridique + partenariats) |
| Palier 4 | M13–M18 | 285 K$ | 610 K$ | 3 (+ dev support) |
| Palier 5 | M19–M27 | 470 K$ | 1 080 K$ | 5 (+ commercial S3 + data scientist) |
| Palier 6 | M28–M36 | 690 K$ | 1 770 K$ | 8 (+ ML eng + community + 2e dev) |

**Hors revenus auto-générés** : ces montants représentent l'investissement brut. Les revenus MRR croissants couvrent progressivement les charges récurrentes à partir du Palier 3-4.

**Besoin de financement net (option C — 1,8 M$)** :
- Couvre intégralement les 6 paliers en mode pessimiste (revenus auto-générés faibles)
- Permet déploiement complet 4 strates + pipeline gouverné + modèle propriétaire
- Marge de sécurité 6-12 mois trésorerie en M36

**Variante optimiste 2,0-2,2 M$** (préférée par David) :
- +200 à 400 K$ de marge de manœuvre sur R&D pipeline
- Permet investissements opportunistes (acquisition compétences clés, partenariats technologiques)
- Sécurise la qualité du pipeline transformation gouvernée (point critique doctrinaire)

---

## Pipeline transformation gouvernée — état par palier

| Palier | Pré-filtrage Axe 1.5 | Extraction Axe 2 | Synthèse vocale | Synthétisation Axe 3 | Modèle propriétaire Phase 3 |
|---|---|---|---|---|---|
| P1 | — | — | — | — | — |
| P2 | ✅ Construit | — | — | — | — |
| P3 | ✅ Mature | ✅ Construit | — | — | — |
| P4 | ✅ Mature | ✅ Mature | ✅ Construit | — | — |
| P5 | ✅ | ✅ | ✅ Mature | ✅ Construit | — |
| P6 | ✅ | ✅ | ✅ | ✅ Mature | ✅ Construit/Mature |

**Lecture** : à M36, l'ensemble du pipeline gouverné est en production mature, les données biométriques individuelles sont systématiquement effacées à J+30 depuis M18, le dataset synthétique est devenu l'actif principal, et le modèle propriétaire IVIA tourne en infra propre.

---

## Strates commerciales — état par palier

| Palier | S1 IVIA Cœur | S2 IVIA Pro | S3 IVIA Soins | S4 IVIA Réseau |
|---|---|---|---|---|
| P1 | 🌱 Pilote 2 | — | — | — |
| P2 | 🌿 Cohorte 2 (5-8) | — | — | — |
| P3 | 🌳 15+ praticiennes | 🔧 Préparation | — | — |
| P4 | 🌳 Mature | 🌱 Lancement (30-50) | — | — |
| P5 | 🌳 | 🌿 Croissance | 🌱 Lancement (80-150) | 🔧 Préparation |
| P6 | 🌳 | 🌳 | 🌿 Croissance | 🌱 Lancement (200+) |

**Légende** : 🔧 préparation / 🌱 lancement / 🌿 croissance / 🌳 mature

---

## Risques principaux et mitigations

### Risque 1 — Échec validation pilote (Palier 1)
**Mitigation** : itération 3 mois supplémentaires sans engager Palier 2. Financement initial dimensionné pour 6 mois de pilote.

### Risque 2 — Refus ou freins ordres professionnels (Strate 2)
**Mitigation** : audit juridique préventif (Palier 3), positionnement strict "outil de productivité" (pas substitution acte professionnel), commencement par psychothérapeutes (encadrement plus souple).

### Risque 3 — Coût pipeline transformation supérieur aux estimations
**Mitigation** : variante optimiste 2,2 M$ avec marge 200 K$ R&D, possibilité de différer Phase 3 (modèle propriétaire) si nécessaire sans compromettre les autres axes.

### Risque 4 — Dérive doctrinaire sous pression croissance
**Mitigation** : charte doctrinaire dans statuts (à valider en A.6 V1.2), comité de gouvernance avec représentation praticiens, audit doctrinaire annuel publié.

### Risque 5 — Accélération concurrence (gros acteurs IA en santé)
**Mitigation** : moat éthique-technique unique (pipeline transformation gouvernée), positionnement Québec/français spécifique, vitesse d'exécution palier par palier.

### Risque 6 — Épuisement fondateur (1 dev seul jusqu'à Palier 4)
**Mitigation** : recrutement dev support dès Palier 4 (M13), répartition charge mentale via délégation aux chargés de partenariats Palier 3.

---

## Synthèse exécutive

Ce plan d'intégration IVIA sur 36 mois propose :

1. **Une trajectoire prudente** ancrée sur la validation pilote avant toute extension
2. **Un déploiement multi-strates progressif** avec gates Go/No-Go entre chaque palier
3. **Un pipeline de transformation gouvernée des données** construit en parallèle, palier par palier
4. **Un investissement total de 1,8 M$ (option de référence)** ou 2,0-2,2 M$ (variante sécurisée)
5. **Un atterrissage M36** avec écosystème complet 4 strates, modèle propriétaire IVIA, équipe de 7-8 personnes, MRR ≥ 150 000 $/mois
6. **Une cohérence doctrinaire absolue** maintenue à chaque palier par charte, audits, gouvernance

C'est un plan **ambitieux mais soutenable**, calibré sur la capacité réelle de développement actuelle et les recrutements financés progressivement par la levée de fonds.

---

## Devise

*Au sein de l'être — En actes.*

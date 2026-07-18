# AUDIT DE COHÉRENCE POST-DÉC-V3-15

**Document** : Rapport d'audit Phase 1
**Date** : 8 mai 2026
**Auteur** : Computer (lead) — pour validation David Phaneuf
**Référence** : DÉC-V3-15 (architecture David → IVIA inc. SPA-mère LSAQ → IVIA OBNL satellite LCQ III + filiales projets)
**Statut** : ✅ **EXÉCUTÉ — PHASE 3 LIVRÉE (8 mai 2026)**
**Portée** : repo `MERLIN_repo` (master post-merge PR #1, 23 249 insertions, 55 fichiers)

---

## 1. Synthèse exécutive

L'audit cohérence post-DÉC-V3-15 révèle **3 points bloquants**, **3 points importants**, **4 points de cohérence** et un **socle propre vérifié sur le code, le schéma DB et les prompts METH**.

**Le repo n'est PAS prêt à servir de base aux consultations cabinets fiscaux ni à un dépôt investisseurs sans patch préalable.**

Les bloquants concernent :
1. **L'INDEX documentaire v2.0 entièrement cassé** sur GitHub (chemins absolus sandbox, 79 liens morts)
2. **La Politique de confidentialité Loi 25** qui désigne encore *MERLIN inc.* comme responsable du traitement — contradiction directe avec les CGU v1.1 et risque légal
3. **Le BP v2.0** qui sous-estime le CRIC (14 % ancien régime au lieu de 30 % remboursable nouveau régime budget Québec 2025-2026), confirmé explicitement par le brief fiscaliste

Le code applicatif (TS/Python), le schéma de données (Prisma + SQLAlchemy) et les prompts METH-001 à 004 sont **entité-agnostiques** — aucun patch nécessaire de ce côté. C'est le différentiel docs/contrats qui crée le risque.

**Recommandation** : déclencher Phase 2 (reclassement par criticité réelle : *bloquant pilote* / *bloquant levée* / *cohérence différable*) puis Phase 3 (plan de patch ordonné, exécution séquentielle avec validation par toi à chaque palier) **avant tout autre chantier produit ou commercial**.

---

## 2. 🔴 Bloquants (3)

### B1 — INDEX_BASE_DOCUMENTAIRE_v2.0 cassé sur GitHub

**Fichier** : `00_GOUVERNANCE/IVIA_INDEX_BASE_DOCUMENTAIRE_v2.0.md`
**Constat** : 79 liens markdown pointent vers des chemins absolus sandbox du type `/home/user/workspace/CHARTE_DOCTRINAIRE_IVIA.md` au lieu de chemins relatifs repo type `00_GOUVERNANCE/IVIA_CHARTE_DOCTRINAIRE_v2.0.md`.
**Impact** : INDEX inutilisable sur GitHub (tous les liens 404). C'est précisément le document qui sert de point d'entrée à toute personne arrivant sur le repo (cabinets, investisseurs, futur DPO, futur CTO).
**Sévérité** : 🔴 Bloquant pour tout partage externe du repo.
**Effort estimé** : 1 h (réécriture systématique des 79 liens avec table de correspondance par dossier).

---

### B2 — IVIA_POLITIQUE_CONFIDENTIALITE_LOI25_v1.0 désigne *MERLIN inc.* comme responsable du traitement

**Fichier** : `12_JURIDIQUE/IVIA_POLITIQUE_CONFIDENTIALITE_LOI25_v1.0.md`
**Constat** : 4 occurrences de *MERLIN inc.* en position de responsable du traitement (lignes 55, 57, 329, 446). Or :
- Les CGU v1.1 (clients + praticiens) ont été refondues le 8 mai 2026 avec note de transition explicite désignant **David Phaneuf, travailleur autonome** comme contractant actuel et **IVIA inc.** comme entité juridique cible (incorporation Q3-Q4 2026, roulement art. 85 LIR).
- Le contrat praticien type v1.1 suit la même structure.
- La Charte doctrinaire v2.0 et la Gouvernance interne v2.0 confirment l'architecture DÉC-V3-15 où IVIA inc. (SPA-mère LSAQ) est l'entité juridique pivot, et *MERLIN* est un produit, pas une personne morale.

**Impact** :
- Contradiction interne entre documents juridiques.
- La Loi 25 (RLRQ c. P-39.1) impose que la Politique de confidentialité identifie correctement le responsable du traitement. Une incohérence est un angle d'attaque CAI direct.
- Tout client signant les CGU v1.1 avec un contractant *David Phaneuf TA* mais lisant que ses données sont sous la responsabilité de *MERLIN inc.* (entité non-existante ce jour) constitue un défaut de transparence.

**Sévérité** : 🔴 Bloquant pour mise en ligne / activation pilote auprès de nouveaux clients.
**Effort estimé** : 1,5 h (patch v1.1 sur le modèle CGU v1.1 — note de transition + responsable du traitement = David Phaneuf TA aujourd'hui, IVIA inc. après incorporation).

---

### B3 — BP v2.0 sous-estime le CRIC

**Fichier** : `01_BUSINESS/IVIA_BP_v2.0.md`
**Constat** : Lignes 195, 623, 702 utilisent un taux CRIC d'environ 14 % (correspond à l'ancien régime CIR pré-réforme). Or le `BRIEF_FISCALISTE_v1.0` (ligne 77 et autour) confirme :
- **CRIC nouveau régime (budget Québec 2025-2026)** : 30 % remboursable sur la première tranche de 1 M$ de dépenses admissibles, 20 % au-delà.
- Le brief précise textuellement : *« Cette projection sous-estime potentiellement le bénéfice du nouveau CRIC à 30 %. À recalibrer. »*

**Impact** :
- Le BP v2.0 minore le retour fiscal sur les dépenses R&D, donc **dégrade artificiellement les indicateurs de viabilité** présentés aux cabinets et aux investisseurs.
- Le `MODELE_VALORISATION_IVIA` et le `PLAN_FINANCEMENT_DETAILLE` héritent vraisemblablement de la même hypothèse — à vérifier (audit v2 nécessaire sur ces deux documents avec la nouvelle hypothèse CRIC).
- Présenter ce BP à RCGT (Pascal Perreault) **sans correction préalable serait amateur** : le fiscaliste va immédiatement signaler l'erreur.

**Sévérité** : 🔴 Bloquant pour les courriels P1 cabinets et tout partage investisseur.
**Effort estimé** : 2-3 h (recalibrage CRIC dans BP v2.0 + impact MODELE_VALORISATION + PLAN_FINANCEMENT_DETAILLE + note d'avertissement dans NOTE_CONFIDENTIELLE_INVESTISSEURS).

---

## 3. 🟠 Importants (3)

### I1 — IVIA_MENTIONS_LEGALES_v0.1 sans note de transition

**Fichier** : `12_JURIDIQUE/IVIA_MENTIONS_LEGALES_v0.1.md`
**Constat** : Mentionne uniquement *David Phaneuf travailleur autonome*, ne mentionne pas la transition vers IVIA inc. À harmoniser avec les CGU v1.1 si le document est affiché en production sur ivia.quebec.
**Sévérité** : 🟠 Important si page publique active.
**Effort estimé** : 30 min (patch v0.2 avec note de transition courte).

---

### I2 — CARTOGRAPHIE_RISQUES_v1.0 réfère encore à *MERLIN inc.*

**Fichier** : `00_GOUVERNANCE/IVIA_CARTOGRAPHIE_RISQUES_v1.0.md`
**Constat** : 10 occurrences *MERLIN inc.*, dont rôle « CTO MERLIN inc. » comme responsable opérationnel de plusieurs risques.
**Statut BILAN_COHERENCE_REFONTE_v2.0** : explicitement déclaré différable à l'incorporation Q3-Q4 2026 (substitution mécanique).
**Tension** : différable doctrinalement, mais matériellement incohérent avec la nouvelle archi présentée à un cabinet.
**Sévérité** : 🟠 Important (pas bloquant pilote, mais incohérent en cas d'audit externe).
**Effort estimé** : 45 min (patch v1.1 avec substitution + note de transition).

---

### I3 — POLITIQUE_TARIFICATION_DYNAMIQUE_v1.0 — Comité tarifaire référé à *MERLIN inc.*

**Fichier** : `00_GOUVERNANCE/IVIA_POLITIQUE_TARIFICATION_DYNAMIQUE_v1.0.md`
**Constat** : 3 occurrences *MERLIN inc.* dans la composition du Comité tarifaire (lignes 158, 175, 176).
**Statut BILAN_COHERENCE** : déclaré différable.
**Sévérité** : 🟠 Important (gouvernance produit, peu visible mais incohérent).
**Effort estimé** : 20 min.

---

## 4. 🟡 Cohérence (4)

### C1 — Date DÉC-V3-15 : 8 mai vs 15 mai 2026

**Constat** : 20 occurrences « 8 mai 2026 » contre 2 occurrences « 15 mai 2026 » (dont `BILAN_COHERENCE_REFONTE_v2.0.md` ligne 9).
**Cause probable** : confusion entre numéro de décision (DÉC-V3-**15**) et date.
**Sévérité** : 🟡 Cohérence rédactionnelle.
**Effort** : 5 min (`grep` + `sed`).

---

### C2 — GLOSSAIRE_v1.0 : 26 occurrences *MERLIN inc.* (ancienne architecture)

**Fichier** : `00_GOUVERNANCE/IVIA_GLOSSAIRE_v1.0.md`
**Constat** : Le glossaire définit l'ancienne archi (IVIA OBNL mère / MERLIN inc. SPA fille) — antérieure à DÉC-V3-15.
**Statut BILAN_COHERENCE** : substitution mécanique différée à l'incorporation = doctrinalement cohérent.
**Recommandation** : ajouter une **note d'avertissement en tête** (« ce glossaire reflète la terminologie pré-DÉC-V3-15 ; substitution mécanique IVIA OBNL → IVIA inc. SPA-mère et MERLIN inc. → IVIA inc. à l'incorporation Q3-Q4 2026 »).
**Sévérité** : 🟡 Cohérence (différable, à ne pas oublier).
**Effort** : 10 min (note d'avertissement) ou 1,5 h (refonte intégrale alignée DÉC-V3-15).

---

### C3 — POLITIQUE_BIEN_ETRE_PRATICIENS_v1.0 — 1 occurrence *MERLIN inc.*

**Fichier** : `00_GOUVERNANCE/IVIA_POLITIQUE_BIEN_ETRE_PRATICIENS_v1.0.md` (ligne 351).
**Sévérité** : 🟡 Cohérence mineure.
**Effort** : 5 min.

---

### C4 — Coexistence de deux systèmes décisionnels

**Constat** :
- **74 occurrences** `DEC-XXX` (ADR techniques + MERLIN_GOUV_*) — système hérité.
- **115 occurrences** `DÉC-V3-X` — système stratégique IVIA en cours.
**Univers documentaires séparés**, pas de conflit identifié — les ADR techniques restent valides pour leur portée.
**Recommandation** : documenter cette coexistence dans `INDEX_GOUVERNANCE_V1.md` ou en tête de l'INDEX_BASE_DOCUMENTAIRE pour qu'un nouvel arrivant ne perde pas pied.
**Sévérité** : 🟡 Cohérence (clarté narrative).
**Effort** : 15 min.

---

## 5. 🟢 Propre / Vérifié

| Élément | État | Note |
|---|---|---|
| **CGU clients v1.1** | ✅ Refondu DÉC-V3-15 | Note transition + roulement art. 85 LIR explicite |
| **CGU praticiens v1.1** | ✅ Refondu DÉC-V3-15 | Idem |
| **CONTRAT_PRATICIEN_TYPE_v1.1** | ✅ Refondu DÉC-V3-15 | Idem |
| **IVIA_POLITIQUE_CONFIDENTIALITE_v0.1** (page publique web) | ✅ | « David Phaneuf fondateur », pas de *MERLIN inc.* |
| **Code TypeScript / Python** | ✅ Entité-agnostique | 0 occurrence *MERLIN inc.*, *IVIA inc.*, *OBNL* |
| **PublicLayout.tsx** | ✅ | « © IVIA. Montréal, Québec. » |
| **Schéma Prisma** (15 modèles) | ✅ Entité-agnostique | Aucun rattachement entité juridique |
| **Schéma SQLAlchemy** (11 modèles) | ✅ Entité-agnostique | Idem |
| **Prompts METH-001 à 004** | ✅ Entité-agnostique | Réfèrent *MERLIN* en tant que produit, pas personne morale |
| **Chiffres BP : 2,2 M$ / 600 K$ tranche 1** | ✅ Cohérents | BP, Note investisseurs, Plan financement, Modèle valo concordent (sous réserve de l'erreur CRIC §B3) |

---

## 6. Statistiques globales

| Indicateur | Valeur |
|---|---|
| Occurrences `MERLIN inc.` totales (hors archives) | **114** |
| Dont GLOSSAIRE | 26 |
| Dont PLAN_SORTIE_CONTINUITE | 17 |
| Dont 00_GOUVERNANCE (autres) | 14 |
| Dont 12_JURIDIQUE (incl. POLITIQUE_CONFIDENTIALITE_LOI25 §B2) | 7 |
| Dont 03_PLANNING | 3 |
| Dont 04_METHODES | 2 |
| Dont INDEX_BASE_DOCUMENTAIRE | 1 |
| Occurrences `DEC-XXX` (ADR) | 74 |
| Occurrences `DÉC-V3-X` (stratégique) | 115 |
| Liens INDEX cassés (chemins sandbox absolus) | 79 |

---

## 7. Recommandations Phase 2 et Phase 3

### Phase 2 — Reclassement par criticité réelle

Trois axes de criticité, **distincts de la sévérité éditoriale ci-dessus** :

- **Axe A — Bloquant pilote** (compromet l'activation/poursuite du pilote Mylène + Émilie) : **B2** (Politique confidentialité Loi 25)
- **Axe B — Bloquant levée / consultations cabinets** (compromet courriels P1 et envoi BP) : **B1** (INDEX cassé), **B3** (CRIC sous-estimé)
- **Axe C — Cohérence différable** (peut attendre l'incorporation Q3-Q4 2026, sous réserve de note d'avertissement claire) : **I1**, **I2**, **I3**, **C1**, **C2**, **C3**, **C4**

### Phase 3 — Plan de patch ordonné (proposition)

| Ordre | Patch | Estimé | Validation requise |
|---|---|---|---|
| 1 | B1 — Réécriture INDEX (chemins relatifs) | 1 h | Toi (revue avant push) |
| 2 | B2 — POLITIQUE_CONFIDENTIALITE_LOI25 v1.1 sur modèle CGU v1.1 | 1,5 h | Toi (revue contenu transition) |
| 3 | B3 — Recalibrage CRIC dans BP v2.0 + impact MODELE_VALORISATION + PLAN_FINANCEMENT + note investisseurs | 2-3 h | Toi (revue chiffres) |
| 4 | C1 — Uniformisation date 8 mai 2026 | 5 min | Pas critique |
| 5 | C2 — Note d'avertissement GLOSSAIRE | 10 min | Toi |
| 6 | C4 — Note coexistence DEC vs DÉC-V3 dans INDEX | 15 min | Toi |
| 7 | I1, I2, I3, C3 — Patches mineurs | ~2 h | Groupé en un seul commit |

**Total estimé** : ~8-10 h de travail concentré pour un repo réellement cohérent et présentable.

**Stratégie commit** : un commit par patch bloquant (B1, B2, B3) avec message clair, puis un commit groupé pour les cohérences mineures. PR séparée par bloquant pour traçabilité.

---

## 8. Phase 3 — Patches livrés

| Patch | Livrable | Fichier |
|---|---|---|
| **B1** | INDEX réécrit avec chemins relatifs cliquables + note coexistence DEC vs DÉC-V3-X | [`IVIA_INDEX_BASE_DOCUMENTAIRE_v2.1.md`](IVIA_INDEX_BASE_DOCUMENTAIRE_v2.1.md) |
| **B2** | Politique confidentialité Loi 25 v1.1 (note transition David TA → IVIA inc.) | [`../12_JURIDIQUE_AFFAIRES/IVIA_POLITIQUE_CONFIDENTIALITE_LOI25_v1.1.md`](../12_JURIDIQUE_AFFAIRES/IVIA_POLITIQUE_CONFIDENTIALITE_LOI25_v1.1.md) |
| **B3** | BP v2.1 + Note investisseurs v2.1 (CRIC nouveau régime 30 % → +110 K $, non-dilutif 54,5 % → 59,5 %) | [`../12_JURIDIQUE_AFFAIRES/IVIA_BP_FINANCEMENT_v2.1.md`](../12_JURIDIQUE_AFFAIRES/IVIA_BP_FINANCEMENT_v2.1.md), [`../12_JURIDIQUE_AFFAIRES/IVIA_NOTE_CONFIDENTIELLE_INVESTISSEURS_v2.1.md`](../12_JURIDIQUE_AFFAIRES/IVIA_NOTE_CONFIDENTIELLE_INVESTISSEURS_v2.1.md) |
| **C1** | Date DÉC-V3-15 uniformisée sur 8 mai 2026 (BILAN_COHERENCE + PLAN_INTEGRATION) | — |
| **C2** | Note d'avertissement terminologique en tête du GLOSSAIRE | [`IVIA_GLOSSAIRE_v1.0.md`](IVIA_GLOSSAIRE_v1.0.md) |
| **C4** | Note coexistence DEC-XXX vs DÉC-V3-X intégrée dans l'INDEX v2.1 | (cf. B1) |
| **I1** | Mentions légales v0.2 (note transition + transfert PI roulement art. 85 LIR + rappel dépôts OPIC) — depuis révisées en v0.3 (2026-07-17) | [`../12_JURIDIQUE_AFFAIRES/IVIA_MENTIONS_LEGALES_v0.3.md`](../12_JURIDIQUE_AFFAIRES/IVIA_MENTIONS_LEGALES_v0.3.md) |
| **I2, I3, C3** | Notes terminologiques en tête des 3 politiques opérationnelles (Cartographie risques, Tarification, Bien-être praticiens) | (cf. fichiers respectifs) |
| **Bonus** | Création du journal de bord pilote MERLIN (angle mort levé) | [`JOURNAUX/JOURNAL_PILOTE_MERLIN.md`](JOURNAUX/JOURNAL_PILOTE_MERLIN.md) |

### Archives

Les versions remplacées ont été déplacées vers `12_JURIDIQUE_AFFAIRES/ARCHIVES/` :
- `IVIA_BP_FINANCEMENT_v2.0_archive.md`
- `IVIA_NOTE_CONFIDENTIELLE_INVESTISSEURS_v2.0_archive.md`
- `IVIA_POLITIQUE_CONFIDENTIALITE_LOI25_v1.0_archive.md`
- `IVIA_MENTIONS_LEGALES_v0.1_archive.md`

### Ce qui reste différé à l'incorporation IVIA inc. (Q3-Q4 2026)

- Substitution mécanique complète `MERLIN inc.` → `IVIA inc.` dans les ~110 occurrences résiduelles (GLOSSAIRE, PLAN_SORTIE_CONTINUITE, CARTOGRAPHIE_RISQUES, etc.) — doctrinalement validé par BILAN_COHERENCE_REFONTE_v2.0 §3, signalé par notes d'avertissement contextuelles dans chaque document concerné.
- Révision intégrale du GLOSSAIRE alignée DÉC-V3-15 (planifiée post-incorporation).
- Mise à jour MENTIONS_LEGALES v1.0 avec NEQ IVIA inc. et siège social (post-incorporation).

### Écarts soulevés par l'audit qui nécessitent un input externe

- **Cumulabilité RS&DE/CRIC sur les mêmes dépenses admissibles** : à confirmer par le fiscaliste mandaté en P1 (cf. BRIEF_FISCALISTE_v1.0 §C.86). Le BP v2.1 retient une hypothèse prudente d'effets complémentaires partiels.
- **Validation cabinet juridique** des CGU v1.1, MENTIONS_LEGALES v0.2, POLITIQUE_CONFIDENTIALITE v1.1 avant publication définitive sur ivia.quebec.

---

*Au sein de l'être — En actes.*

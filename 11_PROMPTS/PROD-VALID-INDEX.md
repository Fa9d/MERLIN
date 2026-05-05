---
titre: INDEX — Plan de validation MERLIN/IVIA pour finançabilité
id: PROD-VALID-INDEX
statut: active
type: charte
couche: PROD
périmètre: navigation livrables
auteur: fondateur
date: 2026-05-05
version: 1.0
dépend_de: [PROD-VALID-001, PROD-VALID-002]
remplace: []
arbitrage_requis: non
source_canonique: 11_PROMPTS/PROD-VALID-INDEX.md
---

# INDEX — Documents de validation MERLIN/IVIA (2026-05-05)

## Navigation rapide

Vous cherchez... → Allez ici

| Besoin | Document | Section |
|---|---|---|
| **Comprendre le moteur** (architecture, routes) | PROD-VALID-001 | Section 1 |
| **Liste des prompts critiques + état** | PROD-VALID-001 | Section 2 |
| **Décision sur un test manquant** | PROD-VALID-002 | LIVRABLE 4 |
| **MVP à montrer au financeur** | PROD-VALID-001 | Section 6 |
| **Chronologie 14 jours** | PROD-VALID-002 | LIVRABLE 6 |
| **Fichiers à créer/modifier** | PROD-VALID-001 | Section 8 |
| **Quels tests démarrer demain** | PROD-VALID-002 | LIVRABLE 4 |
| **Risques de sécurité/intégrité** | PROD-VALID-001 | Section 5 |
| **Couverture de test actuelle** | PROD-VALID-002 | LIVRABLE 3 |
| **Preuves à montrer au financeur** | PROD-VALID-001 | Section 9.1 |

---

## Vue d'ensemble (2 pages)

### Document A: PROD-VALID-001 (cartographie complet)

**20 pages, 8 sections, référence complète**

- **Section 1** : Cartographie backend (modules, routes API, flux critique)
- **Section 2** : Prompts critiques METH-001/002/003 (état externalisation, schéma sortie)
- **Section 3** : Tests existants (~7 tests, couverture 5-10%)
- **Section 4** : Tests manquants (7 tests, plan 5-8 jours)
- **Section 5** : Zones fragiles pour usage sensible
- **Section 6** : MVP démontrable (scénario 8-10 min)
- **Section 7** : Plan 14 jours (chronologie semaine 1-2)
- **Section 8** : Fichiers à modifier (exact)
- **Section 9** : Recommandations finançabilité
- **Annexes A-B** : Dépendances + checklist

**Lecture** : 40-60 min (complet)
**Skim** : 15-20 min (sections 1, 6, 7)

### Document B: PROD-VALID-002 (résumé exécutif)

**5 pages, 7 livrables, action rapide**

- **LIVRABLE 2** : Prompts critiques (table succincte)
- **LIVRABLE 3** : Tests existants (récap)
- **LIVRABLE 4** : Tests manquants prioritaires (7 tests, timeline)
- **LIVRABLE 5** : MVP démontrable (pitch 3 min)
- **LIVRABLE 6** : Plan 14 jours (chronologie)
- **LIVRABLE 7** : Fichiers à modifier (listes)

**Lecture** : 15-20 min (tous les livrables)
**Decision** : 5 min (section "Décision rapide pour fondateur")

---

## Les 7 livrables demandés

| # | Livrable | Fichier | Section | Pages |
|---|---|---|---|---|
| 1 | Cartographie moteur | PROD-VALID-001 | Sect. 1-2 | 8 |
| 2 | Prompts critiques | PROD-VALID-001/002 | Sect. 2 / Livr. 2 | 3+1 |
| 3 | Inventaire tests | PROD-VALID-001/002 | Sect. 3 / Livr. 3 | 2+1 |
| 4 | Tests manquants | PROD-VALID-001/002 | Sect. 4 / Livr. 4 | 2+1 |
| 5 | MVP démontrable | PROD-VALID-001/002 | Sect. 6 / Livr. 5 | 2+0,5 |
| 6 | Plan 14 jours | PROD-VALID-001/002 | Sect. 7 / Livr. 6 | 1+0,5 |
| 7 | Fichiers à modifier | PROD-VALID-001/002 | Sect. 8 / Livr. 7 | 1+0,5 |

**Total** : ~25 pages de contenu structuré

---

## Pour différentes audiences

### Fondateur (decision-maker)
1. Lire PROD-VALID-002 (5 pages, 15 min)
2. Décider : lancer tests P1 maintenant ? (DEC-041 votée)
3. Valider Anthropic API + budget

### Dev lead
1. Lire PROD-VALID-001 Section 1 (architecture)
2. Lire PROD-VALID-001 Section 4 (tests manquants détail)
3. Lire PROD-VALID-002 LIVRABLE 7 (fichiers à créer)
4. Commencer BLOC 1 tests (jour 1)

### Financeur technique
1. Lire PROD-VALID-002 LIVRABLE 5 (MVP pitch, 3 min)
2. Lire PROD-VALID-001 Section 6 (MVP détail, 5 min)
3. Voir démo (8-10 min)
4. Lire PROD-VALID-001 Section 9 (risques, 5 min)

### Superviseur/praticien
1. Lire PROD-VALID-001 Section 2 (prompts MERLIN)
2. Lire PROD-VALID-001 Section 9.1 (preuves de sécurité)
3. Attendre démo MVP (validation superviseur workflow)

---

## Points critiques à retenir (TL;DR)

### Moteur
✅ Backend structuré, routes claires, BDD stable
❌ Tests réels moteur IA = **ABSENT**
⚠️ Zones fragiles = analyse intake + supervision

### Prompts
✅ Externalisés et versionnés (METH-001/002/003)
❌ Aucun test sur contenu/logique
⚠️ Modification passe par fichier Markdown (discipline requise)

### Tests
❌ Couverture très basse (~5-10%)
⚠️ 7 tests manquants = 5-8 jours
✅ Tests P1 exécutables immédiatement

### MVP
✅ Démontrable en 8-10 min (scénario client réel)
✅ Preuve: intake → moteur → document client
❌ Besoin tests P1 **avant** démo financeur

### Timing
✅ Plan 14 jours viable
⚠️ Path critique = jour 1-5 (moteur IA)
❌ Si Claude API indisponible → pivot requis

---

## Décisions déjà prises

| Décision | Référence | Date | Statut |
|---|---|---|---|
| Externaliser 3 prompts critiques | DEC-040 | 2026-05-05 | ✅ Votée |
| Lancer validation technique | **DEC-041** | 2026-05-05 | ⏳ À voter |
| Plan 14 jours pour MVP | PROD-VALID-001 S.7 | 2026-05-05 | Proposé |

---

## Prochaines étapes immédiates

**Jour 1 (après cette lecture)** :
- [ ] Fondateur vote DEC-041 (validation technique)
- [ ] Dev lead crée `tests/test_session_note_generation.py`
- [ ] Valider Anthropic API key + budget

**Jours 2-5** :
- [ ] BLOC 1 tests (moteur IA, schema, prompts)
- [ ] Correction failures
- [ ] Validation finale

**Jours 6-14** :
- [ ] E2E réel + supervision
- [ ] Préparation démo
- [ ] Démo financeur

---

## Fichiers clés (référence rapide)

| Fichier | Rôle | Modifié ? |
|---|---|---|
| `app/ai/prompts/session_note_cercle_v1.py` | Charge les 3 prompts + render prompt | À tester |
| `app/ai/anthropic_session_note_pipeline.py` | Pipeline Claude API | À valider schema |
| `11_PROMPTS/02_METH/METH-001/002/003.md` | Prompts externalisés | Actifs ✅ |
| `app/ai/prompt_loader.py` | Loader dynamique | Actif ✅ |
| `tests/` | Tests | À créer (7 fichiers) |

---

## Ressources

**Lire d'abord** :
1. PROD-VALID-001 Sections 1, 6, 7
2. PROD-VALID-002 LIVRABLES 4, 5, 6

**Puis** :
3. PROD-VALID-001 Sections 2, 3, 4
4. PROD-VALID-001 Section 8 (file creation list)

**Référence complète** :
5. PROD-VALID-001 Sections 5, 8, 9

---

## Historique

| Version | Date | Auteur | Nature |
|---|---|---|---|
| 1.0 | 2026-05-05 | fondateur | Création INDEX |

---

**Questions ?** Consulter PROD-VALID-001 ou PROD-VALID-002 selon le domaine.

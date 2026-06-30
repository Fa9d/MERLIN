# IVIA — Carte d'état du schéma PostgreSQL
**Généré le :** 29 juin 2026  
**Dépôt :** `Fa9d/ivia`  
**Source :** `backend/app/models.py` + 7 migrations Alembic  

---

## 🔴 ALERTE CRITIQUE — Conflit de migration à résoudre EN PREMIER

La chaîne Alembic a **deux têtes de branche non mergées** :

```
98fd6709  (ROOT — initial)
    └── b534280a  (vibrational fields)
         └── ab6a6399  (care_cards)
              ├── bb9f7802  (transcript fields)
              │    └── f3d5702f  (practitioner tables)
              │         └── e1f2a3b4  ← TÊTE 1 (market intelligence)
              │
              └── c1a2b3d4  ← TÊTE 2 (profil_vivant tables)
```

**Conséquence :** `alembic upgrade head` échoue ou se comporte de façon imprévisible.  
**Action requise AVANT tout nouveau développement :**

```bash
# Claude Code doit créer une migration de merge :
alembic merge -m "merge_market_and_profil_vivant" e1f2a3b4c5d6 c1a2b3d4e5f6
```

Cela crée une migration vide avec `down_revision = ('e1f2a3b4c5d6', 'c1a2b3d4e5f6')` qui réconcilie les deux branches. Toutes les nouvelles migrations partent ensuite de ce merge point.

---

## Tables existantes — état complet

### 1. `members`
Classe : `Member`  
Migration créatrice : `98fd6709` (initial)

| Colonne | Type | Notes |
|---|---|---|
| id | String | PK |
| created_at | DateTime(tz) | auto |
| updated_at | DateTime(tz) | auto |
| first_name | String | required |
| last_name | String | required |
| email | String | unique, indexed |
| phone | String | nullable |
| referral | String | nullable |
| status | Enum(ACTIVE/INACTIVE) | default ACTIVE |

Relation : → `sessions` (1-N)

---

### 2. `sessions`
Classe : `Session`  
Migrations : `98fd6709` (base) + `b534280a` (vibrational) + `bb9f7802` (transcript)

| Colonne | Type | Notes |
|---|---|---|
| id | String | PK |
| created_at | DateTime(tz) | auto |
| updated_at | DateTime(tz) | auto |
| member_id | String | FK → members.id |
| date | DateTime(tz) | required |
| type | Enum(INTAKE/FOLLOW_UP) | default INTAKE |
| notes | String | nullable |
| stress_score | Integer | nullable |
| pain_score | Integer | nullable |
| sleep_score | Integer | nullable |
| harmony_score | Integer | nullable |
| vibrational_score | Integer | nullable, indexed |
| vibrational_label | String | nullable, indexed |
| vibrational_analysis | JSON | nullable |
| transcript_id | String | nullable, indexed |
| audio_ref | String | nullable |

⚠️ **Zone de conflit potentiel** : les champs `big_five_client` et `big_five_praticien` (du brief comportemental) doivent être ajoutés ici via une nouvelle migration — après le merge des branches.

---

### 3. `care_cards`
Classe : `CareCard`  
Migration : `ab6a6399`

| Colonne | Type | Notes |
|---|---|---|
| id | Integer | PK |
| session_id | String | FK → sessions.id, unique |
| title | String | — |
| summary | String | — |
| details | Text | — |
| created_at | DateTime(tz) | auto |

---

### 4. `practitioners`
Classe : `Practitioner`  
Migration : `f3d5702f`

| Colonne | Type | Notes |
|---|---|---|
| id | String | PK, indexed |
| name | String | — |
| email | String | unique, indexed |
| is_active | Boolean | — |
| plan | String | — |
| created_at | DateTime(tz) | auto |
| updated_at | DateTime(tz) | auto |

⚠️ **Zone de conflit potentiel** : le profil comportemental praticien (Big Five, Schwartz, LEARY) sera stocké dans la nouvelle table `profil_comportemental` avec FK vers `practitioners.id` — ne pas ajouter de colonnes directement ici.

---

### 5. `practitioner_applications`
Classe : `PractitionerApplication`  
Migration : `f3d5702f`

| Colonne | Type | Notes |
|---|---|---|
| id | String | PK |
| practitioner_name | String | — |
| practitioner_email | String | — |
| practice_types | Text | — |
| experience_years | Integer | — |
| status | String | — |
| created_at / updated_at | DateTime(tz) | auto |

---

### 6. `practitioner_subscriptions`
Classe : `PractitionerSubscription`  
Migration : `f3d5702f`

| Colonne | Type | Notes |
|---|---|---|
| id | String | PK |
| practitioner_id | String | FK → practitioners.id |
| plan | String | — |
| start_date / end_date | DateTime(tz) | — |
| is_active | Boolean | — |

---

### 7. `practitioner_commissions`
Classe : `PractitionerCommission`  
Migration : `f3d5702f`

| Colonne | Type | Notes |
|---|---|---|
| id | String | PK |
| practitioner_id | String | FK → practitioners.id |
| month | String(7) | format YYYY-MM |
| gross_amount | Integer | centimes |
| commission_amount | Integer | centimes |
| net_amount | Integer | centimes |

---

### 8. `practitioner_appointments`
Classe : `PractitionerAppointment`  
Migration : `f3d5702f`

| Colonne | Type | Notes |
|---|---|---|
| id | String | PK |
| practitioner_id | String | FK → practitioners.id |
| member_id | String | FK → members.id |
| start_time / end_time | DateTime(tz) | — |
| price | Integer | centimes |
| status | String | — |
| created_at / updated_at | DateTime(tz) | auto |

---

### 9. `profils_vivants`
Classe : `ProfilVivant`  
Migration : `c1a2b3d4` ← **branche non mergée**

| Colonne | Type | Notes |
|---|---|---|
| id | String | PK |
| member_id | String | FK → members.id, unique |
| objectifs | JSON | — |
| created_at / updated_at | DateTime(tz) | auto |

Relations → `contextes_vie`, `axe_observations`, `notes_vibratoires`, `hypotheses_travail`, `symptome_observations`, `care_cards_vivantes`

---

### 10. `contextes_vie`
Classe : `ContexteVie`  
Migration : `c1a2b3d4`

| Colonne | Type | Notes |
|---|---|---|
| id | String | PK |
| profil_id | String | FK → profils_vivants.id, unique |
| environnement, climat, culture, moyens | String | — |
| contraintes, ressources, appuis | JSON | — |
| date_observation | DateTime(tz) | — |

---

### 11. `axe_observations`
Classe : `AxeObservation`  
Migration : `c1a2b3d4`

| Colonne | Type | Notes |
|---|---|---|
| id | String | PK |
| profil_id | String | FK → profils_vivants.id |
| axe | String | indexed |
| valeur | Integer | — |
| label | String | — |
| commentaire | Text | — |
| date_observation | DateTime(tz) | — |

---

### 12. `notes_vibratoires`
Classe : `NoteVibratoireRecord`  
Migration : `c1a2b3d4`

| Colonne | Type | Notes |
|---|---|---|
| id | String | PK |
| profil_id | String | FK → profils_vivants.id |
| session_id | String | FK → sessions.id |
| score | Integer | — |
| label | String | — |
| analyse | Text | — |
| created_at | DateTime(tz) | auto |

---

### 13. `hypotheses_travail`
Classe : `HypotheseTravail`  
Migration : `c1a2b3d4`

| Colonne | Type | Notes |
|---|---|---|
| id | String | PK |
| profil_id | String | FK → profils_vivants.id |
| version, titre | String | — |
| description | Text | — |
| source, niveau_confiance, statut | String | — |
| domaines | JSON | — |
| created_at / updated_at | DateTime(tz) | auto |

---

### 14. `symptome_observations`
Classe : `SymptomeObservation`  
Migration : `c1a2b3d4`

| Colonne | Type | Notes |
|---|---|---|
| id | String | PK |
| profil_id | String | FK → profils_vivants.id |
| description, type | String | — |
| axes_concernes | JSON | — |
| contexte_apparition, perception_personne | Text | — |
| intensite | Integer | — |
| date_observation | DateTime(tz) | — |

---

### 15. `care_cards_vivantes`
Classe : `CareCardVivante`  
Migration : `c1a2b3d4`

| Colonne | Type | Notes |
|---|---|---|
| id | String | PK |
| profil_id | String | FK → profils_vivants.id |
| session_id | String | FK → sessions.id |
| points, ressources | JSON | — |
| resume | Text | — |
| created_at | DateTime(tz) | auto |

---

### 16. `competitive_centers`
Classe : `CompetitiveCenter`  
Migration : `e1f2a3b4` ← **branche non mergée**

| Colonne | Type | Notes |
|---|---|---|
| id | String | PK |
| name | String | — |
| addresses, semantic_registry, strengths, weaknesses | JSON | — |
| status | String | — |
| notes | Text | — |
| created_at / updated_at | DateTime(tz) | auto |

---

### 17. `market_practitioners`
Classe : `MarketPractitioner`  
Migration : `e1f2a3b4`

| Colonne | Type | Notes |
|---|---|---|
| id | String | PK |
| name, specialties, location, email, phone | String/JSON | — |
| contact_status, tv_level | String | — |
| center_id | String | FK → competitive_centers.id |
| notes | Text | — |
| created_at / updated_at | DateTime(tz) | auto |

---

### 18. `market_keywords`
Classe : `MarketKeyword`  
Migration : `e1f2a3b4`

| Colonne | Type | Notes |
|---|---|---|
| id | String | PK |
| keyword, category | String | — |
| volume, difficulty | Integer | — |
| intent | String | — |
| created_at | DateTime(tz) | auto |

---

## Nouvelles tables à créer (module comportemental)

> À ajouter **après** la migration de merge. Aucune de ces tables n'existe encore.

| Table | Propriétaire | Conflits potentiels |
|---|---|---|
| `profil_comportemental` | Module matching | Aucun — nouvelle table |
| `matching_scores` | Module matching | Aucun — nouvelle table |
| `veille_configs` | Module veille | Aucun — nouvelle table |
| `veille_digests` | Module veille | Aucun — nouvelle table |

---

## Champs à ajouter à des tables existantes

| Table | Champs à ajouter | Migration requise | Conflits potentiels |
|---|---|---|---|
| `sessions` | `big_five_client` (JSON), `big_five_praticien` (JSON) | Nouvelle migration post-merge | Aucun — champs inexistants |

---

## Routers existants — carte des endpoints

| Fichier | Préfixe | Propriétaire fonctionnel |
|---|---|---|
| `routers/auth.py` | `/auth` | Authentification |
| `routers/sessions.py` | `/sessions` | Séances |
| `routers/members.py` | `/members` | Membres/clients |
| `routers/practitioners.py` | `/practitioners` | Praticiens |
| `routers/market.py` | `/market` | Intelligence marché |
| `routers/protocole_vie.py` | `/profil` | Profil vivant |

**Nouveaux routers à créer (sans conflits de préfixe) :**
- `routers/matching.py` → `/matching`
- `routers/veille.py` → `/veille`

---

## Résumé des actions pour Claude Code

```
ÉTAPE 0 (obligatoire) :
  alembic merge -m "merge_market_and_profil_vivant" e1f2a3b4c5d6 c1a2b3d4e5f6

ÉTAPE 1 : Nouvelle migration post-merge
  → Crée tables : profil_comportemental, matching_scores
  → Ajoute champs sessions : big_five_client, big_five_praticien

ÉTAPE 2 : Module matching
  → backend/app/core/matching.py
  → backend/app/routers/matching.py
  (préfixe /matching — aucun conflit)

ÉTAPE 3 : Module Big Five NLP
  → Extension de backend/app/analyse.py
  (ne pas créer un nouveau fichier)

ÉTAPE 4 : Composants frontend
  → frontend/components/RadarProfile.tsx      (nouveau)
  → frontend/components/TernaryPlot.tsx       (nouveau)
  → frontend/components/LearyCircumplex.tsx   (nouveau)
  → frontend/pages/admin/seance.tsx           (modifier existant)
  → frontend/pages/practitioners/dashboard.tsx (modifier existant)

ÉTAPE 5 : Module veille
  → Nouvelle migration : veille_configs, veille_digests
  → backend/app/core/veille.py
  → backend/app/routers/veille.py
  → frontend/pages/admin/veille.tsx           (nouveau)
```

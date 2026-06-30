# Brief Claude Code — Implémentation des modèles comportementaux MERLIN

## Contexte du projet

Plateforme IVIA / MERLIN — outil d'écoute empathique pour praticiens et clients en santé alternative.

**Stack confirmée :**
- Backend : FastAPI (Python), PostgreSQL, SQLAlchemy, Alembic
- Frontend : Next.js / React / TypeScript (pages router)
- Audio : Deepgram + Whisper (transcriptions déjà actives)
- Infrastructure : Docker, OVH VPS
- Dépôt principal : `Fa9d/ivia` (backend + frontend)
- Dépôt doctrine : `Fa9d/MERLIN`

**Structure backend existante :**
- `backend/app/models.py` — modèles SQLAlchemy
- `backend/app/routers/` — sessions, practitioners, members, auth, market
- `backend/alembic/versions/` — migrations existantes
- `backend/app/analyse.py` — pipeline d'analyse existant
- `backend/app/core/vibrational.py` — module d'analyse vibratoire existant

**Structure frontend existante :**
- `frontend/pages/admin/` — pages admin (index, seance, practitioners, market)
- `frontend/components/` — composants (ex. CareCardView.tsx)

---

## Spécification complète

Voir le document de référence : `MERLIN_modeles_comportementaux_v1.md`

Résumé des éléments clés :
- 20 modèles comportementaux classifiés avec Indice de Pertinence MERLIN (IPM /15)
- Logique d'attribution par Score d'Opportunité (SO)
- Formule de rentabilité ROI_action par modèle
- Système de veille admin (10 domaines, OFF par défaut, toggle par clic)

---

## Modules à implémenter — dans cet ordre

### MODULE 1 — Matching vectoriel praticien-client (P1 — IPM 12)

**Objectif :** Calculer la compatibilité entre un profil praticien et un profil client via similarité cosinus sur vecteurs de valeurs/traits.

**Backend à créer :**

1. **Nouveau modèle SQLAlchemy** (`models.py`) :
   - Table `profil_comportemental` : `id`, `user_id`, `user_type` (praticien/client), `big_five` (JSONB), `schwartz_values` (JSONB), `leary_axes` (JSONB), `ternary_plot` (JSONB), `created_at`, `updated_at`
   - Table `matching_scores` : `id`, `praticien_id`, `client_id`, `score_cosine` (float), `score_opportunite` (float), `modeles_actifs` (JSONB), `created_at`

2. **Nouvelle migration Alembic** pour ces deux tables

3. **Nouveau router** `backend/app/routers/matching.py` :
   - `POST /matching/profil` — enregistrer ou mettre à jour un profil comportemental
   - `GET /matching/praticiens/{client_id}` — retourner les praticiens classés par score cosinus descendant
   - `GET /matching/score/{praticien_id}/{client_id}` — score détaillé entre deux profils
   - `POST /matching/recalcul` — recalculer tous les scores (tâche admin)

4. **Module de calcul** `backend/app/core/matching.py` :
   ```python
   # Logique à implémenter :
   # - Normalisation des vecteurs (Big Five + Schwartz + LEARY → vecteur unifié)
   # - Cosine similarity via numpy
   # - Score d'Opportunité : SO = IPM × disponibilité_données × alignement_praticien
   # - Seuil d'activation SO ≥ 8.0
   ```

**Frontend à créer :**

5. **Composant** `frontend/components/MatchingScore.tsx` — affiche le score de compatibilité avec breakdown par dimension
6. **Page admin** enrichie `frontend/pages/admin/matching.tsx` — liste des paires praticien-client avec scores, filtrable

---

### MODULE 2 — Big Five via NLP sur transcriptions (P1 — IPM 11)

**Objectif :** Après chaque séance transcrite, extraire les traits Big Five (OCEAN) du discours du client et du praticien via un appel LLM structuré.

**Backend à créer :**

1. **Fonction d'analyse** dans `backend/app/analyse.py` (étendre l'existant) :
   - `async def extract_big_five(transcript: str, speaker: str) -> dict` 
   - Appel LLM (Anthropic Claude API) avec prompt structuré retournant JSON `{O, C, E, A, N}` scores 0.0–1.0
   - Prompt doit être non-prescriptif, basé sur les patterns linguistiques, pas sur le contenu clinique

2. **Mise à jour du modèle Session** — ajouter champ `big_five_client` (JSONB) et `big_five_praticien` (JSONB)

3. **Nouvelle migration Alembic** pour ces champs

4. **Intégration dans le router sessions** — déclencher `extract_big_five` après transcription complète (post-processing async)

5. **Mise à jour automatique** du `profil_comportemental` du client après chaque séance

**Prompt à utiliser (intégrer dans le code) :**
```
Analyse le texte suivant et évalue les 5 grands traits de personnalité (Big Five / OCEAN) 
de la personne qui parle, uniquement sur la base de ses patterns linguistiques et 
de ses modes d'expression — jamais sur le contenu clinique ou personnel.

Retourne un JSON strict : {"O": 0.0-1.0, "C": 0.0-1.0, "E": 0.0-1.0, "A": 0.0-1.0, "N": 0.0-1.0}

O = Ouverture (curiosité, créativité, flexibilité mentale)
C = Conscienciosité (organisation, rigueur, persévérance)  
E = Extraversion (sociabilité, énergie, assertivité)
A = Agréabilité (empathie, coopération, bienveillance)
N = Névrosisme (instabilité émotionnelle, anxiété, réactivité)

Texte : {transcript}
```

---

### MODULE 3 — Visualisations (Ternary Plot + Radar Chart) (P1 — IPM 14)

**Objectif :** Visualiser les profils comportementaux dans l'interface praticien et admin.

**Dépendances à installer :**
```bash
npm install recharts  # ou d3 selon préférence
```

**Composants frontend à créer :**

1. **`frontend/components/RadarProfile.tsx`**
   - Radar/Spider Chart à 8 axes : O, C, E, A, N (Big Five) + Autonomie, Lien, Structure (3 valeurs IVIA custom)
   - Props : `profil: ProfilComportemental`, `showLabels: boolean`, `compareWith?: ProfilComportemental`
   - Deux profils superposables (praticien vs client) pour visualiser la compatibilité

2. **`frontend/components/TernaryPlot.tsx`**
   - Triangle équilatéral SVG custom
   - 3 axes : **Autonomie** (indépendance, autodétermination) / **Lien** (appartenance, communauté, relation) / **Structure** (cadre, sécurité, organisation)
   - Point du client positionné selon ses scores normalisés (somme = 100%)
   - Zones colorées : centre = équilibre, angles = dominance d'une valeur

3. **`frontend/components/LearyCircumplex.tsx`**
   - Rosace circulaire SVG à 8 octants (axe Dominance–Soumission × Amour–Hostilité)
   - Point praticien + point client sur le même cercle
   - Flèche de complémentarité entre les deux points

4. **Intégration dans les pages existantes :**
   - `frontend/pages/admin/seance.tsx` — ajouter onglet "Profil comportemental" avec les 3 visualisations
   - `frontend/pages/practitioners/dashboard.tsx` — ajouter section "Mon profil" avec RadarProfile

---

### MODULE 4 — Système de veille admin (P2)

**Objectif :** Interface admin pour activer/désactiver des veilles thématiques, avec digest stocké en base.

**Backend à créer :**

1. **Table** `veille_configs` : `id`, `domaine`, `actif` (bool, default false), `frequence` (enum: daily/weekly/monthly), `dernier_run`, `seuil_pertinence` (int, default 7)
2. **Table** `veille_digests` : `id`, `domaine`, `date_run`, `items` (JSONB array), `nb_items_retenus`
3. **Router** `backend/app/routers/veille.py` :
   - `GET /veille/config` — liste des domaines avec état ON/OFF
   - `PATCH /veille/config/{domaine}` — toggle actif + modifier fréquence
   - `GET /veille/digests` — derniers digests par domaine
   - `POST /veille/run/{domaine}` — lancer manuellement une veille
4. **Module** `backend/app/core/veille.py` :
   - Appel Perplexity API par domaine (requêtes préconfigurées par domaine)
   - Scoring de pertinence MERLIN (0-10) via LLM
   - Stockage digest en base

**Frontend à créer :**

5. **Page** `frontend/pages/admin/veille.tsx` :
   - Grille des 10 domaines avec toggle switch ON/OFF
   - Sélecteur de fréquence par domaine
   - Bouton "Lancer maintenant" par domaine
   - Affichage du dernier digest (liste d'items avec score de pertinence + lien)

**10 domaines de veille avec requêtes préconfigurées :**
```python
VEILLE_DOMAINS = {
    "psychometrie_computationnelle": "Big Five OCEAN personality detection NLP LLM 2025 2026",
    "digital_phenotyping": "digital phenotyping behavioral markers mental health smartphone 2025",
    "jitai_mobile_health": "JITAI just-in-time adaptive intervention mobile health 2025",
    "llm_clinique": "LLM GPT clinical psychiatric longitudinal analysis 2025 2026",
    "matching_recommandation": "practitioner client matching recommendation algorithm behavioral 2025",
    "concurrents_holistes": "holistic health platform alternative practitioner app 2025 2026",
    "reglementation_qc": "Loi 25 Quebec RGPD données santé numérique réglementation 2026",
    "financement_qc": "financement santé numérique CALQ CDPQ Innovitech Quebec 2026",
    "savoirs_autochtones": "savoirs autochtones wellness santé holistique research 2025 2026",
    "gut_brain_axis": "gut brain axis microbiome mental health neuroscience 2025 2026",
}
```

---

## Calcul de rentabilité — à intégrer dans l'admin existant

**Ajouter dans le dashboard admin existant** (`frontend/pages/admin/index.tsx`) :

Section "Rentabilité des modèles" avec pour chaque modèle actif :
- Coût estimé par séance (CR)
- Nombre de séances où le modèle a été appliqué
- Coût total du modèle ce mois
- Revenu attribuable (proxy : rétention × LTV estimée)
- ROI affiché comme ratio simple

**Formule à implémenter :**
```python
def roi_action(vm, cp_net, cc_net, cr, cim_amorti):
    benefice_net = vm + cp_net + cc_net - cr - cim_amorti
    cout_total = cr + cim_amorti
    return benefice_net / cout_total if cout_total > 0 else 0

# Coûts par modèle ($/séance) :
COUTS_MODELES = {
    "prosodie_vocale": 0.08,      # Deepgram
    "big_five_nlp": 0.12,         # LLM call
    "leary_circumplex": 0.05,     # calcul local
    "matching_vectoriel": 0.02,   # calcul local
    "schwartz_ternary": 0.02,     # calcul local
    "jitai": 0.25,                # multi-appels
}
```

---

## Contraintes importantes à respecter

1. **Non-prescriptif** — aucun modèle ne produit de diagnostic médical ni recommandation de traitement
2. **Effacement biométrique** — données vocales effacées à J+30 (déjà en place, ne pas casser)
3. **Hébergement Québec** — aucune donnée ne quitte OVH CA
4. **Consentement** — chaque analyse comportementale est couverte par le consentement général de séance
5. **XAI** — chaque score doit être accompagné d'une explication simple visible par le praticien
6. **Posture culturelle** — les savoirs autochtones sont des cadres de référence, pas des variables calculables

---

## Ordre d'exécution recommandé

1. Migration Alembic : tables `profil_comportemental` + `matching_scores`
2. Module `backend/app/core/matching.py` (calcul vectoriel)
3. Router `backend/app/routers/matching.py`
4. Fonction `extract_big_five` dans `backend/app/analyse.py`
5. Migration Alembic : champs `big_five_*` dans sessions
6. Composants frontend : `RadarProfile.tsx`, `TernaryPlot.tsx`, `LearyCircumplex.tsx`
7. Intégration dans `admin/seance.tsx` et `practitioners/dashboard.tsx`
8. Tables veille + router + module `veille.py`
9. Page `admin/veille.tsx`
10. Section rentabilité dans `admin/index.tsx`

---

## Document de référence complet

Le document `MERLIN_modeles_comportementaux_v1.md` contient la classification complète des 20 modèles, les formules détaillées, et la roadmap par strate. S'y référer pour toute décision d'arbitrage.

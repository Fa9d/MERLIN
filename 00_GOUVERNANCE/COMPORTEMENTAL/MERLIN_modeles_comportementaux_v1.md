> ⚠️ **DOCUMENT D'INTENTION (matière), pas un plan d'implémentation.** Rédigé par
> Perplexity sur la branche `master` (état périmé, head 0017). Pour toute implémentation,
> la **référence factuelle** est `SCHEMA_ETAT_REEL.md` (réécrit sur `refonte`, head **0039**).
> Règle dure : **le module comportemental EXISTE DÉJÀ** (`app/models/behavioral_profile.py`
> 5 couches, `services/profile_matching.py`, `behavioral_insights.py`, `<ivia-profile-radar>`)
> derrière une **barrière safety/sécurité B1–B4** + `profiling_safety_suite_v1`. On **étend**
> l'existant, on ne le **duplique pas**. Pas de table `profil_comportemental` parallèle.

---

# MERLIN — Modèles comportementaux & système d'attribution
**Version** : 1.0 — 29 juin 2026  
**Auteur** : David Phaneuf / IVIA.quebec  
**Portée** : Classification complète des méthodes d'analyse comportementale, système de veille admin, indices de valeur, attribution et calcul de rentabilité par action.

---

## 0. Rappel d'architecture

| Composant | Rôle | Interface |
|---|---|---|
| **IVIA.quebec** | Maison commune / accueil | Publique + portail |
| **MERLIN** | Moteur analytique & structurant | Admin + praticien |
| **MÉSANGES** | Interface vocale / relationnelle | Praticien + client |

> *IVIA accueille. MERLIN structure. MÉSANGES accompagne.*

Les modèles comportementaux sont des **modules optionnels** de MERLIN — activables par l'admin, configurables par le praticien, invisibles au client sauf via effets (matching, recommandations, rapport).

---

## 1. Carte complète des modèles comportementaux

### 1.1 Fondements établis

| Modèle | Structure | Dimensions | Applicabilité MERLIN |
|---|---|---|---|
| **Three Telos / Ternary Plot** | Triangle | Liberté, Égalité, Tradition (somme = 100%) | ✓ **Adaptable en 3 valeurs personnalisées** |
| **Big Five / OCEAN** | 5 traits continus | O, C, E, A, N | ✓✓ **Référence empirique principale** |
| **HEXACO** | 6 traits continus | + Honnêteté-Humilité | ✓ Extension Big Five |
| **Enneagramme** | 9 types + ailes | Structure motivationnelle | ✓ Pertinent en approche holiste |
| **Jungien (types)** | 8 fonctions/attitudes | Introversion, Ombre, Anima, etc. | ✓✓ **Déjà ancré dans IVIA** |
| **Schwartz Values** | Cercle (circumplex) | 10 valeurs universelles, 2 axes bipolaires | ✓✓ **Compatibilité directe avec LEARY** |
| **Moral Foundations Theory (MFT)** | Vecteur 6D | Care, Fairness, Loyalty, Authority, Sanctity, Liberty | ✓ Éthique, gouvernance, XAI |
| **Inglehart-Welzel** | Carré 2D | Traditionnel-Laïc × Survie-Épanouissement | ✓ Ancrage culturel / Québec |

### 1.2 Modèle LEARY / Circumplex (déjà référencé dans la doctrine IVIA)

Modèle interpersonnel de Timothy Leary (1957). Deux axes : **Dominance–Soumission** (vertical) et **Amour–Hostilité** (horizontal). Rosace de 8 à 16 octants.

| Composante | Description |
|---|---|
| Axe vertical | Dominance (contrôle) ↔ Soumission (abandon) |
| Axe horizontal | Amour (affiliation) ↔ Hostilité (séparation) |
| Circumplex | Positions intermédiaires : Leader, Soutien, Dépendance, Critique, etc. |
| Complémentarité | Les comportements interpersonnels s'invoquent mutuellement (pull principle) |
| Application MERLIN | Analyse du registre interpersonnel praticien ↔ client ; détection des dynamiques de transfert |

### 1.3 Modèles géométriques avancés

| Représentation | Forme | Idéal pour | Notes MERLIN |
|---|---|---|---|
| **Ternary Plot** | Triangle | 3 valeurs en tension (somme = 100%) | Profil de besoins client : Autonomie / Lien / Structure |
| **Radar / Spider Chart** | Polygone N-axes | N traits simultanés | Profil praticien complet |
| **Circumplex de Leary** | Rosace | Relations interpersonnelles | Analyse des dynamiques de séance |
| **Heatmap temporelle** | Grille 2D | Évolution dans le temps | Suivi longitudinal client |
| **Cluster plot (t-SNE / UMAP)** | Nuage de points | Groupes de profils similaires | Matching et segmentation |

### 1.4 Modèles computationnels émergents (2022–2026)

| Méthode | Description | Applicabilité |
|---|---|---|
| **Big Five via texte (NLP)** | Détection des traits depuis langage naturel | ✓✓ Intégrable pipeline MERLIN — `session_notes` |
| **MFT via NLP** | Moral Foundations Theory sur analyse de discours | ✓ Gouvernance & valeurs |
| **JITAI** | Interventions adaptatives en temps réel (mobile health) | ◑ Strate 3 — suivi continu |
| **Cosine similarity** | Mesure de similarité entre vecteurs de profils | ✓✓ Extension du `matching.py` existant |
| **Clustering K-means** | Groupes discrets de profils | ✓ Segmentation clients |

---

## 2. Classification avec Indice de Pertinence MERLIN (IPM /15)

### Critères de notation (0–3 par critère)

| Critère | Description |
|---|---|
| **V** — Validité scientifique | Niveau de consensus empirique |
| **A** — Applicabilité MERLIN | Cohérence avec stack et flux de données existants |
| **C** — Coût d'implémentation | Inverse du coût (3 = peu coûteux) |
| **I** — Impact praticien | Valeur perçue par le praticien |
| **U** — Utilité client | Bénéfice direct sur l'accompagnement |

### Table de classification

| # | Méthode | V | A | C | I | U | **IPM /15** | Priorité |
|---|---|---|---|---|---|---|---|---|
| 1 | **Big Five / OCEAN** | 3 | 3 | 2 | 3 | 2 | **13** | 🔴 P1 |
| 2 | **LEARY / Circumplex** | 3 | 3 | 2 | 3 | 2 | **13** | 🔴 P1 |
| 3 | **Prosodie vocale (audio_recordings)** | 3 | 3 | 3 | 3 | 1 | **13** | 🔴 P1 |
| 4 | **Schwartz Values** | 3 | 3 | 2 | 2 | 2 | **12** | 🔴 P1 |
| 5 | **Matching vectoriel (extension matching.py)** | 2 | 3 | 2 | 3 | 2 | **12** | 🔴 P1 |
| 6 | **Ternary Plot (3 valeurs custom)** | 2 | 3 | 3 | 3 | 3 | **14** | 🔴 P1 |
| 7 | **Radar / Spider Chart** | 2 | 3 | 3 | 3 | 3 | **14** | 🔴 P1 |
| 8 | **Heatmap temporelle** | 2 | 3 | 3 | 2 | 2 | **12** | 🔴 P1 |
| 9 | **Jungien (types)** | 2 | 3 | 2 | 3 | 3 | **13** | 🔴 P1 |
| 10 | **Enneagramme** | 1 | 3 | 3 | 3 | 3 | **13** | 🔴 P1 |
| 11 | **NLP Big Five detection** | 3 | 3 | 2 | 2 | 1 | **11** | 🟠 P2 |
| 12 | **Moral Foundations Theory** | 3 | 2 | 2 | 2 | 1 | **10** | 🟠 P2 |
| 13 | **MBTI** | 1 | 2 | 3 | 3 | 3 | **12** | 🟠 P2 — faible validité |
| 14 | **JITAI** | 3 | 2 | 1 | 2 | 3 | **11** | 🟠 P2 — Strate 3 |
| 15 | **HEXACO** | 3 | 2 | 2 | 1 | 1 | **9** | 🟡 P3 |
| 16 | **Inglehart-Welzel** | 3 | 2 | 1 | 1 | 1 | **8** | 🟡 P3 |
| 17 | **Digital Phenotyping complet** | 3 | 1 | 0 | 1 | 2 | **7** | 🟢 P4 — Futur |

**Légende :** 🔴 P1 = immédiat | 🟠 P2 = prochaine itération | 🟡 P3 = optionnel | 🟢 P4 = roadmap futur

---

## 3. Carte des vues par interface

### Interface Praticien (`/dashboard` ou équivalent praticien)
| Vue | Contenu | Déclencheur |
|---|---|---|
| Mon profil comportemental | Radar 8 axes (Big Five + 3 valeurs IVIA) | À l'inscription / onboarding |
| Position LEARY | Circumplex — sa position interpersonnelle | Calculé après 3 séances |
| Mes clients — compatibilité | Liste avec score de matching étendu | Automatique |

### Interface Séance (session_notes + derived_documents)
| Vue | Contenu | Déclencheur |
|---|---|---|
| Profil client (session) | Ternary Plot (Autonomie/Lien/Structure) | Post-analyse session_note |
| Dynamique interpersonnelle | LEARY praticien + client superposés | Post-analyse session_note |
| Évolution Big Five | Heatmap temporelle — delta séance par séance | Dès 2e séance |

### Interface Admin
| Vue | Contenu | Déclencheur |
|---|---|---|
| Rentabilité par modèle | ROI par modèle actif ce mois | Temps réel |
| Veille thématique | Digests par domaine, toggle ON/OFF, OFF par défaut | Manuel |
| Matching global | Carte des paires praticien-client | Automatique |

---

## 4. Système de veille admin

### Principes
- **Non-activée par défaut** — chaque module est `OFF` au déploiement
- Activation par clic unique depuis le tableau de bord admin
- 10 domaines configurables indépendamment

### Domaines de veille

| # | Domaine | Fréquence recommandée |
|---|---|---|
| 1 | Psychométrie computationnelle | Hebdomadaire |
| 2 | Digital phenotyping | Hebdomadaire |
| 3 | JITAI & mobile health | Mensuelle |
| 4 | LLMs en contexte clinique | Hebdomadaire |
| 5 | Matching & recommandation | Mensuelle |
| 6 | Concurrents (plateformes holistes) | Mensuelle |
| 7 | Réglementation (Loi 25 QC, LPRPDE) | Mensuelle |
| 8 | Financement (CALQ, CLD, Innovitech) | Mensuelle |
| 9 | Savoirs autochtones & wellness | Mensuelle |
| 10 | Neurosciences & axe gut-brain | Mensuelle |

### Architecture technique

```
Admin Dashboard
  └─ Module Veille [toggle ON/OFF par domaine]
       ├─ Cron job (cadence configurable)
       ├─ Perplexity API → recherche structurée par domaine
       ├─ Filtrage LLM → score pertinence MERLIN (0-10)
       ├─ Digest stocké → PostgreSQL (nouvelles tables)
       └─ Notification admin → email / in-app si score > seuil
```

---

## 5. Attribution des modèles — Score d'Opportunité (SO)

```
SO = IPM × Disponibilité_données × Alignement_praticien

Disponibilité = [0.0 – 1.0] selon complétude des données disponibles
Alignement    = [0.0 – 1.0] selon paramètres du praticien
Seuil d'activation = SO ≥ 8.0
```

### Données disponibles dans MERLIN (mapping)

| Source de données | Tables MERLIN | Modèles déclenchables |
|---|---|---|
| Transcription + notes | `session_notes`, `derived_documents` | Big Five NLP, LEARY, MFT |
| Audio brut | `audio_recordings` | Prosodie vocale |
| Profil praticien | `practitioner_profiles` + champs match | Matching vectoriel étendu |
| Historique séances | `sessions`, `session_temporal_anchors` | Heatmap temporelle, JITAI |
| Événements de vie | `client_life_events`, `client_journal_entries` | Jungien, Enneagramme |
| Intake request | `intake_requests` | Schwartz Values, Ternary Plot |

---

## 6. Évaluation de la rentabilité

### Formule ROI par action

```
ROI_action = (VM + CP_net + CC_net - CR - CIM_amorti) / (CR + CIM_amorti)

VM         = Valeur modèle (proxy : rétention × LTV)
CP_net     = Contribution praticien attribuable à la fonctionnalité
CC_net     = Contribution client attribuable
CR         = Coût ressource (API, calcul) par séance
CIM_amorti = Coût développement / nb séances utilisées
```

### Coûts et seuils estimés

| Modèle | CR/séance | Seuil rentabilité | Statut |
|---|---|---|---|
| Prosodie vocale | 0.08$ | 1 séance | ✓ J1 |
| Big Five NLP | 0.12$ (Anthropic haiku) | 3 séances | ✓ |
| LEARY Circumplex | 0.05$ (calcul local) | 1 séance | ✓ J1 |
| Matching vectoriel étendu | 0.02$ (calcul local) | 1 match | ✓ J1 |
| Schwartz + Ternary | 0.02$ (calcul local) | 2 séances | ✓ |
| JITAI adaptatif | 0.25$ | 8 séances | ◑ Strate 3 |

---

## 7. Roadmap d'intégration par strate

### Strate 1 — Fondation (immédiate)
- [ ] Extension `matching.py` — cosine similarity sur vecteurs Big Five + valeurs
- [ ] Champ `big_five_scores` (JSON) dans `session_notes` ou nouvelle table `profil_comportemental`
- [ ] Extraction Big Five depuis `session_notes.observations_text` via pipeline Anthropic existant
- [ ] Prosodie vocale enrichie depuis `audio_recordings`
- [ ] Composants frontend : `RadarProfile`, `TernaryPlot`, `LearyCircumplex`
- [ ] Intégration dans la vue séance (onglet "Profil comportemental")
- [ ] Heatmap temporelle (évolution client)

### Strate 2 — Expansion
- [ ] Enneagramme et Jungien avancé (modules optionnels praticien)
- [ ] MFT — analyse éthique des échanges
- [ ] Module veille admin (10 domaines, tables `veille_configs` + `veille_digests`)
- [ ] Dashboard rentabilité par modèle
- [ ] Clustering clients (K-means sur profils)

### Strate 3 — Intelligence adaptative
- [ ] JITAI — interventions adaptatives
- [ ] Cognitive maps vectorielles
- [ ] LLM navigateur longitudinal sur `session_temporal_anchors`

---

## 8. Contraintes permanentes

| Principe | Application |
|---|---|
| **Non-prescriptif** | Aucun modèle ne produit de diagnostic médical — Observation / Hypothèse / Orientation uniquement |
| **Transparence (XAI)** | Chaque score est explicable au praticien (pas de boîte noire) |
| **Consentement granulaire** | Via table `consents` existante — consent_type_code à étendre |
| **Effacement biométrique** | Audio effacé à J+30 — règle déjà en place, ne pas casser |
| **Souveraineté des données** | Hébergement OVH VPS Québec uniquement |
| **Posture culturelle** | Savoirs autochtones = cadres de référence, non variables calculables |
| **MFT comme socle éthique** | Les 6 fondements moraux guident les choix de design et d'attribution |

---

*Document vivant — mis à jour à chaque cycle de veille ou itération de strate.*

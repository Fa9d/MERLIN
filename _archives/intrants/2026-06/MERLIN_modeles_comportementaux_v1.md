# MERLIN / IVIA — Modèles comportementaux & système d'attribution
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

### 1.1 Fondements établis (socle théorique validé)

#### A — Modèles de spectre politique / valeurs (origine, applicabilité déplacée vers le psychographique)

| Modèle | Structure | Dimensions | Applicabilité MERLIN |
|---|---|---|---|
| **Spectre linéaire G-D** | Axe unique 1D | Économique/social simplifié | ✗ Trop réducteur |
| **Nolan Chart** | Carré 2 axes | Liberté économique × Liberté personnelle | ◑ Valeurs, pas profil thérapeutique |
| **Political Compass** | Carré 2 axes | Gauche-Droite × Autoritaire-Libertaire | ◑ Référence LLM-biais uniquement |
| **Three Telos / Ternary Plot** | Triangle | Liberté, Égalité, Tradition (somme = 100%) | ✓ **Adaptable en 3 valeurs personnalisées** |
| **Vosem Chart** | Cube 3D | + Gouvernance, Info | ✗ Trop politique |
| **Inglehart-Welzel** | Carré 2D | Traditionnel-Laïc × Survie-Épanouissement | ✓ Pertinent pour ancrage culturel / Québec-Autochtone |

#### B — Modèles psychométriques de personnalité

| Modèle | Structure | Dimensions | Applicabilité MERLIN |
|---|---|---|---|
| **MBTI (Myers-Briggs)** | 16 types discrets | INTJ, ENFP, etc. | ◑ Populaire, faible reproductibilité scientifique |
| **Big Five / OCEAN** | 5 traits continus | O, C, E, A, N | ✓✓ **Référence empirique principale** |
| **HEXACO** | 6 traits continus | + Honnêteté-Humilité | ✓ Extension Big Five, pertinent éthique |
| **Enneagramme** | 9 types + ailes | Structure motivationnelle | ✓ Pertinent en approche holiste / Jungienne |
| **Jungien (types)** | 8 fonctions/attitudes | Introversion, Ombre, Anima, etc. | ✓✓ **Déjà ancré dans IVIA** |

#### C — Modèles de valeurs

| Modèle | Structure | Dimensions | Applicabilité MERLIN |
|---|---|---|---|
| **Schwartz Values** | Cercle (circumplex) | 10 valeurs universelles, 2 axes bipolaires | ✓✓ **Compatibilité directe avec LEARY/Le cercle** |
| **Moral Foundations Theory (MFT)** | Vecteur 6D | Care, Fairness, Loyalty, Authority, Sanctity, Liberty | ✓ Éthique, gouvernance, XAI |
| **World Values Survey (WVS)** | Carte 2D | Traditionnel-Laïc × Survie-Épanouissement | ✓ Ancrage socioculturel |

#### D — Modèle LEARY / Le Cercle (déjà intégré IVIA)

> Modèle interpersonnel de Timothy Leary (1957). Représente les comportements interpersonnels sur deux axes : **Dominance–Soumission** (vertical) et **Amour–Hostilité** (horizontal). Structure en rosace de 8 à 16 octants.

| Composante | Description |
|---|---|
| Axe vertical | Dominance (contrôle) ↔ Soumission (abandon) |
| Axe horizontal | Amour (affiliation) ↔ Hostilité (séparation) |
| Circumplex | Positions intermédiaires : Leader, Soutien, Dépendance, Critique, etc. |
| Complémentarité | Les comportements interpersonnels s'invoquent mutuellement (pull principle) |
| Application MERLIN | Analyse du registre interpersonnel praticien ↔ client ; détection des dynamiques de transfert |

---

### 1.2 Modèles géométriques avancés (visualisation multi-axes)

| Représentation | Forme | Idéal pour | Notes MERLIN |
|---|---|---|---|
| **Ternary Plot** | Triangle | 3 valeurs en tension (somme = 100%) | Profil de besoins client : Autonomie / Communauté / Structure |
| **Radar / Spider Chart** | Polygone N-axes | N traits simultanés | Profil praticien complet (Big Five + Schwartz + LEARY) |
| **Circumplex de Leary** | Rosace | Relations interpersonnelles | Analyse des dynamiques de séance |
| **Circumplex de Schwartz** | Cercle à secteurs | Tensions entre valeurs | Cartographie motivationnelle |
| **Heatmap temporelle** | Grille 2D | Évolution dans le temps | Suivi longitudinal d'un client |
| **Cluster plot (t-SNE / UMAP)** | Nuage de points | Groupes de profils similaires | Matching et segmentation |
| **Score composite 0-100** | Jauge / barre | Indice synthétique | Dashboard admin — ex. Delve Health |

---

### 1.3 Modèles computationnels émergents (2022–2026)

#### Digital Phenotyping
Quantification comportementale passive via données d'appareils.

| Marqueur | Source de données | Pertinence MERLIN |
|---|---|---|
| GPS / mobilité | Smartphone | ✗ Hors périmètre (non-collecté) |
| Actigraphie / sommeil | Wearable | ◑ Futur Strate 3+ |
| Usage app / durée écran | Téléphone | ✗ Hors périmètre |
| **Keystroke dynamics** | Clavier (app) | ✓ Possible dans saisie formulaires |
| **Patterns de communication** | Texte / voix | ✓✓ **Cœur de MÉSANGES** |
| **Prosodie vocale** | Audio séances | ✓✓ **Déjà via Deepgram + Whisper** |

> Marché : 1,5 Md$ (2024) → 3,8 Md$ (2034).

#### AI Psychometrics & NLP
| Méthode | Description | Applicabilité |
|---|---|---|
| **Big Five via texte** | Détection des traits depuis langage naturel (U. Barcelone, 2025) | ✓✓ Intégrable pipeline MERLIN |
| **MFT via NLP** | Moral Foundations Theory appliquée à l'analyse de discours | ✓ Gouvernance & valeurs |
| **LLM comme navigateur clinique** | GPT-4o → analyse longitudinale phénotypage psychiatrique (4× GPT-3.5) | ✓✓ Architecture MERLIN |
| **Cognitive Maps computationnelles** | Représentations vectorielles dynamiques (NeurIPS 2025) | ◑ Recherche frontier |
| **JITAI** | Interventions adaptatives en temps réel (mobile health) | ✓ Strate 3 — suivi continu |

#### Matching & Distance Vectorielle
| Méthode | Description | Applicabilité |
|---|---|---|
| **Spatial Voting Model** | Chaque enjeu = dimension ; distance entre points idéaux = compatibilité | ✓✓ Matching praticien-client |
| **Cosine similarity** | Mesure de similarité entre vecteurs de profils | ✓✓ Algorithme de matching |
| **Clustering K-means / DBSCAN** | Groupes discrets de profils | ✓ Segmentation clients |
| **Typologies à clusters** | Ex : Pew Research 9 groupes | ✓ Classification praticiens |

---

## 2. Classification complète avec indices de valeur

### 2.1 Grille de notation (por méthode)

Chaque méthode est évaluée sur 5 critères, score de 0 à 3 :

| Critère | Description |
|---|---|
| **V** — Validité scientifique | Niveau de consensus empirique et reproductibilité |
| **A** — Applicabilité MERLIN | Cohérence avec l'architecture et les flux de données existants |
| **C** — Coût d'implémentation | Inverse du coût (3 = peu coûteux, 0 = très coûteux) |
| **I** — Impact praticien | Valeur perçue et utilisée par le praticien |
| **U** — Utilité client | Bénéfice direct sur l'expérience et l'accompagnement du client |

**Score total /15 → Indice de pertinence MERLIN (IPM)**

---

### 2.2 Table de classification complète

| # | Méthode | V | A | C | I | U | **IPM /15** | Priorité |
|---|---|---|---|---|---|---|---|---|
| 1 | **Big Five / OCEAN** | 3 | 3 | 2 | 3 | 2 | **13** | 🔴 P1 — Core |
| 2 | **LEARY / Circumplex** | 3 | 3 | 2 | 3 | 2 | **13** | 🔴 P1 — Déjà ancré |
| 3 | **Prosodie vocale (Deepgram)** | 3 | 3 | 3 | 3 | 1 | **13** | 🔴 P1 — Déjà déployé |
| 4 | **Schwartz Values (circumplex)** | 3 | 3 | 2 | 2 | 2 | **12** | 🔴 P1 — Valeurs |
| 5 | **NLP Big Five detection** | 3 | 3 | 2 | 2 | 1 | **11** | 🟠 P2 — Pipeline |
| 6 | **Spatial Matching (vectoriel)** | 2 | 3 | 2 | 3 | 2 | **12** | 🔴 P1 — Matching |
| 7 | **Ternary Plot (3 valeurs custom)** | 2 | 3 | 3 | 3 | 3 | **14** | 🔴 P1 — Visualisation |
| 8 | **Radar / Spider Chart** | 2 | 3 | 3 | 3 | 3 | **14** | 🔴 P1 — Visualisation |
| 9 | **Moral Foundations Theory** | 3 | 2 | 2 | 2 | 1 | **10** | 🟠 P2 — Éthique/XAI |
| 10 | **Jungien (types + Ombre)** | 2 | 3 | 2 | 3 | 3 | **13** | 🔴 P1 — Cadre holistique |
| 11 | **Enneagramme** | 1 | 3 | 3 | 3 | 3 | **13** | 🔴 P1 — Praticiens holistes |
| 12 | **HEXACO** | 3 | 2 | 2 | 1 | 1 | **9** | 🟡 P3 — Optionnel |
| 13 | **MBTI** | 1 | 2 | 3 | 3 | 3 | **12** | 🟠 P2 — Populaire (faible validité) |
| 14 | **Inglehart-Welzel / WVS** | 3 | 2 | 1 | 1 | 1 | **8** | 🟡 P3 — Ancrage culturel |
| 15 | **JITAI** | 3 | 2 | 1 | 2 | 3 | **11** | 🟠 P2 — Strate 3 |
| 16 | **Digital Phenotyping complet** | 3 | 1 | 0 | 1 | 2 | **7** | 🟢 P4 — Futur |
| 17 | **Cognitive Maps vectorielles** | 2 | 2 | 1 | 1 | 1 | **7** | 🟢 P4 — Recherche |
| 18 | **DW-NOMINATE / Spatial N-D** | 3 | 1 | 0 | 0 | 0 | **4** | ✗ Non applicable |
| 19 | **Political Compass** | 3 | 1 | 2 | 0 | 0 | **6** | ✗ Hors périmètre |
| 20 | **Heatmap temporelle** | 2 | 3 | 3 | 2 | 2 | **12** | 🔴 P1 — Longitudinal |

**Légende priorités :**  
🔴 P1 = Intégration immédiate (Strate 1-2) | 🟠 P2 = Prochaine itération | 🟡 P3 = Optionnel selon praticien | 🟢 P4 = Roadmap futur | ✗ = Hors périmètre

---

## 3. Système de veille — Interface administrateur

### 3.1 Principes de design

- **Non-activée par défaut** — chaque module de veille est `OFF` au déploiement
- **Activation par clic unique** depuis le tableau de bord admin
- **Granularité** : veille globale (`tout`) ou par domaine (modèles, marchés, recherche, concurrence)
- **Fréquence configurable** : quotidienne / hebdomadaire / mensuelle
- **Format de sortie** : digest structuré (titre + résumé + pertinence MERLIN + lien)

### 3.2 Domaines de veille disponibles

| # | Domaine | Sources cibles | Fréquence recommandée | Activé par défaut |
|---|---|---|---|---|
| 1 | **Psychométrie computationnelle** | arXiv, PubMed, Semantic Scholar | Hebdomadaire | ✗ |
| 2 | **Digital phenotyping** | PubMed, JMIR, NeurIPS proceedings | Hebdomadaire | ✗ |
| 3 | **JITAI & mobile health** | JMIR, Cochrane, ClinicalTrials.gov | Mensuelle | ✗ |
| 4 | **LLMs en contexte clinique** | arXiv, Nature Digital Medicine | Hebdomadaire | ✗ |
| 5 | **Matching & recommandation** | ACM RecSys, IEEE, arXiv | Mensuelle | ✗ |
| 6 | **Concurrents (plateformes holistes)** | Web, ProductHunt, Crunchbase | Mensuelle | ✗ |
| 7 | **Réglementation (RGPD, Loi 25 QC)** | Journaux officiels, CAI Québec | Mensuelle | ✗ |
| 8 | **Financement (CALQ, CLD, Inno.)** | Portails gouvernementaux QC/CA | Mensuelle | ✗ |
| 9 | **Savoirs autochtones & wellness** | Publications universitaires, UNESCO | Mensuelle | ✗ |
| 10 | **Neurosciences & axe gut-brain** | PubMed, Frontiers, Nature | Mensuelle | ✗ |

### 3.3 Architecture technique (veille)

```
Admin Dashboard
  └─ Module Veille [toggle ON/OFF par domaine]
       ├─ Cron job (cadence configurable)
       ├─ Perplexity API → recherche structurée par domaine
       ├─ Filtrage LLM → pertinence MERLIN (score 0-10)
       ├─ Digest stocké → PostgreSQL (table: veille_digests)
       └─ Notification admin → email / in-app si score > seuil
```

### 3.4 Structure d'un digest de veille

```json
{
  "date": "2026-06-29",
  "domaine": "psychometrie_computationnelle",
  "items": [
    {
      "titre": "Big Five detection from speech — Université de Barcelone",
      "resume": "Modèle atteignant 78% F1 sur transcriptions...",
      "pertinence_merlin": 9,
      "impact_praticien": "Haute",
      "impact_client": "Indirecte",
      "url": "https://arxiv.org/...",
      "action_suggérée": "Évaluer intégration pipeline MERLIN Strate 2"
    }
  ]
}
```

---

## 4. Système d'attribution des modèles

### 4.1 Logique d'attribution

L'attribution d'un modèle à un praticien ou à un cas client suit une logique en 4 étapes :

```
1. DÉTECTION     → Quels signaux disponibles ? (séance audio, formulaire, historique)
2. ÉLIGIBILITÉ   → Le modèle peut-il s'appliquer ? (données suffisantes, consentement)
3. VALEUR        → IPM + contexte cas = Score d'opportunité (SO)
4. RENTABILITÉ   → ROI estimé avant déclenchement
```

### 4.2 Critères d'éligibilité par modèle

| Modèle | Données minimales requises | Consentement requis | Seuil déclenchement |
|---|---|---|---|
| Big Five via NLP | Transcription ≥ 10 min | Général (analyse séance) | IPM ≥ 11 |
| LEARY Circumplex | Transcription ≥ 5 min | Général | Toujours (core) |
| Prosodie vocale | Audio brut disponible | Général | Toujours (core) |
| Schwartz Values | Formulaire d'intake rempli | Général | Si formulaire complet |
| Ternary Plot | 3 scores normalisés | Général | Automatique si scores |
| JITAI | ≥ 3 séances historiques | Spécifique (suivi actif) | Strate 3 uniquement |
| Matching vectoriel | Profil praticien + profil client | Général | Dès inscription |

### 4.3 Score d'opportunité (SO)

```
SO = IPM × Disponibilité_données × Alignement_praticien

où :
  IPM              = Indice de pertinence MERLIN (0-15)
  Disponibilité    = [0.0 – 1.0] selon complétude des données
  Alignement_prat. = [0.0 – 1.0] selon les paramètres du praticien
  
SO_max = 15.0
Seuil d'activation = SO ≥ 8.0
```

---

## 5. Évaluation de la rentabilité

### 5.1 Variables économiques de MERLIN

| Variable | Description | Mesure |
|---|---|---|
| **CR** | Coût de la ressource (calcul, API, transcription) | $ par séance |
| **CP** | Contribution du praticien | Abonnement mensuel + % commissions optionnels |
| **CC** | Contribution du client | Frais de séance via Stripe |
| **VM** | Valeur du modèle appliqué | Augmentation de rétention / satisfaction |
| **CIM** | Coût d'implémentation du modèle | Développement + maintenance |

### 5.2 Formule de rentabilité par action

```
ROI_action = (VM + CP_net + CC_net - CR - CIM_amorti) / (CR + CIM_amorti)

où :
  CP_net  = Revenus praticien générés par la fonctionnalité
  CC_net  = Revenus client générés par la fonctionnalité
  VM      = Proxy : taux de rétention × valeur vie client (LTV)
  CR      = Coût API Deepgram + Whisper + calcul LLM par séance
  CIM_amorti = Coût développement / (nb_séances_utilisées)
```

### 5.3 Table de rentabilité estimée par modèle

| Modèle | CR estimé/séance | Valeur ajoutée | Seuil rentabilité | Statut |
|---|---|---|---|---|
| Prosodie vocale | 0.08$ (Deepgram) | Rétention +15% | 1 séance | ✓ Rentable dès J1 |
| Big Five NLP | 0.12$ (LLM call) | Rapport enrichi | 3 séances | ✓ Rentable |
| LEARY Circumplex | 0.05$ (calcul local) | Insight praticien | 1 séance | ✓ Rentable dès J1 |
| Matching vectoriel | 0.02$ (calcul local) | Acquisition client | 1 match réussi | ✓ Rentable dès J1 |
| Schwartz + Ternary | 0.02$ (calcul local) | Engagement client | 2 séances | ✓ Rentable |
| JITAI adaptatif | 0.25$ (multi-appels) | Rétention long terme | 8 séances | ◑ Strate 3 |
| Digital Phenotyping | 1.50$+ (intégrations) | Suivi clinique | 20+ séances | ✗ Trop coûteux Strate 1-2 |

### 5.4 Tableau de bord rentabilité (vue admin)

```
Par praticien :
  ├─ Revenu généré (séances × prix praticien)
  ├─ Coût plateforme (transcription + LLM + infrastructure)
  ├─ Marge brute MERLIN
  ├─ Modèles utilisés → coût par modèle
  └─ ROI par modèle activé

Par client :
  ├─ LTV estimée (séances complétées × valeur moyenne)
  ├─ Modèles appliqués à son profil
  ├─ Coût d'accompagnement (modèles actifs)
  └─ Marge nette sur ce client

Global :
  ├─ CAC (coût d'acquisition praticien / client)
  ├─ LTV / CAC ratio
  ├─ Revenu par modèle activé
  └─ Classement des modèles par ROI réel
```

---

## 6. Roadmap d'intégration par strate

### Strate 1 — Fondation (actuel)
- [x] Transcription audio (Deepgram / Whisper)
- [x] LEARY / Circumplex interpersonnel
- [ ] Big Five via NLP sur transcriptions
- [ ] Prosodie vocale enrichie (ton, débit, pauses)
- [ ] Radar / Spider Chart — profil praticien
- [ ] Ternary Plot — profil client (3 valeurs custom)
- [ ] Schwartz Values — formulaire intake
- [ ] Matching vectoriel (cosine similarity)
- [ ] Heatmap temporelle (évolution client)

### Strate 2 — Expansion
- [ ] Enneagramme (module optionnel praticien)
- [ ] Jungien avancé (Ombre, Anima, typologies)
- [ ] MFT — analyse éthique des échanges
- [ ] Module veille admin (10 domaines)
- [ ] Dashboard rentabilité par modèle
- [ ] Clustering clients (K-means sur profils)

### Strate 3 — Intelligence adaptative
- [ ] JITAI — interventions adaptatives
- [ ] Digital phenotyping léger (keystroke + patterns app)
- [ ] Cognitive maps vectorielles
- [ ] LLM navigateur longitudinal (GPT-4o niveau)

### Strate 4 — Plateforme ouverte
- [ ] API publique modèles comportementaux
- [ ] Intégration wearables (actigraphie, HRV)
- [ ] Abonnements avancés praticiens (modules à la carte)

---

## 7. Gouvernance & éthique des modèles

| Principe | Application MERLIN |
|---|---|
| **Non-prescriptif** | Aucun modèle ne produit de diagnostic médical ou de recommandation de traitement |
| **Transparence (XAI)** | Chaque score est explicable au praticien (pas de boîte noire) |
| **Consentement granulaire** | Client consent par domaine d'analyse (voix, texte, profil) |
| **Effacement biométrique** | Données vocales effacées à J+30 (Loi 25 QC / RGPD) |
| **Souveraineté des données** | Hébergement Québec uniquement (OVH CA) |
| **Posture culturelle** | Savoirs autochtones traités comme cadres de référence, non comme variables |
| **MFT comme socle éthique** | Les 6 fondements moraux guident les choix de design et d'attribution |

---

## 8. Glossaire

| Terme | Définition |
|---|---|
| **IPM** | Indice de Pertinence MERLIN (0-15) — évaluation interne d'un modèle |
| **SO** | Score d'Opportunité — déclencheur d'attribution dynamique |
| **ROI_action** | Retour sur investissement par action analytique déclenchée |
| **LTV** | Life Time Value — valeur vie d'un praticien ou d'un client |
| **CAC** | Coût d'Acquisition Client |
| **JITAI** | Just-In-Time Adaptive Intervention — intervention mobile adaptative en temps réel |
| **MFT** | Moral Foundations Theory — cadre de valeurs morales en 6 dimensions |
| **XAI** | Explainable AI — IA explicable, transparente pour l'utilisateur final |
| **Digital Phenotyping** | Quantification comportementale passive via appareils numériques |
| **Ternary Plot** | Diagramme triangulaire à 3 variables dont la somme = 100% |
| **Circumplex** | Représentation circulaire de traits en relation continue (ex. : LEARY, Schwartz) |

---

*Document vivant — mis à jour à chaque cycle de veille ou itération de strate.*  
*Prochaine révision recommandée : Strate 2 kick-off.*

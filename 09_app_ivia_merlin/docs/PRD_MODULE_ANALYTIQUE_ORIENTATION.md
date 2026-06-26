# PRD — Module Analytique d'Orientation (IVIA × MERLIN)
**Version :** 1.0 — 25 juin 2026  
**Statut :** Hypothèses fondatrices — à valider en Phase 0 (pilote 10 praticiens)  
**Auteur :** Session de conception Perplexity × Fondateur

---

## 1. Contexte et positionnement

MERLIN est une plateforme SaaS B2B destinée aux praticiens en accompagnement (coachs, thérapeutes, psychopraticiens) au Québec. IVIA est la couche analytique et mémorielle de MERLIN : elle centralise les profils clients, les observations de séance et les données comportementales.

Le **Module Analytique d'Orientation** est une capacité optionnelle de IVIA qui permet au praticien de générer, à partir des données d'un dossier client, une **représentation structurée du profil d'orientation** du client — ses tendances comportementales, ses valeurs dominantes et son positionnement relationnel — à des fins d'accompagnement ciblé.

Ce module **n'est pas un outil de diagnostic clinique**. Il est un outil d'aide à la lecture du client pour le praticien.

---

## 2. Problème à résoudre

### Pour le praticien
- Difficulté à synthétiser les observations accumulées sur un client en un portrait cohérent
- Manque d'un référentiel commun pour communiquer sur l'orientation d'un client (entre séances, entre praticiens, en supervision)
- Temps élevé de préparation de séance → besoin d'un support visuel généré automatiquement

### Pour la plateforme (MERLIN/IVIA)
- Différenciation forte face aux outils généralistes (SimplePractice, Jane App, etc.)
- Levier de rétention : un praticien ayant des profils analytiques constitués a un coût de départ très élevé
- Levier ARPU : add-on à +19 $/mois justifiable par la valeur créée

---

## 3. Périmètre fonctionnel — Version 1.0

### 3.1 Ce qui est inclus (MVP)

| Fonctionnalité | Description |
|---|---|
| **Profil d'orientation client** | Génération d'une carte visuelle (radar / triangle / axes) à partir des données du dossier |
| **Dimensions analysées** | 3 axes configurables par l'admin de la plateforme (ex. : Autonomie / Cadre / Lien) |
| **Entrées acceptées** | Notes de séance, réponses aux questionnaires intake, observations manuelles |
| **Mise à jour dynamique** | Le profil se recalcule à chaque nouvelle entrée validée par le praticien |
| **Export PDF** | Génération d'un rapport de profil exportable (usage praticien uniquement, non partageable au client par défaut) |
| **Historique d'évolution** | Visualisation de l'évolution du profil dans le temps (timeline) |

### 3.2 Ce qui est exclu (V1)

- Partage automatique du profil au client (prévu V2)
- Comparaison entre profils clients
- Intégration avec des référentiels tiers (MBTI, Big Five, etc.) — étudié pour V3
- Module de transcription automatique (module séparé)
- Recommandations d'exercices générées par IA (prévu V2)

---

## 4. Rôles et permissions

| Rôle | Accès | Actions |
|---|---|---|
| **Admin plateforme** | Configuration globale | Définir les dimensions d'orientation, activer/désactiver le module par tenant |
| **Praticien (abonné au module)** | Dossiers de ses clients | Générer, consulter, annoter, exporter les profils |
| **Praticien (non abonné)** | Aperçu verrouillé | Voir la prévisualisation floue, accéder à la page d'upgrade |
| **Client** | Aucun accès V1 | — |
| **Superviseur (futur)** | Accès délégué | Consulter les profils des clients du supervisé (V2) |

---

## 5. Cas d'usage principaux

### UC-01 : Génération initiale du profil
**Acteur :** Praticien abonné au module  
**Prérequis :** Dossier client avec ≥ 1 note de séance ou réponse intake  
**Flux :**
1. Praticien ouvre le dossier client → onglet "Orientation"
2. Clic sur "Générer le profil"
3. IVIA analyse les données disponibles et calcule les scores sur les 3 dimensions
4. La carte visuelle s'affiche avec les scores et une légende textuelle
5. Le praticien peut annoter manuellement et valider

### UC-02 : Mise à jour après séance
**Acteur :** Praticien  
**Flux :**
1. Praticien saisit les notes post-séance
2. IVIA propose automatiquement une mise à jour du profil (notification discrète)
3. Praticien accepte ou ignore la mise à jour
4. Si acceptée : nouveau point ajouté à la timeline d'évolution

### UC-03 : Export pour supervision
**Acteur :** Praticien  
**Flux :**
1. Praticien ouvre le profil → bouton "Exporter PDF"
2. Choix : profil complet / profil anonymisé
3. PDF généré avec carte visuelle + légende + historique d'évolution

### UC-04 : Upgrade depuis aperçu verrouillé
**Acteur :** Praticien non abonné  
**Flux :**
1. Praticien voit l'onglet "Orientation" avec aperçu flou
2. Clic sur "Activer le module" → modal de présentation
3. Redirection vers Stripe Checkout pour add-on +19 $/mois
4. Après paiement : activation immédiate, génération du premier profil guidée

---

## 6. Architecture technique

### 6.1 Couches impliquées

```
┌─────────────────────────────────────────────────┐
│  09_app_ivia_merlin (Next.js frontend)          │
│  └── /dossier/[id]/orientation                  │
│      └── OrientationCard, Timeline, ExportBtn   │
├─────────────────────────────────────────────────┤
│  10_backend_merlin_api (API REST / tRPC)        │
│  └── /api/orientation/                          │
│      ├── generate (POST)                        │
│      ├── history (GET)                          │
│      └── export-pdf (POST)                      │
├─────────────────────────────────────────────────┤
│  Service analytique (Python / Edge Function)    │
│  └── Calcul des scores sur les dimensions       │
│      à partir des embeddings des notes          │
├─────────────────────────────────────────────────┤
│  PostgreSQL (via Prisma)                        │
│  └── Tables : orientation_profiles,            │
│      orientation_snapshots, dimension_config    │
└─────────────────────────────────────────────────┘
```

### 6.2 Schéma SQL (Prisma)

```prisma
model OrientationProfile {
  id          String   @id @default(cuid())
  clientId    String
  tenantId    String
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
  isActive    Boolean  @default(true)

  client      Client   @relation(fields: [clientId], references: [id])
  snapshots   OrientationSnapshot[]

  @@index([clientId, tenantId])
}

model OrientationSnapshot {
  id          String   @id @default(cuid())
  profileId   String
  createdAt   DateTime @default(now())
  triggeredBy String   // 'manual' | 'post_session' | 'intake'
  scores      Json     // { dimension1: 0.72, dimension2: 0.45, dimension3: 0.83 }
  notes       String?  // annotation manuelle du praticien
  validatedAt DateTime?

  profile     OrientationProfile @relation(fields: [profileId], references: [id])
}

model DimensionConfig {
  id          String   @id @default(cuid())
  tenantId    String   @unique
  dimensions  Json     // [{ key: 'autonomie', label: 'Autonomie', color: '#01696f' }, ...]
  updatedAt   DateTime @updatedAt

  @@index([tenantId])
}
```

### 6.3 Événements métier

```json
// orientation.generated
{
  "event": "orientation.generated",
  "tenantId": "tenant_xxx",
  "practitionerId": "pract_xxx",
  "clientId": "client_xxx",
  "snapshotId": "snap_xxx",
  "triggeredBy": "manual",
  "scores": { "autonomie": 0.72, "cadre": 0.45, "lien": 0.83 },
  "timestamp": "2026-06-25T14:00:00Z"
}

// orientation.exported
{
  "event": "orientation.exported",
  "tenantId": "tenant_xxx",
  "practitionerId": "pract_xxx",
  "clientId": "client_xxx",
  "format": "pdf",
  "anonymized": false,
  "timestamp": "2026-06-25T14:05:00Z"
}

// orientation.module.activated
{
  "event": "orientation.module.activated",
  "tenantId": "tenant_xxx",
  "practitionerId": "pract_xxx",
  "plan": "addon_orientation",
  "stripeSubscriptionItemId": "si_xxx",
  "timestamp": "2026-06-25T14:10:00Z"
}
```

---

## 7. Gouvernance du module

### Activation
- Désactivé par défaut pour tous les nouveaux tenants
- Activable via Stripe add-on (+19 $/mois) depuis les paramètres du compte
- L'admin plateforme peut activer gratuitement pour les comptes pilote

### Configuration des dimensions
- L'admin plateforme définit les dimensions par défaut (3 axes, labels, couleurs)
- En V2 : chaque tenant (praticien/cabinet) peut personnaliser ses propres dimensions

### Confidentialité
- Les profils d'orientation sont des données de santé au sens de la Loi 25 (Québec)
- Stockés chiffrés au repos
- Non partagés entre tenants
- Export client nécessite consentement explicite (V2)

---

## 8. KPIs de succès du module

| KPI | Cible Phase 1 | Cible Phase 2 |
|---|---|---|
| Taux d'adoption (praticiens actifs ayant activé le module) | 25 % | 40 % |
| Profils générés par praticien actif / mois | ≥ 3 | ≥ 8 |
| Taux de rétention des abonnés au module | > 90 % | > 95 % |
| ARPU uplift moyen grâce au module | +19 $ | +22 $ (add-ons cumulés) |
| NPS spécifique au module | — | ≥ 45 |

---

## 9. Roadmap

| Phase | Livrable | Délai estimé |
|---|---|---|
| **Phase 0 — Pilote** | Profil statique sur données intake, affichage radar, export PDF basique | M1–M2 |
| **Phase 1 — MVP** | Mise à jour dynamique post-séance, timeline, upgrade flow Stripe | M3–M5 |
| **Phase 2 — Enrichissement** | Partage client, supervision, personnalisation dimensions par tenant | M6–M10 |
| **Phase 3 — IA** | Recommandations d'exercices, intégration référentiels (Big Five, etc.) | M10–M18 |

---

## 10. Dépendances

| Dépendance | Module | Statut |
|---|---|---|
| Système de dossiers clients | Core MERLIN | ✅ Existant |
| Formulaires intake | Core MERLIN | ✅ Existant |
| Notes de séance | Core MERLIN | ✅ Existant |
| Stripe add-ons | 10_backend_merlin_api | 🔄 À implémenter |
| Service d'embeddings (analyse textuelle) | Nouveau service | 🔄 À implémenter |
| Génération PDF | Nouveau service | 🔄 À implémenter |
| Module transcription | Futur module | ⏳ V2 |

---

*Document produit dans le cadre du cycle de conception MERLIN × IVIA — Juin 2026*  
*À réviser après Phase 0 avec retours praticiens pilotes.*

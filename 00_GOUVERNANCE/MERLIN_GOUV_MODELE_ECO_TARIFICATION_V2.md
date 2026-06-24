# MODÈLE ÉCONOMIQUE ET TARIFICATION — IVIA / MÉSANGES
## Version 2.0 — Session du 24 juin 2026

**Auteur** : David Phaneuf + Perplexity  
**Branche** : `refonte-ivia-site-unifie`  
**Remplace** : toute version antérieure de la tarification  
**Statut** : Décisions tranchées — à implémenter

---

## 1. CONTEXTE DE RÉVISION

La session du 24 juin 2026 avait pour objectif de réexaminer le modèle de revenus MÉSANGES dans une optique de **viabilité sans fonds publics** (auto-financement dès le départ), tout en respectant les principes doctrinaux (accessibilité, anti-dépendance, ancrage QC).

Deux tensions identifiées :
- **Tension 1** : accessibilité financière (client à revenu modeste) vs durabilité de la plateforme
- **Tension 2** : fréquence d'usage élevée (idéale pour impact) vs coût unitaire qui augmente avec la fréquence

La résolution : **abonnement mensuel fixe + prix à la séance dégressif selon fréquence choisie.**

---

## 2. MODÈLE TARIFAIRE RETENU

### 2.1 Abonnement mensuel

| Composante | Valeur | Rationale |
|------------|--------|-----------|
| **Frais d'abonnement mensuel** | **39 $/mois** | Donne accès à la plateforme, au journal de bord, aux synthèses, aux ressources MÉSANGES |
| Frais d'abonnement annuel | ~390 $/an (2 mois offerts) | Option fidélisation |

L'abonnement couvre :
- Accès complet à la plateforme MÉSANGES
- Journal de bord (transcription texte permanente — voir §3)
- Synthèses MERLIN (internes, non accessibles au client sous ce nom)
- Ressources orientées autonomie
- 1 séance d'accueil incluse (premier mois)

### 2.2 Tarification à la séance — Paliers dégressifs

Le prix à la séance **diminue** à mesure que la fréquence choisie augmente. La logique : récompenser l'engagement sans punir la sobriété.

| Palier | Fréquence | Prix / séance | Coût mensuel total (abonnement + séances) |
|--------|-----------|--------------|-------------------------------------------|
| **Ponctuel** | 1 séance / mois | 75 $ | 39 + 75 = **114 $** |
| **Régulier** | 2 séances / mois | 65 $ | 39 + 130 = **169 $** |
| **Suivi soutenu** | 4 séances / mois | 55 $ | 39 + 220 = **259 $** |
| **Intensif** | 8 séances / mois | 45 $ | 39 + 360 = **399 $** |

**Séance = 60 minutes avec un praticien MÉSANGES.**

### 2.3 Justification des paliers

- Le palier **Ponctuel** cible les personnes en crise passagère ou en exploration.
- Le palier **Régulier** est le palier cible de la majorité des clients actifs (2x/mois = rythme de suivi sain sans dépendance).
- Le palier **Suivi soutenu** correspond aux transitions de vie majeures (perte d'emploi, deuil, rupture).
- Le palier **Intensif** est temporaire par définition — MÉSANGES n'encourage pas la dépendance.

### 2.4 Coût annuel par fréquence (vision client)

| Fréquence | Coût annuel estimé |
|-----------|--------------------|
| 1 séance/mois | ~1 368 $ |
| 2 séances/mois | ~2 028 $ |
| 4 séances/mois | ~3 108 $ |
| 8 séances/mois | ~4 788 $ |

Pour comparaison : psychologue privé QC = 150–200 $/h, soit 1 800–2 400 $/an pour 1 séance/semaine bimensuelle.

---

## 3. POLITIQUE AUDIO / DONNÉES — DÉCISION TRANCHÉE

### 3.1 Audio des séances

| Donnée | Rétention | Rationale |
|--------|-----------|----------|
| **Fichier audio brut** | **30 jours maximum** puis suppression définitive | Vie privée, confiance, conformité LPRPDE/Loi 25 |
| **Transcription texte** | **Permanente** (durée de l'abonnement actif + 2 ans après résiliation) | Mémoire de parcours, continuité du suivi, journalling |
| Synthèses MERLIN | Permanentes (usage interne praticien + client) | Qualité du suivi |

### 3.2 Droit à la suppression

Le client peut demander la suppression complète de toutes ses données (transcriptions incluses) à tout moment. Délai d'exécution : 30 jours.

### 3.3 Ce que le client voit dans son journal

Le client accède à :
- Ses **transcriptions texte** (ses propres mots, reformulés si demandé)
- Ses **synthèses de séance** (vue praticien, en langage clair)
- Son **fil de progression** (thèmes récurrents, évolutions, jalons)

Il ne voit pas :
- Les fichiers audio (supprimés à J+30)
- Les notes internes du praticien (sauf exception convenue)
- Les données MERLIN brutes

---

## 4. MODÈLE DE REVENUS PRATICIEN

### 4.1 Commission plateforme

| Source | Taux | Description |
|--------|------|-------------|
| **Séances** | Partagé selon accord praticien | Variable selon statut (employé vs indépendant) |
| **Ventes de ressources praticien** | **10 %** | MÉSANGES prélève 10 % sur toute vente de ressource complémentaire publiée par un praticien dans la plateforme (guide, atelier enregistré, programme autonome) |

### 4.2 Rationale du 10 % sur ventes

- Taux bas = incite les praticiens à publier du contenu additionnel
- Crée un revenu passif pour MÉSANGES sans friction
- Cohérent avec l'esprit "espace-vitrine" plutôt que "plateforme-ponction"
- Comparable aux standards des marketplaces de contenu éducatif (Teachable : 5 %, Kajabi : 0 %, Gumroad : 10 %)

### 4.3 Abonnement praticien

À définir en V3. Questions ouvertes :
- Praticien salarié IVIA inc. vs indépendant sous contrat ?
- Frais de plateforme mensuel praticien (accès tableau de bord, outils MERLIN) ?
- Politique de prise en charge des annulations (voir `IVIA_POLITIQUE_ANNULATION_REMBOURSEMENT_v1.0.md`)

---

## 5. SCÉNARIOS DE REVENUS — PHASE PILOTE

Hypothèse : **50 clients actifs** (objectif fin 2026)

| Palier moyen | Revenu abonnements/mois | Revenu séances/mois | Total/mois |
|-------------|------------------------|--------------------|-----------|
| Tous Ponctuels (1/mois) | 50 × 39 = 1 950 $ | 50 × 75 = 3 750 $ | **5 700 $** |
| Tous Réguliers (2/mois) | 50 × 39 = 1 950 $ | 50 × 130 = 6 500 $ | **8 450 $** |
| Mix réaliste (60% Ponctuel, 40% Régulier) | 1 950 $ | ~5 250 $ | **~7 200 $** |

Hypothèse : **200 clients actifs** (objectif mi-2027)

| Palier moyen | Total/mois |
|-------------|------------|
| Mix réaliste | ~28 800 $ |
| Tous Réguliers | ~33 800 $ |

---

## 6. QUESTIONS OUVERTES (à trancher en V3)

- [ ] Prix du palier IVIA OBNL (clientèle subventionnée) — quel rabais ?
- [ ] Gratuité partielle pour praticiens en formation ?
- [ ] Séances de groupe = tarification différente ?
- [ ] Prix de lancement (early adopters) : rabais 20 % les 6 premiers mois ?
- [ ] Intégration assurances / mutuelles QC possible à moyen terme ?

---

## 7. DÉCISIONS NON RÉVISABLES (verrou doctrinal)

Conformément à la Charte Doctrinaire v2.0 :

1. **Aucun modèle freemium basé sur la dépendance** — l'accès gratuit ne peut pas être conditionné à la collecte de données comportementales revendues
2. **Le palier Intensif est temporaire par design** — le praticien doit orienter vers une réduction de fréquence dès que possible
3. **L'abonnement n'est jamais "automatiquement reconduit sans information claire"** — droit de résiliation simple, sans pénalité
4. **Les données audio ne peuvent pas être monétisées** — ni revendues, ni utilisées pour entraîner des modèles tiers

---

*Document produit lors de la session Perplexity du 24 juin 2026. Prochain révision prévue lors de la finalisation du modèle praticien (V3).*

---
titre: Design — header (style getacuity) + refonte du journal + mockups téléphone
id: MERLIN-CSUITE-UX-DESIGN-HEADER-JOURNAL
statut: draft
type: artefact_ux
couche: SYSTEME
périmètre: frontend
auteur: UX (Claude Code) — coordonné ARCH/COMM/CARE/STRAT
date: 2026-06-30
version: 0.1
dépend_de: [MERLIN-CSUITE-UX-COMPO-ACCUEIL, MERLIN-CSUITE-COMM-DISCOURS-IVIA]
cible: ivia_site_v2/
référence_ton: getacuity.io (graphisme repris ; âme NON — Acuity = app IA solo, IVIA = humain)
source_canonique: 11_PROMPTS/06_CSUITE/UX/artefacts/design-header-et-journal.md
---

# Design — header + journal + mockups téléphone V0.1

> On reprend le **graphisme** de getacuity (épure, header flou, lune, mockups téléphone),
> **pas son âme**. Garde-fou STRAT : les mockups montrent l'humain et le fil, jamais un bot solo.

## 1. Header (nav)
- **Pleine largeur, sticky, fond translucide + `backdrop-blur`** : la page défile en flou dessous.
- Logo IVIA à gauche ; **menu aligné à droite**.
- Liens (validés) : **Mon espace · Praticiens · Ressources · À propos**
  (logo = retour accueil ; le journal vit dans « Mon espace »).
- À droite des liens : **🌙 bascule jour/nuit** · **Connexion** · bouton **[ Commencer ]**.
- Libellés (adaptation getacuity → IVIA) : Log in → **Connexion** ; Start free trial → **Commencer**
  (⚠️ pas « essai gratuit » : ton SaaS + trompeur — modèle = 1er échange gratuit puis séances).
- **Numéro d'urgence hors header** (épure) mais ultra-visible bloc ⑧ + footer (CARE).

```
┌──────────────────────────────────────────────────────────────────┐
│  ◐ IVIA          Mon espace  Praticiens  Ressources  À propos      │
│                                     🌙   Connexion   [ Commencer ] │
└──────────────────────────────────────────────────────────────────┘
   pleine largeur · sticky · translucide + backdrop-blur
```

## 2. Mode jour / nuit
- Bascule 🌙 dans le header. Mode nuit = douceur/intimité (colle au « lieu de recueillement »).
- ARCH : CSS variables + classe `.dark` + `localStorage`, vanilla JS (site statique). Faisable sans dépendance.

## 3. Journal refondu (format écran d'abord)
Esprit Acuity « 60 secondes » : peu de friction. **Aucun score affiché** (CARE-client).

```
┌─ Mon journal ─────────────────────────────────────────────────┐
│  📌 Depuis ta dernière rencontre · 12 juin                     │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ Ce qu'on a déposé ensemble…                     [ relire ]│ │  ← différenciateur (le fil)
│  └──────────────────────────────────────────────────────────┘ │
│  Qu'est-ce qui vient aujourd'hui ?                             │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  écrire…                                    🎤 ou parler  │ │  ← voix (cohérent produit)
│  └──────────────────────────────────────────────────────────┘ │
│  Ton fil                                                       │
│   • aujourd'hui ……   • 9 juin ……   • 5 juin ……                │
│  ⤷ À ta prochaine séance, tu arrives avec tout ça.             │
└────────────────────────────────────────────────────────────────┘
```
Éléments : (a) compte rendu de la dernière séance épinglé en haut ; (b) entrée rapide texte **ou voix** ;
(c) fil chronologique sobre ; (d) rappel du bénéfice (« tu arrives avec tout ça »).

## 4. Mockups téléphone (section accueil)
Deux téléphones côte à côte = les deux objets d'analyse. Présentés en réaliste (façon getacuity).
- 📱 **Client** : journal + fil + écoute → « Pas un algorithme. Quelqu'un. »
- 📱 **Praticien** : lecture + repères → « outillé pour être pleinement présent ».
Garde-fou STRAT : montrer du **relationnel/humain** (un vrai compte rendu, un praticien), pas un bot.

## À confirmer avant implémentation CSS/HTML
- [ ] CTA **« Commencer »** (reco) vs autre formule (le fondateur tenait à « Start free trial »).
- [ ] **Numéro d'urgence hors header** (épure) — OK pour CARE/fondateur ?
- [ ] Mode **nuit par défaut ou jour par défaut** ?
- [ ] Une fois validé → tâche **ARCH+UX** : implémenter header + toggle + journal dans `ivia_site_v2/`
      (hors prod tant que non validé).

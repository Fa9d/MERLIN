---
titre: Base design de l'app IVIA — socle validé (spec mss)
id: MERLIN-CSUITE-UX-BASE-DESIGN-APP
statut: active
type: artefact_ux
couche: SYSTEME
périmètre: frontend
auteur: UX (Claude Code) — base validée fondateur 2026-07-01
date: 2026-07-01
version: 1.0
dépend_de: [MERLIN-CSUITE-UX-COMPO-ACCUEIL, MERLIN-CSUITE-COMM-DISCOURS-IVIA]
intrants_consommés:
  - _archives/intrants/2026-07/mss-mobile-screens-showcase.md
  - _archives/intrants/2026-07/mss-design-tokens.md
implementation_reference: ivia_site_v2/_proto/showcase.html
source_canonique: 11_PROMPTS/06_CSUITE/UX/artefacts/base-design-app.md
---

# Base design de l'app IVIA — V1.0

> Socle validé par le fondateur (2026-07-01) après plusieurs itérations. On **part de là**.
> Référence vivante implémentée : `ivia_site_v2/_proto/showcase.html` (clair + sombre).

## Validé (figé)
- **Typographie : Inter** (sans-sérif humaniste, moderne). *(Abandonné : Lora/serif « carnet », rejeté.)*
- **Système de tokens** de la spec `mss` : couleurs (variables), rayons 8–16, ombres douces, espacements.
- **Structure d'app** : format téléphone, header, contenu en sections/cartes, **bottom nav 5 items
  avec bouton central RGNR** (cercle accent qui chevauche la barre).
- **Thème clair + sombre** (toggle via `data-theme`).
- **3 téléphones** de référence : ① Découverte + check-in · ② RGNR · ③ Praticiens.

## À finaliser plus tard (NON figé)
- **Couleurs** : la palette mss (beige/vert RGNR) est une base de travail, à revoir.
- **Contenu / vocabulaire** : la spec parle de « RGNR / régénération », « check-in », « pratiques »,
  « intentions ». À **réconcilier** avec le discours COMM figé (« journal », « écoute », « le fil »,
  « lieu de recueillement »). Décision de vocabulaire produit encore ouverte.

## Historique des itérations (pour mémoire — retirées du _proto, conservées dans Git)
generique pastel (app-client) → contraste vert profond (app-v2) → carnet serif (rejeté) →
**spec mss / Inter (retenue)**. Le rejet du « look IA tendance » a mené ici.

## Garde-fous (rappel)
Non-clinique (Loi 21) ; humeur en mots, pas de score exposé ; « pistes » pas « consignes » ;
bloc urgence toujours accessible (CARE). Voir contrats/client/CARE-client.md.

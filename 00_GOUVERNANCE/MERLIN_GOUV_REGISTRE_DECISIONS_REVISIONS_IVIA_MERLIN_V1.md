# MERLIN - Registre decisions et revisions IVIA / MERLIN V1

Date: 2026-04-21
Statut: draft
Objet: centraliser les decisions structurantes, les revisions et les points de reference canoniques

---

## 1) Usage de ce registre

Ce registre sert a:
- retrouver vite ce qui est retenu;
- distinguer decision, hypothese et revision;
- savoir ou revenir si une direction doit etre corrigee;
- faire le pont entre conversation, gouvernance, marque, produit et prototype.

Chaque entree doit rester courte, verifiable et reliee a une source.

---

## 2) Decisions canoniques

| ID | Date | Type | Scope | Statement | Statut | Source principale |
|---|---|---|---|---|---|---|
| DEC-001 | 2026-04-20 | decision | marque | `IVIA` est la facade publique cote client. | validated | `MERLIN_GOUV_ARCHITECTURE_MARQUE_PLATEFORMES_V1.md` |
| DEC-002 | 2026-04-20 | decision | marque | `MERLIN` est le moteur, la methode, la couche d'analyse et la valeur cote praticiens. | validated | `MERLIN_GOUV_ARCHITECTURE_MARQUE_PLATEFORMES_V1.md` |
| DEC-003 | 2026-04-20 | decision | plateforme | Le portail praticien doit etre separe et non visible dans la navigation publique standard. | validated | `MERLIN_GOUV_ARCHITECTURE_MARQUE_PLATEFORMES_V1.md` |
| DEC-004 | 2026-04-20 | decision | public | La promesse publique doit parler d'ecoute, clarification, orientation et continuite. | validated | `MERLIN_GOUV_POSITIONNEMENT_PUBLIC_SITE_V1.md` |
| DEC-005 | 2026-04-20 | decision | public | `IN VIVO IN ACTU` est une signature doctrinale et non un headline principal. | validated | `MERLIN_GOUV_ARCHITECTURE_MARQUE_PLATEFORMES_V1.md` |
| DEC-006 | 2026-04-20 | decision | public | `La puissance du silence` peut servir de signature de campagne, pas de promesse unique. | validated | `MERLIN_GOUV_ARCHITECTURE_MARQUE_PLATEFORMES_V1.md` |
| DEC-007 | 2026-04-20 | decision | offre | MERLIN ne doit pas etre presente comme therapie reservee ni comme diagnostic. | validated | `MERLIN_GOUV_POSITIONNEMENT_PUBLIC_SITE_V1.md` |
| DEC-008 | 2026-04-20 | decision | priorite | La diffusion client est prioritaire avant l'approfondissement du discours pro. | review | `MERLIN_GOUV_STRATEGIE_DIFFUSION_CLIENT_IVIA_V1.md` |
| DEC-009 | 2026-04-20 | decision | design | La direction visuelle retenue a ce stade est `editorial calme` pour IVIA et `documentaire net` pour MERLIN. | review | `MERLIN_GOUV_DIRECTION_VISUELLE_FINALE_IVIA_MERLIN_V1.md` |
| DEC-010 | 2026-04-20 | decision | logo | Le logo MERLIN doit rester celui fourni par l'utilisateur, sans reinterpretation graphique. | validated | `MERLIN_GOUV_NOTES_LOGO_MERLIN_RECUPERATION_V1.md` |
| DEC-011 | 2026-04-20 | decision | logo | La bougie IVIA de reference est la variante classique, sauf revision ulterieure explicite. | review | `MERLIN_GOUV_NOTES_LOGO_IVIA_VARIANTES_BOUGIE_V1.md` |
| DEC-012 | 2026-04-20 | decision | economie | Le modele economique doit distinguer cout direct par seance, frais fixes, marge brute et marge nette. | validated | `MERLIN_GOUV_SIMULATION_ECO_COUTS_REELS_V2.md` |
| DEC-013 | 2026-04-20 | decision | economie | Stripe peut etre mis a la charge du praticien dans le modele cible afin de proteger la marge MERLIN. | review | `MERLIN_GOUV_SIMULATION_ECO_COUTS_REELS_V2.md` |
| DEC-014 | 2026-04-20 | decision | offre praticiens | Les couches de service pro doivent etre lisibles par niveau: operationnel, reporting, lecture historique. | review | `MERLIN_GOUV_OFFRE_PRATICIENS_GRILLE_COMMERCIALE_V1.md` |
| DEC-015 | 2026-04-21 | decision | memoire | Toute session importante doit produire un checkpoint memoire et un registre de decisions mis a jour. | validated | `MERLIN_MEMO_LOG_SESSION_2026-04-20_2026-04-21_v1.0.md` |

---

## 3) Revisions canoniques

| ID | Date | Type | Scope | Revision | Statut | Source principale |
|---|---|---|---|---|---|---|
| REV-001 | 2026-04-20 | revision | marque | Abandon de la tentative de reconstitution du logo MERLIN. Retour au logo original utilisateur. | validated | `MERLIN_GOUV_NOTES_LOGO_MERLIN_RECUPERATION_V1.md` |
| REV-002 | 2026-04-20 | revision | priorite | Recentrage sur acquisition et diffusion client avant peaufinage du discours praticiens. | review | `MERLIN_GOUV_STRATEGIE_DIFFUSION_CLIENT_IVIA_V1.md` |
| REV-003 | 2026-04-20 | revision | discours | Abandon des formulations trop proches du medical, du diagnostic ou d'une promesse de guerison. | validated | `MERLIN_GOUV_POSITIONNEMENT_PUBLIC_SITE_V1.md` |
| REV-004 | 2026-04-20 | revision | prototype | Le site prototype est considere comme base structurelle seulement, non comme reference de finition. | validated | `MERLIN_MEMO_LOG_SESSION_2026-04-20_2026-04-21_v1.0.md` |

---

## 4) Hypotheses encore ouvertes

| ID | Date | Type | Scope | Statement | Statut |
|---|---|---|---|---|---|
| HYP-001 | 2026-04-20 | assumption | economie | Un modele a frais de volume degressifs peut rester attractif et rentable. | review |
| HYP-002 | 2026-04-20 | assumption | acquisition | Une interface client plus editoriale et plus haut de gamme augmentera la conversion. | review |
| HYP-003 | 2026-04-20 | assumption | produit | La priorite client avant praticiens accelerera la clarte globale du produit. | review |
| HYP-004 | 2026-04-21 | assumption | memoire | Un systeme de checkpoints documentaires limitera la perte de contexte liee a la compression conversationnelle. | review |

---

## 5) Regle de maintenance

Quand une nouvelle decision est prise:
1. l'ajouter ici avec un ID stable;
2. lier la source canonique;
3. preciser si elle est `review` ou `validated`;
4. ne pas supprimer silencieusement l'entree precedente;
5. si une decision est annulee, la passer en `deprecated` ou ajouter une revision.

---

## 6) Decision active

Ce registre devient le point d'entree canonique pour:
- retrouver les arbitrages;
- verifier ce qui est vraiment retenu;
- eviter qu'une conversation utile se perde dans les fichiers disperses.

---
titre: Composition de l'accueil IVIA — schéma des blocs (parcours de conviction)
id: MERLIN-CSUITE-UX-COMPO-ACCUEIL
statut: active
type: artefact_ux
couche: SYSTEME
périmètre: frontend
auteur: UX (Claude Code) — décisions arrêtées par délégation du fondateur 2026-06-30
date: 2026-06-30
version: 1.0
dépend_de: [MERLIN-CSUITE-COMM-DISCOURS-IVIA, MERLIN-GOUV-ETUDE-MARCHE-BESOINS-QC-V1, MERLIN-CARE-CONTRAT-CLIENT-V1]
cible: ivia_site_v2/index.html
source_canonique: 11_PROMPTS/06_CSUITE/UX/artefacts/composition-accueil.md
---

# Composition de l'accueil IVIA — V1.0

> L'accueil est un **parcours de conviction** : chaque bloc répond à la question que le visiteur
> se pose. Le contenu vient du **discours COMM** (`discours-ivia.md`). Décisions arrêtées
> (délégation fondateur 2026-06-30).

## Architecture des pages (décision)
- **Accueil = une page client unique qui scrolle** (les 8 blocs ci-dessous).
- **`/praticiens` = page dédiée** (double marché) ; sur l'accueil, seulement un **bandeau léger** (⑦)
  qui y renvoie — l'accueil ne noie pas le client sous le discours pro.

## Schéma des blocs

```
┌──────────────────────────────────────────────────────────┐
│  NAV   logo IVIA           Pour les praticiens · Connexion │
├──────────────────────────────────────────────────────────┤
│  ① HERO — « c'est quoi ? »                       [COMM]    │
│     « Dire ce que tu vis. Être écouté, pour vrai. »       │
│     lieu de recueillement · « Pas un algorithme. Quelqu'un »│
│     ▸ [ Commencer ]                                        │
├──────────────────────────────────────────────────────────┤
│  ② C'EST POUR MOI ? — reconnaissance             [COMM]    │
│     3-4 situations en mots ordinaires (registres × genre) │
│     démarrage : accompagnant·e épuisé·e + chercheur de sens│
├──────────────────────────────────────────────────────────┤
│  ③ EST / N'EST PAS — clarté non-clinique         [CARE]    │
│     ✓ écoute, présence, orientation                       │
│     ✗ pas un diagnostic, pas un soin, pas un algorithme   │
├──────────────────────────────────────────────────────────┤
│  ④ COMMENT ÇA MARCHE + LE JOURNAL  ★ clé         [UX+COMM] │
│     déposer → être écouté → repartir avec un repère       │
│     LE JOURNAL : le fil entre les séances (différenciateur)│
│     « tu arrives avec le compte rendu de la dernière fois »│
├──────────────────────────────────────────────────────────┤
│  ⑤ POUR LE PRATICIEN — l'outil                [STRAT+UX]   │
│     capte/structure → praticien pleinement présent +      │
│     mieux outillé pour orienter                           │
├──────────────────────────────────────────────────────────┤
│  ⑥ CONFIANCE — « je peux me fier ? »          [STRAT+LEGAL]│
│     humain (pas un algo) · données au Québec (Loi 25) ·   │
│     validation humaine · rien ne se perd                  │
├──────────────────────────────────────────────────────────┤
│  ⑦ OFFRE / FORMULES + bandeau praticiens       [FIN+GROWTH]│
│     1er échange gratuit · tarifs clairs · journal =       │
│     continuité abordable · ▸ bandeau « Pour les praticiens »│
├──────────────────────────────────────────────────────────┤
│  ⑧ URGENCE / CRISE — sécurité (non négociable)   [CARE]    │
│     « IVIA n'est pas un service d'urgence » + ressources  │
├──────────────────────────────────────────────────────────┤
│  FOOTER   mentions · confidentialité · CGU · contact      │
└──────────────────────────────────────────────────────────┘
```

## Logique (entonnoir de conviction)
c'est quoi ① → c'est pour moi ② → c'est pas du clinique ③ → ça marche + le fil ④ →
(le pro derrière) ⑤ → je peux me fier ⑥ → combien + porte praticien ⑦ → sécurité ⑧.

## Points clés (bureau)
- **④ Journal** = le vrai différenciateur. Argument de vente, pas un détail technique — visible, pas enterré.
- **③ Est / n'est pas** = clarificateur n°1 (« comprendre direct ce qu'on vient faire »).
- **⑧ Urgence** = obligatoire, toujours accessible (carte des zones, ligne rouge CARE).

## Prochain pas
- [ ] Confronter ce schéma à `ivia_site_v2/index.html` existant (prod a2903c5 vs wip local) →
      décider, bloc par bloc, ce qu'on garde / refond / écrit.
- [ ] Implémentation : tâche ARCH+UX (Lot frontend, hors prod tant que non validé).

## Historique
| Version | Date | Nature |
|---|---|---|
| 0.1 | 2026-06-30 | brouillon (8 blocs) |
| 1.0 | 2026-06-30 | arrêté (délégation fondateur) ; architecture pages tranchée ; renommé depuis `_DRAFT` |

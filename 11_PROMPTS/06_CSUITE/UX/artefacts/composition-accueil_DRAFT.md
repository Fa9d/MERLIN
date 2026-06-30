---
titre: Composition de l'accueil IVIA — schéma des blocs (parcours de conviction)
id: MERLIN-CSUITE-UX-COMPO-ACCUEIL
statut: draft
type: artefact_ux
couche: SYSTEME
périmètre: frontend
auteur: UX (Claude Code) — coordonné avec COMM/CARE/STRAT/FIN/LEGAL
date: 2026-06-30
version: 0.1
dépend_de: [MERLIN-CSUITE-COMM-DISCOURS-IVIA, MERLIN-GOUV-ETUDE-MARCHE-BESOINS-QC-V1, MERLIN-CARE-CONTRAT-CLIENT-V1]
cible: ivia_site_v2/index.html
source_canonique: 11_PROMPTS/06_CSUITE/UX/artefacts/composition-accueil_DRAFT.md
---

# Composition de l'accueil IVIA — V0.1

> L'accueil n'est pas une vitrine, c'est un **parcours de conviction** : chaque bloc répond à
> la question que le visiteur se pose à ce moment-là. Le contenu de chaque bloc vient du
> **discours COMM** (`voix-et-discours-par-mal`). Ordre = entonnoir.

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
│  ⑤ POUR LE PRATICIEN — l'outil  ★ étoffé      [STRAT+UX]   │
│     capte/structure → praticien pleinement présent +      │
│     mieux outillé pour orienter                           │
├──────────────────────────────────────────────────────────┤
│  ⑥ CONFIANCE — « je peux me fier ? »          [STRAT+LEGAL]│
│     humain (pas un algo) · données au Québec (Loi 25) ·   │
│     validation humaine · rien ne se perd                  │
├──────────────────────────────────────────────────────────┤
│  ⑦ OFFRE / FORMULES — « combien ? »            [FIN+GROWTH]│
│     1er échange gratuit · puis tarifs clairs ·            │
│     journal = continuité abordable (sans multiplier séances)│
├──────────────────────────────────────────────────────────┤
│  ⑧ URGENCE / CRISE — sécurité (non négociable)   [CARE]    │
│     « IVIA n'est pas un service d'urgence » + ressources  │
├──────────────────────────────────────────────────────────┤
│  FOOTER   mentions · confidentialité · CGU · contact      │
└──────────────────────────────────────────────────────────┘
```

## Logique (entonnoir de conviction)
c'est quoi ① → c'est pour moi ② → c'est pas du clinique ③ → ça marche comment + le fil ④ →
(le pro derrière) ⑤ → je peux me fier ⑥ → combien ⑦ → sécurité ⑧.

## Points soulignés par le bureau
- **④ Journal** = le vrai différenciateur (continuité, compte rendu d'une séance à l'autre).
  À ne pas enterrer en bas de page — c'est un argument de vente, pas un détail technique.
- **③ Est / n'est pas** = clarificateur n°1 (« comprendre direct ce qu'on vient faire »).
- **⑧ Urgence** = obligatoire, toujours accessible (carte des zones, ligne rouge CARE).
- **⑤ Praticien** : décider sa place — bandeau sur l'accueil + page dédiée (voir question ouverte).

## À confirmer par le fondateur
- [ ] L'ordre des 8 blocs (enlever / ajouter / déplacer ?).
- [ ] ⑤ Praticien : bandeau sur l'accueil **et** page séparée, ou page séparée seulement ?
- [ ] Une seule page qui scrolle, ou pages distinctes par public (client / praticien) dès l'entrée ?
- [ ] Une fois validé → comparer à `ivia_site_v2/index.html` existant et décider quoi garder/refondre.

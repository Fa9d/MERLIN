# IVIA — Mockups (base botanique v2)

**Source de vérité** : ce dossier
**Architecture** : statique pur — HTML + CSS + JS
**Date de bascule** : 2026-05-09
**Origine** : `ivia_concept_v2_botanique` (8 mai 2026, 16h47 EDT)

## Contenu actuel

- `index.html` — landing botanique
- `lecture-exemple.html` — exemple de lecture (interprétation IVIA)
- `reference-visuelle.html` — charte visuelle de référence
- `styles.css` — feuille de style unique
- `script.js` — interactions

## Test local

```powershell
cd ivia_mockups
python -m http.server 8000
```

Puis ouvrir http://localhost:8000

## Historique

- **Avant 2026-05-09** : version Perplexity (32 pages, architecture Python `pages_*.py` + `build_pages.py`) — archivée sur la branche `archive/site-perplexity-mockup-20260509`
- **2026-05-09** : bascule vers la base botanique de Claude (préférée par David — beauté visuelle, simplicité, doctrine respectée)

## Doctrine

*Au sein de l'être — En actes.*
*Pour le peuple, par le peuple.*

## Prochaine étape

Reconstruire les pages internes (espaces client / praticien / admin / bibliothèque) en respectant la charte botanique. Voir `04_METHODES/BRIEF_COPILOT_REFONTE_LANDING_LIENS_v2.0.md` (à venir).

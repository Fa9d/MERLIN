# JOURNAL — Deck investisseurs Marp (pipeline présentation) — 2026-07-06

**Contexte** : suite du dossier de financement (voir `JOURNAL_dossier-financement_20260706.md`).
Décision fondateur : outil open source pour produire les documents de présentation,
style **épuré** (le produit est la preuve ; cohérence avec la sobriété IVIA).

## Décisions

- **Outil** : Marp (`@marp-team/marp-cli`, MIT) — markdown → PDF / HTML / PPTX.
  Choisi contre Reveal.js / Slidev / Pandoc-Beamer / Typst car le deck source est déjà en markdown.
- **Identité visuelle** : thème CSS custom aux couleurs du site ivia.quebec —
  Lora (titres) + Raleway (corps), vert forêt `#2D6A4F`, crème `#FAFDF8`, encre `#1A2E1D`.
  Le teal `#20808D` mentionné dans les instructions PowerPoint de v1.3/v2.0 est **remplacé**
  par la palette IVIA réelle.
- **Style** : épuré confirmé — pas de flafla ; tableaux sobres, cartes KPI, filet vert sous titre.

## Livrables (`12_JURIDIQUE_AFFAIRES/deck/`)

| Fichier | Contenu |
|---|---|
| `IVIA_DECK_v2.0.marp.md` | 26 slides Marp, notes conférencier en commentaires HTML |
| `ivia-theme.css` | Thème Marp IVIA (cover, divider, cartes .kpi) |
| `IVIA_DECK_v2.0.pdf` | PDF prêt à envoyer (391 Ko) |
| `IVIA_DECK_v2.0.html` | Version navigateur (mode présentateur : touche P) |
| `README.md` | Commandes de régénération (npx marp-cli) |

Source de fond : `IVIA_PITCH_DECK_INVESTISSEURS_v2.0.md` (inchangé) — le deck Marp en est
la mise en forme ; toute évolution de contenu passe d'abord par le fichier de référence.

## Vérifications

- Rendu contrôlé slide par slide (PNG) : couverture sombre dégradée, cartes KPI,
  tableaux comparatifs (concurrence, usage des fonds), slide divider, contact — conformes.
- Accents français corrects (UTF-8 sans BOM).

## Suite

- Ajouter des captures d'écran de la plateforme (slide traction / démo) — liste à préparer.
- Éventuel export PPTX si un investisseur l'exige (commande documentée dans README).
- One-pager : version PDF stylée possible avec le même thème (à la demande).

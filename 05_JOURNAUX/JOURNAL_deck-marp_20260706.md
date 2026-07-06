# JOURNAL â€” Deck investisseurs Marp (pipeline prÃ©sentation) â€” 2026-07-06

**Contexte** : suite du dossier de financement (voir `JOURNAL_dossier-financement_20260706.md`).
DÃ©cision fondateur : outil open source pour produire les documents de prÃ©sentation,
style **Ã©purÃ©** (le produit est la preuve ; cohÃ©rence avec la sobriÃ©tÃ© IVIA).

## DÃ©cisions

- **Outil** : Marp (`@marp-team/marp-cli`, MIT) â€” markdown â†’ PDF / HTML / PPTX.
  Choisi contre Reveal.js / Slidev / Pandoc-Beamer / Typst car le deck source est dÃ©jÃ  en markdown.
- **IdentitÃ© visuelle** : thÃ¨me CSS custom aux couleurs du site ivia.quebec â€”
  Lora (titres) + Raleway (corps), vert forÃªt `#2D6A4F`, crÃ¨me `#FAFDF8`, encre `#1A2E1D`.
  Le teal `#20808D` mentionnÃ© dans les instructions PowerPoint de v1.3/v2.0 est **remplacÃ©**
  par la palette IVIA rÃ©elle.
- **Style** : Ã©purÃ© confirmÃ© â€” pas de flafla ; tableaux sobres, cartes KPI, filet vert sous titre.

## Livrables (`12_JURIDIQUE_AFFAIRES/deck/`)

| Fichier | Contenu |
|---|---|
| `IVIA_DECK_v2.0.marp.md` | 26 slides Marp, notes confÃ©rencier en commentaires HTML |
| `ivia-theme.css` | ThÃ¨me Marp IVIA (cover, divider, cartes .kpi) |
| `IVIA_DECK_v2.0.pdf` | PDF prÃªt Ã  envoyer (391 Ko) |
| `IVIA_DECK_v2.0.html` | Version navigateur (mode prÃ©sentateur : touche P) |
| `README.md` | Commandes de rÃ©gÃ©nÃ©ration (npx marp-cli) |

Source de fond : `IVIA_PITCH_DECK_INVESTISSEURS_v2.0.md` (inchangÃ©) â€” le deck Marp en est
la mise en forme ; toute Ã©volution de contenu passe d'abord par le fichier de rÃ©fÃ©rence.

## VÃ©rifications

- Rendu contrÃ´lÃ© slide par slide (PNG) : couverture sombre dÃ©gradÃ©e, cartes KPI,
  tableaux comparatifs (concurrence, usage des fonds), slide divider, contact â€” conformes.
- Accents franÃ§ais corrects (UTF-8 sans BOM).

## Suite

- Ajouter des captures d'Ã©cran de la plateforme (slide traction / dÃ©mo) â€” liste Ã  prÃ©parer.
- Ã‰ventuel export PPTX si un investisseur l'exige (commande documentÃ©e dans README).
- One-pager : version PDF stylÃ©e possible avec le mÃªme thÃ¨me (Ã  la demande).

---

## Révision v2.1 du deck (même jour)

Demande fondateur : variantes chiffrées et francisation.

- **Anglicismes remplacés** dans tout le deck : MRR/ARR ? RMR/RAR (légende ajoutée),
  gates ? jalons de validation, roadmap ? feuille de route, onboarding ? intégration,
  live ? en production / en ligne, moat ? avantage défendable, pipeline ? chaîne de
  traitement, dataset ? corpus, full-stack ? développement complet, B2B ? offre
  employeurs, due diligence/NDA ? vérification diligente / entente de confidentialité.
- **2 diapositives ajoutées** (chiffres tirés du BP v2.3) :
  - « Les leviers de revenus » : séance 80 $, frais plateforme 3,90–12,90 $/séance,
    abonnement praticien 27,99–84,99 $, services analytiques 1–8 $, enregistrement
    solo 35 $, journal étendu 7 $/mois, employeurs Loi 27 (5–15 K$/an), diffusion MÉSANGES.
  - « Variantes praticiens × clients × revenus (M36) » : 4 scénarios (minimal, pessimiste,
    médian, optimiste) avec praticiens, clients actifs estimés et RAR M36.
- **Trajectoire recalée** sur le scénario médian portefeuille du BP v2.3
  (RMR ~177 K$ M36, RAR ~2,1 M$, équilibre M28–M32) au lieu des chiffres v1.3.
- Piège Marp : K$) ... K$` sur une même ligne interprété comme du LaTeX ? échapper `\$`.
- **Divergence à réconcilier** : le fichier de référence IVIA_PITCH_DECK_INVESTISSEURS_v2.0.md
  n'intègre pas encore ces 2 diapositives ni la francisation ? produire une v2.1 du document
  de référence lors de la prochaine passe sur le corpus de financement.

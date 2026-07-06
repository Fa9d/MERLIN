# Deck investisseurs IVIA — pipeline Marp

Présentation générée depuis le markdown avec [Marp](https://marp.app/) (open source, MIT).
Style **épuré**, identité IVIA (Lora / Raleway, vert forêt `#2D6A4F`, crème `#FAFDF8`).

## Fichiers

| Fichier | Rôle |
|---|---|
| `IVIA_DECK_v2.0.marp.md` | Source des slides (26 slides + notes conférencier en commentaires HTML) |
| `ivia-theme.css` | Thème Marp IVIA (classes : `cover`, `divider`, `.kpi`, `.tag`, `.ok`) |
| `IVIA_DECK_v2.0.pdf` | Sortie PDF (à envoyer aux investisseurs) |
| `IVIA_DECK_v2.0.html` | Sortie HTML (présentation navigateur, flèches ← →) |

Le contenu de référence reste `../IVIA_PITCH_DECK_INVESTISSEURS_v2.0.md` —
toute mise à jour de fond se fait là d'abord, puis se répercute ici.

## Régénérer

Depuis ce dossier (`12_JURIDIQUE_AFFAIRES/deck/`) :

```bash
# HTML
npx --yes @marp-team/marp-cli IVIA_DECK_v2.0.marp.md --theme ivia-theme.css --html -o IVIA_DECK_v2.0.html

# PDF
npx --yes @marp-team/marp-cli IVIA_DECK_v2.0.marp.md --theme ivia-theme.css --html --allow-local-files --pdf -o IVIA_DECK_v2.0.pdf

# PPTX (si un investisseur exige PowerPoint)
npx --yes @marp-team/marp-cli IVIA_DECK_v2.0.marp.md --theme ivia-theme.css --html --pptx -o IVIA_DECK_v2.0.pptx

# Aperçu PNG par slide (contrôle visuel)
npx --yes @marp-team/marp-cli IVIA_DECK_v2.0.marp.md --theme ivia-theme.css --html --images png -o preview.png
```

Prérequis : Node.js + un Chrome/Edge installé (utilisé par Marp pour le rendu PDF/PNG).

## Notes du conférencier

Les notes sont dans le `.marp.md` sous forme de commentaires HTML (`<!-- ... -->`)
après chaque slide. Elles apparaissent dans le mode présentateur HTML (touche `P`)
et dans le PDF si on ajoute `--pdf-notes`.

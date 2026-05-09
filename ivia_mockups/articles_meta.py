"""Métadonnées et parsing simple des 16 articles IVIA."""
import re
from pathlib import Path
import html as html_lib

ARTICLES_DIR = Path(__file__).parent / "articles_md"

# Métadonnées éditoriales : titre court de navigation, axe, ordre de lecture suggéré
ARTICLES = [
    # Section 1 — Écoute & Relation
    ("1_1", "1.1", "Écoute & Relation", "Qu'est-ce qu'une écoute qui respecte le vivant ?"),
    ("1_2", "1.2", "Écoute & Relation", "Quand l'écoute extrait au lieu de soigner"),
    ("1_3", "1.3", "Écoute & Relation", "La présence comme soin"),
    ("1_4", "1.4", "Écoute & Relation", "Tenir le silence sans le remplir"),
    # Section 2 — Équilibre & Vivant
    ("2_1", "2.1", "Équilibre & Vivant", "L'équilibre comme pratique, pas comme état"),
    ("2_2", "2.2", "Équilibre & Vivant", "Les cinq zones du cercle IVIA"),
    ("2_3", "2.3", "Équilibre & Vivant", "Suzuki : quand l'économie oublie qu'elle vit dans la nature"),
    ("2_4", "2.4", "Équilibre & Vivant", "Retrouver sa place dans les cycles"),
    # Section 3 — Frontières & Responsabilité
    ("3_1", "3.1", "Frontières & Responsabilité", "Ce que la responsabilité n'est pas"),
    ("3_2", "3.2", "Frontières & Responsabilité", "La dignité comme cadre"),
    ("3_3", "3.3", "Frontières & Responsabilité", "Quand soutenir devient porter — la limite saine"),
    ("3_4", "3.4", "Frontières & Responsabilité", "Reprendre sa place dans l'échange"),
    # Section 4 — Réalisation & Suite
    ("4_1", "4.1", "Réalisation & Suite", "Que veut dire « se réaliser » ?"),
    ("4_2", "4.2", "Réalisation & Suite", "Choisir une suite concrète"),
    ("4_3", "4.3", "Réalisation & Suite", "Le journal comme pratique vivante"),
    ("4_4", "4.4", "Réalisation & Suite", "Le vivant nous a appris — clore et recommencer"),
]

AXES = {
    "Écoute & Relation": {
        "slug": "ecoute",
        "intro": "Apprendre à écouter ce qui est là, sans extraire ni interpréter.",
        "color": "var(--color-rose)",
    },
    "Équilibre & Vivant": {
        "slug": "equilibre",
        "intro": "Habiter ses cycles, retrouver un rythme qui ressemble à son propre vivant.",
        "color": "var(--color-mousse)",
    },
    "Frontières & Responsabilité": {
        "slug": "frontieres",
        "intro": "Tenir sa place dans la relation. Soutenir sans porter à la place de l'autre.",
        "color": "var(--color-aubergine)",
    },
    "Réalisation & Suite": {
        "slug": "realisation",
        "intro": "Choisir une suite concrète. Tenir parole dans le quotidien ordinaire.",
        "color": "var(--color-miel)",
    },
}


def md_to_html(md_text: str) -> tuple[str, dict]:
    """Convertisseur markdown → HTML très simple, taillé pour le format IVIA.
    Retourne (corps_html, metadata_dict).
    """
    lines = md_text.split("\n")
    meta = {}
    title = ""

    # Extraire titre H1 et bloc meta
    i = 0
    while i < len(lines) and not lines[i].startswith("# "):
        i += 1
    if i < len(lines):
        title = lines[i][2:].strip()
        i += 1

    # Sauter ligne vide et premier "---"
    while i < len(lines) and (not lines[i].strip() or lines[i].strip() == "---"):
        i += 1

    # Lire le bloc meta
    while i < len(lines) and lines[i].strip() != "---":
        line = lines[i].strip()
        m = re.match(r"\*\*([^:]+):\*\*\s*(.+)", line)
        if m:
            meta[m.group(1).strip()] = m.group(2).strip()
        i += 1

    # Sauter --- final du bloc meta
    if i < len(lines) and lines[i].strip() == "---":
        i += 1

    body_lines = lines[i:]
    body_md = "\n".join(body_lines)

    # Parser le corps
    html_out = []
    paragraph = []
    in_list = False
    in_quote = False

    def flush_paragraph():
        nonlocal paragraph
        if paragraph:
            text = " ".join(paragraph).strip()
            if text:
                html_out.append(f"<p>{render_inline(text)}</p>")
            paragraph = []

    def flush_list():
        nonlocal in_list
        if in_list:
            html_out.append("</ul>")
            in_list = False

    def flush_quote():
        nonlocal in_quote
        if in_quote:
            html_out.append("</blockquote>")
            in_quote = False

    def render_inline(s: str) -> str:
        # Échapper d'abord les caractères dangereux (mais on garde italique/gras)
        s = html_lib.escape(s, quote=False)
        # Gras + italique
        s = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", s)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"\*([^\*]+?)\*", r"<em>\1</em>", s)
        # Liens
        s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
        return s

    for raw_line in body_md.split("\n"):
        line = raw_line.rstrip()
        stripped = line.strip()

        if stripped == "---":
            flush_paragraph(); flush_list(); flush_quote()
            html_out.append('<hr class="article-rule">')
            continue
        if not stripped:
            flush_paragraph(); flush_list(); flush_quote()
            continue
        # Headings
        m = re.match(r"^(#{2,6})\s+(.+)$", stripped)
        if m:
            flush_paragraph(); flush_list(); flush_quote()
            level = len(m.group(1))
            html_out.append(f"<h{level}>{render_inline(m.group(2))}</h{level}>")
            continue
        # Bullet
        if stripped.startswith("- "):
            flush_paragraph(); flush_quote()
            if not in_list:
                html_out.append("<ul>")
                in_list = True
            html_out.append(f"<li>{render_inline(stripped[2:])}</li>")
            continue
        # Quote
        if stripped.startswith("> "):
            flush_paragraph(); flush_list()
            if not in_quote:
                html_out.append("<blockquote>")
                in_quote = True
            html_out.append(f"<p>{render_inline(stripped[2:])}</p>")
            continue
        # Italique standalone (ligne en *...*) → on la traite comme paragraphe normal
        flush_list(); flush_quote()
        paragraph.append(stripped)

    flush_paragraph(); flush_list(); flush_quote()

    return "\n".join(html_out), {**meta, "title": title}


def load_article(slug: str) -> dict:
    """Charge un article par son slug (ex '1_1') et retourne {slug, num, axe, title, html, meta}."""
    path = ARTICLES_DIR / f"IVIA_ARTICLE_{slug}_v1.0.md"
    md = path.read_text(encoding="utf-8")
    body_html, meta = md_to_html(md)
    # Récupérer infos de la table
    info = next((a for a in ARTICLES if a[0] == slug), None)
    if not info:
        return {"slug": slug, "num": "", "axe": "", "title": meta.get("title", slug), "html": body_html, "meta": meta}
    return {
        "slug": slug,
        "num": info[1],
        "axe": info[2],
        "title": info[3],
        "html": body_html,
        "meta": meta,
    }


def all_articles() -> list[dict]:
    return [load_article(a[0]) for a in ARTICLES]

# -*- coding: utf-8 -*-
"""Genere les 16 pages d'articles fondateurs dans ivia_site_v2/ressources/.

Source : 04_METHODES/articles/IVIA_ARTICLE_X_Y_v1.0.md (drafts).
- Assainit le vocabulaire interdit (Loi 21) via une table de remplacements ciblee.
- Convertit le markdown simple (##, -, >, **gras**, paragraphes) en HTML.
- Encapsule dans le gabarit sobre du hub /ressources (cf. le-vivant-sait.html).
A relancer si les drafts changent.
"""
import html
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC = os.path.join(ROOT, "04_METHODES", "articles")
OUT = os.path.join(ROOT, "ivia_site_v2", "ressources")

# num -> (slug, section_label, related[num,num])
META = {
    "1_1": ("ecoute-qui-respecte-le-vivant", "Écoute & Relation", ["2_1", "3_1"]),
    "1_2": ("empathie-ethique",              "Écoute & Relation", ["3_2", "4_4"]),
    "1_3": ("lois-de-l-echange",             "Écoute & Relation", ["2_3", "3_4"]),
    "1_4": ("responsabilite-et-dignite",     "Écoute & Relation", ["3_3", "2_4"]),
    "2_1": ("penser-sa-vie-en-cycles",       "Équilibre & Vivant", ["1_1", "4_1"]),
    "2_2": ("le-cercle-carte-d-equilibre",   "Équilibre & Vivant", ["1_3", "4_4"]),
    "2_3": ("economie-et-nature",            "Équilibre & Vivant", ["3_4", "1_3"]),
    "2_4": ("habiter-son-corps",             "Équilibre & Vivant", ["4_2", "1_4"]),
    "3_1": ("espaces-collectifs-qui-epuisent","Empathie & Société", ["1_2", "2_1"]),
    "3_2": ("empathie-et-pouvoir",           "Empathie & Société", ["1_2", "1_4"]),
    "3_3": ("espaces-de-parole-vrais",       "Empathie & Société", ["1_1", "2_2"]),
    "3_4": ("de-la-performance-a-la-presence","Empathie & Société", ["2_3", "4_4"]),
    "4_1": ("tout-vibre",                    "Fréquence & Présence", ["2_1", "2_4"]),
    "4_2": ("le-corps-instrument-de-presence","Fréquence & Présence", ["2_4", "1_2"]),
    "4_3": ("le-savoir-des-plantes",         "Fréquence & Présence", ["2_3", "2_1"]),
    "4_4": ("frequence-et-autonomie",        "Fréquence & Présence", ["1_4", "3_4"]),
}

# Remplacements Loi 21 — par chaine exacte, sens preserve (voir contextes audites)
REPL = [
    ("ne pas forcer la guérison. La laisser venir.", "ne pas forcer le rétablissement. Le laisser venir."),
    ("ne cherche pas à guérir.", "ne cherche pas à réparer l'autre."),
    ("pour que la personne se guérisse elle-même.", "pour que la personne se rétablisse elle-même."),
    ("C'est un diagnostic honnête.", "C'est un constat honnête."),
    ("Ce n'est pas un diagnostic.", "Ce n'est pas un verdict."),
    ("n'est pas un outil de diagnostic.", "n'est pas un outil de verdict."),
    ("certains milieux thérapeutiques.", "certains milieux d'accompagnement."),
    ("pas transformé, pas guéri, juste", "pas transformé, pas réparé, juste"),
    ("n'est pas une thérapie de groupe.", "n'est pas un groupe d'accompagnement encadré."),
    ("ne constituent pas une preuve de guérison par les sons", "ne constituent pas une preuve de mieux-être par les sons"),
    ('"guérir des maladies"', '"faire disparaître la maladie"'),
    ("qu'elle guérit quoi que ce soit.", "qu'elle répare quoi que ce soit."),
    ("active un mode de traitement", "active un mode d'intégration"),
    ("Ce n'est pas une technique thérapeutique.", "Ce n'est pas une technique d'accompagnement."),
    ("Ce que la phytothérapie dit", "Ce que le savoir des plantes dit"),
    ("La phytothérapie — l'usage des plantes à des fins de bien-être —", "Le savoir des plantes — leur usage à des fins de bien-être —"),
    ("La phytothérapie n'est pas une médecine de précision au sens clinique du terme.", "Le savoir des plantes n'est pas une médecine de précision."),
    ("les troubles du sommeil", "le sommeil difficile"),
    ("ni la thérapie seules ne peuvent corriger.", "ni l'accompagnement seuls ne peuvent corriger."),
    ("ne sont pas présentées ici comme des thérapies.", "ne sont pas présentées ici comme des remèdes."),
    ("orienter des traitements.", "orienter des soins médicaux."),
    ("des vibrations à guérir, transformer, attirer.", "des vibrations à tout réparer, transformer, attirer."),
]

# Note de prudence additionnelle par article (constitution §6.4)
EXTRA_NOTE = {
    "4_1": "Registre éducatif uniquement : aucune affirmation de mieux-être par les sons n'est ici un protocole d'usage.",
    "4_3": "Les savoirs des plantes — dont ceux des Premières Nations — sont cités avec respect et jamais appropriés. Registre éducatif ; toute question de santé relève d'une personne qualifiée.",
    "4_4": "Registre éducatif : aucune promesse, aucun protocole d'usage.",
}

def apply_repl(text):
    for a, b in REPL:
        text = text.replace(a, b)
    return text

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return s

def md_to_html(body_lines):
    out, para, ul, bq = [], [], [], []
    def flush_para():
        if para: out.append("      <p>" + " ".join(inline(x) for x in para) + "</p>"); para.clear()
    def flush_ul():
        if ul:
            out.append("      <ul>")
            out.extend("        <li>" + inline(x) + "</li>" for x in ul)
            out.append("      </ul>"); ul.clear()
    def flush_bq():
        if bq:
            out.append("      <blockquote>" + "<br>".join(inline(x) for x in bq) + "</blockquote>"); bq.clear()
    def flush_all(): flush_para(); flush_ul(); flush_bq()
    for raw in body_lines:
        line = raw.rstrip()
        st = line.strip()
        if st == "---" or st == "":
            flush_all(); continue
        if st.startswith("## "):
            flush_all(); out.append("      <h2>" + inline(st[3:]) + "</h2>"); continue
        if st.startswith("# "):
            continue
        if st.startswith("- "):
            flush_para(); flush_bq(); ul.append(st[2:]); continue
        if st.startswith(">"):
            flush_para(); flush_ul(); bq.append(st.lstrip("> ").strip()); continue
        if st.startswith("*") and st.endswith("*") and "Article" in st:
            continue  # "*Article suivant : ...*"
        flush_ul(); flush_bq(); para.append(st)
    flush_all()
    return "\n".join(out)

TPL = """<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{desc}">
  <title>{title} — Ressources IVIA</title>
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://ivia.quebec/ressources/{slug}.html">
  <meta property="og:image" content="https://ivia.quebec/assets/og-praticiens.png">
  <script type="application/ld+json">
  {{ "@context":"https://schema.org","@type":"Article","headline":"{title_js}","description":"{desc_js}","author":{{"@type":"Organization","name":"IVIA"}},"publisher":{{"@type":"Organization","name":"IVIA","url":"https://ivia.quebec"}},"inLanguage":"fr-CA","isAccessibleForFree":true,"url":"https://ivia.quebec/ressources/{slug}.html" }}
  </script>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;0,700;1,400&family=Raleway:wght@400;500;600;700&display=swap" rel="stylesheet">
  <script>tailwind.config={{theme:{{extend:{{colors:{{forest:'#4A7C59',sage:'#8FB99A','forest-deep':'#2D6A4F',cream:'#FAFDF8',surface:'#F0F7F2',ink:'#1A2E1D',muted:'#4B6350',bdr:'#D4E8D0',camerise:'#4C2A86',agrume:'#E8943A',night:'#15121E'}},fontFamily:{{heading:['"Lora"','Georgia','serif']}}}}}}}}</script>
  <style>
    body{{font-family:'Raleway',system-ui,sans-serif;background:#FAFDF8;color:#1A2E1D;}}
    h1,h2,h3{{font-family:'Lora',Georgia,serif;}}
    .prose-ivia p{{margin:0 0 1.1rem;line-height:1.75;color:#2c3a30;}}
    .prose-ivia h2{{font-size:1.5rem;font-weight:700;color:#1A2E1D;margin:2.2rem 0 .8rem;}}
    .prose-ivia ul{{margin:0 0 1.1rem 1.1rem;list-style:disc;}}
    .prose-ivia li{{margin:.3rem 0;line-height:1.7;color:#2c3a30;}}
    .prose-ivia blockquote{{border-left:3px solid #E8943A;padding:.2rem 0 .2rem 1.1rem;margin:1.4rem 0;font-style:italic;color:#4B6350;}}
    .prose-ivia strong{{color:#1A2E1D;}}
  </style>
</head>
<body class="antialiased">

  <nav class="sticky top-0 z-50 bg-night/95 backdrop-blur border-b border-white/10">
    <div class="max-w-3xl mx-auto px-5 py-3 flex items-center justify-between gap-3">
      <a href="/ressources/" class="flex items-center gap-2 text-sm font-semibold text-white/80 hover:text-white">← Ressources</a>
      <a href="/" class="flex items-center gap-2 font-heading text-lg font-semibold text-white">
        <svg width="22" height="22" viewBox="0 0 28 28" fill="none" aria-hidden="true"><rect width="28" height="28" rx="7" fill="#4C2A86"/><rect x="7" y="11" width="3.5" height="6" rx="1.75" fill="white"/><rect x="12.25" y="7" width="3.5" height="14" rx="1.75" fill="white"/><rect x="17.5" y="9" width="3.5" height="10" rx="1.75" fill="white"/></svg>
        IVIA
      </a>
    </div>
  </nav>

  <article class="max-w-3xl mx-auto px-5 py-14">
    <p class="text-xs font-bold uppercase tracking-[0.14em] text-camerise mb-4">{section}</p>
    <h1 class="font-heading text-4xl sm:text-5xl font-bold text-ink leading-[1.08] mb-5">{title}</h1>
    <p class="text-sm text-muted mb-10">Lecture libre · ~5 min · par IVIA</p>

    <div class="prose-ivia text-[17px]">
{content}
    </div>

    <div class="mt-12 bg-surface border border-bdr rounded-[16px] px-5 py-4">
      <p class="text-sm text-muted leading-relaxed"><strong class="text-ink">Le cadre.</strong> Cet article est éducatif. IVIA est un service non clinique : il ne pose aucun nom sur ce que vous vivez et ne remplace aucun avis professionnel.{extra} En situation de crise : <strong class="text-ink">1 866 APPELLE (277-3553)</strong>.</p>
    </div>

    <div class="mt-10">
      <p class="text-xs font-bold uppercase tracking-[0.14em] text-camerise mb-3">Pour aller plus loin</p>
      <div class="flex flex-col gap-2">
{related}
      </div>
    </div>

    <div class="mt-8 flex flex-wrap gap-3">
      <a href="/ressources/" class="border border-bdr text-forest-deep font-semibold px-5 py-3 rounded-full hover:bg-surface transition-colors">← Toutes les ressources</a>
      <a href="/#offres" class="bg-camerise text-white font-semibold px-5 py-3 rounded-full hover:bg-night transition-colors">Ouvrir mon espace IVIA</a>
    </div>
  </article>

  <footer class="bg-night text-white/55 py-8 px-5">
    <div class="max-w-3xl mx-auto text-xs text-center">IVIA — <em>In Vivo, In Actu</em> · Le labo du vivant · 🍁</div>
  </footer>

</body>
</html>
"""

def main():
    titles = {}
    # 1re passe : titres
    for num, (slug, section, rel) in META.items():
        p = os.path.join(SRC, f"IVIA_ARTICLE_{num}_v1.0.md")
        with open(p, encoding="utf-8") as f:
            first = f.readline()
        titles[num] = apply_repl(first.lstrip("# ").strip())
    # 2e passe : generation
    for num, (slug, section, rel) in META.items():
        p = os.path.join(SRC, f"IVIA_ARTICLE_{num}_v1.0.md")
        text = apply_repl(open(p, encoding="utf-8").read())
        lines = text.split("\n")
        title = titles[num]
        dash = [i for i, l in enumerate(lines) if l.strip() == "---"]
        body_start = dash[1] + 1 if len(dash) >= 2 else 1
        content = md_to_html(lines[body_start:])
        # description : 1er paragraphe nettoye
        first_para = ""
        for l in lines[body_start:]:
            s = l.strip()
            if s and not s.startswith(("#", "-", ">", "*", "---")):
                first_para = re.sub(r"\*\*(.+?)\*\*", r"\1", s); break
        desc = (first_para[:155]).strip()
        related = "\n".join(
            f'        <a href="/ressources/{META[r][0]}.html" class="text-sm text-forest-deep font-semibold hover:underline">→ {titles[r]}</a>'
            for r in rel
        )
        extra = ""
        if num in EXTRA_NOTE:
            extra = " " + EXTRA_NOTE[num]
        out_html = TPL.format(
            title=html.escape(title, quote=True), title_js=title.replace('"', "'"),
            desc=html.escape(desc, quote=True), desc_js=desc.replace('"', "'"),
            slug=slug, section=section, content=content, related=related, extra=extra,
        )
        with open(os.path.join(OUT, f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(out_html)
        print(f"OK {num} -> {slug}.html")

if __name__ == "__main__":
    main()

"""Génère les pages des 3 interfaces IVIA à partir de templates partagés.
Header / footer / vrille communs ; contenu spécifique par page.
"""
from pathlib import Path

ROOT = Path(__file__).parent

# ---------------------------------------------------------------- partials
LOGO = '''<svg class="brand__mark" viewBox="0 0 36 36" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true">
  <circle cx="18" cy="18" r="14.5" stroke-opacity="0.4"/>
  <path d="M18 4.5 C 11 12, 25 24, 18 31.5" stroke-linecap="round"/>
  <path d="M11 18 C 14 16, 22 20, 25 18" stroke-linecap="round" stroke-opacity="0.7"/>
  <circle cx="18" cy="18" r="2.5" fill="currentColor" stroke="none"/>
</svg>'''

VRILLE = '''<div class="vrille-fixe" aria-hidden="true">
  <svg viewBox="0 0 500 800" fill="none" xmlns="http://www.w3.org/2000/svg">
    <defs><linearGradient id="vg" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0%" stop-color="#C58A8A" stop-opacity="0.8"/>
      <stop offset="50%" stop-color="#D9A441" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="#6B8266" stop-opacity="0.4"/>
    </linearGradient></defs>
    <path d="M 250 0 C 100 200, 400 350, 200 500 C 50 650, 350 750, 250 800" stroke="url(#vg)" stroke-width="1.5" fill="none"/>
    <path d="M 280 0 C 130 220, 430 360, 230 510 C 80 660, 380 760, 280 800" stroke="#C58A8A" stroke-width="0.8" stroke-opacity="0.4" fill="none"/>
    <ellipse cx="200" cy="180" rx="14" ry="5" fill="#6B8266" fill-opacity="0.3" transform="rotate(-30 200 180)"/>
    <ellipse cx="320" cy="280" rx="12" ry="4" fill="#D89260" fill-opacity="0.3" transform="rotate(20 320 280)"/>
    <ellipse cx="180" cy="430" rx="16" ry="6" fill="#C58A8A" fill-opacity="0.35" transform="rotate(-15 180 430)"/>
    <ellipse cx="290" cy="600" rx="13" ry="5" fill="#9A8AB8" fill-opacity="0.3" transform="rotate(40 290 600)"/>
  </svg>
</div>'''


def header(nav_items, current_page, actions_html, brand_link="index.html"):
    nav_html = "\n".join(
        f'      <a href="{href}"{" aria-current=\"page\"" if href == current_page else ""}>{label}</a>'
        for href, label in nav_items
    )
    return f'''<header class="site-header">
  <div class="container site-header__inner">
    <a href="{brand_link}" class="brand" aria-label="IVIA — accueil">
      {LOGO}
      <span class="brand__name">IV<em>I</em>A</span>
    </a>
    <nav class="nav" aria-label="Navigation principale">
{nav_html}
    </nav>
    <div class="header-actions">
      <button class="mode-calme-toggle" data-mode-calme aria-pressed="false" aria-label="Activer le mode calme">
        <span aria-hidden="true">◐</span> Mode calme
      </button>
      {actions_html}
    </div>
  </div>
</header>'''


CLIENT_NAV = [
    ("index.html", "Accueil"),
    ("praticiens.html", "Praticiens"),
    ("ressources.html", "Ressources"),
    ("rendez-vous.html", "Rendez-vous"),
    ("journal.html", "Journal"),
]
CLIENT_ACTIONS = '<a href="dashboard.html" class="btn btn--ghost btn--sm">Mon espace</a>'

PRATICIEN_NAV = [
    ("index.html", "Tableau de bord"),
    ("agenda.html", "Agenda"),
    ("audios.html", "Audios à traiter"),
    ("clients.html", "Mes clients"),
    ("mes-offres.html", "Mes offres"),
    ("outils.html", "Outils"),
    ("abonnement.html", "Mon abonnement"),
]
PRATICIEN_ACTIONS = '<a href="../client/index.html" class="btn btn--ghost btn--sm" style="opacity:0.7;">Vue client ↗</a>'

ADMIN_NAV = [
    ("index.html", "Vue d'ensemble"),
    ("analytique.html", "Analytique"),
    ("praticiens.html", "Praticiens"),
    ("clients.html", "Clients"),
    ("finance.html", "Finance"),
    ("audios.html", "Audios"),
    ("parametres.html", "Paramètres"),
]
ADMIN_ACTIONS = '<a href="../client/index.html" class="btn btn--ghost btn--sm" style="opacity:0.7;">Vue publique ↗</a>'


FOOTER_CLIENT = '''<footer class="site-footer">
  <div class="container">
    <div class="site-footer__cols">
      <div>
        <p style="font-family: var(--font-display); font-size:1.6rem; margin-bottom:1rem;">IV<em style="font-style:italic; color: var(--color-rose);">I</em>A</p>
        <p style="opacity:0.85; max-width:32ch; font-family:var(--font-serif); font-style:italic;">Au sein de l'être — En actes.</p>
        <p style="opacity:0.5; margin-top:1rem; font-size:var(--text-xs); letter-spacing:0.16em; text-transform:uppercase;">In vivo · In actu</p>
      </div>
      <div><h4>Découvrir</h4><ul role="list">
        <li><a href="index.html">Accueil</a></li>
        <li><a href="praticiens.html">Praticiens</a></li>
        <li><a href="ressources.html">Ressources</a></li>
        <li><a href="journal.html">Journal de vie</a></li>
      </ul></div>
      <div><h4>Pratique</h4><ul role="list">
        <li><a href="rendez-vous.html">Prendre rendez-vous</a></li>
        <li><a href="inscription.html">S'enregistrer</a></li>
        <li><a href="dashboard.html">Mon espace</a></li>
        <li><a href="#">Nous écrire</a></li>
      </ul></div>
      <div><h4>Mentions</h4><ul role="list">
        <li><a href="#">Mentions légales</a></li>
        <li><a href="#">Confidentialité (Loi 25)</a></li>
        <li><a href="#">CGU</a></li>
        <li><a href="../index.html">↩ Retour mockups</a></li>
      </ul></div>
    </div>
    <div class="site-footer__bottom">
      <span>© 2026 IVIA — Pour le peuple, par le peuple.</span>
      <span>IVIA n'est pas un service d'urgence et ne pose pas de diagnostic.</span>
    </div>
  </div>
</footer>'''

FOOTER_INTERNE = '''<footer class="site-footer" style="margin-top:var(--space-16); padding-block:var(--space-8);">
  <div class="container site-footer__bottom" style="border:none; padding-top:0;">
    <span>© 2026 IVIA · Espace de travail interne</span>
    <span><a href="../index.html">↩ Retour mockups</a></span>
  </div>
</footer>'''


def page(title, description, nav_items, current_page, actions_html, body_html,
         brand_link="index.html", footer=FOOTER_CLIENT, css_extra="", body_class=""):
    head_extra = f"<style>{css_extra}</style>" if css_extra else ""
    return f'''<!DOCTYPE html>
<html lang="fr-CA" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..600;1,9..144,300..600&family=Lora:ital,wght@0,400..600;1,400..500&family=Inter:wght@300..600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../shared/coupe.css">
{head_extra}
</head>
<body class="{body_class}">
{VRILLE}
{header(nav_items, current_page, actions_html, brand_link)}
{body_html}
{footer}
<script src="../shared/coupe.js"></script>
</body>
</html>'''


# Dispatcher : importe les modules de pages
if __name__ == "__main__":
    import importlib, sys
    sys.path.insert(0, str(ROOT))
    for module_name in ["pages_client", "pages_funnel", "pages_praticien", "pages_admin", "page_index", "pages_public"]:
        try:
            mod = importlib.import_module(module_name)
            mod.build()
            print(f"✓ {module_name} construit")
        except Exception as e:
            print(f"✗ {module_name} : {e}")
            raise

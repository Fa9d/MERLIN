# -*- coding: utf-8 -*-
"""Genere ivia_site_v2/ressources/index.html — la mediatheque vivante IVIA.

Hub a rails horizontaux (decouverte), ambiance bibliotheque editoriale sobre.
- Hero leger : icone Lucide 'library' + 'IVIA – Ressources' + recherche + acces rapides.
- 8 rails : chaque rail = titre + 'Tout voir' + fleches (desktop) + scroll tactile (mobile).
- Cartes : couverture editoriale (motif organique tinte par theme), badge type, titre, duree.
- Recherche : filtre client live (insensible aux accents) sur titre/theme/type/tags.
- Conserve les ancres #th-ecoute… (les pages d'articles y pointent).
A relancer si le catalogue change.
"""
import html
import os

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "ivia_site_v2", "ressources", "index.html"))

# couleur d'accent par theme (coherente avec les articles)
COL = {
    "Écoute & relation":    "#4C2A86",  # camerise
    "Équilibre & vivant":   "#2D6A4F",  # forest
    "Empathie & société":   "#C6447B",  # pulpe
    "Fréquence & présence": "#E8943A",  # agrume
    "Littératie":           "#4C2A86",
    "Régénération":         "#E8943A",
}

# catalogue : slug -> (titre carte, type, duree, theme, tags de recherche)
CAT = {
    "ecoute-qui-respecte-le-vivant": ("Une écoute qui respecte le vivant", "Article", "~5 min", "Écoute & relation", "ecoute presence relation"),
    "empathie-ethique":              ("Empathie éthique : ressentir sans se perdre", "Article", "~5 min", "Écoute & relation", "empathie ecoute"),
    "lois-de-l-echange":             ("Les lois de l'échange", "Article", "~5 min", "Écoute & relation", "echange lien relation"),
    "responsabilite-et-dignite":     ("La responsabilité comme dignité", "Article", "~5 min", "Écoute & relation", "responsabilite dignite"),
    "penser-sa-vie-en-cycles":       ("Penser sa vie en cycles", "Article", "~5 min", "Équilibre & vivant", "cycles equilibre rythme machine"),
    "le-cercle-carte-d-equilibre":   ("Le cercle, carte d'équilibre", "Article", "~5 min", "Équilibre & vivant", "cercle equilibre carte"),
    "economie-et-nature":            ("Quand l'économie oublie la nature", "Article", "~5 min", "Équilibre & vivant", "economie nature suzuki"),
    "habiter-son-corps":             ("Habiter son corps", "Article", "~5 min", "Équilibre & vivant", "corps presence regeneration"),
    "espaces-collectifs-qui-epuisent":("Ces espaces collectifs qui épuisent", "Article", "~5 min", "Empathie & société", "collectif groupe societe"),
    "empathie-et-pouvoir":           ("Quand l'empathie devient pouvoir", "Article", "~5 min", "Empathie & société", "empathie pouvoir"),
    "espaces-de-parole-vrais":       ("Créer des espaces de parole vrais", "Article", "~5 min", "Empathie & société", "parole espace groupe"),
    "de-la-performance-a-la-presence":("De la performance à la présence", "Article", "~5 min", "Empathie & société", "performance presence soin"),
    "tout-vibre":                    ("Tout vibre : ce que dit la physique", "Article", "~5 min", "Fréquence & présence", "frequence vibration physique"),
    "le-corps-instrument-de-presence":("Le corps, premier instrument de présence", "Article", "~5 min", "Fréquence & présence", "corps presence regeneration"),
    "le-savoir-des-plantes":         ("Plantes & minéraux : pistes de régénération", "Article", "~5 min", "Fréquence & présence", "plantes regeneration corps sommeil"),
    "frequence-et-autonomie":        ("Fréquence et autonomie", "Article", "~5 min", "Fréquence & présence", "frequence autonomie"),
    "plusieurs-regards":             ("Plusieurs regards sur ce que vous vivez", "Article", "~5 min", "Littératie", "modeles regards comprendre"),
    "le-vivant-sait":                ("Le vivant sait se régénérer", "Article", "~4 min", "Régénération", "regeneration sommeil corps vitalite"),
}

# placeholders (a venir) — type Outil
PLACE = {
    "auto-reperes":  ("Auto-repères du quotidien", "Outil", "Bientôt", "Régénération", "outil auto-reperes"),
    "detecteur":     ("Le détecteur de poudre de perlimpinpin", "Outil", "Bientôt", "Littératie", "outil detecteur arnaque"),
    "cartographie":  ("Cartographier votre cercle", "Outil", "Bientôt", "Équilibre & vivant", "outil cercle carte"),
}

# rails : (id, titre, data-q pour 'Tout voir', [slugs ou place:ids])
RAILS = [
    ("commencer", "Commencer avec IVIA", "", [
        "plusieurs-regards", "ecoute-qui-respecte-le-vivant", "penser-sa-vie-en-cycles", "le-vivant-sait", "espaces-de-parole-vrais"]),
    ("th-ecoute", "Écoute & relation", "ecoute", [
        "ecoute-qui-respecte-le-vivant", "empathie-ethique", "lois-de-l-echange", "responsabilite-et-dignite", "plusieurs-regards"]),
    ("th-equilibre", "Équilibre & vivant", "equilibre", [
        "penser-sa-vie-en-cycles", "le-cercle-carte-d-equilibre", "economie-et-nature", "habiter-son-corps"]),
    ("th-empathie", "Empathie & société", "empathie", [
        "espaces-collectifs-qui-epuisent", "empathie-et-pouvoir", "espaces-de-parole-vrais", "de-la-performance-a-la-presence"]),
    ("th-frequence", "Fréquence & présence", "frequence", [
        "tout-vibre", "le-corps-instrument-de-presence", "le-savoir-des-plantes", "frequence-et-autonomie"]),
    ("regeneration", "Sommeil & régénération", "regeneration", [
        "le-vivant-sait", "le-savoir-des-plantes", "habiter-son-corps", "le-corps-instrument-de-presence", "penser-sa-vie-en-cycles"]),
    ("outils", "Outils & auto-repères", "outil", [
        "place:auto-reperes", "place:detecteur", "place:cartographie"]),
    ("nouveautes", "Nouveautés", "", [
        "plusieurs-regards", "le-savoir-des-plantes", "frequence-et-autonomie", "de-la-performance-a-la-presence", "le-vivant-sait"]),
]

# ── Icones Lucide (inline, MIT) ──────────────────────────────────────────────
def lucide(name, cls="w-5 h-5"):
    P = {
        "library": '<path d="m16 6 4 14"/><path d="M12 6v14"/><path d="M8 8v12"/><path d="M4 4v16"/>',
        "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
        "file-text": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>',
        "play": '<polygon points="6 3 20 12 6 21 6 3"/>',
        "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
        "audio-lines": '<path d="M2 10v3"/><path d="M6 6v11"/><path d="M10 3v18"/><path d="M14 8v7"/><path d="M18 5v13"/><path d="M22 10v3"/>',
        "chevron-left": '<path d="m15 18-6-6 6-6"/>',
        "chevron-right": '<path d="m9 18 6-6-6-6"/>',
    }
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{P[name]}</svg>')

TYPE_ICON = {"Article": "file-text", "Vidéo": "play", "Outil": "wrench", "Audio": "audio-lines"}

MOTIF = ('<svg class="absolute inset-0 w-full h-full" viewBox="0 0 200 150" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
         '<g fill="none" stroke="var(--a)" stroke-width="1.5" opacity="0.22">'
         '<path d="M-10 95 C 40 65, 80 115, 130 80 S 220 55, 230 85"/>'
         '<path d="M-10 115 C 40 85, 80 135, 130 100 S 220 75, 230 105"/>'
         '<path d="M-10 135 C 40 105, 80 150, 130 120 S 220 95, 230 125"/>'
         '</g></svg>')


def short_theme(theme):
    return theme.split(" &")[0] if "&" in theme else theme


def card_html(key):
    place = key.startswith("place:")
    if place:
        cid = key.split(":", 1)[1]
        title, typ, dur, theme, tags = PLACE[cid]
        href = None
    else:
        title, typ, dur, theme, tags = CAT[key]
        href = f"/ressources/{key}.html"
    accent = COL[theme]
    badge = (f'<span class="absolute top-3 left-3 inline-flex items-center gap-1.5 bg-white/90 backdrop-blur '
             f'text-[11px] font-bold rounded-full pl-2 pr-2.5 py-1" style="color:{accent}">'
             f'{lucide(TYPE_ICON[typ], "w-3.5 h-3.5")}{typ}</span>')
    soon = '<span class="absolute top-3 right-3 text-[10px] font-bold uppercase tracking-wider text-muted bg-white/85 rounded-full px-2 py-1">Bientôt</span>' if place else ''
    cover = (f'<div class="cover relative rounded-[16px] overflow-hidden border border-bdr" style="--a:{accent};background:{accent}12">'
             f'{MOTIF}{badge}{soon}</div>')
    meta = (f'<p class="text-[11px] text-muted mt-3 mb-1"><span class="font-semibold" style="color:{accent}">'
            f'{html.escape(short_theme(theme))}</span> · {html.escape(dur)}</p>')
    h3 = f'<h3 class="font-heading text-[15px] font-bold text-ink leading-snug">{html.escape(title)}</h3>'
    data = html.escape(f"{title} {theme} {typ} {tags}".lower(), quote=True)
    inner = cover + '\n        <div class="px-0.5">' + meta + h3 + '</div>'
    if href:
        return (f'      <a class="card group" href="{href}" role="listitem" data-tags="{data}">\n'
                f'        {inner}\n      </a>')
    return (f'      <div class="card opacity-80" role="listitem" data-tags="{data}" aria-disabled="true">\n'
            f'        {inner}\n      </div>')


def rail_html(rid, title, q, keys):
    cards = "\n".join(card_html(k) for k in keys)
    voir = (f'<button type="button" class="voir-tout text-sm font-semibold text-forest-deep hover:underline whitespace-nowrap shrink-0" '
            f'data-q="{html.escape(q, quote=True)}">Tout voir →</button>')
    arrows = (
        f'<button type="button" class="rail-arrow rail-prev" aria-label="Faire défiler vers la gauche">{lucide("chevron-left","w-5 h-5")}</button>'
        f'<button type="button" class="rail-arrow rail-next" aria-label="Faire défiler vers la droite">{lucide("chevron-right","w-5 h-5")}</button>')
    return f"""  <section class="rail max-w-6xl mx-auto px-5 mt-12 scroll-mt-24" id="{rid}" aria-labelledby="{rid}-t">
    <div class="flex items-end justify-between gap-4 mb-4">
      <h2 id="{rid}-t" class="font-heading text-2xl font-bold text-ink">{html.escape(title)}</h2>
      {voir}
    </div>
    <div class="rail-viewport at-start at-end">
      <div class="rail-track" role="list">
{cards}
      </div>
      <div class="rail-fade rail-fade-l" aria-hidden="true"></div>
      <div class="rail-fade rail-fade-r" aria-hidden="true"></div>
      {arrows}
    </div>
  </section>"""


HEAD = """<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Ressources IVIA — une médiathèque vivante : articles, outils et contenus éditoriaux pour comprendre vos besoins et soutenir le vivant. Sobre, libre, fièrement québécois.">
  <title>IVIA – Ressources · Le labo du vivant</title>
  <meta property="og:title" content="IVIA – Ressources">
  <meta property="og:description" content="Une médiathèque vivante : articles, outils et contenus éditoriaux. Sobre, libre, québécois.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://ivia.quebec/ressources/">
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;0,700;1,400&family=Raleway:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <script>tailwind.config={theme:{extend:{colors:{forest:'#4A7C59',sage:'#8FB99A','forest-deep':'#2D6A4F',cream:'#FAFDF8',surface:'#F0F7F2',ink:'#1A2E1D',muted:'#4B6350',bdr:'#D4E8D0',camerise:'#4C2A86',agrume:'#E8943A',pulpe:'#C6447B',night:'#15121E'},fontFamily:{heading:['"Lora"','Georgia','serif']}}}}</script>
  <style>
    body{font-family:'Raleway',system-ui,sans-serif;background:#FAFDF8;color:#1A2E1D;}
    h1,h2,h3{font-family:'Lora',Georgia,serif;}
    /* Rails */
    .rail-track{display:flex;gap:1rem;overflow-x:auto;scroll-snap-type:x mandatory;scroll-padding:0 1.25rem;padding:.4rem .25rem 1.2rem;scrollbar-width:none;-webkit-overflow-scrolling:touch;}
    .rail-track::-webkit-scrollbar{display:none;}
    .card{scroll-snap-align:start;flex:0 0 clamp(210px,72vw,250px);text-decoration:none;}
    .card .cover{aspect-ratio:4/3;}
    .card h3{transition:color .15s ease;}
    .card:hover h3{color:var(--a,#2D6A4F);}
    .card .cover{transition:transform .2s ease, box-shadow .2s ease;}
    .card:hover .cover{transform:translateY(-3px);box-shadow:0 16px 32px -18px rgba(26,46,29,.35);}
    .card:focus-visible{outline:none;}
    .card:focus-visible .cover{outline:2px solid var(--a,#2D6A4F);outline-offset:3px;}
    .rail-empty{display:none;}
    /* Viewport + flèches "Netflix" par-dessus les vignettes (au survol) */
    .rail-viewport{position:relative;}
    .rail-arrow{position:absolute;top:34%;transform:translateY(-50%);z-index:20;width:46px;height:46px;border-radius:9999px;background:#fff;border:1px solid #D4E8D0;box-shadow:0 10px 26px -10px rgba(26,46,29,.45);display:flex;align-items:center;justify-content:center;color:#1A2E1D;opacity:0;transition:opacity .22s ease, transform .18s ease;cursor:pointer;}
    .rail-prev{left:-6px;} .rail-next{right:-6px;}
    .rail-arrow:hover{transform:translateY(-50%) scale(1.07);background:#F0F7F2;}
    .rail-fade{position:absolute;top:.4rem;bottom:1.2rem;width:64px;z-index:10;pointer-events:none;opacity:0;transition:opacity .22s ease;}
    .rail-fade-l{left:0;background:linear-gradient(to right,#FAFDF8 28%,rgba(250,253,248,0));}
    .rail-fade-r{right:0;background:linear-gradient(to left,#FAFDF8 28%,rgba(250,253,248,0));}
    @media (hover:hover){
      .rail-viewport:hover .rail-arrow{opacity:1;}
      .rail-viewport:hover .rail-fade{opacity:1;}
    }
    .rail-viewport.at-start .rail-prev,.rail-viewport.at-start .rail-fade-l{opacity:0 !important;pointer-events:none;}
    .rail-viewport.at-end .rail-next,.rail-viewport.at-end .rail-fade-r{opacity:0 !important;pointer-events:none;}
    /* Apparition douce des rails à l'entrée dans le viewport */
    .reveal-on .rail{opacity:0;transform:translateY(20px);transition:opacity .6s ease, transform .6s ease;}
    .reveal-on .rail.in{opacity:1;transform:none;}
    @media (prefers-reduced-motion: reduce){
      .card:hover .cover{transform:none;}
      .rail-arrow{transition:none;}
      .reveal-on .rail{opacity:1 !important;transform:none !important;transition:none !important;}
    }
  </style>
</head>
<body class="antialiased">

  <!-- NAV -->
  <nav class="sticky top-0 z-50 bg-night/95 backdrop-blur border-b border-white/10">
    <div class="max-w-6xl mx-auto px-5 py-3 flex items-center justify-between gap-4 flex-wrap">
      <a href="/ressources/" class="flex items-center gap-2 font-heading text-lg font-semibold text-white shrink-0">
        <svg width="26" height="26" viewBox="0 0 28 28" fill="none" aria-hidden="true"><rect width="28" height="28" rx="7" fill="#4C2A86"/><rect x="7" y="11" width="3.5" height="6" rx="1.75" fill="white"/><rect x="12.25" y="7" width="3.5" height="14" rx="1.75" fill="white"/><rect x="17.5" y="9" width="3.5" height="10" rx="1.75" fill="white"/></svg>
        IVIA <span class="text-agrume font-normal text-sm">· ressources</span>
      </a>
      <div class="flex items-center gap-3 sm:gap-4 text-xs sm:text-sm font-medium flex-wrap">
        <a href="#th-ecoute" class="text-white/70 hover:text-white transition-colors">Écoute</a>
        <a href="#th-equilibre" class="text-white/70 hover:text-white transition-colors">Équilibre</a>
        <a href="#th-empathie" class="text-white/70 hover:text-white transition-colors">Empathie</a>
        <a href="#th-frequence" class="text-white/70 hover:text-white transition-colors">Fréquence</a>
        <a href="/" class="text-white/90 hover:text-white transition-colors">Retour&nbsp;↗</a>
      </div>
    </div>
  </nav>
"""

HERO = f"""
  <!-- HERO editorial leger -->
  <header class="bg-cream border-b border-bdr">
    <div class="max-w-6xl mx-auto px-5 pt-12 pb-10">
      <div class="flex items-start gap-4 mb-6">
        <span class="shrink-0 w-12 h-12 rounded-[14px] bg-surface text-forest-deep border border-bdr flex items-center justify-center">{lucide('library','w-6 h-6')}</span>
        <div>
          <h1 class="font-heading text-3xl sm:text-4xl font-bold text-ink leading-tight">IVIA – Ressources</h1>
          <p class="text-muted text-sm sm:text-base mt-1 max-w-xl">Une médiathèque vivante — articles, outils et repères à parcourir à votre rythme. Sobre, libre, sans poudre magique.</p>
        </div>
      </div>

      <div class="relative max-w-xl">
        <span class="absolute left-4 top-1/2 -translate-y-1/2 text-muted">{lucide('search','w-5 h-5')}</span>
        <input id="ressources-search" type="search" autocomplete="off"
               placeholder="Chercher un sujet, un thème, un type…"
               aria-label="Rechercher dans les ressources"
               class="w-full bg-white border border-bdr rounded-full pl-12 pr-4 py-3.5 text-sm text-ink placeholder:text-muted focus:outline-none focus:ring-2 focus:ring-forest/40 focus:border-forest">
      </div>

      <div class="flex flex-wrap gap-2 mt-5" aria-label="Accès rapides">
        <a href="#commencer" class="text-xs font-semibold text-forest-deep bg-surface border border-bdr rounded-full px-4 py-2 hover:border-forest transition-colors">Par où commencer</a>
        <a href="#regeneration" class="text-xs font-semibold text-forest-deep bg-surface border border-bdr rounded-full px-4 py-2 hover:border-forest transition-colors">Sommeil &amp; régénération</a>
        <a href="#nouveautes" class="text-xs font-semibold text-forest-deep bg-surface border border-bdr rounded-full px-4 py-2 hover:border-forest transition-colors">Nouveautés</a>
      </div>

      <p id="no-results" class="hidden text-sm text-muted mt-6">Aucune ressource ne correspond. <button type="button" id="clear-search" class="text-forest-deep font-semibold hover:underline">Tout afficher</button></p>
    </div>
  </header>

  <main class="pb-8">
"""

CADRE_FOOTER = """  </main>

  <!-- BANDEAU CADRE (Loi 21/25 + attribution) -->
  <section class="bg-surface border-y border-bdr mt-14">
    <div class="max-w-4xl mx-auto px-5 py-10 text-center">
      <p class="text-sm text-ink leading-relaxed">
        <strong>Le cadre, clairement.</strong> IVIA n'est pas un service médical et ne remplace
        aucun avis professionnel. Ici on éduque, on oriente, on s'émerveille du vivant — on ne
        promet rien et on ne vend pas de miracle. Les savoirs des Premières Nations sont cités
        avec respect et attribution, jamais appropriés. Données hébergées au Québec (Loi 25).
      </p>
    </div>
  </section>

  <footer class="bg-night text-white/60 py-10 px-5">
    <div class="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3 text-xs">
      <p>IVIA — <em>In Vivo, In Actu</em> · Le labo du vivant · fièrement québécois 🍁</p>
      <p>Pas un service d'urgence · En crise : <strong class="text-white"><a href="tel:18662773553" class="underline">1 866 APPELLE</a></strong></p>
    </div>
  </footer>

  <script>
    // Révélation progressive activée (sans JS, les rails restent visibles)
    document.documentElement.classList.add('reveal-on');

    // ── Rails : flèches "Netflix" + état début/fin de course ─────────────────
    document.querySelectorAll('.rail').forEach(function (rail) {
      var vp = rail.querySelector('.rail-viewport');
      var track = rail.querySelector('.rail-track');
      var prev = rail.querySelector('.rail-prev');
      var next = rail.querySelector('.rail-next');
      function step() {
        var c = track.querySelector('.card');
        return c ? c.getBoundingClientRect().width + 16 : 240;
      }
      function update() {
        var max = track.scrollWidth - track.clientWidth - 2;
        vp.classList.toggle('at-start', track.scrollLeft <= 2);
        vp.classList.toggle('at-end', max <= 0 || track.scrollLeft >= max);
      }
      if (prev) prev.addEventListener('click', function () { track.scrollBy({ left: -step() * 2, behavior: 'smooth' }); });
      if (next) next.addEventListener('click', function () { track.scrollBy({ left: step() * 2, behavior: 'smooth' }); });
      track.addEventListener('scroll', update, { passive: true });
      window.addEventListener('resize', update);
      update();
    });

    // ── Apparition douce des rails à l'entrée dans le viewport ───────────────
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
      }, { threshold: 0.08 });
      document.querySelectorAll('.rail').forEach(function (r) { io.observe(r); });
    } else {
      document.querySelectorAll('.rail').forEach(function (r) { r.classList.add('in'); });
    }

    // ── Recherche / filtre (insensible aux accents) ──────────────────────────
    var input = document.getElementById('ressources-search');
    var noRes = document.getElementById('no-results');
    function norm(s) { return (s || '').toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g, ''); }
    function applyFilter(q) {
      var nq = norm(q.trim());
      var anyVisible = false;
      document.querySelectorAll('.rail').forEach(function (rail) {
        var shown = 0;
        rail.querySelectorAll('.card').forEach(function (card) {
          var match = !nq || norm(card.getAttribute('data-tags')).indexOf(nq) !== -1;
          card.style.display = match ? '' : 'none';
          if (match) shown++;
        });
        rail.classList.toggle('rail-empty', shown === 0);
        if (shown > 0) anyVisible = true;
      });
      noRes.classList.toggle('hidden', anyVisible || nq === '');
      window.dispatchEvent(new Event('resize'));
    }
    if (input) input.addEventListener('input', function () { applyFilter(input.value); });

    // 'Tout voir' → remplit la recherche avec le mot-clé du rail
    document.querySelectorAll('.voir-tout').forEach(function (b) {
      b.addEventListener('click', function () {
        input.value = b.getAttribute('data-q') || '';
        applyFilter(input.value);
        window.scrollTo({ top: 0, behavior: 'smooth' });
        input.focus();
      });
    });

    var clr = document.getElementById('clear-search');
    if (clr) clr.addEventListener('click', function () { input.value = ''; applyFilter(''); input.focus(); });
  </script>

</body>
</html>
"""


def main():
    rails = "\n\n".join(rail_html(rid, title, q, keys) for rid, title, q, keys in RAILS)
    doc = HEAD + HERO + rails + "\n" + CADRE_FOOTER
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"OK -> {OUT}  ({len(RAILS)} rails)")


if __name__ == "__main__":
    main()

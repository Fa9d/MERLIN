"""Pages publiques IVIA.quebec — landing, comment ça fonctionne, bibliothèque,
articles, ressources urgence, mentions légales, page tests (hub direct accès).

Ces pages constituent la VRAIE façade publique du site (versus le mockup démo
qui est déplacé sous /demo/).
"""
from pathlib import Path
from build_pages import LOGO, VRILLE
from articles_meta import all_articles, load_article, AXES, ARTICLES

ROOT = Path(__file__).parent

# ---------- Navigation publique ----------
PUBLIC_NAV = [
    ("index.html", "Accueil"),
    ("comment.html", "Comment ça fonctionne"),
    ("pourquoi.html", "Pourquoi IVIA"),
    ("bibliotheque.html", "Bibliothèque"),
    ("urgence.html", "Si c'est urgent"),
]

PUBLIC_ACTIONS = (
    '<a href="tests.html" class="btn btn--ghost btn--sm" style="opacity:0.85;">Espace tests</a>'
    '<a href="client/audio-async.html" class="btn btn--primary btn--sm">Commencer une écoute</a>'
)


def public_header(current):
    nav = "\n".join(
        f'      <a href="{href}"{" aria-current=\"page\"" if href == current else ""}>{label}</a>'
        for href, label in PUBLIC_NAV
    )
    return f'''<header class="site-header">
  <div class="container site-header__inner">
    <a href="index.html" class="brand" aria-label="IVIA — accueil">
      {LOGO}
      <span class="brand__name">IV<em>I</em>A</span>
    </a>
    <nav class="nav" aria-label="Navigation principale">
{nav}
    </nav>
    <div class="header-actions">
      <button class="mode-calme-toggle" data-mode-calme aria-pressed="false" aria-label="Activer le mode calme">
        <span aria-hidden="true">◐</span> Mode calme
      </button>
      {PUBLIC_ACTIONS}
    </div>
  </div>
</header>'''


PUBLIC_FOOTER = '''<footer class="site-footer">
  <div class="container">
    <div class="site-footer__cols">
      <div>
        <p style="font-family: var(--font-display); font-size:1.6rem; margin-bottom:1rem;">IV<em style="font-style:italic; color: var(--color-rose);">I</em>A</p>
        <p style="opacity:0.85; max-width:32ch; font-family:var(--font-serif); font-style:italic;">Au sein de l'être — En actes.</p>
        <p style="opacity:0.5; margin-top:1rem; font-size:var(--text-xs); letter-spacing:0.16em; text-transform:uppercase;">In vivo · In actu</p>
      </div>
      <div><h4>Découvrir</h4><ul role="list">
        <li><a href="index.html">Accueil</a></li>
        <li><a href="comment.html">Comment ça fonctionne</a></li>
        <li><a href="pourquoi.html">Pourquoi IVIA</a></li>
        <li><a href="bibliotheque.html">Bibliothèque</a></li>
        <li><a href="urgence.html">Si c'est urgent</a></li>
      </ul></div>
      <div><h4>Pratique</h4><ul role="list">
        <li><a href="client/audio-async.html">Commencer une écoute</a></li>
        <li><a href="client/journal.html">Journal de vie</a></li>
        <li><a href="tests.html">Espace tests</a></li>
        <li><a href="mailto:contact@ivia.quebec">Nous écrire</a></li>
      </ul></div>
      <div><h4>Mentions</h4><ul role="list">
        <li><a href="mentions.html">Mentions légales</a></li>
        <li><a href="confidentialite.html">Confidentialité (Loi 25)</a></li>
        <li><a href="cgu.html">Conditions d'utilisation</a></li>
        <li><a href="demo/index.html">Démo des interfaces</a></li>
      </ul></div>
    </div>
    <div class="site-footer__bottom">
      <span>© 2026 IVIA — Pour le peuple, par le peuple.</span>
      <span>IVIA n'est pas un service d'urgence et ne pose pas de diagnostic.</span>
    </div>
  </div>
</footer>'''


def public_page(title, description, current, body_html, css_extra="", body_class="public-page"):
    head_extra = f"<style>{css_extra}</style>" if css_extra else ""
    return f'''<!DOCTYPE html>
<html lang="fr-CA" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..600;1,9..144,300..600&family=Lora:ital,wght@0,400..600;1,400..500&family=Inter:wght@300..600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="shared/coupe.css">
<link rel="stylesheet" href="shared/public.css">
{head_extra}
</head>
<body class="{body_class}">
{VRILLE}
{public_header(current)}
{body_html}
{PUBLIC_FOOTER}
<script src="shared/coupe.js"></script>
</body>
</html>'''


# ============================================================================
# LANDING — index.html
# ============================================================================
def build_landing():
    body = '''
<main id="main">

  <!-- Hero officiel selon MERLIN_GOUV_PAGE_SITE_CLIENT -->
  <section class="public-hero">
    <div class="container public-hero__inner">
      <p class="public-hero__overline">Espace d'écoute · Québec · Conforme Loi 25</p>
      <h1 class="public-hero__title">
        Un espace d'<em>écoute</em><br>
        pour clarifier ce que vous vivez<br>
        <span class="public-hero__title-soft">et repartir avec une suite concrète.</span>
      </h1>
      <p class="public-hero__lede">
        Vous nous parlez. Nous vous renvoyons un résumé clair et trois pistes concrètes —
        sans jugement, sans diagnostic. À votre rythme.
      </p>
      <div class="public-hero__cta">
        <a href="client/audio-async.html" class="btn btn--primary btn--lg">Commencer une écoute</a>
        <a href="comment.html" class="btn btn--ghost btn--lg">Comprendre comment ça fonctionne</a>
      </div>
      <p class="public-hero__disclaimer">
        IVIA n'est pas un service d'urgence et ne pose pas de diagnostic.
        Si vous êtes en détresse, <a href="urgence.html">cliquez ici</a> ou composez le <strong>911</strong>.
      </p>
    </div>
  </section>

  <!-- Trois portes : c'est l'âme de la landing -->
  <section class="public-section">
    <div class="container">
      <p class="section-overline">Trois portes</p>
      <h2 class="section-title">Selon ce qui vous habite, en ce moment</h2>

      <div class="trois-portes">

        <a class="porte porte--ecoute" href="client/audio-async.html">
          <div class="porte__icon">
            <svg viewBox="0 0 60 60" fill="none" stroke="currentColor" stroke-width="1.4">
              <path d="M15 25 q-3 5 0 10 q3 5 0 10" stroke-linecap="round"/>
              <path d="M22 22 q-5 8 0 16 q5 8 0 16" stroke-linecap="round" stroke-opacity="0.6"/>
              <circle cx="35" cy="30" r="9"/>
              <path d="M35 39 v6 m-4 0 h8" stroke-linecap="round"/>
            </svg>
          </div>
          <h3>Vous voulez être écouté·e</h3>
          <p>Une séance audio avec un·e praticien·ne IVIA — en rendez-vous direct ou en différé selon ce qui vous convient. Vous recevez ensuite un résumé écrit et trois pistes concrètes.</p>
          <span class="porte__cta">Commencer une écoute →</span>
        </a>

        <a class="porte porte--lire" href="bibliotheque.html">
          <div class="porte__icon">
            <svg viewBox="0 0 60 60" fill="none" stroke="currentColor" stroke-width="1.4">
              <path d="M10 18 v32 q10 -3 20 0 q10 -3 20 0 v-32 q-10 -3 -20 0 q-10 -3 -20 0 z"/>
              <path d="M30 18 v32" stroke-opacity="0.5"/>
              <path d="M16 27 h10 M16 33 h10 M34 27 h10 M34 33 h10" stroke-opacity="0.5"/>
            </svg>
          </div>
          <h3>Vous voulez d'abord comprendre</h3>
          <p>Seize articles courts, écrits avec soin. L'écoute, l'équilibre, les frontières, la suite. Lisez sans engagement, à votre rythme.</p>
          <span class="porte__cta">Ouvrir la bibliothèque →</span>
        </a>

        <a class="porte porte--journal" href="client/journal.html">
          <div class="porte__icon">
            <svg viewBox="0 0 60 60" fill="none" stroke="currentColor" stroke-width="1.4">
              <circle cx="30" cy="30" r="20"/>
              <path d="M30 14 v32 M14 30 h32" stroke-opacity="0.4"/>
              <circle cx="30" cy="30" r="3" fill="currentColor"/>
              <path d="M30 30 l10 -10" stroke-linecap="round"/>
            </svg>
          </div>
          <h3>Vous voulez vous suivre dans le temps</h3>
          <p>Le journal de vie consigne vos écoutes, vos suites concrètes et l'évolution de vos cinq zones. Aucun diagnostic — un miroir vivant.</p>
          <span class="porte__cta">Découvrir le journal →</span>
        </a>

      </div>
    </div>
  </section>

  <!-- Ce que IVIA est et n'est pas -->
  <section class="public-section public-section--soft">
    <div class="container ce-quivia">
      <div>
        <p class="section-overline">Pour qu'on se comprenne</p>
        <h2 class="section-title">Ce qu'IVIA <em>est</em></h2>
        <ul class="puces puces--vert">
          <li>Un espace d'écoute audio — en direct ou en différé, selon votre rythme</li>
          <li>Un résumé clair, doux, sans jargon, écrit pour vous</li>
          <li>Trois pistes concrètes que vous choisissez de tenir ou non</li>
          <li>Un journal de vie qui suit vos cycles dans la durée</li>
          <li>Un espace conforme à la <strong>Loi 25 du Québec</strong></li>
        </ul>
      </div>
      <div>
        <p class="section-overline">&nbsp;</p>
        <h2 class="section-title">Ce qu'IVIA <em>n'est pas</em></h2>
        <ul class="puces puces--rose">
          <li>Pas un service d'urgence — pour ça, composez le 911</li>
          <li>Pas un diagnostic médical ou psychologique</li>
          <li>Pas une thérapie, pas un substitut à votre suivi en santé</li>
          <li>Pas une intelligence artificielle qui vous parle à la place d'un humain</li>
          <li>Pas un produit qui vous garde captif·ve — vous êtes libre à chaque étape</li>
        </ul>
      </div>
    </div>
  </section>

  <!-- Cycle visible : les 5 zones du cercle IVIA -->
  <section class="public-section">
    <div class="container">
      <p class="section-overline">Le cercle IVIA</p>
      <h2 class="section-title">Cinq zones, un seul vivant</h2>
      <p class="section-lede">L'humain n'est pas une liste de problèmes. Il est un système vivant. Le cercle nous aide à voir où l'énergie circule et où elle se bloque.</p>

      <div class="cercle-grid">
        <div class="zone zone--corps">
          <h3>Corps</h3>
          <p>Le sommeil, l'énergie, les sensations. Le premier témoin de ce qui se passe.</p>
        </div>
        <div class="zone zone--relation">
          <h3>Relation</h3>
          <p>Les liens, la place que vous prenez, celle que vous laissez aux autres.</p>
        </div>
        <div class="zone zone--sens">
          <h3>Sens</h3>
          <p>Ce qui compte pour vous. Ce qui vous met en mouvement le matin.</p>
        </div>
        <div class="zone zone--ressources">
          <h3>Ressources</h3>
          <p>Le temps, l'argent, le réseau. Ce qui rend possible — ou ce qui contraint.</p>
        </div>
        <div class="zone zone--frequence">
          <h3>Fréquence</h3>
          <p>Le rythme. Pas une croyance — un état du vivant. Haut, bas, en équilibre.</p>
        </div>
      </div>

      <p class="section-foot"><a href="bibliotheque.html#axe-equilibre">Lire « Les cinq zones du cercle IVIA » →</a></p>
    </div>
  </section>

  <!-- Le parcours en 4 étapes -->
  <section class="public-section public-section--soft">
    <div class="container">
      <p class="section-overline">Comment ça se passe</p>
      <h2 class="section-title">Quatre étapes, à votre rythme</h2>

      <ol class="parcours">
        <li>
          <span class="parcours__num">1</span>
          <h3>Vous parlez</h3>
          <p>Au calme, depuis chez vous, en une fois ou plusieurs prises. Aucun temps minimum.</p>
        </li>
        <li>
          <span class="parcours__num">2</span>
          <h3>Nous écoutons</h3>
          <p>Une praticienne ou un praticien IVIA reçoit votre audio. Notre outil interne propose des pistes — l'humain décide toujours.</p>
        </li>
        <li>
          <span class="parcours__num">3</span>
          <h3>Vous recevez un résumé</h3>
          <p>Un texte clair, trois pistes concrètes, et la liberté de choisir si vous voulez aller plus loin. Le délai est annoncé selon le format de séance choisi.</p>
        </li>
        <li>
          <span class="parcours__num">4</span>
          <h3>Vous tenez ou vous ne tenez pas</h3>
          <p>Le journal vous accompagne. Vous restez maître·sse du rythme et des décisions. Toujours.</p>
        </li>
      </ol>

      <p class="section-foot"><a href="comment.html" class="btn btn--ghost">Voir le parcours détaillé →</a></p>
    </div>
  </section>

  <!-- Aperçu bibliothèque -->
  <section class="public-section">
    <div class="container">
      <p class="section-overline">Quelques articles à lire</p>
      <h2 class="section-title">La bibliothèque — accès libre</h2>
      <p class="section-lede">Seize textes courts, organisés en quatre axes. Aucune inscription. Aucun mur.</p>

      <div class="featured-articles">
        ''' + featured_articles_html() + '''
      </div>

      <p class="section-foot"><a href="bibliotheque.html" class="btn btn--ghost">Toute la bibliothèque (16 articles) →</a></p>
    </div>
  </section>

  <!-- Confiance / Loi 25 / sécurité -->
  <section class="public-section public-section--soft">
    <div class="container confiance">
      <p class="section-overline">La confiance est une condition</p>
      <h2 class="section-title">Vos paroles vous appartiennent</h2>

      <div class="confiance__grid">
        <div>
          <h3>Conforme à la Loi 25</h3>
          <p>Tout est traité sous la loi québécoise. Vous pouvez consulter, exporter et supprimer vos données à tout moment depuis votre espace.</p>
        </div>
        <div>
          <h3>Audios chiffrés, accès limité</h3>
          <p>Seul·e le ou la praticien·ne que vous choisissez écoute votre enregistrement. Personne d'autre. Pas même nous.</p>
        </div>
        <div>
          <h3>Effaçable, à votre demande</h3>
          <p>Vos audios et résumés peuvent être effacés sur simple demande dans votre espace. Pas de procédure, pas de friction.</p>
        </div>
        <div>
          <h3>L'humain au centre — toujours</h3>
          <p>Aucune décision automatisée à votre place. Notre outil aide les praticien·ne·s ; il ne vous remplace pas, ne les remplace pas.</p>
        </div>
      </div>

      <p class="section-foot"><a href="confidentialite.html">Lire la politique de confidentialité complète →</a></p>
    </div>
  </section>

  <!-- Bandeau urgence persistant en bas -->
  <section class="bandeau-urgence">
    <div class="container bandeau-urgence__inner">
      <div>
        <p class="bandeau-urgence__title">Vous êtes en détresse maintenant ?</p>
        <p class="bandeau-urgence__lede">IVIA n'est pas un service d'urgence. Si la situation est urgente, composez l'un de ces numéros — gratuit, 24/7.</p>
      </div>
      <div class="bandeau-urgence__nums">
        <a href="tel:911"><strong>911</strong><span>urgence vitale</span></a>
        <a href="tel:811"><strong>811 opt. 2</strong><span>Info-Social</span></a>
        <a href="tel:18662773553"><strong>1 866 APPELLE</strong><span>prévention suicide</span></a>
        <a href="urgence.html"><strong>Voir tous les recours →</strong><span></span></a>
      </div>
    </div>
  </section>

</main>
'''
    html = public_page(
        "IVIA — Un espace d'écoute pour clarifier ce que vous vivez",
        "Espace d'écoute audio québécois. Vous parlez à un·e praticien·ne, vous recevez un résumé clair et trois pistes concrètes. Conforme Loi 25.",
        "index.html",
        body,
    )
    (ROOT / "index.html").write_text(html, encoding="utf-8")


def featured_articles_html():
    """3 articles mis en avant sur la landing."""
    featured = ["1_1", "2_3", "3_3", "4_2"]
    cards = []
    for slug in featured:
        a = load_article(slug)
        # Premier paragraphe pour l'aperçu
        excerpt = ""
        for line in a["html"].split("\n"):
            if line.startswith("<p>") and len(line) > 60:
                excerpt = line.replace("<p>", "").replace("</p>", "")
                if len(excerpt) > 200:
                    excerpt = excerpt[:200].rsplit(" ", 1)[0] + "…"
                break
        cards.append(f'''
        <a class="featured-card" href="bibliotheque.html#article-{a['slug']}">
          <span class="featured-card__num">{a['num']}</span>
          <span class="featured-card__axe">{a['axe']}</span>
          <h3>{a['title']}</h3>
          <p>{excerpt}</p>
          <span class="featured-card__cta">Lire →</span>
        </a>''')
    return "\n".join(cards)


# ============================================================================
# COMMENT ÇA FONCTIONNE — comment.html
# ============================================================================
def build_comment():
    body = '''
<main id="main">
  <section class="public-hero public-hero--small">
    <div class="container">
      <p class="public-hero__overline">Comment ça fonctionne</p>
      <h1 class="public-hero__title">Un parcours simple, conçu pour <em>respecter</em> votre rythme.</h1>
      <p class="public-hero__lede">Pas d'urgence à créer. Vous décidez quand parler, combien de fois, et ce que vous faites du résumé.</p>
    </div>
  </section>

  <section class="public-section">
    <div class="container long-form">

      <h2>Le parcours, étape par étape</h2>

      <h3>1 — Vous arrivez</h3>
      <p>Vous tombez sur IVIA parce que quelqu'un vous en a parlé, parce que vous lisiez un article, ou parce qu'aujourd'hui ça pèse un peu plus que d'habitude. Pas besoin de savoir précisément ce qui ne va pas. Pas besoin de mots techniques. Vous arrivez avec ce que vous avez.</p>

      <h3>2 — Vous choisissez votre porte</h3>
      <p>Trois entrées sont possibles :</p>
      <ul>
        <li><strong>Lire d'abord</strong>, dans la <a href="bibliotheque.html">bibliothèque</a>, pour voir si la manière d'IVIA vous parle.</li>
        <li><strong>Commencer une écoute</strong> directement, sans inscription préalable obligatoire en phase de test.</li>
        <li><strong>Tenir un journal</strong>, gratuitement, sans même enregistrer d'audio.</li>
      </ul>

      <h3>3 — Vous parlez (ou vous écrivez)</h3>
      <p>Si vous choisissez l'écoute audio, l'enregistrement se fait depuis votre navigateur. Vous pouvez :</p>
      <ul>
        <li>Vous arrêter et reprendre autant de fois que vous voulez.</li>
        <li>Effacer et recommencer si rien ne sort comme vous voudriez.</li>
        <li>Enregistrer en plusieurs courtes sessions plutôt qu'en une seule.</li>
      </ul>
      <p>Aucun temps minimum. Aucun script à suivre. Si vous ne savez pas par où commencer, lancez l'enregistrement et dites simplement comment va votre journée.</p>

      <h3>4 — Notre outil prépare une lecture</h3>
      <p>En interne, IVIA s'appuie sur un outil que nous avons développé pour aider les praticiens et praticiennes. Il transcrit votre audio, propose une mise en lumière des cinq zones du cercle (corps, relation, sens, ressources, fréquence), et suggère des pistes possibles.</p>
      <p><strong>Important :</strong> cet outil ne décide jamais à votre place ni à la place de la praticienne. Il prépare une matière. La praticienne lit, écoute, et écrit le résumé final, à la main, pour vous.</p>

      <h3>5 — Vous recevez votre résumé</h3>
      <p>Entre 24 et 72 heures après l'enregistrement, votre résumé arrive dans votre espace. Il contient typiquement :</p>
      <ul>
        <li>Une lecture douce et claire de ce que vous avez exprimé.</li>
        <li>Une mise en lumière des deux ou trois zones du cercle qui semblent les plus actives en ce moment.</li>
        <li><strong>Trois pistes concrètes</strong> — pas un programme, juste trois directions possibles que vous êtes libre d'essayer.</li>
        <li>Une suggestion : revenir, ne pas revenir, ou prendre rendez-vous avec un·e praticien·ne pour une vraie séance.</li>
      </ul>

      <h3>6 — Vous tenez ou vous ne tenez pas</h3>
      <p>Personne ne vous relance. Personne ne vous fait sentir coupable. Si une piste tient, le journal vous aide à le voir. Si rien ne tient, c'est aussi une information utile pour la prochaine écoute.</p>

      <h2>Phase de test — ce qui marche aujourd'hui</h2>
      <p class="callout callout--info">
        <strong>Mai 2026 — phase pilote.</strong>
        Pour cette phase, vous pouvez enregistrer un audio sans praticien·ne assigné·e et recevoir un résumé automatique de notre outil interne. Cela nous permet de valider la qualité de l'analyse avant d'ouvrir le service avec un réseau de praticien·ne·s formé·e·s. Aucun audio n'est conservé au-delà de la durée nécessaire au test.
      </p>

      <h2>Ce que IVIA fait avec vos paroles</h2>
      <p>Nous prenons trois engagements clairs :</p>
      <ul>
        <li><strong>Personne ne lit ni n'écoute votre matière à part la praticienne que vous avez choisie</strong> (et notre outil interne, pour préparer). Aucune équipe marketing. Aucun tiers commercial.</li>
        <li><strong>Vous gardez la main</strong> : depuis votre espace, vous pouvez consulter, exporter ou supprimer un audio, un résumé, ou tout votre compte. Sans question.</li>
        <li><strong>Aucune donnée ne sort du Québec</strong> dès la mise en activité commerciale. Pendant la phase de test actuelle, les serveurs sont temporairement en France ; un transfert vers le Québec est planifié avant l'ouverture publique.</li>
      </ul>
      <p>La page <a href="confidentialite.html">Politique de confidentialité (Loi 25)</a> détaille ces engagements de manière complète.</p>

      <h2>Et si l'écoute IVIA ne suffit pas ?</h2>
      <p>Il y a des situations qui dépassent ce qu'IVIA peut tenir. Si pendant ou après votre écoute vous ressentez :</p>
      <ul>
        <li>Des idées d'en finir avec la vie ou de vous faire du mal.</li>
        <li>De la peur pour votre sécurité ou celle d'un·e proche.</li>
        <li>Un état qui nécessite un avis médical rapide.</li>
      </ul>
      <p>Composez immédiatement l'un de ces numéros gratuits, 24h/24 :</p>
      <ul>
        <li><strong>911</strong> — urgence vitale.</li>
        <li><strong>811 option 2</strong> — Info-Social, intervenants en santé mentale.</li>
        <li><strong>1 866 APPELLE</strong> (1 866 277 3553) — prévention du suicide, Québec.</li>
        <li><strong>Tel-jeunes</strong> : 1 800 263 2266, ou texto au 514 600 1002.</li>
      </ul>
      <p>La page <a href="urgence.html">Si c'est urgent</a> rassemble tous ces recours, en clair, en grand, à toute heure.</p>

      <p class="long-form__cta">
        <a href="client/audio-async.html" class="btn btn--primary btn--lg">Commencer une écoute</a>
        <a href="bibliotheque.html" class="btn btn--ghost btn--lg">Lire d'abord</a>
      </p>
    </div>
  </section>
</main>
'''
    html = public_page(
        "Comment ça fonctionne — IVIA",
        "Le parcours IVIA en six étapes : arriver, choisir, parler, recevoir un résumé, tenir une suite. Avec transparence sur ce que nous faisons de vos paroles.",
        "comment.html",
        body,
    )
    (ROOT / "comment.html").write_text(html, encoding="utf-8")


# ============================================================================
# BIBLIOTHEQUE — bibliotheque.html (avec les 16 articles intégrés in-page)
# ============================================================================
def build_bibliotheque():
    arts = all_articles()
    by_axe = {}
    for a in arts:
        by_axe.setdefault(a["axe"], []).append(a)

    axes_nav = '\n'.join(
        f'<a class="axe-nav__item axe-nav--{AXES[axe]["slug"]}" href="#axe-{AXES[axe]["slug"]}"><span>{axe}</span></a>'
        for axe in AXES
    )

    sections = []
    for axe_name, axe_meta in AXES.items():
        articles_in_axe = by_axe.get(axe_name, [])
        cards = []
        for a in articles_in_axe:
            cards.append(f'''
        <a class="axe-card" href="#article-{a['slug']}">
          <span class="axe-card__num">{a['num']}</span>
          <h3>{a['title']}</h3>
        </a>''')
        sections.append(f'''
  <section class="public-section public-section--axe" id="axe-{axe_meta['slug']}">
    <div class="container">
      <p class="section-overline">Axe {axe_name.split(' ')[0][:3].lower()}</p>
      <h2 class="section-title">{axe_name}</h2>
      <p class="section-lede">{axe_meta['intro']}</p>
      <div class="axe-grid">
{"".join(cards)}
      </div>
    </div>
  </section>''')

    # Articles in-page intégraux
    articles_full = []
    for axe_name in AXES:
        for a in by_axe.get(axe_name, []):
            articles_full.append(f'''
  <article class="article-full" id="article-{a['slug']}">
    <div class="container article-full__inner">
      <p class="article-full__breadcrumb"><a href="#axe-{AXES[a['axe']]['slug']}">{a['axe']}</a> · Article {a['num']}</p>
      <h2 class="article-full__title">{a['title']}</h2>
      <div class="article-full__body">
{a['html']}
      </div>
      <p class="article-full__back"><a href="#top">↑ Retour à la bibliothèque</a></p>
    </div>
  </article>''')

    body = f'''
<main id="main">
  <a id="top"></a>
  <section class="public-hero public-hero--small">
    <div class="container">
      <p class="public-hero__overline">Bibliothèque · 16 articles · accès libre</p>
      <h1 class="public-hero__title">Lire, à votre <em>rythme</em>, ce qui fait IVIA.</h1>
      <p class="public-hero__lede">Quatre axes éditoriaux. Seize textes courts. Aucune inscription. Aucun mur. Aucun jugement.</p>
    </div>
  </section>

  <nav class="axe-nav" aria-label="Naviguer par axe">
    <div class="container axe-nav__inner">
      {axes_nav}
    </div>
  </nav>

  {"".join(sections)}

  <section class="public-section public-section--soft">
    <div class="container" style="text-align:center;">
      <h2 class="section-title">Lire chaque article ↓</h2>
      <p class="section-lede">Tous les articles sont publiés ci-dessous, à la suite, dans l'ordre éditorial.</p>
    </div>
  </section>

  {"".join(articles_full)}

  <!-- Bandeau urgence en pied -->
  <section class="bandeau-urgence">
    <div class="container bandeau-urgence__inner">
      <div>
        <p class="bandeau-urgence__title">Si la lecture remue quelque chose de difficile</p>
        <p class="bandeau-urgence__lede">Pas d'hésitation. Composez un de ces numéros, gratuit, 24/7.</p>
      </div>
      <div class="bandeau-urgence__nums">
        <a href="tel:911"><strong>911</strong><span>urgence vitale</span></a>
        <a href="tel:811"><strong>811 opt. 2</strong><span>Info-Social</span></a>
        <a href="tel:18662773553"><strong>1 866 APPELLE</strong><span>prévention suicide</span></a>
        <a href="urgence.html"><strong>Voir tous les recours →</strong><span></span></a>
      </div>
    </div>
  </section>

</main>
'''
    html = public_page(
        "Bibliothèque — IVIA",
        "Seize articles courts pour comprendre la manière IVIA. Écoute, équilibre, frontières, réalisation. Accès libre, sans inscription.",
        "bibliotheque.html",
        body,
    )
    (ROOT / "bibliotheque.html").write_text(html, encoding="utf-8")


# ============================================================================
# RESSOURCES URGENCE — urgence.html
# ============================================================================
def build_urgence():
    body = '''
<main id="main" class="urgence-page">
  <section class="urgence-hero">
    <div class="container">
      <p class="urgence-hero__overline">Si c'est urgent</p>
      <h1 class="urgence-hero__title">Vous n'êtes <em>pas seul·e</em>.</h1>
      <p class="urgence-hero__lede">Voici les recours d'urgence au Québec. Gratuits. 24 heures sur 24, 7 jours sur 7. N'attendez pas que ça empire.</p>
    </div>
  </section>

  <section class="public-section">
    <div class="container">

      <div class="urgence-grille">

        <a class="urgence-bloc urgence-bloc--rouge" href="tel:911">
          <div class="urgence-bloc__num">911</div>
          <div class="urgence-bloc__label">Urgence vitale</div>
          <p>Pour toute situation où votre vie ou celle d'une autre personne est en danger immédiat. Composez sans hésitation.</p>
          <span class="urgence-bloc__cta">Appeler le 911 →</span>
        </a>

        <a class="urgence-bloc urgence-bloc--bleu" href="tel:811">
          <div class="urgence-bloc__num">811</div>
          <div class="urgence-bloc__label">Info-Social — option 2</div>
          <p>Service de consultation téléphonique gratuit du gouvernement du Québec, en santé sociale et mentale. Intervenant·e·s qualifié·e·s, à toute heure.</p>
          <span class="urgence-bloc__cta">Appeler le 811 (option 2) →</span>
        </a>

        <a class="urgence-bloc urgence-bloc--mauve" href="tel:18662773553">
          <div class="urgence-bloc__num">1 866 APPELLE</div>
          <div class="urgence-bloc__label">1 866 277 3553 · prévention du suicide</div>
          <p>Si vous avez des idées suicidaires, ou que vous êtes inquiet·e pour quelqu'un. Confidentiel, gratuit, partout au Québec.</p>
          <span class="urgence-bloc__cta">Appeler maintenant →</span>
        </a>

        <a class="urgence-bloc urgence-bloc--vert" href="tel:18002632266">
          <div class="urgence-bloc__num">Tel-jeunes</div>
          <div class="urgence-bloc__label">1 800 263 2266 · texto 514 600 1002</div>
          <p>Pour les enfants et adolescent·e·s du Québec. Téléphone, texto, clavardage. Gratuit, anonyme, sans jugement.</p>
          <span class="urgence-bloc__cta">Joindre Tel-jeunes →</span>
        </a>

      </div>

      <h2 class="urgence-h2">Autres recours utiles</h2>

      <div class="urgence-list">

        <div class="urgence-item">
          <h3>SOS Violence conjugale</h3>
          <p><a href="tel:18003639010"><strong>1 800 363 9010</strong></a> — soutien, hébergement, information. 24/7. Tous les genres, partout au Québec.</p>
        </div>

        <div class="urgence-item">
          <h3>Drogue : aide et référence</h3>
          <p><a href="tel:18002650140"><strong>1 800 265 0140</strong></a> — soutien et orientation pour toute personne préoccupée par sa consommation ou celle d'un·e proche. 24/7.</p>
        </div>

        <div class="urgence-item">
          <h3>Ligne Parents</h3>
          <p><a href="tel:18003617622"><strong>1 800 361 5085</strong></a> — soutien aux parents 24/7, en français.</p>
        </div>

        <div class="urgence-item">
          <h3>Interligne (LGBTQ+)</h3>
          <p><a href="tel:18885058088"><strong>1 888 505 8088</strong></a> — écoute, information, référence pour les personnes LGBTQ+ et leurs proches.</p>
        </div>

      </div>

      <div class="urgence-rappel">
        <h3>IVIA n'est pas un service d'urgence</h3>
        <p>Notre espace d'écoute fonctionne sur rendez-vous — en direct ou en différé — avec des délais de réponse qui ne sont pas adaptés aux situations qui exigent une intervention immédiate. Si la situation ne peut pas attendre, l'écoute IVIA n'est pas le bon endroit. Composez l'un des numéros ci-dessus, sans hésiter. Cela ne signifie pas que vous avez « échoué » à utiliser IVIA. Cela signifie que vous prenez soin de vous au bon rythme.</p>
        <p><a href="index.html">← Retour à l'accueil</a></p>
      </div>

    </div>
  </section>
</main>
'''
    html = public_page(
        "Si c'est urgent — IVIA",
        "Ressources d'urgence au Québec : 911, 811 option 2, 1 866 APPELLE, Tel-jeunes. Gratuit, 24/7. IVIA n'est pas un service d'urgence.",
        "urgence.html",
        body,
    )
    (ROOT / "urgence.html").write_text(html, encoding="utf-8")


# ============================================================================
# POURQUOI IVIA — pourquoi.html
# ============================================================================
def build_pourquoi():
    body = '''
<main id="main">
  <section class="public-hero public-hero--small">
    <div class="container">
      <p class="public-hero__overline">Pourquoi IVIA · ce qui rend ce projet nécessaire</p>
      <h1 class="public-hero__title">Le besoin n'est pas une <em>impression</em>. Il est <em>documenté</em>.</h1>
      <p class="public-hero__lede">Il y a une manière facile de présenter un projet : multiplier les promesses. Nous avons choisi l'autre. Voici les chiffres qui nous font lever le matin, et la ligne de crête qu'IVIA décide d'occuper.</p>
    </div>
  </section>

  <section class="public-section">
    <div class="container">
      <p class="section-overline">L'état des lieux</p>
      <h2 class="section-title">Quatre faits qui ne reculent pas</h2>
      <p class="section-lede">Ces données viennent d'institutions publiques québécoises et canadiennes. Elles ne sont pas notre interprétation. Elles sont le sol sur lequel IVIA s'appuie.</p>

      <div class="pourquoi-faits">
        <article class="fait-card">
          <p class="fait-card__chiffre">38,7&nbsp;%</p>
          <h3 class="fait-card__titre">des Québécois·es de 15&nbsp;ans et plus vivent une détresse psychologique élevée</h3>
          <p class="fait-card__source">INSPQ, <em>Portrait de l'état de santé mentale de la population québécoise</em>, 2020-2021. Vs 28,3&nbsp;% en 2014-2015. Chez les 15-24&nbsp;ans : 57,6&nbsp;%. Chez les jeunes femmes : 67,8&nbsp;%.</p>
          <p class="fait-card__lecture">Ce n'est pas un pic conjoncturel. C'est une trajectoire qui monte depuis dix ans. La pression sur les vies, sur les familles, sur les milieux de travail ne va pas redescendre toute seule.</p>
        </article>

        <article class="fait-card">
          <p class="fait-card__chiffre">22&nbsp;000</p>
          <h3 class="fait-card__titre">personnes en attente d'un service en santé mentale au Québec</h3>
          <p class="fait-card__source">Ministère de la Santé et des Services sociaux (cible : 13&nbsp;261). Commissaire à la santé et au bien-être, rapport 2024-2025 : seulement 58&nbsp;% des soins reçus dans les délais prescrits.</p>
          <p class="fait-card__lecture">Le système public fait ce qu'il peut, et ce qu'il peut n'est pas suffisant. Pour les troubles diagnostiqués, l'attente est cliniquement dangereuse. Pour ceux qui ne savent même pas s'ils ont «&nbsp;quelque chose&nbsp;», il n'y a souvent aucune porte.</p>
        </article>

        <article class="fait-card">
          <p class="fait-card__chiffre">6 à 11&nbsp;ans</p>
          <h3 class="fait-card__titre">entre l'apparition des symptômes et le premier traitement</h3>
          <p class="fait-card__source">CAMH (Centre de toxicomanie et de santé mentale). Littérature internationale en <em>help-seeking</em> : le manque de clarté sur ce qu'on vit précède et ralentit la recherche d'aide.</p>
          <p class="fait-card__lecture">Avant qu'on parle d'un «&nbsp;trouble&nbsp;», il y a souvent dix ans pendant lesquels la personne ne sait pas comment nommer ce qui ne va pas. C'est là, dans cet espace de manque de clarté, qu'IVIA s'inscrit.</p>
        </article>

        <article class="fait-card">
          <p class="fait-card__chiffre">120 à 180&nbsp;$</p>
          <h3 class="fait-card__titre">la séance de psychothérapie en cabinet privé</h3>
          <p class="fait-card__source">Tarifs courants Québec 2024-2025. La psychothérapie n'est pas couverte par la RAMQ. Seules certaines assurances privées la remboursent partiellement.</p>
          <p class="fait-card__lecture">Pour une majorité de ménages, c'est un budget impossible — surtout si plusieurs séances sont nécessaires. Entre l'attente publique et le coût du privé, il y a un trou. C'est ce trou qu'on a décidé de combler, en partie, sans prétendre remplacer ni l'un ni l'autre.</p>
        </article>
      </div>
    </div>
  </section>

  <section class="public-section public-section--soft">
    <div class="container">
      <p class="section-overline">Le contexte humain</p>
      <h2 class="section-title">L'isolement n'est pas une <em>métaphore</em></h2>
      <p class="section-lede">Vivre seul·e, ce n'est pas être seul·e — mais l'un favorise l'autre. Et l'isolement social a des effets mesurables sur le corps autant que sur l'esprit.</p>

      <div class="pourquoi-deux-colonnes">
        <div class="pourquoi-bloc">
          <p class="pourquoi-bloc__chiffre">1,3&nbsp;million</p>
          <p class="pourquoi-bloc__texte">de Québécois·es de 15&nbsp;ans et plus vivent seul·e·s (Statistique Canada, recensement 2021). Le phénomène s'amplifie chez les jeunes adultes urbains et chez les aîné·e·s.</p>
        </div>
        <div class="pourquoi-bloc">
          <p class="pourquoi-bloc__chiffre">+35&nbsp;%</p>
          <p class="pourquoi-bloc__texte">de risque de mortalité lié à l'isolement social, équivalent à fumer 15&nbsp;cigarettes par jour (méta-analyses Holt-Lunstad). Ce n'est pas une métaphore littéraire — c'est une donnée épidémiologique.</p>
        </div>
      </div>

      <p class="pourquoi-bilan">Quand quelqu'un cherche un espace pour se déposer, ce n'est pas un confort. C'est, parfois, une question de longue durée — voire de santé tout court. IVIA n'est pas une réponse à l'isolement. C'est un point d'appui pour des gens qui peuvent en ressentir les effets, et qui méritent d'être entendus avant tout.</p>
    </div>
  </section>

  <section class="public-section">
    <div class="container">
      <p class="section-overline">Pourquoi pas une autre app</p>
      <h2 class="section-title">Le format «&nbsp;IA-seule&nbsp;» ne tient pas la confiance</h2>
      <p class="section-lede">L'industrie des applications de santé mentale a connu une expansion massive depuis 2020. Et un effondrement de confiance récent, documenté, qu'il serait malhonnête d'ignorer.</p>

      <ul class="pourquoi-liste-faits">
        <li><strong>Rétention de 3 à 4&nbsp;%</strong> à J30 sur la moyenne du segment des apps de santé mentale (analyses sectorielles 2024-2025). Le format autonome ne tient ni la confiance ni l'usage.</li>
        <li><strong>BetterHelp</strong> a été condamné à 7,8&nbsp;M$ par la <em>Federal Trade Commission</em> en 2023 pour partage de données de santé mentale avec des régies publicitaires.</li>
        <li><strong>Mozilla</strong> (<em>Privacy Not Included</em>, 2023) a épinglé 32&nbsp;applications de santé mentale et de prière pour pratiques de données opaques ou prédatrices.</li>
        <li><strong>Le cas de Sewell Setzer&nbsp;III</strong> (mort en 2024, règlement civil avec Character.AI en 2026) a rendu visible le risque de relations émotionnelles intenses avec des IA conversationnelles, particulièrement chez les jeunes.</li>
      </ul>

      <p class="pourquoi-bilan">Ces événements ne disqualifient pas le numérique en santé mentale. Ils disqualifient un certain modèle : opaque sur les données, automatisé sans humain, optimisé pour l'engagement plutôt que pour la sortie. IVIA prend le contrepied de chacun de ces choix.</p>
    </div>
  </section>

  <section class="public-section public-section--soft">
    <div class="container">
      <p class="section-overline">Le créneau d'IVIA</p>
      <h2 class="section-title">Cinq dimensions, un seul espace</h2>
      <p class="section-lede">Aucun acteur connu, au Québec, ne réunit ces cinq dimensions à la fois. C'est exactement la place qu'IVIA décide d'occuper.</p>

      <div class="pourquoi-creneau">
        <div class="creneau-pilier"><span class="creneau-pilier__num">1</span><h3>Audio</h3><p>La voix porte ce que le texte aplatit. Pas de caméra, pas de mise en scène, pas d'avatar. Juste la parole.</p></div>
        <div class="creneau-pilier"><span class="creneau-pilier__num">2</span><h3>Humain</h3><p>Une personne qualifiée écoute, pas une intelligence artificielle. L'IA est dans la coulisse, jamais dans le siège.</p></div>
        <div class="creneau-pilier"><span class="creneau-pilier__num">3</span><h3>Non-urgence</h3><p>IVIA n'est pas un service de crise. Pour les urgences, il y a le 911, le 811 option 2, le 1 866 APPELLE. IVIA est l'espace d'avant ou d'après.</p></div>
        <div class="creneau-pilier"><span class="creneau-pilier__num">4</span><h3>Francophone</h3><p>Pensé, formulé, opéré en français québécois. Pas une traduction. Une langue.</p></div>
        <div class="creneau-pilier"><span class="creneau-pilier__num">5</span><h3>Conforme Loi 25</h3><p>Dès le départ. Vos données ne sont pas notre produit. La voix est effacée à J+30, l'extraction d'apprentissage anonymisée, le consentement granulaire.</p></div>
      </div>
    </div>
  </section>

  <section class="public-section">
    <div class="container">
      <p class="section-overline">Honnêteté radicale</p>
      <h2 class="section-title">Ce qu'IVIA <em>n'est pas</em>, dit clairement</h2>
      <p class="section-lede">La meilleure preuve qu'on a réfléchi, c'est de nommer ce qu'on ne peut pas faire. Voici nos limites, sans habillage.</p>

      <ul class="pourquoi-limites">
        <li><strong>IVIA ne remplace pas la psychothérapie</strong> pour un trouble diagnostiqué. Si vous avez un diagnostic ou des symptômes intenses, la psychothérapie clinique reste le bon recours.</li>
        <li><strong>IVIA n'est pas un service d'urgence.</strong> Si une vie est en danger, composez le 911 ou le 1&nbsp;866 APPELLE (1&nbsp;866 277-3553).</li>
        <li><strong>IVIA ne couvre pas spontanément</strong> les besoins spécifiques des communautés autochtones, 2SLGBTQ+ ou racisé·e·s sans partenariats explicites avec ces communautés. Ce travail est en cours.</li>
        <li><strong>IVIA ne réduit pas les inégalités structurelles d'accès aux soins.</strong> Tarif accessible, oui ; gratuit pour tous, non. La redistribution se construit via l'OBNL satellite, progressivement.</li>
        <li><strong>IVIA ne garantit pas de résultats thérapeutiques mesurables.</strong> Nous mesurons l'usage, la satisfaction, la clarté ressentie. Pas la «&nbsp;guérison&nbsp;». Ce serait une promesse malhonnête.</li>
      </ul>

      <p class="pourquoi-bilan">Ces limites ne sont pas des défauts à cacher. Ce sont les conditions mêmes de la confiance qu'on souhaite construire avec les personnes qui nous écoutent et avec celles qui nous confient leur voix.</p>
    </div>
  </section>

  <section class="public-section public-section--accent">
    <div class="container pourquoi-cta">
      <h2 class="section-title">Quand tout se mélange, commencez par <em>être entendu</em>.</h2>
      <p class="section-lede">Une séance audio, en français, avec une personne qualifiée qui sait écouter. Sans urgence. Sans diagnostic. Avec une suite concrète à votre rythme.</p>
      <div class="pourquoi-cta__actions">
        <a href="client/audio-async.html" class="btn btn--primary">Commencer une écoute</a>
        <a href="comment.html" class="btn btn--ghost">Voir comment ça fonctionne</a>
      </div>
      <p class="pourquoi-cta__sources">Sources principales : INSPQ · ISQ · Statistique Canada · Commissaire à la santé et au bien-être du Québec · CAMH · Federal Trade Commission · Holt-Lunstad et al. Le corpus complet de preuves est documenté en interne et révisable annuellement.</p>
    </div>
  </section>
</main>
'''
    css = """
.pourquoi-faits {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2.5rem;
  margin-top: 3rem;
}
@media (max-width: 720px) {
  .pourquoi-faits { grid-template-columns: 1fr; gap: 1.75rem; }
}
.fait-card {
  background: var(--color-creme);
  border: 1px solid rgba(74, 47, 74, 0.12);
  border-radius: 14px;
  padding: 2.25rem 2rem 2rem;
  box-shadow: 0 1px 3px rgba(74, 47, 74, 0.06);
}
.fait-card__chiffre {
  font-family: var(--font-display);
  font-size: clamp(2.6rem, 5.5vw, 3.6rem);
  font-weight: 500;
  color: var(--color-aubergine);
  margin: 0 0 0.5rem;
  letter-spacing: -0.02em;
  line-height: 1;
}
.fait-card__titre {
  font-family: var(--font-serif);
  font-size: 1.25rem;
  font-weight: 500;
  color: var(--color-aubergine);
  margin: 0 0 1rem;
  line-height: 1.35;
}
.fait-card__source {
  font-size: 0.86rem;
  color: var(--color-prune);
  margin: 0 0 1rem;
  line-height: 1.55;
  opacity: 0.85;
}
.fait-card__lecture {
  font-family: var(--font-serif);
  font-style: italic;
  font-size: 1rem;
  color: var(--color-aubergine);
  margin: 0;
  line-height: 1.6;
  border-top: 1px solid rgba(74, 47, 74, 0.12);
  padding-top: 1rem;
}
.pourquoi-deux-colonnes {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2.5rem;
  margin: 2.5rem 0 2rem;
}
@media (max-width: 720px) {
  .pourquoi-deux-colonnes { grid-template-columns: 1fr; gap: 1.5rem; }
}
.pourquoi-bloc {
  text-align: center;
  padding: 2rem 1rem;
}
.pourquoi-bloc__chiffre {
  font-family: var(--font-display);
  font-size: clamp(2.8rem, 6vw, 4rem);
  font-weight: 500;
  color: var(--color-rose-deep);
  margin: 0 0 1rem;
  letter-spacing: -0.02em;
  line-height: 1;
}
.pourquoi-bloc__texte {
  font-family: var(--font-serif);
  font-size: 1.05rem;
  color: var(--color-aubergine);
  margin: 0;
  line-height: 1.6;
  max-width: 36ch;
  margin-left: auto;
  margin-right: auto;
}
.pourquoi-bilan {
  font-family: var(--font-serif);
  font-size: 1.1rem;
  font-style: italic;
  color: var(--color-aubergine);
  line-height: 1.65;
  max-width: 64ch;
  margin: 2rem auto 0;
  text-align: center;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(74, 47, 74, 0.15);
}
.pourquoi-liste-faits {
  list-style: none;
  padding: 0;
  margin: 2rem 0 0;
  display: grid;
  gap: 1rem;
  max-width: 70ch;
}
.pourquoi-liste-faits li {
  font-size: 1rem;
  color: var(--color-aubergine);
  line-height: 1.6;
  padding: 1rem 1.25rem;
  background: var(--color-creme);
  border-left: 3px solid var(--color-rose);
  border-radius: 0 8px 8px 0;
}
.pourquoi-liste-faits strong {
  color: var(--color-aubergine);
  font-weight: 600;
}
.pourquoi-creneau {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
  margin-top: 2.5rem;
}
.creneau-pilier {
  background: var(--color-creme);
  border: 1px solid rgba(74, 47, 74, 0.12);
  border-radius: 12px;
  padding: 1.75rem 1.5rem;
  position: relative;
}
.creneau-pilier__num {
  position: absolute;
  top: 1rem;
  right: 1.25rem;
  font-family: var(--font-display);
  font-size: 2.4rem;
  font-weight: 500;
  color: var(--color-rose);
  opacity: 0.55;
  line-height: 1;
}
.creneau-pilier h3 {
  font-family: var(--font-display);
  font-size: 1.4rem;
  font-weight: 500;
  color: var(--color-aubergine);
  margin: 0 0 0.75rem;
}
.creneau-pilier p {
  font-size: 0.95rem;
  color: var(--color-aubergine);
  line-height: 1.55;
  margin: 0;
  opacity: 0.9;
}
.pourquoi-limites {
  list-style: none;
  padding: 0;
  margin: 2rem 0 0;
  display: grid;
  gap: 0.85rem;
  max-width: 70ch;
}
.pourquoi-limites li {
  font-size: 1rem;
  color: var(--color-aubergine);
  line-height: 1.6;
  padding: 1rem 1.25rem;
  background: rgba(255, 255, 255, 0.7);
  border-left: 3px solid var(--color-aubergine);
  border-radius: 0 8px 8px 0;
}
.public-section--accent {
  background: linear-gradient(135deg, var(--color-aubergine) 0%, var(--color-prune) 100%);
  color: var(--color-creme);
}
.public-section--accent .section-overline,
.public-section--accent .section-title,
.public-section--accent .section-lede,
.public-section--accent em {
  color: var(--color-creme);
}
.public-section--accent em {
  font-style: italic;
  color: var(--color-rose);
}
.pourquoi-cta {
  text-align: center;
  max-width: 64ch;
}
.pourquoi-cta__actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
  margin: 2rem 0 1.5rem;
}
.pourquoi-cta__sources {
  font-size: 0.82rem;
  color: var(--color-creme);
  opacity: 0.75;
  line-height: 1.55;
  margin: 1rem auto 0;
  max-width: 60ch;
}
"""
    html = public_page(
        "Pourquoi IVIA — ce qui rend ce projet nécessaire",
        "Les chiffres officiels sur la détresse psychologique, l'accès aux soins et l'isolement au Québec. Ce qu'IVIA décide de faire — et ce qu'IVIA ne fera pas. Honnêteté radicale, sources publiques.",
        "pourquoi.html",
        body,
        css_extra=css,
    )
    (ROOT / "pourquoi.html").write_text(html, encoding="utf-8")


# ============================================================================
# MENTIONS LÉGALES
# ============================================================================
def build_mentions():
    body = '''
<main id="main">
  <section class="public-hero public-hero--small">
    <div class="container">
      <p class="public-hero__overline">Mentions légales</p>
      <h1 class="public-hero__title">Mentions <em>légales</em></h1>
    </div>
  </section>

  <section class="public-section">
    <div class="container long-form">

      <h2>Éditeur du service</h2>
      <p>Le service IVIA est édité dans le cadre du projet IVIA / MERLIN, en phase pilote au Québec, Canada.</p>
      <ul>
        <li><strong>Nom de projet :</strong> IVIA</li>
        <li><strong>Responsable :</strong> David Phaneuf</li>
        <li><strong>Adresse de contact :</strong> <a href="mailto:contact@ivia.quebec">contact@ivia.quebec</a></li>
        <li><strong>Domaine principal :</strong> ivia.quebec (en cours de mise en activité)</li>
      </ul>

      <h2>Hébergement</h2>
      <p><strong>Phase pilote (mai 2026) :</strong> les services techniques sont temporairement hébergés sur des serveurs OVH situés en France, dans le seul but de tester la chaîne de traitement et de valider la qualité de l'outil interne avant l'ouverture publique du service au Québec.</p>
      <p><strong>À la mise en activité commerciale</strong>, l'ensemble des données utilisateurs sera migré vers une infrastructure située au Québec, conformément à l'engagement Loi 25 décrit dans la <a href="confidentialite.html">politique de confidentialité</a>.</p>

      <h2>Propriété intellectuelle</h2>
      <p>L'ensemble des contenus du site IVIA — textes, articles, illustrations, code, charte éditoriale, dénomination « IVIA », logos et identité visuelle — est la propriété du projet IVIA. Toute reproduction, extraction ou réutilisation à des fins commerciales sans autorisation écrite est interdite.</p>
      <p>La citation pour usage personnel, pédagogique ou journalistique est autorisée, à condition de mentionner clairement la source : <em>IVIA — ivia.quebec</em>.</p>

      <h2>Limites du service</h2>
      <p>IVIA est un espace d'écoute audio opéré par des praticien·ne·s humain·e·s, accessible en rendez-vous direct ou en différé. <strong>IVIA n'est pas un service d'urgence et ne pose aucun diagnostic médical, psychologique ou psychiatrique.</strong> En cas de détresse, composez le <a href="urgence.html">911 ou consultez la liste des recours d'urgence</a>.</p>

      <h2>Accessibilité</h2>
      <p>Le site IVIA vise un niveau d'accessibilité conforme aux standards WCAG 2.1 niveau AA. Si vous rencontrez une difficulté d'accès, écrivez à <a href="mailto:contact@ivia.quebec">contact@ivia.quebec</a>.</p>

      <h2>Mise à jour</h2>
      <p>Ces mentions légales sont à jour au 9 mai 2026. Elles peuvent être modifiées à tout moment. La version en vigueur est celle publiée sur cette page.</p>

      <p class="long-form__back"><a href="index.html">← Retour à l'accueil</a></p>
    </div>
  </section>
</main>
'''
    html = public_page("Mentions légales — IVIA", "Mentions légales du service IVIA.", "mentions.html", body)
    (ROOT / "mentions.html").write_text(html, encoding="utf-8")


# ============================================================================
# CONFIDENTIALITÉ Loi 25
# ============================================================================
def build_confidentialite():
    body = '''
<main id="main">
  <section class="public-hero public-hero--small">
    <div class="container">
      <p class="public-hero__overline">Politique de confidentialité · Loi 25 du Québec</p>
      <h1 class="public-hero__title">Vos paroles vous <em>appartiennent</em>.</h1>
      <p class="public-hero__lede">Cette politique explique, en clair, ce qu'IVIA fait de vos données. Pas de jargon, pas de petites lignes.</p>
    </div>
  </section>

  <section class="public-section">
    <div class="container long-form">

      <h2>1. Qui est responsable de vos données</h2>
      <p>Le projet IVIA est responsable du traitement de vos renseignements personnels au sens de la <em>Loi modernisant des dispositions législatives en matière de protection des renseignements personnels</em> (Loi 25, Québec).</p>
      <p><strong>Responsable de la protection des renseignements personnels (RPRP) :</strong> David Phaneuf — joignable à <a href="mailto:privacy@ivia.quebec">privacy@ivia.quebec</a>.</p>

      <h2>2. Quelles données nous traitons</h2>
      <ul>
        <li><strong>Compte :</strong> courriel, mot de passe (en phase de test, accès direct sans inscription).</li>
        <li><strong>Audios :</strong> les enregistrements que vous nous confiez.</li>
        <li><strong>Transcriptions et résumés :</strong> textes générés à partir de vos audios, vus par votre praticien·ne.</li>
        <li><strong>Journal :</strong> les notes que vous écrivez dans votre espace personnel.</li>
        <li><strong>Métadonnées techniques :</strong> dates, durées, état de traitement. Aucun cookie publicitaire, aucun tracker tiers.</li>
      </ul>

      <h2>3. Pourquoi nous les traitons</h2>
      <ul>
        <li><strong>Vous offrir le service</strong> d'écoute, de résumé et de journal.</li>
        <li><strong>Permettre à votre praticien·ne</strong> de vous écrire un retour humain et personnalisé.</li>
        <li><strong>Améliorer la qualité de notre outil interne</strong> de manière strictement encadrée — voir section 6.</li>
      </ul>
      <p>Nous ne traitons vos données pour aucune autre raison. Pas de revente. Pas de profilage publicitaire. Jamais.</p>

      <h2>4. Qui peut voir quoi</h2>
      <ul>
        <li><strong>Vous</strong> : tout — audios, transcriptions, résumés, journal.</li>
        <li><strong>Votre praticien·ne assigné·e</strong> : audios, transcriptions, résumés. Pas votre journal personnel.</li>
        <li><strong>L'équipe technique IVIA</strong> : strictement les métadonnées et, sur demande explicite de votre part, le contenu nécessaire à résoudre un incident technique.</li>
        <li><strong>Personne d'autre</strong>. Aucune équipe marketing, aucun annonceur, aucun partenaire commercial.</li>
      </ul>

      <h2>5. Combien de temps nous gardons vos données</h2>
      <ul>
        <li><strong>Audios bruts :</strong> jusqu'à 30 jours après leur traitement, puis suppression automatique sauf demande explicite de conservation pour un suivi.</li>
        <li><strong>Transcriptions et résumés :</strong> tant que votre compte est actif, ou jusqu'à votre demande d'effacement.</li>
        <li><strong>Journal :</strong> tant que votre compte est actif, ou jusqu'à votre demande d'effacement.</li>
        <li><strong>Compte fermé :</strong> toutes vos données sont effacées dans les 30 jours, sauf obligation légale spécifique.</li>
      </ul>

      <h2>6. Apprentissage de notre outil interne</h2>
      <p>Notre outil d'aide aux praticien·ne·s s'améliore au fil du temps. Cet apprentissage se fait <strong>uniquement à partir de données anonymisées et agrégées</strong> — jamais à partir d'enregistrements ou de textes identifiants.</p>
      <p>Vous pouvez à tout moment refuser que vos données contribuent même de manière anonymisée à cet apprentissage, depuis votre espace, sans justification, sans perte de service.</p>

      <h2>7. Où sont stockées vos données</h2>
      <p><strong>Phase pilote (mai 2026) :</strong> serveurs OVH situés en France, dans un environnement chiffré et à accès strictement limité à l'équipe technique IVIA. Cette configuration sert uniquement à valider l'outil avant ouverture publique.</p>
      <p><strong>À la mise en activité commerciale</strong>, l'ensemble de l'infrastructure sera migré au Québec, conformément à l'esprit de la Loi 25. La date de migration sera publiée et chaque utilisateur·ice en sera informé·e.</p>

      <h2>8. Vos droits — Loi 25</h2>
      <p>Vous disposez à tout moment des droits suivants, exerçables depuis votre espace personnel ou sur simple demande à <a href="mailto:privacy@ivia.quebec">privacy@ivia.quebec</a> :</p>
      <ul>
        <li><strong>Accès</strong> à toutes vos données.</li>
        <li><strong>Rectification</strong> de toute donnée inexacte.</li>
        <li><strong>Suppression</strong> de tout ou partie de vos données.</li>
        <li><strong>Portabilité</strong> : récupérer une copie de vos données dans un format lisible.</li>
        <li><strong>Retrait du consentement</strong> à tout moment.</li>
        <li><strong>Plainte</strong> à la Commission d'accès à l'information du Québec si vous estimez vos droits non respectés.</li>
      </ul>

      <h2>9. Sécurité</h2>
      <ul>
        <li>Communications chiffrées (HTTPS / TLS) entre votre navigateur et nos serveurs.</li>
        <li>Audios chiffrés au repos sur le serveur.</li>
        <li>Accès aux données strictement journalisé.</li>
        <li>Aucune donnée sensible exportée vers des outils tiers non encadrés.</li>
      </ul>

      <h2>10. Modifications</h2>
      <p>Cette politique peut être mise à jour. Toute modification substantielle vous sera notifiée par courriel et dans votre espace, avec un délai raisonnable avant entrée en vigueur.</p>

      <p><strong>Version 1.0 — 9 mai 2026.</strong></p>

      <p class="long-form__back"><a href="index.html">← Retour à l'accueil</a></p>
    </div>
  </section>
</main>
'''
    html = public_page("Politique de confidentialité (Loi 25) — IVIA", "Politique de confidentialité IVIA conforme Loi 25 du Québec.", "confidentialite.html", body)
    (ROOT / "confidentialite.html").write_text(html, encoding="utf-8")


# ============================================================================
# CGU
# ============================================================================
def build_cgu():
    body = '''
<main id="main">
  <section class="public-hero public-hero--small">
    <div class="container">
      <p class="public-hero__overline">Conditions d'utilisation</p>
      <h1 class="public-hero__title">Conditions générales <em>d'utilisation</em></h1>
      <p class="public-hero__lede">Le cadre clair et bref de votre relation avec IVIA.</p>
    </div>
  </section>

  <section class="public-section">
    <div class="container long-form">

      <h2>1. Objet du service</h2>
      <p>IVIA est un espace d'écoute audio opéré par des praticien·ne·s humain·e·s, à destination du grand public au Québec. Deux formats sont proposés : la séance en rendez-vous direct (audio en temps réel) et la séance en différé (vous déposez un enregistrement, le ou la praticien·ne vous renvoie un résumé écrit dans un délai annoncé). Dans les deux cas, vous recevez un résumé écrit et trois pistes concrètes.</p>

      <h2>2. Qui peut utiliser IVIA</h2>
      <p>Toute personne majeure au Québec peut ouvrir un compte. Pour les mineur·e·s, l'usage doit se faire avec accompagnement d'un·e adulte responsable. IVIA se réserve le droit de refuser un compte à toute personne qui détournerait le service de son objet (par exemple en l'utilisant comme moyen de contact répété d'un·e tiers).</p>

      <h2>3. Ce qui est inclus</h2>
      <ul>
        <li>L'enregistrement, la transcription et le traitement de votre audio.</li>
        <li>Un résumé écrit et trois pistes concrètes.</li>
        <li>L'accès à votre journal personnel.</li>
        <li>L'accès à la bibliothèque d'articles, gratuitement.</li>
        <li>L'accès à votre espace pour exercer vos droits (Loi 25).</li>
      </ul>

      <h2>4. Ce qui n'est pas inclus</h2>
      <ul>
        <li><strong>Aucun service d'urgence.</strong> En cas de détresse, composez le <a href="urgence.html">911 ou un autre numéro d'urgence</a>.</li>
        <li><strong>Aucun diagnostic médical, psychologique ou psychiatrique.</strong></li>
        <li><strong>Aucune ordonnance, aucun traitement médicamenteux.</strong></li>
        <li>Aucune garantie sur la résolution de votre situation. IVIA est un appui, pas un raccourci.</li>
      </ul>

      <h2>5. Tarifs (en cours de finalisation)</h2>
      <p>Pendant la phase pilote (mai-août 2026), l'usage de l'écoute audio est <strong>gratuit</strong> dans le cadre des tests internes. La grille tarifaire publique sera publiée avant l'ouverture commerciale, en cohérence avec le plan d'affaires IVIA et avec les conditions négociées avec les praticien·ne·s du réseau.</p>

      <h2>6. Vos engagements</h2>
      <ul>
        <li>Utiliser IVIA pour vous-même, en bonne foi.</li>
        <li>Ne pas enregistrer ni transmettre la parole d'une autre personne sans son consentement explicite.</li>
        <li>Ne pas utiliser IVIA pour menacer, harceler ou nuire à un·e tiers.</li>
        <li>Respecter la propriété intellectuelle des contenus mis à disposition.</li>
      </ul>

      <h2>7. Nos engagements</h2>
      <ul>
        <li>Vous écouter avec soin, à travers nos praticien·ne·s.</li>
        <li>Protéger vos données selon la <a href="confidentialite.html">politique de confidentialité</a>.</li>
        <li>Ne jamais revendre, exposer ou commercialiser vos paroles.</li>
        <li>Vous prévenir clairement de toute évolution importante du service.</li>
      </ul>

      <h2>8. Suspension et résiliation</h2>
      <p>Vous pouvez fermer votre compte à tout moment, depuis votre espace. IVIA peut suspendre un compte en cas d'usage manifestement contraire aux engagements de la section 6, après notification.</p>

      <h2>9. Loi applicable et juridiction</h2>
      <p>Les présentes conditions sont régies par les lois en vigueur dans la province de Québec, Canada. Tout litige relèvera des tribunaux compétents du district judiciaire de Montréal.</p>

      <h2>10. Contact</h2>
      <p>Pour toute question : <a href="mailto:contact@ivia.quebec">contact@ivia.quebec</a></p>

      <p><strong>Version pilote 0.9 — 9 mai 2026.</strong></p>

      <p class="long-form__back"><a href="index.html">← Retour à l'accueil</a></p>
    </div>
  </section>
</main>
'''
    html = public_page("Conditions d'utilisation — IVIA", "Conditions générales d'utilisation IVIA.", "cgu.html", body)
    (ROOT / "cgu.html").write_text(html, encoding="utf-8")


# ============================================================================
# TESTS — hub d'accès direct aux 3 comptes fictifs
# ============================================================================
def build_tests():
    body = '''
<main id="main">
  <section class="public-hero public-hero--small public-hero--tests">
    <div class="container">
      <p class="public-hero__overline">Espace tests · Accès direct sans authentification</p>
      <h1 class="public-hero__title">Trois comptes <em>fictifs</em>, déjà ouverts.</h1>
      <p class="public-hero__lede">
        En phase pilote, vous pouvez tester l'outil bout-en-bout sans inscription ni mot de passe.
        Les comptes ci-dessous sont alimentés avec des données représentatives pour rendre le test crédible.
      </p>
    </div>
  </section>

  <section class="public-section">
    <div class="container">

      <div class="tests-grid">

        <article class="test-card test-card--client">
          <header class="test-card__head">
            <span class="test-card__role">Client·e</span>
            <h2>Camille Leblanc</h2>
            <p class="test-card__sub">35 ans · Montréal · 2 écoutes effectuées · 1 résumé reçu</p>
          </header>
          <div class="test-card__body">
            <p>Vue de la personne qui vit l'écoute IVIA : ses audios, son résumé, son journal, ses outils.</p>
            <ul class="test-card__features">
              <li>Tableau de bord personnel</li>
              <li>Lancer une nouvelle écoute audio</li>
              <li>Recevoir un résumé écrit (mockup)</li>
              <li>Tenir un journal de vie</li>
              <li>4 outils interactifs (cercle, fréquence, sommeil, préparer)</li>
              <li>Choisir un·e praticien·ne et payer (mockup Stripe)</li>
            </ul>
          </div>
          <footer class="test-card__foot">
            <a href="client/dashboard.html" class="btn btn--primary">Entrer comme Camille →</a>
            <a href="client/audio-async.html" class="btn btn--ghost btn--sm">Aller direct à l'écoute</a>
          </footer>
        </article>

        <article class="test-card test-card--praticien">
          <header class="test-card__head">
            <span class="test-card__role">Praticien·ne</span>
            <h2>Mylène Tremblay</h2>
            <p class="test-card__sub">Plan Standard · 4 client·e·s actif·ve·s · 3 audios à traiter</p>
          </header>
          <div class="test-card__body">
            <p>Vue du ou de la praticien·ne qui reçoit, écoute, rédige le résumé et accompagne sa clientèle.</p>
            <ul class="test-card__features">
              <li>Tableau de bord praticien·ne</li>
              <li>Agenda et rendez-vous</li>
              <li>Audios à traiter avec timeline + transcription assistée</li>
              <li>Rédaction du résumé client</li>
              <li>Mes offres et tarifs personnalisés</li>
              <li>Mon abonnement et facturation</li>
              <li>Outils internes (cercle, fréquence, préparer)</li>
            </ul>
          </div>
          <footer class="test-card__foot">
            <a href="praticien/index.html" class="btn btn--primary">Entrer comme Mylène →</a>
            <a href="praticien/audios.html" class="btn btn--ghost btn--sm">Voir les audios à traiter</a>
          </footer>
        </article>

        <article class="test-card test-card--admin">
          <header class="test-card__head">
            <span class="test-card__role">Admin</span>
            <h2>David Phaneuf</h2>
            <p class="test-card__sub">Fondateur · Vue plateforme complète · Pilote M1-M3</p>
          </header>
          <div class="test-card__body">
            <p>Vue de pilotage de la plateforme — santé du service, croissance, finance, qualité de l'outil.</p>
            <ul class="test-card__features">
              <li>Vue d'ensemble (KPIs pilote)</li>
              <li>Section Analytique : finance, données, résultats</li>
              <li>Gestion des praticien·ne·s</li>
              <li>Gestion des client·e·s</li>
              <li>Suivi audios (toute la plateforme)</li>
              <li>Finance et abonnements</li>
              <li>Paramètres système</li>
            </ul>
          </div>
          <footer class="test-card__foot">
            <a href="admin/index.html" class="btn btn--primary">Entrer comme David →</a>
            <a href="admin/analytique.html" class="btn btn--ghost btn--sm">Voir l'analytique</a>
          </footer>
        </article>

      </div>

      <div class="tests-extras">
        <h2>Phase de test — ce qu'on cherche à valider</h2>
        <p>Avant l'ouverture publique avec un réseau de praticien·ne·s, nous voulons valider trois choses :</p>
        <ol>
          <li><strong>La qualité de l'analyse</strong> que produit notre outil interne sur des audios réels (sans praticien·ne dans la boucle pour cette phase).</li>
          <li><strong>La fluidité du parcours client</strong> de A à Z : enregistrer, attendre, recevoir, lire, agir.</li>
          <li><strong>L'expérience praticien·ne</strong> : est-ce qu'on lui fait gagner du temps ? Est-ce qu'on respecte sa pratique ?</li>
        </ol>
        <p>L'écoute en mode test fonctionne <strong>sans praticien·ne assigné·e</strong> : l'enregistrement est traité par notre outil interne, qui produit directement un résumé de démonstration. C'est exactement la phase 1 décrite dans le plan d'affaires.</p>

        <h3>Liens utiles pendant les tests</h3>
        <ul>
          <li><a href="index.html">Vue publique (la « vraie » landing)</a></li>
          <li><a href="comment.html">Comment ça fonctionne</a></li>
          <li><a href="bibliotheque.html">Bibliothèque (16 articles)</a></li>
          <li><a href="urgence.html">Ressources d'urgence</a></li>
          <li><a href="demo/index.html">Vue mockups originale (toutes les pages d'un coup)</a></li>
        </ul>
      </div>

    </div>
  </section>
</main>
'''
    html = public_page("Espace tests — IVIA", "Hub d'accès direct aux 3 comptes fictifs (client, praticien, admin) pour la phase pilote.", "tests.html", body)
    (ROOT / "tests.html").write_text(html, encoding="utf-8")


# ============================================================================
# CSS public additionnel
# ============================================================================
PUBLIC_CSS = r'''
/* ============================================================
   IVIA — Couche publique (landing, comment, bibliothèque, urgence)
   ============================================================ */

.public-page main { padding-top: var(--space-8); }

/* ---------- Hero ---------- */
.public-hero {
  padding-block: var(--space-20) var(--space-12);
  position: relative;
}
.public-hero--small { padding-block: var(--space-12) var(--space-8); }
.public-hero__inner { max-width: 64rem; margin-inline: auto; text-align: left; }
.public-hero__overline {
  font-size: var(--text-xs);
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--color-text-muted);
  margin-bottom: var(--space-6);
  font-family: var(--font-body);
}
.public-hero__title {
  font-size: var(--text-hero);
  font-family: var(--font-display);
  line-height: 1.05;
  letter-spacing: -0.015em;
  margin-bottom: var(--space-6);
  text-wrap: balance;
}
.public-hero__title em {
  font-style: italic;
  color: var(--color-rose);
}
.public-hero__title-soft {
  font-style: italic;
  font-family: var(--font-serif);
  color: var(--color-text-muted);
  font-weight: 400;
}
.public-hero__lede {
  font-size: var(--text-lg);
  font-family: var(--font-serif);
  color: var(--color-text-muted);
  max-width: 56ch;
  margin-bottom: var(--space-8);
}
.public-hero__cta {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
  margin-bottom: var(--space-8);
}
.public-hero__disclaimer {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  max-width: 56ch;
  border-left: 2px solid var(--color-rose);
  padding-left: var(--space-3);
}

.public-hero--tests .public-hero__title em { color: var(--color-aubergine); }

/* ---------- Sections ---------- */
.public-section { padding-block: var(--space-16); }
.public-section--soft { background: var(--color-creme-warm); }
.section-overline {
  font-size: var(--text-xs);
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--color-text-muted);
  margin-bottom: var(--space-3);
}
.section-title {
  font-size: var(--text-2xl);
  font-family: var(--font-display);
  margin-bottom: var(--space-6);
  text-wrap: balance;
}
.section-title em { font-style: italic; color: var(--color-rose); }
.section-lede {
  font-size: var(--text-lg);
  font-family: var(--font-serif);
  color: var(--color-text-muted);
  max-width: 60ch;
  margin-bottom: var(--space-10);
}
.section-foot { margin-top: var(--space-10); }

/* ---------- Trois portes ---------- */
.trois-portes {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--space-6);
  margin-top: var(--space-8);
}
.porte {
  display: block;
  background: var(--color-surface);
  border: 1px solid var(--color-divider);
  border-radius: var(--radius-xl);
  padding: var(--space-8);
  text-decoration: none;
  color: var(--color-text);
  transition: transform var(--transition), box-shadow var(--transition), border-color var(--transition);
  position: relative;
  overflow: hidden;
}
.porte::before {
  content: '';
  position: absolute;
  inset: 0 0 auto 0;
  height: 5px;
  background: var(--accent, var(--color-rose));
  opacity: 0.7;
}
.porte--ecoute { --accent: var(--color-rose); }
.porte--lire { --accent: var(--color-mousse); }
.porte--journal { --accent: var(--color-aubergine); }
.porte:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: var(--accent);
}
.porte__icon {
  width: 64px; height: 64px;
  margin-bottom: var(--space-5);
  color: var(--accent);
}
.porte h3 {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  margin-bottom: var(--space-3);
}
.porte p {
  color: var(--color-text-muted);
  font-family: var(--font-serif);
  font-size: var(--text-base);
  margin-bottom: var(--space-5);
}
.porte__cta {
  display: inline-block;
  font-family: var(--font-body);
  color: var(--accent);
  font-weight: 500;
  letter-spacing: 0.02em;
}

/* ---------- Ce qu'IVIA est / n'est pas ---------- */
.ce-quivia {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: var(--space-10);
}
.puces {
  list-style: none;
  padding-left: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}
.puces li {
  position: relative;
  padding-left: 1.4em;
  font-family: var(--font-serif);
  font-size: var(--text-base);
  line-height: 1.5;
}
.puces li::before {
  content: '';
  position: absolute;
  left: 0; top: 0.55em;
  width: 0.6em; height: 0.6em;
  border-radius: 50%;
  background: var(--puce-color, var(--color-text-muted));
}
.puces--vert li::before { background: var(--color-mousse); }
.puces--rose li::before { background: var(--color-rose); }

/* ---------- Cercle 5 zones ---------- */
.cercle-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: var(--space-5);
  margin-top: var(--space-6);
}
.zone {
  background: var(--color-surface);
  border: 1px solid var(--color-divider);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  border-top: 4px solid var(--zone-c, var(--color-rose));
}
.zone h3 {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  margin-bottom: var(--space-2);
  color: var(--zone-c);
}
.zone p {
  color: var(--color-text-muted);
  font-size: var(--text-sm);
  font-family: var(--font-serif);
}
.zone--corps { --zone-c: var(--color-rose); }
.zone--relation { --zone-c: var(--color-miel); }
.zone--sens { --zone-c: var(--color-aubergine); }
.zone--ressources { --zone-c: var(--color-mousse); }
.zone--frequence { --zone-c: var(--color-aubergine); }

/* ---------- Parcours 4 étapes ---------- */
.parcours {
  list-style: none;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: var(--space-6);
  counter-reset: parcours;
  margin-top: var(--space-6);
}
.parcours li {
  background: var(--color-surface);
  border: 1px solid var(--color-divider);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  position: relative;
}
.parcours__num {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2.4rem; height: 2.4rem;
  border-radius: 50%;
  background: var(--color-aubergine);
  color: var(--color-creme);
  font-family: var(--font-display);
  font-size: var(--text-lg);
  margin-bottom: var(--space-3);
}
.parcours h3 {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  margin-bottom: var(--space-2);
}
.parcours p {
  color: var(--color-text-muted);
  font-family: var(--font-serif);
  font-size: var(--text-sm);
  line-height: 1.5;
}

/* ---------- Featured articles ---------- */
.featured-articles {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: var(--space-5);
  margin-top: var(--space-6);
}
.featured-card {
  display: flex; flex-direction: column; gap: var(--space-2);
  background: var(--color-surface);
  border: 1px solid var(--color-divider);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  text-decoration: none; color: var(--color-text);
  transition: transform var(--transition), border-color var(--transition);
}
.featured-card:hover { transform: translateY(-3px); border-color: var(--color-aubergine); }
.featured-card__num {
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  color: var(--color-rose);
  font-weight: 400;
}
.featured-card__axe {
  font-size: var(--text-xs);
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--color-text-muted);
}
.featured-card h3 {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  line-height: 1.2;
  margin-block: var(--space-2);
}
.featured-card p {
  color: var(--color-text-muted);
  font-family: var(--font-serif);
  font-size: var(--text-sm);
  line-height: 1.5;
  flex-grow: 1;
}
.featured-card__cta {
  margin-top: var(--space-3);
  font-weight: 500;
  color: var(--color-aubergine);
}

/* ---------- Confiance ---------- */
.confiance__grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: var(--space-6);
  margin-top: var(--space-6);
}
.confiance__grid h3 {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  margin-bottom: var(--space-2);
  color: var(--color-aubergine);
}
.confiance__grid p {
  color: var(--color-text-muted);
  font-family: var(--font-serif);
  font-size: var(--text-base);
  line-height: 1.55;
}

/* ---------- Bandeau urgence ---------- */
.bandeau-urgence {
  background: var(--color-aubergine);
  color: var(--color-creme);
  padding-block: var(--space-10);
}
.bandeau-urgence__inner {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: var(--space-8);
  align-items: center;
}
@media (max-width: 720px) {
  .bandeau-urgence__inner { grid-template-columns: 1fr; }
}
.bandeau-urgence__title {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  margin-bottom: var(--space-2);
}
.bandeau-urgence__lede {
  opacity: 0.85;
  font-family: var(--font-serif);
  max-width: 50ch;
}
.bandeau-urgence__nums {
  display: flex; flex-wrap: wrap; gap: var(--space-3);
}
.bandeau-urgence__nums a {
  display: flex; flex-direction: column;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: var(--radius-md);
  padding: var(--space-3) var(--space-4);
  text-decoration: none;
  color: var(--color-creme);
  min-width: 7rem;
  transition: background var(--transition);
}
.bandeau-urgence__nums a:hover {
  background: rgba(255,255,255,0.16);
}
.bandeau-urgence__nums strong {
  font-family: var(--font-display);
  font-size: var(--text-base);
}
.bandeau-urgence__nums span {
  font-size: var(--text-xs);
  opacity: 0.7;
  letter-spacing: 0.05em;
}

/* ---------- Bibliothèque ---------- */
.axe-nav {
  position: sticky; top: 4.5rem; z-index: 5;
  background: rgba(247,246,242,0.92);
  backdrop-filter: blur(10px);
  border-block: 1px solid var(--color-divider);
  padding-block: var(--space-3);
}
.axe-nav__inner {
  display: flex; flex-wrap: wrap; gap: var(--space-3);
  justify-content: center;
}
.axe-nav__item {
  text-decoration: none;
  color: var(--color-text);
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-divider);
  font-family: var(--font-body);
  font-size: var(--text-sm);
  transition: all var(--transition);
}
.axe-nav__item:hover {
  background: var(--color-aubergine);
  color: var(--color-creme);
  border-color: var(--color-aubergine);
}

.public-section--axe { padding-block: var(--space-12); }
.public-section--axe:nth-of-type(odd) { background: var(--color-creme-warm); }

.axe-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: var(--space-4);
  margin-top: var(--space-6);
}
.axe-card {
  background: var(--color-surface);
  border: 1px solid var(--color-divider);
  border-radius: var(--radius-md);
  padding: var(--space-5);
  text-decoration: none;
  color: var(--color-text);
  transition: all var(--transition);
}
.axe-card:hover {
  border-color: var(--color-aubergine);
  transform: translateY(-2px);
}
.axe-card__num {
  display: inline-block;
  font-family: var(--font-display);
  font-size: var(--text-lg);
  color: var(--color-rose);
  margin-bottom: var(--space-2);
}
.axe-card h3 {
  font-family: var(--font-display);
  font-size: var(--text-base);
  line-height: 1.3;
}

/* ---------- Article complet (in-page) ---------- */
.article-full {
  padding-block: var(--space-12);
  border-top: 1px solid var(--color-divider);
}
.article-full__inner { max-width: 42rem; margin-inline: auto; }
.article-full__breadcrumb {
  font-size: var(--text-xs);
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--color-text-muted);
  margin-bottom: var(--space-3);
}
.article-full__title {
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  margin-bottom: var(--space-8);
  line-height: 1.1;
}
.article-full__body {
  font-family: var(--font-serif);
  font-size: 1.125rem;
  line-height: 1.7;
  color: var(--color-text);
}
.article-full__body h2 {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  margin-block: var(--space-8) var(--space-3);
  color: var(--color-aubergine);
}
.article-full__body h3 {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  margin-block: var(--space-6) var(--space-2);
}
.article-full__body p { margin-bottom: var(--space-4); max-width: 64ch; }
.article-full__body ul {
  margin-block: var(--space-4);
  padding-left: 1.5em;
}
.article-full__body li { margin-bottom: var(--space-2); }
.article-full__body blockquote {
  border-left: 3px solid var(--color-rose);
  padding-left: var(--space-5);
  margin-block: var(--space-6);
  font-style: italic;
  color: var(--color-text-muted);
}
.article-full__body hr.article-rule {
  border: none;
  border-top: 1px solid var(--color-divider);
  margin-block: var(--space-6);
  width: 30%;
}
.article-full__body em { font-style: italic; }
.article-full__body strong { font-weight: 600; color: var(--color-text); }
.article-full__back {
  margin-top: var(--space-10);
  font-size: var(--text-sm);
}

/* ---------- Long-form (pages texte) ---------- */
.long-form {
  max-width: 44rem;
  margin-inline: auto;
  font-family: var(--font-serif);
  font-size: 1.0625rem;
  line-height: 1.7;
}
.long-form h2 {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  margin-block: var(--space-10) var(--space-4);
  color: var(--color-aubergine);
}
.long-form h3 {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  margin-block: var(--space-6) var(--space-2);
}
.long-form p { margin-bottom: var(--space-4); }
.long-form ul { padding-left: 1.5em; margin-block: var(--space-4); }
.long-form li { margin-bottom: var(--space-2); }
.long-form .callout {
  background: var(--color-surface);
  border-left: 4px solid var(--color-aubergine);
  border-radius: var(--radius-md);
  padding: var(--space-5) var(--space-6);
  margin-block: var(--space-6);
}
.long-form .callout--info { border-left-color: var(--color-mousse); }
.long-form__cta {
  margin-top: var(--space-12);
  display: flex; flex-wrap: wrap; gap: var(--space-3);
}
.long-form__back { margin-top: var(--space-12); font-size: var(--text-sm); }

/* ---------- Urgence ---------- */
.urgence-page { background: linear-gradient(180deg, #2A1F26 0%, #1A1015 100%); color: #F0E8DC; min-height: 100vh; }
.urgence-page .site-header { background: rgba(20,12,16,0.85); border-bottom-color: rgba(255,255,255,0.1); }
.urgence-page .site-header .nav a, .urgence-page .brand__name { color: #F0E8DC; }
.urgence-page .site-footer { background: rgba(0,0,0,0.3); color: #F0E8DC; border-top: 1px solid rgba(255,255,255,0.1); }
.urgence-page .site-footer h4 { color: #F0E8DC; }
.urgence-page .site-footer a { color: #F0E8DC; opacity: 0.85; }
.urgence-page .vrille-fixe { opacity: 0.15; }

.urgence-hero { padding-block: var(--space-16) var(--space-10); }
.urgence-hero__overline {
  font-size: var(--text-xs);
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: rgba(240,232,220,0.6);
  margin-bottom: var(--space-4);
}
.urgence-hero__title {
  font-family: var(--font-display);
  font-size: var(--text-hero);
  line-height: 1.05;
  margin-bottom: var(--space-5);
}
.urgence-hero__title em { color: #FF8E73; font-style: italic; }
.urgence-hero__lede {
  font-family: var(--font-serif);
  font-size: var(--text-lg);
  max-width: 56ch;
  color: rgba(240,232,220,0.85);
}

.urgence-grille {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--space-5);
  margin-bottom: var(--space-12);
}
.urgence-bloc {
  display: flex; flex-direction: column;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  text-decoration: none;
  color: #F0E8DC;
  border-left: 5px solid var(--c, #FF8E73);
  transition: all var(--transition);
}
.urgence-bloc:hover {
  background: rgba(255,255,255,0.08);
  transform: translateX(4px);
}
.urgence-bloc__num {
  font-family: var(--font-display);
  font-size: 2.4rem;
  font-weight: 400;
  color: var(--c);
  line-height: 1;
  margin-bottom: var(--space-2);
}
.urgence-bloc__label {
  font-size: var(--text-sm);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  opacity: 0.7;
  margin-bottom: var(--space-3);
}
.urgence-bloc p {
  font-family: var(--font-serif);
  flex-grow: 1;
  color: rgba(240,232,220,0.85);
  margin-bottom: var(--space-4);
  line-height: 1.5;
}
.urgence-bloc__cta {
  font-weight: 500;
  letter-spacing: 0.02em;
  color: var(--c);
}
.urgence-bloc--rouge { --c: #FF6B6B; }
.urgence-bloc--bleu { --c: #6BAEFF; }
.urgence-bloc--mauve { --c: #B59AE0; }
.urgence-bloc--vert { --c: #8FD49C; }

.urgence-h2 {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  margin-block: var(--space-10) var(--space-5);
}
.urgence-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: var(--space-4); margin-bottom: var(--space-12); }
.urgence-item {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: var(--radius-md);
  padding: var(--space-5);
}
.urgence-item h3 {
  font-family: var(--font-display);
  font-size: var(--text-base);
  margin-bottom: var(--space-2);
}
.urgence-item p {
  font-family: var(--font-serif);
  font-size: var(--text-sm);
  color: rgba(240,232,220,0.85);
  line-height: 1.55;
}
.urgence-item a { color: #FF8E73; }

.urgence-rappel {
  background: rgba(255,142,115,0.08);
  border: 1px solid rgba(255,142,115,0.3);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
}
.urgence-rappel h3 {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  margin-bottom: var(--space-3);
}
.urgence-rappel p {
  font-family: var(--font-serif);
  color: rgba(240,232,220,0.9);
  margin-bottom: var(--space-3);
  line-height: 1.6;
}
.urgence-rappel a { color: #FF8E73; }

/* ---------- Tests page ---------- */
.tests-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--space-6);
  margin-bottom: var(--space-16);
}
.test-card {
  background: var(--color-surface);
  border: 1px solid var(--color-divider);
  border-radius: var(--radius-xl);
  display: flex; flex-direction: column;
  overflow: hidden;
}
.test-card__head {
  padding: var(--space-6);
  border-bottom: 1px solid var(--color-divider);
  border-top: 5px solid var(--card-c, var(--color-rose));
}
.test-card--client { --card-c: var(--color-rose); }
.test-card--praticien { --card-c: var(--color-mousse); }
.test-card--admin { --card-c: var(--color-aubergine); }
.test-card__role {
  font-size: var(--text-xs);
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--card-c);
  font-weight: 600;
}
.test-card h2 {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  margin-block: var(--space-2);
}
.test-card__sub {
  font-family: var(--font-serif);
  font-size: var(--text-sm);
  color: var(--color-text-muted);
}
.test-card__body { padding: var(--space-6); flex-grow: 1; }
.test-card__body p {
  font-family: var(--font-serif);
  color: var(--color-text-muted);
  margin-bottom: var(--space-4);
  line-height: 1.55;
}
.test-card__features {
  list-style: none;
  padding: 0;
  display: flex; flex-direction: column; gap: var(--space-1);
}
.test-card__features li {
  position: relative;
  padding-left: 1.4em;
  font-size: var(--text-sm);
  font-family: var(--font-body);
}
.test-card__features li::before {
  content: '✓';
  position: absolute;
  left: 0; top: 0;
  color: var(--card-c);
  font-weight: 600;
}
.test-card__foot {
  padding: var(--space-5) var(--space-6);
  border-top: 1px solid var(--color-divider);
  background: var(--color-creme-warm);
  display: flex; flex-wrap: wrap; gap: var(--space-3);
  align-items: center;
}

.tests-extras {
  max-width: 44rem;
  margin: 0 auto;
  font-family: var(--font-serif);
  font-size: 1rem;
  line-height: 1.6;
}
.tests-extras h2 {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  margin-bottom: var(--space-4);
  color: var(--color-aubergine);
}
.tests-extras h3 {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  margin-block: var(--space-6) var(--space-3);
}
.tests-extras ol, .tests-extras ul { padding-left: 1.5em; margin-block: var(--space-3); }
.tests-extras li { margin-bottom: var(--space-2); }

/* ---------- Mobile ---------- */
@media (max-width: 720px) {
  .public-hero__title { font-size: clamp(2rem, 1.5rem + 4vw, 3rem); }
  .public-hero__cta { flex-direction: column; }
  .public-hero__cta .btn { width: 100%; }
  .axe-nav { position: relative; top: 0; }
}
'''


def build_public_css():
    (ROOT / "shared" / "public.css").write_text(PUBLIC_CSS, encoding="utf-8")


def build():
    build_public_css()
    build_landing()
    build_comment()
    build_pourquoi()
    build_bibliotheque()
    build_urgence()
    build_mentions()
    build_confidentialite()
    build_cgu()
    build_tests()
    print("✓ Pages publiques générées : index, comment, pourquoi, bibliotheque, urgence, mentions, confidentialite, cgu, tests")


if __name__ == "__main__":
    build()

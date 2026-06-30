"""Pages côté client (sauf index.html qui est manuscrit)."""
from pathlib import Path
from build_pages import page, CLIENT_NAV, CLIENT_ACTIONS, FOOTER_CLIENT

OUT = Path(__file__).parent / "client"

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
        <li><a href="dashboard.html">Mon espace</a></li>
        <li><a href="compte.html">Mon compte</a></li>
        <li><a href="mot-de-passe-oublie.html">Mot de passe oublié</a></li>
      </ul></div>
      <div><h4>Mentions</h4><ul role="list">
        <li><a href="mentions.html">Mentions légales</a></li>
        <li><a href="confidentialite.html">Confidentialité (Loi 25)</a></li>
        <li><a href="cgu.html">CGU</a></li>
        <li><a href="mailto:contact@ivia.quebec">Nous écrire</a></li>
      </ul></div>
    </div>
    <div class="site-footer__bottom">
      <span>© 2026 IVIA — Pour le peuple, par le peuple.</span>
      <span>IVIA n'est pas un service d'urgence.</span>
    </div>
  </div>
</footer>'''


# =============================================================
# PRATICIENS — annuaire public
# =============================================================
PRATICIENS_BODY = '''
<section class="section">
  <div class="container">
    <span class="eyebrow">Annuaire</span>
    <h1 class="section-title" style="font-size: var(--text-2xl);">Les personnes qui écoutent.</h1>
    <p class="section-lede" style="max-width: 56ch;">
      Chaque praticien·ne d'IVIA a été reçu·e en entretien, formé·e à la posture d'écoute commune,
      et travaille selon les six repères de la maison. Choisissez par voie, par lieu, ou par disponibilité.
    </p>

    <div class="cluster" style="margin-bottom: var(--space-8);">
      <span class="chip chip--rose">Toutes les voies</span>
      <span class="chip">Fréquence</span>
      <span class="chip">Sommeil</span>
      <span class="chip">Connaissance</span>
      <span class="chip">Disponible cette semaine</span>
      <span class="chip">En français</span>
      <span class="chip">À distance</span>
    </div>

    <div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: var(--space-6);">

      <article class="card card--clickable">
        <div style="display:flex; gap:var(--space-4); align-items:flex-start; margin-bottom:var(--space-4);">
          <div style="width:64px; height:64px; border-radius:50%; background:linear-gradient(135deg, #C58A8A, #D89260); flex-shrink:0;"></div>
          <div>
            <h3 class="card__title" style="margin-bottom:2px;">Maïté Lavoie-Therrien</h3>
            <p style="font-size:var(--text-xs); color:var(--color-text-muted);">Montréal · à distance</p>
          </div>
        </div>
        <p style="font-family:var(--font-serif); font-size:var(--text-sm); color:var(--color-text-muted); margin-bottom:var(--space-4);">
          « J'écoute ce qui ne se dit pas tout de suite. Mon travail commence souvent là où le silence s'installe. »
        </p>
        <div class="cluster" style="margin-bottom:var(--space-4);">
          <span class="chip chip--mousse">Fréquence</span>
          <span class="chip chip--glacier">Sommeil</span>
        </div>
        <div class="flex-between">
          <span style="font-size:var(--text-xs); color:var(--color-mousse);"><span class="status-dot status-dot--ok"></span> Place dispo dès jeudi</span>
          <a href="rendez-vous.html" class="btn btn--ghost btn--sm">Voir →</a>
        </div>
      </article>

      <article class="card card--clickable">
        <div style="display:flex; gap:var(--space-4); align-items:flex-start; margin-bottom:var(--space-4);">
          <div style="width:64px; height:64px; border-radius:50%; background:linear-gradient(135deg, #6B8266, #8DA9B8); flex-shrink:0;"></div>
          <div>
            <h3 class="card__title" style="margin-bottom:2px;">Étienne Grondin-Côté</h3>
            <p style="font-size:var(--text-xs); color:var(--color-text-muted);">Québec · présentiel & visio</p>
          </div>
        </div>
        <p style="font-family:var(--font-serif); font-size:var(--text-sm); color:var(--color-text-muted); margin-bottom:var(--space-4);">
          « Comprendre avant d'agir. C'est souvent ce que les gens viennent chercher, sans le formuler ainsi. »
        </p>
        <div class="cluster" style="margin-bottom:var(--space-4);">
          <span class="chip chip--lavande">Connaissance</span>
        </div>
        <div class="flex-between">
          <span style="font-size:var(--text-xs); color:var(--color-text-muted);"><span class="status-dot status-dot--pending"></span> Plein jusqu'au 22 mai</span>
          <a href="rendez-vous.html" class="btn btn--ghost btn--sm">Voir →</a>
        </div>
      </article>

      <article class="card card--clickable">
        <div style="display:flex; gap:var(--space-4); align-items:flex-start; margin-bottom:var(--space-4);">
          <div style="width:64px; height:64px; border-radius:50%; background:linear-gradient(135deg, #9A8AB8, #7B5B7E); flex-shrink:0;"></div>
          <div>
            <h3 class="card__title" style="margin-bottom:2px;">Soraya Ben-Amar</h3>
            <p style="font-size:var(--text-xs); color:var(--color-text-muted);">Sherbrooke · à distance</p>
          </div>
        </div>
        <p style="font-family:var(--font-serif); font-size:var(--text-sm); color:var(--color-text-muted); margin-bottom:var(--space-4);">
          « Je travaille beaucoup par la voix et par l'écoute du rythme. Ce qui se dit, et ce qui se respire entre. »
        </p>
        <div class="cluster" style="margin-bottom:var(--space-4);">
          <span class="chip chip--mousse">Fréquence</span>
          <span class="chip chip--rose">Famille</span>
        </div>
        <div class="flex-between">
          <span style="font-size:var(--text-xs); color:var(--color-mousse);"><span class="status-dot status-dot--ok"></span> Disponible cette semaine</span>
          <a href="rendez-vous.html" class="btn btn--ghost btn--sm">Voir →</a>
        </div>
      </article>

      <article class="card card--clickable">
        <div style="display:flex; gap:var(--space-4); align-items:flex-start; margin-bottom:var(--space-4);">
          <div style="width:64px; height:64px; border-radius:50%; background:linear-gradient(135deg, #D9A441, #D89260); flex-shrink:0;"></div>
          <div>
            <h3 class="card__title" style="margin-bottom:2px;">Marc-André Pelletier</h3>
            <p style="font-size:var(--text-xs); color:var(--color-text-muted);">Trois-Rivières · à distance</p>
          </div>
        </div>
        <p style="font-family:var(--font-serif); font-size:var(--text-sm); color:var(--color-text-muted); margin-bottom:var(--space-4);">
          « Le sommeil est un baromètre honnête. Il dit souvent ce que l'on n'arrive pas à dire le jour. »
        </p>
        <div class="cluster" style="margin-bottom:var(--space-4);">
          <span class="chip chip--glacier">Sommeil</span>
          <span class="chip chip--lavande">Connaissance</span>
        </div>
        <div class="flex-between">
          <span style="font-size:var(--text-xs); color:var(--color-mousse);"><span class="status-dot status-dot--ok"></span> Place dispo demain</span>
          <a href="rendez-vous.html" class="btn btn--ghost btn--sm">Voir →</a>
        </div>
      </article>

      <article class="card card--clickable">
        <div style="display:flex; gap:var(--space-4); align-items:flex-start; margin-bottom:var(--space-4);">
          <div style="width:64px; height:64px; border-radius:50%; background:linear-gradient(135deg, #8DA9B8, #6B8266); flex-shrink:0;"></div>
          <div>
            <h3 class="card__title" style="margin-bottom:2px;">Nicole Tremblay-Roy</h3>
            <p style="font-size:var(--text-xs); color:var(--color-text-muted);">Saguenay · à distance</p>
          </div>
        </div>
        <p style="font-family:var(--font-serif); font-size:var(--text-sm); color:var(--color-text-muted); margin-bottom:var(--space-4);">
          « Mon travail, c'est de tenir un cadre suffisamment solide pour que vous n'ayez plus à le faire. »
        </p>
        <div class="cluster" style="margin-bottom:var(--space-4);">
          <span class="chip chip--rose">Famille</span>
          <span class="chip chip--lavande">Connaissance</span>
        </div>
        <div class="flex-between">
          <span style="font-size:var(--text-xs); color:var(--color-text-muted);"><span class="status-dot status-dot--pending"></span> Liste d'attente</span>
          <a href="rendez-vous.html" class="btn btn--ghost btn--sm">Voir →</a>
        </div>
      </article>

      <article class="card card--clickable">
        <div style="display:flex; gap:var(--space-4); align-items:flex-start; margin-bottom:var(--space-4);">
          <div style="width:64px; height:64px; border-radius:50%; background:linear-gradient(135deg, #C58A8A, #9A8AB8); flex-shrink:0;"></div>
          <div>
            <h3 class="card__title" style="margin-bottom:2px;">Jean-Philippe Côté</h3>
            <p style="font-size:var(--text-xs); color:var(--color-text-muted);">Gatineau · à distance</p>
          </div>
        </div>
        <p style="font-family:var(--font-serif); font-size:var(--text-sm); color:var(--color-text-muted); margin-bottom:var(--space-4);">
          « Mettre des mots simples sur ce qui pèse, sans rajouter de complication. C'est déjà beaucoup. »
        </p>
        <div class="cluster" style="margin-bottom:var(--space-4);">
          <span class="chip chip--mousse">Fréquence</span>
          <span class="chip chip--glacier">Sommeil</span>
        </div>
        <div class="flex-between">
          <span style="font-size:var(--text-xs); color:var(--color-mousse);"><span class="status-dot status-dot--ok"></span> 3 places cette semaine</span>
          <a href="rendez-vous.html" class="btn btn--ghost btn--sm">Voir →</a>
        </div>
      </article>

    </div>

    <p style="text-align:center; margin-top:var(--space-12); font-family:var(--font-serif); color:var(--color-text-muted);">
      Pas certain·e de qui choisir ? <a href="audio-async.html" style="color:var(--color-rose-deep);">Enregistrez-vous d'abord</a> — un·e praticien·ne vous reviendra avec une suggestion adaptée.
    </p>
  </div>
</section>
'''


# =============================================================
# RENDEZ-VOUS — choix créneau + formulaire
# =============================================================
RDV_BODY = '''
<section class="section">
  <div class="container">
    <span class="eyebrow">Prendre rendez-vous</span>
    <h1 class="section-title" style="font-size: var(--text-2xl);">Trois étapes, à votre rythme.</h1>

    <!-- Stepper -->
    <div style="display:flex; gap:var(--space-4); margin-block: var(--space-10) var(--space-12); flex-wrap:wrap;">
      <div style="flex:1; min-width:200px; border-bottom:2px solid var(--color-aubergine); padding-bottom:var(--space-3);">
        <p style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-rose-deep); font-weight:500;">Étape 1 — En cours</p>
        <p style="font-family:var(--font-display); font-size:var(--text-lg);">Choisir un·e praticien·ne</p>
      </div>
      <div style="flex:1; min-width:200px; border-bottom:2px solid var(--color-divider); padding-bottom:var(--space-3); opacity:0.5;">
        <p style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-text-muted);">Étape 2</p>
        <p style="font-family:var(--font-display); font-size:var(--text-lg);">Choisir un créneau</p>
      </div>
      <div style="flex:1; min-width:200px; border-bottom:2px solid var(--color-divider); padding-bottom:var(--space-3); opacity:0.5;">
        <p style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-text-muted);">Étape 3</p>
        <p style="font-family:var(--font-display); font-size:var(--text-lg);">Confirmer</p>
      </div>
    </div>

    <div class="grid" style="grid-template-columns: 2fr 1fr; gap:var(--space-8);">
      <div>
        <h2 class="section-title" style="font-size: var(--text-xl);">Maïté Lavoie-Therrien</h2>
        <p style="color:var(--color-text-muted); margin-bottom:var(--space-6); font-family:var(--font-serif);">
          Voie : Fréquence & Sommeil · Montréal · à distance · 60 min · 95 $
        </p>

        <h3 style="font-family:var(--font-display); font-size:var(--text-lg); margin-bottom:var(--space-4);">Créneaux disponibles cette semaine</h3>

        <div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: var(--space-3); margin-bottom: var(--space-8);">
          <button class="card" style="padding:var(--space-3) var(--space-4); text-align:center; cursor:pointer;">
            <p style="font-size:var(--text-xs); color:var(--color-text-muted); letter-spacing:0.1em; text-transform:uppercase;">Jeudi 12 mai</p>
            <p style="font-family:var(--font-display); font-size:var(--text-base); margin-top:2px;">10 h 30</p>
          </button>
          <button class="card" style="padding:var(--space-3) var(--space-4); text-align:center; cursor:pointer; border-color: var(--color-aubergine); background: var(--color-surface-warm);">
            <p style="font-size:var(--text-xs); color:var(--color-rose-deep); letter-spacing:0.1em; text-transform:uppercase;">Jeudi 12 mai</p>
            <p style="font-family:var(--font-display); font-size:var(--text-base); margin-top:2px;">14 h 00</p>
          </button>
          <button class="card" style="padding:var(--space-3) var(--space-4); text-align:center; cursor:pointer;">
            <p style="font-size:var(--text-xs); color:var(--color-text-muted); letter-spacing:0.1em; text-transform:uppercase;">Vendredi 13 mai</p>
            <p style="font-family:var(--font-display); font-size:var(--text-base); margin-top:2px;">9 h 00</p>
          </button>
          <button class="card" style="padding:var(--space-3) var(--space-4); text-align:center; cursor:pointer;">
            <p style="font-size:var(--text-xs); color:var(--color-text-muted); letter-spacing:0.1em; text-transform:uppercase;">Vendredi 13 mai</p>
            <p style="font-family:var(--font-display); font-size:var(--text-base); margin-top:2px;">15 h 30</p>
          </button>
          <button class="card" style="padding:var(--space-3) var(--space-4); text-align:center; cursor:pointer;">
            <p style="font-size:var(--text-xs); color:var(--color-text-muted); letter-spacing:0.1em; text-transform:uppercase;">Lundi 16 mai</p>
            <p style="font-family:var(--font-display); font-size:var(--text-base); margin-top:2px;">11 h 00</p>
          </button>
          <button class="card" style="padding:var(--space-3) var(--space-4); text-align:center; cursor:pointer;">
            <p style="font-size:var(--text-xs); color:var(--color-text-muted); letter-spacing:0.1em; text-transform:uppercase;">Mardi 17 mai</p>
            <p style="font-family:var(--font-display); font-size:var(--text-base); margin-top:2px;">17 h 00</p>
          </button>
        </div>

        <details class="card" style="background: var(--color-surface-warm);">
          <summary style="cursor:pointer; font-family:var(--font-display); font-size:var(--text-base);">Préférez préparer la rencontre ? (facultatif)</summary>
          <div class="stack" style="margin-top:var(--space-4);">
            <div class="field">
              <label for="contexte">En quelques lignes : qu'est-ce qui vous amène ?</label>
              <textarea id="contexte" rows="4" placeholder="Vous pouvez aussi laisser vide. La rencontre commencera à votre rythme."></textarea>
            </div>
          </div>
        </details>

        <div class="flex" style="margin-top:var(--space-8); justify-content: flex-end;">
          <a href="praticiens.html" class="btn btn--ghost">← Changer de praticien·ne</a>
          <a href="dashboard.html" class="btn btn--primary">Confirmer le 12 mai à 14 h →</a>
        </div>
      </div>

      <aside class="card card--warm" style="height:fit-content; position:sticky; top:6rem;">
        <p class="card__meta">Récapitulatif</p>
        <h3 class="card__title">Rencontre simple</h3>
        <ul role="list" style="margin-top:var(--space-4); display:flex; flex-direction:column; gap:var(--space-2); font-size:var(--text-sm);">
          <li><strong>Durée</strong> · 60 minutes</li>
          <li><strong>Format</strong> · à distance (vidéo)</li>
          <li><strong>Tarif</strong> · 95 $ CAD</li>
          <li><strong>Annulation</strong> · gratuite jusqu'à 24 h avant</li>
        </ul>
        <hr style="margin:var(--space-4) 0; border:none; border-top:1px solid var(--color-divider);">
        <p style="font-family:var(--font-serif); font-size:var(--text-xs); color:var(--color-text-muted);">
          IVIA n'est pas un service d'urgence et ne pose pas de diagnostic.
        </p>
      </aside>
    </div>
  </div>
</section>
'''

# =============================================================
# AUDIO ASYNC — l'écran clé
# =============================================================
AUDIO_ASYNC_BODY = '''
<section class="section">
  <div class="container container--default">

    <!-- Bandeau Mode pilote -->
    <div class="pilote-banner" style="background: var(--color-mousse); color:var(--color-creme); padding: var(--space-4) var(--space-6); border-radius: var(--radius-md); margin-bottom: var(--space-8); display:flex; flex-wrap:wrap; gap: var(--space-4); align-items:center; justify-content: space-between;">
      <div>
        <strong style="font-family:var(--font-display); font-size:var(--text-base);">Mode pilote — phase 1 sans praticien·ne</strong>
        <p style="font-family:var(--font-serif); font-size:var(--text-sm); opacity:0.92; margin-top:var(--space-1);">Vous enregistrez, notre outil interne propose un résumé directement. Pas d'attente de 48 h.</p>
      </div>
      <button class="btn btn--ghost btn--sm" data-mode-pilote-toggle aria-pressed="true" style="border-color: rgba(255,255,255,0.4); color:var(--color-creme);">Mode pilote actif ✓</button>
    </div>

    <span class="eyebrow">Audio asynchrone</span>
    <h1 class="section-title" style="font-size: var(--text-2xl);">Une autre porte — la vôtre.</h1>
    <p class="section-lede">
      Vous parlez seul·e, à votre rythme, ce qui vous traverse en ce moment. En phase pilote, notre outil interne vous renvoie un résumé en moins d'une minute pour que vous puissiez tester l'expérience de bout en bout.
    </p>

    <!-- Stepper visuel -->
    <ol style="display:grid; grid-template-columns: repeat(4, 1fr); gap:var(--space-4); margin-block: var(--space-12); list-style:none;">
      <li style="text-align:center;">
        <div style="width:48px; height:48px; border-radius:50%; background: var(--color-aubergine); color:var(--color-creme); display:inline-flex; align-items:center; justify-content:center; font-family:var(--font-display); font-size:var(--text-base); margin-bottom:var(--space-3);">1</div>
        <p style="font-family:var(--font-display); font-size:var(--text-base);">Vous enregistrez</p>
        <p style="font-size:var(--text-xs); color:var(--color-text-muted); margin-top:var(--space-1);">3 à 15 min, à votre aise</p>
      </li>
      <li style="text-align:center; opacity:0.5;">
        <div style="width:48px; height:48px; border-radius:50%; background: transparent; border:1.5px solid var(--color-aubergine); color:var(--color-aubergine); display:inline-flex; align-items:center; justify-content:center; font-family:var(--font-display); font-size:var(--text-base); margin-bottom:var(--space-3);">2</div>
        <p style="font-family:var(--font-display); font-size:var(--text-base);">Un·e praticien·ne écoute</p>
        <p style="font-size:var(--text-xs); color:var(--color-text-muted); margin-top:var(--space-1);">Sous 48 h ouvrables</p>
      </li>
      <li style="text-align:center; opacity:0.5;">
        <div style="width:48px; height:48px; border-radius:50%; background: transparent; border:1.5px solid var(--color-aubergine); color:var(--color-aubergine); display:inline-flex; align-items:center; justify-content:center; font-family:var(--font-display); font-size:var(--text-base); margin-bottom:var(--space-3);">3</div>
        <p style="font-family:var(--font-display); font-size:var(--text-base);">Résumé écrit reçu</p>
        <p style="font-size:var(--text-xs); color:var(--color-text-muted); margin-top:var(--space-1);">Court. Honnête. Sans diagnostic.</p>
      </li>
      <li style="text-align:center; opacity:0.5;">
        <div style="width:48px; height:48px; border-radius:50%; background: transparent; border:1.5px solid var(--color-aubergine); color:var(--color-aubergine); display:inline-flex; align-items:center; justify-content:center; font-family:var(--font-display); font-size:var(--text-base); margin-bottom:var(--space-3);">4</div>
        <p style="font-family:var(--font-display); font-size:var(--text-base);">Bref appel — ou non.</p>
        <p style="font-size:var(--text-xs); color:var(--color-text-muted); margin-top:var(--space-1);">15 min offertes. Vous décidez après.</p>
      </li>
    </ol>

    <!-- Module enregistrement -->
    <div class="card" style="padding: var(--space-12) var(--space-8); background: var(--color-surface-2); text-align:center;">

      <p class="card__meta">Étape 1 sur 4</p>
      <h2 style="font-family:var(--font-display); font-size:var(--text-xl); margin-bottom:var(--space-3);">Quand vous êtes prêt·e, parlez.</h2>
      <p style="font-family:var(--font-serif); color:var(--color-text-muted); max-width:46ch; margin-inline:auto; margin-bottom:var(--space-8);">
        Pas de plan à suivre. Dites ce qui vient. Vous pouvez mettre pause, recommencer, supprimer. Rien n'est envoyé tant que vous ne le demandez pas.
      </p>

      <!-- Onde simulée -->
      <div data-record-wave style="height:80px; display:flex; align-items:center; justify-content:center; gap:3px; margin-bottom:var(--space-8);">
        <span style="width:3px; height:20px; background: var(--color-rose); border-radius:2px;"></span>
        <span style="width:3px; height:40px; background: var(--color-rose); border-radius:2px;"></span>
        <span style="width:3px; height:30px; background: var(--color-rose); border-radius:2px;"></span>
        <span style="width:3px; height:55px; background: var(--color-rose); border-radius:2px;"></span>
        <span style="width:3px; height:25px; background: var(--color-rose); border-radius:2px;"></span>
        <span style="width:3px; height:45px; background: var(--color-rose); border-radius:2px;"></span>
        <span style="width:3px; height:35px; background: var(--color-rose); border-radius:2px;"></span>
        <span style="width:3px; height:50px; background: var(--color-rose); border-radius:2px;"></span>
        <span style="width:3px; height:22px; background: var(--color-rose); border-radius:2px;"></span>
        <span style="width:3px; height:38px; background: var(--color-rose); border-radius:2px;"></span>
        <span style="width:3px; height:28px; background: var(--color-rose); border-radius:2px;"></span>
      </div>

      <p data-record-time style="font-family:var(--font-display); font-size:var(--text-2xl); color:var(--color-text-muted); margin-bottom:var(--space-6); font-variant-numeric: tabular-nums;">00:00</p>

      <div data-recorder-controls style="display:flex; gap:var(--space-3); justify-content:center; flex-wrap:wrap;">
        <button class="btn btn--primary btn--lg" data-record-start style="border-radius: var(--radius-full); padding: var(--space-4) var(--space-8);">
          <span style="display:inline-block; width:14px; height:14px; border-radius:50%; background: var(--color-rose); margin-right: var(--space-2);"></span>
          <span class="label">Démarrer l'enregistrement</span>
        </button>
        <button class="btn btn--ghost btn--lg" data-record-stop hidden style="border-radius: var(--radius-full); padding: var(--space-4) var(--space-8);">
          <span style="display:inline-block; width:14px; height:14px; background: var(--color-aubergine); margin-right: var(--space-2); border-radius:2px;"></span>
          <span class="label">Arrêter</span>
        </button>
        <button class="btn btn--ghost btn--lg" data-record-skip style="border-radius: var(--radius-full); padding: var(--space-4) var(--space-8); opacity:0.7;">
          <span class="label">Sauter (mode démo)</span>
        </button>
      </div>

      <!-- Lecture du test -->
      <div data-record-playback hidden style="margin-top: var(--space-8);">
        <p style="font-family:var(--font-display); font-size:var(--text-base); margin-bottom:var(--space-3);">Votre enregistrement</p>
        <audio controls data-record-audio style="width:100%; max-width: 500px; margin-inline:auto;"></audio>
        <div style="display:flex; gap:var(--space-3); justify-content:center; flex-wrap:wrap; margin-top:var(--space-6);">
          <button class="btn btn--ghost" data-record-redo>Recommencer</button>
          <button class="btn btn--primary" data-record-send>Envoyer pour analyse →</button>
        </div>
      </div>

      <!-- Phase d'analyse simulée -->
      <div data-record-analyze hidden style="margin-top: var(--space-8);">
        <div class="analyze-shimmer" style="display:flex; flex-direction:column; gap:var(--space-3); align-items:center;">
          <p style="font-family:var(--font-display); font-size:var(--text-lg);">Notre outil écoute votre audio…</p>
          <div style="width:300px; height:6px; background: var(--color-divider); border-radius:3px; overflow:hidden;">
            <div data-analyze-bar style="height:100%; background: linear-gradient(90deg, var(--color-rose), var(--color-miel)); width:0%; transition: width 0.3s ease;"></div>
          </div>
          <p data-analyze-step style="font-family:var(--font-serif); color: var(--color-text-muted); font-size:var(--text-sm);">Préparation…</p>
        </div>
      </div>

      <p style="margin-top:var(--space-8); font-size:var(--text-xs); color:var(--color-text-faint); letter-spacing: 0.04em;">
        L'enregistrement reste local dans votre navigateur jusqu'à ce que vous l'envoyiez. <a href="../confidentialite.html" style="text-decoration:underline;">Comment vos données sont protégées</a>.
      </p>
    </div>

    <script>
    (function(){
      const startBtn = document.querySelector('[data-record-start]');
      const stopBtn  = document.querySelector('[data-record-stop]');
      const skipBtn  = document.querySelector('[data-record-skip]');
      const wave     = document.querySelector('[data-record-wave]');
      const timeEl   = document.querySelector('[data-record-time]');
      const playback = document.querySelector('[data-record-playback]');
      const audioEl  = document.querySelector('[data-record-audio]');
      const redoBtn  = document.querySelector('[data-record-redo]');
      const sendBtn  = document.querySelector('[data-record-send]');
      const analyze  = document.querySelector('[data-record-analyze]');
      const bar      = document.querySelector('[data-analyze-bar]');
      const stepEl   = document.querySelector('[data-analyze-step]');
      const controls = document.querySelector('[data-recorder-controls]');
      let mediaRecorder, chunks = [], stream, startTime, timerId, audioBlob;

      function fmt(s){ const m=Math.floor(s/60), ss=Math.floor(s%60); return String(m).padStart(2,'0')+':'+String(ss).padStart(2,'0'); }

      function tickTimer(){
        if (!startTime) return;
        const elapsed = (Date.now()-startTime)/1000;
        timeEl.textContent = fmt(elapsed);
      }

      async function startRecording(){
        try {
          stream = await navigator.mediaDevices.getUserMedia({audio:true});
          mediaRecorder = new MediaRecorder(stream);
          chunks = [];
          mediaRecorder.ondataavailable = e => { if (e.data.size>0) chunks.push(e.data); };
          mediaRecorder.onstop = () => {
            audioBlob = new Blob(chunks, { type: chunks[0]?.type || 'audio/webm' });
            audioEl.src = URL.createObjectURL(audioBlob);
            playback.hidden = false;
            stream.getTracks().forEach(t => t.stop());
          };
          mediaRecorder.start();
          startTime = Date.now();
          timerId = setInterval(tickTimer, 200);
          wave.classList.add('is-recording');
          startBtn.hidden = true;
          stopBtn.hidden = false;
          skipBtn.hidden = true;
        } catch(err){
          alert("Le micro n'est pas accessible. Vous pouvez utiliser le bouton « Sauter (mode démo) » pour tester la suite du parcours.");
        }
      }

      function stopRecording(){
        if (mediaRecorder && mediaRecorder.state !== 'inactive') mediaRecorder.stop();
        clearInterval(timerId);
        wave.classList.remove('is-recording');
        controls.hidden = true;
      }

      function skipRecording(){
        // Mode démo : faux enregistrement de 4 minutes
        timeEl.textContent = '04:00';
        playback.hidden = false;
        controls.hidden = true;
        // Pas d'audio réel à lire
        audioEl.style.display = 'none';
      }

      function redo(){
        playback.hidden = true;
        controls.hidden = false;
        startBtn.hidden = false;
        stopBtn.hidden = true;
        skipBtn.hidden = false;
        timeEl.textContent = '00:00';
        audioEl.style.display = '';
      }

      function send(){
        playback.hidden = true;
        analyze.hidden = false;
        const steps = [
          {pct: 18, txt: 'Transcription en cours…'},
          {pct: 38, txt: 'Lecture des cinq zones du cercle…'},
          {pct: 58, txt: 'Identification des thèmes principaux…'},
          {pct: 78, txt: 'Préparation des trois pistes concrètes…'},
          {pct: 95, txt: 'Mise en forme du résumé…'},
          {pct: 100, txt: 'Prêt.'}
        ];
        let i = 0;
        const next = () => {
          if (i >= steps.length) {
            window.location = 'audio-resume.html?source=pilote';
            return;
          }
          bar.style.width = steps[i].pct + '%';
          stepEl.textContent = steps[i].txt;
          i++;
          setTimeout(next, 750);
        };
        next();
      }

      startBtn?.addEventListener('click', startRecording);
      stopBtn?.addEventListener('click', stopRecording);
      skipBtn?.addEventListener('click', skipRecording);
      redoBtn?.addEventListener('click', redo);
      sendBtn?.addEventListener('click', send);
    })();
    </script>

    <style>
      [data-record-wave].is-recording span {
        animation: wave-anim 1.2s ease-in-out infinite alternate;
      }
      [data-record-wave].is-recording span:nth-child(2)  { animation-delay: 0.1s; }
      [data-record-wave].is-recording span:nth-child(3)  { animation-delay: 0.15s; }
      [data-record-wave].is-recording span:nth-child(4)  { animation-delay: 0.2s; }
      [data-record-wave].is-recording span:nth-child(5)  { animation-delay: 0.25s; }
      [data-record-wave].is-recording span:nth-child(6)  { animation-delay: 0.3s; }
      [data-record-wave].is-recording span:nth-child(7)  { animation-delay: 0.35s; }
      [data-record-wave].is-recording span:nth-child(8)  { animation-delay: 0.4s; }
      [data-record-wave].is-recording span:nth-child(9)  { animation-delay: 0.45s; }
      [data-record-wave].is-recording span:nth-child(10) { animation-delay: 0.5s; }
      [data-record-wave].is-recording span:nth-child(11) { animation-delay: 0.55s; }
      @keyframes wave-anim { from { transform: scaleY(0.4); } to { transform: scaleY(1.2); } }
    </style>

    <!-- Cadre éthique -->
    <div class="cadre-ethique" style="margin-top: var(--space-12);">
      <svg class="cadre-ethique__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
        <circle cx="12" cy="12" r="10"/><path d="M12 8 L 12 13 M 12 16 L 12 16.01"/>
      </svg>
      <p>
        L'audio asynchrone n'est pas adapté aux situations urgentes. Si vous traversez une crise immédiate, contactez le <strong>811 option 2</strong> (Info-Social, Québec) ou le <strong>911</strong>. Pour une réponse plus rapide, optez pour un <a href="rendez-vous.html">rendez-vous direct</a>.
      </p>
    </div>
  </div>
</section>
'''


# =============================================================
# AUDIO ASYNC — État "en attente" (résumé reçu plus tard)
# =============================================================
AUDIO_ATTENTE_BODY = '''
<section class="section">
  <div class="container container--default">
    <p class="card__meta">Étape 2 sur 4</p>
    <h1 class="section-title" style="font-size: var(--text-xl); margin-bottom:var(--space-4);">Votre enregistrement est en route.</h1>
    <p class="section-lede" style="margin-bottom:var(--space-12);">
      Maïté Lavoie-Therrien a été notifiée. Elle reviendra vers vous dans les <strong>48 h ouvrables</strong>
      avec un résumé écrit de ce qui a été entendu et une proposition de bref appel.
    </p>

    <div class="card" style="padding: var(--space-8);">
      <div class="flex-between" style="margin-bottom: var(--space-6);">
        <div>
          <p style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-rose-deep);">Audio envoyé · 09 mai · 14 h 22</p>
          <h2 style="font-family:var(--font-display); font-size:var(--text-lg); margin-top:var(--space-2);">5 min 41 s · « Sans titre »</h2>
        </div>
        <span class="chip chip--miel"><span class="status-dot status-dot--pending"></span> En écoute</span>
      </div>

      <button class="btn btn--ghost btn--sm" data-audio-fake aria-pressed="false">▶︎ Écouter mon audio</button>

      <hr style="margin:var(--space-6) 0; border:none; border-top:1px solid var(--color-divider);">

      <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm);">
        <strong style="color:var(--color-text);">Ce qui se passe maintenant :</strong> votre praticien·ne va prendre le temps d'écouter votre enregistrement et d'écrire une réponse — pas un résumé automatique, mais une lecture humaine. Cela demande un peu de temps. Vous serez notifié·e par courriel dès que la réponse est prête.
      </p>
    </div>

    <!-- Rappel 10 min — déjà planifié -->
    <div class="card" style="padding: var(--space-8); margin-top: var(--space-6); background: var(--color-surface-warm); border-left: 3px solid var(--color-rose-deep);">
      <p style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-rose-deep); margin-bottom:var(--space-3);">Rappel personnalisé · inclus dans le forfait</p>
      <h3 style="font-family:var(--font-display); font-size:var(--text-lg); margin-bottom:var(--space-3);">Un rappel de 10 minutes vous attend après la lecture du résumé.</h3>
      <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-bottom:var(--space-4);">
        Selon les disponibilités que vous avez indiquées au formulaire, Maïté vous proposera trois créneaux dès que son résumé écrit sera prêt. Vous choisirez celui qui vous convient — ou vous reporterez. Aucun frais supplémentaire.
      </p>
      <div style="display:flex; gap:var(--space-6); flex-wrap:wrap; font-size:var(--text-xs); color:var(--color-text-muted);">
        <span><strong style="color:var(--color-text);">Disponibilités saisies :</strong> en soirée, semaine</span>
        <span><strong style="color:var(--color-text);">Format :</strong> téléphone</span>
        <span><strong style="color:var(--color-text);">Durée :</strong> 10 min</span>
      </div>
    </div>

    <div class="cadre-ethique" style="margin-top: var(--space-8);">
      <svg class="cadre-ethique__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
        <circle cx="12" cy="12" r="10"/><path d="M12 8 L 12 13 M 12 16 L 12 16.01"/>
      </svg>
      <p>
        Si votre situation se dégrade pendant l'attente, n'hésitez pas à <a href="rendez-vous.html">prendre un rendez-vous direct</a> ou à contacter le <strong>811 option 2</strong>. L'audio asynchrone est un confort, pas un substitut à une rencontre quand elle est nécessaire.
      </p>
    </div>
  </div>
</section>
'''


# =============================================================
# AUDIO ASYNC — Résumé reçu (étape 3 / 4)
# =============================================================
AUDIO_RESUME_BODY = '''
<div id="pilote-banner" style="display:none; background:var(--color-mousse); color:#fff; padding:var(--space-4) var(--space-6); text-align:center; font-size:var(--text-sm);">
  Mode pilote — ce résumé est généré à des fins de démonstration. En conditions réelles, il serait rédigé par votre praticien·ne dans un délai de 24 à 72 heures.
</div>
<script>
  (function(){
    try { if (new URLSearchParams(window.location.search).get('source') === 'pilote') { document.getElementById('pilote-banner').style.display = 'block'; } } catch(e) {}
  })();
</script>
<section class="section">
  <div class="container container--default">
    <p class="card__meta">Étape 3 sur 4 — Résumé reçu</p>
    <h1 class="section-title" style="font-size: var(--text-xl); margin-bottom:var(--space-4);">Maïté vous a écrit.</h1>
    <p class="section-lede" style="margin-bottom:var(--space-10);">
      Reçu le 11 mai à 10 h 47. Prenez le temps de lire — il n'y a aucune urgence à répondre.
    </p>

    <article class="card" style="padding: var(--space-10) var(--space-8); background: var(--color-surface-warm);">
      <header style="display:flex; gap:var(--space-4); align-items:center; margin-bottom:var(--space-6);">
        <div style="width:56px; height:56px; border-radius:50%; background:linear-gradient(135deg, #C58A8A, #D89260);"></div>
        <div>
          <p style="font-family:var(--font-display); font-size:var(--text-base); font-weight:500;">Maïté Lavoie-Therrien</p>
          <p style="font-size:var(--text-xs); color:var(--color-text-muted); letter-spacing:0.04em;">Praticienne · Voie Fréquence & Sommeil</p>
        </div>
      </header>

      <div style="font-family:var(--font-serif); font-size:var(--text-base); line-height:1.7; color:var(--color-text); max-width:none;">
        <p style="margin-bottom:1em;">Bonjour,</p>
        <p style="margin-bottom:1em;">
          Merci pour votre enregistrement. J'ai pris le temps de l'écouter deux fois — le matin, puis hier soir. Je vais vous restituer simplement ce que j'ai entendu, sans interpréter plus que nécessaire.
        </p>
        <p style="margin-bottom:1em;">
          Vous décrivez une période où le sommeil ne vous repose plus, et où les journées vous semblent passer « comme dans un brouillard ». Vous nommez clairement la fatigue, mais vous hésitez à mettre un mot sur ce qui se passe en dessous. Ce qui m'a touchée, c'est ce moment vers la fin où vous dites : « je ne suis pas en détresse, mais quelque chose ne va plus comme avant ». C'est une phrase juste — et c'est souvent le bon point de départ.
        </p>
        <p style="margin-bottom:1em;">
          Je vous propose qu'on prenne <strong>15 minutes au téléphone cette semaine</strong>, pour préciser un peu, et voir ensemble si une rencontre plus posée vous serait utile. Pas de pression : si vous préférez attendre, ou ne pas donner suite, c'est entièrement votre choix.
        </p>
        <p style="margin-bottom:1em;">
          Voici trois créneaux possibles pour l'appel court (gratuit) :
        </p>
        <ul style="padding-left: 1.5em; margin-bottom:1em;">
          <li>Mardi 13 mai · 11 h 30</li>
          <li>Mercredi 14 mai · 16 h 00</li>
          <li>Jeudi 15 mai · 9 h 30</li>
        </ul>
        <p style="margin-bottom:1em;">Bien à vous,</p>
        <p style="font-style:italic; color:var(--color-rose-deep);">Maïté</p>
      </div>
    </article>

    <!-- Bloc rappel 10 min planifié -->
    <div class="card" style="padding: var(--space-10) var(--space-8); margin-top: var(--space-8); background: var(--color-surface-warm); border-left: 3px solid var(--color-rose-deep);">
      <p style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-rose-deep); margin-bottom:var(--space-3);">Rappel 10 min · planifié · inclus dans votre forfait</p>
      <h2 style="font-family:var(--font-display); font-size:var(--text-xl); margin-bottom:var(--space-4);">Maïté vous appelle mardi 13 mai à 11 h 30.</h2>
      <p style="font-family:var(--font-serif); color:var(--color-text-muted); margin-bottom:var(--space-6); max-width:60ch;">
        Ce rappel personnalisé de 10 minutes est déjà au calendrier. Il sert à vérifier ensemble si quelque chose s'est précisé à la lecture du résumé, et à décider — sans engagement — s'il y a lieu d'aller plus loin par un rendez-vous d'approfondissement.
      </p>
      <div style="display:flex; gap:var(--space-3); flex-wrap:wrap;">
        <button class="btn btn--ghost btn--sm" type="button">Décaler le créneau</button>
        <button class="btn btn--ghost btn--sm" type="button">Préférer un autre praticien·ne</button>
        <button class="btn btn--ghost btn--sm" type="button">Annuler le rappel</button>
      </div>
    </div>

    <!-- Décision après le rappel : RDV d'approfondissement ou non -->
    <div style="margin-top: var(--space-12); padding-top: var(--space-8); border-top:1px solid var(--color-divider);">
      <p class="eyebrow">Et après le rappel ?</p>
      <h2 class="section-title" style="font-size: var(--text-lg); margin-bottom:var(--space-4);">Vous déciderez à ce moment-là — pas avant.</h2>
      <p class="section-lede" style="margin-bottom:var(--space-8);">
        À l'issue du rappel, deux portes s'ouvrent. Aucune n'est obligatoire. La troisième — ne rien faire — est tout à fait recevable.
      </p>

      <div class="grid grid-2">
        <div class="card card--clickable" data-href="rendez-vous.html" style="cursor:pointer;">
          <p class="card__meta">Si un approfondissement vous parle</p>
          <h3 class="card__title">Prendre un rendez-vous d'approfondissement</h3>
          <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm);">Une rencontre plus posée — visio ou présentiel — pour continuer le travail amorcé. Tarif fixé par votre praticien·ne, indiqué avant la réservation.</p>
          <p style="margin-top:var(--space-4);"><span class="btn btn--primary btn--sm">Voir les créneaux →</span></p>
        </div>
        <div class="card card--clickable" data-href="dashboard.html" style="cursor:pointer;">
          <p class="card__meta">Si vous voulez laisser reposer</p>
          <h3 class="card__title">Garder le résumé, ne rien décider</h3>
          <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm);">Le résumé reste dans votre espace, accessible 30 jours. Vous pouvez revenir plus tard, ou pas. Aucune relance commerciale.</p>
          <p style="margin-top:var(--space-4);"><span class="btn btn--ghost btn--sm">Retour à mon espace →</span></p>
        </div>
      </div>
    </div>

    <p style="text-align:center; margin-top: var(--space-10); font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm);">
      Vous préférez ne rien faire pour l'instant ? <a href="dashboard.html" style="color:var(--color-rose-deep);">C'est OK aussi.</a> Le résumé reste dans votre espace.
    </p>

    <script>
      document.querySelectorAll('[data-href]').forEach(function(el){
        el.addEventListener('click', function(e){
          if (e.target.closest('a') || e.target.closest('button')) return;
          window.location.href = el.dataset.href;
        });
      });
    </script>
  </div>
</section>
'''


# =============================================================
# DASHBOARD CLIENT — espace personnel
# =============================================================
DASHBOARD_BODY = '''
<section class="section--tight">
  <div class="container">
    <span class="eyebrow">Mon espace</span>
    <h1 class="section-title" style="font-size: var(--text-2xl);">Bonjour, Camille.</h1>
    <p class="section-lede">Tout ce qui vous concerne, à un seul endroit. Sans alerte, sans pression.</p>

    <!-- Status cards -->
    <div class="grid grid-3" style="margin-bottom: var(--space-12);">
      <article class="card card--warm">
        <p class="card__meta">Prochain rendez-vous</p>
        <h2 class="card__title" style="font-size: var(--text-lg);">Jeudi 12 mai · 14 h</h2>
        <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-top:var(--space-2);">Avec Maïté Lavoie-Therrien · à distance</p>
        <div class="flex" style="margin-top:var(--space-4);">
          <button class="btn btn--ghost btn--sm">Détails</button>
          <button class="btn btn--ghost btn--sm">Annuler</button>
        </div>
      </article>

      <article class="card">
        <p class="card__meta">Audio en écoute</p>
        <h2 class="card__title" style="font-size: var(--text-lg);">Réponse attendue sous 48 h</h2>
        <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-top:var(--space-2);">Envoyé hier à Maïté · 5 min 41 s</p>
        <a href="audio-attente.html" class="btn btn--ghost btn--sm" style="margin-top:var(--space-4);">Voir l'enregistrement →</a>
      </article>

      <article class="card">
        <p class="card__meta">Journal</p>
        <h2 class="card__title" style="font-size: var(--text-lg);">3 entrées ce mois-ci</h2>
        <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-top:var(--space-2);">Dernière : « Une bonne journée », 7 mai.</p>
        <a href="journal.html" class="btn btn--ghost btn--sm" style="margin-top:var(--space-4);">Ouvrir le journal →</a>
      </article>
    </div>

    <!-- 2 colonnes : historique + outils -->
    <div class="grid" style="grid-template-columns: 2fr 1fr; gap:var(--space-8);">
      <div>
        <h2 class="section-title" style="font-size: var(--text-xl);">Mes rencontres</h2>

        <div class="stack stack-lg">
          <article class="card">
            <div class="flex-between">
              <div>
                <p style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-rose-deep);">À venir · Jeu 12 mai · 14 h</p>
                <h3 class="card__title" style="font-size:var(--text-lg); margin-top:var(--space-1);">Rencontre simple · 60 min</h3>
                <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-top:var(--space-2);">Avec Maïté Lavoie-Therrien · à distance</p>
              </div>
              <span class="chip chip--mousse"><span class="status-dot status-dot--ok"></span> Confirmé</span>
            </div>
          </article>
          <article class="card">
            <div class="flex-between">
              <div>
                <p style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-text-muted);">Passée · 28 avr · 10 h</p>
                <h3 class="card__title" style="font-size:var(--text-lg); margin-top:var(--space-1);">Première rencontre · 60 min</h3>
                <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-top:var(--space-2);">Avec Maïté · résumé partagé disponible</p>
              </div>
              <button class="btn btn--ghost btn--sm">Lire le résumé</button>
            </div>
          </article>
          <article class="card" style="opacity:0.85;">
            <div class="flex-between">
              <div>
                <p style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-text-muted);">Audio · 9 mai</p>
                <h3 class="card__title" style="font-size:var(--text-lg); margin-top:var(--space-1);">Enregistrement asynchrone</h3>
                <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-top:var(--space-2);">5 min 41 s · réponse en cours</p>
              </div>
              <span class="chip chip--miel"><span class="status-dot status-dot--pending"></span> En attente</span>
            </div>
          </article>
        </div>

        <h2 class="section-title" style="font-size: var(--text-xl); margin-top: var(--space-12);">Notes & repères</h2>

        <article class="card card--warm">
          <p class="card__meta">Résumé · Première rencontre du 28 avr</p>
          <p style="font-family:var(--font-serif); line-height:1.7;">
            « Vous arrivez avec une fatigue qui vous surprend. Vous nommez la difficulté à dormir, mais vous savez aussi que ce n'est peut-être pas que ça. Nous avons commencé par poser ce qui pèse, sans chercher à le nommer trop vite. Pour la prochaine, je vous propose de noter, sans vous y obliger, deux ou trois moments dans la semaine où vous vous êtes senti·e plus calme — ou plus tendu·e. Ça nous donnera des repères concrets. »
          </p>
          <p style="margin-top:var(--space-4); font-style:italic; color:var(--color-rose-deep); font-family:var(--font-display);">— Maïté</p>
        </article>
      </div>

      <aside>
        <h2 style="font-family:var(--font-display); font-size:var(--text-lg); margin-bottom:var(--space-4);">Outils à votre rythme</h2>
        <div class="stack">
          <a href="outil-ou-en-etes-vous.html" class="card card--clickable" style="text-decoration:none; padding:var(--space-4);">
            <h3 style="font-size:var(--text-base);">Où en êtes-vous ?</h3>
            <p style="font-size:var(--text-xs); color:var(--color-text-muted); margin-top:var(--space-1);">Fait il y a 3 jours · ▷ refaire</p>
          </a>
          <a href="outil-sommeil.html" class="card card--clickable" style="text-decoration:none; padding:var(--space-4);">
            <h3 style="font-size:var(--text-base);">Sommeil et apaisement</h3>
            <p style="font-size:var(--text-xs); color:var(--color-text-muted); margin-top:var(--space-1);">Pas commencé</p>
          </a>
          <a href="outil-preparer.html" class="card card--clickable" style="text-decoration:none; padding:var(--space-4);">
            <h3 style="font-size:var(--text-base);">Préparer la rencontre du 12 mai</h3>
            <p style="font-size:var(--text-xs); color:var(--color-rose-deep); margin-top:var(--space-1);">Suggéré pour vous</p>
          </a>
        </div>

        <h2 style="font-family:var(--font-display); font-size:var(--text-lg); margin-top:var(--space-8); margin-bottom:var(--space-4);">À lire</h2>
        <div class="stack">
          <a href="bibliotheque.html#article-1_1" class="card card--clickable" style="text-decoration:none; padding:var(--space-4);">
            <p class="card__meta">Lecture · 4 min</p>
            <h3 style="font-size:var(--text-sm);">Pourquoi être entendu change quelque chose</h3>
          </a>
          <a href="bibliotheque.html#article-2_2" class="card card--clickable" style="text-decoration:none; padding:var(--space-4);">
            <p class="card__meta">Lecture · 6 min</p>
            <h3 style="font-size:var(--text-sm);">Sommeil — ce qui aide vraiment</h3>
          </a>
        </div>
      </aside>
    </div>
  </div>
</section>
'''


def build_compte():
    body = '''
<section class="section">
  <div class="container container--default">
    <span class="eyebrow">Compte</span>
    <h1 class="section-title" style="font-size: var(--text-2xl);">Vos accès, vos préférences, votre rythme.</h1>
    <p class="section-lede">Ici, vous voyez ce qui est lié à votre espace. Vous gardez la main sur votre mot de passe, vos préférences et vos façons d'entrer.</p>

    <div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: var(--space-5);">
      <article class="card">
        <p class="card__meta">Profil</p>
        <h2 class="card__title">Camille T.</h2>
        <p style="font-family:var(--font-serif); color:var(--color-text-muted); margin-top:var(--space-3);">Courriel de connexion : vous@exemple.ca</p>
        <p style="font-family:var(--font-serif); color:var(--color-text-muted); margin-top:var(--space-2);">Langue : français québécois</p>
      </article>
      <article class="card">
        <p class="card__meta">Sécurité</p>
        <h2 class="card__title">Changer votre mot de passe</h2>
        <p style="font-family:var(--font-serif); color:var(--color-text-muted); margin-top:var(--space-3);">Gardez un accès simple et stable à votre compte.</p>
        <a href="mot-de-passe-oublie.html" class="btn btn--ghost btn--sm" style="margin-top:var(--space-4);">Réinitialiser le mot de passe</a>
      </article>
      <article class="card">
        <p class="card__meta">Préférences</p>
        <h2 class="card__title">Entrées et rappels</h2>
        <p style="font-family:var(--font-serif); color:var(--color-text-muted); margin-top:var(--space-3);">Recevoir un lien de connexion par courriel, garder l'historique de vos écoutes, ou repartir de zéro au besoin.</p>
      </article>
      <article class="card">
        <p class="card__meta">Accès rapide</p>
        <h2 class="card__title">Reprendre là où vous étiez</h2>
        <p style="font-family:var(--font-serif); color:var(--color-text-muted); margin-top:var(--space-3);">Retour au tableau de bord, au journal ou à une nouvelle écoute.</p>
        <div class="cluster" style="margin-top:var(--space-4);">
          <a class="btn btn--ghost btn--sm" href="dashboard.html">Mon espace</a>
          <a class="btn btn--ghost btn--sm" href="journal.html">Journal</a>
        </div>
      </article>
    </div>
  </div>
</section>
'''
    html = page(
        "Mon compte — IVIA",
        "Préférences de compte et accès à votre espace IVIA.",
        CLIENT_NAV,
        "compte.html",
        CLIENT_ACTIONS,
        body,
        "index.html",
        FOOTER_CLIENT,
    )
    (OUT / "compte.html").write_text(html, encoding="utf-8")


def build_mot_de_passe_oublie():
    body = '''
<section class="section">
  <div class="container container--narrow">
    <span class="eyebrow">Accès</span>
    <h1 class="section-title" style="font-size: var(--text-2xl);">Recevoir un lien pour revenir.</h1>
    <p class="section-lede">Entrez votre courriel, on vous envoie un lien de connexion tout simple. Pas de détour, pas de formulaire de trop.</p>

    <div class="card">
      <div class="stack">
        <div class="field">
          <label for="reset-email">Courriel</label>
          <input id="reset-email" type="email" placeholder="vous@exemple.ca">
        </div>
        <a href="compte.html" class="btn btn--primary">Envoyer le lien</a>
        <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm);">Si vous avez déjà un mot de passe, vous pouvez aussi retourner à la <a href="connexion.html">page de connexion</a>.</p>
      </div>
    </div>
  </div>
</section>
'''
    html = page(
        "Mot de passe oublié — IVIA",
        "Recevez un lien de connexion par courriel pour reprendre votre espace IVIA.",
        CLIENT_NAV,
        "mot-de-passe-oublie.html",
        CLIENT_ACTIONS,
        body,
        "index.html",
        FOOTER_CLIENT,
    )
    (OUT / "mot-de-passe-oublie.html").write_text(html, encoding="utf-8")


# =============================================================
# JOURNAL DE VIE — blog perso, sans téléchargements
# =============================================================
JOURNAL_BODY = '''
<section class="section">
  <div class="container container--default">
    <span class="eyebrow">Journal de vie</span>
    <h1 class="section-title" style="font-size: var(--text-2xl);">Ce que je veux garder, sans le perdre.</h1>
    <p class="section-lede">
      Un espace simple, fixe, à vous. Comme un blog tenu en privé. Pas d'export, pas de partage — sauf si vous le demandez.
      Ce que vous écrivez ici reste ici.
    </p>

    <div class="flex-between" style="margin-bottom: var(--space-8);">
      <div class="cluster">
        <span class="chip chip--rose">Tout</span>
        <span class="chip">Notes</span>
        <span class="chip">Rêves</span>
        <span class="chip">Repères</span>
      </div>
      <button class="btn btn--primary btn--sm">＋ Nouvelle entrée</button>
    </div>

    <div class="stack stack-lg">

      <article class="card">
        <header class="flex-between" style="margin-bottom:var(--space-4);">
          <p style="font-family:var(--font-display); font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-rose-deep);">Vendredi 7 mai · 21 h 14</p>
          <span class="chip">Note</span>
        </header>
        <h2 style="font-family:var(--font-display); font-size:var(--text-lg); margin-bottom:var(--space-3);">Une bonne journée</h2>
        <p style="font-family:var(--font-serif); line-height:1.7;">
          Je sais pas exactement pourquoi, mais aujourd'hui c'était plus léger. Peut-être la marche en début d'après-midi. Peut-être juste qu'il a fait soleil. Je veux noter ça parce que la dernière fois que je me suis senti comme ça remonte à février, et j'avais oublié comment ça faisait.
        </p>
      </article>

      <article class="card">
        <header class="flex-between" style="margin-bottom:var(--space-4);">
          <p style="font-family:var(--font-display); font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-rose-deep);">Mardi 4 mai · 06 h 41</p>
          <span class="chip chip--lavande">Rêve</span>
        </header>
        <h2 style="font-family:var(--font-display); font-size:var(--text-lg); margin-bottom:var(--space-3);">L'eau qui montait sans bruit</h2>
        <p style="font-family:var(--font-serif); line-height:1.7;">
          Une cuisine, peut-être celle de mes parents, mais pas tout à fait. L'eau montait par le plancher, sans bruit. Je n'avais pas peur. Je rangeais des choses, calmement, sur une étagère plus haute. À la fin, l'eau était à mi-mollet et je trouvais ça beau.
        </p>
      </article>

      <article class="card">
        <header class="flex-between" style="margin-bottom:var(--space-4);">
          <p style="font-family:var(--font-display); font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-rose-deep);">Dimanche 2 mai · 23 h 02</p>
          <span class="chip chip--mousse">Repère</span>
        </header>
        <h2 style="font-family:var(--font-display); font-size:var(--text-lg); margin-bottom:var(--space-3);">Ce qui me coûte le moins</h2>
        <p style="font-family:var(--font-serif); line-height:1.7;">
          Quand j'ai pas l'énergie : faire la vaisselle, en silence, fenêtre ouverte. Faire 3 minutes d'étirements en sortant du lit. Préparer un thé au lieu d'un café. C'est rien, mais c'est ce qui passe quand le reste passe pas.
        </p>
      </article>

    </div>

    <p style="text-align:center; margin-top:var(--space-12); font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm);">
      Vos entrées ne sont jamais lues par les praticien·ne·s, sauf si vous décidez de partager une entrée précise lors d'une rencontre.
    </p>
  </div>
</section>
'''


# =============================================================
# RESSOURCES — index articles + 4 outils
# =============================================================
RESSOURCES_BODY = '''
<section class="section">
  <div class="container">
    <span class="eyebrow">Ressources</span>
    <h1 class="section-title" style="font-size: var(--text-2xl);">Lire, faire, comprendre — sans rendez-vous.</h1>
    <p class="section-lede">Articles écrits par les praticien·ne·s d'IVIA et petits outils à votre rythme. Tout est gratuit, sans inscription.</p>

    <h2 class="section-title" style="font-size: var(--text-xl); margin-top: var(--space-12);">Quatre outils</h2>
    <div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: var(--space-4);">
      <a href="outil-ou-en-etes-vous.html" class="card card--clickable" style="text-decoration:none;">
        <h3 style="font-size:var(--text-base);">Où en êtes-vous ?</h3>
        <p style="font-size:var(--text-xs); color:var(--color-text-muted); margin-top:var(--space-2);">10 questions · 4 min</p>
      </a>
      <a href="outil-sommeil.html" class="card card--clickable" style="text-decoration:none;">
        <h3 style="font-size:var(--text-base);">Sommeil et apaisement</h3>
        <p style="font-size:var(--text-xs); color:var(--color-text-muted); margin-top:var(--space-2);">Auto-évaluation · 6 min</p>
      </a>
      <a href="outil-frequence.html" class="card card--clickable" style="text-decoration:none;">
        <h3 style="font-size:var(--text-base);">Fréquence et environnement</h3>
        <p style="font-size:var(--text-xs); color:var(--color-text-muted); margin-top:var(--space-2);">Cartographie · 5 min</p>
      </a>
      <a href="outil-preparer.html" class="card card--clickable" style="text-decoration:none;">
        <h3 style="font-size:var(--text-base);">Préparer une rencontre</h3>
        <p style="font-size:var(--text-xs); color:var(--color-text-muted); margin-top:var(--space-2);">Trame guidée · 8 min</p>
      </a>
    </div>

    <h2 class="section-title" style="font-size: var(--text-xl); margin-top: var(--space-16);">Articles</h2>
    <div class="cluster" style="margin-bottom: var(--space-8);">
      <span class="chip chip--rose">Tous</span>
      <span class="chip">Connaissance</span>
      <span class="chip">Présence</span>
      <span class="chip">Cadre</span>
      <span class="chip">Soin</span>
      <span class="chip">Famille</span>
      <span class="chip">Fréquence</span>
    </div>

    <div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: var(--space-6);">
      <article class="card card--clickable">
        <p class="card__meta">Connaissance · 7 min</p>
        <h3 class="card__title">Fatigue, blues, épuisement : où est la frontière ?</h3>
        <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-top:var(--space-2);">Trois mots qui se ressemblent, trois réalités différentes.</p>
      </article>
      <article class="card card--clickable">
        <p class="card__meta">Présence · 4 min</p>
        <h3 class="card__title">Pourquoi être entendu change quelque chose</h3>
        <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-top:var(--space-2);">Ce qui se passe dans le corps quand quelqu'un écoute vraiment.</p>
      </article>
      <article class="card card--clickable">
        <p class="card__meta">Cadre · 5 min</p>
        <h3 class="card__title">Quand consulter — et quand ce n'est pas le moment</h3>
        <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-top:var(--space-2);">Quelques repères honnêtes pour décider sans pression.</p>
      </article>
      <article class="card card--clickable">
        <p class="card__meta">Soin · 6 min</p>
        <h3 class="card__title">Prendre soin, sans en faire un projet de plus</h3>
        <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-top:var(--space-2);">Petites pratiques sobres pour les jours sans force.</p>
      </article>
      <article class="card card--clickable">
        <p class="card__meta">Famille · 8 min</p>
        <h3 class="card__title">L'écoute en famille : ce qui peut s'inventer</h3>
        <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-top:var(--space-2);">Quand les liens deviennent tendus, comment ouvrir un espace plus calme.</p>
      </article>
      <article class="card card--clickable">
        <p class="card__meta">Fréquence · 5 min</p>
        <h3 class="card__title">Voix, son et soin : une autre approche</h3>
        <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-top:var(--space-2);">Pourquoi le son agit sur ce que les mots ne suffisent pas à dire.</p>
      </article>
    </div>
  </div>
</section>
'''

# =============================================================
# OUTILS — exemple : Où en êtes-vous (quiz simple)
# =============================================================
OUTIL_OUENETES_BODY = '''
<section class="section">
  <div class="container container--narrow">
    <p class="card__meta">Outil · Question 4 sur 10</p>
    <h1 class="section-title" style="font-size: var(--text-xl); margin-top:var(--space-2);">Au cours des sept derniers jours,<br>vous est-il arrivé de vous sentir « ailleurs » la plupart du temps ?</h1>

    <!-- Progress bar -->
    <div style="height:3px; background: var(--color-divider); border-radius:2px; margin-block:var(--space-8); overflow:hidden;">
      <div style="width:40%; height:100%; background: var(--color-rose);"></div>
    </div>

    <div class="stack">
      <button class="card card--clickable" style="text-align:left; width:100%;">Pas du tout</button>
      <button class="card card--clickable" style="text-align:left; width:100%;">Un peu, par moments</button>
      <button class="card card--clickable" style="text-align:left; width:100%; border-color: var(--color-aubergine); background: var(--color-surface-warm);">Souvent, oui</button>
      <button class="card card--clickable" style="text-align:left; width:100%;">Presque tout le temps</button>
      <button class="card card--clickable" style="text-align:left; width:100%; opacity:0.6;">Je préfère ne pas répondre</button>
    </div>

    <div class="flex-between" style="margin-top:var(--space-8);">
      <button class="btn btn--ghost btn--sm">← Précédent</button>
      <button class="btn btn--primary btn--sm">Suivant →</button>
    </div>

    <p style="margin-top:var(--space-12); text-align:center; font-family:var(--font-serif); font-style:italic; color:var(--color-text-muted); font-size:var(--text-sm); max-width:42ch; margin-inline:auto;">
      Cet outil n'évalue rien et ne pose aucun diagnostic. Il sert seulement à vous aider à mettre des mots, si ça vous parle.
    </p>
  </div>
</section>
'''


# ============================== build ============================
def build():
    pages = [
        ("praticiens.html",       "Praticiens — IVIA",                 "Annuaire des praticien·ne·s d'IVIA — par voie, lieu et disponibilité.", PRATICIENS_BODY),
        ("rendez-vous.html",      "Prendre rendez-vous — IVIA",        "Choisir un·e praticien·ne et un créneau pour une rencontre IVIA.",       RDV_BODY),
        ("audio-async.html",      "S'enregistrer — IVIA",              "Enregistrer un audio asynchrone et recevoir une réponse écrite d'un·e praticien·ne.", AUDIO_ASYNC_BODY),
        ("audio-attente.html",    "Audio en écoute — IVIA",            "Votre enregistrement est en cours d'écoute par un·e praticien·ne.",      AUDIO_ATTENTE_BODY),
        ("audio-resume.html",     "Réponse reçue — IVIA",              "Votre praticien·ne vous a fait parvenir un résumé écrit.",               AUDIO_RESUME_BODY),
        ("dashboard.html",        "Mon espace — IVIA",                 "Tableau de bord client : rendez-vous, notes, journal, outils.",         DASHBOARD_BODY),
      ("compte.html",           "Mon compte — IVIA",                 "Préférences de compte et accès à votre espace IVIA.",                    None),
      ("mot-de-passe-oublie.html", "Mot de passe oublié — IVIA",    "Recevoir un lien de connexion par courriel.",                           None),
        ("journal.html",          "Journal de vie — IVIA",             "Espace privé d'écriture personnelle : notes, rêves, repères.",          JOURNAL_BODY),
        ("ressources.html",       "Ressources — IVIA",                 "Articles et outils à votre rythme, sans rendez-vous.",                  RESSOURCES_BODY),
        ("outil-ou-en-etes-vous.html", "Où en êtes-vous ? — IVIA",     "Petit auto-questionnaire pour faire le point.",                         OUTIL_OUENETES_BODY),
    ]
    for filename, title, description, body in pages:
      if body is None:
        if filename == "compte.html":
          build_compte()
          continue
        if filename == "mot-de-passe-oublie.html":
          build_mot_de_passe_oublie()
          continue
        html = page(title, description, CLIENT_NAV, filename, CLIENT_ACTIONS, body, "index.html", FOOTER_CLIENT)
        (OUT / filename).write_text(html, encoding="utf-8")

    # Outils non détaillés : on duplique outil-ou-en-etes-vous comme placeholder cohérent
    for stub in ["outil-sommeil.html", "outil-frequence.html", "outil-preparer.html"]:
        body = OUTIL_OUENETES_BODY.replace("Où en êtes-vous ?", {
            "outil-sommeil.html": "Sommeil et apaisement",
            "outil-frequence.html": "Fréquence et environnement",
            "outil-preparer.html": "Préparer une rencontre",
        }[stub])
        html = page(f"Outil — IVIA", "Outil interactif IVIA.", CLIENT_NAV, stub, CLIENT_ACTIONS, body, "index.html", FOOTER_CLIENT)
        (OUT / stub).write_text(html, encoding="utf-8")

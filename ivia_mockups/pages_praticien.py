"""Pages côté praticien — interface pro mais accessible, pas médicale ni abrupte."""
from pathlib import Path
from build_pages import page, PRATICIEN_NAV, PRATICIEN_ACTIONS, FOOTER_INTERNE

OUT = Path(__file__).parent / "praticien"

# CSS shared admin/praticien : layout dashboard 2 colonnes (sidebar + content)
WORKSPACE_CSS = '''
.workspace { display: grid; grid-template-columns: 240px 1fr; min-height: calc(100vh - 80px); }
.sidebar { background: var(--color-surface-2); border-right: 1px solid var(--color-divider); padding: var(--space-6) 0; position: sticky; top: 80px; height: calc(100vh - 80px); overflow-y: auto; }
.sidebar h4 { font-size: var(--text-xs); letter-spacing: 0.14em; text-transform: uppercase; color: var(--color-text-faint); padding: 0 var(--space-6); margin-block: var(--space-6) var(--space-2); }
.sidebar h4:first-child { margin-top: 0; }
.sidebar a { display: flex; align-items: center; gap: var(--space-3); padding: var(--space-3) var(--space-6); color: var(--color-text-muted); text-decoration: none; font-size: var(--text-sm); border-left: 2px solid transparent; transition: all var(--transition); }
.sidebar a:hover { color: var(--color-text); background: var(--color-surface-warm); }
.sidebar a[aria-current="page"] { color: var(--color-aubergine); border-left-color: var(--color-rose); background: var(--color-surface-warm); font-weight: 500; }
.sidebar .badge { margin-left: auto; background: var(--color-rose); color: var(--color-creme); font-size: var(--text-xs); padding: 2px 8px; border-radius: var(--radius-full); }
.workspace__content { padding: var(--space-8) var(--space-10); max-width: 100%; }
@media (max-width: 900px) { .workspace { grid-template-columns: 1fr; } .sidebar { position: relative; height: auto; top: 0; } }

.kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: var(--space-4); margin-bottom: var(--space-10); }
.kpi { padding: var(--space-5) var(--space-6); background: var(--color-surface); border: 1px solid var(--color-divider); border-radius: var(--radius-md); }
.kpi__label { font-size: var(--text-xs); letter-spacing: 0.1em; text-transform: uppercase; color: var(--color-text-muted); margin-bottom: var(--space-2); }
.kpi__value { font-family: var(--font-display); font-size: var(--text-xl); }
.kpi__delta { font-size: var(--text-xs); color: var(--color-mousse); margin-top: var(--space-2); }
.kpi__delta--down { color: var(--color-rose-deep); }

.data-table { width: 100%; border-collapse: collapse; }
.data-table th, .data-table td { padding: var(--space-3) var(--space-4); text-align: left; border-bottom: 1px solid var(--color-divider); font-size: var(--text-sm); }
.data-table th { font-size: var(--text-xs); letter-spacing: 0.1em; text-transform: uppercase; color: var(--color-text-muted); font-weight: 500; }
.data-table tbody tr { transition: background var(--transition); cursor: pointer; }
.data-table tbody tr:hover { background: var(--color-surface-warm); }

.workspace__header { margin-bottom: var(--space-8); }
.workspace__header h1 { font-family: var(--font-display); font-size: var(--text-xl); margin-bottom: var(--space-2); }
.workspace__header p { color: var(--color-text-muted); font-family: var(--font-serif); }
'''

# Sidebar HTML praticien
def praticien_sidebar(active):
    items = [
        ("index.html",      "Tableau de bord", None,    "M3 12 L 12 3 L 21 12 M5 10 V 21 H 19 V 10"),
        ("agenda.html",     "Agenda",          None,    "M8 2 V 6 M16 2 V 6 M3 10 H 21 M3 6 H 21 V 22 H 3 Z"),
        ("audios.html",     "Audios à traiter", "3",    "M12 3 V 19 M5 9 V 13 M9 6 V 16 M15 7 V 15 M19 9 V 13"),
        ("clients.html",    "Mes clients",     None,    "M9 11 A 4 4 0 1 0 9 3 A 4 4 0 0 0 9 11 Z M2 21 V 19 A 5 5 0 0 1 7 14 H 11 A 5 5 0 0 1 16 19 V 21"),
        ("mes-offres.html", "Mes offres",      None,    "M3 7 H 21 L 19 21 H 5 Z M 8 7 V 4 A 3 3 0 0 1 11 1 H 13 A 3 3 0 0 1 16 4 V 7"),
        ("outils.html",     "Mes outils",      None,    "M11 4 H 5 V 20 H 19 V 12 M15 3 H 21 V 9 M21 3 L 11 13"),
        ("abonnement.html", "Mon abonnement",  None,    "M2 7 H 22 V 17 H 2 Z M2 11 H 22"),
    ]
    rows = []
    for href, label, badge, path in items:
        cur = ' aria-current="page"' if href == active else ""
        bdg = f'<span class="badge">{badge}</span>' if badge else ""
        icon = f'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="{path}"/></svg>'
        rows.append(f'<a href="{href}"{cur}>{icon}<span>{label}</span>{bdg}</a>')

    profil = '''<a href="#" style="margin-top: auto;">
      <div style="width:24px; height:24px; border-radius:50%; background:linear-gradient(135deg, #C58A8A, #D89260);"></div>
      <span>Maïté L.-T.</span>
    </a>'''
    return f'<aside class="sidebar" aria-label="Navigation espace praticien"><h4>Espace praticien</h4>{"".join(rows)}<h4 style="margin-top:var(--space-12);">Compte</h4>{profil}</aside>'


# =============================================================
# INDEX praticien — tableau de bord
# =============================================================
def index_body():
    return f'''
<div class="workspace">
  {praticien_sidebar("index.html")}
  <div class="workspace__content">
    <header class="workspace__header">
      <p style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-rose-deep);">Samedi 9 mai · 7 h 12</p>
      <h1>Bonjour, Maïté.</h1>
      <p>Trois audios vous attendent. Deux rencontres aujourd'hui. Le reste peut attendre demain.</p>
    </header>

    <div class="kpi-grid">
      <div class="kpi"><p class="kpi__label">Rencontres cette semaine</p><p class="kpi__value">14</p><p class="kpi__delta">+3 vs sem. dernière</p></div>
      <div class="kpi"><p class="kpi__label">Audios à traiter</p><p class="kpi__value">3</p><p class="kpi__delta kpi__delta--down">2 reçus aujourd'hui</p></div>
      <div class="kpi"><p class="kpi__label">Clients actifs</p><p class="kpi__value">28</p><p class="kpi__delta">+2 ce mois</p></div>
      <div class="kpi"><p class="kpi__label">Revenu prévu (mois)</p><p class="kpi__value">2 660 $</p><p class="kpi__delta">Après commission IVIA</p></div>
    </div>

    <div class="grid" style="grid-template-columns: 1.5fr 1fr; gap:var(--space-8);">
      <div>
        <h2 style="font-family:var(--font-display); font-size:var(--text-lg); margin-bottom:var(--space-4);">Aujourd'hui</h2>
        <div class="stack">
          <article class="card">
            <div class="flex-between">
              <div>
                <p style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-rose-deep);">10 h 30 — 11 h 30</p>
                <h3 class="card__title" style="font-size:var(--text-base); margin-top:var(--space-1);">Camille T. · Suivi</h3>
                <p style="font-size:var(--text-xs); color:var(--color-text-muted); margin-top:var(--space-2);">3<sup>e</sup> rencontre · à distance · note préparée</p>
              </div>
              <div class="flex">
                <button class="btn btn--ghost btn--sm">Préparer</button>
                <button class="btn btn--primary btn--sm">Démarrer</button>
              </div>
            </div>
          </article>
          <article class="card">
            <div class="flex-between">
              <div>
                <p style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-text-muted);">14 h 00 — 15 h 00</p>
                <h3 class="card__title" style="font-size:var(--text-base); margin-top:var(--space-1);">Olivier R. · Première rencontre</h3>
                <p style="font-size:var(--text-xs); color:var(--color-text-muted); margin-top:var(--space-2);">Référé par audio asynchrone du 5 mai</p>
              </div>
              <div class="flex">
                <button class="btn btn--ghost btn--sm">Préparer</button>
              </div>
            </div>
          </article>
          <article class="card" style="opacity:0.7;">
            <div class="flex-between">
              <div>
                <p style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-text-muted);">16 h 30 — 17 h 00</p>
                <h3 class="card__title" style="font-size:var(--text-base); margin-top:var(--space-1);">Léa B. · Appel court (15 min)</h3>
                <p style="font-size:var(--text-xs); color:var(--color-text-muted); margin-top:var(--space-2);">Suite d'audio asynchrone du 8 mai</p>
              </div>
            </div>
          </article>
        </div>

        <h2 style="font-family:var(--font-display); font-size:var(--text-lg); margin-block: var(--space-10) var(--space-4);">Audios reçus</h2>
        <div class="stack">
          <article class="card">
            <div class="flex-between">
              <div>
                <p style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-rose-deep);">Reçu · 9 mai · 14 h 22</p>
                <h3 class="card__title" style="font-size:var(--text-base); margin-top:var(--space-1);">Camille T. · 5 min 41 s</h3>
                <p style="font-size:var(--text-xs); color:var(--color-text-muted); margin-top:var(--space-2);">Échéance de réponse : 11 mai · 14 h 22</p>
              </div>
              <a href="audio-traiter.html" class="btn btn--primary btn--sm">Écouter & répondre</a>
            </div>
          </article>
          <article class="card" style="opacity:0.85;">
            <div class="flex-between">
              <div>
                <p style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-text-muted);">Reçu · 8 mai · 22 h 04</p>
                <h3 class="card__title" style="font-size:var(--text-base); margin-top:var(--space-1);">Nouvelle personne · 8 min 03 s</h3>
                <p style="font-size:var(--text-xs); color:var(--color-text-muted); margin-top:var(--space-2);">Échéance : 10 mai · 22 h 04</p>
              </div>
              <a href="audio-traiter.html" class="btn btn--ghost btn--sm">Écouter</a>
            </div>
          </article>
        </div>
      </div>

      <aside>
        <div class="card card--warm">
          <p class="card__meta">Pause</p>
          <h3 class="card__title">Vous avez écouté 4 audios cette semaine.</h3>
          <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-top:var(--space-3);">
            Pensez à respirer entre deux écoutes. Le système vous suggère de bloquer 30 min sans rendez-vous demain matin — voulez-vous l'ajouter à votre agenda ?
          </p>
          <button class="btn btn--ghost btn--sm" style="margin-top:var(--space-4);">Bloquer 30 min</button>
        </div>

        <div class="card" style="margin-top:var(--space-4);">
          <p class="card__meta">À venir</p>
          <h3 class="card__title">5 nouvelles demandes en file</h3>
          <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-top:var(--space-2);">
            Trois personnes vous ont demandé·e en première rencontre cette semaine. Voulez-vous traiter la file maintenant ?
          </p>
          <a href="clients.html" class="btn btn--ghost btn--sm" style="margin-top:var(--space-4);">Voir la file →</a>
        </div>

        <div class="card" style="margin-top:var(--space-4); background: linear-gradient(135deg, var(--color-mousse), var(--color-glacier)); color: var(--color-creme); border:none;">
          <p style="font-family:var(--font-display); font-size:var(--text-base); font-style:italic; line-height:1.5;">
            « Tenir un cadre suffisamment solide pour que la personne en face n'ait plus à le faire. »
          </p>
          <p style="margin-top:var(--space-3); font-size:var(--text-xs); letter-spacing:0.1em; opacity:0.85;">— Repère IV de la maison</p>
        </div>
      </aside>
    </div>
  </div>
</div>
'''


# =============================================================
# AGENDA
# =============================================================
def agenda_body():
    # Crée 5 colonnes (lun-ven) avec 12 lignes (8h-19h)
    days = ["Lun 11", "Mar 12", "Mer 13", "Jeu 14", "Ven 15"]
    hours = list(range(8, 20))

    cells = []
    # On bloque quelques rendez-vous pour rendre l'agenda crédible
    fixed = {
        ("Lun 11", 9):  ("Camille T.", "rose"),
        ("Lun 11", 14): ("Bloc audios", "miel"),
        ("Mar 12", 10): ("Olivier R.", "glacier"),
        ("Mar 12", 14): ("Léa B.", "lavande"),
        ("Mer 13", 11): ("Pause", "warm"),
        ("Mer 13", 15): ("Anne P.", "mousse"),
        ("Jeu 14", 9):  ("Camille T.", "rose"),
        ("Jeu 14", 16): ("Appel court", "abricot"),
        ("Ven 15", 10): ("Nicolas D.", "glacier"),
        ("Ven 15", 13): ("Bloc admin", "miel"),
    }
    color_map = {
        "rose":    "background: color-mix(in oklab, var(--color-rose) 30%, var(--color-creme)); color: var(--color-rose-deep); border-color: var(--color-rose);",
        "mousse":  "background: color-mix(in oklab, var(--color-mousse) 25%, var(--color-creme)); color: #3F5239; border-color: var(--color-mousse);",
        "glacier": "background: color-mix(in oklab, var(--color-glacier) 25%, var(--color-creme)); color: #3F5566; border-color: var(--color-glacier);",
        "lavande": "background: color-mix(in oklab, var(--color-lavande) 25%, var(--color-creme)); color: #4A3D6A; border-color: var(--color-lavande);",
        "abricot": "background: color-mix(in oklab, var(--color-abricot) 25%, var(--color-creme)); color: #7A4A20; border-color: var(--color-abricot);",
        "miel":    "background: color-mix(in oklab, var(--color-miel) 30%, var(--color-creme)); color: #6E5018; border-color: var(--color-miel);",
        "warm":    "background: var(--color-surface-warm); color: var(--color-text-muted); border-color: var(--color-divider);",
    }

    rows = ""
    for h in hours:
        row = f'<div class="hour-label">{h:02d}:00</div>'
        for d in days:
            entry = fixed.get((d, h))
            if entry:
                label, color = entry
                row += f'<div class="cell cell--booked" style="{color_map[color]}"><strong>{label}</strong></div>'
            else:
                row += '<div class="cell"></div>'
        rows += f'<div class="row">{row}</div>'

    days_header = '<div class="hour-label"></div>' + "".join(f'<div class="day-label">{d}</div>' for d in days)
    return f'''
<div class="workspace">
  {praticien_sidebar("agenda.html")}
  <div class="workspace__content">
    <header class="workspace__header">
      <p style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-rose-deep);">Semaine du 11 au 15 mai 2026</p>
      <h1>Mon agenda</h1>
      <p>14 rencontres planifiées · 3 plages libres réservables · 2 plages bloquées (audios, admin)</p>
    </header>

    <div class="flex-between" style="margin-bottom:var(--space-6);">
      <div class="flex">
        <button class="btn btn--ghost btn--sm">← Sem. précédente</button>
        <button class="btn btn--ghost btn--sm">Sem. suivante →</button>
        <button class="btn btn--ghost btn--sm">Aujourd'hui</button>
      </div>
      <div class="flex">
        <button class="btn btn--ghost btn--sm">Bloquer une plage</button>
        <button class="btn btn--primary btn--sm">＋ Ajouter rencontre</button>
      </div>
    </div>

    <div class="agenda">
      <div class="row row--header">{days_header}</div>
      {rows}
    </div>

    <style>
      .agenda {{ background: var(--color-surface); border: 1px solid var(--color-divider); border-radius: var(--radius-md); overflow: hidden; }}
      .row {{ display: grid; grid-template-columns: 80px repeat(5, 1fr); border-bottom: 1px solid var(--color-divider); }}
      .row:last-child {{ border-bottom: none; }}
      .row--header {{ background: var(--color-surface-warm); position: sticky; top: 80px; z-index:5; }}
      .hour-label, .day-label {{ padding: var(--space-3) var(--space-4); font-size: var(--text-xs); letter-spacing: 0.1em; text-transform: uppercase; color: var(--color-text-muted); border-right: 1px solid var(--color-divider); }}
      .day-label {{ font-family: var(--font-display); font-weight: 500; color: var(--color-text); }}
      .cell {{ padding: var(--space-2) var(--space-3); border-right: 1px solid var(--color-divider); min-height: 56px; font-size: var(--text-xs); }}
      .cell:last-child {{ border-right: none; }}
      .cell--booked {{ border-left: 2px solid; cursor: pointer; transition: filter var(--transition); }}
      .cell--booked:hover {{ filter: brightness(1.05); }}
      .cell--booked strong {{ font-family: var(--font-display); font-size: var(--text-sm); font-weight: 500; }}
    </style>

    <p style="margin-top:var(--space-8); font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm);">
      <strong>Astuce :</strong> les plages « Pause » et « Bloc admin » sont créées automatiquement par le système après une charge soutenue de rencontres. Vous pouvez les déplacer ou les supprimer.
    </p>
  </div>
</div>
'''


# =============================================================
# AUDIOS À TRAITER (liste)
# =============================================================
def audios_body():
    return f'''
<div class="workspace">
  {praticien_sidebar("audios.html")}
  <div class="workspace__content">
    <header class="workspace__header">
      <h1>Audios à traiter</h1>
      <p>Trois audios reçus en attente d'écoute. L'engagement de la maison : réponse écrite sous 48 h ouvrables.</p>
    </header>

    <div class="cluster" style="margin-bottom: var(--space-6);">
      <span class="chip chip--rose">Tous (3)</span>
      <span class="chip">Urgents (1)</span>
      <span class="chip">Nouveaux clients (1)</span>
      <span class="chip">Suivis (2)</span>
    </div>

    <div class="card" style="padding:0; overflow:hidden;">
      <table class="data-table">
        <thead>
          <tr>
            <th>Personne</th>
            <th>Reçu</th>
            <th>Durée</th>
            <th>Échéance réponse</th>
            <th>Statut</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Camille T.</strong><br><span style="font-size:var(--text-xs); color:var(--color-text-muted);">Suivi · 4<sup>e</sup> audio</span></td>
            <td>9 mai · 14 h 22</td>
            <td>5 min 41 s</td>
            <td><span style="color:var(--color-mousse);">Demain · 14 h</span></td>
            <td><span class="chip chip--miel"><span class="status-dot status-dot--pending"></span> En attente</span></td>
            <td><a href="audio-traiter.html" class="btn btn--primary btn--sm">Écouter</a></td>
          </tr>
          <tr>
            <td><strong>Personne (1<sup>er</sup> contact)</strong><br><span style="font-size:var(--text-xs); color:var(--color-text-muted);">Audio d'arrivée</span></td>
            <td>8 mai · 22 h 04</td>
            <td>8 min 03 s</td>
            <td><span style="color:var(--color-rose-deep);">Aujourd'hui · 22 h</span></td>
            <td><span class="chip chip--miel"><span class="status-dot status-dot--alert"></span> Urgent</span></td>
            <td><a href="audio-traiter.html" class="btn btn--primary btn--sm">Écouter</a></td>
          </tr>
          <tr>
            <td><strong>Léa B.</strong><br><span style="font-size:var(--text-xs); color:var(--color-text-muted);">Suivi · 2<sup>e</sup> audio</span></td>
            <td>8 mai · 11 h 17</td>
            <td>3 min 28 s</td>
            <td>Demain · 11 h</td>
            <td><span class="chip chip--miel"><span class="status-dot status-dot--pending"></span> En attente</span></td>
            <td><a href="audio-traiter.html" class="btn btn--ghost btn--sm">Écouter</a></td>
          </tr>
        </tbody>
      </table>
    </div>

    <h2 style="font-family:var(--font-display); font-size:var(--text-lg); margin-block: var(--space-12) var(--space-4);">Récemment répondu</h2>
    <div class="card" style="padding:0; overflow:hidden;">
      <table class="data-table">
        <thead><tr><th>Personne</th><th>Répondu le</th><th>Suite</th></tr></thead>
        <tbody>
          <tr><td><strong>Marc V.</strong></td><td>7 mai · 16 h 12</td><td><span class="chip chip--mousse">A pris RV</span></td></tr>
          <tr><td><strong>Nadia O.</strong></td><td>6 mai · 9 h 47</td><td><span class="chip">Sans suite (OK)</span></td></tr>
          <tr><td><strong>Hugo P.</strong></td><td>5 mai · 17 h 30</td><td><span class="chip chip--glacier">Appel court prévu</span></td></tr>
        </tbody>
      </table>
    </div>
  </div>
</div>
'''


# =============================================================
# AUDIO À TRAITER — écran de réponse (le cœur du métier)
# =============================================================
def audio_traiter_body():
    return f'''
<div class="workspace">
  {praticien_sidebar("audios.html")}
  <div class="workspace__content">
    <header class="workspace__header">
      <p style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-rose-deep);"><a href="audios.html" style="color:inherit;">← Retour à la file</a></p>
      <h1>Camille T. · audio du 9 mai</h1>
      <p>5 min 41 s · 4<sup>e</sup> audio reçu · suivi en cours depuis le 28 avril</p>
    </header>

    <div class="grid" style="grid-template-columns: 1.5fr 1fr; gap:var(--space-8); align-items:flex-start;">

      <!-- Colonne gauche : audio + transcription + zone réponse -->
      <div>
        <!-- Lecteur -->
        <div class="card">
          <div class="flex-between" style="margin-bottom:var(--space-4);">
            <div>
              <p class="card__meta">Audio · 5 min 41 s</p>
              <h3 class="card__title" style="font-size:var(--text-base);">Sans titre — déposé hier à 14 h 22</h3>
            </div>
            <div class="flex">
              <button class="btn btn--ghost btn--sm">×0.75</button>
              <button class="btn btn--ghost btn--sm">×1</button>
              <button class="btn btn--ghost btn--sm">×1.5</button>
            </div>
          </div>

          <div data-record-wave style="height:60px; display:flex; align-items:center; gap:2px; margin-block: var(--space-3);">
            ''' + "".join(f'<span style="width:3px; height:{20+(i*7)%40}px; background: var(--color-rose); border-radius:1px; opacity:{0.4 if i > 30 else 1};"></span>' for i in range(60)) + '''
          </div>

          <div class="flex-between" style="font-family:var(--font-display); font-variant-numeric:tabular-nums; font-size:var(--text-sm); color:var(--color-text-muted);">
            <span>02:14</span>
            <span>05:41</span>
          </div>

          <div class="flex" style="margin-top:var(--space-4); justify-content:center; gap:var(--space-3);">
            <button class="btn btn--ghost btn--sm">⏮ -10s</button>
            <button class="btn btn--primary" data-audio-fake aria-pressed="false">▶︎ Écouter</button>
            <button class="btn btn--ghost btn--sm">+10s ⏭</button>
          </div>
        </div>

        <!-- Transcription auto (avec disclaimer) -->
        <details class="card" style="margin-top:var(--space-4); background: var(--color-surface-warm);">
          <summary style="cursor:pointer; font-family:var(--font-display); font-size:var(--text-base);">Transcription automatique <span style="font-size:var(--text-xs); color:var(--color-text-muted); font-family:var(--font-body); font-style:normal;">(brouillon · ne remplace pas l'écoute)</span></summary>
          <div style="margin-top:var(--space-4); font-family:var(--font-serif); font-size:var(--text-sm); line-height:1.7; color:var(--color-text-muted);">
            <p style="margin-bottom:0.8em;"><strong style="color:var(--color-text);">[00:00]</strong> Allô, Maïté, c'est Camille. Euh… j'ai pas trop dormi cette nuit non plus, ça fait je pense la quatrième nuit en cinq, et je voulais juste, vous, t'enregistrer un peu ce que ça donne, parce que je sais pas si on va se voir avant jeudi.</p>
            <p style="margin-bottom:0.8em;"><strong style="color:var(--color-text);">[01:12]</strong> Pendant la journée j'arrive à fonctionner, mais c'est comme si je passais à côté de moi-même. Je fais les choses, mais je suis pas vraiment dans les choses…</p>
            <p style="margin-bottom:0.8em;"><strong style="color:var(--color-text);">[03:02]</strong> Et hier, juste pour être honnête, j'ai pleuré dans le métro sans raison. C'était pas une grosse crise mais c'était la première fois depuis longtemps. Je veux pas que tu t'inquiètes mais je voulais le dire.</p>
            <p><strong style="color:var(--color-text);">[04:48]</strong> Donc voilà. Je suis pas en détresse, mais quelque chose ne va plus comme avant. Merci d'écouter. À jeudi.</p>
          </div>
        </details>

        <!-- Réponse à rédiger -->
        <div class="card" style="margin-top:var(--space-6);">
          <div class="flex-between" style="margin-bottom:var(--space-4);">
            <h3 style="font-family:var(--font-display); font-size:var(--text-lg);">Votre réponse écrite</h3>
            <span style="font-size:var(--text-xs); color:var(--color-text-muted);">Auto-sauvegardé · 2 min</span>
          </div>

          <div class="field">
            <label for="reponse">Texte (sera envoyé à Camille)</label>
            <textarea id="reponse" rows="14" placeholder="Une réponse honnête, courte si possible. La maison ne demande pas un compte-rendu, mais un retour humain.">Bonjour Camille,

Merci pour cet enregistrement. Je l'ai écouté ce matin — deux fois. Je veux d'abord vous dire que ce que vous décrivez (passer à côté de soi pendant la journée, pleurer sans raison apparente) n'a pas besoin d'être justifié pour mériter qu'on s'y arrête. Et le fait que vous l'ayez nommé, surtout sans dramatiser, c'est important pour la suite.

Je propose qu'on garde le rendez-vous de jeudi, mais que je prenne d'abord 5 minutes au début pour ouvrir avec ce que vous venez de partager. Pas pour le creuser tout de suite — pour le poser, simplement.

D'ici là : si une nuit redevient difficile, n'hésitez pas à m'envoyer un autre audio, même très court. Pas besoin d'attendre d'avoir trouvé les bons mots.

Bien à vous,
Maïté</textarea>
          </div>

          <div class="flex" style="margin-top:var(--space-4); flex-wrap:wrap;">
            <button class="btn btn--ghost btn--sm">📎 Joindre une ressource</button>
            <button class="btn btn--ghost btn--sm">⤓ Insérer une trame</button>
            <button class="btn btn--ghost btn--sm">✦ Suggérer un appel court</button>
          </div>

          <hr style="margin:var(--space-6) 0; border:none; border-top:1px solid var(--color-divider);">

          <div class="flex-between" style="flex-wrap:wrap; gap:var(--space-3);">
            <span style="font-size:var(--text-xs); color:var(--color-text-muted);">256 mots · ~1 min de lecture · ton : posé, sobre.</span>
            <div class="flex">
              <button class="btn btn--ghost btn--sm">Sauvegarder le brouillon</button>
              <button class="btn btn--primary">Envoyer à Camille →</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Colonne droite : contexte client -->
      <aside>
        <div class="card card--warm">
          <p class="card__meta">Personne</p>
          <h3 class="card__title">Camille T.</h3>
          <p style="font-size:var(--text-sm); color:var(--color-text-muted); font-family:var(--font-serif);">36 ans · suivie depuis le 28 avril (3 rencontres + 4 audios) · voie : Sommeil + Fréquence.</p>
          <a href="clients.html" class="btn btn--ghost btn--sm" style="margin-top:var(--space-4);">Ouvrir la fiche →</a>
        </div>

        <div class="card" style="margin-top:var(--space-4);">
          <p class="card__meta">Repères de la dernière rencontre</p>
          <ul role="list" style="display:flex; flex-direction:column; gap:var(--space-2); font-size:var(--text-sm); margin-top:var(--space-3);">
            <li>• Fatigue installée, ne disparaît plus avec le repos</li>
            <li>• A commencé à noter ses « bons moments » de la semaine</li>
            <li>• N'a pas reparlé de sa relation au travail (à laisser venir)</li>
            <li>• Préfère les rencontres en début de matinée</li>
          </ul>
        </div>

        <div class="card" style="margin-top:var(--space-4); border-color: var(--color-rose); background: color-mix(in oklab, var(--color-rose) 10%, var(--color-creme));">
          <p class="card__meta" style="color: var(--color-rose-deep);">⚠ Repère vigilance</p>
          <p style="font-family:var(--font-serif); font-size:var(--text-sm); color:var(--color-text);">
            « Pleurer dans le métro sans raison » + 4<sup>e</sup> nuit difficile. Sans alarme, mais à noter dans la suite. Si récurrence : envisager un point en présentiel.
          </p>
        </div>
      </aside>
    </div>
  </div>
</div>
'''


# =============================================================
# CLIENTS — annuaire praticien
# =============================================================
def clients_body():
    return f'''
<div class="workspace">
  {praticien_sidebar("clients.html")}
  <div class="workspace__content">
    <header class="workspace__header">
      <h1>Mes clients</h1>
      <p>28 personnes accompagnées · 3 nouvelles demandes en file · 5 suivis longs (≥ 6 rencontres).</p>
    </header>

    <div class="flex-between" style="margin-bottom:var(--space-6); flex-wrap:wrap; gap:var(--space-4);">
      <div class="cluster">
        <span class="chip chip--rose">Tous (28)</span>
        <span class="chip">Suivis (12)</span>
        <span class="chip">Première rencontre passée (11)</span>
        <span class="chip">Audio uniquement (5)</span>
        <span class="chip">Nouvelles demandes (3)</span>
      </div>
      <div class="field" style="max-width:280px;">
        <input type="search" placeholder="Rechercher une personne…">
      </div>
    </div>

    <div class="card" style="padding:0; overflow:hidden;">
      <table class="data-table">
        <thead><tr><th>Nom</th><th>Voie</th><th>Dernier contact</th><th>Prochain</th><th>Suivi</th><th>Statut</th></tr></thead>
        <tbody>
          <tr>
            <td><strong>Camille T.</strong></td>
            <td><span class="chip chip--mousse">Fréquence</span> <span class="chip chip--glacier">Sommeil</span></td>
            <td>9 mai (audio)</td>
            <td>Jeu 12 mai · 14 h</td>
            <td>3 rencontres · 4 audios</td>
            <td><span class="status-dot status-dot--ok"></span> En cours</td>
          </tr>
          <tr>
            <td><strong>Olivier R.</strong></td>
            <td><span class="chip chip--lavande">Connaissance</span></td>
            <td>5 mai (audio d'arrivée)</td>
            <td>Mar 12 mai · 14 h</td>
            <td>Première à venir</td>
            <td><span class="status-dot status-dot--ok"></span> Nouvelle</td>
          </tr>
          <tr>
            <td><strong>Léa B.</strong></td>
            <td><span class="chip chip--glacier">Sommeil</span></td>
            <td>8 mai (audio)</td>
            <td>Jeu 14 · 16 h 30 (appel)</td>
            <td>2 audios</td>
            <td><span class="status-dot status-dot--pending"></span> Audio en attente</td>
          </tr>
          <tr>
            <td><strong>Anne P.</strong></td>
            <td><span class="chip chip--rose">Famille</span></td>
            <td>2 mai (rencontre)</td>
            <td>Mer 13 mai · 15 h</td>
            <td>5 rencontres</td>
            <td><span class="status-dot status-dot--ok"></span> En cours</td>
          </tr>
          <tr>
            <td><strong>Nicolas D.</strong></td>
            <td><span class="chip chip--mousse">Fréquence</span></td>
            <td>26 avril (rencontre)</td>
            <td>Ven 15 mai · 10 h</td>
            <td>2 rencontres</td>
            <td><span class="status-dot status-dot--ok"></span> En cours</td>
          </tr>
          <tr style="opacity:0.85;">
            <td><strong>Hugo P.</strong></td>
            <td><span class="chip">À préciser</span></td>
            <td>5 mai (audio)</td>
            <td>—</td>
            <td>1 audio · appel à fixer</td>
            <td><span class="status-dot status-dot--pending"></span> À recontacter</td>
          </tr>
          <tr style="opacity:0.7;">
            <td><strong>Nadia O.</strong></td>
            <td><span class="chip chip--glacier">Sommeil</span></td>
            <td>6 mai (audio)</td>
            <td>—</td>
            <td>1 audio · sans suite (OK)</td>
            <td><span class="status-dot"></span> Non poursuivi</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</div>
'''


# =============================================================
# OUTILS PRATICIEN
# =============================================================
def outils_body():
    return f'''
<div class="workspace">
  {praticien_sidebar("outils.html")}
  <div class="workspace__content">
    <header class="workspace__header">
      <h1>Mes outils</h1>
      <p>Trames d'écoute, modèles de réponse, ressources à partager. Tout reste modifiable, rien n'est imposé.</p>
    </header>

    <div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: var(--space-6);">

      <article class="card card--clickable">
        <p class="card__meta">Trame d'écoute</p>
        <h3 class="card__title">Première rencontre — ouvrir l'espace</h3>
        <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-top:var(--space-2);">9 questions repères pour une première séance, sans formulaire à cocher.</p>
        <div class="cluster" style="margin-top:var(--space-4);"><span class="chip">Texte · 4 pages</span></div>
      </article>

      <article class="card card--clickable">
        <p class="card__meta">Trame d'écoute</p>
        <h3 class="card__title">Quand la fatigue s'installe</h3>
        <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-top:var(--space-2);">Distinguer fatigue, blues, épuisement — ce qu'il faut écouter, ce qu'il faut renvoyer ailleurs.</p>
        <div class="cluster" style="margin-top:var(--space-4);"><span class="chip chip--glacier">Sommeil</span></div>
      </article>

      <article class="card card--clickable">
        <p class="card__meta">Modèle de réponse audio</p>
        <h3 class="card__title">Réponse à un 1<sup>er</sup> audio</h3>
        <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-top:var(--space-2);">Squelette à adapter : accusé d'écoute, restitution, proposition de bref appel.</p>
        <div class="cluster" style="margin-top:var(--space-4);"><span class="chip">Modèle texte</span></div>
      </article>

      <article class="card card--clickable">
        <p class="card__meta">Cadrage</p>
        <h3 class="card__title">Quand IVIA n'est pas le bon endroit</h3>
        <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-top:var(--space-2);">Indicateurs et formulations sobres pour orienter vers un médecin, urgence sociale, etc.</p>
        <div class="cluster" style="margin-top:var(--space-4);"><span class="chip chip--rose">Vigilance</span></div>
      </article>

      <article class="card card--clickable">
        <p class="card__meta">Ressource client</p>
        <h3 class="card__title">À partager — « Petits gestes pour les nuits difficiles »</h3>
        <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-top:var(--space-2);">Document court à envoyer en pièce jointe d'une réponse audio.</p>
        <div class="cluster" style="margin-top:var(--space-4);"><span class="chip chip--glacier">Sommeil</span></div>
      </article>

      <article class="card card--clickable">
        <p class="card__meta">Trame d'écoute</p>
        <h3 class="card__title">Préparer une fin de suivi</h3>
        <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-top:var(--space-2);">Comment nommer une dernière rencontre, sans la dramatiser ni la précipiter.</p>
        <div class="cluster" style="margin-top:var(--space-4);"><span class="chip">Texte · 2 pages</span></div>
      </article>

    </div>

    <h2 style="font-family:var(--font-display); font-size:var(--text-lg); margin-block: var(--space-12) var(--space-4);">Vos propres trames</h2>
    <p style="color:var(--color-text-muted); font-family:var(--font-serif); margin-bottom:var(--space-6);">
      Vous pouvez créer vos propres trames et les garder pour vous, ou les proposer à la maison pour qu'elles enrichissent la bibliothèque commune.
    </p>
    <button class="btn btn--primary">＋ Créer une trame</button>
  </div>
</div>
'''


# =============================================================
# ABONNEMENT PRATICIEN — page attractive
# =============================================================
def abonnement_body():
    return f'''
<div class="workspace">
  {praticien_sidebar("abonnement.html")}
  <div class="workspace__content">
    <header class="workspace__header">
      <p style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-rose-deep);">Mon abonnement</p>
      <h1>Pratiquer sereinement, sans gérer l'administratif.</h1>
      <p>L'abonnement IVIA prend en charge l'agenda, la facturation, la promotion, et la sécurité de vos données. Vous, vous écoutez.</p>
    </header>

    <!-- Statut actuel -->
    <div class="card card--warm" style="margin-bottom:var(--space-12); padding:var(--space-8);">
      <div class="flex-between" style="flex-wrap:wrap; gap:var(--space-6);">
        <div>
          <p class="card__meta">Plan actuel</p>
          <h2 style="font-family:var(--font-display); font-size:var(--text-xl);">Praticien·ne — Suivi régulier</h2>
          <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-top:var(--space-2);">
            Renouvelé le 1<sup>er</sup> mai · prochain prélèvement le 1<sup>er</sup> juin
          </p>
        </div>
        <div style="text-align:right;">
          <p style="font-family:var(--font-display); font-size:var(--text-2xl); font-weight:400;">79 $<span style="font-size:var(--text-base); color:var(--color-text-muted); font-weight:400;"> /mois</span></p>
          <p style="font-size:var(--text-xs); color:var(--color-text-muted);">+ 12 % par rencontre encaissée via IVIA</p>
        </div>
      </div>
      <div class="flex" style="margin-top:var(--space-6);">
        <button class="btn btn--ghost btn--sm">Voir mes factures</button>
        <button class="btn btn--ghost btn--sm">Modifier le mode de paiement</button>
      </div>
    </div>

    <h2 style="font-family:var(--font-display); font-size:var(--text-lg); margin-bottom:var(--space-6);">Ce qu'IVIA fait pour vous</h2>

    <div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:var(--space-4); margin-bottom:var(--space-12);">
      <div class="card" style="padding:var(--space-5);">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" style="color:var(--color-rose); margin-bottom:var(--space-3);"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 9 H 21 M 8 3 V 7 M 16 3 V 7"/></svg>
        <h3 style="font-family:var(--font-display); font-size:var(--text-base); margin-bottom:var(--space-2);">Agenda & rappels</h3>
        <p style="font-family:var(--font-serif); font-size:var(--text-sm); color:var(--color-text-muted);">Vos clients réservent en ligne. Rappels SMS et courriels automatiques.</p>
      </div>
      <div class="card" style="padding:var(--space-5);">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" style="color:var(--color-mousse); margin-bottom:var(--space-3);"><path d="M12 1 L 3 5 V 11 C 3 16.5, 7 21, 12 23 C 17 21, 21 16.5, 21 11 V 5 Z"/></svg>
        <h3 style="font-family:var(--font-display); font-size:var(--text-base); margin-bottom:var(--space-2);">Sécurité & confidentialité</h3>
        <p style="font-family:var(--font-serif); font-size:var(--text-sm); color:var(--color-text-muted);">Hébergement Québec, conformité Loi 25. Vous gardez la main sur les notes, IVIA garde les murs.</p>
      </div>
      <div class="card" style="padding:var(--space-5);">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" style="color:var(--color-glacier); margin-bottom:var(--space-3);"><path d="M2 21 V 19 A 5 5 0 0 1 7 14 H 11 A 5 5 0 0 1 16 19 V 21 M 9 11 A 4 4 0 1 0 9 3 A 4 4 0 0 0 9 11 Z M 18 9 A 3 3 0 1 0 18 3 A 3 3 0 0 0 18 9 Z"/></svg>
        <h3 style="font-family:var(--font-display); font-size:var(--text-base); margin-bottom:var(--space-2);">Annuaire & demandes</h3>
        <p style="font-family:var(--font-serif); font-size:var(--text-sm); color:var(--color-text-muted);">Visibilité sur l'annuaire IVIA. Trois nouvelles demandes vous attendent en moyenne par mois.</p>
      </div>
      <div class="card" style="padding:var(--space-5);">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" style="color:var(--color-lavande); margin-bottom:var(--space-3);"><path d="M12 3 V 21 M 5 9 V 13 M 9 6 V 16 M 15 7 V 15 M 19 9 V 13"/></svg>
        <h3 style="font-family:var(--font-display); font-size:var(--text-base); margin-bottom:var(--space-2);">Audio asynchrone</h3>
        <p style="font-family:var(--font-serif); font-size:var(--text-sm); color:var(--color-text-muted);">Outil de réception, transcription, gabarits de réponse. Une voie d'entrée bas engagement pour vos clients.</p>
      </div>
      <div class="card" style="padding:var(--space-5);">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" style="color:var(--color-miel); margin-bottom:var(--space-3);"><circle cx="12" cy="12" r="9"/><path d="M12 7 V 12 L 15 14"/></svg>
        <h3 style="font-family:var(--font-display); font-size:var(--text-base); margin-bottom:var(--space-2);">Pause auto & charge</h3>
        <p style="font-family:var(--font-serif); font-size:var(--text-sm); color:var(--color-text-muted);">Le système suggère des pauses quand votre charge devient lourde. Personne ne vous pousse à en prendre plus.</p>
      </div>
      <div class="card" style="padding:var(--space-5);">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" style="color:var(--color-prune); margin-bottom:var(--space-3);"><path d="M4 7 H 20 L 18 21 H 6 Z M 8 7 V 4 A 2 2 0 0 1 10 2 H 14 A 2 2 0 0 1 16 4 V 7"/></svg>
        <h3 style="font-family:var(--font-display); font-size:var(--text-base); margin-bottom:var(--space-2);">Trousse de trames</h3>
        <p style="font-family:var(--font-serif); font-size:var(--text-sm); color:var(--color-text-muted);">Bibliothèque de trames d'écoute et de modèles, enrichie chaque mois par les praticien·ne·s de la maison.</p>
      </div>
    </div>

    <!-- Plans -->
    <h2 style="font-family:var(--font-display); font-size:var(--text-lg); margin-bottom:var(--space-6);">Plans</h2>
    <div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:var(--space-6);">

      <div class="card" style="padding:var(--space-8);">
        <p class="card__meta">Découverte</p>
        <h3 class="card__title" style="font-size:var(--text-lg);">Pratique légère</h3>
        <p style="font-family:var(--font-display); font-size:var(--text-2xl); margin-block:var(--space-3);">39 $<span style="font-size:var(--text-base); color:var(--color-text-muted);"> /mois</span></p>
        <p style="font-size:var(--text-xs); color:var(--color-text-muted); margin-bottom:var(--space-6);">+ 15 % par rencontre encaissée</p>
        <ul role="list" style="display:flex; flex-direction:column; gap:var(--space-2); font-size:var(--text-sm); margin-bottom:var(--space-6);">
          <li>✓ Jusqu'à 8 rencontres / semaine</li>
          <li>✓ Agenda & rappels</li>
          <li>✓ Audio asynchrone</li>
          <li style="opacity:0.5;">✗ Visibilité annuaire</li>
        </ul>
        <button class="btn btn--ghost" style="width:100%;">Choisir Découverte</button>
      </div>

      <div class="card" style="padding:var(--space-8); border-color: var(--color-aubergine); background: var(--color-surface-warm); position:relative;">
        <span style="position:absolute; top:-12px; left:var(--space-6); background: var(--color-aubergine); color: var(--color-creme); font-size: var(--text-xs); padding: 4px 12px; border-radius: var(--radius-full); letter-spacing:0.08em;">Plan actuel</span>
        <p class="card__meta">Le plus choisi</p>
        <h3 class="card__title" style="font-size:var(--text-lg);">Suivi régulier</h3>
        <p style="font-family:var(--font-display); font-size:var(--text-2xl); margin-block:var(--space-3);">79 $<span style="font-size:var(--text-base); color:var(--color-text-muted);"> /mois</span></p>
        <p style="font-size:var(--text-xs); color:var(--color-text-muted); margin-bottom:var(--space-6);">+ 12 % par rencontre encaissée</p>
        <ul role="list" style="display:flex; flex-direction:column; gap:var(--space-2); font-size:var(--text-sm); margin-bottom:var(--space-6);">
          <li>✓ Rencontres illimitées</li>
          <li>✓ Visibilité annuaire</li>
          <li>✓ Audio asynchrone + gabarits</li>
          <li>✓ Trousse de trames complète</li>
          <li>✓ Pause auto & alertes charge</li>
        </ul>
        <button class="btn btn--primary" style="width:100%;" disabled>Plan actuel</button>
      </div>

      <div class="card" style="padding:var(--space-8);">
        <p class="card__meta">Pratique soutenue</p>
        <h3 class="card__title" style="font-size:var(--text-lg);">Maison &amp; supervision</h3>
        <p style="font-family:var(--font-display); font-size:var(--text-2xl); margin-block:var(--space-3);">149 $<span style="font-size:var(--text-base); color:var(--color-text-muted);"> /mois</span></p>
        <p style="font-size:var(--text-xs); color:var(--color-text-muted); margin-bottom:var(--space-6);">+ 9 % par rencontre encaissée</p>
        <ul role="list" style="display:flex; flex-direction:column; gap:var(--space-2); font-size:var(--text-sm); margin-bottom:var(--space-6);">
          <li>✓ Tout du plan régulier</li>
          <li>✓ Supervision mensuelle (groupe)</li>
          <li>✓ Mise en avant annuaire</li>
          <li>✓ API & exports avancés</li>
          <li>✓ Espace de travail dédié (visio)</li>
        </ul>
        <button class="btn btn--ghost" style="width:100%;">Passer à ce plan</button>
      </div>
    </div>

    <p style="text-align:center; margin-top:var(--space-12); font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm);">
      Vous traversez une période plus calme ? Vous pouvez mettre votre abonnement <a href="#" style="color:var(--color-rose-deep);">en pause jusqu'à 3 mois</a> sans perdre votre fiche annuaire.
    </p>
  </div>
</div>
'''


# =============================================================
# MES OFFRES — configuration des formats, durées, tarifs
# =============================================================
def mes_offres_body():
    return f'''
<div class="workspace">
  {praticien_sidebar("mes-offres.html")}
  <div class="workspace__content">
    <header class="workspace__header">
      <p style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-rose-deep);">Mes offres · ce que je propose</p>
      <h1>Vos formats, vos durées, vos tarifs.</h1>
      <p>Vous décidez de ce qui est offert, sous quelle durée, et à quel tarif. IVIA n'impose pas de grille — vous nommez ce qui correspond à votre pratique. Les personnes qui vous choisissent verront ces informations avant de réserver.</p>
    </header>

    <!-- Bandeau visibilité -->
    <div class="card card--warm" style="margin-bottom:var(--space-10); padding:var(--space-6); display:flex; align-items:center; gap:var(--space-5);">
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" style="color:var(--color-rose); flex-shrink:0;"><circle cx="12" cy="12" r="3"/><path d="M2 12 C 5 6, 19 6, 22 12 C 19 18, 5 18, 2 12 Z"/></svg>
      <div style="flex:1;">
        <p style="font-family:var(--font-display); font-size:var(--text-base);">Visible dans l'annuaire IVIA</p>
        <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-top:var(--space-1);">3 offres actives · dernière mise à jour le 12 avril 2026</p>
      </div>
      <label class="toggle" style="display:flex; align-items:center; gap:var(--space-2); cursor:pointer;">
        <input type="checkbox" checked style="position:absolute; opacity:0; pointer-events:none;">
        <span style="width:36px; height:20px; background:var(--color-aubergine); border-radius:10px; position:relative; transition:background 0.2s;">
          <span style="position:absolute; top:2px; right:2px; width:16px; height:16px; background:var(--color-creme); border-radius:50%;"></span>
        </span>
        <span style="font-size:var(--text-sm);">Visible</span>
      </label>
    </div>

    <!-- OFFRE 1 — Rappel 10 min (offert) -->
    <article class="card" style="padding:var(--space-8); margin-bottom:var(--space-6);">
      <div class="flex-between" style="flex-wrap:wrap; gap:var(--space-4); margin-bottom:var(--space-6);">
        <div>
          <p style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-rose-deep);">Premier contact · inclus</p>
          <h2 style="font-family:var(--font-display); font-size:var(--text-xl); margin-top:var(--space-1);">Rappel personnalisé · 10 min</h2>
          <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-top:var(--space-2); max-width:60ch;">
            Bref échange téléphonique offert après la lecture du résumé d'un audio asynchrone. Sert à décider, sans engagement, s'il y a lieu d'aller plus loin.
          </p>
        </div>
        <div style="text-align:right;">
          <p style="font-family:var(--font-display); font-size:var(--text-2xl); color:var(--color-mousse);">Offert</p>
          <p style="font-size:var(--text-xs); color:var(--color-text-muted);">inclus dans l'audio asynchrone</p>
        </div>
      </div>
      <div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:var(--space-4); padding-top:var(--space-5); border-top:1px solid var(--color-divider);">
        <div><p class="card__meta">Format</p><p style="font-family:var(--font-display); font-size:var(--text-base);">Téléphone</p></div>
        <div><p class="card__meta">Déclenchement</p><p style="font-family:var(--font-display); font-size:var(--text-base);">Après résumé audio</p></div>
        <div><p class="card__meta">Délai</p><p style="font-family:var(--font-display); font-size:var(--text-base);">48 h ouvr.</p></div>
        <div><p class="card__meta">Statut</p><p style="font-family:var(--font-display); font-size:var(--text-base); color:var(--color-mousse);">Actif</p></div>
      </div>
      <div style="margin-top:var(--space-5); display:flex; gap:var(--space-3);">
        <button class="btn btn--ghost btn--sm">Modifier le descriptif</button>
      </div>
    </article>

    <!-- OFFRE 2 — Audio asynchrone -->
    <article class="card" style="padding:var(--space-8); margin-bottom:var(--space-6);">
      <div class="flex-between" style="flex-wrap:wrap; gap:var(--space-4); margin-bottom:var(--space-6);">
        <div>
          <p style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-rose-deep);">Écoute asynchrone</p>
          <h2 style="font-family:var(--font-display); font-size:var(--text-xl); margin-top:var(--space-1);">Audio asynchrone · jusqu'à 45 min</h2>
          <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-top:var(--space-2); max-width:60ch;">
            La personne enregistre librement, vous l'écoutez à votre rythme, vous répondez par écrit. Comprend le résumé écrit et le rappel 10 min.
          </p>
        </div>
        <div style="text-align:right;">
          <label style="font-size:var(--text-xs); color:var(--color-text-muted); display:block; margin-bottom:var(--space-1);">Tarif annoncé</label>
          <div style="display:flex; align-items:baseline; gap:4px; justify-content:flex-end;">
            <input type="number" value="45" min="0" step="5" style="width:80px; padding:var(--space-2) var(--space-3); font-family:var(--font-display); font-size:var(--text-2xl); text-align:right; background:var(--color-surface-warm); border:1px solid var(--color-divider); border-radius:var(--radius-sm);">
            <span style="font-family:var(--font-display); font-size:var(--text-2xl);">$</span>
          </div>
          <p style="font-size:var(--text-xs); color:var(--color-text-muted); margin-top:var(--space-1);">CAD · taxes en sus</p>
        </div>
      </div>
      <div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:var(--space-4); padding-top:var(--space-5); border-top:1px solid var(--color-divider);">
        <div>
          <label class="card__meta">Durée max audio</label>
          <select style="width:100%; margin-top:4px; padding:var(--space-2); background:var(--color-surface-warm); border:1px solid var(--color-divider); border-radius:var(--radius-sm); font-family:var(--font-display);"><option>15 min</option><option>30 min</option><option selected>45 min</option><option>60 min</option></select>
        </div>
        <div>
          <label class="card__meta">Délai réponse</label>
          <select style="width:100%; margin-top:4px; padding:var(--space-2); background:var(--color-surface-warm); border:1px solid var(--color-divider); border-radius:var(--radius-sm); font-family:var(--font-display);"><option>24 h</option><option selected>48 h</option><option>72 h</option><option>5 jours</option></select>
        </div>
        <div><p class="card__meta">Inclus</p><p style="font-family:var(--font-display); font-size:var(--text-sm); line-height:1.5;">Résumé écrit<br>Rappel 10 min</p></div>
        <div><p class="card__meta">Statut</p><p style="font-family:var(--font-display); font-size:var(--text-base); color:var(--color-mousse);">Actif</p></div>
      </div>
      <div style="margin-top:var(--space-5); display:flex; gap:var(--space-3); flex-wrap:wrap;">
        <button class="btn btn--primary btn--sm">Enregistrer</button>
        <button class="btn btn--ghost btn--sm">Modifier le descriptif</button>
        <button class="btn btn--ghost btn--sm" style="color:var(--color-text-muted);">Mettre en pause</button>
      </div>
    </article>

    <!-- OFFRE 3 — Rencontre 30 min -->
    <article class="card" style="padding:var(--space-8); margin-bottom:var(--space-6);">
      <div class="flex-between" style="flex-wrap:wrap; gap:var(--space-4); margin-bottom:var(--space-6);">
        <div>
          <p style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-rose-deep);">Rencontre synchrone · demi-heure</p>
          <h2 style="font-family:var(--font-display); font-size:var(--text-xl); margin-top:var(--space-1);">Rencontre brève · 30 min</h2>
          <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-top:var(--space-2); max-width:60ch;">
            Rencontre directe par téléphone, visio ou présentiel. Format ajusté pour un point ciblé ou une suite légère.
          </p>
        </div>
        <div style="text-align:right;">
          <label style="font-size:var(--text-xs); color:var(--color-text-muted); display:block; margin-bottom:var(--space-1);">Tarif annoncé</label>
          <div style="display:flex; align-items:baseline; gap:4px; justify-content:flex-end;">
            <input type="number" value="45" min="0" step="5" style="width:80px; padding:var(--space-2) var(--space-3); font-family:var(--font-display); font-size:var(--text-2xl); text-align:right; background:var(--color-surface-warm); border:1px solid var(--color-divider); border-radius:var(--radius-sm);">
            <span style="font-family:var(--font-display); font-size:var(--text-2xl);">$</span>
          </div>
          <p style="font-size:var(--text-xs); color:var(--color-text-muted); margin-top:var(--space-1);">CAD · 90 $/h équivalent</p>
        </div>
      </div>
      <div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:var(--space-4); padding-top:var(--space-5); border-top:1px solid var(--color-divider);">
        <div>
          <label class="card__meta">Formats acceptés</label>
          <div style="display:flex; gap:var(--space-2); margin-top:var(--space-2); flex-wrap:wrap;">
            <span class="chip" style="background:var(--color-aubergine); color:var(--color-creme);">Visio</span>
            <span class="chip" style="background:var(--color-aubergine); color:var(--color-creme);">Téléphone</span>
            <span class="chip" style="opacity:0.4;">Présentiel</span>
          </div>
        </div>
        <div><p class="card__meta">Plage horaire</p><p style="font-family:var(--font-display); font-size:var(--text-sm);">Lun — jeu<br>9 h — 16 h</p></div>
        <div><p class="card__meta">Annulation</p><p style="font-family:var(--font-display); font-size:var(--text-sm);">Gratuite jusqu'à 24 h</p></div>
        <div><p class="card__meta">Statut</p><p style="font-family:var(--font-display); font-size:var(--text-base); color:var(--color-mousse);">Actif</p></div>
      </div>
      <div style="margin-top:var(--space-5); display:flex; gap:var(--space-3); flex-wrap:wrap;">
        <button class="btn btn--primary btn--sm">Enregistrer</button>
        <button class="btn btn--ghost btn--sm">Modifier le descriptif</button>
      </div>
    </article>

    <!-- OFFRE 4 — Rencontre 60 min -->
    <article class="card" style="padding:var(--space-8); margin-bottom:var(--space-6);">
      <div class="flex-between" style="flex-wrap:wrap; gap:var(--space-4); margin-bottom:var(--space-6);">
        <div>
          <p style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-rose-deep);">Rencontre synchrone · heure complète</p>
          <h2 style="font-family:var(--font-display); font-size:var(--text-xl); margin-top:var(--space-1);">Rencontre approfondie · 60 min</h2>
          <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-top:var(--space-2); max-width:60ch;">
            Format standard pour un travail de fond. Le rythme et la profondeur se posent. Convient aux suivis réguliers comme aux premières rencontres approfondies.
          </p>
        </div>
        <div style="text-align:right;">
          <label style="font-size:var(--text-xs); color:var(--color-text-muted); display:block; margin-bottom:var(--space-1);">Tarif annoncé</label>
          <div style="display:flex; align-items:baseline; gap:4px; justify-content:flex-end;">
            <input type="number" value="60" min="0" step="5" style="width:80px; padding:var(--space-2) var(--space-3); font-family:var(--font-display); font-size:var(--text-2xl); text-align:right; background:var(--color-surface-warm); border:1px solid var(--color-divider); border-radius:var(--radius-sm);">
            <span style="font-family:var(--font-display); font-size:var(--text-2xl);">$</span>
          </div>
          <p style="font-size:var(--text-xs); color:var(--color-text-muted); margin-top:var(--space-1);">CAD · 60 $/h</p>
        </div>
      </div>
      <div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:var(--space-4); padding-top:var(--space-5); border-top:1px solid var(--color-divider);">
        <div>
          <label class="card__meta">Formats acceptés</label>
          <div style="display:flex; gap:var(--space-2); margin-top:var(--space-2); flex-wrap:wrap;">
            <span class="chip" style="background:var(--color-aubergine); color:var(--color-creme);">Visio</span>
            <span class="chip" style="background:var(--color-aubergine); color:var(--color-creme);">Téléphone</span>
            <span class="chip" style="background:var(--color-aubergine); color:var(--color-creme);">Présentiel</span>
          </div>
        </div>
        <div><p class="card__meta">Plage horaire</p><p style="font-family:var(--font-display); font-size:var(--text-sm);">Lun — ven<br>9 h — 18 h</p></div>
        <div><p class="card__meta">Annulation</p><p style="font-family:var(--font-display); font-size:var(--text-sm);">Gratuite jusqu'à 24 h</p></div>
        <div><p class="card__meta">Statut</p><p style="font-family:var(--font-display); font-size:var(--text-base); color:var(--color-mousse);">Actif</p></div>
      </div>
      <div style="margin-top:var(--space-5); display:flex; gap:var(--space-3); flex-wrap:wrap;">
        <button class="btn btn--primary btn--sm">Enregistrer</button>
        <button class="btn btn--ghost btn--sm">Modifier le descriptif</button>
      </div>
    </article>

    <!-- Ajouter une offre -->
    <button class="btn btn--ghost" style="width:100%; padding:var(--space-6); border-style:dashed; margin-bottom:var(--space-12);">+ Ajouter un format (atelier, suivi, accompagnement long)</button>

    <!-- Voies que j'accueille -->
    <h2 style="font-family:var(--font-display); font-size:var(--text-lg); margin-bottom:var(--space-4);">Voies que j'accueille</h2>
    <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-bottom:var(--space-6); max-width:60ch;">
      Les voies sont les portes d'entrée que vous reconnaissez dans votre pratique. Elles servent à orienter les demandes — pas à enfermer la rencontre.
    </p>
    <div class="card" style="padding:var(--space-6); margin-bottom:var(--space-12);">
      <div style="display:flex; gap:var(--space-3); flex-wrap:wrap;">
        <span class="chip" style="background:var(--color-aubergine); color:var(--color-creme); padding: 6px 14px;">Voie Sommeil <button style="background:none; border:none; color:var(--color-creme); margin-left:6px; cursor:pointer; opacity:0.7;">×</button></span>
        <span class="chip" style="background:var(--color-aubergine); color:var(--color-creme); padding: 6px 14px;">Voie Fréquence <button style="background:none; border:none; color:var(--color-creme); margin-left:6px; cursor:pointer; opacity:0.7;">×</button></span>
        <button class="chip" style="background:transparent; border:1px dashed var(--color-divider); padding: 6px 14px; cursor:pointer;">+ Ajouter une voie</button>
      </div>
    </div>

    <!-- Politique tarifaire personnelle -->
    <h2 style="font-family:var(--font-display); font-size:var(--text-lg); margin-bottom:var(--space-4);">Politique tarifaire personnelle</h2>
    <div class="card" style="padding:var(--space-8);">
      <div style="display:flex; flex-direction:column; gap:var(--space-5);">
        <label style="display:flex; gap:var(--space-3); align-items:flex-start; cursor:pointer;">
          <input type="checkbox" checked style="margin-top:4px;">
          <div>
            <p style="font-family:var(--font-display); font-size:var(--text-base);">Tarif solidaire · 1 créneau par semaine à 30 $</p>
            <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-top:var(--space-1);">Réservé aux personnes en précarité déclarée. Visible sur votre fiche annuaire.</p>
          </div>
        </label>
        <label style="display:flex; gap:var(--space-3); align-items:flex-start; cursor:pointer;">
          <input type="checkbox" style="margin-top:4px;">
          <div>
            <p style="font-family:var(--font-display); font-size:var(--text-base);">Première rencontre 50 % — découverte</p>
            <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-top:var(--space-1);">Une seule fois par personne. Active sur la 60 min uniquement.</p>
          </div>
        </label>
        <label style="display:flex; gap:var(--space-3); align-items:flex-start; cursor:pointer;">
          <input type="checkbox" checked style="margin-top:4px;">
          <div>
            <p style="font-family:var(--font-display); font-size:var(--text-base);">Réglage automatique selon la charge</p>
            <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-top:var(--space-1);">Quand votre semaine dépasse la cible, IVIA met les nouvelles demandes en file plutôt que d'augmenter votre tarif. Pas de tarification dynamique sans votre accord.</p>
          </div>
        </label>
      </div>
    </div>

    <!-- Aperçu côté client -->
    <div class="card card--warm" style="margin-top:var(--space-12); padding:var(--space-6); display:flex; gap:var(--space-5); align-items:center; flex-wrap:wrap;">
      <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" style="color:var(--color-rose); flex-shrink:0;"><circle cx="12" cy="12" r="3"/><path d="M2 12 C 5 6, 19 6, 22 12 C 19 18, 5 18, 2 12 Z"/></svg>
      <div style="flex:1; min-width:200px;">
        <p style="font-family:var(--font-display); font-size:var(--text-base);">Voir comment mes offres apparaissent</p>
        <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-top:var(--space-1);">Visualisez votre fiche côté personne accompagnée avant de publier vos changements.</p>
      </div>
      <a href="../client/choix-praticien.html" class="btn btn--ghost btn--sm" target="_blank" rel="noopener">Aperçu annuaire ↗</a>
    </div>
  </div>
</div>
'''


def build():
    pages = [
        ("index.html",         "Tableau de bord — Espace praticien IVIA",  "Vue d'ensemble : agenda du jour, audios à traiter, repères de pratique.", index_body()),
        ("agenda.html",        "Agenda — Espace praticien IVIA",           "Vue hebdomadaire de l'agenda praticien.",                              agenda_body()),
        ("audios.html",        "Audios à traiter — Espace praticien IVIA", "File d'audios reçus en attente de réponse.",                          audios_body()),
        ("mes-offres.html",    "Mes offres — Espace praticien IVIA",       "Configuration des formats, durées et tarifs proposés aux personnes écoutées.", mes_offres_body()),
        ("audio-traiter.html", "Répondre à un audio — Espace praticien IVIA", "Écran d'écoute et rédaction de réponse à un audio asynchrone.",   audio_traiter_body()),
        ("clients.html",       "Mes clients — Espace praticien IVIA",      "Annuaire interne des personnes accompagnées.",                         clients_body()),
        ("outils.html",        "Mes outils — Espace praticien IVIA",       "Trames d'écoute, modèles de réponse, ressources à partager.",         outils_body()),
        ("abonnement.html",    "Mon abonnement — Espace praticien IVIA",   "Plans d'abonnement praticien IVIA.",                                   abonnement_body()),
    ]
    for filename, title, description, body in pages:
        html = page(title, description, PRATICIEN_NAV, filename, PRATICIEN_ACTIONS, body, "index.html", FOOTER_INTERNE, css_extra=WORKSPACE_CSS)
        (OUT / filename).write_text(html, encoding="utf-8")

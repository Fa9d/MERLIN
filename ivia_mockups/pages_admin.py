"""Pages côté admin — pilotage maison IVIA."""
from pathlib import Path
from build_pages import page, ADMIN_NAV, ADMIN_ACTIONS, FOOTER_INTERNE
from pages_praticien import WORKSPACE_CSS

OUT = Path(__file__).parent / "admin"


def admin_sidebar(active):
    items = [
        ("index.html",      "Vue d'ensemble", None,  "M3 12 L 12 3 L 21 12 M5 10 V 21 H 19 V 10"),
        ("analytique.html", "Analytique",     None,  "M3 21 V 3 M3 21 H 21 M 7 16 V 11 M 11 16 V 8 M 15 16 V 13 M 19 16 V 6"),
        ("praticiens.html", "Praticien·ne·s", "1",   "M9 11 A 4 4 0 1 0 9 3 A 4 4 0 0 0 9 11 Z M2 21 V 19 A 5 5 0 0 1 7 14 H 11 A 5 5 0 0 1 16 19 V 21"),
        ("clients.html",    "Clients",        None,  "M16 11 A 4 4 0 1 0 16 3 A 4 4 0 0 0 16 11 Z M8 11 A 3 3 0 1 0 8 5 A 3 3 0 0 0 8 11 Z"),
        ("audios.html",     "Audios",         None,  "M12 3 V 19 M5 9 V 13 M9 6 V 16 M15 7 V 15 M19 9 V 13"),
        ("finance.html",    "Finance",        None,  "M3 12 H 21 M 6 6 L 12 12 L 18 6 M 6 18 L 12 12 L 18 18"),
        ("parametres.html", "Paramètres",     None,  "M12 8 A 4 4 0 1 1 12 16 A 4 4 0 0 1 12 8 Z"),
    ]
    rows = []
    for href, label, badge, path in items:
        cur = ' aria-current="page"' if href == active else ""
        bdg = f'<span class="badge">{badge}</span>' if badge else ""
        icon = f'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="{path}"/></svg>'
        rows.append(f'<a href="{href}"{cur}>{icon}<span>{label}</span>{bdg}</a>')
    return f'<aside class="sidebar" aria-label="Navigation admin"><h4>Maison IVIA · pilotage</h4>{"".join(rows)}<h4 style="margin-top:var(--space-12);">Compte</h4><a href="#"><div style="width:24px; height:24px; border-radius:50%; background:var(--color-aubergine);"></div><span>Admin · D. Phaneuf</span></a></aside>'


# =============================================================
# INDEX admin
# =============================================================
def index_body():
    return f'''
<div class="workspace">
  {admin_sidebar("index.html")}
  <div class="workspace__content">
    <header class="workspace__header">
      <p style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-rose-deep);">Samedi 9 mai 2026</p>
      <h1>Vue d'ensemble — IVIA Maison</h1>
      <p>La maison fonctionne. Une demande de praticienne en attente, deux signalements vigilance à examiner, finance dans les clous.</p>
    </header>

    <div class="kpi-grid">
      <div class="kpi"><p class="kpi__label">Praticien·ne·s actif·ve·s</p><p class="kpi__value">23</p><p class="kpi__delta">+1 ce mois</p></div>
      <div class="kpi"><p class="kpi__label">Clients accompagnés (90 j)</p><p class="kpi__value">412</p><p class="kpi__delta">+38 vs trimestre précédent</p></div>
      <div class="kpi"><p class="kpi__label">Rencontres ce mois</p><p class="kpi__value">681</p><p class="kpi__delta">Moyenne hebdo : 170</p></div>
      <div class="kpi"><p class="kpi__label">Audios reçus (90 j)</p><p class="kpi__value">189</p><p class="kpi__delta">Conversion appel court : 64 %</p></div>
      <div class="kpi"><p class="kpi__label">Revenus mensuels (estimé)</p><p class="kpi__value">71 200 $</p><p class="kpi__delta">+8 % vs mois passé</p></div>
      <div class="kpi"><p class="kpi__label">NPS clients (90 j)</p><p class="kpi__value">+62</p><p class="kpi__delta">Stable</p></div>
    </div>

    <div class="grid" style="grid-template-columns: 1.5fr 1fr; gap:var(--space-8);">
      <div>
        <h2 style="font-family:var(--font-display); font-size:var(--text-lg); margin-bottom:var(--space-4);">À traiter aujourd'hui</h2>

        <div class="stack">
          <article class="card">
            <div class="flex-between">
              <div>
                <p style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-rose-deep);">Nouvelle candidature</p>
                <h3 class="card__title" style="font-size:var(--text-base); margin-top:var(--space-1);">Karim B.-S. — Voie Connaissance</h3>
                <p style="font-size:var(--text-xs); color:var(--color-text-muted); margin-top:var(--space-2);">Reçu le 7 mai · entretien à planifier</p>
              </div>
              <a href="praticiens.html" class="btn btn--primary btn--sm">Examiner</a>
            </div>
          </article>

          <article class="card" style="border-color: var(--color-rose);">
            <div class="flex-between">
              <div>
                <p style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-rose-deep);">⚠ Signalement vigilance</p>
                <h3 class="card__title" style="font-size:var(--text-base); margin-top:var(--space-1);">Sujet : « pleurs sans raison » · Camille T.</h3>
                <p style="font-size:var(--text-xs); color:var(--color-text-muted); margin-top:var(--space-2);">Maïté L.-T. a noté le repère vigilance dans une réponse audio. Nature : non urgente, à suivre.</p>
              </div>
              <button class="btn btn--ghost btn--sm">Lire le contexte</button>
            </div>
          </article>

          <article class="card">
            <div class="flex-between">
              <div>
                <p style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-rose-deep);">Audio sans praticien·ne attribué·e</p>
                <h3 class="card__title" style="font-size:var(--text-base); margin-top:var(--space-1);">Audio reçu il y a 18 h</h3>
                <p style="font-size:var(--text-xs); color:var(--color-text-muted); margin-top:var(--space-2);">Échéance d'attribution : sous 6 h pour respecter le délai de réponse de 48 h.</p>
              </div>
              <a href="audios.html" class="btn btn--primary btn--sm">Attribuer</a>
            </div>
          </article>

          <article class="card" style="opacity:0.85;">
            <div class="flex-between">
              <div>
                <p style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-text-muted);">Charge praticienne</p>
                <h3 class="card__title" style="font-size:var(--text-base); margin-top:var(--space-1);">Soraya B.-A. : 6<sup>e</sup> sem. au-dessus de la charge cible</h3>
                <p style="font-size:var(--text-xs); color:var(--color-text-muted); margin-top:var(--space-2);">Suggestion : proposer une pause de 7 jours et redistribuer 4 nouvelles demandes.</p>
              </div>
              <button class="btn btn--ghost btn--sm">Examiner</button>
            </div>
          </article>
        </div>

        <h2 style="font-family:var(--font-display); font-size:var(--text-lg); margin-block: var(--space-12) var(--space-4);">Activité de la semaine</h2>
        <div class="card" style="padding:var(--space-6);">
          <p style="font-family:var(--font-serif); color:var(--color-text-muted); margin-bottom:var(--space-4); font-size:var(--text-sm);">
            Rencontres effectuées par jour
          </p>
          <!-- Mini graphe SVG inline -->
          <svg viewBox="0 0 600 160" style="width:100%; height:auto; max-width:none;">
            <defs>
              <linearGradient id="bar-grad" x1="0" x2="0" y1="0" y2="1">
                <stop offset="0%" stop-color="#C58A8A" stop-opacity="0.9"/>
                <stop offset="100%" stop-color="#C58A8A" stop-opacity="0.3"/>
              </linearGradient>
            </defs>
            ''' + "".join(f'<rect x="{40+i*75}" y="{160-h}" width="40" height="{h}" rx="4" fill="url(#bar-grad)"/>' for i, h in enumerate([90, 110, 75, 130, 105, 50, 30])) + '''
            ''' + "".join(f'<text x="{60+i*75}" y="155" text-anchor="middle" font-family="Inter" font-size="10" fill="#6E5F71">{label}</text>' for i, label in enumerate(["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"])) + '''
          </svg>
        </div>
      </div>

      <aside>
        <div class="card card--warm">
          <p class="card__meta">Voies — répartition (90 j)</p>
          <div style="display:flex; flex-direction:column; gap:var(--space-3); margin-top:var(--space-4);">
            <div>
              <div class="flex-between" style="margin-bottom:4px;"><span style="font-size:var(--text-sm);">Fréquence</span><span style="font-size:var(--text-xs); color:var(--color-text-muted);">38 %</span></div>
              <div style="height:6px; background:var(--color-divider); border-radius:3px; overflow:hidden;"><div style="width:38%; height:100%; background:var(--color-mousse);"></div></div>
            </div>
            <div>
              <div class="flex-between" style="margin-bottom:4px;"><span style="font-size:var(--text-sm);">Sommeil</span><span style="font-size:var(--text-xs); color:var(--color-text-muted);">31 %</span></div>
              <div style="height:6px; background:var(--color-divider); border-radius:3px; overflow:hidden;"><div style="width:31%; height:100%; background:var(--color-glacier);"></div></div>
            </div>
            <div>
              <div class="flex-between" style="margin-bottom:4px;"><span style="font-size:var(--text-sm);">Connaissance</span><span style="font-size:var(--text-xs); color:var(--color-text-muted);">19 %</span></div>
              <div style="height:6px; background:var(--color-divider); border-radius:3px; overflow:hidden;"><div style="width:19%; height:100%; background:var(--color-lavande);"></div></div>
            </div>
            <div>
              <div class="flex-between" style="margin-bottom:4px;"><span style="font-size:var(--text-sm);">Famille</span><span style="font-size:var(--text-xs); color:var(--color-text-muted);">12 %</span></div>
              <div style="height:6px; background:var(--color-divider); border-radius:3px; overflow:hidden;"><div style="width:12%; height:100%; background:var(--color-rose);"></div></div>
            </div>
          </div>
        </div>

        <div class="card" style="margin-top:var(--space-4);">
          <p class="card__meta">Maison · état du fil</p>
          <ul role="list" style="display:flex; flex-direction:column; gap:var(--space-3); font-size:var(--text-sm); margin-top:var(--space-3);">
            <li class="flex" style="align-items:flex-start;"><span class="status-dot status-dot--ok" style="margin-top:5px; flex-shrink:0;"></span><span>Tous les services en ligne (api, app, audio)</span></li>
            <li class="flex" style="align-items:flex-start;"><span class="status-dot status-dot--ok" style="margin-top:5px; flex-shrink:0;"></span><span>Déploiement INFRA-005 réussi · 9 mai 06 h 13</span></li>
            <li class="flex" style="align-items:flex-start;"><span class="status-dot status-dot--pending" style="margin-top:5px; flex-shrink:0;"></span><span>Migration UI v2 « La Coupe » en cours</span></li>
            <li class="flex" style="align-items:flex-start;"><span class="status-dot status-dot--alert" style="margin-top:5px; flex-shrink:0;"></span><span>Bug 405 actif : POST /register/client</span></li>
          </ul>
        </div>
      </aside>
    </div>
  </div>
</div>
'''


# =============================================================
# PRATICIENS — admin
# =============================================================
def praticiens_body():
    return f'''
<div class="workspace">
  {admin_sidebar("praticiens.html")}
  <div class="workspace__content">
    <header class="workspace__header">
      <h1>Praticien·ne·s</h1>
      <p>23 actif·ve·s · 1 candidature en cours · 1 en pause volontaire (3 mois). Charge moyenne : 14 rencontres/sem.</p>
    </header>

    <div class="cluster" style="margin-bottom:var(--space-6);">
      <span class="chip chip--rose">Tous (24)</span>
      <span class="chip">Actifs (23)</span>
      <span class="chip">Candidatures (1)</span>
      <span class="chip">En pause (1)</span>
      <span class="chip">Charge élevée (3)</span>
    </div>

    <!-- Candidature en cours -->
    <div class="card" style="background: color-mix(in oklab, var(--color-miel) 12%, var(--color-creme)); border-color: var(--color-miel); margin-bottom:var(--space-8);">
      <div class="flex-between" style="flex-wrap:wrap; gap:var(--space-4);">
        <div>
          <p class="card__meta" style="color: #8B6A22;">Nouvelle candidature · à examiner</p>
          <h3 class="card__title">Karim Benhamou-Soltani</h3>
          <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); max-width:50ch;">
            Voie principale : Connaissance · Voie secondaire : Famille · Montréal · DEC en intervention sociale + 8 ans de pratique en travail communautaire.
          </p>
        </div>
        <div class="flex">
          <button class="btn btn--ghost btn--sm">Voir le dossier</button>
          <button class="btn btn--ghost btn--sm">Planifier l'entretien</button>
          <button class="btn btn--primary btn--sm">Approuver</button>
        </div>
      </div>
    </div>

    <div class="card" style="padding:0; overflow:hidden;">
      <table class="data-table">
        <thead>
          <tr><th>Nom</th><th>Voies</th><th>Plan</th><th>Charge (sem.)</th><th>Note maison</th><th>Statut</th><th></th></tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Maïté Lavoie-Therrien</strong><br><span style="font-size:var(--text-xs); color:var(--color-text-muted);">Montréal</span></td>
            <td><span class="chip chip--mousse">Fréquence</span> <span class="chip chip--glacier">Sommeil</span></td>
            <td>Suivi régulier</td>
            <td>14 rencontres</td>
            <td>4,8 / 5</td>
            <td><span class="status-dot status-dot--ok"></span> Active</td>
            <td><button class="btn btn--ghost btn--sm">Fiche</button></td>
          </tr>
          <tr>
            <td><strong>Étienne Grondin-Côté</strong><br><span style="font-size:var(--text-xs); color:var(--color-text-muted);">Québec</span></td>
            <td><span class="chip chip--lavande">Connaissance</span></td>
            <td>Maison & supervision</td>
            <td>16 rencontres</td>
            <td>4,7 / 5</td>
            <td><span class="status-dot status-dot--ok"></span> Active</td>
            <td><button class="btn btn--ghost btn--sm">Fiche</button></td>
          </tr>
          <tr style="background: color-mix(in oklab, var(--color-rose) 10%, transparent);">
            <td><strong>Soraya Ben-Amar</strong><br><span style="font-size:var(--text-xs); color:var(--color-text-muted);">Sherbrooke</span></td>
            <td><span class="chip chip--mousse">Fréquence</span> <span class="chip chip--rose">Famille</span></td>
            <td>Suivi régulier</td>
            <td><strong style="color:var(--color-rose-deep);">22 ⚠</strong></td>
            <td>4,9 / 5</td>
            <td><span class="status-dot status-dot--alert"></span> Charge élevée</td>
            <td><button class="btn btn--primary btn--sm">Action</button></td>
          </tr>
          <tr>
            <td><strong>Marc-André Pelletier</strong><br><span style="font-size:var(--text-xs); color:var(--color-text-muted);">Trois-Rivières</span></td>
            <td><span class="chip chip--glacier">Sommeil</span> <span class="chip chip--lavande">Connaissance</span></td>
            <td>Suivi régulier</td>
            <td>11 rencontres</td>
            <td>4,6 / 5</td>
            <td><span class="status-dot status-dot--ok"></span> Active</td>
            <td><button class="btn btn--ghost btn--sm">Fiche</button></td>
          </tr>
          <tr>
            <td><strong>Nicole Tremblay-Roy</strong><br><span style="font-size:var(--text-xs); color:var(--color-text-muted);">Saguenay</span></td>
            <td><span class="chip chip--rose">Famille</span></td>
            <td>Suivi régulier</td>
            <td>12 rencontres</td>
            <td>4,8 / 5</td>
            <td><span class="status-dot status-dot--ok"></span> Active</td>
            <td><button class="btn btn--ghost btn--sm">Fiche</button></td>
          </tr>
          <tr>
            <td><strong>Jean-Philippe Côté</strong><br><span style="font-size:var(--text-xs); color:var(--color-text-muted);">Gatineau</span></td>
            <td><span class="chip chip--mousse">Fréquence</span> <span class="chip chip--glacier">Sommeil</span></td>
            <td>Découverte</td>
            <td>9 rencontres</td>
            <td>4,7 / 5</td>
            <td><span class="status-dot status-dot--ok"></span> Active</td>
            <td><button class="btn btn--ghost btn--sm">Fiche</button></td>
          </tr>
          <tr style="opacity:0.7;">
            <td><strong>François L.</strong><br><span style="font-size:var(--text-xs); color:var(--color-text-muted);">Lévis</span></td>
            <td><span class="chip chip--mousse">Fréquence</span></td>
            <td>Suivi régulier (en pause)</td>
            <td>—</td>
            <td>4,9 / 5</td>
            <td><span class="status-dot"></span> En pause (j 12/90)</td>
            <td><button class="btn btn--ghost btn--sm">Fiche</button></td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="flex" style="margin-top:var(--space-8); justify-content:flex-end;">
      <button class="btn btn--ghost">⤓ Exporter (CSV)</button>
      <button class="btn btn--primary">＋ Inviter un·e praticien·ne</button>
    </div>
  </div>
</div>
'''


# =============================================================
# CLIENTS admin
# =============================================================
def clients_body():
    return f'''
<div class="workspace">
  {admin_sidebar("clients.html")}
  <div class="workspace__content">
    <header class="workspace__header">
      <h1>Clients</h1>
      <p>412 personnes accompagnées (90 derniers jours). Données affichées à la maille agrégée — l'admin n'accède pas au contenu des notes ni des audios.</p>
    </header>

    <div class="kpi-grid">
      <div class="kpi"><p class="kpi__label">Total comptes</p><p class="kpi__value">847</p><p class="kpi__delta">+62 ce mois</p></div>
      <div class="kpi"><p class="kpi__label">Actifs (90 j)</p><p class="kpi__value">412</p><p class="kpi__delta">49 % du total</p></div>
      <div class="kpi"><p class="kpi__label">1<sup>re</sup> rencontre cette semaine</p><p class="kpi__value">11</p><p class="kpi__delta">Stable</p></div>
      <div class="kpi"><p class="kpi__label">Taux de retour ≥ 2 rencontres</p><p class="kpi__value">68 %</p><p class="kpi__delta">+4 pts</p></div>
    </div>

    <div class="cluster" style="margin-bottom:var(--space-6);">
      <span class="chip chip--rose">Tous</span>
      <span class="chip">Actifs (412)</span>
      <span class="chip">Inactifs (435)</span>
      <span class="chip">À recontacter (signalé)</span>
      <span class="chip">RGPD/Loi 25 — demandes (2)</span>
    </div>

    <div class="card" style="padding:0; overflow:hidden;">
      <table class="data-table">
        <thead><tr><th>Identifiant</th><th>Inscription</th><th>Rencontres</th><th>Audios</th><th>Praticien·ne attitré·e</th><th>État</th><th></th></tr></thead>
        <tbody>
          <tr>
            <td><strong>#IV-12783</strong><br><span style="font-size:var(--text-xs); color:var(--color-text-muted);">Camille T.</span></td>
            <td>28 avr 2026</td>
            <td>3</td>
            <td>4</td>
            <td>Maïté L.-T.</td>
            <td><span class="status-dot status-dot--ok"></span> En suivi</td>
            <td><button class="btn btn--ghost btn--sm">Profil</button></td>
          </tr>
          <tr>
            <td><strong>#IV-12791</strong><br><span style="font-size:var(--text-xs); color:var(--color-text-muted);">Olivier R.</span></td>
            <td>5 mai 2026</td>
            <td>0 (à venir)</td>
            <td>1</td>
            <td>Maïté L.-T.</td>
            <td><span class="status-dot status-dot--ok"></span> Nouveau</td>
            <td><button class="btn btn--ghost btn--sm">Profil</button></td>
          </tr>
          <tr>
            <td><strong>#IV-12774</strong><br><span style="font-size:var(--text-xs); color:var(--color-text-muted);">Léa B.</span></td>
            <td>20 avr 2026</td>
            <td>0</td>
            <td>2</td>
            <td>Maïté L.-T.</td>
            <td><span class="status-dot status-dot--pending"></span> Audio en attente</td>
            <td><button class="btn btn--ghost btn--sm">Profil</button></td>
          </tr>
          <tr>
            <td><strong>#IV-12640</strong><br><span style="font-size:var(--text-xs); color:var(--color-text-muted);">Anne P.</span></td>
            <td>15 mar 2026</td>
            <td>5</td>
            <td>0</td>
            <td>Maïté L.-T.</td>
            <td><span class="status-dot status-dot--ok"></span> En suivi</td>
            <td><button class="btn btn--ghost btn--sm">Profil</button></td>
          </tr>
          <tr style="opacity:0.85;">
            <td><strong>#IV-12388</strong></td>
            <td>2 fév 2026</td>
            <td>1</td>
            <td>0</td>
            <td>Étienne G.-C.</td>
            <td><span class="status-dot"></span> Inactif</td>
            <td><button class="btn btn--ghost btn--sm">Profil</button></td>
          </tr>
          <tr style="background: color-mix(in oklab, var(--color-miel) 10%, transparent);">
            <td><strong>#IV-12091</strong></td>
            <td>15 jan 2026</td>
            <td>0</td>
            <td>0</td>
            <td>Non attribué</td>
            <td><span class="status-dot status-dot--pending"></span> Demande Loi 25 (suppression)</td>
            <td><button class="btn btn--primary btn--sm">Traiter</button></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</div>
'''


# =============================================================
# AUDIOS admin
# =============================================================
def audios_body():
    return f'''
<div class="workspace">
  {admin_sidebar("audios.html")}
  <div class="workspace__content">
    <header class="workspace__header">
      <h1>Audios — vue d'ensemble</h1>
      <p>Suivi de la file d'audios asynchrones, des délais de réponse, et des cas non attribués.</p>
    </header>

    <div class="kpi-grid">
      <div class="kpi"><p class="kpi__label">En attente (tous prat.)</p><p class="kpi__value">14</p><p class="kpi__delta">Délai moyen restant : 22 h</p></div>
      <div class="kpi"><p class="kpi__label">Non attribués</p><p class="kpi__value">1</p><p class="kpi__delta kpi__delta--down">Échéance attribution dans 6 h</p></div>
      <div class="kpi"><p class="kpi__label">Délai de réponse médian</p><p class="kpi__value">28 h</p><p class="kpi__delta">Sous l'objectif de 48 h</p></div>
      <div class="kpi"><p class="kpi__label">Conv. audio → appel court</p><p class="kpi__value">64 %</p><p class="kpi__delta">+3 pts</p></div>
    </div>

    <h2 style="font-family:var(--font-display); font-size:var(--text-lg); margin-bottom:var(--space-4);">Audios non attribués</h2>
    <div class="card" style="background: color-mix(in oklab, var(--color-rose) 8%, var(--color-creme)); border-color:var(--color-rose);">
      <div class="flex-between" style="flex-wrap:wrap; gap:var(--space-4);">
        <div>
          <p class="card__meta" style="color:var(--color-rose-deep);">Audio reçu il y a 18 h</p>
          <h3 class="card__title">Compte #IV-12791 — 8 min 03 s</h3>
          <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm);">
            Voie demandée : à préciser · Région : Montréal · Audio d'arrivée d'un nouveau compte. Les praticiennes Maïté L.-T. et Soraya B.-A. correspondent au profil.
          </p>
        </div>
        <div class="flex">
          <button class="btn btn--ghost btn--sm">Réécouter (admin)</button>
          <button class="btn btn--primary btn--sm">Attribuer →</button>
        </div>
      </div>
    </div>

    <h2 style="font-family:var(--font-display); font-size:var(--text-lg); margin-block: var(--space-12) var(--space-4);">File globale</h2>
    <div class="card" style="padding:0; overflow:hidden;">
      <table class="data-table">
        <thead><tr><th>Compte</th><th>Reçu</th><th>Praticien·ne</th><th>Échéance réponse</th><th>Statut</th></tr></thead>
        <tbody>
          <tr><td>#IV-12783 (Camille T.)</td><td>9 mai · 14 h 22</td><td>Maïté L.-T.</td><td>11 mai · 14 h 22</td><td><span class="chip chip--miel">En écoute</span></td></tr>
          <tr><td>#IV-12774 (Léa B.)</td><td>8 mai · 11 h 17</td><td>Maïté L.-T.</td><td>10 mai · 11 h 17</td><td><span class="chip chip--miel">En écoute</span></td></tr>
          <tr><td>#IV-12791 (nouveau)</td><td>8 mai · 22 h 04</td><td>—</td><td>10 mai · 22 h 04</td><td><span class="chip" style="background: color-mix(in oklab, var(--color-error) 15%, var(--color-creme)); color: var(--color-error);">Non attribué</span></td></tr>
          <tr><td>#IV-12702</td><td>8 mai · 09 h 30</td><td>Étienne G.-C.</td><td>10 mai · 09 h 30</td><td><span class="chip chip--miel">En écoute</span></td></tr>
          <tr><td>#IV-12655</td><td>7 mai · 19 h 47</td><td>Soraya B.-A.</td><td>9 mai · 19 h 47</td><td><span class="chip chip--mousse">Réponse en rédaction</span></td></tr>
        </tbody>
      </table>
    </div>
  </div>
</div>
'''


# =============================================================
# FINANCE admin
# =============================================================
def finance_body():
    return f'''
<div class="workspace">
  {admin_sidebar("finance.html")}
  <div class="workspace__content">
    <header class="workspace__header">
      <h1>Finance</h1>
      <p>Vue exécutive sur revenus, commissions, abonnements, reversements praticien·ne·s. Données arrondies au dollar.</p>
    </header>

    <div class="kpi-grid">
      <div class="kpi"><p class="kpi__label">Revenu mois en cours</p><p class="kpi__value">71 200 $</p><p class="kpi__delta">+8 % vs avr.</p></div>
      <div class="kpi"><p class="kpi__label">À reverser (mai)</p><p class="kpi__value">53 880 $</p><p class="kpi__delta">76 % du revenu</p></div>
      <div class="kpi"><p class="kpi__label">Commission maison</p><p class="kpi__value">15 500 $</p><p class="kpi__delta">12 % moyen</p></div>
      <div class="kpi"><p class="kpi__label">Abonnements actifs</p><p class="kpi__value">23</p><p class="kpi__delta">1 820 $/mois récurrent</p></div>
      <div class="kpi"><p class="kpi__label">Trésorerie (60 j)</p><p class="kpi__value">186 400 $</p><p class="kpi__delta">Marge de 4,2 mois</p></div>
      <div class="kpi"><p class="kpi__label">Coût par client acquis</p><p class="kpi__value">17 $</p><p class="kpi__delta">Stable</p></div>
    </div>

    <h2 style="font-family:var(--font-display); font-size:var(--text-lg); margin-bottom:var(--space-4);">Revenus 6 derniers mois</h2>
    <div class="card" style="padding:var(--space-6);">
      <svg viewBox="0 0 600 200" style="width:100%; height:auto;">
        <defs>
          <linearGradient id="line-grad" x1="0" x2="0" y1="0" y2="1">
            <stop offset="0%" stop-color="#6B8266" stop-opacity="0.4"/>
            <stop offset="100%" stop-color="#6B8266" stop-opacity="0"/>
          </linearGradient>
        </defs>
        <!-- aire -->
        <path d="M 30 150 L 120 130 L 210 110 L 300 95 L 390 80 L 480 60 L 570 40 L 570 200 L 30 200 Z" fill="url(#line-grad)"/>
        <!-- ligne -->
        <path d="M 30 150 L 120 130 L 210 110 L 300 95 L 390 80 L 480 60 L 570 40" stroke="#6B8266" stroke-width="2" fill="none"/>
        <!-- points -->
        ''' + "".join(f'<circle cx="{30+i*90}" cy="{y}" r="4" fill="#6B8266"/>' for i, y in enumerate([150, 130, 110, 95, 80, 60, 40])) + '''
        <!-- labels -->
        ''' + "".join(f'<text x="{30+i*90}" y="195" text-anchor="middle" font-family="Inter" font-size="11" fill="#6E5F71">{m}</text>' for i, m in enumerate(["Nov", "Déc", "Jan", "Fév", "Mar", "Avr", "Mai"])) + '''
        ''' + "".join(f'<text x="{30+i*90}" y="{y-12}" text-anchor="middle" font-family="Fraunces" font-size="11" fill="#2A1F2D">{v}</text>' for i, (y, v) in enumerate(zip([150, 130, 110, 95, 80, 60, 40], ["38k", "44k", "51k", "57k", "62k", "66k", "71k"]))) + '''
      </svg>
    </div>

    <h2 style="font-family:var(--font-display); font-size:var(--text-lg); margin-block: var(--space-12) var(--space-4);">Reversements praticien·ne·s — Mai (à valider)</h2>
    <div class="card" style="padding:0; overflow:hidden;">
      <table class="data-table">
        <thead><tr><th>Praticien·ne</th><th>Rencontres</th><th>Brut</th><th>Comm.</th><th>Net à verser</th><th>Statut</th></tr></thead>
        <tbody>
          <tr><td><strong>Maïté Lavoie-Therrien</strong></td><td>56</td><td>5 320 $</td><td>− 638 $ (12 %)</td><td><strong>4 682 $</strong></td><td><span class="chip chip--mousse">Prêt</span></td></tr>
          <tr><td><strong>Étienne Grondin-Côté</strong></td><td>62</td><td>5 890 $</td><td>− 530 $ (9 %)</td><td><strong>5 360 $</strong></td><td><span class="chip chip--mousse">Prêt</span></td></tr>
          <tr><td><strong>Soraya Ben-Amar</strong></td><td>78</td><td>7 410 $</td><td>− 889 $ (12 %)</td><td><strong>6 521 $</strong></td><td><span class="chip chip--miel">Bonus charge à appliquer</span></td></tr>
          <tr><td><strong>Marc-André Pelletier</strong></td><td>44</td><td>4 180 $</td><td>− 502 $ (12 %)</td><td><strong>3 678 $</strong></td><td><span class="chip chip--mousse">Prêt</span></td></tr>
          <tr><td><strong>Nicole Tremblay-Roy</strong></td><td>48</td><td>4 560 $</td><td>− 547 $ (12 %)</td><td><strong>4 013 $</strong></td><td><span class="chip chip--mousse">Prêt</span></td></tr>
          <tr><td><strong>Jean-Philippe Côté</strong></td><td>36</td><td>3 420 $</td><td>− 513 $ (15 %)</td><td><strong>2 907 $</strong></td><td><span class="chip chip--mousse">Prêt</span></td></tr>
        </tbody>
      </table>
    </div>

    <div class="flex" style="margin-top:var(--space-6); justify-content:flex-end; flex-wrap:wrap;">
      <button class="btn btn--ghost">⤓ Export Excel (compta)</button>
      <button class="btn btn--ghost">Aperçu virements</button>
      <button class="btn btn--primary">Valider tous les reversements →</button>
    </div>
  </div>
</div>
'''


# =============================================================
# PARAMÈTRES admin
# =============================================================
def parametres_body():
    return f'''
<div class="workspace">
  {admin_sidebar("parametres.html")}
  <div class="workspace__content">
    <header class="workspace__header">
      <h1>Paramètres</h1>
      <p>Configuration de la maison IVIA. Toute modification est journalisée et visible dans l'historique des décisions.</p>
    </header>

    <div data-tabs>
      <div role="tablist" style="display:flex; gap:var(--space-2); border-bottom:1px solid var(--color-divider); margin-bottom:var(--space-8);">
        <button role="tab" data-target="tab-general" aria-selected="true" style="padding:var(--space-3) var(--space-5); border:none; background:none; cursor:pointer; border-bottom:2px solid var(--color-aubergine); font-family:var(--font-display); color:var(--color-text);">Général</button>
        <button role="tab" data-target="tab-doctrine" aria-selected="false" style="padding:var(--space-3) var(--space-5); border:none; background:none; cursor:pointer; border-bottom:2px solid transparent; font-family:var(--font-display); color:var(--color-text-muted);">Doctrine & cadre</button>
        <button role="tab" data-target="tab-tarifs" aria-selected="false" style="padding:var(--space-3) var(--space-5); border:none; background:none; cursor:pointer; border-bottom:2px solid transparent; font-family:var(--font-display); color:var(--color-text-muted);">Tarifs & abonnements</button>
        <button role="tab" data-target="tab-loi25" aria-selected="false" style="padding:var(--space-3) var(--space-5); border:none; background:none; cursor:pointer; border-bottom:2px solid transparent; font-family:var(--font-display); color:var(--color-text-muted);">Loi 25 & sécurité</button>
        <button role="tab" data-target="tab-equipe" aria-selected="false" style="padding:var(--space-3) var(--space-5); border:none; background:none; cursor:pointer; border-bottom:2px solid transparent; font-family:var(--font-display); color:var(--color-text-muted);">Équipe maison</button>
      </div>

      <div id="tab-general" role="tabpanel">
        <div class="grid grid-2" style="gap:var(--space-6);">
          <div class="card">
            <h3 style="font-family:var(--font-display); font-size:var(--text-base); margin-bottom:var(--space-4);">Identité</h3>
            <div class="stack">
              <div class="field"><label>Nom de la maison</label><input type="text" value="IVIA — IN VIVO IN ACTU"></div>
              <div class="field"><label>Devise principale</label><input type="text" value="Au sein de l'être — En actes."></div>
              <div class="field"><label>Devise secondaire</label><input type="text" value="Pour le peuple, par le peuple."></div>
            </div>
          </div>
          <div class="card">
            <h3 style="font-family:var(--font-display); font-size:var(--text-base); margin-bottom:var(--space-4);">Contact public</h3>
            <div class="stack">
              <div class="field"><label>Courriel maison</label><input type="text" value="bonjour@ivia.quebec"></div>
              <div class="field"><label>Téléphone (réception)</label><input type="text" value="+1 514 555 0420"></div>
              <div class="field"><label>Adresse</label><input type="text" value="Montréal, Québec, Canada"></div>
            </div>
          </div>
          <div class="card">
            <h3 style="font-family:var(--font-display); font-size:var(--text-base); margin-bottom:var(--space-4);">Apparence du site public</h3>
            <div class="stack">
              <div class="field">
                <label>Identité graphique active</label>
                <select><option>La Coupe (V2 — actuelle)</option><option disabled>V1 minéral (obsolète)</option></select>
              </div>
              <div class="field">
                <label>Mode Calme par défaut pour visiteurs sensibles</label>
                <select><option>Activé si reduced-motion détecté</option><option>Toujours activé</option><option>Manuel uniquement</option></select>
              </div>
            </div>
          </div>
          <div class="card">
            <h3 style="font-family:var(--font-display); font-size:var(--text-base); margin-bottom:var(--space-4);">Délais & SLA</h3>
            <div class="stack">
              <div class="field"><label>Délai max de réponse audio</label><input type="text" value="48 h ouvrables"></div>
              <div class="field"><label>Délai max d'attribution audio</label><input type="text" value="6 h"></div>
              <div class="field"><label>Annulation gratuite avant</label><input type="text" value="24 h"></div>
            </div>
          </div>
        </div>
      </div>

      <div id="tab-doctrine" role="tabpanel" hidden>
        <div class="card">
          <h3 style="font-family:var(--font-display); font-size:var(--text-base); margin-bottom:var(--space-4);">Frontières du discours public</h3>
          <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-bottom:var(--space-4);">
            Vocabulaire admis dans les pages publiques et les réponses praticien·ne·s. Les modifications ici déclenchent une revue par le comité doctrinaire.
          </p>
          <div class="grid grid-2">
            <div>
              <h4 style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-mousse); margin-bottom:var(--space-3);">Vocabulaire OK</h4>
              <div class="cluster">
                <span class="chip chip--mousse">présence</span>
                <span class="chip chip--mousse">écoute</span>
                <span class="chip chip--mousse">clarté</span>
                <span class="chip chip--mousse">repère</span>
                <span class="chip chip--mousse">chemins</span>
                <span class="chip chip--mousse">voies</span>
                <span class="chip chip--mousse">équilibre</span>
                <span class="chip chip--mousse">indépendance choisie</span>
              </div>
            </div>
            <div>
              <h4 style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-error); margin-bottom:var(--space-3);">Vocabulaire à éviter</h4>
              <div class="cluster">
                <span class="chip" style="background: color-mix(in oklab, var(--color-error) 12%, var(--color-creme)); color:var(--color-error);">thérapie</span>
                <span class="chip" style="background: color-mix(in oklab, var(--color-error) 12%, var(--color-creme)); color:var(--color-error);">traitement</span>
                <span class="chip" style="background: color-mix(in oklab, var(--color-error) 12%, var(--color-creme)); color:var(--color-error);">guérison</span>
                <span class="chip" style="background: color-mix(in oklab, var(--color-error) 12%, var(--color-creme)); color:var(--color-error);">diagnostic</span>
                <span class="chip" style="background: color-mix(in oklab, var(--color-error) 12%, var(--color-creme)); color:var(--color-error);">symptôme</span>
                <span class="chip" style="background: color-mix(in oklab, var(--color-error) 12%, var(--color-creme)); color:var(--color-error);">pathologie</span>
                <span class="chip" style="background: color-mix(in oklab, var(--color-error) 12%, var(--color-creme)); color:var(--color-error);">protocole</span>
              </div>
            </div>
          </div>
          <div class="cadre-ethique" style="margin-top:var(--space-6);">
            <svg class="cadre-ethique__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><path d="M12 8 V 13 M 12 16 L 12 16.01"/></svg>
            <p>« IVIA n'est pas un service d'urgence et ne pose pas de diagnostic » — cette mention est obligatoirement affichée sur toutes les pages publiques et toutes les réponses audio. Elle ne peut pas être désactivée.</p>
          </div>
        </div>
      </div>

      <div id="tab-tarifs" role="tabpanel" hidden>
        <div class="card">
          <h3 style="font-family:var(--font-display); font-size:var(--text-base); margin-bottom:var(--space-4);">Tarifs publics</h3>
          <table class="data-table">
            <thead><tr><th>Offre</th><th>Tarif standard</th><th>Tarif solidaire</th></tr></thead>
            <tbody>
              <tr><td>Rencontre simple (60 min)</td><td>95 $</td><td>55 $</td></tr>
              <tr><td>Audio asynchrone + bref appel</td><td>Inclus dans rencontre</td><td>—</td></tr>
              <tr><td>Appel court (15 min)</td><td>Gratuit</td><td>Gratuit</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <div id="tab-loi25" role="tabpanel" hidden>
        <div class="card">
          <h3 style="font-family:var(--font-display); font-size:var(--text-base); margin-bottom:var(--space-4);">Conformité Loi 25 (Québec)</h3>
          <ul role="list" style="display:flex; flex-direction:column; gap:var(--space-3); font-family:var(--font-serif);">
            <li class="flex" style="align-items:flex-start;"><span class="status-dot status-dot--ok" style="margin-top:6px;"></span><span>Hébergement Québec (OVH BHS) confirmé pour audios et notes praticien·ne·s</span></li>
            <li class="flex" style="align-items:flex-start;"><span class="status-dot status-dot--ok" style="margin-top:6px;"></span><span>Politique de confidentialité publiée et versionnée (v3 — 1<sup>er</sup> mai 2026)</span></li>
            <li class="flex" style="align-items:flex-start;"><span class="status-dot status-dot--ok" style="margin-top:6px;"></span><span>Responsable de la protection des renseignements personnels désigné·e (D. Phaneuf)</span></li>
            <li class="flex" style="align-items:flex-start;"><span class="status-dot status-dot--pending" style="margin-top:6px;"></span><span>Évaluation des facteurs relatifs à la vie privée (EFVP) à mettre à jour pour fonctionnalité audio asynchrone</span></li>
            <li class="flex" style="align-items:flex-start;"><span class="status-dot status-dot--ok" style="margin-top:6px;"></span><span>Procédure de droit à l'oubli automatisée — 2 demandes en cours</span></li>
          </ul>
        </div>
      </div>

      <div id="tab-equipe" role="tabpanel" hidden>
        <div class="card">
          <h3 style="font-family:var(--font-display); font-size:var(--text-base); margin-bottom:var(--space-4);">Comptes maison</h3>
          <table class="data-table">
            <thead><tr><th>Personne</th><th>Rôle</th><th>Accès</th><th>Statut</th></tr></thead>
            <tbody>
              <tr><td><strong>D. Phaneuf</strong></td><td>Fondateur · admin total</td><td>Toutes données</td><td><span class="chip chip--mousse">Actif</span></td></tr>
              <tr><td><strong>Coordination clinique</strong></td><td>Encadrement praticien·ne·s</td><td>Données agrégées + dossiers vigilance</td><td><span class="chip">Poste à pourvoir</span></td></tr>
              <tr><td><strong>Comité doctrinaire</strong></td><td>Validation discours & cadre</td><td>Lecture seule + propositions</td><td><span class="chip chip--lavande">3 membres</span></td></tr>
            </tbody>
          </table>
          <button class="btn btn--ghost" style="margin-top:var(--space-4);">＋ Inviter un membre</button>
        </div>
      </div>
    </div>
  </div>
</div>
'''


# =============================================================
# ANALYTIQUE — lecture qualitative de l'activité IVIA
# =============================================================
def analytique_body():
    # Mini-graphes inline
    bars_profondeur = "".join(f'<rect x="{40+i*65}" y="{180-h}" width="36" height="{h}" rx="4" fill="url(#g-mousse)"/><text x="{58+i*65}" y="175" text-anchor="middle" font-family="Inter" font-size="9" fill="#6E5F71">{lbl}</text><text x="{58+i*65}" y="{170-h}" text-anchor="middle" font-family="Inter" font-size="10" fill="#2A1F2D" font-weight="500">{val}</text>' for i, (h, lbl, val) in enumerate([(40, "<5min", "12%"), (78, "5-10", "24%"), (120, "10-15", "37%"), (95, "15-20", "18%"), (52, "20-30", "7%"), (28, ">30", "2%")]))

    line_retour = "M40,140 L100,125 L160,135 L220,110 L280,95 L340,85 L400,80 L460,75 L520,72 L580,70"

    return f'''
<div class="workspace">
  {admin_sidebar("analytique.html")}
  <div class="workspace__content">
    <header class="workspace__header">
      <p style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-rose-deep);">Analytique · lecture de la maison · 90 derniers jours</p>
      <h1>Ce que la pratique nous apprend.</h1>
      <p>Les chiffres ici ne mesurent pas la croissance à tout prix. Ils mesurent la qualité de présence, la justesse de l'orientation, et la santé de la maison. Aucune donnée nominative — tout est agrégé et anonymisé (consentement N1, Loi 25 art. 12).</p>
    </header>

    <!-- Sélecteur période -->
    <div style="display:flex; gap:var(--space-3); margin-bottom:var(--space-10); flex-wrap:wrap; align-items:center;">
      <span style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-text-muted);">Période</span>
      <button class="btn btn--ghost btn--sm">7 j</button>
      <button class="btn btn--ghost btn--sm">30 j</button>
      <button class="btn btn--primary btn--sm">90 j</button>
      <button class="btn btn--ghost btn--sm">12 mois</button>
      <button class="btn btn--ghost btn--sm" style="margin-left:auto;">Exporter (.csv)</button>
    </div>

    <!-- KPIs alignement intentions -->
    <h2 style="font-family:var(--font-display); font-size:var(--text-lg); margin-bottom:var(--space-2);">Indicateurs d'alignement</h2>
    <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-bottom:var(--space-6); max-width:70ch;">
      Les métriques que nous avons choisi de suivre, parce qu'elles reflètent l'intention IVIA — et non les vanity metrics standard du SaaS. Lecture qualitative à côté de chaque indicateur.
    </p>
    <div class="kpi-grid" style="margin-bottom:var(--space-12);">
      <div class="kpi">
        <p class="kpi__label">Profondeur d'écoute</p>
        <p class="kpi__value">11 m 43</p>
        <p class="kpi__delta">Durée moy. audio asynchrone</p>
      </div>
      <div class="kpi">
        <p class="kpi__label">Taux « ne rien décider »</p>
        <p class="kpi__value">38 %</p>
        <p class="kpi__delta">Sain · cible 30-50 %</p>
      </div>
      <div class="kpi">
        <p class="kpi__label">Conversion appel → RDV</p>
        <p class="kpi__value">42 %</p>
        <p class="kpi__delta">Pas un objectif à maximiser</p>
      </div>
      <div class="kpi">
        <p class="kpi__label">Récurrence saine 30 j</p>
        <p class="kpi__value">61 %</p>
        <p class="kpi__delta">Reviennent par choix, non par dépendance</p>
      </div>
      <div class="kpi">
        <p class="kpi__label">Charge praticien·ne moy.</p>
        <p class="kpi__value">14 / sem</p>
        <p class="kpi__delta">Cible 12-16 · sous contrôle</p>
      </div>
      <div class="kpi">
        <p class="kpi__label">Redirections externes</p>
        <p class="kpi__value">7</p>
        <p class="kpi__delta">Vers ressources spécialisées · 90 j</p>
      </div>
    </div>

    <!-- Profondeur des audios -->
    <div class="grid" style="grid-template-columns: 1.6fr 1fr; gap:var(--space-8); margin-bottom:var(--space-12);">
      <div class="card" style="padding:var(--space-8);">
        <p class="card__meta">Distribution des durées d'audio asynchrone (n=189)</p>
        <h3 style="font-family:var(--font-display); font-size:var(--text-lg); margin-block:var(--space-2) var(--space-1);">Les gens prennent le temps qu'il faut.</h3>
        <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-bottom:var(--space-6);">
          La majorité des audios font entre 10 et 15 minutes. Les enregistrements très courts (&lt;5 min) tendent à être des essais ; les très longs (&gt;30 min) signalent souvent un besoin d'orientation vers une rencontre directe.
        </p>
        <svg viewBox="0 0 460 200" style="width:100%; height:auto;">
          <defs>
            <linearGradient id="g-mousse" x1="0" x2="0" y1="0" y2="1">
              <stop offset="0%" stop-color="#6B8266" stop-opacity="0.85"/>
              <stop offset="100%" stop-color="#6B8266" stop-opacity="0.3"/>
            </linearGradient>
          </defs>
          {bars_profondeur}
        </svg>
      </div>
      <div class="card card--warm" style="padding:var(--space-6);">
        <p class="card__meta">Lecture</p>
        <h3 style="font-family:var(--font-display); font-size:var(--text-base); margin-top:var(--space-2);">Ce que cela nous dit</h3>
        <ul role="list" style="display:flex; flex-direction:column; gap:var(--space-3); font-family:var(--font-serif); font-size:var(--text-sm); margin-top:var(--space-4);">
          <li>La fenêtre 10–15 min est le repère naturel. Pas besoin d'imposer une durée.</li>
          <li>Les 12 % &lt; 5 min méritent un nudge doux : « vous pouvez prendre plus de temps si ça vient ».</li>
          <li>Les 2 % &gt; 30 min signalent un besoin réel de rencontre directe — pas un problème technique.</li>
        </ul>
      </div>
    </div>

    <!-- Concepts émergents -->
    <h2 style="font-family:var(--font-display); font-size:var(--text-lg); margin-bottom:var(--space-2);">Structuration des concepts émergents</h2>
    <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-bottom:var(--space-6); max-width:70ch;">
      Ce qui revient dans les conversations, agrégé à partir des résumés anonymisés (consentement N2 uniquement, n=124). Sert à reconnaitre les voies qui se dessinent et à mieux outiller la pratique — jamais à segmenter les personnes.
    </p>
    <div class="grid" style="grid-template-columns: 1.4fr 1fr; gap:var(--space-8); margin-bottom:var(--space-12);">
      <div class="card" style="padding:var(--space-8);">
        <p class="card__meta">Nuage thématique · 90 derniers jours</p>
        <div style="display:flex; flex-wrap:wrap; gap:var(--space-3); align-items:center; margin-top:var(--space-5); line-height:1.4;">
          <span style="font-family:var(--font-display); font-size:2.4rem; color:var(--color-aubergine);">sommeil</span>
          <span style="font-family:var(--font-display); font-size:1.4rem; color:var(--color-rose-deep);">fatigue</span>
          <span style="font-family:var(--font-display); font-size:2rem; color:var(--color-mousse);">brouillard</span>
          <span style="font-family:var(--font-display); font-size:1.2rem; color:var(--color-glacier);">silence</span>
          <span style="font-family:var(--font-display); font-size:1.7rem; color:var(--color-aubergine);">retour</span>
          <span style="font-family:var(--font-display); font-size:1rem; color:var(--color-text-muted);">attente</span>
          <span style="font-family:var(--font-display); font-size:1.5rem; color:var(--color-rose);">rythme</span>
          <span style="font-family:var(--font-display); font-size:1.1rem; color:var(--color-lavande);">famille</span>
          <span style="font-family:var(--font-display); font-size:1.9rem; color:var(--color-aubergine);">présence</span>
          <span style="font-family:var(--font-display); font-size:1.3rem; color:var(--color-mousse);">corps</span>
          <span style="font-family:var(--font-display); font-size:1rem; color:var(--color-text-muted);">détour</span>
          <span style="font-family:var(--font-display); font-size:1.6rem; color:var(--color-prune);">deuil</span>
          <span style="font-family:var(--font-display); font-size:1.1rem; color:var(--color-text-muted);">ralentir</span>
          <span style="font-family:var(--font-display); font-size:1.4rem; color:var(--color-glacier);">ouverture</span>
          <span style="font-family:var(--font-display); font-size:1rem; color:var(--color-text-muted);">attendre</span>
          <span style="font-family:var(--font-display); font-size:1.2rem; color:var(--color-rose);">apprivoiser</span>
        </div>
        <p style="font-size:var(--text-xs); color:var(--color-text-muted); margin-top:var(--space-6); font-style:italic;">Termes extraits des résumés anonymisés, fréquence ≥ 5 occurrences. Filtre Loi 25 : aucune mention identifiante (lieux précis, noms, employeurs).</p>
      </div>

      <div class="card" style="padding:var(--space-6);">
        <p class="card__meta">Voies — répartition fine</p>
        <div style="display:flex; flex-direction:column; gap:var(--space-4); margin-top:var(--space-5);">
          <div>
            <div class="flex-between" style="margin-bottom:4px;"><span style="font-size:var(--text-sm); font-family:var(--font-display);">Sommeil</span><span style="font-size:var(--text-xs); color:var(--color-text-muted);">31 % · +4 pts</span></div>
            <div style="height:8px; background:var(--color-divider); border-radius:4px; overflow:hidden;"><div style="width:31%; height:100%; background:var(--color-glacier);"></div></div>
          </div>
          <div>
            <div class="flex-between" style="margin-bottom:4px;"><span style="font-size:var(--text-sm); font-family:var(--font-display);">Fréquence</span><span style="font-size:var(--text-xs); color:var(--color-text-muted);">28 % · stable</span></div>
            <div style="height:8px; background:var(--color-divider); border-radius:4px; overflow:hidden;"><div style="width:28%; height:100%; background:var(--color-mousse);"></div></div>
          </div>
          <div>
            <div class="flex-between" style="margin-bottom:4px;"><span style="font-size:var(--text-sm); font-family:var(--font-display);">Connaissance</span><span style="font-size:var(--text-xs); color:var(--color-text-muted);">18 % · −2 pts</span></div>
            <div style="height:8px; background:var(--color-divider); border-radius:4px; overflow:hidden;"><div style="width:18%; height:100%; background:var(--color-lavande);"></div></div>
          </div>
          <div>
            <div class="flex-between" style="margin-bottom:4px;"><span style="font-size:var(--text-sm); font-family:var(--font-display);">Famille · lien</span><span style="font-size:var(--text-xs); color:var(--color-text-muted);">14 % · +2 pts</span></div>
            <div style="height:8px; background:var(--color-divider); border-radius:4px; overflow:hidden;"><div style="width:14%; height:100%; background:var(--color-rose);"></div></div>
          </div>
          <div>
            <div class="flex-between" style="margin-bottom:4px;"><span style="font-size:var(--text-sm); font-family:var(--font-display);">Deuil · transition</span><span style="font-size:var(--text-xs); color:var(--color-text-muted);">9 % · émergente</span></div>
            <div style="height:8px; background:var(--color-divider); border-radius:4px; overflow:hidden;"><div style="width:9%; height:100%; background:var(--color-prune);"></div></div>
          </div>
        </div>
        <p style="font-size:var(--text-xs); color:var(--color-text-muted); margin-top:var(--space-5); font-style:italic;">La voie « Deuil · transition » émerge depuis 6 semaines. À documenter — peut-être une porte officielle à ouvrir.</p>
      </div>
    </div>

    <!-- Santé du retour -->
    <h2 style="font-family:var(--font-display); font-size:var(--text-lg); margin-bottom:var(--space-2);">Qualité du retour des personnes</h2>
    <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-bottom:var(--space-6); max-width:70ch;">
      Pas un retention rate. Une lecture du fait que les gens reviennent par choix — et qu'ils savent aussi s'arrêter.
    </p>
    <div class="card" style="padding:var(--space-8); margin-bottom:var(--space-12);">
      <div class="flex-between" style="flex-wrap:wrap; gap:var(--space-6); margin-bottom:var(--space-6);">
        <div>
          <p class="card__meta">Indice de retour sain (90 j)</p>
          <p style="font-family:var(--font-display); font-size:var(--text-2xl); margin-top:var(--space-2);">+62</p>
          <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-top:var(--space-1); max-width:50ch;">Compose la satisfaction déclarée (44 réponses), la récurrence libre, et le taux de clôtures explicites. Inclut le « je suis bien, je n'ai plus besoin » comme un signal positif.</p>
        </div>
        <div style="flex:1; min-width:280px;">
          <svg viewBox="0 0 600 160" style="width:100%; height:auto;">
            <defs>
              <linearGradient id="g-area" x1="0" x2="0" y1="0" y2="1">
                <stop offset="0%" stop-color="#C58A8A" stop-opacity="0.4"/>
                <stop offset="100%" stop-color="#C58A8A" stop-opacity="0"/>
              </linearGradient>
            </defs>
            <path d="{line_retour} L580,160 L40,160 Z" fill="url(#g-area)"/>
            <path d="{line_retour}" fill="none" stroke="#C58A8A" stroke-width="2"/>
            <text x="40" y="155" font-family="Inter" font-size="9" fill="#6E5F71">Fév</text>
            <text x="160" y="155" font-family="Inter" font-size="9" fill="#6E5F71">Mars</text>
            <text x="280" y="155" font-family="Inter" font-size="9" fill="#6E5F71">Avr</text>
            <text x="400" y="155" font-family="Inter" font-size="9" fill="#6E5F71">Mai</text>
          </svg>
        </div>
      </div>
    </div>

    <!-- Vigilance -->
    <h2 style="font-family:var(--font-display); font-size:var(--text-lg); margin-bottom:var(--space-2);">Vigilance · signaux à lire</h2>
    <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-bottom:var(--space-6); max-width:70ch;">
      Les chiffres qui méritent une lecture humaine, pas une alerte automatisée.
    </p>
    <div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:var(--space-5); margin-bottom:var(--space-12);">
      <article class="card" style="padding:var(--space-6); border-left:3px solid var(--color-rose);">
        <p style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-rose-deep);">Signal · charge</p>
        <h3 style="font-family:var(--font-display); font-size:var(--text-base); margin-top:var(--space-2);">2 praticien·ne·s au-dessus de la cible &gt; 4 sem.</h3>
        <p style="font-family:var(--font-serif); font-size:var(--text-sm); color:var(--color-text-muted); margin-top:var(--space-2);">Soraya B.-A. (6 sem.) et Étienne G.-C. (5 sem.). Suggestion : pause auto + redistribution.</p>
      </article>
      <article class="card" style="padding:var(--space-6); border-left:3px solid var(--color-miel);">
        <p style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-rose-deep);">Signal · redirections</p>
        <h3 style="font-family:var(--font-display); font-size:var(--text-base); margin-top:var(--space-2);">7 redirections externes en 90 j</h3>
        <p style="font-family:var(--font-serif); font-size:var(--text-sm); color:var(--color-text-muted); margin-top:var(--space-2);">5 vers Info-Social 811, 2 vers ressources spécialisées. Indique que le filtre vigilance fonctionne.</p>
      </article>
      <article class="card" style="padding:var(--space-6); border-left:3px solid var(--color-mousse);">
        <p style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-rose-deep);">Signal · santé</p>
        <h3 style="font-family:var(--font-display); font-size:var(--text-base); margin-top:var(--space-2);">Délai réponse audio : 32 h moy.</h3>
        <p style="font-family:var(--font-serif); font-size:var(--text-sm); color:var(--color-text-muted); margin-top:var(--space-2);">SLA 48 h respecté à 96 %. 3 audios ont dépassé ce trimestre, tous explicités aux personnes concernées.</p>
      </article>
      <article class="card" style="padding:var(--space-6); border-left:3px solid var(--color-lavande);">
        <p style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; color:var(--color-rose-deep);">Signal · consentements</p>
        <h3 style="font-family:var(--font-display); font-size:var(--text-base); margin-top:var(--space-2);">Adoption N2 · 66 %, N3 · 11 %</h3>
        <p style="font-family:var(--font-serif); font-size:var(--text-sm); color:var(--color-text-muted); margin-top:var(--space-2);">Stable. Le consentement N3 (modèle IA propriétaire) reste minoritaire — c'est sain : nous ne le poussons pas.</p>
      </article>
    </div>

    <!-- Outils intelligents -->
    <h2 style="font-family:var(--font-display); font-size:var(--text-lg); margin-bottom:var(--space-2);">Outils d'analyse</h2>
    <p style="font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm); margin-bottom:var(--space-6); max-width:70ch;">
      Approfondir une question précise. Toujours sur des données agrégées — jamais sur le contenu d'un audio identifié.
    </p>
    <div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:var(--space-5);">
      <article class="card card--clickable" data-href="#" style="padding:var(--space-6); cursor:pointer;">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" style="color:var(--color-mousse); margin-bottom:var(--space-3);"><circle cx="11" cy="11" r="7"/><path d="M21 21 L 16 16"/></svg>
        <h3 style="font-family:var(--font-display); font-size:var(--text-base);">Recherche thématique</h3>
        <p style="font-family:var(--font-serif); font-size:var(--text-sm); color:var(--color-text-muted); margin-top:var(--space-2);">Combien de mentions « brouillard » par voie ? Comment évolue le thème « deuil » ?</p>
      </article>
      <article class="card card--clickable" data-href="#" style="padding:var(--space-6); cursor:pointer;">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" style="color:var(--color-glacier); margin-bottom:var(--space-3);"><path d="M3 12 H 21 M 12 3 V 21"/><circle cx="12" cy="12" r="4"/></svg>
        <h3 style="font-family:var(--font-display); font-size:var(--text-base);">Croisement voies × durée</h3>
        <p style="font-family:var(--font-serif); font-size:var(--text-sm); color:var(--color-text-muted); margin-top:var(--space-2);">Quelles voies prennent plus de temps à trouver le bon rythme ? Y a-t-il des saisons ?</p>
      </article>
      <article class="card card--clickable" data-href="#" style="padding:var(--space-6); cursor:pointer;">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" style="color:var(--color-prune); margin-bottom:var(--space-3);"><path d="M12 2 V 6 M 12 18 V 22 M 4.93 4.93 L 7.76 7.76 M 16.24 16.24 L 19.07 19.07 M 2 12 H 6 M 18 12 H 22"/><circle cx="12" cy="12" r="4"/></svg>
        <h3 style="font-family:var(--font-display); font-size:var(--text-base);">Cycles & rythmes</h3>
        <p style="font-family:var(--font-serif); font-size:var(--text-sm); color:var(--color-text-muted); margin-top:var(--space-2);">Comment l'activité évolue selon le cycle lunaire, les saisons, les moments de transition.</p>
      </article>
      <article class="card card--clickable" data-href="#" style="padding:var(--space-6); cursor:pointer;">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" style="color:var(--color-rose); margin-bottom:var(--space-3);"><path d="M12 1 L 3 5 V 11 C 3 16.5, 7 21, 12 23 C 17 21, 21 16.5, 21 11 V 5 Z"/></svg>
        <h3 style="font-family:var(--font-display); font-size:var(--text-base);">Conformité Loi 25</h3>
        <p style="font-family:var(--font-serif); font-size:var(--text-sm); color:var(--color-text-muted); margin-top:var(--space-2);">Audit du respect des durées de conservation, des consentements actifs, et des suppressions effectuées.</p>
      </article>
    </div>

    <!-- Note doctrinale -->
    <div class="card" style="margin-top:var(--space-12); padding:var(--space-6); background:var(--color-aubergine); color:var(--color-creme);">
      <p style="font-size:var(--text-xs); letter-spacing:0.12em; text-transform:uppercase; opacity:0.7; margin-bottom:var(--space-2);">Charte doctrinaire IVIA · rappel</p>
      <p style="font-family:var(--font-serif); font-size:var(--text-sm); line-height:1.7; opacity:0.95;">
        Cette interface ne sert pas à optimiser une croissance. Elle sert à voir si la maison tient ses promesses : présence, justesse, et respect des personnes accompagnées. Toute métrique qui pousserait à augmenter le volume au détriment de la qualité doit être signalée — et retirée.
      </p>
    </div>
  </div>
</div>
'''


def build():
    pages = [
        ("index.html",     "Vue d'ensemble — Admin IVIA",   "Tableau de bord global de la maison IVIA.",          index_body()),
        ("analytique.html","Analytique — Admin IVIA",       "Lecture qualitative de l'activité IVIA : profondeur d'écoute, concepts émergents, santé du retour.", analytique_body()),
        ("praticiens.html","Praticien·ne·s — Admin IVIA",   "Gestion des praticien·ne·s : candidatures, charge, statuts.", praticiens_body()),
        ("clients.html",   "Clients — Admin IVIA",          "Suivi agrégé des clients (sans accès au contenu des notes).", clients_body()),
        ("audios.html",    "Audios — Admin IVIA",           "File d'audios, attribution, SLA.",                    audios_body()),
        ("finance.html",   "Finance — Admin IVIA",          "Revenus, commissions, reversements, abonnements.",    finance_body()),
        ("parametres.html","Paramètres — Admin IVIA",       "Configuration de la maison IVIA.",                    parametres_body()),
    ]
    for filename, title, description, body in pages:
        html = page(title, description, ADMIN_NAV, filename, ADMIN_ACTIONS, body, "index.html", FOOTER_INTERNE, css_extra=WORKSPACE_CSS)
        (OUT / filename).write_text(html, encoding="utf-8")

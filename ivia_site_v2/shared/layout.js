/**
 * IVIA — shared/layout.js
 * Header et footer uniques de l'espace connecté — UNE seule source pour toutes les pages.
 * Coquille stylée par /shared/ivia-espace.css (thème « Maison habitée » Signature/Doux,
 * défaut clair). Navigation client : Mon espace · Journal · Ligne de vie.
 *
 * Usage dans une page :
 *   <script src="/shared/api.js?v=..."></script>
 *   <script src="/shared/layout.js?v=..."></script>
 *   <body> commence par <div id="ivia-header"></div> et finit par <div id="ivia-footer"></div>
 *   puis renderLayout('parler')              → fil « Accueil › Parler »
 *   ou   renderLayout('parler', 'Séance express') → fil « Accueil › Parler › Séance express »
 */

const IVIA_NAV = [
  { id: 'aujourdhui', label: 'Mon espace',   href: '/client/dashboard.html' },
  { id: 'ecrire',     label: 'Journal',      href: '/client/journal.html' },
  { id: 'miroir',     label: 'Miroir',       href: '/client/mon-reflet.html', crumb: 'Miroir' },
  { id: 'voir',       label: 'Horizon',      href: '/client/carte-de-vie.html', crumb: 'Horizon' },
];

const IVIA_ACCUEIL = 'https://ivia.quebec';

const IVIA_FOOTER = {
  espace: [
    { label: 'Mon espace',           href: '/client/dashboard.html' },
    { label: 'Journal',              href: '/client/journal.html' },
    { label: 'Mon reflet',           href: '/client/mon-reflet.html' },
    { label: 'Vie',                  href: '/client/carte-de-vie.html' },
    { label: 'Réserver une séance',  href: '/client/agenda.html' },
    { label: 'Mes séances',          href: '/client/seances.html' },
    { label: 'Mes enregistrements',  href: '/client/mes-enregistrements.html' },
    // Repères et exercices vivent dans « Mon reflet » (écran branché) —
    // les anciennes pages dédiées étaient des maquettes en doublon.
    { label: 'Mes résumés',          href: '/client/mes-resumes.html' },
    { label: 'Séance expresse',      href: '/client/enregistrement.html' },
    { label: 'Mon compte',           href: '/client/compte.html' },
  ],
  decouvrir: [
    { label: 'Pourquoi IVIA',        href: '/pourquoi.html' },
    { label: 'Pour les praticiens',  href: '/praticiens.html' },
    { label: 'Réserver une séance',  href: '/reserver.html' },
  ],
  legal: [
    { label: 'Confidentialité',      href: '/confidentialite.html' },
    { label: 'Conditions (CGU)',     href: '/cgu.html' },
    { label: 'Mentions légales',     href: '/mentions.html' },
  ],
};

// Charge la feuille de style de la coquille si la page ne l'a pas déjà incluse.
(function ensureEspaceCss() {
  if (typeof document === 'undefined') return;
  if (!document.querySelector('link[data-ivia-espace]')) {
    const l = document.createElement('link');
    l.rel = 'stylesheet';
    l.href = '/shared/ivia-espace.css?v=20260709b';
    l.setAttribute('data-ivia-espace', '1');
    document.head.appendChild(l);
  }
})();

const _ic = (d) => `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">${d}</svg>`;
const IVIA_ICON = {
  aujourdhui: _ic('<path stroke-linecap="round" stroke-linejoin="round" d="M3 11l9-8 9 8M5 10v10h14V10"/>'),
  parler:     _ic('<path stroke-linecap="round" stroke-linejoin="round" d="M19 11a7 7 0 01-14 0m7 7v3m-3 0h6M12 14a3 3 0 01-3-3V5a3 3 0 016 0v6a3 3 0 01-3 3z"/>'),
  ecrire:     _ic('<path stroke-linecap="round" stroke-linejoin="round" d="M11 4H4v16h16v-7M18.5 2.5a2.12 2.12 0 013 3L12 15l-4 1 1-4z"/>'),
  voir:       _ic('<path stroke-linecap="round" stroke-linejoin="round" d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/>'),
  agenda:     _ic('<rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>'),
  miroir:     _ic('<ellipse cx="12" cy="10" rx="6" ry="8"/><path stroke-linecap="round" d="M9 20h6M12 18v3"/>'),
};


function renderLayout(active, pageLabel) {
  // Auto-réparant (bug fondateur 2026-07-11 : Horizon sans footer, Miroir sans
  // menu ni footer) : on attend que la page soit chargée, et on CRÉE les
  // points de montage s'ils manquent — plus aucune page ne peut les oublier.
  const run = () => _renderLayoutNow(active, pageLabel);
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run, { once: true });
  } else {
    run();
  }
}

function _renderLayoutNow(active, pageLabel) {
  let header = document.getElementById('ivia-header');
  if (!header) {
    header = document.createElement('div');
    header.id = 'ivia-header';
    document.body.prepend(header);
  }
  if (header) {
    const links = '';

    const section = IVIA_NAV.find(n => n.id === active);
    // Breadcrumb: Accueil (site public) › Mon espace › [section] › [pageLabel]
    const crumbs = [`<a href="${IVIA_ACCUEIL}">Accueil</a>`];
    if (!section || section.id === 'aujourdhui') {
      // On Mon espace or unknown section
      if (!pageLabel) {
        crumbs.push('<span class="here">Mon espace</span>');
      } else {
        crumbs.push('<a href="/client/dashboard.html">Mon espace</a>');
        crumbs.push(`<span class="here">${pageLabel}</span>`);
      }
    } else {
      // On a named section (Journal, Carte de vie, Agenda…)
      crumbs.push('<a href="/client/dashboard.html">Mon espace</a>');
      const sectionLabel = section.crumb || section.label;
      if (pageLabel) {
        crumbs.push(`<a href="${section.href}">${sectionLabel}</a>`);
        crumbs.push(`<span class="here">${pageLabel}</span>`);
      } else {
        crumbs.push(`<span class="here">${sectionLabel}</span>`);
      }
    }
    const fil = `<div class="ivia-fil"><div class="ivia-fil-row">${crumbs.join('<span class="sep">›</span>')}</div></div>`;

    header.innerHTML = `
    <nav class="ivia-nav">
      <div class="ivia-nav-row">
        <a href="/client/dashboard.html" class="ivia-brand" aria-label="IVIA — Mon espace">
          <svg width="24" height="24" viewBox="0 0 28 28" fill="none" aria-hidden="true">
            <rect width="28" height="28" rx="7" fill="currentColor"/>
            <rect x="7" y="11" width="3.5" height="6" rx="1.75" fill="var(--menu-bg)"/>
            <rect x="12.25" y="7" width="3.5" height="14" rx="1.75" fill="var(--menu-bg)"/>
            <rect x="17.5" y="9" width="3.5" height="10" rx="1.75" fill="var(--menu-bg)"/>
          </svg>
          IVIA
        </a>
        <div class="ivia-links">${links}</div>
        <div class="ivia-end">
          <a href="/client/enregistrement.html" class="ivia-cta">Séance express</a>
          <div class="ivia-menu">
            <button id="ivia-menu-btn" type="button" class="ivia-menu-btn" aria-haspopup="true" aria-expanded="false" onclick="iviaToggleMenu(event)" title="Mon compte">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path stroke-linecap="round" stroke-linejoin="round" d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/></svg>
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M6 9l6 6 6-6"/></svg>
            </button>
            <div id="ivia-menu-panel" class="ivia-menu-panel" role="menu" hidden>
              <p class="ivia-menu-lbl">Ambiance</p>
              <div class="ivia-amb" role="tablist" aria-label="Ambiance">
                <button id="ivia-amb-signature" type="button" role="tab" onclick="iviaSetTheme('signature')">Signature</button>
                <button id="ivia-amb-doux" type="button" role="tab" onclick="iviaSetTheme('doux')">Doux</button>
              </div>
              <hr class="ivia-menu-sep">
              <a href="/client/dashboard.html" class="ivia-menu-item">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M3 11l9-8 9 8M5 10v10h14V10"/></svg>
                Mon espace
              </a>
              <a href="/client/journal.html" class="ivia-menu-item">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M11 4H4v16h16v-7M18.5 2.5a2.12 2.12 0 013 3L12 15l-4 1 1-4z"/></svg>
                Journal
              </a>
              <a href="/client/mon-reflet.html" class="ivia-menu-item">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><ellipse cx="12" cy="10" rx="6" ry="8"/><path stroke-linecap="round" d="M9 20h6M12 18v3"/></svg>
                Miroir
              </a>
              <a href="/client/carte-de-vie.html" class="ivia-menu-item">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="2.2"/><circle cx="5" cy="6" r="1.4"/><circle cx="19" cy="5" r="1.4"/><circle cx="20" cy="15" r="1.4"/><circle cx="7" cy="19" r="1.4"/><path stroke-linecap="round" d="M6.2 7l4.2 3.6M13.8 10.5L18 6M13.9 13.2l4.8 1.4M10.3 13.6L8 17.6"/></svg>
                Horizon
              </a>
              <hr class="ivia-menu-sep">
              <a href="/client/enregistrement.html" class="ivia-menu-item">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M19 11a7 7 0 01-14 0m7 7v3m-3 0h6M12 14a3 3 0 01-3-3V5a3 3 0 016 0v6a3 3 0 01-3 3z"/></svg>
                Séance expresse
              </a>
              <a href="/client/agenda.html" class="ivia-menu-item">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                Réservation
              </a>
              <a href="/client/mon-profil.html" class="ivia-menu-item">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path stroke-linecap="round" stroke-linejoin="round" d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/></svg>
                Mon profil
              </a>
              <hr class="ivia-menu-sep">
              <button type="button" class="ivia-menu-item danger" onclick="localStorage.removeItem('ivia_session');localStorage.removeItem('ivia_user');location.href='/connexion.html'">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M16 17l5-5-5-5M21 12H9M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4"/></svg>
                Déconnexion
              </button>
              </div>
          </div>
        </div>
      </div>
      ${fil}
    </nav>`;

    iviaApplyTheme(iviaCurrentTheme());
  }

  let footer = document.getElementById('ivia-footer');
  if (!footer) {
    footer = document.createElement('div');
    footer.id = 'ivia-footer';
    document.body.appendChild(footer);
  }
  if (footer) {
    // Footer contextuel ESPACE CLIENT (décision fondateur 2026-07-10) :
    // les liens du menu client + Services / Ressources / Légal en _blank.
    const lien = (i) => `<li><a href="${i.href}"${i.blank ? ' target="_blank" rel="noopener"' : ''}>${i.label}</a></li>`;
    const col = (titre, items) =>
      `<div class="ivia-footer-col"><p>${titre}</p><ul>${items.map(lien).join('')}</ul></div>`;
    footer.innerHTML = `
    <footer class="ivia-footer">
      <div class="ivia-footer-in">
        <div class="ivia-footer-cols">
          ${col('Espace client', [
            { label: 'Mon espace', href: '/client/dashboard.html' },
            { label: 'Journal', href: '/client/journal.html' },
            { label: 'Miroir', href: '/client/mon-reflet.html' },
            { label: 'Horizon', href: '/client/carte-de-vie.html' },
            { label: 'Séance expresse', href: '/client/enregistrement.html' },
            { label: 'Réservation', href: '/client/agenda.html' },
            { label: 'Mon profil', href: '/client/mon-profil.html' },
          ])}
          ${col('Services', [
            { label: 'Pourquoi IVIA', href: '/pourquoi.html', blank: true },
            { label: 'Pour les praticiens', href: '/praticiens.html', blank: true },
            { label: 'Réserver une séance', href: '/reserver.html', blank: true },
          ])}
          ${col('Ressources', [
            { label: '9-8-8 — Ligne de crise (24/7)', href: 'https://988.ca/fr', blank: true },
            { label: 'Info-Social 8-1-1', href: 'https://www.quebec.ca/sante/trouver-une-ressource/info-social-811', blank: true },
            { label: 'Urgence : 9-1-1', href: 'tel:911' },
          ])}
          ${col('Légal', [
            { label: 'Confidentialité', href: '/confidentialite.html', blank: true },
            { label: 'Conditions (CGU)', href: '/cgu.html', blank: true },
            { label: 'Mentions légales', href: '/mentions.html', blank: true },
          ])}
        </div>
        <div class="ivia-footer-base">
          <p>IVIA — <em>In Vivo, In Actu</em> · Données hébergées au Canada (Loi 25)</p>
          <p>Pas un service d'urgence · En crise : <strong><a href="tel:988">9-8-8</a></strong> · 811 option 2</p>
        </div>
      </div>
    </footer>`;
  }
}

// ── Ambiance (Signature / Doux) — préférence persistée, partagée avec l'enregistreur ──
function iviaCurrentTheme() {
  try { return localStorage.getItem('ivia_recorder_theme') || 'signature'; } catch { return 'signature'; }
}
function iviaApplyTheme(t) {
  // N'applique le thème que si la page a opté (data-theme déjà posé en <head>).
  // Sinon on met seulement à jour l'état des boutons (la page reste claire).
  if (document.documentElement.dataset.theme) {
    document.documentElement.dataset.theme = t;
    if (document.body) document.body.dataset.theme = t;
  }
  const s = document.getElementById('ivia-amb-signature'), d = document.getElementById('ivia-amb-doux');
  if (s) s.classList.toggle('on', t === 'signature');
  if (d) d.classList.toggle('on', t === 'doux');
}
function iviaSetTheme(t) {
  try { localStorage.setItem('ivia_recorder_theme', t); } catch (e) {}
  // N'applique le thème QUE si la page a opté (data-theme posé en <head>).
  // Sur une page pas encore convertie, on mémorise seulement la préférence :
  // elle prendra effet dès la prochaine page thémable. Évite un header sombre
  // sur un corps clair.
  iviaApplyTheme(t);
}
function iviaToggleMenu(e) {
  e.stopPropagation();
  const p = document.getElementById('ivia-menu-panel'), b = document.getElementById('ivia-menu-btn');
  if (!p) return;
  const open = p.hasAttribute('hidden');
  if (open) { p.removeAttribute('hidden'); } else { p.setAttribute('hidden', ''); }
  b.setAttribute('aria-expanded', String(open));
}
document.addEventListener('click', (e) => {
  const p = document.getElementById('ivia-menu-panel');
  if (p && !p.hasAttribute('hidden') && !e.target.closest('#ivia-menu-panel') && !e.target.closest('#ivia-menu-btn')) {
    p.setAttribute('hidden', '');
    const b = document.getElementById('ivia-menu-btn');
    b && b.setAttribute('aria-expanded', 'false');
  }
});

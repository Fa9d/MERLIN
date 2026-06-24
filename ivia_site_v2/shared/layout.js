/**
 * IVIA — shared/layout.js
 * Header et footer uniques de l'espace connecté — UNE seule source pour toutes les pages.
 * Navigation quatre verbes : Aujourd'hui · Parler · Écrire · Voir.
 *
 * Usage dans une page :
 *   <script src="/shared/api.js?v=..."></script>
 *   <script src="/shared/layout.js?v=..."></script>
 *   <body> commence par <div id="ivia-header"></div> et finit par <div id="ivia-footer"></div>
 *   puis appeler renderLayout('parler')              → fil d'Ariane « Accueil › Parler »
 *   ou     renderLayout('parler', 'Séance express')  → fil « Accueil › Parler › Séance express »
 */

const IVIA_NAV = [
  { id: 'aujourdhui', label: "Aujourd'hui", href: '/client/dashboard.html' },
  { id: 'parler',     label: 'Parler',      href: '/client/seances.html' },
  { id: 'ecrire',     label: 'Écrire',      href: '/client/journal.html' },
  { id: 'voir',       label: 'Voir',        href: '/client/carte-de-vie.html' },
];

// Liens du footer (regroupés). Le pied de page rassemble TOUS les accès.
const IVIA_FOOTER = {
  espace: [
    { label: "Aujourd'hui",     href: '/client/dashboard.html' },
    { label: 'Mes séances',     href: '/client/seances.html' },
    { label: 'Séance express',  href: '/client/enregistrement.html' },
    { label: 'Mes enregistrements', href: '/client/mes-enregistrements.html' },
    { label: 'Journal',         href: '/client/journal.html' },
    { label: 'Ma carte de vie', href: '/client/carte-de-vie.html' },
    { label: 'Mon compte',      href: '/client/compte.html' },
  ],
  decouvrir: [
    { label: 'Pourquoi IVIA',   href: '/pourquoi.html' },
    { label: 'Pour les praticiens', href: '/praticiens.html' },
    { label: 'Réserver une séance',  href: '/reserver.html' },
  ],
  legal: [
    { label: 'Confidentialité', href: '/confidentialite.html' },
    { label: "Conditions (CGU)", href: '/cgu.html' },
    { label: 'Mentions légales', href: '/mentions.html' },
  ],
};

function renderLayout(active, pageLabel) {
  const header = document.getElementById('ivia-header');
  if (header) {
    const links = IVIA_NAV.map(n =>
      `<a href="${n.href}" class="px-3 py-1.5 rounded-full text-sm ${n.id === active
        ? 'bg-[#2D6A4F] text-white font-semibold'
        : 'text-[#4B6350] hover:text-[#1A2E1D] hover:bg-[#F0F7F2] font-medium'}">${n.label}</a>`
    ).join('');

    // Fil d'Ariane : Accueil › Section [› Page]
    const section = IVIA_NAV.find(n => n.id === active);
    const crumbs = ['<a href="/client/dashboard.html" class="hover:text-[#1A2E1D]">Accueil</a>'];
    if (section && section.id !== 'aujourdhui') crumbs.push(`<a href="${section.href}" class="hover:text-[#1A2E1D]">${section.label}</a>`);
    if (pageLabel) crumbs.push(`<span class="text-[#2D6A4F] font-semibold">${pageLabel}</span>`);
    else if (crumbs.length > 1) crumbs[crumbs.length - 1] = crumbs[crumbs.length - 1].replace('hover:text-[#1A2E1D]', 'text-[#2D6A4F] font-semibold pointer-events-none');
    const fil = crumbs.length > 1
      ? `<div class="border-b border-[#D4E8D0] bg-[#FAFDF8]"><div class="max-w-5xl mx-auto px-5 py-2 text-xs text-[#4B6350] flex items-center gap-2 flex-wrap">${crumbs.join('<span class="text-[#9CB3A1]">›</span>')}</div></div>`
      : '';

    header.innerHTML = `
    <nav class="sticky top-0 z-50 bg-white/90 backdrop-blur-sm border-b border-[#D4E8D0]">
      <div class="max-w-5xl mx-auto px-5 py-2.5 flex items-center justify-between gap-3">
        <a href="/client/dashboard.html" class="flex items-center gap-2 font-heading text-xl font-semibold text-[#2D6A4F] shrink-0" aria-label="IVIA — Mon espace">
          <svg width="24" height="24" viewBox="0 0 28 28" fill="none" aria-hidden="true">
            <rect width="28" height="28" rx="7" fill="#2D6A4F"/>
            <rect x="7" y="11" width="3.5" height="6" rx="1.75" fill="white"/>
            <rect x="12.25" y="7" width="3.5" height="14" rx="1.75" fill="white"/>
            <rect x="17.5" y="9" width="3.5" height="10" rx="1.75" fill="white"/>
          </svg>
          IVIA
        </a>
        <div class="flex items-center gap-1 overflow-x-auto">${links}</div>
        <div class="flex items-center gap-2 shrink-0">
          <a href="/client/enregistrement.html" class="bg-[#2D6A4F] text-white text-xs font-semibold px-3 py-1.5 rounded-full hover:bg-[#4A7C59] transition-colors whitespace-nowrap">Séance express</a>

          <!-- Menu compte : Ambiance + Mon compte + Déconnexion -->
          <div class="relative">
            <button id="ivia-menu-btn" type="button" aria-haspopup="true" aria-expanded="false" onclick="iviaToggleMenu(event)"
                    class="flex items-center gap-1 border border-[#D4E8D0] rounded-full px-2 py-1.5 text-[#4B6350] hover:bg-[#F0F7F2] transition-colors" title="Mon compte">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path stroke-linecap="round" stroke-linejoin="round" d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/></svg>
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M6 9l6 6 6-6"/></svg>
            </button>
            <div id="ivia-menu-panel" class="hidden absolute right-0 mt-2 w-56 bg-white border border-[#D4E8D0] rounded-2xl shadow-xl p-3 z-[60]">
              <p class="text-[10px] font-bold uppercase tracking-wider text-[#9CB3A1] mb-2">Ambiance</p>
              <div class="inline-flex gap-1 bg-[#F0F7F2] border border-[#D4E8D0] rounded-full p-1 mb-3" role="tablist" aria-label="Ambiance">
                <button id="ivia-amb-signature" type="button" role="tab" onclick="iviaSetTheme('signature')" class="text-xs font-bold px-3 py-1.5 rounded-full transition-colors">Signature</button>
                <button id="ivia-amb-doux" type="button" role="tab" onclick="iviaSetTheme('doux')" class="text-xs font-bold px-3 py-1.5 rounded-full transition-colors">Doux</button>
              </div>
              <hr class="border-[#D4E8D0] my-2">
              <a href="/client/compte.html" class="flex items-center gap-2 text-sm font-medium text-[#1A2E1D] hover:bg-[#F0F7F2] rounded-lg px-2 py-2">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path stroke-linecap="round" stroke-linejoin="round" d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/></svg>
                Mon compte
              </a>
              <button type="button" onclick="localStorage.removeItem('ivia_session');localStorage.removeItem('ivia_user');location.href='/connexion.html'"
                      class="w-full flex items-center gap-2 text-sm font-semibold text-red-600 hover:bg-red-50 rounded-lg px-2 py-2">
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

  const footer = document.getElementById('ivia-footer');
  if (footer) {
    const col = (titre, items) =>
      `<div>
        <p class="text-[11px] font-bold uppercase tracking-wider text-[#2D6A4F] mb-3">${titre}</p>
        <ul class="space-y-2">${items.map(i => `<li><a href="${i.href}" class="text-sm text-[#4B6350] hover:text-[#1A2E1D] hover:underline underline-offset-2">${i.label}</a></li>`).join('')}</ul>
      </div>`;
    footer.innerHTML = `
    <footer class="mt-16 border-t border-[#D4E8D0] bg-[#F0F7F2]/50">
      <div class="max-w-5xl mx-auto px-5 py-10">
        <div class="grid grid-cols-2 sm:grid-cols-3 gap-8 mb-8">
          ${col('Mon espace', IVIA_FOOTER.espace)}
          ${col('Découvrir', IVIA_FOOTER.decouvrir)}
          ${col('Cadre & confiance', IVIA_FOOTER.legal)}
        </div>
        <div class="border-t border-[#D4E8D0] pt-6 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-[#4B6350]">
          <p>IVIA — <em>In Vivo, In Actu</em> · Données hébergées au Canada (Loi 25)</p>
          <p>Pas un service d'urgence · En crise : <strong><a href="tel:18662773553" class="underline">1 866 APPELLE</a></strong> · 811 option 2</p>
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
  document.documentElement.dataset.theme = t;
  document.body && (document.body.dataset.theme = t);
  const s = document.getElementById('ivia-amb-signature'), d = document.getElementById('ivia-amb-doux');
  const on = 'bg-[#2D6A4F] text-white', off = 'text-[#4B6350]';
  if (s) s.className = `text-xs font-bold px-3 py-1.5 rounded-full transition-colors ${t === 'signature' ? on : off}`;
  if (d) d.className = `text-xs font-bold px-3 py-1.5 rounded-full transition-colors ${t === 'doux' ? on : off}`;
}
function iviaSetTheme(t) {
  try { localStorage.setItem('ivia_recorder_theme', t); } catch (e) {}
  iviaApplyTheme(t);
}
function iviaToggleMenu(e) {
  e.stopPropagation();
  const p = document.getElementById('ivia-menu-panel'), b = document.getElementById('ivia-menu-btn');
  if (!p) return;
  const open = p.classList.toggle('hidden') === false;
  b.setAttribute('aria-expanded', String(open));
}
document.addEventListener('click', (e) => {
  const p = document.getElementById('ivia-menu-panel');
  if (p && !p.classList.contains('hidden') && !e.target.closest('#ivia-menu-panel') && !e.target.closest('#ivia-menu-btn')) {
    p.classList.add('hidden');
    const b = document.getElementById('ivia-menu-btn');
    b && b.setAttribute('aria-expanded', 'false');
  }
});

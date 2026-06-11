/**
 * IVIA — shared/layout.js
 * Header et footer uniques de l'espace connecté — UNE seule source pour toutes les pages.
 * Navigation quatre verbes : Aujourd'hui · Parler · Écrire · Voir (+ Compte).
 *
 * Usage dans une page :
 *   <script src="/shared/api.js?v=..."></script>
 *   <script src="/shared/layout.js?v=..."></script>
 *   <body> commence par <div id="ivia-header"></div> et finit par <div id="ivia-footer"></div>
 *   puis appeler renderLayout('parler') avec le verbe actif.
 */

const IVIA_NAV = [
  { id: 'aujourdhui', label: "Aujourd'hui", href: '/client/dashboard.html' },
  { id: 'parler',     label: 'Parler',      href: '/client/seances.html' },
  { id: 'ecrire',     label: 'Écrire',      href: '/client/journal.html' },
  { id: 'voir',       label: 'Voir',        href: '/client/carte-de-vie.html' },
];

function renderLayout(active) {
  const user = (() => { try { return JSON.parse(localStorage.getItem('ivia_user') || 'null'); } catch { return null; } })();
  const prenom = user?.display_name ? user.display_name.split(' ')[0] : '';

  const header = document.getElementById('ivia-header');
  if (header) {
    const links = IVIA_NAV.map(n =>
      `<a href="${n.href}" class="px-3 py-1.5 rounded-full text-sm ${n.id === active
        ? 'bg-[#2D6A4F] text-white font-semibold'
        : 'text-[#4B6350] hover:text-[#1A2E1D] hover:bg-[#F0F7F2] font-medium'}">${n.label}</a>`
    ).join('');
    header.innerHTML = `
    <nav class="sticky top-0 z-50 bg-white/90 backdrop-blur-sm border-b border-[#D4E8D0]">
      <div class="max-w-5xl mx-auto px-5 py-2.5 flex items-center justify-between gap-3">
        <a href="/" class="font-heading text-xl font-semibold text-[#2D6A4F] shrink-0">IVIA</a>
        <div class="flex items-center gap-1 overflow-x-auto">${links}</div>
        <div class="flex items-center gap-3 shrink-0">
          <a href="/client/compte.html" class="text-sm text-[#4B6350] hover:text-[#1A2E1D]" title="Compte">${prenom || 'Compte'}</a>
          <button onclick="localStorage.removeItem('ivia_session');localStorage.removeItem('ivia_user');location.href='/connexion.html'"
                  class="text-xs text-[#4B6350] hover:text-red-600 cursor-pointer" title="Déconnexion">Sortir</button>
        </div>
      </div>
    </nav>`;
  }

  const footer = document.getElementById('ivia-footer');
  if (footer) {
    footer.innerHTML = `
    <footer class="mt-16 border-t border-[#D4E8D0] bg-[#F0F7F2]/50 py-8 px-4">
      <div class="max-w-5xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-[#4B6350]">
        <p>IVIA — <em>In Vivo, In Actu</em> · Données hébergées au Canada · <a href="/confidentialite.html" class="underline underline-offset-2">Confidentialité</a> · <a href="/cgu.html" class="underline underline-offset-2">CGU</a></p>
        <p>Pas un service d'urgence · En crise : <strong><a href="tel:18662773553" class="underline">1 866 APPELLE</a></strong> · 811 option 2</p>
      </div>
    </footer>`;
  }
}

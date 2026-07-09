/**
 * IVIA — Gestion de session (auth guard, logout, utilisateur courant)
 * Importé par toutes les pages protégées : client/, praticien/, admin/
 *
 * Contrat : localStorage conserve deux clés :
 *   ivia_session  → token opaque (présence = authentifié)
 *   ivia_user     → JSON du profil utilisateur
 *
 * Quand l'API réelle sera connectée, remplacer getCurrentUser()
 * par un appel fetch + validation JWT, sans toucher au reste.
 */

const SESSION_KEY = 'ivia_session';
const USER_KEY    = 'ivia_user';

/**
 * Redirige vers /connexion.html si la session est absente.
 * À appeler en tout premier dans le <head> de chaque page protégée.
 */
function requireAuth() {
  if (!localStorage.getItem(SESSION_KEY)) {
    const retour = encodeURIComponent(location.pathname + location.search);
    // Les pages admin renvoient vers la porte admin dédiée ; le reste vers la connexion publique.
    const adminPage = location.pathname.startsWith('/admin/');
    const porte = adminPage ? '/admin/connexion.html' : '/connexion.html';
    location.replace(porte + '?retour=' + retour);
  }
}

/**
 * Retourne l'objet utilisateur stocké, ou null.
 * Structure attendue :
 * {
 *   id, prenom, nom, email, role,
 *   courriel_verifie: bool,
 *   nouveau_compte: bool,
 *   avatar_url: string|null
 * }
 */
function getCurrentUser() {
  try {
    const raw = localStorage.getItem(USER_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

/**
 * Persiste un objet utilisateur dans localStorage.
 * Appelé depuis connexion.html après authentification réussie.
 */
function setCurrentUser(user) {
  localStorage.setItem(USER_KEY, JSON.stringify(user));
  if (user?.prenom) localStorage.setItem('ivia_prenom', user.prenom); // rétrocompat
}

/**
 * Déconnecte l'utilisateur et redirige vers /connexion.html.
 */
function logout() {
  localStorage.removeItem(SESSION_KEY);
  localStorage.removeItem(USER_KEY);
  localStorage.removeItem('ivia_prenom');
  location.replace('/connexion.html');
}

/**
 * Vrai si l'utilisateur connecté a des droits admin (champ `is_admin` du backend).
 */
function isAdminUser() {
  const u = getCurrentUser();
  return !!(u && u.is_admin);
}

/**
 * Masque tous les éléments marqués `[data-admin-only]` sauf si l'utilisateur est admin.
 */
function applyAdminVisibility() {
  const admin = isAdminUser();
  document.querySelectorAll('[data-admin-only]').forEach(el => {
    el.style.display = admin ? '' : 'none';
  });
}

/**
 * Liens de la console admin (porte séparée). Source unique de la navigation admin.
 */

/* ── Barre latérale praticien — SOURCE UNIQUE ─────────────────────────────────
 * Un seul menu canonique pour TOUT l'espace praticien (les barres codées en
 * dur par page avaient dérivé : trois menus différents selon la page).
 * Chaque page pose <aside id="praticien-sidebar"></aside> et
 * <nav id="praticien-mobile-nav"></nav>, puis appelle renderPraticienChrome().
 */

const PRATICIEN_ICONS = {
  bord: '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
  agenda: '<path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>',
  express: '<path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z"/>',
  clients: '<path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a4 4 0 00-3-3.87M9 20H4v-2a4 4 0 013-3.87m6-1.13a4 4 0 10-4-4 4 4 0 004 4zm6-4a3 3 0 11-3-3"/>',
  analyses: '<path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>',
  guide: '<path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>',
  pratique: '<circle cx="12" cy="12" r="9"/><path stroke-linecap="round" d="M8 12a4 4 0 018 0"/>',
  profil: '<circle cx="12" cy="8" r="4"/><path stroke-linecap="round" stroke-linejoin="round" d="M4 20c0-4 3.582-7 8-7s8 3 8 7"/>',
  compte: '<path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><circle cx="12" cy="12" r="3"/>',
  admin: '<path stroke-linecap="round" stroke-linejoin="round" d="M7 8h10M7 12h10M7 16h6"/><path stroke-linecap="round" stroke-linejoin="round" d="M5 4h14a2 2 0 012 2v12a2 2 0 01-2 2H5a2 2 0 01-2-2V6a2 2 0 012-2z"/>',
};

const PRATICIEN_NAV = [
  { href: '/praticien/dashboard.html',       label: 'Tableau de bord', court: 'Bord',     icon: 'bord' },
  { href: '/praticien/agenda.html',          label: 'Agenda',          court: 'Agenda',   icon: 'agenda' },
  { href: '/praticien/seance-express.html',  label: 'Séance express',  court: 'Express',  icon: 'express' },
  { href: '/praticien/clients-journal.html', label: 'Clients',         court: 'Clients',  icon: 'clients' },
  { href: '/praticien/livraisons.html',      label: 'Analyses',        court: 'Analyses', icon: 'analyses' },
  { href: '/praticien/guide.html',           label: 'Guide',           court: null,       icon: 'guide' },
  { href: '/praticien/ma-pratique.html',     label: 'Ma pratique',     court: null,       icon: 'pratique' },
  { spacer: true },
  { href: '/admin/vue.html',                 label: 'Console admin',   court: null,       icon: 'admin', adminOnly: true },
  { href: '/praticien/profil.html',          label: 'Mon profil',      court: null,       icon: 'profil' },
  { href: '/praticien/compte.html',          label: 'Mon compte',      court: null,       icon: 'compte' },
];

function _pIcon(name, cls) {
  return '<svg class="' + cls + '" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" aria-hidden="true">' + (PRATICIEN_ICONS[name] || '') + '</svg>';
}

function renderPraticienChrome() {
  // Style des liens injecté ici (source unique) — certaines pages ne le
  // définissaient pas, d'où des barres latérales incohérentes.
  if (!document.getElementById('praticien-chrome-css')) {
    const st = document.createElement('style');
    st.id = 'praticien-chrome-css';
    st.textContent = '.sidebar-link{display:flex;align-items:center;gap:10px;padding:9px 16px;border-radius:10px;font-size:14px;font-weight:500;color:#4B6350;transition:all .15s;cursor:pointer;text-decoration:none;}'
      + '.sidebar-link:hover,.sidebar-link.active{background:#D4E8D0;color:#1A2E1D;}'
      + '.sidebar-link.active{font-weight:700;}';
    document.head.appendChild(st);
  }
  const path = location.pathname;
  const aside = document.getElementById('praticien-sidebar');
  if (aside) {
    aside.className = 'hidden lg:flex flex-col w-60 bg-cream border-r border-bdr px-4 py-6 fixed top-0 left-0 h-screen z-10';
    const links = PRATICIEN_NAV.map(l => {
      if (l.spacer) return '<div class="flex-1"></div>';
      const active = path === l.href;
      return '<a href="' + l.href + '" class="sidebar-link' + (active ? ' active' : '') + '"'
        + (l.adminOnly ? ' data-admin-only' : '') + '>'
        + _pIcon(l.icon, 'w-5 h-5 shrink-0') + l.label + '</a>';
    }).join('');
    aside.innerHTML =
      '<a href="/praticien/dashboard.html" class="flex items-center gap-2.5 font-heading text-xl font-semibold text-forest-deep px-2 mb-2 block" aria-label="IVIA — Accueil">'
      + '<svg width="26" height="26" viewBox="0 0 28 28" fill="none" aria-hidden="true"><rect width="28" height="28" rx="7" fill="#2D6A4F"/><rect x="7" y="11" width="3.5" height="6" rx="1.75" fill="white"/><rect x="12.25" y="7" width="3.5" height="14" rx="1.75" fill="white"/><rect x="17.5" y="9" width="3.5" height="10" rx="1.75" fill="white"/></svg>IVIA</a>'
      + '<p class="text-xs text-muted px-2 mb-6 font-semibold uppercase tracking-wider">Espace praticien·ne</p>'
      + '<nav class="flex flex-col gap-1 flex-1">' + links + '<div id="sidebar-logout" class="mt-2"></div></nav>';
  }
  const mobile = document.getElementById('praticien-mobile-nav');
  if (mobile) {
    mobile.className = 'lg:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-bdr flex items-center justify-around px-2 py-2 z-20';
    mobile.innerHTML = PRATICIEN_NAV.filter(l => l.court).map(l => {
      const active = path === l.href;
      return '<a href="' + l.href + '" class="flex flex-col items-center gap-0.5 text-xs font-medium '
        + (active ? 'text-forest-deep' : 'text-muted') + ' px-3 py-1">'
        + _pIcon(l.icon, 'w-5 h-5') + l.court + '</a>';
    }).join('');
  }
  const logout = document.getElementById('sidebar-logout');
  if (logout && !logout.childElementCount && typeof renderLogoutButton === 'function') renderLogoutButton(logout);
  if (typeof applyAdminVisibility === 'function') applyAdminVisibility();
}

const ADMIN_NAV = [
  { href: '/admin/vue.html', label: 'Vue d\'ensemble' },
  { href: '/admin/dossiers.html', label: 'Dossiers clients' },
  { href: '/admin/comptes.html', label: 'Comptes & accès' },
  { href: '/admin/demandes.html', label: 'Demandes d\'entrée' },
  { href: '/admin/comptabilite.html', label: 'Comptabilité' },
  { href: '/admin/facturation.html', label: 'Facturation' },
  { href: '/admin/analyses.html', label: 'Analyses & droits' },
  { href: '/admin/lectures.html', label: 'Atelier des lectures' },
];

/**
 * Construit la barre latérale « Administration » dédiée dans l'élément #admin-sidebar
 * (présent sur les pages admin et sur /admin/). Interface séparée de l'espace praticien.
 * L'espace praticien, lui, n'affiche plus aucun lien admin.
 */
function renderAdminSidebar() {
  const aside = document.getElementById('admin-sidebar');
  if (!aside) return;
  // Thème sombre distinct : on est visiblement dans la console d'administration.
  aside.className = 'hidden lg:flex flex-col w-60 px-4 py-6 fixed top-0 left-0 h-screen z-10 '
    + 'bg-[#13261A] border-r border-[#22432F]';
  const base = 'flex items-center px-4 py-2.5 rounded-[10px] text-sm transition-colors';
  const idle = ' font-medium text-[#A7C4B2] hover:bg-[#1E3A28] hover:text-white';
  const on = ' font-semibold bg-forest text-white';
  const links = ADMIN_NAV.map(l => {
    const active = location.pathname === l.href;
    return `<a href="${l.href}" class="${base}${active ? on : idle}">${l.label}</a>`;
  }).join('');
  aside.innerHTML = `
    <a href="/admin/" class="font-heading text-xl font-semibold text-white px-2 mb-1 block">IVIA</a>
    <p class="text-[11px] text-sage px-2 mb-6 font-semibold uppercase tracking-[0.18em]">Administration</p>
    <nav class="flex flex-col gap-1 flex-1">
      ${links}
      <div class="flex-1"></div>
      <a href="/praticien/dashboard.html" class="${base}${idle}">← Espace praticien</a>
      <div id="admin-logout" class="mt-1"></div>
    </nav>`;
  const logout = document.getElementById('admin-logout');
  if (logout) renderLogoutButton(logout, {
    className: 'flex items-center gap-2.5 px-4 py-2.5 rounded-[10px] text-sm font-semibold '
      + 'text-red-300 hover:bg-red-500/20 hover:text-red-200 cursor-pointer',
  });
}

/**
 * Garde d'accès des pages admin : si #admin-sidebar existe mais que l'utilisateur
 * n'est pas admin, on le renvoie vers l'espace praticien. À n'appeler qu'après
 * refreshCurrentUser() (données serveur à jour) pour éviter un faux négatif.
 */
function enforceAdminPage() {
  if (document.getElementById('admin-sidebar') && !isAdminUser()) {
    location.replace('/praticien/dashboard.html');
  }
}

/**
 * Rafraîchit l'utilisateur stocké depuis /auth/me (source de vérité serveur).
 * Évite un `ivia_user` périmé : un changement de rôle ou de droit admin
 * (liste blanche) est pris en compte au prochain chargement, sans re-login.
 */
async function refreshCurrentUser() {
  if (typeof apiMe !== 'function') return;
  if (!localStorage.getItem(SESSION_KEY)) return;
  try {
    const me = await apiMe();
    if (me && me.id) setCurrentUser(me);
  } catch (e) {
    // Token invalide/expiré : laisser les gardes habituels gérer la suite.
  }
}

document.addEventListener('DOMContentLoaded', () => {
  // 1er passage immédiat depuis le cache (peut être périmé)…
  renderAdminSidebar();
  applyAdminVisibility();
  // …puis on resynchronise avec le serveur et on réapplique (rôle/droit admin à jour).
  refreshCurrentUser().then(() => {
    renderAdminSidebar();
    applyAdminVisibility();
    enforceAdminPage();
  });
});

/**
 * Injecte le bouton Déconnexion dans le noeud cible.
 * @param {HTMLElement} container — élément qui recevra le bouton
 * @param {object} [opts] — { className } pour surcharger les classes
 */
function renderLogoutButton(container, opts = {}) {
  if (!container) return;
  const cls = opts.className || 'sidebar-link text-red-500 hover:bg-red-50 hover:text-red-700 mt-2';
  const btn = document.createElement('button');
  btn.type = 'button';
  btn.className = cls;
  btn.setAttribute('aria-label', 'Se déconnecter');
  btn.innerHTML = `
    <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" aria-hidden="true">
      <path stroke-linecap="round" stroke-linejoin="round"
        d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h6a2 2 0 012 2v1"/>
    </svg>
    Déconnexion`;
  btn.addEventListener('click', logout);
  container.appendChild(btn);
}

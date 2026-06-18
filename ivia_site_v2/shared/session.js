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
    const adminPage = location.pathname.startsWith('/admin/')
      || /\/praticien\/admin-/.test(location.pathname);
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
const ADMIN_NAV = [
  { href: '/praticien/admin-vue.html', label: 'Vue d\'ensemble' },
  { href: '/praticien/admin-dossiers.html', label: 'Dossiers clients' },
  { href: '/praticien/admin-comptes.html', label: 'Comptes & accès' },
  { href: '/praticien/admin-demandes.html', label: 'Demandes d\'entrée' },
  { href: '/praticien/admin-comptabilite.html', label: 'Comptabilité' },
  { href: '/praticien/admin-facturation.html', label: 'Facturation' },
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

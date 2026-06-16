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
    location.replace('/connexion.html?retour=' + retour);
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
 * Injecte les liens d'administration dans la barre latérale praticien, uniquement
 * pour les admins. Clone le style du lien « Mon profil » de la page pour s'harmoniser
 * automatiquement (une seule source, pas N sidebars à éditer).
 */
function injectAdminLink() {
  if (!isAdminUser()) return;
  const ref = document.querySelector('aside a[href="/praticien/profil.html"]');
  if (!ref || !ref.parentNode) return;
  const liens = [
    { href: '/praticien/admin-comptes.html', label: 'Comptes (admin)' },
    { href: '/praticien/admin-demandes.html', label: 'Demandes (admin)' },
    { href: '/praticien/admin-comptabilite.html', label: 'Comptabilité (admin)' },
    { href: '/praticien/admin-facturation.html', label: 'Facturation (admin)' },
  ];
  liens.forEach(l => {
    if (document.querySelector(`aside a[href="${l.href}"]`)) return; // déjà présent (page courante)
    const link = document.createElement('a');
    link.href = l.href;
    link.className = (ref.className || '').replace(/\bactive\b/, '').trim();
    link.setAttribute('data-admin-only', '');
    link.textContent = l.label;
    ref.parentNode.insertBefore(link, ref);
  });
}

document.addEventListener('DOMContentLoaded', () => {
  injectAdminLink();
  applyAdminVisibility();
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

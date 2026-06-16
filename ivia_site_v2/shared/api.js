/**
 * IVIA — shared/api.js
 *
 * Client API vanilla JS pour l'espace statique (ivia_site_v2).
 * Miroir de 09_app_ivia_merlin/src/lib/merlin-api.ts — même endpoints, même logique.
 *
 * Swap mock → API :
 *   Dans chaque page, remplacer getMock*() par les fonctions de ce fichier.
 *   Le token JWT provient de localStorage.ivia_session.
 *
 * Base URL :
 *   - Dev  : http://localhost:8000  (même hôte, port 8000)
 *   - Prod : même protocole + hôte + port 8000 (ou proxy nginx /api/)
 *   - Override : window.IVIA_API_BASE avant de charger ce fichier
 */

// ── Base URL ─────────────────────────────────────────────────────────────────
function _apiBase() {
  if (typeof window !== 'undefined' && window.IVIA_API_BASE) return window.IVIA_API_BASE.replace(/\/$/, '');
  if (typeof window !== 'undefined') {
    // Prod : le site statique est servi sur ivia.quebec, l'API sur api.ivia.quebec (443).
    if (/(^|\.)ivia\.quebec$/.test(location.hostname)) return 'https://api.ivia.quebec';
    const proto = location.protocol;
    return `${proto}//${location.hostname}:8000`;
  }
  return 'http://127.0.0.1:8000';
}

// ── Token helper ─────────────────────────────────────────────────────────────
function _token() {
  return localStorage.getItem('ivia_session') || null;
}

// ── Fetch wrapper ─────────────────────────────────────────────────────────────
async function _req(path, { method = 'GET', body, token, publicEndpoint = false } = {}) {
  const base = _apiBase();
  const headers = { 'Content-Type': 'application/json' };
  const tok = token || (publicEndpoint ? null : _token());
  if (tok) headers['Authorization'] = `Bearer ${tok}`;

  let res;
  try {
    res = await fetch(`${base}${path}`, {
      method,
      headers,
      body: body != null ? JSON.stringify(body) : undefined,
    });
  } catch (err) {
    throw new Error(`API inaccessible sur ${base}. Vérifiez que le backend tourne. (${err.message})`);
  }

  if (res.status === 204) return null;

  const json = await res.json().catch(() => null);

  // Jeton absent/expiré/ancien format (mock '1') → on repart proprement par la connexion.
  if (res.status === 401 && !publicEndpoint) {
    localStorage.removeItem('ivia_session');
    localStorage.removeItem('ivia_user');
    location.href = '/connexion.html?retour=' + encodeURIComponent(location.pathname + location.search);
    throw new Error('Session expirée — reconnectez-vous.');
  }

  if (!res.ok) {
    const detail = typeof json?.detail === 'string' ? json.detail
      : Array.isArray(json?.detail) ? json.detail.map(e => e.msg || JSON.stringify(e)).join(' · ')
      : `Erreur ${res.status}`;
    throw new Error(detail);
  }
  return json;
}

// ── Authentification & compte ────────────────────────────────────────────────
/**
 * Connexion par courriel + mot de passe.
 * Stocke le JWT (ivia_session) et le profil (ivia_user) en localStorage.
 * @returns {Promise<{access_token, token_type, user}>}
 */
async function apiLogin(email, password) {
  const res = await _req('/api/v1/auth/login', {
    method: 'POST',
    body: { email, password },
    publicEndpoint: true,
  });
  localStorage.setItem('ivia_session', res.access_token);
  localStorage.setItem('ivia_user', JSON.stringify(res.user));
  if (res.user?.display_name) localStorage.setItem('ivia_prenom', res.user.display_name.split(' ')[0]);
  return res;
}

/**
 * Inscription publique d'un client. Déclenche le courriel de vérification.
 * @param {{email, password, display_name, redirect_path?}} payload
 * @returns {Promise<{id, email, display_name, email_sent, message}>}
 */
async function apiRegisterClient(payload) {
  return _req('/api/v1/register/client', { method: 'POST', body: payload, publicEndpoint: true });
}

/**
 * Consomme un token de vérification courriel.
 * @returns {Promise<{message}>}
 */
async function apiVerifyEmail(token) {
  return _req(`/api/v1/verify-email/${encodeURIComponent(token)}`, { publicEndpoint: true });
}

/**
 * Profil du compte connecté (source de vérité, dont email_verified).
 */
async function apiMe() {
  return _req('/api/v1/auth/me');
}

/**
 * Définit ou change le mot de passe du compte connecté.
 * current_password requis seulement si un mot de passe existe déjà.
 */
async function apiSetPassword(newPassword, currentPassword = null) {
  return _req('/api/v1/auth/set-password', {
    method: 'POST',
    body: { new_password: newPassword, current_password: currentPassword },
  });
}

// ── Paiement d'un créneau (prix serveur) ─────────────────────────────────────
/**
 * Crée la session Stripe Checkout pour un créneau en hold.
 * Le prix est fixé côté serveur — on ne transmet jamais de montant.
 * @param {{slot_id, notes?, success_url?, cancel_url?}} payload
 * @returns {Promise<{order_id, checkout_url, amount_cents, currency}>}
 */
async function bookingCheckout(payload) {
  return _req('/api/v1/bookings/checkout', { method: 'POST', body: payload });
}

/**
 * Réservation pilote tout-en-un (sans paiement) — phase pilote uniquement.
 * @param {{praticien_id, slot_date, start_time, end_time, session_type?, notes?}} payload
 */
async function pilotBook(payload) {
  return _req('/api/v1/bookings/pilot-book', { method: 'POST', body: payload });
}

// ── Espace client (authentifié) ──────────────────────────────────────────────
/** Fiche Client durable du compte connecté (404 si pas encore de dossier). */
async function getMyClient() {
  return _req('/api/v1/clients/me');
}

/**
 * Met à jour la fiche client du compte connecté (profil de détermination).
 * @param {{birth_year?, gender_identity?, birthplace?, territory_code?, ...}} payload
 */
async function updateMyClient(payload) {
  return _req('/api/v1/clients/me', { method: 'PATCH', body: payload });
}

/** Confirme un paiement SIMULÉ (mode test) — aucun débit. */
async function confirmTestPayment(orderId) {
  return _req('/api/v1/payments/test/confirm/' + encodeURIComponent(orderId), { method: 'POST' });
}

/**
 * Garde « profil complété » : redirige vers /client/mon-profil.html si le profil
 * obligatoire (tranche d'âge, genre, lieu de naissance, territoire) n'est pas rempli.
 * @returns {Promise<boolean>} true si le profil est complet (on peut continuer).
 */
async function requireCompleteProfile() {
  let c = null;
  try { c = await getMyClient(); } catch (e) { c = null; }
  if (!c || c.profile_complete === false) {
    const retour = encodeURIComponent(location.pathname + location.search);
    location.href = '/client/mon-profil.html?gate=1&retour=' + retour;
    return false;
  }
  return true;
}

/** Réservations (hold + confirmées) du compte connecté, triées par date. */
async function getMyBookings() {
  return _req('/api/v1/bookings/my');
}

/** Entrées de journal du compte connecté (plus récentes d'abord côté rendu). */
async function getMyJournal(includeArchived = false) {
  return _req('/api/v1/me/journal' + (includeArchived ? '?include_archived=true' : ''));
}

/**
 * Crée une entrée de journal.
 * @param {{body_text, entry_type?, emotional_tone?, event_year_ref?}} payload
 */
async function createMyJournalEntry(payload) {
  return _req('/api/v1/me/journal', { method: 'POST', body: payload });
}

// ── Enregistrements solo (client connecté) ───────────────────────────────────
/**
 * Envoie un enregistrement solo (base64) — transcription lancée en tâche de fond.
 * @param {{audio_data, filename?, formule?, duration_seconds?}} payload
 */
async function uploadMyRecording(payload) {
  return _req('/api/v1/me/recordings', { method: 'POST', body: payload });
}

/** Enregistrements solo du compte connecté, avec transcription quand prête. */
async function getMyRecordings() {
  return _req('/api/v1/me/recordings');
}

/**
 * Indique si une formule exige un paiement et si un crédit est déjà détenu.
 * @param {string} formule  ex. 'solo30'
 * @returns {Promise<{payant, has_credit, needs_payment, amount_cents}>}
 */
async function getSoloAccess(formule = 'solo30') {
  return _req('/api/v1/me/recordings/access?formule=' + encodeURIComponent(formule));
}

/**
 * Achète un crédit d'enregistrement solo (35 $, prix serveur).
 * @param {{success_url?, cancel_url?, client_id, intake_request_id?}} payload
 * @returns {Promise<{order_id, checkout_url, amount_cents, currency}>}
 *   Si l'offre est gratuite (mode test), checkout_url pointe directement la page de succès.
 */
async function soloRecordingCheckout(payload) {
  return _req('/api/v1/payments/stripe/public-checkout', {
    method: 'POST',
    body: {
      product_kind_code: 'solo_recording',
      product_code: 'solo_recording',
      product_label: 'Enregistrement solo · 30 min',
      fulfillment_mode_code: 'grant_entitlement_only',
      entitlement_type_code: 'solo_recording_credit',
      entitlement_quantity: 1,
      amount_cents: 0,        // écrasé par le prix serveur (anti-manipulation)
      currency: 'cad',
      ...payload,
    },
  });
}

// ── Séance express ────────────────────────────────────────────────────────────
/**
 * Praticien : crée une séance express, renvoie { session_id, token, ... }.
 * @param {{client_name?, duration_minutes, payment_status, private_notes?}} payload
 */
async function createExpressSession(payload) {
  return _req('/api/v1/sessions/express', { method: 'POST', body: payload });
}

/** Public (token) : infos d'accueil d'une séance express. */
async function getExpressSession(token) {
  return _req('/api/v1/public/express/' + encodeURIComponent(token), { publicEndpoint: true });
}

/** Public (token) : dépôt de l'enregistrement du client sur une séance express. */
async function uploadExpressRecording(token, payload) {
  return _req('/api/v1/public/express/' + encodeURIComponent(token) + '/recording',
    { method: 'POST', body: payload, publicEndpoint: true });
}

// ── Analyses de séance (praticien / clinique interne) ───────────────────────
/** Liste les notes d'analyse générées par le pipeline IA (filtrables). */
async function getSessionNotes({ sessionId, clientId } = {}) {
  const qs = new URLSearchParams();
  if (sessionId) qs.set('session_id', sessionId);
  if (clientId) qs.set('client_id', clientId);
  const s = qs.toString();
  return _req('/api/v1/session-notes' + (s ? '?' + s : ''));
}

/** Détail d'une note d'analyse. */
async function getSessionNote(id) {
  return _req('/api/v1/session-notes/' + encodeURIComponent(id));
}

/** Séances du praticien connecté (filtré côté serveur par praticien_id). */
async function listMySessions() {
  return _req('/api/v1/sessions');
}

/** Détail d'une séance (dont transcript_text). */
async function getSession(id) {
  return _req('/api/v1/sessions/' + encodeURIComponent(id));
}

/** Valider une note d'analyse (praticien/opérateur/superviseur). */
async function validateSessionNote(id, { validated = true, corrections = null } = {}) {
  return _req('/api/v1/session-notes/' + encodeURIComponent(id) + '/validate',
    { method: 'PATCH', body: { validated, corrections } });
}

/**
 * Crée un document dérivé (reformulation client). Visible au client si
 * `client_visible: true` ET la note source est validée.
 * @param {{client_id, session_id, source_note_id, title, body_text, client_visible?}} payload
 */
async function createDerivedDocument(payload) {
  return _req('/api/v1/derived-documents', { method: 'POST', body: payload });
}

/** Documents livrés au client connecté (reformulations déposées dans son espace). */
async function getMyDocuments() {
  return _req('/api/v1/me/documents');
}

/** Convertit un Blob audio en base64 (sans le préfixe data:). */
function blobToBase64(blob) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => resolve(String(reader.result).split(',')[1]);
    reader.onerror = reject;
    reader.readAsDataURL(blob);
  });
}

// ── Praticiens (public) ───────────────────────────────────────────────────────
/**
 * Liste les praticiens publics.
 * @returns {Promise<Array<{id, display_name, title_line, intro_text, spoken_languages, available_channels}>>}
 */
async function listPraticiens() {
  return _req('/api/v1/praticiens', { publicEndpoint: true });
}

// ── Créneaux disponibles (public) ────────────────────────────────────────────
/**
 * Retourne les créneaux disponibles d'un praticien sur une plage.
 * @param {string} praticienId
 * @param {string} dateFrom  YYYY-MM-DD
 * @param {string} dateTo    YYYY-MM-DD (max 90j de plage)
 * @returns {Promise<Array<AvailableSlotRecord>>}
 *
 * AvailableSlotRecord : {
 *   praticien_id, praticien_name,
 *   slot_date, start_time, end_time,
 *   session_type, session_type_label, duration_minutes,
 *   slot_id, status   // "available"|"hold"|"confirmed"|"cancelled"
 * }
 */
async function getAvailableSlots(praticienId, dateFrom, dateTo, durationMinutes) {
  const qs = new URLSearchParams({ praticien_id: praticienId, date_from: dateFrom, date_to: dateTo });
  if (durationMinutes) qs.set('duration_minutes', durationMinutes);
  return _req(`/api/v1/schedules/available?${qs}`, { publicEndpoint: true });
}

// ── Gabarit hebdomadaire praticien ───────────────────────────────────────────
/**
 * Récupère le gabarit de disponibilités du praticien connecté.
 * @returns {Promise<Array<ScheduleSlotRecord>>}
 *
 * ScheduleSlotRecord : {
 *   id, praticien_id,
 *   day_of_week (0=lundi), day_label,
 *   start_time "HH:MM:SS", end_time,
 *   session_duration_minutes, buffer_minutes,
 *   session_type, session_type_label,
 *   is_active, valid_from, valid_until,
 *   created_at, updated_at
 * }
 */
async function getMySchedule() {
  return _req('/api/v1/schedules/my');
}

/**
 * Crée un bloc de disponibilité dans le gabarit.
 * @param {{ day_of_week: number, start_time: string, end_time: string,
 *           session_duration_minutes?: number, buffer_minutes?: number,
 *           session_type?: string }} payload
 */
async function createScheduleBlock(payload) {
  return _req('/api/v1/schedules/my', { method: 'POST', body: payload });
}

/**
 * Modifie un bloc de disponibilité.
 */
async function updateScheduleBlock(blockId, payload) {
  return _req(`/api/v1/schedules/my/${blockId}`, { method: 'PATCH', body: payload });
}

/**
 * Supprime un bloc de disponibilité.
 */
async function deleteScheduleBlock(blockId) {
  return _req(`/api/v1/schedules/my/${blockId}`, { method: 'DELETE' });
}

// ── Exceptions praticien ──────────────────────────────────────────────────────
/**
 * Retourne les exceptions du praticien (congés, ajouts ponctuels).
 */
async function getMyExceptions() {
  return _req('/api/v1/schedules/my/exceptions');
}

/**
 * Crée une exception.
 * @param {{ exception_date: string, exception_type?: "blocked"|"extra",
 *           start_time?: string|null, end_time?: string|null, reason?: string }} payload
 */
async function createScheduleException(payload) {
  return _req('/api/v1/schedules/my/exceptions', { method: 'POST', body: payload });
}

/**
 * Supprime une exception.
 */
async function deleteScheduleException(excId) {
  return _req(`/api/v1/schedules/my/exceptions/${excId}`, { method: 'DELETE' });
}

// ── Réservations client ───────────────────────────────────────────────────────
/**
 * Place un hold de 15 min sur un créneau.
 * @param {{ slot_id?: string, praticien_id?: string, slot_date?: string,
 *           start_time?: string, end_time?: string, session_type?: string }} payload
 * @returns {Promise<BookingSlotRecord>}
 */
async function holdSlot(payload) {
  return _req('/api/v1/bookings/hold', { method: 'POST', body: payload });
}

/**
 * Confirme la réservation après paiement.
 * @param {string} slotId
 * @param {string|null} notes
 */
async function confirmSlot(slotId, notes = null) {
  return _req('/api/v1/bookings/confirm', { method: 'POST', body: { slot_id: slotId, notes } });
}

/**
 * Annule une réservation.
 */
async function cancelSlot(slotId) {
  return _req('/api/v1/bookings/cancel', { method: 'POST', body: { slot_id: slotId } });
}

// ── Helpers utilitaires ──────────────────────────────────────────────────────
const JOURS_FR = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'];
const JOURS_LONG = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'];
const MOIS_FR = ['janvier','février','mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre'];

/**
 * Retourne { from: 'YYYY-MM-DD', to: 'YYYY-MM-DD' } pour une semaine donnée.
 * @param {number} weekOffset  0 = semaine courante, ±1 = semaines adjacentes
 */
function getWeekBounds(weekOffset = 0) {
  const now = new Date();
  const day = now.getDay(); // 0=dim
  const monday = new Date(now);
  monday.setDate(now.getDate() - (day === 0 ? 6 : day - 1) + weekOffset * 7);
  monday.setHours(0, 0, 0, 0);
  const sunday = new Date(monday);
  sunday.setDate(monday.getDate() + 6);
  return {
    from: monday.toISOString().slice(0, 10),
    to:   sunday.toISOString().slice(0, 10),
    monday,
  };
}

/**
 * Retourne { from, to } pour un mois donné.
 * @param {Date} monthDate  Premier jour du mois (ou n'importe quel jour)
 */
function getMonthBounds(monthDate) {
  const d = new Date(monthDate);
  d.setDate(1);
  const from = d.toISOString().slice(0, 10);
  d.setMonth(d.getMonth() + 1);
  d.setDate(0); // dernier jour du mois
  const to = d.toISOString().slice(0, 10);
  return { from, to };
}

/**
 * "HH:MM:SS" → "HHhMM"
 */
function formatHeure(timeStr) {
  if (!timeStr) return '';
  const [h, m] = timeStr.split(':');
  return m === '00' ? `${parseInt(h)}h` : `${parseInt(h)}h${m}`;
}

/**
 * "YYYY-MM-DD" → "Lundi 10 juin"
 */
function formatDateCourteLocale(iso) {
  const d = new Date(iso + 'T12:00:00');
  const jour = JOURS_LONG[d.getDay() === 0 ? 6 : d.getDay() - 1];
  return `${jour} ${d.getDate()} ${MOIS_FR[d.getMonth()]}`;
}

// ── Admin · demandes d'entrée (intake) ───────────────────────────────────────
/** Liste des demandes d'entrée (file d'arrivée via /rendez-vous). */
async function adminListIntake() {
  return _req('/api/v1/intake-requests');
}
/** Traite une demande : statut + note. */
async function adminUpdateIntakeHandling(id, handling_status_code, handling_notes) {
  return _req('/api/v1/intake-requests/' + encodeURIComponent(id) + '/handling',
    { method: 'PATCH', body: { handling_status_code, handling_notes } });
}

// ── Admin · comptabilité (grand livre) ───────────────────────────────────────
/** Résumé comptable agrégé sur une période (cents). */
async function adminAccountingSummary(dateFrom, dateTo) {
  return _req(`/api/v1/admin/accounting/summary?date_from=${dateFrom}&date_to=${dateTo}`);
}
/** Grand livre ligne à ligne (encaissements ventilés) sur une période. */
async function adminAccountingLedger(dateFrom, dateTo) {
  return _req(`/api/v1/admin/accounting/ledger?date_from=${dateFrom}&date_to=${dateTo}`);
}

// ── Admin · comptes & accès ───────────────────────────────────────────────────
/** Liste des comptes (filtre courriel/nom optionnel). */
async function adminListAccounts(q) {
  return _req('/api/v1/admin/accounts' + (q ? ('?q=' + encodeURIComponent(q)) : ''));
}
/** Renvoie le lien de confirmation au courriel du compte. */
async function adminResendVerification(id) {
  return _req('/api/v1/admin/accounts/' + encodeURIComponent(id) + '/resend-verification', { method: 'POST' });
}
/** Marque le courriel comme vérifié (dépannage). */
async function adminVerifyAccount(id) {
  return _req('/api/v1/admin/accounts/' + encodeURIComponent(id) + '/verify', { method: 'POST' });
}
/** Change le rôle métier du compte. */
async function adminSetRole(id, role) {
  return _req('/api/v1/admin/accounts/' + encodeURIComponent(id) + '/role', { method: 'POST', body: { role } });
}
/** Suspend (true) ou réactive (false) le compte. */
async function adminSetStatus(id, suspend) {
  return _req('/api/v1/admin/accounts/' + encodeURIComponent(id) + '/status', { method: 'POST', body: { suspend } });
}

// ── Admin · interrupteurs de facturation par offre ───────────────────────────
/**
 * Lit l'état payant/gratuit de chaque offre.
 * @returns {Promise<{flags: Object<string, boolean>}>}  coché=payant
 */
async function apiGetBillingFlags() {
  return _req('/api/v1/admin/billing-flags');
}

/**
 * Met à jour les interrupteurs. Décoché = gratuit (mode test).
 * @param {Object<string, boolean>} flags  { offre_code: payant }
 * @returns {Promise<{flags: Object<string, boolean>}>}  état après mise à jour
 */
async function apiSetBillingFlags(flags) {
  return _req('/api/v1/admin/billing-flags', { method: 'PATCH', body: { flags } });
}

// Export implicite — toutes les fonctions sont disponibles en global
// dans les pages HTML qui incluent ce script.

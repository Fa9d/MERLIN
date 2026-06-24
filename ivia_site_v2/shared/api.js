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

  if (!res.ok) {
    const detail = typeof json?.detail === 'string' ? json.detail
      : Array.isArray(json?.detail) ? json.detail.map(e => e.msg || JSON.stringify(e)).join(' · ')
      : `Erreur ${res.status}`;
    throw new Error(detail);
  }
  return json;
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
async function getAvailableSlots(praticienId, dateFrom, dateTo) {
  const qs = new URLSearchParams({ praticien_id: praticienId, date_from: dateFrom, date_to: dateTo });
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

/**
 * Réservation pilote tout-en-un (sans Stripe).
 * Hold + crédit gratuit automatique + confirmation en une seule requête.
 * @param {{ praticien_id, slot_date, start_time, end_time, session_type?, notes? }} payload
 * @returns {Promise<BookingSlotRecord & { session_id: string }>}
 */
async function pilotBookSlot(payload) {
  return _req('/api/v1/bookings/pilot-book', { method: 'POST', body: payload });
}

/**
 * Retourne le premier créneau disponible d'un praticien sur les 60 prochains jours.
 * @param {string} praticienId
 * @returns {Promise<{slot_date, start_time, end_time}|null>}
 */
async function getNextAvailableSlot(praticienId) {
  const from = new Date();
  const to = new Date();
  to.setDate(to.getDate() + 60);
  const dateFrom = from.toISOString().slice(0, 10);
  const dateTo   = to.toISOString().slice(0, 10);
  const slots = await getAvailableSlots(praticienId, dateFrom, dateTo);
  return Array.isArray(slots) && slots.length > 0 ? slots[0] : null;
}

// ── Sessions (praticien) ──────────────────────────────────────────────────────

/**
 * Démarre une séance (status → in_progress).
 * @param {string} sessionId
 * @returns {Promise<SessionRead>}
 */
async function startSession(sessionId) {
  return _req(`/api/v1/sessions/${sessionId}/start`, { method: 'POST', body: {} });
}

/**
 * Upload un fichier audio WebM pour transcription + analyse AI.
 * @param {string} sessionId
 * @param {Blob} audioBlob
 * @returns {Promise<{ session_id, audio_file_path, pipeline_queued }>}
 */
async function uploadSessionAudio(sessionId, audioBlob) {
  // Encode blob to base64 (avoids python-multipart requirement on server)
  const arrayBuffer = await audioBlob.arrayBuffer();
  const bytes = new Uint8Array(arrayBuffer);
  let binary = '';
  for (let i = 0; i < bytes.byteLength; i++) binary += String.fromCharCode(bytes[i]);
  const audio_data = btoa(binary);
  const filename = `session_${sessionId}.webm`;
  return _req(`/api/v1/sessions/${sessionId}/upload-audio`, {
    method: 'POST',
    body: { audio_data, filename },
  });
}

/**
 * Clôture une séance (requiert transcript_text).
 * Déclenche l'analyse AI si transcript_text fourni.
 * @param {string} sessionId
 * @param {{ session_status_code, presenting_topic_text?, session_highlights_text?,
 *           transcript_text?, operator_assessment_text?, client_visible? }} payload
 */
async function closeSession(sessionId, payload) {
  return _req(`/api/v1/sessions/${sessionId}/close`, { method: 'POST', body: payload });
}

// ── Enregistrements solo (client connecté) ────────────────────────────────────
/**
 * Convertit un Blob audio en base64 « nu » (sans préfixe data:…;base64,) —
 * format attendu par le backend (base64.b64decode).
 * @param {Blob} blob
 * @returns {Promise<string>}
 */
function blobToBase64(blob) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onerror = () => reject(new Error("Lecture du fichier audio impossible."));
    reader.onload = () => {
      const result = String(reader.result || '');
      const comma = result.indexOf(',');
      resolve(comma >= 0 ? result.slice(comma + 1) : result);
    };
    reader.readAsDataURL(blob);
  });
}

/**
 * Envoie un enregistrement solo (audio base64) pour transcription en tâche de fond.
 * @param {{ audio_data: string, filename?: string, formule?: string,
 *           duration_seconds?: number }} payload
 * @returns {Promise<MyRecordingRead>}  // status 202 — transcription en file
 */
async function uploadMyRecording(payload) {
  return _req('/api/v1/me/recordings', { method: 'POST', body: payload });
}

/**
 * Liste les enregistrements solo du client connecté (avec statut de transcription).
 * @returns {Promise<Array<{ id, formule, created_at, actual_end_at, duration_minutes,
 *           status, transcript_ready, transcript_text }>>}
 */
async function getMyRecordings() {
  return _req('/api/v1/me/recordings');
}

/**
 * Indique si une formule exige un paiement et si le client a déjà un crédit.
 * @param {string} formule
 * @returns {Promise<{ formule, requires_payment, has_credit }>}
 */
async function getMyRecordingAccess(formule = 'solo30') {
  const qs = new URLSearchParams({ formule });
  return _req(`/api/v1/me/recordings/access?${qs}`);
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

// Export implicite — toutes les fonctions sont disponibles en global
// dans les pages HTML qui incluent ce script.

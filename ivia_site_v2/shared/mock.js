/**
 * IVIA — Données mock (développement frontend)
 *
 * Simule les réponses API pour le développement des interfaces.
 * Quand l'API sera connectée, remplacer chaque fonction getMock*()
 * par un appel fetch correspondant — les renderers HTML ne changent pas.
 *
 * Contrat de données : chaque structure reflète le schéma API prévu.
 */

// ── Utilisateur connecté ─────────────────────────────────────────────────────
const MOCK_USER = {
  id:                'usr_001',
  prenom:            'Marie',
  nom:               'Tremblay',
  email:             'marie.tremblay@exemple.ca',
  role:              'client',
  courriel_verifie:  false,
  nouveau_compte:    false,
  avatar_url:        null,
  praticien_id:      'pra_001',
};

// ── Praticien assigné ────────────────────────────────────────────────────────
const MOCK_PRATICIEN = {
  id:       'pra_001',
  prenom:   'Mylène',
  nom:      'Pelletier',
  approche: 'Psychologie somato-narrative',
  avatar_url: null,
};

// ── Prochaine séance ─────────────────────────────────────────────────────────
const MOCK_PROCHAINE_SEANCE = {
  id:              'sea_003',
  praticien:       MOCK_PRATICIEN,
  date_iso:        '2026-06-10T14:00:00',
  duree_min:       60,
  format:          'Audio en direct',
  tags:            ['Présence', 'Ancrage corporel'],
  statut:          'confirmee',   // confirmee | en_attente | annulee
  lien_rejoindre:  '#',
};

// ── Historique séances ───────────────────────────────────────────────────────
const MOCK_SEANCES = [
  {
    id: 'sea_001',
    praticien:  MOCK_PRATICIEN,
    date_iso:   '2026-05-15T14:00:00',
    duree_min:  60,
    format:     'Audio en direct',
    tags:       ['Ancrage', 'Corps'],
    statut:     'complete',
    audio_resume: { duree: '4 min 12', url: '/client/audio-resume.html' },
    notes_client: '',
  },
  {
    id: 'sea_002',
    praticien:  MOCK_PRATICIEN,
    date_iso:   '2026-04-28T10:00:00',
    duree_min:  60,
    format:     'Audio en direct',
    tags:       ['Émotions', 'Présence'],
    statut:     'complete',
    audio_resume: null,
    notes_client: '',
  },
  {
    id: 'sea_000',
    praticien:  MOCK_PRATICIEN,
    date_iso:   '2026-04-10T14:00:00',
    duree_min:  60,
    format:     'Audio en direct',
    tags:       ['Découverte'],
    statut:     'complete',
    audio_resume: null,
    notes_client: '',
  },
  MOCK_PROCHAINE_SEANCE,
];

// ── Journal ──────────────────────────────────────────────────────────────────
const MOCK_JOURNAL = [
  {
    id:        'j_001',
    titre:     'Sur la lenteur — ne pas confondre repos et fuite',
    date_iso:  '2026-05-29',
    registres: ['corporel', 'émotionnel'],
    extrait:   'Aujourd\'hui j\'ai remarqué que me reposer différait de fuir. La lenteur peut être active.',
    humeur:    4,   // 1–5
    prive:     false,
  },
  {
    id:        'j_002',
    titre:     'Après la séance avec Mylène — quelques images',
    date_iso:  '2026-05-22',
    registres: ['relationnel'],
    extrait:   'Des images sont remontées pendant la séance. Un terrain mou, une lumière tamisée.',
    humeur:    3,
    prive:     false,
  },
  {
    id:        'j_003',
    titre:     'Premier matin sans résistance',
    date_iso:  '2026-05-10',
    registres: ['corporel'],
    extrait:   'Je me suis levée sans cette pesanteur habituelle.',
    humeur:    5,
    prive:     true,
  },
  {
    id:        'j_004',
    titre:     'Résistance au changement',
    date_iso:  '2026-05-03',
    registres: ['émotionnel', 'mental'],
    extrait:   'Une peur diffuse avant la séance. Mais ça s\'est ouvert.',
    humeur:    2,
    prive:     false,
  },
  {
    id:        'j_005',
    titre:     'Note après séance découverte',
    date_iso:  '2026-04-12',
    registres: ['relationnel', 'corporel'],
    extrait:   'Premier contact avec Mylène. Je ne savais pas trop à quoi m\'attendre.',
    humeur:    3,
    prive:     false,
  },
];

// ── Statistiques dashboard ───────────────────────────────────────────────────
const MOCK_STATS = {
  nb_seances:        3,
  nb_journal:        MOCK_JOURNAL.length,
  ancrage_complete:  false,
  prochaine_seance:  MOCK_PROCHAINE_SEANCE,
};

// ── Résumé audio disponible ──────────────────────────────────────────────────
const MOCK_AUDIO_DISPONIBLE = {
  seance_id:   'sea_001',
  titre:       'Séance du 15 mai',
  praticien:   MOCK_PRATICIEN,
  duree_label: '4 min 12',
  url:         '/client/audio-resume.html',
};

// ── Progression profil dimensionnel (arc métacognitif) ───────────────────────
// Chaque entrée = snapshot du profil_dim à un moment donné.
// réflexion ∈ {1,2,3} est l'indicateur-clé d'internalisation métacognitive.
const MOCK_PROFIL_PROGRESSION = [
  {
    label:    'Ancrage initial',
    date_iso: '2026-04-10',
    seq:      0,
    profil_dim: { presence:1, comprehension:3, choix:1, sol:2, vivant:1, reflexion:1 },
  },
  {
    label:    'Séance 1',
    date_iso: '2026-04-28',
    seq:      1,
    profil_dim: { presence:1, comprehension:3, choix:1, sol:2, vivant:2, reflexion:1 },
  },
  {
    label:    'Séance 2',
    date_iso: '2026-05-15',
    seq:      2,
    profil_dim: { presence:2, comprehension:3, choix:1, sol:2, vivant:2, reflexion:1 },
  },
  {
    label:    'Séance 3',
    date_iso: '2026-05-27',
    seq:      3,
    profil_dim: { presence:2, comprehension:3, choix:2, sol:2, vivant:2, reflexion:2 },
  },
];

// Jalons narratifs auto-générés depuis les seuils dimensionnels
const JALONS = [
  { id:'j1', dim:'vivant',        seuil:2, texte:'Tu accueilles ta nature changeante' },
  { id:'j2', dim:'presence',      seuil:2, texte:'Tu habites davantage le moment présent' },
  { id:'j3', dim:'sol',           seuil:2, texte:'Tu trouves appui dans tes racines' },
  { id:'j4', dim:'choix',         seuil:2, texte:'Tu exprimes tes préférences avec plus de clarté' },
  { id:'j5', dim:'comprehension', seuil:3, texte:'Tu décodes les systèmes qui t\'entourent' },
  { id:'j6', dim:'reflexion',     seuil:2, texte:'Tu commences à nommer tes propres schémas' },
];

// ── Accesseurs (interface pour remplacement API) ─────────────────────────────

function getMockUser()            { return Promise.resolve(MOCK_USER); }
function getMockStats()           { return Promise.resolve(MOCK_STATS); }
function getMockSeances()         { return Promise.resolve(MOCK_SEANCES); }
function getMockJournal()         { return Promise.resolve(MOCK_JOURNAL); }
function getMockAudioDisponible() { return Promise.resolve(MOCK_AUDIO_DISPONIBLE); }
function getMockProgression()     { return Promise.resolve([...MOCK_PROFIL_PROGRESSION]); }
function getMockJalons()          { return Promise.resolve([...JALONS]); }

// ── Helpers utilitaires ──────────────────────────────────────────────────────

/**
 * Calcule "Dans X jours" / "Aujourd'hui" / "Dans X h" à partir d'un ISO string.
 * @param {string} isoDate
 * @returns {string}
 */
function countdownLabel(isoDate) {
  const now  = new Date();
  const cible = new Date(isoDate);
  const diffMs = cible - now;
  if (diffMs < 0)         return 'Passée';
  const diffH = Math.floor(diffMs / 3600000);
  if (diffH < 2)          return 'Maintenant';
  if (diffH < 24)         return `Dans ${diffH} h`;
  const diffJ = Math.ceil(diffMs / 86400000);
  if (diffJ === 1)        return 'Demain';
  return `Dans ${diffJ} jours`;
}

/**
 * Formate une date ISO en "Lundi 10 juin 2026 · 14h00"
 * @param {string} isoDate
 * @returns {string}
 */
function formatDateSeance(isoDate) {
  const d = new Date(isoDate);
  const jour  = d.toLocaleDateString('fr-CA', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
  const heure = d.toLocaleTimeString('fr-CA', { hour: '2-digit', minute: '2-digit' }).replace(':', 'h');
  return `${jour.charAt(0).toUpperCase() + jour.slice(1)} · ${heure}`;
}

/**
 * Formate une date ISO courte : "29 mai 2026"
 * @param {string} isoDate
 * @returns {string}
 */
function formatDateCourte(isoDate) {
  return new Date(isoDate).toLocaleDateString('fr-CA', { day: 'numeric', month: 'long', year: 'numeric' });
}

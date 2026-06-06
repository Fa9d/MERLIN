/**
 * IVIA — Données mock PRATICIEN (développement frontend)
 *
 * Simule les réponses API côté praticien.
 * Swap : remplacer chaque getMock*() par fetch('/api/v1/praticien/...')
 */

// ── Praticien connecté ────────────────────────────────────────────────────────
const MOCK_PRAT_USER = {
  id:      'pra_001',
  prenom:  'Mylène',
  nom:     'Pelletier',
  email:   'mylene.pelletier@ivia.quebec',
  role:    'praticien',
  approche:'Psychologie somato-narrative',
  avatar_url: null,
};

// ── Clients ───────────────────────────────────────────────────────────────────
const MOCK_CLIENTS = [
  {
    id:          'usr_001',
    prenom:      'Marie',
    nom:         'Tremblay',
    initiales:   'MT',
    statut:      'active',
    registres:   ['Corporel', 'Émotionnel'],
    derniere_seance: '2026-05-27',
    prochaine_seance:'2026-06-10',
    nb_seances:  6,
    nb_journal:  8,
    registre_dominant: 'Émotionnel',
    journal_recent: [
      { date:'2026-05-29', registres:['Corporel','Émotionnel'], extrait:'«\u00a0Aujourd\'hui j\'ai remarqué que me reposer différait de fuir.\u00a0»' },
      { date:'2026-05-22', registres:['Relationnel'],           extrait:'«\u00a0Des images sont remontées pendant la séance.\u00a0»' },
    ],
    notes_prat: '',
    livraison_en_attente: true,
    livraison_date: '2026-05-27',
    livraison_duree: '52 min',
    livraison_registres: ['Émotionnel', 'Relationnel'],
    journal_semaine: 3,
  },
  {
    id:          'usr_002',
    prenom:      'Théo',
    nom:         'Marchand',
    initiales:   'TM',
    statut:      'actif',
    registres:   ['Mental', 'Spirituel'],
    derniere_seance: '2026-05-22',
    prochaine_seance:'2026-06-05',
    nb_seances:  4,
    nb_journal:  3,
    registre_dominant: 'Spirituel',
    journal_recent: [
      { date:'2026-05-27', registres:['Spirituel','Mental'], extrait:'«\u00a0Quelque chose se dépose. Je ne sais pas encore quoi.\u00a0»' },
    ],
    notes_prat: '',
    livraison_en_attente: true,
    livraison_date: '2026-05-22',
    livraison_duree: '48 min',
    livraison_registres: ['Spirituel'],
    journal_semaine: 1,
  },
  {
    id:          'usr_003',
    prenom:      'Sophie',
    nom:         'Racine',
    initiales:   'SR',
    statut:      'inactive',
    registres:   ['Relationnel'],
    derniere_seance: '2026-04-15',
    prochaine_seance: null,
    nb_seances:  2,
    nb_journal:  0,
    registre_dominant: 'Relationnel',
    journal_recent: [],
    notes_prat: '',
    livraison_en_attente: false,
    livraison_date: null,
    livraison_duree: null,
    livraison_registres: [],
    journal_semaine: 0,
  },
];

// ── Stats financières / qualitatives ──────────────────────────────────────────
const MOCK_PRAT_STATS = {
  revenus_mois:       540,
  revenus_mois_delta: '+12 %',
  seances_livrees:    9,
  seances_planifiees: 5,
  taux_presence:      88,
  clients_actifs:     2,
  clients_en_attente: 1,
  revenu_moy_seance:  60,
  revenus_cumules:    2340,
  revenus_cumules_depuis: 'mars 2026',
  satisfaction:       4.8,
  presence_auto:      4.2,
  nps:                67,
  journal_post_seance_ratio: '6 / 9',
};

// ── Créneaux agenda (semaine en cours) ────────────────────────────────────────
// Format : clé "AAAA-MM-JJ_HH:MM", valeur : "reserve" | "disponible" | "bloque"
// On génère dynamiquement pour la semaine contenant aujourd'hui
function buildMockAgendaSlots() {
  const slots = {};
  const now = new Date();
  const day = now.getDay();
  const diff = (day === 0 ? -6 : 1 - day);
  const monday = new Date(now);
  monday.setDate(now.getDate() + diff);
  monday.setHours(0, 0, 0, 0);

  // Réservations hardcodées (jours relatifs au lundi 0=lun, …)
  const reservations = [
    { jour: 1, heure: '09:00', client: 'Marie T.' },  // mardi 9h
    { jour: 1, heure: '10:00', client: 'Théo M.' },   // mardi 10h
    { jour: 3, heure: '14:00', client: 'Marie T.' },  // jeudi 14h
    { jour: 4, heure: '11:00', client: 'Sophie R.' }, // vendredi 11h
  ];

  reservations.forEach(r => {
    const d = new Date(monday);
    d.setDate(monday.getDate() + r.jour);
    const key = `${d.toISOString().slice(0, 10)}_${r.heure}`;
    slots[key] = 'reserve';
  });

  // Disponibles
  const disponibles = [
    { jour: 0, heure: '10:00' },
    { jour: 0, heure: '14:00' },
    { jour: 2, heure: '09:00' },
    { jour: 2, heure: '15:00' },
    { jour: 4, heure: '14:00' },
  ];
  disponibles.forEach(r => {
    const d = new Date(monday);
    d.setDate(monday.getDate() + r.jour);
    const key = `${d.toISOString().slice(0, 10)}_${r.heure}`;
    slots[key] = 'disponible';
  });

  return slots;
}

// ── Accesseurs (interface pour remplacement API) ──────────────────────────────

function getMockPratUser()   { return Promise.resolve({ ...MOCK_PRAT_USER }); }
function getMockClients()    { return Promise.resolve([...MOCK_CLIENTS]); }
function getMockPratStats()  { return Promise.resolve({ ...MOCK_PRAT_STATS }); }
function getMockAgendaSlots(){ return Promise.resolve(buildMockAgendaSlots()); }

function getMockLivraisons() {
  return Promise.resolve(
    MOCK_CLIENTS.filter(c => c.livraison_en_attente)
  );
}

// ── Helpers ───────────────────────────────────────────────────────────────────
function formatDateCourte(iso) {
  if (!iso) return '—';
  const [y, m, d] = iso.split('-');
  const mois = ['jan.','fév.','mars','avr.','mai','juin','juil.','août','sept.','oct.','nov.','déc.'];
  return `${parseInt(d)} ${mois[parseInt(m)-1]} ${y}`;
}

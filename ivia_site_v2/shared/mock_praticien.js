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

// ── Compte-rendus de séance (avec double radar client/praticien) ──────────────
// profil_client_dim = snapshot du profil_dim client AU MOMENT de la séance
// profil_prat_dim   = évaluation de l'intervention par le praticien
//   { ancrage, ecoute, regulation, cadrage, agentivite, ethique } ∈ {1,2,3}
const MOCK_COMPTE_RENDUS = [
  {
    id:           'cr_003',
    seance_id:    'sea_003',
    client_id:    'usr_001',
    client_prenom:'Marie',
    date_seance:  '2026-05-27',
    duree_min:    60,
    profil_client_dim: { presence:2, comprehension:3, choix:2, sol:2, vivant:2, reflexion:2 },
    profil_prat_dim:   { ancrage:3, ecoute:3, regulation:2, cadrage:1, agentivite:2, ethique:3 },
    texte_cr: 'Séance marquante : Marie a spontanément nommé un schéma récurrent sans que je le désigne en premier. La réflexivité s\'installe. J\'ai volontairement réduit le guidage narratif pour laisser de l\'espace à l\'agentivité.',
    registres_travailles: ['Corporel', 'Émotionnel', 'Réflexif'],
    intentions_prochaine: 'Continuer à réduire le cadrage narratif. Observer si le Choix se consolide. Tenter une entrée par le registre Sol pour ancrer les nouvelles capacités.',
    statut: 'redige',
  },
  {
    id:           'cr_002',
    seance_id:    'sea_002',
    client_id:    'usr_001',
    client_prenom:'Marie',
    date_seance:  '2026-05-15',
    duree_min:    60,
    profil_client_dim: { presence:2, comprehension:3, choix:1, sol:2, vivant:2, reflexion:1 },
    profil_prat_dim:   { ancrage:3, ecoute:3, regulation:3, cadrage:2, agentivite:1, ethique:2 },
    texte_cr: 'Fort travail d\'ancrage et d\'écoute pré-verbale. La Présence de Marie grandit. Le Choix reste faible — l\'accompagnement porte encore beaucoup de ce côté.',
    registres_travailles: ['Corporel', 'Émotionnel'],
    intentions_prochaine: 'Introduire des questions ouvertes sur les préférences et les limites pour stimuler la dimension Choix.',
    statut: 'redige',
  },
  {
    id:           'cr_001',
    seance_id:    'sea_001',
    client_id:    'usr_001',
    client_prenom:'Marie',
    date_seance:  '2026-04-28',
    duree_min:    60,
    profil_client_dim: { presence:1, comprehension:3, choix:1, sol:2, vivant:2, reflexion:1 },
    profil_prat_dim:   { ancrage:3, ecoute:3, regulation:3, cadrage:2, agentivite:1, ethique:2 },
    texte_cr: 'Première séance après ancrage. Marie est dans la Compréhension — elle décrit bien, mais le rapport au corps et à la présence est encore mince. L\'accompagnement est très soutenant.',
    registres_travailles: ['Corporel', 'Cognitif'],
    intentions_prochaine: 'Ralentir. Moins de cadrage, plus de présence à la texture de l\'expérience.',
    statut: 'redige',
  },
];

// ── Accesseurs (interface pour remplacement API) ──────────────────────────────

function getMockPratUser()   { return Promise.resolve({ ...MOCK_PRAT_USER }); }
function getMockClients()    { return Promise.resolve([...MOCK_CLIENTS]); }
function getMockPratStats()  { return Promise.resolve({ ...MOCK_PRAT_STATS }); }
function getMockAgendaSlots(){ return Promise.resolve(buildMockAgendaSlots()); }
function getMockCompteRendus() { return Promise.resolve([...MOCK_COMPTE_RENDUS]); }
function getMockCompteRendu(seanceId) {
  const cr = MOCK_COMPTE_RENDUS.find(c => c.seance_id === seanceId);
  return Promise.resolve(cr || MOCK_COMPTE_RENDUS[0]);
}

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

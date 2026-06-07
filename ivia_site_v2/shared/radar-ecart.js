/**
 * IVIA — shared/radar-ecart.js
 *
 * Composant Chart.js : double radar client/praticien avec zones d'écart colorées.
 * Usage :
 *   const rc = new RadarEcart(canvasEl, profilClient, profilPraticien);
 *   rc.render();
 *
 * profilClient    = { presence, comprehension, choix, sol, vivant, reflexion }
 *                   valeurs ∈ {1, 2, 3}
 * profilPraticien = { ancrage, ecoute, regulation, cadrage, agentivite, ethique }
 *                   valeurs ∈ {1, 2, 3}
 *
 * Les paires dimensionnelles sont :
 *   Vivant cluster  : presence ↔ ancrage | sol ↔ ecoute | vivant ↔ regulation
 *   Société cluster : comprehension ↔ cadrage | choix ↔ agentivite | reflexion ↔ ethique
 *
 * Quand remplacer par l'API :
 *   Remplacer les objets profilClient / profilPraticien par les valeurs retournées
 *   par GET /api/v1/seance/{id}/analyse — les labels et la logique de calcul ne changent pas.
 */

// ── Constantes de couleurs ────────────────────────────────────────────────────
const RC_COLORS = {
  client:          'rgba(74,  124,  89,  0.55)',   // forest vert
  clientBorder:    '#4A7C59',
  praticien:       'rgba(45,  106,  79,  0.20)',   // forest-deep transparent
  praticienBorder: '#2D6A4F',
  compensation:    'rgba(74,  124,  89,  0.25)',   // vert = praticien > client dans zone faible
  collusion:       'rgba(217, 119,   6,  0.20)',   // amber = praticien suit le fort du client
  angleMort:       'rgba(220,  38,  38,  0.25)',   // rouge = vide non couvert
  resonance:       'rgba(240, 247, 242,  0.0)',    // transparent = alignement
};

// ── Ordre des dimensions dans le radar ────────────────────────────────────────
// Alternance Vivant / Société pour un radar lisible
const RC_DIMS = [
  { label: 'Présence',       clientKey: 'presence',      pratKey: 'ancrage',     cluster: 'vivant'  },
  { label: 'Compréhension',  clientKey: 'comprehension', pratKey: 'cadrage',     cluster: 'societe' },
  { label: 'Sol',            clientKey: 'sol',           pratKey: 'ecoute',      cluster: 'vivant'  },
  { label: 'Choix',          clientKey: 'choix',         pratKey: 'agentivite',  cluster: 'societe' },
  { label: 'Vivant·e',       clientKey: 'vivant',        pratKey: 'regulation',  cluster: 'vivant'  },
  { label: 'Réflexion',      clientKey: 'reflexion',     pratKey: 'ethique',     cluster: 'societe' },
];

// ── Calcul des métriques d'écart ──────────────────────────────────────────────
/**
 * Pour chaque dimension, calcule la nature de l'écart.
 * @param {Object} client  - profil_dim du client
 * @param {Object} prat    - profil_prat_dim du praticien
 * @returns {Array<{label, clientVal, pratVal, gap, nature, score}>}
 */
function computeEcartDims(client, prat) {
  return RC_DIMS.map(dim => {
    const cv = client[dim.clientKey] || 1;
    const pv = prat[dim.pratKey]     || 1;
    const gap = pv - cv;   // positif = praticien surpasse la dimension client

    let nature;
    if      (cv <= 1 && pv >= 2) nature = 'compensation';  // praticien couvre le vide → sain
    else if (cv >= 3 && pv >= 3) nature = 'collusion';     // les deux forts → risque dépendance
    else if (cv <= 1 && pv <= 1) nature = 'angle_mort';    // vide non couvert → critique
    else                          nature = 'resonance';     // alignement

    return { ...dim, clientVal: cv, pratVal: pv, gap, nature };
  });
}

/**
 * Calcule les scores d'adéquation globaux et par cluster.
 * @param {Array} dims - sortie de computeEcartDims
 * @returns {{ adequation: number, compensation: number, angleMort: number, collusion: number,
 *             vivant: {score, label}, societe: {score, label} }}
 */
function computeAdequation(dims) {
  let comp = 0, mort = 0, collu = 0;
  dims.forEach(d => {
    if (d.nature === 'compensation') comp++;
    else if (d.nature === 'angle_mort') mort++;
    else if (d.nature === 'collusion') collu++;
  });
  const total = comp + mort + collu + (dims.length - comp - mort - collu);
  const adequation = Math.round(comp / (comp + mort + Math.max(collu * 0.5, 0) + 0.01) * 100);

  const vivantDims   = dims.filter(d => d.cluster === 'vivant');
  const societeDims  = dims.filter(d => d.cluster === 'societe');
  const clusterScore = (arr) => {
    const c = arr.filter(d => d.nature === 'compensation').length;
    const m = arr.filter(d => d.nature === 'angle_mort').length;
    if (m > 0)     return { score: 'bas',   label: 'Angle mort présent' };
    if (c >= 2)    return { score: 'fort',  label: 'Bonne couverture' };
    return           { score: 'moyen', label: 'Couverture partielle' };
  };

  return {
    adequation: Math.min(adequation, 100),
    compensation: comp,
    angleMort: mort,
    collusion: collu,
    vivant:  clusterScore(vivantDims),
    societe: clusterScore(societeDims),
  };
}

// ── Classe principale ─────────────────────────────────────────────────────────
class RadarEcart {
  /**
   * @param {HTMLCanvasElement} canvas
   * @param {Object} profilClient    - { presence, comprehension, choix, sol, vivant, reflexion }
   * @param {Object} profilPraticien - { ancrage, ecoute, regulation, cadrage, agentivite, ethique }
   * @param {Object} opts            - { praticienPrenom: 'Mylène', height: 280 }
   */
  constructor(canvas, profilClient, profilPraticien, opts = {}) {
    this.canvas   = canvas;
    this.client   = profilClient;
    this.praticien = profilPraticien;
    this.opts     = { praticienPrenom: 'Mylène', height: 280, ...opts };
    this.dims     = computeEcartDims(profilClient, profilPraticien);
    this.metrics  = computeAdequation(this.dims);
    this._chart   = null;
  }

  render() {
    const labels  = this.dims.map(d => d.label);
    const cVals   = this.dims.map(d => d.clientVal);
    const pVals   = this.dims.map(d => d.pratVal);

    this._chart = new Chart(this.canvas, {
      type: 'radar',
      data: {
        labels,
        datasets: [
          {
            label:           'Toile client',
            data:            cVals,
            borderColor:     RC_COLORS.clientBorder,
            borderWidth:     2.5,
            pointBackgroundColor: RC_COLORS.clientBorder,
            pointRadius:     4,
            backgroundColor: RC_COLORS.client,
            order:           2,
          },
          {
            label:           `Intervention ${this.opts.praticienPrenom}`,
            data:            pVals,
            borderColor:     RC_COLORS.praticienBorder,
            borderWidth:     2,
            borderDash:      [4, 3],
            pointBackgroundColor: RC_COLORS.praticienBorder,
            pointRadius:     3,
            backgroundColor: RC_COLORS.praticien,
            order:           1,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          r: {
            min: 0,
            max: 3,
            ticks: { stepSize: 1, display: false },
            pointLabels: {
              font: { family: 'Raleway', size: 11, weight: '600' },
              color: '#4B6350',
            },
            grid:       { color: 'rgba(212,232,208,0.9)' },
            angleLines: { color: 'rgba(212,232,208,0.6)' },
          },
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: ctx => {
                const v = ['Rare', 'Parfois', 'Souvent'][ctx.raw - 1] || ctx.raw;
                return `${ctx.dataset.label} : ${v}`;
              },
            },
          },
        },
      },
    });
    return this._chart;
  }

  /**
   * Rendu des métriques d'adéquation dans un conteneur DOM.
   * @param {HTMLElement} container
   */
  renderMetrics(container) {
    const m = this.metrics;
    const natures = {
      compensation: { label: 'Compensation',  color: '#4A7C59', bg: '#F0F7F2', desc: 'Praticien couvre un vide du client' },
      resonance:    { label: 'Résonance',     color: '#8FB99A', bg: '#F8FBF9', desc: 'Alignement naturel' },
      collusion:    { label: 'Collusion',     color: '#D97706', bg: '#FFFBEB', desc: 'Renforcement d\'une zone déjà forte' },
      angle_mort:   { label: 'Angle mort',    color: '#DC2626', bg: '#FEF2F2', desc: 'Vide non couvert — priorité d\'intervention' },
    };

    // Score d'adéquation global
    const scoreEl = document.createElement('div');
    scoreEl.className = 'flex items-center justify-between mb-4';
    scoreEl.innerHTML = `
      <div>
        <p class="text-xs font-semibold uppercase tracking-wide text-muted">Score d'adéquation</p>
        <p class="font-heading text-2xl font-bold text-ink mt-0.5">${m.adequation} <span class="text-base font-normal text-muted">/ 100</span></p>
      </div>
      <div class="text-right text-xs text-muted">
        <p><span class="text-[#4A7C59] font-semibold">${m.compensation}</span> compensation${m.compensation > 1 ? 's' : ''}</p>
        <p><span class="text-[#D97706] font-semibold">${m.collusion}</span> collusion${m.collusion > 1 ? 's' : ''}</p>
        ${m.angleMort ? `<p><span class="text-[#DC2626] font-semibold">${m.angleMort}</span> angle${m.angleMort > 1 ? 's' : ''} mort${m.angleMort > 1 ? 's' : ''}</p>` : ''}
      </div>`;
    container.appendChild(scoreEl);

    // Détail par dimension
    const table = document.createElement('div');
    table.className = 'space-y-2';
    this.dims.forEach(dim => {
      const n = natures[dim.nature];
      const row = document.createElement('div');
      row.className = 'flex items-center gap-3';
      row.innerHTML = `
        <span class="text-xs font-semibold w-28 shrink-0 text-ink">${dim.label}</span>
        <div class="flex gap-1 items-center shrink-0">
          ${[1,2,3].map(v => `<span class="w-4 h-4 rounded-sm border ${v <= dim.clientVal ? 'bg-[#4A7C59] border-[#4A7C59]' : 'bg-transparent border-[#D4E8D0]'}"></span>`).join('')}
          <span class="text-[10px] text-muted mx-1">vs</span>
          ${[1,2,3].map(v => `<span class="w-4 h-4 rounded-sm border ${v <= dim.pratVal ? 'bg-[#2D6A4F] border-[#2D6A4F]' : 'bg-transparent border-[#D4E8D0]'}"></span>`).join('')}
        </div>
        <span class="text-xs px-2 py-0.5 rounded-full font-medium" style="background:${n.bg};color:${n.color};">${n.label}</span>`;
      table.appendChild(row);
    });
    container.appendChild(table);

    // Clusters
    const clusters = document.createElement('div');
    clusters.className = 'mt-4 grid grid-cols-2 gap-3';
    [
      { label: 'Vivant', ...m.vivant  },
      { label: 'Société', ...m.societe },
    ].forEach(c => {
      const el = document.createElement('div');
      const scoreColor = c.score === 'fort' ? '#4A7C59' : c.score === 'bas' ? '#DC2626' : '#D97706';
      el.className = 'rounded-[10px] border border-[#D4E8D0] px-3 py-2 bg-[#F8FBF9]';
      el.innerHTML = `<p class="text-xs font-semibold text-muted">${c.label}</p><p class="text-sm font-medium mt-0.5" style="color:${scoreColor}">${c.label_value || c.label} — ${c.label}</p>`;
      clusters.appendChild(el);
    });
    container.appendChild(clusters);
  }

  destroy() {
    if (this._chart) { this._chart.destroy(); this._chart = null; }
  }
}

// Export des fonctions utilitaires pour usage direct
// (swap API : remplacer getData() par fetch('/api/v1/seance/{id}/analyse'))

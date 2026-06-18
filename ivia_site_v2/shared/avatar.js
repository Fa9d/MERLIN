/**
 * IVIA — Représentation abstraite d'un·e praticien·ne (sans photo).
 *
 * On ne représente pas les praticiens par leur image physique mais par une
 * « constellation » générée de façon déterministe à partir de leur nom :
 * mêmes entrées → même motif, stable dans le temps, unique par personne.
 *
 * Usage : element.innerHTML = iviaConstellation('David Phaneuf');
 */

/** Hash déterministe (FNV-1a 32 bits) d'une chaîne → entier non signé. */
function _iviaHash(str) {
  let h = 0x811c9dc5;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = Math.imul(h, 0x01000193);
  }
  return h >>> 0;
}

/** PRNG déterministe (mulberry32) à partir d'une graine entière. */
function _iviaRng(seed) {
  let a = seed >>> 0;
  return function () {
    a |= 0; a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/**
 * Renvoie une chaîne SVG (viewBox 0 0 64 64, mise à l'échelle par CSS).
 * @param {string} seed — nom (ou identifiant) du praticien
 * @param {{ring?:boolean}} [opts]
 */
function iviaConstellation(seed, opts) {
  opts = opts || {};
  const s = (seed || 'IVIA').trim() || 'IVIA';
  const hash = _iviaHash(s);
  const rng = _iviaRng(hash);

  // Palette forêt — teinte stable par personne.
  const palettes = [
    { dot: '#2D6A4F', line: '#4A7C59', bg: '#E8F5EE' },
    { dot: '#4A7C59', line: '#8FB99A', bg: '#F0F7F2' },
    { dot: '#1A2E1D', line: '#4A7C59', bg: '#E8F5EE' },
    { dot: '#2563EB', line: '#8FB99A', bg: '#EAF1FF' },
  ];
  const pal = palettes[hash % palettes.length];

  // 5 ou 6 nœuds répartis dans un cadre avec marge.
  const pad = 14, span = 64 - pad * 2;
  const n = 5 + (hash % 2);
  const pts = [];
  for (let i = 0; i < n; i++) {
    pts.push({ x: +(pad + rng() * span).toFixed(1), y: +(pad + rng() * span).toFixed(1) });
  }

  // Liens : chemin séquentiel à travers les nœuds (+ une corde de retour discrète).
  let lines = '';
  for (let i = 0; i < n - 1; i++) {
    lines += `<line x1="${pts[i].x}" y1="${pts[i].y}" x2="${pts[i + 1].x}" y2="${pts[i + 1].y}" stroke="${pal.line}" stroke-width="1.1" stroke-linecap="round" opacity="0.7"/>`;
  }
  lines += `<line x1="${pts[n - 1].x}" y1="${pts[n - 1].y}" x2="${pts[0].x}" y2="${pts[0].y}" stroke="${pal.line}" stroke-width="0.8" stroke-linecap="round" opacity="0.35"/>`;

  let dots = '';
  pts.forEach((p, i) => {
    const r = i === 0 ? 2.6 : (1.4 + rng() * 1.1);
    dots += `<circle cx="${p.x}" cy="${p.y}" r="${r.toFixed(1)}" fill="${pal.dot}"/>`;
  });

  const ring = opts.ring === false ? '' :
    `<circle cx="32" cy="32" r="31" fill="none" stroke="${pal.line}" stroke-width="1" opacity="0.25"/>`;

  return `<svg viewBox="0 0 64 64" role="img" aria-label="Représentation de ${s.replace(/[<>&"]/g, '')}" class="w-full h-full">`
    + `<rect width="64" height="64" rx="32" fill="${pal.bg}"/>`
    + ring + lines + dots
    + `</svg>`;
}

if (typeof window !== 'undefined') { window.iviaConstellation = iviaConstellation; }

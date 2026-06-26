/**
 * IVIA — <ivia-profile-radar> (Web Component natif, zéro dépendance)
 *
 * Portage statique de 09_app_ivia_merlin/src/components/ProfileRadar.tsx vers le site
 * statique (ivia_site_v2). Aucun React, aucun build, aucune lib de chart : SVG natif.
 *
 * Usage :
 *   <ivia-profile-radar></ivia-profile-radar>
 *   const r = document.querySelector('ivia-profile-radar');
 *   r.profileA = { ocean:{...}, love:{...}, ... };   // client
 *   r.profileB = { ... };                            // praticien (optionnel)
 *   r.activeLayer = 'love';
 *   r.addEventListener('layer-change', e => console.log(e.detail.layer));
 *
 * Surface : INTERNE (praticien) par défaut. Une variante client devrait être revue
 * (B3 : pas de scores bruts) — voir 03_DESIGN/PORTAGE_PROFILE_RADAR_v1.0.md.
 * Thème : couleurs via variables CSS (Signature/Doux) avec repli clair.
 * Accessibilité : rôle img + <title>/<desc>, onglets clavier, prefers-reduced-motion.
 */
(function () {
  "use strict";

  const LAYER_LABELS = {
    ocean: "Traits (OCEAN)", schwartz: "Valeurs", love: "Expressions",
    attachment: "Attachement", vad: "État du moment",
  };
  const LAYER_AXES = {
    ocean: [["openness", "Ouverture"], ["conscientiousness", "Rigueur"], ["extraversion", "Extraversion"],
            ["agreeableness", "Amabilité"], ["neuroticism", "Réactivité"]],
    schwartz: [["self_direction", "Autonomie"], ["stimulation", "Stimulation"], ["hedonism", "Plaisir"],
               ["achievement", "Accompl."], ["power", "Pouvoir"], ["security", "Sécurité"],
               ["conformity", "Conformité"], ["tradition", "Tradition"], ["benevolence", "Bienveill."],
               ["universalism", "Universel"]],
    love: [["paroles_valorisantes", "Paroles"], ["moments_qualite", "Moments"], ["contact_physique", "Contact"],
           ["services_rendus", "Services"], ["cadeaux", "Cadeaux"], ["soutien_emotionnel", "Soutien"],
           ["espace_autonomie", "Espace"], ["engagement_fiabilite", "Engagement"]],
    attachment: [["secure_score", "Sécure"], ["preoccupied_score", "Préoccupé"],
                 ["dismissing_score", "Détaché"], ["fearful_score", "Craintif"]],
    vad: [["valence", "Tonalité"], ["arousal", "Activation"], ["dominance", "Assurance"]],
  };
  const LAYERS = Object.keys(LAYER_LABELS);
  const SIZE = 360, CX = 180, CY = 180, R = 124;
  const SVGNS = "http://www.w3.org/2000/svg";

  const num = (layer, v) => {
    if (v == null || isNaN(v)) return 0;
    const x = layer === "vad" ? (v + 1) / 2 : v;
    return Math.max(0, Math.min(1, x));
  };
  const toVec = (layer, profile) => {
    const src = (profile && profile[layer]) || {};
    return LAYER_AXES[layer].map(([k]) => num(layer, src[k]));
  };
  const pt = (i, n, r) => {
    const a = -Math.PI / 2 + (i * 2 * Math.PI) / n;
    return [CX + R * r * Math.cos(a), CY + R * r * Math.sin(a)];
  };
  const poly = (vals) => vals.map((r, i) => {
    const [x, y] = pt(i, vals.length, r); return `${x.toFixed(1)},${y.toFixed(1)}`;
  }).join(" ");

  const el = (tag, attrs) => {
    const n = document.createElementNS(SVGNS, tag);
    for (const k in attrs) n.setAttribute(k, attrs[k]);
    return n;
  };
  const reduceMotion = () =>
    window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  class IviaProfileRadar extends HTMLElement {
    constructor() {
      super();
      this._a = {}; this._b = null; this._layer = "love";
      this._dispA = []; this._dispB = []; this._raf = null;
    }
    connectedCallback() {
      if (!this.getAttribute("activeLayer") && this.getAttribute("active-layer"))
        this._layer = this.getAttribute("active-layer");
      this._render();
    }
    set profileA(v) { this._a = v || {}; this._animate(); }
    get profileA() { return this._a; }
    set profileB(v) { this._b = v || null; this._render(); }
    get profileB() { return this._b; }
    set activeLayer(v) { if (LAYERS.includes(v)) { this._layer = v; this._render(); } }
    get activeLayer() { return this._layer; }

    _setLayer(layer) {
      this._layer = layer;
      this.dispatchEvent(new CustomEvent("layer-change", { detail: { layer }, bubbles: true }));
      this._render();
    }

    _animate() {
      const target = toVec(this._layer, this._a);
      const targetB = this._b ? toVec(this._layer, this._b) : [];
      if (reduceMotion()) { this._dispA = target; this._dispB = targetB; this._paint(); return; }
      const fromA = this._dispA.length === target.length ? this._dispA : target.map(() => 0);
      const fromB = this._dispB.length === targetB.length ? this._dispB : targetB.map(() => 0);
      const start = performance.now(), dur = 500;
      if (this._raf) cancelAnimationFrame(this._raf);
      const tick = (now) => {
        const t = Math.min(1, (now - start) / dur), e = 1 - Math.pow(1 - t, 3);
        this._dispA = target.map((v, i) => fromA[i] + (v - fromA[i]) * e);
        this._dispB = targetB.map((v, i) => fromB[i] + (v - fromB[i]) * e);
        this._paint();
        if (t < 1) this._raf = requestAnimationFrame(tick);
      };
      this._raf = requestAnimationFrame(tick);
    }

    _render() {
      const labelA = this.getAttribute("label-a") || "Client";
      const labelB = this.getAttribute("label-b") || "Praticien·ne";
      const tabs = LAYERS.map((l) =>
        `<button type="button" role="tab" aria-selected="${l === this._layer}" data-layer="${l}"
           class="ivr-tab${l === this._layer ? " on" : ""}">${LAYER_LABELS[l]}</button>`).join("");
      this.innerHTML = `
        <div class="ivr-wrap" role="group" aria-label="Profil radar">
          <div class="ivr-tabs" role="tablist" aria-label="Couches du profil">${tabs}</div>
          <svg class="ivr-svg" viewBox="0 0 ${SIZE} ${SIZE}" role="img"
               aria-label="Profil radar — ${LAYER_LABELS[this._layer]}">
            <title>Profil radar — ${LAYER_LABELS[this._layer]}</title>
            <desc>Visualisation de tendances ; ce n'est pas un diagnostic.</desc>
            <g class="ivr-grid"></g><g class="ivr-axes"></g><g class="ivr-data"></g>
          </svg>
          <div class="ivr-legend">
            <span><i class="ivr-sw-a"></i>${labelA}</span>
            ${this._b ? `<span><i class="ivr-sw-b"></i>${labelB}</span>` : ""}
          </div>
        </div>`;
      this.querySelectorAll(".ivr-tab").forEach((btn) => {
        btn.addEventListener("click", () => this._setLayer(btn.dataset.layer));
        btn.addEventListener("keydown", (e) => {
          if (e.key !== "ArrowRight" && e.key !== "ArrowLeft") return;
          e.preventDefault();
          const i = LAYERS.indexOf(this._layer);
          const j = e.key === "ArrowRight" ? (i + 1) % LAYERS.length : (i - 1 + LAYERS.length) % LAYERS.length;
          this._setLayer(LAYERS[j]);
          const next = this.querySelector(`.ivr-tab[data-layer="${LAYERS[j]}"]`); next && next.focus();
        });
      });
      this._injectStyleOnce();
      this._dispA = toVec(this._layer, this._a);
      this._dispB = this._b ? toVec(this._layer, this._b) : [];
      this._buildStatic(); this._paint();
    }

    _buildStatic() {
      const grid = this.querySelector(".ivr-grid"), axesG = this.querySelector(".ivr-axes");
      grid.innerHTML = ""; axesG.innerHTML = "";
      [0.25, 0.5, 0.75, 1].forEach((r) =>
        grid.appendChild(el("circle", { cx: CX, cy: CY, r: R * r, fill: "none",
          stroke: "var(--bdr,#D4E8D0)", "stroke-width": 1 })));
      const axes = LAYER_AXES[this._layer], n = axes.length;
      axes.forEach(([, label], i) => {
        const [x, y] = pt(i, n, 1), [lx, ly] = pt(i, n, 1.18);
        axesG.appendChild(el("line", { x1: CX, y1: CY, x2: x, y2: y, stroke: "var(--bdr,#D4E8D0)", "stroke-width": 1 }));
        const t = el("text", { x: lx, y: ly + 3, "font-size": 10, "font-weight": 600,
          fill: "var(--muted,#4B6350)", "text-anchor": Math.abs(lx - CX) < 8 ? "middle" : lx > CX ? "start" : "end" });
        t.textContent = label; axesG.appendChild(t);
      });
    }

    _paint() {
      const g = this.querySelector(".ivr-data"); if (!g) return;
      g.innerHTML = "";
      if (this._b && this._dispB.length) {
        g.appendChild(el("polygon", { points: poly(this._dispB), fill: "var(--accent-2,#C9748B)",
          "fill-opacity": 0.22, stroke: "var(--accent-2,#C9748B)", "stroke-width": 2 }));
      }
      g.appendChild(el("polygon", { points: poly(this._dispA), fill: "var(--forest-deep,#2D6A4F)",
        "fill-opacity": 0.25, stroke: "var(--forest-deep,#2D6A4F)", "stroke-width": 2 }));
      this._dispA.forEach((r, i) => {
        const [x, y] = pt(i, this._dispA.length, r);
        g.appendChild(el("circle", { cx: x, cy: y, r: 3, fill: "var(--forest-deep,#2D6A4F)" }));
      });
    }

    _injectStyleOnce() {
      if (document.getElementById("ivr-style")) return;
      const s = document.createElement("style");
      s.id = "ivr-style";
      s.textContent = `
        ivia-profile-radar{display:block;max-width:28rem;margin:0 auto;font-family:'Raleway',system-ui,sans-serif;}
        .ivr-tabs{display:flex;flex-wrap:wrap;justify-content:center;gap:6px;margin-bottom:10px;}
        .ivr-tab{cursor:pointer;border:0;border-radius:9999px;padding:6px 12px;font-size:12px;font-weight:600;
          background:var(--surface,#F0F7F2);color:var(--muted,#4B6350);transition:.15s;}
        .ivr-tab.on{background:var(--forest-deep,#2D6A4F);color:#fff;}
        .ivr-svg{width:100%;height:auto;display:block;}
        .ivr-legend{display:flex;justify-content:center;gap:20px;margin-top:8px;font-size:12px;color:var(--muted,#4B6350);}
        .ivr-legend span{display:inline-flex;align-items:center;gap:6px;}
        .ivr-legend i{width:12px;height:12px;border-radius:3px;display:inline-block;}
        .ivr-sw-a{background:var(--forest-deep,#2D6A4F);}
        .ivr-sw-b{background:var(--accent-2,#C9748B);}`;
      document.head.appendChild(s);
    }
  }

  if (!customElements.get("ivia-profile-radar"))
    customElements.define("ivia-profile-radar", IviaProfileRadar);
})();

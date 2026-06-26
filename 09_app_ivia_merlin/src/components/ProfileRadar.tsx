"use client";

/**
 * ProfileRadar — radar (spider chart) multi-couches pour MERLIN.
 *
 * - Superpose deux profils (client + praticien) en transparence, couleurs distinctes.
 * - Toggle entre les 5 couches (OCEAN, Schwartz, 8 Expressions, Attachement, VAD).
 * - Anime la transition entre états (temps réel ↔ historique) par interpolation rAF.
 * - Responsive (SVG viewBox), thème « Maison habitée » (vert / rosé).
 *
 * Radar SVG natif (aucune dépendance externe) : robuste avec React 19. On peut
 * basculer vers Recharts plus tard si la dépendance est ajoutée au projet.
 *
 * Posture IVIA : visualisation d'observations/préférences, jamais un diagnostic.
 */
import { useEffect, useMemo, useRef, useState } from "react";

export type LayerKey = "ocean" | "schwartz" | "love" | "attachment" | "vad";

/** Un profil = scores par couche. Valeurs en [0,1] sauf VAD en [-1,1]. */
export type ProfileData = Partial<Record<LayerKey, Record<string, number | null | undefined>>>;

export interface ProfileRadarProps {
  profileA: ProfileData;                 // client (vert)
  profileB?: ProfileData;                // praticien (rosé) — optionnel
  activeLayer: LayerKey;
  onLayerChange: (layer: LayerKey) => void;
  labelA?: string;
  labelB?: string;
  /** durée d'animation (ms) à chaque changement d'état */
  animationMs?: number;
}

const LAYER_LABELS: Record<LayerKey, string> = {
  ocean: "Traits (OCEAN)",
  schwartz: "Valeurs",
  love: "Expressions",
  attachment: "Attachement",
  vad: "État du moment",
};

/** Axes (clé → libellé FR) par couche. */
const LAYER_AXES: Record<LayerKey, { key: string; label: string }[]> = {
  ocean: [
    { key: "openness", label: "Ouverture" },
    { key: "conscientiousness", label: "Rigueur" },
    { key: "extraversion", label: "Extraversion" },
    { key: "agreeableness", label: "Amabilité" },
    { key: "neuroticism", label: "Réactivité" },
  ],
  schwartz: [
    { key: "self_direction", label: "Autonomie" },
    { key: "stimulation", label: "Stimulation" },
    { key: "hedonism", label: "Plaisir" },
    { key: "achievement", label: "Accompl." },
    { key: "power", label: "Pouvoir" },
    { key: "security", label: "Sécurité" },
    { key: "conformity", label: "Conformité" },
    { key: "tradition", label: "Tradition" },
    { key: "benevolence", label: "Bienveill." },
    { key: "universalism", label: "Universel" },
  ],
  love: [
    { key: "paroles_valorisantes", label: "Paroles" },
    { key: "moments_qualite", label: "Moments" },
    { key: "contact_physique", label: "Contact" },
    { key: "services_rendus", label: "Services" },
    { key: "cadeaux", label: "Cadeaux" },
    { key: "soutien_emotionnel", label: "Soutien" },
    { key: "espace_autonomie", label: "Espace" },
    { key: "engagement_fiabilite", label: "Engagement" },
  ],
  attachment: [
    { key: "secure_score", label: "Sécure" },
    { key: "preoccupied_score", label: "Préoccupé" },
    { key: "dismissing_score", label: "Détaché" },
    { key: "fearful_score", label: "Craintif" },
  ],
  vad: [
    { key: "valence", label: "Tonalité" },
    { key: "arousal", label: "Activation" },
    { key: "dominance", label: "Assurance" },
  ],
};

const COLOR_A = "#2D6A4F"; // vert IVIA (client)
const COLOR_B = "#C9748B"; // rosé (praticien)

/** Normalise une valeur de couche en [0,1] (VAD : [-1,1] → [0,1]). */
function norm(layer: LayerKey, v: number | null | undefined): number {
  if (v == null || Number.isNaN(v)) return 0;
  const x = layer === "vad" ? (v + 1) / 2 : v;
  return Math.max(0, Math.min(1, x));
}

function toVector(layer: LayerKey, profile?: ProfileData): number[] {
  const axes = LAYER_AXES[layer];
  const src = profile?.[layer] ?? {};
  return axes.map((a) => norm(layer, src[a.key]));
}

/** Point cartésien d'un axe i (sur n) au rayon r∈[0,1]. */
function point(i: number, n: number, r: number, cx: number, cy: number, R: number) {
  const ang = -Math.PI / 2 + (i * 2 * Math.PI) / n;
  return [cx + R * r * Math.cos(ang), cy + R * r * Math.sin(ang)] as const;
}

function polygon(values: number[], cx: number, cy: number, R: number): string {
  const n = values.length;
  return values
    .map((r, i) => {
      const [x, y] = point(i, n, r, cx, cy, R);
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .join(" ");
}

export default function ProfileRadar({
  profileA,
  profileB,
  activeLayer,
  onLayerChange,
  labelA = "Client",
  labelB = "Praticien·ne",
  animationMs = 500,
}: ProfileRadarProps) {
  const axes = LAYER_AXES[activeLayer];
  const n = axes.length;

  const targetA = useMemo(() => toVector(activeLayer, profileA), [activeLayer, profileA]);
  const targetB = useMemo(() => toVector(activeLayer, profileB), [activeLayer, profileB]);

  // Valeurs affichées (interpolées) — animation à chaque changement d'état.
  const [dispA, setDispA] = useState<number[]>(targetA);
  const [dispB, setDispB] = useState<number[]>(targetB);
  const raf = useRef<number | null>(null);

  useEffect(() => {
    const fromA = dispA.length === n ? dispA : new Array(n).fill(0);
    const fromB = dispB.length === n ? dispB : new Array(n).fill(0);
    const start = performance.now();
    const tick = (now: number) => {
      const t = Math.min(1, (now - start) / animationMs);
      const ease = 1 - Math.pow(1 - t, 3); // easeOutCubic
      setDispA(targetA.map((v, i) => fromA[i] + (v - fromA[i]) * ease));
      setDispB(targetB.map((v, i) => fromB[i] + (v - fromB[i]) * ease));
      if (t < 1) raf.current = requestAnimationFrame(tick);
    };
    raf.current = requestAnimationFrame(tick);
    return () => {
      if (raf.current) cancelAnimationFrame(raf.current);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeLayer, JSON.stringify(targetA), JSON.stringify(targetB)]);

  // Géométrie SVG (viewBox carré, responsive).
  const SIZE = 360;
  const cx = SIZE / 2;
  const cy = SIZE / 2;
  const R = SIZE / 2 - 56; // marge pour les libellés
  const rings = [0.25, 0.5, 0.75, 1];

  return (
    <div className="w-full max-w-md mx-auto">
      {/* Toggle des 5 couches */}
      <div className="flex flex-wrap justify-center gap-1.5 mb-3" role="tablist" aria-label="Couches du profil">
        {(Object.keys(LAYER_LABELS) as LayerKey[]).map((layer) => (
          <button
            key={layer}
            role="tab"
            aria-selected={layer === activeLayer}
            onClick={() => onLayerChange(layer)}
            className={`px-3 py-1.5 rounded-full text-xs font-semibold transition-colors ${
              layer === activeLayer
                ? "bg-[#2D6A4F] text-white"
                : "bg-[#F0F7F2] text-[#4B6350] hover:bg-[#e2efe6]"
            }`}
          >
            {LAYER_LABELS[layer]}
          </button>
        ))}
      </div>

      <svg viewBox={`0 0 ${SIZE} ${SIZE}`} className="w-full h-auto" role="img"
           aria-label={`Profil radar — ${LAYER_LABELS[activeLayer]}`}>
        {/* Anneaux de la grille */}
        {rings.map((r) => (
          <circle key={r} cx={cx} cy={cy} r={R * r} fill="none" stroke="#D4E8D0" strokeWidth={1} />
        ))}

        {/* Axes + libellés */}
        {axes.map((a, i) => {
          const [x, y] = point(i, n, 1, cx, cy, R);
          const [lx, ly] = point(i, n, 1.16, cx, cy, R);
          const anchor = Math.abs(lx - cx) < 8 ? "middle" : lx > cx ? "start" : "end";
          return (
            <g key={a.key}>
              <line x1={cx} y1={cy} x2={x} y2={y} stroke="#D4E8D0" strokeWidth={1} />
              <text x={lx} y={ly + 3} textAnchor={anchor} fontSize={10} fill="#4B6350" fontWeight={600}>
                {a.label}
              </text>
            </g>
          );
        })}

        {/* Profil B (praticien) — dessous */}
        {profileB && (
          <polygon points={polygon(dispB, cx, cy, R)} fill={COLOR_B} fillOpacity={0.22}
                   stroke={COLOR_B} strokeWidth={2} />
        )}
        {/* Profil A (client) — dessus */}
        <polygon points={polygon(dispA, cx, cy, R)} fill={COLOR_A} fillOpacity={0.25}
                 stroke={COLOR_A} strokeWidth={2} />

        {/* Sommets A */}
        {dispA.map((r, i) => {
          const [x, y] = point(i, n, r, cx, cy, R);
          return <circle key={`a${i}`} cx={x} cy={y} r={3} fill={COLOR_A} />;
        })}
      </svg>

      {/* Légende */}
      <div className="flex items-center justify-center gap-5 mt-2 text-xs text-[#4B6350]">
        <span className="inline-flex items-center gap-1.5">
          <span className="w-3 h-3 rounded-sm" style={{ background: COLOR_A }} /> {labelA}
        </span>
        {profileB && (
          <span className="inline-flex items-center gap-1.5">
            <span className="w-3 h-3 rounded-sm" style={{ background: COLOR_B }} /> {labelB}
          </span>
        )}
      </div>
    </div>
  );
}

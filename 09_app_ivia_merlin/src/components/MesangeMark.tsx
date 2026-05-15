"use client";

import { CSSProperties } from "react";

type MesangeMarkProps = {
  /** Diamètre approximatif de la carte noire en px. */
  size?: number;
  /** Coupe le fond noir (utile pour usage en symbole pur sur surface claire). */
  bare?: boolean;
  /** Active les petites ondes de chant au hover. */
  withSong?: boolean;
  /** Inverse les couleurs (oiseau noir, fond clair) — pour usages en pied de page. */
  inverse?: boolean;
  className?: string;
  ariaLabel?: string;
};

/**
 * Mésange — symbole MÉSANGES.
 *
 * - Respiration douce permanente (scale 1.000 ↔ 1.018, 4.5s ease-in-out).
 * - Petites ondes de chant au survol (3 arcs concentriques qui partent
 *   du bec, opacité décroissante, durée 1.6s).
 * - Respecte `prefers-reduced-motion` : la respiration et les ondes sont
 *   neutralisées au niveau du CSS (voir styles.css).
 *
 * Le tracé reprend exactement la silhouette du brand pack
 * MÉSANGE (mesange-logo.svg) — pas une variante.
 */
export function MesangeMark({
  size = 96,
  bare = false,
  withSong = false,
  inverse = false,
  className = "",
  ariaLabel = "Mésange — accueil IVIA",
}: MesangeMarkProps) {
  const bg = inverse ? "#fdfaf2" : "#0a0a0a";
  const figure = inverse ? "#0a0a0a" : "#fdfaf2";
  const eye = inverse ? "#fdfaf2" : "#0a0a0a";

  const wrapperStyle: CSSProperties = {
    width: size,
    height: size,
  };

  const classes = [
    "mesange-mark",
    bare ? "mesange-mark--bare" : "",
    withSong ? "mesange-mark--song" : "",
    className,
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <span className={classes} style={wrapperStyle} aria-hidden={!ariaLabel}>
      <svg
        viewBox="0 0 400 400"
        width="100%"
        height="100%"
        role="img"
        aria-label={ariaLabel}
        focusable="false"
      >
        <title>MÉSANGES — IVIA</title>
        {!bare && <rect width="400" height="400" rx="32" fill={bg} />}

        <g
          transform="translate(60, 130)"
          className="mesange-mark__body"
        >
          <path
            fill={figure}
            d="M 80 70
               Q 72 12 118 -4
               Q 155 -12 182 6
               Q 208 -4 240 6
               Q 262 16 268 42
               Q 245 48 218 46
               Q 245 76 255 112
               Q 218 94 182 89
               Q 175 122 150 134
               Q 128 122 128 94
               Q 95 86 80 70 Z"
          />
          <polygon fill={figure} points="75,24 50,30 75,36" />
          <circle fill={eye} cx="108" cy="22" r="4.2" />
        </g>

        {withSong && (
          <g
            className="mesange-mark__song"
            transform="translate(110, 158)"
            stroke={figure}
            fill="none"
            strokeLinecap="round"
            opacity="0"
          >
            <path
              className="mesange-mark__song-wave mesange-mark__song-wave--1"
              d="M -2 0 Q -16 -10 -28 0"
              strokeWidth="2.5"
            />
            <path
              className="mesange-mark__song-wave mesange-mark__song-wave--2"
              d="M -2 0 Q -22 -16 -42 0"
              strokeWidth="2"
            />
            <path
              className="mesange-mark__song-wave mesange-mark__song-wave--3"
              d="M -2 0 Q -28 -22 -56 0"
              strokeWidth="1.5"
            />
          </g>
        )}
      </svg>
    </span>
  );
}

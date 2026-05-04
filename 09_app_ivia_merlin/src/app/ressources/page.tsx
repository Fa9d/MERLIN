"use client";

import { useState } from "react";
import Link from "next/link";
import { PublicLayout } from "@/components/layout/PublicLayout";

const CATEGORIES = [
  {
    key: "ecoute",
    label: "Écoute & relation",
    dot: "home-cat-dot-1",
    desc: "Comprendre ce qui se passe dans une relation, apprendre à recevoir et donner une attention vraie.",
  },
  {
    key: "equilibre",
    label: "Équilibre & vivant",
    dot: "home-cat-dot-2",
    desc: "Retrouver un rythme. Prendre soin du corps, du temps, de l'énergie disponible.",
  },
  {
    key: "empathie",
    label: "Empathie & société",
    dot: "home-cat-dot-3",
    desc: "Ce que nos liens sociaux nous apprennent sur nous-mêmes. Vivre ensemble sans se perdre.",
  },
  {
    key: "vibration",
    label: "Vibration & soin",
    dot: "home-cat-dot-4",
    desc: "Pratiques sensorielles, présence au corps, voix et sons comme vecteurs de mieux-être.",
  },
];

const ARTICLES = [
  {
    slug: "distinguer-fatigue-blues-epuisement",
    cat: "equilibre",
    title: "Fatigue, blues ou épuisement — comment les distinguer",
    intro: "Trois états qui se ressemblent, mais qui n'appellent pas les mêmes réponses. Une grille simple pour y voir plus clair.",
    readingTime: "5 min",
    date: "2026-04-28",
  },
  {
    slug: "pourquoi-etre-entendu-aide",
    cat: "ecoute",
    title: "Pourquoi être entendu — vraiment — fait une différence",
    intro: "Quand quelqu'un nomme ce que vous vivez avec justesse, quelque chose se dépose. Voici pourquoi.",
    readingTime: "4 min",
    date: "2026-04-15",
  },
  {
    slug: "quand-consulter-professionnel",
    cat: "empathie",
    title: "Quand faut-il consulter un professionnel de la santé mentale ?",
    intro: "Psychologue, travailleur social, médecin, psychiatre — ce guide vous aide à identifier la bonne porte d'entrée.",
    readingTime: "6 min",
    date: "2026-04-10",
  },
  {
    slug: "prendre-soin-de-soi-au-quotidien",
    cat: "equilibre",
    title: "Ce que signifie vraiment « prendre soin de soi »",
    intro: "L'expression est galvaudée. Derrière elle se cache quelque chose de plus concret — et de plus exigeant.",
    readingTime: "4 min",
    date: "2026-03-22",
  },
  {
    slug: "ecoute-active-famille",
    cat: "ecoute",
    title: "L'écoute active en famille : plus facile à dire qu'à faire",
    intro: "Ce n'est pas une technique — c'est une posture. Comment créer les conditions pour que vos proches se sentent vraiment entendus.",
    readingTime: "5 min",
    date: "2026-03-10",
  },
  {
    slug: "sons-voix-bien-etre",
    cat: "vibration",
    title: "La voix, le son et le soin — ce que la science commence à comprendre",
    intro: "Des berceuses aux thérapies sonores, l'effet des vibrations sur le système nerveux est plus documenté qu'on ne le pense.",
    readingTime: "7 min",
    date: "2026-02-18",
  },
];

export default function RessourcesPage() {
  const [activeFilter, setActiveFilter] = useState<string | null>(null);

  const filtered = activeFilter ? ARTICLES.filter((a) => a.cat === activeFilter) : ARTICLES;

  return (
    <PublicLayout>
    <div style={{ background: "var(--background)", minHeight: "100vh", fontFamily: "var(--font-body, sans-serif)", color: "var(--foreground)" }}>
      <div style={{ width: "min(1100px, calc(100% - 2rem))", margin: "0 auto", paddingBottom: "5rem" }}>
        {/* Header */}
        <header style={{ padding: "3.5rem 0 2.5rem", display: "grid", gap: "1rem" }}>
          <h1 style={{ fontFamily: "var(--font-display, serif)", fontWeight: 400, fontSize: "clamp(2.5rem,6vw,4.5rem)", lineHeight: 1, letterSpacing: "-0.04em", color: "var(--foreground)" }}>
            Ressources
          </h1>
          <p style={{ color: "var(--muted)", fontSize: "1.1rem", lineHeight: 1.75, maxWidth: "50ch" }}>
            Textes, guides et réflexions pour nommer ce que vous vivez, mieux vous orienter, et prendre soin de vous autrement.
          </p>
        </header>

        {/* Category tiles */}
        <section style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: "1rem", marginBottom: "3rem" }} aria-label="Catégories">
          {CATEGORIES.map((cat) => (
            <button
              key={cat.key}
              onClick={() => setActiveFilter(activeFilter === cat.key ? null : cat.key)}
              style={{
                display: "grid", gap: "0.75rem", padding: "1.5rem", textAlign: "left",
                border: `1px solid ${activeFilter === cat.key ? "var(--accent)" : "var(--border)"}`,
                borderRadius: "var(--r-lg, 2rem)", background: activeFilter === cat.key ? "var(--accent-surf)" : "var(--surface)",
                cursor: "pointer", color: "inherit", transition: "all 180ms ease", minHeight: "44px",
                boxShadow: "var(--shadow-sm)",
              }}
              aria-pressed={activeFilter === cat.key}
            >
              <div style={{ width: "2rem", height: "2rem", borderRadius: "999px", background: cat.key === "ecoute" ? "oklch(72% 0.09 145 / 0.35)" : cat.key === "equilibre" ? "var(--surface-alt)" : cat.key === "empathie" ? "oklch(68% 0.082 56 / 0.35)" : "oklch(72% 0.1 68 / 0.35)" }} />
              <div style={{ fontFamily: "var(--font-display, serif)", fontSize: "1rem", color: "var(--foreground)" }}>{cat.label}</div>
              <div style={{ fontSize: "0.85rem", color: "var(--muted)", lineHeight: 1.6 }}>{cat.desc}</div>
            </button>
          ))}
        </section>

        {/* Filter pill / reset */}
        {activeFilter && (
          <div style={{ marginBottom: "1.5rem", display: "flex", alignItems: "center", gap: "0.75rem" }}>
            <span style={{ fontSize: "0.88rem", color: "var(--muted)" }}>
              Filtre actif : <strong style={{ color: "var(--foreground)" }}>{CATEGORIES.find((c) => c.key === activeFilter)?.label}</strong>
            </span>
            <button onClick={() => setActiveFilter(null)} style={{ fontSize: "0.82rem", color: "var(--accent)", background: "none", border: "1px solid var(--border)", borderRadius: "999px", padding: "0.2rem 0.8rem", cursor: "pointer", minHeight: "32px" }}>
              Tout afficher
            </button>
          </div>
        )}

        {/* Article grid */}
        <section aria-label="Articles">
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(320px, 1fr))", gap: "1.25rem" }}>
            {filtered.map((article) => {
              const catInfo = CATEGORIES.find((c) => c.key === article.cat);
              return (
                <article key={article.slug} style={{ display: "grid", gap: "1rem", padding: "1.75rem", border: "1px solid var(--border)", borderRadius: "var(--r-lg, 2rem)", background: "var(--surface)", boxShadow: "var(--shadow-sm)" }}>
                  <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
                    <div style={{ width: "0.75rem", height: "0.75rem", borderRadius: "50%", background: article.cat === "ecoute" ? "oklch(72% 0.09 145 / 0.7)" : article.cat === "equilibre" ? "var(--border-solid)" : article.cat === "empathie" ? "oklch(68% 0.082 56 / 0.7)" : "oklch(72% 0.1 68 / 0.7)" }} />
                    <span style={{ fontSize: "0.78rem", fontWeight: 700, letterSpacing: "0.08em", textTransform: "uppercase" as const, color: "var(--muted)" }}>{catInfo?.label}</span>
                  </div>
                  <h2 style={{ fontFamily: "var(--font-display, serif)", fontWeight: 400, fontSize: "1.2rem", lineHeight: 1.25, letterSpacing: "-0.02em", color: "var(--foreground)", margin: 0 }}>
                    {article.title}
                  </h2>
                  <p style={{ color: "var(--muted)", fontSize: "0.95rem", lineHeight: 1.7, margin: 0 }}>{article.intro}</p>
                  <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginTop: "auto", paddingTop: "0.5rem", borderTop: "1px solid var(--border)" }}>
                    <span style={{ fontSize: "0.82rem", color: "var(--subtle)" }}>{article.readingTime} · {new Date(article.date).toLocaleDateString("fr-CA", { year: "numeric", month: "long", day: "numeric" })}</span>
                    <Link href={`/ressources/${article.slug}`} style={{ fontSize: "0.88rem", fontWeight: 600, color: "var(--accent)", textDecoration: "none", minHeight: "44px", display: "inline-flex", alignItems: "center" }}>
                      Lire →
                    </Link>
                  </div>
                </article>
              );
            })}
          </div>
        </section>

        {/* CTA */}
        <div style={{ marginTop: "4rem", padding: "3rem", border: "1px solid var(--border)", borderRadius: "var(--r-lg, 2rem)", background: "var(--surface)", textAlign: "center", display: "grid", gap: "1rem", justifyItems: "center" }}>
          <h2 style={{ fontFamily: "var(--font-display, serif)", fontWeight: 400, fontSize: "clamp(1.7rem,4vw,2.4rem)", letterSpacing: "-0.03em", color: "var(--foreground)", margin: 0 }}>
            Prêt à vous accorder une heure d'écoute?
          </h2>
          <Link href="/rendez-vous/reserver" style={{ display: "inline-flex", alignItems: "center", minHeight: "44px", padding: "0 1.75rem", borderRadius: "999px", background: "var(--accent-deep)", color: "oklch(95% 0.01 80)", textDecoration: "none", fontWeight: 600, fontSize: "0.97rem", boxShadow: "0 12px 28px oklch(30% 0.07 145 / 0.3)" }}>
            Réserver une séance — 65&nbsp;$
          </Link>
        </div>
      </div>
    </div>
    </PublicLayout>
  );
}

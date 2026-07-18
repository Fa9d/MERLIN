import type { Metadata } from "next";
import { getAllArticles, CATEGORIES } from "./articles";
import ArticleGrid from "./ArticleGrid";
import { SiteHeader, SiteFooter } from "./components";

export const metadata: Metadata = {
  title: "Ressources IVIA — Littératie du vivant",
  description:
    "Textes et ressources pour cultiver l'écoute, l'empathie éthique, l'équilibre et la présence. Une littératie du vivant proposée par IVIA.",
};

const STATS = [
  { value: "1 sur 5", label: "Québécois vivra un trouble mental au cours de sa vie" },
  { value: "39 %", label: "de la population en détresse psychologique élevée (2020-2021)" },
  { value: "6-24 mois", label: "d'attente pour un psy dans le réseau public québécois" },
];

export default function BlogPage() {
  const articles = getAllArticles();

  return (
    <>
      <SiteHeader />
      <main>
        <div className="page-wrap">
          {/* Hero */}
          <section className="hero">
            <div className="hero-eyebrow">Ressources</div>
            <h1>
              Une littératie
              <br />
              <em>du vivant.</em>
            </h1>
            <p className="hero-sub">
              Des repères chiffrés sur la santé mentale au Québec et des textes
              pour apprendre à écouter, ralentir et habiter le présent. Comprendre,
              se situer, prendre soin — à votre rythme.
            </p>
          </section>

          {/* Stats Québec */}
          <div className="stats-band">
            {STATS.map((s) => (
              <div className="stat-item" key={s.label}>
                <div className="stat-value">{s.value}</div>
                <div className="stat-label">{s.label}</div>
              </div>
            ))}
          </div>

          {/* Recherche + filtres + grille (interactif) */}
          <ArticleGrid articles={articles} categories={CATEGORIES} />
        </div>
      </main>
      <SiteFooter />
    </>
  );
}

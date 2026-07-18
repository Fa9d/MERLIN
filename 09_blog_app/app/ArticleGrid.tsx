"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import type { Article, Category } from "./articles";
import { ArrowIcon } from "./components";

/* Retire les diacritiques pour une recherche insensible aux accents */
function norm(s: string): string {
  return (s || "")
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
}

function ArticleCard({ article, index }: { article: Article; index: number }) {
  return (
    <Link
      href={`/${article.slug}`}
      className={`article-card${article.featured ? " featured" : ""}`}
      style={{ animationDelay: `${index * 0.055}s` }}
    >
      {!article.featured && (
        <div className="card-visual">
          <div className="card-visual-inner">
            <div
              className="card-bg-blob"
              style={{
                background: `radial-gradient(circle, ${article.gradient[0]} 0%, ${article.gradient[1]} 100%)`,
              }}
            />
            <span className="card-emoji" role="img" aria-label={article.categoryLabel}>
              {article.emoji}
            </span>
          </div>
        </div>
      )}
      <div className="card-body">
        <div className="card-meta">
          <span className="card-cat">{article.categoryLabel}</span>
          <span className="card-dot">●</span>
          <span className="card-time">{article.readingTime}</span>
        </div>
        <h2 className="card-title">{article.title}</h2>
        <p className="card-excerpt">{article.excerpt}</p>
        <div className="card-footer">
          <div className="card-tags">
            {article.tags.map((t) => (
              <span key={t} className="card-tag">
                {t}
              </span>
            ))}
          </div>
          <div className="card-arrow" aria-hidden="true">
            <ArrowIcon />
          </div>
        </div>
      </div>
      {article.featured && (
        <div className="card-visual">
          <div className="card-visual-inner">
            <div
              className="card-bg-blob"
              style={{
                background: `radial-gradient(circle, ${article.gradient[0]} 0%, ${article.gradient[1]} 100%)`,
              }}
            />
            <span className="card-emoji" role="img" aria-label={article.categoryLabel}>
              {article.emoji}
            </span>
          </div>
        </div>
      )}
    </Link>
  );
}

export default function ArticleGrid({
  articles,
  categories,
}: {
  articles: Article[];
  categories: Category[];
}) {
  const [activeTag, setActiveTag] = useState("tous");
  const [search, setSearch] = useState("");

  const visible = useMemo(() => {
    const q = norm(search.trim());
    return articles.filter((a) => {
      const haystack = norm(
        [a.searchTerms, a.title, a.excerpt].join(" ")
      );
      const matchTag = activeTag === "tous" || a.category === activeTag;
      const matchText = q === "" || haystack.includes(q);
      return matchTag && matchText;
    });
  }, [articles, activeTag, search]);

  return (
    <>
      {/* Filter bar */}
      <div className="filter-bar">
        <div className="search-wrap">
          <svg
            className="search-icon"
            width="15"
            height="15"
            fill="none"
            stroke="currentColor"
            strokeWidth={2}
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <circle cx="11" cy="11" r="8" />
            <path d="m21 21-4.35-4.35" />
          </svg>
          <input
            className="search-input"
            type="search"
            placeholder="Rechercher par mot-clé…"
            autoComplete="off"
            aria-label="Rechercher un article"
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              if (e.target.value.trim() !== "") setActiveTag("tous");
            }}
          />
        </div>
        <div className="tags-wrap" role="group" aria-label="Filtrer par catégorie">
          <button
            className={`tag${activeTag === "tous" ? " active" : ""}`}
            onClick={() => {
              setActiveTag("tous");
              setSearch("");
            }}
          >
            Tous
          </button>
          {categories.map((c) => (
            <button
              key={c.slug}
              className={`tag${activeTag === c.slug ? " active" : ""}`}
              onClick={() => {
                setActiveTag(c.slug);
                setSearch("");
              }}
            >
              {c.label}
            </button>
          ))}
        </div>
      </div>

      {/* Results count */}
      <div className="results-line" aria-live="polite">
        <span>{visible.length}</span> article{visible.length > 1 ? "s" : ""}
      </div>

      {/* Grid */}
      <div className="articles-grid">
        {visible.length === 0 ? (
          <div className="no-results" role="status">
            <div style={{ fontSize: "2.5rem", marginBottom: 12 }}>🔍</div>
            <strong style={{ color: "var(--text-2)" }}>
              Aucun article trouvé
            </strong>
            <p>Essayez un autre mot-clé ou explorez toutes les catégories.</p>
          </div>
        ) : (
          visible.map((a, i) => (
            <ArticleCard key={a.slug} article={a} index={i} />
          ))
        )}
      </div>
    </>
  );
}

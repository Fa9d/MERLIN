import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import {
  getAllSlugs,
  getArticleBySlug,
  type Block,
} from "../articles";
import { SiteHeader, SiteFooter } from "../components";

// Génère statiquement une page par article (SSG)
export function generateStaticParams() {
  return getAllSlugs().map((slug) => ({ slug }));
}

// Metadata dynamique par article (Next 16 : params est async)
export async function generateMetadata(
  props: PageProps<"/[slug]">
): Promise<Metadata> {
  const { slug } = await props.params;
  const article = getArticleBySlug(slug);
  if (!article) return { title: "Article introuvable — IVIA" };
  return {
    title: `${article.title} — Blogue IVIA`,
    description: article.excerpt,
    openGraph: {
      title: article.title,
      description: article.excerpt,
      type: "article",
    },
  };
}

function renderBlock(block: Block, i: number) {
  switch (block.type) {
    case "h2":
      return <h2 key={i}>{block.text}</h2>;
    case "p":
      return <p key={i}>{block.text}</p>;
    case "quote":
      return <blockquote key={i}>{block.text}</blockquote>;
    case "ul":
      return (
        <ul key={i}>
          {block.items.map((item, j) => (
            <li key={j}>{item}</li>
          ))}
        </ul>
      );
  }
}

export default async function ArticlePage(props: PageProps<"/[slug]">) {
  const { slug } = await props.params;
  const article = getArticleBySlug(slug);

  if (!article) notFound();

  return (
    <>
      <SiteHeader />
      <article className="article-wrap">
        <Link href="/" className="back-link">
          ← Tous les articles
        </Link>

        <header className="article-header">
          <span
            className="article-emoji"
            role="img"
            aria-label={article.categoryLabel}
          >
            {article.emoji}
          </span>
          <div className="card-meta">
            <span className="card-cat">{article.categoryLabel}</span>
            <span className="card-dot">●</span>
            <span className="card-time">{article.readingTime}</span>
          </div>
          <h1 className="article-title">{article.title}</h1>
          <p className="article-excerpt">{article.excerpt}</p>
        </header>

        <div className="article-body">
          {article.content.map((block, i) => renderBlock(block, i))}
        </div>

        {article.sources && article.sources.length > 0 && (
          <div className="article-sources">
            <h2>Sources</h2>
            <ul>
              {article.sources.map((s) => (
                <li key={s.url}>
                  <a href={s.url} target="_blank" rel="noopener noreferrer">
                    {s.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        )}

        <div className="card-tags" style={{ marginTop: 40 }}>
          {article.tags.map((t) => (
            <span key={t} className="card-tag">
              {t}
            </span>
          ))}
        </div>
      </article>
      <SiteFooter />
    </>
  );
}

import Link from "next/link";

export function SiteHeader() {
  return (
    <header className="site-header">
      <div className="header-inner">
        <Link href="/" className="logo">
          <span className="logo-dot" />
          IVIA
        </Link>
        <a href="#checkin" className="nav-cta">
          Faire mon check-in →
        </a>
      </div>
    </header>
  );
}

export function SiteFooter() {
  return (
    <footer className="site-footer">
      <div className="page-wrap">
        <p>
          © 2025 IVIA — Contenu informatif uniquement. Ne remplace pas un
          professionnel de la santé mentale.
          <br />
          Sources :{" "}
          <a href="https://www.inspq.qc.ca" target="_blank" rel="noopener">
            INSPQ
          </a>{" "}
          ·{" "}
          <a href="https://www.ordrepsy.qc.ca" target="_blank" rel="noopener">
            OPQ
          </a>{" "}
          ·{" "}
          <a href="https://www.cnesst.gouv.qc.ca" target="_blank" rel="noopener">
            CNESST
          </a>{" "}
          ·{" "}
          <a href="https://www.msss.gouv.qc.ca" target="_blank" rel="noopener">
            MSSS Québec
          </a>
        </p>
      </div>
    </footer>
  );
}

export function ArrowIcon() {
  return (
    <svg
      width="14"
      height="14"
      fill="none"
      stroke="currentColor"
      strokeWidth={2}
      viewBox="0 0 24 24"
      aria-hidden="true"
    >
      <path d="M7 17 17 7M7 7h10v10" />
    </svg>
  );
}

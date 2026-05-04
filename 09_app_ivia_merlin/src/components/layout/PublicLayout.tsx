"use client";

import { useState } from "react";
import Link from "next/link";
import { ThemeToggle } from "@/components/theme-toggle";
import "@/app/styles.css";

function IviaLogo({ className = "" }: { className?: string }) {
  return (
    <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" className={className} aria-hidden="true">
      <circle cx="16" cy="16" r="14" stroke="currentColor" strokeWidth="1.5" />
      <circle cx="16" cy="16" r="2.5" fill="currentColor" />
      <line x1="16" y1="2" x2="16" y2="13.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      <line x1="16" y1="18.5" x2="16" y2="30" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      <line x1="2" y1="16" x2="13.5" y2="16" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
    </svg>
  );
}

type PublicLayoutProps = {
  children: React.ReactNode;
  /**
   * Page title — for SEO prefer `export const metadata` in the Server Component
   * parent. This prop is accepted for cases where a quick `<title>` override
   * is needed from a Client Component page.
   */
  title?: string;
};

export function PublicLayout({ children, title }: PublicLayoutProps) {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <>
      {title && <title>{title}</title>}

      <header className="hp-nav">
        <div className="hp-nav__inner">
          <Link href="/" className="hp-nav__logo" aria-label="IVIA — accueil">
            <IviaLogo className="hp-nav__logo-svg" />
            <span className="hp-nav__brand">IVIA</span>
          </Link>

          <nav
            className={`hp-nav__links${menuOpen ? " is-open" : ""}`}
            aria-label="Navigation principale"
          >
            <Link
              href="/"
              className="hp-nav__link"
              onClick={() => setMenuOpen(false)}
            >
              Accueil
            </Link>
            <Link
              href="/praticiens"
              className="hp-nav__link"
              onClick={() => setMenuOpen(false)}
            >
              Praticiens
            </Link>
            <Link
              href="/ressources"
              className="hp-nav__link"
              onClick={() => setMenuOpen(false)}
            >
              Ressources
            </Link>
          </nav>

          <div className="hp-nav__actions">
            <ThemeToggle />
            <Link href="/rendez-vous" className="hp-nav__cta">
              Prendre rendez-vous
            </Link>
            <button
              className="hp-nav__burger"
              aria-label={menuOpen ? "Fermer le menu" : "Ouvrir le menu"}
              aria-expanded={menuOpen}
              onClick={() => setMenuOpen(!menuOpen)}
            >
              <span />
              <span />
              <span />
            </button>
          </div>
        </div>
      </header>

      {children}

      <footer className="hp-footer">
        <div className="hp-section__inner hp-footer__inner">
          <Link href="/" className="hp-footer__logo" aria-label="IVIA">
            <IviaLogo className="hp-nav__logo-svg" />
            <span>IVIA</span>
          </Link>
          <p className="hp-footer__copy">
            &copy; {new Date().getFullYear()} IVIA. Montréal, Québec.
          </p>
          <nav className="hp-footer__links" aria-label="Liens du pied de page">
            <Link href="/confidentialite" className="hp-footer__link">
              Confidentialité
            </Link>
            <Link href="/cgu" className="hp-footer__link">CGU</Link>
            <Link href="/contact" className="hp-footer__link">Contact</Link>
          </nav>
        </div>
      </footer>
    </>
  );
}

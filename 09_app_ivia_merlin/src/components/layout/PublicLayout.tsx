"use client";

import { useState } from "react";
import Link from "next/link";
import { ThemeToggle } from "@/components/theme-toggle";
import { MesangeMark } from "@/components/MesangeMark";
import "@/app/styles.css";

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
          <Link href="/" className="hp-nav__logo" aria-label="MÉSANGES — un service IVIA, accueil">
            <MesangeMark
              size={28}
              bare
              ariaLabel="MÉSANGES — accueil"
              className="hp-nav__logo-mark"
            />
            <span className="hp-nav__brand">MÉSANGES</span>
            <span className="hp-nav__brand-sub" aria-hidden="true">
              un service IVIA
            </span>
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
              href="/demarche"
              className="hp-nav__link"
              onClick={() => setMenuOpen(false)}
            >
              Pour moi
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
          <Link href="/" className="hp-footer__logo" aria-label="MÉSANGES — un service IVIA">
            <MesangeMark size={24} bare ariaLabel="" className="hp-nav__logo-mark" />
            <span>MÉSANGES · IVIA</span>
          </Link>
          <p className="hp-footer__copy">
            &copy; {new Date().getFullYear()} IVIA. Montréal, Québec. Données au Québec.
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

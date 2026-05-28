"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import Image from "next/image";
import "@/app/styles.css";

const MESANGES_LOGO_SRC = "/assets/brand/ivia-mesanges-logo2000.png";

type PublicLayoutProps = {
  children: React.ReactNode;
  /**
   * Page title — for SEO prefer `export const metadata` in the Server Component
   * parent. This prop is accepted for cases where a quick `<title>` override
   * is needed from a Client Component page.
   */
  title?: string;
};

type AuthState = "anonymous" | "client" | "praticien";

function readAuthState(): AuthState {
  if (typeof window === "undefined") return "anonymous";
  try {
    if (window.localStorage.getItem("merlin_praticien_session")) return "praticien";
    const raw =
      window.localStorage.getItem("merlin_public_client_session") ??
      window.sessionStorage.getItem("merlin_public_client_session");
    if (raw) return "client";
  } catch {}
  return "anonymous";
}

export function PublicLayout({ children, title }: PublicLayoutProps) {
  const [menuOpen, setMenuOpen] = useState(false);
  const [authState, setAuthState] = useState<AuthState>("anonymous");

  useEffect(() => {
    setAuthState(readAuthState());
  }, []);

  return (
    <>
      {title && <title>{title}</title>}

      <header className="hp-nav">
        <div className="hp-nav__inner">
          <Link href="/" className="hp-nav__logo" aria-label="IVIA - MÉSANGES, accueil">
            <Image
              src={MESANGES_LOGO_SRC}
              alt="IVIA - MÉSANGES"
              width={36}
              height={36}
              priority
              className="hp-nav__logo-img"
            />
            <span className="hp-nav__brand">IVIA - MÉSANGES</span>
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
              href="/collectivites"
              className="hp-nav__link"
              onClick={() => setMenuOpen(false)}
            >
              Collectivités
            </Link>
            <Link
              href="/ressources"
              className="hp-nav__link"
              onClick={() => setMenuOpen(false)}
            >
              Ressources
            </Link>            <Link
              href="/praticiens/rejoindre"
              className="hp-nav__link"
              onClick={() => setMenuOpen(false)}
            >
              Pratiquer avec IVIA
            </Link>          </nav>

          <div className="hp-nav__actions" suppressHydrationWarning>
            {authState === "praticien" ? (
              <Link href="/espace-praticien" className="hp-nav__cta">
                Tableau de bord
              </Link>
            ) : authState === "client" ? (
              <Link href="/mon-espace" className="hp-nav__cta">
                Mon espace
              </Link>
            ) : (
              <Link href="/acces-client" className="hp-nav__cta">
                Connexion
              </Link>
            )}
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
            <span>MÉSANGES · Québec</span>
          </Link>
          <p className="hp-footer__copy">
            &copy; {new Date().getFullYear()} IVIA. Montréal. Données au Québec.
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

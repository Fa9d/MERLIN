"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import Image from "next/image";
import "@/app/styles.css";

import { LoginPopup } from "@/components/auth/LoginPopup";
import {
  PUBLIC_CLIENT_STORAGE_KEY,
  readStoredPublicClientSession,
  type LoginResponse,
} from "@/lib/merlin-api";

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

function roleDashboardHref(role: string): string {
  switch (role) {
    case "public_client":
      return "/mon-espace";
    case "practitioner":
      return "/espace-praticien";
    case "operator":
      return "/operator";
    case "supervisor":
      return "/supervision";
    case "admin_tech":
      return "/admin";
    default:
      return "/mon-espace";
  }
}

function roleDashboardLabel(role: string): string {
  switch (role) {
    case "public_client":
      return "Mon espace";
    case "practitioner":
      return "Espace praticien";
    case "operator":
      return "Espace opérateur";
    case "supervisor":
      return "Supervision";
    case "admin_tech":
      return "Admin";
    default:
      return "Mon espace";
  }
}

export function PublicLayout({ children, title }: PublicLayoutProps) {
  const [menuOpen, setMenuOpen] = useState(false);
  const [session, setSession] = useState<LoginResponse | null>(null);
  const [showLogin, setShowLogin] = useState(false);
  const [userMenuOpen, setUserMenuOpen] = useState(false);

  useEffect(() => {
    // Lecture initiale + synchronisation cross-onglets via l'évènement storage.
    setSession(readStoredPublicClientSession());

    const onStorage = (e: StorageEvent) => {
      if (e.key === PUBLIC_CLIENT_STORAGE_KEY) {
        setSession(readStoredPublicClientSession());
      }
    };
    window.addEventListener("storage", onStorage);
    return () => window.removeEventListener("storage", onStorage);
  }, []);

  const handleSignOut = useCallback(() => {
    window.localStorage.removeItem(PUBLIC_CLIENT_STORAGE_KEY);
    window.sessionStorage.removeItem(PUBLIC_CLIENT_STORAGE_KEY);
    setSession(null);
    setUserMenuOpen(false);
  }, []);

  const handleLoginSuccess = useCallback((s: LoginResponse) => {
    setSession(s);
  }, []);

  const dashboardHref = session ? roleDashboardHref(session.user.role) : "/mon-espace";
  const dashboardLabel = session ? roleDashboardLabel(session.user.role) : "Mon espace";

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
            <Link href="/" className="hp-nav__link" onClick={() => setMenuOpen(false)}>
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
            </Link>
          </nav>

          <div className="hp-nav__actions">
            {session ? (
              <div className="hp-nav__user">
                <button
                  type="button"
                  className="hp-nav__user-trigger"
                  aria-expanded={userMenuOpen ? "true" : "false"}
                  aria-haspopup="menu"
                  onClick={() => setUserMenuOpen((v) => !v)}
                >
                  <span className="hp-nav__user-greeting">
                    Bonjour <strong>{session.user.display_name || "vous"}</strong>
                  </span>
                  <span aria-hidden="true">▾</span>
                </button>
                {userMenuOpen ? (
                  <div className="hp-nav__user-menu" role="menu">
                    <Link
                      href={dashboardHref}
                      className="hp-nav__user-menu-item"
                      role="menuitem"
                      onClick={() => setUserMenuOpen(false)}
                    >
                      {dashboardLabel}
                    </Link>
                    <Link
                      href="/rendez-vous/reserver"
                      className="hp-nav__user-menu-item"
                      role="menuitem"
                      onClick={() => setUserMenuOpen(false)}
                    >
                      Réserver un créneau
                    </Link>
                    <button
                      type="button"
                      className="hp-nav__user-menu-item hp-nav__user-menu-item--danger"
                      role="menuitem"
                      onClick={handleSignOut}
                    >
                      Me déconnecter
                    </button>
                  </div>
                ) : null}
              </div>
            ) : (
              <button
                type="button"
                className="hp-nav__link hp-nav__login"
                onClick={() => setShowLogin(true)}
              >
                Se connecter
              </button>
            )}

            <Link
              href={session ? "/rendez-vous/reserver" : "/rendez-vous"}
              className="hp-nav__cta"
            >
              {session ? "Prendre rendez-vous" : "Faire une demande"}
            </Link>
            <button
              type="button"
              className="hp-nav__burger"
              aria-label={menuOpen ? "Fermer le menu" : "Ouvrir le menu"}
              aria-expanded={menuOpen ? "true" : "false"}
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
          <Link
            href="/"
            className="hp-footer__logo"
            aria-label="MÉSANGES — un service IVIA"
          >
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

      <LoginPopup
        isOpen={showLogin}
        onClose={() => setShowLogin(false)}
        onSuccess={handleLoginSuccess}
      />
    </>
  );
}

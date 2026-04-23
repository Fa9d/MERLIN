"use client";

import Link from "next/link";
import { FormEvent, useEffect, useState } from "react";

import { loginOperator, registerOperator, type LoginResponse } from "@/lib/merlin-api";

const STORAGE_KEY = "merlin_admin_session";

export default function AdminPage() {
  const [email, setEmail] = useState("admin@example.com");
  const [password, setPassword] = useState("admin-secret");
  const [session, setSession] = useState<LoginResponse | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const [isBootstrapping, setIsBootstrapping] = useState(false);

  useEffect(() => {
    if (typeof window === "undefined") {
      return;
    }

    window.setTimeout(() => {
      const stored = window.localStorage.getItem(STORAGE_KEY);
      if (!stored) {
        return;
      }

      try {
        setSession(JSON.parse(stored) as LoginResponse);
      } catch {
        window.localStorage.removeItem(STORAGE_KEY);
      }
    }, 0);
  }, []);

  async function handleLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsLoggingIn(true);
    setErrorMessage(null);
    setSuccessMessage(null);

    try {
      const result = await loginOperator(email, password);
      setSession(result);
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(result));
      setSuccessMessage("Session admin technique ouverte.");
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Connexion admin impossible.");
    } finally {
      setIsLoggingIn(false);
    }
  }

  async function handleBootstrapAdmin() {
    setIsBootstrapping(true);
    setErrorMessage(null);
    setSuccessMessage(null);

    try {
      await registerOperator({
        email,
        password,
        display_name: "Admin technique",
        role: "admin_tech",
      });
      const result = await loginOperator(email, password);
      setSession(result);
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(result));
      setSuccessMessage("Admin technique initialise et connecte.");
    } catch (error) {
      setErrorMessage(
        error instanceof Error ? error.message : "Impossible d'initialiser l'admin technique.",
      );
    } finally {
      setIsBootstrapping(false);
    }
  }

  function handleLogout() {
    if (typeof window !== "undefined") {
      window.localStorage.removeItem(STORAGE_KEY);
    }
    setSession(null);
    setErrorMessage(null);
    setSuccessMessage(null);
  }

  return (
    <div className="page-shell">
      <header className="topbar">
        <div className="wordmark">MERLIN / Admin</div>
        <nav className="nav">
          <Link href="/">Accueil</Link>
          <Link href="/operator">Operateur</Link>
          <Link href="/supervision">Supervision</Link>
        </nav>
      </header>

      <main className="section">
        <div className="section-header">
          <div className="eyebrow">SCR-301 a SCR-303</div>
          <h2>Administration technique minimale</h2>
          <p>
            Cet espace sert au bootstrap initial et a la connexion du role
            <span className="mono"> admin_tech</span>. Il ne doit pas etre confondu avec la
            production operateur.
          </p>
        </div>

        {!session ? (
          <form className="card form-stack operator-auth-card" onSubmit={handleLogin}>
            <h3>Connexion admin technique</h3>
            <label className="field">
              <span>Courriel</span>
              <input value={email} onChange={(event) => setEmail(event.target.value)} type="email" />
            </label>
            <label className="field">
              <span>Mot de passe</span>
              <input
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                type="password"
              />
            </label>
            <div className="cta-row">
              <button className="button button-primary" disabled={isLoggingIn} type="submit">
                {isLoggingIn ? "Connexion..." : "Se connecter"}
              </button>
              <button
                className="button button-secondary"
                disabled={isBootstrapping}
                onClick={handleBootstrapAdmin}
                type="button"
              >
                {isBootstrapping ? "Initialisation..." : "Initialiser admin technique"}
              </button>
            </div>
            <p className="inline-note">
              Utiliser cet ecran seulement pour le bootstrap et la maintenance technique.
            </p>
            {errorMessage ? <p className="message message-error">{errorMessage}</p> : null}
            {successMessage ? <p className="message message-success">{successMessage}</p> : null}
          </form>
        ) : (
          <article className="card form-stack">
            <h3>Session admin</h3>
            <p>
              Connecte comme <span className="mono">{session.user.email}</span>
            </p>
            <p>Role: {session.user.role}</p>
            {session.user.role !== "admin_tech" ? (
              <p className="message message-error">
                Ce compte n&apos;est pas un admin technique. Cet espace n&apos;est pas destine a la
                production operateur.
              </p>
            ) : (
              <p className="inline-note">
                La console admin complete viendra ensuite. Pour le Sprint A, cet ecran isole
                simplement le bootstrap et l&apos;authentification technique.
              </p>
            )}
            {successMessage ? <p className="message message-success">{successMessage}</p> : null}
            <div className="cta-row">
              <Link className="button button-secondary" href="/operator">
                Retour operateur
              </Link>
              <button className="button button-secondary" onClick={handleLogout} type="button">
                Se deconnecter
              </button>
            </div>
          </article>
        )}
      </main>
    </div>
  );
}

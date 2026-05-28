"use client";

import Link from "next/link";
import { Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { FormEvent, useState } from "react";

import { PublicLayout } from "@/components/layout/PublicLayout";
import {
  holdSlot,
  loginUser,
  PUBLIC_CLIENT_STORAGE_KEY,
} from "@/lib/merlin-api";

function buildRendezVousHref(params: {
  praticienName: string;
  slotDate: string;
  slotTime: string;
  sessionType: string;
  slotId: string;
  urgency: boolean;
  slotHeld?: boolean;
  holdExpiresAt?: string | null;
}): string {
  const query = new URLSearchParams();
  if (params.praticienName) query.set("praticienName", params.praticienName);
  if (params.slotDate) query.set("slotDate", params.slotDate);
  if (params.slotTime) query.set("slotTime", params.slotTime);
  if (params.sessionType) query.set("sessionType", params.sessionType);
  if (params.slotId) query.set("slotId", params.slotId);
  if (params.urgency) query.set("urgency", "true");
  if (params.slotHeld) query.set("slotHeld", "true");
  if (params.holdExpiresAt) query.set("holdExpiresAt", params.holdExpiresAt);
  return `/rendez-vous?${query.toString()}`;
}

function AccesClientContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const praticienName = searchParams.get("praticienName") ?? "";
  const slotDate = searchParams.get("slotDate") ?? "";
  const slotTime = searchParams.get("slotTime") ?? "";
  const sessionType = searchParams.get("sessionType") ?? "";
  const slotId = searchParams.get("slotId") ?? "";
  const urgency = searchParams.get("urgency") === "true";

  const [mode, setMode] = useState<"client" | "praticien" | null>(null);
  const [loginEmail, setLoginEmail] = useState("");
  const [loginPassword, setLoginPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isLoggingIn, setIsLoggingIn] = useState(false);

  async function handleLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsLoggingIn(true);
    setErrorMessage(null);

    try {
      const session = await loginUser(loginEmail.trim(), loginPassword);

      const isPraticien = ["practitioner", "operator", "admin"].includes(session.user.role);

      // Cookie de session pour le middleware Next.js (routes protégées)
      const maxAge = 60 * 60 * 24; // 24 h
      document.cookie = `session_token=${session.access_token}; path=/; max-age=${maxAge}; samesite=lax`;

      if (isPraticien) {
        // Praticien : stocker uniquement sous la clé praticien (pas dans PUBLIC_CLIENT_STORAGE_KEY)
        window.localStorage.setItem("merlin_praticien_session", JSON.stringify(session));
      } else {
        // Client : stocker sous la clé client
        window.sessionStorage.setItem(PUBLIC_CLIENT_STORAGE_KEY, JSON.stringify(session));
        window.localStorage.setItem(PUBLIC_CLIENT_STORAGE_KEY, JSON.stringify(session));
      }

      if (slotId && !isPraticien) {
        const slot = await holdSlot(slotId, session.access_token);
        router.push(
          buildRendezVousHref({
            praticienName,
            slotDate,
            slotTime,
            sessionType,
            slotId,
            urgency,
            slotHeld: true,
            holdExpiresAt: slot.hold_expires_at,
          }),
        );
      } else if (isPraticien) {
        router.push("/espace-praticien");
      } else {
        router.push("/mon-espace");
      }
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Erreur de connexion.");
    } finally {
      setIsLoggingIn(false);
    }
  }

  return (
    <PublicLayout>
      <div className="page-shell">
        <main className="section public-access-main">
          <div className="section-header public-access-header">
            <div className="eyebrow">Connexion</div>
            <h1>Accédez à votre espace.</h1>
            {slotId ? (
              <p>
                Votre créneau sera réservé pendant 15 minutes après la connexion.
              </p>
            ) : (
              <p>Client, praticien ou opérateur — connectez-vous pour accéder à votre espace.</p>
            )}
          </div>

          <div className="public-access-mode-selector">
            <button
              type="button"
              className={`public-access-mode-card${mode === "client" ? " is-selected" : ""}`}
              onClick={() => setMode("client")}
            >
              <span className="public-access-mode-card__title">Client</span>
              <span className="public-access-mode-card__desc">Votre dossier et vos documents</span>
            </button>
            <button
              type="button"
              className={`public-access-mode-card${mode === "praticien" ? " is-selected" : ""}`}
              onClick={() => setMode("praticien")}
            >
              <span className="public-access-mode-card__title">Praticien · Opérateur</span>
              <span className="public-access-mode-card__desc">Tableau de bord et gestion</span>
            </button>
          </div>

          {mode !== null && (
          <form className="card form-stack public-access-form" onSubmit={handleLogin}>
            <label className="field">
              <span>Courriel</span>
              <input
                required
                type="email"
                autoComplete="email"
                value={loginEmail}
                onChange={(event) => setLoginEmail(event.target.value)}
                placeholder="nom@exemple.com"
              />
            </label>
            <label className="field">
              <span>Mot de passe</span>
              <input
                required
                type="password"
                autoComplete="current-password"
                value={loginPassword}
                onChange={(event) => setLoginPassword(event.target.value)}
                placeholder="Votre mot de passe"
              />
            </label>
            {errorMessage ? (
              <p className="message message-error">{errorMessage}</p>
            ) : null}
            <button className="button button-primary" disabled={isLoggingIn} type="submit">
              {isLoggingIn ? "Connexion en cours…" : "Se connecter"}
            </button>
            {mode === "client" && (
              <p className="inline-note" style={{ textAlign: "center" }}>
                Pas encore de compte ?{" "}
                <Link href="/rejoindre">Créer mon espace →</Link>
              </p>
            )}
          </form>
          )}
        </main>
      </div>
    </PublicLayout>
  );
}

export default function AccesClientPage() {
  return (
    <Suspense
      fallback={
        <PublicLayout>
          <div className="page-shell">
            <main className="section public-access-main">
              <p className="inline-note">Chargement…</p>
            </main>
          </div>
        </PublicLayout>
      }
    >
      <AccesClientContent />
    </Suspense>
  );
}
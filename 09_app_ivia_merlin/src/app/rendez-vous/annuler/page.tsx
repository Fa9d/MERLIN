"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { FormEvent, Suspense, useEffect, useState } from "react";

import { PublicLayout } from "@/components/layout/PublicLayout";
import {
  cancelSlot,
  loginUser,
  PUBLIC_CLIENT_STORAGE_KEY,
  type LoginResponse,
} from "@/lib/merlin-api";

function readStoredSession(): LoginResponse | null {
  if (typeof window === "undefined") {
    return null;
  }

  const raw = window.localStorage.getItem(PUBLIC_CLIENT_STORAGE_KEY)
    ?? window.sessionStorage.getItem(PUBLIC_CLIENT_STORAGE_KEY);

  if (!raw) {
    return null;
  }

  try {
    return JSON.parse(raw) as LoginResponse;
  } catch {
    return null;
  }
}

function persistSession(session: LoginResponse): void {
  window.localStorage.setItem(PUBLIC_CLIENT_STORAGE_KEY, JSON.stringify(session));
  window.sessionStorage.setItem(PUBLIC_CLIENT_STORAGE_KEY, JSON.stringify(session));
}

function AnnulerRendezVousContent() {
  const searchParams = useSearchParams();
  const slotId = searchParams.get("slot") ?? "";

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isCheckingSession, setIsCheckingSession] = useState(true);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    if (!slotId) {
      setIsCheckingSession(false);
      return;
    }

    const storedSession = readStoredSession();
    if (!storedSession) {
      setIsCheckingSession(false);
      return;
    }
    const activeSession = storedSession;

    let active = true;

    async function cancelWithStoredSession() {
      try {
        await cancelSlot(slotId, activeSession.access_token);
        if (!active) return;
        setSuccessMessage("Votre rendez-vous a bien été annulé.");
      } catch (error) {
        if (!active) return;
        setErrorMessage(
          error instanceof Error
            ? error.message
            : "Impossible d'annuler ce rendez-vous.",
        );
      } finally {
        if (active) setIsCheckingSession(false);
      }
    }

    void cancelWithStoredSession();

    return () => {
      active = false;
    };
  }, [slotId]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSubmitting(true);
    setErrorMessage(null);
    setSuccessMessage(null);

    try {
      const session = await loginUser(email.trim(), password);
      persistSession(session);
      await cancelSlot(slotId, session.access_token);
      setSuccessMessage("Votre rendez-vous a bien été annulé.");
    } catch (error) {
      setErrorMessage(
        error instanceof Error ? error.message : "Impossible d'annuler ce rendez-vous.",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <PublicLayout>
      <div className="page-shell">
        <main className="section public-access-main">
          <div className="section-header public-access-header">
            <div className="eyebrow">Annulation</div>
            <h1>Annuler un rendez-vous confirme</h1>
            <p>
              Le lien du courriel permet d&apos;annuler votre rendez-vous. Si vous n&apos;etes pas déjà reconnu,
              reconnectez-vous avec le compte client utilisé pour la réservation.
            </p>
          </div>

          <section className="card rendezvous-context-card">
            <div className="info-strip">
              <span>Rendez-vous confirme</span>
              {slotId ? <span>Ref. {slotId.slice(0, 8)}</span> : null}
            </div>
            {!slotId ? (
              <p className="message message-error">
                Lien d&apos;annulation incomplet. Le numéro de créneau est manquant.
              </p>
            ) : null}
            {isCheckingSession && slotId ? (
              <p className="inline-note">Verification de votre session en cours...</p>
            ) : null}
            {successMessage ? <p className="message message-success">{successMessage}</p> : null}
            {errorMessage ? <p className="message message-error">{errorMessage}</p> : null}
          </section>

          {!successMessage && slotId ? (
            <form className="card form-stack" onSubmit={handleSubmit}>
              <h2>Me reconnecter pour annuler</h2>
              <label className="field">
                <span>Courriel</span>
                <input
                  required
                  type="email"
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  placeholder="nom@exemple.com"
                />
              </label>
              <label className="field">
                <span>Mot de passe</span>
                <input
                  required
                  type="password"
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  placeholder="Votre mot de passe"
                />
              </label>
              <button className="button button-primary" disabled={isSubmitting || isCheckingSession} type="submit">
                {isSubmitting ? "Annulation en cours..." : "Me connecter et annuler"}
              </button>
            </form>
          ) : null}

          <div className="public-access-actions">
            <Link href="/" className="button button-secondary">
              Retour a l&apos;accueil
            </Link>
            <Link href="/rendez-vous" className="button button-ghost">
              Nouveau parcours rendez-vous
            </Link>
          </div>
        </main>
      </div>
    </PublicLayout>
  );
}

export default function AnnulerRendezVousPage() {
  return (
    <Suspense
      fallback={
        <PublicLayout>
          <div className="page-shell">
            <main className="section public-access-main">
              <p className="inline-note">Chargement de l&apos;annulation…</p>
            </main>
          </div>
        </PublicLayout>
      }
    >
      <AnnulerRendezVousContent />
    </Suspense>
  );
}
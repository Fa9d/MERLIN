"use client";

import Link from "next/link";
import { Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { FormEvent, useMemo, useState } from "react";

import { PublicLayout } from "@/components/layout/PublicLayout";
import {
  holdSlot,
  loginUser,
  PUBLIC_CLIENT_STORAGE_KEY,
  registerClient,
  type BookingSlotRecord,
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
  const searchParams = useSearchParams();
  const praticienName = searchParams.get("praticienName") ?? "";
  const slotDate = searchParams.get("slotDate") ?? "";
  const slotTime = searchParams.get("slotTime") ?? "";
  const sessionType = searchParams.get("sessionType") ?? "";
  const slotId = searchParams.get("slotId") ?? "";
  const urgency = searchParams.get("urgency") === "true";

  const [registerName, setRegisterName] = useState("");
  const [registerEmail, setRegisterEmail] = useState("");
  const [registerPassword, setRegisterPassword] = useState("");
  const [loginEmail, setLoginEmail] = useState("");
  const [loginPassword, setLoginPassword] = useState("");
  const [registerMessage, setRegisterMessage] = useState<string | null>(null);
  const [loginMessage, setLoginMessage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isRegistering, setIsRegistering] = useState(false);
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const [heldSlot, setHeldSlot] = useState<BookingSlotRecord | null>(null);

  const rendezVousHref = useMemo(
    () =>
      buildRendezVousHref({
        praticienName,
        slotDate,
        slotTime,
        sessionType,
        slotId,
        urgency,
      }),
    [praticienName, sessionType, slotDate, slotId, slotTime, urgency],
  );

  const redirectPath = useMemo(() => {
    const query = new URLSearchParams();
    if (praticienName) query.set("praticienName", praticienName);
    if (slotDate) query.set("slotDate", slotDate);
    if (slotTime) query.set("slotTime", slotTime);
    if (sessionType) query.set("sessionType", sessionType);
    if (slotId) query.set("slotId", slotId);
    if (urgency) query.set("urgency", "true");
    return `/acces-client?${query.toString()}`;
  }, [praticienName, sessionType, slotDate, slotId, slotTime, urgency]);

  const heldRendezVousHref = useMemo(() => {
    if (!heldSlot) return rendezVousHref;
    return buildRendezVousHref({
      praticienName,
      slotDate,
      slotTime,
      sessionType,
      slotId,
      urgency,
      slotHeld: true,
      holdExpiresAt: heldSlot.hold_expires_at,
    });
  }, [heldSlot, praticienName, rendezVousHref, sessionType, slotDate, slotId, slotTime, urgency]);

  async function handleRegister(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsRegistering(true);
    setRegisterMessage(null);
    setErrorMessage(null);

    try {
      const result = await registerClient({
        email: registerEmail.trim(),
        password: registerPassword,
        display_name: registerName.trim(),
        redirect_path: redirectPath,
      });
      setRegisterMessage(result.message);
      setLoginEmail(registerEmail.trim());
      setRegisterPassword("");
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Erreur inconnue.");
    } finally {
      setIsRegistering(false);
    }
  }

  async function handleLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsLoggingIn(true);
    setLoginMessage(null);
    setErrorMessage(null);

    try {
      const session = await loginUser(loginEmail.trim(), loginPassword);
      window.sessionStorage.setItem(PUBLIC_CLIENT_STORAGE_KEY, JSON.stringify(session));
      window.localStorage.setItem(PUBLIC_CLIENT_STORAGE_KEY, JSON.stringify(session));

      if (!slotId) {
        setLoginMessage("Connexion réussie. Vous pouvez revenir à votre demande.");
        return;
      }

      const slot = await holdSlot(slotId, session.access_token);
      setHeldSlot(slot);
      setLoginMessage("Connexion réussie. Le créneau est maintenant tenu pendant 15 minutes.");
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Erreur inconnue.");
    } finally {
      setIsLoggingIn(false);
    }
  }

  return (
    <PublicLayout>
      <div className="page-shell">
        <main className="section public-access-main">
          <div className="section-header public-access-header">
            <div className="eyebrow">Acces client</div>
            <h1>Activez votre acces pour tenir un créneau.</h1>
            <p>
              Le hold réel d&apos;un créneau public demande un compte client, un courriel vérifié,
              puis une connexion.
            </p>
          </div>

          <section className="card rendezvous-context-card">
            <div className="info-strip">
              <span>{urgency ? "Urgence 30 min" : "Reservation praticien"}</span>
              {slotDate || slotTime ? <span>{[slotDate, slotTime].filter(Boolean).join(" ")}</span> : null}
            </div>
            {praticienName ? <p className="inline-note">Praticien demandé: {praticienName}</p> : null}
            {sessionType ? <p className="inline-note">Type de séance: {sessionType}</p> : null}
            {slotId ? <p className="inline-note">Un hold de 15 minutes sera posé après connexion.</p> : null}
          </section>

          <div className="grid public-access-grid">
            <form className="card form-stack" onSubmit={handleRegister}>
              <h2>Créer mon accès</h2>
              <label className="field">
                <span>Nom affiché</span>
                <input
                  required
                  value={registerName}
                  onChange={(event) => setRegisterName(event.target.value)}
                  placeholder="Prenom ou alias"
                />
              </label>
              <label className="field">
                <span>Courriel</span>
                <input
                  required
                  type="email"
                  value={registerEmail}
                  onChange={(event) => setRegisterEmail(event.target.value)}
                  placeholder="nom@exemple.com"
                />
              </label>
              <label className="field">
                <span>Mot de passe</span>
                <input
                  required
                  minLength={8}
                  type="password"
                  value={registerPassword}
                  onChange={(event) => setRegisterPassword(event.target.value)}
                  placeholder="8 caracteres minimum"
                />
              </label>
              <button className="button button-primary" disabled={isRegistering} type="submit">
                {isRegistering ? "Creation en cours..." : "Creer mon compte"}
              </button>
              <p className="inline-note">
                Vous recevrez un courriel d&apos;activation. Le lien vous ramènera ici pour continuer.
              </p>
              {registerMessage ? <p className="message message-success">{registerMessage}</p> : null}
            </form>

            <form className="card form-stack" onSubmit={handleLogin}>
              <h2>Me connecter</h2>
              <label className="field">
                <span>Courriel</span>
                <input
                  required
                  type="email"
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
                  value={loginPassword}
                  onChange={(event) => setLoginPassword(event.target.value)}
                  placeholder="Votre mot de passe"
                />
              </label>
              <button className="button button-secondary" disabled={isLoggingIn} type="submit">
                {isLoggingIn ? "Connexion en cours..." : slotId ? "Me connecter et tenir le créneau" : "Me connecter"}
              </button>
              <p className="inline-note">
                Si votre courriel n&apos;est pas encore vérifié, activez d&apos;abord le lien reçu par mail.
              </p>
              {loginMessage ? <p className="message message-success">{loginMessage}</p> : null}
              {heldSlot ? (
                <div className="public-access-actions">
                  <Link href={heldRendezVousHref} className="button button-primary">
                    Revenir a la demande avec le créneau tenu
                  </Link>
                </div>
              ) : (
                <div className="public-access-actions">
                  <Link href={rendezVousHref} className="button button-ghost">
                    Revenir a la demande
                  </Link>
                </div>
              )}
            </form>
          </div>

          {errorMessage ? <p className="message message-error">{errorMessage}</p> : null}
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
              <p className="inline-note">Chargement du parcours d&apos;acces…</p>
            </main>
          </div>
        </PublicLayout>
      }
    >
      <AccesClientContent />
    </Suspense>
  );
}
"use client";

import Link from "next/link";
import { FormEvent, useEffect, useRef, useState } from "react";

import {
  loginUser,
  PUBLIC_CLIENT_STORAGE_KEY,
  type LoginResponse,
} from "@/lib/merlin-api";

type LoginPopupProps = {
  isOpen: boolean;
  onClose: () => void;
  onSuccess?: (session: LoginResponse) => void;
};

export function LoginPopup({ isOpen, onClose, onSuccess }: LoginPopupProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const firstInputRef = useRef<HTMLInputElement | null>(null);

  useEffect(() => {
    if (!isOpen) return;
    firstInputRef.current?.focus();
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsLoggingIn(true);
    setErrorMessage(null);

    try {
      const session = await loginUser(email.trim(), password);
      const serialized = JSON.stringify(session);
      window.localStorage.setItem(PUBLIC_CLIENT_STORAGE_KEY, serialized);
      window.sessionStorage.setItem(PUBLIC_CLIENT_STORAGE_KEY, serialized);
      onSuccess?.(session);
      onClose();
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Erreur inconnue.");
    } finally {
      setIsLoggingIn(false);
    }
  }

  return (
    <div
      className="login-popup-backdrop"
      role="dialog"
      aria-modal="true"
      aria-labelledby="login-popup-title"
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div className="login-popup">
        <button
          type="button"
          className="login-popup__close"
          aria-label="Fermer"
          onClick={onClose}
        >
          ×
        </button>

        <h3 id="login-popup-title">Se connecter à IVIA</h3>
        <p className="inline-note">
          Entrez vos identifiants pour ouvrir votre espace personnel.
        </p>

        <form onSubmit={handleSubmit} className="form-stack">
          <label className="field">
            <span>Courriel</span>
            <input
              ref={firstInputRef}
              required
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="nom@exemple.com"
            />
          </label>

          <label className="field">
            <span>Mot de passe</span>
            <input
              required
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
            />
          </label>

          <button
            type="submit"
            className="button button-primary"
            disabled={isLoggingIn}
          >
            {isLoggingIn ? "Connexion…" : "Se connecter"}
          </button>

          {errorMessage ? (
            <p className="message message-error">{errorMessage}</p>
          ) : null}
        </form>

        <div className="login-popup__divider">
          <span>ou</span>
        </div>

        <div className="login-popup__alt">
          <Link href="/rendez-vous" className="button button-secondary" onClick={onClose}>
            Première fois — Faire une demande
          </Link>
          <p className="inline-note">
            Vous n&apos;avez pas de mot de passe ? Faites une nouvelle demande pour recevoir
            un lien d&apos;activation par courriel.
          </p>
        </div>
      </div>
    </div>
  );
}

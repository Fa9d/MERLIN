"use client";

import Link from "next/link";
import { FormEvent, useEffect, useRef, useState } from "react";

import {
  startPublicIntake,
  type PublicIntakeStartResult,
} from "@/lib/merlin-api";

type RegisterPopupProps = {
  isOpen: boolean;
  onClose: () => void;
  /**
   * Marqueur d'origine pour traçabilité (`entry_summary_text` de l'intake).
   * Ex. "Inscription depuis /ressources".
   */
  source?: string;
};

export function RegisterPopup({ isOpen, onClose, source }: RegisterPopupProps) {
  const [firstNameOrAlias, setFirstNameOrAlias] = useState("");
  const [email, setEmail] = useState("");
  const [agreed, setAgreed] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [result, setResult] = useState<PublicIntakeStartResult | null>(null);
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

  // Reset état quand la popup se referme
  useEffect(() => {
    if (!isOpen) {
      setResult(null);
      setErrorMessage(null);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSubmitting(true);
    setErrorMessage(null);

    try {
      const response = await startPublicIntake({
        first_name_or_alias: firstNameOrAlias.trim(),
        email: email.trim(),
        phone: null,
        is_adult_confirmed: true,
        primary_need_code: "other",
        perceived_urgency_code: "non_urgent",
        support_already_in_place: false,
        requested_outcome_text: null,
        entry_summary_text: source ?? "Inscription rapide depuis le site",
        consent_terms_accepted: true,
        consent_terms_version: "v1.2",
      });
      setResult(response);
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Erreur inconnue.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div
      className="login-popup-backdrop"
      role="dialog"
      aria-modal="true"
      aria-labelledby="register-popup-title"
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

        {result ? (
          <>
            <h3 id="register-popup-title">Bienvenue dans la maison du vivant</h3>
            <p>
              Un courriel d&apos;activation vient d&apos;être envoyé à{" "}
              <strong className="mono">{result.email_used}</strong>.
            </p>
            <p className="inline-note">
              Ouvrez votre boîte mail (vérifiez aussi les indésirables) et cliquez
              sur <strong>Ouvrir mon espace IVIA</strong>. Lien valide 7 jours.
            </p>
            <div className="public-access-actions">
              <button type="button" className="button button-primary" onClick={onClose}>
                Fermer
              </button>
              <Link href="/ressources" className="button button-secondary" onClick={onClose}>
                Continuer à lire
              </Link>
            </div>
          </>
        ) : (
          <>
            <h3 id="register-popup-title">Créer mon compte IVIA</h3>
            <p className="inline-note">
              Ouvrez un espace personnel pour suivre votre démarche, accéder aux
              ressources réservées aux membres et garder le fil au fil des semaines.
            </p>

            <form onSubmit={handleSubmit} className="form-stack">
              <label className="field">
                <span>Comment souhaitez-vous être appelé ?</span>
                <input
                  ref={firstInputRef}
                  required
                  value={firstNameOrAlias}
                  onChange={(e) => setFirstNameOrAlias(e.target.value)}
                  placeholder="Prénom ou alias"
                />
              </label>

              <label className="field">
                <span>Courriel</span>
                <input
                  required
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="nom@exemple.com"
                />
              </label>

              <label className="checkbox-row">
                <input
                  type="checkbox"
                  checked={agreed}
                  onChange={(e) => setAgreed(e.target.checked)}
                />
                <span>
                  Je confirme être majeur et j&apos;accepte que mes coordonnées soient
                  enregistrées pour ouvrir un espace personnel IVIA. Mes données
                  restent au Québec (Loi 25) et ne sont jamais partagées sans mon
                  consentement explicite.
                </span>
              </label>

              <button
                type="submit"
                className="button button-primary"
                disabled={isSubmitting || !agreed}
              >
                {isSubmitting ? "Envoi en cours…" : "Recevoir mon lien d'activation"}
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
                Faire une demande de séance détaillée
              </Link>
              <p className="inline-note">
                Préférable si vous voulez préparer dès maintenant votre première séance avec un praticien.
              </p>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

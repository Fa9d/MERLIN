"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";

import { PublicLayout } from "@/components/layout/PublicLayout";
import {
  loginUser,
  PUBLIC_CLIENT_STORAGE_KEY,
  registerClient,
} from "@/lib/merlin-api";

export default function RejoindreClientPage() {
  const router = useRouter();

  const [displayName, setDisplayName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConfirm, setPasswordConfirm] = useState("");

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [successEmail, setSuccessEmail] = useState<string | null>(null);

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setErrorMessage(null);

    if (password !== passwordConfirm) {
      setErrorMessage("Les deux mots de passe ne correspondent pas.");
      return;
    }
    if (password.length < 8) {
      setErrorMessage("Le mot de passe doit contenir au moins 8 caractères.");
      return;
    }

    setIsSubmitting(true);
    try {
      await registerClient({
        email: email.trim().toLowerCase(),
        password,
        display_name: displayName.trim(),
      });

      // Connexion automatique après inscription
      const session = await loginUser(email.trim().toLowerCase(), password);
      const maxAge = 60 * 60 * 24;
      document.cookie = `session_token=${session.access_token}; path=/; max-age=${maxAge}; samesite=lax`;
      window.localStorage.setItem(PUBLIC_CLIENT_STORAGE_KEY, JSON.stringify(session));
      window.sessionStorage.setItem(PUBLIC_CLIENT_STORAGE_KEY, JSON.stringify(session));

      setSuccessEmail(email.trim().toLowerCase());
      router.push("/mon-espace");
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Erreur inattendue.";
      if (msg.includes("409") || msg.toLowerCase().includes("existe déjà") || msg.toLowerCase().includes("existe deja")) {
        setErrorMessage(
          "Un compte existe déjà avec cette adresse. Connectez-vous à la place.",
        );
      } else {
        setErrorMessage(msg);
      }
    } finally {
      setIsSubmitting(false);
    }
  }

  if (successEmail) {
    return (
      <PublicLayout>
        <div className="page-shell">
          <main className="section public-access-main">
            <div className="section-header public-access-header">
              <div className="eyebrow">Bienvenue</div>
              <h1>Votre espace est prêt.</h1>
              <p>
                Un courriel de confirmation a été envoyé à{" "}
                <strong>{successEmail}</strong>.{" "}
                Vous pouvez déjà naviguer — la vérification sera demandée avant
                votre premier rendez-vous.
              </p>
            </div>
            <Link href="/mon-espace" className="button button-primary">
              Accéder à mon espace →
            </Link>
          </main>
        </div>
      </PublicLayout>
    );
  }

  return (
    <PublicLayout>
      <div className="page-shell">
        <main className="section public-access-main">
          <div className="section-header public-access-header">
            <div className="eyebrow">Inscription</div>
            <h1>Créez votre espace IVIA.</h1>
            <p>
              Accès immédiat. Aucune carte de crédit requise.
            </p>
          </div>

          <form
            className="card form-stack public-access-form"
            onSubmit={handleSubmit}
          >
            <label className="field">
              <span>Prénom ou pseudonyme</span>
              <input
                required
                type="text"
                autoComplete="given-name"
                value={displayName}
                onChange={(e) => setDisplayName(e.target.value)}
                placeholder="Comment vous appeler ?"
                maxLength={80}
              />
            </label>

            <label className="field">
              <span>Courriel</span>
              <input
                required
                type="email"
                autoComplete="email"
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
                autoComplete="new-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Au moins 8 caractères"
                minLength={8}
              />
            </label>

            <label className="field">
              <span>Confirmer le mot de passe</span>
              <input
                required
                type="password"
                autoComplete="new-password"
                value={passwordConfirm}
                onChange={(e) => setPasswordConfirm(e.target.value)}
                placeholder="Répétez votre mot de passe"
                minLength={8}
              />
            </label>

            {errorMessage ? (
              <p className="message message-error">
                {errorMessage}{" "}
                {errorMessage.includes("existe déjà") && (
                  <Link href="/acces-client">Se connecter →</Link>
                )}
              </p>
            ) : null}

            <button
              className="button button-primary"
              type="submit"
              disabled={isSubmitting}
            >
              {isSubmitting ? "Création en cours…" : "Créer mon espace →"}
            </button>

            <p className="inline-note" style={{ textAlign: "center" }}>
              Déjà un compte ?{" "}
              <Link href="/acces-client">Se connecter</Link>
            </p>
          </form>
        </main>
      </div>
    </PublicLayout>
  );
}

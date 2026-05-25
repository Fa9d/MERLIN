"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Suspense, useCallback, useEffect, useState } from "react";

import { PublicLayout } from "@/components/layout/PublicLayout";
import {
  consumeMagicLink,
  previewMagicLink,
  PUBLIC_CLIENT_STORAGE_KEY,
  type PublicActivatePreview,
  type PublicActivateResult,
} from "@/lib/merlin-api";

type PreviewState =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "valid"; preview: PublicActivatePreview }
  | { status: "invalid"; reason: string };

function ActiverContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const token = searchParams.get("token") ?? "";

  const [preview, setPreview] = useState<PreviewState>({ status: "idle" });
  const [isOpening, setIsOpening] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    if (!token) {
      setPreview({ status: "invalid", reason: "Aucun token fourni." });
      return;
    }

    let cancelled = false;
    setPreview({ status: "loading" });

    previewMagicLink(token)
      .then((data) => {
        if (cancelled) return;
        if (data.valid) {
          setPreview({ status: "valid", preview: data });
        } else {
          setPreview({
            status: "invalid",
            reason: "Lien expiré ou déjà utilisé.",
          });
        }
      })
      .catch((error: unknown) => {
        if (cancelled) return;
        const message = error instanceof Error ? error.message : "Erreur inconnue.";
        setPreview({ status: "invalid", reason: message });
      });

    return () => {
      cancelled = true;
    };
  }, [token]);

  const handleOpenSpace = useCallback(async () => {
    if (!token) return;
    setIsOpening(true);
    setErrorMessage(null);
    try {
      const result: PublicActivateResult = await consumeMagicLink(token);

      // Compose une session compatible avec le format `LoginResponse` utilisé
      // ailleurs pour rester homogène avec /acces-client.
      const sessionPayload = {
        access_token: result.access_token,
        token_type: result.token_type,
        user: {
          id: result.user_id,
          email: result.email,
          display_name: result.display_name,
          role: result.role,
          created_at: "",
          updated_at: "",
        },
      };
      const serialized = JSON.stringify(sessionPayload);
      window.localStorage.setItem(PUBLIC_CLIENT_STORAGE_KEY, serialized);
      window.sessionStorage.setItem(PUBLIC_CLIENT_STORAGE_KEY, serialized);
      // Cookie pour le middleware (cohérence avec /acces-client)
      document.cookie = `session_token=${result.access_token}; path=/; max-age=${60 * 60 * 24}; samesite=lax`;

      const nextParams = new URLSearchParams();
      if (result.password_needed) nextParams.set("welcome", "magic");
      const query = nextParams.toString();
      router.replace(`/mon-espace${query ? `?${query}` : ""}`);
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Erreur inconnue.");
      setIsOpening(false);
    }
  }, [router, token]);

  return (
    <PublicLayout>
      <div className="page-shell">
        <main className="section">
          <div className="section-header">
            <div className="eyebrow">Activation</div>
            <h2>Bienvenue dans la maison du vivant.</h2>
          </div>

          <section className="card stack-md activer-card">
            {preview.status === "idle" || preview.status === "loading" ? (
              <p className="inline-note">Vérification de votre lien…</p>
            ) : preview.status === "invalid" ? (
              <>
                <p>
                  Ce lien n&apos;est plus valide. Il a peut-être expiré ou a déjà été utilisé.
                </p>
                <p className="inline-note">{preview.reason}</p>
                <div className="public-access-actions">
                  <Link className="button button-primary" href="/rendez-vous">
                    Recommencer une demande
                  </Link>
                  <Link className="button button-secondary" href="/acces-client">
                    J&apos;ai déjà un compte
                  </Link>
                </div>
              </>
            ) : (
              <>
                <p>
                  Bonjour <strong>{preview.preview.display_name ?? "et bienvenue"}</strong>.
                  Votre espace IVIA est prêt à s&apos;ouvrir.
                </p>
                {preview.preview.email ? (
                  <p className="inline-note">
                    Compte associé à <span className="mono">{preview.preview.email}</span>.
                  </p>
                ) : null}
                <button
                  type="button"
                  className="button button-primary"
                  disabled={isOpening}
                  onClick={handleOpenSpace}
                >
                  {isOpening ? "Ouverture..." : "Ouvrir mon espace IVIA"}
                </button>
                <p className="inline-note">
                  En entrant, vous activez votre compte. Aucune saisie de mot de passe n&apos;est requise pour cette première fois.
                </p>
                {errorMessage ? <p className="message message-error">{errorMessage}</p> : null}
              </>
            )}
          </section>
        </main>
      </div>
    </PublicLayout>
  );
}

export default function ActiverPage() {
  return (
    <Suspense
      fallback={
        <PublicLayout>
          <div className="page-shell">
            <main className="section">
              <p className="inline-note">Chargement…</p>
            </main>
          </div>
        </PublicLayout>
      }
    >
      <ActiverContent />
    </Suspense>
  );
}

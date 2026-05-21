"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import { verifyEmail } from "@/lib/merlin-api";

type Status = "loading" | "success" | "error" | "no-token";

function VerifyEmailContent() {
  const searchParams = useSearchParams();
  const token = searchParams.get("token");
  const redirect = searchParams.get("redirect") || "/rendez-vous";
  const [status, setStatus] = useState<Status>(token ? "loading" : "no-token");
  const [message, setMessage] = useState("");

  useEffect(() => {
    if (!token) return;
    verifyEmail(token)
      .then((res) => {
        setMessage(res.message);
        setStatus("success");
      })
      .catch((err: Error) => {
        setMessage(err.message);
        setStatus("error");
      });
  }, [token]);

  return (
    <main className="page-center">
      <div className="card verify-email-card">
        <h1 className="card-title">Vérification de courriel</h1>

        {status === "loading" && <p className="text-muted">Vérification en cours…</p>}

        {status === "no-token" && (
          <p className="text-muted">Lien de vérification invalide ou manquant.</p>
        )}

        {status === "success" && (
          <>
            <p className="verify-email-success">
              ✓ {message}
            </p>
            <Link href={redirect} className="button button-primary">
              Continuer
            </Link>
          </>
        )}

        {status === "error" && (
          <>
            <p className="error-msg verify-email-error">
              {message}
            </p>
            <Link href={redirect} className="button button-secondary">
              Retour au parcours
            </Link>
          </>
        )}
      </div>
    </main>
  );
}

export default function VerifyEmailPage() {
  return (
    <Suspense fallback={<main className="page-center"><p className="text-muted">Chargement…</p></main>}>
      <VerifyEmailContent />
    </Suspense>
  );
}

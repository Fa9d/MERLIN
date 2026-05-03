"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import { verifyEmail } from "@/lib/merlin-api";

type Status = "loading" | "success" | "error" | "no-token";

function VerifyEmailContent() {
  const searchParams = useSearchParams();
  const token = searchParams.get("token");
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
      <div className="card" style={{ maxWidth: 480, margin: "80px auto", textAlign: "center" }}>
        <h1 className="card-title">Vérification de courriel</h1>

        {status === "loading" && <p className="text-muted">Vérification en cours…</p>}

        {status === "no-token" && (
          <p className="text-muted">Lien de vérification invalide ou manquant.</p>
        )}

        {status === "success" && (
          <>
            <p style={{ color: "var(--color-success, #16a34a)", marginBottom: "1.5rem" }}>
              ✓ {message}
            </p>
            <Link href="/rendez-vous/reserver" className="btn btn-primary">
              Réserver un rendez-vous
            </Link>
          </>
        )}

        {status === "error" && (
          <>
            <p className="error-msg" style={{ marginBottom: "1.5rem" }}>
              {message}
            </p>
            <Link href="/rendez-vous/reserver" className="btn btn-outline">
              Retour à la réservation
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

"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Suspense } from "react";
import { appRoutes } from "@/lib/routes";

function CheckoutSuccessContent() {
  const searchParams = useSearchParams();
  const sessionId = searchParams.get("session_id");

  return (
    <main
      style={{
        maxWidth: 560,
        margin: "80px auto",
        padding: "0 1.5rem",
        textAlign: "center",
      }}
    >
      <div
        style={{
          fontSize: "3rem",
          marginBottom: "1.5rem",
          color: "var(--accent, #4a7c59)",
        }}
      >
        ✓
      </div>

      <h1 style={{ marginBottom: "1rem" }}>Paiement reçu</h1>

      <p style={{ color: "var(--muted, #666)", marginBottom: "1rem", lineHeight: 1.6 }}>
        Votre demande de consultation audio a été transmise à votre praticien.
        <br />
        Vous recevrez une réponse audio dans les prochaines 24–48 heures.
      </p>

      {sessionId && (
        <p
          style={{
            fontSize: "0.75rem",
            color: "var(--muted, #999)",
            marginBottom: "2rem",
            fontFamily: "monospace",
          }}
        >
          Référence : {sessionId}
        </p>
      )}

      {!sessionId && <div style={{ marginBottom: "2rem" }} />}

      <div style={{ display: "flex", gap: "1rem", justifyContent: "center", flexWrap: "wrap" }}>
        <Link href={appRoutes.suivi} className="btn btn-primary">
          Suivre ma demande
        </Link>
        <Link href={appRoutes.home} className="btn btn-outline">
          Retour à l&apos;accueil
        </Link>
      </div>
    </main>
  );
}

export default function CheckoutSuccessPage() {
  return (
    <Suspense fallback={<main style={{ maxWidth: 560, margin: "80px auto", padding: "0 1.5rem", textAlign: "center" }}>Chargement…</main>}>
      <CheckoutSuccessContent />
    </Suspense>
  );
}

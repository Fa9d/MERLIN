"use client";

import Link from "next/link";
import { appRoutes } from "@/lib/routes";
import { PublicLayout } from "@/components/layout/PublicLayout";

/**
 * /rendez-vous/confirmation
 *
 * Placeholder — cette page recevra la migration de l'état "confirmed"
 * actuellement inline dans /rendez-vous/reserver.
 *
 * Le passage de données (date, heure, praticien) se fera via
 * searchParams ou sessionStorage selon le choix d'implémentation.
 */
export default function ConfirmationPage() {
  return (
    <PublicLayout>
      <main style={{ maxWidth: 560, margin: "80px auto", padding: "0 1.5rem", textAlign: "center" }}>
      <div
        style={{
          fontSize: "2.5rem",
          marginBottom: "1.5rem",
          color: "var(--accent, #4a7c59)",
        }}
      >
        ✓
      </div>
      <h1 style={{ marginBottom: "1rem" }}>Rendez-vous confirmé</h1>
      <p style={{ color: "var(--muted, #666)", marginBottom: "2rem" }}>
        Vous recevrez une confirmation par courriel avec les détails de votre séance.
      </p>
      <Link href={appRoutes.home} className="btn btn-outline">
        Retour à l&apos;accueil
      </Link>
      </main>
    </PublicLayout>
  );
}

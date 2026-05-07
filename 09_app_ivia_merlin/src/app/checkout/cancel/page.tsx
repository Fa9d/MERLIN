"use client";

import Link from "next/link";
import { appRoutes } from "@/lib/routes";

/**
 * /checkout/cancel
 *
 * Affiché quand l'utilisateur abandonne le checkout Stripe.
 */
export default function CheckoutCancelPage() {
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
          color: "var(--muted, #888)",
        }}
      >
        ←
      </div>

      <h1 style={{ marginBottom: "1rem" }}>Paiement annulé</h1>

      <p style={{ color: "var(--muted, #666)", marginBottom: "2rem", lineHeight: 1.6 }}>
        Votre paiement n&apos;a pas été complété. Aucun montant n&apos;a été débité.
        <br />
        Vous pouvez relancer une demande à tout moment.
      </p>

      <div style={{ display: "flex", gap: "1rem", justifyContent: "center", flexWrap: "wrap" }}>
        <Link href={appRoutes.booking} className="btn btn-primary">
          Réessayer
        </Link>
        <Link href={appRoutes.home} className="btn btn-outline">
          Retour à l&apos;accueil
        </Link>
      </div>
    </main>
  );
}

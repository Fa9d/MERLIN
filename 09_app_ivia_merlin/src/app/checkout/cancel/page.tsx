"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Suspense } from "react";
import { appRoutes } from "@/lib/routes";

/**
 * /checkout/cancel
 *
 * Affiché quand l'utilisateur abandonne le checkout Stripe.
 */
function CheckoutCancelContent() {
  const searchParams = useSearchParams();
  const clientCode = searchParams.get("client_code");
  const intakeId = searchParams.get("intake_id");
  const retryHref = clientCode && intakeId
    ? `${appRoutes.suivi}?code=${encodeURIComponent(clientCode)}&intake=${encodeURIComponent(intakeId)}`
    : appRoutes.booking;

  return (
    <main className="checkout-status-page">
      <div className="checkout-status-icon checkout-status-icon--cancel">
        ←
      </div>

      <h1 className="checkout-status-title">Paiement annulé</h1>

      <p className="checkout-status-body checkout-status-body--wide">
        Votre paiement n&apos;a pas été complété. Aucun montant n&apos;a été débité.
        <br />
        Vous pouvez reprendre le parcours ou choisir Interac a tout moment.
      </p>

      <div className="checkout-status-actions">
        <Link href={appRoutes.booking} className="btn btn-primary">
          Revenir au paiement
        </Link>
        <Link href={retryHref} className="btn btn-outline">
          Suivre ma demande
        </Link>
        <Link href={appRoutes.home} className="btn btn-outline">
          Retour à l&apos;accueil
        </Link>
      </div>
    </main>
  );
}

export default function CheckoutCancelPage() {
  return (
    <Suspense fallback={<main className="checkout-status-page">Chargement…</main>}>
      <CheckoutCancelContent />
    </Suspense>
  );
}

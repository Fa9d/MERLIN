"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Suspense } from "react";
import { appRoutes } from "@/lib/routes";

function CheckoutSuccessContent() {
  const searchParams = useSearchParams();
  const sessionId = searchParams.get("session_id");
  const orderId = searchParams.get("order_id");
  const clientCode = searchParams.get("client_code");
  const intakeId = searchParams.get("intake_id");
  const productCode = searchParams.get("product_code");
  const suiviHref =
    clientCode && intakeId
      ? `${appRoutes.suivi}?code=${encodeURIComponent(clientCode)}&intake=${encodeURIComponent(intakeId)}`
      : appRoutes.suivi;

  return (
    <main className="checkout-status-page">
      <div className="checkout-status-icon checkout-status-icon--success">
        ✓
      </div>

      <h1 className="checkout-status-title">Paiement reçu</h1>

      <p className="checkout-status-body">
        Votre paiement a bien ete enregistre pour votre parcours IVIA.
        <br />
        La confirmation clinique ou operative suit maintenant le mode de service choisi.
      </p>

      {productCode ? (
        <p className="checkout-status-body">
          Produit regle: <strong>{productCode}</strong>
        </p>
      ) : null}

      {(sessionId || orderId) && (
        <p className="checkout-status-reference">
          Référence : {orderId ?? sessionId}
        </p>
      )}

      {!sessionId && !orderId && <div className="checkout-status-spacer" />}

      <div className="checkout-status-actions">
        <Link href={suiviHref} className="btn btn-primary">
          Suivre ma demande
        </Link>
        <Link href={appRoutes.booking} className="btn btn-outline">
          Retour au rendez-vous
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
    <Suspense fallback={<main className="checkout-status-page">Chargement…</main>}>
      <CheckoutSuccessContent />
    </Suspense>
  );
}

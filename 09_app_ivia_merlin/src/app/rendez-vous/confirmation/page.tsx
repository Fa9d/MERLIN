"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { PublicLayout } from "@/components/layout/PublicLayout";

type InteracResult = {
  recipient_email: string;
  recipient_name: string;
  transfer_reference: string;
  amount_cents: number;
  instructions_emailed: boolean;
};

type SelectedSlot = {
  slot_date: string;
  start_time: string;
  duration_minutes: number;
  session_type_label: string;
  praticien_name: string;
};

function formatLongDate(iso: string): string {
  return new Date(iso + "T12:00:00").toLocaleDateString("fr-CA", {
    weekday: "long", day: "numeric", month: "long", year: "numeric",
  });
}

export default function ConfirmationPage() {
  const router = useRouter();
  const [interacResult, setInteracResult] = useState<InteracResult | null>(null);
  const [selectedSlot, setSelectedSlot] = useState<SelectedSlot | null>(null);

  useEffect(() => {
    const raw = sessionStorage.getItem("ivia_booking_confirmation");
    if (!raw) {
      router.replace("/rendez-vous/reserver");
      return;
    }
    try {
      const { interacResult: ir, selectedSlot: ss } = JSON.parse(raw);
      setInteracResult(ir);
      setSelectedSlot(ss);
      sessionStorage.removeItem("ivia_booking_confirmation");
    } catch {
      router.replace("/rendez-vous/reserver");
    }
  }, [router]);

  if (!interacResult || !selectedSlot) return null;

  return (
    <PublicLayout>
      <div className="page-shell">
        <main className="section reserver-main">

          <div className="section-header">
            <div className="eyebrow">Réservation</div>
            <h2>Créneau réservé</h2>
          </div>

          <div className="card stack-md reserver-interac">
            <div className="reserver-interac__confirm">
              <p className="reserver-interac__check">✓</p>
              <div>
                <p><strong>Créneau réservé</strong></p>
                <p className="inline-note">
                  {formatLongDate(selectedSlot.slot_date)} à {selectedSlot.start_time.slice(0, 5)}
                </p>
                <p className="inline-note">
                  {selectedSlot.session_type_label} · {selectedSlot.duration_minutes} min · En ligne
                </p>
                <p className="inline-note">Praticien : <strong>{selectedSlot.praticien_name}</strong></p>
              </div>
            </div>

            <h3>Paiement par Interac Virement</h3>
            <p className="inline-note">
              Depuis votre application bancaire, envoyez le virement avec ces informations :
            </p>

            <div className="interac-details">
              <div className="interac-row">
                <span className="interac-row__label">Destinataire</span>
                <span className="interac-row__value">{interacResult.recipient_name}</span>
              </div>
              <div className="interac-row">
                <span className="interac-row__label">Adresse courriel</span>
                <span className="interac-row__value mono">{interacResult.recipient_email}</span>
              </div>
              <div className="interac-row">
                <span className="interac-row__label">Montant</span>
                <span className="interac-row__value">
                  <strong>{(interacResult.amount_cents / 100).toFixed(2)} $</strong>
                </span>
              </div>
              <div className="interac-row interac-row--highlight">
                <span className="interac-row__label">Référence (message obligatoire)</span>
                <span className="interac-row__value mono interac-reference">
                  {interacResult.transfer_reference}
                </span>
              </div>
            </div>

            <div className="card message message-info">
              <p className="inline-note">
                <strong>Inscrivez obligatoirement</strong> la référence{" "}
                <span className="mono">{interacResult.transfer_reference}</span>{" "}
                dans le champ message ou note de votre virement. Votre rendez-vous sera confirmé
                dès réception, sous 24 h.
              </p>
            </div>

            {interacResult.instructions_emailed ? (
              <p className="inline-note">Un courriel avec ces instructions vous a été envoyé.</p>
            ) : null}

            <Link href="/mon-espace" className="button button-primary">
              Voir mon espace
            </Link>
          </div>

        </main>
      </div>
    </PublicLayout>
  );
}


import Link from "next/link";
import { PublicLayout } from "@/components/layout/PublicLayout";

export const metadata = {
  title: "Conditions générales de vente — IVIA",
};

export default function CgvPage() {
  return (
    <PublicLayout>
      <div className="page-shell">
        <main className="section legal-page">
          <div className="section-header">
            <div className="eyebrow">Conditions générales de vente</div>
            <h1>Ce que vous achetez, et comment ça fonctionne.</h1>
          </div>

          <div className="legal-body">
            <p className="legal-date">Version en vigueur : 28 mai 2026</p>

            <h2>1. Prestataire</h2>
            <p>
              Les présentes conditions régissent les achats de séances d&apos;écoute effectués
              sur la plateforme IVIA, exploitée par le fondateur de la plateforme IVIA,
              accessible à l&apos;adresse <strong>ivia.quebec</strong>.
            </p>

            <h2>2. Services vendus</h2>
            <p>
              IVIA propose des séances d&apos;écoute individuelle avec des praticien·ne·s
              formé·e·s à l&apos;écoute profonde. Ces séances ne constituent pas des services
              médicaux, psychothérapeutiques ou diagnostiques.
            </p>
            <ul>
              <li>Séance audio différée (enregistrement + réponse sous 24–72 h)</li>
              <li>Séance en direct (vidéo ou audio temps réel)</li>
            </ul>

            <h2>3. Prix et paiement</h2>
            <p>
              Les prix sont affichés en dollars canadiens (CAD), toutes taxes applicables
              incluses. Le paiement est exigible au moment de la confirmation de la réservation,
              par virement Interac ou carte de crédit via Stripe.
            </p>

            <h2>4. Annulation et remboursement</h2>
            <p>
              Une annulation effectuée plus de 24 heures avant la séance ouvre droit à un
              remboursement intégral ou à un crédit sur votre compte. Toute annulation dans
              les 24 heures précédant la séance est non remboursable, sauf en cas d&apos;urgence
              documentée.
            </p>

            <h2>5. Droit applicable</h2>
            <p>
              Les présentes CGV sont régies par les lois de la province de Québec et les lois
              fédérales du Canada applicables.
            </p>

            <h2>6. Contact</h2>
            <p>
              Pour toute question relative à votre achat, contactez-nous à{" "}
              <a href="mailto:aide@ivia.quebec">aide@ivia.quebec</a>.
            </p>

            <div className="legal-links">
              <Link href="/cgu">Conditions d&apos;utilisation</Link>
              <Link href="/confidentialite">Politique de confidentialité</Link>
            </div>
          </div>
        </main>
      </div>
    </PublicLayout>
  );
}

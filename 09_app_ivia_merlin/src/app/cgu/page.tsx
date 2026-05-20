import Link from "next/link";
import { PublicLayout } from "@/components/layout/PublicLayout";

export const metadata = {
  title: "Conditions générales d'utilisation — IVIA",
};

export default function CguPage() {
  return (
    <PublicLayout>
      <div className="page-shell">
        <main className="section legal-page">
          <div className="section-header">
            <div className="eyebrow">Conditions générales d&apos;utilisation</div>
            <h1>Le cadre de votre relation avec IVIA, en clair.</h1>
            <p className="inline-note">
              Version 1.2 — entrée en vigueur le 31 mai 2026. Loi applicable :
              lois du Québec (Canada). Contact : <span className="mono">bonjour@ivia.quebec</span>.
            </p>
          </div>

          <article className="card stack-md">
            <h2>1. Qui est IVIA</h2>
            <p>
              IVIA est une plateforme d&apos;écoute éthique née d&apos;une conviction simple :
              les personnes qui traversent une difficulté ont besoin, avant tout, d&apos;être entendues.
              Pas diagnostiquées. Pas orientées mécaniquement. Pas catégorisées.
            </p>
            <p className="inline-note">
              Pendant la phase pilote (mai-automne 2026), la responsabilité opérationnelle est assumée
              par David Phaneuf, fondateur, en qualité de travailleur autonome. À l&apos;incorporation
              d&apos;IVIA inc. (société par actions à mission, automne 2026), l&apos;ensemble des
              droits et obligations sera transféré à IVIA inc. sans modification de vos droits.
            </p>
          </article>

          <article className="card stack-md">
            <h2>2. Conditions pour utiliser IVIA</h2>
            <ul>
              <li>Avoir 14 ans ou plus (avec accompagnement parental pour les 14-17 ans).</li>
              <li>Résider au Canada ou dans un territoire reconnu par IVIA comme éligible.</li>
              <li>Fournir une adresse courriel valide.</li>
              <li>Accepter les présentes CGU et la politique de confidentialité.</li>
            </ul>
          </article>

          <article className="card stack-md">
            <h2>3. Ce qu&apos;IVIA fait — et ne fait pas</h2>
            <p><strong>IVIA fait :</strong></p>
            <ul>
              <li>Un espace d&apos;écoute, de clarté, d&apos;orientation.</li>
              <li>Des séances audio confidentielles avec un·e praticien·ne formé·e.</li>
              <li>Des documents de suivi structurés, validés par votre praticien·ne avant diffusion.</li>
            </ul>
            <p><strong>IVIA ne fait pas :</strong></p>
            <ul>
              <li>Pas de diagnostic médical ou psychologique.</li>
              <li>Pas de prescription.</li>
              <li>Pas de service d&apos;urgence. En cas de danger immédiat : <strong>911</strong> ;
                  crise suicidaire au Canada : <strong>988</strong> ; Info-Santé Québec : <strong>811</strong>.</li>
              <li>Aucune substitution aux soins cliniques.</li>
            </ul>
          </article>

          <article className="card stack-md">
            <h2>4. Vos consentements</h2>
            <p>
              En cochant la case d&apos;acceptation des présentes CGU, vous consentez aux usages suivants,
              tous nécessaires au service que vous demandez :
            </p>
            <ul>
              <li><strong>Préparation d&apos;une séance d&apos;accueil</strong> à partir de votre demande.</li>
              <li><strong>Production d&apos;une note de séance structurée</strong> pour la continuité de votre suivi.</li>
              <li><strong>Mise en lien de vos séances</strong> entre elles, à votre rythme, pour préserver le fil de votre démarche.</li>
              <li><strong>Conservation</strong> de vos coordonnées pendant la durée de votre compte + 12 mois après clôture.</li>
            </ul>
            <p className="inline-note">
              <strong>Hors omnibus :</strong> l&apos;enregistrement audio et la transcription d&apos;une séance
              constituent des données <strong>biométriques sensibles</strong> au sens de la Loi 25 (art. 8.1).
              Ils font l&apos;objet d&apos;un <strong>consentement distinct et exprès</strong>, présenté au moment
              de votre première séance — pas avant. Vous pouvez le révoquer à tout moment.
            </p>
          </article>

          <article className="card stack-md">
            <h2>5. Tarification</h2>
            <p>
              Pendant la phase pilote :
            </p>
            <ul>
              <li>Première séance d&apos;écoute (60-75 min, en ligne) : 65 $ CAD.</li>
              <li>Séance d&apos;urgence prioritaire (30 min) : 50 $ CAD.</li>
            </ul>
            <p>
              Modes de paiement : Stripe (carte) ou Interac e-transfer. Aucun débit récurrent
              automatique. Politique d&apos;annulation : annulation gratuite jusqu&apos;à 24 h
              avant la séance.
            </p>
          </article>

          <article className="card stack-md">
            <h2>6. Vos droits sur vos données</h2>
            <p>
              Conformément à la Loi 25, vous avez en tout temps le droit de :
            </p>
            <ul>
              <li><strong>Accéder</strong> à vos données : section « Mon dossier » de votre espace.</li>
              <li><strong>Rectifier</strong> vos coordonnées : onglet « Compléter mon profil » de votre espace.</li>
              <li><strong>Exporter</strong> vos données dans un format portable.</li>
              <li><strong>Demander l&apos;effacement</strong> de votre compte et de vos données (délai cible IVIA : 72 h ; délai légal max : 30 jours).</li>
              <li><strong>Révoquer</strong> n&apos;importe quel consentement, à tout moment.</li>
            </ul>
            <p className="inline-note">
              Pour exercer vos droits, contactez le Responsable de la protection des renseignements personnels :
              {" "}<span className="mono">privacy@ivia.quebec</span>.
            </p>
          </article>

          <article className="card stack-md">
            <h2>7. Limites de responsabilité</h2>
            <p>
              IVIA s&apos;engage à offrir un service de qualité, mais ne garantit pas un résultat
              thérapeutique ou clinique — IVIA n&apos;est pas un service de soins. La relation
              d&apos;accompagnement repose sur l&apos;engagement mutuel entre vous et votre praticien·ne.
            </p>
            <p>
              IVIA n&apos;est responsable que des dommages directs résultant d&apos;une faute prouvée,
              dans les limites des lois applicables au Québec.
            </p>
          </article>

          <article className="card stack-md">
            <h2>8. Modification des présentes CGU</h2>
            <p>
              Toute modification matérielle des présentes CGU vous sera notifiée par courriel
              avec un préavis minimum de 30 jours. Vous aurez toujours la possibilité de refuser
              les nouvelles conditions et de fermer votre compte sans frais.
            </p>
          </article>

          <article className="card stack-md">
            <h2>9. Droit applicable et juridiction</h2>
            <p>
              Les présentes CGU sont régies par les lois du Québec et les lois fédérales du Canada
              qui s&apos;y appliquent. Tout différend sera soumis aux tribunaux compétents
              du district de Montréal, sauf disposition impérative contraire.
            </p>
          </article>

          <article className="card stack-md">
            <h2>10. Contact</h2>
            <ul>
              <li>Questions générales : <span className="mono">bonjour@ivia.quebec</span></li>
              <li>Vie privée et données : <span className="mono">privacy@ivia.quebec</span></li>
              <li>Adresse postale : à publier lors de l&apos;incorporation d&apos;IVIA inc. (automne 2026)</li>
            </ul>
          </article>

          <p className="inline-note">
            La version complète et signée des CGU (430 articles détaillés) est conservée dans
            les archives juridiques d&apos;IVIA et fournie sur demande à{" "}
            <span className="mono">privacy@ivia.quebec</span>. La présente page en est le résumé
            opposable, rédigé en langage clair (Loi 25 art. 14).
          </p>

          <div className="public-access-actions" style={{ marginTop: "1.5rem" }}>
            <Link href="/confidentialite" className="button button-secondary">
              Voir la politique de confidentialité
            </Link>
            <Link href="/rendez-vous" className="button button-primary">
              Faire une demande
            </Link>
          </div>
        </main>
      </div>
    </PublicLayout>
  );
}

import Link from "next/link";
import { PublicLayout } from "@/components/layout/PublicLayout";

export const metadata = {
  title: "Politique de confidentialité — IVIA",
};

export default function ConfidentialitePage() {
  return (
    <PublicLayout>
      <div className="page-shell">
        <main className="section legal-page">
          <div className="section-header">
            <div className="eyebrow">Politique de confidentialité</div>
            <h1>Comment IVIA protège vos données.</h1>
            <p className="inline-note">
              Version 1.1 — conformité Loi 25 (Québec) et LPRPDE (Canada).
              Responsable de la protection des renseignements personnels (RPRP) :
              David Phaneuf · <span className="mono">privacy@ivia.quebec</span>.
            </p>
          </div>

          <article className="card stack-md">
            <h2>1. Engagement</h2>
            <p>
              Vos données restent <strong>au Québec</strong>. Elles ne sont jamais vendues, ni cédées,
              ni louées à un tiers. Elles servent <strong>uniquement</strong> à vous accompagner
              dans votre démarche IVIA et à améliorer notre service de manière éthique.
            </p>
            <p>
              IVIA applique strictement le principe de <strong>limitation de la collecte</strong>
              {" "}(Loi 25 art. 4-5) : nous ne collectons que ce qui est nécessaire à la finalité
              déclarée. Pas plus.
            </p>
          </article>

          <article className="card stack-md">
            <h2>2. Quelles données nous collectons, et pourquoi</h2>
            <div className="legal-table-wrap">
              <table className="legal-table">
                <thead>
                  <tr>
                    <th>Donnée</th>
                    <th>Finalité</th>
                    <th>Conservation</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>Identité (prénom, courriel, téléphone)</td>
                    <td>Ouvrir et tenir votre compte. Vous contacter.</td>
                    <td>Durée du compte + 12 mois après clôture</td>
                  </tr>
                  <tr>
                    <td>Demande initiale (texte libre, besoin déclaré)</td>
                    <td>Préparer votre première séance. Orienter votre démarche.</td>
                    <td>Durée du compte</td>
                  </tr>
                  <tr>
                    <td>Réponses au parcours d&apos;orientation</td>
                    <td>Affiner l&apos;accompagnement proposé.</td>
                    <td>Durée du compte (purgées si pas de compte créé : 30 minutes)</td>
                  </tr>
                  <tr>
                    <td><strong>Enregistrement audio d&apos;une séance</strong></td>
                    <td>Produire la transcription. <strong>Détruit à J+30.</strong></td>
                    <td>Maximum 30 jours</td>
                  </tr>
                  <tr>
                    <td>Transcription de séance</td>
                    <td>Continuité de votre suivi. Production de notes.</td>
                    <td>Durée du compte, chiffrée</td>
                  </tr>
                  <tr>
                    <td>Statistiques agrégées anonymisées</td>
                    <td>Améliorer le service. Recherche éthique. Tableau de bord public.</td>
                    <td>Indéfinie (les données ne sont plus rattachables à vous)</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </article>

          <article className="card stack-md">
            <h2>3. Données biométriques : la voix</h2>
            <p>
              La voix est une <strong>donnée biométrique sensible</strong> (Loi 25 art. 8.1).
              Elle exige un consentement <strong>exprès</strong>, présenté au moment où la collecte
              commence. C&apos;est pourquoi nous ne demandons jamais ce consentement à l&apos;inscription :
              vous y serez invité·e seulement <strong>au moment de votre première séance</strong>,
              avec une explication claire de ce qui sera capté et de ce qui en sera fait.
            </p>
            <p>
              <strong>Pipeline J+30</strong> : après chaque séance, l&apos;audio est transcrit puis
              <strong> détruit dans un délai maximum de 30 jours</strong>. Seule la transcription
              chiffrée est conservée pour assurer la continuité de votre suivi. Le fichier audio
              brut n&apos;est jamais cédé, vendu, ou utilisé à d&apos;autres fins.
            </p>
          </article>

          <article className="card stack-md">
            <h2>4. Qui voit quoi</h2>
            <ul>
              <li><strong>Vous</strong> : tout ce qui vous concerne (identité, demande, transcriptions, notes diffusées).</li>
              <li><strong>Votre praticien·ne</strong> : ce qui concerne votre relation d&apos;accompagnement,
                  par défaut sous votre alias public (<span className="mono">CLI-XXXXX</span>), pas sous votre nom légal.</li>
              <li><strong>Équipe IVIA opérationnelle</strong> : accès uniquement sur incident technique documenté, journalisé.</li>
              <li><strong>Praticien·ne·s tiers·ces, organismes externes, partenaires</strong> : <strong>jamais</strong>,
                  sauf consentement distinct et explicite à un projet précis.</li>
              <li><strong>Chercheurs externes</strong> : uniquement statistiques agrégées anonymisées.</li>
            </ul>
          </article>

          <article className="card stack-md">
            <h2>5. Hébergement et sécurité</h2>
            <ul>
              <li>Serveurs hébergés au Québec et au Canada.</li>
              <li>Chiffrement en transit (TLS) et au repos pour les données sensibles.</li>
              <li>Mots de passe stockés sous forme de hachage cryptographique (scrypt).</li>
              <li>Accès interne journalisé et tracé.</li>
              <li>Mise à jour régulière des dépendances et des correctifs de sécurité.</li>
            </ul>
          </article>

          <article className="card stack-md">
            <h2>6. Vos droits — comment les exercer</h2>
            <p>Loi 25 vous donne les droits suivants :</p>
            <ul>
              <li><strong>Accéder</strong> à vos données — section « Mon dossier ».</li>
              <li><strong>Rectifier</strong> vos données — onglet « Compléter mon profil ».</li>
              <li><strong>Exporter</strong> vos données — bouton « Exporter mes données » (à venir).</li>
              <li><strong>Demander l&apos;effacement</strong> — bouton « Effacer mon compte » (à venir).</li>
              <li><strong>Révoquer</strong> un consentement spécifique — section « Mes consentements ».</li>
              <li><strong>Déposer une plainte</strong> auprès de la Commission d&apos;accès à l&apos;information
                  du Québec (CAI) : <a href="https://www.cai.gouv.qc.ca" target="_blank" rel="noopener">cai.gouv.qc.ca</a>.</li>
            </ul>
            <p className="inline-note">
              Délai cible de réponse IVIA : 72 heures. Délai légal maximum : 30 jours
              (Loi 25 art. 32).
            </p>
          </article>

          <article className="card stack-md">
            <h2>7. Cookies et traçage</h2>
            <p>
              IVIA n&apos;utilise <strong>aucun cookie publicitaire</strong>, <strong>aucun pixel
              de réseau social</strong>, <strong>aucun traceur tiers commercial</strong>.
              Nous utilisons uniquement :
            </p>
            <ul>
              <li>Des cookies fonctionnels strictement nécessaires (session de connexion).</li>
              <li>Des événements de navigation anonymes pour comprendre les parcours d&apos;abandon
                  et améliorer l&apos;expérience (Strate A — non identifiante, 24 mois).</li>
            </ul>
          </article>

          <article className="card stack-md">
            <h2>8. Incident de sécurité</h2>
            <p>
              En cas d&apos;incident de confidentialité présentant un risque sérieux,
              IVIA notifie la <strong>Commission d&apos;accès à l&apos;information du Québec</strong>
              {" "}et les personnes concernées sans délai, conformément à la Loi 25 art. 3.5.
            </p>
          </article>

          <article className="card stack-md">
            <h2>9. Mise à jour de la politique</h2>
            <p>
              Toute modification matérielle de cette politique sera notifiée par courriel
              avec un préavis minimum de 30 jours. Si la modification touche les finalités
              ou la durée de conservation, un re-consentement explicite vous sera demandé
              (Loi 25 art. 9).
            </p>
          </article>

          <article className="card stack-md">
            <h2>10. Contact RPRP</h2>
            <p>
              Pour toute question, demande d&apos;accès ou plainte :
            </p>
            <ul>
              <li><strong>Courriel</strong> : <span className="mono">privacy@ivia.quebec</span></li>
              <li><strong>Délai de réponse</strong> : 30 jours maximum (Loi 25 art. 32), cible interne 72 h</li>
              <li><strong>Autorité de contrôle</strong> :{" "}
                <a href="https://www.cai.gouv.qc.ca" target="_blank" rel="noopener">
                  Commission d&apos;accès à l&apos;information du Québec
                </a>
              </li>
            </ul>
          </article>

          <div className="public-access-actions" style={{ marginTop: "1.5rem" }}>
            <Link href="/cgu" className="button button-secondary">
              Voir les Conditions générales d&apos;utilisation
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

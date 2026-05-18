import Link from "next/link";
import { PublicLayout } from "@/components/layout/PublicLayout";

export const metadata = {
  title: "Collectivités — MÉSANGES · IVIA",
  description:
    "MÉSANGES pour les collectivités : organismes communautaires, milieux de travail, écoles et municipalités du Québec qui souhaitent offrir une voie d'accueil et d'écoute à leurs membres.",
};

export default function CollectivitesPage() {
  return (
    <PublicLayout>
      <main className="hp">
        <section className="hp-section">
          <div className="hp-section__inner">
            <p className="hp-kicker">Collectivités</p>
            <h1 className="hp-h1">
              MÉSANGES au service des collectivités du Québec
            </h1>
            <p className="hp-lede">
              Organismes communautaires, milieux de travail, écoles,
              municipalités, premières lignes : MÉSANGES propose une voie
              d&apos;accueil et d&apos;écoute structurée, ancrée localement,
              respectueuse des cadres et des règles de confidentialité du
              Québec (Loi 25).
            </p>

            <div className="hp-collectivites-grid">
              <article className="hp-card">
                <h2 className="hp-h3">Une porte d&apos;entrée commune</h2>
                <p>
                  Un seul seuil pour vos membres ou vos équipes — accueil sans
                  tri, orientation respectueuse, suivi possible dans la durée.
                </p>
              </article>

              <article className="hp-card">
                <h2 className="hp-h3">Cadre québécois</h2>
                <p>
                  Données hébergées au Québec, connecteurs privés, conformité
                  Loi 25. Les ressources d&apos;urgence (811, 911, 988)
                  restent toujours mises en avant.
                </p>
              </article>

              <article className="hp-card">
                <h2 className="hp-h3">Pas de diagnostic</h2>
                <p>
                  MÉSANGES n&apos;établit aucun diagnostic et ne remplace pas
                  les professionnels de la santé. La posture est celle de
                  l&apos;accueil et de l&apos;orientation — toujours sous
                  validation humaine.
                </p>
              </article>
            </div>

            <div className="hp-cta-row">
              <Link href="/rendez-vous" className="hp-btn hp-btn--primary">
                Discuter d&apos;un déploiement
              </Link>
              <Link href="/ressources" className="hp-btn hp-btn--ghost">
                Voir les ressources publiques
              </Link>
            </div>

            <p className="hp-fineprint">
              En cas d&apos;urgence : 911 (urgence vitale), 811 (Info-Santé /
              Info-Social), 988 (ligne canadienne de prévention du suicide).
            </p>
          </div>
        </section>
      </main>
    </PublicLayout>
  );
}

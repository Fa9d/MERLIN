import Link from "next/link";
import { PublicLayout } from "@/components/layout/PublicLayout";

export const metadata = {
  title: "Pratiquer avec IVIA — MÉSANGES",
  description:
    "Rejoignez la plateforme IVIA et exercez votre pratique d'écoute dans un environnement numérique structuré, au Québec.",
};

const OFFRES = [
  {
    glyph: "◎",
    label: "Votre agenda, sous votre contrôle",
    body: "Définissez vos disponibilités à la semaine ou par exception. Les clients voient vos créneaux en temps réel et réservent sans intermédiaire.",
  },
  {
    glyph: "◇",
    label: "Dossier client structuré",
    body: "Chaque client dispose d'un profil : demande initiale, historique de séances, notes, consentements. Tout en un seul endroit, accessible depuis votre tableau de bord.",
  },
  {
    glyph: "⊘",
    label: "Sans diagnostic ni étiquette",
    body: "IVIA ne demande pas de diagnostic médical. Vous travaillez avec des personnes, pas des dossiers. Notre approche est non-directive et centrée sur l'écoute.",
  },
  {
    glyph: "◻",
    label: "Notes de séance et suivi",
    body: "Rédigez vos notes directement après chaque séance. Ajoutez des alertes de vigilance, planifiez la prochaine rencontre, consultez l'historique complet.",
  },
  {
    glyph: "▲",
    label: "Indépendance du réseau de la santé",
    body: "Vous exercez en dehors — ou en complément — du système public. Pas de référence médicale requise. Vos clients choisissent librement de vous consulter.",
  },
  {
    glyph: "◈",
    label: "Données au Québec, confidentialité stricte",
    body: "Toutes les données sont hébergées en sol québécois. Confidentialité des échanges garantie. Vos clients savent que leurs informations ne quittent pas la province.",
  },
];

const ETAPES = [
  {
    n: "1",
    titre: "Candidature",
    corps:
      "Transmettez votre dossier — formation, approche, langues, disponibilités. Nous prenons connaissance de votre pratique et vous contactons dans les 5 jours ouvrables.",
  },
  {
    n: "2",
    titre: "Rencontre d'intégration",
    corps:
      "Un échange de 30 minutes pour aligner votre approche avec la philosophie IVIA, comprendre la plateforme et répondre à vos questions.",
  },
  {
    n: "3",
    titre: "Activation de votre profil",
    corps:
      "Votre profil est créé, votre agenda configuré. Vous apparaissez dans la liste des praticiens disponibles. Votre pratique commence dès que vous le souhaitez.",
  },
];

export default function PraticienRejoindrePage() {
  return (
    <PublicLayout>
      <div className="hp hp--v3">
        <main>

          {/* ── HERO ────────────────────────────────────────────────── */}
          <section
            className="v3-section"
            style={{
              background: "#0d0d08",
              color: "#f5f0eb",
              paddingTop: "5rem",
              paddingBottom: "4rem",
              borderBottom: "none",
            }}
            aria-labelledby="praticien-hero-title"
          >
            <div className="v3-section__inner" style={{ maxWidth: "700px" }}>
              <p className="v3-kicker" style={{ color: "#8fba9f" }}>
                Pour les praticien·ne·s
              </p>
              <h1
                id="praticien-hero-title"
                className="v3-h2"
                style={{
                  color: "#f5f0eb",
                  fontWeight: 800,
                  letterSpacing: "-0.025em",
                  marginBottom: "1.5rem",
                }}
              >
                Exercez votre pratique{" "}
                <em style={{ color: "#8fba9f", fontStyle: "normal" }}>
                  avec les bons outils.
                </em>
              </h1>
              <p
                style={{
                  fontSize: "1.125rem",
                  lineHeight: 1.7,
                  color: "#c8c2ba",
                  marginBottom: "2.5rem",
                  maxWidth: "560px",
                }}
              >
                IVIA est une plateforme d&apos;&eacute;coute ind&eacute;pendante
                au Qu&eacute;bec. Nous cherchons des praticien·ne·s form&eacute;s
                &agrave; l&apos;&eacute;coute active et non-directive, qui
                souhaitent exercer &agrave; leur rythme &mdash; en ligne, en
                pr&eacute;sentiel ou en mode asynchrone.
              </p>
              <Link
                href="mailto:praticiens@ivia.quebec?subject=Candidature%20praticien%20IVIA"
                className="v3-btn v3-btn--ink"
                style={{ fontSize: "1.0625rem", padding: "0.875rem 2rem", fontWeight: 700 }}
              >
                D&eacute;poser ma candidature
                <span className="v3-btn__arrow" aria-hidden="true">&rarr;</span>
              </Link>
            </div>
          </section>

          {/* ── CE QU'ON OFFRE ──────────────────────────────────────── */}
          <section
            className="v3-section"
            style={{ background: "#fff", borderTop: "1px solid #e8e4df" }}
            aria-labelledby="offres-title"
          >
            <div className="v3-section__inner">
              <p className="v3-kicker">La plateforme</p>
              <h2
                id="offres-title"
                className="v3-h2 v3-h2--center"
                style={{ marginBottom: "3rem" }}
              >
                Ce que nous mettons &agrave; votre disposition
              </h2>
              <div className="v3-valeurs-cles__grid">
                {OFFRES.map((o) => (
                  <div key={o.label} className="v3-valeur-cle">
                    <div className="v3-valeur-cle__glyph" aria-hidden="true">
                      {o.glyph}
                    </div>
                    <div className="v3-valeur-cle__text">
                      <p className="v3-valeur-cle__label">{o.label}</p>
                      <p className="v3-valeur-cle__body">{o.body}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </section>

          {/* ── PROFIL RECHERCHÉ ────────────────────────────────────── */}
          <section
            className="v3-section"
            style={{
              background: "#f7f4f0",
              borderTop: "1px solid #e8e4df",
              borderBottom: "1px solid #e8e4df",
            }}
            aria-labelledby="profil-title"
          >
            <div className="v3-section__inner" style={{ maxWidth: "680px" }}>
              <p className="v3-kicker">Profil recherch&eacute;</p>
              <h2
                id="profil-title"
                className="v3-h2"
                style={{ marginBottom: "2rem" }}
              >
                Qui peut rejoindre IVIA&nbsp;?
              </h2>
              <ul
                style={{
                  listStyle: "none",
                  padding: 0,
                  margin: 0,
                  display: "flex",
                  flexDirection: "column",
                  gap: "1rem",
                }}
              >
                {[
                  "Formation reconnue en écoute active, accompagnement psychosocial, relation d'aide ou discipline connexe",
                  "Capacité à exercer de façon autonome et confidentielle",
                  "Maîtrise du français ; l'anglais est un atout",
                  "Disponible pour au moins 5 créneaux par semaine",
                  "Résident·e au Québec ou pouvant exercer légalement en ligne depuis le Québec",
                ].map((item) => (
                  <li
                    key={item}
                    style={{
                      display: "flex",
                      gap: "0.875rem",
                      alignItems: "flex-start",
                      color: "#2a2a1e",
                      lineHeight: 1.6,
                    }}
                  >
                    <span
                      style={{
                        color: "#3d6b4f",
                        fontWeight: 700,
                        fontSize: "1.1rem",
                        marginTop: "0.05rem",
                        flexShrink: 0,
                      }}
                      aria-hidden="true"
                    >
                      ✓
                    </span>
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          </section>

          {/* ── PROCESSUS ───────────────────────────────────────────── */}
          <section
            className="v3-section"
            style={{ background: "#fff", borderTop: "1px solid #e8e4df" }}
            aria-labelledby="processus-title"
          >
            <div className="v3-section__inner" style={{ maxWidth: "680px" }}>
              <p className="v3-kicker">Comment &ccedil;a se passe</p>
              <h2
                id="processus-title"
                className="v3-h2 v3-h2--center"
                style={{ marginBottom: "3rem" }}
              >
                Trois &eacute;tapes pour commencer
              </h2>
              <ol
                style={{
                  listStyle: "none",
                  padding: 0,
                  margin: 0,
                  display: "flex",
                  flexDirection: "column",
                  gap: "2.5rem",
                }}
              >
                {ETAPES.map((e) => (
                  <li
                    key={e.n}
                    style={{ display: "flex", gap: "1.5rem", alignItems: "flex-start" }}
                  >
                    <span
                      style={{
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        width: "2.5rem",
                        height: "2.5rem",
                        minWidth: "2.5rem",
                        borderRadius: "50%",
                        background: "#3d6b4f",
                        color: "#ffffff",
                        fontWeight: 700,
                        fontSize: "1rem",
                      }}
                    >
                      {e.n}
                    </span>
                    <div>
                      <h3
                        style={{
                          fontSize: "1.0625rem",
                          fontWeight: 600,
                          marginBottom: "0.5rem",
                          color: "#0d0d08",
                        }}
                      >
                        {e.titre}
                      </h3>
                      <p style={{ color: "#2a2a1e", lineHeight: 1.7, margin: 0 }}>
                        {e.corps}
                      </p>
                    </div>
                  </li>
                ))}
              </ol>
              <div style={{ textAlign: "center", marginTop: "3rem" }}>
                <Link
                  href="mailto:praticiens@ivia.quebec?subject=Candidature%20praticien%20IVIA"
                  className="v3-btn v3-btn--ink"
                  style={{
                    fontSize: "1.0625rem",
                    padding: "0.875rem 2rem",
                    fontWeight: 700,
                    outline: "1px solid currentColor",
                    outlineOffset: "3px",
                  }}
                >
                  D&eacute;poser ma candidature
                  <span className="v3-btn__arrow" aria-hidden="true">&rarr;</span>
                </Link>
                <p
                  style={{
                    marginTop: "1rem",
                    fontSize: "0.875rem",
                    color: "#6b6b5a",
                  }}
                >
                  R&eacute;ponse garantie sous 5 jours ouvrables.
                </p>
              </div>
            </div>
          </section>

          {/* ── LIEN VERS L'ÉQUIPE ──────────────────────────────────── */}
          <section
            className="v3-section"
            style={{
              background: "#f7f4f0",
              borderTop: "1px solid #e8e4df",
              paddingTop: "3rem",
              paddingBottom: "3rem",
            }}
          >
            <div
              className="v3-section__inner"
              style={{ textAlign: "center", maxWidth: "560px" }}
            >
              <p style={{ color: "#6b6b5a", marginBottom: "1.25rem" }}>
                Vous souhaitez d&apos;abord rencontrer l&apos;&eacute;quipe&nbsp;?
              </p>
              <Link href="/praticiens" className="v3-btn v3-btn--ghost">
                Voir nos praticiens
              </Link>
            </div>
          </section>

        </main>
      </div>
    </PublicLayout>
  );
}

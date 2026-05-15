"use client";
import Link from "next/link";
import "./styles.css";
import { PublicLayout } from "@/components/layout/PublicLayout";

/* ── Données éditoriales ──────────────────────────────────────────────────────
   Refonte 2026-05-15 — branche `refonte-ivia-site-unifie`.
   Positionnement : IVIA n'est pas une clinique. Pas une promesse de guérison.
   C'est un espace québécois d'écoute, de compréhension du vivant et
   d'accompagnement vers l'autonomie.
   ────────────────────────────────────────────────────────────────────────── */

const DEPOTS = [
  "Un poids que vous portez seul·e depuis longtemps.",
  "Une transition qui ne se laisse pas nommer.",
  "Un doute, une fatigue, une perte de sens.",
  "Une question sur votre corps, votre rythme, vos liens.",
  "Une intuition que quelque chose doit changer.",
];

const DIMENSIONS = [
  {
    num: "01",
    title: "Vécu",
    body: "Ce que vous traversez en ce moment, mis en mots à votre rythme.",
  },
  {
    num: "02",
    title: "Corps & métabolisme",
    body: "Sommeil, énergie, alimentation, rythme — le corps comme témoin et indicateur.",
  },
  {
    num: "03",
    title: "Relations",
    body: "Les liens qui portent, ceux qui pèsent, ceux qu'on cherche à clarifier.",
  },
  {
    num: "04",
    title: "Temps & lignées",
    body: "Ce qui se transmet, ce qui se répète, ce qui demande à être reposé.",
  },
  {
    num: "05",
    title: "Sens",
    body: "Vos repères, ce qui compte, la direction que vous reconnaissez comme vôtre.",
  },
];

const ETAPES = [
  {
    num: "01",
    title: "Un questionnaire calme",
    body: "Quelques questions, à votre rythme, pour déposer ce qui est là — sans grille clinique, sans diagnostic.",
  },
  {
    num: "02",
    title: "Une synthèse personnelle",
    body: "IVIA organise ce que vous avez partagé en une lecture claire, que vous gardez et que vous pouvez retravailler.",
  },
  {
    num: "03",
    title: "Un·e praticien·ne, si vous le souhaitez",
    body: "Si une rencontre humaine fait sens, IVIA vous oriente vers un·e praticien·ne au Québec, en respectant votre consentement.",
  },
];

const SAVOIRS = [
  {
    tag: "Corps & métabolisme",
    body: "Sommeil, glycémie, microbiote, charge inflammatoire : ce qu'on commence à comprendre du vivant — sans recette universelle.",
  },
  {
    tag: "Relations & attachement",
    body: "Comment les liens se forment, se réparent, se choisissent. Ce que la recherche dit, ce qu'elle ne dit pas encore.",
  },
  {
    tag: "Temporalité & lignées",
    body: "Ce qui se transmet d'une génération à l'autre, dans les histoires et dans les corps. Lecture exploratoire, prudente.",
  },
  {
    tag: "Recherche émergente",
    body: "Travaux en cours sur les états de conscience modifiés (méditation, respiration, molécules à l'étude). Cadre, prudence, et sources.",
  },
  {
    tag: "Autonomie & souveraineté",
    body: "Prévention, soin de soi, données personnelles : reprendre du pouvoir sur sa santé sans dépendre d'une autorité unique.",
  },
];

/* ── Composant ────────────────────────────────────────────────────────────── */
export default function HomePage() {
  return (
    <PublicLayout>
      <div className="hp">
        <main>
          {/* ── HERO ──────────────────────────────────────────────────────── */}
          <section className="hp-hero">
            <div className="hp-hero__inner">
              <div className="hp-hero__copy">
                <p className="hp-kicker">IVIA · Québec</p>
                <h1 className="hp-hero__h1">
                  Parlez en toute liberté
                  <br />
                  dans votre espace privé.
                </h1>
                <p className="hp-hero__sub">
                  IVIA n’est ni une clinique ni un site de soins. C’est un espace
                  d’écoute et de compréhension du vivant — vos mots restent chez
                  vous, hébergés au Québec.
                </p>
                <div className="hp-hero__ctas">
                  <Link href="/demarche" className="hp-btn hp-btn--primary">
                    Commencer dans mon espace privé
                  </Link>
                  <Link href="#savoirs" className="hp-btn hp-btn--ghost">
                    Explorer les savoirs du vivant
                  </Link>
                </div>
              </div>
              <div className="hp-hero__visual">
                <div className="hp-hero__video-wrap">
                  <video
                    className="hp-hero__video"
                    src="/assets/video/ivia_accueil_trace_vocale_v2.mp4"
                    controls
                    preload="metadata"
                    playsInline
                    aria-label="Trace vocale d'introduction d'IVIA par David Phaneuf"
                  >
                    <p className="hp-hero__video-fallback">
                      Trace vocale d’introduction d’IVIA — votre navigateur ne
                      supporte pas la lecture vidéo HTML5.
                    </p>
                  </video>
                </div>
              </div>
            </div>
          </section>

          {/* ── POSITIONNEMENT / PONT ─────────────────────────────────────── */}
          <section className="hp-pont">
            <p className="hp-pont__text">
              IVIA n’apporte pas de diagnostic, pas de protocole, pas de
              promesse de guérison.
              <br />
              <em>
                IVIA fait de la place pour que vous puissiez vous entendre vous-même.
              </em>
            </p>
          </section>

          {/* ── CE QUE VOUS POUVEZ DÉPOSER ────────────────────────────────── */}
          <section className="hp-section hp-depots" id="deposer">
            <div className="hp-section__inner">
              <p className="hp-kicker">Ce que vous pouvez déposer</p>
              <h2 className="hp-h2">
                Vous n’avez pas besoin d’avoir les mots parfaits.
              </h2>
              <ul className="hp-depots__list">
                {DEPOTS.map((d) => (
                  <li key={d} className="hp-depots__item">
                    {d}
                  </li>
                ))}
              </ul>
            </div>
          </section>

          {/* ── 5 DIMENSIONS ──────────────────────────────────────────────── */}
          <section className="hp-section hp-dimensions" id="dimensions">
            <div className="hp-section__inner">
              <p className="hp-kicker">Les cinq dimensions IVIA</p>
              <h2 className="hp-h2">
                Une lecture du vivant, sans le réduire.
              </h2>
              <p className="hp-section__intro">
                Vous n’êtes pas un symptôme, ni une case. IVIA propose une
                lecture en cinq dimensions — comme cinq portes d’entrée pour
                comprendre ce qui se passe pour vous, à votre rythme.
              </p>
              <div className="hp-dim-grid">
                {DIMENSIONS.map((d) => (
                  <article key={d.num} className="hp-dim-card">
                    <span className="hp-dim-card__num">{d.num}</span>
                    <h3 className="hp-dim-card__title">{d.title}</h3>
                    <p className="hp-dim-card__body">{d.body}</p>
                  </article>
                ))}
              </div>
            </div>
          </section>

          {/* ── COMMENT IVIA ACCOMPAGNE ───────────────────────────────────── */}
          <section className="hp-section hp-accompagne" id="accompagnement">
            <div className="hp-section__inner">
              <p className="hp-kicker">Comment IVIA accompagne</p>
              <h2 className="hp-h2">
                Trois temps, à votre rythme.
              </h2>
              <ol className="hp-etapes">
                {ETAPES.map((e) => (
                  <li key={e.num} className="hp-etape">
                    <span className="hp-etape__num">{e.num}</span>
                    <div>
                      <h3 className="hp-etape__title">{e.title}</h3>
                      <p className="hp-etape__body">{e.body}</p>
                    </div>
                  </li>
                ))}
              </ol>
            </div>
          </section>

          {/* ── CONFIDENTIALITÉ & SOUVERAINETÉ ────────────────────────────── */}
          <section className="hp-section hp-souverainete" id="souverainete">
            <div className="hp-section__inner hp-souverainete__inner">
              <div className="hp-souverainete__copy">
                <p className="hp-kicker">Confidentialité &amp; souveraineté</p>
                <h2 className="hp-h2">
                  Vos mots restent les vôtres.
                </h2>
                <p className="hp-section__intro">
                  IVIA est conçu au Québec, pour le Québec. Vos données sont
                  hébergées ici, sous le cadre de la Loi 25. Aucun partage par
                  défaut. Aucun envoi sans votre consentement explicite.
                </p>
              </div>
              <ul className="hp-souverainete__list">
                <li>
                  <strong>Hébergement québécois.</strong> Les serveurs et la
                  base de données restent sur le territoire.
                </li>
                <li>
                  <strong>Connecteurs privés.</strong> Aucune analyse publicitaire,
                  aucun pixel tiers sur votre parcours.
                </li>
                <li>
                  <strong>Consentement par étape.</strong> Vous décidez à
                  chaque pas ce qui peut être partagé, et avec qui.
                </li>
                <li>
                  <strong>Retrait possible.</strong> Vous pouvez exporter ou
                  effacer vos traces à tout moment.
                </li>
              </ul>
            </div>
          </section>

          {/* ── SAVOIRS DU VIVANT ─────────────────────────────────────────── */}
          <section className="hp-section hp-savoirs" id="savoirs">
            <div className="hp-section__inner">
              <p className="hp-kicker">Savoirs du vivant · Bibliothèque éditoriale</p>
              <h2 className="hp-h2">
                Comprendre, sans prescrire.
              </h2>
              <p className="hp-section__intro">
                IVIA rassemble des lectures, des synthèses et des sujets de
                recherche émergente. On y parle du corps, des liens, du temps
                long, et des frontières mouvantes de la conscience — toujours
                avec prudence, sources, et sans recommandation thérapeutique.
              </p>
              <div className="hp-savoirs__grid">
                {SAVOIRS.map((s) => (
                  <article key={s.tag} className="hp-savoir-card">
                    <h3 className="hp-savoir-card__tag">{s.tag}</h3>
                    <p className="hp-savoir-card__body">{s.body}</p>
                  </article>
                ))}
              </div>
              <p className="hp-savoirs__note">
                <Link href="/ressources" className="hp-link">
                  Parcourir la bibliothèque complète →
                </Link>
              </p>
            </div>
          </section>

          {/* ── DISCLAIMER NON MÉDICAL ────────────────────────────────────── */}
          <section className="hp-disclaimer" aria-label="Avertissement non médical">
            <div className="hp-section__inner">
              <p>
                <strong>IVIA n’est pas un service médical.</strong> IVIA ne pose pas
                de diagnostic, ne prescrit pas de traitement et ne remplace pas
                un·e professionnel·le de la santé. Si vous vivez une situation
                de détresse, composez le <strong>988</strong> (ligne canadienne
                d’aide en cas de crise suicidaire) ou rendez-vous à l’urgence
                la plus proche.
              </p>
            </div>
          </section>

          {/* ── CTA FINAL ─────────────────────────────────────────────────── */}
          <section className="hp-cta-final">
            <div className="hp-section__inner hp-cta-final__inner">
              <p className="hp-cta-final__text">
                Si quelque chose résonne,
                <br />
                vous pouvez entrer doucement.
              </p>
              <div className="hp-hero__ctas">
                <Link href="/demarche" className="hp-btn hp-btn--primary">
                  Entrer dans IVIA
                </Link>
                <Link href="#savoirs" className="hp-btn hp-btn--ghost">
                  Continuer à explorer
                </Link>
              </div>
            </div>
          </section>
        </main>
      </div>
    </PublicLayout>
  );
}

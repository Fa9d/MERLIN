"use client";
import Link from "next/link";
import "./styles.css";
import { PublicLayout } from "@/components/layout/PublicLayout";

/* ── Données éditoriales ──────────────────────────────────────────────────────
   Refonte V2 — branche `refonte-ivia-site-unifie`.
   Positionnement : IVIA n'est pas une clinique. Pas une promesse de guérison.
   C'est un espace québécois d'écoute, de compréhension du vivant et
   d'accompagnement vers l'autonomie.
   ────────────────────────────────────────────────────────────────────────── */

const DEPOTS = [
  "Un poids porté seul·e",
  "Une transition floue",
  "Un doute, une fatigue",
  "Une question sur le corps",
  "Une intuition de changement",
  "Un mot qui ne vient pas",
];

const DIMENSIONS = [
  {
    num: "01",
    title: "Vécu",
    body: "Ce que vous traversez, mis en mots à votre rythme.",
  },
  {
    num: "02",
    title: "Corps & métabolisme",
    body: "Sommeil, énergie, rythme — le corps comme témoin.",
  },
  {
    num: "03",
    title: "Relations",
    body: "Les liens qui portent, ceux qui pèsent, ceux à clarifier.",
  },
  {
    num: "04",
    title: "Temps & lignées",
    body: "Ce qui se transmet, se répète, demande à être reposé.",
  },
  {
    num: "05",
    title: "Sens",
    body: "Vos repères, ce qui compte, la direction qui est vôtre.",
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
    body: "Sommeil, glycémie, microbiote, charge inflammatoire : ce qu’on commence à comprendre du vivant — sans recette universelle.",
    size: "lg",
  },
  {
    tag: "Relations & attachement",
    body: "Comment les liens se forment, se réparent, se choisissent.",
    size: "sm",
  },
  {
    tag: "Temporalité & lignées",
    body: "Ce qui se transmet d’une génération à l’autre, dans les histoires et dans les corps.",
    size: "sm",
  },
  {
    tag: "Recherche émergente",
    body: "Travaux en cours sur les états de conscience modifiés. Cadre, prudence, sources.",
    size: "sm",
  },
  {
    tag: "Autonomie & souveraineté",
    body: "Prévention, soin de soi, données personnelles — reprendre du pouvoir sur sa santé.",
    size: "sm",
  },
];

/* ── Composant ────────────────────────────────────────────────────────────── */
export default function HomePage() {
  return (
    <PublicLayout>
      <div className="hp hp--v2">
        <main>
          {/* ── HERO ──────────────────────────────────────────────────────── */}
          <section className="hp-hero hp-hero--v2">
            <div className="hp-hero__bg" aria-hidden="true">
              <span className="hp-hero__bg-dot hp-hero__bg-dot--a" />
              <span className="hp-hero__bg-dot hp-hero__bg-dot--b" />
            </div>

            <div className="hp-hero__inner">
              <div className="hp-hero__copy">
                <p className="hp-eyebrow">
                  <span className="hp-eyebrow__dot" aria-hidden="true" />
                  IVIA · Québec · 2026
                </p>
                <h1 className="hp-hero__h1">
                  Parlez en toute liberté
                  <br />
                  dans <em>votre espace privé.</em>
                </h1>
                <p className="hp-hero__sub">
                  IVIA n’est ni une clinique ni un site de soins. C’est un espace
                  d’écoute et de compréhension du vivant — vos mots restent chez
                  vous, hébergés au Québec.
                </p>
                <div className="hp-hero__ctas">
                  <Link href="/demarche" className="hp-btn hp-btn--primary">
                    Commencer dans mon espace privé
                    <span className="hp-btn__arrow" aria-hidden="true">→</span>
                  </Link>
                  <Link href="#savoirs" className="hp-btn hp-btn--ghost">
                    Explorer les savoirs du vivant
                  </Link>
                </div>
                <ul className="hp-hero__signals" aria-label="Repères IVIA">
                  <li>Hébergé au Québec</li>
                  <li aria-hidden="true">·</li>
                  <li>Sans diagnostic</li>
                  <li aria-hidden="true">·</li>
                  <li>À votre rythme</li>
                </ul>
              </div>

              <figure className="hp-hero__visual">
                <div className="hp-hero__video-wrap">
                  <span className="hp-hero__video-tag" aria-hidden="true">
                    <span className="hp-hero__video-tag-dot" />
                    Trace vocale · 01
                  </span>
                  <video
                    className="hp-hero__video"
                    src="/assets/video/ivia_accueil_trace_vocale_v2.mp4"
                    controls
                    preload="metadata"
                    playsInline
                    aria-label="Trace vocale d’introduction d’IVIA par David Phaneuf"
                  >
                    <p className="hp-hero__video-fallback">
                      Trace vocale d’introduction d’IVIA — votre navigateur ne
                      supporte pas la lecture vidéo HTML5.
                    </p>
                  </video>
                  <div className="hp-hero__wave" aria-hidden="true">
                    {Array.from({ length: 28 }).map((_, i) => (
                      <span key={i} style={{ ["--i" as string]: i }} />
                    ))}
                  </div>
                </div>
                <figcaption className="hp-hero__caption">
                  David Phaneuf · fondateur · Montréal
                </figcaption>
              </figure>
            </div>
          </section>

          {/* ── POSITIONNEMENT / PONT ─────────────────────────────────────── */}
          <section className="hp-pont hp-pont--v2">
            <div className="hp-section__inner">
              <p className="hp-pont__text">
                IVIA n’apporte pas de diagnostic.
                <br />
                Pas de protocole. Pas de promesse de guérison.
              </p>
              <p className="hp-pont__em">
                <em>
                  IVIA fait de la place pour que vous puissiez vous entendre
                  vous-même.
                </em>
              </p>
            </div>
          </section>

          {/* ── CE QUE VOUS POUVEZ DÉPOSER ────────────────────────────────── */}
          <section className="hp-section hp-depots hp-depots--v2" id="deposer">
            <div className="hp-section__inner">
              <div className="hp-section__head">
                <p className="hp-kicker">Ce que vous pouvez déposer</p>
                <h2 className="hp-h2">
                  Vous n’avez pas besoin <em>d’avoir les mots parfaits.</em>
                </h2>
              </div>
              <ul className="hp-depots__cloud">
                {DEPOTS.map((d, i) => (
                  <li
                    key={d}
                    className="hp-depots__pill"
                    style={{ ["--i" as string]: i }}
                  >
                    {d}
                  </li>
                ))}
              </ul>
            </div>
          </section>

          {/* ── 5 DIMENSIONS ──────────────────────────────────────────────── */}
          <section className="hp-section hp-dimensions hp-dimensions--v2" id="dimensions">
            <div className="hp-section__inner">
              <div className="hp-section__head">
                <p className="hp-kicker">Les cinq dimensions IVIA</p>
                <h2 className="hp-h2">
                  Une lecture du vivant, <em>sans le réduire.</em>
                </h2>
                <p className="hp-section__intro">
                  Cinq portes d’entrée pour comprendre ce qui se passe pour
                  vous — à votre rythme, sans case à cocher.
                </p>
              </div>
              <ol className="hp-dim-list">
                {DIMENSIONS.map((d) => (
                  <li key={d.num} className="hp-dim-row">
                    <span className="hp-dim-row__num">{d.num}</span>
                    <h3 className="hp-dim-row__title">{d.title}</h3>
                    <p className="hp-dim-row__body">{d.body}</p>
                  </li>
                ))}
              </ol>
            </div>
          </section>

          {/* ── COMMENT IVIA ACCOMPAGNE ───────────────────────────────────── */}
          <section className="hp-section hp-accompagne hp-accompagne--v2" id="accompagnement">
            <div className="hp-section__inner">
              <div className="hp-section__head">
                <p className="hp-kicker">Comment IVIA accompagne</p>
                <h2 className="hp-h2">
                  Trois temps, <em>à votre rythme.</em>
                </h2>
              </div>
              <ol className="hp-timeline">
                {ETAPES.map((e) => (
                  <li key={e.num} className="hp-timeline__step">
                    <span className="hp-timeline__bullet" aria-hidden="true" />
                    <span className="hp-timeline__num">{e.num}</span>
                    <div className="hp-timeline__body">
                      <h3 className="hp-timeline__title">{e.title}</h3>
                      <p className="hp-timeline__text">{e.body}</p>
                    </div>
                  </li>
                ))}
              </ol>
            </div>
          </section>

          {/* ── CONFIDENTIALITÉ & SOUVERAINETÉ ────────────────────────────── */}
          <section className="hp-section hp-souverainete hp-souverainete--v2" id="souverainete">
            <div className="hp-section__inner hp-souverainete__inner">
              <div className="hp-souverainete__copy">
                <p className="hp-kicker">Confidentialité &amp; souveraineté</p>
                <h2 className="hp-h2">
                  Vos mots <em>restent les vôtres.</em>
                </h2>
                <p className="hp-section__intro">
                  IVIA est conçu au Québec, pour le Québec. Vos données sont
                  hébergées ici, sous le cadre de la Loi 25. Aucun partage par
                  défaut.
                </p>
              </div>
              <ul className="hp-souverainete__list">
                <li>
                  <span className="hp-souverainete__glyph" aria-hidden="true">
                    QC
                  </span>
                  <div>
                    <strong>Hébergement québécois.</strong>
                    <span>
                      Les serveurs et la base de données restent sur le
                      territoire.
                    </span>
                  </div>
                </li>
                <li>
                  <span className="hp-souverainete__glyph" aria-hidden="true">
                    ◯
                  </span>
                  <div>
                    <strong>Connecteurs privés.</strong>
                    <span>
                      Aucune analyse publicitaire, aucun pixel tiers sur votre
                      parcours.
                    </span>
                  </div>
                </li>
                <li>
                  <span className="hp-souverainete__glyph" aria-hidden="true">
                    ✓
                  </span>
                  <div>
                    <strong>Consentement par étape.</strong>
                    <span>
                      Vous décidez à chaque pas ce qui peut être partagé, et
                      avec qui.
                    </span>
                  </div>
                </li>
                <li>
                  <span className="hp-souverainete__glyph" aria-hidden="true">
                    ⟲
                  </span>
                  <div>
                    <strong>Retrait possible.</strong>
                    <span>
                      Vous pouvez exporter ou effacer vos traces à tout moment.
                    </span>
                  </div>
                </li>
              </ul>
            </div>
          </section>

          {/* ── SAVOIRS DU VIVANT ─────────────────────────────────────────── */}
          <section className="hp-section hp-savoirs hp-savoirs--v2" id="savoirs">
            <div className="hp-section__inner">
              <div className="hp-section__head">
                <p className="hp-kicker">Savoirs du vivant · Bibliothèque éditoriale</p>
                <h2 className="hp-h2">
                  Comprendre, <em>sans prescrire.</em>
                </h2>
                <p className="hp-section__intro">
                  Des lectures et synthèses sur le corps, les liens, le temps
                  long, et les frontières mouvantes de la conscience. Toujours
                  avec prudence, sources, et sans recommandation thérapeutique.
                </p>
              </div>
              <div className="hp-savoirs__mosaic">
                {SAVOIRS.map((s, i) => (
                  <article
                    key={s.tag}
                    className={`hp-savoir-card hp-savoir-card--${s.size}`}
                    style={{ ["--i" as string]: i }}
                  >
                    <span className="hp-savoir-card__index">
                      {String(i + 1).padStart(2, "0")}
                    </span>
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
                <strong>IVIA n’est pas un service médical.</strong> IVIA ne pose
                pas de diagnostic, ne prescrit pas de traitement et ne remplace
                pas un·e professionnel·le de la santé. En cas de détresse,
                composez le <strong>988</strong> (ligne canadienne d’aide en cas
                de crise suicidaire) ou rendez-vous à l’urgence la plus proche.
              </p>
            </div>
          </section>

          {/* ── CTA FINAL ─────────────────────────────────────────────────── */}
          <section className="hp-cta-final hp-cta-final--v2">
            <div className="hp-cta-final__halo" aria-hidden="true" />
            <div className="hp-section__inner hp-cta-final__inner">
              <p className="hp-eyebrow hp-eyebrow--center">
                <span className="hp-eyebrow__dot" aria-hidden="true" />
                Quand vous êtes prêt·e
              </p>
              <p className="hp-cta-final__text">
                Si quelque chose résonne,
                <br />
                <em>vous pouvez entrer doucement.</em>
              </p>
              <div className="hp-hero__ctas hp-hero__ctas--center">
                <Link href="/demarche" className="hp-btn hp-btn--primary">
                  Entrer dans IVIA
                  <span className="hp-btn__arrow" aria-hidden="true">→</span>
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

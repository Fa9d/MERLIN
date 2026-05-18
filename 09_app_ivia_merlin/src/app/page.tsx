"use client";
import Link from "next/link";
import Image from "next/image";
import "./styles.css";

import "./styles.v3.css";
import "./styles.orientation.css";
import { PublicLayout } from "@/components/layout/PublicLayout";
import { MesangeMark } from "@/components/MesangeMark";
import { OrientationFlow } from "@/components/orientation/OrientationFlow";

/* ──────────────────────────────────────────────────────────────────────────
   IVIA — Refonte UI/UX du seuil public
   Concept : La maison du vivant — cartographie vivante, lumière hivernale.
   Doctrine : IVIA accueille · MERLIN structure · MÉSANGES accompagne.
   Posture : non médicale, québécoise, sous consentement, sans diagnostic.
   ────────────────────────────────────────────────────────────────────────── */

const PATHWAYS = [
  {
    id: "pour-moi",
    kicker: "Pour moi",
    title: "Déposer ce que je vis",
    body:
      "Comprendre ce qui se répète, ce qui pèse et ce qui pourrait retrouver une voie d'équilibre.",
    href: "#orientation",
    cta: "Commencer mon orientation",
    tone: "ink",
  },
  {
    id: "pour-praticiens",
    kicker: "Pour les praticiens",
    title: "Structurer ma pratique",
    body:
      "Préparer, interpréter, ajuster. Sans grille rigide, sans effacer mon jugement professionnel.",
    href: "/praticiens",
    cta: "Découvrir l'espace praticien",
    tone: "sage",
  },
  {
    id: "ressources",
    kicker: "Ressources",
    title: "Lire et s'orienter",
    body:
      "Articles, repères et lexique vivant pour mieux saisir ce que MÉSANGES propose, à votre rythme.",
    href: "/ressources",
    cta: "Parcourir les ressources",
    tone: "cream",
  },
] as const;

const ACCOMPAGNEMENT = [
  {
    num: "01",
    label: "Vous déposez",
    body:
      "Dans vos mots, avec votre histoire, votre situation, vos questions et ce que vous êtes prêt·e à nommer.",
  },
  {
    num: "02",
    label: "MERLIN structure",
    body:
      "MERLIN met en ordre les éléments transmis, repère les liens possibles et prépare une lecture, toujours sous validation humaine.",
  },
  {
    num: "03",
    label: "Nous ouvrons une lecture",
    body:
      "Une lecture sensible et multidimensionnelle, sans diagnostic, pour faire apparaître des pistes de compréhension et de clarification.",
  },
  {
    num: "04",
    label: "MÉSANGES accompagne",
    body:
      "Les mésanges ne quittent pas le Québec lorsque vient l'hiver. Elles restent, traversent le froid et rappellent qu'une présence demeure possible. MÉSANGES accompagne par petites touches : une question, une nuance, une piste.",
  },
  {
    num: "05",
    label: "Vous agissez",
    body:
      "Le simple fait de déposer ce que vous vivez peut devenir un premier acte de clarté. IVIA soutient ce mouvement sans décider à votre place.",
  },
  {
    num: "06",
    label: "Nous suivons l'évolution",
    body:
      "Ensemble, nous observons ce qui change, ce qui résiste, ce qui revient et ce qui demande une attention nouvelle.",
  },
];

const ARCHITECTURE = [
  {
    name: "IVIA",
    role: "accueille",
    body:
      "IVIA est le seuil et la maison commune. IVIA signifie In Vivo In Actu : au sein de l'être, en actes.",
  },
  {
    name: "MERLIN",
    role: "structure",
    body:
      "MERLIN est l'infrastructure interne : écoute, analyse, mise en relation et structuration, sous validation humaine.",
  },
  {
    name: "MÉSANGES",
    role: "accompagne",
    body:
      "MÉSANGES accompagne par la voix, les nuances et les petites orientations qui aident à reprendre direction.",
  },
];

const SOUVERAINETE = [
  {
    glyph: "QC",
    title: "Données au Québec",
    body: "Serveurs et données sur le territoire, sous Loi 25.",
  },
  {
    glyph: "✓",
    title: "Consentement",
    body: "Vous décidez, à chaque pas, ce que vous partagez ici.",
  },
  {
    glyph: "◯",
    title: "Connecteurs privés",
    body:
      "Pas de pixels tiers, pas de branchement externe imposé. Les connecteurs restent internes et consentis.",
  },
  {
    glyph: "⚕",
    title: "Posture non médicale",
    body:
      "IVIA n'est pas une clinique. Nous ne diagnostiquons pas et nous ne prescrivons rien.",
  },
];

export default function HomePage() {
  return (
    <PublicLayout>
      <div className="hp hp--v3 hp--maison hp--seuil">
        <main>
          {/* ── HERO — La maison du vivant ─────────────────────────────── */}
          <section className="v3-hero v3-hero--seuil" aria-labelledby="hero-title">
            <div className="v3-hero__media" aria-hidden="true">
              <Image
                src="/assets/imagery/territoire-vivant-hero.png"
                alt=""
                fill
                priority
                sizes="100vw"
                className="v3-hero__img"
              />
              <span className="v3-hero__veil" />
            </div>

            <div className="v3-hero__inner v3-hero__inner--seuil">
              <h1 id="hero-title" className="v3-hero__h1 v3-hero__h1--seuil">
                MÉSANGES
              </h1>

              <p className="v3-hero__tagline">
                Écoute empathique, ancrée au Québec.
              </p>

              <p className="v3-hero__lede v3-hero__lede--seuil">
                Votre PRATICIEN MÉSANGES vous aide à clarifier et à préparer la suite.
              </p>

              <div className="v3-hero__cta-row">
                <Link
                  href="/orientation"
                  className="v3-btn v3-btn--primary"
                  data-testid="hero-cta-orientation"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  M&apos;inscrire
                  <span className="v3-btn__arrow" aria-hidden="true">↗</span>
                </Link>
                <Link
                  href="/rendez-vous"
                  className="v3-btn v3-btn--ghost"
                >
                  Prendre RDV
                </Link>
              </div>

              <p className="v3-signals v3-signals--statement">
                IVIA — MÉSANGES — Pensé par et pour les Québécois
              </p>
            </div>

            <div className="v3-hero__brand-mark" aria-hidden="true">
              <MesangeMark size={112} bare ariaLabel="" className="v3-hero__brand-mark-bird" />
            </div>
          </section>

          {/* ── PRÉSENTATION SOBRE — la voix qui accompagne ────────────── */}
          <section
            className="v3-section v3-mesanges-intro"
            id="mesanges-intro"
            aria-labelledby="mesanges-intro-title"
          >
            <div className="v3-section__inner v3-mesanges-intro__inner">
              <p className="v3-kicker">MÉSANGES</p>
              <h2 id="mesanges-intro-title" className="v3-h2">
                Une voix et une écoute qui <em>respecte votre parcours.</em>
              </h2>
              <p className="v3-section__intro">
                MÉSANGES ne remplace ni la médecine, ni les services
                d&apos;urgence. Nous vous aidons à mettre des mots, à
                reconnaître les troubles, en vous laissant choisir et
                déterminer votre voie d&apos;action.
              </p>
            </div>
          </section>

          {/* ── ORIENTATION — parcours interactif ──────────────────────── */}
          <section
            className="v3-section v3-orientation"
            id="orientation"
            aria-labelledby="orientation-title"
          >
            <div className="v3-section__inner v3-orientation__inner">
              <header className="v3-orientation__head">
                <p className="v3-kicker">Parcours d&apos;orientation</p>
                <h2 id="orientation-title" className="v3-h2">
                  Quelques questions pour <em>préparer une conversation.</em>
                </h2>
                <p className="v3-section__intro">
                  Quatre portes, une même maison. Le parcours est court,
                  mobile-first, et reste dans cette fenêtre. À la fin, un
                  portrait d&apos;orientation propose trois couches
                  prioritaires et un prochain pas. Ce n&apos;est pas un
                  diagnostic, c&apos;est un point de départ.
                </p>
              </header>

              <div className="v3-orientation__panel">
                <OrientationFlow />
              </div>
            </div>
          </section>

          {/* ── QUATRE PORTES — vue d'ensemble ────────────────────────── */}
          <section className="v3-section v3-pathways" id="voies">
            <div className="v3-section__inner">
              <p className="v3-kicker">Quatre portes</p>
              <h2 className="v3-h2 v3-h2--center">
                Choisir une porte, <em>retrouver la maison.</em>
              </h2>
              <ul className="v3-pathways__grid" aria-label="Portes IVIA">
                {PATHWAYS.map((p) => (
                  <li
                    key={p.id}
                    className={`v3-pathway v3-pathway--${p.tone}`}
                  >
                    <Link href={p.href} className="v3-pathway__inner">
                      <span className="v3-pathway__kicker">{p.kicker}</span>
                      <h3 className="v3-pathway__title">{p.title}</h3>
                      <p className="v3-pathway__body">{p.body}</p>
                      <span className="v3-pathway__cta">
                        {p.cta}
                        <span className="v3-pathway__arrow" aria-hidden="true">
                          →
                        </span>
                      </span>
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          </section>

          {/* ── COMMENT MÉSANGES VOUS ACCOMPAGNE — pas à pas ─────────── */}
          <section className="v3-section v3-accompagnement" id="approche">
            <div className="v3-section__inner">
              <p className="v3-kicker">Comment IVIA vous accompagne</p>
              <h2 className="v3-h2">
                Pas à pas, <em>à votre rythme.</em>
              </h2>
              <p className="v3-section__intro">
                IVIA est un espace structuré pour vous accueillir. Vous
                décidez du tempo, du niveau de partage et de ce qui peut être
                partagé ou non.
              </p>
              <ol className="v3-steps">
                {ACCOMPAGNEMENT.map((s) => (
                  <li key={s.num} className="v3-step">
                    <span className="v3-step__num">{s.num}</span>
                    <h3 className="v3-step__label">{s.label}</h3>
                    <p className="v3-step__body">{s.body}</p>
                  </li>
                ))}
              </ol>
            </div>
          </section>

          {/* ── MÉSANGES — présence subtile ─────────────────────────────── */}
          <section className="v3-section v3-mesanges" aria-labelledby="mesanges-title">
            <div className="v3-section__inner v3-mesanges__inner">
              <div className="v3-mesanges__copy">
                <p className="v3-kicker">MÉSANGES accompagne</p>
                <h2 id="mesanges-title" className="v3-h2">
                  Une présence <em>qui reste, même en hiver.</em>
                </h2>
                <p className="v3-section__intro">
                  Les mésanges sont parmi les rares oiseaux qui ne quittent
                  pas le Québec quand vient le froid. Elles restent, elles
                  traversent, elles signalent qu&apos;une présence demeure
                  possible. MÉSANGES accompagne dans cet esprit : petites
                  voix, nuances, pistes — jamais à la place de votre jugement.
                </p>
                <p className="v3-section__intro">
                  Aucune voix tutélaire ne remplace une décision. La présence
                  reste subtile, et c&apos;est vous qui choisissez le rythme.
                </p>
              </div>
              <figure className="v3-mesanges__media" aria-hidden="true">
                <Image
                  src="/assets/imagery/mesanges-hiver.png"
                  alt=""
                  width={720}
                  height={720}
                  className="v3-mesanges__img"
                />
              </figure>
            </div>
          </section>

          {/* ── ARCHITECTURE — IVIA · MERLIN · MÉSANGES (concis) ──────── */}
          <section className="v3-section v3-arch" id="architecture">
            <div className="v3-section__inner">
              <p className="v3-kicker">L&apos;architecture, en bref</p>
              <h2 className="v3-h2">
                Trois noms, <em>une seule attention.</em>
              </h2>
              <p className="v3-section__intro">
                MÉSANGES est la voix qui vous reçoit. Derrière, deux noms
                travaillent en silence : <strong>IVIA</strong>, la maison
                commune (In Vivo In Actu — au sein de l&apos;être, en actes),
                et <strong>MERLIN</strong>, le noyau interne qui aide à
                structurer ce qui est entendu, sous validation humaine.
              </p>
              <ol className="v3-arch__list">
                {ARCHITECTURE.map((a, i) => (
                  <li key={a.name} className="v3-arch__row">
                    <span className="v3-arch__num">
                      {String(i + 1).padStart(2, "0")}
                    </span>
                    <div className="v3-arch__name">
                      <strong>{a.name}</strong>
                      <span className="v3-arch__role">{a.role}</span>
                    </div>
                    <p className="v3-arch__body">{a.body}</p>
                  </li>
                ))}
              </ol>
            </div>
          </section>

          {/* ── SOUVERAINETÉ & PRUDENCE ─────────────────────────────────── */}
          <section className="v3-section v3-souverainete" id="souverainete">
            <div className="v3-section__inner">
              <p className="v3-kicker">Souveraineté &amp; prudence</p>
              <h2 className="v3-h2">
                Vos mots <em>restent les vôtres.</em>
              </h2>
              <ul className="v3-trust__grid">
                {SOUVERAINETE.map((t) => (
                  <li key={t.title} className="v3-trust__card">
                    <span className="v3-trust__glyph" aria-hidden="true">
                      {t.glyph}
                    </span>
                    <strong>{t.title}</strong>
                    <span>{t.body}</span>
                  </li>
                ))}
              </ul>
              <p className="v3-collectivites__not">
                IVIA aide à structurer ce que vous exprimez, à clarifier les
                choix possibles et à reconnaître les prochaines étapes à
                considérer.
              </p>
            </div>
          </section>

          {/* ── DISCLAIMER — Posture non médicale + urgence 988 ────────── */}
          <section
            className="v3-disclaimer"
            aria-label="Avertissement non médical et urgence"
          >
            <div className="v3-section__inner">
              <p>
                <strong>IVIA n&apos;est pas une clinique.</strong> Nous ne
                diagnostiquons pas et nous ne prescrivons rien. IVIA ne
                remplace pas un·e professionnel·le de la santé.
              </p>
              <p>
                <strong>Situation d&apos;urgence.</strong> IVIA n&apos;est pas
                un service d&apos;urgence. Si vous êtes en danger immédiat, si
                vous craignez de poser un geste contre vous-même ou contre
                quelqu&apos;un d&apos;autre, appelez le <strong>911</strong>.
                Au Canada, vous pouvez aussi appeler ou texter le{" "}
                <strong>988</strong> pour obtenir du soutien en cas de crise
                suicidaire. Au Québec, Info-Social est joignable au{" "}
                <strong>811</strong>.
              </p>
            </div>
          </section>

          {/* ── APPEL FINAL ─────────────────────────────────────────────── */}
          <section className="v3-final">
            <div className="v3-final__halo" aria-hidden="true" />
            <div className="v3-section__inner v3-final__inner">
              <MesangeMark
                size={64}
                withSong
                className="v3-final__mark"
              />
              <p className="v3-eyebrow v3-eyebrow--center">
                <span className="v3-eyebrow__dot" aria-hidden="true" />
                Quand vous êtes prêt·e
              </p>
              <p className="v3-final__text">
                <strong>In Vivo In Actu</strong>
                <br />
                <em>: au sein de l&apos;être, en actes.</em>
              </p>
              <ul className="v3-final__paths" aria-label="Quatre portes">
                {PATHWAYS.map((p) => (
                  <li key={p.id}>
                    <Link href={p.href} className="v3-final__path">
                      <span className="v3-final__path-kicker">{p.kicker}</span>
                      <span className="v3-final__path-arrow" aria-hidden="true">
                        →
                      </span>
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          </section>
        </main>
      </div>
    </PublicLayout>
  );
}

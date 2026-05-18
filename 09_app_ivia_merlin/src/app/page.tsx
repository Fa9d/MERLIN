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
      "Dans vos mots, votre histoire, votre situation, vos questions et ce que vous êtes prêt·e à nommer, ce que vous voulez acquérir, surmonter, parfaire.",
  },
  {
    num: "02",
    label: "MERLIN structure",
    body:
      "IVIA repère les possibles, prépare son analyse, sous validation humaine.",
  },
  {
    num: "03",
    label: "Les possibles - VOS SOLUTIONS",
    body:
      "Une interprétation sensible, multidimensionnelle, sans diagnostic et en compréhension et clarification.",
  },
  {
    num: "04",
    label: "MÉSANGES accompagne",
    body:
      "Les mésanges ne quittent pas le Québec, même en hiver. Elles restent. Elles rappellent qu'une présence demeure possible. MÉSANGES accompagne en force de proposition. Qu'enfin vous puissiez y voir clair, entendre et comprendre votre plein potentiel.",
  },
  {
    num: "05",
    label: "Vous agissez",
    body:
      "Le simple fait de déposer ce que vous vivez peut devenir un premier acte de clarté. MÉSANGES soutient ce mouvement sans décider à votre place. Ce regard extérieur et totalement objectif peut dépeindre une réalité qui parfois nous échape.",
  },
  {
    num: "06",
    label: "Nous suivons l'évolution",
    body:
      "Ensemble, nous observons ce qui change, ce qui résiste, ce qui revient et ce qui demande une attention nouvelle. Trouver vos solutions est peut-être plus simple que vous le pensiez. Les outils d'analyse et de performance développés chez IVIA offrent objectivité, clairvoyance et autonomie. À vous de jouer maintenant.",
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

          {/* ── IVIA — MÉSANGES VOUS ACCOMPAGNE — pas à pas ─────────── */}
          <section className="v3-section v3-accompagnement" id="approche">
            <div className="v3-section__inner">
              <h2 className="v3-h2">
                IVIA — MÉSANGES
                <br />
                <em>Pas à pas, à votre rythme.</em>
              </h2>
              <p className="v3-section__intro">
                Un espace structuré pour vous accueillir. À votre tempo,
                votre niveau de partage, votre réussite.
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
        </main>
      </div>
    </PublicLayout>
  );
}

"use client";
import Link from "next/link";
import Image from "next/image";
import { useState } from "react";
import "./styles.css";
import "./styles.v3.css";
import "./styles.orientation.css";
import "./styles.sondage.css";
import { PublicLayout } from "@/components/layout/PublicLayout";
import { MesangeMark } from "@/components/MesangeMark";
import { NumeriqueSondagePopup } from "@/components/sondage/NumeriqueSondagePopup";

/* ──────────────────────────────────────────────────────────────────────────
   IVIA — Refonte UI/UX du seuil public
   Concept : La maison du vivant — cartographie vivante, lumière hivernale.
   Doctrine : IVIA accueille · MÉSANGES accompagne.
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
    label: "MÉSANGES analyse",
    body:
      "MÉSANGES repère les possibles, prépare son analyse, sous validation humaine.",
  },
  {
    num: "03",
    label: "Les possibles — vos pistes",
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
      "Le simple fait de déposer ce que vous vivez peut devenir un premier acte de clarté. MÉSANGES soutient ce mouvement sans décider à votre place. Ce regard extérieur et totalement objectif peut dépeindre une réalité qui parfois nous échappe.",
  },
  {
    num: "06",
    label: "Nous suivons l'évolution",
    body:
      "Ensemble, nous observons ce qui change, ce qui résiste, ce qui revient et ce qui demande une attention nouvelle. Trouver vos solutions est peut-être plus simple que vous le pensiez. Les outils d'analyse et de performance développés chez IVIA offrent objectivité, clairvoyance et autonomie. À vous de jouer maintenant.",
  },
];

export default function HomePage() {
  const [showSondage, setShowSondage] = useState(false);

  return (
    <PublicLayout>
      <div className="hp hp--v3 hp--maison hp--seuil">
        <main>
          {/* ── HERO — Variante B (repositionnement MÉSANGES, 21 mai 2026) ─── */}
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
                Ce que vous vivez mérite d&apos;être entendu.<br />
                Pas mis en liste d&apos;attente.
              </h1>

              <p className="v3-hero__lede v3-hero__lede--seuil">
                Au Québec, 1 adulte sur 4 porte une détresse psychologique que le système
                de soins ne peut pas absorber. MÉSANGES vous accompagne pour nommer
                ce qui pèse, le clarifier — et repartir avec vos propres repères.
              </p>

              <div className="v3-hero__cta-row">
                <Link
                  href="/rendez-vous"
                  className="v3-btn v3-btn--primary"
                  data-testid="hero-cta-rendez-vous"
                >
                  Parler à quelqu&apos;un aujourd&apos;hui
                  <span className="v3-btn__arrow" aria-hidden="true">↗</span>
                </Link>
              </div>

              <p className="v3-signals v3-signals--statement">
                MÉSANGES — un service IVIA — Pensé par et pour les Québécois
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
                d&apos;urgence. Nous vous aidons à nommer ce que vous vivez
                et à déterminer votre voie d&apos;action.
              </p>
            </div>
          </section>

          {/* ── IVIA — MÉSANGES VOUS ACCOMPAGNE — pas à pas ─────────── */}
          <section className="v3-section v3-accompagnement" id="approche">
            <div className="v3-section__inner">
              <h2 className="v3-h2">
                MÉSANGES
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
                <p className="v3-kicker">MÉSANGES</p>
                <h2 id="orientation-title" className="v3-h2">
                  Quelques questions pour <em>préparer une conversation.</em>
                </h2>
                <p className="v3-section__intro">
                  Le parcours commence par ce que vous ressentez, puis affine
                  votre situation pour ouvrir une première réponse utile. À la
                  fin, un portrait d&apos;orientation propose trois axes
                  prioritaires et un prochain pas. Ce n&apos;est pas un
                  diagnostic, c&apos;est un point de départ.
                </p>
                <div className="v3-orientation__cta-row">
                  <Link href="/orientation" className="v3-btn v3-btn--primary">
                    Faire le Parcours
                    <span className="v3-btn__arrow" aria-hidden="true">↗</span>
                  </Link>
                </div>
              </header>
            </div>
          </section>

          {/* ── PROBLÈMES NUMÉRIQUES — ce que le numérique fait à nos vies ── */}
          <section className="v3-section v3-pathways" id="voies" aria-labelledby="numerique-title">
            <div className="v3-section__inner">
              <p className="v3-kicker">Le numérique et nous</p>
              <h2 id="numerique-title" className="v3-h2 v3-h2--center">
                Ce que le numérique <em>fait à votre équilibre.</em>
              </h2>
              <p className="v3-section__intro sondage-section-intro">
                La connexion permanente crée des charges invisibles. MÉSANGES
                aide à les nommer, sans jugement — pour retrouver un rapport
                sain à la technologie et à soi-même.
              </p>
              <div className="sondage-cta-wrap">
                <button
                  onClick={() => setShowSondage(true)}
                  className="v3-btn v3-btn--primary"
                >
                  Sonder mon rapport au numérique
                  <span aria-hidden="true">↗</span>
                </button>
                <p className="sondage-cta-caption">
                  3 minutes · 7 questions · résultat immédiat
                </p>
              </div>
              <ul className="v3-pathways__grid" aria-label="Problèmes liés au numérique">
                <li className="v3-pathway v3-pathway--ink">
                  <div className="v3-pathway__inner">
                    <span className="v3-pathway__kicker">Isolation</span>
                    <h3 className="v3-pathway__title">Connecté·e, mais seul·e</h3>
                    <p className="v3-pathway__body">
                      Les réseaux sociaux donnent l&apos;illusion de proximité tout
                      en creusant la distance réelle. Comparaison, validation
                      externe, peur de rater — une solitude paradoxale s&apos;installe.
                    </p>
                  </div>
                </li>
                <li className="v3-pathway v3-pathway--sage">
                  <div className="v3-pathway__inner">
                    <span className="v3-pathway__kicker">Surcharge</span>
                    <h3 className="v3-pathway__title">Trop d&apos;informations, trop peu de clarté</h3>
                    <p className="v3-pathway__body">
                      Notifications, flux continus, décisions impossibles à
                      prioriser. Le bruit numérique épuise la capacité de
                      concentration et brouille ce qui compte vraiment.
                    </p>
                  </div>
                </li>
                <li className="v3-pathway v3-pathway--cream">
                  <div className="v3-pathway__inner">
                    <span className="v3-pathway__kicker">Disponibilité constante</span>
                    <h3 className="v3-pathway__title">Jamais vraiment au repos</h3>
                    <p className="v3-pathway__body">
                      Toujours joignable, toujours réactif·ve. La frontière entre
                      vie personnelle et exigences extérieures s&apos;efface — le
                      repos devient difficile, la récupération incomplète.
                    </p>
                  </div>
                </li>
                <li className="v3-pathway v3-pathway--ink">
                  <div className="v3-pathway__inner">
                    <span className="v3-pathway__kicker">Identité fragmentée</span>
                    <h3 className="v3-pathway__title">Soi en ligne, soi réel</h3>
                    <p className="v3-pathway__body">
                      Maintenir une image numérique cohérente épuise. La
                      dissonance entre ce qu&apos;on projette et ce qu&apos;on vit
                      crée une tension sourde, difficile à nommer.
                    </p>
                  </div>
                </li>
              </ul>
            </div>
          </section>
        </main>
      </div>
      {showSondage && (
        <NumeriqueSondagePopup onClose={() => setShowSondage(false)} />
      )}
    </PublicLayout>
  );
}

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
    label: "Vous réservez",
    body:
      "En ligne, en moins de 2 minutes, sans dossier ni formulaire médical. Vous choisissez le moment qui vous convient.",
  },
  {
    num: "02",
    label: "Vous vous retrouvez",
    body:
      "Votre praticien MÉSANGES vous rejoint par audio à l\u2019heure convenue. Vous parlez. Il écoute, pose des questions, vous aide à nommer ce qui se passe — sans jugement, sans étiquette.",
  },
  {
    num: "03",
    label: "Vous repartez avec quelque chose",
    body:
      "Une lecture plus claire de votre situation, des pistes concrètes pour la suite — et, si vous le souhaitez, un document récapitulatif que vous gardez. Pas de prescription. Pas de dossier. Vos propres repères.",
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

          {/* ── QU’EST-CE QUE MÉSANGES — concret, humain ───────────────── */}
          <section
            className="v3-section v3-mesanges-intro"
            id="mesanges-intro"
            aria-labelledby="mesanges-intro-title"
          >
            <div className="v3-section__inner v3-mesanges-intro__inner">
              <p className="v3-kicker">MÉSANGES</p>
              <h2 id="mesanges-intro-title" className="v3-h2">
                Une rencontre avec <em>une vraie personne.</em>
              </h2>
              <p className="v3-section__intro">
                Vous prenez rendez-vous. Un praticien MÉSANGES vous rejoint par audio.
                Vous parlez. Il écoute, pose des questions, vous aide à nommer ce qui
                se passe. À la fin, vous repartez avec une lecture plus claire de votre
                situation — et, si vous le souhaitez, un document récapitulatif que vous gardez.
              </p>
              <ul className="v3-mesanges-intro__reassurance">
                <li>Pas d&apos;appli à installer</li>
                <li>Pas de liste d&apos;attente</li>
                <li>Pas de dossier médical requis</li>
              </ul>
            </div>
          </section>

          {/* ── OFFRES — trois façons de commencer ─────────────────────── */}
          <section
            className="v3-section v3-offres"
            id="offres"
            aria-labelledby="offres-title"
          >
            <div className="v3-section__inner">
              <p className="v3-kicker">MÉSANGES</p>
              <h2 id="offres-title" className="v3-h2">
                Trois façons de <em>commencer.</em>
              </h2>
              <ul className="v3-offres__grid">
                <li className="v3-offre">
                  <h3 className="v3-offre__title">Rencontre d&apos;écoute</h3>
                  <p className="v3-offre__body">
                    Une séance, un praticien, une heure pour déposer ce qui pèse.
                    Vous repartez avec une direction.
                  </p>
                </li>
                <li className="v3-offre">
                  <h3 className="v3-offre__title">Écoute avec compte rendu</h3>
                  <p className="v3-offre__body">
                    La même rencontre, plus un résumé écrit de ce que vous avez
                    exploré ensemble et des pistes concrètes pour la suite.
                  </p>
                </li>
                <li className="v3-offre">
                  <h3 className="v3-offre__title">Parcours de soutien</h3>
                  <p className="v3-offre__body">
                    Plusieurs rencontres dans le temps, avec un suivi documenté
                    à chaque étape. Pour ceux qui traversent quelque chose de plus long.
                  </p>
                </li>
              </ul>
            </div>
          </section>

          {/* ── POUR MOI ? — qualification + frontières ───────────────────── */}
          <section
            className="v3-section v3-pour-moi"
            id="pour-moi"
            aria-labelledby="pour-moi-title"
          >
            <div className="v3-section__inner">
              <p className="v3-kicker">MÉSANGES</p>
              <h2 id="pour-moi-title" className="v3-h2">
                Est-ce que c&apos;est <em>pour moi ?</em>
              </h2>
              <div className="v3-pour-moi__cols">
                <div className="v3-pour-moi__col v3-pour-moi__col--oui">
                  <p className="v3-pour-moi__subtitle">MÉSANGES est fait pour vous si :</p>
                  <ul className="v3-pour-moi__list">
                    <li>Vous n&apos;avez pas de médecin de famille et vous portez quelque chose seul·e</li>
                    <li>Vous traversez une transition difficile (travail, relation, deuil, isolement)</li>
                    <li>Vous voulez comprendre ce qui se répète dans votre vie — sans passer par le système de santé</li>
                    <li>Vous cherchez quelqu&apos;un à qui parler, sans étiquette, sans jugement</li>
                  </ul>
                </div>
                <div className="v3-pour-moi__col v3-pour-moi__col--non">
                  <p className="v3-pour-moi__subtitle">MÉSANGES n&apos;est pas :</p>
                  <ul className="v3-pour-moi__list">
                    <li>Un service d&apos;urgence — si vous êtes en crise, composez le <strong>3114</strong></li>
                    <li>Un service de psychothérapie réglementée</li>
                    <li>Une application de méditation ou de contenu</li>
                  </ul>
                </div>
              </div>
            </div>
          </section>

          {/* ── PROCESSUS — une rencontre en 3 temps ────────────────────── */}
          <section className="v3-section v3-accompagnement" id="approche">
            <div className="v3-section__inner">
              <h2 className="v3-h2">
                Une rencontre <em>en 3 temps.</em>
              </h2>
              <p className="v3-section__intro">
                Simple, concret, sans démarche administrative. Voici ce qui se passe
                de votre côté, du début à la fin.
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

import fs from "fs";
import path from "path";

const APP = "C:/MERLIN/09_app_ivia_merlin/src/app";

/* ============================================================
   HOMEPAGE  /
   ============================================================ */
const homepage = `"use client";
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

export default function HomePage() {
  const [showSondage, setShowSondage] = useState(false);

  return (
    <PublicLayout>
      <div className="hp hp--v3 hp--maison hp--seuil">
        <main>

          {/* ── HERO ───────────────────────────────────────────────── */}
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
                Quelqu&apos;un qui vous&nbsp;&eacute;coute.
              </h1>
              <p className="v3-hero__lede v3-hero__lede--seuil">
                Au Qu&eacute;bec. Aujourd&apos;hui. Sans liste d&apos;attente.
              </p>
              <div className="v3-hero__cta-row">
                <Link href="/mesange" className="v3-btn v3-btn--primary">
                  D&eacute;couvrir M&Eacute;SANGES
                  <span className="v3-btn__arrow" aria-hidden="true">&rarr;</span>
                </Link>
                <Link href="/rendez-vous" className="v3-btn v3-btn--secondary">
                  Prendre rendez-vous
                </Link>
              </div>
              <p className="v3-signals v3-signals--statement">
                M&Eacute;SANGES &mdash; un service IVIA &mdash; Pens&eacute; par et pour les Qu&eacute;b&eacute;cois
              </p>
            </div>

            <div className="v3-hero__brand-mark" aria-hidden="true">
              <MesangeMark size={112} bare ariaLabel="" className="v3-hero__brand-mark-bird" />
            </div>
          </section>

          {/* ── ENTRÉES — seuil client / praticien ───────────────── */}
          <section className="v3-section v3-seuil" id="entrees" aria-labelledby="seuil-title">
            <div className="v3-section__inner">
              <h2 id="seuil-title" className="v3-h2 v3-h2--center">
                Par o&ugrave; <em>commencer&nbsp;?</em>
              </h2>
              <div className="v3-seuil__grid">
                <div className="v3-seuil__card v3-seuil__card--client">
                  <p className="v3-kicker">Pour vous</p>
                  <h3 className="v3-seuil__title">Vous traversez quelque chose.</h3>
                  <p className="v3-seuil__body">
                    Transition difficile, d&eacute;tresse silencieuse, besoin de clart&eacute;.
                    M&Eacute;SANGES vous accompagne avec une vraie personne &mdash; sans dossier, sans d&eacute;lai.
                  </p>
                  <Link href="/mesange" className="v3-btn v3-btn--primary">
                    L&apos;exp&eacute;rience M&Eacute;SANGES
                    <span className="v3-btn__arrow" aria-hidden="true">&rarr;</span>
                  </Link>
                </div>

                <div className="v3-seuil__card v3-seuil__card--praticien">
                  <p className="v3-kicker">Pour les praticiens</p>
                  <h3 className="v3-seuil__title">Vous accompagnez des gens.</h3>
                  <p className="v3-seuil__body">
                    IVIA vous offre une plateforme structur&eacute;e, des clients d&eacute;j&agrave; orient&eacute;s
                    et les outils pour exercer &mdash; sans la gestion administrative.
                  </p>
                  <Link href="/praticiens" className="v3-btn v3-btn--outline">
                    Rejoindre l&apos;&eacute;quipe
                    <span className="v3-btn__arrow" aria-hidden="true">&rarr;</span>
                  </Link>
                </div>
              </div>
            </div>
          </section>

          {/* ── NUMÉRIQUE ────────────────────────────────────────── */}
          <section className="v3-section v3-pathways" id="voies" aria-labelledby="numerique-title">
            <div className="v3-section__inner">
              <p className="v3-kicker">Le num&eacute;rique et nous</p>
              <h2 id="numerique-title" className="v3-h2 v3-h2--center">
                Ce que le num&eacute;rique <em>fait &agrave; votre &eacute;quilibre.</em>
              </h2>
              <p className="v3-section__intro sondage-section-intro">
                La connexion permanente cr&eacute;e des charges invisibles. M&Eacute;SANGES
                aide &agrave; les nommer, sans jugement &mdash; pour retrouver un rapport
                sain &agrave; la technologie et &agrave; soi-m&ecirc;me.
              </p>
              <div className="sondage-cta-wrap">
                <button
                  onClick={() => setShowSondage(true)}
                  className="v3-btn v3-btn--primary"
                >
                  Sonder mon rapport au num&eacute;rique
                  <span aria-hidden="true">&rarr;</span>
                </button>
                <p className="sondage-cta-caption">
                  3 minutes &middot; 7 questions &middot; r&eacute;sultat imm&eacute;diat
                </p>
              </div>
              <ul className="v3-pathways__grid" aria-label="Probl&egrave;mes li&eacute;s au num&eacute;rique">
                <li className="v3-pathway v3-pathway--ink">
                  <div className="v3-pathway__inner">
                    <span className="v3-pathway__kicker">Isolation</span>
                    <h3 className="v3-pathway__title">Connect&eacute;&middot;e, mais seul&middot;e</h3>
                    <p className="v3-pathway__body">
                      Les r&eacute;seaux sociaux donnent l&apos;illusion de proximit&eacute; tout
                      en creusant la distance r&eacute;elle. Comparaison, validation
                      externe, peur de rater &mdash; une solitude paradoxale s&apos;installe.
                    </p>
                  </div>
                </li>
                <li className="v3-pathway v3-pathway--sage">
                  <div className="v3-pathway__inner">
                    <span className="v3-pathway__kicker">Surcharge</span>
                    <h3 className="v3-pathway__title">Trop d&apos;informations, trop peu de clart&eacute;</h3>
                    <p className="v3-pathway__body">
                      Notifications, flux continus, d&eacute;cisions impossibles &agrave;
                      prioriser. Le bruit num&eacute;rique &eacute;puise la capacit&eacute; de
                      concentration et brouille ce qui compte vraiment.
                    </p>
                  </div>
                </li>
                <li className="v3-pathway v3-pathway--cream">
                  <div className="v3-pathway__inner">
                    <span className="v3-pathway__kicker">Disponibilit&eacute; constante</span>
                    <h3 className="v3-pathway__title">Jamais vraiment au repos</h3>
                    <p className="v3-pathway__body">
                      Toujours joignable, toujours r&eacute;actif&middot;ve. La fronti&egrave;re entre
                      vie personnelle et exigences ext&eacute;rieures s&apos;efface &mdash; le
                      repos devient difficile, la r&eacute;cup&eacute;ration incompl&egrave;te.
                    </p>
                  </div>
                </li>
                <li className="v3-pathway v3-pathway--ink">
                  <div className="v3-pathway__inner">
                    <span className="v3-pathway__kicker">Identit&eacute; fragment&eacute;e</span>
                    <h3 className="v3-pathway__title">Soi en ligne, soi r&eacute;el</h3>
                    <p className="v3-pathway__body">
                      Maintenir une image num&eacute;rique coh&eacute;rente &eacute;puise. La
                      dissonance entre ce qu&apos;on projette et ce qu&apos;on vit
                      cr&eacute;e une tension sourde, difficile &agrave; nommer.
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
`;

/* ============================================================
   PAGE /mesange
   ============================================================ */
const mesange = `import Link from "next/link";
import { PublicLayout } from "@/components/layout/PublicLayout";
import { MesangeMark } from "@/components/MesangeMark";
import "../styles.css";
import "../styles.v3.css";

const OFFRES = [
  {
    title: "Rencontre d\u2019\u00e9coute",
    body: "Une s\u00e9ance, un praticien, une heure pour d\u00e9poser ce qui p\u00e8se. Vous repartez avec une direction.",
  },
  {
    title: "\u00c9coute avec compte rendu",
    body: "La m\u00eame rencontre, plus un r\u00e9sum\u00e9 \u00e9crit de ce que vous avez explor\u00e9 ensemble et des pistes concr\u00e8tes pour la suite.",
  },
  {
    title: "Parcours de soutien",
    body: "Plusieurs rencontres dans le temps, avec un suivi document\u00e9 \u00e0 chaque \u00e9tape. Pour ceux qui traversent quelque chose de plus long.",
  },
];

const ETAPES = [
  {
    num: "01",
    label: "Vous r\u00e9servez",
    body: "En ligne, en moins de 2 minutes, sans dossier ni formulaire m\u00e9dical. Vous choisissez le moment qui vous convient.",
  },
  {
    num: "02",
    label: "Vous vous retrouvez",
    body: "Votre praticien M\u00c9SANGES vous rejoint par audio \u00e0 l\u2019heure convenue. Vous parlez. Il \u00e9coute, pose des questions, vous aide \u00e0 nommer ce qui se passe \u2014 sans jugement, sans \u00e9tiquette.",
  },
  {
    num: "03",
    label: "Vous repartez avec quelque chose",
    body: "Une lecture plus claire de votre situation, des pistes concr\u00e8tes pour la suite \u2014 et, si vous le souhaitez, un document r\u00e9capitulatif que vous gardez. Pas de prescription. Pas de dossier. Vos propres rep\u00e8res.",
  },
];

export default function MesangePage() {
  return (
    <PublicLayout>
      <div className="hp hp--v3 hp--mesange">
        <main>

          {/* HERO */}
          <section className="v3-section v3-mesange-hero" aria-labelledby="mesange-hero-title">
            <div className="v3-section__inner">
              <div className="v3-mesange-hero__mark" aria-hidden="true">
                <MesangeMark size={72} bare ariaLabel="" />
              </div>
              <p className="v3-kicker">M\u00c9SANGES</p>
              <h1 id="mesange-hero-title" className="v3-h2">
                Une rencontre avec <em>une vraie personne.</em>
              </h1>
              <p className="v3-section__intro v3-section__intro--large">
                Pas une application. Pas un chatbot. Pas un formulaire.
                Un praticien form\u00e9 \u00e0 l\u2019\u00e9coute active vous rejoint par audio
                pour une conversation qui compte.
              </p>
              <div className="v3-cta-row">
                <Link href="/rendez-vous" className="v3-btn v3-btn--primary">
                  Prendre rendez-vous
                  <span className="v3-btn__arrow" aria-hidden="true">&rarr;</span>
                </Link>
                <Link href="/orientation" className="v3-btn v3-btn--outline">
                  Faire le parcours d\u2019orientation
                </Link>
              </div>
            </div>
          </section>

          {/* VALEURS */}
          <section className="v3-section v3-mesange-valeurs" id="valeurs" aria-labelledby="valeurs-title">
            <div className="v3-section__inner">
              <p className="v3-kicker">Ce que M\u00c9SANGES est</p>
              <h2 id="valeurs-title" className="v3-h2">
                Un espace d\u2019\u00e9coute. <em>Honn\u00eate et sans \u00e9tiquette.</em>
              </h2>
              <div className="v3-mesange-valeurs__cols">
                <div className="v3-mesange-valeur">
                  <h3 className="v3-mesange-valeur__title">On ne vous vendra pas une promesse qu\u2019on ne peut pas tenir.</h3>
                  <p className="v3-mesange-valeur__body">
                    Pas de transformation en sept jours. Pas de d\u00e9clic garanti.
                    Ce que M\u00c9SANGES offre est plus modeste et plus honn\u00eate\u00a0: un endroit
                    pour d\u00e9poser ce que vous portez, retrouver de la clart\u00e9, et repartir
                    avec un rep\u00e8re.
                  </p>
                </div>
                <div className="v3-mesange-valeur">
                  <h3 className="v3-mesange-valeur__title">On ne vous \u00e9crira jamais comme si vous \u00e9tiez fragile.</h3>
                  <p className="v3-mesange-valeur__body">
                    Nous parlons \u00e0 des personnes qui r\u00e9fl\u00e9chissent, qui doutent,
                    qui cherchent. Notre ton est pos\u00e9. Nous comptons sur votre
                    intelligence avant de compter sur votre \u00e9motion.
                  </p>
                </div>
                <div className="v3-mesange-valeur">
                  <h3 className="v3-mesange-valeur__title">Notre objectif\u00a0: que vous n\u2019ayez plus besoin de nous.</h3>
                  <p className="v3-mesange-valeur__body">
                    L\u2019autonomie \u00e9motionnelle est notre horizon. Pas la d\u00e9pendance.
                    Chaque rencontre vise \u00e0 vous donner vos propres rep\u00e8res \u2014 pas
                    \u00e0 vous attacher \u00e0 un service.
                  </p>
                </div>
              </div>
            </div>
          </section>

          {/* DÉROULEMENT */}
          <section className="v3-section v3-accompagnement" id="deroulement" aria-labelledby="deroulement-title">
            <div className="v3-section__inner">
              <p className="v3-kicker">Une rencontre en 3 temps</p>
              <h2 id="deroulement-title" className="v3-h2">
                Simple, concret, <em>sans d\u00e9marche administrative.</em>
              </h2>
              <ol className="v3-steps">
                {ETAPES.map((s) => (
                  <li key={s.num} className="v3-step">
                    <span className="v3-step__num">{s.num}</span>
                    <h3 className="v3-step__label">{s.label}</h3>
                    <p className="v3-step__body">{s.body}</p>
                  </li>
                ))}
              </ol>
            </div>
          </section>

          {/* OFFRES */}
          <section className="v3-section v3-offres" id="offres" aria-labelledby="offres-title">
            <div className="v3-section__inner">
              <p className="v3-kicker">Trois fa\u00e7ons de commencer</p>
              <h2 id="offres-title" className="v3-h2">
                Choisissez ce qui <em>vous convient.</em>
              </h2>
              <ul className="v3-offres__grid">
                {OFFRES.map((o) => (
                  <li key={o.title} className="v3-offre">
                    <h3 className="v3-offre__title">{o.title}</h3>
                    <p className="v3-offre__body">{o.body}</p>
                  </li>
                ))}
              </ul>
              <div className="v3-cta-row v3-cta-row--center">
                <Link href="/rendez-vous" className="v3-btn v3-btn--primary">
                  R\u00e9server une rencontre
                  <span className="v3-btn__arrow" aria-hidden="true">&rarr;</span>
                </Link>
              </div>
            </div>
          </section>

          {/* FRONTIÈRES */}
          <section className="v3-section v3-pour-moi" id="frontieres" aria-labelledby="frontieres-title">
            <div className="v3-section__inner">
              <p className="v3-kicker">Ce que M\u00c9SANGES n\u2019est pas</p>
              <h2 id="frontieres-title" className="v3-h2">
                Des fronti\u00e8res <em>claires et honn\u00eates.</em>
              </h2>
              <ul className="v3-mesange-frontieres">
                <li>
                  <strong>M\u00c9SANGES ne fait pas de diagnostic.</strong>{" "}
                  Aucun de nos contenus n\u2019est un avis m\u00e9dical, psychologique ou psychiatrique.
                </li>
                <li>
                  <strong>M\u00c9SANGES ne traite pas la d\u00e9tresse aigu\u00eb.</strong>{" "}
                  Si vous traversez une crise, composez le <strong>811</strong> (Info-Social),
                  le <strong>1\u00a0866\u00a0APPELLE</strong> (pr\u00e9vention du suicide)
                  ou le <strong>911</strong> si le danger est imm\u00e9diat.
                </li>
                <li>
                  <strong>M\u00c9SANGES n\u2019est pas de la psychoth\u00e9rapie r\u00e9glement\u00e9e.</strong>{" "}
                  Si vous avez d\u00e9j\u00e0 un suivi clinique, continuez avec votre professionnel.
                  IVIA peut \u00eatre un compl\u00e9ment \u2014 jamais un substitut.
                </li>
                <li>
                  <strong>M\u00c9SANGES n\u2019est pas une application.</strong>{" "}
                  Pas de notifications, pas d\u2019abonnement mensuel, pas de contenu \u00e0 consommer.
                  Une conversation. Une vraie personne.
                </li>
              </ul>
            </div>
          </section>

        </main>
      </div>
    </PublicLayout>
  );
}
`;

/* ============================================================
   PAGE /praticiens  (refonte)
   ============================================================ */
const praticiens = `"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { listPraticiens, PraticienPublic } from "@/lib/merlin-api";
import { PublicLayout } from "@/components/layout/PublicLayout";
import "../styles.css";
import "../styles.v3.css";

const AVANTAGES = [
  {
    title: "Des clients d\u00e9j\u00e0 orient\u00e9s",
    body: "Les personnes qui vous rejoignent ont fait le parcours d\u2019orientation IVIA. Vous commencez avec du contexte, pas \u00e0 z\u00e9ro.",
  },
  {
    title: "Z\u00e9ro gestion administrative",
    body: "R\u00e9servations, paiements, rappels \u2014 tout est g\u00e9r\u00e9 par la plateforme. Vous vous concentrez sur la rencontre.",
  },
  {
    title: "Des outils pour documenter",
    body: "Compte rendu structur\u00e9, suivi entre s\u00e9ances, espace priv\u00e9 pour vos notes. Ce qu\u2019il faut, rien de plus.",
  },
  {
    title: "Une communaut\u00e9 de pratique",
    body: "Vous rejoignez une \u00e9quipe de praticiens qui partagent la m\u00eame posture\u00a0: honn\u00eate, non m\u00e9dicale, qu\u00e9b\u00e9coise.",
  },
];

const ETAPES_CANDIDATURE = [
  {
    num: "01",
    label: "Vous candidatez",
    body: "Un formulaire court. Votre formation, votre approche, votre disponibilit\u00e9. On lit tout.",
  },
  {
    num: "02",
    label: "On se rencontre",
    body: "Un entretien de 30 minutes par audio. On vous explique la plateforme, vous nous expliquez votre pratique.",
  },
  {
    num: "03",
    label: "Vous int\u00e9grez l\u2019\u00e9quipe",
    body: "Profil activ\u00e9, premi\u00e8res disponibilit\u00e9s, premier client. On vous accompagne dans les premi\u00e8res rencontres.",
  },
];

export default function PraticiensPage() {
  const [praticiens, setPraticiens] = useState<PraticienPublic[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    listPraticiens()
      .then(setPraticiens)
      .catch((err: unknown) => {
        const msg = err instanceof Error ? err.message : "Erreur inconnue";
        setError(msg);
      })
      .finally(() => setLoading(false));
  }, []);

  const langLabel = (code: string) => {
    const map: Record<string, string> = { fr: "Fran\u00e7ais", en: "English" };
    return map[code] ?? code;
  };

  const channelLabel = (code: string) => {
    const map: Record<string, string> = {
      direct: "Direct",
      in_person: "Pr\u00e9sentiel",
      async: "Asynchrone",
    };
    return map[code] ?? code;
  };

  const parseTags = (json: string | null): string[] => {
    if (!json) return [];
    try {
      const parsed: unknown = JSON.parse(json);
      if (Array.isArray(parsed)) {
        return parsed.filter((v): v is string => typeof v === "string");
      }
    } catch {
      // ignore
    }
    return [];
  };

  return (
    <PublicLayout>
      <div className="hp hp--v3 hp--praticiens">
        <main>

          {/* HERO */}
          <section className="v3-section v3-mesange-hero" aria-labelledby="praticiens-hero-title">
            <div className="v3-section__inner">
              <p className="v3-kicker">Pour les praticiens</p>
              <h1 id="praticiens-hero-title" className="v3-h2">
                Pratiquez avec <em>M\u00c9SANGES.</em>
              </h1>
              <p className="v3-section__intro v3-section__intro--large">
                IVIA r\u00e9unit des praticiens form\u00e9s \u00e0 l\u2019\u00e9coute active et \u00e0
                l\u2019accompagnement en premi\u00e8re ligne. Vous apportez votre pr\u00e9sence
                et votre jugement. On s\u2019occupe du reste.
              </p>
              <div className="v3-cta-row">
                <Link href="/praticien" className="v3-btn v3-btn--primary">
                  Rejoindre l\u2019\u00e9quipe
                  <span className="v3-btn__arrow" aria-hidden="true">&rarr;</span>
                </Link>
              </div>
            </div>
          </section>

          {/* AVANTAGES */}
          <section className="v3-section v3-offres" id="avantages" aria-labelledby="avantages-title">
            <div className="v3-section__inner">
              <p className="v3-kicker">Ce que vous gagnez</p>
              <h2 id="avantages-title" className="v3-h2">
                Exercez mieux, <em>sans friction administrative.</em>
              </h2>
              <ul className="v3-offres__grid">
                {AVANTAGES.map((a) => (
                  <li key={a.title} className="v3-offre">
                    <h3 className="v3-offre__title">{a.title}</h3>
                    <p className="v3-offre__body">{a.body}</p>
                  </li>
                ))}
              </ul>
            </div>
          </section>

          {/* PROCESSUS */}
          <section className="v3-section v3-accompagnement" id="processus" aria-labelledby="processus-title">
            <div className="v3-section__inner">
              <p className="v3-kicker">Comment \u00e7a fonctionne</p>
              <h2 id="processus-title" className="v3-h2">
                De la candidature <em>\u00e0 la premi\u00e8re rencontre.</em>
              </h2>
              <ol className="v3-steps">
                {ETAPES_CANDIDATURE.map((s) => (
                  <li key={s.num} className="v3-step">
                    <span className="v3-step__num">{s.num}</span>
                    <h3 className="v3-step__label">{s.label}</h3>
                    <p className="v3-step__body">{s.body}</p>
                  </li>
                ))}
              </ol>
              <div className="v3-cta-row v3-cta-row--center">
                <Link href="/praticien" className="v3-btn v3-btn--primary">
                  D\u00e9marrer ma candidature
                  <span className="v3-btn__arrow" aria-hidden="true">&rarr;</span>
                </Link>
              </div>
            </div>
          </section>

          {/* ÉQUIPE */}
          <section className="v3-section" id="equipe" aria-labelledby="equipe-title">
            <div className="v3-section__inner">
              <p className="v3-kicker">L\u2019\u00e9quipe</p>
              <h2 id="equipe-title" className="v3-h2">
                Ceux qui <em>pratiquent d\u00e9j\u00e0.</em>
              </h2>
              {loading && <p className="praticiens-page-state">Chargement\u2026</p>}
              {error && <p className="praticiens-page-error">{error}</p>}
              {!loading && !error && praticiens.length === 0 && (
                <p className="praticiens-page-state">
                  L\u2019\u00e9quipe se constitue. Les premiers praticiens arrivent bient\u00f4t.
                </p>
              )}
              {!loading && praticiens.length > 0 && (
                <div className="grid praticiens-grid">
                  {praticiens.map((p) => {
                    const langs = parseTags(p.spoken_languages);
                    const channels = parseTags(p.available_channels);
                    return (
                      <article key={p.id} className="card praticiens-card">
                        <div>
                          <h3 className="praticiens-card-title">{p.display_name}</h3>
                          {p.title_line && (
                            <p className="praticiens-card-subtitle">{p.title_line}</p>
                          )}
                        </div>
                        {p.intro_text && (
                          <p className="praticiens-card-intro">{p.intro_text}</p>
                        )}
                        {(langs.length > 0 || channels.length > 0) && (
                          <div className="praticiens-card-tags">
                            {langs.map((l) => (
                              <span key={l} className="praticiens-tag praticiens-tag--language">
                                {langLabel(l)}
                              </span>
                            ))}
                            {channels.map((c) => (
                              <span key={c} className="praticiens-tag praticiens-tag--channel">
                                {channelLabel(c)}
                              </span>
                            ))}
                          </div>
                        )}
                        <Link href={\`/praticiens/\${p.id}\`} className="button button-primary">
                          Voir les disponibilit\u00e9s
                        </Link>
                      </article>
                    );
                  })}
                </div>
              )}
            </div>
          </section>

        </main>
      </div>
    </PublicLayout>
  );
}
`;

/* ============================================================
   CSS — nouvelles classes
   ============================================================ */
const css = `
/* ── SEUIL — 2 cartes d'entrée homepage ──────────────────────── */
.v3-seuil { background: var(--color-cream, #f9f5ef); }

.v3-seuil__grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
  margin-top: 2.5rem;
}
@media (max-width: 720px) {
  .v3-seuil__grid { grid-template-columns: 1fr; }
}

.v3-seuil__card {
  background: var(--color-white, #fff);
  border-radius: 1rem;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  border: 1px solid var(--color-border, rgba(0,0,0,.08));
}
.v3-seuil__card--praticien {
  background: var(--color-ink, #1a1a2e);
  color: var(--color-white, #fff);
  border-color: transparent;
}
.v3-seuil__card--praticien .v3-kicker { opacity: .7; }

.v3-seuil__title {
  font-size: clamp(1.15rem, 2vw, 1.35rem);
  font-weight: 600;
  line-height: 1.3;
  margin: 0;
}
.v3-seuil__body {
  font-size: .95rem;
  line-height: 1.6;
  opacity: .85;
  flex: 1;
}

/* ── BTN variants ─────────────────────────────────────────────── */
.v3-btn--secondary {
  background: transparent;
  border: 2px solid var(--color-white, #fff);
  color: var(--color-white, #fff);
  padding: .7rem 1.4rem;
  border-radius: 2rem;
  font-weight: 600;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: .4rem;
  transition: background .2s, color .2s;
}
.v3-btn--secondary:hover {
  background: rgba(255,255,255,.15);
}
.v3-btn--outline {
  background: transparent;
  border: 2px solid currentColor;
  color: inherit;
  padding: .7rem 1.4rem;
  border-radius: 2rem;
  font-weight: 600;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: .4rem;
  transition: background .2s;
}
.v3-btn--outline:hover { background: rgba(0,0,0,.06); }

/* ── MÉSANGE page hero ────────────────────────────────────────── */
.v3-mesange-hero { padding-block: 5rem 3rem; }
.v3-mesange-hero__mark {
  margin-bottom: 1.5rem;
  opacity: .7;
}
.v3-section__intro--large {
  font-size: clamp(1rem, 2vw, 1.2rem);
  max-width: 640px;
  line-height: 1.7;
}

/* ── CTA ROW (generic) ───────────────────────────────────────── */
.v3-cta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 2rem;
}
.v3-cta-row--center { justify-content: center; }

/* ── VALEURS — 3 colonnes ────────────────────────────────────── */
.v3-mesange-valeurs__cols {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin-top: 2.5rem;
}
@media (max-width: 860px) {
  .v3-mesange-valeurs__cols { grid-template-columns: 1fr; }
}
.v3-mesange-valeur {
  padding: 1.75rem;
  background: var(--color-cream, #f9f5ef);
  border-radius: .75rem;
}
.v3-mesange-valeur__title {
  font-size: 1rem;
  font-weight: 700;
  margin: 0 0 .75rem;
  line-height: 1.4;
}
.v3-mesange-valeur__body {
  font-size: .9rem;
  line-height: 1.65;
  opacity: .85;
  margin: 0;
}

/* ── FRONTIÈRES — liste texte ────────────────────────────────── */
.v3-mesange-frontieres {
  list-style: none;
  padding: 0;
  margin: 2rem 0 0;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  max-width: 740px;
}
.v3-mesange-frontieres li {
  padding-left: 1.25rem;
  border-left: 3px solid var(--color-argile, #c8735a);
  line-height: 1.65;
  font-size: .95rem;
}
.v3-mesange-frontieres strong { color: var(--color-ink, #1a1a2e); }

/* ── Dark mode adaptations ───────────────────────────────────── */
@media (prefers-color-scheme: dark) {
  .v3-seuil { background: var(--color-surface-2, #1e1e2e); }
  .v3-seuil__card { background: var(--color-surface-1, #16161e); border-color: rgba(255,255,255,.08); }
  .v3-seuil__card--praticien { background: var(--color-cream-dark, #2a2a3a); }
  .v3-mesange-valeur { background: var(--color-surface-2, #1e1e2e); }
  .v3-mesange-frontieres strong { color: var(--color-cream, #f9f5ef); }
}
[data-theme="dark"] .v3-seuil { background: var(--color-surface-2, #1e1e2e); }
[data-theme="dark"] .v3-seuil__card { background: var(--color-surface-1, #16161e); border-color: rgba(255,255,255,.08); }
[data-theme="dark"] .v3-seuil__card--praticien { background: #2a2a3a; }
[data-theme="dark"] .v3-mesange-valeur { background: var(--color-surface-2, #1e1e2e); }
[data-theme="dark"] .v3-mesange-frontieres strong { color: var(--color-cream, #f9f5ef); }
`;

// Write files
fs.writeFileSync(path.join(APP, "page.tsx"), homepage, "utf8");
console.log("✓ page.tsx");

fs.mkdirSync(path.join(APP, "mesange"), { recursive: true });
fs.writeFileSync(path.join(APP, "mesange/page.tsx"), mesange, "utf8");
console.log("✓ mesange/page.tsx");

fs.writeFileSync(path.join(APP, "praticiens/page.tsx"), praticiens, "utf8");
console.log("✓ praticiens/page.tsx");

// Append CSS (avoid duplicates)
const cssPath = path.join(APP, "styles.v3.css");
const existing = fs.readFileSync(cssPath, "utf8");
if (!existing.includes("v3-seuil__grid")) {
  fs.appendFileSync(cssPath, css, "utf8");
  console.log("✓ styles.v3.css (CSS ajouté)");
} else {
  console.log("~ styles.v3.css (déjà à jour)");
}

console.log("\nDone.");

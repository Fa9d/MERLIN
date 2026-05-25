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

const TABS = [
  { id: "individuel", label: "\u00c9coute individuelle" },
  { id: "parcours",   label: "Parcours de soutien" },
  { id: "praticiens", label: "Pour les praticiens" },
];

const CARDS: Record<
  string,
  { badge?: string; title: string; body: string; cta: string; href: string; ctaSecondaire?: string; hrefSecondaire?: string }[]
> = {
  individuel: [
    {
      badge: "Le plus demand\u00e9",
      title: "Rencontre d\u2019\u00e9coute",
      body: "Une s\u00e9ance, un praticien, une heure pour d\u00e9poser ce qui p\u00e8se. Vous repartez avec une direction.",
      cta: "R\u00e9server",
      href: "/rendez-vous",
      ctaSecondaire: "En savoir plus",
      hrefSecondaire: "/mesange",
    },
    {
      badge: "Avec suivi \u00e9crit",
      title: "\u00c9coute avec compte rendu",
      body: "La m\u00eame rencontre, plus un r\u00e9sum\u00e9 \u00e9crit de ce que vous avez explor\u00e9 ensemble et des pistes concr\u00e8tes pour la suite.",
      cta: "R\u00e9server",
      href: "/rendez-vous",
      ctaSecondaire: "En savoir plus",
      hrefSecondaire: "/mesange",
    },
  ],
  parcours: [
    {
      badge: "Recommand\u00e9",
      title: "Parcours court",
      body: "Deux ou trois rencontres rapproch\u00e9es pour traverser une p\u00e9riode difficile avec un fil conducteur. Un m\u00eame praticien tout au long.",
      cta: "Commencer",
      href: "/rendez-vous",
      ctaSecondaire: "En savoir plus",
      hrefSecondaire: "/mesange",
    },
    {
      badge: "Sur la dur\u00e9e",
      title: "Accompagnement continu",
      body: "Plusieurs rencontres dans le temps, avec un suivi document\u00e9 \u00e0 chaque \u00e9tape. Pour ceux qui traversent quelque chose de plus long.",
      cta: "Commencer",
      href: "/rendez-vous",
      ctaSecondaire: "En savoir plus",
      hrefSecondaire: "/mesange",
    },
  ],
  praticiens: [
    {
      badge: "Rejoignez l\u2019\u00e9quipe",
      title: "Devenir praticien M\u00c9SANGES",
      body: "IVIA vous offre une plateforme structur\u00e9e, des clients d\u00e9j\u00e0 orient\u00e9s et les outils pour exercer \u2014 sans la gestion administrative.",
      cta: "Rejoindre l\u2019\u00e9quipe",
      href: "/praticiens",
      ctaSecondaire: "D\u00e9couvrir les outils",
      hrefSecondaire: "/praticiens",
    },
    {
      badge: "D\u00e9j\u00e0 praticien",
      title: "Acc\u00e9der \u00e0 votre espace",
      body: "Consultez vos prochains rendez-vous, vos notes de s\u00e9ance et les demandes de nouveaux clients depuis votre espace d\u00e9di\u00e9.",
      cta: "Se connecter",
      href: "/acces-client",
      ctaSecondaire: "D\u00e9couvrir les outils",
      hrefSecondaire: "/praticiens",
    },
  ],
};

const VALEURS = [
  {
    glyph: "⊘",
    label: "Aucun dossier m\u00e9dical",
    body: "Vous n\u2019avez pas \u00e0 vous qualifier pour \u00eatre entendu. Aucun formulaire clinique, aucune \u00e9tiquette diagnostique.",
  },
  {
    glyph: "◎",
    label: "Praticiens qu\u00e9b\u00e9cois form\u00e9s",
    body: "Nos praticiens sont form\u00e9s \u00e0 l\u2019\u00e9coute active non-directive. Vous repartez avec de vraies pistes, pas des platitudes.",
  },
  {
    glyph: "◇",
    label: "Disponible 7\u202fjours sur\u202f7",
    body: "Trouvez un cr\u00e9neau quand vous en avez besoin, sans attendre des semaines.",
  },
  {
    glyph: "◻",
    label: "Confidentialit\u00e9 stricte",
    body: "Vos conversations restent strictement confidentielles. Aucun partage sans votre consentement explicite.",
  },
];

export default function HomePage() {
  const [activeTab, setActiveTab]   = useState("individuel");
  const [showSondage, setShowSondage] = useState(false);

  return (
    <PublicLayout>
      <div className="hp hp--v3 hp--maison hp--seuil">
        <main>

          {/* ── HERO — photo fondue, style EQ ──────────────────────── */}
          <section className="v3-hero v3-hero--seuil v3-hero--eq" aria-labelledby="hero-title">
            <div className="v3-hero__photo-wrap" aria-hidden="true">
              <Image
                src="/assets/imagery/territoire-vivant-hero.png"
                alt=""
                fill
                priority
                sizes="100vw"
                className="v3-hero__photo"
              />
              <span className="v3-hero__photo-fade" />
            </div>

            <div className="v3-hero__inner v3-hero__inner--eq">
              <h1 id="hero-title" className="v3-hero__h1 v3-hero__h1--eq">
                Faites affaire avec&nbsp;<em>quelqu&apos;un qui vous &eacute;coute.</em>
              </h1>
              <p className="v3-hero__lede v3-hero__lede--eq">
                Parlez. D&eacute;posez. Repartez plus l&eacute;ger.
                Au Qu&eacute;bec. Aujourd&apos;hui. Sans liste d&apos;attente.
              </p>
              <div className="v3-hero__cta-row">
                <Link href="/rendez-vous" className="v3-btn v3-btn--ink">
                  Prendre rendez-vous
                  <span className="v3-btn__arrow" aria-hidden="true">&rarr;</span>
                </Link>
                <Link href="/mesange" className="v3-btn v3-btn--ghost">
                  D&eacute;couvrir M&Eacute;SANGES
                </Link>
              </div>
              <p className="v3-hero__trinity">
                <strong>M&Eacute;SANGES</strong> &mdash; un service IVIA &mdash; Pens&eacute; par et pour les Qu&eacute;b&eacute;cois
              </p>
            </div>

            <div className="v3-hero__brand-mark" aria-hidden="true">
              <MesangeMark size={112} bare ariaLabel="" className="v3-hero__brand-mark-bird" />
            </div>
          </section>

          {/* ── PROOF BAR — 3 colonnes chiffres clés ──────────────── */}
          <section className="v3-proof-bar" aria-label="Nos engagements">
            <div className="v3-proof-bar__inner">
              <div className="v3-proof-bar__stat">
                <strong>+ de praticiens</strong>
                <span>en exercice sur la plateforme</span>
              </div>
              <div className="v3-proof-bar__sep" aria-hidden="true" />
              <div className="v3-proof-bar__stat">
                <strong>Gagnez jusqu&apos;&agrave;&nbsp;7&times;</strong>
                <span>plus de clart&eacute; qu&apos;en r&eacute;seau social</span>
              </div>
              <div className="v3-proof-bar__sep" aria-hidden="true" />
              <div className="v3-proof-bar__stat">
                <strong>0&nbsp;dossier m&eacute;dical</strong>
                <span>aucune &eacute;tiquette, aucun diagnostic</span>
              </div>
            </div>
          </section>

          {/* ── SERVICES — onglets + cartes ───────────────────────── */}
          <section className="v3-section v3-services" id="services" aria-labelledby="services-title">
            <div className="v3-section__inner">
              <p className="v3-kicker">Nos services</p>
              <h2 id="services-title" className="v3-h2 v3-h2--center">
                Ce que vous pouvez faire <em>sur M&Eacute;SANGES.</em>
              </h2>

              <div className="v3-services__tabs" role="tablist" aria-label="Cat&eacute;gories de services">
                {TABS.map(tab => (
                  <button
                    key={tab.id}
                    role="tab"
                    aria-selected={activeTab === tab.id ? "true" : "false"}
                    aria-controls={`panel-${tab.id}`}
                    id={`tab-${tab.id}`}
                    onClick={() => setActiveTab(tab.id)}
                    className={`v3-tab-btn${activeTab === tab.id ? " v3-tab-btn--active" : ""}`}
                  >
                    {tab.label}
                  </button>
                ))}
              </div>

              <div
                role="tabpanel"
                id={`panel-${activeTab}`}
                aria-labelledby={`tab-${activeTab}`}
                className="v3-services__grid"
              >
                {CARDS[activeTab].map(card => (
                  <div key={card.title} className="v3-service-card">
                    {card.badge && (
                      <span className="v3-service-card__badge">{card.badge}</span>
                    )}
                    <h3 className="v3-service-card__title">{card.title}</h3>
                    <p className="v3-service-card__body">{card.body}</p>
                    <div className="v3-service-card__actions">
                      <Link href={card.href} className="v3-btn v3-btn--ink v3-btn--sm">
                        {card.cta}
                        <span className="v3-btn__arrow" aria-hidden="true">&rarr;</span>
                      </Link>
                      {card.ctaSecondaire && (
                        <Link href={card.hrefSecondaire!} className="v3-btn v3-btn--ghost v3-btn--sm">
                          {card.ctaSecondaire}
                        </Link>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </section>

          {/* ── VALEURS CLÉS — 4 blocs ───────────────────────────── */}
          <section className="v3-section v3-valeurs-cles" aria-labelledby="valeurs-title">
            <div className="v3-section__inner">
              <h2 id="valeurs-title" className="v3-h2 v3-h2--center v3-valeurs-cles__heading">
                Faites valoir votre mieux-&ecirc;tre avec <em>une des meilleures solutions au Qu&eacute;bec.</em>
              </h2>
              <div className="v3-valeurs-cles__grid">
                {VALEURS.map(v => (
                  <div key={v.label} className="v3-valeur-cle">
                    <div className="v3-valeur-cle__glyph" aria-hidden="true">{v.glyph}</div>
                    <div className="v3-valeur-cle__text">
                      <p className="v3-valeur-cle__label">{v.label}</p>
                      <p className="v3-valeur-cle__body">{v.body}</p>
                    </div>
                  </div>
                ))}
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
              <p className="v3-section__intro sondage-section-intro">La connexion permanente cr&eacute;e des charges invisibles. M&Eacute;SANGES aide &agrave; les nommer, sans jugement &mdash; pour retrouver un rapport sain &agrave; la technologie et &agrave; soi-m&ecirc;me.</p>
              <div className="sondage-cta-wrap">
                <button
                  onClick={() => setShowSondage(true)}
                  className="v3-btn v3-btn--primary"
                >
                  Sonder mon rapport au num&eacute;rique
                  <span aria-hidden="true">&rarr;</span>
                </button>
                <p className="sondage-cta-caption">3 minutes &middot; 7 questions &middot; r&eacute;sultat imm&eacute;diat</p>
              </div>
              <ul className="v3-pathways__grid" aria-label="Probl&egrave;mes li&eacute;s au num&eacute;rique">
                <li className="v3-pathway v3-pathway--ink">
                  <div className="v3-pathway__inner">
                    <span className="v3-pathway__kicker">Isolation</span>
                    <h3 className="v3-pathway__title">Connect&eacute;&middot;e, mais seul&middot;e</h3>
                    <p className="v3-pathway__body">Les r&eacute;seaux sociaux donnent l&apos;illusion de proximit&eacute; tout en creusant la distance r&eacute;elle. Comparaison, validation externe, peur de rater &mdash; une solitude paradoxale s&apos;installe.</p>
                  </div>
                </li>
                <li className="v3-pathway v3-pathway--sage">
                  <div className="v3-pathway__inner">
                    <span className="v3-pathway__kicker">Surcharge</span>
                    <h3 className="v3-pathway__title">Trop d&apos;informations, trop peu de clart&eacute;</h3>
                    <p className="v3-pathway__body">Notifications, flux continus, d&eacute;cisions impossibles &agrave; prioriser. Le bruit num&eacute;rique &eacute;puise la capacit&eacute; de concentration et brouille ce qui compte vraiment.</p>
                  </div>
                </li>
                <li className="v3-pathway v3-pathway--cream">
                  <div className="v3-pathway__inner">
                    <span className="v3-pathway__kicker">Disponibilit&eacute; constante</span>
                    <h3 className="v3-pathway__title">Jamais vraiment au repos</h3>
                    <p className="v3-pathway__body">Toujours joignable, toujours r&eacute;actif&middot;ve. La fronti&egrave;re entre vie personnelle et exigences ext&eacute;rieures s&apos;efface &mdash; le repos devient difficile, la r&eacute;cup&eacute;ration incompl&egrave;te.</p>
                  </div>
                </li>
                <li className="v3-pathway v3-pathway--ink">
                  <div className="v3-pathway__inner">
                    <span className="v3-pathway__kicker">Identit&eacute; fragment&eacute;e</span>
                    <h3 className="v3-pathway__title">Soi en ligne, soi r&eacute;el</h3>
                    <p className="v3-pathway__body">Maintenir une image num&eacute;rique coh&eacute;rente &eacute;puise. La dissonance entre ce qu&apos;on projette et ce qu&apos;on vit cr&eacute;e une tension sourde, difficile &agrave; nommer.</p>
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

"use client";
import Link from "next/link";
import Image from "next/image";
import { useState } from "react";
import "./styles.css";
import "./styles.v3.css";
import "./styles.orientation.css";
import { PublicLayout } from "@/components/layout/PublicLayout";
import { MesangeMark } from "@/components/MesangeMark";

const TABS = [
  { id: "dependances", label: "D\u00e9pendances" },
  { id: "relations",   label: "Relations\u00a0& couple" },
  { id: "equilibre",   label: "\u00c9quilibre de vie" },
];

const CARDS: Record<
  string,
  { badge?: string; title: string; body: string; cta: string; href: string; ctaSecondaire?: string; hrefSecondaire?: string }[]
> = {
  dependances: [
    {
      badge: "Affective \u00b7 \u00c9motionnelle",
      title: "Quand un lien devient une prison",
      body: "Besoin constant d\u2019approbation, peur de l\u2019abandon, attachement douloureux. Que la d\u00e9pendance soit \u00e0 une personne, \u00e0 un r\u00f4le ou \u00e0 une dynamique relationnelle \u2014 elle a une histoire. On peut la comprendre, sans en avoir honte.",
      cta: "En parler",
      href: "/rendez-vous",
    },
    {
      badge: "Num\u00e9rique \u00b7 Alimentaire \u00b7 Substances",
      title: "Ce qu\u2019on consomme pour ne pas ressentir",
      body: "Alcool, cannabis, jeu compulsif, achats, travail, pornographie, nourriture \u2014 les formes sont nombreuses. Ce qu\u2019elles ont en commun\u00a0: une douleur sous-jacente qui cherche \u00e0 s\u2019apaiser. Nos praticiens vous accompagnent sans jugement.",
      cta: "En parler",
      href: "/rendez-vous",
    },
  ],
  relations: [
    {
      badge: "Relations toxiques",
      title: "Se sortir des sch\u00e9mas qui font mal",
      body: "Manipulation, emprise, cycles de rupture et retour, deuil impossible, patterns qui se r\u00e9p\u00e8tent. On ne choisit pas consciemment de r\u00e9p\u00e9ter ce qui blesse. Comprendre d\u2019o\u00f9 \u00e7a vient, c\u2019est le premier pas pour choisir autrement.",
      cta: "En parler",
      href: "/rendez-vous",
    },
    {
      badge: "Vie de couple",
      title: "Ce qui se passe entre deux personnes",
      body: "Communication bris\u00e9e, conflits cycliques, d\u00e9sir qui s\u2019\u00e9teint, jalousie, mensonge, \u00e9loignement silencieux. Nos praticiens accompagnent les individus et les couples \u2014 pour renouer avec ce qui compte vraiment.",
      cta: "En parler",
      href: "/rendez-vous",
    },
  ],
  equilibre: [
    {
      badge: "Alimentation\u00a0& corps",
      title: "Votre rapport \u00e0 la nourriture et \u00e0 votre corps",
      body: "Restriction, compulsion, honte, relation perturb\u00e9e aux aliments. Ce que vous mangez \u2014 ou refusez de manger \u2014 parle souvent d\u2019autre chose. Retrouver un rapport apais\u00e9 \u00e0 la nourriture et \u00e0 son corps, c\u2019est possible.",
      cta: "En parler",
      href: "/rendez-vous",
    },
    {
      badge: "Rythme\u00a0& sens",
      title: "Se retrouver quand tout s\u2019acc\u00e9l\u00e8re",
      body: "\u00c9puisement profond, surcharge cognitive, difficult\u00e9 \u00e0 dormir, perte de sens, sentiment de flotter sans ancrage. L\u2019\u00e9quilibre ne revient pas seul. Nos praticiens vous aident \u00e0 nommer ce qui cloche \u2014 et \u00e0 retrouver le fil.",
      cta: "En parler",
      href: "/rendez-vous",
    },
  ],
};

const VALEURS = [
  {
    glyph: "⊘",
    label: "Sans \u00e9tiquette ni diagnostic",
    body: "Vous n\u2019avez pas besoin d\u2019un dossier m\u00e9dical ou d\u2019un diagnostic pour \u00eatre entendu. Ce qui vous p\u00e8se suffit pour commencer.",
  },
  {
    glyph: "◎",
    label: "Avec ou sans le r\u00e9seau de la sant\u00e9",
    body: "Nos praticiens travaillent en compl\u00e9ment \u2014 ou enti\u00e8rement en dehors \u2014 du syst\u00e8me de sant\u00e9 traditionnel. Vous choisissez votre parcours.",
  },
  {
    glyph: "◇",
    label: "Depuis les racines, si vous le souhaitez",
    body: "Enfance, parents, h\u00e9ritage transg\u00e9n\u00e9rationnel. Si vous voulez aller au fond des choses, vos praticiens vous y accompagnent.",
  },
  {
    glyph: "◻",
    label: "Des praticiens form\u00e9s",
    body: "Form\u00e9s \u00e0 l\u2019\u00e9coute profonde et non-directive. Au Qu\u00e9bec. Disponibles sans d\u00e9lai. Confidentialit\u00e9 stricte.",
  },
];

export default function HomePage() {
  const [activeTab, setActiveTab] = useState("dependances");

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
                Prendre soin &mdash; <em>&Agrave;&nbsp;son rythme.</em>
              </h1>
              <p className="v3-hero__lede v3-hero__lede--eq">
                Une &eacute;coute authentique et personnalis&eacute;e &mdash;<br />
                Retrouvez &eacute;quilibre et v&eacute;rit&eacute;
              </p>
              <div className="v3-hero__cta-row">
                <Link href="/rendez-vous" className="v3-btn v3-btn--ink">
                  Prendre rendez-vous
                  <span className="v3-btn__arrow" aria-hidden="true">&rarr;</span>
                </Link>
                <Link href="#comment-ca-fonctionne" className="v3-btn v3-btn--ghost">
                  Comment &ccedil;a fonctionne
                </Link>
              </div>
              <p className="v3-hero__trinity">
                IVIA est une plateforme d&apos;&eacute;coute et de compr&eacute;hension ind&eacute;pendante et sans parti pris. Venez tel que vous &ecirc;tes.
              </p>
            </div>

            <div className="v3-hero__brand-mark" aria-hidden="true">
              <MesangeMark size={112} bare ariaLabel="" className="v3-hero__brand-mark-bird" />
            </div>
          </section>

          {/* ── PROOF BAR — 3 colonnes engagements ────────────────── */}
          <section id="comment-ca-fonctionne" className="v3-proof-bar" aria-label="Nos engagements">
            <div className="v3-proof-bar__inner">
              <div className="v3-proof-bar__stat">
                <strong>Aucune attente</strong>
                <span>D&egrave;s aujourd&apos;hui, partout au Qu&eacute;bec</span>
              </div>
              <div className="v3-proof-bar__sep" aria-hidden="true" />
              <div className="v3-proof-bar__stat">
                <strong>Aucun diagnostic</strong>
                <span>On vous &eacute;coute &amp; vous accompagne</span>
              </div>
              <div className="v3-proof-bar__sep" aria-hidden="true" />
              <div className="v3-proof-bar__stat">
                <strong>Devenir membre</strong>
                <span>Ouvrez un compte et prenez rendez-vous</span>
              </div>
            </div>
          </section>

          {/* ── COMMENT ÇA FONCTIONNE — 3 étapes ──────────────── */}
          <section className="v3-section" aria-labelledby="how-title" style={{ background: "#fff", borderTop: "1px solid #e8e4df", borderBottom: "1px solid #e8e4df" }}>
            <div className="v3-section__inner" style={{ maxWidth: "760px" }}>
              <p className="v3-kicker">D&eacute;couvrir IVIA-M&Eacute;SAGES</p>
              <h2 id="how-title" className="v3-h2 v3-h2--center" style={{ marginBottom: "3rem", color: "#0d0d08", fontWeight: 800, letterSpacing: "-0.02em" }}>
                L&apos;unique plate-forme d&apos;&eacute;coute
              </h2>
              <ol style={{ listStyle: "none", padding: 0, margin: 0, display: "flex", flexDirection: "column", gap: "2.5rem" }}>
                <li style={{ display: "flex", gap: "1.5rem", alignItems: "flex-start" }}>
                  <span style={{ display: "flex", alignItems: "center", justifyContent: "center", width: "2.5rem", height: "2.5rem", minWidth: "2.5rem", borderRadius: "50%", background: "#3d6b4f", color: "#ffffff", fontWeight: 700, fontSize: "1rem" }}>1</span>
                  <div>
                    <h3 style={{ fontSize: "1.0625rem", fontWeight: 600, marginBottom: "0.5rem", color: "#0d0d08" }}>Votre espace personnalis&eacute;</h3>
                    <p style={{ color: "#2a2a1e", lineHeight: 1.7, margin: 0 }}>D&egrave;s aujourd&apos;hui. &Agrave; votre rythme &mdash; D&eacute;finissez votre parcours et la voie du bien-&ecirc;tre qui vous ressemble.</p>
                  </div>
                </li>
                <li style={{ display: "flex", gap: "1.5rem", alignItems: "flex-start" }}>
                  <span style={{ display: "flex", alignItems: "center", justifyContent: "center", width: "2.5rem", height: "2.5rem", minWidth: "2.5rem", borderRadius: "50%", background: "#3d6b4f", color: "#ffffff", fontWeight: 700, fontSize: "1rem" }}>2</span>
                  <div>
                    <h3 style={{ fontSize: "1.0625rem", fontWeight: 600, marginBottom: "0.5rem", color: "#0d0d08" }}>D&eacute;crivez-vous</h3>
                    <p style={{ color: "#2a2a1e", lineHeight: 1.7, margin: 0 }}>En quelques minutes, sans dossier m&eacute;dical ni diagnostic. Juste votre histoire et vos besoins.</p>
                  </div>
                </li>
                <li style={{ display: "flex", gap: "1.5rem", alignItems: "flex-start" }}>
                  <span style={{ display: "flex", alignItems: "center", justifyContent: "center", width: "2.5rem", height: "2.5rem", minWidth: "2.5rem", borderRadius: "50%", background: "#3d6b4f", color: "#ffffff", fontWeight: 700, fontSize: "1rem" }}>3</span>
                  <div>
                    <h3 style={{ fontSize: "1.0625rem", fontWeight: 600, marginBottom: "0.5rem", color: "#0d0d08" }}>Enfin votre parcours personnel</h3>
                    <p style={{ color: "#2a2a1e", lineHeight: 1.7, margin: 0 }}>Dans votre espace vous pourrez tout dire et comprendre. Profitez de votre journal pour d&eacute;poser vos pens&eacute;es du moment. Elles favoriseront l&apos;analyse de votre situation et acc&eacute;l&eacute;reront la compr&eacute;hension de vos &eacute;tats &eacute;motionnels et physiologiques. Que la reg&eacute;n&eacute;ration commence.</p>
                  </div>
                </li>
              </ol>
              <div style={{ textAlign: "center", marginTop: "3rem" }}>
                <Link href="/rendez-vous" className="v3-btn v3-btn--ink" style={{ fontSize: "1.0625rem", padding: "0.875rem 2rem", fontWeight: 700, outline: "1px solid currentColor", outlineOffset: "3px" }}>
                  Commencer ma d&eacute;marche
                  <span className="v3-btn__arrow" aria-hidden="true">&rarr;</span>
                </Link>
              </div>
            </div>
          </section>

          {/* ── CE QUI VOUS AMÈNE ICI — onglets + cartes ─────────── */}
          <section className="v3-section v3-services" id="services" aria-labelledby="services-title">
            <div className="v3-section__inner">
              <p className="v3-kicker">Ce qui vous am&egrave;ne ici</p>
              <h2 id="services-title" className="v3-h2 v3-h2--center">
                Des r&eacute;ponses pour ce qui vous touche <em>vraiment.</em>
              </h2>

              <div className="v3-services__tabs" role="tablist" aria-label="Th&egrave;mes">
                {TABS.map(tab => (
                  <button
                    key={tab.id}
                    role="tab"
                    aria-selected={activeTab === tab.id}
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
                      {card.ctaSecondaire && card.hrefSecondaire && (
                        <Link href={card.hrefSecondaire} className="v3-btn v3-btn--ghost v3-btn--sm">
                          {card.ctaSecondaire}
                        </Link>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </section>

          {/* ── NOTRE APPROCHE — 4 blocs ──────────────────────────── */}
          <section className="v3-section v3-valeurs-cles" aria-labelledby="valeurs-title">
            <div className="v3-section__inner">
              <h2 id="valeurs-title" className="v3-h2 v3-h2--center v3-valeurs-cles__heading">
                Une approche qui vous respecte &mdash; <em>&agrave; votre mesure.</em>
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

          {/* ── ALLER EN PROFONDEUR — si on le souhaite ──────────── */}
          <section className="v3-section v3-pathways" id="en-profondeur" aria-labelledby="profondeur-title">
            <div className="v3-section__inner">
              <p className="v3-kicker">Aller plus loin</p>
              <h2 id="profondeur-title" className="v3-h2 v3-h2--center">
                Red&eacute;finir son existence &mdash; <em>si on le souhaite.</em>
              </h2>
              <p className="v3-section__intro">
                Il y a des choses que l&apos;on tra&icirc;ne depuis longtemps. Des sch&eacute;mas qui se r&eacute;p&egrave;tent sans qu&apos;on sache pourquoi. Des r&eacute;actions qui d&eacute;passent la situation. Nos praticiens peuvent vous accompagner aussi loin que vous le souhaitez &mdash; y compris dans les couches les plus profondes de votre histoire.
              </p>
              <ul className="v3-pathways__grid" aria-label="&Eacute;tapes d&apos;exploration">
                <li className="v3-pathway v3-pathway--ink">
                  <div className="v3-pathway__inner">
                    <span className="v3-pathway__kicker">Les origines</span>
                    <h3 className="v3-pathway__title">Depuis votre naissance</h3>
                    <p className="v3-pathway__body">L&apos;histoire de votre arriv&eacute;e au monde, les conditions dans lesquelles vous avez grandi, les mod&egrave;les int&eacute;gr&eacute;s avant m&ecirc;me que vous puissiez les choisir. Tout commence l&agrave;.</p>
                  </div>
                </li>
                <li className="v3-pathway v3-pathway--sage">
                  <div className="v3-pathway__inner">
                    <span className="v3-pathway__kicker">Les liens fondateurs</span>
                    <h3 className="v3-pathway__title">Vos parents, votre h&eacute;ritage</h3>
                    <p className="v3-pathway__body">La nature du lien &agrave; votre m&egrave;re, &agrave; votre p&egrave;re. Ce qu&apos;ils vous ont transmis &mdash; voulu ou non. Les deuils jamais faits, les amours jamais exprim&eacute;s. Ces dynamiques vivent encore en vous, aujourd&apos;hui.</p>
                  </div>
                </li>
                <li className="v3-pathway v3-pathway--cream">
                  <div className="v3-pathway__inner">
                    <span className="v3-pathway__kicker">La m&eacute;moire des g&eacute;n&eacute;rations</span>
                    <h3 className="v3-pathway__title">Vos anc&ecirc;tres, si n&eacute;cessaire</h3>
                    <p className="v3-pathway__body">Certaines blessures traversent les g&eacute;n&eacute;rations. Deuils non r&eacute;solus, traumatismes tu&eacute;s, secrets de famille. Les reconna&icirc;tre &mdash; pas pour les porter, mais pour s&apos;en lib&eacute;rer.</p>
                  </div>
                </li>
                <li className="v3-pathway v3-pathway--ink">
                  <div className="v3-pathway__inner">
                    <span className="v3-pathway__kicker">Votre r&eacute;alit&eacute; d&apos;aujourd&apos;hui</span>
                    <h3 className="v3-pathway__title">Se positionner, s&apos;&eacute;panouir</h3>
                    <p className="v3-pathway__body">Tout ce travail vise un seul objectif&nbsp;: vous positionner clairement dans votre vie actuelle, et d&eacute;gager les voies d&apos;un &eacute;panouissement r&eacute;el et durable &mdash; avec ou sans le r&eacute;seau de la sant&eacute;.</p>
                  </div>
                </li>
              </ul>
            </div>
          </section>

        </main>
      </div>
    </PublicLayout>
  );
}

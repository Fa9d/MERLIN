"use client";
import Link from "next/link";
import "./styles.css";
import "./styles.v3.css";
import { PublicLayout } from "@/components/layout/PublicLayout";
import { MesangeMark } from "@/components/MesangeMark";

/* ──────────────────────────────────────────────────────────────────────────
   IVIA — Refonte stratégique (branche refonte-ivia-site-unifie)
   Concept : La maison du vivant.
   Doctrine : IVIA accueille · MERLIN structure · MÉSANGES accompagne.
   Posture : non médicale, québécoise, sous consentement, sans diagnostic.
   Source de copy : ivia_textes_accueil_fusion_v1.md (approuvée).
   ────────────────────────────────────────────────────────────────────────── */

/* Quatre portes publiques — pas de tarification, pas de promesse de soin. */
const PATHWAYS = [
  {
    id: "pour-moi",
    kicker: "Pour moi",
    title: "Déposer ce que je vis",
    body:
      "Je veux mieux comprendre ce qui m’arrive, ce qui se répète et ce qui pourrait m’aider à retrouver une voie d’équilibre.",
    href: "/demarche",
    cta: "Commencer mon espace privé",
    tone: "ink",
  },
  {
    id: "pour-une-collectivite",
    kicker: "Pour une collectivité",
    title: "Explorer · Analyser · Relier",
    body:
      "Nous sommes une famille, une communauté, un organisme ou un groupe humain, et quelque chose demande à être nommé.",
    href: "#collectivites-vivantes",
    cta: "Ouvrir un espace commun",
    tone: "argile",
  },
  {
    id: "pour-praticiens",
    kicker: "Pour les praticiens",
    title: "Structurer ma pratique",
    body:
      "Je veux intégrer une approche différente de préparation, d’interprétation et d’amélioration continue, sans perdre ma posture ni mon jugement.",
    href: "/espace-praticien",
    cta: "Découvrir l’espace praticien",
    tone: "sage",
  },
  {
    id: "comprendre-ivia",
    kicker: "Comprendre IVIA",
    title: "Lire l’approche",
    body:
      "Je veux comprendre la maison du vivant, IVIA, MERLIN, MÉSANGES et le positionnement de cette démarche.",
    href: "#approche",
    cta: "Lire l’approche",
    tone: "cream",
  },
] as const;

/* Neuf dimensions observées — territoire en premier axe. */
const DIMENSIONS = [
  {
    label: "Territoire & terrain vivant",
    body:
      "La terre, les lieux, les saisons, les paysages, les communautés et l’appartenance. Ce qui nous porte avant même que nous sachions le nommer.",
  },
  {
    label: "Corps & métabolisme",
    body:
      "Signaux somatiques, énergie, inflammation, sommeil, rythme circadien, digestion et capacité du corps à retrouver un mouvement plus juste.",
  },
  {
    label: "Émotions & états intérieurs",
    body:
      "Ce qui traverse, ce qui appuie, ce qui déborde ou ce qui demande à être nommé sans être réduit à une étiquette.",
  },
  {
    label: "Relations & famille",
    body:
      "Liens proches, tensions, transmissions, rôles, silences et ce qui circule entre les êtres.",
  },
  {
    label: "Temporalité & répétitions",
    body:
      "Ce qui revient, les cycles, les boucles, les angles morts et les moments où l’histoire semble se répéter.",
  },
  {
    label: "Alimentation, sommeil & rythmes",
    body:
      "Le quotidien comme terrain vivant : gestes, habitudes, repos, repas, mouvements, excès, manques et équilibres physiologiques.",
  },
  {
    label: "Héritages & transgénérationnel",
    body:
      "Mémoires familiales, traces de l’histoire, savoirs ancestraux, loyautés, blessures et transmissions parfois inscrites sans mots.",
  },
  {
    label: "Pression sociale & culturelle",
    body:
      "Attentes, normes, injonctions, isolement, performance, précarité, appartenance et ce qui pèse parfois sans être nommé.",
  },
  {
    label: "Autonomie, échange & action",
    body:
      "Ce qui peut se remettre en mouvement lorsque la personne retrouve un rapport plus juste à elle-même, aux autres, au territoire et au vivant.",
  },
];

/* Six pas — comment IVIA accueille et accompagne, au rythme du vivant. */
const ACCOMPAGNEMENT = [
  {
    num: "01",
    label: "Vous déposez",
    body:
      "Dans vos mots, avec votre histoire, votre situation, vos questions et ce que vous êtes prêt à nommer.",
  },
  {
    num: "02",
    label: "MERLIN structure",
    body:
      "MERLIN met en ordre les éléments transmis, repère les liens possibles et prépare une lecture structurée, toujours sous validation humaine.",
  },
  {
    num: "03",
    label: "Nous ouvrons une lecture",
    body:
      "Une lecture sensible et multidimensionnelle, sans diagnostic, pour faire apparaître des pistes de compréhension, de clarification et d’orientation.",
  },
  {
    num: "04",
    label: "MÉSANGES accompagne",
    body:
      "Les mésanges ne quittent pas le Québec lorsque vient l’hiver. Elles restent, traversent le froid et rappellent qu’une présence demeure possible. MÉSANGES accompagne ainsi par petites touches : une question, une nuance, une piste.",
  },
  {
    num: "05",
    label: "Vous agissez",
    body:
      "Le simple fait de déposer ce que vous vivez peut devenir un premier acte de clarté. IVIA soutient ce mouvement sans décider à votre place.",
  },
  {
    num: "06",
    label: "Nous suivons l’évolution",
    body:
      "Ensemble, grâce aux outils proposés, nous observons ce qui change, ce qui résiste, ce qui revient et ce qui demande une attention nouvelle.",
  },
];

/* Architecture trinitaire — trois noms, une seule attention. */
const ARCHITECTURE = [
  {
    name: "IVIA",
    role: "accueille",
    body:
      "IVIA est le seuil, la maison commune et le concept. IVIA signifie In Vivo In Actu : Au sein de l’être, en actes.",
  },
  {
    name: "MERLIN",
    role: "structure",
    body:
      "MERLIN est l’infrastructure interne : écoute, analyse, classification, mise en relation et structuration, sous validation humaine.",
  },
  {
    name: "MÉSANGES",
    role: "accompagne",
    body:
      "MÉSANGES accompagne par la voix, les nuances, les pistes et les petites orientations qui aident à reprendre direction.",
  },
];

/* Collectivités vivantes — clarifier, sans imposer une lecture unique. */
const COLLECTIF_PROMISES = [
  "Cartographier les tensions, mais aussi ce qui est sain, vivant et déjà présent.",
  "Identifier les difficultés, les craintes, les répétitions et les angles morts.",
  "Soutenir une action commune, réaliste et partagée, sans imposer une lecture unique.",
  "Ouvrir des pistes d’action plutôt que prescrire une direction.",
];

const COLLECTIF_PUBLICS = [
  "Familles",
  "Organismes communautaires",
  "Communautés territoriales",
  "Groupes de praticiens",
  "Équipes de terrain",
  "Milieux humains en transition",
];

/* Espace praticien — valeur concrète, posture éthique. */
const PRATICIEN_VALUE = [
  {
    label: "Interprétation structurée",
    body:
      "Une lecture sensible des séances, de ce qui revient, de ce qui se transforme et de ce qui demande à être ouvert avec prudence.",
  },
  {
    label: "Préparation des rencontres",
    body:
      "Un fil clair entre les séances, sans grille rigide. Un cadre qui sert l’écoute, la mémoire, la préparation et la continuité.",
  },
  {
    label: "Compétences & limites déclarées",
    body:
      "Diplômé·e, en formation, hors ordre ou issu·e d’une pratique complémentaire : chaque statut est nommé, cadré et jamais effacé.",
  },
  {
    label: "Boucle de feedback éthique",
    body:
      "Vos interprétations nourrissent votre pratique. IVIA propose un miroir structuré pour enrichir votre préparation, votre interprétation et votre suivi.",
  },
];

/* Souveraineté & prudence — sans jargon, sans corporate. */
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
      "Pas de pixels tiers, pas de branchement externe imposé. Les connecteurs sont pensés comme internes, privés et consentis.",
  },
  {
    glyph: "⚕",
    title: "Posture non médicale",
    body:
      "IVIA n’est pas une clinique. Nous ne diagnostiquons pas et nous ne prescrivons rien.",
  },
];

/* ── Composant ────────────────────────────────────────────────────────────── */
export default function HomePage() {
  return (
    <PublicLayout>
      <div className="hp hp--v3 hp--maison">
        <main>
          {/* ── HERO — La maison du vivant ─────────────────────────────── */}
          <section className="v3-hero v3-hero--maison">
            <div className="v3-hero__bg" aria-hidden="true">
              <span className="v3-hero__glow v3-hero__glow--a" />
              <span className="v3-hero__glow v3-hero__glow--b" />
              <span className="v3-hero__grain" />
            </div>

            <div className="v3-hero__inner v3-hero__inner--maison">
              <p className="v3-eyebrow">
                <span className="v3-eyebrow__dot" aria-hidden="true" />
                IVIA · In Vivo In Actu · Au sein de l’être, en actes
              </p>

              <h1 className="v3-hero__h1 v3-hero__h1--maison">
                La maison <em>du vivant.</em>
              </h1>

              <p className="v3-hero__lede v3-hero__lede--maison">
                Le corps d’un côté, l’esprit de l’autre. La famille ici, la
                société là. IVIA propose un espace pour{" "}
                <strong>déposer</strong>, <strong>comprendre</strong> et{" "}
                <strong>remettre en relation</strong> ce que la vie tient
                ensemble.
              </p>

              <div className="v3-hero__mesange-wrap">
                <MesangeMark
                  size={120}
                  withSong
                  ariaLabel="Mésange — symbole d’accueil IVIA"
                />
                <p className="v3-hero__mesange-caption">
                  <strong>IVIA</strong> accueille ·{" "}
                  <strong>MERLIN</strong> structure ·{" "}
                  <strong>MÉSANGES</strong> accompagne
                </p>
              </div>

              <ul className="v3-signals" aria-label="Repères IVIA">
                <li>Pensé au Québec, à partir du Québec</li>
                <li aria-hidden="true">·</li>
                <li>Sans diagnostic</li>
                <li aria-hidden="true">·</li>
                <li>À votre rythme</li>
                <li aria-hidden="true">·</li>
                <li>Sous consentement</li>
              </ul>
            </div>
          </section>

          {/* ── QUATRE PORTES ──────────────────────────────────────────── */}
          <section className="v3-section v3-pathways" id="voies">
            <div className="v3-section__inner">
              <p className="v3-kicker">Choisir votre porte</p>
              <h2 className="v3-h2 v3-h2--center">
                Quatre portes, <em>une même maison.</em>
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

          {/* ── LA MAISON DU VIVANT — section concept ──────────────────── */}
          <section className="v3-section v3-maison" id="maison">
            <div className="v3-section__inner v3-maison__inner">
              <div className="v3-maison__copy">
                <p className="v3-kicker">La maison du vivant</p>
                <h2 className="v3-h2">
                  Commencer par <em>le territoire.</em>
                </h2>
                <p className="v3-section__intro">
                  La maison du vivant commence par le territoire : la terre
                  qui nous porte, les lieux qui nous constituent, les saisons,
                  les paysages, les appartenances et les mémoires qui nous
                  traversent.
                </p>
                <p className="v3-maison__paragraph">
                  Elle vit aussi dans le corps, la voix, la famille, les
                  liens, les émotions, les relations, les gestes quotidiens
                  et ce qui demande à retrouver une place plus juste.
                </p>
                <p className="v3-maison__paragraph">
                  IVIA est un seuil pour entrer dans cette maison. On y
                  dépose ce que l’on porte. On tente de comprendre ce qui
                  arrive. On remet en relation ce qui a été séparé, figé ou
                  rendu difficile à nommer. Nous croyons qu’il est possible
                  d’apprendre, de comprendre et d’agir, à partir de ce qui
                  est vivant, réel et présent.
                </p>
              </div>
              <aside className="v3-maison__visual" aria-hidden="true">
                <div className="v3-maison__rings">
                  <span className="v3-maison__ring v3-maison__ring--1" />
                  <span className="v3-maison__ring v3-maison__ring--2" />
                  <span className="v3-maison__ring v3-maison__ring--3" />
                  <span className="v3-maison__core" />
                </div>
                <ul className="v3-maison__labels">
                  <li>territoire</li>
                  <li>corps</li>
                  <li>liens</li>
                  <li>mémoire</li>
                  <li>société</li>
                  <li>gestes</li>
                </ul>
              </aside>
            </div>
          </section>

          {/* ── CE QUE NOUS OBSERVONS — neuf dimensions ───────────────── */}
          <section className="v3-section v3-dimensions" id="dimensions">
            <div className="v3-section__inner">
              <p className="v3-kicker">Ce que nous observons</p>
              <h2 className="v3-h2">
                Neuf dimensions, <em>une seule lecture.</em>
              </h2>
              <p className="v3-section__intro">
                IVIA ne sépare pas ce que la vie tient ensemble. Voici les
                couches que la maison du vivant abrite, sans grille rigide,
                sans étiquette clinique et sans hiérarchie fermée.
              </p>
              <ul className="v3-dimensions__grid">
                {DIMENSIONS.map((d, i) => (
                  <li key={d.label} className="v3-dimension">
                    <span className="v3-dimension__num">
                      {String(i + 1).padStart(2, "0")}
                    </span>
                    <h3 className="v3-dimension__label">{d.label}</h3>
                    <p className="v3-dimension__body">{d.body}</p>
                  </li>
                ))}
              </ul>
            </div>
          </section>

          {/* ── COMMENT IVIA VOUS ACCOMPAGNE — six pas ───────────────── */}
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

          {/* ── COLLECTIVITÉS VIVANTES ──────────────────────────────────── */}
          <section
            className="v3-section v3-collectivites"
            id="collectivites-vivantes"
          >
            <div className="v3-section__inner v3-collectivites__inner">
              <header className="v3-collectivites__head">
                <p className="v3-kicker">Collectivités vivantes</p>
                <h2 className="v3-h2">
                  Pour les familles, organismes, communautés{" "}
                  <em>et lieux de vie.</em>
                </h2>
                <p className="v3-section__intro">
                  Un collectif n’est pas une entreprise à optimiser. C’est un
                  milieu vivant, avec ses tensions, ses difficultés, ses
                  contraintes, ses ressources et ses façons propres de tenir
                  ensemble. IVIA aide à nommer ce qui circule, à clarifier ce
                  qui pèse et à soutenir un repositionnement plus sain, plus
                  lisible et plus favorable à l’épanouissement de chacun.
                </p>
                <ul className="v3-publics" aria-label="Milieux concernés">
                  {COLLECTIF_PUBLICS.map((pub) => (
                    <li key={pub}>{pub}</li>
                  ))}
                </ul>
              </header>

              <ul className="v3-promises">
                {COLLECTIF_PROMISES.map((p) => (
                  <li key={p} className="v3-promise">
                    <span className="v3-promise__bullet" aria-hidden="true" />
                    <p>{p}</p>
                  </li>
                ))}
              </ul>

              <p className="v3-collectivites__not">
                <strong>Ce que ce n’est pas :</strong> IVIA Collectivités
                vivantes ne remplace pas une thérapie familiale, une
                médiation juridique, une intervention clinique, un arbitrage
                de conflit ou une démarche d’urgence. IVIA ne pose pas de
                diagnostic collectif : IVIA aide à structurer une lecture
                commune, à clarifier les besoins et à ouvrir des pistes
                d’action.
              </p>
            </div>
          </section>

          {/* ── ESPACE PRATICIEN ───────────────────────────────────────── */}
          <section className="v3-section v3-praticien-strat">
            <div className="v3-section__inner v3-praticien-strat__inner">
              <header className="v3-praticien-strat__head">
                <p className="v3-kicker">Espace praticien</p>
                <h2 className="v3-h2">
                  Structurer l’écoute, <em>évoluer dans sa pratique.</em>
                </h2>
                <p className="v3-section__intro">
                  IVIA n’est pas un annuaire. C’est un outil
                  d’interprétation, de préparation et d’amélioration continue
                  pour les praticien·nes diplômé·es, en formation ou hors
                  ordre. La posture reste prudente, jamais prescriptive.
                  IVIA n’appartient à aucun courant de pensée. Sa fonction
                  est d’offrir une lecture claire, indépendante et
                  structurée de ce qui se dit, se répète et demande à être
                  mieux compris.
                </p>
                <div className="v3-cta-row">
                  <Link
                    href="/espace-praticien"
                    className="v3-btn v3-btn--primary"
                  >
                    Découvrir l’espace praticien
                    <span className="v3-btn__arrow" aria-hidden="true">→</span>
                  </Link>
                </div>
              </header>

              <ul className="v3-prat-value">
                {PRATICIEN_VALUE.map((b, i) => (
                  <li key={b.label} className="v3-prat-value__card">
                    <span className="v3-prat-value__num">
                      {String(i + 1).padStart(2, "0")}
                    </span>
                    <h3 className="v3-prat-value__label">{b.label}</h3>
                    <p className="v3-prat-value__body">{b.body}</p>
                  </li>
                ))}
              </ul>

              <p className="v3-collectivites__not">
                IVIA ne remplace pas la supervision, la formation continue,
                la consultation entre pairs ni le jugement professionnel.
                Vous restez maître à bord, mais vous n’êtes pas laissé seul
                devant la complexité.
              </p>
            </div>
          </section>

          {/* ── ARCHITECTURE ──────────────────────────────────────────── */}
          <section className="v3-section v3-arch" id="architecture">
            <div className="v3-section__inner">
              <p className="v3-kicker">L’architecture</p>
              <h2 className="v3-h2">
                Trois noms, <em>une seule attention.</em>
              </h2>
              <p className="v3-section__intro">
                IVIA n’est pas un produit isolé. C’est ce que vous voyez
                d’un ensemble plus large, pensé au Québec, sous validation
                humaine, avec une maison commune appelée{" "}
                <strong>ivia.quebec</strong>.
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
              <p className="v3-section__intro">
                Ce que nous cherchons : autonomie, équilibre, relation plus
                juste au vivant.
              </p>
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

          {/* ── VOIX DU FONDATEUR (vidéo) ───────────────────────────────── */}
          <section className="v3-section v3-voice">
            <div className="v3-section__inner v3-voice__inner">
              <div className="v3-voice__copy">
                <p className="v3-kicker">La voix du fondateur</p>
                <h2 className="v3-h2">
                  Une trace vocale, <em>plutôt qu’un slogan.</em>
                </h2>
                <p className="v3-section__intro">
                  Je m’appelle David. Laissez-moi vous expliquer ce qu’IVIA
                  cherche à faire, et ce qu’IVIA refuse de faire. Sans
                  jargon, sans promesse de soin, je vous accueille dans
                  cette démarche : comprendre ce qui agit, respecter ce qui
                  est vivant et ouvrir une voie plus claire vers
                  l’autonomie, l’équilibre et l’action.
                </p>
                <p className="v3-voice__hint">
                  Audio + vidéo · sous-titres à venir · 1 min 48
                </p>
              </div>
              <figure className="v3-voice__media">
                <div className="v3-voice__frame">
                  <span className="v3-voice__tag" aria-hidden="true">
                    <span className="v3-voice__tag-dot" />
                    Trace vocale · 01
                  </span>
                  <video
                    className="v3-voice__video"
                    src="/assets/video/ivia_accueil_trace_vocale_v2.mp4"
                    controls
                    preload="metadata"
                    playsInline
                    aria-label="Trace vocale d’introduction d’IVIA par David Phaneuf"
                  >
                    <p>
                      Trace vocale d’introduction d’IVIA — votre navigateur
                      ne supporte pas la lecture vidéo HTML5.
                    </p>
                  </video>
                </div>
                <figcaption>David Phaneuf · fondateur · Montréal</figcaption>
              </figure>
            </div>
          </section>

          {/* ── DISCLAIMER — Posture non médicale + urgence 988 ────────── */}
          <section
            className="v3-disclaimer"
            aria-label="Avertissement non médical et urgence"
          >
            <div className="v3-section__inner">
              <p>
                <strong>IVIA n’est pas une clinique.</strong> Nous ne
                diagnostiquons pas et nous ne prescrivons rien. IVIA ne
                remplace pas un·e professionnel·le de la santé.
              </p>
              <p>
                <strong>Situation d’urgence.</strong> IVIA n’est pas un
                service d’urgence. Si vous êtes en danger immédiat, si vous
                craignez de poser un geste contre vous-même ou contre
                quelqu’un d’autre, appelez les services d’urgence de votre
                région. Au Canada, vous pouvez aussi appeler ou texter le{" "}
                <strong>988</strong> pour obtenir du soutien en cas de crise
                suicidaire.
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
                <strong>IVIA</strong> accueille.
                <br />
                <strong>MERLIN</strong> structure.
                <br />
                <em>MÉSANGES accompagne.</em>
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

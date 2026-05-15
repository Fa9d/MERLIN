"use client";
import Link from "next/link";
import "./styles.css";
import "./styles.v3.css";
import { PublicLayout } from "@/components/layout/PublicLayout";
import { MesangeMark } from "@/components/MesangeMark";

/* ──────────────────────────────────────────────────────────────────────────
   IVIA — Refonte stratégique (branche refonte-ivia-site-unifie)
   Concept : La maison du vivant. Pas un lieu — le vivant lui-même.
   Architecture : IVIA accueille · MERLIN structure · MÉSANGES accompagne.
   Posture : non médicale, québécoise, sous consentement, sans diagnostic.
   ────────────────────────────────────────────────────────────────────────── */

/* Quatre voies publiques — pas de tarification, pas de promesse de soin. */
const PATHWAYS = [
  {
    id: "pour-moi",
    kicker: "Pour moi",
    title: "Déposer ce que je vis",
    body:
      "Je veux déposer ce que je vis, comprendre ce qui se répète et retrouver une voie d’équilibre.",
    href: "/demarche",
    cta: "Commencer mon espace privé",
    tone: "ink",
  },
  {
    id: "pour-mon-collectif",
    kicker: "Pour mon collectif",
    title: "Explorer Collectivités vivantes",
    body:
      "Nous sommes une famille, une communauté, un organisme ou un groupe humain — et quelque chose demande à être nommé.",
    href: "#collectivites-vivantes",
    cta: "Explorer Collectivités vivantes",
    tone: "argile",
  },
  {
    id: "pour-praticiens",
    kicker: "Pour les praticiens",
    title: "Découvrir l’espace praticien",
    body:
      "Je veux intégrer une approche d’interprétation, de suivi et d’amélioration continue de ma pratique.",
    href: "/espace-praticien",
    cta: "Découvrir l’espace praticien",
    tone: "sage",
  },
  {
    id: "comprendre-ivia",
    kicker: "Comprendre IVIA",
    title: "Lire l’approche",
    body:
      "Je veux comprendre la maison du vivant, MERLIN, MÉSANGES, les données au Québec et la posture non médicale.",
    href: "#approche",
    cta: "Lire l’approche",
    tone: "cream",
  },
] as const;

/* Dimensions observées — ce que la maison du vivant abrite réellement. */
const DIMENSIONS = [
  {
    label: "Corps & métabolisme",
    body: "Signaux somatiques, énergie, inflammation, sommeil, rythme circadien.",
  },
  {
    label: "Émotions & états intérieurs",
    body: "Ce qui traverse, ce qui appuie, ce qui veut être nommé sans étiquette.",
  },
  {
    label: "Relations & famille",
    body: "Liens proches, tensions, transmissions, ce qui circule entre les êtres.",
  },
  {
    label: "Temporalité & répétitions",
    body: "Ce qui revient, les cycles, les boucles, les angles morts récurrents.",
  },
  {
    label: "Alimentation, sommeil, inflammation",
    body: "Le quotidien comme terrain — gestes, rythmes, équilibres physiologiques.",
  },
  {
    label: "Héritages & transgénérationnel",
    body: "Mémoires familiales, savoirs ancestraux, ce qui se transmet sans mot.",
  },
  {
    label: "Pression sociale & culturelle",
    body: "Attentes, normes, injonctions, ce qui pèse sans qu’on le voie.",
  },
  {
    label: "Territoire & appartenance",
    body: "Lieu, paysage, communauté, racines québécoises et liens au vivant.",
  },
  {
    label: "Autonomie & action",
    body: "Marges de manœuvre, gestes possibles, ce qui peut se remettre en mouvement.",
  },
];

/* Six pas — comment la maison accueille et accompagne, sans révéler le système. */
const ACCOMPAGNEMENT = [
  {
    num: "01",
    label: "Vous déposez",
    body: "À votre rythme, dans vos mots. Choix doux + espace libre.",
  },
  {
    num: "02",
    label: "MERLIN structure",
    body: "Une mise en forme interne, traçable, sous validation humaine.",
  },
  {
    num: "03",
    label: "Nous interprétons",
    body: "Une lecture sensible, multi-dimensionnelle, jamais diagnostique.",
  },
  {
    num: "04",
    label: "Nous orientons",
    body: "Si vous le souhaitez, vers la modalité ou la personne juste.",
  },
  {
    num: "05",
    label: "Vous agissez",
    body: "Des gestes proportionnés à ce que vous traversez, à votre tempo.",
  },
  {
    num: "06",
    label: "Nous suivons l’évolution",
    body: "Ce qui se déplace, ce qui se stabilise, ce qui demande à être rouvert.",
  },
];

/* Architecture trinitaire — trois noms, une seule attention. */
const ARCHITECTURE = [
  {
    name: "IVIA",
    role: "accueille",
    body:
      "La maison commune, le seuil public — le champ partagé où vous arrivez et déposez ce que vous portez, sans tri ni diagnostic.",
  },
  {
    name: "MERLIN",
    role: "structure",
    body:
      "L’infrastructure interne — classifier, interpréter, tracer, garder la mémoire. Sous validation humaine.",
  },
  {
    name: "MÉSANGES",
    role: "accompagne",
    body:
      "Les voix subtiles d’accompagnement — orientation, résonance, présence discrète à travers les sujets qui vous touchent.",
  },
];

/* Promesses pour les collectifs — pas de performance corporative. */
const COLLECTIF_PROMISES = [
  "Clarifier ce qui circule entre les êtres.",
  "Cartographier les tensions et les zones de soin.",
  "Identifier les répétitions, les angles morts, les ressources.",
  "Soutenir une action commune, à la mesure du collectif.",
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
    body: "Une lecture sensible des séances, de ce qui revient, de ce qui demande à être rouvert.",
  },
  {
    label: "Préparation des rencontres",
    body: "Un fil clair entre séances — sans grille rigide, un cadre qui sert l’écoute.",
  },
  {
    label: "Compétences & limites déclarées",
    body: "Diplômé·e, en formation, hors-ordre : chaque statut est cadré, jamais effacé.",
  },
  {
    label: "Boucle de feedback éthique",
    body: "Vos interprétations nourrissent votre pratique. Posture prudente, jamais prescriptive.",
  },
];

/* Souveraineté — sans jargon, sans corporate. */
const SOUVERAINETE = [
  {
    glyph: "QC",
    title: "Données au Québec",
    body: "Serveurs et données sur le territoire, sous Loi 25.",
  },
  {
    glyph: "✓",
    title: "Consentement par étape",
    body: "Vous décidez, à chaque pas, ce qui peut être partagé.",
  },
  {
    glyph: "◯",
    title: "Connecteurs privés",
    body: "Pas de pixels tiers, pas de scraping externe. Internes uniquement.",
  },
  {
    glyph: "⚕",
    title: "Posture non médicale",
    body: "IVIA n’est pas une clinique. Pas de diagnostic, pas de prescription.",
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
                Nous avons appris à traiter le vivant en morceaux. Le corps
                d’un côté, l’esprit de l’autre. La famille d’un côté, la
                société de l’autre. IVIA propose un autre espace :{" "}
                <strong>déposer</strong>, <strong>comprendre</strong> et{" "}
                <strong>remettre en relation</strong> ce qui agit en nous.
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
                <li>Hébergé au Québec</li>
                <li aria-hidden="true">·</li>
                <li>Sans diagnostic</li>
                <li aria-hidden="true">·</li>
                <li>À votre rythme</li>
                <li aria-hidden="true">·</li>
                <li>Sous consentement</li>
              </ul>
            </div>
          </section>

          {/* ── QUATRE VOIES ───────────────────────────────────────────── */}
          <section className="v3-section v3-pathways" id="voies">
            <div className="v3-section__inner">
              <p className="v3-kicker">Choisir votre voie d’entrée</p>
              <h2 className="v3-h2 v3-h2--center">
                Quatre portes, <em>une même maison.</em>
              </h2>
              <ul className="v3-pathways__grid" aria-label="Voies IVIA">
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
                  Ce n’est pas un lieu. <em>C’est le vivant lui-même.</em>
                </h2>
                <p className="v3-section__intro">
                  La maison du vivant n’est pas une bâtisse. C’est ce qui
                  vit autour et en nous — le corps, la voix, la mémoire, la
                  famille, les liens, le territoire, les pressions sociales,
                  les savoirs ancestraux, les couches métaboliques,
                  émotionnelles, relationnelles.
                </p>
                <p className="v3-maison__paragraph">
                  IVIA est un seuil pour entrer dans cette maison, y déposer
                  ce qu’on porte, comprendre ce qui s’y joue, et remettre en
                  relation ce qui a été séparé. Sans promesse de soin, sans
                  diagnostic, sans jargon — au rythme du vivant.
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
                  <li>corps</li>
                  <li>liens</li>
                  <li>mémoire</li>
                  <li>territoire</li>
                  <li>société</li>
                  <li>gestes</li>
                </ul>
              </aside>
            </div>
          </section>

          {/* ── CE QUE NOUS OBSERVONS — dimensions ─────────────────────── */}
          <section className="v3-section v3-dimensions" id="dimensions">
            <div className="v3-section__inner">
              <p className="v3-kicker">Ce que nous observons</p>
              <h2 className="v3-h2">
                Neuf dimensions, <em>une seule lecture.</em>
              </h2>
              <p className="v3-section__intro">
                IVIA ne sépare pas ce que la vie tient ensemble. Voici les
                couches que la maison du vivant abrite — sans hiérarchie,
                sans grille rigide, sans étiquette clinique.
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

          {/* ── COMMENT LA MAISON ACCUEILLE ET ACCOMPAGNE — six pas ───── */}
          <section className="v3-section v3-accompagnement" id="approche">
            <div className="v3-section__inner">
              <p className="v3-kicker">Comment la maison accueille et accompagne</p>
              <h2 className="v3-h2">
                Six pas, <em>au rythme du vivant.</em>
              </h2>
              <p className="v3-section__intro">
                IVIA ne court pas. À chaque pas, vous décidez du tempo, du
                niveau de partage, et de ce qui peut être ouvert ou refermé.
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
                  Pour les familles, les organismes, <em>les milieux humains.</em>
                </h2>
                <p className="v3-section__intro">
                  Un collectif n’est pas une entreprise à optimiser. C’est un
                  milieu vivant — avec ses tensions, ses répétitions, ses
                  ressources, ses angles morts. IVIA aide à nommer ce qui
                  circule.
                </p>
                <ul className="v3-publics" aria-label="Publics accueillis">
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
                <strong>Ce que ce n’est pas :</strong> une mesure de performance,
                un substitut à la thérapie, un outil de diagnostic. IVIA
                soutient l’action commune — elle ne la prescrit pas.
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
                  IVIA n’est pas un annuaire. C’est un outil d’interprétation,
                  de préparation et d’amélioration continue — pour les
                  praticien·nes diplômé·es, en formation, ou hors-ordre. La
                  posture reste prudente, jamais prescriptive.
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
                IVIA n’est pas un produit isolé. C’est ce que vous voyez d’un
                ensemble plus large — pensé au Québec, sous validation
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
                  David Phaneuf raconte en deux minutes ce qu’IVIA cherche à
                  faire — et ce qu’IVIA refuse de faire. Sans jargon, sans
                  promesse de soin.
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

          {/* ── DISCLAIMER ──────────────────────────────────────────────── */}
          <section
            className="v3-disclaimer"
            aria-label="Avertissement non médical"
          >
            <div className="v3-section__inner">
              <p>
                <strong>IVIA n’est pas un service médical.</strong> IVIA ne
                pose pas de diagnostic, ne prescrit pas de traitement et ne
                remplace pas un·e professionnel·le de la santé. En cas de
                détresse, composez le <strong>988</strong> (ligne canadienne
                d’aide en cas de crise suicidaire) ou rendez-vous à l’urgence
                la plus proche.
              </p>
            </div>
          </section>

          {/* ── CTA FINAL ───────────────────────────────────────────────── */}
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
              <ul className="v3-final__paths" aria-label="Quatre voies">
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

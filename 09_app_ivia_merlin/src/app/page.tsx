"use client";
import Link from "next/link";
import "./styles.css";
import "./styles.v3.css";
import { PublicLayout } from "@/components/layout/PublicLayout";
import { MesangeMark } from "@/components/MesangeMark";

/* ──────────────────────────────────────────────────────────────────────────
   IVIA — Refonte V3 (branche refonte-ivia-site-unifie)
   Portail de conversion clair : Client / Praticien.
   Concept central : IVIA, In Vivo In Actu — au sein de l'être, en actes.
   Architecture : MÉSANGES accueille · MERLIN structure · IVIA accompagne.
   ────────────────────────────────────────────────────────────────────────── */

/* Voix client : ce qu'on peut déposer, écrit à la première personne. */
const CLIENT_THEMES = [
  "ce qui pèse depuis trop longtemps",
  "une transition que je n'arrive pas à nommer",
  "un doute, une fatigue, un signal du corps",
  "une relation qui demande de la clarté",
  "une intuition qu'il est temps de changer",
];

/* Sorties tangibles du parcours client. */
const CLIENT_OUTPUTS = [
  {
    label: "Mon espace privé",
    body:
      "Un endroit calme pour écrire à mon rythme. Personne d'autre que moi n'y accède sans mon accord.",
  },
  {
    label: "Ma carte IVIA",
    body:
      "Une lecture en cinq dimensions de ce que je traverse — vécu, corps, relations, lignées, sens.",
  },
  {
    label: "Une synthèse claire",
    body:
      "Un texte court, structuré, que je peux relire, retravailler ou partager à un·e praticien·ne.",
  },
  {
    label: "Une orientation",
    body:
      "Si je le souhaite, IVIA m'oriente vers un·e praticien·ne au Québec — au bon moment, pas avant.",
  },
];

/* Voix praticien·ne — bénéfices concrets, prudence sur statut. */
const PRACTITIONER_BENEFITS = [
  {
    label: "Interprétation des séances",
    body:
      "Une lecture structurée de ce qui s'est dit, ce qui revient, ce qui demande à être rouvert.",
  },
  {
    label: "Structuration des interactions",
    body:
      "Un fil clair entre rencontres, sans grille rigide — un cadre qui sert l'écoute, pas l'inverse.",
  },
  {
    label: "Évolution de la pratique",
    body:
      "Une vue d'ensemble de vos interprétations, interactions, compétences déclarées — qui évolue avec vous.",
  },
  {
    label: "Statuts accueillis",
    body:
      "Praticien·ne diplômé·e, en formation, ou hors-ordre — chaque statut est cadré, jamais effacé.",
  },
];

const ARCHITECTURE = [
  {
    name: "MÉSANGES",
    role: "accueille",
    body:
      "Le premier seuil — un espace sobre, sensible, québécois, qui reçoit ce que vous arrivez avec.",
  },
  {
    name: "MERLIN",
    role: "structure",
    body:
      "L'infrastructure interne — gouvernance, méthodes, traçabilité, sous validation humaine.",
  },
  {
    name: "IVIA",
    role: "accompagne",
    body:
      "L'expérience que vous vivez — questionnaires calmes, synthèses, orientation au bon moment.",
  },
];

const TRUST = [
  { glyph: "QC", title: "Hébergé au Québec", body: "Serveurs et données sur le territoire, sous Loi 25." },
  { glyph: "✓", title: "Consentement par étape", body: "Vous décidez, à chaque pas, ce qui peut être partagé." },
  { glyph: "◯", title: "Sans pixels tiers", body: "Aucune analyse publicitaire, aucun traceur externe." },
  { glyph: "⟲", title: "Retrait possible", body: "Vous pouvez exporter ou effacer vos traces à tout moment." },
];

/* ── Composant ────────────────────────────────────────────────────────────── */
export default function HomePage() {
  return (
    <PublicLayout>
      <div className="hp hp--v3">
        <main>
          {/* ── HERO ──────────────────────────────────────────────────────── */}
          <section className="v3-hero">
            <div className="v3-hero__bg" aria-hidden="true">
              <span className="v3-hero__glow v3-hero__glow--a" />
              <span className="v3-hero__glow v3-hero__glow--b" />
            </div>

            <div className="v3-hero__inner">
              <p className="v3-eyebrow">
                <span className="v3-eyebrow__dot" aria-hidden="true" />
                IVIA · In Vivo In Actu · Québec
              </p>

              <h1 className="v3-hero__h1">
                Au sein de l’être, <em>en actes.</em>
              </h1>

              <p className="v3-hero__lede">
                IVIA est un espace québécois d’écoute et de compréhension du
                vivant. Pas une clinique. Pas un site de soins. Un seuil pour
                déposer ce que vous portez — et, si vous le souhaitez, être
                accompagné·e vers une prochaine étape.
              </p>

              <div className="v3-hero__mesange-wrap">
                <MesangeMark
                  size={132}
                  withSong
                  ariaLabel="Mésange — symbole d’accueil IVIA"
                />
                <p className="v3-hero__mesange-caption">
                  <strong>MÉSANGES</strong> accueille ·{" "}
                  <strong>MERLIN</strong> structure ·{" "}
                  <strong>IVIA</strong> accompagne
                </p>
              </div>

              <div className="v3-paths" role="group" aria-label="Choisir votre voie d’entrée">
                <Link href="#voie-client" className="v3-path v3-path--client">
                  <span className="v3-path__kicker">Je viens déposer ce que je vis</span>
                  <span className="v3-path__title">Entrer dans mon espace privé</span>
                  <span className="v3-path__hint">Pour moi · à mon rythme · confidentiel</span>
                  <span className="v3-path__arrow" aria-hidden="true">→</span>
                </Link>
                <Link
                  href="#voie-praticien"
                  className="v3-path v3-path--praticien"
                >
                  <span className="v3-path__kicker">Je suis praticien·ne</span>
                  <span className="v3-path__title">Découvrir l’espace praticien</span>
                  <span className="v3-path__hint">
                    Diplômé·e, en formation, ou hors-ordre
                  </span>
                  <span className="v3-path__arrow" aria-hidden="true">→</span>
                </Link>
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

          {/* ── ARCHITECTURE ──────────────────────────────────────────────── */}
          <section className="v3-section v3-arch" id="architecture">
            <div className="v3-section__inner">
              <p className="v3-kicker">L’architecture</p>
              <h2 className="v3-h2">
                Trois noms, <em>une seule attention.</em>
              </h2>
              <p className="v3-section__intro">
                Pour qu’un espace d’écoute soit fiable, il faut le penser à
                trois niveaux. IVIA n’est pas un produit isolé — c’est ce que
                vous voyez d’un système plus large, pensé au Québec.
              </p>
              <ol className="v3-arch__list">
                {ARCHITECTURE.map((a, i) => (
                  <li key={a.name} className="v3-arch__row">
                    <span className="v3-arch__num">{String(i + 1).padStart(2, "0")}</span>
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

          {/* ── VOIE CLIENT ───────────────────────────────────────────────── */}
          <section className="v3-section v3-client" id="voie-client">
            <div className="v3-section__inner v3-two-col">
              <header className="v3-two-col__head">
                <p className="v3-kicker">Voie client · pour vous</p>
                <h2 className="v3-h2">
                  Un journal qui <em>vous appartient</em>, qui éclaire ce qui vient.
                </h2>
                <p className="v3-section__intro">
                  Avant même une rencontre, vous pouvez écrire à votre rythme
                  ce que vous traversez. IVIA organise ce que vous déposez
                  pour le restituer sous une forme claire — utile à vous
                  d’abord, et, si vous le souhaitez, à un·e praticien·ne.
                </p>
                <p className="v3-card__note">
                  Ce que vous écrivez est <strong>récompensé</strong> par une
                  lecture plus rapide et plus juste de votre situation. Vous
                  gagnez du temps quand vous décidez d’en parler.
                </p>
                <div className="v3-cta-row">
                  <Link href="/demarche" className="v3-btn v3-btn--primary">
                    Commencer mon espace privé
                    <span className="v3-btn__arrow" aria-hidden="true">→</span>
                  </Link>
                  <Link href="#trust" className="v3-btn v3-btn--ghost">
                    Voir mes garanties
                  </Link>
                </div>
              </header>

              <div className="v3-mock v3-mock--client" aria-label="Aperçu — espace client IVIA">
                <header className="v3-mock__head">
                  <span className="v3-mock__dot" aria-hidden="true" />
                  <span className="v3-mock__title">Mon espace privé</span>
                  <span className="v3-mock__tag">Privé · Québec</span>
                </header>
                <div className="v3-mock__body">
                  <p className="v3-mock__eyebrow">Je dépose</p>
                  <ul className="v3-mock__themes">
                    {CLIENT_THEMES.map((t, i) => (
                      <li
                        key={t}
                        className={i < 2 ? "is-checked" : ""}
                      >
                        <span className="v3-mock__check" aria-hidden="true" />
                        {t}
                      </li>
                    ))}
                  </ul>
                  <p className="v3-mock__eyebrow">Ce que j’ajoute en mes mots</p>
                  <p className="v3-mock__field">
                    « Je sens que je tiens debout, mais il y a quelque chose
                    que je ne nomme pas encore. Je voudrais arriver à le
                    voir. »
                  </p>
                </div>
                <footer className="v3-mock__foot">
                  <span>Brouillon · enregistré localement</span>
                  <span className="v3-mock__cta">Continuer →</span>
                </footer>
              </div>

              <ul className="v3-outputs v3-two-col__full">
                {CLIENT_OUTPUTS.map((o, i) => (
                  <li key={o.label} className="v3-output">
                    <span className="v3-output__num">
                      {String(i + 1).padStart(2, "0")}
                    </span>
                    <h3 className="v3-output__label">{o.label}</h3>
                    <p className="v3-output__body">{o.body}</p>
                  </li>
                ))}
              </ul>
            </div>
          </section>

          {/* ── VOIE PRATICIEN ────────────────────────────────────────────── */}
          <section className="v3-section v3-praticien" id="voie-praticien">
            <div className="v3-section__inner v3-two-col v3-two-col--reverse">
              <header className="v3-two-col__head">
                <p className="v3-kicker">Voie praticien · pour vous</p>
                <h2 className="v3-h2">
                  Lire ce qui se passe en séance, <em>structurer votre pratique.</em>
                </h2>
                <p className="v3-section__intro">
                  IVIA assiste votre travail entre les rencontres : lecture
                  des séances, repérage de ce qui revient, mise en forme des
                  interactions. Votre pratique évolue avec vous —
                  diplômé·e, en formation, ou hors-ordre.
                </p>
                <p className="v3-card__note">
                  Aucune affirmation de statut médical n’est faite à votre
                  place. Vous restez seul·e responsable de votre cadre, et
                  votre profil affiche clairement ce que vous déclarez.
                </p>
                <div className="v3-cta-row">
                  <Link href="/espace-praticien" className="v3-btn v3-btn--primary">
                    Découvrir l’espace praticien
                    <span className="v3-btn__arrow" aria-hidden="true">→</span>
                  </Link>
                  <Link href="#trust" className="v3-btn v3-btn--ghost">
                    Souveraineté &amp; données
                  </Link>
                </div>
              </header>

              <div className="v3-mock v3-mock--praticien" aria-label="Aperçu — espace praticien IVIA">
                <header className="v3-mock__head">
                  <span className="v3-mock__dot v3-mock__dot--earth" aria-hidden="true" />
                  <span className="v3-mock__title">Lecture de séance</span>
                  <span className="v3-mock__tag">14 mai · 50 min</span>
                </header>
                <div className="v3-mock__body">
                  <p className="v3-mock__eyebrow">Ce qui revient</p>
                  <ul className="v3-mock__chips">
                    <li>Fatigue de fin de semaine</li>
                    <li>Voix intérieure sévère</li>
                    <li>Rythme imposé</li>
                  </ul>
                  <p className="v3-mock__eyebrow">À rouvrir</p>
                  <p className="v3-mock__field">
                    « Lien à la mère — évoqué brièvement, à reprendre quand
                    le terrain sera prêt. »
                  </p>
                  <p className="v3-mock__eyebrow">Évolution déclarée</p>
                  <div className="v3-mock__progress" aria-hidden="true">
                    <span style={{ ["--w" as string]: "62%" }} />
                  </div>
                  <p className="v3-mock__progress-label">
                    Écoute structurée · 62 % des séances cadrées ces 3 mois
                  </p>
                </div>
                <footer className="v3-mock__foot">
                  <span>Vue praticien — privé</span>
                  <span className="v3-mock__cta">Ouvrir la séance →</span>
                </footer>
              </div>

              <ul className="v3-outputs v3-two-col__full">
                {PRACTITIONER_BENEFITS.map((b, i) => (
                  <li key={b.label} className="v3-output">
                    <span className="v3-output__num">
                      {String(i + 1).padStart(2, "0")}
                    </span>
                    <h3 className="v3-output__label">{b.label}</h3>
                    <p className="v3-output__body">{b.body}</p>
                  </li>
                ))}
              </ul>
            </div>
          </section>

          {/* ── COLLECTE STRATÉGIQUE ──────────────────────────────────────── */}
          <section className="v3-section v3-collecte">
            <div className="v3-section__inner">
              <p className="v3-kicker">Comment IVIA pose ses questions</p>
              <h2 className="v3-h2">
                Choix multiples, <em>plus l’espace de vos mots.</em>
              </h2>
              <p className="v3-section__intro">
                IVIA ne vous fait pas remplir un formulaire clinique. À chaque
                étape, vous choisissez parmi quelques propositions et — surtout —
                vous précisez librement, en quelques phrases, ce qui ne rentre
                pas dans les cases.
              </p>
              <div className="v3-collecte__grid">
                <article className="v3-collecte__card">
                  <span className="v3-collecte__step">01</span>
                  <h3>Choix multiples doux</h3>
                  <p>
                    Quelques propositions courtes, écrites en langage humain.
                    Aucun jargon clinique, aucune obligation d’en cocher.
                  </p>
                </article>
                <article className="v3-collecte__card">
                  <span className="v3-collecte__step">02</span>
                  <h3>Espace libre, en vos mots</h3>
                  <p>
                    Un champ ouvert pour préciser ce que les options n’atteignent
                    pas. C’est cet espace qui rend la lecture juste.
                  </p>
                </article>
                <article className="v3-collecte__card">
                  <span className="v3-collecte__step">03</span>
                  <h3>Orientation, si vous le souhaitez</h3>
                  <p>
                    IVIA vous propose une modalité adaptée — texte, voix, ou
                    rencontre avec un·e praticien·ne. Vous décidez du tempo.
                  </p>
                </article>
              </div>
            </div>
          </section>

          {/* ── VOIX DU FONDATEUR (vidéo) ─────────────────────────────────── */}
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
                      Trace vocale d’introduction d’IVIA — votre navigateur ne
                      supporte pas la lecture vidéo HTML5.
                    </p>
                  </video>
                </div>
                <figcaption>David Phaneuf · fondateur · Montréal</figcaption>
              </figure>
            </div>
          </section>

          {/* ── TRUST / SOUVERAINETÉ ──────────────────────────────────────── */}
          <section className="v3-section v3-trust" id="trust">
            <div className="v3-section__inner">
              <p className="v3-kicker">Confidentialité &amp; souveraineté</p>
              <h2 className="v3-h2">
                Vos mots <em>restent les vôtres.</em>
              </h2>
              <ul className="v3-trust__grid">
                {TRUST.map((t) => (
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

          {/* ── DISCLAIMER ────────────────────────────────────────────────── */}
          <section className="v3-disclaimer" aria-label="Avertissement non médical">
            <div className="v3-section__inner">
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
          <section className="v3-final">
            <div className="v3-final__halo" aria-hidden="true" />
            <div className="v3-section__inner v3-final__inner">
              <MesangeMark size={64} withSong className="v3-final__mark" />
              <p className="v3-eyebrow v3-eyebrow--center">
                <span className="v3-eyebrow__dot" aria-hidden="true" />
                Quand vous êtes prêt·e
              </p>
              <p className="v3-final__text">
                Vous pouvez entrer doucement.
                <br />
                <em>Vous choisissez la voie.</em>
              </p>
              <div className="v3-cta-row v3-cta-row--center">
                <Link href="/demarche" className="v3-btn v3-btn--primary">
                  Commencer mon espace privé
                  <span className="v3-btn__arrow" aria-hidden="true">→</span>
                </Link>
                <Link href="/espace-praticien" className="v3-btn v3-btn--ghost">
                  Je suis praticien·ne
                </Link>
              </div>
            </div>
          </section>
        </main>
      </div>
    </PublicLayout>
  );
}

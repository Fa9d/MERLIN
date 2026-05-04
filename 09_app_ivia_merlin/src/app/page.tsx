"use client";
import { useState } from "react";
import Link from "next/link";
import "./styles.css";
import { PublicLayout } from "@/components/layout/PublicLayout";

/* ── Data ─────────────────────────────────────────────────────────────────── */
const PILIERS = [
  {
    num: "01",
    title: "L\u2019\u00e9coute avant tout",
    body: "Je prends le temps de comprendre ce que vous vivez, sans grille, sans jugement. Chaque personne arrive avec son histoire unique.",
  },
  {
    num: "02",
    title: "Des rep\u00e8res concrets",
    body: "À chaque rencontre, on cherche quelque chose que vous pouvez garder — une prise de conscience, une d\u00e9cision, une direction.",
  },
  {
    num: "03",
    title: "Un rythme qui vous appartient",
    body: "Pas de protocole impos\u00e9. On avance \u00e0 votre rythme, selon ce dont vous avez besoin.",
  },
];

const AUDIENCE = [
  {
    tag: "Adultes",
    mod: "--adults",
    body: "Vous traversez une p\u00e9riode difficile, une transition, un doute profond. Vous cherchez \u00e0 comprendre ce qui se passe en vous — et \u00e0 trouver une direction.",
  },
  {
    tag: "Adolescents",
    mod: "--ados",
    body: "L\u2019adolescence peut \u00eatre un temps de turbulence int\u00e9rieure. Je cr\u00e9e un espace s\u00e9curitaire o\u00f9 parler devient possible, sans pression, sans jugement.",
  },
  {
    tag: "Parents \u0026 familles",
    mod: "--families",
    body: "Parfois c\u2019est la dynamique familiale qui a besoin d\u2019attention. On regarde ensemble ce qui se passe et comment retrouver un terrain commun.",
  },
];

const ETAPES = [
  { num: "01", title: "Vous arrivez comme vous \u00eates", body: "Pas besoin de pr\u00e9parer quoi que ce soit. Vous arrivez avec ce qui est l\u00e0." },
  { num: "02", title: "On prend le temps d\u2019\u00e9couter", body: "Je pose des questions, j\u2019\u00e9coute, je refl\u00e8te. On explore ce que vous portez." },
  { num: "03", title: "On cherche ensemble", body: "Pas de r\u00e9ponses toutes faites. On cherche ce qui a du sens pour vous, maintenant." },
  { num: "04", title: "Vous repartez avec quelque chose", body: "Une clart\u00e9, une d\u00e9cision, une prochaine \u00e9tape. Quelque chose qui vous appartient." },
];

/* ── Component ────────────────────────────────────────────────────────────── */
export default function HomePage() {
  const [emailVal, setEmailVal] = useState("");
  const [emailSent, setEmailSent] = useState(false);

  function handleEmailSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (emailVal.trim()) setEmailSent(true);
  }

  return (
    <PublicLayout>
      <div className="hp">
      <main>
        {/* ── HERO ──────────────────────────────────────────────────────── */
        <section className="hp-hero">
          <div className="hp-hero__inner">
            <div className="hp-hero__copy">
              <p className="hp-kicker">Accompagnement individuel · Montréal</p>
              <h1 className="hp-hero__h1">
                Un espace pour déposer<br />
                ce que vous portez
              </h1>
              <p className="hp-hero__sub">
                Je vous accompagne avec calme et une vraie présence — pour retrouver de la clarté et repartir avec quelque chose de concret.
              </p>
              <Link href="/rendez-vous" className="hp-btn hp-btn--primary">
                Prendre un premier rendez-vous
              </Link>
            </div>
            <div className="hp-hero__visual" aria-hidden="true">
              <div className="hp-hero__art">
                <span className="hp-hero__art-word hp-hero__art-word--1">présence</span>
                <span className="hp-hero__art-word hp-hero__art-word--2">écoute</span>
                <span className="hp-hero__art-word hp-hero__art-word--3">clarté</span>
              </div>
            </div>
          </div>
        </section>

        {/* ── PONT ──────────────────────────────────────────────────────── */}
        <section className="hp-pont">
          <p className="hp-pont__text">
            Vous n’avez pas à avoir les mots parfaits.<br />
            <em>Vous avez juste à commencer.</em>
          </p>
        </section>

        {/* ── APPROCHE ──────────────────────────────────────────────────── */}
        <section className="hp-section hp-approche" id="approche">
          <div className="hp-section__inner">
            <p className="hp-kicker">Ma manière d’accompagner</p>
            <h2 className="hp-h2">Je ne suis pas là pour diagnostiquer<br className="hp-br" /> ni pour diriger.</h2>
            <p className="hp-approche__intro">
              Je suis là pour écouter vraiment, poser les bonnes questions, et vous aider à voir plus clair.
            </p>
            <div className="hp-piliers">
              {PILIERS.map((p) => (
                <div key={p.num} className="hp-pilier">
                  <span className="hp-pilier__num">{p.num}</span>
                  <h3 className="hp-pilier__title">{p.title}</h3>
                  <p className="hp-pilier__body">{p.body}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ── POUR QUI ──────────────────────────────────────────────────── */}
        <section className="hp-section hp-pourqui" id="pour-qui">
          <div className="hp-section__inner">
            <p className="hp-kicker">Pour qui</p>
            <h2 className="hp-h2">Chaque personne arrive avec son histoire.</h2>
            <div className="hp-audience">
              {AUDIENCE.map((a) => (
                <div key={a.tag} className={`hp-audience__card hp-audience__card${a.mod}`}>
                  <h3 className="hp-audience__tag">{a.tag}</h3>
                  <p className="hp-audience__body">{a.body}</p>
                  <a href="#rencontre" className="hp-link">Je veux en savoir plus →</a>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ── RENCONTRE ─────────────────────────────────────────────────── */}
        <section className="hp-section hp-rencontre" id="rencontre">
          <div className="hp-section__inner">
            <p className="hp-kicker">Comment se passe une rencontre</p>
            <h2 className="hp-h2">50 minutes de présence complète.</h2>
            <div className="hp-etapes">
              {ETAPES.map((e) => (
                <div key={e.num} className="hp-etape">
                  <span className="hp-etape__num">{e.num}</span>
                  <div>
                    <h3 className="hp-etape__title">{e.title}</h3>
                    <p className="hp-etape__body">{e.body}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ── CAPSULES ──────────────────────────────────────────────────── */}
        <section className="hp-section hp-capsules">
          <div className="hp-section__inner hp-capsules__inner">
            <div className="hp-capsules__copy">
              <p className="hp-kicker">Capsules audio · À venir</p>
              <h2 className="hp-h2 hp-h2--sm">De courtes écoutes pour<br />les moments difficiles.</h2>
              <p className="hp-capsules__body">
                La fatigue décisionnelle, l’anxiété du dimanche soir, la voix intérieure trop sévère. Je travaille en ce moment à vous les offrir.
              </p>
            </div>
            <div className="hp-capsules__form-wrap">
              {emailSent ? (
                <p className="hp-capsules__confirm">Merci — je vous écrirai à leur sortie.</p>
              ) : (
                <form className="hp-capsules__form" onSubmit={handleEmailSubmit} aria-label="Notification capsules audio">
                  <label htmlFor="capsule-email" className="hp-capsules__label">
                    Recevoir un mot à leur sortie
                  </label>
                  <div className="hp-capsules__row">
                    <input
                      id="capsule-email"
                      type="email"
                      required
                      placeholder="votre@courriel.com"
                      className="hp-input"
                      value={emailVal}
                      onChange={(e) => setEmailVal(e.target.value)}
                    />
                    <button type="submit" className="hp-btn hp-btn--secondary">M’avertir</button>
                  </div>
                </form>
              )}
            </div>
          </div>
        </section>

        {/* ── CTA FINAL ─────────────────────────────────────────────────── */}
        <section className="hp-cta-final">
          <div className="hp-section__inner hp-cta-final__inner">
            <p className="hp-cta-final__text">
              Si quelque chose résonne,<br />
              c’est peut-être le bon moment.
            </p>
            <Link href="/rendez-vous" className="hp-btn hp-btn--primary">
              Prendre un premier rendez-vous →
            </Link>
          </div>
        </section>
      </main>
      </div>
    </PublicLayout>
  );
}

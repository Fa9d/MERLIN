import Link from "next/link";
import { PublicLayout } from "@/components/layout/PublicLayout";
import { MesangeMark } from "@/components/MesangeMark";
import "../styles.css";
import "../styles.v3.css";

const OFFRES = [
  {
    title: "Rencontre d’écoute",
    body: "Une séance, un praticien, une heure pour déposer ce qui pèse. Vous repartez avec une direction.",
  },
  {
    title: "Écoute avec compte rendu",
    body: "La même rencontre, plus un résumé écrit de ce que vous avez exploré ensemble et des pistes concrètes pour la suite.",
  },
  {
    title: "Parcours de soutien",
    body: "Plusieurs rencontres dans le temps, avec un suivi documenté à chaque étape. Pour ceux qui traversent quelque chose de plus long.",
  },
];

const ETAPES = [
  {
    num: "01",
    label: "Vous réservez",
    body: "En ligne, en moins de 2 minutes, sans dossier ni formulaire médical. Vous choisissez le moment qui vous convient.",
  },
  {
    num: "02",
    label: "Vous vous retrouvez",
    body: "Votre praticien MÉSANGES vous rejoint par audio à l’heure convenue. Vous parlez. Il écoute, pose des questions, vous aide à nommer ce qui se passe — sans jugement, sans étiquette.",
  },
  {
    num: "03",
    label: "Vous repartez avec quelque chose",
    body: "Une lecture plus claire de votre situation, des pistes concrètes pour la suite — et, si vous le souhaitez, un document récapitulatif que vous gardez. Pas de prescription. Pas de dossier. Vos propres repères.",
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
              <p className="v3-kicker">MÉSANGES</p>
              <h1 id="mesange-hero-title" className="v3-h2">
                Une rencontre avec <em>une vraie personne.</em>
              </h1>
              <p className="v3-section__intro v3-section__intro--large">
                Pas une application. Pas un chatbot. Pas un formulaire.
                Un praticien formé à l’écoute active vous rejoint par audio
                pour une conversation qui compte.
              </p>
              <div className="v3-cta-row">
                <Link href="/rendez-vous" className="v3-btn v3-btn--primary">
                  Prendre rendez-vous
                  <span className="v3-btn__arrow" aria-hidden="true">&rarr;</span>
                </Link>
                <Link href="/orientation" className="v3-btn v3-btn--outline">
                  Faire le parcours d’orientation
                </Link>
              </div>
            </div>
          </section>

          {/* VALEURS */}
          <section className="v3-section v3-mesange-valeurs" id="valeurs" aria-labelledby="valeurs-title">
            <div className="v3-section__inner">
              <p className="v3-kicker">Ce que MÉSANGES est</p>
              <h2 id="valeurs-title" className="v3-h2">
                Un espace d’écoute. <em>Honnête et sans étiquette.</em>
              </h2>
              <div className="v3-mesange-valeurs__cols">
                <div className="v3-mesange-valeur">
                  <h3 className="v3-mesange-valeur__title">On ne vous vendra pas une promesse qu’on ne peut pas tenir.</h3>
                  <p className="v3-mesange-valeur__body">
                    Pas de transformation en sept jours. Pas de déclic garanti.
                    Ce que MÉSANGES offre est plus modeste et plus honnête : un endroit
                    pour déposer ce que vous portez, retrouver de la clarté, et repartir
                    avec un repère.
                  </p>
                </div>
                <div className="v3-mesange-valeur">
                  <h3 className="v3-mesange-valeur__title">On ne vous écrira jamais comme si vous étiez fragile.</h3>
                  <p className="v3-mesange-valeur__body">
                    Nous parlons à des personnes qui réfléchissent, qui doutent,
                    qui cherchent. Notre ton est posé. Nous comptons sur votre
                    intelligence avant de compter sur votre émotion.
                  </p>
                </div>
                <div className="v3-mesange-valeur">
                  <h3 className="v3-mesange-valeur__title">Notre objectif : que vous n’ayez plus besoin de nous.</h3>
                  <p className="v3-mesange-valeur__body">
                    L’autonomie émotionnelle est notre horizon. Pas la dépendance.
                    Chaque rencontre vise à vous donner vos propres repères — pas
                    à vous attacher à un service.
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
                Simple, concret, <em>sans démarche administrative.</em>
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
              <p className="v3-kicker">Trois façons de commencer</p>
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
                  Réserver une rencontre
                  <span className="v3-btn__arrow" aria-hidden="true">&rarr;</span>
                </Link>
              </div>
            </div>
          </section>

          {/* FRONTIÈRES */}
          <section className="v3-section v3-pour-moi" id="frontieres" aria-labelledby="frontieres-title">
            <div className="v3-section__inner">
              <p className="v3-kicker">Ce que MÉSANGES n’est pas</p>
              <h2 id="frontieres-title" className="v3-h2">
                Des frontières <em>claires et honnêtes.</em>
              </h2>
              <ul className="v3-mesange-frontieres">
                <li>
                  <strong>MÉSANGES ne fait pas de diagnostic.</strong>{" "}
                  Aucun de nos contenus n’est un avis médical, psychologique ou psychiatrique.
                </li>
                <li>
                  <strong>MÉSANGES ne traite pas la détresse aiguë.</strong>{" "}
                  Si vous traversez une crise, composez le <strong>811</strong> (Info-Social),
                  le <strong>1 866 APPELLE</strong> (prévention du suicide)
                  ou le <strong>911</strong> si le danger est immédiat.
                </li>
                <li>
                  <strong>MÉSANGES n’est pas de la psychothérapie réglementée.</strong>{" "}
                  Si vous avez déjà un suivi clinique, continuez avec votre professionnel.
                  IVIA peut être un complément — jamais un substitut.
                </li>
                <li>
                  <strong>MÉSANGES n’est pas une application.</strong>{" "}
                  Pas de notifications, pas d’abonnement mensuel, pas de contenu à consommer.
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

"use client";

import { useMemo, useState } from "react";
import Link from "next/link";

/* ──────────────────────────────────────────────────────────────────────────
   Orientation MÉSANGES — Survey téléphone
   - Une question par écran, barre de progression, navigation précédent/suivant.
   - Données conservées **uniquement en React state**. Aucune persistance
     (localStorage, sessionStorage, cookies) — voir CLAUDE.md §5 (PII).
   - Posture non médicale, FR québécois, sous consentement.
   ────────────────────────────────────────────────────────────────────────── */

type OptionDef = { value: string; label: string; hint?: string };
type StepKind = "single" | "multi" | "text" | "contact" | "intro" | "result";

type Step = {
  id: string;
  kind: StepKind;
  title: string;
  hint?: string;
  options?: OptionDef[];
  placeholder?: string;
  optional?: boolean;
  /** Si présent, déclenche l'affichage du garde-fou urgence à valeur égale */
  safeguardOn?: string;
};

// ─── Définition du parcours ───────────────────────────────────────────────

const STEPS: Step[] = [
  {
    id: "intro",
    kind: "intro",
    title: "Quelques minutes pour situer ce que vous vivez.",
    hint:
      "Ce court parcours nous aide à préparer une écoute juste, à votre rythme. Nous commençons par ce qui se ressent, puis nous situons votre profil et la suite possible.",
  },
  {
    id: "emotion",
    kind: "single",
    title: "Quelle émotion ou quel état vous amène ici en premier ?",
    options: [
      { value: "anxiete", label: "Anxiété, inquiétude" },
      { value: "tristesse", label: "Tristesse, vide" },
      { value: "epuisement", label: "Fatigue, épuisement" },
      { value: "colere", label: "Colère, tension" },
      { value: "confusion", label: "Confusion, brouillard" },
      { value: "isolement", label: "Isolement, retrait" },
      { value: "transition", label: "Transition, perte de repères" },
      { value: "elan", label: "Je veux surtout clarifier et avancer" },
    ],
  },
  {
    id: "demarche",
    kind: "single",
    title: "Pour qui faites-vous cette démarche ?",
    options: [
      { value: "self", label: "Pour moi" },
      { value: "relative", label: "Pour un proche ou ma famille" },
      { value: "collective", label: "Pour une collectivité ou une équipe" },
      { value: "praticien", label: "Je suis praticien·ne et je découvre" },
    ],
  },
  {
    id: "genre",
    kind: "single",
    title: "Comment vous identifiez-vous ?",
    hint: "Cette information aide à ajuster le ton, sans rien présupposer.",
    options: [
      { value: "femme", label: "Femme" },
      { value: "homme", label: "Homme" },
      { value: "nonbinaire", label: "Non binaire" },
      { value: "preciser", label: "Je préfère préciser plus tard" },
      { value: "norep", label: "Je préfère ne pas répondre" },
    ],
  },
  {
    id: "age",
    kind: "single",
    title: "Dans quelle tranche d'âge vous situez-vous ?",
    options: [
      { value: "lt18", label: "Moins de 18 ans" },
      { value: "18-24", label: "18 — 24 ans" },
      { value: "25-34", label: "25 — 34 ans" },
      { value: "35-44", label: "35 — 44 ans" },
      { value: "45-54", label: "45 — 54 ans" },
      { value: "55-64", label: "55 — 64 ans" },
      { value: "65p", label: "65 ans et plus" },
    ],
  },
  {
    id: "localisation",
    kind: "single",
    title: "Où vous trouvez-vous principalement ?",
    options: [
      { value: "qc", label: "Au Québec" },
      { value: "ca", label: "Ailleurs au Canada" },
      { value: "hors", label: "Hors Canada" },
    ],
  },
  {
    id: "region",
    kind: "text",
    title: "Une ville ou région, si vous le souhaitez ?",
    hint: "Facultatif. Cela peut nous aider à orienter vers un appui local.",
    placeholder: "Ex. Montréal, Saguenay, Laurentides…",
    optional: true,
  },
  {
    id: "intention",
    kind: "single",
    title: "Quelle est votre intention principale aujourd'hui ?",
    options: [
      { value: "ecoute", label: "Être écouté·e simplement" },
      { value: "clarifier", label: "Clarifier une situation" },
      { value: "preparer", label: "Préparer une rencontre" },
      { value: "repetitions", label: "Mieux comprendre des répétitions" },
      { value: "relations", label: "Relations, famille, liens" },
      { value: "corps", label: "Corps, métabolisme, sommeil" },
      { value: "stress", label: "Stress, charge mentale" },
      { value: "numerique", label: "Numérique, attention, écrans" },
      { value: "autre", label: "Autre chose" },
    ],
  },
  {
    id: "poids",
    kind: "multi",
    title: "Qu'est-ce qui pèse le plus en ce moment ?",
    hint: "Plusieurs choix possibles.",
    options: [
      { value: "fatigue", label: "Fatigue persistante" },
      { value: "anxiete", label: "Inquiétude ou anxiété" },
      { value: "tristesse", label: "Tristesse, vide" },
      { value: "isolement", label: "Sentiment d'isolement" },
      { value: "deuil", label: "Deuil ou perte" },
      { value: "famille", label: "Tensions familiales" },
      { value: "travail", label: "Charge professionnelle" },
      { value: "sante", label: "Préoccupations de santé" },
      { value: "transition", label: "Transition de vie" },
      { value: "rien", label: "Rien de précis pour l'instant" },
    ],
  },
  {
    id: "precision",
    kind: "text",
    title: "Souhaitez-vous préciser dans vos propres mots ?",
    hint:
      "Facultatif. Ce que vous écrivez ici ne quitte pas votre appareil dans ce prototype.",
    placeholder: "Quelques phrases suffisent…",
    optional: true,
  },
  {
    id: "intensite",
    kind: "single",
    title: "Comment décririez-vous l'intensité actuelle ?",
    options: [
      { value: "calme", label: "Plutôt calme" },
      { value: "inconfort", label: "Un inconfort présent" },
      { value: "difficile", label: "C'est difficile" },
      { value: "tres", label: "C'est très difficile" },
      { value: "danger", label: "Je ressens un danger immédiat" },
    ],
    safeguardOn: "danger",
  },
  {
    id: "corps",
    kind: "multi",
    title: "Y a-t-il un rythme corporel qui attire votre attention ?",
    hint: "Plusieurs choix possibles. Aucune dimension médicale ici.",
    options: [
      { value: "sommeil", label: "Sommeil" },
      { value: "energie", label: "Énergie" },
      { value: "alimentation", label: "Alimentation, digestion" },
      { value: "tensions", label: "Douleurs ou tensions" },
      { value: "cycles", label: "Cycles, hormonal" },
      { value: "aucun", label: "Aucune de ces réponses" },
      { value: "norep", label: "Je préfère ne pas répondre" },
    ],
  },
  {
    id: "accompagnement",
    kind: "single",
    title: "Quel accompagnement vous parle le plus ?",
    options: [
      { value: "ponctuel", label: "Un suivi ponctuel" },
      { value: "regulier", label: "Un suivi régulier" },
      { value: "preparation", label: "Préparer une rencontre avec un·e praticien·ne" },
      { value: "journal", label: "Un journal guidé" },
      { value: "orientation", label: "Une orientation vers un·e praticien·ne" },
      { value: "idk", label: "Je ne sais pas encore" },
    ],
  },
  {
    id: "contact",
    kind: "contact",
    title: "Comment souhaitez-vous être recontacté·e ?",
    hint:
      "Vos coordonnées servent à préparer la suite. Dans ce prototype, elles ne sont pas transmises.",
  },
  {
    id: "result",
    kind: "result",
    title: "Votre portrait d'orientation",
  },
];

// ─── Garde-fous urgence ───────────────────────────────────────────────────

function Safeguard() {
  return (
    <aside className="os-safeguard" role="note">
      <strong>Si vous ressentez un danger immédiat :</strong>
      MÉSANGES n&apos;est pas un service d&apos;urgence. En cas de danger pour
      vous ou pour quelqu&apos;un, contactez sans attendre :
      <ul>
        <li>
          <strong>911</strong> — urgence immédiate
        </li>
        <li>
          <strong>988</strong> — ligne canadienne de prévention du suicide
        </li>
        <li>
          <strong>811</strong> — Info-Santé / Info-Social (Québec)
        </li>
      </ul>
    </aside>
  );
}

// ─── État du formulaire ───────────────────────────────────────────────────

type Answers = {
  emotion?: string;
  demarche?: string;
  genre?: string;
  age?: string;
  localisation?: string;
  region?: string;
  intention?: string;
  poids: string[];
  precision?: string;
  intensite?: string;
  corps: string[];
  accompagnement?: string;
  contact: {
    first_name: string;
    email: string;
    phone: string;
    preference: "" | "email" | "phone" | "sms";
    consent: boolean;
  };
};

const EMPTY_ANSWERS: Answers = {
  poids: [],
  corps: [],
  contact: { first_name: "", email: "", phone: "", preference: "", consent: false },
};

// ─── Génération du portrait final ─────────────────────────────────────────

type Axe = { title: string; body: string };

function buildPortrait(a: Answers): { lead: string; axes: Axe[]; suite: string[] } {
  const axes: Axe[] = [];

  if (a.emotion) {
    const emotionMap: Record<string, Axe> = {
      anxiete: {
        title: "Une inquiétude à déposer",
        body: "Vos réponses suggèrent d'abord le besoin de ralentir, de clarifier et de réduire ce qui tourne en boucle.",
      },
      tristesse: {
        title: "Une part plus lourde à reconnaître",
        body: "Ce qui se présente ici demande une écoute sobre, sans forcer une conclusion trop rapide.",
      },
      epuisement: {
        title: "Un niveau de charge trop élevé",
        body: "Le premier enjeu semble être la charge portée : énergie, rythme, récupération, bande passante.",
      },
      colere: {
        title: "Une tension qui cherche sa forme",
        body: "Il y a possiblement quelque chose à nommer plus nettement pour retrouver un axe d'action clair.",
      },
      confusion: {
        title: "Un besoin de clarté",
        body: "Vos réponses pointent vers le besoin de distinguer, ordonner et comprendre ce qui se mêle en ce moment.",
      },
      isolement: {
        title: "Un lien à retisser",
        body: "La solitude ou le retrait semblent occuper une place importante dans ce que vous traversez actuellement.",
      },
      transition: {
        title: "Un passage en cours",
        body: "Vous semblez traverser un moment de bascule où il faut reconnaître ce qui change et ce qui reste à reconstruire.",
      },
      elan: {
        title: "Un désir d'avancer avec justesse",
        body: "Vous arrivez avec l'élan de mieux comprendre et de choisir une suite cohérente, sans dramatiser ce que vous vivez.",
      },
    };
    axes.push(emotionMap[a.emotion]);
  }

  if (a.intention) {
    const map: Record<string, Axe> = {
      ecoute: {
        title: "Un besoin d'écoute simple",
        body: "Ce que vous indiquez d'abord, c'est le besoin d'un espace où déposer, sans être orienté trop vite.",
      },
      clarifier: {
        title: "Clarifier ce qui se joue",
        body: "Mettre des mots, distinguer ce qui pèse de ce qui revient, repérer une ligne de fond.",
      },
      preparer: {
        title: "Préparer une rencontre",
        body: "Arriver à un rendez-vous avec une lecture déjà posée, sans la subir.",
      },
      repetitions: {
        title: "Comprendre des répétitions",
        body: "Observer ce qui revient, ce qui résiste, ce qui mérite une attention nouvelle.",
      },
      relations: {
        title: "Liens et relations",
        body: "Famille, proches, équipe — un appui pour nommer ce qui circule sans forcer une issue.",
      },
      corps: {
        title: "Rythmes du corps",
        body: "Sommeil, énergie, alimentation. Une lecture non médicale, à mettre en dialogue avec votre médecin si besoin.",
      },
      stress: {
        title: "Charge mentale et stress",
        body: "Mettre en pause, identifier ce qui mobilise trop, retrouver une bande passante.",
      },
      numerique: {
        title: "Attention et numérique",
        body: "Écrans, notifications, dispersion : ce qui prend la place qu'on ne lui a pas accordée.",
      },
      autre: {
        title: "Quelque chose à nommer",
        body: "Vous avez choisi une voie qui ne tient pas dans une seule case. Nous prenons le temps de la dérouler.",
      },
    };
    if (map[a.intention]) axes.push(map[a.intention]);
  }

  if (a.poids.length) {
    const tops = a.poids.slice(0, 2).map((v) =>
      ({
        fatigue: "fatigue persistante",
        anxiete: "inquiétude diffuse",
        tristesse: "traversée plus sombre",
        isolement: "sentiment d'isolement",
        deuil: "deuil ou perte",
        famille: "tensions familiales",
        travail: "charge professionnelle",
        sante: "préoccupations de santé",
        transition: "transition de vie",
        rien: "ouverture sans point précis",
      }[v] ?? v),
    );
    axes.push({
      title: "Ce qui pèse aujourd'hui",
      body: `Vous avez nommé : ${tops.join(", ")}. C'est ce que nous garderons à portée d'écoute.`,
    });
  }

  if (a.corps.length && !a.corps.includes("aucun") && !a.corps.includes("norep")) {
    const map: Record<string, string> = {
      sommeil: "sommeil",
      energie: "énergie",
      alimentation: "alimentation et digestion",
      tensions: "douleurs ou tensions",
      cycles: "cycles",
    };
    const corps = a.corps.map((v) => map[v]).filter(Boolean).slice(0, 3);
    if (corps.length) {
      axes.push({
        title: "Rythmes corporels à observer",
        body: `Vous évoquez : ${corps.join(", ")}. À mettre en dialogue avec un·e professionnel·le de santé si nécessaire.`,
      });
    }
  }

  // Toujours garantir 3 axes
  while (axes.length < 3) {
    axes.push({
      title: "Une part en attente",
      body: "Ce qui n'a pas encore été dit fait aussi partie du portrait. Nous le garderons en réserve.",
    });
  }

  const suite: string[] = [];
  switch (a.accompagnement) {
    case "ponctuel":
      suite.push("Une écoute initiale ponctuelle avec MÉSANGES.");
      break;
    case "regulier":
      suite.push("Un suivi régulier, à votre rythme.");
      break;
    case "preparation":
      suite.push("Une préparation guidée avant votre prochaine rencontre.");
      break;
    case "journal":
      suite.push("L'amorce d'un journal préparatoire MÉSANGES.");
      break;
    case "orientation":
      suite.push("Une orientation vers un·e praticien·ne dont la voie résonne avec ce que vous décrivez.");
      break;
    default:
      suite.push("Un premier échange MÉSANGES pour préciser ensemble la voie qui convient.");
  }
  suite.push("Un retour écrit doux, à confirmer avec vous.");
  suite.push("La possibilité d'ouvrir un espace privé pour vos notes, sous consentement.");

  const lead =
    "Voici un portrait d'orientation MÉSANGES. Ce n'est ni un diagnostic, ni une conclusion : c'est une première lecture de ce que vos réponses laissent apparaître, à confirmer avec vous.";

  return { lead, axes: axes.slice(0, 3), suite };
}

// ─── Composant principal ──────────────────────────────────────────────────

export function OrientationSurvey() {
  const [stepIdx, setStepIdx] = useState(0);
  const [answers, setAnswers] = useState<Answers>(EMPTY_ANSWERS);

  const step = STEPS[stepIdx];
  const total = STEPS.length;
  const progress = useMemo(
    () => Math.round(((stepIdx + 1) / total) * 100),
    [stepIdx, total],
  );

  const isFirst = stepIdx === 0;
  const isResult = step.kind === "result";

  // Validation par étape
  const canContinue = useMemo(() => {
    if (step.kind === "intro" || step.kind === "result") return true;
    if (step.optional) return true;
    if (step.kind === "text") {
      return Boolean((answers as Record<string, unknown>)[step.id]);
    }
    if (step.kind === "single") {
      return Boolean((answers as Record<string, unknown>)[step.id]);
    }
    if (step.kind === "multi") {
      const v = (answers as unknown as Record<string, string[]>)[step.id] ?? [];
      return v.length > 0;
    }
    if (step.kind === "contact") {
      const c = answers.contact;
      return (
        c.first_name.trim().length > 0 &&
        /^\S+@\S+\.\S+$/.test(c.email) &&
        c.phone.trim().length >= 7 &&
        c.preference !== "" &&
        c.consent
      );
    }
    return true;
  }, [step, answers]);

  const showSafeguard =
    step.safeguardOn !== undefined &&
    (answers as Record<string, unknown>)[step.id] === step.safeguardOn;

  function selectSingle(value: string) {
    setAnswers((a) => ({ ...a, [step.id]: value }));
  }

  function toggleMulti(value: string) {
    setAnswers((a) => {
      const current = (a as unknown as Record<string, string[]>)[step.id] ?? [];
      const next = current.includes(value)
        ? current.filter((v) => v !== value)
        : [...current, value];
      return { ...a, [step.id]: next };
    });
  }

  function setText(value: string) {
    setAnswers((a) => ({ ...a, [step.id]: value }));
  }

  function setContact<K extends keyof Answers["contact"]>(
    key: K,
    value: Answers["contact"][K],
  ) {
    setAnswers((a) => ({ ...a, contact: { ...a.contact, [key]: value } }));
  }

  function goNext() {
    if (!canContinue) return;
    if (stepIdx < total - 1) setStepIdx(stepIdx + 1);
  }
  function goBack() {
    if (stepIdx > 0) setStepIdx(stepIdx - 1);
  }
  function restart() {
    setAnswers(EMPTY_ANSWERS);
    setStepIdx(0);
  }

  return (
    <div className="os-shell">
      <div className="os-topbar">
        <div className="os-brand">
          <strong>MÉSANGES</strong>
          <span>· orientation</span>
        </div>
        <Link href="/" className="os-exit" aria-label="Quitter et revenir à l'accueil">
          Fermer
        </Link>
      </div>

      <section
        className="os-phone"
        role="region"
        aria-label="Parcours d'orientation MÉSANGES"
      >
        <div className="os-progress" aria-hidden="true">
          <div className="os-progress__bar" style={{ width: `${progress}%` }} />
        </div>

        <p className="os-step-label">
          Étape {stepIdx + 1} sur {total}
        </p>

        <h1 className="os-question">{step.title}</h1>
        {step.hint ? <p className="os-hint">{step.hint}</p> : null}

        {/* ── Rendu selon le type d'étape ─────────────────────────────── */}

        {step.kind === "intro" ? (
          <div style={{ flex: 1 }}>
            <p className="os-hint" style={{ marginTop: 0 }}>
              Vous pouvez répondre en quelques minutes. À la fin, nous vous
              proposons un portrait d&apos;orientation et un suivi adapté.
            </p>
          </div>
        ) : null}

        {step.kind === "single" && step.options ? (
          <ul className="os-options" role="radiogroup" aria-label={step.title}>
            {step.options.map((opt) => {
              const selected =
                (answers as Record<string, unknown>)[step.id] === opt.value;
              return (
                <li key={opt.value}>
                  <button
                    type="button"
                    role="radio"
                    aria-checked={selected}
                    className={`os-option ${selected ? "os-option--selected" : ""}`}
                    onClick={() => selectSingle(opt.value)}
                  >
                    <span className="os-option__bullet" aria-hidden="true" />
                    <span>{opt.label}</span>
                  </button>
                </li>
              );
            })}
          </ul>
        ) : null}

        {step.kind === "multi" && step.options ? (
          <ul className="os-options" role="group" aria-label={step.title}>
            {step.options.map((opt) => {
              const v =
                (answers as unknown as Record<string, string[]>)[step.id] ?? [];
              const selected = v.includes(opt.value);
              return (
                <li key={opt.value}>
                  <button
                    type="button"
                    aria-pressed={selected}
                    className={`os-option ${selected ? "os-option--selected" : ""}`}
                    onClick={() => toggleMulti(opt.value)}
                  >
                    <span className="os-option__square" aria-hidden="true" />
                    <span>{opt.label}</span>
                  </button>
                </li>
              );
            })}
          </ul>
        ) : null}

        {step.kind === "text" ? (
          <div className="os-field" style={{ flex: 1 }}>
            <label className="os-field__label" htmlFor={`field-${step.id}`}>
              Votre réponse
            </label>
            <textarea
              id={`field-${step.id}`}
              className="os-field__textarea"
              placeholder={step.placeholder}
              value={(answers as unknown as Record<string, string>)[step.id] ?? ""}
              onChange={(e) => setText(e.target.value)}
              rows={4}
            />
            {step.optional ? (
              <p className="os-field__hint">
                Vous pouvez passer cette question.
              </p>
            ) : null}
          </div>
        ) : null}

        {step.kind === "contact" ? (
          <div style={{ flex: 1 }}>
            <div className="os-field">
              <label className="os-field__label" htmlFor="contact-first-name">
                Prénom
              </label>
              <input
                id="contact-first-name"
                className="os-field__input"
                type="text"
                value={answers.contact.first_name}
                onChange={(e) => setContact("first_name", e.target.value)}
                autoComplete="given-name"
              />
            </div>
            <div className="os-field">
              <label className="os-field__label" htmlFor="contact-email">
                Courriel
              </label>
              <input
                id="contact-email"
                className="os-field__input"
                type="email"
                inputMode="email"
                value={answers.contact.email}
                onChange={(e) => setContact("email", e.target.value)}
                autoComplete="email"
              />
            </div>
            <div className="os-field">
              <label className="os-field__label" htmlFor="contact-phone">
                Téléphone
              </label>
              <input
                id="contact-phone"
                className="os-field__input"
                type="tel"
                inputMode="tel"
                value={answers.contact.phone}
                onChange={(e) => setContact("phone", e.target.value)}
                autoComplete="tel"
              />
            </div>
            <div className="os-field">
              <label className="os-field__label" htmlFor="contact-pref">
                Préférence de contact
              </label>
              <select
                id="contact-pref"
                className="os-field__input"
                value={answers.contact.preference}
                onChange={(e) =>
                  setContact("preference", e.target.value as Answers["contact"]["preference"])
                }
              >
                <option value="">— Choisir —</option>
                <option value="email">Courriel</option>
                <option value="phone">Appel</option>
                <option value="sms">SMS</option>
              </select>
            </div>

            <div className="os-consent">
              <input
                id="contact-consent"
                type="checkbox"
                checked={answers.contact.consent}
                onChange={(e) => setContact("consent", e.target.checked)}
              />
              <label htmlFor="contact-consent">
                J&apos;accepte que MÉSANGES utilise mes coordonnées pour
                préparer la suite, au Québec et sous consentement.
              </label>
            </div>
          </div>
        ) : null}

        {step.kind === "result"
          ? (() => {
              const portrait = buildPortrait(answers);
              return (
                <div className="os-result">
                  <p className="os-result__lead">{portrait.lead}</p>

                  <ul className="os-axes">
                    {portrait.axes.map((axe, i) => (
                      <li className="os-axe" key={i}>
                        <span className="os-axe__title">{axe.title}</span>
                        <span className="os-axe__body">{axe.body}</span>
                      </li>
                    ))}
                  </ul>

                  <div className="os-result__follow">
                    <h3>Suivi MÉSANGES proposé</h3>
                    <p>
                      À partir de vos réponses, voici les pistes que nous
                      pourrions ouvrir ensemble :
                    </p>
                    <ul>
                      {portrait.suite.map((s, i) => (
                        <li key={i}>{s}</li>
                      ))}
                    </ul>
                  </div>

                  <p className="os-result__disclaimer">
                    Ce portrait ne remplace pas un avis médical ni un service
                    d&apos;urgence. Vos informations serviront à préparer la
                    suite. Dans ce prototype, elles ne sont pas encore
                    transmises.
                  </p>

                  <div className="os-result__actions">
                    <Link href="/rendez-vous" className="os-btn os-btn--primary">
                      Prendre rendez-vous
                    </Link>
                    <button
                      type="button"
                      className="os-btn os-btn--ghost"
                      onClick={restart}
                    >
                      Recommencer le parcours
                    </button>
                  </div>
                </div>
              );
            })()
          : null}

        {showSafeguard ? <Safeguard /> : null}

        {/* ── Navigation ─────────────────────────────────────────────── */}
        {!isResult ? (
          <div className="os-nav">
            <button
              type="button"
              className="os-btn os-btn--ghost"
              onClick={goBack}
              disabled={isFirst}
            >
              ← Précédent
            </button>
            <button
              type="button"
              className="os-btn os-btn--primary"
              onClick={goNext}
              disabled={!canContinue}
            >
              {stepIdx === total - 2 ? "Voir mon portrait" : "Continuer"}
              <span aria-hidden="true">→</span>
            </button>
          </div>
        ) : null}
      </section>
    </div>
  );
}

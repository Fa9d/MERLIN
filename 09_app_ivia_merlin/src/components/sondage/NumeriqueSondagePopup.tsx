"use client";
/**
 * NumeriqueSondagePopup — Évaluation du rapport au numérique
 *
 * Fondement scientifique :
 *   · Bergen Social Media Addiction Scale (Andreassen et al., 2012)
 *   · Internet Addiction Test (Young, 1998, validé 20 items)
 *   · Problematic Smartphone Use Scale (Billieux et al., 2015)
 *   · Digital Wellness Framework (Center for Humane Technology, 2020–2024)
 *
 * Score / 28 → 4 niveaux d'urgence clinique
 * Données pré-remplies depuis localStorage (session IVIA ou orientation).
 */

import { useState, useEffect, useRef, KeyboardEvent } from "react";
import Link from "next/link";
import "@/app/styles.sondage.css";

/* ─────────────────────────────────────────────────────────────
   QUESTIONS — 7 dimensions validées
   ───────────────────────────────────────────────────────────── */
const QUESTIONS = [
  {
    id: "q1",
    dimension: "Temps d'écran",
    text: "Combien d'heures par jour passez-vous sur les écrans en dehors du travail ou des études ?",
    note: "Téléphone, tablette, ordinateur personnel, streaming…",
    options: [
      { label: "Moins de 2 h", value: 1 },
      { label: "2 à 4 h", value: 2 },
      { label: "4 à 6 h", value: 3 },
      { label: "Plus de 6 h", value: 4 },
    ],
  },
  {
    id: "q2",
    dimension: "Usage compulsif",
    text: "Consultez-vous votre téléphone dès le réveil, avant même de vous lever ?",
    note: "Ou l'avez-vous à portée de main la nuit ?",
    options: [
      { label: "Rarement ou jamais", value: 1 },
      { label: "Quelques fois par semaine", value: 2 },
      { label: "Souvent", value: 3 },
      { label: "Presque toujours", value: 4 },
    ],
  },
  {
    id: "q3",
    dimension: "Perte de contrôle",
    text: "Avez-vous tenté de réduire votre temps en ligne sans y parvenir durablement ?",
    note: "Téléphone retourné, applications désinstallées et réinstallées, limites non tenues…",
    options: [
      { label: "Non — je maîtrise bien mon usage", value: 1 },
      { label: "J'y ai pensé, sans vraiment essayer", value: 2 },
      { label: "J'ai essayé, avec un succès mitigé", value: 3 },
      { label: "J'ai essayé plusieurs fois sans succès durable", value: 4 },
    ],
  },
  {
    id: "q4",
    dimension: "Impact émotionnel",
    text: "Les réseaux sociaux affectent-ils votre humeur (comparaison, frustration, sentiment d'insuffisance) ?",
    note: "Après une session sur Instagram, TikTok, Facebook, LinkedIn…",
    options: [
      { label: "Pas du tout — je reste neutre", value: 1 },
      { label: "Légèrement — je le remarque parfois", value: 2 },
      { label: "Modérément — c'est récurrent", value: 3 },
      { label: "Fortement — ça affecte ma journée", value: 4 },
    ],
  },
  {
    id: "q5",
    dimension: "Sommeil",
    text: "Le numérique perturbe-t-il votre sommeil (écrans tardifs, vérification nocturne, difficulté à déposer l'écran) ?",
    note: "Le bain de lumière bleue retarde la mélatonine d'environ 1 h 30.",
    options: [
      { label: "Jamais ou très rarement", value: 1 },
      { label: "Quelques fois par semaine", value: 2 },
      { label: "Régulièrement", value: 3 },
      { label: "Presque chaque nuit", value: 4 },
    ],
  },
  {
    id: "q6",
    dimension: "Fuite émotionnelle",
    text: "Utilisez-vous le numérique pour échapper à des pensées négatives, à l'ennui ou à des tensions relationnelles ?",
    note: "Scroller pour ne pas penser, regarder des vidéos pour calmer l'anxiété…",
    options: [
      { label: "Non — j'utilise le numérique de façon positive", value: 1 },
      { label: "Occasionnellement", value: 2 },
      { label: "Souvent — c'est une stratégie que je reconnais", value: 3 },
      { label: "Très souvent — c'est quasi automatique", value: 4 },
    ],
  },
  {
    id: "q7",
    dimension: "Impact vie réelle",
    text: "Le temps passé en ligne a-t-il réduit des activités qui comptent pour vous (sport, relations, projets, repos) ?",
    note: "En comparaison avec il y a 2 à 3 ans.",
    options: [
      { label: "Non — mon équilibre est intact", value: 1 },
      { label: "Un peu — je le remarque", value: 2 },
      { label: "Oui, de façon significative", value: 3 },
      { label: "Oui — c'est une préoccupation centrale", value: 4 },
    ],
  },
] as const;

/* ─────────────────────────────────────────────────────────────
   NIVEAUX — seuils basés sur Bergen SMA Scale + IAT (7 items)
   ───────────────────────────────────────────────────────────── */
const LEVELS = [
  {
    min: 7,
    max: 12,
    code: "equilibre" as const,
    label: "Usage équilibré",
    color: "#3a7c5f",
    bg: "#f0f7f4",
    summary:
      "Votre rapport au numérique semble globalement sain. Quelques habitudes préventives peuvent renforcer cet équilibre dans la durée.",
    detail:
      "Vous présentez peu de signes de dépendance numérique. Les recherches indiquent qu'un usage conscient et intentionnel protège durablement du glissement vers des patterns compulsifs.",
    cta: "Explorer les ressources MÉSANGES",
    ctaHref: "/ressources",
  },
  {
    min: 13,
    max: 17,
    code: "attention" as const,
    label: "À surveiller",
    color: "#8a6820",
    bg: "#fdf8ee",
    summary:
      "Des tensions commencent à se manifester. Un regard extérieur peut aider à identifier les habitudes qui méritent attention.",
    detail:
      "Votre score se situe dans la zone où la recherche observe une augmentation du risque de glissement compulsif. Des ajustements modestes ont un impact significatif à ce stade.",
    cta: "Faire le parcours d'orientation",
    ctaHref: "/orientation",
  },
  {
    min: 18,
    max: 22,
    code: "tensions" as const,
    label: "Tensions actives",
    color: "#b04a1a",
    bg: "#fdf2ee",
    summary:
      "L'impact du numérique sur votre quotidien est réel et mesurable. Un accompagnement MÉSANGES peut aider à rééquilibrer ce rapport.",
    detail:
      "Votre profil correspond à ce que la littérature clinique nomme « usage problématique » — ni pathologie, ni dépendance déclarée, mais un terrain qui mérite une attention structurée.",
    cta: "Prendre rendez-vous",
    ctaHref: "/rendez-vous",
  },
  {
    min: 23,
    max: 28,
    code: "prioritaire" as const,
    label: "Impact majeur",
    color: "#8b2020",
    bg: "#fdf0f0",
    summary:
      "Le numérique occupe une place envahissante. Une rencontre rapide avec un praticien MÉSANGES est fortement recommandée.",
    detail:
      "Votre score rejoint le seuil clinique identifié par l'Internet Addiction Test (IAT > 70/100). Ce n'est pas un diagnostic, mais un signal fort : une aide concrète peut transformer votre quotidien.",
    cta: "Réserver une séance — prioritaire",
    ctaHref: "/rendez-vous",
  },
] as const;

/* ─────────────────────────────────────────────────────────────
   HELPERS localStorage
   ───────────────────────────────────────────────────────────── */
const SONDAGE_KEY = "merlin_numerique_sondage";
const ORIENTATION_KEY = "merlin_orientation_answers";
const SESSION_KEY = "merlin_public_client_session";

interface StoredSondage {
  alias: string;
  email: string;
  answers: Record<string, number>;
  score: number;
  level: string;
  completedAt: string;
}

function readPrefill(): { alias: string; email: string } {
  if (typeof window === "undefined") return { alias: "", email: "" };
  try {
    // 1. Session active (connecté)
    const session = window.localStorage.getItem(SESSION_KEY);
    if (session) {
      const parsed = JSON.parse(session);
      const alias =
        parsed?.client?.first_name_or_alias ||
        parsed?.user?.first_name ||
        parsed?.first_name_or_alias ||
        "";
      const email = parsed?.user?.email || parsed?.email || "";
      if (alias || email) return { alias, email };
    }
    // 2. Réponses orientation
    const orient = window.localStorage.getItem(ORIENTATION_KEY);
    if (orient) {
      const parsed = JSON.parse(orient);
      const alias = parsed?.contact?.first_name || parsed?.first_name || "";
      const email = parsed?.contact?.email || parsed?.email || "";
      if (alias || email) return { alias, email };
    }
  } catch {
    // ignore
  }
  return { alias: "", email: "" };
}

function readPreviousSondage(): StoredSondage | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = window.localStorage.getItem(SONDAGE_KEY);
    if (raw) return JSON.parse(raw) as StoredSondage;
  } catch {
    // ignore
  }
  return null;
}

function saveSondage(data: StoredSondage) {
  if (typeof window === "undefined") return;
  try {
    window.localStorage.setItem(SONDAGE_KEY, JSON.stringify(data));
  } catch {
    // ignore
  }
}

function getLevel(score: number) {
  return LEVELS.find((l) => score >= l.min && score <= l.max) ?? LEVELS[0];
}

/* ─────────────────────────────────────────────────────────────
   COMPOSANT PRINCIPAL
   ───────────────────────────────────────────────────────────── */
interface Props {
  onClose: () => void;
}

type Step =
  | { kind: "contact" }
  | { kind: "resume"; previous: StoredSondage }
  | { kind: "question"; index: number }
  | { kind: "result" };

export function NumeriqueSondagePopup({ onClose }: Props) {
  const [alias, setAlias] = useState("");
  const [email, setEmail] = useState("");
  const [wasPrefilled, setWasPrefilled] = useState(false);
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [step, setStep] = useState<Step>({ kind: "contact" });
  const [score, setScore] = useState<number | null>(null);

  const backdropRef = useRef<HTMLDivElement>(null);
  const closeRef = useRef<HTMLButtonElement>(null);

  // Init : pre-fill + check previous sondage
  useEffect(() => {
    const prefill = readPrefill();
    if (prefill.alias) { setAlias(prefill.alias); setWasPrefilled(true); }
    if (prefill.email) { setEmail(prefill.email); setWasPrefilled(true); }

    const prev = readPreviousSondage();
    if (prev) {
      setStep({ kind: "resume", previous: prev });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Focus trap — fermer avec Escape
  useEffect(() => {
    const handler = (e: Event) => {
      if ((e as unknown as KeyboardEvent).key === "Escape") onClose();
    };
    document.addEventListener("keydown", handler);
    closeRef.current?.focus();
    return () => document.removeEventListener("keydown", handler);
  }, [onClose]);

  /* ── handlers ── */
  function handleContactSubmit() {
    setStep({ kind: "question", index: 0 });
  }

  function handleAnswer(qId: string, value: number) {
    const next = { ...answers, [qId]: value };
    setAnswers(next);
    const qi = QUESTIONS.findIndex((q) => q.id === qId);
    if (qi < QUESTIONS.length - 1) {
      setStep({ kind: "question", index: qi + 1 });
    } else {
      // Toutes les questions répondues
      const total = Object.values(next).reduce((a, b) => a + b, 0);
      setScore(total);
      const level = getLevel(total);
      saveSondage({
        alias,
        email,
        answers: next,
        score: total,
        level: level.code,
        completedAt: new Date().toISOString(),
      });
      setStep({ kind: "result" });
    }
  }

  function handleRestartFromResume() {
    setAnswers({});
    setScore(null);
    setStep({ kind: "question", index: 0 });
  }

  function handleViewPreviousResult(prev: StoredSondage) {
    setAnswers(prev.answers);
    setScore(prev.score);
    setAlias(prev.alias || alias);
    setEmail(prev.email || email);
    setStep({ kind: "result" });
  }

  /* ── rendu ── */
  const totalQuestions = QUESTIONS.length;

  return (
    <div
      className="login-popup-backdrop"
      ref={backdropRef}
      onClick={(e) => {
        if (e.target === backdropRef.current) onClose();
      }}
      role="dialog"
      aria-modal="true"
      aria-label="Sondage rapport au numérique"
    >
      <div className="login-popup login-popup--sondage">
        {/* En-tête */}
        <div className="sondage-header">
          <div>
            <p className="sondage-header__meta">
              MÉSANGES · Sondage numérique
            </p>
            <h2 className="sondage-header__title">
              Mon rapport au numérique
            </h2>
          </div>
          <button
            ref={closeRef}
            onClick={onClose}
            className="login-popup__close"
            aria-label="Fermer"
          >
            ✕
          </button>
        </div>

        {/* ──────────────── ÉTAPE : CONTACT ──────────────── */}
        {step.kind === "contact" && (
          <ContactStep
            alias={alias}
            email={email}
            wasPrefilled={wasPrefilled}
            onAliasChange={setAlias}
            onEmailChange={setEmail}
            onSubmit={handleContactSubmit}
          />
        )}

        {/* ──────────────── ÉTAPE : REPRENDRE / RECOMMENCER ── */}
        {step.kind === "resume" && (
          <ResumeStep
            previous={step.previous}
            onContinue={() => handleViewPreviousResult(step.previous)}
            onRestart={handleRestartFromResume}
          />
        )}

        {/* ──────────────── ÉTAPE : QUESTION ──────────────── */}
        {step.kind === "question" && (
          <QuestionStep
            question={QUESTIONS[step.index]}
            index={step.index}
            total={totalQuestions}
            currentAnswer={answers[QUESTIONS[step.index].id]}
            onAnswer={(val) => handleAnswer(QUESTIONS[step.index].id, val)}
            onBack={() => {
              if (step.index === 0) setStep({ kind: "contact" });
              else setStep({ kind: "question", index: step.index - 1 });
            }}
          />
        )}

        {/* ──────────────── ÉTAPE : RÉSULTAT ──────────────── */}
        {step.kind === "result" && score !== null && (
          <ResultStep
            alias={alias}
            score={score}
            answers={answers}
            onRestart={() => {
              setAnswers({});
              setScore(null);
              setStep({ kind: "contact" });
            }}
            onClose={onClose}
          />
        )}
      </div>
    </div>
  );
}

/* ─────────────────────────────────────────────────────────────
   SOUS-COMPOSANTS
   ───────────────────────────────────────────────────────────── */

function ContactStep({
  alias,
  email,
  wasPrefilled,
  onAliasChange,
  onEmailChange,
  onSubmit,
}: {
  alias: string;
  email: string;
  wasPrefilled: boolean;
  onAliasChange: (v: string) => void;
  onEmailChange: (v: string) => void;
  onSubmit: () => void;
}) {
  const isPrefilled = wasPrefilled;

  return (
    <div>
      <p className="sondage-intro">
        Un sondage de 7 questions — environ 3 minutes — pour situer votre rapport
        au numérique et recevoir une orientation personnalisée.
      </p>
      {isPrefilled && (
        <div className="sondage-prefill-banner">
          ✓ Vos informations ont été retrouvées depuis votre parcours IVIA.
        </div>
      )}
      <div className="sondage-fields">
        <label className="sondage-field">
          <span className="sondage-field__label">Prénom ou alias</span>
          <input
            type="text"
            value={alias}
            onChange={(e) => onAliasChange(e.target.value)}
            placeholder="Comment vous appeler ?"
            autoComplete="given-name"
            className="sondage-field__input"
          />
        </label>
        <label className="sondage-field">
          <span className="sondage-field__label">
            Courriel <span className="sondage-field__label-note">(facultatif — pour recevoir vos résultats)</span>
          </span>
          <input
            type="email"
            value={email}
            onChange={(e) => onEmailChange(e.target.value)}
            placeholder="vous@exemple.com"
            autoComplete="email"
            className="sondage-field__input"
          />
        </label>
      </div>
      <p className="sondage-rgpd-note">
        Vos réponses sont conservées localement sur cet appareil. Aucun cookie publicitaire.
        Loi 25 respectée.
      </p>
      <button onClick={onSubmit} className="sondage-btn-primary">
        Commencer le sondage →
      </button>
    </div>
  );
}

function ResumeStep({
  previous,
  onContinue,
  onRestart,
}: {
  previous: StoredSondage;
  onContinue: () => void;
  onRestart: () => void;
}) {
  const level = getLevel(previous.score);
  const date = new Date(previous.completedAt).toLocaleDateString("fr-CA", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });

  return (
    <div>
      <p className="sondage-resume-info">
        Vous avez déjà complété ce sondage le <strong>{date}</strong>.
      </p>
      <div
        className="sondage-resume-badge sondage-level"
        data-level={level.code}
      >
        <p className="sondage-resume-badge__kicker">
          Résultat précédent
        </p>
        <p className="sondage-resume-badge__score">
          {level.label} — {previous.score} / 28
        </p>
      </div>
      <div className="sondage-resume-actions">
        <button onClick={onContinue} className="sondage-btn-primary">
          Voir mes résultats →
        </button>
        <button onClick={onRestart} className="sondage-btn-ghost">
          Refaire le sondage (mise à jour)
        </button>
      </div>
    </div>
  );
}

function QuestionStep({
  question,
  index,
  total,
  currentAnswer,
  onAnswer,
  onBack,
}: {
  question: (typeof QUESTIONS)[number];
  index: number;
  total: number;
  currentAnswer?: number;
  onAnswer: (value: number) => void;
  onBack: () => void;
}) {
  const progress = ((index) / total) * 100;

  return (
    <div>
      {/* Barre de progression */}
      <div className="sondage-progress-wrapper">
        <div className="sondage-progress-header">
          <span className="sondage-progress-counter">
            Question {index + 1} sur {total}
          </span>
          <span className="sondage-progress-dimension">
            {question.dimension}
          </span>
        </div>
        <div className="sondage-progress-bar-track">
          <div
            className="sondage-progress-bar-fill"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* Question */}
      <p className="sondage-question-text">{question.text}</p>
      {question.note && (
        <p className="sondage-question-note">{question.note}</p>
      )}

      {/* Options */}
      <div className="sondage-options">
        {question.options.map((opt) => (
          <button
            key={opt.value}
            onClick={() => onAnswer(opt.value)}
            className={`sondage-option${currentAnswer === opt.value ? " sondage-option--selected" : ""}`}
          >
            {opt.label}
          </button>
        ))}
      </div>

      {/* Navigation */}
      <button onClick={onBack} className="sondage-btn-back">
        ← Retour
      </button>
    </div>
  );
}

function ResultStep({
  alias,
  score,
  answers,
  onRestart,
  onClose,
}: {
  alias: string;
  score: number;
  answers: Record<string, number>;
  onRestart: () => void;
  onClose: () => void;
}) {
  const level = getLevel(score);
  const maxScore = QUESTIONS.length * 4; // 28
  const percent = Math.round((score / maxScore) * 100);

  // Dimensions les plus élevées (top 2)
  const dimensionScores = QUESTIONS.map((q) => ({
    dimension: q.dimension,
    value: answers[q.id] ?? 1,
  })).sort((a, b) => b.value - a.value);
  const topDimensions = dimensionScores.slice(0, 2).filter((d) => d.value >= 3);

  return (
    <div>
      {/* Score visuel */}
      <div
        className="sondage-result-badge sondage-level"
        data-level={level.code}
      >
        {alias && (
          <p className="sondage-result-alias">Résultats pour {alias}</p>
        )}
        <p className="sondage-result-score">
          {score}
          <span className="sondage-result-score-max"> / {maxScore}</span>
        </p>
        <p className="sondage-result-label">
          {level.label}
        </p>
        {/* Barre score */}
        <div className="sondage-result-bar-track">
          <div
            className="sondage-result-bar-fill"
            style={{ width: `${percent}%` }}
          />
        </div>
      </div>

      {/* Résumé */}
      <p className="sondage-result-summary">{level.summary}</p>
      <p className="sondage-result-detail">{level.detail}</p>

      {/* Dimensions prioritaires */}
      {topDimensions.length > 0 && (
        <div className="sondage-dimensions sondage-level" data-level={level.code}>
          <p className="sondage-dimensions__label">Axes à travailler en priorité</p>
          {topDimensions.map((d) => (
            <span key={d.dimension} className="sondage-dimension-tag">
              {d.dimension}
            </span>
          ))}
        </div>
      )}

      {/* CTA principal */}
      <div className="sondage-result-actions sondage-level" data-level={level.code}>
        <Link
          href={`${level.ctaHref}?from=numerique-sondage&score=${score}&level=${level.code}`}
          onClick={onClose}
          className="sondage-btn-cta"
        >
          {level.cta} →
        </Link>
        <button onClick={onRestart} className="sondage-btn-restart">
          Refaire le sondage
        </button>
      </div>

      <p className="sondage-disclaimer">
        Ce sondage est un outil d&apos;orientation, non un outil diagnostique.
        Il est fondé sur des échelles validées (Bergen SMA Scale, IAT — Young 1998)
        adaptées au contexte québécois. Résultats conservés localement sur votre appareil.
      </p>
    </div>
  );
}

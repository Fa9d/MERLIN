"use client";

/* ──────────────────────────────────────────────────────────────────────────
   OrientationFlow — Parcours d'orientation public IVIA
   Composant mobile-first, une question à la fois, barre de progression,
   choix multiples + champ texte facultatif, portrait final non médical.
   Aucune donnée n'est persistée (pas de localStorage / sessionStorage).
   ────────────────────────────────────────────────────────────────────────── */

import { useMemo, useState } from "react";
import Link from "next/link";
import {
  Answers,
  VoieKey,
  buildPortrait,
  buildSteps,
  Step,
} from "@/data/orientationFlow";

type FlowState = {
  index: number;
  answers: Answers;
  done: boolean;
};

const INITIAL: FlowState = { index: 0, answers: {}, done: false };

function isAnswered(step: Step, answers: Answers): boolean {
  const raw = answers[step.id];
  if (step.optional) return true;
  if (step.kind === "multi") {
    return Array.isArray(raw) && raw.length > 0;
  }
  if (step.kind === "text") {
    return typeof raw === "string" && raw.trim().length > 0;
  }
  return typeof raw === "string" && raw.length > 0;
}

export function OrientationFlow() {
  const [state, setState] = useState<FlowState>(INITIAL);

  const voie = (state.answers.voie as VoieKey | undefined) ?? null;
  const steps = useMemo(() => buildSteps(voie), [voie]);
  const currentStep = steps[state.index];
  const portrait = state.done ? buildPortrait(state.answers) : null;
  const progress = state.done
    ? 100
    : Math.round(((state.index + 1) / Math.max(steps.length, 1)) * 100);

  function setAnswer(stepId: string, value: string | string[]) {
    setState((s) => ({ ...s, answers: { ...s.answers, [stepId]: value } }));
  }

  function toggleMulti(stepId: string, optionId: string) {
    setState((s) => {
      const current = (s.answers[stepId] as string[]) ?? [];
      const next = current.includes(optionId)
        ? current.filter((x) => x !== optionId)
        : [...current, optionId];
      return { ...s, answers: { ...s.answers, [stepId]: next } };
    });
  }

  function goNext() {
    setState((s) => {
      const last = s.index >= steps.length - 1;
      if (last) return { ...s, done: true };
      return { ...s, index: s.index + 1 };
    });
  }

  function goBack() {
    setState((s) => {
      if (s.done) return { ...s, done: false };
      return { ...s, index: Math.max(0, s.index - 1) };
    });
  }

  function reset() {
    setState(INITIAL);
  }

  /* ── Résultat ───────────────────────────────────────────────────────── */
  if (state.done && portrait) {
    return (
      <div className="of of--portrait" data-testid="orientation-portrait">
        <div className="of__inner">
          <p className="of__kicker">Votre portrait d&apos;orientation</p>
          <h3 className="of__h3">
            {portrait.phrase.split(".")[0]}
            <span aria-hidden="true">.</span>
          </h3>
          <p className="of__lede">{portrait.phrase}</p>

          {portrait.urgent ? (
            <div
              className="of__urgent"
              role="alert"
              data-testid="orientation-urgent"
            >
              <strong>Si vous traversez une crise immédiate.</strong> IVIA
              n&apos;est pas un service d&apos;urgence. Au Canada, appelez ou
              textez le <strong>988</strong>, ou composez le <strong>911</strong> en
              cas de danger immédiat. Vous pouvez aussi joindre Info-Social au{" "}
              <strong>811</strong>.
            </div>
          ) : null}

          <ol className="of__layers" aria-label="Trois couches prioritaires">
            {portrait.layers.map((l, i) => (
              <li key={l.key} className={`of__layer of__layer--${l.key}`}>
                <span className="of__layer-num">
                  {String(i + 1).padStart(2, "0")}
                </span>
                <span className="of__layer-label">{l.label}</span>
              </li>
            ))}
          </ol>

          <p className="of__disclaimer">
            Ce portrait n&apos;est pas un diagnostic. Il sert à préparer une
            conversation et à orienter la suite.
          </p>

          <div className="of__cta-row">
            <Link
              href={portrait.cta.href}
              className={`of__cta of__cta--${portrait.cta.tone}`}
              data-testid="orientation-cta"
            >
              {portrait.cta.label}
              <span className="of__cta-arrow" aria-hidden="true">
                →
              </span>
            </Link>
            <button
              type="button"
              className="of__ghost"
              onClick={reset}
              data-testid="orientation-restart"
            >
              Reprendre depuis le début
            </button>
          </div>

          <p className="of__cta-hint">{portrait.cta.hint}</p>
        </div>
      </div>
    );
  }

  if (!currentStep) return null;

  const answered = isAnswered(currentStep, state.answers);

  return (
    <div className="of" data-testid="orientation-flow">
      <div className="of__inner">
        <div
          className="of__progress"
          aria-label="Progression du parcours d'orientation"
        >
          <div
            className="of__progress-bar"
            style={{ width: `${progress}%` }}
            role="progressbar"
            aria-valuenow={progress}
            aria-valuemin={0}
            aria-valuemax={100}
          />
          <span className="of__progress-label">
            Étape {state.index + 1} sur {steps.length}
          </span>
        </div>

        <fieldset className="of__step">
          <legend className="of__question">{currentStep.question}</legend>
          {currentStep.helper ? (
            <p className="of__helper">{currentStep.helper}</p>
          ) : null}

          {currentStep.kind === "single" || currentStep.kind === "intensity" ? (
            <ul className="of__options">
              {(currentStep.options ?? []).map((opt) => {
                const selected = state.answers[currentStep.id] === opt.id;
                return (
                  <li key={opt.id}>
                    <button
                      type="button"
                      className={`of__option${
                        selected ? " of__option--selected" : ""
                      }`}
                      onClick={() => setAnswer(currentStep.id, opt.id)}
                      data-testid={`orientation-option-${opt.id}`}
                      aria-pressed={selected}
                    >
                      <span className="of__option-label">{opt.label}</span>
                      {opt.hint ? (
                        <span className="of__option-hint">{opt.hint}</span>
                      ) : null}
                    </button>
                  </li>
                );
              })}
            </ul>
          ) : null}

          {currentStep.kind === "multi" ? (
            <ul className="of__options of__options--multi">
              {(currentStep.options ?? []).map((opt) => {
                const current =
                  (state.answers[currentStep.id] as string[]) ?? [];
                const selected = current.includes(opt.id);
                return (
                  <li key={opt.id}>
                    <button
                      type="button"
                      className={`of__option of__option--multi${
                        selected ? " of__option--selected" : ""
                      }`}
                      onClick={() => toggleMulti(currentStep.id, opt.id)}
                      data-testid={`orientation-option-${opt.id}`}
                      aria-pressed={selected}
                    >
                      <span
                        className="of__check"
                        aria-hidden="true"
                        data-checked={selected ? "true" : "false"}
                      />
                      <span className="of__option-label">{opt.label}</span>
                    </button>
                  </li>
                );
              })}
            </ul>
          ) : null}

          {currentStep.kind === "text" ? (
            <label className="of__textwrap">
              <span className="of__textlabel">
                Précisez dans vos mots
                <span className="of__textmeta"> · facultatif</span>
              </span>
              <textarea
                className="of__textarea"
                placeholder={currentStep.placeholder}
                rows={4}
                value={(state.answers[currentStep.id] as string) ?? ""}
                onChange={(e) => setAnswer(currentStep.id, e.target.value)}
                data-testid="orientation-textarea"
                maxLength={1200}
              />
            </label>
          ) : null}
        </fieldset>

        <div className="of__nav">
          <button
            type="button"
            className="of__ghost"
            onClick={goBack}
            disabled={state.index === 0}
            data-testid="orientation-back"
          >
            Revenir
          </button>
          <button
            type="button"
            className="of__next"
            onClick={goNext}
            disabled={!answered}
            data-testid="orientation-next"
          >
            {state.index >= steps.length - 1
              ? "Voir mon portrait"
              : "Continuer"}
            <span className="of__cta-arrow" aria-hidden="true">
              →
            </span>
          </button>
        </div>

        <p className="of__privacy">
          Vos réponses restent dans cette fenêtre. Aucune donnée n&apos;est
          enregistrée tant que vous n&apos;avez pas ouvert un espace privé.
        </p>
      </div>
    </div>
  );
}

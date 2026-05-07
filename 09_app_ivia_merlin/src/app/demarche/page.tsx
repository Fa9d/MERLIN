"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";
import { PublicLayout } from "@/components/layout/PublicLayout";
import {
  createClient,
  createIntakeRequest,
} from "@/lib/merlin-api";

// ─── Types locaux ────────────────────────────────────────────────────────────

type Step = "besoin" | "identite" | "confirmation";

type BesoinForm = {
  request_for_code: "self" | "relative" | "other";
  primary_need_code:
    | "clarification"
    | "support"
    | "orientation"
    | "loneliness"
    | "distress"
    | "other";
  perceived_urgency_code: "non_urgent" | "watch" | "priority" | "urgent";
  support_already_in_place: boolean;
  requested_outcome_text: string;
};

type IdentiteForm = {
  first_name_or_alias: string;
  email: string;
};

// ─── Libellés Mésange (ton posé, pas clinique) ───────────────────────────────

const POUR_QUI_OPTIONS: { value: BesoinForm["request_for_code"]; label: string; desc: string }[] = [
  { value: "self",     label: "Pour moi",          desc: "Je souhaite un espace pour moi." },
  { value: "relative", label: "Pour un proche",     desc: "Je cherche un appui pour quelqu'un que j'accompagne." },
  { value: "other",    label: "Pour une situation", desc: "Il y a une situation que je veux mieux comprendre." },
];

const BESOIN_OPTIONS: { value: BesoinForm["primary_need_code"]; label: string }[] = [
  { value: "clarification", label: "Mettre de l'ordre dans ce que je vis" },
  { value: "support",       label: "Sentir que je ne suis pas seul·e" },
  { value: "orientation",   label: "Savoir vers où me tourner" },
  { value: "loneliness",    label: "Sortir d'un isolement" },
  { value: "distress",      label: "Traverser un moment difficile" },
  { value: "other",         label: "Autre chose" },
];

const URGENCE_OPTIONS: { value: BesoinForm["perceived_urgency_code"]; label: string; desc: string }[] = [
  { value: "non_urgent", label: "Pas urgent",      desc: "Je prends le temps d'y aller à mon rythme." },
  { value: "watch",      label: "À surveiller",    desc: "Je préfère ne pas attendre trop longtemps." },
  { value: "priority",   label: "Assez urgent",    desc: "La situation me pèse et j'ai besoin d'un espace bientôt." },
  { value: "urgent",     label: "Urgent",          desc: "J'ai besoin d'aide rapidement." },
];

// ─── Composant principal ─────────────────────────────────────────────────────

export default function DemarchePage() {
  const [step, setStep] = useState<Step>("besoin");

  const [besoin, setBesoin] = useState<BesoinForm>({
    request_for_code:          "self",
    primary_need_code:         "clarification",
    perceived_urgency_code:    "non_urgent",
    support_already_in_place:  false,
    requested_outcome_text:    "",
  });

  const [identite, setIdentite] = useState<IdentiteForm>({
    first_name_or_alias: "",
    email: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState<string | null>(null);

  // ── Soumission finale ──────────────────────────────────────────────────────

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    if (!identite.first_name_or_alias.trim()) {
      setError("Merci d'indiquer un prénom ou un alias pour continuer.");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // 1. Créer le profil client (sans auth — endpoint public)
      const client = await createClient({
        first_name_or_alias: identite.first_name_or_alias.trim(),
        email: identite.email.trim() || null,
        language_code: "fr",
        territory_code: "QC",
        is_adult_confirmed: true,
      });

      // 2. Soumettre la demande d'entrée
      await createIntakeRequest({
        client_id:                  client.id,
        request_channel_code:       "web",
        request_for_code:           besoin.request_for_code,
        primary_need_code:          besoin.primary_need_code,
        perceived_urgency_code:     besoin.perceived_urgency_code,
        support_already_in_place:   besoin.support_already_in_place,
        requested_outcome_text:     besoin.requested_outcome_text.trim() || null,
      });

      setStep("confirmation");
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Une erreur est survenue. Veuillez réessayer."
      );
    } finally {
      setLoading(false);
    }
  }

  // ── Rendu ──────────────────────────────────────────────────────────────────

  return (
    <PublicLayout title="Votre démarche — IVIA">
      <main className="hp-section">
        <div className="hp-section__inner" style={{ maxWidth: "640px" }}>

          {/* ── Étape 1 : Besoin ─────────────────────────────────────────── */}
          {step === "besoin" && (
            <div>
              <p className="hp-kicker">Votre démarche</p>
              <h1 className="hp-h2" style={{ marginBottom: "0.5rem" }}>
                Ce qui vous amène
              </h1>
              <p style={{ color: "var(--ink-soft)", marginBottom: "2rem", lineHeight: 1.6 }}>
                Quelques questions pour mieux comprendre où vous en êtes.
                Il n&apos;y a pas de bonne ou de mauvaise réponse.
              </p>

              {/* Pour qui */}
              <fieldset style={fieldsetStyle}>
                <legend style={legendStyle}>Cette démarche, c&apos;est…</legend>
                <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
                  {POUR_QUI_OPTIONS.map((opt) => (
                    <label key={opt.value} style={radioCardStyle(besoin.request_for_code === opt.value)}>
                      <input
                        type="radio"
                        name="request_for_code"
                        value={opt.value}
                        checked={besoin.request_for_code === opt.value}
                        onChange={() => setBesoin((b) => ({ ...b, request_for_code: opt.value }))}
                        style={{ marginRight: "0.75rem", accentColor: "var(--sage)" }}
                      />
                      <span>
                        <strong>{opt.label}</strong>
                        <span style={{ display: "block", fontSize: "0.875rem", color: "var(--ink-soft)", marginTop: "0.125rem" }}>
                          {opt.desc}
                        </span>
                      </span>
                    </label>
                  ))}
                </div>
              </fieldset>

              {/* Ce qui vous amène */}
              <fieldset style={fieldsetStyle}>
                <legend style={legendStyle}>Ce qui vous amène principalement</legend>
                <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
                  {BESOIN_OPTIONS.map((opt) => (
                    <label key={opt.value} style={radioCardStyle(besoin.primary_need_code === opt.value)}>
                      <input
                        type="radio"
                        name="primary_need_code"
                        value={opt.value}
                        checked={besoin.primary_need_code === opt.value}
                        onChange={() => setBesoin((b) => ({ ...b, primary_need_code: opt.value }))}
                        style={{ marginRight: "0.75rem", accentColor: "var(--sage)" }}
                      />
                      {opt.label}
                    </label>
                  ))}
                </div>
              </fieldset>

              {/* Urgence */}
              <fieldset style={fieldsetStyle}>
                <legend style={legendStyle}>Comment vous situez-vous par rapport à l&apos;urgence&nbsp;?</legend>
                <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
                  {URGENCE_OPTIONS.map((opt) => (
                    <label key={opt.value} style={radioCardStyle(besoin.perceived_urgency_code === opt.value)}>
                      <input
                        type="radio"
                        name="perceived_urgency_code"
                        value={opt.value}
                        checked={besoin.perceived_urgency_code === opt.value}
                        onChange={() => setBesoin((b) => ({ ...b, perceived_urgency_code: opt.value }))}
                        style={{ marginRight: "0.75rem", accentColor: "var(--sage)" }}
                      />
                      <span>
                        <strong>{opt.label}</strong>
                        <span style={{ display: "block", fontSize: "0.875rem", color: "var(--ink-soft)", marginTop: "0.125rem" }}>
                          {opt.desc}
                        </span>
                      </span>
                    </label>
                  ))}
                </div>
              </fieldset>

              {/* Suivi en place */}
              <fieldset style={fieldsetStyle}>
                <legend style={legendStyle}>Avez-vous déjà un suivi en place&nbsp;?</legend>
                <div style={{ display: "flex", gap: "1rem" }}>
                  {[
                    { val: false, label: "Non" },
                    { val: true,  label: "Oui" },
                  ].map(({ val, label }) => (
                    <label key={String(val)} style={radioCardStyle(besoin.support_already_in_place === val)}>
                      <input
                        type="radio"
                        name="support_already_in_place"
                        checked={besoin.support_already_in_place === val}
                        onChange={() => setBesoin((b) => ({ ...b, support_already_in_place: val }))}
                        style={{ marginRight: "0.5rem", accentColor: "var(--sage)" }}
                      />
                      {label}
                    </label>
                  ))}
                </div>
              </fieldset>

              {/* Ce que vous souhaitez en sortir */}
              <div style={{ marginBottom: "2rem" }}>
                <label style={legendStyle} htmlFor="requested_outcome_text">
                  Ce que vous aimeriez retrouver en sortant d&apos;ici{" "}
                  <span style={{ color: "var(--ink-soft)", fontWeight: 400 }}>(facultatif)</span>
                </label>
                <textarea
                  id="requested_outcome_text"
                  className="hp-input"
                  rows={3}
                  placeholder="Un mot, une image, une phrase…"
                  value={besoin.requested_outcome_text}
                  onChange={(e) => setBesoin((b) => ({ ...b, requested_outcome_text: e.target.value }))}
                  style={{ width: "100%", resize: "vertical", marginTop: "0.5rem" }}
                />
              </div>

              {/* Navigation */}
              <div style={{ display: "flex", justifyContent: "flex-end" }}>
                <button
                  type="button"
                  className="hp-btn hp-btn--primary"
                  onClick={() => setStep("identite")}
                >
                  Continuer →
                </button>
              </div>

              {/* Note urgence */}
              {(besoin.perceived_urgency_code === "urgent") && (
                <p style={{ marginTop: "1.5rem", fontSize: "0.875rem", color: "var(--ink-soft)", lineHeight: 1.6, padding: "1rem", background: "var(--sage-light)", borderRadius: "6px" }}>
                  Si vous traversez une crise ou un danger immédiat, composez le{" "}
                  <strong>811</strong> (Info-Social),{" "}
                  <strong>1&nbsp;866&nbsp;APPELLE</strong> (prévention du suicide)
                  {" "}ou le <strong>911</strong>.
                  IVIA n&apos;est pas équipée pour recevoir les situations d&apos;urgence.
                </p>
              )}
            </div>
          )}

          {/* ── Étape 2 : Identité ───────────────────────────────────────── */}
          {step === "identite" && (
            <form onSubmit={handleSubmit}>
              <p className="hp-kicker">Votre démarche</p>
              <h1 className="hp-h2" style={{ marginBottom: "0.5rem" }}>
                Pour vous retrouver
              </h1>
              <p style={{ color: "var(--ink-soft)", marginBottom: "2rem", lineHeight: 1.6 }}>
                Un prénom ou un alias suffit. Le courriel est utile si vous souhaitez
                recevoir un suivi — il n&apos;est pas obligatoire.
              </p>

              <div style={{ marginBottom: "1.5rem" }}>
                <label style={legendStyle} htmlFor="first_name_or_alias">
                  Prénom ou alias <span style={{ color: "var(--sage)" }}>*</span>
                </label>
                <input
                  id="first_name_or_alias"
                  type="text"
                  className="hp-input"
                  placeholder="Ex. : Marie, M., ou simplement « quelqu'un »"
                  value={identite.first_name_or_alias}
                  onChange={(e) =>
                    setIdentite((i) => ({ ...i, first_name_or_alias: e.target.value }))
                  }
                  required
                  autoFocus
                  style={{ width: "100%", marginTop: "0.5rem" }}
                />
              </div>

              <div style={{ marginBottom: "2rem" }}>
                <label style={legendStyle} htmlFor="email">
                  Courriel{" "}
                  <span style={{ color: "var(--ink-soft)", fontWeight: 400 }}>(facultatif)</span>
                </label>
                <input
                  id="email"
                  type="email"
                  className="hp-input"
                  placeholder="votre@courriel.com"
                  value={identite.email}
                  onChange={(e) =>
                    setIdentite((i) => ({ ...i, email: e.target.value }))
                  }
                  style={{ width: "100%", marginTop: "0.5rem" }}
                />
                <p style={{ fontSize: "0.8125rem", color: "var(--ink-soft)", marginTop: "0.375rem" }}>
                  Utilisé uniquement pour vous transmettre un résumé ou une suggestion.
                </p>
              </div>

              {error && (
                <p role="alert" style={{ color: "var(--earth)", marginBottom: "1rem", fontSize: "0.9rem" }}>
                  {error}
                </p>
              )}

              <div style={{ display: "flex", gap: "1rem", justifyContent: "space-between" }}>
                <button
                  type="button"
                  className="hp-btn hp-btn--secondary"
                  onClick={() => { setStep("besoin"); setError(null); }}
                >
                  ← Retour
                </button>
                <button
                  type="submit"
                  className="hp-btn hp-btn--primary"
                  disabled={loading}
                >
                  {loading ? "Envoi en cours…" : "Soumettre ma démarche"}
                </button>
              </div>
            </form>
          )}

          {/* ── Étape 3 : Confirmation ───────────────────────────────────── */}
          {step === "confirmation" && (
            <div style={{ textAlign: "center", paddingBlock: "3rem" }}>
              <div style={{ fontSize: "2.5rem", marginBottom: "1rem" }} aria-hidden="true">
                ✦
              </div>
              <p className="hp-kicker">Reçu</p>
              <h1 className="hp-h2" style={{ marginBottom: "1rem" }}>
                Votre démarche est enregistrée.
              </h1>
              <p style={{ color: "var(--ink-soft)", lineHeight: 1.7, marginBottom: "2rem", maxWidth: "480px", marginInline: "auto" }}>
                Un praticien vous sera suggéré sous peu.
                Si vous avez laissé un courriel, vous recevrez la suggestion directement.
                Sinon, revenez ici avec votre alias pour retrouver votre espace.
              </p>
              <div style={{ display: "flex", gap: "1rem", justifyContent: "center", flexWrap: "wrap" }}>
                <Link href="/ressources" className="hp-btn hp-btn--secondary">
                  Lire nos ressources
                </Link>
                <Link href="/" className="hp-btn hp-btn--primary">
                  Retour à l&apos;accueil
                </Link>
              </div>
            </div>
          )}

        </div>
      </main>
    </PublicLayout>
  );
}

// ─── Helpers styles inline ───────────────────────────────────────────────────

const fieldsetStyle: React.CSSProperties = {
  border: "none",
  padding: 0,
  marginBottom: "2rem",
};

const legendStyle: React.CSSProperties = {
  display: "block",
  fontWeight: 600,
  fontSize: "0.9375rem",
  color: "var(--ink)",
  marginBottom: "0.75rem",
};

function radioCardStyle(selected: boolean): React.CSSProperties {
  return {
    display: "flex",
    alignItems: "flex-start",
    padding: "0.75rem 1rem",
    borderRadius: "6px",
    border: `1.5px solid ${selected ? "var(--sage)" : "var(--border-soft)"}`,
    background: selected ? "var(--sage-light)" : "transparent",
    cursor: "pointer",
    transition: "border-color 0.15s, background 0.15s",
    fontSize: "0.9375rem",
    color: "var(--ink)",
    lineHeight: 1.4,
  };
}

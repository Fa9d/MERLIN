"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";

import { createClient, createConsent, createIntakeRequest } from "@/lib/merlin-api";

type SubmissionState = {
  clientCode: string;
  intakeId: string;
};

export default function RendezVousPage() {
  const [firstNameOrAlias, setFirstNameOrAlias] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [isAdultConfirmed, setIsAdultConfirmed] = useState(false);
  const [sessionConsent, setSessionConsent] = useState(false);
  const [sessionNoteConsent, setSessionNoteConsent] = useState(false);
  const [historyConsent, setHistoryConsent] = useState(false);
  const [need, setNeed] = useState<
    "clarification" | "support" | "orientation" | "loneliness" | "distress" | "other"
  >("support");
  const [requestText, setRequestText] = useState("");
  const [supportInPlace, setSupportInPlace] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [submissionState, setSubmissionState] = useState<SubmissionState | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSubmitting(true);
    setErrorMessage(null);
    setSubmissionState(null);

    if (!isAdultConfirmed) {
      setErrorMessage("La demande est reservee aux adultes de 18 ans et plus.");
      setIsSubmitting(false);
      return;
    }

    if (!sessionConsent || !sessionNoteConsent) {
      setErrorMessage("Les consentements de seance et de note sont requis pour continuer.");
      setIsSubmitting(false);
      return;
    }

    try {
      const client = await createClient({
        first_name_or_alias: firstNameOrAlias.trim(),
        email: email.trim() || null,
        phone: phone.trim() || null,
        is_adult_confirmed: isAdultConfirmed,
      });

      const intake = await createIntakeRequest({
        client_id: client.id,
        request_channel_code: "web_form",
        request_for_code: "self",
        primary_need_code: need,
        perceived_urgency_code: "non_urgent",
        support_already_in_place: supportInPlace,
        requested_outcome_text: requestText.trim() || null,
      });

      await Promise.all([
        createConsent({
          client_id: client.id,
          consent_type_code: "consent_session",
          consent_value: sessionConsent,
          granted_by_actor_code: "client",
        }),
        createConsent({
          client_id: client.id,
          consent_type_code: "consent_session_note",
          consent_value: sessionNoteConsent,
          granted_by_actor_code: "client",
        }),
        createConsent({
          client_id: client.id,
          consent_type_code: "consent_history",
          consent_value: historyConsent,
          granted_by_actor_code: "client",
        }),
      ]);

      setSubmissionState({
        clientCode: client.public_client_code,
        intakeId: intake.id,
      });
      setFirstNameOrAlias("");
      setEmail("");
      setPhone("");
      setIsAdultConfirmed(false);
      setSessionConsent(false);
      setSessionNoteConsent(false);
      setHistoryConsent(false);
      setNeed("support");
      setRequestText("");
      setSupportInPlace(false);
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Erreur inconnue.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="page-shell">
      <header className="topbar">
        <div className="wordmark">IVIA</div>
        <nav className="nav">
          <Link href="/">Accueil</Link>
        </nav>
      </header>

      <main className="section">
        <div className="section-header">
          <div className="eyebrow">Premiere seance</div>
          <h2>Vous avez fait un pas important en decidant d&apos;en parler.</h2>
          <p>
            Prenez quelques minutes pour nous dire ou vous en etes. Pas de jugement.
            Pas de case a cocher parfaitement. Juste ce qui vous ressemble.
          </p>
        </div>

        <div className="grid intake-layout">
          <article className="card stack-md">
            <h3>Avant de commencer</h3>
            <ul>
              <li>IVIA s&apos;adresse aux adultes hors situation d&apos;urgence immediate.</li>
              <li>Le but est de vous offrir un espace d&apos;ecoute, de clarte et de suite concrete.</li>
              <li>Votre demande est enregistree pour etre reprise dans le cadre IVIA.</li>
            </ul>
            <div className="info-strip">
              <span>65 $</span>
              <span>60 a 75 min</span>
              <span>En ligne</span>
            </div>
            <p className="inline-note">
              Les echanges sont traites avec confidentialite, dans les limites
              prevues par la loi.
            </p>
          </article>

          <form className="card form-stack" onSubmit={handleSubmit}>
            <label className="field">
              <span>Comment souhaitez-vous etre appele ?</span>
              <input
                required
                value={firstNameOrAlias}
                onChange={(event) => setFirstNameOrAlias(event.target.value)}
                placeholder="Prenom ou alias"
              />
            </label>
            <p className="inline-note">Vous pouvez utiliser un prenom fictif si vous preferez.</p>

            <div className="form-grid-2">
              <label className="field">
                <span>Courriel</span>
                <input
                  type="email"
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  placeholder="nom@exemple.com"
                />
              </label>

              <label className="field">
                <span>Telephone</span>
                <input
                  value={phone}
                  onChange={(event) => setPhone(event.target.value)}
                  placeholder="514 000 0000"
                />
              </label>
            </div>

            <label className="checkbox-row">
              <input
                type="checkbox"
                checked={isAdultConfirmed}
                onChange={(event) => setIsAdultConfirmed(event.target.checked)}
              />
              <span>Je confirme etre majeur (18 ans et plus).</span>
            </label>

            <label className="field">
              <span>En ce moment, vous cherchez plutot...</span>
              <select value={need} onChange={(event) => setNeed(event.target.value as typeof need)}>
                <option value="support">Parler de ce qui se passe et etre entendu</option>
                <option value="clarification">Comprendre ce que vous ressentez</option>
                <option value="orientation">Savoir vers ou vous tourner</option>
                <option value="loneliness">Sortir de la solitude</option>
                <option value="distress">Dire une detresse qui monte</option>
                <option value="other">Autre chose</option>
              </select>
            </label>

            <label className="field">
              <span>En quelques phrases, decrivez ce qui vous amene.</span>
              <textarea
                rows={5}
                value={requestText}
                onChange={(event) => setRequestText(event.target.value)}
                placeholder="Decrivez en quelques phrases ce que vous vivez, ce qui vous pese ou ce que vous aimeriez comprendre."
              />
            </label>
            <p className="inline-note">
              Exemple: Je n&apos;arrive plus a dormir, je me sens depasse par ma
              situation familiale et je ne sais pas par ou commencer.
            </p>

            <label className="checkbox-row">
              <input
                type="checkbox"
                checked={supportInPlace}
                onChange={(event) => setSupportInPlace(event.target.checked)}
              />
              <span>Un autre soutien est deja en place</span>
            </label>
            <p className="inline-note">
              Cette information nous aide a mieux comprendre ou vous en etes. Elle
              ne change pas votre acces au service.
            </p>

            <div className="stack-sm">
              <h3>Consentements de base</h3>
              <p className="inline-note">
                Vous donnez ici les accords minimaux pour ouvrir votre demande. Aucun
                enregistrement, aucune transcription et aucune transmission a un tiers
                ne sont autorises par ce formulaire.
              </p>

              <label className="checkbox-row">
                <input
                  type="checkbox"
                  checked={sessionConsent}
                  onChange={(event) => setSessionConsent(event.target.checked)}
                />
                <span>
                  J&apos;accepte une premiere seance d&apos;ecoute IVIA dans le cadre
                  presente.
                </span>
              </label>

              <label className="checkbox-row">
                <input
                  type="checkbox"
                  checked={sessionNoteConsent}
                  onChange={(event) => setSessionNoteConsent(event.target.checked)}
                />
                <span>
                  J&apos;accepte qu&apos;une note breve de seance soit conservee pour le
                  suivi.
                </span>
              </label>

              <label className="checkbox-row">
                <input
                  type="checkbox"
                  checked={historyConsent}
                  onChange={(event) => setHistoryConsent(event.target.checked)}
                />
                <span>
                  J&apos;accepte qu&apos;un historique court soit maintenu pour eviter de
                  recommencer a zero.
                </span>
              </label>
            </div>

            <div className="message message-error">
              IVIA n&apos;est pas un service d&apos;urgence. Si vous etes en danger
              immediat, composez le 911. En cas de crise suicidaire ou de detresse
              intense au Canada, appelez ou textez le 988.
            </div>

            <button className="button button-primary" disabled={isSubmitting} type="submit">
              {isSubmitting ? "Envoi en cours..." : "Demander ma seance"}
            </button>
            <p className="inline-note">
              Votre demande est confidentielle. Nous reprendrons contact a partir
              des coordonnees fournies.
            </p>

            {errorMessage ? <p className="message message-error">{errorMessage}</p> : null}

            {submissionState ? (
              <div className="message message-success">
                <p>
                  Votre demande a ete recue. Reference client:{" "}
                  <span className="mono">{submissionState.clientCode}</span>
                </p>
                <p>
                  Reference d&apos;entree: <span className="mono">{submissionState.intakeId}</span>
                </p>
                <p>
                  Nous reprendrons contact a partir des coordonnees transmises pour
                  la suite du parcours.
                </p>
                <p>
                  Vous pourrez consulter les syntheses diffusees plus tard dans{" "}
                  <Link
                    href={`/suivi?code=${submissionState.clientCode}&intake=${submissionState.intakeId}`}
                  >
                    votre espace de suivi
                  </Link>.
                </p>
              </div>
            ) : null}
          </form>
        </div>
      </main>
    </div>
  );
}

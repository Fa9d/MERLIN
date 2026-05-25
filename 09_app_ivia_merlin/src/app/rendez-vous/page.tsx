"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { FormEvent, Suspense, useEffect, useMemo, useState } from "react";

import { PublicLayout } from "@/components/layout/PublicLayout";
import {
  getMyClient,
  readStoredPublicClientSession,
  startPublicIntake,
  type PublicIntakeStartResult,
} from "@/lib/merlin-api";

type Need =
  | "clarification"
  | "support"
  | "orientation"
  | "loneliness"
  | "distress"
  | "other";

const NEED_OPTIONS: { code: Need; label: string }[] = [
  { code: "support", label: "Parler de ce qui se passe et être entendu" },
  { code: "clarification", label: "Comprendre ce que vous ressentez" },
  { code: "orientation", label: "Savoir vers où vous tourner" },
  { code: "loneliness", label: "Sortir de la solitude" },
  { code: "distress", label: "Dire une détresse qui monte" },
  { code: "other", label: "Autre chose" },
];

function RendezVousContent() {
  const searchParams = useSearchParams();
  const praticienName = searchParams.get("praticienName") ?? "";
  const slotDate = searchParams.get("slotDate") ?? "";
  const slotTime = searchParams.get("slotTime") ?? "";
  const sessionType = searchParams.get("sessionType") ?? "";
  const urgency = searchParams.get("urgency") === "true";

  const [firstNameOrAlias, setFirstNameOrAlias] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [isAdultConfirmed, setIsAdultConfirmed] = useState(false);
  const [prefilled, setPrefilled] = useState(false);

  useEffect(() => {
    const session = readStoredPublicClientSession();
    if (!session?.access_token) return;
    getMyClient(session.access_token).then((profile) => {
      if (!profile) return;
      setFirstNameOrAlias(profile.first_name_or_alias ?? "");
      setEmail(profile.email ?? "");
      setPhone(profile.phone ?? "");
      setIsAdultConfirmed(profile.is_adult_confirmed ?? false);
      setPrefilled(true);
    }).catch(() => { /* session expirée ou invalide — on laisse les champs vides */ });
  }, []);

  const [consentTerms, setConsentTerms] = useState(false);

  const [need, setNeed] = useState<Need>("support");
  const [requestText, setRequestText] = useState("");
  const [supportInPlace, setSupportInPlace] = useState(false);

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [result, setResult] = useState<PublicIntakeStartResult | null>(null);

  const contextSummary = useMemo(() => {
    const parts: string[] = [];
    if (praticienName) parts.push(praticienName);
    if (slotDate) parts.push(slotDate);
    if (slotTime) parts.push(slotTime);
    if (sessionType) parts.push(sessionType);
    return parts.join(" · ");
  }, [praticienName, sessionType, slotDate, slotTime]);

  const entrySummary = useMemo(() => {
    const lines: string[] = [];
    if (praticienName) lines.push(`Praticien souhaité : ${praticienName}`);
    if (slotDate || slotTime) {
      lines.push(`Créneau souhaité : ${[slotDate, slotTime].filter(Boolean).join(" ")}`.trim());
    }
    if (sessionType) lines.push(`Type de séance souhaitée : ${sessionType}`);
    if (urgency) lines.push("Demande urgence : format court prioritaire 30 min à 50 $");
    return lines.length ? lines.join(" | ") : null;
  }, [praticienName, sessionType, slotDate, slotTime, urgency]);

  const requestTextLength = requestText.length;

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSubmitting(true);
    setErrorMessage(null);
    setResult(null);

    if (!isAdultConfirmed) {
      setErrorMessage("La demande est réservée aux adultes de 18 ans et plus.");
      setIsSubmitting(false);
      return;
    }

    if (!consentTerms) {
      setErrorMessage("Vous devez accepter les CGU et la politique de confidentialité pour continuer.");
      setIsSubmitting(false);
      return;
    }

    try {
      const response = await startPublicIntake({
        first_name_or_alias: firstNameOrAlias.trim(),
        email: email.trim() ? email.trim() : null,
        phone: phone.trim() ? phone.trim() : null,
        is_adult_confirmed: isAdultConfirmed,
        primary_need_code: need,
        perceived_urgency_code: urgency ? "priority" : "non_urgent",
        support_already_in_place: supportInPlace,
        requested_outcome_text: requestText.trim() || null,
        entry_summary_text: entrySummary,
        consent_terms_accepted: consentTerms,
        consent_terms_version: "v1.2",
      });
      setResult(response);
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Erreur inconnue.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <PublicLayout>
      <div className="page-shell">
        <main className="section">
          <div className="section-header">
            <div className="eyebrow">Première séance</div>
            <h2>Vous avez fait un pas important en décidant d&apos;en parler.</h2>
            <p>
              Prenez quelques minutes pour nous dire où vous en êtes. Pas de jugement.
              Pas de case à cocher parfaitement. Juste ce qui vous ressemble.
            </p>
          </div>

          {contextSummary ? (
            <section className="card rendezvous-context-card">
              <div className="info-strip">
                <span>{urgency ? "Urgence 30 min" : "Demande de rendez-vous"}</span>
                {urgency ? <span>50 $</span> : null}
              </div>
              <p className="inline-note">
                Demande préparée depuis la page de <strong>{praticienName || "praticien"}</strong>
                {slotDate || slotTime ? ` pour ${contextSummary}.` : "."}
              </p>
              {urgency ? (
                <p className="inline-note">
                  Format court prioritaire. Cette demande n&apos;est pas un service d&apos;urgence vitale.
                </p>
              ) : null}
            </section>
          ) : null}

          {result ? (
            <SubmissionSuccess result={result} />
          ) : (
            <div className="grid intake-layout">
              <article className="card stack-md">
                <h3>Avant de commencer</h3>
                <ul>
                  <li>IVIA s&apos;adresse aux adultes hors situation d&apos;urgence immédiate.</li>
                  <li>Notre but : un espace d&apos;écoute, de clarté et de suite concrète — sans diagnostic, sans prescription.</li>
                  <li>Nous ne remplaçons pas les soins. Nous aidons à trouver le bon chemin vers eux.</li>
                </ul>
                <div className="info-strip">
                  <span>{urgency ? "50 $" : "65 $"}</span>
                  <span>{urgency ? "30 min" : "60 min"}</span>
                  <span>En ligne</span>
                </div>
                <div className="stack-sm">
                  <h4>Comment ça se passe ensuite</h4>
                  <p className="inline-note">
                    1. Vous soumettez votre demande ci-contre.
                  </p>
                  <p className="inline-note">
                    2. Si vous indiquez un courriel, un lien d&apos;activation vous est envoyé immédiatement.
                  </p>
                  <p className="inline-note">
                    3. Un clic sur ce lien ouvre votre espace personnel IVIA — où vous pourrez réserver une séance, lire les ressources réservées aux membres et tenir votre journal au fil des semaines.
                  </p>
                </div>
              </article>

              <form className="card form-stack" onSubmit={handleSubmit}>
                {prefilled ? (
                  <p className="inline-note intake-prefilled-note">Vos coordonnées ont été reprises depuis votre profil.</p>
                ) : null}

                <label className="field">
                  <span>Comment souhaitez-vous être appelé ?</span>
                  <input
                    required
                    value={firstNameOrAlias}
                    onChange={(event) => setFirstNameOrAlias(event.target.value)}
                    placeholder="Prénom ou alias"
                  />
                </label>

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
                    <span>Téléphone</span>
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
                  <span>Je confirme être majeur (18 ans et plus).</span>
                </label>

                <label className="field">
                  <span>En ce moment, vous cherchez plutôt…</span>
                  <select value={need} onChange={(event) => setNeed(event.target.value as Need)}>
                    {NEED_OPTIONS.map((option) => (
                      <option key={option.code} value={option.code}>
                        {option.label}
                      </option>
                    ))}
                  </select>
                </label>

                <label className="field">
                  <span>En quelques phrases, décrivez ce qui vous amène.</span>
                  <textarea
                    maxLength={6000}
                    rows={5}
                    value={requestText}
                    onChange={(event) => setRequestText(event.target.value)}
                    placeholder="Décrivez ce que vous vivez, ce qui vous pèse ou ce que vous aimeriez comprendre."
                  />
                </label>
                <div className="form-meta-row">
                  <p className="inline-note">
                    Exemple : Je n&apos;arrive plus à dormir, je me sens dépassé par ma situation familiale et je ne sais pas par où commencer.
                  </p>
                  <p className="field-counter" aria-live="polite">{requestTextLength} / 6000</p>
                </div>

                <label className="checkbox-row">
                  <input
                    type="checkbox"
                    checked={supportInPlace}
                    onChange={(event) => setSupportInPlace(event.target.checked)}
                  />
                  <span>Un accompagnement est déjà en place (psychologue, médecin, autre).</span>
                </label>

                <div className="stack-sm consent-block">
                  <h4>Consentements pour commencer votre démarche</h4>
                  <p className="inline-note">
                    En soumettant cette demande, vous acceptez que vos informations soient
                    traitées conformément aux{" "}
                    <a href="/cgu" target="_blank" rel="noopener noreferrer">CGU</a>{" "}et à la{" "}
                    <a href="/confidentialite" target="_blank" rel="noopener noreferrer">politique de confidentialité</a>{" "}d&apos;IVIA
                    (Loi 25, hébergement Québec).
                  </p>
                  <label className="checkbox-row">
                    <input
                      type="checkbox"
                      checked={consentTerms}
                      onChange={(event) => setConsentTerms(event.target.checked)}
                    />
                    <span>
                      J&apos;accepte les <strong>CGU</strong> et la <strong>politique de confidentialité</strong> d&apos;IVIA.
                    </span>
                  </label>
                </div>

                <div className="message-safety">
                  IVIA n&apos;est pas un service d&apos;urgence. Si vous êtes en danger immédiat,
                  composez le <strong>911</strong>. En cas de crise suicidaire ou de détresse intense au Canada,
                  appelez ou textez le <strong>988</strong>.
                </div>

                <button className="button button-primary" disabled={isSubmitting} type="submit">
                  {isSubmitting ? "Envoi en cours..." : "Envoyer ma demande"}
                </button>
                <p className="inline-note">
                  Votre demande est confidentielle. Hébergement Québec, conforme à la Loi 25.
                </p>

                {errorMessage ? <p className="message message-error">{errorMessage}</p> : null}
              </form>
            </div>
          )}
        </main>
      </div>
    </PublicLayout>
  );
}

function SubmissionSuccess({ result }: { result: PublicIntakeStartResult }) {
  const hasMagicLink = result.magic_link_sent && result.email_used;

  return (
    <section className="card stack-md submission-success">
      <div className="eyebrow">Demande reçue</div>
      <h3>Merci. Votre démarche IVIA est ouverte.</h3>

      {hasMagicLink ? (
        <>
          <p>
            Un courriel d&apos;activation vient d&apos;être envoyé à{" "}
            <strong className="mono">{result.email_used}</strong>.
            <br />
            Ouvrez votre boîte mail (vérifiez aussi les indésirables) et cliquez sur le bouton{" "}
            <strong>Ouvrir mon espace IVIA</strong> — vous arriverez directement dans votre espace
            personnel, sans mot de passe à retenir.
          </p>
          <p className="inline-note">
            Le lien est valide 7 jours. Vous pourrez, dans votre espace, définir un mot de passe
            si vous souhaitez revenir plus facilement.
          </p>
        </>
      ) : result.email_used ? (
        <p>
          Votre demande est enregistrée, mais l&apos;envoi du lien d&apos;activation a échoué temporairement.
          Un membre de l&apos;équipe IVIA prendra contact à <strong>{result.email_used}</strong>.
        </p>
      ) : (
        <p>
          Votre demande est enregistrée. Pour ouvrir un espace personnel et suivre votre démarche en autonomie,
          vous pouvez créer votre accès depuis la{" "}
          <Link href="/acces-client">page d&apos;accès client</Link>.
        </p>
      )}

      <div className="stack-sm">
        <p className="inline-note">
          Référence de votre dossier : <span className="mono">{result.public_client_code}</span>
        </p>
        <p className="inline-note">
          Référence d&apos;entrée : <span className="mono">{result.intake_request_id}</span>
        </p>
        <p className="inline-note">
          Conservez ces références : elles permettent à l&apos;équipe IVIA de retrouver votre démarche.
        </p>
      </div>

      <div className="public-access-actions">
        <Link className="button button-secondary" href="/ressources">
          Lire les ressources IVIA
        </Link>
        <Link className="button button-secondary" href="/praticiens">
          Découvrir les praticiens
        </Link>
      </div>
    </section>
  );
}

export default function RendezVousPage() {
  return (
    <Suspense
      fallback={
        <PublicLayout>
          <div className="page-shell">
            <main className="section">
              <p className="inline-note">Chargement du formulaire…</p>
            </main>
          </div>
        </PublicLayout>
      }
    >
      <RendezVousContent />
    </Suspense>
  );
}

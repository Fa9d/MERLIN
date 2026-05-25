"use client";

import { Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { PublicLayout } from "@/components/layout/PublicLayout";
import { FormEvent, useEffect, useState } from "react";

import { type DerivedDocumentRecord, listPublicDerivedDocuments } from "@/lib/merlin-api";

function SuiviPageContent() {
  const searchParams = useSearchParams();
  const [clientCode, setClientCode] = useState(searchParams.get("code") ?? "");
  const [intakeReference, setIntakeReference] = useState(searchParams.get("intake") ?? "");
  const [documents, setDocuments] = useState<DerivedDocumentRecord[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    const initialCode = searchParams.get("code");
    const initialIntake = searchParams.get("intake");
    if (!initialCode || !initialIntake) {
      return;
    }

    void loadDocuments(initialCode, initialIntake);
  }, [searchParams]);

  async function loadDocuments(code: string, intakeId: string) {
    setIsLoading(true);
    setErrorMessage(null);

    try {
      const result = await listPublicDerivedDocuments(
        code.trim().toUpperCase(),
        intakeId.trim(),
      );
      setDocuments(result);
    } catch (error) {
      setDocuments([]);
      setErrorMessage(
        error instanceof Error ? error.message : "Impossible de charger vos documents.",
      );
    } finally {
      setIsLoading(false);
    }
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!clientCode.trim()) {
      setErrorMessage("Entrez votre reference client.");
      return;
    }
    if (!intakeReference.trim()) {
      setErrorMessage("Entrez votre reference d'entree.");
      return;
    }
    await loadDocuments(clientCode, intakeReference);
  }

  return (
    <main className="section">
        <div className="section-header">
          <div className="eyebrow">Suivi client</div>
          <h2>Consulter vos syntheses diffuses</h2>
          <p>
            Entrez votre reference client pour voir uniquement les documents que
            l&apos;equipe a marques comme diffusable au client.
          </p>
        </div>

        <div className="grid intake-layout">
          <form className="card form-stack" onSubmit={handleSubmit}>
            <label className="field">
              <span>Reference client</span>
              <input
                value={clientCode}
                onChange={(event) => setClientCode(event.target.value.toUpperCase())}
                placeholder="CLI-XXXXXXXXXX"
              />
            </label>
            <label className="field">
              <span>Reference d&apos;entree</span>
              <input
                value={intakeReference}
                onChange={(event) => setIntakeReference(event.target.value)}
                placeholder="UUID de votre demande"
              />
            </label>
            <button className="button button-primary" disabled={isLoading} type="submit">
              {isLoading ? "Chargement..." : "Voir mes documents"}
            </button>
            <p className="inline-note">
              Cette page n&apos;affiche pas les notes internes, seulement les syntheses diffusees.
              Les deux references remises a l&apos;entree sont necessaires.
            </p>
            {errorMessage ? <p className="message message-error">{errorMessage}</p> : null}
          </form>

          <section className="stack-md">
            {documents.length === 0 && !isLoading && !errorMessage ? (
              <article className="card">
                <h3>Aucun document diffusable pour le moment</h3>
                <p>
                  Si votre reference est correcte, cela signifie simplement qu&apos;aucune
                  synthese n&apos;a encore ete publiee pour vous.
                </p>
              </article>
            ) : null}

            {documents.map((document) => (
              <article className="card stack-sm" key={document.id}>
                <div className="info-strip">
                  <span>{document.title}</span>
                  <span>{new Date(document.created_at).toLocaleString("fr-CA")}</span>
                </div>
                <p>{document.body_text}</p>
              </article>
            ))}
          </section>
        </div>
    </main>
  );
}

export default function SuiviPage() {
  return (
    <PublicLayout>
      <Suspense fallback={<main className="section"><p>Chargement du suivi...</p></main>}>
        <SuiviPageContent />
      </Suspense>
    </PublicLayout>
  );
}

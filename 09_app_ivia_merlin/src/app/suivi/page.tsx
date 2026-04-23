"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { FormEvent, useEffect, useState } from "react";

import {
  type DerivedDocumentRecord,
  listPublicDerivedDocuments,
} from "@/lib/merlin-api";

export default function SuiviPage() {
  const searchParams = useSearchParams();
  const [clientCode, setClientCode] = useState(searchParams.get("code") ?? "");
  const [documents, setDocuments] = useState<DerivedDocumentRecord[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    const initialCode = searchParams.get("code");
    if (!initialCode) {
      return;
    }

    void loadDocuments(initialCode);
  }, [searchParams]);

  async function loadDocuments(code: string) {
    setIsLoading(true);
    setErrorMessage(null);

    try {
      const result = await listPublicDerivedDocuments(code.trim().toUpperCase());
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
    await loadDocuments(clientCode);
  }

  return (
    <div className="page-shell">
      <header className="topbar">
        <div className="wordmark">IVIA</div>
        <nav className="nav">
          <Link href="/">Accueil</Link>
          <Link href="/rendez-vous">Rendez-vous</Link>
        </nav>
      </header>

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
            <button className="button button-primary" disabled={isLoading} type="submit">
              {isLoading ? "Chargement..." : "Voir mes documents"}
            </button>
            <p className="inline-note">
              Cette page n&apos;affiche pas les notes internes, seulement les syntheses diffusees.
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
    </div>
  );
}

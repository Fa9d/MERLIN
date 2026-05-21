"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { listPraticiens, PraticienPublic } from "@/lib/merlin-api";
import { PublicLayout } from "@/components/layout/PublicLayout";
export default function PraticiensPage() {
  const [praticiens, setPraticiens] = useState<PraticienPublic[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    listPraticiens()
      .then(setPraticiens)
      .catch((err: unknown) => {
        const msg = err instanceof Error ? err.message : "Erreur inconnue";
        setError(msg);
      })
      .finally(() => setLoading(false));
  }, []);

  const langLabel = (code: string) => {
    const map: Record<string, string> = { fr: "Français", en: "English" };
    return map[code] ?? code;
  };

  const channelLabel = (code: string) => {
    const map: Record<string, string> = {
      direct: "Direct",
      in_person: "Présentiel",
      async: "Asynchrone",
    };
    return map[code] ?? code;
  };

  const parseTags = (json: string | null): string[] => {
    if (!json) return [];
    try {
      const parsed: unknown = JSON.parse(json);
      if (Array.isArray(parsed)) {
        return parsed.filter((v): v is string => typeof v === "string");
      }
    } catch {}
    return [];
  };

  return (
    <PublicLayout>
    <div className="page-shell praticiens-page-shell">
      <main>
        <div className="hero praticiens-page-hero">
          <p className="eyebrow">Équipe IVIA</p>
          <h1 className="praticiens-page-title">
            Nos praticiens
          </h1>
          <p className="praticiens-page-intro">
            Des professionnels formés à l&apos;écoute active et à l&apos;accompagnement en première
            ligne.
          </p>
        </div>

        {loading && (
          <p className="praticiens-page-state">Chargement…</p>
        )}

        {error && (
          <p className="praticiens-page-error">{error}</p>
        )}

        {!loading && !error && praticiens.length === 0 && (
          <p className="praticiens-page-state">
            Aucun praticien disponible pour le moment.
          </p>
        )}

        {!loading && praticiens.length > 0 && (
          <div className="grid praticiens-grid">
            {praticiens.map((p) => {
              const langs = parseTags(p.spoken_languages);
              const channels = parseTags(p.available_channels);

              return (
                <article key={p.id} className="card praticiens-card">
                  <div>
                    <h2 className="praticiens-card-title">
                      {p.display_name}
                    </h2>
                    {p.title_line && (
                      <p className="praticiens-card-subtitle">
                        {p.title_line}
                      </p>
                    )}
                  </div>

                  {p.intro_text && (
                    <p className="praticiens-card-intro">
                      {p.intro_text}
                    </p>
                  )}

                  {(langs.length > 0 || channels.length > 0) && (
                    <div className="praticiens-card-tags">
                      {langs.map((l) => (
                        <span key={l} className="praticiens-tag praticiens-tag--language">
                          {langLabel(l)}
                        </span>
                      ))}
                      {channels.map((c) => (
                        <span key={c} className="praticiens-tag praticiens-tag--channel">
                          {channelLabel(c)}
                        </span>
                      ))}
                    </div>
                  )}

                  <Link
                    href={`/praticiens/${p.id}`}
                    className="button button-primary"
                  >
                    Voir les disponibilites
                  </Link>
                </article>
              );
            })}
          </div>
        )}
      </main>
    </div>
    </PublicLayout>
  );
}

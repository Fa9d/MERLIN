"use client";

import { useEffect, useState } from "react";
import { listPraticiens, PraticienPublic } from "@/lib/merlin-api";

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
    <div className="page-shell" style={{ paddingBottom: "4rem" }}>
      <header className="topbar">
        <a className="wordmark" href="/">
          IVIA
        </a>
        <nav className="nav">
          <a href="/">Accueil</a>
          <a href="/rendez-vous">Prendre rendez-vous</a>
        </nav>
      </header>

      <main>
        <div className="hero" style={{ paddingBottom: "1.5rem" }}>
          <p className="eyebrow">Équipe IVIA</p>
          <h1 style={{ fontSize: "clamp(2rem, 5vw, 3.5rem)", letterSpacing: "-0.03em" }}>
            Nos praticiens
          </h1>
          <p style={{ maxWidth: "56ch", color: "var(--muted)", lineHeight: 1.7 }}>
            Des professionnels formés à l&apos;écoute active et à l&apos;accompagnement en première
            ligne.
          </p>
        </div>

        {loading && (
          <p style={{ color: "var(--muted)", fontSize: "0.95rem" }}>Chargement…</p>
        )}

        {error && (
          <p style={{ color: "#c0392b", fontSize: "0.95rem" }}>{error}</p>
        )}

        {!loading && !error && praticiens.length === 0 && (
          <p style={{ color: "var(--muted)", fontSize: "0.95rem" }}>
            Aucun praticien disponible pour le moment.
          </p>
        )}

        {!loading && praticiens.length > 0 && (
          <div
            className="grid"
            style={{
              gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))",
              gap: "1.25rem",
            }}
          >
            {praticiens.map((p) => {
              const langs = parseTags(p.spoken_languages);
              const channels = parseTags(p.available_channels);

              return (
                <article key={p.id} className="card" style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
                  <div>
                    <h2 style={{ fontSize: "1.1rem", fontWeight: 600, marginBottom: "0.15rem" }}>
                      {p.display_name}
                    </h2>
                    {p.title_line && (
                      <p style={{ fontSize: "0.85rem", color: "var(--muted)", fontWeight: 500 }}>
                        {p.title_line}
                      </p>
                    )}
                  </div>

                  {p.intro_text && (
                    <p style={{ fontSize: "0.95rem", color: "var(--muted)", lineHeight: 1.6 }}>
                      {p.intro_text}
                    </p>
                  )}

                  {(langs.length > 0 || channels.length > 0) && (
                    <div style={{ display: "flex", flexWrap: "wrap", gap: "0.4rem", marginTop: "auto" }}>
                      {langs.map((l) => (
                        <span
                          key={l}
                          style={{
                            fontSize: "0.75rem",
                            padding: "0.2rem 0.55rem",
                            borderRadius: "999px",
                            background: "rgba(76, 100, 84, 0.1)",
                            color: "var(--accent-deep)",
                            fontWeight: 500,
                          }}
                        >
                          {langLabel(l)}
                        </span>
                      ))}
                      {channels.map((c) => (
                        <span
                          key={c}
                          style={{
                            fontSize: "0.75rem",
                            padding: "0.2rem 0.55rem",
                            borderRadius: "999px",
                            background: "rgba(62, 74, 66, 0.07)",
                            color: "var(--muted)",
                            fontWeight: 500,
                          }}
                        >
                          {channelLabel(c)}
                        </span>
                      ))}
                    </div>
                  )}

                  <a
                    href="/rendez-vous"
                    className="button button-primary"
                    style={{ alignSelf: "flex-start", fontSize: "0.88rem", marginTop: "0.5rem" }}
                  >
                    Prendre rendez-vous
                  </a>
                </article>
              );
            })}
          </div>
        )}
      </main>
    </div>
  );
}

"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useMemo, useState } from "react";

import { PublicLayout } from "@/components/layout/PublicLayout";
import {
  listAvailableSlots,
  listPraticiens,
  type AvailableSlotRecord,
  type PraticienPublic,
} from "@/lib/merlin-api";

const LOOKAHEAD_DAYS = 14;
const MAX_VISIBLE_SLOTS = 12;

function addDays(date: Date, days: number): Date {
  const next = new Date(date);
  next.setDate(next.getDate() + days);
  return next;
}

function toDateInput(date: Date): string {
  return date.toISOString().slice(0, 10);
}

function parseTags(json: string | null): string[] {
  if (!json) return [];
  try {
    const parsed: unknown = JSON.parse(json);
    if (Array.isArray(parsed)) {
      return parsed.filter((value): value is string => typeof value === "string");
    }
  } catch {}
  return [];
}

function channelLabel(code: string): string {
  const map: Record<string, string> = {
    direct: "Direct",
    in_person: "Presentiel",
    async: "Asynchrone",
  };
  return map[code] ?? code;
}

function formatSlotDate(slot: AvailableSlotRecord): string {
  return new Date(`${slot.slot_date}T${slot.start_time}`).toLocaleDateString("fr-CA", {
    weekday: "short",
    day: "numeric",
    month: "short",
  });
}

function formatSlotTime(slot: AvailableSlotRecord): string {
  return slot.start_time.slice(0, 5);
}

function buildBookingHref(praticien: PraticienPublic, slot?: AvailableSlotRecord, urgency = false): string {
  const params = new URLSearchParams({
    praticienId: praticien.id,
    praticienName: praticien.display_name,
  });

  if (slot) {
    params.set("slotDate", slot.slot_date);
    params.set("slotTime", slot.start_time.slice(0, 5));
    params.set("sessionType", String(slot.session_type));
    if (slot.slot_id) {
      params.set("slotId", slot.slot_id);
    }
  }

  if (urgency) {
    params.set("urgency", "true");
  }

  return `/rendez-vous?${params.toString()}`;
}

export default function PraticienPublicPage() {
  const params = useParams<{ id: string }>();
  const [praticien, setPraticien] = useState<PraticienPublic | null>(null);
  const [slots, setSlots] = useState<AvailableSlotRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const id = params?.id;
    if (!id || typeof id !== "string") {
      setError("Praticien introuvable.");
      setLoading(false);
      return;
    }

    let active = true;

    async function loadPage() {
      setLoading(true);
      setError(null);
      try {
        const praticiens = await listPraticiens();
        if (!active) return;

        const current = praticiens.find((item) => item.id === id) ?? null;
        if (!current) {
          setPraticien(null);
          setSlots([]);
          setError("Praticien introuvable.");
          return;
        }

        setPraticien(current);
        const from = new Date();
        const to = addDays(from, LOOKAHEAD_DAYS);
        const available = await listAvailableSlots(
          current.id,
          toDateInput(from),
          toDateInput(to),
        );
        if (!active) return;
        setSlots(available.slice(0, MAX_VISIBLE_SLOTS));
      } catch (loadError) {
        if (!active) return;
        setError(loadError instanceof Error ? loadError.message : "Impossible de charger cette page.");
      } finally {
        if (active) setLoading(false);
      }
    }

    void loadPage();
    return () => {
      active = false;
    };
  }, [params]);

  const channels = useMemo(() => parseTags(praticien?.available_channels ?? null), [praticien]);
  const languages = useMemo(() => parseTags(praticien?.spoken_languages ?? null), [praticien]);

  return (
    <PublicLayout>
      <div className="page-shell praticien-public-shell">
        <main className="section praticien-public-main">
          <Link href="/praticiens" className="inline-note praticien-public-backlink">
            Retour aux praticiens
          </Link>

          {loading ? <p className="text-muted">Chargement…</p> : null}
          {error ? <p className="message message-error">{error}</p> : null}

          {praticien ? (
            <>
              <section
                className="card praticien-public-hero"
              >
                <div className="praticien-public-copy">
                  <div>
                    <p className="eyebrow">Praticien IVIA</p>
                    <h1 className="praticien-public-title">
                      {praticien.display_name}
                    </h1>
                    {praticien.title_line ? (
                      <p className="praticien-public-subtitle">{praticien.title_line}</p>
                    ) : null}
                  </div>

                  {praticien.intro_text ? (
                    <p className="praticien-public-intro">
                      {praticien.intro_text}
                    </p>
                  ) : null}

                  {(languages.length > 0 || channels.length > 0) ? (
                    <div className="praticien-public-tags">
                      {languages.map((language) => (
                        <span key={language} className="praticiens-tag praticiens-tag--language">
                          {language}
                        </span>
                      ))}
                      {channels.map((channel) => (
                        <span key={channel} className="praticiens-tag praticiens-tag--channel">
                          {channelLabel(channel)}
                        </span>
                      ))}
                    </div>
                  ) : null}
                </div>

                <aside className="praticien-public-urgence">
                  <div>
                    <p className="eyebrow praticien-public-urgence-kicker">Urgence</p>
                    <h2 className="praticien-public-urgence-title">50 $ / 30 min</h2>
                  </div>
                  <p className="inline-note praticien-public-urgence-note">
                    Pour une situation qui demande une prise rapide, sans relever du 911 ou du 988.
                  </p>
                  <Link
                    href={buildBookingHref(praticien, undefined, true)}
                    className="button button-primary"
                  >
                    Bouton urgence
                  </Link>
                  <p className="inline-note">
                    Si vous etes en danger immediat, composez le 911. En cas de crise suicidaire ou de detresse intense au Canada: 988.
                  </p>
                </aside>
              </section>

              <section className="card praticien-public-slots-card">
                <div className="praticien-public-slots-head">
                  <div>
                    <p className="eyebrow">Disponibilites</p>
                    <h2 className="praticien-public-slots-title">Format compact et efficace</h2>
                  </div>
                  <Link href={buildBookingHref(praticien)} className="button button-secondary">
                    Demande libre
                  </Link>
                </div>

                {slots.length === 0 ? (
                  <div className="message message-error praticien-public-empty-state">
                    Aucune disponibilite publique dans les 14 prochains jours. Vous pouvez tout de meme envoyer une demande libre.
                  </div>
                ) : (
                  <div className="praticien-public-slots-list">
                    {slots.map((slot) => (
                      <article key={`${slot.slot_date}-${slot.start_time}-${slot.session_type}`} className="praticien-public-slot-row">
                        <div className="praticien-public-slot-copy">
                          <strong className="praticien-public-slot-title">
                            {formatSlotDate(slot)} · {formatSlotTime(slot)}
                          </strong>
                          <span className="inline-note">
                            {slot.session_type_label} · {slot.duration_minutes} min
                          </span>
                        </div>
                        <Link
                          href={buildBookingHref(praticien, slot)}
                          className="button button-primary"
                        >
                          Reserver
                        </Link>
                      </article>
                    ))}
                  </div>
                )}
              </section>
            </>
          ) : null}
        </main>
      </div>
    </PublicLayout>
  );
}
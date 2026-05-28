"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";

import { PublicLayout } from "@/components/layout/PublicLayout";
import {
  confirmSlot,
  getMyClient,
  holdVirtualSlot,
  holdSlot,
  listAvailableSlots,
  listPraticiens,
  requestInteracEtransfer,
  readStoredPublicClientSession,
  type AvailableSlotRecord,
  type BookingSlotRecord,
  type PraticienPublic,
} from "@/lib/merlin-api";

// ── Jours de la semaine en français ──
const FR_DAYS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"];

function getWeekBounds(offset: number): { from: string; to: string } {
  const now = new Date();
  const day = now.getDay(); // 0=dim
  const monday = new Date(now);
  monday.setDate(now.getDate() - (day === 0 ? 6 : day - 1) + offset * 7);
  monday.setHours(0, 0, 0, 0);
  const sunday = new Date(monday);
  sunday.setDate(monday.getDate() + 6);
  return {
    from: monday.toISOString().slice(0, 10),
    to: sunday.toISOString().slice(0, 10),
  };
}

function formatLongDate(iso: string): string {
  return new Date(iso + "T12:00:00").toLocaleDateString("fr-CA", {
    weekday: "long", day: "numeric", month: "long", year: "numeric",
  });
}

// ── Types locaux ──
type Step = "calendar" | "confirming";
type ViewMode = "month" | "week" | "day";

// ── Composant ──
export default function ReserverPage() {
  const router = useRouter();

  const [token, setToken] = useState<string | null>(null);
  const [clientId, setClientId] = useState<string | null>(null);
  const [praticiens, setPraticiens] = useState<PraticienPublic[]>([]);
  const [selectedPraticienId, setSelectedPraticienId] = useState<string | null>(null);

  const [weekOffset, setWeekOffset] = useState(0);
  const [slots, setSlots] = useState<AvailableSlotRecord[]>([]);
  const [loadingSlots, setLoadingSlots] = useState(false);

  const [step, setStep] = useState<Step>("calendar");
  const [selectedSlot, setSelectedSlot] = useState<AvailableSlotRecord | null>(null);
  const [heldSlot, setHeldSlot] = useState<BookingSlotRecord | null>(null);

  const [error, setError] = useState<string | null>(null);
  const [working, setWorking] = useState(false);

  // ── Vue calendrier ──
  const [viewMode, setViewMode] = useState<ViewMode>("month");
  const [currentMonth, setCurrentMonth] = useState<Date>(() => {
    const d = new Date(); d.setDate(1); d.setHours(0, 0, 0, 0); return d;
  });
  const [monthSlots, setMonthSlots] = useState<AvailableSlotRecord[]>([]);
  const [loadingMonthSlots, setLoadingMonthSlots] = useState(false);
  const [selectedDayDate, setSelectedDayDate] = useState<string | null>(null);

  // ── Auth check ──
  useEffect(() => {
    const session = readStoredPublicClientSession();
    if (!session?.access_token) {
      router.replace("/acces-client");
      return;
    }
    setToken(session.access_token);
    getMyClient(session.access_token)
      .then((c) => { if (c?.id) setClientId(c.id); })
      .catch(() => {});
    listPraticiens()
      .then((list) => {
        setPraticiens(list);
        if (list.length === 1) setSelectedPraticienId(list[0].id);
      })
      .catch(() => setError("Impossible de charger les praticiens."));
  }, [router]);

  // ── Chargement des créneaux ──
  const { from, to } = useMemo(() => getWeekBounds(weekOffset), [weekOffset]);

  useEffect(() => {
    if (!selectedPraticienId) return;
    setLoadingSlots(true);
    setSlots([]);
    listAvailableSlots(selectedPraticienId, from, to)
      .then(setSlots)
      .catch(() => setError("Impossible de charger les créneaux."))
      .finally(() => setLoadingSlots(false));
  }, [selectedPraticienId, from, to]);

  // ── Grouper par jour ──
  const slotsByDay = useMemo(() => {
    const map = new Map<string, AvailableSlotRecord[]>();
    for (const s of slots) {
      if (!map.has(s.slot_date)) map.set(s.slot_date, []);
      map.get(s.slot_date)!.push(s);
    }
    for (const [d, list] of map) {
      map.set(d, [...list].sort((a, b) => a.start_time.localeCompare(b.start_time)));
    }
    return map;
  }, [slots]);

  // ── Chargement créneaux — vue mois ──
  useEffect(() => {
    if (!selectedPraticienId || viewMode !== "month") return;
    setLoadingMonthSlots(true);
    setMonthSlots([]);
    const y = currentMonth.getFullYear();
    const m = currentMonth.getMonth();
    const mFrom = `${y}-${String(m + 1).padStart(2, "0")}-01`;
    const mTo = new Date(y, m + 1, 0).toISOString().slice(0, 10);
    listAvailableSlots(selectedPraticienId, mFrom, mTo)
      .then(setMonthSlots)
      .catch(() => setError("Impossible de charger le mois."))
      .finally(() => setLoadingMonthSlots(false));
  }, [selectedPraticienId, currentMonth, viewMode]);

  // ── Grouper créneaux du mois par jour ──
  const slotsByDayMonth = useMemo(() => {
    const map = new Map<string, AvailableSlotRecord[]>();
    for (const s of monthSlots) {
      if (!map.has(s.slot_date)) map.set(s.slot_date, []);
      map.get(s.slot_date)!.push(s);
    }
    for (const [, list] of map) list.sort((a, b) => a.start_time.localeCompare(b.start_time));
    return map;
  }, [monthSlots]);

  // ── Dates de la semaine (filtrer passé) ──
  const today = new Date().toISOString().slice(0, 10);
  const weekDates = useMemo(() => {
    const dates: string[] = [];
    const d = new Date(from + "T12:00:00");
    for (let i = 0; i < 7; i++) {
      const iso = d.toISOString().slice(0, 10);
      if (iso >= today) dates.push(iso);
      d.setDate(d.getDate() + 1);
    }
    return dates;
  }, [from, today]);

  // ── Handlers ──
  async function handleSelectSlot(slot: AvailableSlotRecord) {
    if (!token) return;
    setError(null);
    setWorking(true);
    try {
      let held: BookingSlotRecord;
      if (slot.slot_id) {
        held = await holdSlot(slot.slot_id, token);
      } else {
        held = await holdVirtualSlot(
          {
            praticien_id: slot.praticien_id,
            slot_date: slot.slot_date,
            start_time: slot.start_time,
            end_time: slot.end_time,
            session_type: slot.session_type,
          },
          token,
        );
      }
      setSelectedSlot(slot);
      setHeldSlot(held);
      setStep("confirming");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Ce créneau n'est plus disponible.");
    } finally {
      setWorking(false);
    }
  }

  async function handlePayInterac() {
    if (!token || !heldSlot) return;
    setError(null);
    setWorking(true);
    try {
      // confirmSlot est appelé côté backend par mark-paid (après réception du paiement)
      if (clientId) {
        const result = await requestInteracEtransfer({
          client_id: clientId,
          slot_id: heldSlot.id,
          product_code: "session_intake",
          product_label: "Séance IVIA — 60 min",
          product_kind_code: "session_intake",
          fulfillment_mode_code: "grant_entitlement_only",
          amount_cents: 6500,
          currency: "cad",
          entitlement_type_code: "intake_session_credit",
          entitlement_quantity: 1,
        });
        const ir = {
          recipient_email: result.recipient_email,
          recipient_name: result.recipient_name,
          transfer_reference: result.transfer_reference,
          amount_cents: result.amount_cents,
          instructions_emailed: result.instructions_emailed,
        };
        sessionStorage.setItem(
          "ivia_booking_confirmation",
          JSON.stringify({ interacResult: ir, selectedSlot: selectedSlot }),
        );
      } else {
        const ir = {
          recipient_email: "david@fa9.quebec",
          recipient_name: "IVIA",
          transfer_reference: `IVIA-${heldSlot.id.split("-")[0].toUpperCase()}`,
          amount_cents: 6500,
          instructions_emailed: false,
        };
        sessionStorage.setItem(
          "ivia_booking_confirmation",
          JSON.stringify({ interacResult: ir, selectedSlot: selectedSlot }),
        );
      }
      router.push("/rendez-vous/confirmation");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Erreur lors de la création du paiement.");
    } finally {
      setWorking(false);
    }
  }

  function handleBack() {
    setStep("calendar");
    setHeldSlot(null);
    setSelectedSlot(null);
    setError(null);
  }

  if (!token) return null;

  return (
    <PublicLayout>
      <div className="page-shell">
        <main className="section reserver-main">

          <div className="section-header">
            <Link href="/mon-espace" className="button button-text reserver-back">← Mon espace</Link>
            <div className="eyebrow">Réserver un créneau</div>
            <h2>Choisissez un moment qui vous convient.</h2>
          </div>

          {error ? (
            <div className="card message message-error" role="alert"><p>{error}</p></div>
          ) : null}

          {/* ══ CALENDRIER ══ */}
          {step === "calendar" && (
            <div className="reserver-layout">

              {praticiens.length > 1 ? (
                <div className="card reserver-praticien-select">
                  <p className="label-sm">Praticien</p>
                  <div className="reserver-praticien-list">
                    {praticiens.map((p) => (
                      <button
                        key={p.id}
                        type="button"
                        className={`praticien-chip${selectedPraticienId === p.id ? " is-active" : ""}`}
                        onClick={() => setSelectedPraticienId(p.id)}
                      >
                        <span className="praticien-chip__name">{p.display_name}</span>
                        {p.title_line ? <span className="praticien-chip__title">{p.title_line}</span> : null}
                      </button>
                    ))}
                  </div>
                </div>
              ) : null}

              {selectedPraticienId ? (
                <div className="card reserver-calendar">

                  {/* ── Sélecteur de vue ── */}
                  <div className="reserver-view-toggle">
                    {(["month", "week", "day"] as ViewMode[]).map((v) => (
                      <button
                        key={v}
                        type="button"
                        className={`reserver-view-btn${viewMode === v ? " is-active" : ""}`}
                        onClick={() => setViewMode(v)}
                      >
                        {v === "month" ? "Mois" : v === "week" ? "Semaine" : "Jour"}
                      </button>
                    ))}
                  </div>

                  {/* ══ VUE MOIS ══ */}
                  {viewMode === "month" && (
                    <>
                      <div className="reserver-month-nav">
                        <button
                          type="button"
                          className="button button-text"
                          onClick={() => setCurrentMonth((prev) => new Date(prev.getFullYear(), prev.getMonth() - 1, 1))}
                        >
                          ← Précédent
                        </button>
                        <span className="reserver-week-label">
                          {currentMonth.toLocaleDateString("fr-CA", { month: "long", year: "numeric" })}
                        </span>
                        <button
                          type="button"
                          className="button button-text"
                          onClick={() => setCurrentMonth((prev) => new Date(prev.getFullYear(), prev.getMonth() + 1, 1))}
                        >
                          Suivant →
                        </button>
                      </div>

                      {loadingMonthSlots ? (
                        <p className="inline-note reserver-loading">Chargement…</p>
                      ) : (
                        <div className="reserver-month-grid">
                          {["Lu", "Ma", "Me", "Je", "Ve", "Sa", "Di"].map((d) => (
                            <div key={d} className="reserver-month-head">{d}</div>
                          ))}
                          {(() => {
                            const y = currentMonth.getFullYear();
                            const m = currentMonth.getMonth();
                            const firstWd = new Date(y, m, 1).getDay();
                            const prefix = firstWd === 0 ? 6 : firstWd - 1;
                            const daysInMonth = new Date(y, m + 1, 0).getDate();
                            const cells: Array<{ iso: string | null; day: number | null }> = [];
                            for (let i = 0; i < prefix; i++) cells.push({ iso: null, day: null });
                            for (let dd = 1; dd <= daysInMonth; dd++) {
                              cells.push({
                                iso: `${y}-${String(m + 1).padStart(2, "0")}-${String(dd).padStart(2, "0")}`,
                                day: dd,
                              });
                            }
                            return cells.map((cell, idx) => {
                              if (!cell.iso) return <div key={`e-${idx}`} className="reserver-month-cell is-empty" />;
                              const hasSlots = (slotsByDayMonth.get(cell.iso)?.length ?? 0) > 0 && cell.iso >= today;
                              const isToday = cell.iso === today;
                              const isPast = cell.iso < today;
                              return (
                                <div
                                  key={cell.iso}
                                  className={`reserver-month-cell${hasSlots ? " has-slots" : ""}${isToday ? " is-today" : ""}${isPast ? " is-past" : ""}`}
                                  role={hasSlots ? "button" : undefined}
                                  tabIndex={hasSlots ? 0 : undefined}
                                  onClick={hasSlots ? () => { setSelectedDayDate(cell.iso!); setViewMode("day"); } : undefined}
                                  onKeyDown={hasSlots ? (e) => { if (e.key === "Enter" || e.key === " ") { setSelectedDayDate(cell.iso!); setViewMode("day"); } } : undefined}
                                >
                                  <span className="reserver-month-cell__num">{cell.day}</span>
                                  {hasSlots && <span className="reserver-month-cell__dot" aria-hidden="true" />}
                                </div>
                              );
                            });
                          })()}
                        </div>
                      )}
                    </>
                  )}

                  {/* ══ VUE SEMAINE ══ */}
                  {viewMode === "week" && (
                    <>
                      <div className="reserver-week-nav">
                        <button
                          type="button"
                          className="button button-text"
                          onClick={() => setWeekOffset((w) => w - 1)}
                          disabled={weekOffset <= 0}
                        >
                          ← Précédente
                        </button>
                        <span className="reserver-week-label">
                          {new Date(from + "T12:00:00").toLocaleDateString("fr-CA", { day: "numeric", month: "long" })}
                          {" – "}
                          {new Date(to + "T12:00:00").toLocaleDateString("fr-CA", { day: "numeric", month: "long", year: "numeric" })}
                        </span>
                        <button
                          type="button"
                          className="button button-text"
                          onClick={() => setWeekOffset((w) => w + 1)}
                        >
                          Suivante →
                        </button>
                      </div>

                      {loadingSlots ? (
                        <p className="inline-note reserver-loading">Chargement…</p>
                      ) : (
                        <>
                          {weekDates.length === 0 ? (
                            <p className="inline-note">Aucune journée future cette semaine.</p>
                          ) : (
                            <div className="reserver-week-grid">
                              {weekDates.map((date) => {
                                const daySlots = slotsByDay.get(date) ?? [];
                                const jsDay = new Date(date + "T12:00:00").getDay();
                                const dayName = jsDay === 0 ? FR_DAYS[6] : FR_DAYS[jsDay - 1];
                                const dayNum = new Date(date + "T12:00:00").getDate();
                                const monthShort = new Date(date + "T12:00:00").toLocaleDateString("fr-CA", { month: "short" });
                                return (
                                  <div key={date} className="reserver-day">
                                    <div className="reserver-day__header">
                                      <span className="reserver-day__name">{dayName}</span>
                                      <span className="reserver-day__date">{dayNum} {monthShort}</span>
                                    </div>
                                    {daySlots.length > 0 ? (
                                      <ul className="reserver-day__slots">
                                        {daySlots.map((s) => (
                                          <li key={`${s.slot_date}-${s.start_time}`}>
                                            <button
                                              type="button"
                                              className="slot-btn"
                                              onClick={() => handleSelectSlot(s)}
                                              disabled={working}
                                            >
                                              <span className="slot-btn__time">{s.start_time.slice(0, 5)}</span>
                                              <span className="slot-btn__meta">{s.duration_minutes} min</span>
                                            </button>
                                          </li>
                                        ))}
                                      </ul>
                                    ) : (
                                      <p className="reserver-day__empty">—</p>
                                    )}
                                  </div>
                                );
                              })}
                            </div>
                          )}
                          {!loadingSlots && slots.length === 0 && weekDates.length > 0 ? (
                            <p className="inline-note reserver-no-slots">
                              Aucun créneau disponible cette semaine. Essayez la semaine suivante.
                            </p>
                          ) : null}
                        </>
                      )}
                    </>
                  )}

                  {/* ══ VUE JOUR ══ */}
                  {viewMode === "day" && (
                    <>
                      <div className="reserver-day-view-header">
                        <button
                          type="button"
                          className="button button-text"
                          onClick={() => setViewMode("month")}
                        >
                          ← Retour au mois
                        </button>
                        {selectedDayDate && (
                          <p className="reserver-day-view-title">{formatLongDate(selectedDayDate)}</p>
                        )}
                      </div>
                      {selectedDayDate ? (
                        (() => {
                          const daySlots = (slotsByDayMonth.get(selectedDayDate) ?? slotsByDay.get(selectedDayDate) ?? [])
                            .filter((s) => s.slot_date >= today);
                          return daySlots.length > 0 ? (
                            <ul className="reserver-day__slots reserver-day-view-slots">
                              {daySlots.map((s) => (
                                <li key={`${s.slot_date}-${s.start_time}`}>
                                  <button
                                    type="button"
                                    className="slot-btn slot-btn--lg"
                                    onClick={() => handleSelectSlot(s)}
                                    disabled={working}
                                  >
                                    <span className="slot-btn__time">{s.start_time.slice(0, 5)}</span>
                                    <span className="slot-btn__meta">{s.session_type_label} · {s.duration_minutes} min</span>
                                  </button>
                                </li>
                              ))}
                            </ul>
                          ) : (
                            <p className="inline-note">Aucun créneau disponible ce jour.</p>
                          );
                        })()
                      ) : (
                        <p className="inline-note">Sélectionnez un jour dans la vue mensuelle.</p>
                      )}
                    </>
                  )}

                </div>
              ) : (
                <div className="card">
                  <p className="inline-note">Sélectionnez un praticien pour voir les disponibilités.</p>
                </div>
              )}
            </div>
          )}

          {/* ══ CONFIRMATION ══ */}
          {step === "confirming" && selectedSlot ? (
            <div className="card stack-md reserver-confirm">
              <h3>Confirmer votre réservation</h3>

              <div className="reserver-confirm__slot">
                <p className="rdv-preview__date">{formatLongDate(selectedSlot.slot_date)}</p>
                <p className="rdv-preview__time">{selectedSlot.start_time.slice(0, 5)}</p>
                <p className="inline-note">{selectedSlot.session_type_label} · {selectedSlot.duration_minutes} min · En ligne</p>
                <p className="inline-note">Praticien : <strong>{selectedSlot.praticien_name}</strong></p>
              </div>

              <div className="reserver-confirm__price">
                <span className="reserver-price">65 $</span>
                <span className="inline-note"> CAD</span>
              </div>

              <div className="reserver-payment-methods">
                <p className="label-sm">Mode de paiement</p>
                <button
                  type="button"
                  className="payment-method-btn is-available"
                  onClick={handlePayInterac}
                  disabled={working}
                >
                  <span className="payment-method-btn__name">Interac Virement</span>
                  <span className="payment-method-btn__note">Gratuit · 100 % canadien · Confirmation sous 24 h</span>
                </button>
                <div className="payment-method-btn is-soon" aria-disabled="true">
                  <span className="payment-method-btn__name">
                    Carte de crédit / débit
                    <span className="badge-soon">à venir</span>
                  </span>
                  <span className="payment-method-btn__note">Visa, Mastercard, débit</span>
                </div>
              </div>

              {working ? <p className="inline-note">Traitement en cours…</p> : null}

              <button type="button" className="button button-text" onClick={handleBack}>
                ← Choisir un autre créneau
              </button>
            </div>
          ) : null}

        </main>
      </div>
    </PublicLayout>
  );
}

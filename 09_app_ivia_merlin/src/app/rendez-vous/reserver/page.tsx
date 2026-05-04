"use client";

import { FormEvent, useEffect, useState } from "react";
import Link from "next/link";
import { PublicLayout } from "@/components/layout/PublicLayout";
import {
  listPraticiens,
  listAvailableSlots,
  registerClient,
  holdSlot,
  confirmSlot,
  loginOperator,
  type PraticienPublic,
  type AvailableSlotRecord,
  type LoginResponse,
} from "@/lib/merlin-api";

type Step = "slots" | "auth" | "pending-verification" | "hold" | "confirmed";

function todayStr() {
  return new Date().toISOString().slice(0, 10);
}
function plusDays(n: number) {
  const d = new Date();
  d.setDate(d.getDate() + n);
  return d.toISOString().slice(0, 10);
}
function fmtDate(dateStr: string) {
  const d = new Date(dateStr + "T00:00:00");
  return d.toLocaleDateString("fr-CA", { weekday: "long", day: "numeric", month: "long" });
}
function fmtTime(t: string) {
  return t.slice(0, 5).replace(":", "h");
}

export default function ReserverPage() {
  // — Step & auth state —
  const [step, setStep] = useState<Step>("slots");
  const [token, setToken] = useState<string | null>(null);
  const [authEmail, setAuthEmail] = useState("");

  // — Slot picker —
  const [praticiens, setPraticiens] = useState<PraticienPublic[]>([]);
  const [selectedPraticienId, setSelectedPraticienId] = useState("");
  const [dateFrom, setDateFrom] = useState(todayStr());
  const [dateTo, setDateTo] = useState(plusDays(14));
  const [slots, setSlots] = useState<AvailableSlotRecord[]>([]);
  const [slotsLoading, setSlotsLoading] = useState(false);
  const [slotsError, setSlotsError] = useState<string | null>(null);
  const [selectedSlot, setSelectedSlot] = useState<AvailableSlotRecord | null>(null);

  // — Auth forms —
  const [authMode, setAuthMode] = useState<"login" | "register">("register");
  const [displayName, setDisplayName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [authLoading, setAuthLoading] = useState(false);
  const [authError, setAuthError] = useState<string | null>(null);

  // — Booking —
  const [heldSlotId, setHeldSlotId] = useState<string | null>(null);
  const [bookingLoading, setBookingLoading] = useState(false);
  const [bookingError, setBookingError] = useState<string | null>(null);
  const [confirmedInfo, setConfirmedInfo] = useState<{ date: string; time: string; praticien: string } | null>(null);

  // Load praticiens on mount
  useEffect(() => {
    listPraticiens()
      .then((list) => {
        setPraticiens(list);
        if (list.length === 1) setSelectedPraticienId(list[0].id);
      })
      .catch(() => {});
  }, []);

  // Load slots when praticien or dates change
  async function fetchSlots() {
    if (!selectedPraticienId) return;
    setSlotsLoading(true);
    setSlotsError(null);
    try {
      const data = await listAvailableSlots(selectedPraticienId, dateFrom, dateTo);
      setSlots(data.filter((s) => s.status === "available"));
    } catch (err: unknown) {
      setSlotsError(err instanceof Error ? err.message : "Erreur");
    } finally {
      setSlotsLoading(false);
    }
  }

  function handleSelectSlot(slot: AvailableSlotRecord) {
    setSelectedSlot(slot);
    setStep("auth");
  }

  // — Auth submit —
  async function handleAuth(e: FormEvent) {
    e.preventDefault();
    setAuthLoading(true);
    setAuthError(null);
    try {
      if (authMode === "register") {
        await registerClient({ email, password, display_name: displayName });
        setAuthEmail(email);
        setStep("pending-verification");
      } else {
        const result: LoginResponse = await loginOperator(email, password);
        setToken(result.access_token);
        await proceedToHold(result.access_token);
      }
    } catch (err: unknown) {
      setAuthError(err instanceof Error ? err.message : "Erreur");
    } finally {
      setAuthLoading(false);
    }
  }

  // — Hold then confirm —
  async function proceedToHold(tok: string) {
    if (!selectedSlot?.slot_id) {
      setAuthError("Ce créneau ne peut pas être réservé en ligne (pas encore matérialisé).");
      return;
    }
    setBookingLoading(true);
    setBookingError(null);
    try {
      const held = await holdSlot(selectedSlot.slot_id, tok);
      setHeldSlotId(held.id);
      setStep("hold");
    } catch (err: unknown) {
      setBookingError(err instanceof Error ? err.message : "Erreur de réservation");
    } finally {
      setBookingLoading(false);
    }
  }

  async function handleConfirm() {
    if (!heldSlotId || !token) return;
    setBookingLoading(true);
    setBookingError(null);
    try {
      await confirmSlot(heldSlotId, token);
      setConfirmedInfo({
        date: fmtDate(selectedSlot!.slot_date),
        time: fmtTime(selectedSlot!.start_time),
        praticien: selectedSlot!.praticien_name,
      });
      setStep("confirmed");
    } catch (err: unknown) {
      setBookingError(err instanceof Error ? err.message : "Erreur de confirmation");
    } finally {
      setBookingLoading(false);
    }
  }

  // ─── RENDER ───────────────────────────────────────────────────────────────

  return (
    <PublicLayout>
    <main style={{ maxWidth: 720, margin: "2rem auto", padding: "0 1.5rem" }}>
      <h1 style={{ marginBottom: "1.5rem" }}>Réserver un rendez-vous</h1>

      {/* ── STEP 1 : Slot picker ──────────────────────────────────────── */}
      {step === "slots" && (
        <>
          <div className="card" style={{ marginBottom: "1.5rem" }}>
            <div className="form-grid-auto">
              <div>
                <label className="form-label">Intervenant·e</label>
                <select
                  className="form-control"
                  value={selectedPraticienId}
                  onChange={(e) => setSelectedPraticienId(e.target.value)}
                >
                  <option value="">— Choisir —</option>
                  {praticiens.map((p) => (
                    <option key={p.id} value={p.id}>
                      {p.display_name}
                      {p.title_line ? ` — ${p.title_line}` : ""}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="form-label">Du</label>
                <input
                  type="date"
                  className="form-control"
                  value={dateFrom}
                  min={todayStr()}
                  onChange={(e) => setDateFrom(e.target.value)}
                />
              </div>
              <div>
                <label className="form-label">Au</label>
                <input
                  type="date"
                  className="form-control"
                  value={dateTo}
                  min={dateFrom}
                  onChange={(e) => setDateTo(e.target.value)}
                />
              </div>
            </div>
            <button
              className="btn btn-primary"
              style={{ marginTop: "1rem" }}
              disabled={!selectedPraticienId || slotsLoading}
              onClick={fetchSlots}
            >
              {slotsLoading ? "Chargement…" : "Voir les disponibilités"}
            </button>
          </div>

          {slotsError && <p className="error-msg">{slotsError}</p>}

          {slots.length > 0 && (
            <div className="card">
              <h2 className="card-title" style={{ marginBottom: "1rem" }}>
                Créneaux disponibles
              </h2>
              <div style={{ display: "grid", gap: "0.5rem" }}>
                {slots.map((s, i) => (
                  <button
                    key={s.slot_id ?? i}
                    className="btn btn-outline"
                    style={{ textAlign: "left", justifyContent: "flex-start" }}
                    onClick={() => handleSelectSlot(s)}
                  >
                    <strong>{fmtDate(s.slot_date)}</strong>
                    &nbsp;·&nbsp;{fmtTime(s.start_time)} – {fmtTime(s.end_time)}
                    &nbsp;·&nbsp;<span style={{ color: "var(--color-muted, #888)" }}>{s.session_type_label}</span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {slots.length === 0 && !slotsLoading && selectedPraticienId && (
            <p className="text-muted">Aucun créneau disponible pour cette période.</p>
          )}
        </>
      )}

      {/* ── STEP 2 : Auth ─────────────────────────────────────────────── */}
      {step === "auth" && selectedSlot && (
        <div className="card" style={{ maxWidth: 460 }}>
          <p style={{ marginBottom: "1rem", color: "var(--color-muted, #555)" }}>
            Créneau sélectionné :{" "}
            <strong>
              {fmtDate(selectedSlot.slot_date)} à {fmtTime(selectedSlot.start_time)}
            </strong>
          </p>

          <div style={{ display: "flex", gap: "0.5rem", marginBottom: "1.5rem" }}>
            <button
              className={`btn ${authMode === "register" ? "btn-primary" : "btn-outline"}`}
              onClick={() => setAuthMode("register")}
            >
              Nouveau compte
            </button>
            <button
              className={`btn ${authMode === "login" ? "btn-primary" : "btn-outline"}`}
              onClick={() => setAuthMode("login")}
            >
              Déjà inscrit
            </button>
          </div>

          <form onSubmit={handleAuth}>
            {authMode === "register" && (
              <div style={{ marginBottom: "0.75rem" }}>
                <label className="form-label">Votre prénom ou surnom</label>
                <input
                  type="text"
                  className="form-control"
                  required
                  value={displayName}
                  onChange={(e) => setDisplayName(e.target.value)}
                />
              </div>
            )}
            <div style={{ marginBottom: "0.75rem" }}>
              <label className="form-label">Adresse courriel</label>
              <input
                type="email"
                className="form-control"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div style={{ marginBottom: "1rem" }}>
              <label className="form-label">Mot de passe</label>
              <input
                type="password"
                className="form-control"
                required
                minLength={authMode === "register" ? 8 : 1}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            {authError && <p className="error-msg" style={{ marginBottom: "0.75rem" }}>{authError}</p>}
            <div style={{ display: "flex", gap: "0.75rem" }}>
              <button type="submit" className="btn btn-primary" disabled={authLoading}>
                {authLoading ? "…" : authMode === "register" ? "Créer mon compte" : "Connexion"}
              </button>
              <button
                type="button"
                className="btn btn-outline"
                onClick={() => setStep("slots")}
              >
                Retour
              </button>
            </div>
          </form>
        </div>
      )}

      {/* ── STEP 3 : Pending verification ─────────────────────────────── */}
      {step === "pending-verification" && (
        <div className="card" style={{ maxWidth: 480, textAlign: "center" }}>
          <h2 className="card-title">Vérifiez votre courriel</h2>
          <p style={{ margin: "1rem 0" }}>
            Un lien d&apos;activation a été envoyé à <strong>{authEmail}</strong>.
          </p>
          <p className="text-muted" style={{ marginBottom: "1.5rem" }}>
            Cliquez sur le lien dans votre boîte de réception pour activer votre compte,
            puis revenez vous connecter ici pour confirmer votre rendez-vous.
          </p>
          <button
            className="btn btn-primary"
            onClick={() => {
              setAuthMode("login");
              setStep("auth");
            }}
          >
            J&apos;ai confirmé — me connecter
          </button>
        </div>
      )}

      {/* ── STEP 4 : Hold → Confirm ───────────────────────────────────── */}
      {step === "hold" && selectedSlot && (
        <div className="card" style={{ maxWidth: 480 }}>
          <h2 className="card-title">Confirmer le rendez-vous</h2>
          <table style={{ width: "100%", borderCollapse: "collapse", margin: "1rem 0" }}>
            <tbody>
              <tr>
                <td style={{ padding: "6px 0", color: "var(--color-muted, #777)", width: 130 }}>Praticien·ne</td>
                <td style={{ padding: "6px 0", fontWeight: 600 }}>{selectedSlot.praticien_name}</td>
              </tr>
              <tr>
                <td style={{ padding: "6px 0", color: "var(--color-muted, #777)" }}>Date</td>
                <td style={{ padding: "6px 0", fontWeight: 600 }}>{fmtDate(selectedSlot.slot_date)}</td>
              </tr>
              <tr>
                <td style={{ padding: "6px 0", color: "var(--color-muted, #777)" }}>Heure</td>
                <td style={{ padding: "6px 0", fontWeight: 600 }}>
                  {fmtTime(selectedSlot.start_time)} – {fmtTime(selectedSlot.end_time)}
                </td>
              </tr>
              <tr>
                <td style={{ padding: "6px 0", color: "var(--color-muted, #777)" }}>Type</td>
                <td style={{ padding: "6px 0" }}>{selectedSlot.session_type_label}</td>
              </tr>
            </tbody>
          </table>
          <p className="text-muted" style={{ fontSize: "0.85rem", marginBottom: "1.25rem" }}>
            Ce créneau vous est réservé pendant 15 minutes. Confirmez maintenant pour sécuriser votre place.
          </p>
          {bookingError && <p className="error-msg" style={{ marginBottom: "0.75rem" }}>{bookingError}</p>}
          <div style={{ display: "flex", gap: "0.75rem" }}>
            <button className="btn btn-primary" onClick={handleConfirm} disabled={bookingLoading}>
              {bookingLoading ? "Confirmation…" : "Confirmer"}
            </button>
            <button className="btn btn-outline" onClick={() => setStep("slots")}>
              Annuler
            </button>
          </div>
        </div>
      )}

      {/* ── STEP 5 : Confirmed ────────────────────────────────────────── */}
      {step === "confirmed" && confirmedInfo && (
        <div className="card" style={{ maxWidth: 480, textAlign: "center" }}>
          <h2 className="card-title" style={{ color: "var(--color-success, #16a34a)" }}>
            ✓ Rendez-vous confirmé !
          </h2>
          <p style={{ margin: "1rem 0" }}>
            <strong>{confirmedInfo.date}</strong> à <strong>{confirmedInfo.time}</strong>
            <br />
            avec <strong>{confirmedInfo.praticien}</strong>
          </p>
          <p className="text-muted" style={{ marginBottom: "1.5rem" }}>
            Un courriel de confirmation vous a été envoyé.
          </p>
          <Link href="/" className="btn btn-outline">
            Retour à l&apos;accueil
          </Link>
        </div>
      )}
    </main>
    </PublicLayout>
  );
}

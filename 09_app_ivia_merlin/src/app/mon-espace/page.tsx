"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { FormEvent, Suspense, useEffect, useMemo, useState } from "react";

import { PublicLayout } from "@/components/layout/PublicLayout";
import {
  cancelSlot,
  getMyClient,
  listMyBookings,
  listMyEntitlements,
  listMyJournal,
  createMyJournalEntry,
  updateMyJournalEntry,
  archiveMyJournalEntry,
  PUBLIC_CLIENT_STORAGE_KEY,
  readStoredPublicClientSession,
  setMyPassword,
  updateMyClient,
  type BookingSlotRecord,
  type ClientEntitlementRecord,
  type JournalEntryRecord,
  type JournalEntryType,
  type LoginResponse,
  type MyClientRecord,
} from "@/lib/merlin-api";

type Dashboard = {
  session: LoginResponse;
  client: MyClientRecord | null;
  bookings: BookingSlotRecord[];
  entitlements: ClientEntitlementRecord[];
};

// ── Journal client ──────────────────────────────────────────────────────────

const ENTRY_TYPE_LABELS: Record<JournalEntryType, string> = {
  aujourd_hui: "Aujourd\u2019hui",
  souvenir: "Souvenir",
  reflexion: "R\u00e9flexion",
};

function JournalTab({ token }: { token: string }) {
  const [entries, setEntries] = useState<JournalEntryRecord[] | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);

  // form state
  const [entryType, setEntryType] = useState<JournalEntryType>("aujourd_hui");
  const [bodyText, setBodyText] = useState("");
  const [emotionalTone, setEmotionalTone] = useState("");
  const [eventYearRef, setEventYearRef] = useState("");
  const [isSaving, setIsSaving] = useState(false);
  const [saveError, setSaveError] = useState<string | null>(null);

  // archive confirmation
  const [archivingId, setArchivingId] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      setIsLoading(true);
      try {
        const data = await listMyJournal(token);
        if (!cancelled) setEntries(data);
      } catch (err) {
        if (!cancelled) setErrorMsg(err instanceof Error ? err.message : "Erreur de chargement.");
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    }
    void load();
    return () => { cancelled = true; };
  }, [token]);

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setSaveError(null);
    setIsSaving(true);
    try {
      const entry = await createMyJournalEntry(
        {
          entry_type: entryType,
          body_text: bodyText.trim(),
          emotional_tone: emotionalTone.trim() || null,
          event_year_ref: eventYearRef ? parseInt(eventYearRef, 10) : null,
        },
        token,
      );
      setEntries((prev) => (prev ? [entry, ...prev] : [entry]));
      setBodyText("");
      setEmotionalTone("");
      setEventYearRef("");
      setEntryType("aujourd_hui");
      setShowForm(false);
    } catch (err) {
      setSaveError(err instanceof Error ? err.message : "Erreur lors de l\u2019enregistrement.");
    } finally {
      setIsSaving(false);
    }
  }

  async function handleArchive(entryId: string) {
    setArchivingId(entryId);
    try {
      await archiveMyJournalEntry(entryId, token);
      setEntries((prev) => prev ? prev.filter((e) => e.id !== entryId) : prev);
    } catch (err) {
      alert(err instanceof Error ? err.message : "Erreur lors de la suppression.");
    } finally {
      setArchivingId(null);
    }
  }

  return (
    <div className="mon-espace-tab-panel stack-md">
      <div className="mon-espace-journal-header">
        <div>
          <h3>Mon journal</h3>
          <p className="inline-note">
            Un espace personnel pour noter ce qui traverse votre d\u00e9marche — moments du quotidien, souvenirs, r\u00e9flexions.
          </p>
        </div>
        {!showForm ? (
          <button type="button" className="button button-primary button-sm" onClick={() => setShowForm(true)}>
            + Nouvelle entr\u00e9e
          </button>
        ) : null}
      </div>

      {showForm ? (
        <article className="card stack-md">
          <h4>Nouvelle entr\u00e9e</h4>
          <form className="form-stack" onSubmit={(e) => { void handleSubmit(e); }}>
            <label className="field">
              <span>Type</span>
              <select value={entryType} onChange={(e) => setEntryType(e.target.value as JournalEntryType)}>
                {(Object.entries(ENTRY_TYPE_LABELS) as [JournalEntryType, string][]).map(([code, label]) => (
                  <option key={code} value={code}>{label}</option>
                ))}
              </select>
            </label>

            <label className="field">
              <span>Ce que vous souhaitez noter</span>
              <textarea
                required
                rows={5}
                value={bodyText}
                onChange={(e) => setBodyText(e.target.value)}
                placeholder="Librement, à votre rythme\u2026"
              />
            </label>

            <div className="form-grid-2">
              <label className="field">
                <span>Ton \u00e9motionnel (optionnel)</span>
                <input
                  value={emotionalTone}
                  onChange={(e) => setEmotionalTone(e.target.value)}
                  placeholder="Ex. : s\u00e9r\u00e9nit\u00e9, tristesse, soulagement\u2026"
                />
              </label>
              <label className="field">
                <span>Ann\u00e9e de r\u00e9f\u00e9rence (optionnel)</span>
                <input
                  type="number"
                  min={1900}
                  max={new Date().getFullYear()}
                  value={eventYearRef}
                  onChange={(e) => setEventYearRef(e.target.value)}
                  placeholder="Ex. : 2019"
                />
              </label>
            </div>

            {saveError ? <p className="message message-error">{saveError}</p> : null}

            <div className="public-access-actions">
              <button type="submit" className="button button-primary" disabled={isSaving || !bodyText.trim()}>
                {isSaving ? "Enregistrement\u2026" : "Enregistrer"}
              </button>
              <button
                type="button"
                className="button button-secondary"
                onClick={() => { setShowForm(false); setSaveError(null); }}
              >
                Annuler
              </button>
            </div>
          </form>
        </article>
      ) : null}

      {isLoading ? (
        <section className="card"><p className="inline-note">Chargement du journal\u2026</p></section>
      ) : errorMsg ? (
        <section className="card message message-error"><p>{errorMsg}</p></section>
      ) : entries && entries.length === 0 ? (
        <section className="card card--muted">
          <p className="inline-note">Votre journal est vide pour l\u2019instant. Vos entr\u00e9es restent priv\u00e9es — jamais lues par votre praticien. Elles alimentent l\u2019analyse de votre parcours.</p>
        </section>
      ) : entries ? (
        <ul className="journal-entries list-plain stack-md">
          {entries.map((entry) => (
            <li key={entry.id}>
              <article className="card stack-sm">
                <div className="journal-entry__meta">
                  <span className="journal-entry__type-badge">{ENTRY_TYPE_LABELS[entry.entry_type as JournalEntryType] ?? entry.entry_type}</span>
                  <time className="inline-note" dateTime={entry.written_at}>
                    {new Date(entry.written_at).toLocaleDateString("fr-CA", { year: "numeric", month: "long", day: "numeric" })}
                  </time>
                  {entry.event_year_ref ? (
                    <span className="inline-note">\u00b7 ann\u00e9e\u00a0{entry.event_year_ref}</span>
                  ) : null}
                </div>
                <p className="journal-entry__body">{entry.body_text}</p>
                {entry.emotional_tone ? (
                  <p className="inline-note journal-entry__tone">{entry.emotional_tone}</p>
                ) : null}
                <div className="journal-entry__actions">
                  <button
                    type="button"
                    className="button button-text button-sm"
                    disabled={archivingId === entry.id}
                    onClick={() => { void handleArchive(entry.id); }}
                  >
                    {archivingId === entry.id ? "Suppression\u2026" : "Supprimer"}
                  </button>
                </div>
              </article>
            </li>
          ))}
        </ul>
      ) : null}
    </div>
  );
}

// ── Espace principal ────────────────────────────────────────────────────────

function MonEspaceContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const isMagicWelcome = searchParams.get("welcome") === "magic";

  const [data, setData] = useState<Dashboard | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  // Skip hub when arriving from magic-link activation or when no praticien session
  const [view, setView] = useState<"hub" | "dashboard">(isMagicWelcome ? "dashboard" : "hub");
  const [hasPraticienSession, setHasPraticienSession] = useState(false);
  const [praticienName, setPraticienName] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<"apercu" | "rendez-vous" | "journal" | "ressources" | "profil">("apercu");
  const [cancellingId, setCancellingId] = useState<string | null>(null);

  async function handleCancelSlot(slotId: string) {
    const session = readStoredPublicClientSession();
    if (!session) return;
    setCancellingId(slotId);
    try {
      const updated = await cancelSlot(slotId, session.access_token);
      setData((prev) =>
        prev
          ? { ...prev, bookings: prev.bookings.map((b) => (b.id === slotId ? updated : b)) }
          : prev,
      );
    } catch (err) {
      alert(err instanceof Error ? err.message : "Erreur lors de l'annulation.");
    } finally {
      setCancellingId(null);
    }
  }

  useEffect(() => {
    let cancelled = false;

    async function load() {
      let ps: { user?: { display_name?: string } } | null = null;
      try {
        const raw = window.localStorage.getItem("merlin_praticien_session");
        if (raw) ps = JSON.parse(raw) as { user?: { display_name?: string } };
      } catch {}

      const session = readStoredPublicClientSession();
      if (!session) {
        router.replace(ps ? "/espace-praticien" : "/acces-client");
        return;
      }

      if (!cancelled) {
        setHasPraticienSession(!!ps);
        setPraticienName(ps?.user?.display_name ?? null);
        // Si client seul (aucune session praticien) et pas de magic welcome → aller direct au dashboard
        if (!ps && !isMagicWelcome) setView("dashboard");
      }

      try {
        const [client, bookings, entitlements] = await Promise.all([
          getMyClient(session.access_token),
          listMyBookings(session.access_token).catch(() => [] as BookingSlotRecord[]),
          listMyEntitlements(session.access_token).catch(() => [] as ClientEntitlementRecord[]),
        ]);
        if (cancelled) return;
        setData({ session, client, bookings, entitlements });
      } catch (error) {
        if (cancelled) return;
        const message = error instanceof Error ? error.message : "Erreur inconnue.";
        // Token expired or invalid → clear session and redirect to login
        if (/token invalide|authentification requise|expired/i.test(message)) {
          window.localStorage.removeItem(PUBLIC_CLIENT_STORAGE_KEY);
          window.sessionStorage.removeItem(PUBLIC_CLIENT_STORAGE_KEY);
          document.cookie = "session_token=; path=/; max-age=0; samesite=lax";
          router.replace("/acces-client");
          return;
        }
        setErrorMessage(message);
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    }

    void load();
    return () => {
      cancelled = true;
    };
  }, [router]);

  const upcomingBookings = useMemo(() => {
    if (!data) return [] as BookingSlotRecord[];
    const today = new Date().toISOString().slice(0, 10);
    return data.bookings
      .filter((b) => b.slot_date >= today && b.status !== "cancelled")
      .sort((a, b) => a.slot_date.localeCompare(b.slot_date));
  }, [data]);

  const pastBookings = useMemo(() => {
    if (!data) return [] as BookingSlotRecord[];
    const today = new Date().toISOString().slice(0, 10);
    return data.bookings
      .filter((b) => b.slot_date < today || b.status === "cancelled")
      .sort((a, b) => b.slot_date.localeCompare(a.slot_date))
      .slice(0, 12);
  }, [data]);

  const activeEntitlements = useMemo(() => {
    if (!data) return [] as ClientEntitlementRecord[];
    return data.entitlements.filter(
      (e) => e.record_status === "active" && e.quantity_remaining > 0,
    );
  }, [data]);

  const completedSessionCount = useMemo(() => {
    if (!data) return 0;
    const today = new Date().toISOString().slice(0, 10);
    return data.bookings.filter(
      (b) => b.slot_date < today && b.status !== "cancelled",
    ).length;
  }, [data]);

  const clientPhase: 1 | 2 | 3 =
    completedSessionCount === 0 && upcomingBookings.length === 0
      ? 1
      : completedSessionCount >= 3
      ? 3
      : 2;

  function handleSignOut() {
    window.localStorage.removeItem(PUBLIC_CLIENT_STORAGE_KEY);
    window.sessionStorage.removeItem(PUBLIC_CLIENT_STORAGE_KEY);
    document.cookie = "session_token=; path=/; max-age=0; samesite=lax";
    router.replace("/");
  }

  if (view === "hub") {
    return (
      <PublicLayout>
        <div className="page-shell">
          <main className="section mon-espace-main">
            <div className="section-header">
              <div className="eyebrow">Mon espace IVIA</div>
              <h1>
                {data?.session.user.display_name
                  ? `Bonjour, ${data.session.user.display_name}.`
                  : "Votre espace"}
              </h1>
              <p>Choisissez l&apos;espace auquel vous souhaitez accéder.</p>
            </div>

            {isLoading ? (
              <section className="card">
                <p className="inline-note">Vérification de votre session…</p>
              </section>
            ) : errorMessage ? (
              <section className="card message message-error">
                <p>{errorMessage}</p>
              </section>
            ) : (
              <div className="mon-espace-gateway">
                <article className="card mon-espace-gateway-card stack-md">
                  <div className="eyebrow">Espace client</div>
                  <h3>{data?.session.user.display_name ?? "Espace personnel"}</h3>
                  <p className="inline-note">
                    Vos rendez-vous, votre dossier et vos ressources personnelles.
                  </p>
                  <button
                    type="button"
                    className="button button-primary"
                    onClick={() => setView("dashboard")}
                  >
                    Ouvrir mon espace personnel
                  </button>
                </article>

                {hasPraticienSession ? (
                  <article className="card mon-espace-gateway-card stack-md">
                    <div className="eyebrow">Espace praticien · opérateur</div>
                    <h3>{praticienName ?? "Tableau de bord"}</h3>
                    <p className="inline-note">
                      Gestion des séances, dossiers clients et opérations.
                    </p>
                    <Link href="/espace-praticien" className="button button-secondary">
                      Accéder au tableau de bord
                    </Link>
                  </article>
                ) : null}
              </div>
            )}

            <div className="section-footer">
              <button type="button" className="button button-text" onClick={handleSignOut}>
                Me déconnecter
              </button>
            </div>
          </main>
        </div>
      </PublicLayout>
    );
  }

  return (
    <PublicLayout>
      <div className="page-shell">
        <main className="section mon-espace-main">

          {/* ── En-tête + onglets ── */}
          <div className="mon-espace-header">
            <div className="mon-espace-header__top">
              <div>
                <div className="eyebrow">Mon espace IVIA</div>
                <h2 className="mon-espace-header__title">
                  {data?.session.user.display_name
                    ? `Bonjour, ${data.session.user.display_name}.`
                    : "Votre espace personnel"}
                </h2>
              </div>
              <div className="mon-espace-header__actions">
                {hasPraticienSession ? (
                  <Link href="/espace-praticien" className="button button-secondary button-sm">
                    Espace praticien
                  </Link>
                ) : null}
                <button type="button" className="button button-text" onClick={handleSignOut}>
                  Déconnexion
                </button>
              </div>
            </div>
            <nav className="mon-espace-tabs" aria-label="Sections de votre espace">
              {(["apercu", "rendez-vous", "journal", "ressources", "profil"] as const).map((tab) => (
                <button
                  key={tab}
                  type="button"
                  className={`mon-espace-tab${activeTab === tab ? " is-active" : ""}`}
                  onClick={() => setActiveTab(tab)}
                >
                  {tab === "apercu" && "Vue d\u2019ensemble"}
                  {tab === "rendez-vous" && (upcomingBookings.length > 0 ? `Rendez-vous\u00a0(${upcomingBookings.length})` : "Rendez-vous")}
                  {tab === "journal" && "Mon journal"}
                  {tab === "ressources" && "Ressources"}
                  {tab === "profil" && "Profil"}
                </button>
              ))}
            </nav>
          </div>

          {/* ── Corps ── */}
          <div className="mon-espace-body">

            {isMagicWelcome ? (
              <section className="card message message-success mon-espace-welcome">
                <p><strong>Votre compte est activé.</strong> Vous êtes connecté sans mot de passe.</p>
                <p className="inline-note">
                  Vous pouvez définir un mot de passe dans l&apos;onglet{" "}
                  <button type="button" className="link-inline" onClick={() => setActiveTab("profil")}>
                    Profil
                  </button>{" "}
                  quand vous le souhaitez — c&apos;est optionnel.
                </p>
              </section>
            ) : null}

            {errorMessage ? (
              <section className="card message message-error"><p>{errorMessage}</p></section>
            ) : null}

            {isLoading ? (
              <section className="card"><p className="inline-note">Chargement de votre espace…</p></section>
            ) : data ? (
              <>
                {/* ══ TAB : Vue d'ensemble ══ */}
                {activeTab === "apercu" && (
                  <div className="mon-espace-tab-panel stack-md">

                    {/* ── Phase 1 : aucune séance – invitation à commencer ── */}
                    {clientPhase === 1 ? (
                      <>
                        <section className="card stack-md">
                          <div className="eyebrow">Première étape</div>
                          <h3>Prenez votre première séance</h3>
                          <p className="inline-note">
                            Votre espace est prêt. La prochaine étape&nbsp;: choisir un créneau avec l&apos;un de nos praticiens — aujourd&apos;hui, sans attente.
                          </p>
                          <div className="public-access-actions">
                            <Link href="/rendez-vous" className="button button-primary">Prendre rendez-vous →</Link>
                            <button type="button" className="button button-secondary" onClick={() => setActiveTab("journal")}>Commencer mon journal</button>
                          </div>
                        </section>

                        <section className="card stack-sm">
                          <h3>Préparez votre première rencontre</h3>
                          <p className="inline-note">
                            Avant votre séance, notez ce qui vous amène ici — un moment, un souvenir, une question.
                            Ces notes enrichissent l&apos;analyse de votre parcours et restent <strong>strictement privées</strong>.
                          </p>
                          <button type="button" className="link-inline" onClick={() => setActiveTab("journal")}>
                            Ouvrir mon journal →
                          </button>
                        </section>

                        <div className="mon-espace-apercu-grid">
                          <article className="card stack-sm">
                            <h3>Mon dossier</h3>
                            {data.client ? (
                              <>
                                <p><strong>{data.client.first_name_or_alias}{data.client.last_name ? ` ${data.client.last_name}` : ""}</strong></p>
                                <p className="inline-note">Réf. : <span className="mono">{data.client.public_client_code}</span></p>
                                <button type="button" className="link-inline" onClick={() => setActiveTab("profil")}>Compléter mon profil →</button>
                              </>
                            ) : (
                              <p className="inline-note">Dossier non encore ouvert.</p>
                            )}
                          </article>

                          <article className="card stack-sm">
                            <h3>Pas encore prêt&nbsp;?</h3>
                            <p className="inline-note">Faites d&apos;abord le parcours d&apos;orientation — cela prend 3 minutes et précise votre démarche.</p>
                            <Link href="/orientation" className="link-inline">Faire le parcours d&apos;orientation →</Link>
                          </article>
                        </div>
                      </>
                    ) : clientPhase === 3 ? (
                      <>
                        {/* ── Phase 3 : parcours établi (3+ séances) ── */}
                        <section className="card stack-sm">
                          <div className="eyebrow">Votre trajectoire</div>
                          <p>
                            <strong>{completedSessionCount} séance{completedSessionCount > 1 ? "s" : ""} complétée{completedSessionCount > 1 ? "s" : ""}</strong>
                            {upcomingBookings.length > 0 ? (
                              <> &mdash; prochain RDV le{" "}
                                {new Date(upcomingBookings[0].slot_date).toLocaleDateString("fr-CA", { weekday: "long", day: "numeric", month: "long" })}
                                {" "}à {upcomingBookings[0].start_time.slice(0, 5)}.
                              </>
                            ) : (
                              <> &mdash; <Link href="/rendez-vous" className="link-inline">approfondir — prochaine séance →</Link></>
                            )}
                          </p>
                        </section>

                        <div className="mon-espace-stats">
                          <div className="stat-card">
                            <span className="stat-card__value">{completedSessionCount}</span>
                            <span className="stat-card__label">séances</span>
                          </div>
                          <div className="stat-card">
                            <span className="stat-card__value">{upcomingBookings.length}</span>
                            <span className="stat-card__label">RDV à venir</span>
                          </div>
                          <div className="stat-card">
                            <span className="stat-card__value">{activeEntitlements.reduce((s, e) => s + e.quantity_remaining, 0)}</span>
                            <span className="stat-card__label">crédits</span>
                          </div>
                        </div>

                        <div className="mon-espace-apercu-grid">
                          <article className="card stack-sm">
                            <h3>Mon journal</h3>
                            <p className="inline-note">
                              Vos entrées approfondissent la compréhension de votre parcours. Elles restent <strong>strictement privées</strong> — votre praticien ne les lit pas directement.
                            </p>
                            <button type="button" className="link-inline" onClick={() => setActiveTab("journal")}>Ouvrir mon journal →</button>
                          </article>

                          <article className="card stack-sm">
                            <div className="card-row-header">
                              <h3>Dernière séance</h3>
                              <button type="button" className="link-inline" onClick={() => setActiveTab("rendez-vous")}>Historique →</button>
                            </div>
                            {pastBookings.length > 0 ? (
                              <div className="rdv-preview">
                                <p className="rdv-preview__date">
                                  {new Date(pastBookings[0].slot_date).toLocaleDateString("fr-CA", { weekday: "long", day: "numeric", month: "long" })}
                                </p>
                                <p className="rdv-preview__time">{pastBookings[0].start_time.slice(0, 5)}</p>
                                <Link href="/suivi" className="link-inline">Consulter mon suivi →</Link>
                              </div>
                            ) : null}
                          </article>
                        </div>

                        <article className="card stack-sm">
                          <h3>Accès rapide</h3>
                          <div className="mon-espace-quick-actions">
                            <Link href="/rendez-vous" className="quick-action-btn">Réserver un créneau</Link>
                            <button type="button" className="quick-action-btn" onClick={() => setActiveTab("journal")}>Mon journal</button>
                            <Link href="/suivi" className="quick-action-btn">Mon suivi</Link>
                            <Link href="/ressources" className="quick-action-btn">Ressources</Link>
                          </div>
                        </article>
                      </>
                    ) : (
                      <>
                        {/* ── Phase 2 : 1-2 séances ── */}
                        <div className="mon-espace-stats">
                          <div className="stat-card">
                            <span className="stat-card__value">{upcomingBookings.length}</span>
                            <span className="stat-card__label">RDV à venir</span>
                          </div>
                          <div className="stat-card">
                            <span className="stat-card__value">{completedSessionCount}</span>
                            <span className="stat-card__label">séances complétées</span>
                          </div>
                          <div className="stat-card">
                            <span className="stat-card__value">{activeEntitlements.reduce((s, e) => s + e.quantity_remaining, 0)}</span>
                            <span className="stat-card__label">crédits</span>
                          </div>
                        </div>

                        <div className="mon-espace-apercu-grid">
                          <article className="card stack-sm">
                            <h3>Mon dossier</h3>
                            {data.client ? (
                              <>
                                <p>
                                  <strong>{data.client.first_name_or_alias}{data.client.last_name ? ` ${data.client.last_name}` : ""}</strong>
                                </p>
                                {data.client.email ? (
                                  <p className="inline-note">Courriel : <span className="mono">{data.client.email}</span></p>
                                ) : null}
                                <p className="inline-note">Réf. : <span className="mono">{data.client.public_client_code}</span></p>
                                <button type="button" className="link-inline" onClick={() => setActiveTab("profil")}>Modifier le profil →</button>
                              </>
                            ) : (
                              <>
                                <p className="inline-note">Aucun dossier rattaché pour l&apos;instant.</p>
                                <Link href="/rendez-vous" className="button button-primary">Réserver une séance</Link>
                              </>
                            )}
                          </article>

                          <article className="card stack-sm">
                            <div className="card-row-header">
                              <h3>Prochain rendez-vous</h3>
                              {data.bookings.length > 0 ? (
                                <button type="button" className="link-inline" onClick={() => setActiveTab("rendez-vous")}>Tous →</button>
                              ) : null}
                            </div>
                            {upcomingBookings.length > 0 ? (
                              <div className="rdv-preview">
                                <p className="rdv-preview__date">
                                  {new Date(upcomingBookings[0].slot_date).toLocaleDateString("fr-CA", {
                                    weekday: "long", day: "numeric", month: "long",
                                  })}
                                </p>
                                <p className="rdv-preview__time">{upcomingBookings[0].start_time.slice(0, 5)}</p>
                                <p className="inline-note">{upcomingBookings[0].session_type}</p>
                              </div>
                            ) : (
                              <>
                                <p className="inline-note">Aucun rendez-vous à venir.</p>
                                <Link href="/rendez-vous" className="button button-primary">Réserver un créneau</Link>
                              </>
                            )}
                          </article>
                        </div>

                        <article className="card stack-sm">
                          <h3>Mon journal</h3>
                          <p className="inline-note">
                            Continuez d&apos;alimenter votre journal entre les séances. Vos entrées restent <strong>strictement privées</strong> et enrichissent l&apos;analyse de votre démarche.
                          </p>
                          <button type="button" className="link-inline" onClick={() => setActiveTab("journal")}>Ouvrir mon journal →</button>
                        </article>

                        <article className="card stack-sm">
                          <h3>Accès rapide</h3>
                          <div className="mon-espace-quick-actions">
                            <Link href="/rendez-vous" className="quick-action-btn">Réserver un créneau</Link>
                            <button type="button" className="quick-action-btn" onClick={() => setActiveTab("journal")}>Mon journal</button>
                            <Link href="/praticiens" className="quick-action-btn">Découvrir les praticiens</Link>
                            <Link href="/ressources" className="quick-action-btn">Ressources membres</Link>
                          </div>
                        </article>
                      </>
                    )}
                  </div>
                )}

                {/* ══ TAB : Rendez-vous ══ */}
                {activeTab === "rendez-vous" && (
                  <div className="mon-espace-tab-panel stack-md">
                    <div className="card-row-header">
                      <h3>Rendez-vous à venir</h3>
                      <Link href="/rendez-vous/reserver" className="button button-primary button-sm">
                        + Réserver
                      </Link>
                    </div>
                    {upcomingBookings.length === 0 ? (
                      <section className="card stack-sm">
                        <p className="inline-note">Aucun rendez-vous à venir pour l&apos;instant.</p>
                        <Link href="/rendez-vous/reserver" className="button button-primary">
                          Réserver un créneau
                        </Link>
                      </section>
                    ) : (
                      <ul className="rdv-list">
                        {upcomingBookings.map((slot) => (
                          <li key={slot.id} className="rdv-list__item card">
                            <div className="rdv-list__date">
                              <span className="rdv-list__day">
                                {new Date(slot.slot_date).toLocaleDateString("fr-CA", { day: "numeric", month: "short" })}
                              </span>
                              <span className="rdv-list__weekday">
                                {new Date(slot.slot_date).toLocaleDateString("fr-CA", { weekday: "long" })}
                              </span>
                            </div>
                            <div className="rdv-list__info">
                              <strong>{slot.start_time.slice(0, 5)}</strong>
                              <span className="inline-note">{slot.session_type}</span>
                            </div>
                            <span className={`rdv-list__badge rdv-badge--${slot.status}`}>
                              {slot.status === "confirmed" ? "Confirmé" : slot.status === "hold" ? "En attente" : slot.status === "cancelled" ? "Annulé" : slot.status}
                            </span>
                            <button
                              type="button"
                              className="button button-ghost button-sm"
                              disabled={cancellingId === slot.id}
                              onClick={() => {
                                if (window.confirm("Annuler ce rendez-vous ?")) void handleCancelSlot(slot.id);
                              }}
                            >
                              {cancellingId === slot.id ? "…" : "Annuler"}
                            </button>
                          </li>
                        ))}
                      </ul>
                    )}

                    {pastBookings.length > 0 ? (
                      <>
                        <p className="section-subheading">Historique</p>
                        <ul className="rdv-list rdv-list--past">
                          {pastBookings.map((slot) => (
                            <li key={slot.id} className="rdv-list__item card card--muted">
                              <div className="rdv-list__date">
                                <span className="rdv-list__day">
                                  {new Date(slot.slot_date).toLocaleDateString("fr-CA", { day: "numeric", month: "short" })}
                                </span>
                                <span className="rdv-list__weekday">
                                  {new Date(slot.slot_date).toLocaleDateString("fr-CA", { weekday: "long" })}
                                </span>
                              </div>
                              <div className="rdv-list__info">
                                <strong>{slot.start_time.slice(0, 5)}</strong>
                                <span className="inline-note">{slot.session_type}</span>
                              </div>
                              <span className={`rdv-list__badge rdv-badge--${slot.status}`}>
                                {slot.status === "confirmed" ? "Confirmé" : slot.status === "hold" ? "En attente" : slot.status === "cancelled" ? "Annulé" : slot.status}
                              </span>
                            </li>
                          ))}
                        </ul>
                      </>
                    ) : null}
                  </div>
                )}

                {/* ══ TAB : Ressources ══ */}
                {activeTab === "ressources" && (
                  <div className="mon-espace-tab-panel stack-md">
                    <div className="mon-espace-ressources-grid">
                      <article className="card stack-md">
                        <h3>Ressources membres</h3>
                        <p className="inline-note">Articles, supports et fiches de réflexion accessibles depuis votre espace.</p>
                        <Link href="/ressources" className="button button-secondary">Lire les ressources</Link>
                      </article>
                      <article className="card stack-md">
                        <h3>Mon suivi</h3>
                        <p className="inline-note">Consultez l&apos;avancement de votre démarche.</p>
                        <Link href="/suivi" className="button button-secondary">Voir mon suivi</Link>
                      </article>
                      {activeEntitlements.length > 0 ? (
                        <article className="card stack-md">
                          <h3>Mes crédits IVIA</h3>
                          <ul className="list-plain">
                            {activeEntitlements.map((e) => (
                              <li key={e.id}>
                                <strong>{e.entitlement_type_code}</strong>{" "}
                                · {e.quantity_remaining}/{e.quantity_total} disponible
                                {e.expires_at ? (
                                  <span className="inline-note">
                                    {" "}· expire le {new Date(e.expires_at).toLocaleDateString("fr-CA")}
                                  </span>
                                ) : null}
                              </li>
                            ))}
                          </ul>
                        </article>
                      ) : null}
                    </div>
                  </div>
                )}

                {/* ══ TAB : Journal ══ */}
                {activeTab === "journal" && (
                  <JournalTab token={data.session.access_token} />
                )}

                {/* ══ TAB : Profil ══ */}
                {activeTab === "profil" && (
                  <div className="mon-espace-tab-panel stack-md">
                    {data.client ? (
                      <ProfileEditCard
                        client={data.client}
                        token={data.session.access_token}
                        onUpdated={(updated) => setData((d) => (d ? { ...d, client: updated } : d))}
                      />
                    ) : null}
                    <SetPasswordCard token={data.session.access_token} firstTime={isMagicWelcome} />
                  </div>
                )}
              </>
            ) : null}
          </div>

        </main>
      </div>
    </PublicLayout>
  );
}

type ProfileEditCardProps = {
  client: MyClientRecord;
  token: string;
  onUpdated: (next: MyClientRecord) => void;
};

const LANGUAGE_OPTIONS: { code: string; label: string }[] = [
  { code: "fr-CA", label: "Français (Québec)" },
  { code: "en-CA", label: "English (Canada)" },
  { code: "es-CA", label: "Español" },
];

const TERRITORY_OPTIONS: { code: string; label: string }[] = [
  { code: "QC", label: "Québec" },
  { code: "ON", label: "Ontario" },
  { code: "NB", label: "Nouveau-Brunswick" },
  { code: "AUTRE", label: "Autre / hors Canada" },
];

function ProfileEditCard({ client, token, onUpdated }: ProfileEditCardProps) {
  const [firstNameOrAlias, setFirstNameOrAlias] = useState(client.first_name_or_alias);
  const [lastName, setLastName] = useState(client.last_name ?? "");
  const [phone, setPhone] = useState(client.phone ?? "");
  const [languageCode, setLanguageCode] = useState(client.language_code);
  const [territoryCode, setTerritoryCode] = useState(client.territory_code);
  const [isSaving, setIsSaving] = useState(false);
  const [savedAt, setSavedAt] = useState<Date | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSaving(true);
    setErrorMessage(null);
    try {
      const updated = await updateMyClient(
        {
          first_name_or_alias: firstNameOrAlias.trim() || null,
          last_name: lastName.trim() || null,
          phone: phone.trim() || null,
          language_code: languageCode || null,
          territory_code: territoryCode || null,
        },
        token,
      );
      onUpdated(updated);
      setSavedAt(new Date());
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Erreur inconnue.");
    } finally {
      setIsSaving(false);
    }
  }

  return (
    <article className="card stack-md">
      <h3>Compléter mon profil</h3>
      <p className="inline-note">
        Quelques précisions facultatives nous aident à mieux orienter votre accompagnement.
        Vous pouvez sauter cette étape pour l&apos;instant — rien n&apos;est obligatoire ici.
      </p>

      <form className="form-stack profile-edit-form" onSubmit={handleSubmit}>
        <label className="field">
          <span>Comment souhaitez-vous être appelé ?</span>
          <input
            value={firstNameOrAlias}
            onChange={(e) => setFirstNameOrAlias(e.target.value)}
            placeholder="Prénom ou alias"
          />
        </label>

        <div className="form-grid-2">
          <label className="field">
            <span>Nom (optionnel)</span>
            <input
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              placeholder="Nom de famille"
            />
          </label>

          <label className="field">
            <span>Téléphone (optionnel)</span>
            <input
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              placeholder="514 000 0000"
            />
          </label>
        </div>

        <div className="form-grid-2">
          <label className="field">
            <span>Langue de préférence</span>
            <select
              value={languageCode}
              onChange={(e) => setLanguageCode(e.target.value)}
            >
              {LANGUAGE_OPTIONS.map((o) => (
                <option key={o.code} value={o.code}>{o.label}</option>
              ))}
            </select>
          </label>

          <label className="field">
            <span>Territoire</span>
            <select
              value={territoryCode}
              onChange={(e) => setTerritoryCode(e.target.value)}
            >
              {TERRITORY_OPTIONS.map((o) => (
                <option key={o.code} value={o.code}>{o.label}</option>
              ))}
            </select>
          </label>
        </div>

        <button type="submit" className="button button-primary" disabled={isSaving}>
          {isSaving ? "Enregistrement…" : "Enregistrer mes informations"}
        </button>

        {errorMessage ? <p className="message message-error">{errorMessage}</p> : null}
        {savedAt && !errorMessage ? (
          <p className="profile-edit-saved">
            Enregistré à {savedAt.toLocaleTimeString("fr-CA")}.
          </p>
        ) : null}
      </form>
    </article>
  );
}

type SetPasswordCardProps = {
  token: string;
  firstTime: boolean;
};

function SetPasswordCard({ token, firstTime }: SetPasswordCardProps) {
  const [isOpen, setIsOpen] = useState(firstTime);
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isSaving, setIsSaving] = useState(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setErrorMessage(null);
    setSuccessMessage(null);

    if (newPassword.length < 8) {
      setErrorMessage("Le mot de passe doit contenir au moins 8 caractères.");
      return;
    }
    if (newPassword !== confirmPassword) {
      setErrorMessage("Les deux mots de passe ne correspondent pas.");
      return;
    }

    setIsSaving(true);
    try {
      const result = await setMyPassword(
        token,
        {
          new_password: newPassword,
          current_password: firstTime || !currentPassword ? null : currentPassword,
        },
      );
      setSuccessMessage(result.message);
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Erreur inconnue.");
    } finally {
      setIsSaving(false);
    }
  }

  return (
    <article className="card stack-md">
      <h3>{firstTime ? "Définir un mot de passe (optionnel)" : "Changer mon mot de passe"}</h3>
      <p className="inline-note">
        {firstTime
          ? "Vous êtes entré via un lien magique. Si vous voulez revenir plus facilement à votre espace, vous pouvez définir un mot de passe maintenant — ou plus tard, depuis cette page."
          : "Choisissez un nouveau mot de passe pour votre compte IVIA."}
      </p>

      {!isOpen ? (
        <button
          type="button"
          className="button button-secondary"
          onClick={() => setIsOpen(true)}
        >
          {firstTime ? "Définir mon mot de passe" : "Changer mon mot de passe"}
        </button>
      ) : (
        <form className="form-stack" onSubmit={handleSubmit}>
          {!firstTime ? (
            <label className="field">
              <span>Mot de passe actuel</span>
              <input
                type="password"
                autoComplete="current-password"
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
                placeholder="••••••••"
              />
              <span className="inline-note">
                Laissez vide si vous n&apos;en avez jamais défini.
              </span>
            </label>
          ) : null}

          <label className="field">
            <span>Nouveau mot de passe</span>
            <input
              required
              minLength={8}
              type="password"
              autoComplete="new-password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              placeholder="Au moins 8 caractères"
            />
          </label>

          <label className="field">
            <span>Confirmer le nouveau mot de passe</span>
            <input
              required
              minLength={8}
              type="password"
              autoComplete="new-password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Re-saisissez"
            />
          </label>

          <div className="public-access-actions">
            <button type="submit" className="button button-primary" disabled={isSaving}>
              {isSaving ? "Enregistrement…" : "Enregistrer"}
            </button>
            {!firstTime ? (
              <button
                type="button"
                className="button button-secondary"
                onClick={() => {
                  setIsOpen(false);
                  setErrorMessage(null);
                  setSuccessMessage(null);
                }}
              >
                Annuler
              </button>
            ) : null}
          </div>

          {errorMessage ? <p className="message message-error">{errorMessage}</p> : null}
          {successMessage ? (
            <p className="profile-edit-saved">{successMessage}</p>
          ) : null}
        </form>
      )}
    </article>
  );
}

export default function MonEspacePage() {
  return (
    <Suspense
      fallback={
        <PublicLayout>
          <div className="page-shell">
            <main className="section">
              <p className="inline-note">Chargement de votre espace…</p>
            </main>
          </div>
        </PublicLayout>
      }
    >
      <MonEspaceContent />
    </Suspense>
  );
}

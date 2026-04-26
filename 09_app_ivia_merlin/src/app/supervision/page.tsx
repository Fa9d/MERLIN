"use client";

import Link from "next/link";
import { FormEvent, useEffect, useState } from "react";

import {
  listDerivedDocuments,
  listSessionNotes,
  listSessions,
  loginOperator,
  type DerivedDocumentRecord,
  type LoginResponse,
  type SessionNoteRecord,
  type SessionNoteValidationPayload,
  type SessionRecord,
  validateSessionNote,
} from "@/lib/merlin-api";

const STORAGE_KEY = "merlin_supervision_session";
type ReviewFilter = "pending" | "needs_correction" | "validated" | "all";

function getReviewStatus(note: SessionNoteRecord) {
  if (note.validated_by_practitioner) {
    return {
      key: "validated",
      label: "Validee",
      description: "La note a deja ete validee par la supervision.",
    } as const;
  }
  if (note.practitioner_corrections) {
    return {
      key: "needs_correction",
      label: "A corriger",
      description: "La supervision a deja demande une correction.",
    } as const;
  }
  return {
    key: "pending",
    label: "A revoir",
    description: "La note attend une relecture supervision.",
  } as const;
}

function matchesReviewFilter(note: SessionNoteRecord, filter: ReviewFilter) {
  if (filter === "all") {
    return true;
  }
  return getReviewStatus(note).key === filter;
}

function getPublicationStatus(document: DerivedDocumentRecord | null) {
  if (!document) {
    return {
      key: "missing",
      label: "Aucun document",
      description: "Aucun document derive n'est encore relie a cette note.",
    } as const;
  }
  if (document.audience_code === "client" && document.client_visible) {
    return {
      key: "published",
      label: "Diffuse client",
      description: "Le document est actuellement visible cote client.",
    } as const;
  }
  if (document.audience_code === "client_pending_review") {
    return {
      key: "pending",
      label: "En attente supervision",
      description: "La diffusion client reste bloquee tant que la note n'est pas validee.",
    } as const;
  }
  return {
    key: "internal",
    label: "Interne",
    description: "Le document reste reserve a l'usage interne.",
  } as const;
}

export default function SupervisionPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [session, setSession] = useState<LoginResponse | null>(null);
  const [sessionNotes, setSessionNotes] = useState<SessionNoteRecord[]>([]);
  const [sessions, setSessions] = useState<SessionRecord[]>([]);
  const [derivedDocuments, setDerivedDocuments] = useState<DerivedDocumentRecord[]>([]);
  const [selectedNoteId, setSelectedNoteId] = useState("");
  const [reviewFilter, setReviewFilter] = useState<ReviewFilter>("pending");
  const [authErrorMessage, setAuthErrorMessage] = useState<string | null>(null);
  const [dashboardErrorMessage, setDashboardErrorMessage] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const [isLoadingDashboard, setIsLoadingDashboard] = useState(false);
  const [isUpdatingSessionNoteValidation, setIsUpdatingSessionNoteValidation] = useState(false);
  const [isCorrectionMode, setIsCorrectionMode] = useState(false);
  const [correctionCoeur, setCorrectionCoeur] = useState("");
  const [correctionCorps, setCorrectionCorps] = useState("");
  const [correctionEsprit, setCorrectionEsprit] = useState("");
  const [correctionEtre, setCorrectionEtre] = useState("");
  const [correctionTensions, setCorrectionTensions] = useState("");
  const [correctionVigilance, setCorrectionVigilance] = useState("");
  const [correctionNextStep, setCorrectionNextStep] = useState("");
  const isSupervisorSession = session?.user.role === "supervisor";

  useEffect(() => {
    if (typeof window === "undefined") {
      return;
    }

    window.setTimeout(() => {
      const stored = window.localStorage.getItem(STORAGE_KEY);
      if (!stored) {
        return;
      }

      try {
        setSession(JSON.parse(stored) as LoginResponse);
      } catch {
        window.localStorage.removeItem(STORAGE_KEY);
      }
    }, 0);
  }, []);

  useEffect(() => {
    if (!session || session.user.role !== "supervisor") {
      return;
    }

    const currentSession = session;
    let active = true;

    async function loadDashboard() {
      setIsLoadingDashboard(true);
      setDashboardErrorMessage(null);

      try {
        const [nextNotes, nextSessions, nextDerivedDocuments] = await Promise.all([
          listSessionNotes(currentSession.access_token),
          listSessions(currentSession.access_token),
          listDerivedDocuments(currentSession.access_token),
        ]);

        if (!active) {
          return;
        }

        setSessionNotes(nextNotes);
        setSessions(nextSessions);
        setDerivedDocuments(nextDerivedDocuments);
        setSelectedNoteId((current) => current || nextNotes[0]?.id || "");
      } catch (error) {
        if (!active) {
          return;
        }
        setDashboardErrorMessage(
          error instanceof Error
            ? error.message
            : "Impossible de charger les notes de supervision.",
        );
      } finally {
        if (active) {
          setIsLoadingDashboard(false);
        }
      }
    }

    void loadDashboard();

    return () => {
      active = false;
    };
  }, [session]);

  async function handleLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsLoggingIn(true);
    setAuthErrorMessage(null);

    try {
      const result = await loginOperator(email, password);
      setSession(result);
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(result));
    } catch (error) {
      setAuthErrorMessage(error instanceof Error ? error.message : "Connexion impossible.");
    } finally {
      setIsLoggingIn(false);
    }
  }

  function handleLogout() {
    window.localStorage.removeItem(STORAGE_KEY);
    setSession(null);
    setSessionNotes([]);
    setSessions([]);
    setDerivedDocuments([]);
    setSelectedNoteId("");
    setAuthErrorMessage(null);
    setDashboardErrorMessage(null);
    setSuccessMessage(null);
  }

  function resetCorrectionFields() {
    setCorrectionCoeur("");
    setCorrectionCorps("");
    setCorrectionEsprit("");
    setCorrectionEtre("");
    setCorrectionTensions("");
    setCorrectionVigilance("");
    setCorrectionNextStep("");
  }

  function hydrateCorrectionFields(note: SessionNoteRecord) {
    setCorrectionCoeur(note.coeur_summary_text ?? "");
    setCorrectionCorps(note.corps_summary_text ?? "");
    setCorrectionEsprit(note.esprit_summary_text ?? "");
    setCorrectionEtre(note.etre_summary_text ?? "");
    setCorrectionVigilance(note.vigilance_level_code ?? "");
    setCorrectionNextStep(note.next_session_focus_text ?? "");
    setCorrectionTensions(
      Array.isArray(note.identified_tensions_json)
        ? note.identified_tensions_json
            .map((item) =>
              typeof item === "object" && item && "tension_code" in item
                ? String(item.tension_code)
                : "",
            )
            .filter(Boolean)
            .join(", ")
        : "",
    );
  }

  function buildCorrectionPayload(): SessionNoteValidationPayload["corrections"] {
    const tensions = correctionTensions
      .split(",")
      .map((value) => value.trim())
      .filter(Boolean);

    const payload: NonNullable<SessionNoteValidationPayload["corrections"]> = {};
    if (correctionCoeur.trim()) payload.coeur = correctionCoeur.trim();
    if (correctionCorps.trim()) payload.corps = correctionCorps.trim();
    if (correctionEsprit.trim()) payload.esprit = correctionEsprit.trim();
    if (correctionEtre.trim()) payload.etre = correctionEtre.trim();
    if (tensions.length > 0) payload.tensions = tensions;
    if (correctionVigilance.trim()) payload.vigilance = correctionVigilance.trim();
    if (correctionNextStep.trim()) payload.next_step = correctionNextStep.trim();

    return Object.keys(payload).length > 0 ? payload : null;
  }

  async function handleValidateGeneratedNote(
    noteId: string,
    payload: SessionNoteValidationPayload,
    nextSuccessMessage: string,
  ) {
    if (!session) {
      return;
    }

    setIsUpdatingSessionNoteValidation(true);
    setDashboardErrorMessage(null);
    setSuccessMessage(null);

    try {
      await validateSessionNote(noteId, payload, session.access_token);
      const [nextNotes, nextDerivedDocuments] = await Promise.all([
        listSessionNotes(session.access_token),
        listDerivedDocuments(session.access_token),
      ]);
      setSessionNotes(nextNotes);
      setDerivedDocuments(nextDerivedDocuments);
      setSuccessMessage(nextSuccessMessage);
      if (payload.validated || payload.corrections) {
        setIsCorrectionMode(false);
        resetCorrectionFields();
      }
    } catch (error) {
      setDashboardErrorMessage(
        error instanceof Error
          ? error.message
          : "Impossible de mettre a jour la validation supervision.",
      );
    } finally {
      setIsUpdatingSessionNoteValidation(false);
    }
  }

  const filteredNotes = [...sessionNotes]
    .filter((note) => matchesReviewFilter(note, reviewFilter))
    .sort((left, right) => {
      const leftStatus = getReviewStatus(left);
      const rightStatus = getReviewStatus(right);
      const priority = {
        pending: 0,
        needs_correction: 1,
        validated: 2,
      } as const;
      const statusDelta = priority[leftStatus.key] - priority[rightStatus.key];
      if (statusDelta !== 0) {
        return statusDelta;
      }
      return right.updated_at.localeCompare(left.updated_at);
    });

  const effectiveSelectedNoteId = filteredNotes.some((note) => note.id === selectedNoteId)
    ? selectedNoteId
    : (filteredNotes[0]?.id ?? "");
  const selectedNote = filteredNotes.find((note) => note.id === effectiveSelectedNoteId) ?? null;
  const selectedSession =
    selectedNote ? sessions.find((item) => item.id === selectedNote.session_id) ?? null : null;
  const selectedDocument = selectedNote
    ? [...derivedDocuments]
        .filter((document) => document.source_note_id === selectedNote.id)
        .sort((left, right) => right.updated_at.localeCompare(left.updated_at))[0] ?? null
    : null;
  const selectedReviewStatus = selectedNote ? getReviewStatus(selectedNote) : null;
  const selectedPublicationStatus = getPublicationStatus(selectedDocument);
  const reviewCounts = {
    pending: sessionNotes.filter((note) => getReviewStatus(note).key === "pending").length,
    needsCorrection: sessionNotes.filter((note) => getReviewStatus(note).key === "needs_correction")
      .length,
    validated: sessionNotes.filter((note) => getReviewStatus(note).key === "validated").length,
    published: derivedDocuments.filter(
      (document) => document.audience_code === "client" && document.client_visible,
    ).length,
  };

  return (
    <div className="page-shell">
      <header className="topbar">
        <div className="wordmark">MERLIN / Supervision</div>
        <nav className="nav">
          <Link href="/">Accueil</Link>
          <Link href="/operator">Operateur</Link>
          <Link href="/admin">Admin</Link>
        </nav>
      </header>

      <main className="section">
        <div className="section-header">
          <div className="eyebrow">SCR-201 a SCR-203</div>
          <h2>Supervision et validation V1</h2>
          <p>
            Cette surface est reservee a la relecture et a la validation. Elle ne doit
            pas etre confondue avec la production operateur. Une validation positive
            publie aussi la synthese client si une diffusion a ete demandee.
          </p>
        </div>

        {!session ? (
          <form className="card form-stack" onSubmit={handleLogin}>
            <h3>Connexion supervision</h3>
            <label className="field">
              <span>Courriel</span>
              <input value={email} onChange={(event) => setEmail(event.target.value)} type="email" />
            </label>
            <label className="field">
              <span>Mot de passe</span>
              <input
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                type="password"
              />
            </label>
            <button className="button button-primary" disabled={isLoggingIn} type="submit">
              {isLoggingIn ? "Connexion..." : "Se connecter"}
            </button>
            {authErrorMessage ? <p className="message message-error">{authErrorMessage}</p> : null}
          </form>
        ) : !isSupervisorSession ? (
          <article className="card">
            <h3>Session ouverte hors perimetre supervision</h3>
            <p>
              Connecte comme <span className="mono">{session.user.email}</span>
            </p>
            <p>Role: {session.user.role}</p>
            <div className="cta-row">
              {session.user.role === "operator" ? (
                <Link className="button button-secondary" href="/operator">
                  Aller a l&apos;operateur
                </Link>
              ) : null}
              {session.user.role === "admin_tech" ? (
                <Link className="button button-secondary" href="/admin">
                  Aller a l&apos;administration
                </Link>
              ) : null}
              <button className="button button-secondary" onClick={handleLogout} type="button">
                Se deconnecter
              </button>
            </div>
          </article>
        ) : (
          <div className="grid operator-layout">
            <article className="card">
              <h3>Session supervision</h3>
              <p>
                Connecte comme <span className="mono">{session.user.email}</span>
              </p>
              <p>Role: {session.user.role}</p>
              <div className="cta-row">
                <button className="button button-secondary" onClick={handleLogout} type="button">
                  Se deconnecter
                </button>
              </div>
            </article>

            <article className="card">
              <div className="stack-md">
                <h3>File de notes</h3>
                <div className="stats-grid">
                  <article className="stat-card">
                    <span className="stat-label">A revoir</span>
                    <strong className="stat-value">{reviewCounts.pending}</strong>
                  </article>
                  <article className="stat-card">
                    <span className="stat-label">A corriger</span>
                    <strong className="stat-value">{reviewCounts.needsCorrection}</strong>
                  </article>
                  <article className="stat-card">
                    <span className="stat-label">Validees</span>
                    <strong className="stat-value">{reviewCounts.validated}</strong>
                  </article>
                  <article className="stat-card">
                    <span className="stat-label">Diffusees client</span>
                    <strong className="stat-value">{reviewCounts.published}</strong>
                  </article>
                </div>
                {isLoadingDashboard ? <p>Chargement...</p> : null}
                {dashboardErrorMessage ? (
                  <p className="message message-error">{dashboardErrorMessage}</p>
                ) : null}
                {successMessage ? <p className="message message-success">{successMessage}</p> : null}

                {sessionNotes.length === 0 && !isLoadingDashboard ? (
                  <p>Aucune note disponible pour la supervision.</p>
                ) : null}

                {sessionNotes.length > 0 ? (
                  <>
                    <label className="field">
                      <span>Vue</span>
                      <select
                        value={reviewFilter}
                        onChange={(event) => setReviewFilter(event.target.value as ReviewFilter)}
                      >
                        <option value="pending">Priorite: a revoir</option>
                        <option value="needs_correction">A corriger</option>
                        <option value="validated">Validees</option>
                        <option value="all">Toutes les notes</option>
                      </select>
                    </label>

                    <label className="field">
                      <span>Note</span>
                      <select
                        value={effectiveSelectedNoteId}
                        onChange={(event) => {
                          setSelectedNoteId(event.target.value);
                          setIsCorrectionMode(false);
                          resetCorrectionFields();
                        }}
                      >
                        {filteredNotes.map((note) => {
                          const noteSession =
                            sessions.find((item) => item.id === note.session_id) ?? null;
                          const sessionLabel = noteSession
                            ? `S-${noteSession.session_sequence_number}`
                            : note.session_id.slice(0, 8);
                          const reviewStatus = getReviewStatus(note);
                          return (
                            <option key={note.id} value={note.id}>
                              {`N-${note.note_sequence_number} / ${sessionLabel} / ${reviewStatus.label}`}
                            </option>
                          );
                        })}
                      </select>
                    </label>

                    <div className="table-wrap">
                      <table className="data-table">
                        <thead>
                          <tr>
                            <th>Note</th>
                            <th>Seance</th>
                            <th>Resume</th>
                            <th>Validation</th>
                          </tr>
                        </thead>
                        <tbody>
                          {filteredNotes.map((note) => {
                            const noteSession =
                              sessions.find((item) => item.id === note.session_id) ?? null;
                            const reviewStatus = getReviewStatus(note);
                            const linkedDocument =
                              derivedDocuments.find((document) => document.source_note_id === note.id) ??
                              null;
                            const publicationStatus = getPublicationStatus(linkedDocument);
                            return (
                              <tr key={note.id}>
                                <td className="mono">N-{note.note_sequence_number}</td>
                                <td className="mono">
                                  {noteSession
                                    ? `S-${noteSession.session_sequence_number}`
                                    : note.session_id.slice(0, 8)}
                                </td>
                                <td>{note.summary_text}</td>
                                <td>{reviewStatus.label}</td>
                                <td>{publicationStatus.label}</td>
                              </tr>
                            );
                          })}
                        </tbody>
                      </table>
                    </div>
                  </>
                ) : null}
              </div>
            </article>

            {selectedNote ? (
              <article className="card form-stack">
                <div className="info-strip">
                  <span className="mono">N-{selectedNote.note_sequence_number}</span>
                  <span>
                    {selectedSession
                      ? `S-${selectedSession.session_sequence_number}`
                      : selectedNote.session_id.slice(0, 8)}
                  </span>
                  {selectedReviewStatus ? (
                    <span className={`status-pill status-pill-${selectedReviewStatus.key}`}>
                      {selectedReviewStatus.label}
                    </span>
                  ) : null}
                  <span className={`status-pill status-pill-${selectedPublicationStatus.key}`}>
                    {selectedPublicationStatus.label}
                  </span>
                  <span>
                    {selectedNote.validated_at
                      ? new Date(selectedNote.validated_at).toLocaleString("fr-CA")
                      : "Aucune validation"}
                  </span>
                </div>

                <div className="form-grid-2">
                  <div className="card">
                    <h4>Resume</h4>
                    <p>{selectedNote.summary_text}</p>
                  </div>
                  <div className="card">
                    <h4>Supervision</h4>
                    <p>{selectedNote.supervision_summary_text ?? "Aucune synthese supervision."}</p>
                  </div>
                </div>

                <div className="form-grid-2">
                  <div className="card">
                    <h4>Statut de revue</h4>
                    <p>{selectedReviewStatus?.description}</p>
                  </div>
                  <div className="card">
                    <h4>Etat de diffusion client</h4>
                    <p>{selectedPublicationStatus.description}</p>
                  </div>
                </div>

                <div className="form-grid-2">
                  <div className="card">
                    <h4>Resume client</h4>
                    <p>{selectedNote.client_facing_summary_text ?? "Aucun resume client genere."}</p>
                  </div>
                  <div className="card">
                    <h4>Document derive</h4>
                    <p>{selectedDocument?.body_text ?? "Aucun document derive relie a cette note."}</p>
                  </div>
                </div>

                <div className="form-grid-2">
                  <label className="field">
                    <span>Coeur</span>
                    <textarea readOnly rows={2} value={selectedNote.coeur_summary_text ?? ""} />
                  </label>
                  <label className="field">
                    <span>Corps</span>
                    <textarea readOnly rows={2} value={selectedNote.corps_summary_text ?? ""} />
                  </label>
                  <label className="field">
                    <span>Esprit</span>
                    <textarea readOnly rows={2} value={selectedNote.esprit_summary_text ?? ""} />
                  </label>
                  <label className="field">
                    <span>Etre</span>
                    <textarea readOnly rows={2} value={selectedNote.etre_summary_text ?? ""} />
                  </label>
                </div>

                <label className="field">
                  <span>Hypotheses contextuelles</span>
                  <textarea
                    readOnly
                    rows={4}
                    value={
                      selectedNote.context_hypotheses_json
                        ? JSON.stringify(selectedNote.context_hypotheses_json, null, 2)
                        : ""
                    }
                  />
                </label>

                {selectedNote.practitioner_corrections ? (
                  <label className="field">
                    <span>Corrections deja enregistrees</span>
                    <textarea
                      readOnly
                      rows={4}
                      value={JSON.stringify(selectedNote.practitioner_corrections, null, 2)}
                    />
                  </label>
                ) : null}

                <div className="cta-row">
                  <button
                    className="button button-primary"
                    disabled={isUpdatingSessionNoteValidation}
                    onClick={() =>
                      void handleValidateGeneratedNote(
                        selectedNote.id,
                        { validated: true, corrections: null },
                        "Note validee par la supervision. La diffusion client est activee si elle etait demandee.",
                      )
                    }
                    style={{ backgroundColor: "#1f7a45", borderColor: "#1f7a45" }}
                    type="button"
                  >
                    {isUpdatingSessionNoteValidation ? "Validation..." : "Valider"}
                  </button>
                  <button
                    className="button button-secondary"
                    disabled={isUpdatingSessionNoteValidation}
                    onClick={() => {
                      setIsCorrectionMode((current) => !current);
                      hydrateCorrectionFields(selectedNote);
                    }}
                    type="button"
                  >
                    Corriger
                  </button>
                  <button
                    className="button button-secondary"
                    disabled={isUpdatingSessionNoteValidation}
                    onClick={() =>
                      void handleValidateGeneratedNote(
                        selectedNote.id,
                        { validated: false, corrections: buildCorrectionPayload() },
                        "Note rejetee par la supervision.",
                      )
                    }
                    style={{ backgroundColor: "#9b2c2c", borderColor: "#9b2c2c", color: "#fff" }}
                    type="button"
                  >
                    {isUpdatingSessionNoteValidation ? "Mise a jour..." : "Rejeter"}
                  </button>
                </div>

                {isCorrectionMode ? (
                  <div className="form-stack">
                    <h4>Correction supervision</h4>
                    <div className="form-grid-2">
                      <label className="field">
                        <span>Coeur</span>
                        <textarea
                          rows={2}
                          value={correctionCoeur}
                          onChange={(event) => setCorrectionCoeur(event.target.value)}
                        />
                      </label>
                      <label className="field">
                        <span>Corps</span>
                        <textarea
                          rows={2}
                          value={correctionCorps}
                          onChange={(event) => setCorrectionCorps(event.target.value)}
                        />
                      </label>
                      <label className="field">
                        <span>Esprit</span>
                        <textarea
                          rows={2}
                          value={correctionEsprit}
                          onChange={(event) => setCorrectionEsprit(event.target.value)}
                        />
                      </label>
                      <label className="field">
                        <span>Etre</span>
                        <textarea
                          rows={2}
                          value={correctionEtre}
                          onChange={(event) => setCorrectionEtre(event.target.value)}
                        />
                      </label>
                    </div>

                    <label className="field">
                      <span>Tensions (codes separes par virgule)</span>
                      <input
                        value={correctionTensions}
                        onChange={(event) => setCorrectionTensions(event.target.value)}
                      />
                    </label>

                    <div className="form-grid-2">
                      <label className="field">
                        <span>Vigilance</span>
                        <input
                          value={correctionVigilance}
                          onChange={(event) => setCorrectionVigilance(event.target.value)}
                        />
                      </label>
                      <label className="field">
                        <span>Prochaine etape</span>
                        <input
                          value={correctionNextStep}
                          onChange={(event) => setCorrectionNextStep(event.target.value)}
                        />
                      </label>
                    </div>

                    <div className="cta-row">
                      <button
                        className="button button-primary"
                        disabled={isUpdatingSessionNoteValidation}
                        onClick={() =>
                          void handleValidateGeneratedNote(
                            selectedNote.id,
                            {
                              validated: true,
                              corrections: buildCorrectionPayload(),
                            },
                            "Corrections supervision enregistrees. La diffusion client est activee si elle etait demandee.",
                          )
                        }
                        type="button"
                      >
                        {isUpdatingSessionNoteValidation ? "Enregistrement..." : "Appliquer la correction"}
                      </button>
                      <button
                        className="button button-secondary"
                        disabled={isUpdatingSessionNoteValidation}
                        onClick={() => {
                          setIsCorrectionMode(false);
                          resetCorrectionFields();
                        }}
                        type="button"
                      >
                        Annuler
                      </button>
                    </div>
                  </div>
                ) : null}
              </article>
            ) : null}
          </div>
        )}
      </main>
    </div>
  );
}

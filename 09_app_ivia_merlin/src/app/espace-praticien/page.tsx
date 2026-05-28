"use client";

import Link from "next/link";
import { FormEvent, useEffect, useState } from "react";

import { OperatorLiveKitPanel } from "@/components/operator-livekit-panel";
import {
  type AudioRecordingRecord,
  type AudioSessionRecord,
  closeSession,
  createSessionNote,
  type ClientRecord,
  type ConsentRecord,
  type DerivedDocumentRecord,
  type IntakeRequestRecord,
  listAudioRecordings,
  listAudioSessions,
  listClients,
  listConsents,
  listDerivedDocuments,
  listIntakeRequests,
  listSessionNotes,
  listSessions,
  loginOperator,
  provisionAudioSession,
  startAudioRecording,
  startSession,
  stopAudioRecording,
  type LoginResponse,
  type SessionCloseResult,
  type SessionNoteRecord,
  type SessionNoteValidationPayload,
  type SessionRecord,
  createSession,
  validateSessionNote,
  // Agenda
  type ScheduleSlotRecord,
  type ScheduleExceptionRecord,
  type AvailableSlotRecord,
  listMySchedule,
  createScheduleSlot,
  deleteScheduleSlot,
  listMyExceptions,
  createScheduleException,
  deleteScheduleException,
  listAvailableSlots,
  // Ancres temporelles
  type EmotionalChargeCode,
  type SessionTemporalAnchorRecord,
  type SessionTemporalAnchorCreatePayload,
  listSessionTemporalAnchors,
  createSessionTemporalAnchor,
  archiveSessionTemporalAnchor,
} from "@/lib/merlin-api";

const STORAGE_KEY = "merlin_praticien_session";
const INTAKE_CONSENT_TYPES = [
  "consent_session",
  "consent_session_note",
  "consent_history",
] as const;

const SESSION_MODE_LABELS: Record<string, string> = {
  intake: "Premier RDV",
  standard: "Suivi",
  follow_up: "Reprise",
};

const SESSION_STATUS_LABELS: Record<string, string> = {
  scheduled: "Planifiée",
  in_progress: "En cours",
  completed: "Complétée",
  cancelled: "Annulée",
  no_show: "Absence",
  escalated: "Escaladée",
};

type ActiveView = "clients" | "seance" | "cloture" | "historique" | "agenda" | "ancres";

export default function PraticienPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [session, setSession] = useState<LoginResponse | null>(null);
  const [activeView, setActiveView] = useState<ActiveView>("clients");

  // Données
  const [clients, setClients] = useState<ClientRecord[]>([]);
  const [consents, setConsents] = useState<ConsentRecord[]>([]);
  const [intakeRequests, setIntakeRequests] = useState<IntakeRequestRecord[]>([]);
  const [sessions, setSessions] = useState<SessionRecord[]>([]);
  const [sessionNotes, setSessionNotes] = useState<SessionNoteRecord[]>([]);
  const [audioSessions, setAudioSessions] = useState<AudioSessionRecord[]>([]);
  const [audioRecordings, setAudioRecordings] = useState<AudioRecordingRecord[]>([]);
  const [derivedDocuments, setDerivedDocuments] = useState<DerivedDocumentRecord[]>([]);

  // Sélections
  const [selectedClientId, setSelectedClientId] = useState("");
  const [selectedSessionId, setSelectedSessionId] = useState("");

  // Formulaire nouvelle séance
  const [sessionModeCode, setSessionModeCode] = useState<"intake" | "standard" | "follow_up">("intake");
  const [sessionChannelCode, setSessionChannelCode] = useState<"direct" | "in_person" | "async">("direct");
  const [scheduledStartAt, setScheduledStartAt] = useState("");
  const [durationMinutes, setDurationMinutes] = useState("60");

  // Formulaire clôture
  const [actualStartAt, setActualStartAt] = useState("");
  const [actualEndAt, setActualEndAt] = useState("");
  const [finalSessionStatus, setFinalSessionStatus] = useState<"completed" | "cancelled" | "no_show" | "escalated">("completed");
  const [presentingTopicText, setPresentingTopicText] = useState("");
  const [sessionHighlightsText, setSessionHighlightsText] = useState("");
  const [operatorAssessmentText, setOperatorAssessmentText] = useState("");
  const [vigilanceLevelCode, setVigilanceLevelCode] = useState<"non_urgent" | "watch" | "priority" | "urgent">("non_urgent");
  const [followUpActionsText, setFollowUpActionsText] = useState("");
  const [nextSessionFocusText, setNextSessionFocusText] = useState("");
  const [clientVisible, setClientVisible] = useState(false);

  // Messages
  const [authError, setAuthError] = useState<string | null>(null);
  const [globalError, setGlobalError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  // Indicateurs de chargement
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const [isLoadingData, setIsLoadingData] = useState(false);
  const [isCreatingSession, setIsCreatingSession] = useState(false);
  const [isStartingSession, setIsStartingSession] = useState(false);
  const [isClosingSession, setIsClosingSession] = useState(false);
  const [isProvisioningAudio, setIsProvisioningAudio] = useState(false);
  const [isStartingRecording, setIsStartingRecording] = useState(false);
  const [isStoppingRecording, setIsStoppingRecording] = useState(false);
  const [isValidatingNote, setIsValidatingNote] = useState(false);
  const [noteCorrections, setNoteCorrections] = useState<SessionNoteValidationPayload["corrections"]>(null);
  const [expandedNoteId, setExpandedNoteId] = useState<string | null>(null);

  // Note rapide post-séance
  const [quickNoteText, setQuickNoteText] = useState("");
  const [isSubmittingQuickNote, setIsSubmittingQuickNote] = useState(false);

  // Agenda — gabarit hebdomadaire
  const [scheduleSlots, setScheduleSlots] = useState<ScheduleSlotRecord[]>([]);
  const [exceptions, setExceptions] = useState<ScheduleExceptionRecord[]>([]);
  const [isLoadingSchedule, setIsLoadingSchedule] = useState(false);
  const [scheduleError, setScheduleError] = useState<string | null>(null);
  const [scheduleSuccess, setScheduleSuccess] = useState<string | null>(null);

  // Agenda — vue calendrier mensuelle
  const [agendaCalMonth, setAgendaCalMonth] = useState<Date>(() => {
    const d = new Date(); d.setDate(1); d.setHours(0, 0, 0, 0); return d;
  });
  const [agendaMonthSlots, setAgendaMonthSlots] = useState<AvailableSlotRecord[]>([]);
  const [loadingAgendaCal, setLoadingAgendaCal] = useState(false);

  // Formulaire nouveau bloc
  const [newSlotDay, setNewSlotDay] = useState<number>(0);
  const [newSlotStart, setNewSlotStart] = useState("09:00");
  const [newSlotEnd, setNewSlotEnd] = useState("17:00");
  const [newSlotDuration, setNewSlotDuration] = useState<number>(60);
  const [newSlotBuffer, setNewSlotBuffer] = useState<number>(15);
  const [newSlotType, setNewSlotType] = useState<"intake" | "standard" | "follow_up" | "any">("standard");
  const [isAddingSlot, setIsAddingSlot] = useState(false);

  // Formulaire exception
  const [newExcDate, setNewExcDate] = useState("");
  const [newExcType, setNewExcType] = useState<"blocked" | "extra">("blocked");
  const [newExcReason, setNewExcReason] = useState("");
  const [isAddingException, setIsAddingException] = useState(false);

  // Ancres temporelles
  const [temporalAnchors, setTemporalAnchors] = useState<SessionTemporalAnchorRecord[]>([]);
  const [isLoadingAnchors, setIsLoadingAnchors] = useState(false);
  const [anchorVerbatim, setAnchorVerbatim] = useState("");
  const [anchorYear, setAnchorYear] = useState("");
  const [anchorAge, setAnchorAge] = useState("");
  const [anchorOffsetSec, setAnchorOffsetSec] = useState("");
  const [anchorCharge, setAnchorCharge] = useState<EmotionalChargeCode | "">("");
  const [anchorIsSilence, setAnchorIsSilence] = useState(false);
  const [anchorInterpretation, setAnchorInterpretation] = useState("");
  const [isSavingAnchor, setIsSavingAnchor] = useState(false);
  const [archivingAnchorId, setArchivingAnchorId] = useState<string | null>(null);

  // Restaurer la session depuis le localStorage
  useEffect(() => {
    if (typeof window === "undefined") return;
    window.setTimeout(() => {
      const stored = window.localStorage.getItem(STORAGE_KEY);
      if (!stored) return;
      try {
        const parsed = JSON.parse(stored) as LoginResponse;
        if (parsed.user.role !== "practitioner") {
          window.localStorage.removeItem(STORAGE_KEY);
          return;
        }
        setSession(parsed);
      } catch {
        window.localStorage.removeItem(STORAGE_KEY);
      }
    }, 0);
  }, []);

  // Charger les données après connexion
  useEffect(() => {
    if (!session || session.user.role !== "practitioner") return;
    const currentSession = session;
    let active = true;

    async function loadData() {
      setIsLoadingData(true);
      setGlobalError(null);
      try {
        const [
          clientsData,
          consentsData,
          intakeData,
          sessionsData,
          notesData,
          audioSessionsData,
          audioRecordingsData,
          derivedDocsData,
        ] = await Promise.all([
          listClients(currentSession.access_token),
          listConsents(currentSession.access_token),
          listIntakeRequests(currentSession.access_token),
          listSessions(currentSession.access_token),
          listSessionNotes(currentSession.access_token),
          listAudioSessions(currentSession.access_token),
          listAudioRecordings(currentSession.access_token),
          listDerivedDocuments(currentSession.access_token),
        ]);
        if (!active) return;
        setClients(clientsData);
        setConsents(consentsData);
        setIntakeRequests(intakeData);
        setSessions(sessionsData);
        setSessionNotes(notesData);
        setAudioSessions(audioSessionsData);
        setAudioRecordings(audioRecordingsData);
        setDerivedDocuments(derivedDocsData);
      } catch (error) {
        if (!active) return;
        setGlobalError(error instanceof Error ? error.message : "Impossible de charger les données.");
      } finally {
        if (active) setIsLoadingData(false);
      }
    }

    async function loadSchedule() {
      setIsLoadingSchedule(true);
      try {
        const [slots, excs] = await Promise.all([
          listMySchedule(currentSession.access_token),
          listMyExceptions(currentSession.access_token),
        ]);
        if (!active) return;
        setScheduleSlots(slots);
        setExceptions(excs);
      } catch {
        // non-bloquant
      } finally {
        if (active) setIsLoadingSchedule(false);
      }
    }

    void loadData();
    void loadSchedule();
    return () => { active = false; };
  }, [session]);

  // Chargement des créneaux disponibles du mois (agenda praticien)
  useEffect(() => {
    if (!session || activeView !== "agenda") return;
    let active = true;
    const y = agendaCalMonth.getFullYear();
    const m = agendaCalMonth.getMonth();
    const mFrom = `${y}-${String(m + 1).padStart(2, "0")}-01`;
    const mTo = new Date(y, m + 1, 0).toISOString().slice(0, 10);
    setLoadingAgendaCal(true);
    setAgendaMonthSlots([]);
    listAvailableSlots(session.user.id, mFrom, mTo)
      .then((slots) => { if (active) setAgendaMonthSlots(slots); })
      .catch(() => {})
      .finally(() => { if (active) setLoadingAgendaCal(false); });
    return () => { active = false; };
  }, [session, activeView, agendaCalMonth]);

  // Chargement des ancres temporelles pour la séance sélectionnée
  useEffect(() => {
    if (!session || activeView !== "ancres" || !selectedSessionId) {
      setTemporalAnchors([]);
      return;
    }
    let active = true;
    setIsLoadingAnchors(true);
    listSessionTemporalAnchors(selectedSessionId, session.access_token)
      .then((data) => { if (active) setTemporalAnchors(data); })
      .catch(() => {})
      .finally(() => { if (active) setIsLoadingAnchors(false); });
    return () => { active = false; };
  }, [session, activeView, selectedSessionId]);

  async function handleLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsLoggingIn(true);
    setAuthError(null);
    try {
      const result = await loginOperator(email, password);
      if (result.user.role !== "practitioner") {
        setAuthError("Cet espace est réservé aux praticiens. Votre compte n'a pas le rôle requis.");
        setIsLoggingIn(false);
        return;
      }
      setSession(result);
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(result));
    } catch (error) {
      setAuthError(error instanceof Error ? error.message : "Connexion impossible.");
    } finally {
      setIsLoggingIn(false);
    }
  }

  function handleLogout() {
    window.localStorage.removeItem(STORAGE_KEY);
    setSession(null);
    setClients([]);
    setConsents([]);
    setIntakeRequests([]);
    setSessions([]);
    setSessionNotes([]);
    setAudioSessions([]);
    setAudioRecordings([]);
    setDerivedDocuments([]);
    setAuthError(null);
    setGlobalError(null);
    setSuccessMessage(null);
  }

  function clearMessages() {
    setGlobalError(null);
    setSuccessMessage(null);
  }

  async function refreshData() {
    if (!session) return;
    const [
      nextSessions,
      nextNotes,
      nextAudioSessions,
      nextAudioRecordings,
      nextDocs,
    ] = await Promise.all([
      listSessions(session.access_token),
      listSessionNotes(session.access_token),
      listAudioSessions(session.access_token),
      listAudioRecordings(session.access_token),
      listDerivedDocuments(session.access_token),
    ]);
    setSessions(nextSessions);
    setSessionNotes(nextNotes);
    setAudioSessions(nextAudioSessions);
    setAudioRecordings(nextAudioRecordings);
    setDerivedDocuments(nextDocs);
  }

  async function handleCreateSession(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!session || !selectedClientId) return;
    clearMessages();
    setIsCreatingSession(true);
    try {
      const created = await createSession(
        {
          client_id: selectedClientId,
          session_mode_code: sessionModeCode,
          session_channel_code: sessionChannelCode,
          scheduled_start_at: scheduledStartAt ? new Date(scheduledStartAt).toISOString() : null,
          duration_minutes: durationMinutes ? Number(durationMinutes) : null,
          session_status_code: "scheduled",
        },
        session.access_token,
      );
      await provisionAudioSession(created.id, session.access_token);
      await refreshData();
      setSelectedSessionId(created.id);
      setSuccessMessage(`Séance ${created.session_sequence_number} créée et salle audio préparée.`);
      setActiveView("seance");
    } catch (error) {
      setGlobalError(error instanceof Error ? error.message : "Impossible de créer la séance.");
    } finally {
      setIsCreatingSession(false);
    }
  }

  async function handleStartSession() {
    if (!session || !selectedSessionId) return;
    clearMessages();
    setIsStartingSession(true);
    try {
      const started = await startSession(
        selectedSessionId,
        { actual_start_at: actualStartAt ? new Date(actualStartAt).toISOString() : null },
        session.access_token,
      );
      await refreshData();
      setActualStartAt(
        started.actual_start_at
          ? new Date(started.actual_start_at).toISOString().slice(0, 16)
          : new Date().toISOString().slice(0, 16),
      );
      setSuccessMessage(`Séance ${started.session_sequence_number} démarrée.`);
    } catch (error) {
      setGlobalError(error instanceof Error ? error.message : "Impossible de démarrer la séance.");
    } finally {
      setIsStartingSession(false);
    }
  }

  async function handleStartRecording() {
    if (!session || !selectedAudioSession) return;
    clearMessages();
    setIsStartingRecording(true);
    try {
      await startAudioRecording(selectedAudioSession.id, session.access_token);
      await refreshData();
      setSuccessMessage("Enregistrement démarré.");
    } catch (error) {
      setGlobalError(error instanceof Error ? error.message : "Impossible de démarrer l'enregistrement.");
    } finally {
      setIsStartingRecording(false);
    }
  }

  async function handleStopRecording() {
    if (!session || !selectedAudioRecording) return;
    clearMessages();
    setIsStoppingRecording(true);
    try {
      await stopAudioRecording(selectedAudioRecording.id, session.access_token);
      await refreshData();
      setSuccessMessage("Enregistrement arrêté.");
    } catch (error) {
      setGlobalError(error instanceof Error ? error.message : "Impossible d'arrêter l'enregistrement.");
    } finally {
      setIsStoppingRecording(false);
    }
  }

  async function handleQuickNote(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!session || !selectedSessionId || !quickNoteText.trim()) return;
    const selectedSession_ = sessions.find((s) => s.id === selectedSessionId);
    if (!selectedSession_) return;
    clearMessages();
    setIsSubmittingQuickNote(true);
    try {
      await createSessionNote(
        {
          session_id: selectedSessionId,
          client_id: selectedSession_.client_id,
          summary_text: quickNoteText.trim(),
        },
        session.access_token,
      );
      await refreshData();
      setQuickNoteText("");
      setSuccessMessage("Note enregistrée.");
    } catch (error) {
      setGlobalError(error instanceof Error ? error.message : "Impossible d'enregistrer la note.");
    } finally {
      setIsSubmittingQuickNote(false);
    }
  }

  async function handleValidateNote(noteId: string, withCorrections: boolean) {
    if (!session) return;
    clearMessages();
    setIsValidatingNote(true);
    try {
      const payload: SessionNoteValidationPayload = {
        validated: true,
        corrections: withCorrections ? noteCorrections : null,
      };
      await validateSessionNote(noteId, payload, session.access_token);
      await refreshData();
      setNoteCorrections(null);
      setExpandedNoteId(null);
      setSuccessMessage("Note validée.");
    } catch (error) {
      setGlobalError(error instanceof Error ? error.message : "Impossible de valider la note.");
    } finally {
      setIsValidatingNote(false);
    }
  }

  async function handleCloseSession(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!session || !selectedSessionId) return;
    clearMessages();
    setIsClosingSession(true);
    try {
      const result: SessionCloseResult = await closeSession(
        selectedSessionId,
        {
          actual_start_at: actualStartAt ? new Date(actualStartAt).toISOString() : null,
          actual_end_at: actualEndAt ? new Date(actualEndAt).toISOString() : null,
          session_status_code: finalSessionStatus,
          presenting_topic_text: presentingTopicText,
          session_highlights_text: sessionHighlightsText,
          operator_assessment_text: operatorAssessmentText || null,
          vigilance_level_code: vigilanceLevelCode,
          follow_up_actions_text: followUpActionsText || null,
          next_session_focus_text: nextSessionFocusText || null,
          client_visible: clientVisible,
        },
        session.access_token,
      );
      await refreshData();
      setSuccessMessage(
        clientVisible
          ? `Séance ${result.session.session_sequence_number} clôturée. Document généré — en attente de validation supervision avant diffusion client.`
          : `Séance ${result.session.session_sequence_number} clôturée. Note ${result.generated_note.note_sequence_number} générée pour usage interne.`,
      );
      setPresentingTopicText("");
      setSessionHighlightsText("");
      setOperatorAssessmentText("");
      setFollowUpActionsText("");
      setNextSessionFocusText("");
      setClientVisible(false);
      setActualEndAt("");
      setActiveView("historique");
    } catch (error) {
      setGlobalError(error instanceof Error ? error.message : "Impossible de clôturer la séance.");
    } finally {
      setIsClosingSession(false);
    }
  }

  async function handleCreateAnchor(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!session || !selectedSessionId) return;
    const selectedSession_ = sessions.find((s) => s.id === selectedSessionId);
    if (!selectedSession_) return;
    clearMessages();
    setIsSavingAnchor(true);
    try {
      const payload: SessionTemporalAnchorCreatePayload = {
        client_id: selectedSession_.client_id,
        verbatim_fragment: anchorVerbatim.trim() || null,
        event_year_approx: anchorYear ? parseInt(anchorYear, 10) : null,
        client_age_ref: anchorAge ? parseInt(anchorAge, 10) : null,
        said_at_offset_sec: anchorOffsetSec ? parseInt(anchorOffsetSec, 10) : null,
        emotional_charge: anchorCharge || null,
        is_silence_marker: anchorIsSilence,
        interpretation_note: anchorInterpretation.trim() || null,
      };
      const anchor = await createSessionTemporalAnchor(selectedSessionId, payload, session.access_token);
      setTemporalAnchors((prev) => [...prev, anchor].sort(
        (a, b) => (a.said_at_offset_sec ?? Infinity) - (b.said_at_offset_sec ?? Infinity),
      ));
      setAnchorVerbatim("");
      setAnchorYear("");
      setAnchorAge("");
      setAnchorOffsetSec("");
      setAnchorCharge("");
      setAnchorIsSilence(false);
      setAnchorInterpretation("");
    } catch (error) {
      setGlobalError(error instanceof Error ? error.message : "Impossible d\u2019enregistrer l\u2019ancre.");
    } finally {
      setIsSavingAnchor(false);
    }
  }

  async function handleArchiveAnchor(anchorId: string) {
    if (!session || !selectedSessionId) return;
    setArchivingAnchorId(anchorId);
    try {
      await archiveSessionTemporalAnchor(selectedSessionId, anchorId, session.access_token);
      setTemporalAnchors((prev) => prev.filter((a) => a.id !== anchorId));
    } catch (error) {
      setGlobalError(error instanceof Error ? error.message : "Impossible de supprimer l\u2019ancre.");
    } finally {
      setArchivingAnchorId(null);
    }
  }

  // Dérivés
  const selectedClient = clients.find((c) => c.id === selectedClientId) ?? null;
  const selectedClientIntakeRequest =
    intakeRequests.find((ir) => ir.client_id === selectedClientId) ?? null;
  const selectedClientConsents = consents.filter((c) => c.client_id === selectedClientId);
  const selectedSession = sessions.find((s) => s.id === selectedSessionId) ?? null;
  const selectedAudioSession =
    audioSessions.find((a) => a.session_id === selectedSessionId) ?? null;
  const selectedAudioRecording =
    audioRecordings.find((r) => r.audio_session_id === selectedAudioSession?.id) ?? null;
  const activeSessions = sessions.filter(
    (s) => s.session_status_code === "scheduled" || s.session_status_code === "in_progress",
  );
  const sessionOptions = sessions.map((s) => {
    const client = clients.find((c) => c.id === s.client_id);
    return {
      id: s.id,
      label: `S-${s.session_sequence_number} · ${client?.public_client_code ?? s.client_id.slice(0, 8)} · ${s.session_mode_code} · ${s.session_status_code}`,
    };
  });
  const selectedSessionNotes = sessionNotes.filter((n) => n.session_id === selectedSessionId);
  const selectedSessionDocs = derivedDocuments.filter((d) => d.session_id === selectedSessionId);

  if (!session) {
    return (
      <div className="page-shell">
        <header className="topbar">
          <div className="wordmark">IVIA · MERLIN</div>
          <nav className="nav">
            <Link href="/">Accueil</Link>
          </nav>
        </header>
        <main className="section">
          <div className="section-header">
            <h2>Espace praticien</h2>
            <p className="muted-sm-text">
              Connectez-vous pour accéder à vos clients et séances.
            </p>
          </div>
          <form className="card form-stack auth-card-narrow" onSubmit={handleLogin}>
            <label className="field">
              <span>Courriel</span>
              <input
                autoComplete="email"
                required
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </label>
            <label className="field">
              <span>Mot de passe</span>
              <input
                autoComplete="current-password"
                required
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </label>
            {authError ? <p className="message message-error">{authError}</p> : null}
            <div className="cta-row">
              <button className="button button-primary" disabled={isLoggingIn} type="submit">
                {isLoggingIn ? "Connexion..." : "Se connecter"}
              </button>
            </div>
          </form>
        </main>
      </div>
    );
  }

  return (
    <div className="page-shell">
      <header className="topbar">
        <div className="wordmark">IVIA · MERLIN</div>
        <nav className="nav">
          <Link href="/">Accueil</Link>
          <Link href="/supervision">Supervision</Link>
          <button
            className="button button-secondary button-xs"
            onClick={handleLogout}
            type="button"
          >
            Déconnexion
          </button>
        </nav>
      </header>

      <main className="section">
        <div className="section-header">
          <h2>Espace praticien</h2>
          <p className="section-subtitle">
            {session.user.display_name} · {session.user.email}
          </p>
        </div>

        {isLoadingData ? (
          <p className="inline-note">Chargement des données...</p>
        ) : null}

        {globalError ? (
          <p className="message message-error message-mb">{globalError}</p>
        ) : null}
        {successMessage ? (
          <p className="message message-success message-mb">{successMessage}</p>
        ) : null}

        {/* Navigation interne */}
        <nav className="praticien-nav">
          {(["clients", "seance", "cloture", "historique", "agenda", "ancres"] as ActiveView[]).map((view) => {
            const labels: Record<ActiveView, string> = {
              clients: "Clients",
              seance: `Séances (${activeSessions.length})`,
              cloture: "Clôturer",
              historique: "Historique",
              agenda: "Mon Agenda",
              ancres: selectedSessionId ? `Ancres (${temporalAnchors.length})` : "Ancres",
            };
            return (
              <button
                key={view}
                className={`button button-sm ${activeView === view ? "button-primary" : "button-secondary"}`}
                onClick={() => { clearMessages(); setActiveView(view); }}
                type="button"
              >
                {labels[view]}
              </button>
            );
          })}
        </nav>

        {/* === CLIENTS === */}
        {activeView === "clients" && (
          <div className="stack-md">

            {/* Formulaire nouvelle séance — visible uniquement si un client est sélectionné */}
            {selectedClientId ? (
              <div className="card form-stack">
                <div className="section-header-row">
                  <h3>Nouvelle séance — {selectedClient?.first_name_or_alias}</h3>
                  <button
                    className="button button-secondary button-xs"
                    onClick={() => setSelectedClientId("")}
                    type="button"
                  >
                    Changer de client
                  </button>
                </div>

                {selectedClient ? (
                  <div className="info-strip">
                    <span className="mono">{selectedClient.public_client_code}</span>
                    {selectedClient.email ? <span>{selectedClient.email}</span> : null}
                    {selectedClientIntakeRequest ? (
                      <span>Besoin : {selectedClientIntakeRequest.primary_need_code}</span>
                    ) : null}
                    <span>
                      Consentements :{" "}
                      {INTAKE_CONSENT_TYPES.map((type) => {
                        const consent = selectedClientConsents.find((c) => c.consent_type_code === type);
                        const short = { consent_session: "S", consent_session_note: "N", consent_history: "H" } as const;
                        return `${short[type]}:${consent ? (consent.consent_value ? "✓" : "✗") : "—"}`;
                      }).join("  ")}
                    </span>
                  </div>
                ) : null}

                <form className="form-stack" onSubmit={handleCreateSession}>
                  <div className="form-grid-2">
                    <label className="field">
                      <span>Mode</span>
                      <select value={sessionModeCode} onChange={(e) => setSessionModeCode(e.target.value as typeof sessionModeCode)}>
                        <option value="intake">Premier RDV</option>
                        <option value="standard">Suivi</option>
                        <option value="follow_up">Reprise</option>
                      </select>
                      <span className="field-hint">
                        {sessionModeCode === "intake" && "Ouverture du dossier — évaluation initiale, contexte et besoins."}
                        {sessionModeCode === "standard" && "Séance ordinaire dans une relation continue."}
                        {sessionModeCode === "follow_up" && "Retour après interruption — reconstitution historique, état actuel et plan de suite."}
                      </span>
                    </label>
                    <label className="field">
                      <span>Canal</span>
                      <select value={sessionChannelCode} onChange={(e) => setSessionChannelCode(e.target.value as typeof sessionChannelCode)}>
                        <option value="direct">Direct</option>
                        <option value="in_person">Présentiel</option>
                        <option value="async">Asynchrone</option>
                      </select>
                    </label>
                  </div>

                  <div className="form-grid-2">
                    <label className="field">
                      <span>Début planifié</span>
                      <input type="datetime-local" value={scheduledStartAt} onChange={(e) => setScheduledStartAt(e.target.value)} />
                    </label>
                    <label className="field">
                      <span>Durée estimée (min)</span>
                      <input type="number" min="15" step="5" value={durationMinutes} onChange={(e) => setDurationMinutes(e.target.value)} />
                    </label>
                  </div>

                  <div className="cta-row">
                    <button className="button button-primary" disabled={isCreatingSession} type="submit">
                      {isCreatingSession ? "Création..." : "Créer la séance et préparer la salle"}
                    </button>
                  </div>
                </form>
              </div>
            ) : null}

            {clients.length === 0 ? (
              <p className="muted-text">Aucun client enregistré pour le moment.</p>
            ) : (
              <>
                {/* Section 1 — Demandes en attente (intake soumis, aucune séance) */}
                {(() => {
                  const pending = clients.filter((c) => {
                    const hasIntake = intakeRequests.some((ir) => ir.client_id === c.id);
                    const hasSessions = sessions.some((s) => s.client_id === c.id);
                    return hasIntake && !hasSessions;
                  });
                  if (pending.length === 0) return null;
                  return (
                    <div className="card">
                      <h3 className="section-label-urgent">Demandes en attente ({pending.length})</h3>
                      <div className="table-wrap">
                        <table className="data-table">
                          <thead>
                            <tr>
                              <th>Client</th>
                              <th>Besoin</th>
                              <th>Urgence</th>
                              <th>Demande</th>
                              <th></th>
                            </tr>
                          </thead>
                          <tbody>
                            {pending.map((c) => {
                              const ir = intakeRequests.find((r) => r.client_id === c.id);
                              return (
                                <tr key={c.id}>
                                  <td>
                                    <span className="mono">{c.public_client_code}</span>{" "}
                                    {c.first_name_or_alias}
                                  </td>
                                  <td>{ir?.primary_need_code ?? "—"}</td>
                                  <td>{ir?.perceived_urgency_code ?? "—"}</td>
                                  <td className="text-muted-sm">{ir?.requested_outcome_text ?? "—"}</td>
                                  <td>
                                    <button
                                      className="button button-primary button-xs"
                                      onClick={() => {
                                        setSelectedClientId(c.id);
                                        setSessionModeCode("intake");
                                        clearMessages();
                                      }}
                                      type="button"
                                    >
                                      Créer séance
                                    </button>
                                  </td>
                                </tr>
                              );
                            })}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  );
                })()}

                {/* Section 2 — Séances actives */}
                {(() => {
                  const activeClientIds = new Set(
                    sessions
                      .filter((s) => s.session_status_code === "scheduled" || s.session_status_code === "in_progress")
                      .map((s) => s.client_id),
                  );
                  const active = clients.filter((c) => activeClientIds.has(c.id));
                  if (active.length === 0) return null;
                  return (
                    <div className="card">
                      <h3>Séances en cours ({active.length})</h3>
                      <div className="table-wrap">
                        <table className="data-table">
                          <thead>
                            <tr>
                              <th>Client</th>
                              <th>Séance</th>
                              <th>Mode</th>
                              <th>Statut</th>
                              <th></th>
                            </tr>
                          </thead>
                          <tbody>
                            {active.map((c) => {
                              const activeSess = sessions.find(
                                (s) =>
                                  s.client_id === c.id &&
                                  (s.session_status_code === "scheduled" || s.session_status_code === "in_progress"),
                              );
                              return (
                                <tr key={c.id}>
                                  <td>
                                    <span className="mono">{c.public_client_code}</span>{" "}
                                    {c.first_name_or_alias}
                                  </td>
                                  <td className="mono">S-{activeSess?.session_sequence_number}</td>
                                  <td>{activeSess ? (SESSION_MODE_LABELS[activeSess.session_mode_code] ?? activeSess.session_mode_code) : "—"}</td>
                                  <td>{activeSess ? (SESSION_STATUS_LABELS[activeSess.session_status_code] ?? activeSess.session_status_code) : "—"}</td>
                                  <td>
                                    <button
                                      className="button button-secondary button-xs"
                                      onClick={() => {
                                        setSelectedClientId(c.id);
                                        if (activeSess) setSelectedSessionId(activeSess.id);
                                        clearMessages();
                                        setActiveView("seance");
                                      }}
                                      type="button"
                                    >
                                      Reprendre →
                                    </button>
                                  </td>
                                </tr>
                              );
                            })}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  );
                })()}

                {/* Section 3 — Dossiers fermés */}
                {(() => {
                  const closedStatuses = new Set(["completed", "cancelled", "no_show", "escalated"]);
                  const closedClientIds = new Set(
                    sessions.filter((s) => closedStatuses.has(s.session_status_code)).map((s) => s.client_id),
                  );
                  const activeClientIds = new Set(
                    sessions
                      .filter((s) => s.session_status_code === "scheduled" || s.session_status_code === "in_progress")
                      .map((s) => s.client_id),
                  );
                  const closed = clients.filter(
                    (c) => closedClientIds.has(c.id) && !activeClientIds.has(c.id),
                  );
                  if (closed.length === 0) return null;
                  return (
                    <div className="card">
                      <h3 className="text-muted">Dossiers fermés ({closed.length})</h3>
                      <div className="table-wrap">
                        <table className="data-table">
                          <thead>
                            <tr>
                              <th>Client</th>
                              <th>Séances</th>
                              <th>Courriel</th>
                              <th></th>
                            </tr>
                          </thead>
                          <tbody>
                            {closed.map((c) => {
                              const clientSessions = sessions.filter((s) => s.client_id === c.id);
                              return (
                                <tr key={c.id}>
                                  <td>
                                    <span className="mono">{c.public_client_code}</span>{" "}
                                    {c.first_name_or_alias}
                                  </td>
                                  <td>{clientSessions.length}</td>
                                  <td>{c.email ?? "—"}</td>
                                  <td>
                                    <button
                                      className="button button-secondary button-xs"
                                      onClick={() => {
                                        setSelectedClientId(c.id);
                                        clearMessages();
                                        setActiveView("historique");
                                      }}
                                      type="button"
                                    >
                                      Historique →
                                    </button>
                                  </td>
                                </tr>
                              );
                            })}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  );
                })()}

                {/* Clients sans intake ni séance */}
                {(() => {
                  const noIntakeNoSession = clients.filter(
                    (c) =>
                      !intakeRequests.some((ir) => ir.client_id === c.id) &&
                      !sessions.some((s) => s.client_id === c.id),
                  );
                  if (noIntakeNoSession.length === 0) return null;
                  return (
                    <div className="card">
                      <h3 className="text-muted">Sans demande active ({noIntakeNoSession.length})</h3>
                      <div className="table-wrap">
                        <table className="data-table">
                          <thead>
                            <tr>
                              <th>Code</th>
                              <th>Nom</th>
                              <th>Courriel</th>
                              <th></th>
                            </tr>
                          </thead>
                          <tbody>
                            {noIntakeNoSession.map((c) => (
                              <tr key={c.id}>
                                <td className="mono">{c.public_client_code}</td>
                                <td>{c.first_name_or_alias}</td>
                                <td>{c.email ?? "—"}</td>
                                <td>
                                  <button
                                    className="button button-secondary button-xs"
                                    onClick={() => { setSelectedClientId(c.id); clearMessages(); }}
                                    type="button"
                                  >
                                    Sélectionner
                                  </button>
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  );
                })()}
              </>
            )}
          </div>
        )}

        {/* === SÉANCE EN COURS === */}
        {activeView === "seance" && (
          <div className="stack-md">
            <div className="card form-stack">
              <h3>Séance active</h3>

              <label className="field">
                <span>Séance</span>
                <select value={selectedSessionId} onChange={(e) => setSelectedSessionId(e.target.value)}>
                  <option value="">— Sélectionner une séance —</option>
                  {sessionOptions.map((opt) => (
                    <option key={opt.id} value={opt.id}>{opt.label}</option>
                  ))}
                </select>
              </label>

              {selectedSession ? (
                <div className="info-strip">
                  <span className="mono">S-{selectedSession.session_sequence_number}</span>
                  <span>{SESSION_STATUS_LABELS[selectedSession.session_status_code] ?? selectedSession.session_status_code}</span>
                  <span>{SESSION_MODE_LABELS[selectedSession.session_mode_code] ?? selectedSession.session_mode_code} · {selectedSession.session_channel_code}</span>
                  {selectedSession.duration_minutes ? <span>{selectedSession.duration_minutes} min</span> : null}
                </div>
              ) : null}

              {selectedSession?.session_status_code === "scheduled" ? (
                <div className="form-stack">
                  <label className="field">
                    <span>Heure de début réelle</span>
                    <input type="datetime-local" value={actualStartAt} onChange={(e) => setActualStartAt(e.target.value)} />
                  </label>
                  <div className="cta-row">
                    <button className="button button-primary" disabled={isStartingSession || !selectedSessionId} onClick={handleStartSession} type="button">
                      {isStartingSession ? "Démarrage..." : "Démarrer la séance"}
                    </button>
                  </div>
                </div>
              ) : null}

              {selectedSession?.session_status_code === "in_progress" && selectedAudioSession ? (
                <div className="form-stack">
                  <div className="info-strip">
                    <span className="mono">{selectedAudioSession.room_name}</span>
                    <span>{selectedAudioSession.audio_session_status_code}</span>
                    {selectedAudioRecording ? (
                      <span>{selectedAudioRecording.audio_recording_status_code}</span>
                    ) : null}
                  </div>

                  <OperatorLiveKitPanel
                    key={selectedAudioSession.id}
                    audioSession={selectedAudioSession}
                    operatorAccessToken={session.access_token}
                  />

                  {selectedAudioRecording?.failure_reason ? (
                    <p className="message message-error">{selectedAudioRecording.failure_reason}</p>
                  ) : null}

                  <div className="cta-row">
                    <button
                      className="button button-secondary"
                      disabled={isStartingRecording || selectedAudioRecording?.audio_recording_status_code === "recording"}
                      onClick={handleStartRecording}
                      type="button"
                    >
                      {isStartingRecording ? "Démarrage..." : "Démarrer l'enregistrement"}
                    </button>
                    <button
                      className="button button-secondary"
                      disabled={isStoppingRecording || selectedAudioRecording?.audio_recording_status_code !== "recording"}
                      onClick={handleStopRecording}
                      type="button"
                    >
                      {isStoppingRecording ? "Arrêt..." : "Arrêter l'enregistrement"}
                    </button>
                    <button
                      className="button button-primary"
                      onClick={() => { clearMessages(); setActiveView("cloture"); }}
                      type="button"
                    >
                      Clôturer la séance →
                    </button>
                    <button
                      className="button button-secondary"
                      onClick={() => { clearMessages(); setActiveView("ancres"); }}
                      type="button"
                    >
                      Ancres temporelles →
                    </button>
                  </div>
                </div>
              ) : null}

              {activeSessions.length === 0 && sessions.length > 0 ? (
                <p className="inline-note">Aucune séance active. Créez une nouvelle séance depuis l'onglet Clients.</p>
              ) : null}
            </div>

            {/* Note rapide post-séance */}
            {selectedSessionId ? (
              <div className="card form-stack">
                <h3>Note rapide post-séance</h3>
                <form className="form-stack" onSubmit={handleQuickNote}>
                  <label className="field">
                    <span>Résumé / observations</span>
                    <textarea
                      required
                      rows={4}
                      placeholder="Points saillants, observations, suites envisagées…"
                      value={quickNoteText}
                      onChange={(e) => setQuickNoteText(e.target.value)}
                    />
                  </label>
                  <div className="cta-row">
                    <button className="button button-primary" disabled={isSubmittingQuickNote || !quickNoteText.trim()} type="submit">
                      {isSubmittingQuickNote ? "Enregistrement..." : "Enregistrer la note"}
                    </button>
                  </div>
                </form>
              </div>
            ) : null}
          </div>
        )}

        {/* === CLÔTURE === */}
        {activeView === "cloture" && (
          <div className="card form-stack">
            <h3>Clôturer une séance</h3>
            <form className="form-stack" onSubmit={handleCloseSession}>
              <label className="field">
                <span>Séance</span>
                <select required value={selectedSessionId} onChange={(e) => setSelectedSessionId(e.target.value)}>
                  <option value="">— Sélectionner une séance —</option>
                  {sessionOptions.map((opt) => (
                    <option key={opt.id} value={opt.id}>{opt.label}</option>
                  ))}
                </select>
              </label>

              <div className="form-grid-2">
                <label className="field">
                  <span>Début réel</span>
                  <input type="datetime-local" value={actualStartAt} onChange={(e) => setActualStartAt(e.target.value)} />
                </label>
                <label className="field">
                  <span>Fin réelle</span>
                  <input type="datetime-local" value={actualEndAt} onChange={(e) => setActualEndAt(e.target.value)} />
                </label>
              </div>

              <div className="form-grid-2">
                <label className="field">
                  <span>Statut final</span>
                  <select value={finalSessionStatus} onChange={(e) => setFinalSessionStatus(e.target.value as typeof finalSessionStatus)}>
                    <option value="completed">Complétée</option>
                    <option value="cancelled">Annulée</option>
                    <option value="no_show">Absence</option>
                    <option value="escalated">Escaladée</option>
                  </select>
                </label>
                <label className="field">
                  <span>Niveau de vigilance</span>
                  <select value={vigilanceLevelCode} onChange={(e) => setVigilanceLevelCode(e.target.value as typeof vigilanceLevelCode)}>
                    <option value="non_urgent">Non urgent</option>
                    <option value="watch">Surveillance</option>
                    <option value="priority">Prioritaire</option>
                    <option value="urgent">Urgent</option>
                  </select>
                </label>
              </div>

              <label className="field">
                <span>Sujet principal traité *</span>
                <textarea required rows={2} value={presentingTopicText} onChange={(e) => setPresentingTopicText(e.target.value)} />
              </label>

              <label className="field">
                <span>Points saillants de la séance *</span>
                <textarea required rows={3} value={sessionHighlightsText} onChange={(e) => setSessionHighlightsText(e.target.value)} />
              </label>

              <label className="field">
                <span>Évaluation praticien</span>
                <textarea rows={3} value={operatorAssessmentText} onChange={(e) => setOperatorAssessmentText(e.target.value)} />
              </label>

              <label className="field">
                <span>Suites proposées</span>
                <textarea rows={2} value={followUpActionsText} onChange={(e) => setFollowUpActionsText(e.target.value)} />
              </label>

              <label className="field">
                <span>Focus prochaine séance</span>
                <textarea rows={2} value={nextSessionFocusText} onChange={(e) => setNextSessionFocusText(e.target.value)} />
              </label>

              <label className="checkbox-row">
                <input
                  checked={clientVisible}
                  type="checkbox"
                  onChange={(e) => setClientVisible(e.target.checked)}
                />
                <span>Proposer une diffusion au client après validation supervision</span>
              </label>

              <div className="cta-row">
                <button
                  className="button button-primary"
                  disabled={isClosingSession || !selectedSessionId || !presentingTopicText.trim() || !sessionHighlightsText.trim()}
                  type="submit"
                >
                  {isClosingSession ? "Clôture en cours..." : "Clôturer et générer la note"}
                </button>
              </div>
            </form>
          </div>
        )}

        {/* === HISTORIQUE === */}
        {activeView === "historique" && (
          <div className="stack-md">
            <div className="card form-stack">
              <h3>Filtrer par séance</h3>
              <label className="field">
                <span>Séance</span>
                <select value={selectedSessionId} onChange={(e) => setSelectedSessionId(e.target.value)}>
                  <option value="">— Toutes les séances —</option>
                  {sessionOptions.map((opt) => (
                    <option key={opt.id} value={opt.id}>{opt.label}</option>
                  ))}
                </select>
              </label>
            </div>

            {sessions.length > 0 ? (
              <div className="card">
                <h3>Séances</h3>
                <div className="table-wrap">
                  <table className="data-table">
                    <thead>
                      <tr>
                        <th>Séq.</th>
                        <th>Client</th>
                        <th>Mode</th>
                        <th>Canal</th>
                        <th>Statut</th>
                        <th>Durée</th>
                      </tr>
                    </thead>
                    <tbody>
                      {sessions.map((s) => {
                        const client = clients.find((c) => c.id === s.client_id);
                        return (
                          <tr
                            key={s.id}
                            className={`row-clickable${selectedSessionId === s.id ? " row-selected" : ""}`}
                            onClick={() => setSelectedSessionId(s.id)}
                          >
                            <td className="mono">S-{s.session_sequence_number}</td>
                            <td className="mono">{client?.public_client_code ?? s.client_id.slice(0, 8)}</td>
                            <td>{SESSION_MODE_LABELS[s.session_mode_code] ?? s.session_mode_code}</td>
                            <td>{s.session_channel_code === "direct" ? "Direct" : s.session_channel_code === "in_person" ? "Présentiel" : s.session_channel_code === "async" ? "Asynchrone" : s.session_channel_code}</td>
                            <td>{SESSION_STATUS_LABELS[s.session_status_code] ?? s.session_status_code}</td>
                            <td>{s.duration_minutes ?? "—"}</td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </div>
            ) : null}

            {selectedSessionNotes.length > 0 ? (
              <div className="card form-stack">
                <h3>Note de séance</h3>
                {selectedSessionNotes.map((note) => (
                  <div key={note.id} className="form-stack">
                    <div className="info-strip">
                      <span className="mono">N-{note.note_sequence_number}</span>
                      <span>{note.validated_by_practitioner ? "✓ Validée" : "Non validée"}</span>
                      {note.validated_at ? (
                        <span>{new Date(note.validated_at).toLocaleString("fr-CA")}</span>
                      ) : null}
                      {note.vigilance_level_code !== "non_urgent" ? (
                        <span>Vigilance : {note.vigilance_level_code === "watch" ? "Surveillance" : note.vigilance_level_code === "priority" ? "Prioritaire" : "Urgent"}</span>
                      ) : null}
                    </div>

                    {(note.coeur_summary_text || note.corps_summary_text || note.esprit_summary_text || note.etre_summary_text) ? (
                      <div className="form-grid-2">
                        {note.coeur_summary_text ? (
                          <div className="card">
                            <h4>Cœur</h4>
                            <p>{note.coeur_summary_text}</p>
                          </div>
                        ) : null}
                        {note.corps_summary_text ? (
                          <div className="card">
                            <h4>Corps</h4>
                            <p>{note.corps_summary_text}</p>
                          </div>
                        ) : null}
                        {note.esprit_summary_text ? (
                          <div className="card">
                            <h4>Esprit</h4>
                            <p>{note.esprit_summary_text}</p>
                          </div>
                        ) : null}
                        {note.etre_summary_text ? (
                          <div className="card">
                            <h4>Être</h4>
                            <p>{note.etre_summary_text}</p>
                          </div>
                        ) : null}
                      </div>
                    ) : null}

                    {note.client_facing_summary_text ? (
                      <div className="card">
                        <h4>Synthèse client</h4>
                        <p>{note.client_facing_summary_text}</p>
                      </div>
                    ) : null}

                    {!note.validated_by_practitioner ? (
                      <div className="form-stack">
                        {expandedNoteId === note.id ? (
                          <div className="form-stack">
                            <p className="inline-note">Corrections optionnelles — laisser vide pour valider sans changement.</p>
                            <div className="form-grid-2">
                              <label className="field">
                                <span>Cœur (correction)</span>
                                <textarea
                                  rows={2}
                                  value={noteCorrections?.coeur ?? ""}
                                  onChange={(e) => setNoteCorrections((prev) => ({ ...prev, coeur: e.target.value || undefined }))}
                                />
                              </label>
                              <label className="field">
                                <span>Corps (correction)</span>
                                <textarea
                                  rows={2}
                                  value={noteCorrections?.corps ?? ""}
                                  onChange={(e) => setNoteCorrections((prev) => ({ ...prev, corps: e.target.value || undefined }))}
                                />
                              </label>
                              <label className="field">
                                <span>Esprit (correction)</span>
                                <textarea
                                  rows={2}
                                  value={noteCorrections?.esprit ?? ""}
                                  onChange={(e) => setNoteCorrections((prev) => ({ ...prev, esprit: e.target.value || undefined }))}
                                />
                              </label>
                              <label className="field">
                                <span>Être (correction)</span>
                                <textarea
                                  rows={2}
                                  value={noteCorrections?.etre ?? ""}
                                  onChange={(e) => setNoteCorrections((prev) => ({ ...prev, etre: e.target.value || undefined }))}
                                />
                              </label>
                            </div>
                            <div className="cta-row">
                              <button
                                className="button button-primary"
                                disabled={isValidatingNote}
                                onClick={() => handleValidateNote(note.id, true)}
                                type="button"
                              >
                                {isValidatingNote ? "Validation..." : "Valider avec corrections"}
                              </button>
                              <button
                                className="button button-secondary"
                                onClick={() => { setExpandedNoteId(null); setNoteCorrections(null); }}
                                type="button"
                              >
                                Annuler
                              </button>
                            </div>
                          </div>
                        ) : (
                          <div className="cta-row">
                            <button
                              className="button button-primary"
                              disabled={isValidatingNote}
                              onClick={() => handleValidateNote(note.id, false)}
                              type="button"
                            >
                              {isValidatingNote ? "Validation..." : "Valider la note"}
                            </button>
                            <button
                              className="button button-secondary"
                              onClick={() => { setExpandedNoteId(note.id); setNoteCorrections(null); }}
                              type="button"
                            >
                              Valider avec corrections
                            </button>
                          </div>
                        )}
                      </div>
                    ) : null}
                  </div>
                ))}
              </div>
            ) : selectedSessionId ? (
              <p className="muted-text">Aucune note pour cette séance.</p>
            ) : null}

            {selectedSessionDocs.length > 0 ? (
              <div className="card form-stack">
                <h3>Document dérivé</h3>
                {selectedSessionDocs.map((doc) => (
                  <div key={doc.id} className="form-stack">
                    <div className="info-strip">
                      <span>{doc.title}</span>
                      <span>{doc.audience_code === "client" && doc.client_visible ? "Diffusé client" : doc.audience_code === "client_pending_review" ? "En attente supervision" : "Interne"}</span>
                    </div>
                    <label className="field">
                      <span>Contenu</span>
                      <textarea readOnly rows={5} value={doc.body_text} />
                    </label>
                  </div>
                ))}
              </div>
            ) : selectedSessionId ? (
              <p className="muted-text">Aucun document dérivé pour cette séance.</p>
            ) : null}
          </div>
        )}

        {/* === AGENDA — Gabarit hebdomadaire === */}
        {activeView === "agenda" && (
          <div className="stack-md">

            {/* Vue calendrier mensuelle */}
            <div className="card">
              <div className="reserver-month-nav">
                <button
                  type="button"
                  className="button button-text"
                  onClick={() => setAgendaCalMonth((prev) => new Date(prev.getFullYear(), prev.getMonth() - 1, 1))}
                >
                  ← Précédent
                </button>
                <span className="reserver-week-label">
                  {agendaCalMonth.toLocaleDateString("fr-CA", { month: "long", year: "numeric" })}
                </span>
                <button
                  type="button"
                  className="button button-text"
                  onClick={() => setAgendaCalMonth((prev) => new Date(prev.getFullYear(), prev.getMonth() + 1, 1))}
                >
                  Suivant →
                </button>
              </div>
              {loadingAgendaCal ? (
                <p className="muted-text">Chargement…</p>
              ) : (
                <div className="reserver-month-grid">
                  {["Lu", "Ma", "Me", "Je", "Ve", "Sa", "Di"].map((d) => (
                    <div key={d} className="reserver-month-head">{d}</div>
                  ))}
                  {(() => {
                    const today = new Date().toISOString().slice(0, 10);
                    const y = agendaCalMonth.getFullYear();
                    const m = agendaCalMonth.getMonth();
                    const firstWd = new Date(y, m, 1).getDay();
                    const prefix = firstWd === 0 ? 6 : firstWd - 1;
                    const daysInMonth = new Date(y, m + 1, 0).getDate();
                    const slotDates = new Set(agendaMonthSlots.map((s) => s.slot_date));
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
                      const hasSlots = slotDates.has(cell.iso) && cell.iso >= today;
                      const isToday = cell.iso === today;
                      const isPast = cell.iso < today;
                      return (
                        <div
                          key={cell.iso}
                          className={`reserver-month-cell${hasSlots ? " has-slots" : ""}${isToday ? " is-today" : ""}${isPast ? " is-past" : ""}`}
                          title={hasSlots ? `${agendaMonthSlots.filter((s) => s.slot_date === cell.iso).length} créneau(x)` : undefined}
                        >
                          <span className="reserver-month-cell__num">{cell.day}</span>
                          {hasSlots && <span className="reserver-month-cell__dot" aria-hidden="true" />}
                        </div>
                      );
                    });
                  })()}
                </div>
              )}
              <p className="muted-text" style={{ fontSize: "0.75rem", marginTop: "0.5rem" }}>
                Les points indiquent vos créneaux disponibles à la réservation ce mois-ci.
              </p>
            </div>
            <div className="card form-stack">
              <h3>Gabarit hebdomadaire</h3>
              <p className="muted-text">
                Définissez vos blocs de disponibilité récurrents. Les créneaux seront générés
                automatiquement pour les clients lors de la prise de rendez-vous.
              </p>

              {scheduleError ? <p className="message message-error">{scheduleError}</p> : null}
              {scheduleSuccess ? <p className="message message-success">{scheduleSuccess}</p> : null}

              {/* Liste des blocs existants */}
              {isLoadingSchedule ? (
                <p className="muted-text">Chargement…</p>
              ) : scheduleSlots.length === 0 ? (
                <p className="muted-text">Aucun bloc de disponibilité défini.</p>
              ) : (
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Jour</th>
                      <th>Début</th>
                      <th>Fin</th>
                      <th>Durée</th>
                      <th>Tampon</th>
                      <th>Type</th>
                      <th>Actif</th>
                      <th></th>
                    </tr>
                  </thead>
                  <tbody>
                    {scheduleSlots.map((slot) => (
                      <tr key={slot.id}>
                        <td>{slot.day_label}</td>
                        <td>{slot.start_time.slice(0, 5)}</td>
                        <td>{slot.end_time.slice(0, 5)}</td>
                        <td>{slot.session_duration_minutes} min</td>
                        <td>{slot.buffer_minutes} min</td>
                        <td>{slot.session_type_label}</td>
                        <td>{slot.is_active ? "✓" : "—"}</td>
                        <td>
                          <button
                            className="button button-danger button-xs"
                            type="button"
                            onClick={async () => {
                              if (!session) return;
                              try {
                                await deleteScheduleSlot(slot.id, session.access_token);
                                setScheduleSlots((prev) => prev.filter((s) => s.id !== slot.id));
                                setScheduleSuccess("Bloc supprimé.");
                              } catch (e) {
                                setScheduleError(e instanceof Error ? e.message : "Erreur suppression.");
                              }
                            }}
                          >
                            Supprimer
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>

            {/* Formulaire — nouveau bloc */}
            <div className="card form-stack">
              <h3>Ajouter un bloc</h3>
              <div className="form-grid-auto">
                <label className="field">
                  <span>Jour</span>
                  <select value={newSlotDay} onChange={(e) => setNewSlotDay(Number(e.target.value))}>
                    {["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"].map((d, i) => (
                      <option key={i} value={i}>{d}</option>
                    ))}
                  </select>
                </label>
                <label className="field">
                  <span>Début</span>
                  <input type="time" value={newSlotStart} onChange={(e) => setNewSlotStart(e.target.value)} />
                </label>
                <label className="field">
                  <span>Fin</span>
                  <input type="time" value={newSlotEnd} onChange={(e) => setNewSlotEnd(e.target.value)} />
                </label>
                <label className="field">
                  <span>Durée séance (min)</span>
                  <select value={newSlotDuration} onChange={(e) => setNewSlotDuration(Number(e.target.value))}>
                    <option value={45}>45 min</option>
                    <option value={60}>60 min</option>
                    <option value={90}>90 min</option>
                  </select>
                </label>
                <label className="field">
                  <span>Tampon (min)</span>
                  <select value={newSlotBuffer} onChange={(e) => setNewSlotBuffer(Number(e.target.value))}>
                    <option value={0}>0 min</option>
                    <option value={5}>5 min</option>
                    <option value={10}>10 min</option>
                    <option value={15}>15 min</option>
                    <option value={30}>30 min</option>
                  </select>
                </label>
                <label className="field">
                  <span>Type</span>
                  <select value={newSlotType} onChange={(e) => setNewSlotType(e.target.value as typeof newSlotType)}>
                    <option value="standard">Standard (60 min)</option>
                    <option value="intake">Évaluation (90 min)</option>
                    <option value="follow_up">Suivi court (45 min)</option>
                    <option value="any">Libre</option>
                  </select>
                </label>
              </div>
              <button
                className="button button-primary button-sm"
                type="button"
                disabled={isAddingSlot}
                onClick={async () => {
                  if (!session) return;
                  setIsAddingSlot(true);
                  setScheduleError(null);
                  setScheduleSuccess(null);
                  try {
                    const created = await createScheduleSlot(
                      {
                        day_of_week: newSlotDay,
                        start_time: newSlotStart,
                        end_time: newSlotEnd,
                        session_duration_minutes: newSlotDuration,
                        buffer_minutes: newSlotBuffer,
                        session_type: newSlotType,
                      },
                      session.access_token,
                    );
                    setScheduleSlots((prev) => [...prev, created]);
                    setScheduleSuccess("Bloc ajouté.");
                  } catch (e) {
                    setScheduleError(e instanceof Error ? e.message : "Erreur création bloc.");
                  } finally {
                    setIsAddingSlot(false);
                  }
                }}
              >
                {isAddingSlot ? "Ajout…" : "Ajouter"}
              </button>
            </div>

            {/* Exceptions */}
            <div className="card form-stack">
              <h3>Exceptions (congés, jours bloqués)</h3>
              {exceptions.length === 0 ? (
                <p className="muted-text">Aucune exception enregistrée.</p>
              ) : (
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Date</th>
                      <th>Type</th>
                      <th>Raison</th>
                      <th></th>
                    </tr>
                  </thead>
                  <tbody>
                    {exceptions.map((exc) => (
                      <tr key={exc.id}>
                        <td>{exc.exception_date}</td>
                        <td>{exc.exception_type === "blocked" ? "Bloqué" : "Extra"}</td>
                        <td>{exc.reason ?? "—"}</td>
                        <td>
                          <button
                            className="button button-danger button-xs"
                            type="button"
                            onClick={async () => {
                              if (!session) return;
                              try {
                                await deleteScheduleException(exc.id, session.access_token);
                                setExceptions((prev) => prev.filter((e) => e.id !== exc.id));
                              } catch (e) {
                                setScheduleError(e instanceof Error ? e.message : "Erreur.");
                              }
                            }}
                          >
                            Supprimer
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}

              <div className="form-grid-auto-wide">
                <label className="field">
                  <span>Date</span>
                  <input type="date" value={newExcDate} onChange={(e) => setNewExcDate(e.target.value)} />
                </label>
                <label className="field">
                  <span>Type</span>
                  <select value={newExcType} onChange={(e) => setNewExcType(e.target.value as "blocked" | "extra")}>
                    <option value="blocked">Journée bloquée</option>
                    <option value="extra">Créneau supplémentaire</option>
                  </select>
                </label>
                <label className="field">
                  <span>Raison (optionnel)</span>
                  <input type="text" value={newExcReason} onChange={(e) => setNewExcReason(e.target.value)} placeholder="Congé, formation…" />
                </label>
              </div>
              <button
                className="button button-secondary button-sm"
                type="button"
                disabled={isAddingException || !newExcDate}
                onClick={async () => {
                  if (!session || !newExcDate) return;
                  setIsAddingException(true);
                  setScheduleError(null);
                  try {
                    const created = await createScheduleException(
                      { exception_date: newExcDate, exception_type: newExcType, reason: newExcReason || null },
                      session.access_token,
                    );
                    setExceptions((prev) => [...prev, created]);
                    setNewExcDate("");
                    setNewExcReason("");
                    setScheduleSuccess("Exception ajoutée.");
                  } catch (e) {
                    setScheduleError(e instanceof Error ? e.message : "Erreur.");
                  } finally {
                    setIsAddingException(false);
                  }
                }}
              >
                {isAddingException ? "Ajout…" : "Bloquer cette date"}
              </button>
            </div>
          </div>
        )}

        {/* === ANCRES TEMPORELLES === */}
        {activeView === "ancres" && (
          <div className="stack-md">
            <div className="card form-stack">
              <h3>
                Ancres temporelles
                {selectedSession
                  ? ` — Séance S-${selectedSession.session_sequence_number}`
                  : ""}
              </h3>
              {!selectedSessionId ? (
                <p className="inline-note">
                  Sélectionnez une séance depuis l&apos;onglet Séances pour annoter des ancres temporelles.
                </p>
              ) : (
                <>
                  <p className="inline-note">
                    Notez un moment où le client a évoqué un événement passé. L&apos;écart temporel
                    (Z&nbsp;−&nbsp;Y) est calculé automatiquement par le serveur.
                  </p>
                  <form className="form-stack" onSubmit={(e) => { void handleCreateAnchor(e); }}>
                    <label className="field">
                      <span>Fragment verbatim</span>
                      <textarea
                        rows={3}
                        value={anchorVerbatim}
                        onChange={(e) => setAnchorVerbatim(e.target.value)}
                        placeholder={`"Quand j\u2019avais 12 ans, mon père est parti\u2026"`}
                      />
                    </label>
                    <div className="form-grid-2">
                      <label className="field">
                        <span>Année de l&apos;événement (Y)</span>
                        <input
                          type="number"
                          min={1900}
                          max={new Date().getFullYear()}
                          value={anchorYear}
                          onChange={(e) => setAnchorYear(e.target.value)}
                          placeholder="Ex. : 1998"
                        />
                      </label>
                      <label className="field">
                        <span>Âge du client à ce moment</span>
                        <input
                          type="number"
                          min={0}
                          max={120}
                          value={anchorAge}
                          onChange={(e) => setAnchorAge(e.target.value)}
                          placeholder="Ex. : 12"
                        />
                      </label>
                    </div>
                    <div className="form-grid-2">
                      <label className="field">
                        <span>Offset dans la séance (sec)</span>
                        <input
                          type="number"
                          min={0}
                          value={anchorOffsetSec}
                          onChange={(e) => setAnchorOffsetSec(e.target.value)}
                          placeholder="Ex. : 840 (= 14 min)"
                        />
                      </label>
                      <label className="field">
                        <span>Charge émotionnelle</span>
                        <select
                          value={anchorCharge}
                          onChange={(e) => setAnchorCharge(e.target.value as EmotionalChargeCode | "")}
                        >
                          <option value="">— non évaluée —</option>
                          <option value="faible">Faible</option>
                          <option value="moyen">Moyenne</option>
                          <option value="fort">Forte</option>
                          <option value="tres_fort">Très forte</option>
                        </select>
                      </label>
                    </div>
                    <label className="field field-inline">
                      <input
                        type="checkbox"
                        checked={anchorIsSilence}
                        onChange={(e) => setAnchorIsSilence(e.target.checked)}
                      />
                      <span>Marqueur de silence (silence cliniquement significatif)</span>
                    </label>
                    <label className="field">
                      <span>Note d&apos;interprétation (optionnel)</span>
                      <textarea
                        rows={2}
                        value={anchorInterpretation}
                        onChange={(e) => setAnchorInterpretation(e.target.value)}
                        placeholder="Lien avec d&apos;autres événements, hypothèse clinique…"
                      />
                    </label>
                    <div className="cta-row">
                      <button
                        className="button button-primary"
                        disabled={isSavingAnchor || (!anchorVerbatim.trim() && !anchorIsSilence)}
                        type="submit"
                      >
                        {isSavingAnchor ? "Enregistrement…" : "Ajouter l\u2019ancre"}
                      </button>
                    </div>
                  </form>
                </>
              )}
            </div>

            {selectedSessionId && (
              <div className="card">
                <h3>Ancres de la séance ({temporalAnchors.length})</h3>
                {isLoadingAnchors ? (
                  <p className="inline-note">Chargement…</p>
                ) : temporalAnchors.length === 0 ? (
                  <p className="inline-note">Aucune ancre enregistrée pour cette séance.</p>
                ) : (
                  <ul className="list-plain stack-sm">
                    {temporalAnchors.map((anchor) => (
                      <li key={anchor.id} className="card card--inset stack-sm">
                        <div className="info-strip">
                          {anchor.said_at_offset_sec != null ? (
                            <span className="mono">
                              {Math.floor(anchor.said_at_offset_sec / 60)}:
                              {String(anchor.said_at_offset_sec % 60).padStart(2, "0")}
                            </span>
                          ) : null}
                          {anchor.event_year_approx != null ? (
                            <span>
                              Événement : <strong>{anchor.event_year_approx}</strong>
                            </span>
                          ) : null}
                          {anchor.gap_years != null ? (
                            <span className="badge-gap">&Delta;&nbsp;{anchor.gap_years}&nbsp;ans</span>
                          ) : null}
                          {anchor.client_age_ref != null ? (
                            <span>Âge : {anchor.client_age_ref}&nbsp;ans</span>
                          ) : null}
                          {anchor.emotional_charge ? (
                            <span className={`badge-charge badge-charge--${anchor.emotional_charge}`}>
                              {anchor.emotional_charge.replace("_", "\u00a0")}
                            </span>
                          ) : null}
                          {anchor.is_silence_marker ? (
                            <span className="badge-silence">&#9679;&nbsp;Silence</span>
                          ) : null}
                        </div>
                        {anchor.verbatim_fragment ? (
                          <blockquote className="anchor-verbatim">
                            &ldquo;{anchor.verbatim_fragment}&rdquo;
                          </blockquote>
                        ) : null}
                        {anchor.interpretation_note ? (
                          <p className="inline-note anchor-interpretation">
                            {anchor.interpretation_note}
                          </p>
                        ) : null}
                        <button
                          className="button button-text button-xs"
                          disabled={archivingAnchorId === anchor.id}
                          onClick={() => { void handleArchiveAnchor(anchor.id); }}
                          type="button"
                        >
                          {archivingAnchorId === anchor.id ? "Suppression…" : "Retirer"}
                        </button>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

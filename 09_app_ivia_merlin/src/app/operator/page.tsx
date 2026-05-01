"use client";

import Link from "next/link";
import { FormEvent, useEffect, useState } from "react";

import { OperatorLiveKitPanel } from "@/components/operator-livekit-panel";
import {
  type AudioRecordingRecord,
  type AudioSessionRecord,
  closeSession,
  type ClientRecord,
  type ConsentRecord,
  createSession,
  type DerivedDocumentRecord,
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
  type IntakeRequestRecord,
  type LoginResponse,
  type SessionCloseResult,
  type SessionNoteRecord,
  type SessionRecord,
} from "@/lib/merlin-api";

const STORAGE_KEY = "merlin_operator_session";
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

export default function OperatorPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [session, setSession] = useState<LoginResponse | null>(null);
  const [clients, setClients] = useState<ClientRecord[]>([]);
  const [consents, setConsents] = useState<ConsentRecord[]>([]);
  const [derivedDocuments, setDerivedDocuments] = useState<DerivedDocumentRecord[]>([]);
  const [intakeRequests, setIntakeRequests] = useState<IntakeRequestRecord[]>([]);
  const [sessions, setSessions] = useState<SessionRecord[]>([]);
  const [sessionNotes, setSessionNotes] = useState<SessionNoteRecord[]>([]);
  const [audioSessions, setAudioSessions] = useState<AudioSessionRecord[]>([]);
  const [audioRecordings, setAudioRecordings] = useState<AudioRecordingRecord[]>([]);
  const [authErrorMessage, setAuthErrorMessage] = useState<string | null>(null);
  const [dashboardErrorMessage, setDashboardErrorMessage] = useState<string | null>(null);
  const [sessionSuccessMessage, setSessionSuccessMessage] = useState<string | null>(null);
  const [sessionClosureSuccessMessage, setSessionClosureSuccessMessage] = useState<string | null>(
    null,
  );
  const [audioSessionSuccessMessage, setAudioSessionSuccessMessage] = useState<string | null>(null);
  const [audioRecordingSuccessMessage, setAudioRecordingSuccessMessage] = useState<string | null>(
    null,
  );
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const [isLoadingDashboard, setIsLoadingDashboard] = useState(false);
  const [isCreatingSession, setIsCreatingSession] = useState(false);
  const [isCreatingListeningSlot, setIsCreatingListeningSlot] = useState(false);
  const [isProvisioningAudio, setIsProvisioningAudio] = useState(false);
  const [isStartingAudioRecording, setIsStartingAudioRecording] = useState(false);
  const [isStoppingAudioRecording, setIsStoppingAudioRecording] = useState(false);
  const [isStartingSession, setIsStartingSession] = useState(false);
  const [isClosingSession, setIsClosingSession] = useState(false);
  const [selectedClientId, setSelectedClientId] = useState("");
  const [selectedSessionId, setSelectedSessionId] = useState("");
  const [sessionModeCode, setSessionModeCode] = useState<"intake" | "standard" | "follow_up">(
    "intake",
  );
  const [sessionChannelCode, setSessionChannelCode] = useState<
    "direct" | "in_person" | "async"
  >("direct");
  const [scheduledStartAt, setScheduledStartAt] = useState("");
  const [durationMinutes, setDurationMinutes] = useState("60");
  const [plannedActualStartAt, setPlannedActualStartAt] = useState("");
  const [actualStartAt, setActualStartAt] = useState("");
  const [actualEndAt, setActualEndAt] = useState("");
  const [finalSessionStatus, setFinalSessionStatus] = useState<
    "completed" | "cancelled" | "no_show" | "escalated"
  >("completed");
  const [presentingTopicText, setPresentingTopicText] = useState("");
  const [sessionHighlightsText, setSessionHighlightsText] = useState("");
  const [operatorAssessmentText, setOperatorAssessmentText] = useState("");
  const [vigilanceLevelCode, setVigilanceLevelCode] = useState<
    "non_urgent" | "watch" | "priority" | "urgent"
  >("non_urgent");
  const [followUpActionsText, setFollowUpActionsText] = useState("");
  const [nextSessionFocusText, setNextSessionFocusText] = useState("");
  const [clientVisible, setClientVisible] = useState(false);
  const isOperatorSession = session?.user.role === "operator";

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
    if (!session) {
      return;
    }

    if (session.user.role !== "operator") {
      return;
    }

    const currentSession = session;
    let active = true;

    async function loadDashboard() {
      setIsLoadingDashboard(true);
      setDashboardErrorMessage(null);

      try {
        const [
          clientResult,
          consentResult,
          derivedDocumentResult,
          intakeRequestResult,
          sessionResult,
          sessionNoteResult,
          audioSessionResult,
          audioRecordingResult,
        ] =
          await Promise.all([
            listClients(currentSession.access_token),
            listConsents(currentSession.access_token),
            listDerivedDocuments(currentSession.access_token),
            listIntakeRequests(currentSession.access_token),
            listSessions(currentSession.access_token),
            listSessionNotes(currentSession.access_token),
            listAudioSessions(currentSession.access_token),
            listAudioRecordings(currentSession.access_token),
          ]);
        if (!active) {
          return;
        }
        setClients(clientResult);
        setConsents(consentResult);
        setDerivedDocuments(derivedDocumentResult);
        setIntakeRequests(intakeRequestResult);
        setSessions(sessionResult);
        setSessionNotes(sessionNoteResult);
        setAudioSessions(audioSessionResult);
        setAudioRecordings(audioRecordingResult);
        if (clientResult.length > 0) {
          setSelectedClientId((currentValue) => currentValue || clientResult[0].id);
        }
        if (sessionResult.length > 0) {
          setSelectedSessionId((currentValue) => currentValue || sessionResult[0].id);
        }
      } catch (error) {
        if (!active) {
          return;
        }
        setDashboardErrorMessage(
          error instanceof Error
            ? error.message
            : "Impossible de charger les donnees operateur.",
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
    setClients([]);
    setConsents([]);
    setDerivedDocuments([]);
    setIntakeRequests([]);
    setSessions([]);
    setSessionNotes([]);
    setAudioSessions([]);
    setAudioRecordings([]);
    setAuthErrorMessage(null);
    setDashboardErrorMessage(null);
    setSessionSuccessMessage(null);
    setSessionClosureSuccessMessage(null);
    setAudioSessionSuccessMessage(null);
    setAudioRecordingSuccessMessage(null);
  }

  async function handleCreateSession(event?: { preventDefault?: () => void }) {
    event?.preventDefault?.();
    if (!session || !selectedClientId) {
      return;
    }

    setIsCreatingSession(true);
    setDashboardErrorMessage(null);
    setSessionSuccessMessage(null);
    setSessionClosureSuccessMessage(null);
    setAudioSessionSuccessMessage(null);
    setAudioRecordingSuccessMessage(null);

    try {
      const createdSession = await createSession(
        {
          client_id: selectedClientId,
          session_mode_code: sessionModeCode,
          session_channel_code: sessionChannelCode,
          scheduled_start_at: scheduledStartAt
            ? new Date(scheduledStartAt).toISOString()
            : null,
          duration_minutes: durationMinutes ? Number(durationMinutes) : null,
          session_status_code: "scheduled",
        },
        session.access_token,
      );

      const nextSessions = await listSessions(session.access_token);
      setSessions(nextSessions);
      setSelectedSessionId(createdSession.id);
      setSessionSuccessMessage(
        `Seance ${createdSession.session_sequence_number} creee pour le client selectionne.`,
      );
      setPlannedActualStartAt("");
      setSessionModeCode("follow_up");
    } catch (error) {
      setDashboardErrorMessage(
        error instanceof Error ? error.message : "Impossible de creer la seance.",
      );
    } finally {
      setIsCreatingSession(false);
    }
  }

  async function handleProvisionAudioSession() {
    if (!session || !selectedSessionId) {
      return;
    }

    setIsProvisioningAudio(true);
    setDashboardErrorMessage(null);
    setAudioSessionSuccessMessage(null);
    setAudioRecordingSuccessMessage(null);

    try {
      const provisionedAudioSession = await provisionAudioSession(
        selectedSessionId,
        session.access_token,
      );
      const nextAudioSessions = await listAudioSessions(session.access_token);
      setAudioSessions(nextAudioSessions);
      setAudioRecordingSuccessMessage(null);
      setAudioSessionSuccessMessage(
        `Salle audio ${provisionedAudioSession.room_name} preparee.`,
      );
    } catch (error) {
      setDashboardErrorMessage(
        error instanceof Error ? error.message : "Impossible de preparer l'audio.",
      );
    } finally {
      setIsProvisioningAudio(false);
    }
  }

  async function handleCreateListeningSlot(event?: { preventDefault?: () => void }) {
    event?.preventDefault?.();
    if (!session || !selectedClientId) {
      return;
    }

    setIsCreatingListeningSlot(true);
    setDashboardErrorMessage(null);
    setSessionSuccessMessage(null);
    setSessionClosureSuccessMessage(null);
    setAudioSessionSuccessMessage(null);
    setAudioRecordingSuccessMessage(null);

    try {
      const createdSession = await createSession(
        {
          client_id: selectedClientId,
          session_mode_code: sessionModeCode,
          session_channel_code: sessionChannelCode,
          scheduled_start_at: scheduledStartAt
            ? new Date(scheduledStartAt).toISOString()
            : null,
          duration_minutes: durationMinutes ? Number(durationMinutes) : null,
          session_status_code: "scheduled",
        },
        session.access_token,
      );

      const provisionedAudioSession = await provisionAudioSession(
        createdSession.id,
        session.access_token,
      );

      const [nextSessions, nextAudioSessions] = await Promise.all([
        listSessions(session.access_token),
        listAudioSessions(session.access_token),
      ]);
      setSessions(nextSessions);
      setAudioSessions(nextAudioSessions);
      setSelectedSessionId(createdSession.id);
      setPlannedActualStartAt("");
      setSessionModeCode("follow_up");
      setSessionSuccessMessage(
        `Creneau ${createdSession.session_sequence_number} cree et salle ${provisionedAudioSession.room_name} preparee.`,
      );
      setAudioSessionSuccessMessage(
        "La salle audio est prete. Tu peux maintenant generer le lien client.",
      );
    } catch (error) {
      setDashboardErrorMessage(
        error instanceof Error
          ? error.message
          : "Impossible de creer le creneau d'ecoute.",
      );
    } finally {
      setIsCreatingListeningSlot(false);
    }
  }

  async function handleStartSession() {
    if (!session || !selectedSessionId) {
      return;
    }

    const targetSession = sessions.find((sessionRecord) => sessionRecord.id === selectedSessionId);
    if (!targetSession) {
      setDashboardErrorMessage("Seance selectionnee introuvable.");
      return;
    }

    setIsStartingSession(true);
    setDashboardErrorMessage(null);
    setSessionSuccessMessage(null);
    setSessionClosureSuccessMessage(null);

    try {
      const startedSession = await startSession(
        targetSession.id,
        {
          actual_start_at: plannedActualStartAt ? new Date(plannedActualStartAt).toISOString() : null,
        },
        session.access_token,
      );
      const nextSessions = await listSessions(session.access_token);
      setSessions(nextSessions);
      setSelectedSessionId(startedSession.id);
      const nextAudioSessions = await listAudioSessions(session.access_token);
      setAudioSessions(nextAudioSessions);
      setActualStartAt(
        startedSession.actual_start_at
          ? new Date(startedSession.actual_start_at).toISOString().slice(0, 16)
          : "",
      );
      setSessionSuccessMessage(
        `Seance ${startedSession.session_sequence_number} demarree.`,
      );
    } catch (error) {
      setDashboardErrorMessage(
        error instanceof Error ? error.message : "Impossible de demarrer la seance.",
      );
    } finally {
      setIsStartingSession(false);
    }
  }

  async function handleStartAudioRecording() {
    if (!session || !selectedAudioSession) {
      return;
    }

    setIsStartingAudioRecording(true);
    setDashboardErrorMessage(null);
    setAudioRecordingSuccessMessage(null);

    try {
      const recording = await startAudioRecording(
        selectedAudioSession.id,
        session.access_token,
      );
      const nextAudioRecordings = await listAudioRecordings(session.access_token);
      setAudioRecordings(nextAudioRecordings);
      setAudioRecordingSuccessMessage(
        recording.audio_recording_status_code === "failed"
          ? "Tentative d'enregistrement lancee mais le provider a retourne un echec."
          : "Cycle d'enregistrement demarre pour cette salle audio.",
      );
    } catch (error) {
      setDashboardErrorMessage(
        error instanceof Error ? error.message : "Impossible de demarrer l'enregistrement.",
      );
    } finally {
      setIsStartingAudioRecording(false);
    }
  }

  async function handleStopAudioRecording() {
    if (!session || !selectedAudioRecording) {
      return;
    }

    setIsStoppingAudioRecording(true);
    setDashboardErrorMessage(null);
    setAudioRecordingSuccessMessage(null);

    try {
      await stopAudioRecording(selectedAudioRecording.id, session.access_token);
      const nextAudioRecordings = await listAudioRecordings(session.access_token);
      setAudioRecordings(nextAudioRecordings);
      setAudioRecordingSuccessMessage("Enregistrement arrete et marque comme pret.");
    } catch (error) {
      setDashboardErrorMessage(
        error instanceof Error ? error.message : "Impossible d'arreter l'enregistrement.",
      );
    } finally {
      setIsStoppingAudioRecording(false);
    }
  }

  async function handleCloseSession(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!session || !selectedSessionId) {
      return;
    }

    const targetSession = sessions.find((sessionRecord) => sessionRecord.id === selectedSessionId);
    if (!targetSession) {
      setDashboardErrorMessage("Seance selectionnee introuvable.");
      return;
    }

    setIsClosingSession(true);
    setDashboardErrorMessage(null);
    setSessionClosureSuccessMessage(null);

    try {
      const closeResult: SessionCloseResult = await closeSession(
        targetSession.id,
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

      const [nextSessions, nextNotes] = await Promise.all([
        listSessions(session.access_token),
        listSessionNotes(session.access_token),
      ]);
      setSessions(nextSessions);
      setSessionNotes(nextNotes);
      const [nextAudioSessions, nextAudioRecordings, nextDerivedDocuments] = await Promise.all([
        listAudioSessions(session.access_token),
        listAudioRecordings(session.access_token),
        listDerivedDocuments(session.access_token),
      ]);
      setAudioSessions(nextAudioSessions);
      setAudioRecordings(nextAudioRecordings);
      setDerivedDocuments(nextDerivedDocuments);
      setSessionClosureSuccessMessage(
        closeResult.generated_note.client_visible
          ? `Seance ${closeResult.session.session_sequence_number} cloturee. Note ${closeResult.generated_note.note_sequence_number} et document derives generes. La diffusion client reste en attente de validation supervision.`
          : `Seance ${closeResult.session.session_sequence_number} cloturee. Note ${closeResult.generated_note.note_sequence_number} et document derives generes pour usage interne.`,
      );
      setActualStartAt("");
      setActualEndAt("");
      setPresentingTopicText("");
      setSessionHighlightsText("");
      setOperatorAssessmentText("");
      setFollowUpActionsText("");
      setNextSessionFocusText("");
      setClientVisible(false);
    } catch (error) {
      setDashboardErrorMessage(
        error instanceof Error ? error.message : "Impossible de cloturer la seance.",
      );
    } finally {
      setIsClosingSession(false);
    }
  }

  const selectedClient =
    clients.find((client) => client.id === selectedClientId) ?? null;
  const selectedClientConsents = selectedClientId
    ? consents.filter((consent) => consent.client_id === selectedClientId)
    : [];
  const latestSelectedClientConsentByType = new Map(
    selectedClientConsents.map((consent) => [consent.consent_type_code, consent]),
  );
  const selectedClientIntakeConsentSummary = INTAKE_CONSENT_TYPES.map((consentType) => {
    const consent = latestSelectedClientConsentByType.get(consentType) ?? null;
    const labelByType = {
      consent_session: "Seance",
      consent_session_note: "Note",
      consent_history: "Historique",
    } as const;

    return {
      consentType,
      label: labelByType[consentType],
      status: consent ? (consent.consent_value ? "Accorde" : "Refuse") : "Manquant",
      grantedAt: consent?.granted_at ?? null,
    };
  });
  const selectedClientIntakeRequests = selectedClientId
    ? intakeRequests.filter((intakeRequest) => intakeRequest.client_id === selectedClientId)
    : [];
  const selectedClientLatestIntakeRequest = selectedClientIntakeRequests[0] ?? null;
  const selectedSession =
    sessions.find((sessionRecord) => sessionRecord.id === selectedSessionId) ?? null;
  const selectedAudioSession =
    audioSessions.find((audioSession) => audioSession.session_id === selectedSessionId) ?? null;
  const selectedAudioSessionRecordings = selectedAudioSession
    ? audioRecordings.filter((audioRecording) => audioRecording.audio_session_id === selectedAudioSession.id)
    : [];
  const selectedAudioRecording = selectedAudioSessionRecordings[0] ?? null;
  const sessionOptions = sessions.map((sessionRecord) => {
    const client = clients.find((item) => item.id === sessionRecord.client_id);
    const clientLabel = client?.public_client_code ?? sessionRecord.client_id.slice(0, 8);
    return {
      id: sessionRecord.id,
      label: `S-${sessionRecord.session_sequence_number} / ${clientLabel} / ${sessionRecord.session_mode_code}`,
    };
  });
  const visibleNotes = selectedSessionId
    ? sessionNotes.filter((note) => note.session_id === selectedSessionId)
    : sessionNotes;
  const selectedSessionGeneratedNote = visibleNotes[0] ?? null;
  const visibleDerivedDocuments = selectedSessionId
    ? derivedDocuments.filter((document) => document.session_id === selectedSessionId)
    : derivedDocuments;
  const selectedSessionDerivedDocument = visibleDerivedDocuments[0] ?? null;

  return (
    <div className="page-shell">
      <header className="topbar">
        <div className="wordmark">MERLIN / Operateur</div>
        <nav className="nav">
          <Link href="/">Accueil</Link>
          <Link href="/rendez-vous">Entree client</Link>
          <Link href="/supervision">Supervision</Link>
        </nav>
      </header>

      <main className="section">
        <div className="section-header">
          <div className="eyebrow">SCR-101 a SCR-109</div>
          <h2>Backoffice operateur</h2>
          <p>
            Cette surface est centree sur la production operateur: entrees client,
            planification, conduite de seance, cloture et lecture des sorties.
          </p>
        </div>

        {!session ? (
          <form className="card form-stack operator-auth-card" onSubmit={handleLogin}>
            <h3>Connexion operateur</h3>
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
        ) : !isOperatorSession ? (
          <div className="grid operator-layout">
            <article className="card">
              <h3>Session ouverte hors perimetre operateur</h3>
              <p>
                Connecte comme <span className="mono">{session.user.email}</span>
              </p>
              <p>Role: {session.user.role}</p>
              <p className="inline-note">
                Cet ecran est reserve a la production operateur. Les droits du role actif ne
                doivent pas charger le tableau de production.
              </p>
              <div className="cta-row">
                {session.user.role === "supervisor" ? (
                  <Link className="button button-secondary" href="/supervision">
                    Aller a la supervision
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
          </div>
        ) : (
          <div className="grid operator-layout">
            <article className="card">
              <h3>Session operateur</h3>
              <p>
                Connecte comme <span className="mono">{session.user.email}</span>
              </p>
              <p>Role: {session.user.role}</p>
              <p className="inline-note">Identifiant operateur: <span className="mono">{session.user.id}</span></p>
              <div className="cta-row">
                <button className="button button-secondary" onClick={handleLogout} type="button">
                  Se deconnecter
                </button>
              </div>
            </article>

            <article className="card">
              <div className="stack-lg">
                <div>
                  <h3>Creer un creneau d'ecoute</h3>
                  <p>
                    Le praticien doit pouvoir creer une seance, preparer la salle et envoyer le
                    lien client sans naviguer entre plusieurs etapes techniques.
                  </p>
                </div>

                {isLoadingDashboard ? <p>Chargement du tableau operateur...</p> : null}
                {dashboardErrorMessage ? (
                  <p className="message message-error">{dashboardErrorMessage}</p>
                ) : null}
                {sessionSuccessMessage ? (
                  <p className="message message-success">{sessionSuccessMessage}</p>
                ) : null}

                {clients.length === 0 ? (
                  <p>Aucun client encore enregistre.</p>
                ) : (
                  <form className="form-stack" onSubmit={handleCreateListeningSlot}>
                    <label className="field">
                      <span>Client</span>
                      <select
                        value={selectedClientId}
                        onChange={(event) => setSelectedClientId(event.target.value)}
                      >
                        {clients.map((client) => (
                          <option key={client.id} value={client.id}>
                            {client.public_client_code} - {client.first_name_or_alias}
                          </option>
                        ))}
                      </select>
                    </label>

                    {selectedClient ? (
                      <div className="stack-sm">
                        <div className="info-strip">
                          <span className="mono">{selectedClient.public_client_code}</span>
                          <span>{selectedClient.email ?? "Sans courriel"}</span>
                          <span>{selectedClient.phone ?? "Sans telephone"}</span>
                        </div>
                        <div className="card">
                          <h4>Consentements d&apos;entree</h4>
                          <div className="info-strip">
                            {selectedClientIntakeConsentSummary.map((item) => (
                              <span key={item.consentType}>
                                {item.label}: {item.status}
                              </span>
                            ))}
                          </div>
                          <p className="inline-note">
                            Enregistrement, transcription et transmission tiers restent hors du
                            consentement public initial.
                          </p>
                        </div>
                        <div className="card">
                          <h4>Demande d&apos;entree</h4>
                          {selectedClientLatestIntakeRequest ? (
                            <div className="stack-sm">
                              <div className="info-strip">
                                <span>Besoin: {selectedClientLatestIntakeRequest.primary_need_code}</span>
                                <span>Urgence: {selectedClientLatestIntakeRequest.perceived_urgency_code}</span>
                                <span>
                                  Soutien en place:{" "}
                                  {selectedClientLatestIntakeRequest.support_already_in_place
                                    ? "oui"
                                    : "non"}
                                </span>
                              </div>
                              <p>
                                {selectedClientLatestIntakeRequest.requested_outcome_text ??
                                  "Aucun texte libre transmis dans la demande d'entree."}
                              </p>
                            </div>
                          ) : (
                            <p className="inline-note">
                              Aucune demande d&apos;entree trouvee pour ce client.
                            </p>
                          )}
                        </div>
                      </div>
                    ) : null}

                    <div className="form-grid-2">
                      <label className="field">
                        <span>Mode</span>
                        <select
                          value={sessionModeCode}
                          onChange={(event) =>
                            setSessionModeCode(
                              event.target.value as "intake" | "standard" | "follow_up",
                            )
                          }
                        >
                          <option value="intake">Premier RDV</option>
                          <option value="standard">Suivi</option>
                          <option value="follow_up">Reprise</option>
                        </select>
                      </label>

                      <label className="field">
                        <span>Canal</span>
                        <select
                          value={sessionChannelCode}
                          onChange={(event) =>
                            setSessionChannelCode(
                              event.target.value as "direct" | "in_person" | "async",
                            )
                          }
                        >
                          <option value="direct">Direct</option>
                          <option value="in_person">Presentiel</option>
                          <option value="async">Asynchrone</option>
                        </select>
                      </label>
                    </div>

                    <div className="form-grid-2">
                      <label className="field">
                        <span>Debut planifie</span>
                        <input
                          type="datetime-local"
                          value={scheduledStartAt}
                          onChange={(event) => setScheduledStartAt(event.target.value)}
                        />
                      </label>

                      <label className="field">
                        <span>Duree estimee (minutes)</span>
                        <input
                          type="number"
                          min="15"
                          step="5"
                          value={durationMinutes}
                          onChange={(event) => setDurationMinutes(event.target.value)}
                        />
                      </label>
                    </div>

                    <div className="cta-row">
                      <button
                        className="button button-primary"
                        disabled={isCreatingListeningSlot || !selectedClientId}
                        type="submit"
                      >
                        {isCreatingListeningSlot
                          ? "Creation..."
                          : "Creer et preparer la salle"}
                      </button>
                      <button
                        className="button button-secondary"
                        disabled={isCreatingSession || !selectedClientId}
                        onClick={handleCreateSession}
                        type="button"
                      >
                        {isCreatingSession ? "Creation..." : "Creer la seance"}
                      </button>
                    </div>
                    <p className="inline-note">
                      Action principale: cree la seance puis prepare immediatement la salle audio.
                    </p>
                  </form>
                )}

                <div className="stack-md">
                  <h3>Clients entres dans MERLIN</h3>
                  {clients.length > 0 ? (
                    <div className="table-wrap">
                      <table className="data-table">
                        <thead>
                          <tr>
                            <th>Code</th>
                            <th>Nom</th>
                            <th>Courriel</th>
                            <th>Telephone</th>
                            <th>Consentements</th>
                            <th>Demande</th>
                          </tr>
                        </thead>
                        <tbody>
                          {clients.map((client) => (
                            <tr key={client.id}>
                              <td className="mono">{client.public_client_code}</td>
                              <td>{client.first_name_or_alias}</td>
                              <td>{client.email ?? "-"}</td>
                              <td>{client.phone ?? "-"}</td>
                              <td>
                                {INTAKE_CONSENT_TYPES.map((consentType) => {
                                  const consent = consents.find(
                                    (item) =>
                                      item.client_id === client.id &&
                                      item.consent_type_code === consentType,
                                  );
                                  const shortLabelByType = {
                                    consent_session: "S",
                                    consent_session_note: "N",
                                    consent_history: "H",
                                  } as const;
                                  const status = consent
                                    ? consent.consent_value
                                      ? "oui"
                                      : "non"
                                    : "-";
                                  return `${shortLabelByType[consentType]}:${status}`;
                                }).join("  ")}
                              </td>
                              <td>
                                {(() => {
                                  const intakeRequest = intakeRequests.find(
                                    (item) => item.client_id === client.id,
                                  );
                                  if (!intakeRequest) {
                                    return "-";
                                  }
                                  return `${intakeRequest.primary_need_code} / ${intakeRequest.perceived_urgency_code}`;
                                })()}
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  ) : null}
                </div>

                <div className="stack-md">
                  <h3>Salle audio et enregistrement</h3>
                  {sessions.length === 0 ? (
                    <p>Aucune seance disponible pour preparer l&apos;audio.</p>
                  ) : (
                    <div className="form-stack">
                      <label className="field">
                        <span>Seance</span>
                        <select
                          value={selectedSessionId}
                          onChange={(event) => setSelectedSessionId(event.target.value)}
                        >
                          {sessionOptions.map((option) => (
                            <option key={option.id} value={option.id}>
                              {option.label}
                            </option>
                          ))}
                        </select>
                      </label>

                      {selectedAudioSession ? (
                        <div className="info-strip">
                          <span className="mono">{selectedAudioSession.room_name}</span>
                          <span>{selectedAudioSession.audio_session_status_code}</span>
                          <span>{selectedAudioSession.provider_code}</span>
                          <span>
                            {selectedAudioSession.recording_enabled
                              ? "Enregistrement actif"
                              : "Sans enregistrement"}
                          </span>
                        </div>
                      ) : (
                        <p className="inline-note">
                          Aucune salle audio encore preparee pour cette seance.
                        </p>
                      )}

                      {selectedAudioSession?.provider_room_url ? (
                        <p className="inline-note">
                          Point de media configure:{" "}
                          <span className="mono">{selectedAudioSession.provider_room_url}</span>
                        </p>
                      ) : (
                        <p className="inline-note">
                          Aucune URL media configuree pour le moment. La salle est preparee cote
                          MERLIN mais le provider temps reel n&apos;est pas encore branche.
                        </p>
                      )}

                      <OperatorLiveKitPanel
                        key={selectedAudioSession?.id ?? "no-audio-session"}
                        audioSession={selectedAudioSession}
                        operatorAccessToken={session.access_token}
                      />

                      {audioSessionSuccessMessage ? (
                        <p className="message message-success">{audioSessionSuccessMessage}</p>
                      ) : null}

                      <div className="stack-md">
                        <h4>Enregistrement</h4>
                        {selectedAudioRecording ? (
                          <div className="info-strip">
                            <span>{selectedAudioRecording.audio_recording_status_code}</span>
                            <span className="mono">{selectedAudioRecording.id.slice(0, 8)}</span>
                            <span>
                              {selectedAudioRecording.output_location ?? "Sans emplacement de sortie"}
                            </span>
                          </div>
                        ) : (
                          <p className="inline-note">
                            Aucun cycle d&apos;enregistrement encore trace pour cette salle.
                          </p>
                        )}

                        {selectedAudioRecording?.failure_reason ? (
                          <p className="message message-error">
                            {selectedAudioRecording.failure_reason}
                          </p>
                        ) : null}

                        {audioRecordingSuccessMessage ? (
                          <p className="message message-success">{audioRecordingSuccessMessage}</p>
                        ) : null}

                        <div className="cta-row">
                          <button
                            className="button button-secondary"
                            disabled={
                              isStartingAudioRecording ||
                              !selectedAudioSession ||
                              selectedAudioRecording?.audio_recording_status_code === "recording"
                            }
                            onClick={handleStartAudioRecording}
                            type="button"
                          >
                            {isStartingAudioRecording
                              ? "Demarrage..."
                              : "Demarrer l'enregistrement"}
                          </button>
                          <button
                            className="button button-secondary"
                            disabled={
                              isStoppingAudioRecording ||
                              !selectedAudioRecording ||
                              selectedAudioRecording.audio_recording_status_code !== "recording"
                            }
                            onClick={handleStopAudioRecording}
                            type="button"
                          >
                            {isStoppingAudioRecording
                              ? "Arret..."
                              : "Arreter l'enregistrement"}
                          </button>
                        </div>
                      </div>

                      <div className="cta-row">
                        <button
                          className="button button-primary"
                          disabled={
                            isProvisioningAudio ||
                            !selectedSessionId ||
                            selectedSession?.session_status_code === "completed" ||
                            selectedSession?.session_status_code === "cancelled" ||
                            selectedSession?.session_status_code === "no_show" ||
                            selectedSession?.session_status_code === "escalated"
                          }
                          onClick={handleProvisionAudioSession}
                          type="button"
                        >
                          {isProvisioningAudio ? "Preparation..." : "Preparer la salle"}
                        </button>
                      </div>
                    </div>
                  )}
                </div>

                <div className="stack-md">
                  <h3>Demarrage de seance</h3>
                  {sessions.length === 0 ? (
                    <p>Aucune seance disponible pour le demarrage.</p>
                  ) : (
                    <div className="form-stack">
                      <label className="field">
                        <span>Seance</span>
                        <select
                          value={selectedSessionId}
                          onChange={(event) => setSelectedSessionId(event.target.value)}
                        >
                          {sessionOptions.map((option) => (
                            <option key={option.id} value={option.id}>
                              {option.label}
                            </option>
                          ))}
                        </select>
                      </label>

                      {selectedSession ? (
                        <div className="info-strip">
                          <span className="mono">{selectedSession.id.slice(0, 8)}</span>
                          <span>{selectedSession.session_status_code}</span>
                          <span>{selectedSession.session_channel_code}</span>
                          <span>{selectedSession.scheduled_start_at ?? "Sans horaire"}</span>
                        </div>
                      ) : null}

                      <label className="field">
                        <span>Debut reel a enregistrer</span>
                        <input
                          type="datetime-local"
                          value={plannedActualStartAt}
                          onChange={(event) => setPlannedActualStartAt(event.target.value)}
                        />
                      </label>

                      <div className="cta-row">
                        <button
                          className="button button-primary"
                          disabled={
                            isStartingSession ||
                            !selectedSessionId ||
                            selectedSession?.session_status_code !== "scheduled"
                          }
                          onClick={handleStartSession}
                          type="button"
                        >
                          {isStartingSession ? "Demarrage..." : "Demarrer la seance"}
                        </button>
                      </div>
                    </div>
                  )}
                </div>

                <div className="stack-md">
                  <h3>Cloture de seance</h3>
                  {sessions.length === 0 ? (
                    <p>Aucune seance disponible pour la cloture.</p>
                  ) : (
                    <form className="form-stack" onSubmit={handleCloseSession}>
                      <label className="field">
                        <span>Seance</span>
                        <select
                          value={selectedSessionId}
                          onChange={(event) => setSelectedSessionId(event.target.value)}
                        >
                          {sessionOptions.map((option) => (
                            <option key={option.id} value={option.id}>
                              {option.label}
                            </option>
                          ))}
                        </select>
                      </label>

                      {selectedSession ? (
                        <div className="info-strip">
                          <span className="mono">{selectedSession.id.slice(0, 8)}</span>
                          <span>{selectedSession.session_status_code}</span>
                          <span>{selectedSession.session_channel_code}</span>
                          <span>{selectedSession.duration_minutes ?? "-"} min</span>
                        </div>
                      ) : null}

                      <div className="form-grid-2">
                        <label className="field">
                          <span>Debut reel</span>
                          <input
                            type="datetime-local"
                            value={actualStartAt}
                            onChange={(event) => setActualStartAt(event.target.value)}
                          />
                        </label>

                        <label className="field">
                          <span>Fin reelle</span>
                          <input
                            type="datetime-local"
                            value={actualEndAt}
                            onChange={(event) => setActualEndAt(event.target.value)}
                          />
                        </label>
                      </div>

                      <div className="form-grid-2">
                        <label className="field">
                          <span>Statut final</span>
                          <select
                            value={finalSessionStatus}
                            onChange={(event) =>
                              setFinalSessionStatus(
                                event.target.value as
                                  | "completed"
                                  | "cancelled"
                                  | "no_show"
                                  | "escalated",
                              )
                            }
                          >
                            <option value="completed">Completee</option>
                            <option value="cancelled">Annulee</option>
                            <option value="no_show">Absence</option>
                            <option value="escalated">Escaladee</option>
                          </select>
                        </label>

                        <label className="field">
                          <span>Niveau de vigilance</span>
                          <select
                            value={vigilanceLevelCode}
                            onChange={(event) =>
                              setVigilanceLevelCode(
                                event.target.value as
                                  | "non_urgent"
                                  | "watch"
                                  | "priority"
                                  | "urgent",
                              )
                            }
                          >
                            <option value="non_urgent">Non urgent</option>
                            <option value="watch">Surveillance</option>
                            <option value="priority">Prioritaire</option>
                            <option value="urgent">Urgent</option>
                          </select>
                        </label>
                      </div>

                      <label className="field">
                        <span>Sujet principal traite</span>
                        <textarea
                          rows={2}
                          value={presentingTopicText}
                          onChange={(event) => setPresentingTopicText(event.target.value)}
                          required
                        />
                      </label>

                      <label className="field">
                        <span>Points saillants de la seance</span>
                        <textarea
                          rows={3}
                          value={sessionHighlightsText}
                          onChange={(event) => setSessionHighlightsText(event.target.value)}
                          required
                        />
                      </label>

                      <label className="field">
                        <span>Evaluation operateur</span>
                        <textarea
                          rows={3}
                          value={operatorAssessmentText}
                          onChange={(event) => setOperatorAssessmentText(event.target.value)}
                        />
                      </label>

                      <label className="field">
                        <span>Suites proposees</span>
                        <textarea
                          rows={3}
                          value={followUpActionsText}
                          onChange={(event) => setFollowUpActionsText(event.target.value)}
                        />
                      </label>

                      <label className="field">
                        <span>Focus prochaine seance</span>
                        <textarea
                          rows={2}
                          value={nextSessionFocusText}
                          onChange={(event) => setNextSessionFocusText(event.target.value)}
                        />
                      </label>

                      <label className="checkbox-row">
                        <input
                          checked={clientVisible}
                          onChange={(event) => setClientVisible(event.target.checked)}
                          type="checkbox"
                        />
                        <span>Proposer une diffusion client apres validation supervision</span>
                      </label>

                      {sessionClosureSuccessMessage ? (
                        <p className="message message-success">{sessionClosureSuccessMessage}</p>
                      ) : null}

                      <div className="cta-row">
                        <button
                          className="button button-primary"
                          disabled={
                            isClosingSession ||
                            !selectedSessionId ||
                            !presentingTopicText.trim() ||
                            !sessionHighlightsText.trim()
                          }
                          type="submit"
                        >
                          {isClosingSession ? "Cloture..." : "Cloturer et generer la note"}
                        </button>
                      </div>
                    </form>
                  )}
                </div>

                <div className="stack-md">
                  <h3>Seances creees</h3>
                  {sessions.length === 0 ? <p>Aucune seance encore planifiee.</p> : null}
                  {sessions.length > 0 ? (
                    <div className="table-wrap">
                      <table className="data-table">
                        <thead>
                          <tr>
                            <th>Seq.</th>
                            <th>Client</th>
                            <th>Mode</th>
                            <th>Canal</th>
                            <th>Statut</th>
                            <th>Duree</th>
                          </tr>
                        </thead>
                        <tbody>
                          {sessions.map((sessionRecord) => (
                            <tr key={sessionRecord.id}>
                              <td className="mono">S-{sessionRecord.session_sequence_number}</td>
                              <td className="mono">{sessionRecord.client_id.slice(0, 8)}</td>
                              <td>{SESSION_MODE_LABELS[sessionRecord.session_mode_code] ?? sessionRecord.session_mode_code}</td>
                              <td>{sessionRecord.session_channel_code}</td>
                              <td>{SESSION_STATUS_LABELS[sessionRecord.session_status_code] ?? sessionRecord.session_status_code}</td>
                              <td>{sessionRecord.duration_minutes ?? "-"}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  ) : null}
                </div>

                <div className="stack-md">
                  <h3>Document derive</h3>
                  {selectedSessionDerivedDocument ? (
                      <div className="card form-stack">
                        <div className="info-strip">
                          <span>{selectedSessionDerivedDocument.title}</span>
                          <span>{selectedSessionDerivedDocument.document_kind_code}</span>
                          <span>{selectedSessionDerivedDocument.audience_code}</span>
                          <span>
                          {selectedSessionDerivedDocument.client_visible
                            ? "Diffuse client"
                            : selectedSessionDerivedDocument.audience_code === "client_pending_review"
                              ? "En attente supervision"
                              : "Interne"}
                          </span>
                        </div>
                      <label className="field">
                        <span>Contenu</span>
                        <textarea
                          readOnly
                          rows={6}
                          value={selectedSessionDerivedDocument.body_text}
                        />
                      </label>
                      {visibleDerivedDocuments.length > 1 ? (
                        <div className="table-wrap">
                          <table className="data-table">
                            <thead>
                              <tr>
                                <th>Titre</th>
                                <th>Audience</th>
                                <th>Visible client</th>
                              </tr>
                            </thead>
                            <tbody>
                              {visibleDerivedDocuments.map((document) => (
                                <tr key={document.id}>
                                  <td>{document.title}</td>
                                  <td>{document.audience_code}</td>
                                  <td>
                                    {document.client_visible
                                      ? "Diffuse"
                                      : document.audience_code === "client_pending_review"
                                        ? "En attente"
                                        : "Non"}
                                  </td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      ) : null}
                    </div>
                  ) : (
                    <p>Aucun document derive pour la selection courante.</p>
                  )}
                </div>

                <div className="stack-md">
                  <h3>Notes de seance</h3>
                  {visibleNotes.length === 0 ? <p>Aucune note pour la selection courante.</p> : null}
                  {selectedSessionGeneratedNote ? (
                    <div className="card form-stack">
                      <div className="info-strip">
                        <span className="mono">N-{selectedSessionGeneratedNote.note_sequence_number}</span>
                        <span>{selectedSessionGeneratedNote.validated_by_practitioner ? "Validee" : "Non validee"}</span>
                        <span>
                          {selectedSessionGeneratedNote.validated_at
                            ? new Date(selectedSessionGeneratedNote.validated_at).toLocaleString("fr-CA")
                            : "Aucune validation"}
                        </span>
                      </div>

                      <div className="form-grid-2">
                        <div className="card">
                          <h4>Client delivery</h4>
                            <p>
                              {selectedSessionGeneratedNote.client_facing_summary_text ??
                              "Aucune synthese proposee pour le client."}
                            </p>
                          </div>
                        <div className="card">
                          <h4>Supervision</h4>
                          <p>
                            {selectedSessionGeneratedNote.supervision_summary_text ??
                              "Aucune synthese supervision pour cette note."}
                          </p>
                        </div>
                      </div>

                      <div className="form-grid-2">
                        <label className="field">
                          <span>Coeur</span>
                          <textarea readOnly rows={2} value={selectedSessionGeneratedNote.coeur_summary_text ?? ""} />
                        </label>
                        <label className="field">
                          <span>Corps</span>
                          <textarea readOnly rows={2} value={selectedSessionGeneratedNote.corps_summary_text ?? ""} />
                        </label>
                        <label className="field">
                          <span>Esprit</span>
                          <textarea readOnly rows={2} value={selectedSessionGeneratedNote.esprit_summary_text ?? ""} />
                        </label>
                        <label className="field">
                          <span>Etre</span>
                          <textarea readOnly rows={2} value={selectedSessionGeneratedNote.etre_summary_text ?? ""} />
                        </label>
                      </div>

                      <label className="field">
                        <span>Hypotheses contextuelles</span>
                        <textarea
                          readOnly
                          rows={4}
                          value={
                            selectedSessionGeneratedNote.context_hypotheses_json
                              ? JSON.stringify(selectedSessionGeneratedNote.context_hypotheses_json, null, 2)
                              : ""
                          }
                        />
                      </label>

                      {selectedSessionGeneratedNote.practitioner_corrections ? (
                        <label className="field">
                          <span>Corrections praticien enregistrees</span>
                          <textarea
                            readOnly
                            rows={4}
                            value={JSON.stringify(selectedSessionGeneratedNote.practitioner_corrections, null, 2)}
                          />
                        </label>
                      ) : null}

                      <div className="message message-success">
                        La validation et la correction de note sont maintenant reservees a la
                        supervision. Une proposition de diffusion client reste en attente tant que
                        la supervision n&apos;a pas valide la note. Utiliser{" "}
                        <Link href="/supervision">/supervision</Link> pour relire, valider ou
                        rejeter une sortie.
                      </div>

                      {visibleNotes.length > 1 ? (
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
                              {visibleNotes.map((note) => (
                                <tr key={note.id}>
                                  <td className="mono">N-{note.note_sequence_number}</td>
                                  <td className="mono">{note.session_id.slice(0, 8)}</td>
                                  <td>{note.summary_text}</td>
                                  <td>{note.validated_by_practitioner ? "Validee" : "Non"}</td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      ) : null}
                    </div>
                  ) : null}
                </div>
              </div>
            </article>
          </div>
        )}
      </main>
    </div>
  );
}

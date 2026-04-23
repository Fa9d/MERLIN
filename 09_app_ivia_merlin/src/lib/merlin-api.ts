export const MERLIN_API_BASE_URL =
  process.env.NEXT_PUBLIC_MERLIN_API_BASE_URL?.replace(/\/$/, "") ??
  "http://127.0.0.1:8000";

type RequestOptions = {
  method?: "GET" | "POST" | "PATCH";
  body?: unknown;
  token?: string;
};

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const response = await fetch(`${MERLIN_API_BASE_URL}${path}`, {
    method: options.method ?? "GET",
    headers: {
      "Content-Type": "application/json",
      ...(options.token ? { Authorization: `Bearer ${options.token}` } : {}),
    },
    body: options.body ? JSON.stringify(options.body) : undefined,
  });

  if (!response.ok) {
    let detail = `Erreur API (${response.status})`;

    try {
      const payload = (await response.json()) as { detail?: string };
      if (payload.detail) {
        detail = payload.detail;
      }
    } catch {}

    throw new Error(detail);
  }

  return (await response.json()) as T;
}

export type ClientPayload = {
  first_name_or_alias: string;
  last_name?: string | null;
  email?: string | null;
  phone?: string | null;
  language_code?: string;
  timezone?: string;
  territory_code?: string;
  is_adult_confirmed?: boolean;
};

export type ClientRecord = {
  id: string;
  public_client_code: string;
  first_name_or_alias: string;
  last_name: string | null;
  email: string | null;
  phone: string | null;
  language_code: string;
  timezone: string;
  territory_code: string;
  is_adult_confirmed: boolean;
  created_at: string;
  updated_at: string;
};

export type IntakeRequestPayload = {
  client_id: string;
  request_channel_code: string;
  request_for_code: "self" | "relative" | "other";
  primary_need_code:
    | "clarification"
    | "support"
    | "orientation"
    | "loneliness"
    | "distress"
    | "other";
  perceived_urgency_code: "non_urgent" | "watch" | "priority" | "urgent";
  support_already_in_place: boolean;
  requested_outcome_text?: string | null;
  entry_summary_text?: string | null;
};

export type IntakeRequestRecord = {
  id: string;
  client_id: string;
  request_channel_code: string;
  request_for_code: string;
  primary_need_code: string;
  perceived_urgency_code: string;
  support_already_in_place: boolean;
  requested_outcome_text: string | null;
  entry_summary_text: string | null;
  created_at: string;
  updated_at: string;
};

export type ConsentTypeCode =
  | "consent_session"
  | "consent_session_note"
  | "consent_history"
  | "consent_recording"
  | "consent_transcription"
  | "consent_client_delivery"
  | "consent_third_party_transmission";

export type GrantedByActorCode = "client" | "operator" | "system";

export type RevocationScopeCode = "future_only" | "future_and_pending";

export type ConsentPayload = {
  client_id: string;
  session_id?: string | null;
  consent_type_code: ConsentTypeCode;
  consent_value: boolean;
  consent_version_code?: string;
  granted_by_actor_code: GrantedByActorCode;
  granted_at?: string | null;
  revoked_at?: string | null;
  revocation_scope_code?: RevocationScopeCode | null;
  notes?: string | null;
  record_status?: "draft" | "active" | "validated" | "closed" | "deprecated" | "archived";
};

export type ConsentRecord = {
  id: string;
  client_id: string;
  session_id: string | null;
  consent_type_code: ConsentTypeCode;
  consent_value: boolean;
  consent_version_code: string;
  granted_by_actor_code: GrantedByActorCode;
  granted_at: string;
  revoked_at: string | null;
  revocation_scope_code: RevocationScopeCode | null;
  notes: string | null;
  record_status: "draft" | "active" | "validated" | "closed" | "deprecated" | "archived";
  created_at: string;
  updated_at: string;
};

export type DerivedDocumentRecord = {
  id: string;
  client_id: string;
  session_id: string;
  source_note_id: string;
  document_kind_code: string;
  audience_code: string;
  title: string;
  body_text: string;
  client_visible: boolean;
  record_status: "draft" | "active" | "validated" | "closed" | "deprecated" | "archived";
  data_sensitivity_class: "low" | "moderate" | "high" | "restricted";
  retention_class: "ephemeral" | "short_term" | "standard" | "extended" | "archival";
  created_at: string;
  updated_at: string;
};

export type AuthUser = {
  id: string;
  email: string;
  display_name: string;
  role: string;
  created_at: string;
  updated_at: string;
};

export type LoginResponse = {
  access_token: string;
  token_type: string;
  user: AuthUser;
};

export type SessionPayload = {
  client_id: string;
  intake_request_id?: string | null;
  session_sequence_number?: number | null;
  session_mode_code?: "standard" | "intake" | "follow_up";
  session_channel_code?: "phone" | "video" | "in_person" | "async";
  scheduled_start_at?: string | null;
  actual_start_at?: string | null;
  actual_end_at?: string | null;
  duration_minutes?: number | null;
  session_status_code?: "scheduled" | "in_progress" | "completed" | "cancelled" | "no_show" | "escalated";
  record_status?: "draft" | "active" | "validated" | "closed" | "deprecated" | "archived";
  data_sensitivity_class?: "low" | "moderate" | "high" | "restricted";
  retention_class?: "ephemeral" | "short_term" | "standard" | "extended" | "archival";
};

export type SessionRecord = {
  id: string;
  client_id: string;
  intake_request_id: string | null;
  session_sequence_number: number;
  session_mode_code: string;
  session_channel_code: string;
  scheduled_start_at: string | null;
  actual_start_at: string | null;
  actual_end_at: string | null;
  duration_minutes: number | null;
  operator_user_id: string;
  session_status_code: string;
  record_status: string;
  data_sensitivity_class: string;
  retention_class: string;
  created_at: string;
  updated_at: string;
};

export type SessionClosePayload = {
  actual_start_at?: string | null;
  actual_end_at?: string | null;
  session_status_code: "completed" | "cancelled" | "no_show" | "escalated";
  presenting_topic_text: string;
  session_highlights_text: string;
  operator_assessment_text?: string | null;
  vigilance_level_code?: "non_urgent" | "watch" | "priority" | "urgent";
  follow_up_actions_text?: string | null;
  next_session_focus_text?: string | null;
  client_visible?: boolean;
};

export type SessionCloseResult = {
  session: SessionRecord;
  generated_note: SessionNoteRecord;
  generated_document: DerivedDocumentRecord;
};

export type SessionStartPayload = {
  actual_start_at?: string | null;
};

export type AudioSessionRecord = {
  id: string;
  session_id: string;
  provider_code: "livekit" | "manual";
  audio_session_status_code: "provisioned" | "active" | "closed" | "failed";
  room_name: string;
  provider_room_url: string | null;
  recording_enabled: boolean;
  operator_participant_identity: string;
  client_participant_identity: string;
  practitioner_participant_identity: string | null;
  created_at: string;
  updated_at: string;
};

export type AudioSessionJoinRecord = {
  audio_session_id: string;
  room_name: string;
  participant_identity: string;
  provider_code: "livekit" | "manual";
  ws_url: string;
  token: string;
};

export type AudioRecordingRecord = {
  id: string;
  audio_session_id: string;
  provider_code: "livekit" | "manual";
  audio_recording_status_code: "starting" | "recording" | "ready" | "failed";
  provider_recording_id: string | null;
  output_location: string | null;
  failure_reason: string | null;
  requested_by_user_id: string;
  started_at: string | null;
  ended_at: string | null;
  created_at: string;
  updated_at: string;
};

export type SessionNotePayload = {
  session_id: string;
  client_id: string;
  note_sequence_number?: number | null;
  summary_text: string;
  observations_text?: string | null;
  follow_up_actions_text?: string | null;
  next_session_focus_text?: string | null;
  client_visible?: boolean;
  record_status?: "draft" | "active" | "validated" | "closed" | "deprecated" | "archived";
  data_sensitivity_class?: "low" | "moderate" | "high" | "restricted";
  retention_class?: "ephemeral" | "short_term" | "standard" | "extended" | "archival";
};

export type SessionNoteRecord = {
  id: string;
  session_id: string;
  client_id: string;
  note_sequence_number: number;
  summary_text: string;
  observations_text: string | null;
  follow_up_actions_text: string | null;
  next_session_focus_text: string | null;
  coeur_summary_text: string | null;
  corps_summary_text: string | null;
  esprit_summary_text: string | null;
  etre_summary_text: string | null;
  immediate_context_text: string | null;
  context_factors_json: Record<string, unknown> | Array<unknown> | null;
  context_hypotheses_json: Record<string, unknown> | Array<unknown> | null;
  identified_tensions_json: Record<string, unknown> | Array<unknown> | null;
  vigilance_level_code: "non_urgent" | "watch" | "priority" | "urgent";
  next_step_type_code: string | null;
  client_facing_summary_text: string | null;
  supervision_summary_text: string | null;
  research_notes_text: string | null;
  model_used: string | null;
  prompt_version: string | null;
  complexity_score: number | null;
  validated_by_practitioner: boolean;
  validated_at: string | null;
  practitioner_corrections: Record<string, unknown> | Array<unknown> | null;
  client_visible: boolean;
  record_status: string;
  data_sensitivity_class: string;
  retention_class: string;
  created_at: string;
  updated_at: string;
};

export type SessionNoteValidationPayload = {
  validated: boolean;
  corrections?: {
    coeur?: string;
    corps?: string;
    esprit?: string;
    etre?: string;
    tensions?: string[];
    vigilance?: string;
    next_step?: string;
  } | null;
};

export async function registerOperator(payload: {
  email: string;
  password: string;
  display_name: string;
  role: "admin_tech" | "operator" | "supervisor" | "public_client";
}): Promise<AuthUser> {
  return request<AuthUser>("/api/v1/auth/register", {
    method: "POST",
    body: payload,
  });
}

export async function createClient(payload: ClientPayload): Promise<ClientRecord> {
  return request<ClientRecord>("/api/v1/clients", {
    method: "POST",
    body: payload,
  });
}

export async function createIntakeRequest(
  payload: IntakeRequestPayload,
): Promise<IntakeRequestRecord> {
  return request<IntakeRequestRecord>("/api/v1/intake-requests", {
    method: "POST",
    body: payload,
  });
}

export async function listIntakeRequests(
  token: string,
  options?: { clientId?: string },
): Promise<IntakeRequestRecord[]> {
  const query = options?.clientId
    ? `?client_id=${encodeURIComponent(options.clientId)}`
    : "";

  return request<IntakeRequestRecord[]>(`/api/v1/intake-requests${query}`, {
    token,
  });
}

export async function createConsent(
  payload: ConsentPayload,
  token?: string,
): Promise<ConsentRecord> {
  return request<ConsentRecord>("/api/v1/consents", {
    method: "POST",
    body: payload,
    token,
  });
}

export async function loginOperator(
  email: string,
  password: string,
): Promise<LoginResponse> {
  return request<LoginResponse>("/api/v1/auth/login", {
    method: "POST",
    body: { email, password },
  });
}

export async function listClients(token: string): Promise<ClientRecord[]> {
  return request<ClientRecord[]>("/api/v1/clients", {
    token,
  });
}

export async function listConsents(
  token: string,
  options?: { clientId?: string },
): Promise<ConsentRecord[]> {
  const query = options?.clientId
    ? `?client_id=${encodeURIComponent(options.clientId)}`
    : "";

  return request<ConsentRecord[]>(`/api/v1/consents${query}`, {
    token,
  });
}

export async function listDerivedDocuments(
  token: string,
  options?: { clientId?: string; sessionId?: string },
): Promise<DerivedDocumentRecord[]> {
  const params = new URLSearchParams();
  if (options?.clientId) {
    params.set("client_id", options.clientId);
  }
  if (options?.sessionId) {
    params.set("session_id", options.sessionId);
  }
  const query = params.size > 0 ? `?${params.toString()}` : "";

  return request<DerivedDocumentRecord[]>(`/api/v1/derived-documents${query}`, {
    token,
  });
}

export async function listPublicDerivedDocuments(
  publicClientCode: string,
): Promise<DerivedDocumentRecord[]> {
  return request<DerivedDocumentRecord[]>(
    `/api/v1/derived-documents/public/client/${encodeURIComponent(publicClientCode)}`,
  );
}

export async function createSession(
  payload: SessionPayload,
  token: string,
): Promise<SessionRecord> {
  return request<SessionRecord>("/api/v1/sessions", {
    method: "POST",
    body: payload,
    token,
  });
}

export async function listSessions(token: string): Promise<SessionRecord[]> {
  return request<SessionRecord[]>("/api/v1/sessions", {
    token,
  });
}

export async function startSession(
  sessionId: string,
  payload: SessionStartPayload,
  token: string,
): Promise<SessionRecord> {
  return request<SessionRecord>(`/api/v1/sessions/${sessionId}/start`, {
    method: "POST",
    body: payload,
    token,
  });
}

export async function closeSession(
  sessionId: string,
  payload: SessionClosePayload,
  token: string,
): Promise<SessionCloseResult> {
  return request<SessionCloseResult>(`/api/v1/sessions/${sessionId}/close`, {
    method: "POST",
    body: payload,
    token,
  });
}

export async function provisionAudioSession(
  sessionId: string,
  token: string,
): Promise<AudioSessionRecord> {
  return request<AudioSessionRecord>(`/api/v1/audio-sessions/sessions/${sessionId}/provision`, {
    method: "POST",
    body: {},
    token,
  });
}

export async function listAudioSessions(token: string): Promise<AudioSessionRecord[]> {
  return request<AudioSessionRecord[]>("/api/v1/audio-sessions", {
    token,
  });
}

export async function listAudioRecordings(token: string): Promise<AudioRecordingRecord[]> {
  return request<AudioRecordingRecord[]>("/api/v1/audio-recordings", {
    token,
  });
}

export async function createOperatorJoinContext(
  audioSessionId: string,
  token: string,
): Promise<AudioSessionJoinRecord> {
  return request<AudioSessionJoinRecord>(`/api/v1/audio-sessions/${audioSessionId}/operator-join`, {
    method: "POST",
    body: {},
    token,
  });
}

export async function createClientJoinContext(
  audioSessionId: string,
  token: string,
): Promise<AudioSessionJoinRecord> {
  return request<AudioSessionJoinRecord>(`/api/v1/audio-sessions/${audioSessionId}/client-join`, {
    method: "POST",
    body: {},
    token,
  });
}

export async function startAudioRecording(
  audioSessionId: string,
  token: string,
): Promise<AudioRecordingRecord> {
  return request<AudioRecordingRecord>(`/api/v1/audio-recordings/audio-sessions/${audioSessionId}/start`, {
    method: "POST",
    body: {},
    token,
  });
}

export async function stopAudioRecording(
  audioRecordingId: string,
  token: string,
): Promise<AudioRecordingRecord> {
  return request<AudioRecordingRecord>(`/api/v1/audio-recordings/${audioRecordingId}/stop`, {
    method: "POST",
    body: {},
    token,
  });
}

export async function createSessionNote(
  payload: SessionNotePayload,
  token: string,
): Promise<SessionNoteRecord> {
  return request<SessionNoteRecord>("/api/v1/session-notes", {
    method: "POST",
    body: payload,
    token,
  });
}

export async function listSessionNotes(token: string): Promise<SessionNoteRecord[]> {
  return request<SessionNoteRecord[]>("/api/v1/session-notes", {
    token,
  });
}

export async function validateSessionNote(
  noteId: string,
  payload: SessionNoteValidationPayload,
  token: string,
): Promise<SessionNoteRecord> {
  return request<SessionNoteRecord>(`/api/v1/session-notes/${noteId}/validate`, {
    method: "PATCH",
    body: payload,
    token,
  });
}

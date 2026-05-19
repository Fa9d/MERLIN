function resolveMerlinApiBaseUrl(): string {
  const explicitBaseUrl = process.env.NEXT_PUBLIC_MERLIN_API_BASE_URL?.replace(/\/$/, "");
  if (explicitBaseUrl) {
    return explicitBaseUrl;
  }

  if (typeof window !== "undefined") {
    const protocol = window.location.protocol === "https:" ? "https:" : "http:";
    return `${protocol}//${window.location.hostname}:8000`;
  }

  return "http://127.0.0.1:8000";
}

export const MERLIN_API_BASE_URL = resolveMerlinApiBaseUrl();

type RequestOptions = {
  method?: "GET" | "POST" | "PATCH";
  body?: unknown;
  token?: string;
};

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const baseUrl = resolveMerlinApiBaseUrl();
  let response: Response;

  try {
    response = await fetch(`${baseUrl}${path}`, {
      method: options.method ?? "GET",
      headers: {
        "Content-Type": "application/json",
        ...(options.token ? { Authorization: `Bearer ${options.token}` } : {}),
      },
      body: options.body ? JSON.stringify(options.body) : undefined,
    });
  } catch (error) {
    const suffix = error instanceof Error && error.message ? ` (${error.message})` : "";
    throw new Error(
      `Connexion au serveur IVIA impossible. Verifiez que l'API repond sur ${baseUrl}.${suffix}`,
    );
  }

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
  record_status?: string;
  data_sensitivity_class?: string;
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

export type ClientEntitlementRecord = {
  id: string;
  client_id: string;
  payment_order_id: string | null;
  entitlement_type_code: "intake_session_credit" | "follow_up_session_credit" | "journal_day";
  quantity_total: number;
  quantity_remaining: number;
  starts_at: string;
  expires_at: string | null;
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

export const PUBLIC_CLIENT_STORAGE_KEY = "merlin_public_client_session";

export type SessionPayload = {
  client_id: string;
  intake_request_id?: string | null;
  session_sequence_number?: number | null;
  session_mode_code?: "standard" | "intake" | "follow_up";
  session_channel_code?: "direct" | "in_person" | "async";
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
  praticien_id: string | null;
  session_status_code: string;
  record_status: string;
  data_sensitivity_class: string;
  retention_class: string;
  created_at: string;
  updated_at: string;
  room_name: string | null;
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

export async function createClient(payload: ClientPayload, token?: string): Promise<ClientRecord> {
  return request<ClientRecord>("/api/v1/clients", {
    method: "POST",
    body: payload,
    token,
  });
}

export async function createIntakeRequest(
  payload: IntakeRequestPayload,
  token?: string,
): Promise<IntakeRequestRecord> {
  return request<IntakeRequestRecord>("/api/v1/intake-requests", {
    method: "POST",
    body: payload,
    token,
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

export async function listClientEntitlements(
  token: string,
  options?: { clientId?: string },
): Promise<ClientEntitlementRecord[]> {
  const query = options?.clientId
    ? `?client_id=${encodeURIComponent(options.clientId)}`
    : "";

  return request<ClientEntitlementRecord[]>(`/api/v1/client-entitlements${query}`, {
    token,
  });
}

export async function listMyEntitlements(token: string): Promise<ClientEntitlementRecord[]> {
  return request<ClientEntitlementRecord[]>("/api/v1/client-entitlements/me", {
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
  intakeRequestId: string,
): Promise<DerivedDocumentRecord[]> {
  const query = `?intake_request_id=${encodeURIComponent(intakeRequestId)}`;
  return request<DerivedDocumentRecord[]>(
    `/api/v1/derived-documents/public/client/${encodeURIComponent(publicClientCode)}${query}`,
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

export async function assignPraticien(
  sessionId: string,
  praticienId: string | null,
  token: string,
): Promise<SessionRecord> {
  return request<SessionRecord>(`/api/v1/sessions/${sessionId}/assign`, {
    method: "PATCH",
    body: { praticien_id: praticienId },
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

export type PraticienPublic = {
  id: string;
  display_name: string;
  title_line: string | null;
  intro_text: string | null;
  spoken_languages: string | null;
  available_channels: string | null;
};

export async function listPraticiens(): Promise<PraticienPublic[]> {
  return request<PraticienPublic[]>("/api/v1/praticiens");
}

export type IntakeSignal = {
  code: string;
  label: string;
  severity: "rouge" | "orange" | "jaune" | "info";
};

export type IntakeAnalysisResult = {
  intake_request_id: string;
  risk_signals: IntakeSignal[];
  gap_signals: IntakeSignal[];
  suggested_urgency: string;
  current_urgency: string;
  has_risk: boolean;
  has_gaps: boolean;
  urgency_upgrade_suggested: boolean;
};

export async function analyseIntakeRequest(
  intakeRequestId: string,
  token: string,
): Promise<IntakeAnalysisResult> {
  return request<IntakeAnalysisResult>(`/api/v1/intake-requests/${intakeRequestId}/analyse`, {
    token,
  });
}

// ---------------------------------------------------------------------------
// Schedule / Disponibilités praticien
// ---------------------------------------------------------------------------

export type SessionTypeCode = "intake" | "standard" | "follow_up" | "any";
export type ExceptionType = "blocked" | "extra";
export type SlotStatus = "available" | "hold" | "confirmed" | "cancelled";

export type ScheduleSlotRecord = {
  id: string;
  praticien_id: string;
  day_of_week: number;
  day_label: string;
  start_time: string;     // "HH:MM:SS"
  end_time: string;
  session_duration_minutes: number;
  buffer_minutes: number;
  session_type: SessionTypeCode;
  session_type_label: string;
  valid_from: string | null;
  valid_until: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
};

export type ScheduleSlotCreate = {
  day_of_week: number;
  start_time: string;     // "HH:MM"
  end_time: string;
  session_duration_minutes?: number;
  buffer_minutes?: number;
  session_type?: SessionTypeCode;
  valid_from?: string | null;
  valid_until?: string | null;
};

export type ScheduleExceptionRecord = {
  id: string;
  praticien_id: string;
  exception_date: string;
  exception_type: ExceptionType;
  start_time: string | null;
  end_time: string | null;
  reason: string | null;
  created_at: string;
};

export type ScheduleExceptionCreate = {
  exception_date: string;
  exception_type?: ExceptionType;
  start_time?: string | null;
  end_time?: string | null;
  reason?: string | null;
};

export type AvailableSlotRecord = {
  praticien_id: string;
  praticien_name: string;
  slot_date: string;
  start_time: string;
  end_time: string;
  session_type: SessionTypeCode;
  session_type_label: string;
  duration_minutes: number;
  slot_id: string | null;
  status: SlotStatus;
};

export async function listMySchedule(token: string): Promise<ScheduleSlotRecord[]> {
  return request<ScheduleSlotRecord[]>("/api/v1/schedules/my", { token });
}

export async function createScheduleSlot(
  payload: ScheduleSlotCreate,
  token: string,
): Promise<ScheduleSlotRecord> {
  return request<ScheduleSlotRecord>("/api/v1/schedules/my", {
    method: "POST",
    body: payload,
    token,
  });
}

export async function deleteScheduleSlot(slotId: string, token: string): Promise<void> {
  const url = `${MERLIN_API_BASE_URL}/api/v1/schedules/my/${slotId}`;
  const res = await fetch(url, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok && res.status !== 204) {
    throw new Error(`Erreur suppression créneau (${res.status})`);
  }
}

export async function listMyExceptions(token: string): Promise<ScheduleExceptionRecord[]> {
  return request<ScheduleExceptionRecord[]>("/api/v1/schedules/my/exceptions", { token });
}

export async function createScheduleException(
  payload: ScheduleExceptionCreate,
  token: string,
): Promise<ScheduleExceptionRecord> {
  return request<ScheduleExceptionRecord>("/api/v1/schedules/my/exceptions", {
    method: "POST",
    body: payload,
    token,
  });
}

export async function deleteScheduleException(excId: string, token: string): Promise<void> {
  const url = `${MERLIN_API_BASE_URL}/api/v1/schedules/my/exceptions/${excId}`;
  const res = await fetch(url, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok && res.status !== 204) {
    throw new Error(`Erreur suppression exception (${res.status})`);
  }
}

export async function listAvailableSlots(
  praticienId: string,
  dateFrom: string,
  dateTo: string,
): Promise<AvailableSlotRecord[]> {
  const params = new URLSearchParams({
    praticien_id: praticienId,
    date_from: dateFrom,
    date_to: dateTo,
  });
  return request<AvailableSlotRecord[]>(`/api/v1/schedules/available?${params.toString()}`);
}

// ---------------------------------------------------------------------------
// Inscription client + vérification email
// ---------------------------------------------------------------------------

export type ClientRegisterPayload = {
  email: string;
  password: string;
  display_name: string;
  redirect_path?: string | null;
};

export type ClientRegisterResult = {
  id: string;
  email: string;
  display_name: string;
  message: string;
};

export async function registerClient(
  payload: ClientRegisterPayload,
): Promise<ClientRegisterResult> {
  return request<ClientRegisterResult>("/api/v1/register/client", {
    method: "POST",
    body: payload,
  });
}

export async function loginUser(
  email: string,
  password: string,
): Promise<LoginResponse> {
  return loginOperator(email, password);
}

export function readStoredPublicClientSession(): LoginResponse | null {
  if (typeof window === "undefined") {
    return null;
  }

  const raw = window.localStorage.getItem(PUBLIC_CLIENT_STORAGE_KEY)
    ?? window.sessionStorage.getItem(PUBLIC_CLIENT_STORAGE_KEY);
  if (!raw) {
    return null;
  }

  try {
    return JSON.parse(raw) as LoginResponse;
  } catch {
    return null;
  }
}

export type VerifyEmailResult = {
  message: string;
};

export async function verifyEmail(token: string): Promise<VerifyEmailResult> {
  return request<VerifyEmailResult>(`/api/v1/verify-email/${token}`);
}

// ---------------------------------------------------------------------------
// Bookings
// ---------------------------------------------------------------------------

export type BookingSlotRecord = {
  id: string;
  praticien_id: string;
  client_id: string | null;
  slot_date: string;
  start_time: string;
  end_time: string;
  session_type: SessionTypeCode;
  status: SlotStatus;
  hold_expires_at: string | null;
  notes: string | null;
  created_at: string;
  updated_at: string;
};

export type InteracEtransferPayload = {
  client_id: string;
  operator_user_id?: string | null;
  intake_request_id?: string | null;
  slot_id?: string | null;
  product_code: string;
  product_label: string;
  product_kind_code:
    | "session_intake"
    | "session_follow_up"
    | "journal_days_pack"
    | "audio_async_follow_up"
    | "custom";
  fulfillment_mode_code:
    | "grant_entitlement_only"
    | "grant_entitlement_and_create_audio_async_session";
  amount_cents: number;
  currency?: string;
  entitlement_type_code?: "intake_session_credit" | "follow_up_session_credit" | "journal_day" | null;
  entitlement_quantity?: number | null;
};

export type InteracEtransferRequestRecord = {
  order_id: string;
  status: string;
  amount_cents: number;
  currency: string;
  recipient_name: string;
  recipient_email: string;
  transfer_reference: string;
  instructions_text: string;
  instructions_emailed: boolean;
};

export type StripeCheckoutPayload = {
  client_id: string;
  operator_user_id?: string | null;
  intake_request_id?: string | null;
  slot_id?: string | null;
  product_code: string;
  product_label: string;
  product_kind_code:
    | "session_intake"
    | "session_follow_up"
    | "journal_days_pack"
    | "audio_async_follow_up"
    | "custom";
  fulfillment_mode_code:
    | "grant_entitlement_only"
    | "grant_entitlement_and_create_audio_async_session";
  amount_cents: number;
  currency?: string;
  entitlement_type_code?: "intake_session_credit" | "follow_up_session_credit" | "journal_day" | null;
  entitlement_quantity?: number | null;
  success_url?: string | null;
  cancel_url?: string | null;
};

export type StripeCheckoutSessionRecord = {
  order_id: string;
  product_code: string;
  checkout_session_id: string;
  checkout_url: string;
  amount_cents: number;
  currency: string;
};

export async function holdSlot(slotId: string, token: string): Promise<BookingSlotRecord> {
  return request<BookingSlotRecord>("/api/v1/bookings/hold", {
    method: "POST",
    body: { slot_id: slotId },
    token,
  });
}

export async function confirmSlot(
  slotId: string,
  token: string,
  notes?: string,
): Promise<BookingSlotRecord> {
  return request<BookingSlotRecord>("/api/v1/bookings/confirm", {
    method: "POST",
    body: { slot_id: slotId, notes: notes ?? null },
    token,
  });
}

export async function cancelSlot(slotId: string, token: string): Promise<BookingSlotRecord> {
  return request<BookingSlotRecord>("/api/v1/bookings/cancel", {
    method: "POST",
    body: { slot_id: slotId },
    token,
  });
}

export async function listMyBookings(token: string): Promise<BookingSlotRecord[]> {
  return request<BookingSlotRecord[]>("/api/v1/bookings/my", { token });
}

export async function requestInteracEtransfer(
  payload: InteracEtransferPayload,
): Promise<InteracEtransferRequestRecord> {
  return request<InteracEtransferRequestRecord>("/api/v1/payments/interac/etransfer/request", {
    method: "POST",
    body: payload,
  });
}

export async function requestPublicStripeCheckout(
  payload: StripeCheckoutPayload,
): Promise<StripeCheckoutSessionRecord> {
  return request<StripeCheckoutSessionRecord>("/api/v1/payments/stripe/public-checkout", {
    method: "POST",
    body: payload,
  });
}

// ---------------------------------------------------------------------------
// Parcours public d'entrée — un seul appel orchestre intake + magic link.
// Le mail d'activation est envoyé automatiquement par le backend si email fourni.
// ---------------------------------------------------------------------------

export type PublicIntakeStartPayload = {
  first_name_or_alias: string;
  email?: string | null;
  phone?: string | null;
  is_adult_confirmed: boolean;
  primary_need_code:
    | "clarification"
    | "support"
    | "orientation"
    | "loneliness"
    | "distress"
    | "other";
  perceived_urgency_code?: "non_urgent" | "watch" | "priority" | "urgent";
  support_already_in_place?: boolean;
  requested_outcome_text?: string | null;
  entry_summary_text?: string | null;
  consent_session: boolean;
  consent_session_note: boolean;
  consent_history: boolean;
};

export type PublicIntakeStartResult = {
  client_id: string;
  public_client_code: string;
  intake_request_id: string;
  magic_link_sent: boolean;
  email_used: string | null;
  message: string;
};

export async function startPublicIntake(
  payload: PublicIntakeStartPayload,
): Promise<PublicIntakeStartResult> {
  return request<PublicIntakeStartResult>("/api/v1/public/intake/start", {
    method: "POST",
    body: payload,
  });
}

export type PublicActivateResult = {
  access_token: string;
  token_type: string;
  user_id: string;
  email: string;
  display_name: string;
  role: string;
  client_id: string;
  public_client_code: string;
  password_needed: boolean;
  message: string;
};

export async function consumeMagicLink(token: string): Promise<PublicActivateResult> {
  return request<PublicActivateResult>(
    `/api/v1/public/activate/${encodeURIComponent(token)}`,
    { method: "POST" },
  );
}

export type PublicActivatePreview = {
  valid: boolean;
  expires_at?: string | null;
  display_name?: string | null;
  email?: string | null;
};

export async function previewMagicLink(token: string): Promise<PublicActivatePreview> {
  return request<PublicActivatePreview>(
    `/api/v1/public/activate/preview/${encodeURIComponent(token)}`,
  );
}

// ---------------------------------------------------------------------------
// Fiche client durable — utilisée par /mon-espace
// ---------------------------------------------------------------------------

export type MyClientRecord = ClientRecord & {
  app_user_id: string | null;
  activation_invited_at: string | null;
  activation_accepted_at: string | null;
};

export async function getMyClient(token: string): Promise<MyClientRecord | null> {
  try {
    return await request<MyClientRecord>("/api/v1/clients/me", { token });
  } catch (error) {
    // 404 = aucun dossier client lié — comportement attendu pour /acces-client first.
    if (error instanceof Error && /404|introuvable/i.test(error.message)) {
      return null;
    }
    throw error;
  }
}


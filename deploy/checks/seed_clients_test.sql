-- ============================================================
-- MERLIN — Données de test clients (seed)
-- Généré : 2026-05-01
-- Clients couverts :
--   1. Sophie T.     — historique complet (1 × 10 min + 5 × 60 min)
--   2. Marc L.       — clarification, 1 séance planifiée
--   3. Lucie B.      — proche inquiet (pour son fils), vigilance priorité
--   4. André K.      — demande d'orientatif/alternatif, vidéo
--   5. Alex M.       — détresse, niveau watch, alias seulement
-- Opérateur : David Phaneuf (8dab08e6-27af-4195-a05a-ccc4ac1f2eac)
-- ============================================================

-- ============================================================
-- CLIENT 1 : Sophie T. — Historique complet
-- ============================================================

INSERT INTO clients (id, public_client_code, first_name_or_alias, last_name, email, phone,
  language_code, timezone, territory_code, is_adult_confirmed,
  record_status, data_sensitivity_class, created_at, updated_at)
VALUES (
  'a1cafe01-test-0001-0001-000000000001',
  'CLI-SOPHIE0001',
  'Sophie', 'T.', 'sophie.t.test@ivia.quebec', NULL,
  'fr-CA', 'America/Toronto', 'QC', true,
  'active', 'high',
  '2026-02-01 09:00:00+00', '2026-04-17 10:00:00+00'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO intake_requests (id, client_id, request_channel_code, request_for_code,
  primary_need_code, perceived_urgency_code, support_already_in_place,
  requested_outcome_text, entry_summary_text, referential_version,
  record_status, created_at, updated_at)
VALUES (
  'b1cafe01-test-0001-0001-000000000001',
  'a1cafe01-test-0001-0001-000000000001',
  'direct', 'self', 'support', 'non_urgent', false,
  'Je veux mieux comprendre ce que je vis et avoir un espace pour en parler.',
  'Femme ~34 ans, séparation récente (3 mois), épuisement émotionnel, ruminations. Pas de danger immédiat. Porte ouverte sur suivi court.',
  'v1', 'active',
  '2026-02-01 09:00:00+00', '2026-02-01 09:00:00+00'
) ON CONFLICT (id) DO NOTHING;

-- Consentements client Sophie (niveau dossier)
INSERT INTO consents (id, client_id, session_id, consent_type_code, consent_value,
  consent_version_code, granted_by_actor_code, granted_at, record_status, created_at, updated_at)
VALUES
  ('c1ca0101-test-0001-0001-000000000001', 'a1cafe01-test-0001-0001-000000000001', NULL,
   'consent_history', true, 'v1', 'client', '2026-02-01 09:05:00+00',
   'active', '2026-02-01 09:05:00+00', '2026-02-01 09:05:00+00'),
  ('c1ca0102-test-0001-0001-000000000001', 'a1cafe01-test-0001-0001-000000000001', NULL,
   'consent_session_note', true, 'v1', 'client', '2026-02-01 09:05:00+00',
   'active', '2026-02-01 09:05:00+00', '2026-02-01 09:05:00+00'),
  ('c1ca0103-test-0001-0001-000000000001', 'a1cafe01-test-0001-0001-000000000001', NULL,
   'consent_recording', false, 'v1', 'client', '2026-02-01 09:05:00+00',
   'active', '2026-02-01 09:05:00+00', '2026-02-01 09:05:00+00'),
  ('c1ca0104-test-0001-0001-000000000001', 'a1cafe01-test-0001-0001-000000000001', NULL,
   'consent_transcription', false, 'v1', 'client', '2026-02-01 09:05:00+00',
   'active', '2026-02-01 09:05:00+00', '2026-02-01 09:05:00+00')
ON CONFLICT (id) DO NOTHING;

-- ---- SÉANCE 1 : 10 min, intake/test ----
INSERT INTO sessions (id, client_id, intake_request_id, session_sequence_number,
  session_mode_code, session_channel_code,
  scheduled_start_at, actual_start_at, actual_end_at, duration_minutes,
  operator_user_id, session_status_code, record_status,
  data_sensitivity_class, retention_class, created_at, updated_at)
VALUES (
  's1cafe01-test-0001-0001-000000000001',
  'a1cafe01-test-0001-0001-000000000001',
  'b1cafe01-test-0001-0001-000000000001',
  1, 'intake', 'direct',
  '2026-02-01 10:00:00+00', '2026-02-01 10:00:00+00', '2026-02-01 10:10:00+00', 10,
  '8dab08e6-27af-4195-a05a-ccc4ac1f2eac',
  'completed', 'active', 'high', 'standard',
  '2026-02-01 10:00:00+00', '2026-02-01 10:12:00+00'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO consents (id, client_id, session_id, consent_type_code, consent_value,
  consent_version_code, granted_by_actor_code, granted_at, record_status, created_at, updated_at)
VALUES
  ('c1ca0201-test-0001-0001-000000000001',
   'a1cafe01-test-0001-0001-000000000001',
   's1cafe01-test-0001-0001-000000000001',
   'consent_session', true, 'v1', 'client', '2026-02-01 10:00:00+00',
   'active', '2026-02-01 10:00:00+00', '2026-02-01 10:00:00+00')
ON CONFLICT (id) DO NOTHING;

INSERT INTO session_notes (id, session_id, client_id, note_sequence_number,
  summary_text, observations_text, follow_up_actions_text, next_session_focus_text,
  vigilance_level_code, next_step_type_code,
  validated_by_practitioner, client_visible, record_status,
  data_sensitivity_class, retention_class, created_at, updated_at)
VALUES (
  'n1cafe01-test-0001-0001-000000000001',
  's1cafe01-test-0001-0001-000000000001',
  'a1cafe01-test-0001-0001-000000000001',
  1,
  'Premier contact 10 min. Sophie, ~34 ans, séparation récente 3 mois. Épuisement émotionnel, rumination. Pas de danger. Cadre MERLIN présenté et accepté. Entrée confirmée.',
  'Voix stable, ton contenu. Débit légèrement rapide — anxiété légère possible. Réceptive à l''approche.',
  'Fixer prochaine séance 60 min.',
  'Espace de parole sur la séparation et l''identité.',
  'non_urgent', 'propose_follow_up',
  true, false, 'active', 'high', 'standard',
  '2026-02-01 10:15:00+00', '2026-02-01 10:20:00+00'
) ON CONFLICT (id) DO NOTHING;

-- ---- SÉANCE 2 : 60 min ----
INSERT INTO sessions (id, client_id, intake_request_id, session_sequence_number,
  session_mode_code, session_channel_code,
  scheduled_start_at, actual_start_at, actual_end_at, duration_minutes,
  operator_user_id, session_status_code, record_status,
  data_sensitivity_class, retention_class, created_at, updated_at)
VALUES (
  's1cafe02-test-0001-0001-000000000001',
  'a1cafe01-test-0001-0001-000000000001',
  'b1cafe01-test-0001-0001-000000000001',
  2, 'follow_up', 'direct',
  '2026-02-15 10:00:00+00', '2026-02-15 10:02:00+00', '2026-02-15 11:02:00+00', 60,
  '8dab08e6-27af-4195-a05a-ccc4ac1f2eac',
  'completed', 'active', 'high', 'standard',
  '2026-02-15 10:00:00+00', '2026-02-15 11:05:00+00'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO consents (id, client_id, session_id, consent_type_code, consent_value,
  consent_version_code, granted_by_actor_code, granted_at, record_status, created_at, updated_at)
VALUES
  ('c1ca0301-test-0001-0001-000000000001',
   'a1cafe01-test-0001-0001-000000000001',
   's1cafe02-test-0001-0001-000000000001',
   'consent_session', true, 'v1', 'client', '2026-02-15 10:02:00+00',
   'active', '2026-02-15 10:02:00+00', '2026-02-15 10:02:00+00')
ON CONFLICT (id) DO NOTHING;

INSERT INTO session_notes (id, session_id, client_id, note_sequence_number,
  summary_text, observations_text, follow_up_actions_text, next_session_focus_text,
  coeur_summary_text, corps_summary_text, esprit_summary_text, etre_summary_text,
  vigilance_level_code, next_step_type_code,
  validated_by_practitioner, client_visible, record_status,
  data_sensitivity_class, retention_class, created_at, updated_at)
VALUES (
  'n1cafe02-test-0001-0001-000000000001',
  's1cafe02-test-0001-0001-000000000001',
  'a1cafe01-test-0001-0001-000000000001',
  1,
  'Retour sur la rupture. Mélange de soulagement et de perte identitaire. Exprime difficulté à «exister seule». Travail d''écoute, espace de parole tenu.',
  'Pleure à l''évocation de la vie à deux. Humour défensif observé en fin de séance — mécanisme de clôture habituel.',
  NULL,
  'Explorer qui est Sophie en dehors du couple.',
  'Deuil relationnel actif. Confond fin du couple avec fin d''elle-même.',
  'Rapporte insomnie légère, appétit variable.',
  'Identité fortement définie par la relation perdue.',
  NULL,
  'non_urgent', 'continue_to_structure',
  true, false, 'active', 'high', 'standard',
  '2026-02-15 11:08:00+00', '2026-02-15 11:20:00+00'
) ON CONFLICT (id) DO NOTHING;

-- ---- SÉANCE 3 : 60 min ----
INSERT INTO sessions (id, client_id, intake_request_id, session_sequence_number,
  session_mode_code, session_channel_code,
  scheduled_start_at, actual_start_at, actual_end_at, duration_minutes,
  operator_user_id, session_status_code, record_status,
  data_sensitivity_class, retention_class, created_at, updated_at)
VALUES (
  's1cafe03-test-0001-0001-000000000001',
  'a1cafe01-test-0001-0001-000000000001',
  'b1cafe01-test-0001-0001-000000000001',
  3, 'follow_up', 'direct',
  '2026-03-01 10:00:00+00', '2026-03-01 10:01:00+00', '2026-03-01 11:01:00+00', 60,
  '8dab08e6-27af-4195-a05a-ccc4ac1f2eac',
  'completed', 'active', 'high', 'standard',
  '2026-03-01 10:00:00+00', '2026-03-01 11:05:00+00'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO consents (id, client_id, session_id, consent_type_code, consent_value,
  consent_version_code, granted_by_actor_code, granted_at, record_status, created_at, updated_at)
VALUES
  ('c1ca0401-test-0001-0001-000000000001',
   'a1cafe01-test-0001-0001-000000000001',
   's1cafe03-test-0001-0001-000000000001',
   'consent_session', true, 'v1', 'client', '2026-03-01 10:01:00+00',
   'active', '2026-03-01 10:01:00+00', '2026-03-01 10:01:00+00')
ON CONFLICT (id) DO NOTHING;

INSERT INTO session_notes (id, session_id, client_id, note_sequence_number,
  summary_text, observations_text, follow_up_actions_text, next_session_focus_text,
  coeur_summary_text,
  vigilance_level_code, next_step_type_code,
  validated_by_practitioner, client_visible, record_status,
  data_sensitivity_class, retention_class, created_at, updated_at)
VALUES (
  'n1cafe03-test-0001-0001-000000000001',
  's1cafe03-test-0001-0001-000000000001',
  'a1cafe01-test-0001-0001-000000000001',
  1,
  'Exploration des rôles portés dans la relation de couple. Sophie parle de sa mère pour la première fois — comparaison implicite. Fatigue accrue au travail rapportée. Légère montée en vigilance ce cycle.',
  'Évite les silences — les remplit aussitôt. Possible inconfort avec le vide (émotionnel ou relationnel).',
  'Observer si le sujet maternel revient spontanément.',
  'Fatigue et limites professionnelles. Liens possibles avec le schème relationnel.',
  'Début de lien entre la relation amoureuse et la relation maternelle.',
  'watch', 'continue_to_structure',
  true, false, 'active', 'high', 'standard',
  '2026-03-01 11:08:00+00', '2026-03-01 11:22:00+00'
) ON CONFLICT (id) DO NOTHING;

-- ---- SÉANCE 4 : 60 min ----
INSERT INTO sessions (id, client_id, intake_request_id, session_sequence_number,
  session_mode_code, session_channel_code,
  scheduled_start_at, actual_start_at, actual_end_at, duration_minutes,
  operator_user_id, session_status_code, record_status,
  data_sensitivity_class, retention_class, created_at, updated_at)
VALUES (
  's1cafe04-test-0001-0001-000000000001',
  'a1cafe01-test-0001-0001-000000000001',
  'b1cafe01-test-0001-0001-000000000001',
  4, 'follow_up', 'direct',
  '2026-03-15 10:00:00+00', '2026-03-15 10:00:00+00', '2026-03-15 11:00:00+00', 60,
  '8dab08e6-27af-4195-a05a-ccc4ac1f2eac',
  'completed', 'active', 'high', 'standard',
  '2026-03-15 10:00:00+00', '2026-03-15 11:04:00+00'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO consents (id, client_id, session_id, consent_type_code, consent_value,
  consent_version_code, granted_by_actor_code, granted_at, record_status, created_at, updated_at)
VALUES
  ('c1ca0501-test-0001-0001-000000000001',
   'a1cafe01-test-0001-0001-000000000001',
   's1cafe04-test-0001-0001-000000000001',
   'consent_session', true, 'v1', 'client', '2026-03-15 10:00:00+00',
   'active', '2026-03-15 10:00:00+00', '2026-03-15 10:00:00+00')
ON CONFLICT (id) DO NOTHING;

INSERT INTO session_notes (id, session_id, client_id, note_sequence_number,
  summary_text, observations_text, next_session_focus_text,
  coeur_summary_text, corps_summary_text,
  vigilance_level_code, next_step_type_code,
  validated_by_practitioner, client_visible, record_status,
  data_sensitivity_class, retention_class, created_at, updated_at)
VALUES (
  'n1cafe04-test-0001-0001-000000000001',
  's1cafe04-test-0001-0001-000000000001',
  'a1cafe01-test-0001-0001-000000000001',
  1,
  'Retour à vigilance normale. Sophie fait état d''une «semaine différente» : appel d''une vieille amie, deux sorties. Travail sur la distinction désir/obligation dans ses engagements.',
  'Premier sourire authentique depuis le début du suivi. La fatigue semble moins centrale.',
  'Continuer l''exploration des désirs propres vs obligations intériorisées.',
  'Début d''une vie affective propre. Moins de deuil actif.',
  'Insomnie réduite. Appétit revenu.',
  'non_urgent', 'stabilize_rhythm_and_load',
  true, false, 'active', 'high', 'standard',
  '2026-03-15 11:06:00+00', '2026-03-15 11:18:00+00'
) ON CONFLICT (id) DO NOTHING;

-- ---- SÉANCE 5 : 60 min ----
INSERT INTO sessions (id, client_id, intake_request_id, session_sequence_number,
  session_mode_code, session_channel_code,
  scheduled_start_at, actual_start_at, actual_end_at, duration_minutes,
  operator_user_id, session_status_code, record_status,
  data_sensitivity_class, retention_class, created_at, updated_at)
VALUES (
  's1cafe05-test-0001-0001-000000000001',
  'a1cafe01-test-0001-0001-000000000001',
  'b1cafe01-test-0001-0001-000000000001',
  5, 'follow_up', 'direct',
  '2026-04-01 10:00:00+00', '2026-04-01 10:00:00+00', '2026-04-01 11:00:00+00', 60,
  '8dab08e6-27af-4195-a05a-ccc4ac1f2eac',
  'completed', 'active', 'high', 'standard',
  '2026-04-01 10:00:00+00', '2026-04-01 11:03:00+00'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO consents (id, client_id, session_id, consent_type_code, consent_value,
  consent_version_code, granted_by_actor_code, granted_at, record_status, created_at, updated_at)
VALUES
  ('c1ca0601-test-0001-0001-000000000001',
   'a1cafe01-test-0001-0001-000000000001',
   's1cafe05-test-0001-0001-000000000001',
   'consent_session', true, 'v1', 'client', '2026-04-01 10:00:00+00',
   'active', '2026-04-01 10:00:00+00', '2026-04-01 10:00:00+00')
ON CONFLICT (id) DO NOTHING;

INSERT INTO session_notes (id, session_id, client_id, note_sequence_number,
  summary_text, observations_text, next_session_focus_text,
  etre_summary_text,
  vigilance_level_code, next_step_type_code,
  validated_by_practitioner, client_visible, record_status,
  data_sensitivity_class, retention_class, created_at, updated_at)
VALUES (
  'n1cafe05-test-0001-0001-000000000001',
  's1cafe05-test-0001-0001-000000000001',
  'a1cafe01-test-0001-0001-000000000001',
  1,
  'Réseau de soutien évoqué : Sophie identifie 3 personnes ressources. Aborde la question de la thérapie formelle — pas prête. Préfère continuer avec IVIA pour l''instant.',
  'Capacité de nommer les ressources sans les dévaloriser — évolution notable.',
  'Clarifier ce qu''elle attend de IVIA à long terme. Valider les acquis.',
  'Commence à se définir indépendamment de ses relations.',
  'non_urgent', 'mobilize_relational_resource',
  true, false, 'active', 'high', 'standard',
  '2026-04-01 11:05:00+00', '2026-04-01 11:17:00+00'
) ON CONFLICT (id) DO NOTHING;

-- ---- SÉANCE 6 : 60 min ----
INSERT INTO sessions (id, client_id, intake_request_id, session_sequence_number,
  session_mode_code, session_channel_code,
  scheduled_start_at, actual_start_at, actual_end_at, duration_minutes,
  operator_user_id, session_status_code, record_status,
  data_sensitivity_class, retention_class, created_at, updated_at)
VALUES (
  's1cafe06-test-0001-0001-000000000001',
  'a1cafe01-test-0001-0001-000000000001',
  'b1cafe01-test-0001-0001-000000000001',
  6, 'follow_up', 'direct',
  '2026-04-17 10:00:00+00', '2026-04-17 10:00:00+00', '2026-04-17 11:00:00+00', 60,
  '8dab08e6-27af-4195-a05a-ccc4ac1f2eac',
  'completed', 'active', 'high', 'standard',
  '2026-04-17 10:00:00+00', '2026-04-17 11:04:00+00'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO consents (id, client_id, session_id, consent_type_code, consent_value,
  consent_version_code, granted_by_actor_code, granted_at, record_status, created_at, updated_at)
VALUES
  ('c1ca0701-test-0001-0001-000000000001',
   'a1cafe01-test-0001-0001-000000000001',
   's1cafe06-test-0001-0001-000000000001',
   'consent_session', true, 'v1', 'client', '2026-04-17 10:00:00+00',
   'active', '2026-04-17 10:00:00+00', '2026-04-17 10:00:00+00')
ON CONFLICT (id) DO NOTHING;

INSERT INTO session_notes (id, session_id, client_id, note_sequence_number,
  summary_text, observations_text, follow_up_actions_text,
  coeur_summary_text, etre_summary_text,
  vigilance_level_code, next_step_type_code,
  validated_by_practitioner, client_visible, record_status,
  data_sensitivity_class, retention_class, created_at, updated_at)
VALUES (
  'n1cafe06-test-0001-0001-000000000001',
  's1cafe06-test-0001-0001-000000000001',
  'a1cafe01-test-0001-0001-000000000001',
  1,
  'Séance de bilan partiel. Évolution nette depuis S1 : moins de rumination, humeur stabilisée. Aborde projet de voyage solo pour l''été. Cadre ouvert, suivi non urgent.',
  'Transformation visible du ton. Moins besoin d''être rassurée, plus de curiosité sur elle-même. Rit franchement à deux reprises.',
  'Proposer cadence mensuelle ou selon besoins. Rappeler option de retour à tout moment.',
  'Deuil traversé. Lien reconstruit avec elle-même.',
  'Projet personnel émergent (voyage solo) — signe d''ancrage identitaire.',
  'non_urgent', 'propose_follow_up',
  true, true, 'active', 'high', 'standard',
  '2026-04-17 11:06:00+00', '2026-04-17 11:20:00+00'
) ON CONFLICT (id) DO NOTHING;


-- ============================================================
-- CLIENT 2 : Marc L. — Clarification, séance planifiée
-- ============================================================

INSERT INTO clients (id, public_client_code, first_name_or_alias, last_name, email, phone,
  language_code, timezone, territory_code, is_adult_confirmed,
  record_status, data_sensitivity_class, created_at, updated_at)
VALUES (
  'a2cafe02-test-0002-0002-000000000002',
  'CLI-MARC00002',
  'Marc', 'L.', 'marc.l.test@ivia.quebec', NULL,
  'fr-CA', 'America/Toronto', 'QC', true,
  'active', 'high',
  '2026-04-28 14:00:00+00', '2026-04-28 14:00:00+00'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO intake_requests (id, client_id, request_channel_code, request_for_code,
  primary_need_code, perceived_urgency_code, support_already_in_place,
  requested_outcome_text, entry_summary_text, referential_version,
  record_status, created_at, updated_at)
VALUES (
  'b2cafe02-test-0002-0002-000000000002',
  'a2cafe02-test-0002-0002-000000000002',
  'web_form', 'self', 'clarification', 'non_urgent', true,
  'Besoin d''y voir plus clair. Je veux juste qu''on m''explique mes options.',
  'Homme ~41 ans, consultant, soutien déjà en place (médecin de famille). Demande de clarification sur ses options — pas de détresse active. Première séance planifiée en vidéo.',
  'v1', 'active',
  '2026-04-28 14:00:00+00', '2026-04-28 14:00:00+00'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO consents (id, client_id, session_id, consent_type_code, consent_value,
  consent_version_code, granted_by_actor_code, granted_at, record_status, created_at, updated_at)
VALUES
  ('c2ca0101-test-0002-0002-000000000002', 'a2cafe02-test-0002-0002-000000000002', NULL,
   'consent_history', true, 'v1', 'client', '2026-04-28 14:05:00+00',
   'active', '2026-04-28 14:05:00+00', '2026-04-28 14:05:00+00'),
  ('c2ca0102-test-0002-0002-000000000002', 'a2cafe02-test-0002-0002-000000000002', NULL,
   'consent_session_note', true, 'v1', 'client', '2026-04-28 14:05:00+00',
   'active', '2026-04-28 14:05:00+00', '2026-04-28 14:05:00+00'),
  ('c2ca0103-test-0002-0002-000000000002', 'a2cafe02-test-0002-0002-000000000002', NULL,
   'consent_recording', true, 'v1', 'client', '2026-04-28 14:05:00+00',
   'active', '2026-04-28 14:05:00+00', '2026-04-28 14:05:00+00')
ON CONFLICT (id) DO NOTHING;

INSERT INTO sessions (id, client_id, intake_request_id, session_sequence_number,
  session_mode_code, session_channel_code,
  scheduled_start_at, actual_start_at, actual_end_at, duration_minutes,
  operator_user_id, session_status_code, record_status,
  data_sensitivity_class, retention_class, created_at, updated_at)
VALUES (
  's2cafe01-test-0002-0002-000000000002',
  'a2cafe02-test-0002-0002-000000000002',
  'b2cafe02-test-0002-0002-000000000002',
  1, 'standard', 'direct',
  '2026-05-05 15:00:00+00', NULL, NULL, NULL,
  '8dab08e6-27af-4195-a05a-ccc4ac1f2eac',
  'scheduled', 'active', 'high', 'standard',
  '2026-04-28 14:10:00+00', '2026-04-28 14:10:00+00'
) ON CONFLICT (id) DO NOTHING;


-- ============================================================
-- CLIENT 3 : Lucie B. — Proche inquiet, vigilance priorité
-- ============================================================

INSERT INTO clients (id, public_client_code, first_name_or_alias, last_name, email, phone,
  language_code, timezone, territory_code, is_adult_confirmed,
  record_status, data_sensitivity_class, created_at, updated_at)
VALUES (
  'a3cafe03-test-0003-0003-000000000003',
  'CLI-LUCIE0003',
  'Lucie', 'B.', NULL, '+15141230001',
  'fr-CA', 'America/Toronto', 'QC', true,
  'active', 'restricted',
  '2026-04-22 16:00:00+00', '2026-04-25 11:00:00+00'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO intake_requests (id, client_id, request_channel_code, request_for_code,
  primary_need_code, perceived_urgency_code, support_already_in_place,
  requested_outcome_text, entry_summary_text, referential_version,
  record_status, created_at, updated_at)
VALUES (
  'b3cafe03-test-0003-0003-000000000003',
  'a3cafe03-test-0003-0003-000000000003',
  'direct', 'relative', 'distress', 'priority', false,
  NULL,
  'Mère (Lucie) appelle pour son fils 22 ans — retrait social, changements comportementaux depuis 6 mois. Aucun danger immédiat rapporté. Fils non présent à l''appel. Dossier ouvert au nom de Lucie pour suivi parent-inquiet. Niveau priorité par prudence.',
  'v1', 'active',
  '2026-04-22 16:00:00+00', '2026-04-22 16:00:00+00'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO consents (id, client_id, session_id, consent_type_code, consent_value,
  consent_version_code, granted_by_actor_code, granted_at, record_status, created_at, updated_at)
VALUES
  ('c3ca0101-test-0003-0003-000000000003', 'a3cafe03-test-0003-0003-000000000003', NULL,
   'consent_session', true, 'v1', 'operator', '2026-04-22 16:05:00+00',
   'active', '2026-04-22 16:05:00+00', '2026-04-22 16:05:00+00'),
  ('c3ca0102-test-0003-0003-000000000003', 'a3cafe03-test-0003-0003-000000000003', NULL,
   'consent_session_note', true, 'v1', 'operator', '2026-04-22 16:05:00+00',
   'active', '2026-04-22 16:05:00+00', '2026-04-22 16:05:00+00')
ON CONFLICT (id) DO NOTHING;

INSERT INTO sessions (id, client_id, intake_request_id, session_sequence_number,
  session_mode_code, session_channel_code,
  scheduled_start_at, actual_start_at, actual_end_at, duration_minutes,
  operator_user_id, session_status_code, record_status,
  data_sensitivity_class, retention_class, created_at, updated_at)
VALUES (
  's3cafe01-test-0003-0003-000000000003',
  'a3cafe03-test-0003-0003-000000000003',
  'b3cafe03-test-0003-0003-000000000003',
  1, 'standard', 'direct',
  '2026-04-25 10:00:00+00', '2026-04-25 10:02:00+00', '2026-04-25 11:02:00+00', 60,
  '8dab08e6-27af-4195-a05a-ccc4ac1f2eac',
  'completed', 'active', 'restricted', 'extended',
  '2026-04-22 16:10:00+00', '2026-04-25 11:05:00+00'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO session_notes (id, session_id, client_id, note_sequence_number,
  summary_text, observations_text, follow_up_actions_text,
  vigilance_level_code, next_step_type_code,
  validated_by_practitioner, client_visible, record_status,
  data_sensitivity_class, retention_class, created_at, updated_at)
VALUES (
  'n3cafe01-test-0003-0003-000000000003',
  's3cafe01-test-0003-0003-000000000003',
  'a3cafe03-test-0003-0003-000000000003',
  1,
  'Séance avec Lucie (mère). Fils non présent. Décrit retrait social progressif, refus de sortir, changement de rythme de sommeil, communication réduite. Lucie épuisée, culpabilité importante. Pas de danger immédiat.',
  'Lucie pleure en décrivant son fils. Se sent seule dans cette situation. Mari peu impliqué selon elle.',
  'Informer Lucie des ressources pour la famille (ACSM, ligne parents). Prochaine séance : évaluer si fils accepterait un contact direct.',
  'priority', 'orient_to_appropriate_service',
  true, false, 'active', 'restricted', 'extended',
  '2026-04-25 11:08:00+00', '2026-04-25 11:25:00+00'
) ON CONFLICT (id) DO NOTHING;


-- ============================================================
-- CLIENT 4 : André K. — Demande d'orientatif/alternatif, vidéo
-- ============================================================

INSERT INTO clients (id, public_client_code, first_name_or_alias, last_name, email, phone,
  language_code, timezone, territory_code, is_adult_confirmed,
  record_status, data_sensitivity_class, created_at, updated_at)
VALUES (
  'a4cafe04-test-0004-0004-000000000004',
  'CLI-ANDRE0004',
  'André', 'K.', 'andre.k.test@ivia.quebec', NULL,
  'fr-CA', 'America/Toronto', 'QC', true,
  'active', 'high',
  '2026-04-25 09:00:00+00', '2026-04-28 12:00:00+00'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO intake_requests (id, client_id, request_channel_code, request_for_code,
  primary_need_code, perceived_urgency_code, support_already_in_place,
  requested_outcome_text, entry_summary_text, referential_version,
  record_status, created_at, updated_at)
VALUES (
  'b4cafe04-test-0004-0004-000000000004',
  'a4cafe04-test-0004-0004-000000000004',
  'web_form', 'self', 'orientation', 'non_urgent', true,
  'J''ai déjà un psy mais je cherche quelque chose de différent. Pas sûr de ce que IVIA offre exactement.',
  'Homme ~48 ans, suivi psychologique actif mais insatisfait. Cherche un espace complémentaire moins clinique. Curieux de l''approche MERLIN. Première séance vidéo complétée.',
  'v1', 'active',
  '2026-04-25 09:00:00+00', '2026-04-25 09:00:00+00'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO consents (id, client_id, session_id, consent_type_code, consent_value,
  consent_version_code, granted_by_actor_code, granted_at, record_status, created_at, updated_at)
VALUES
  ('c4ca0101-test-0004-0004-000000000004', 'a4cafe04-test-0004-0004-000000000004', NULL,
   'consent_history', true, 'v1', 'client', '2026-04-25 09:05:00+00',
   'active', '2026-04-25 09:05:00+00', '2026-04-25 09:05:00+00'),
  ('c4ca0102-test-0004-0004-000000000004', 'a4cafe04-test-0004-0004-000000000004', NULL,
   'consent_session_note', true, 'v1', 'client', '2026-04-25 09:05:00+00',
   'active', '2026-04-25 09:05:00+00', '2026-04-25 09:05:00+00'),
  ('c4ca0103-test-0004-0004-000000000004', 'a4cafe04-test-0004-0004-000000000004', NULL,
   'consent_recording', true, 'v1', 'client', '2026-04-25 09:05:00+00',
   'active', '2026-04-25 09:05:00+00', '2026-04-25 09:05:00+00'),
  ('c4ca0104-test-0004-0004-000000000004', 'a4cafe04-test-0004-0004-000000000004', NULL,
   'consent_transcription', true, 'v1', 'client', '2026-04-25 09:05:00+00',
   'active', '2026-04-25 09:05:00+00', '2026-04-25 09:05:00+00')
ON CONFLICT (id) DO NOTHING;

INSERT INTO sessions (id, client_id, intake_request_id, session_sequence_number,
  session_mode_code, session_channel_code,
  scheduled_start_at, actual_start_at, actual_end_at, duration_minutes,
  operator_user_id, session_status_code, record_status,
  data_sensitivity_class, retention_class, created_at, updated_at)
VALUES (
  's4cafe01-test-0004-0004-000000000004',
  'a4cafe04-test-0004-0004-000000000004',
  'b4cafe04-test-0004-0004-000000000004',
  1, 'standard', 'direct',
  '2026-04-28 11:00:00+00', '2026-04-28 11:02:00+00', '2026-04-28 12:02:00+00', 60,
  '8dab08e6-27af-4195-a05a-ccc4ac1f2eac',
  'completed', 'active', 'high', 'standard',
  '2026-04-25 09:10:00+00', '2026-04-28 12:05:00+00'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO session_notes (id, session_id, client_id, note_sequence_number,
  summary_text, observations_text, next_session_focus_text,
  esprit_summary_text,
  vigilance_level_code, next_step_type_code,
  validated_by_practitioner, client_visible, record_status,
  data_sensitivity_class, retention_class, created_at, updated_at)
VALUES (
  'n4cafe01-test-0004-0004-000000000004',
  's4cafe01-test-0004-0004-000000000004',
  'a4cafe04-test-0004-0004-000000000004',
  1,
  'Première séance André. Fonctionnel, articulé. Suivi psy actif depuis 2 ans — relation froide selon lui. Cherche espace plus humain, moins technique. A bien reçu la présentation de l''approche MERLIN.',
  'Intellectualise fortement. Questions précises sur la méthode. Méfiance saine — pas résistance.',
  'Explorer ce qu''il cherche que son psy actuel ne lui donne pas. L''approche CŒUR-CORPS-ESPRIT-ÊTRE à introduire.',
  'Fort ancrage cognitif. Ouvre timidement sur une dimension plus intuitive.',
  'non_urgent', 'clarify_major_point',
  true, false, 'active', 'high', 'standard',
  '2026-04-28 12:08:00+00', '2026-04-28 12:22:00+00'
) ON CONFLICT (id) DO NOTHING;


-- ============================================================
-- CLIENT 5 : Alex M. — Détresse, niveau watch, alias seulement
-- ============================================================

INSERT INTO clients (id, public_client_code, first_name_or_alias, last_name, email, phone,
  language_code, timezone, territory_code, is_adult_confirmed,
  record_status, data_sensitivity_class, created_at, updated_at)
VALUES (
  'a5cafe05-test-0005-0005-000000000005',
  'CLI-ALEX00005',
  'Alex', NULL, NULL, '+15140000009',
  'fr-CA', 'America/Toronto', 'QC', true,
  'active', 'restricted',
  '2026-04-30 08:00:00+00', '2026-04-30 09:00:00+00'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO intake_requests (id, client_id, request_channel_code, request_for_code,
  primary_need_code, perceived_urgency_code, support_already_in_place,
  requested_outcome_text, entry_summary_text, referential_version,
  record_status, created_at, updated_at)
VALUES (
  'b5cafe05-test-0005-0005-000000000005',
  'a5cafe05-test-0005-0005-000000000005',
  'direct', 'self', 'distress', 'watch', false,
  NULL,
  'Personne s''identifie «Alex», refuse de donner le nom de famille, téléphone seulement. Détresse émotionnelle diffuse, pleurs en début d''appel. Pas de danger immédiat identifié mais retrait social important. Niveau watch par précaution. Séance courte (30 min) pour établir le lien.',
  'v1', 'active',
  '2026-04-30 08:00:00+00', '2026-04-30 08:00:00+00'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO consents (id, client_id, session_id, consent_type_code, consent_value,
  consent_version_code, granted_by_actor_code, granted_at, record_status, created_at, updated_at)
VALUES
  ('c5ca0101-test-0005-0005-000000000005', 'a5cafe05-test-0005-0005-000000000005', NULL,
   'consent_session', true, 'v1', 'operator', '2026-04-30 08:05:00+00',
   'active', '2026-04-30 08:05:00+00', '2026-04-30 08:05:00+00'),
  ('c5ca0102-test-0005-0005-000000000005', 'a5cafe05-test-0005-0005-000000000005', NULL,
   'consent_recording', false, 'v1', 'client', '2026-04-30 08:05:00+00',
   'active', '2026-04-30 08:05:00+00', '2026-04-30 08:05:00+00')
ON CONFLICT (id) DO NOTHING;

INSERT INTO sessions (id, client_id, intake_request_id, session_sequence_number,
  session_mode_code, session_channel_code,
  scheduled_start_at, actual_start_at, actual_end_at, duration_minutes,
  operator_user_id, session_status_code, record_status,
  data_sensitivity_class, retention_class, created_at, updated_at)
VALUES (
  's5cafe01-test-0005-0005-000000000005',
  'a5cafe05-test-0005-0005-000000000005',
  'b5cafe05-test-0005-0005-000000000005',
  1, 'intake', 'direct',
  '2026-04-30 08:30:00+00', '2026-04-30 08:32:00+00', '2026-04-30 09:02:00+00', 30,
  '8dab08e6-27af-4195-a05a-ccc4ac1f2eac',
  'completed', 'active', 'restricted', 'extended',
  '2026-04-30 08:10:00+00', '2026-04-30 09:05:00+00'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO session_notes (id, session_id, client_id, note_sequence_number,
  summary_text, observations_text, follow_up_actions_text, next_session_focus_text,
  vigilance_level_code, next_step_type_code,
  validated_by_practitioner, client_visible, record_status,
  data_sensitivity_class, retention_class, created_at, updated_at)
VALUES (
  'n5cafe01-test-0005-0005-000000000005',
  's5cafe01-test-0005-0005-000000000005',
  'a5cafe05-test-0005-0005-000000000005',
  1,
  'Séance d''entrée 30 min. Alias «Alex». Refuse de donner son nom. Pleurs au début de l''appel, puis stabilisation progressive. Détresse diffuse liée à un isolement social important. Pas de danger identifié. Vit seul. Fin de séance : Alex demande à rappeler.',
  'N''exprime pas clairement ce qu''il veut — dit «je sais pas». Non-réponse au champ «résultat espéré» à noter : incapacité de projection vers l''avant, signe possible d''épuisement cognitif ou de shutdown émotionnel. A accepté de fixer une prochaine séance.',
  'Rappel dans 5 jours si pas de nouvelles. Numéro de crise transmis.',
  'Établir le lien et le nommer. Explorer ce que «aller mieux» veut dire pour Alex.',
  'watch', 'stabilize_rhythm_and_load',
  true, false, 'active', 'restricted', 'extended',
  '2026-04-30 09:08:00+00', '2026-04-30 09:22:00+00'
) ON CONFLICT (id) DO NOTHING;

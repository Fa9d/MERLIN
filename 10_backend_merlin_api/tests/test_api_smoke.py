import os
from pathlib import Path
from unittest.mock import AsyncMock

from fastapi.testclient import TestClient


def test_core_flow_smoke() -> None:
    tmp_db = Path("test_smoke_merlin.db").resolve()
    if tmp_db.exists():
        tmp_db.unlink()

    os.environ["MERLIN_DATABASE_URL"] = f"sqlite:///{tmp_db.as_posix()}"
    os.environ["MERLIN_AUTO_CREATE_TABLES"] = "true"
    os.environ["MERLIN_MEDIA_LIVEKIT_WS_URL"] = "wss://livekit.example.test"
    os.environ["MERLIN_MEDIA_LIVEKIT_API_KEY"] = "devkey"
    os.environ["MERLIN_MEDIA_LIVEKIT_API_SECRET"] = "devsecret-devsecret-devsecret-2026"
    os.environ["MERLIN_MEDIA_RECORDING_STRATEGY"] = "metadata_only"

    from app.main import app
    from app.api.routes import audio_recordings as audio_recordings_routes
    from app.api.routes import sessions as sessions_routes

    with TestClient(app) as client:
        original_start_provider_recording = audio_recordings_routes._start_provider_recording
        original_stop_provider_recording = audio_recordings_routes._stop_provider_recording
        original_generate_session_note = sessions_routes.generate_session_note_from_transcript
        original_create_livekit_room_for_session = sessions_routes.create_livekit_room_for_session
        audio_recordings_routes._start_provider_recording = AsyncMock(
            return_value=(None, "pending://audio-recordings/test-recording")
        )
        audio_recordings_routes._stop_provider_recording = AsyncMock(
            return_value="file://audio-recordings/test-recording.ogg"
        )
        sessions_routes.generate_session_note_from_transcript = AsyncMock(
            return_value={
                "production_note": {
                    "summary_text": "Lecture structuree de la seance.",
                    "observations_text": "Le recit montre une charge soutenue avec peu de repit.",
                    "coeur_summary_text": "Sentiment d'epuisement et de solitude.",
                    "corps_summary_text": "Sommeil perturbe et fatigue persistante.",
                    "esprit_summary_text": "Difficulte a prioriser et a se projeter.",
                    "etre_summary_text": "Perte de reperes dans le rythme de vie actuel.",
                    "immediate_context_text": "Contexte familial et charge mentale eleves.",
                    "context_factors_json": [
                        {
                            "factor_family_code": "travail_ou_charge",
                            "impact_direction_code": "contrainte",
                            "summary_text": "Charge quotidienne importante.",
                        }
                    ],
                    "context_hypotheses_json": [
                        {
                            "hypothesis_code": "pression_silence_et_minimisation",
                            "summary_text": "Le recit minimise une charge presente depuis longtemps.",
                            "matched_signals": [
                                "minimisation_verbale",
                                "consultation_tardive",
                            ],
                            "primary_dimension": "coeur",
                            "confidence_code": "moyen",
                        },
                        {
                            "hypothesis_code": "pression_performance_travail",
                            "summary_text": "La fatigue semble integree comme normale et reliee a la performance.",
                            "matched_signals": [
                                "burnout_normalise",
                                "honte_du_repos",
                            ],
                            "primary_dimension": "esprit",
                            "confidence_code": "moyen",
                        },
                    ],
                    "identified_tensions_json": [
                        {
                            "tension_code": "tension_charge_exigences",
                            "description": "Accumulation de demandes et peu de marge.",
                            "dimensions_impactees": ["corps", "esprit"],
                            "intensite_presumee": "moderee",
                            "niveau_de_confiance": "moyen",
                        }
                    ],
                    "vigilance_level_code": "watch",
                    "vigilance_summary_text": "Situation a surveiller sans urgence immediate.",
                    "next_step_type_code": "propose_follow_up",
                    "follow_up_actions_text": "Proposer un suivi dans une semaine.",
                    "next_session_focus_text": "Clarifier les declencheurs et le rythme.",
                },
                "client_delivery": {
                    "client_visible_recommended": True,
                    "client_facing_summary_text": "Vous repartez avec une situation mieux nommee et une prochaine etape concrete.",
                },
                "supervision": {
                    "supervision_summary_text": "Garder une vigilance sur l'epuisement et l'isolement.",
                    "detected_context_signals": [
                        "minimisation_verbale",
                        "consultation_tardive",
                        "burnout_normalise",
                    ],
                    "low_confidence_flags": [],
                    "excluded_from_client_delivery": ["hypotheses implicites"],
                },
                "research": {
                    "research_notes_text": None,
                    "experimental_hypotheses": [],
                },
                "metadata": {
                    "model_used": "claude-sonnet-4-20250514",
                    "prompt_version": "session_note_cercle_v1",
                    "complexity_score": None,
                    "validated_by_practitioner": False,
                    "practitioner_corrections": None,
                },
            }
        )
        sessions_routes.create_livekit_room_for_session = AsyncMock(
            return_value={
                "room_name": "merlin-session-test-room",
                "room_sid": "RM_test_room_sid",
                "livekit_url": "wss://livekit.example.test",
                "practitioner_identity": "practitioner-test",
                "practitioner_token": "jwt-practitioner-test-token",
                "client_identity": "client-test",
                "client_token": "jwt-client-test-token",
            }
        )
        try:
            bootstrap_resp = client.post(
            "/api/v1/auth/register",
            json={
                "email": "admin@example.com",
                "password": "admin-secret",
                "display_name": "Admin",
                "role": "admin_tech",
            },
        )
            assert bootstrap_resp.status_code == 201

            login_resp = client.post(
            "/api/v1/auth/login",
            json={
                "email": "admin@example.com",
                "password": "admin-secret",
            },
        )
            assert login_resp.status_code == 200
            login_payload = login_resp.json()
            admin_headers = {
                "Authorization": f"Bearer {login_payload['access_token']}",
            }

            operator_register_resp = client.post(
                "/api/v1/auth/register",
                json={
                    "email": "operator@example.com",
                    "password": "operator-secret",
                    "display_name": "Operator",
                    "role": "operator",
                },
                headers=admin_headers,
            )
            assert operator_register_resp.status_code == 201

            operator_login_resp = client.post(
                "/api/v1/auth/login",
                json={
                    "email": "operator@example.com",
                    "password": "operator-secret",
                },
            )
            assert operator_login_resp.status_code == 200
            operator_login_payload = operator_login_resp.json()
            auth_headers = {
                "Authorization": f"Bearer {operator_login_payload['access_token']}",
            }

            client_resp = client.post(
            "/api/v1/clients",
            json={
                "first_name_or_alias": "Alice",
                "email": "alice@example.com",
                "is_adult_confirmed": True,
            },
        )
            assert client_resp.status_code == 201
            client_id = client_resp.json()["id"]

            public_consent_resp = client.post(
            "/api/v1/consents",
            json={
                "client_id": client_id,
                "consent_type_code": "consent_session",
                "consent_value": True,
                "granted_by_actor_code": "client",
            },
        )
            assert public_consent_resp.status_code == 201
            assert public_consent_resp.json()["consent_type_code"] == "consent_session"

            public_recording_resp = client.post(
            "/api/v1/consents",
            json={
                "client_id": client_id,
                "consent_type_code": "consent_recording",
                "consent_value": True,
                "granted_by_actor_code": "client",
            },
        )
            assert public_recording_resp.status_code == 401

            intake_resp = client.post(
            "/api/v1/intake-requests",
            json={
                "client_id": client_id,
                "request_channel_code": "web_form",
                "request_for_code": "self",
                "primary_need_code": "support",
                "perceived_urgency_code": "non_urgent",
                "support_already_in_place": False,
            },
        )
            assert intake_resp.status_code == 201
            intake_id = intake_resp.json()["id"]

            list_intake_requests_resp = client.get(
            f"/api/v1/intake-requests?client_id={client_id}",
            headers=auth_headers,
        )
            assert list_intake_requests_resp.status_code == 200
            assert list_intake_requests_resp.json()[0]["id"] == intake_id

            session_resp = client.post(
            "/api/v1/sessions",
            json={
                "client_id": client_id,
                "intake_request_id": intake_id,
                "session_mode_code": "intake",
                "session_channel_code": "phone",
                "session_status_code": "scheduled",
            },
            headers=auth_headers,
        )
            assert session_resp.status_code == 201
            first_session = session_resp.json()
            session_id = first_session["id"]
            assert first_session["session_sequence_number"] == 1
            assert first_session["operator_user_id"] == operator_login_payload["user"]["id"]

            second_session_resp = client.post(
            "/api/v1/sessions",
            json={
                "client_id": client_id,
                "session_mode_code": "follow_up",
                "session_channel_code": "video",
                "session_status_code": "scheduled",
            },
            headers=auth_headers,
        )
            assert second_session_resp.status_code == 201
            second_session = second_session_resp.json()
            assert second_session["session_sequence_number"] == 2

            room_resp = client.post(
                f"/api/v1/sessions/{second_session['id']}/room",
                headers=auth_headers,
            )
            assert room_resp.status_code == 200
            room_payload = room_resp.json()
            assert room_payload["room_name"] == "merlin-session-test-room"
            assert room_payload["room_sid"] == "RM_test_room_sid"
            assert room_payload["livekit_url"] == "wss://livekit.example.test"
            assert room_payload["practitioner_token"] == "jwt-practitioner-test-token"
            assert room_payload["client_token"] == "jwt-client-test-token"

            start_session_resp = client.post(
            f"/api/v1/sessions/{second_session['id']}/start",
            json={
                "actual_start_at": "2026-04-21T13:00:00Z",
            },
            headers=auth_headers,
        )
            audio_provision_resp = client.post(
            f"/api/v1/audio-sessions/sessions/{second_session['id']}/provision",
            json={},
            headers=auth_headers,
        )
            assert audio_provision_resp.status_code == 201
            assert audio_provision_resp.json()["audio_session_status_code"] == "active"

            assert start_session_resp.status_code == 200
            assert start_session_resp.json()["session_status_code"] == "in_progress"

            audio_list_resp = client.get(
            f"/api/v1/audio-sessions?session_id={second_session['id']}",
            headers=auth_headers,
        )
            assert audio_list_resp.status_code == 200
            assert len(audio_list_resp.json()) == 1

            join_resp = client.post(
            f"/api/v1/audio-sessions/{audio_provision_resp.json()['id']}/operator-join",
            headers=auth_headers,
        )
            assert join_resp.status_code == 200
            assert join_resp.json()["ws_url"] == "wss://livekit.example.test"
            assert isinstance(join_resp.json()["token"], str)
            assert len(join_resp.json()["token"]) > 20

            client_join_resp = client.post(
            f"/api/v1/audio-sessions/{audio_provision_resp.json()['id']}/client-join",
            headers=auth_headers,
        )
            assert client_join_resp.status_code == 200
            assert client_join_resp.json()["ws_url"] == "wss://livekit.example.test"
            assert client_join_resp.json()["participant_identity"].startswith("client-")
            assert isinstance(client_join_resp.json()["token"], str)
            assert len(client_join_resp.json()["token"]) > 20

            recording_start_resp = client.post(
                f"/api/v1/audio-recordings/audio-sessions/{audio_provision_resp.json()['id']}/start",
                headers=auth_headers,
            )
            assert recording_start_resp.status_code == 201
            assert recording_start_resp.json()["audio_recording_status_code"] == "recording"

            recording_list_resp = client.get(
                f"/api/v1/audio-recordings?audio_session_id={audio_provision_resp.json()['id']}",
                headers=auth_headers,
            )
            assert recording_list_resp.status_code == 200
            assert len(recording_list_resp.json()) == 1

            recording_stop_resp = client.post(
                f"/api/v1/audio-recordings/{recording_start_resp.json()['id']}/stop",
                headers=auth_headers,
            )
            assert recording_stop_resp.status_code == 200
            assert recording_stop_resp.json()["audio_recording_status_code"] == "ready"

            close_session_resp = client.post(
            f"/api/v1/sessions/{second_session['id']}/close",
            json={
                "actual_end_at": "2026-04-21T13:50:00Z",
                "session_status_code": "completed",
                "presenting_topic_text": "Besoin de soutien",
                "session_highlights_text": "Le client a precise son contexte principal.",
                "operator_assessment_text": "Echange stable et coherent.",
                "vigilance_level_code": "watch",
                "transcript_text": "Je dors mal, je me sens depasse et je ne sais plus par ou commencer.",
                "follow_up_actions_text": "Proposer un suivi dans une semaine.",
                "next_session_focus_text": "Clarifier les declencheurs.",
                "client_visible": True,
            },
            headers=auth_headers,
        )
            assert close_session_resp.status_code == 200
            close_payload = close_session_resp.json()
            assert close_payload["session"]["session_status_code"] == "completed"
            assert close_payload["session"]["duration_minutes"] == 50
            assert close_payload["generated_note"]["note_sequence_number"] == 1
            assert close_payload["generated_note"]["summary_text"] == "Lecture structuree de la seance."
            assert close_payload["generated_note"]["coeur_summary_text"] == "Sentiment d'epuisement et de solitude."
            assert len(close_payload["generated_note"]["context_hypotheses_json"]) == 2
            assert (
                close_payload["generated_note"]["context_hypotheses_json"][0]["hypothesis_code"]
                == "pression_silence_et_minimisation"
            )
            assert close_payload["generated_note"]["vigilance_level_code"] == "watch"
            assert close_payload["generated_note"]["next_step_type_code"] == "propose_follow_up"
            assert close_payload["generated_note"]["client_visible"] is True
            assert (
                close_payload["generated_note"]["client_facing_summary_text"]
                == "Vous repartez avec une situation mieux nommee et une prochaine etape concrete."
            )
            assert close_payload["generated_note"]["model_used"] == "claude-sonnet-4-20250514"
            assert close_payload["generated_note"]["prompt_version"] == "session_note_cercle_v1"
            assert close_payload["generated_note"]["complexity_score"] is None
            assert close_payload["generated_note"]["validated_by_practitioner"] is False
            assert close_payload["generated_note"]["validated_at"] is None
            assert close_payload["generated_note"]["practitioner_corrections"] is None
            assert close_payload["generated_document"]["document_kind_code"] == "session_summary"
            assert close_payload["generated_document"]["audience_code"] == "client"
            assert close_payload["generated_document"]["client_visible"] is True
            assert "Vous repartez avec une situation mieux nommee" in close_payload["generated_document"]["body_text"]

            list_derived_documents_resp = client.get(
            f"/api/v1/derived-documents?session_id={second_session['id']}",
            headers=auth_headers,
        )
            assert list_derived_documents_resp.status_code == 200
            assert len(list_derived_documents_resp.json()) == 1
            assert list_derived_documents_resp.json()[0]["source_note_id"] == close_payload["generated_note"]["id"]

            validate_note_resp = client.patch(
                f"/api/v1/session-notes/{close_payload['generated_note']['id']}/validate",
                json={
                    "validated": True,
                    "corrections": None,
                },
                headers=auth_headers,
            )
            assert validate_note_resp.status_code == 200
            validated_note = validate_note_resp.json()
            assert validated_note["validated_by_practitioner"] is True
            assert validated_note["validated_at"] is not None
            assert validated_note["practitioner_corrections"] is None

            correct_note_resp = client.patch(
                f"/api/v1/session-notes/{close_payload['generated_note']['id']}/validate",
                json={
                    "validated": True,
                    "corrections": {
                        "coeur": "Charge affective plus marquee que formulee.",
                        "vigilance": "watch",
                        "next_step": "Proposer un suivi de regulation.",
                    },
                },
                headers=auth_headers,
            )
            assert correct_note_resp.status_code == 200
            corrected_note = correct_note_resp.json()
            assert corrected_note["validated_by_practitioner"] is True
            assert corrected_note["practitioner_corrections"]["coeur"] == (
                "Charge affective plus marquee que formulee."
            )

            reject_note_resp = client.patch(
                f"/api/v1/session-notes/{close_payload['generated_note']['id']}/validate",
                json={
                    "validated": False,
                    "corrections": {
                        "tensions": ["tension_charge_exigences"],
                    },
                },
                headers=auth_headers,
            )
            assert reject_note_resp.status_code == 200
            rejected_note = reject_note_resp.json()
            assert rejected_note["validated_by_practitioner"] is False
            assert rejected_note["validated_at"] is not None
            assert rejected_note["practitioner_corrections"]["tensions"] == [
                "tension_charge_exigences"
            ]

            closed_audio_list_resp = client.get(
            f"/api/v1/audio-sessions?session_id={second_session['id']}",
            headers=auth_headers,
        )
            assert closed_audio_list_resp.status_code == 200
            assert closed_audio_list_resp.json()[0]["audio_session_status_code"] == "closed"

            consent_resp = client.post(
            "/api/v1/consents",
            json={
                "client_id": client_id,
                "session_id": session_id,
                "consent_type_code": "consent_session",
                "consent_value": True,
                "granted_by_actor_code": "client",
            },
            headers=auth_headers,
        )
            assert consent_resp.status_code == 201

            list_consents_resp = client.get(
            f"/api/v1/consents?client_id={client_id}",
            headers=auth_headers,
        )
            assert list_consents_resp.status_code == 200
            assert len(list_consents_resp.json()) >= 2

            get_client_resp = client.get(f"/api/v1/clients/{client_id}", headers=auth_headers)
            assert get_client_resp.status_code == 200

            list_sessions_resp = client.get("/api/v1/sessions", headers=auth_headers)
            assert list_sessions_resp.status_code == 200
            assert len(list_sessions_resp.json()) == 2

            session_note_resp = client.post(
            "/api/v1/session-notes",
            json={
                "session_id": session_id,
                "client_id": client_id,
                "summary_text": "Premier resume operateur.",
                "observations_text": "Client coherent et engage.",
                "follow_up_actions_text": "Planifier un suivi.",
            },
            headers=auth_headers,
        )
            assert session_note_resp.status_code == 201
            assert session_note_resp.json()["note_sequence_number"] == 1

            list_session_notes_resp = client.get(
            f"/api/v1/session-notes?session_id={session_id}",
            headers=auth_headers,
        )
            assert list_session_notes_resp.status_code == 200
            assert len(list_session_notes_resp.json()) == 1

            health_resp = client.get("/health")
            assert health_resp.status_code == 200
            assert health_resp.json()["status"] == "ok"
        finally:
            audio_recordings_routes._start_provider_recording = original_start_provider_recording
            audio_recordings_routes._stop_provider_recording = original_stop_provider_recording
            sessions_routes.generate_session_note_from_transcript = original_generate_session_note
            sessions_routes.create_livekit_room_for_session = original_create_livekit_room_for_session

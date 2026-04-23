"use client";

import { useEffect, useRef, useState } from "react";
import { Room, RoomEvent, Track } from "livekit-client";

import {
  createOperatorJoinContext,
  type AudioSessionJoinRecord,
  type AudioSessionRecord,
} from "@/lib/merlin-api";

type OperatorLiveKitPanelProps = {
  audioSession: AudioSessionRecord | null;
  operatorAccessToken: string;
};

export function OperatorLiveKitPanel({
  audioSession,
  operatorAccessToken,
}: OperatorLiveKitPanelProps) {
  const roomRef = useRef<Room | null>(null);
  const remoteAudioContainerRef = useRef<HTMLDivElement | null>(null);
  const [joinContext, setJoinContext] = useState<AudioSessionJoinRecord | null>(null);
  const [connectionState, setConnectionState] = useState("disconnected");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isConnecting, setIsConnecting] = useState(false);

  useEffect(() => {
    const audioContainer = remoteAudioContainerRef.current;
    return () => {
      if (roomRef.current) {
        roomRef.current.disconnect();
        roomRef.current = null;
      }
      if (audioContainer) {
        audioContainer.replaceChildren();
      }
    };
  }, []);

  async function handleConnect() {
    if (!audioSession) {
      return;
    }

    setIsConnecting(true);
    setErrorMessage(null);

    try {
      const nextJoinContext = await createOperatorJoinContext(
        audioSession.id,
        operatorAccessToken,
      );
      const room = new Room();

      room.on(RoomEvent.ConnectionStateChanged, (state) => {
        setConnectionState(state);
      });

      room.on(RoomEvent.TrackSubscribed, (track) => {
        if (track.kind !== Track.Kind.Audio) {
          return;
        }
        const element = track.attach();
        element.autoplay = true;
        if (remoteAudioContainerRef.current) {
          remoteAudioContainerRef.current.appendChild(element);
        }
      });

      room.on(RoomEvent.TrackUnsubscribed, (track) => {
        if (track.kind !== Track.Kind.Audio) {
          return;
        }
        track.detach().forEach((element) => element.remove());
      });

      await room.connect(nextJoinContext.ws_url, nextJoinContext.token);
      await room.startAudio();
      await room.localParticipant.setMicrophoneEnabled(true);

      roomRef.current = room;
      setJoinContext(nextJoinContext);
      setConnectionState("connected");
    } catch (error) {
      if (roomRef.current) {
        roomRef.current.disconnect();
        roomRef.current = null;
      }
      setErrorMessage(
        error instanceof Error ? error.message : "Impossible de rejoindre la salle LiveKit.",
      );
      setConnectionState("disconnected");
    } finally {
      setIsConnecting(false);
    }
  }

  function handleDisconnect() {
    if (roomRef.current) {
      roomRef.current.disconnect();
      roomRef.current = null;
    }
    if (remoteAudioContainerRef.current) {
      remoteAudioContainerRef.current.replaceChildren();
    }
    setConnectionState("disconnected");
  }

  if (!audioSession) {
    return <p className="inline-note">Aucune salle audio selectionnee.</p>;
  }

  return (
    <div className="stack-md">
      <div className="info-strip">
        <span className="mono">{audioSession.room_name}</span>
        <span>{audioSession.audio_session_status_code}</span>
        <span>{connectionState}</span>
      </div>

      {joinContext ? (
        <p className="inline-note">
          Participant operateur: <span className="mono">{joinContext.participant_identity}</span>
        </p>
      ) : null}

      {errorMessage ? <p className="message message-error">{errorMessage}</p> : null}

      <div className="cta-row">
        <button
          className="button button-primary"
          disabled={isConnecting || !audioSession.provider_room_url || connectionState === "connected"}
          onClick={handleConnect}
          type="button"
        >
          {isConnecting ? "Connexion..." : "Rejoindre la salle"}
        </button>
        <button
          className="button button-secondary"
          disabled={connectionState !== "connected"}
          onClick={handleDisconnect}
          type="button"
        >
          Quitter la salle
        </button>
      </div>

      <div className="audio-stage" ref={remoteAudioContainerRef} />
    </div>
  );
}

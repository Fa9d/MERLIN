"use client";

import { useEffect, useRef, useState } from "react";
import { Room, RoomEvent, Track } from "livekit-client";

import {
  createClientJoinContext,
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
  const [clientJoinUrl, setClientJoinUrl] = useState<string | null>(null);
  const [connectionState, setConnectionState] = useState("disconnected");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isConnecting, setIsConnecting] = useState(false);
  const [isGeneratingClientLink, setIsGeneratingClientLink] = useState(false);
  const [isPromptOpen, setIsPromptOpen] = useState(false);
  const [isRequestingMicrophone, setIsRequestingMicrophone] = useState(false);
  const [clientLinkMessage, setClientLinkMessage] = useState<string | null>(null);

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

  useEffect(() => {
    setJoinContext(null);
    setClientJoinUrl(null);
    setClientLinkMessage(null);
    setConnectionState("disconnected");
    setErrorMessage(null);
  }, [audioSession?.id]);

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

  async function handleGenerateClientLink() {
    if (!audioSession || typeof window === "undefined") {
      return;
    }

    setIsGeneratingClientLink(true);
    setErrorMessage(null);
    setClientLinkMessage(null);

    try {
      const clientJoinContext = await createClientJoinContext(
        audioSession.id,
        operatorAccessToken,
      );
      const nextClientJoinUrl = new URL("/audio-room", window.location.origin);
      nextClientJoinUrl.searchParams.set("wsUrl", clientJoinContext.ws_url);
      nextClientJoinUrl.searchParams.set("token", clientJoinContext.token);
      nextClientJoinUrl.searchParams.set("roomName", clientJoinContext.room_name);
      nextClientJoinUrl.searchParams.set("identity", clientJoinContext.participant_identity);
      nextClientJoinUrl.searchParams.set("role", "client");
      setClientJoinUrl(nextClientJoinUrl.toString());
      setClientLinkMessage("Lien client genere. Il peut maintenant rejoindre la salle.");
    } catch (error) {
      setErrorMessage(
        error instanceof Error ? error.message : "Impossible de generer le lien client.",
      );
    } finally {
      setIsGeneratingClientLink(false);
    }
  }

  async function handleCopyClientLink() {
    if (!clientJoinUrl || !navigator.clipboard) {
      return;
    }

    try {
      await navigator.clipboard.writeText(clientJoinUrl);
      setClientLinkMessage("Lien client copie dans le presse-papiers.");
    } catch {
      setClientLinkMessage("Copie automatique impossible. Copie le lien manuellement.");
    }
  }

  function handleOpenMicrophonePrompt() {
    setErrorMessage(null);
    setIsPromptOpen(true);
  }

  async function handleAuthorizeMicrophone() {
    if (!navigator.mediaDevices?.getUserMedia) {
      setErrorMessage("Ce navigateur ne permet pas l'autorisation micro requise.");
      setIsPromptOpen(false);
      return;
    }

    setIsRequestingMicrophone(true);
    setErrorMessage(null);

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      stream.getTracks().forEach((track) => track.stop());
      setIsPromptOpen(false);
      await handleConnect();
    } catch (error) {
      setErrorMessage(
        error instanceof Error
          ? error.message
          : "Le navigateur a refuse l'acces au micro.",
      );
    } finally {
      setIsRequestingMicrophone(false);
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

      {clientJoinUrl ? (
        <div className="stack-sm">
          <p className="inline-note">
            Lien client: <span className="mono">{clientJoinUrl}</span>
          </p>
          <div className="cta-row">
            <button
              className="button button-secondary"
              onClick={handleCopyClientLink}
              type="button"
            >
              Copier le lien client
            </button>
            <a
              className="button button-secondary"
              href={clientJoinUrl}
              rel="noreferrer"
              target="_blank"
            >
              Ouvrir le lien client
            </a>
          </div>
        </div>
      ) : null}

      {clientLinkMessage ? <p className="message message-success">{clientLinkMessage}</p> : null}

      {errorMessage ? <p className="message message-error">{errorMessage}</p> : null}

      <div className="cta-row">
        <button
          className="button button-secondary"
          disabled={isGeneratingClientLink || !audioSession.provider_room_url}
          onClick={handleGenerateClientLink}
          type="button"
        >
          {isGeneratingClientLink ? "Generation..." : "Generer le lien client"}
        </button>
        <button
          className="button button-primary"
          disabled={isConnecting || !audioSession.provider_room_url || connectionState === "connected"}
          onClick={handleOpenMicrophonePrompt}
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

      {isPromptOpen ? (
        <div className="permission-modal-backdrop" role="presentation">
          <div
            aria-describedby="operator-microphone-modal-description"
            aria-labelledby="operator-microphone-modal-title"
            aria-modal="true"
            className="permission-modal"
            role="dialog"
          >
            <h3 id="operator-microphone-modal-title">Autoriser le micro</h3>
            <p
              className="inline-note"
              id="operator-microphone-modal-description"
            >
              Pour rejoindre la salle, IVIA doit demander l'acces au micro dans le navigateur.
            </p>
            <div className="permission-modal-actions">
              <button
                className="button button-primary"
                disabled={isRequestingMicrophone}
                onClick={handleAuthorizeMicrophone}
                type="button"
              >
                {isRequestingMicrophone ? "Demande en cours..." : "Autoriser le micro"}
              </button>
              <button
                className="button button-secondary"
                disabled={isRequestingMicrophone}
                onClick={() => setIsPromptOpen(false)}
                type="button"
              >
                Annuler
              </button>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
}

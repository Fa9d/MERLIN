"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { Room, RoomEvent, Track } from "livekit-client";

export function AudioTestRoom() {
  const searchParams = useSearchParams();
  const roomRef = useRef<Room | null>(null);
  const remoteAudioContainerRef = useRef<HTMLDivElement | null>(null);
  const [connectionState, setConnectionState] = useState("disconnected");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isConnecting, setIsConnecting] = useState(false);
  const [isPromptOpen, setIsPromptOpen] = useState(false);
  const [isRequestingMicrophone, setIsRequestingMicrophone] = useState(false);

  const wsUrl = searchParams.get("wsUrl");
  const token = searchParams.get("token");
  const roomName = searchParams.get("roomName");
  const identity = searchParams.get("identity");
  const role = searchParams.get("role") ?? "client";

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
    if (!wsUrl || !token) {
      setErrorMessage("Le lien de salle audio est incomplet.");
      return;
    }

    setIsConnecting(true);
    setErrorMessage(null);

    try {
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

      await room.connect(wsUrl, token);
      await room.startAudio();
      await room.localParticipant.setMicrophoneEnabled(true);

      roomRef.current = room;
      setConnectionState("connected");
    } catch (error) {
      if (roomRef.current) {
        roomRef.current.disconnect();
        roomRef.current = null;
      }
      setErrorMessage(
        error instanceof Error ? error.message : "Impossible de rejoindre la salle audio.",
      );
      setConnectionState("disconnected");
    } finally {
      setIsConnecting(false);
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

  return (
    <div className="page-shell">
      <header className="topbar">
        <div className="wordmark">IVIA / Salle audio</div>
        <nav className="nav">
          <Link href="/">Accueil</Link>
          <Link href="/operator">Operateur</Link>
        </nav>
      </header>

      <main className="section">
        <div className="section-header">
          <div className="eyebrow">SALLE AUDIO</div>
          <h2>Connexion a la seance</h2>
          <p>
            Rejoins la salle audio securisee envoyee par ton praticien et autorise le micro pour
            demarrer l&apos;echange.
          </p>
        </div>

        <div className="grid operator-layout">
          <article className="card">
            <h3>Contexte</h3>
            <div className="stack-md">
              <div className="info-strip">
                <span>{role}</span>
                <span>{connectionState}</span>
              </div>
              <p className="inline-note">
                Salle: <span className="mono">{roomName ?? "absente"}</span>
              </p>
              <p className="inline-note">
                Identite: <span className="mono">{identity ?? "absente"}</span>
              </p>
              <p className="inline-note">
                Media: <span className="mono">{wsUrl ?? "absent"}</span>
              </p>
              <p className="inline-note">
                Autorise l&apos;acces micro dans le navigateur pour publier ta voix dans la salle.
              </p>
              {errorMessage ? <p className="message message-error">{errorMessage}</p> : null}
              <div className="cta-row">
                <button
                  className="button button-primary"
                  disabled={isConnecting || !wsUrl || !token || connectionState === "connected"}
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
            </div>
          </article>

          <article className="card">
            <h3>Audio distant</h3>
            <p className="inline-note">
              Si un operateur est deja connecte dans la meme salle, son flux audio distant sera
              lu ici.
            </p>
            <div className="audio-stage" ref={remoteAudioContainerRef} />
          </article>
        </div>

        {isPromptOpen ? (
          <div className="permission-modal-backdrop" role="presentation">
            <div
              aria-describedby="audio-test-microphone-modal-description"
              aria-labelledby="audio-test-microphone-modal-title"
              aria-modal="true"
              className="permission-modal"
              role="dialog"
            >
              <h3 id="audio-test-microphone-modal-title">Autoriser le micro</h3>
              <p
                className="inline-note"
                id="audio-test-microphone-modal-description"
              >
                Le navigateur va demander l'acces au micro avant la connexion a la salle.
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
      </main>
    </div>
  );
}

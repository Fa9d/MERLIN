import { Suspense } from "react";

import { AudioTestRoom } from "@/components/audio-test-room";

export default function AudioRoomPage() {
  return (
    <Suspense fallback={<div className="page-shell section">Chargement de la salle audio...</div>}>
      <AudioTestRoom />
    </Suspense>
  );
}

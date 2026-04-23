import { Suspense } from "react";

import { AudioTestRoom } from "@/components/audio-test-room";

export default function AudioTestPage() {
  return (
    <Suspense fallback={<div className="page-shell section">Chargement du test audio...</div>}>
      <AudioTestRoom />
    </Suspense>
  );
}

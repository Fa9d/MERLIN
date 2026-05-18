import type { Metadata } from "next";
import { OrientationSurvey } from "./OrientationSurvey";
import "./styles.orientation-survey.css";

export const metadata: Metadata = {
  title: "Orientation — MÉSANGES | IVIA",
  description:
    "Un court parcours d'orientation MÉSANGES pour préparer une écoute juste. Au Québec, sous consentement, sans diagnostic.",
};

// Page dédiée au parcours d'orientation MÉSANGES (format survey téléphone).
// Volontairement détachée du PublicLayout : expérience plein écran centrée.
export default function OrientationPage() {
  return <OrientationSurvey />;
}

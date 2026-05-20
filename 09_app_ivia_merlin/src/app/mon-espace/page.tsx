"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { FormEvent, Suspense, useEffect, useMemo, useState } from "react";

import { PublicLayout } from "@/components/layout/PublicLayout";
import {
  getMyClient,
  listMyBookings,
  listMyEntitlements,
  PUBLIC_CLIENT_STORAGE_KEY,
  readStoredPublicClientSession,
  setMyPassword,
  updateMyClient,
  type BookingSlotRecord,
  type ClientEntitlementRecord,
  type LoginResponse,
  type MyClientRecord,
} from "@/lib/merlin-api";

type Dashboard = {
  session: LoginResponse;
  client: MyClientRecord | null;
  bookings: BookingSlotRecord[];
  entitlements: ClientEntitlementRecord[];
};

function MonEspaceContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const isMagicWelcome = searchParams.get("welcome") === "magic";

  const [data, setData] = useState<Dashboard | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      const session = readStoredPublicClientSession();
      if (!session) {
        router.replace("/acces-client");
        return;
      }

      try {
        const [client, bookings, entitlements] = await Promise.all([
          getMyClient(session.access_token),
          listMyBookings(session.access_token).catch(() => [] as BookingSlotRecord[]),
          listMyEntitlements(session.access_token).catch(() => [] as ClientEntitlementRecord[]),
        ]);
        if (cancelled) return;
        setData({ session, client, bookings, entitlements });
      } catch (error) {
        if (cancelled) return;
        const message = error instanceof Error ? error.message : "Erreur inconnue.";
        setErrorMessage(message);
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    }

    void load();
    return () => {
      cancelled = true;
    };
  }, [router]);

  const upcomingBookings = useMemo(() => {
    if (!data) return [] as BookingSlotRecord[];
    const today = new Date().toISOString().slice(0, 10);
    return data.bookings
      .filter((b) => b.slot_date >= today && b.status !== "cancelled")
      .sort((a, b) => a.slot_date.localeCompare(b.slot_date));
  }, [data]);

  const activeEntitlements = useMemo(() => {
    if (!data) return [] as ClientEntitlementRecord[];
    return data.entitlements.filter(
      (e) => e.record_status === "active" && e.quantity_remaining > 0,
    );
  }, [data]);

  function handleSignOut() {
    window.localStorage.removeItem(PUBLIC_CLIENT_STORAGE_KEY);
    window.sessionStorage.removeItem(PUBLIC_CLIENT_STORAGE_KEY);
    router.replace("/");
  }

  return (
    <PublicLayout>
      <div className="page-shell">
        <main className="section mon-espace-main">
          <div className="section-header">
            <div className="eyebrow">Mon espace IVIA</div>
            <h2>
              {data?.session.user.display_name
                ? `Bonjour ${data.session.user.display_name}.`
                : "Votre espace personnel"}
            </h2>
            <p>
              Voici votre démarche en cours, vos prochains rendez-vous, et les ressources réservées aux membres.
            </p>
          </div>

          {isMagicWelcome ? (
            <section className="card message message-success">
              <p>
                <strong>Votre compte est activé.</strong> Vous êtes connecté sans avoir eu à retenir
                de mot de passe.
              </p>
              <p className="inline-note">
                Si vous souhaitez revenir facilement plus tard, vous pourrez définir un mot de passe
                dans les paramètres de votre compte — c&apos;est optionnel.
              </p>
            </section>
          ) : null}

          {errorMessage ? (
            <section className="card message message-error">
              <p>{errorMessage}</p>
            </section>
          ) : null}

          {isLoading ? (
            <section className="card">
              <p className="inline-note">Chargement de votre espace…</p>
            </section>
          ) : data ? (
            <div className="grid mon-espace-grid">
              <article className="card stack-md">
                <h3>Mon dossier</h3>
                {data.client ? (
                  <>
                    <p>
                      <strong>{data.client.first_name_or_alias}</strong>
                      {data.client.last_name ? ` ${data.client.last_name}` : ""}
                    </p>
                    {data.client.email ? (
                      <p className="inline-note">
                        Courriel : <span className="mono">{data.client.email}</span>
                      </p>
                    ) : null}
                    <p className="inline-note">
                      Référence dossier : <span className="mono">{data.client.public_client_code}</span>
                    </p>
                    {data.client.activation_accepted_at ? (
                      <p className="inline-note">
                        Espace ouvert le{" "}
                        {new Date(data.client.activation_accepted_at).toLocaleDateString("fr-CA")}
                      </p>
                    ) : null}
                  </>
                ) : (
                  <>
                    <p>Aucune fiche client n&apos;est encore rattachée à votre compte.</p>
                    <p className="inline-note">
                      Faites votre première demande pour ouvrir un dossier durable.
                    </p>
                    <Link href="/rendez-vous" className="button button-primary">
                      Faire une demande
                    </Link>
                  </>
                )}
              </article>

              <article className="card stack-md">
                <h3>Prochaines actions</h3>
                <p className="inline-note">
                  Une demande déposée n&apos;est pas un rendez-vous confirmé. Pour réserver un créneau,
                  passez par la page de réservation.
                </p>
                <div className="public-access-actions">
                  <Link href="/rendez-vous/reserver" className="button button-primary">
                    Réserver un créneau
                  </Link>
                  <Link href="/praticiens" className="button button-secondary">
                    Découvrir les praticiens
                  </Link>
                </div>
              </article>

              <article className="card stack-md">
                <h3>Mes rendez-vous</h3>
                {upcomingBookings.length === 0 ? (
                  <p className="inline-note">
                    Aucun rendez-vous à venir pour l&apos;instant.
                  </p>
                ) : (
                  <ul className="list-plain">
                    {upcomingBookings.map((slot) => (
                      <li key={slot.id} className="stack-xs">
                        <strong>
                          {new Date(slot.slot_date).toLocaleDateString("fr-CA", {
                            weekday: "long",
                            day: "numeric",
                            month: "long",
                          })}
                        </strong>{" "}
                        à <strong>{slot.start_time.slice(0, 5)}</strong>
                        <span className="inline-note">
                          {" "}
                          · {slot.session_type} · statut {slot.status}
                        </span>
                      </li>
                    ))}
                  </ul>
                )}
              </article>

              <article className="card stack-md">
                <h3>Mes crédits IVIA</h3>
                {activeEntitlements.length === 0 ? (
                  <p className="inline-note">
                    Aucun crédit actif. Les crédits sont activés à la suite d&apos;un paiement.
                  </p>
                ) : (
                  <ul className="list-plain">
                    {activeEntitlements.map((e) => (
                      <li key={e.id}>
                        <strong>{e.entitlement_type_code}</strong> ·{" "}
                        {e.quantity_remaining} sur {e.quantity_total} disponible
                        {e.expires_at ? (
                          <span className="inline-note">
                            {" "}
                            · expire le {new Date(e.expires_at).toLocaleDateString("fr-CA")}
                          </span>
                        ) : null}
                      </li>
                    ))}
                  </ul>
                )}
              </article>

              <article className="card stack-md">
                <h3>Ressources réservées aux membres</h3>
                <p className="inline-note">
                  Articles, supports, fiches de réflexion — accès libre une fois votre espace ouvert.
                </p>
                <div className="public-access-actions">
                  <Link href="/ressources" className="button button-secondary">
                    Lire les ressources
                  </Link>
                  <Link href="/suivi" className="button button-secondary">
                    Mon suivi public
                  </Link>
                </div>
              </article>

              <article className="card stack-md">
                <h3>Mon journal (à venir)</h3>
                <p className="inline-note">
                  Un journal personnel pour noter ce qui traverse votre démarche sera bientôt disponible
                  dans votre espace. C&apos;est à ce moment-là que vous activerez, si vous le souhaitez, les
                  consentements d&apos;enregistrement et de transcription nécessaires pour vos séances.
                </p>
              </article>

              {data.client ? (
                <ProfileEditCard
                  client={data.client}
                  token={data.session.access_token}
                  onUpdated={(updated) =>
                    setData((d) => (d ? { ...d, client: updated } : d))
                  }
                />
              ) : null}

              <SetPasswordCard
                token={data.session.access_token}
                firstTime={isMagicWelcome}
              />
            </div>
          ) : null}

          {data ? (
            <div className="section-footer">
              <button type="button" className="button button-text" onClick={handleSignOut}>
                Me déconnecter
              </button>
            </div>
          ) : null}
        </main>
      </div>
    </PublicLayout>
  );
}

type ProfileEditCardProps = {
  client: MyClientRecord;
  token: string;
  onUpdated: (next: MyClientRecord) => void;
};

const LANGUAGE_OPTIONS: { code: string; label: string }[] = [
  { code: "fr-CA", label: "Français (Québec)" },
  { code: "en-CA", label: "English (Canada)" },
  { code: "es-CA", label: "Español" },
];

const TERRITORY_OPTIONS: { code: string; label: string }[] = [
  { code: "QC", label: "Québec" },
  { code: "ON", label: "Ontario" },
  { code: "NB", label: "Nouveau-Brunswick" },
  { code: "AUTRE", label: "Autre / hors Canada" },
];

function ProfileEditCard({ client, token, onUpdated }: ProfileEditCardProps) {
  const [firstNameOrAlias, setFirstNameOrAlias] = useState(client.first_name_or_alias);
  const [lastName, setLastName] = useState(client.last_name ?? "");
  const [phone, setPhone] = useState(client.phone ?? "");
  const [languageCode, setLanguageCode] = useState(client.language_code);
  const [territoryCode, setTerritoryCode] = useState(client.territory_code);
  const [isSaving, setIsSaving] = useState(false);
  const [savedAt, setSavedAt] = useState<Date | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSaving(true);
    setErrorMessage(null);
    try {
      const updated = await updateMyClient(
        {
          first_name_or_alias: firstNameOrAlias.trim() || null,
          last_name: lastName.trim() || null,
          phone: phone.trim() || null,
          language_code: languageCode || null,
          territory_code: territoryCode || null,
        },
        token,
      );
      onUpdated(updated);
      setSavedAt(new Date());
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Erreur inconnue.");
    } finally {
      setIsSaving(false);
    }
  }

  return (
    <article className="card stack-md">
      <h3>Compléter mon profil</h3>
      <p className="inline-note">
        Quelques précisions facultatives nous aident à mieux orienter votre accompagnement.
        Vous pouvez sauter cette étape pour l&apos;instant — rien n&apos;est obligatoire ici.
      </p>

      <form className="form-stack profile-edit-form" onSubmit={handleSubmit}>
        <label className="field">
          <span>Comment souhaitez-vous être appelé ?</span>
          <input
            value={firstNameOrAlias}
            onChange={(e) => setFirstNameOrAlias(e.target.value)}
            placeholder="Prénom ou alias"
          />
        </label>

        <div className="form-grid-2">
          <label className="field">
            <span>Nom (optionnel)</span>
            <input
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              placeholder="Nom de famille"
            />
          </label>

          <label className="field">
            <span>Téléphone (optionnel)</span>
            <input
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              placeholder="514 000 0000"
            />
          </label>
        </div>

        <div className="form-grid-2">
          <label className="field">
            <span>Langue de préférence</span>
            <select
              value={languageCode}
              onChange={(e) => setLanguageCode(e.target.value)}
            >
              {LANGUAGE_OPTIONS.map((o) => (
                <option key={o.code} value={o.code}>{o.label}</option>
              ))}
            </select>
          </label>

          <label className="field">
            <span>Territoire</span>
            <select
              value={territoryCode}
              onChange={(e) => setTerritoryCode(e.target.value)}
            >
              {TERRITORY_OPTIONS.map((o) => (
                <option key={o.code} value={o.code}>{o.label}</option>
              ))}
            </select>
          </label>
        </div>

        <button type="submit" className="button button-primary" disabled={isSaving}>
          {isSaving ? "Enregistrement…" : "Enregistrer mes informations"}
        </button>

        {errorMessage ? <p className="message message-error">{errorMessage}</p> : null}
        {savedAt && !errorMessage ? (
          <p className="profile-edit-saved">
            Enregistré à {savedAt.toLocaleTimeString("fr-CA")}.
          </p>
        ) : null}
      </form>
    </article>
  );
}

type SetPasswordCardProps = {
  token: string;
  firstTime: boolean;
};

function SetPasswordCard({ token, firstTime }: SetPasswordCardProps) {
  const [isOpen, setIsOpen] = useState(firstTime);
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isSaving, setIsSaving] = useState(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setErrorMessage(null);
    setSuccessMessage(null);

    if (newPassword.length < 8) {
      setErrorMessage("Le mot de passe doit contenir au moins 8 caractères.");
      return;
    }
    if (newPassword !== confirmPassword) {
      setErrorMessage("Les deux mots de passe ne correspondent pas.");
      return;
    }

    setIsSaving(true);
    try {
      const result = await setMyPassword(
        {
          new_password: newPassword,
          current_password: firstTime || !currentPassword ? null : currentPassword,
        },
        token,
      );
      setSuccessMessage(result.message);
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Erreur inconnue.");
    } finally {
      setIsSaving(false);
    }
  }

  return (
    <article className="card stack-md">
      <h3>{firstTime ? "Définir un mot de passe (optionnel)" : "Changer mon mot de passe"}</h3>
      <p className="inline-note">
        {firstTime
          ? "Vous êtes entré via un lien magique. Si vous voulez revenir plus facilement à votre espace, vous pouvez définir un mot de passe maintenant — ou plus tard, depuis cette page."
          : "Choisissez un nouveau mot de passe pour votre compte IVIA."}
      </p>

      {!isOpen ? (
        <button
          type="button"
          className="button button-secondary"
          onClick={() => setIsOpen(true)}
        >
          {firstTime ? "Définir mon mot de passe" : "Changer mon mot de passe"}
        </button>
      ) : (
        <form className="form-stack" onSubmit={handleSubmit}>
          {!firstTime ? (
            <label className="field">
              <span>Mot de passe actuel</span>
              <input
                type="password"
                autoComplete="current-password"
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
                placeholder="••••••••"
              />
              <span className="inline-note">
                Laissez vide si vous n&apos;en avez jamais défini.
              </span>
            </label>
          ) : null}

          <label className="field">
            <span>Nouveau mot de passe</span>
            <input
              required
              minLength={8}
              type="password"
              autoComplete="new-password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              placeholder="Au moins 8 caractères"
            />
          </label>

          <label className="field">
            <span>Confirmer le nouveau mot de passe</span>
            <input
              required
              minLength={8}
              type="password"
              autoComplete="new-password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Re-saisissez"
            />
          </label>

          <div className="public-access-actions">
            <button type="submit" className="button button-primary" disabled={isSaving}>
              {isSaving ? "Enregistrement…" : "Enregistrer"}
            </button>
            {!firstTime ? (
              <button
                type="button"
                className="button button-secondary"
                onClick={() => {
                  setIsOpen(false);
                  setErrorMessage(null);
                  setSuccessMessage(null);
                }}
              >
                Annuler
              </button>
            ) : null}
          </div>

          {errorMessage ? <p className="message message-error">{errorMessage}</p> : null}
          {successMessage ? (
            <p className="profile-edit-saved">{successMessage}</p>
          ) : null}
        </form>
      )}
    </article>
  );
}

export default function MonEspacePage() {
  return (
    <Suspense
      fallback={
        <PublicLayout>
          <div className="page-shell">
            <main className="section">
              <p className="inline-note">Chargement de votre espace…</p>
            </main>
          </div>
        </PublicLayout>
      }
    >
      <MonEspaceContent />
    </Suspense>
  );
}

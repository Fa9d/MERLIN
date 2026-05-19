"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Suspense, useEffect, useMemo, useState } from "react";

import { PublicLayout } from "@/components/layout/PublicLayout";
import {
  getMyClient,
  listMyBookings,
  listMyEntitlements,
  PUBLIC_CLIENT_STORAGE_KEY,
  readStoredPublicClientSession,
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

# JOURNAL — Console admin, parcours payant unifié & correctifs CI

**Date** : 2026-06-16
**Branche** : `refonte-ivia-site-unifie`
**Opérateur** : David Phaneuf + Claude Code (Opus 4.8)
**Référence amont** : `JOURNAL_REPRISE_REFERENTIELS_TRANSCRIPTION_20260610.md`

---

## 1. Facturation par offre & interrupteurs de test

- Table `app_settings` (clé→valeur runtime) + migration `20260615_0030`.
- `billing.is_offer_payant(db, code)` + endpoint `GET/PATCH /admin/billing-flags`
  (coché = payant ; décoché = gratuit pour tester).
- Câblage dans `_create_checkout_order` : offre décochée → parcours gratuit sans Stripe.

## 2. Offre 35 $ solo puis réconciliation des 3 offres

- D'abord crédit `solo_recording_credit` + `POST /payments/stripe/checkout/solo-recording`.
- **Redéfinition des 3 offres** (décision fondateur 2026-06-16) :
  - **35 $** = enregistrement + rappel 10 min · **49 $** = séance live 30 min · **75 $** = séance live 1 h.
  - Toutes incluent transcription + analyse. Prix séance live **selon la durée du créneau**.
  - Aligné : `billing.OFFERS`, `config`, `index.html`, `rendez-vous.html`, `confirmation.html`, admin.
- **Bug corrigé** : `bookings.checkout_held_slot` était sync et n'`await`ait pas
  `_create_checkout_order` (devenu async) → checkout live cassé. Passé en async.

## 3. Boucle de livraison praticien → client

- `client_facing_summary_text` (déjà généré par `session_note_cercle_v1`) désormais **éditable**
  + bouton « Valider et livrer au client » → crée un `DerivedDocument` visible client.
- `GET /me/documents` + page client `mes-resumes.html` (dépôt dans l'espace, sans courriel).

## 4. Parcours imposé : profil → paiement → séance

- Profil obligatoire : `clients.birthplace` (migration `20260616_0031`) + `profile_complete`
  (âge/genre/lieu/territoire), `PATCH /clients/me`, page `client/mon-profil.html`, gate sur
  `reserver.html` et `enregistrement.html`.
- **Paiement toujours avant** : `PILOT_MODE` retiré de `reserver.html`.
- **Mode paiement simulé** (`MERLIN_PAYMENTS_TEST_MODE=true` en prod, ou si pas de clé Stripe) :
  page `checkout/paiement-test.html` + `POST /payments/test/confirm/{id}` — étape paiement
  toujours visible, aucun débit. `false` au lancement.

## 5. Créneaux : pavage propre selon l'offre

- `schedules.available` : pas = durée du créneau (ancré au début de plage) → plus de
  demi-heure orpheline. `reserver.html` envoie la durée + sélecteur d'offre + message.

## 6. Rôles & droits admin

- Liste blanche admin par courriel : `MERLIN_ADMIN_EMAILS` (en prod : davidphaneuf@gmail.com),
  `is_admin()` / `require_admin()`. `UserRead.is_admin` exposé → UI conditionnelle.
- `lagent009@gmail.com` : déjà `public_client` (vérifié, aucune écriture nécessaire).

## 7. Console d'administration (5 modules, require_admin)

- **Vue d'ensemble** `/admin/overview` — chiffres clés + alertes de vigilance (Loi 21).
- **Comptes & accès** `/admin/accounts` — resend-verification, verify, role, status.
- **Demandes d'entrée** — `PATCH /intake-requests/{id}/handling` (tri/statut/note).
- **Comptabilité** `/admin/accounting` (summary + ledger) — grand livre, test exclu.
- **Facturation** `/admin/billing-flags`.
- Liens admin injectés par `session.js` (visibles des admins uniquement).

## 8. Courriels & déblocage testeurs

- **Override pilote** (`MERLIN_PILOT_EMAIL_OVERRIDE`) **désactivé** (était à 1 → tous les
  courriels arrivaient chez David). Les testeurs reçoivent désormais leur propre courriel.
- Stéphanie (inscrite avant la bascule) : lien de confirmation toujours valide ; déblocable
  via Comptes (admin) → Renvoyer lien / Vérifier.

## 9. CI

- **lint (ruff)** : imports/variables inutilisés retirés → vert.
- **full-suite** : `era_contexts.data` JSONB → `with_variant(JSON, "sqlite")` (Postgres
  inchangé en prod) → tests SQLite passent. CI vert.

## 10. Décisions / suites notées

- **Abonnement récurrent = pour les praticiens** ; ponctuel pour des sections encore à
  déterminer → à construire quand les sections seront définies (Stripe récurrent).
- **Assignation d'une demande à un praticien nommé** : à construire (suite de ce journal).
- **Frais Stripe réels** (via webhook) : le jour des vrais paiements.

## Migrations

HEAD : `20260616_0031`. Chaîne : `0028` transcript_text · `0029` express · `0030`
app_settings · `0031` clients.birthplace.

## Déploiement

Tout déployé en prod (OVH) au fil de l'eau, rebuilds détachés `deploy/prod-up.sh`,
audits liens/JS à 0, vérifs santé + routes gardées (401/403) à chaque étape.

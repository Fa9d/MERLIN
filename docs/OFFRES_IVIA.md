# Catalogue des offres IVIA — source de vérité

> Brouillon 2026-06-15, **à valider par David**. Sert de référence pour la tarification,
> la réservation et les parcours. Deux hypothèses prises faute de confirmation explicite,
> marquées ⚠ — à infirmer si besoin.

## Les offres

| # | Offre | Prix | Durée | Praticien en direct ? | Parcours | État technique |
|---|-------|------|-------|----------------------|----------|----------------|
| 1 | **Enregistrement seul** | 35 $ | libre (≤ 40 min) | Non | Le client enregistre sa voix → transcription dans son espace | ✅ construit (`/client/enregistrement.html`, `/me/recordings`) — **paiement non branché** |
| 2 | **Enregistrement + rappel** | 45 $ | 30 min enregistrés | Non sur le moment, puis **rappel praticien de 10 min** | Enregistre 30 min → **compte-rendu par courriel** → le praticien clique « rappeler » → **lien de rappel plafonné à 10 min** | 🟡 socle présent (enregistrement + compte-rendu IA) ; **à construire** : envoi courriel du compte-rendu + lien de rappel limité à 10 min |
| 3 | **Séance live** | 65 $ | 1 h | Oui | Réservation d'un créneau d'1 h dans une fenêtre du praticien → séance + analyse | 🟡 réservation OK ; **place flexible dans la fenêtre = fait** ; **prix à corriger** |

⚠ **Hypothèse A** : il n'existe **pas** de séance live de 30 min — le live, c'est uniquement le 1 h (offre 3). Le « 30 min » correspond à l'offre 2 (enregistré + rappel).
⚠ **Hypothèse B** : le **rappel de 10 min** (offre 2) est **déclenché par le praticien** après lecture du compte-rendu (bouton « rappeler »), pas automatiquement.

## Incohérences tarifaires à régler (⚠ décision de David)

- Le backend facture **un prix unique** (`MERLIN_STRIPE_SEANCE_AMOUNT_CENTS`, défaut **90 $**) pour toute séance réservée — il ne connaît pas 35/45/65.
- Les offres **1 et 2** (enregistrement) passent par un parcours **sans paiement** aujourd'hui (`/me/recordings` ne crée aucune commande Stripe).
- **À décider** : grille de prix par offre + faut-il faire payer les offres d'enregistrement (et comment — au dépôt ? avant ?).

## Découpage des disponibilités (fait)

- Le praticien définit des **fenêtres** (jour + début–fin), sans durée imposée — `/praticien/profil.html`.
- `GET /schedules/available` propose des **départs flexibles** (toutes les 30 min) pour une durée donnée (défaut 60 min, ou `duration_minutes` de l'offre), en excluant toute plage qui **chevauche** une réservation existante. Le client place donc sa séance où il veut dans la fenêtre.

## Reste à construire (séquencé)

1. **Tarif par offre** (backend) : résoudre le montant selon l'offre/durée au lieu du prix unique. ⚠ attend la grille.
2. **Sélecteur d'offre à la réservation** (`reserver.html`) : choisir l'offre → durée → créneau, en passant `duration_minutes` à `getAvailableSlots` (déjà supporté).
3. **Offre 2** : envoi du **compte-rendu par courriel** + **lien de rappel praticien plafonné à 10 min** (variante de la séance express avec `max_minutes`).
4. (option) brancher le **paiement** sur les offres d'enregistrement si décidé.

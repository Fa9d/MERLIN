# Modèle praticien IVIA — simple

> **Décidé le 2026-06-16** (David Phaneuf). Simplifie le modèle 3×3 du business plan
> `12_JURIDIQUE_AFFAIRES/IVIA_BP_FINANCEMENT_v2.3.md` §4.1.5 (qui est désormais **superseded**
> par ce document pour l'opérationnel). Principe : **simple, pas de surcharge d'infos.**

## En une phrase

Le praticien s'abonne (29,99 $/mois), fixe lui-même le prix de ses séances, et IVIA
prélève un petit frais plateforme par séance au-delà des 5 incluses chaque mois.

## L'abonnement — 29,99 $/mois

Inclut : agenda, gestion des rendez-vous, centralisation + sécurité des données (Québec,
Loi 25), et **5 séances par mois sans frais plateforme** (compteur remis à zéro chaque mois).

## Frais plateforme par séance (au-delà des 5 incluses)

Couvre l'analyse + la transcription. Selon la durée :

| Durée | Frais plateforme |
|---|---:|
| Séance 30 min | **3 $** |
| Séance 1 h | **5 $** |

### Réduction au volume (par mois, recalculée chaque mois)

| Séances payantes / mois | Réduction | 30 min | 1 h |
|---|---:|---:|---:|
| 0 – 29 | — | 3,00 $ | 5,00 $ |
| 30 – 79 | −20 % | 2,40 $ | 4,00 $ |
| 80 + | −40 % | 1,80 $ | 3,00 $ |

## Frais Stripe

**Ajoutés** au paiement (non absorbés par IVIA). Le jour des vrais paiements, le frais réel
vient du webhook Stripe ; d'ici là il est estimé (≈ 2,9 % + 0,30 $).

## Prix des séances

**Le praticien fixe le prix de ses séances** dans son espace perso (ajustable au besoin).
Les prix publics actuels **35 / 49 / 75 $** deviennent des **valeurs par défaut suggérées**.

## Revenu IVIA

= **abonnement** (29,99 $/mois) **+ frais plateforme** par séance (au-delà des 5).
IVIA ne prend pas le prix de la séance — celui-ci revient au praticien.

## Repère de rentabilité

Coût réel IVIA par séance ≈ **0,15 $** (transcription faster-whisper **locale** ≈ 0 $ +
analyse Claude ~0,12 $ + stockage ~0,01 $). Le frais 3/5 $ est donc quasi entièrement de la
marge ; Stripe est passé au client. Modèle sain même à bas volume.

## À construire (non encore implémenté)

- Abonnement praticien récurrent (Stripe récurrent **ou** suivi interne payé/impayé au début).
- Compteur « 5 séances incluses / mois » + frais plateforme par séance + paliers de volume.
- Champ « prix de séance » réglable dans l'espace praticien.
- Comptabilité : distinguer revenu abonnement vs frais plateforme (le module `/admin/accounting` existe).

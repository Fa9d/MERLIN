# JOURNAL — Mode bêta : séances offertes — 2026-07-18

## Décision fondateur

Pas de facturation client tant que l'entreprise n'est pas constituée (REQ fin
juillet, structuration ensuite). IVIA **assume les frais d'analyse** pendant la
phase bêta, et en fait un levier d'attraction : « séances offertes pendant la
version bêta ».

## Ce qui a été fait

1. **Aucun code de paiement retiré** — l'infrastructure existante fait tout :
   les interrupteurs admin « payant/offert » par offre (`pay_seance_live`,
   `pay_enr_rappel` dans app_settings) basculent le checkout en parcours
   gratuit (`_fulfill_free_order`, payments.py) sans Stripe. Réversible en un
   clic dans la console admin (Options de facturation).
2. **Nouvel endpoint public** `GET /payments/offers` — catalogue + état
   payant/offert, pour que le site adapte son discours sans dupliquer la
   vérité serveur.
3. **Discours bêta** : flux de réservation (« Confirmer ma séance → », note
   « cette séance vous est offerte — votre retour nous aide »), badge hero sur
   l'accueil, tarifs de la fiche praticien barrés → « offert », meta d'ecoute.html.
   Prix corrigés au passage sur la fiche (65/45/35 affichés vs catalogue réel
   75/35 — incohérence relevée à l'audit).
4. **Interrupteurs basculés en prod** : pay_seance_live=false, pay_enr_rappel=false.
5. **Porte Loi 27 ouverte** (audit, proposition 7) : formulaire employeurs →
   `POST /organization-leads` (confirmation client + notification admin par
   courriel), conversion Matomo `lead_employeur`.

## Économie de la bêta

Les coûts IA restent tracés par séance dans le grand livre `llm_usage_events`
(console admin Économie) — la bêta a un coût mesuré, pas subi (~0,12 $/analyse
estimé + coûts de régénération du circuit transcription). Revue hebdo du
cumul recommandée pendant la bêta.

## Retour arrière

Console admin → Options de facturation → recocher les offres. Aucun déploiement requis.

# IVIA — Coûts de conformité & gouvernance des données (Loi 25)

**Version** : v1.0 — 2026-06-18
**Statut** : DRAFT à valider (chiffres = estimations à confirmer avec le fournisseur retenu)
**Périmètre** : sauvegarde chiffrée · portabilité · droit à l'effacement
**Rattachement** : complète `IVIA_BP_FINANCEMENT_v2.4` et le modèle de ventilation
comptable (`admin_accounting.py` : HT/TPS/TVQ/frais_stripe/cout_ia/part_praticien/marge).

---

## 1. Principe

Trois capacités obligatoires (Loi 25), **toutes chiffrées** (au repos + en transit) :

| Capacité | Nature du coût | Récurrence |
|---|---|---|
| **Sauvegarde multi-support chiffrée** | Stockage objet hors-site Québec/Canada + transfert | OPEX mensuel |
| **Export / portabilité** | Compute ponctuel (génération d'archive) + transfert | Quasi nul (à la demande) |
| **Effacement sur demande** | Compute ponctuel + journalisation | Quasi nul (à la demande) |

> Le coût dominant est **la sauvegarde** (stockage récurrent). Export et effacement
> sont des actions ponctuelles à coût marginal négligeable.

---

## 2. Chiffrage (estimations 2026, à valider)

**Hypothèses** : stockage objet région Québec (ex. OVH Public Cloud Beauharnois) ≈
0,01–0,02 $/Go/mois ; audios conservés 30 jours (~30–60 Mo/séance) ; base + métadonnées
légères ; chiffrement côté client (age/gpg), aucun coût de licence.

| Phase | Volume sauvegardé estimé | Stockage hors-site /mois | Égress/transfert /mois |
|---|---|---|---|
| **Amorçage** (actuel) | < 5 Go | **≈ 1–3 $** | ≈ 0–1 $ |
| **Croissance** (~200 clients actifs) | 50–150 Go | **≈ 5–15 $** | ≈ 1–3 $ |
| **Échelle** (~1 000 clients actifs) | 300–700 Go | **≈ 20–60 $** | ≈ 3–10 $ |

- **Compute sauvegarde** : exécuté sur le VPS existant (cron) → **0 $ marginal**.
- **Développement (one-time)** : scripts de sauvegarde/restauration + endpoint d'export
  + flux d'effacement journalisé → effort interne, **pas de dépense externe**.
- **Coût de conformité par client/mois** : **≈ 0,02–0,10 $** en régime de croissance
  (négligeable au regard de l'abonnement praticien 29,99 $/mois).

---

## 3. Répercussion dans les frais

**Aucun frais additionnel visible au client** — cohérent avec la marque (pas de
sur-facturation de la confidentialité, qui est un dû). Le coût est **absorbé par la
marge existante** :

- **Abonnement praticien (29,99 $/mois)** : porte l'OPEX d'infrastructure & conformité.
  La gouvernance des données représente **< 1 %** de cet abonnement même à l'échelle.
- **Frais de plateforme par séance (3 $/5 $)** : inchangés ; déjà ventilés (dont `cout_ia`).
- La **portabilité et l'effacement** sont **gratuits pour le client** (obligation légale).

> Positionnement plan d'affaires : la conformité Loi 25 chiffrée n'est pas un centre
> de coût à refacturer, c'est un **argument de confiance** (cf. section « La confiance,
> en actes » du site) et un **différenciateur** face aux apps qui externalisent les données.

---

## 4. Répercussion en comptabilité

- **Nouvelle ligne de charge d'exploitation** : « Sauvegarde & conformité Loi 25 »
  (stockage objet hors-site + transfert), catégorie **OPEX récurrent mensuel**.
- Distincte des coûts **par transaction** déjà suivis dans `admin_accounting.py`
  (`frais_stripe`, `cout_ia`) : la conformité est un **coût fixe**, pas une ventilation
  d'encaissement.
- Recommandation : suivre cette ligne dans le **grand livre** (charges) et la refléter
  dans le tableau de marge mensuel (marge IVIA nette = marge brute − OPEX infra/conformité).
- À l'échelle, prévoir une **provision** « conservation & restauration » (tests de
  restauration trimestriels = temps interne, pas de dépense externe).

---

## 5. Suite

1. **Bâtir la sauvegarde** (filet de sécurité prioritaire) — script chiffré + cron +
   cible hors-site Québec/Canada à confirmer.
2. **Export / portabilité** (endpoints + boutons client/admin).
3. **Effacement sur demande** (cascade journalisée, précédée d'un export).

Décision attendue : **cible de stockage hors-site** (fournisseur Québec/Canada) +
secret de chiffrement, pour figer les coûts réels et démarrer la Phase 1.

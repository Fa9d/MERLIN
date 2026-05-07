# PLANNING — VAGUE 9

**Période cible** : 8 mai → ~12 mai 2026
**Date création** : 7 mai 2026 (fin de Vague 8.2)
**Auteur** : David Phaneuf + Perplexity Computer
**Pilote** : 31 mai 2026 (J‑24 au démarrage de cette vague)

---

## Contexte d'entrée

Sortie de Vague 8 + 8.2 :

- Stack outils figée 24 outils (analyse v1.1 commitée).
- Infra obs basique en ligne : `status.ivia.quebec` + `logs.ivia.quebec`.
- Runbook deploy v1.0 livré (OPS-001) → tout redéploiement futur est documenté.
- Repo `C:\MERLIN` = source de vérité ; `/opt/merlin` VPS = déploiement non versionné.
- Calibration estimations : infra ×1,5 / docs ×0,4 / mixte ×1,0.

Cette vague mélange **business plan opérationnel** (rentabilité 3 profils praticiens) et **3 tickets ops courts** (OPS-006, OPS-007, OPS-008).

---

## Objectif global

À la fin de Vague 9, David doit pouvoir répondre clairement à 3 questions :

1. **Combien je dois charger un praticien et combien je peux lui verser** pour que MERLIN soit rentable sur 12 mois (3 scénarios profils).
2. **Combien de visiteurs uniques par jour sur ivia.quebec** (analytics en place, sans cookies).
3. **Où sont mes secrets** : décision Infisical vs `.env.prod` actuel, et plan de migration si applicable.

Bonus : v0.app Premium activé pour accélérer maquettes UI MESANGE / MERLIN admin.

---

## Tickets / Tâches

### BP-001 — Business Plan opérationnel 3 profils praticiens × P&L 12 mois (P0)

**Estimé** : 3h30 (avec coef ×1,0 → ~3h30 réel attendu)
**Livrable** : `BP_OPERATIONNEL_V1.md` + `BP_OPERATIONNEL_V1.xlsx` (P&L 12 mois, 3 onglets)

**Sous-étapes** :

1. Définir les 3 profils praticiens (ex : massothérapeute débutant, ostéopathe établi, naturopathe spécialisé) — tarif horaire client, fréquence séances, % MERLIN, charges spécifiques. (~30 min)
2. Modéliser P&L mensuel sur 12 mois pour chaque profil : revenus bruts → commission MERLIN → coûts variables (paiement Stripe, hébergement par praticien, support) → marge contributive. (~1h30)
3. Agréger en un P&L MERLIN consolidé : combien de praticiens de chaque profil pour atteindre seuil de rentabilité (charges fixes : VPS, outils, salaire David, marketing). (~45 min)
4. Note de synthèse `BP_OPERATIONNEL_V1.md` : hypothèses, formules, conclusions, sensibilités (que se passe-t-il si commission baisse de 2 pts ? si churn = 15%/an ?). (~45 min)

**Critère d'acceptation** : David peut donner un chiffre de commission cible et un seuil minimum de praticiens actifs au mois 6 et au mois 12.

---

### OPS-006 — Umami Analytics self-hosted (P1)

**Estimé** : 45 min (×1,5 → ~1h10 réel attendu)
**Livrable** : `analytics.ivia.quebec` en ligne + script tracking sur `ivia.quebec`

**Sous-étapes** :

1. Ajouter service Umami au `docker-compose.yml` (image officielle + base Postgres dédiée ou réutilisée). (~15 min)
2. Configuration nginx : nouveau server block HTTPS pour `analytics.ivia.quebec` + DNS OVH A record. (~15 min)
3. Certbot + smoke test login. (~10 min)
4. Créer site dans Umami → coller snippet `<script>` dans le `<head>` de `ivia.quebec`. (~5 min)

**Critère d'acceptation** : compteur de visiteurs incrémente quand David charge la page en navigation privée depuis son téléphone.

**Sync** : pull modifs VPS vers `C:\MERLIN` via scp + commit + push (réflexe Vague 8).

---

### OPS-007 — Décision Infisical vs `.env.prod` (P1)

**Estimé** : 1h30 (×1,5 → ~2h15 réel attendu)
**Livrable** : Note de décision `DECISION_SECRETS_MGMT.md` + (si GO Infisical) ticket OPS-007b pour la migration effective en Vague 10

**Sous-étapes** :

1. Lister tous les secrets actuels dans `/opt/merlin/.env.prod` + tous les secrets générés ce mois (Dozzle htpasswd, JWT, OPENAI_API_KEY, OVH, etc.). (~20 min)
2. Comparer 3 options : `.env.prod` actuel / Infisical self-hosted / Infisical cloud free tier. Critères : sécurité, rotation, coût, complexité opérationnelle pour 1 dev solo. (~40 min)
3. Décision argumentée + plan de migration en 4 étapes si Infisical retenu. (~30 min)

**Critère d'acceptation** : décision écrite signée par David. Pas de migration effective dans cette vague (trop coûteux à valider en pilote J‑24).

**Note honnête** : pour un dev solo à J‑24, l'option « rester sur `.env.prod` + ticket OPS-012 centraliser credentials dans 1Password personnel » a une probabilité élevée d'être la bonne. À ne pas écarter par biais d'outillage.

---

### OPS-008 — v0.app Premium activation (P2)

**Estimé** : 5 min (×1,0 → 5 min)
**Livrable** : Compte v0.app Premium actif, lien sauvegardé dans `IVIA_ANALYSE_STACK_OUTILS_v1.1.md`

**Sous-étapes** :

1. S'abonner via vercel.com/v0 (carte déjà en place sur Vercel).
2. Tester 1 prompt simple ("page admin liste praticiens en shadcn/ui") pour valider que l'output est exploitable.

**Critère d'acceptation** : 1 composant React généré et collable dans MESANGE.

---

## Synthèse temps

| Tâche | Estimé | Coef | Réel attendu |
|---|---:|---:|---:|
| BP-001 | 3h30 | ×1,0 | 3h30 |
| OPS-006 Umami | 45 min | ×1,5 | 1h10 |
| OPS-007 Décision secrets | 1h30 | ×1,5 | 2h15 |
| OPS-008 v0.app | 5 min | ×1,0 | 5 min |
| **TOTAL** | **5h50** | — | **~7h00** |

À 3h/jour soutenable → **2,5 jours** (Vague 9 finie ~ samedi 9 mai soir).
À 6h/jour intensif → **1 jour et demi**.

---

## Définition de fini (Vague 9)

- [ ] BP_OPERATIONNEL_V1 livré (.md + .xlsx) et commité dans `C:\MERLIN\00_GOUVERNANCE\BP\`
- [ ] `analytics.ivia.quebec` répond, snippet posé sur ivia.quebec, 1 visite enregistrée
- [ ] `DECISION_SECRETS_MGMT.md` commité dans `C:\MERLIN\00_GOUVERNANCE\PLANNING\`
- [ ] v0.app Premium actif, 1 composant test généré
- [ ] Bilan rétrospective `BILAN_VAGUE9_RETROSPECTIVE.md` rédigé avec estimé/réel mesuré
- [ ] Tous commits poussés sur `master`

---

## Risques identifiés

| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| Modélisation BP plus longue que prévu (formules Excel) | Moyenne | Moyen | Limiter à 3 profils, pas 5. Itérer en V10 si besoin. |
| Umami casse certbot (nouveau server block) | Faible | Moyen | Suivre runbook OPS-001 section "Ajouter un sous-domaine HTTPS". |
| Décision Infisical par biais d'outillage (over-engineering) | Élevée | Faible | Forcer la question : *que perd David s'il garde `.env.prod` 60 jours de plus ?* |
| Fatigue post-Vague 8 (10h écran le 7 mai) | Élevée | Moyen | Démarrer V9 le 8 mai après-midi seulement, pas le 7 au soir. |

---

## Reportés explicitement (PAS dans cette vague)

- **OPS-004** GlitchTip monitoring erreurs → Vague 10
- **OPS-005** Linear migration → Vague 10
- **OPS-012** Centraliser credentials → Vague 10 (déclenché par OPS-007 si Infisical refusé)
- **OPS-014** Cron renouvellement Let's Encrypt → Vague 10 (urgent avant J+60 = 6 juillet)
- **BACK-010** Refactor prompt_loader.py → Backlog tech
- **GOUV-002** Hiérarchiser 80 docs gouvernance → Backlog perma

---

## Devise

*Au sein de l'être — En actes.*

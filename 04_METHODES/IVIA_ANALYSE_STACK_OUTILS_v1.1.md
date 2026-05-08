# IVIA / MERLIN — Analyse stratégique de la stack d'outils

**Document de plan d'affaires • v1.1 • 7 mai 2026**
**Auteur** : Perplexity Computer (analyse) en appui à David Phaneuf (décision)
**Horizon** : 12 mois (mai 2026 → mai 2027)
**Contexte** : Solo founder, MVP rentable juin 2026, premier praticien pilote 31 mai 2026

---

## ✅ Note de validation — Décisions actées

**Date d'arbitrage** : Jeudi 7 mai 2026, 13h53 EDT
**Validateur** : David Phaneuf
**Méthode** : revue par blocs (4 blocs, validation "tout OK" par bloc)

### Tableau de décisions finales

| Catégorie | Outil | Décision | Vague |
|---|---|---|---|
| IDE + IA codage | VSCode + Claude Code + Codex + Copilot | ✅ GARDER | Déjà actif |
| IDE alternatif | Zed Editor | ⏳ À tester gratuit | Quand utile |
| Terminal | Warp Terminal (free tier) | ⏳ À tester gratuit | Quand utile |
| IDE alternatif payant | Cursor Pro / Pro+ | ❌ REJETÉ | — |
| Génération UI | v0.app Premium (3 mois) | ✅ SOUSCRIRE | Vague 9 |
| Composants UI | shadcn/ui | ✅ ADOPTER | Immédiat |
| Maquettes | Figma Free | ✅ GARDER | Déjà actif |
| Génération UI alt. | Bolt.new / Lovable | ❌ REJETÉ | — |
| Monitoring erreurs | **GlitchTip** self-hosted | ✅ DÉPLOYER | Vague 8 (OPS-004) |
| Monitoring erreurs alt. | Sentry Team SaaS | ❌ REJETÉ | — |
| Analytics web | **Umami** self-hosted | ✅ DÉPLOYER | Vague 9 (OPS-006) |
| Analytics alt. | Plausible Cloud / PostHog Cloud | ❌ REJETÉ | — |
| Analytics futur | PostHog self-hosted | ⏳ REPORTÉ | Vague 12+ |
| Gestion tickets | **Linear Free** | ✅ ADOPTER | Vague 8 (OPS-005) |
| Gestion tickets alt. | Linear Basic / OpenProject | ❌ REJETÉ / ⏳ | — / Plus tard |
| Code review | CodeRabbit Free + Claude Code | ✅ PATTERN HYBRIDE | Immédiat |
| Code review alt. | CodeRabbit Pro | ❌ REJETÉ | — |
| Secrets | **Infisical** self-hosted | ✅ DÉPLOYER | Vague 9 (OPS-007) |
| Secrets alt. | Doppler Team | ❌ REJETÉ | — |
| Logs Docker | **Dozzle** self-hosted | ✅ DÉPLOYER | Vague 8 (OPS-002) |
| Status page | **Uptime Kuma** self-hosted | ✅ DÉPLOYER | Vague 8 (OPS-003) |
| Status page alt. | Better Stack Status | ❌ REJETÉ | — |
| Métriques | Grafana + Loki + Prometheus | ⏳ REPORTÉ | Vague 10 (OPS-009) |
| Logs alt. | Better Stack Logtail | ❌ REJETÉ | — |

### Récapitulatif numérique acté

- **✅ GO** : 11 outils retenus
- **❌ REJETÉS** : 9 outils écartés
- **⏳ REPORTÉS** : 4 outils à réévaluer plus tard
- **Coût annuel validé** : ~684 $ CAD (vs 3 276 $ scenario tout-SaaS)
- **Économie actée** : 2 592 $ CAD/an minimum

### Tickets backlog créés

Voir `00_GOUVERNANCE/PLANNING/TICKETS_BACKLOG_VAGUE8.md` — 10 tickets OPS planifiés sur Vagues 8-12.

---

---

## 1. Synthèse exécutive

David dispose déjà d'un trio d'IA de codage exceptionnel (Claude Code + Codex + Copilot) intégré à VSCode. La question n'est donc pas « quels outils acheter » mais **« quels outils ajoutent de la valeur sans alourdir le P&L d'un MVP solo »**.

### Recommandation centrale

> **Construire une stack 95 % open-source / self-hosted sur ton VPS OVH existant, en gardant uniquement 2-3 SaaS payants à fort effet de levier (les 3 IA de codage déjà en place + 1 outil de design).**

**Coût total mensuel recommandé** : **~85-110 CAD/mois** (vs ~520 CAD/mois pour la version « tout SaaS commercial »).
**Économie sur 12 mois** : **~5 000 CAD**, soit l'équivalent d'un mois de revenus du palier de rentabilité.

### Les 3 décisions clés

1. **Garder Claude Code + Codex + Copilot** : ROI démontré sur Vague 6-7. Ne pas migrer vers Cursor maintenant — coût additionnel sans gain marginal.
2. **Tout le monitoring/analytics/secrets en open-source self-hosted** sur le VPS OVH : économie de 200-400 CAD/mois pour 4-6 h de setup unique.
3. **Investir uniquement en SaaS pour le design/UX** : c'est là que le ROI est asymétrique et que l'open-source n'égale pas encore.

---

## 2. Cadre d'analyse — Les 4 critères de décision

Pour chaque outil, j'ai évalué :

| Critère | Pondération | Question |
|---|---|---|
| **Coût direct** | 30 % | Combien ça coûte par mois sur 12 mois ? |
| **Coût caché** | 20 % | Temps de setup, maintenance, lock-in vendeur ? |
| **Conformité Loi 25 / RGPD** | 25 % | Hébergement local possible ? Données chez qui ? |
| **Effet de levier business** | 25 % | Est-ce que ça accélère MVP/revenus ? |

**Filtre final** : si l'outil ne fait pas gagner > 4 h/mois OU n'apporte pas un signal de qualité visible au praticien pilote, il est rejeté.

---

## 3. Analyse détaillée par catégorie

### 3.1. IDE et environnement de développement

| Outil | Tarif mensuel (CAD) | Verdict | Justification |
|---|---|---|---|
| **VSCode + Claude Code + Codex + Copilot** ✅ DÉJÀ EN PLACE | Variable selon usage (estim. 40-80 $) | **GARDER** | Stack actuelle, productivité prouvée Vague 6-7 |
| Cursor Pro | 28 $ ([Cursor](https://cursor.com/pricing)) | **REJETER** | Doublon avec Claude Code/Copilot ; pas de gain marginal |
| Cursor Pro+ | 84 $ | **REJETER** | Idem, prix prohibitif |
| **Zed Editor** (open-source, MIT) | 0 $ ([Zed](https://zed.dev/pricing)) | **À TESTER** | Plan Personal gratuit à vie ; ultra-rapide ; bring-your-own-key pour IA. Garder en backup si VSCode rame. |
| **Warp Terminal** | 0 $ (gratuit) ou 28 $/mois Build ([Warp](https://www.warp.dev/pricing)) | **TESTER GRATUIT** | Tier gratuit suffit pour solo. BYOK = utilise tes clés Anthropic/OpenAI déjà payées. |

**Décision** : ne RIEN ajouter de payant ce trimestre. Tester Zed et Warp gratuits pour évaluer.

### 3.2. Génération UI / Design

C'est ici que le ROI est le plus asymétrique pour la phase visuelle d'IVIA.

| Outil | Tarif mensuel (CAD) | Verdict | Justification |
|---|---|---|---|
| **v0.app Premium** (Vercel) | 28 $ ([v0 review](https://www.taskade.com/blog/v0-review)) | **OUI, 3 mois ciblés** | Génère du shadcn/ui prêt à coller. Crédits illimités. ROI immédiat sur landing IVIA. |
| **shadcn/ui** (composants open-source MIT) | 0 $ | **OUI, foundation** | Base de composants gratuits, copié-collé directement. Compatible v0 output. |
| **Figma Free** | 0 $ | **OUI** | Suffisant pour 1 designer solo. AI gratuit en limité. |
| **Bolt.new / Lovable** | 28 $/mois | **REJETER** | Doublon v0, moins bon pour ton stack React existant |

**Décision** : v0.app Premium pendant 3 mois (mai-juin-juillet) pour landing + onboarding praticien, puis évaluer. Coût total : ~85 CAD.

### 3.3. Monitoring d'erreurs

| Outil | Tarif mensuel (CAD) | Verdict | Justification |
|---|---|---|---|
| Sentry Team | 36 $ ([Sentry](https://sentry.io/pricing/)) | **REJETER** | Free tier 5k events/mois suffisant... mais alternative open-source meilleure |
| **GlitchTip** (self-hosted, AGPL) | 0 $ (compute VPS existant) ([Uptrace comparison](https://uptrace.dev/comparisons/sentry-alternatives)) | **CHOIX RECOMMANDÉ** | API-compatible Sentry (mêmes SDK FastAPI/React) ; déploiement Docker en 30 min ; respect Loi 25 (données restent OVH Beauharnois) |
| **Highlight.io** (self-hosted) | 0 $ | Alternative | Plus lourd, ajoute session replay |

**Décision** : GlitchTip self-hosted sur VPS. **Économie 12 mois : ~430 CAD**.

### 3.4. Analytics web (conformité Loi 25 critique)

| Outil | Tarif mensuel (CAD) | Verdict | Justification |
|---|---|---|---|
| Plausible Cloud | 12 $ ([Plausible](https://plausible.io/self-hosted-web-analytics)) | Acceptable | Loi 25-compliant, pas de cookies, mais hébergé UE |
| **Plausible self-hosted** (AGPL) | 0 $ | **OPTION 1** | Polish UI, Docker compose, AGPL force partage modifs (peu probable) |
| **Umami** (MIT, self-hosted) | 0 $ ([OpenPanel comparison](https://openpanel.dev/articles/self-hosted-web-analytics)) | **OPTION 2 RECOMMANDÉE** | Licence MIT (pas de contrainte AGPL), ultra-léger, déploiement 15 min |
| PostHog Cloud | 0 $ free tier puis usage ([PostHog](https://posthog.com/pricing)) | **REJETER pour MVP** | Trop puissant, courbe d'apprentissage, hébergé US |
| PostHog self-hosted | 0 $ + ~2 GB RAM dédiée | À considérer **plus tard** | Quand tu auras besoin de session replay + feature flags (post-MVP) |

**Décision** : **Umami self-hosted** maintenant. PostHog self-hosted en Vague 12+ quand tu auras 50+ praticiens et besoin de comportement utilisateur.

### 3.5. Gestion de projet / tickets

| Outil | Tarif mensuel (CAD) | Verdict | Justification |
|---|---|---|---|
| Linear Free | 0 $ ([Linear](https://linear.app/pricing)) | **OUI MAINTENANT** | 250 issues, 2 teams, illimité membres. Largement suffisant solo. |
| Linear Basic | ~12 $ | Plus tard | Quand tu dépasseras 250 issues |
| GitHub Projects | 0 $ (déjà inclus) | **ALTERNATIVE GRATUITE** | Intégré au repo, suffisant si tu n'as pas envie de migrer |
| **OpenProject** (self-hosted GPL) | 0 $ | Alternative | Plus lourd, pour équipe future > 5 personnes |

**Décision** : Linear Free immédiatement. Migration tickets MES-/MATCH-/INFRA- en 2 h. Gain de clarté énorme sur Vague 8+.

### 3.6. Code review automatique

| Outil | Tarif mensuel (CAD) | Verdict | Justification |
|---|---|---|---|
| **CodeRabbit Free** | 0 $ ([CodeRabbit](https://coderabbit.ai/pricing)) | **OUI** | Free tier suffit pour repos publics ou < N PRs. Tu codes seul donc volume faible. |
| CodeRabbit Pro | 21 $ | Pas maintenant | Si volume PR augmente |
| **Claude Code en review mode** | Inclus | **ALTERNATIVE** | Tu peux demander à Claude Code de reviewer une PR avant merge. Gratuit dans ton stack actuel. |

**Décision** : Pattern hybride — Claude Code review systématique avant merge sur master, CodeRabbit Free en filet de sécurité GitHub.

### 3.7. Gestion de secrets

| Outil | Tarif mensuel (CAD) | Verdict | Justification |
|---|---|---|---|
| Doppler Team | ~10 $/dev | Pas maintenant | Plat per-user, polish ([Doppler comparison](https://www.doppler.com/blog/infisical-doppler-secrets-management-comparison-2025)) |
| **Infisical self-hosted** (MIT) | 0 $ | **CHOIX** | Open-source réel, données chez toi, end-to-end encryption |
| **Bitwarden Secrets Manager** (self-hosted) | 0 $ | Alternative | Si tu utilises déjà Bitwarden personnel |
| .env files actuels | 0 $ | Stop-gap | OK jusqu'à 5 services, devient ingérable après |

**Décision** : Infisical self-hosted en Vague 9 (post-déploiement Vague 7). Pas urgent ce mois-ci.

### 3.8. Logs et observabilité

| Outil | Tarif mensuel (CAD) | Verdict | Justification |
|---|---|---|---|
| Better Stack (Logtail) | 35 $ minimum | **REJETER** | Cher pour solo |
| **Grafana + Loki + Prometheus** (Apache 2) | 0 $ | **CHOIX MVP** | Stack standard 2026, déploiement Docker compose, dashboards beaux |
| **Dozzle** (MIT) | 0 $ | **AJOUT IMMÉDIAT** | UI web pour logs Docker, 1 conteneur, 50 MB RAM. Setup 5 min. |

**Décision** : Dozzle cette semaine (5 min). Grafana stack en Vague 10 quand tu voudras alertes + métriques applicatives.

### 3.9. Status page (signal de sérieux praticien)

| Outil | Tarif mensuel (CAD) | Verdict | Justification |
|---|---|---|---|
| Better Stack Status | 35 $ | **REJETER** | Cher |
| **Uptime Kuma** (MIT, self-hosted) | 0 $ | **CHOIX** | Status page publique + monitoring uptime, déploiement 10 min, magnifique. |

**Décision** : Uptime Kuma cette semaine. Page publique `status.ivia.quebec` = signal pro pour praticien pilote.

---

## 4. Stack recommandée — Tableau récapitulatif

| Catégorie | Outil retenu | Type | Coût mensuel CAD | Hébergement |
|---|---|---|---|---|
| IDE + IA codage | VSCode + Claude Code + Codex + Copilot | SaaS | ~50 $ (estim.) | Cloud (déjà payé) |
| Génération UI | v0.app Premium (3 mois ciblés) | SaaS | 28 $ × 3 mois | Cloud |
| Composants UI | shadcn/ui | Open-source MIT | 0 $ | Code repo |
| Maquettes | Figma Free | Freemium | 0 $ | Cloud |
| Monitoring erreurs | **GlitchTip** | Self-hosted AGPL | 0 $ | VPS OVH |
| Analytics web | **Umami** | Self-hosted MIT | 0 $ | VPS OVH |
| Gestion tickets | Linear Free | SaaS Freemium | 0 $ | Cloud |
| Code review | CodeRabbit Free + Claude Code | Freemium + déjà payé | 0 $ | Cloud |
| Logs Docker | **Dozzle** | Self-hosted MIT | 0 $ | VPS OVH |
| Status page | **Uptime Kuma** | Self-hosted MIT | 0 $ | VPS OVH |
| Secrets (Vague 9) | **Infisical** | Self-hosted MIT | 0 $ | VPS OVH |
| Métriques (Vague 10) | **Grafana + Loki** | Open-source | 0 $ | VPS OVH |

**Total mois 1-3** : ~78 $ CAD/mois (50 $ IA + 28 $ v0)
**Total mois 4-12** : ~50 $ CAD/mois (IA seulement)
**Coût annuel total estimé** : **~684 $ CAD**

---

## 5. Comparaison avec scénario « tout SaaS commercial »

| Outil SaaS équivalent | Tarif mensuel (CAD) |
|---|---|
| Cursor Pro+ (au lieu de stack actuelle) | 84 $ |
| Sentry Team | 36 $ |
| Plausible Cloud | 12 $ |
| Linear Basic | 12 $ |
| CodeRabbit Pro | 21 $ |
| Doppler Team | 30 $ |
| Better Stack | 50 $ |
| v0.app Premium | 28 $ |
| **Total mensuel** | **273 $ CAD** |
| **Total annuel** | **3 276 $ CAD** |

### Économie nette stack open-source recommandée

**3 276 $ - 684 $ = 2 592 $ CAD/an d'économisés**

À cela s'ajoute l'évitement des coûts cachés Sentry (au-delà de 50k events) qui peuvent monter à **400-800 $/mois** rapidement avec un trafic réel.

**Économie réaliste sur 12 mois** : **3 500 - 5 000 $ CAD**.

---

## 6. Impact sur le P&L MERLIN (12 mois)

### Hypothèses
- 1er praticien pilote actif 31 mai 2026
- 5 praticiens actifs au 31 août 2026
- 15 praticiens au 31 décembre 2026
- Revenu moyen MERLIN par praticien : ~50 $/mois (commission + abonnement plateforme — à confirmer modèle)

### Lignes de coût « Outils » du P&L

| Mois | Stack open-source | Stack tout-SaaS | Différentiel |
|---|---|---|---|
| Mai 2026 | 78 $ | 273 $ | -195 $ |
| Juin 2026 | 78 $ | 273 $ | -195 $ |
| Juillet 2026 | 78 $ | 273 $ | -195 $ |
| Août → Mai 2027 (×9) | 50 $ | 273 $ | -223 $/mois |
| **Total 12 mois** | **684 $** | **3 276 $** | **-2 592 $** |

### Interprétation business

- **Point mort accéléré** : avec 50 $/mois de coûts outils au lieu de 273 $, tu n'as besoin que de **1 praticien** au lieu de 5-6 pour couvrir tes outils.
- **Marge brute MVP** : sur 15 praticiens × 50 $ = 750 $/mois de revenus, la stack open-source consomme 6,7 % vs 36,4 % en SaaS commercial.
- **Cash runway** : 2 600 $ économisés = ~2 mois de runway personnel additionnel pour toi.

---

## 7. Coûts cachés à anticiper

### Coûts cachés stack open-source (à provisionner)

| Poste | Estimation | Mitigation |
|---|---|---|
| Setup initial (5 outils self-hosted) | 8-12 h dev | Faire en Vague 8-10, déléguer à Claude Code |
| Maintenance mensuelle (updates, backups) | 2 h/mois | Automatiser avec Watchtower + cron rsync |
| Compute additionnel VPS | +10-20 $/mois si OVH actuel saturé | Monitorer load avant d'ajouter Grafana stack |
| Risque uptime (auto-hébergé) | Tolérable MVP | Status page publique gère la communication |

### Coûts cachés stack tout-SaaS

| Poste | Estimation | Risque |
|---|---|---|
| Dépassement Sentry (events) | 0-800 $/mois variable | Élevé en cas de bug en prod |
| Lock-in données analytics | Coût migration ~10 h | Élevé long-terme |
| Conformité Loi 25 (données hors Canada) | Risque juridique | Critique pour secteur santé |

---

## 8. Plan d'exécution recommandé

### Vague 8 (cette semaine — après déploiement Vague 7 actuel)

1. **Linear migration** (2 h, Claude Code) — exporter MD tickets → Linear
2. **Dozzle** (10 min, Claude Code) — UI logs Docker sur VPS
3. **Uptime Kuma** (30 min, Claude Code) — status.ivia.quebec
4. **GlitchTip** (1-2 h, Claude Code) — remplace `print()` errors par SDK Sentry pointant vers GlitchTip self-hosted

### Vague 9 (semaine du 14 mai)

5. **Umami Analytics** (30 min) — script tracking sur ivia.quebec
6. **v0.app Premium** (souscription 28 $) — refonte landing + onboarding praticien

### Vague 10 (semaine du 21 mai, J-10 avant pilote)

7. **Infisical secrets** (2 h) — migrer .env critiques
8. **Grafana + Loki** (3 h, optionnel) — dashboards perf

### Vague 11+ (post-31 mai pilote actif)

9. **PostHog self-hosted** quand 5+ praticiens et besoin d'analyse comportementale
10. **CodeRabbit Pro** si volume PR augmente
11. **Évaluer migration Cursor** si productivité IA stagne

---

## 9. Risques et points d'attention

### Risque #1 — Surcharge VPS OVH
**Probabilité** : moyenne
**Impact** : moyen
**Mitigation** : surveiller `htop` avant chaque ajout. Si > 70 % RAM utilisée, upgrade VPS (≈ +15 $/mois) reste moins cher que SaaS équivalents.

### Risque #2 — Maintenance des outils self-hosted
**Probabilité** : élevée à long terme
**Impact** : faible (2 h/mois)
**Mitigation** : Watchtower pour auto-updates Docker + scripts backup hebdo. Inclure dans GOUV-005.

### Risque #3 — Conformité Loi 25 sur services SaaS résiduels
**Probabilité** : moyenne
**Impact** : critique (santé)
**Mitigation** : tous les outils SaaS retenus (v0, Linear, GitHub) **ne traitent pas de données patients**. Données patients restent 100 % sur VPS OVH Beauharnois. Politique de confidentialité v0.1 déjà conforme.

### Risque #4 — Lock-in sur Claude Code / Anthropic
**Probabilité** : faible court-terme, élevée long-terme
**Impact** : élevé
**Mitigation** : Codex (OpenAI) + Copilot (Microsoft) déjà en place = redondance fournisseurs IA. Tu peux toujours basculer.

---

## 10. Réponse aux 2 questions de David

### Q1 : « Y a-t-il des sources Git ou open-source aussi performantes ? »

**Oui, dans 90 % des catégories.** Les exceptions notables :

- **IA de codage** : pas d'équivalent open-source à Claude Code/Codex/Copilot pour la qualité. Continodes (open-source) est correct mais 6-12 mois en retard. **Garder le payant.**
- **Génération UI premium** : v0.app reste devant les alternatives open-source (Windai, etc.) pour la qualité shadcn/ui. **Investir 3 mois ciblés.**
- **Tout le reste** (monitoring, analytics, secrets, logs, status, tickets jusqu'à un certain volume) : **les open-source sont équivalents ou supérieurs**, surtout pour ton contexte Loi 25.

### Q2 : « Comment intégrer ça au plan d'affaires ? »

Trois lignes à ajouter dans le P&L MERLIN section « Charges d'exploitation » :

```
COMPTE 6230 — OUTILS LOGICIELS & SAAS
├── 6231 Outils IA développement       50 $/mois × 12 = 600 $
├── 6232 Outils design (3 mois)        28 $ × 3       =  84 $
└── 6233 Hébergement open-source       0 $ (inclus VPS)
TOTAL ANNUEL                                          684 $ CAD
```

À comparer avec un budget « stack SaaS standard » de 3 276 $/an.

**L'économie de 2 592 $/an équivaut à 4-5 mois de coûts opérationnels MVP.**

---

## 11. Décision attendue de David

**Trois options pour la suite :**

**Option A — Validation totale + lancement progressif**
Tu valides cette stack, je prépare les prompts Claude Code pour Vagues 8-10 dans l'ordre proposé.

**Option B — Validation partielle + ajustements**
Tu veux modifier certains choix (ex: garder Sentry SaaS pour la simplicité, ou prendre Cursor pour tester). On en discute, je révise.

**Option C — Mise en pause stack outils, focus déploiement Vague 7**
On finit d'abord le déploiement Vague 7 en cours, on revient à cette analyse une fois en prod stable.

---

## Sources et références

- [Cursor Pricing 2026](https://cursor.com/pricing)
- [Zed Pricing](https://zed.dev/pricing)
- [Warp Terminal Pricing](https://www.warp.dev/pricing)
- [Sentry Plans](https://sentry.io/pricing/)
- [GlitchTip vs Sentry comparison (Uptrace)](https://uptrace.dev/comparisons/sentry-alternatives)
- [PostHog Pricing](https://posthog.com/pricing)
- [Linear Pricing](https://linear.app/pricing)
- [CodeRabbit Pricing](https://coderabbit.ai/pricing)
- [Plausible Self-Hosted](https://plausible.io/self-hosted-web-analytics)
- [Umami vs Plausible (OpenPanel)](https://openpanel.dev/articles/self-hosted-web-analytics)
- [Doppler vs Infisical](https://www.doppler.com/blog/infisical-doppler-secrets-management-comparison-2025)
- [v0 Review 2026 (Taskade)](https://www.taskade.com/blog/v0-review)
- [v0 Alternatives 2026 (Builder.io)](https://www.builder.io/blog/v0-alternatives)

---

**Devise IVIA : Au sein de l'être — En actes**

*Document préparé pour intégration au plan d'affaires MERLIN. Toute donnée chiffrée est une estimation basée sur prix publics 2026 en CAD ($1 USD ≈ $1,40 CAD au 7 mai 2026 — à raffiner avec taux du jour si nécessaire).*

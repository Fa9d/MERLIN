---
titre: PRD canonique — IVIA / MERLIN (Option 1)
id: IVIA-PRD-001
statut: active
couche: PROD
type: PRD
auteur: fondateur
date: 2026-06-26
version: 1.0
dépend_de: [ADR-0006, ADR-0003]
remplace: []
source_canonique: 00_GOUVERNANCE/IVIA_PRD_CANONIQUE_v1.0.md
---

# PRD canonique — IVIA / MERLIN

> **Source de vérité produit.** Aligné sur **Option 1 (ADR-0006)** : backend
> **Python/FastAPI**, frontend **statique vanilla `ivia_site_v2/`**, pipeline IA **en
> Python** (faster-whisper local — Loi 25). Le Next.js `09_app_ivia_merlin/` est **legacy
> archivé**. **Aucune migration Node/Prisma.**
>
> Réfs : `ARCHITECTURE.md`, `00_GOUVERNANCE/ADR/ADR-0006-…`, `CLAUDE.md`,
> `12_JURIDIQUE_AFFAIRES/IVIA_BP_FINANCEMENT_v2.4.md`.

---

## 1. Vision & posture

**IVIA accueille. MERLIN structure. MÉSANGES accompagne.** IVIA (`ivia.quebec`) est une
**maison du vivant** : un lieu d'accueil et d'accompagnement à l'écoute, **non clinique**.

**Posture non-médicale (opposable)** : pas de diagnostic, pronostic, prescription ni
décision clinique. Toute sortie orientée client suit la triade **Observation → Hypothèse →
Orientation**. Détection d'urgence → **escalade humaine immédiate**. Vocabulaire **Loi 21**
respecté.

## 2. Stack canonique (non négociable — ADR-0006)
- **Backend** : Python / FastAPI / SQLAlchemy / Alembic (migrations, head `0039`).
- **Frontend prod** : site **statique `ivia_site_v2/`** (HTML + Tailwind CDN), servi par nginx,
  consommant l'API (`https://api.ivia.quebec`).
- **IA** : **faster-whisper local** (transcription, données Québec) + API Anthropic (analyses,
  sous validation humaine).
- **Média** : LiveKit. **Infra** : Docker Compose, OVH VPS (Beauharnois).
- **Archivé** : `09_app_ivia_merlin/` (Next.js) — gelé, non servi, non développé.

## 3. Utilisateurs & rôles
`admin (admin_tech) > superviseur > praticien > client`, plus **prospect** (avant compte).
Un compte est admin via rôle, liste blanche courriel, ou drapeau `is_platform_admin`.

## 4. Parcours & surfaces (grammaire unique)
Quatre voies d'accompagnement, du public à l'espace connecté :
1. **Déposer** — enregistrement solo (asynchrone) ; 1ᵉʳ dépôt offert, puis offre payante.
2. **Rencontrer** — séance live avec un·e praticien·ne (réservation + paiement).
3. **Écrire** — journal client (privé ; nourrit la carte de vie).
4. **Voir** — carte de vie (lecture multidimensionnelle, axes de la doctrine).

**Entrée publique (magic link)** : `/rendez-vous` → `POST /public/intake/start` (orchestrateur :
Client + IntakeRequest + 3 consentements publics ; magic link 7 j si courriel) → `/activer?token`
→ `POST /public/activate/{token}` → JWT → espace.

## 5. Exigences fonctionnelles (existant en prod)
- **Intake public** + magic link (§4). **3 consentements** max en entrée publique.
- **Enregistrement solo** (`/me/recordings`) : capture navigateur → base64 → transcription
  faster-whisper en fond → relecture client. Interrupteur de facturation par offre (admin).
- **Séances** : réservation de créneaux, **hold/confirm**, paiement (Stripe) ; salle LiveKit ;
  transcription + note praticien (validation humaine).
- **Journal** + **carte de vie** + **progression** (espace client).
- **Console admin** : comptes, demandes d'entrée (tri/vigilance), facturation (interrupteurs),
  comptabilité (grand livre, exclut les paiements test), vue d'ensemble.
- **Paiements** : Stripe ; mode test (page simulée) si pas de clé ou `MERLIN_PAYMENTS_TEST_MODE`.

## 6. Profilage comportemental (feature EN PRÉPARATION — non exposée)
Bloc 5 couches (OCEAN, Schwartz, 8 Expressions, Attachement, VAD) + **matching** + **insights
LLM**. **Statut : barrière safety/security non levée** → migration `0039` **non appliquée**,
routes internes **non exposées au client**, insights Anthropic **désactivés** (`insights_enabled=False`).
Règle fondatrice : **un profil n'est jamais un diagnostic** (`profiling_safety_suite_v1`).
Blocants avant exposition : B1 (cadre transfrontalier + consentement), B2 (consentement à
l'écriture), B3 (surface client sans scores), B4 (post-filtre Loi 21 + triage urgence) — voir
`05_PREUVES_SOURCES/SECURITY_REVIEW_PROFILAGE_v1.0.md`.

## 7. Exigences non-fonctionnelles
- **Loi 25** : données hébergées Québec/Canada ; consentements **N1/N2/N3** (horodatés,
  révocables) ; connecteurs privés/internes ; aucun export tiers non encadré.
- **Loi 21** : vocabulaire filtré, triade obligatoire, escalade d'urgence.
- **Sécurité** : secrets en `.env.prod` (jamais en dur) ; auth JWT via backend ; rôles via
  `app/core/deps.py`.
- **Déploiement tracé** : `/opt/merlin` = checkout Git ; déploiement par `pull-deploy.sh` /
  `prod-up.sh` ; jamais `docker compose` sans `--env-file .env.prod`.
- **Qualité** : audits liens/JS à 0 avant commit frontend ; tests backend verts ; eval-driven
  dès qu'un comportement IA touche client/praticien.

## 8. Pilote
- **Démarrage prévu : juillet 2026** (cf. BP v2.4).
- Équipe : **David Phaneuf** (fondateur/dev) + **Praticienne A** et **Praticienne B**
  (**à confirmer** — noms non publiés tant que l'engagement n'est pas formalisé).
- Cible : **2 praticiennes actives minimum**, séances réelles, conformité consentements 100 %.

## 9. Hors périmètre (explicite)
- Migration Node.js / Prisma / Next.js (rejeté — ADR-0006).
- Développement dans `09_app_ivia_merlin/` (archivé).
- Exposition client du profilage/matching/insights tant que B1–B4 + validation humaine
  clinique/Loi 21 ne sont pas faits.
- Sortie du pipeline IA hors Python (résidence des données).

## 10. Références
- `ARCHITECTURE.md` · `CLAUDE.md` · `00_GOUVERNANCE/ADR/ADR-0006-…` · `ADR-0003`
- `12_JURIDIQUE_AFFAIRES/IVIA_BP_FINANCEMENT_v2.4.md`
- `00_DOCTRINE/correspondances-vivantes.md`
- `managed_agents/evals/profiling_safety_suite_v1.yaml` · `05_PREUVES_SOURCES/SECURITY_REVIEW_PROFILAGE_v1.0.md`

---

## Historique
| Version | Date | Auteur | Nature |
|---|---|---|---|
| 1.0 | 2026-06-26 | fondateur | Création — PRD canonique aligné Option 1 (ADR-0006) |

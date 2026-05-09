# Journal vague 9 — Branchement bout en bout pilote

**Date** : 9 mai 2026, soir (Montréal)
**Phase** : produit pilote (P1)
**Devise** : *Au sein de l'être — En actes.*

---

## Contexte d'ouverture

David a redirigé l'effort du légal vers le branchement produit. Objectif : un outil qui fonctionne end-to-end pour le pilote. Mails, transcription, funnel, paiement — tout branché.

---

## Découvertes majeures de la session

### 1. Production déjà déployée (ce que la doctrine n'avait pas tracé)

Test manuel `curl` sur les domaines :
- ✅ `https://ivia.quebec/` → HTTP 200, Next.js 16, nginx 1.27.5 OVH
- ✅ `https://api.ivia.quebec/api/health` → `{"status":"ok","service":"MERLIN API","environment":"production","database":"ok"}`
- ✅ `https://api.ivia.quebec/api/v1/praticiens` → 1 praticien en BD : David (`8dab08e6-27af-4195-a05a-ccc4ac1f2eac`)
- ✅ DNS pointe vers `137.74.42.121` (VPS OVH Beauharnois)
- ⚠️ `https://www.ivia.quebec/` → certificat SSL ne couvre pas le sous-domaine www (mineur, à corriger)
- ⚠️ `/docs` Swagger désactivé en production (normal sécurité)

**Conséquence** : le Sprint 2 ne part pas d'une feuille blanche, on enrichit une production saine.

### 2. Stack code ↔ doctrine — décalages

- **Transcription** : code = AssemblyAI / doctrine = Deepgram → décision godmode : **garde AssemblyAI**, MAJ doctrine v1.1
- **Email** : code = SMTP OVH / doctrine = Resend → décision godmode : **garde SMTP OVH**, MAJ doctrine v1.1

Documenté dans `04_METHODES/IVIA_STRATEGIE_TECHNOLOGIQUE_36MOIS_v1.1_ADDENDUM.md`.

### 3. Backend déjà très avancé

`10_backend_merlin_api/` contient :
- 19 routes API (auth, register, verify_email, clients, praticiens, bookings, schedules, sessions, audio_sessions, audio_recordings, session_notes, derived_documents, intake_requests, matching, consents, payments, health)
- 9+ migrations Alembic
- Services email, intake_analysis, livekit_audio, matching, session_documents
- Pipeline Anthropic Claude pour notes de séance
- Stripe intégré (45 $ CAD audio async par défaut)

Champs déjà présents dans modèle `AppUser` : `display_name`, `title_line`, `intro_text`, `presentation_audio_url`, `spoken_languages`, `available_channels`, `is_publicly_listed`. Bonus inattendu : `presentation_audio_url` était déjà prévu pour la voix.

### 4. Frontend Next.js déjà 18 pages

`09_app_ivia_merlin/src/app/` :
admin, audio-room, audio-test, checkout (success/cancel), démarche (415 lignes), espace-praticien, opérateur, praticien, praticiens (158 lignes), rendez-vous (confirmation/réserver), ressources, suivi, supervision, verify-email.

Page `/praticiens` actuelle = liste basique sans voix, sans cartes abstraites. C'est la cible de refonte Sprint 2.

---

## Actions effectuées cette vague

### Commits (chronologiques)

1. `2a8b898` — `feat(email)` mode pilote override Gmail (modifié `services/email.py`, ajout paramètre `audience`, headers X-IVIA-*, préfixe sujet `[PILOTE→original_email]`)
2. `5682f9b` — `voix pilote` 6 enregistrements David (poussés par David depuis VS Code)
3. `b7fe0c8` — merge auto résolution divergence
4. `b56bf5b` — `voix pilote` conversion MP3 96k + nommage doctrine + README

### Fichiers créés

- `00_DOCTRINE/IVIA_DOCTRINE_CARTE_ABSTRAITE_v1.0.md` (vague 8, 195 lignes)
- `04_METHODES/IVIA_SPEC_PAGE_PRATICIENS_v2.0.md` (vague 8, 1012 lignes)
- `04_METHODES/IVIA_DECISION_MOBILE_PWA_VS_NATIF_v1.0.md` (277 lignes — verdict PWA)
- `04_METHODES/IVIA_SPEC_PWA_v1.0.md` (1184 lignes)
- `04_METHODES/IVIA_FUNNEL_QUIZ_TO_GUIDANCE_v1.2_ADDENDUM.md` (148 lignes)
- `04_METHODES/IVIA_STRATEGIE_TECHNOLOGIQUE_36MOIS_v1.1_ADDENDUM.md` (alignement code)
- `04_METHODES/BRIEF_COPILOT_SPRINT_2_v1.0.md` (brief implémentation 7-8h)
- `ivia_mockups/assets/voix_pilote/` 6 MP3 (210-298 KB chacun) + README

### Voix pilotes — mapping personas fictifs

| MP3 | Persona | Style |
|---|---|---|
| `voix_01_presence_corporelle.mp3` | Aëlis | Corps & silence — voix posée, lente |
| `voix_02_mots_structure.mp3` | Naël | Parole & clarté — voix nette, articulée |
| `voix_03_frequence_vibration.mp3` | Sève | Fréquence & vibration — voix douce, ample |
| `voix_04_contemplation_ancrage.mp3` | Telma | Contemplation & ancrage — voix grave |
| `voix_05_energie_mouvement.mp3` | Nori | Énergie & mouvement — voix vive |
| `voix_06_deuil_transition.mp3` | Solène | Deuil & transition — voix retenue |

Durées : 17-25 secondes chacun, dans la cible 15-30s.

---

## Reste à faire (à briefer Copilot)

Brief complet : `04_METHODES/BRIEF_COPILOT_SPRINT_2_v1.0.md`

1. **Backend** : ajouter champs `abstract_palette`, `abstract_texture`, `abstract_motif`, `listening_modalities`, `pilot_persona_label` au modèle `AppUser` + migration Alembic
2. **Backend** : seed des 6 personas pilotes avec leurs voix
3. **Backend** : route `POST /api/v1/matching/recommend` (algo simple modalité ↔ besoin)
4. **Backend** : produit Stripe pilote 80 $ CAD 60 min (David crée price_id dashboard)
5. **Frontend** : composants `AbstractCardVisual`, `VoicePlayer`, `PraticienCard`, `PraticiensGrid`
6. **Frontend** : refonte `/praticiens` carte abstraite + lecteur voix
7. **Frontend** : étape recommandation au bout de `/demarche`
8. **Frontend** : copie voix dans `09_app_ivia_merlin/public/assets/voix_pilote/` (FAIT par Computer)
9. **Tests** : pytest + lint + build + smoke E2E
10. **Déploiement** : push origin master + pull VPS OVH + alembic upgrade + restart

---

## Décisions à escalader

1. **DPA AssemblyAI** : à signer avant onboarding premier client P2
2. **Domaine `www.ivia.quebec`** : ajouter au certificat SSL (1 ligne nginx ou Let's Encrypt)
3. **Stripe pilote price_id** : David doit créer manuellement dans dashboard Stripe
4. **Désactivation override** : prévoir un script ou config pour désactiver `MERLIN_PILOT_EMAIL_OVERRIDE` au passage P2

---

## Prochaine vague (vague 10)

Implémentation Copilot Sprint 2 (7-8h) → test E2E → onboarding premier client réel pilote.

---

*Au sein de l'être — En actes.*
*Pour le peuple, par le peuple.*

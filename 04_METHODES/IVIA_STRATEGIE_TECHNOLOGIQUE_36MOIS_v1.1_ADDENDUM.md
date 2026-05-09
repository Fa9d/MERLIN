# IVIA — Stratégie technologique 36 mois — Addendum v1.1

**Date** : 9 mai 2026
**Statut** : Addendum à `IVIA_STRATEGIE_TECHNOLOGIQUE_36MOIS_v1.0.md` (validé 7 mai 2026)
**Cause** : décalage doctrine ↔ code production découvert le 9 mai 2026
**Décision** : alignement de la doctrine sur le code réel (godmode David — souveraineté + simplicité)

---

## Décalages identifiés

| Domaine | Doctrine v1.0 | Code production | Décision v1.1 |
|---|---|---|---|
| **Transcription audio** | Deepgram Nova-3 | AssemblyAI | **Garder AssemblyAI** |
| **Email transactionnel** | Resend | SMTP OVH (`ssl0.ovh.net`) | **Garder SMTP OVH** |

---

## Décision 1 — Transcription : AssemblyAI plutôt que Deepgram

### Justification

Le code de `10_backend_merlin_api/app/services/livekit_audio.py` et le pipeline AI utilisent AssemblyAI depuis le démarrage. Migrer vers Deepgram représenterait :
- 8-15 jours de redéveloppement
- Re-signature DPA, re-tests qualité, re-calibration prompts
- Aucun gain qualité prouvé pour l'usage IVIA en français québécois (les deux fournisseurs sont à parité sur ce segment)

### AssemblyAI — points pour

- Universal-2 modèle multilingue avec excellente qualité française
- API stable, SDK Python mature
- Intégration speaker diarization native (utile pour séances duo)
- Tarification compétitive (~0.37 $/h transcription async)
- DPA disponible, conformité SOC 2 Type II
- Endpoint US par défaut — point d'attention Loi 25

### AssemblyAI — points d'attention (à mitiger)

1. **Localisation des données** : AssemblyAI traite les données aux États-Unis. Pas d'endpoint canadien à ce jour.
   - Mitigation : DPA signé, clause non-rétention, communication transparente dans CGU client + politique de confidentialité Loi 25.
   - Mention explicite dans `politique_confidentialite_loi25` : "La transcription audio est effectuée par AssemblyAI Inc. (États-Unis) sous DPA. Les fichiers audio sont supprimés après traitement."
2. **Évaluation annuelle** : revue à 12 mois (mai 2027) :
   - Déclencheurs migration : (a) Deepgram lance endpoint canadien, (b) Whisper open-source self-hosted atteint qualité production, (c) AssemblyAI augmente tarif > 50 %
3. **Continuité** : abstraction backend `app/services/transcription_service.py` permet swap fournisseur sans toucher au pipeline AI.

### Plan de migration éventuelle (M24-M36)

Identique à v1.0 mais cible : faster-whisper self-hosted OVH pour transcription async, AssemblyAI maintenu pour temps réel séance. Économies cibles à volume : 30-50 % coûts AssemblyAI.

---

## Décision 2 — Email : SMTP OVH plutôt que Resend

### Justification

Le code de `10_backend_merlin_api/app/services/email.py` utilise SMTP OVH (`ssl0.ovh.net:587` STARTTLS) avec le compte mail David. C'est :
- 100 % souverain Canada (OVH Beauharnois)
- Aucun fournisseur tiers américain dans le chemin email
- Coût marginal nul (compris dans hébergement OVH)
- Déjà fonctionnel en production avec authentification SPF/DKIM/DMARC OVH

### Resend — pourquoi NE PAS le choisir

- Fournisseur américain (San Francisco), Loi 25 contrainte additionnelle
- Coût récurrent : ~30-50 $/mois à volume IVIA pilote
- Avantages (analytics, templating React) ne compensent pas la complexité Loi 25
- Si besoin futur d'analytics email avancées : self-host Listmonk OVH

### SMTP OVH — limites assumées

1. **Volume** : ~250 mails/jour limite OVH (suffisant pilote, à monitorer si > 50 RDV/jour)
   - Mitigation Phase 2 : compte SMTP OVH Pro (1000/jour) ou self-host Postfix
2. **Analytics** : aucune (taux ouverture, clics non trackés)
   - Mitigation : ne pas faire d'email marketing IVIA. Email transactionnel uniquement = analytics inutiles.
3. **Templating** : HTML statique, pas de moteur React Email
   - Mitigation : Jinja2 templates suffisants pour le pilote. Migration possible vers MJML si besoin.

### Mode pilote en production (mai 2026)

Variables env actives sur VPS OVH :
- `MERLIN_PILOT_EMAIL_OVERRIDE=1`
- `MERLIN_PILOT_CLIENT_PRACTITIONER_EMAIL=davidphaneuf@gmail.com`
- `MERLIN_PILOT_ADMIN_EMAIL=lagent009@gmail.com`

Tous les emails transactionnels sont redirigés vers ces deux comptes Gmail tant que `MERLIN_PILOT_EMAIL_OVERRIDE=1`. À désactiver lors du passage en P2 (vrais clients, vrais praticiens).

---

## Mise à jour table risques fournisseurs (v1.0 §M.7)

| Fournisseur | Risque | Mitigation v1.1 |
|---|---|---|
| AssemblyAI (transcription) | Localisation US, dépendance forte | DPA + abstraction service + revue annuelle |
| SMTP OVH (email) | Volume 250/j, pas d'analytics | Suffisant pilote, plan Pro Phase 2 |
| Anthropic Claude (synthèse) | Localisation US, dépendance forte | Identique v1.0 (DPA + pseudonymisation) |
| OpenAI GPT-4.1 (analyse) | Localisation US, dépendance forte | Identique v1.0 (DPA + pseudonymisation) |
| Stripe (paiement) | Inchangé | Identique v1.0 |
| LiveKit + S3 OVH (audio storage) | Inchangé | Identique v1.0 |
| PostgreSQL OVH (BD) | Inchangé | Identique v1.0 |

---

## Cohérence documentaire — fichiers à mettre à jour

À MAJ dans une vague suivante (pas bloquant pour Sprint 2) :
- `politique_confidentialite_loi25` — remplacer "Deepgram" par "AssemblyAI", "Resend" par "SMTP OVH"
- `cgu_clients` — idem
- `cartographie_risques` — table fournisseurs alignée v1.1
- `manuel_operations_pilote` — section "configuration emails pilote" + override Gmail
- `note_confidentielle_investisseurs` — pile technique alignée

---

## Statut

- ✅ Décisions actées godmode David (9 mai 2026)
- ✅ Code aligné production (commit `2a8b898` mode pilote email)
- ⏳ Documents satellites à MAJ vague suivante
- ⏳ DPA AssemblyAI à signer formellement avant onboarding premier client réel P2

**Prochaine revue** : 9 mai 2027 (M+12).

---

*Au sein de l'être — En actes.*

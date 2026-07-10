# DÉCISION — Mode autonome, extension à la séance enregistrée (reflet de séance)

**Statut** : actée — décision fondateur 2026-07-10
**Étend** : `IVIA_DECISION_MODE_AUTONOME_JOURNAL_v1.0.md` (2026-07-09)
**Portée** : deuxième sortie IA→client sans validation praticien

---

## Décision

> « L'analyse doit être complète pour le client qui cherche simplement une
> analyse pure, sans contact avec un humain — simplement ses propos, et
> avancer avec le compte rendu, sans contact humain direct. » (fondateur, 2026-07-10)

Le client autonome qui **enregistre sa voix** (séance solo / express, avec
`consent_recording` + `consent_transcription`) peut demander un **reflet de
séance** : une lecture directe de ses propres propos transcrits, livrée sans
praticien.

## Ce que c'est / ce que ce n'est pas

- C'EST une restitution client en triade **Observation / Hypothèse /
  Orientation**, dans SES mots, au même ton doux que le reflet de journal.
- Ce N'EST PAS le compte rendu praticien (note de séance) : cette lecture
  professionnelle reste réservée au praticien et à la voie validée
  (`analysis_deliveries`). Aucun contournement de l'étape 4.

## Triple verrou (identique au reflet de journal)

1. Suite safety dédiée `seance_client_safety_suite_v1` **≥ 0.90** avant toute
   exposition client (registre `managed_agents/evals.registry.yaml`) ;
2. **Filtre Loi 21 EN CODE** sur toute la voix du reflet (échec = rien ne sort) ;
3. **Protocole d'urgence EN CODE** : signal détecté → ressources de crise
   (9-8-8, 8-1-1, 9-1-1) injectées serveur, analyse neutralisée.

## Gardes supplémentaires

- Prompt versionné **PROD-ANA-006** (`11_PROMPTS/07_analyses/PROMPT_reflet_seance_client_v1.md`) ;
- Capacité gouvernée `seance_reflet_client` (vanne profil×capacité, un clic admin) ;
- **Un reflet par enregistrement** (idempotent) + plafond quotidien global des insights ;
- Sa matière seulement : l'enregistrement doit appartenir au client connecté ;
- Aucun contenu de transcript dans les logs ;
- Les tiers nommés dans ses propos ne reçoivent aucune hypothèse.

## Traçabilité

- `AnalysisResult` capability=`seance_reflet_client` (sensibilité `hypothese`) ;
- coût réel au grand livre (`llm_usage_events`, purpose=`seance_reflet_client`) ;
- re-run de la suite OBLIGATOIRE à chaque bump du prompt (§8.3 CLAUDE.md).

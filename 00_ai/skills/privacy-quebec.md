# Skill — privacy-quebec

> À charger dès qu'on touche à de la donnée client, journalisation, intégration tierce, ou sortie IA.

## Cadre légal applicable

- **Loi 25** (Québec) — protection des renseignements personnels dans le secteur privé.
- **LPRPDE** (fédéral) — applicable en complément.
- MERLIN traite des données **de santé mentale** : sensibilité maximale.

## Règles absolues

1. **Aucune donnée client réelle dans les tests, fixtures, screenshots, logs commités, ou prompts versionnés.** Toujours des données fictives.
2. **Aucune donnée sortante vers un service tiers non explicitement autorisé.** Liste autorisée actuelle :
   - **Anthropic API** (Claude haiku/sonnet) — connecteur IA validé.
   - **LiveKit auto-hébergé / privé** — audio/vidéo.
   - **AssemblyAI** — transcription, sous contrat.
   - **Hébergement OVH (VPS Québec)** — infrastructure.
3. **Connecteurs non autorisés** (ne pas réintroduire) : Supabase, Whisper hosted, Speechmatics, ou tout SaaS sans contrat de traitement de données conforme Loi 25.
4. **Localisation des données** : préférer hébergement Canada/Québec. Si une donnée transite par les US (ex: Anthropic), elle doit être **dépourvue d'identifiants directs** et l'usage doit être documenté.
5. **Sortie IA** : jamais archivée comme vérité clinique sans **validation humaine**. Un flag `Sécurité` à priorité HAUTE déclenche escalade immédiate.

## Vérifications avant commit

- [ ] Pas de `nom`, `prénom`, `NAM`, courriel, téléphone réel dans le diff.
- [ ] Pas de `.env*` contenant des secrets — seul `.env*.example` est commitable.
- [ ] Pas de URL/clé d'un service tiers non listé ci-dessus.
- [ ] Pas de log incluant un payload complet de patient/usager.

## Vérifications avant intégration d'un nouveau service

1. Le service est-il sur la liste autorisée ? Si non, **stop**, demander à l'humain.
2. Données traitées : type, sensibilité, durée de rétention.
3. Localisation des serveurs.
4. Contrat / DPA en place ?

## Anti-patterns observés

- Logger un objet `user` ou `patient` complet pour debug → masquer ou ne logger que l'ID.
- Mettre un vrai numéro de dossier dans un commit de doc.
- Tester une intégration en pointant vers un endpoint de prod avec données réelles.

## Référence

- `12_JURIDIQUE_AFFAIRES/` — documents stratégiques (lecture seule pour agents code).
- `00_GOUVERNANCE/` — décisions liées à la confidentialité.

# IVIA — Cadrage du chantier « Analyses · Journal · Restitutions »

**Version** : v1.4 — 2026-07-08 (v1.0 : cadrage initial ; v1.1 : décision fondateur §6 ;
v1.2 : étape 1 livrée ; v1.3 : étape 2 livrée ; v1.4 : étape 3a livrée —
sémantique de séance ; croisement prosodie/sémantique restant en 3b)
**Statut** : canon (cadrage validé à faire vivre ; toute évolution bumpe la version)
**Auteur** : Claude Code (Fable 5), sous directive de David Phaneuf (2026-07-07)
**Références** : `05_JOURNAUX/JOURNAL_reunification_depot_20260708.md`,
`app/services/capability_gate.py` (décision fondateur 2026-07-04 « moteur plein /
vannes par profil »), `00_DOCTRINE/correspondances-vivantes.md`.

---

## 1. Directive fondatrice (2026-07-07)

> « L'analyse complète des séances et des enregistrements. La gestion, la
> structuration et l'intégration aux analyses des éléments du journal entre les
> séances — le journal doit être écrit. Coordonner ces analyses et la
> représentation des données pour tout acte, client ou praticien. Fournir
> l'analyse du praticien lorsqu'il procède à des entretiens avec ses clients. »

Traduction opérationnelle : un **cycle vivant** où chaque séance nourrit le
journal, le journal nourrit la séance suivante, et les deux nourrissent des
restitutions coordonnées — lecture client (triade O/H/O) et lecture praticien
(analytique, sous vanne).

## 2. Ce qui existe déjà (inventaire du code, vérifié 2026-07-08)

### Capture & analyse de séance
- Enregistrements LiveKit + solo (`me_recordings`, `audio_recordings`) ;
  transcription **locale** faster-whisper (`services/transcription.py`, Loi 25).
- **Prosodie locale automatique post-transcription** (`services/prosody.py`,
  déclenchée dans `services/livekit_audio.py`) — niveau `observation` :
  débit, pauses, F0, énergie. L'audio ne quitte jamais le serveur.
- **Moteur d'analyse** (`models/analysis.py`, migration 0047) : résultats
  versionnés, sensibilités `observation → hypothese → inference_clinique →
  recherche`, accès journalisés (`analysis_access_logs`).
- **Vanne de capacités** (`services/capability_gate.py`) : catalogue versionné
  en code (`prosody_local`, `emotion_saas`, `semantic_llm`,
  `semantic_embeddings`, `behavioral_profiling`, `societal_aggregation`,
  `carte_de_vie`) × profils (`ivia_quebec_client`, `praticien_certifie`,
  `recherche_societale`) ; réglable en un clic (`/admin/analysis`).

### Journal & continuité entre séances
- **Journal structuré** (`client_journal_entries`, migration 0049) :
  nature (`libre|checkin|exercice|moment`), axes MERLIN (`dimensions`),
  phase (`avant|apres|entre` séance), ancrage biographique
  (`client_life_events`), ton émotionnel, `structured_payload`.
- **Intentions client** (`client_intentions`, migration 0050) + vue équilibre
  (projection doctrine 11 axes → 4 voies).
- Ancrages temporels de séance (`session_temporal_anchors`, migration 0045),
  contextes d'époque (`era_context`), carte de vie praticien (upsert
  `PUT /analysis/clients/{id}/carte-de-vie`, niveau `hypothese`).

### Restitutions
- **Notes de séance** (`session_notes`, migration 0046) : rédaction praticien,
  validation, livraison client via `me_documents` (document dérivé + note
  validée uniquement).
- Lecture des analyses par séance/client filtrée par la vanne
  (`GET /analysis/sessions/{id}`, `GET /analysis/clients/{id}`) ;
  droits de transmission (`GET /analysis/transmission-rights` —
  inférences cliniques transmissibles au client par les seuls praticiens
  `recognized_by_order`).
- Espace client : Mes enregistrements, Mes résumés, Ma progression
  (données réelles), vue équilibre.

## 3. Les flux manquants (l'objet du chantier)

| # | Flux | État |
|---|------|------|
| A | **Journal → analyse** : rien n'analyse les entrées de journal ; aucune synthèse inter-séances ne prépare la séance suivante | À construire |
| B | **Sémantique de séance** : `semantic_llm` et `semantic_embeddings` sont déclarées au catalogue mais **sans service implémenté** (seule la prosodie produit) | À construire |
| C | **Préparation d'entretien praticien** : pas de dossier agrégé (intentions actives + journal depuis dernière séance + analyses + dernière note) au moment où le praticien reçoit | À construire |
| D | **Représentations coordonnées** : lectures client et praticien produites indépendamment, pas depuis une même source de restitution | À unifier |

## 4. Découpage en étapes livrables

### Étape 1 — Dossier de préparation d'entretien (praticien) — *agrégation pure*

> **LIVRÉE 2026-07-08** : `GET /sessions/{id}/preparation`
> (`app/api/routes/session_preparation.py`) + page `praticien/preparation.html?session=<id>`
> + 4 tests de gardes (`tests/test_session_preparation.py`) + security-review passée sans
> trouvaille. Journal exposé UNIQUEMENT sous `consent_history` actif, quel que soit le rôle.
Nouveau `GET /sessions/{id}/preparation` : intentions actives, entrées de
journal depuis la dernière séance (**si consentement explicite**), dernières
analyses (filtrées vanne), dernière note validée, ancrages temporels.
Page praticien correspondante. **Aucune IA nouvelle** : lecture seule de
l'existant → livrable rapide, valeur immédiate. C'est la première réponse à
« fournir l'analyse du praticien lorsqu'il procède à des entretiens ».

### Étape 2 — Analyse du journal (capacité `journal_semantic`)

> **LIVRÉE 2026-07-08 (exposition praticien SEULEMENT)** : capacité au catalogue
> (`hypothese`, `data_leaves_server=True`), prompt `PROD-ANA-001` v1.0
> (`11_PROMPTS/07_analyses/`), service `app/services/journal_semantic.py`
> (consentement + fenêtre inter-séances + post-filtre Loi 21 + vigilance),
> route `POST /analysis/sessions/{id}/journal-synthese`, 5 tests mockés,
> suite `journal_semantic_safety_suite_v1` scaffoldée au registre.
> **Gate d'exposition client** : suite safety ≥ 0.90 requise avant toute surface client.
Nouvelle capacité au catalogue (max `hypothese`), service LLM interne
(Anthropic), prompt versionné dans `11_PROMPTS/` : synthèse des entrées
entre deux séances, axes MERLIN touchés, mouvements d'intention, signaux de
vigilance (→ escalade humaine). Sortie stockée comme `AnalysisResult` ;
côté client uniquement en triade O/H/O. **Safety suite obligatoire avant
toute exposition** (§8 CLAUDE.md).

### Étape 3 — Sémantique de séance + croisement prosodie/sémantique

> **3a LIVRÉE 2026-07-08 (exposition praticien SEULEMENT)** : capacité `semantic_llm`
> implémentée — prompt `PROD-ANA-002` v1.0 (`11_PROMPTS/07_analyses/`), service
> `app/services/session_semantic.py` (transcript tronqué avec marqueur au-delà de
> 30k caractères, verbatims fidèles, filtre Loi 21 sur la voix de l'analyse),
> route `POST /analysis/sessions/{id}/semantique`, 4 tests mockés, suite
> `session_semantic_safety_suite_v1` scaffoldée (gate client ≥ 0.90).
> **3b restante** : croisement prosodie/sémantique (`inference_clinique`,
> praticien vérifié) + `semantic_embeddings` locaux.
Implémenter `semantic_llm` sur transcript (thèmes, axes, triade) puis la
capacité de croisement (divergence dit/manière-de-dire, aplatissement vocal)
en `inference_clinique` — **réservée praticien vérifié**, journalisée.
`semantic_embeddings` locaux pour la recherche inter-séances (Loi 25).

### Étape 4 — Restitutions coordonnées (une source, deux lectures)
Un même `AnalysisResult` alimente : vue client (O/H/O, langage des
correspondances vivantes, jamais de scores bruts) et vue praticien
(analytique, tendances, timeline séances × journal). Dataviz sobres
(progression, équilibre 4 voies, continuité inter-séances).

### Ordre et dépendances
1 (immédiat, sans IA) → 2 (journal) → 3 (séance) → 4 (représentations).
Chaque étape : prompt versionné + evals safety ≥ 0.85 sur les 10 catégories +
`security-review` avant merge + journal `05_JOURNAUX/`.

## 5. Gardes-fous non négociables (rappel constitution)

- Triade **Observation / Hypothèse / Orientation** sur toute sortie client ;
  jamais diagnostic/prescription ; vocabulaire Loi 21 filtré (`loi21_filter`).
- Signal d'urgence dans journal ou séance → **escalade humaine immédiate**,
  l'analyse ne poursuit pas.
- Accès praticien au journal : **consentement explicite du client**, tracé.
- Toute capacité `data_leaves_server=True` : validation fondateur préalable.

## 6. Point de vigilance relevé (anti-sycophantie)

Le profil `ivia_quebec_client` a **toutes les capacités actives par défaut en
phase test**, y compris `emotion_saas` (`data_leaves_server=True`,
sensibilité `recherche`). Le code le note lui-même : « à réévaluer avant mise
en marché ».

**Décision fondateur (2026-07-08)** : recommandation de désactivation
**refusée** — `emotion_saas` reste active par défaut en phase test. Le point
de contrôle demeure : réévaluation explicite des capacités
`data_leaves_server` avant mise en marché / premiers clients hors pilote.

## 7. Destination et circulation

Ce document est **canon** dans `00_GOUVERNANCE/`. Les étapes livrées seront
datées dans `05_JOURNAUX/` ; les prompts créés vivront dans `11_PROMPTS/`
(avec version) ; les capacités nouvelles s'ajoutent au catalogue en code
(`capability_gate.py`) et leurs evals dans `managed_agents/evals/`.

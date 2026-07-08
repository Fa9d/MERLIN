# JOURNAL — Moteur d'analyse « moteur plein / vannes par profil » — 2026-07-04

## Décision fondateur

David (2026-07-04) : implémenter le **maximum des capacités d'analyse** dès maintenant
(phase test), ajuster au moment de la mise en marché. Le modèle servira à terme à
d'autres projets (analyse sociétale) ; il faut pouvoir **valider/invalider en un clic**
chaque capacité selon l'utilisation. Pour IVIA (écoute enracinée), le champ d'action
reste limité selon les règles canadiennes/québécoises. Les praticiens **reconnus par
les instances appropriées** accèdent à toutes les informations du modèle et ne peuvent
les transmettre à leurs clients que s'ils sont reconnus.

## Architecture livrée

- **Moteur toujours à pleine capacité** — les sorties brutes sont stockées
  (`analysis_results`) avec un niveau de sensibilité :
  `observation` → `hypothese` → `inference_clinique` → `recherche`.
- **Vannes par profil** (`capability_gate.py`) — le filtrage se fait **à la lecture** :
  - `ivia_quebec_client` : Loi 25/21, plafond `hypothese`, `emotion_saas` OFF par défaut ;
  - `praticien_certifie` : plafond `inference_clinique`, toutes capacités ON —
    accordé automatiquement à tout praticien porteur d'un credential **vérifié** ;
  - `recherche_societale` : pleine capacité, SaaS externes autorisés.
- **Interrupteurs un-clic** : `GET/PATCH /api/v1/admin/analysis/capabilities`
  (matrice profil × capacité, persistée en DB, défauts en code).
- **Credentials praticiens** : `practitioner_credentials` (ordre, permis, statut,
  vérification admin, expiration). `recognized_by_order=True` = droit de **transmettre
  au client** des contenus `inference_clinique` (`can_transmit_to_client`).
- **Traçabilité** : tout accès à une sortie `inference_clinique`/`recherche` est
  journalisé dans `analysis_access_logs` (qui, quand, quel client, contexte).
- **Premier analyseur** : prosodie locale (`prosody.py`, librosa — l'audio ne quitte
  pas le serveur) : durée, ratio de pauses, pauses longues, F0 (moyenne/écart/étendue),
  énergie RMS, débit approx. `POST /api/v1/analysis/sessions/{id}/prosody`.

## Capacités au catalogue (capability_gate.CAPABILITIES)

`prosody_local` · `emotion_saas` (connecteur à brancher) · `semantic_llm` ·
`semantic_embeddings` (à brancher) · `behavioral_profiling` · `societal_aggregation`
(à brancher).

## Migration

`20260704_0047_add_analysis_engine` (idempotente) — 4 tables.
Image prod : + `ffmpeg` (décodage webm) + `requirements-analysis.txt` (librosa).

## Posture de conformité

La constitution (CLAUDE.md §6.4) continue de gouverner **les sorties client** du
profil `ivia_quebec_client`. L'accès praticien élargi est **plus** conforme à la
Loi 21, pas moins : les contenus réservés le sont à des professionnels dont la
reconnaissance par leur ordre est vérifiée et tracée. Chaque consultation sensible
laisse une trace d'audit — preuve de conformité au moment de la mise en marché.

## Suites

- Connecteur `emotion_saas` (Hume AI / autre) derrière la vanne — OFF pour IVIA Québec.
- Embeddings locaux (sentence-transformers multilingue) pour la recherche inter-séances.
- UI admin (matrice d'interrupteurs + gestion credentials) dans la console admin.
- Croisement prosodie × sémantique (divergences) en capacité `inference_clinique`.

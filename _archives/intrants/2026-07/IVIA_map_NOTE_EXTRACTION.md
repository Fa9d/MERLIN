# Note d'extraction — IVIA_map (intrant gelé le 2026-07-10)

**Origine** : dépôt concept pré-doctrine (`github Fa9d/_IVIA.map`) — README « RGNR »,
2 maquettes HTML (dashboards client/praticien), esquisse de pipeline audio (148 lignes,
jamais branchée). Conserve son propre `.git`.

## Ce qui en a été retenu (et où c'est allé)

1. **Boucle quotidienne côté client** (check-in → équilibre par axe → évolution 7 jours)
   → bande « Vos 7 derniers jours » ajoutée à `ivia_site_v2/client/ma-progression.html`
   (2026-07-10), calculée depuis le journal réel (axes MERLIN, pas RGNR).
2. **Vue d'ensemble praticien** → vue mensuelle ajoutée à `praticien/agenda.html`
   (basculement Semaine/Mois, 2026-07-10).
3. **Diarisation (SpeechBrain)** → idée notée pour le chantier 3c (embeddings/analyse
   locale par locuteur) — non implémentée, infra séparée.

## Ce qui a été explicitement écarté

- Vocabulaire contraire à la Loi 21 (« Thérapeute », « TCC », « ACT », « Burn-out
  prévention », « santé mentale ») — remplacé par le lexique des correspondances vivantes.
- Connecteurs tiers US (OPENAI_API_KEY, HUME_API_KEY) — contraires à la posture Loi 25.
- Branding « RGNR » — remplacé par les 11 axes MERLIN.
- Tout le code des maquettes (aucune reprise telle quelle).

Statut : **intrant consommé, gelé** (règle `.claude/rules/hygiene-sources.md`).
Ne pas rééditer sur place.

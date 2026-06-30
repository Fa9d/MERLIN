---
titre: Journal — Audit de base propre + décision noyau modulaire / bureau complet
id: JOURNAL-AUDIT-REFONTE-BUREAU-20260630
type: journal
couche: SYSTEME
date: 2026-06-30
auteur: fondateur + Claude Code
dépend_de: [ADR-0008, ADR-0004, ADR-0006, ADR-0007]
---

# Journal — Audit « base propre » et décision de refonte structurelle (2026-06-30)

> Append-only. Ce journal date un état et des décisions. Il ne remplace pas la doctrine
> (`00_DOCTRINE/`) ni l'ADR-0008 qui porte la décision d'architecture.

## 1. Point de départ — le constat

Sentiment de dispersion du fondateur. Cause réelle identifiée : non pas un manque de
contenu, mais une **absence de règle sur les sources**. Symptômes concrets :

- **Deux clones locaux** du même dépôt `Fa9d/MERLIN` : `C:/MERLIN` (ancien, racine
  encombrée, `.git` 201 Mo) et `C:/Dev/IVIA/MERLIN` (récent, plus propre, `.git` 165 Mo).
  → **Source unique retenue : `C:/Dev/IVIA/MERLIN`.** `C:/MERLIN` à abandonner.
- **Trois documents stratégiques qui se contredisent** (dans `PROD perplexity/`) :
  CAC/LTV (26 juin, SaaS B2B praticiens), synthèse concepts (moteur analytique ambitieux),
  recentrage (29 juin, offre solo). → traités comme **intrants**, à consommer puis geler.
- **12 branches distantes** (Frankenstein). Branche canonique = `refonte-ivia-site-unifie`
  (`origin/HEAD` pointe déjà dessus).

## 2. Audit lecture seule de `C:/Dev/IVIA/MERLIN`

- **~50 Mo de poids mort** : `09_app_ivia_merlin` (Next.js archivé ADR-0006, 47 Mo, non
  servi) + `.git` gonflé à 165 Mo (tarballs d'historique).
- **3 frontends concurrents** : `ivia_site_v2` (LIVE), `09_app_ivia_merlin` (Next.js gelé),
  `ivia_mockups` (maquettes HTML + scripts Python).
- **Plus grosse réserve de bruit** : `05_PREUVES_SOURCES` (401 fichiers), `DAVID_CORPUS`
  (16 Mo, 12 fichiers).
- **Sources canon qui se chevauchent** : `ARCHITECTURE.md`, `INDEX.md`, `CLAUDE.md` (33 Ko).

## 3. Décisions prises ce jour (validées fondateur)

1. **Niveau d'ambition** : bureau complet + architecture modulaire **maintenant** (pas
   l'offre solo minimale). Choix assumé. Voir ADR-0008.
2. **Next.js `09_app_ivia_merlin`** → **retiré du repo de travail** (l'historique Git le
   conserve). *Exécution en attente de validation finale du plan.*
3. **`ivia_mockups`** → **archivé** (`_archives/`). *Exécution en attente.*
4. **Gros intrants** (`DAVID_CORPUS`, `05_PREUVES_SOURCES`) → **archivés en bloc**
   (`_archives/intrants/`), triage fin ultérieur si besoin. *Exécution en attente.*
5. **Discipline anti-bordel** actée (3 classes : intrant / canon / dérivé ; une source
   canonique par fait ; Git = l'historique ; zéro `_v2`/`.bak`/orphelin). Voir ADR-0008.

## 4. Produits de cette session

- Ce journal (trace de l'audit).
- **ADR-0008** — noyau modulaire + bureau complet + objet d'analyse pluggable + deux
  contrats CARE (client/praticien) + loi de circulation des sources.
- **`11_PROMPTS/06_CSUITE/_anatomie-siege.md`** — gabarit d'un siège + table de circulation.

## 5. Reste à faire (non exécuté — attend validation du plan final)

- [ ] Exécuter le nettoyage par lots (retrait Next.js, archivage mockups + intrants,
      consolidation des scripts deploy racine, finalisation des 9 images supprimées).
- [ ] Consommer les intrants `PROD perplexity/` dans l'ADR/FIN/DATA puis les geler dans
      `_archives/intrants/2026-06/`.
- [ ] Restructurer l'arborescence cible (`noyau / bureau / contrats / instances`) —
      réconcilier avec ADR-0004 (normalisation arborescence).
- [ ] Hygiène Git : choisir et appliquer le nettoyage des ~11 branches non canoniques.
- [ ] Lot 3 (plus tard) : dégonflage `.git` (réécriture d'historique).
- [ ] Dégraisser `CLAUDE.md` (<200 lignes) une fois la nouvelle arbo en place.

## Historique

| Date | Auteur | Nature |
|---|---|---|
| 2026-06-30 | fondateur + Claude Code | Création — audit + décisions de refonte |

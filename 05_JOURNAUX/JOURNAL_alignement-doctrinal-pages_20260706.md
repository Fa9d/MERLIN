# JOURNAL — Alignement doctrinal des pages de destination

**Date** : 2026-07-06
**Auteur** : David Phaneuf + Copilot
**Références** : `00_DOCTRINE/correspondances-vivantes.md`, `00_DOCTRINE/ivia_living_lexicon.yaml`,
`09_app_ivia_merlin/CLAUDE.md` §4, `12_JURIDIQUE_AFFAIRES/IVIA_PLAN_MISE_EN_MARCHE_v1.0.md`
**Journaux précédents** : `JOURNAL_dossier-financement_20260706.md`, `JOURNAL_deck-marp_20260706.md`

---

## Contexte

Les 5 pages de destination par segment (`/attente`, `/ecoute`, `/travail`, `/proche`, `/employeurs`)
avaient été rédigées dans un registre de réponse directe (douleur → preuves → action) sans ancrage
explicite dans le lexique vivant, alors que la règle dure de `correspondances-vivantes.md` §4 exige :
« Tout copy frontend doit pouvoir s'y rattacher. »

## Décisions (validées par le fondateur)

1. **Voix de marque : tutoiement partout** — pages publiques ET réseaux sociaux.
   Justification : proximité, langage ordinaire, cohérence avec l'esprit du lexique
   (expressions telles qu'on les entend). Note : le lexique lui-même vouvoie dans ses
   `formulations_autorisees` (contexte de restitution praticien/IA) — cette différence de
   contexte est assumée : le tutoiement vaut pour le **marketing public**, le vouvoiement
   reste la norme des **restitutions client dans l'app**.
   **Mise à jour (même jour)** : le fondateur a statué que l'app passera **aussi au tutoiement**
   ultérieurement. Chantier reporté (todo `tutoiement-app`) : lexique vivant
   (`formulations_autorisees`, relecture humaine requise), prompts client de `11_PROMPTS/`
   (bump de version), espace client, puis passage de la safety suite.
2. **Ancrage lexique** — chaque page de destination cite 1 à 3 expressions du lexique vivant :
   - `/attente` → « ça va pas fort », « je pense trop », « j'ai besoin qu'on m'écoute »
   - `/ecoute` → « je fonctionne, mais… », « ça va, ça va très bien »
   - `/travail` → « je suis vidé·e », « je suis sur les nerfs », « j'ai peur de craquer »
   - `/proche` → « je veux aider, mais j'en peux plus »
   - `/employeurs` → sans ancrage (public organisationnel, pas personne en souffrance)
3. **Quatre voies d'accompagnement** — le bloc « Comment ça marche » de `/attente` reflète
   désormais accueil sans tri → écoute → lecture restituée + orientation.
4. **Triade explicite** — `/ecoute` expose la posture Observation / Hypothèse / Orientation
   en langage public.
5. **Couture des registres** — la phrase-manifeste de `pourquoi.html`
   (« l'entre-deux n'est pas un vide, c'est un espace qui mérite d'être habité »)
   est reprise dans le bloc Important de `/attente` pour relier les deux registres.

## Divergence corrigée au passage

« Tendre une porte » (métaphore fautive) → « ouvrir une porte » partout
(pages, publications réseaux, plan de mise en marché) — commit `c6d0239`.

## À surveiller

- Les futures campagnes payantes (plan de mise en marché §5) doivent puiser leurs accroches
  dans le lexique vivant — le lexique est le laboratoire du wording, l'organique son banc d'essai.
- Toute nouvelle page publique doit passer par cette grille : ancrage lexique + triade +
  urgence + tutoiement.

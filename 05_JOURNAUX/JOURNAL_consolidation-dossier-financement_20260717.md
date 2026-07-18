# JOURNAL — Consolidation du dossier de financement — 2026-07-17

## Contexte

Demande fondateur : reprendre le plan d'affaires, la demande de financement et les pièces
associées pour constituer un dossier complet et opérationnel, en intégrant le travail
réalisé depuis le 13 juillet (blogue, corpus de contenu d'acquisition — intrant `ivia-map`).

## Ce qui a été fait

### 1. Archivage des versions supersédées (loi d'hygiène des sources)

Déplacés vers `12_JURIDIQUE_AFFAIRES/ARCHIVES/` (suffixe `_archive`) :
`IVIA_BP_FINANCEMENT_v2.1/v2.2/v2.3`, `IVIA_PITCH_DECK_INVESTISSEURS_v1.0/v1.2/v1.3`.
Le canon vivant est désormais sans ambiguïté : **BP v2.4** et **deck v2.0**.

### 2. Références harmonisées sur BP v2.4

Corrigées dans : dossier volet social, plan de mise en marché, one-pager, coûts de
conformité, feuille de route innovation, trousse PME MTL, dossier volet commercial,
index base documentaire (00_GOUVERNANCE, entrée V1-08 → deck v2.0).

### 3. Trajectoire de portage propagée (BP v2.4 §2.1.0)

La séquence canonique — **entreprise individuelle → IVIA OBNL →
entité commerciale (SPA à mission, LSAQ)** — actée le 13 juillet, restait inversée
dans deux pièces du 6 juillet. Alignées :

- `IVIA_DOSSIER_VOLET_COMMERCIAL_v1.1.md` (bump v1.0→v1.1) — entité porteuse réelle,
  pivot recadré vers « constitution de l'entité commerciale après l'OBNL », pièces
  mises à jour (ajout note de demande + trousse PME MTL).
- `IVIA_ECHEANCIER_FONDATEUR_v1.1.md` (bump v1.0→v1.1) — phases 3-5 réordonnées :
  automne 2026 = préparation structuration (avocat, CA pressenti, lettres d'appui) ;
  hiver 2026-27 = constitution OBNL + premiers dépôts sociaux ; printemps 2027 =
  entité commerciale (roulement art. 85, licence sociale signée) + RS&DE/CRIC,
  fondations, tranche A1. Le garde-fou « pas d'OBNL avant l'inc. » (contraire à la
  décision du 13 juillet) est remplacé par « aucune forme revendiquée avant son
  existence ».

### 4. Traction depuis le 13 juillet intégrée

Corpus d'acquisition produit (intrant `ivia-map/content/`, dépôt externe) : 5 articles
de fond, 20 scripts vidéo courts, 2 séquences courriel, plan SEO 120+ mots-clés, meta
par page. Blogue intégré au site (`public/ivia-blog.html`, branche `feat/ivia-blog-deploy`),
**pas encore en production** — formulé partout comme « en déploiement », jamais « en ligne ».

Intégré dans : note de demande de financement v1.0 (§2), dossier volet commercial v1.1
(récit), trousse PME MTL v1.1 (stade du projet), plan de mise en marché v1.1
(bump v1.0→v1.1, bloc « État de réalisation » pilier organique).

### 5. Décision fondateur — immatriculation REQ fin juillet (2026-07-17)

Le fondateur choisit de **finaliser les documents sans NEQ** et de procéder à
l'immatriculation REQ (entreprise individuelle sous « IVIA », ~40 $, en ligne)
**d'ici fin juillet 2026**, avant le dépôt PME MTL de mi-août. Rappel juridique :
un travailleur autonome opérant sous son nom légal complet est exempté, mais
l'exploitation sous la marque « IVIA » et le dépôt PME MTL exigent le NEQ.

Formulation propagée — « immatriculation REQ prévue d'ici fin juillet 2026 » — dans :

- BP v2.4 (récit + tableau §2.1.0)
- Note de demande de financement v1.0 (§1, §5, §6)
- Dossier volet commercial v1.1 (entité porteuse)
- Trousse PME MTL v1.1 (admissibilité + premier geste)
- Trousse prospecteur v1.0 (objection « pas encore incorporé »)
- Échéancier fondateur v1.1 (nouvelle action 1.6, fin juillet)
- Contrat praticien type v1.1 (champ NEQ)
- Pitch deck v2.0 (4 occurrences) + source Marp `deck/IVIA_DECK_v2.0.marp.md`
- **Mentions légales v0.2 → v0.3** (bump : note de transition réécrite sur la
  trajectoire EI → OBNL → entité commerciale, éditeur = David Phaneuf TA,
  NEQ à venir) ; lien mis à jour dans l'audit gouvernance (§I1).

Rendus deck régénérés : `deck/IVIA_DECK_v2.0.html` + `.pdf` (Marp CLI, thème ivia).

## Garde-fous et points ouverts

1. **Loi 21 — vocabulaire de l'intrant `ivia-map`** : le contenu brut contient
   « thérapie », « thérapeute » (dont l'article 05 « Thérapie ou coaching » et la page
   blogue déployable `public/ivia-blog.html`, 5 occurrences). À trancher par le fondateur
   avant mise en ligne : conserver uniquement pour désigner les professions réglementées
   tierces (usage éditorial défendable), jamais l'offre IVIA. Garde-fou inscrit au plan
   de mise en marché v1.1. Noter aussi que le README d'`ivia-map` (positionnement
   « RGNR », clés OpenAI/Hume) ne fait pas foi — c'est un intrant, pas le canon.
2. **Champs administratifs bloquants** (note de demande §5-6) : NEQ (immatriculation REQ
   prévue d'ici fin juillet 2026) et code postal du siège. À compléter dès réception.
3. **Captures d'écran** du deck (`deck/LISTE_CAPTURES.md`) : toujours à produire.
4. **BP v3.0** : après premiers clients payants (inchangé).
5. **Intrant à geler** : quand le contenu d'`ivia-map` aura été consommé (blogue fusionné,
   contenus filtrés Loi 21 et publiés), geler la copie dans `_archives/intrants/2026-07/`
   conformément à la loi de circulation.

## Prochaine action réelle (échéancier v1.1, phase 1)

Des séances réelles et payées : 2 clés techniques (S3 OVH, secret `ANTHROPIC_API_KEY`),
test bout en bout, première séance payée. Puis dépôt PME MTL mi-août avec la trousse v1.1.

# Audit des repertoires (6 mois) — MÉSANGE vers MERLIN

Date: 2026-04-11
Statut: analyse de tri avant migration finale

---

## 1) Portee de l'audit

Repertoires compares:
- C:\MÉSANGE
- C:\Users\PC\Documents
- C:\Dev
- C:\CERCLE

Objectif:
- identifier sources actives, doublons, archives et dossiers satellites
- classer selon contribution au projet MERLIN
- preparer une migration one-way propre et decouplee

---

## 2) Constat global

1. Le workspace MÉSANGE actuel inclut des racines tres larges (`../Dev`, `../Users/PC/Documents`, etc.).
2. Plusieurs familles de projets existent en versions paralleles.
3. Les sources de verite ne sont pas uniformes selon les domaines.
4. La migration MERLIN doit etre pilotee par priorites et non par copie massive.

---

## 3) Classement par contribution a MERLIN

### A. Noyau critique (a integrer en priorite)

1. C:\MÉSANGE\00_PIVOT
- gouvernance, methode, cadrage, master plan
- contribution: tres elevee

2. C:\MÉSANGE\01_ROMAN
- corpus narratif et canon en cours
- contribution: elevee (pole diffusion/doctrine)

3. C:\Dev\ivia
- backend Python actif (emploi/soin)
- contribution: tres elevee (moteur)

4. C:\Users\PC\Documents\fa9_qc
- frontend/backend TS actif, point d'entree produit
- contribution: tres elevee (vitrine + parcours)

5. C:\CERCLE
- doctrine conceptuelle et structure analytique
- contribution: elevee (socle methodologique)

### B. Import methodique (utile mais a filtrer)

1. C:\Users\PC\Documents\Qc I\RECHERCHES (via dossier Desktop/Qc I actuellement monte)
- corpus livres/fiches/syntheses
- contribution: elevee pour fondements et nations
- action: importer par lots thematiques, pas en bloc

2. C:\Dev\ivia Qc
- contenus medias/politiques et strategie editoriale
- contribution: moyenne a elevee (pole citoyennete/diffusion)

3. C:\Users\PC\Documents\vibratoire
- historique et actifs soin
- contribution: moyenne (a trier avant integration)

### C. Doublons/parallelismes critiques (a arbitrer)

1. `ivia` duplique
- C:\Dev\ivia (HEAD plus avance)
- C:\MÉSANGE\ivia (HEAD plus ancien + suppressions locales)
- decision proposee: source canon = C:\Dev\ivia, C:\MÉSANGE\ivia en lecture/legacy

2. `ivia-app` / Pickleball duplique
- C:\Dev\ivia-app (git actif)
- C:\Users\PC\Documents\Pickelball (git actif, divergent)
- decision proposee: choisir un canon unique apres comparaison fonctionnelle

3. Roman duplique partiellement
- C:\MÉSANGE\01_ROMAN
- C:\Users\PC\Documents\TOME I
- decision proposee: source canon = C:\MÉSANGE\01_ROMAN, l'autre en import archive

### D. Archives/satellites (a isoler)

- C:\Dev\ivia-app-BACKUP-20260313
- C:\Dev\ivia-pickleball
- C:\Dev\ivia-pklb
- C:\Users\PC\Documents\OLD
- C:\Users\PC\Documents\PKLB_simple
- autres dossiers personnels non projet (images, musique, etc.)

Action: ne pas migrer par defaut; conserver hors noyau MERLIN.

---

## 4) Differences majeures constatees

### `C:\Dev\ivia` vs `C:\MÉSANGE\ivia`
- `C:\Dev\ivia` est en avance de commit sur la branche commune.
- `C:\MÉSANGE\ivia` contient des suppressions locales importantes (alembic notamment).
- risque: confusion sur la bonne base de deploiement.

### `C:\Dev\ivia-app` vs `C:\Users\PC\Documents\Pickelball`
- commits differents (divergence)
- etats de travail differents (modifs locales et suppressions differentes)
- risque: pertes/collisions si merge sans tri.

---

## 5) Risques detectes

1. Risque de source de verite multiple
- plusieurs versions actives d'un meme projet

2. Risque d'import bruit
- le montage de `C:\Users\PC\Documents` entier apporte des dossiers non strategiques

3. Risque de securite
- un repo backup contient une URL remote avec token integre (a revoquer immediatement)

4. Risque operationnel
- migration massive sans taxonomie = dette documentaire et gouvernance faible

---

## 6) Decisions proposees avant migration finale

1. Verrouiller les canons par famille:
- ivia: C:\Dev\ivia
- fa9_qc: C:\Users\PC\Documents\fa9_qc
- roman: C:\MÉSANGE\01_ROMAN
- gouvernance: C:\MÉSANGE\00_PIVOT
- doctrine: C:\CERCLE

2. Retirer les racines "fourre-tout" des workspaces d'operation.

3. Migrer par lots vers MERLIN:
- lot 1: fondements/gouvernance
- lot 2: emploi (ivia + fa9_qc)
- lot 3: nations et corpus
- lot 4: citoyennete/gouvernance avancee

4. Exiger un manifest de migration par lot.

---

## 7) Categorisation pratique pour MERLIN

### `A_MIGRER_IMMEDIATEMENT`
- 00_PIVOT
- 01_ROMAN (parties canon/methodo)
- C:\Dev\ivia (docs + architecture + routes emploi)
- C:\Users\PC\Documents\fa9_qc (docs + architecture + emploi)
- C:\CERCLE (fichiers maitres)

### `A_AUDITER_AVANT_MIGRATION`
- C:\Users\PC\Documents\Pickelball
- C:\Dev\ivia-app
- C:\Users\PC\Documents\vibratoire
- C:\Dev\ivia Qc

### `A_ARCHIVER` (hors noyau MERLIN)
- backups et copies historiques
- dossiers personnels non projet

---

## 8) Prochaine action recommandee

1. Valider ce classement.
2. Geler les canons (par ecrit).
3. Lancer la migration one-way par lot 1 (fondements).
4. Ouvrir ensuite lot 2 (MERLIN EMPLOI).

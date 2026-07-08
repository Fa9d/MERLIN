# Loi de circulation des sources — toujours chargée

> Découle d'ADR-0008 §6. Gardée par le siège COS. Anti-bordel : empêche le retour des
> sources concurrentes, des doublons et des fichiers orphelins.

## Trois classes — tout fichier appartient à une seule
- **Intrant** : matière brute (docs externes, brainstorms). Consommé une fois, puis **gelé**
  dans `_archives/intrants/AAAA-MM/`. Jamais une source vivante, jamais réédité sur place.
- **Canon** : vérité vivante (ADR, doctrine, contrats, prompts, sièges). **Une seule par
  sujet**, versionnée dans le fichier.
- **Dérivé** : produit à partir du canon (code, site, docs générés). Jetable, reconstructible.

## Règles dures
1. **Un fait = une source canonique.** Pour recadrer : bumper la version du canon, ou marquer
   l'ancien `statut: superseded` + `remplace:` et le déplacer en archive. **Jamais** un doc à côté.
2. **Git est l'historique.** Zéro `_v2`, `_final`, `_old`, `.bak`, zéro fichier daté orphelin.
3. **Aucun orphelin.** Tout artefact produit a une destination déclarée (`11_PROMPTS/06_CSUITE/_circulation.md`).
4. **Intrants gelés.** Toute matière brute consommée part dans `_archives/intrants/`.
5. **Une source de travail.** Le dépôt canonique est `C:\_IVIA` (basculement acté le
   2026-07-08, voir `05_JOURNAUX/JOURNAL_reunification_depot_20260708.md`) ; branche
   `refonte-ivia-site-unifie`. L'ancienne copie `C:/Dev/IVIA/MERLIN` est gelée (lecture seule).

## Réflexe avant de créer un fichier
Demander : est-ce intrant, canon, ou dérivé ? Existe-t-il déjà une source canonique sur ce
sujet ? Quelle est sa destination dans la circulation ? Si pas de réponse claire → ne pas créer.

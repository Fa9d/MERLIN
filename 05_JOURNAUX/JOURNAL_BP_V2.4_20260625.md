# JOURNAL — IVIA_BP_FINANCEMENT v2.4

**Date** : 2026-06-25
**Opérateur** : David Phaneuf + Claude Code
**Fichier produit** : `12_JURIDIQUE_AFFAIRES/IVIA_BP_FINANCEMENT_v2.4.md`
**Source** : `12_JURIDIQUE_AFFAIRES/IVIA_BP_FINANCEMENT_v2.3.md` (copié à 100 %, puis modifications chirurgicales)
**Statut** : ✅ Terminé et vérifié

---

## Méthode
Copie intégrale octet‑pour‑octet du v2.3, puis application des seules modifications listées via script à assertions (chaque remplacement devait toucher exactement sa cible, sinon échec). Aucune partie du corps n'a été résumée, raccourcie ou omise.

## Comptes de lignes
- v2.3 : **1425** lignes
- v2.4 : **1438** lignes
- Delta **+13** : ajouts demandés (3 annexes = +6, bloc changelog v2.4 = +8, ligne contrôle documentaire = +1) **moins** la suppression des 2 descriptions personnelles de praticiennes (−2 nettes). Le corps reste intégral.

## Modifications effectuées

### 1. Page de garde
- L. 4 — `**Version** : 2.3 — …` → `**Version** : 2.4 — Mise à jour juin 2026 — suppression références praticiennes nommées, pilote redéfini juillet 2026, ajout 3 nouveaux documents de référence`
- L. 5 — `**Date** : 9 mai 2026` → `**Date** : 25 juin 2026`

### 2. Suppression des praticiennes nommées (Mylène / Émilie / praticiennes‑fondatrices)
- L. 194 (résumé exécutif) — « dès le 31 mai 2026 avec deux praticiennes‑fondatrices (Mylène, Émilie) déjà engagées » → « prévu juillet 2026 — praticiennes en cours de confirmation ».
- L. 285 (tableau readiness) — « Démarrage 31 mai 2026 : David fondateur + Mylène + Émilie identifiées et engagées » → « Démarrage prévu juillet 2026 : David fondateur + praticiennes à confirmer ».
- L. 607 (tableau acquisition) — « M1 (juin 2026) | 3 | Pilote David + Mylène + Émilie » → « M1 (juin 2026) | 2 | Pilote David + praticiennes à confirmer ».
- §12.1 (Équipe pilote) — les **deux blocs descriptifs personnels** (### Mylène … / ### Émilie …, profils de présence + rôles) remplacés par un bloc unique « ### Praticiennes pilotes — à confirmer (juillet 2026) » + ligne neutre.
- §12.2 (objectifs) — « Praticiens actifs | 3 | 3 » → « Praticiens actifs | 2 (min.) | 3 » (applique « 3 praticiens actifs → 2 praticiens actifs minimum »).
- §12.4 (conditions) — « Formation pilote Mylène + Émilie | À planifier | 15‑30 mai 2026 » → « Formation pilote praticiennes | À planifier | juillet 2026 ».
- **Vérification finale** : `grep` Mylène/Émilie/praticiennes‑fondatrices = **0 occurrence**.

### 3. Annexes (PARTIE XIII, §13.1) — ajout en fin de liste
- **Annexe 17** — `ARCHITECTURE.md` (racine) : Architecture plateforme évolutive MERLIN v1.0 (25 juin 2026).
- **Annexe 18** — `02_NATIONS_QC/LETTRE_INVITATION_COCONSTRUCTION_v1.0.md` : Lettre invitation co‑construction nations autochtones (25 juin 2026).
- **Annexe 19** — `12_JURIDIQUE_AFFAIRES/FINANCEMENT_PUBLIC_PROGRAMMES_2026.md` : Programmes financement public, 5 cibles 250‑430 K$ (25 juin 2026).

### 4. Changelog — bloc v2.4 ajouté AVANT l'entrée v2.2 → v2.3
Bloc « # CHANGELOG v2.3 → v2.4 » + 4 puces (suppression noms / pilote juillet 2026 / 3 documents / mise à jour date et version).

### 5. Cohérence de version (stamps)
- Ligne v2.4 ajoutée au tableau **CONTRÔLE DOCUMENTAIRE**.
- Pied de page : « *Version 2.3 — 9 mai 2026* » → « *Version 2.4 — 25 juin 2026* » ; « — Fin du document v2.3 — » → « v2.4 ».

## Écarts / notes au fondateur (à valider)
1. **Numérotation réelle ≠ numéros romains de la consigne** : dans le document, Annexes = **PARTIE XIII**, Changelog = **PARTIE XIV** (la consigne disait XII/XIII). Les modifications ont été appliquées **au bon emplacement selon le contenu**.
2. **Cohérence non listée mais appliquée** (jugée nécessaire pour un v2.4 propre) : ligne au contrôle documentaire + stamps de pied de page. À retirer si tu préfères un strict minimalisme.
3. **Laissés inchangés faute d'instruction explicite** (signalés) :
   - Titre « PARTIE XII — PILOTE OPÉRATIONNEL 31 MAI 2026 » et §12.4 « AVANT 31 mai 2026 » / « Statut au 8 mai 2026 » conservent les dates de mai. Si le pilote est officiellement juillet 2026, un passage de cohérence sur ces dates serait à faire (non demandé ici).
   - Ligne 607 : mois « M1 (juin 2026) » conservé (seul le compteur 3→2 et les noms ont été modifiés).
   - Page de garde « **Remplace** : BP_FINANCEMENT_v2.2 » conservé tel quel (le v2.3 lui‑même ne l'avait pas mis à jour).
4. **3 documents référencés non encore créés** : `ARCHITECTURE.md`, `02_NATIONS_QC/LETTRE_INVITATION_COCONSTRUCTION_v1.0.md`, `12_JURIDIQUE_AFFAIRES/FINANCEMENT_PUBLIC_PROGRAMMES_2026.md` — les annexes pointent vers eux ; à produire séparément.

## Suite — 3 documents d'annexe créés (même jour)
Les 3 documents référencés en Annexes 17‑19 ont été produits :
- `ARCHITECTURE.md` (racine) v1.0 — **factuel**, dérivé du repo (stack, données, évolutivité, posture non‑médicale).
- `12_JURIDIQUE_AFFAIRES/FINANCEMENT_PUBLIC_PROGRAMMES_2026.md` v1.0 — 5 cibles 250‑430 K$ ; **montants présentés comme cibles à valider** (fiscaliste/avocat), non confirmés.
- `02_NATIONS_QC/LETTRE_INVITATION_COCONSTRUCTION_v1.0.md` v1.0 — **BROUILLON à ne pas envoyer en l'état** ; posture humble/non‑appropriative (constitution), relecture autochtone requise avant tout envoi.

## Références
- Doctrine / conventions : `CLAUDE.md`
- Document source : `IVIA_BP_FINANCEMENT_v2.3.md` (conservé, non modifié)

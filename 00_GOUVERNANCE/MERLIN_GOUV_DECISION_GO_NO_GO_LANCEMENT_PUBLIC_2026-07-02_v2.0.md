# MERLIN — Décision GO/NO-GO lancement public v2.0

**Date** : 2026-07-02  
**Statut** : valide  
**Remplace** : `MERLIN_GOUV_DECISION_GO_NO_GO_PILOTE_FERME_2026-04-26_v1.0.md`  
**Auteur** : David Phaneuf  

---

## 1. Décision

> **GO — Lancement public encadré avec praticien pilote**

Ce GO couvre l'ouverture à de vrais utilisateurs via un praticien pilote identifié,
avec un suivi rapproché. Il ne couvre pas une diffusion large non accompagnée.

---

## 2. Grille d'évaluation (2 juillet 2026)

| # | Critère | Statut | Preuve |
|---|---------|--------|--------|
| 1 | **Prod tracée sur Git** | ✅ GO | VPS = commit `bf66da6`, `git diff` vide depuis le 22 juin |
| 2 | **API health production** | ✅ GO | `{"status":"ok","database":"ok"}` vérifié ce jour |
| 3 | **TLS valide** | ✅ GO | Let's Encrypt `ivia.quebec` + `api.ivia.quebec` — expire le 3 sept 2026 |
| 4 | **CI bloquant (lint + tests + DB)** | ✅ GO | `full-suite` Postgres bloquant depuis le 22 juin |
| 5 | **Sauvegarde locale active** | ✅ GO | `deploy/backup.sh` — dump DB + audios, rétention 7 j |
| 6 | **Mentions légales en ligne** | ✅ GO | `/mentions.html`, `/confidentialite.html`, `/cgu.html` — 200 en prod, liées depuis le footer |
| 7 | **Parcours public fonctionnel** | ✅ GO | `/rendez-vous.html` 200, magic link opérationnel (journal 22 juin) |
| 8 | **Espace client fonctionnel** | ✅ GO | `/mon-espace`, journal, séances, enregistrements — cf. commits espace juillet 2026 |
| 9 | **Posture non-médicale dans les textes** | ✅ GO | CGU + mentions : "non clinique, non médical, non urgence" — conforme constitution §6.4 |
| 10 | **Numéro urgence affiché** | ✅ GO | `1 866 APPELLE (277-3553)` dans le footer de chaque page |
| 11 | **Sauvegarde hors-site OVH** | ⚠️ CONDITION | À activer avant dépassement de 10 clients réels (voir `docs/ops-sauvegarde.md`) |
| 12 | **Safety suite CI** | ⚠️ CONDITION | Job commenté — activer dès que `ANTHROPIC_API_KEY` ajouté dans GitHub Secrets |
| 13 | **Recette audio** | ⚠️ PRUDENCE | Non stabilisée — ne pas mettre l'audio en avant dans le discours de lancement |
| 14 | **Données de test prod** | ⚠️ PRUDENCE | Nettoyer les comptes de test avant les premiers vrais clients |

---

## 3. Périmètre du GO

**Autorisé :**
- Ouvrir l'accès à **1 praticien pilote** + ses premiers clients réels
- Diffusion ciblée (bouche-à-oreille, 1 canal) — pas de campagne large
- Communication honnête : "plateforme en lancement" — pas "plateforme mature"
- Démonstrations encadrées

**Non autorisé (conditions non remplies) :**
- Diffusion large non accompagnée avant activation sauvegarde OVH
- Mise en avant de la fonctionnalité audio tant que la recette dédiée n'est pas bouclée
- Multiplication de nouveaux chantiers produit avant le retour du praticien pilote

---

## 4. Conditions à remplir avant 10 clients réels

1. **Sauvegarde hors-site OVH** — `docs/ops-sauvegarde.md` (créer conteneur BHS + clés S3 + passphrase)
2. **Safety suite CI** — décommenter job dans `.github/workflows/ci.yml` + ajouter secret `ANTHROPIC_API_KEY`
3. **Nettoyage comptes de test prod** — via console admin `/admin/accounts`

---

## 5. Prochaine étape immédiate

1. Identifier et contacter le praticien pilote (MES-007)
2. Ouvrir 1 canal de diffusion ciblé (courriel, réseau professionnel)
3. Activer sauvegarde OVH en parallèle

---

## 6. Verdict exécutif

> **GO pour un lancement public encadré avec praticien pilote et diffusion ciblée.**  
> **Conditions de progression vers l'ouverture large : sauvegarde hors-site + safety suite + retour pilote.**

# JOURNAL — Lancement public IVIA (2 juillet 2026)

**Type** : décision structurante + bilan opérationnel  
**Auteur** : David Phaneuf + Claude Code  
**Branche** : `agents/cleanup-production-workflow` → `refonte-ivia-site-unifie`  
**Références** : `00_GOUVERNANCE/MERLIN_GOUV_DECISION_GO_NO_GO_LANCEMENT_PUBLIC_2026-07-02_v2.0.md`

---

## Contexte

Session du 2 juillet 2026 — objectif : faire le ménage dans la prod et finaliser les fondations
pour démarrer l'entreprise. Trois phases exécutées en séquence.

---

## Phase 1 — Ménage repo + VPS ✅

**Repo :**
- Scripts de déploiement dépréciés → `deploy/ARCHIVES/`
- Logs de sprint mai 2026 (7 fichiers) → `05_JOURNAUX/ARCHIVES/`
- Images logo racine → `03_DESIGN/logos/`
- Scripts ad-hoc (`check_routes.py`, `write_pages.mjs`) → `tools/`
- Suppression `build_output.txt`
- Commit : `8062553` sur `agents/cleanup-production-workflow`

**VPS (`ubuntu@137.74.42.121`) :**
- Suppression `.env.prod.bak` et `.env.prod.bak-` (avril 2026, obsolètes)
- `git pull` via `deploy/pull-deploy.sh` → VPS aligné sur commit `bf66da6`
- Racine VPS propre

---

## Phase 2 — Stabilisation ✅ (bilan)

| Élément | État |
|---------|------|
| CI suite DB bloquante | ✅ Déjà actif depuis le 22 juin |
| TLS `ivia.quebec` + `api.ivia.quebec` | ✅ Valide jusqu'au 3 sept 2026 |
| Nginx config | ✅ Syntax OK |
| API health prod | ✅ `{"status":"ok","database":"ok"}` |
| Safety suite CI | ⏳ Commentée — nécessite secret `ANTHROPIC_API_KEY` GitHub |
| Sauvegarde hors-site OVH | ⏳ À activer avant 10 clients réels |

---

## Phase 3 — Lancement public ✅

**Pages légales vérifiées en prod (200) :**
- `https://ivia.quebec/mentions.html`
- `https://ivia.quebec/confidentialite.html`
- `https://ivia.quebec/cgu.html`
- Toutes liées depuis le footer + page inscription

**Décision GO/NO-GO formalisée :**
- Fichier : `00_GOUVERNANCE/MERLIN_GOUV_DECISION_GO_NO_GO_LANCEMENT_PUBLIC_2026-07-02_v2.0.md`
- Verdict : **GO lancement public encadré avec praticien pilote**

---

## Prochaines actions (non techniques, à initier par David)

| Priorité | Action |
|----------|--------|
| P1 | Contacter le praticien pilote (MES-007) |
| P1 | Activer sauvegarde hors-site OVH avant 10 clients réels |
| P2 | Ajouter secret `ANTHROPIC_API_KEY` dans GitHub → activer safety suite |
| P2 | Nettoyer comptes de test prod (console admin `/admin/accounts`) |
| P3 | Ouvrir 1 canal de diffusion ciblé (bouche-à-oreille ou courriel) |

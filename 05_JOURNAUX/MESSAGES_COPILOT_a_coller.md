# Messages Copilot — copier-coller dans VS Code

**Pour David** : ouvre VS Code, ouvre le panneau Copilot Chat, et colle UN des deux messages ci-dessous selon ce que tu veux faire en premier.

---

## Message 1 — Activer le mode pilote sur le VPS OVH (5 min)

```
@workspace pull la derniere version master.

Puis lis 05_JOURNAUX/PROCEDURE_VPS_OVH_pilote_email.md
et execute les etapes 1 a 7 sur le VPS OVH 137.74.42.121.

Tu connais mon SSH key et le chemin du projet sur le VPS.
Apres chaque etape critique (backup, edition .env.prod, restart),
confirme avant de continuer.

Quand tout est applique, fais un curl test sur api.ivia.quebec/api/health
et un vrai test fonctionnel: creer un compte test sur ivia.quebec/demarche
et verifier que le mail arrive sur davidphaneuf@gmail.com
avec le sujet prefixe [PILOTE -> ...].
```

---

## Message 2 — Lancer le Sprint 2 (7-8h Copilot autonome)

```
@workspace pull la derniere version master.

Puis lis ces 4 documents dans l'ordre:
1. 04_METHODES/BRIEF_COPILOT_SPRINT_2_COURANT.md (le brief principal a executer)
2. 00_DOCTRINE/IVIA_DOCTRINE_CARTE_ABSTRAITE_v1.0.md (anti-doctrine, INTERDITS)
3. 04_METHODES/IVIA_SPEC_PAGE_PRATICIENS_v2.0.md (spec UI detaillee)
4. ivia_mockups/assets/voix_pilote/README.md (mapping voix-personas)

Execute toutes les phases A a H du brief dans l'ordre.

Regles:
- Commits granulaires comme indique dans la phase H
- Push regulier (au moins apres chaque phase backend ou frontend)
- Si tu rencontres une ambiguite ou une erreur de schema,
  arrete-toi et ecris-moi avant de continuer
- Respecte ABSOLUMENT l'anti-doctrine (zero visage, zero photo, zero emoji)
- Les voix MP3 sont DEJA dans 09_app_ivia_merlin/public/assets/voix_pilote/
  (Computer les a copiees, ne les recopie pas)

Quand tu as fini les phases A-H locales, NE deploie PAS automatiquement
sur le VPS. Dis-moi que c'est pret a deployer et attends mon feu vert.

Lance-toi.
```

---

## Ordre recommandé

**1ER** : Message 1 (mode pilote) — c'est rapide (5 min) et ça permet de tester immédiatement avec les emails redirigés vers Gmail.

**2ÈME** : Message 2 (Sprint 2) — c'est long (7-8h Copilot), tu peux le lancer et aller dormir. Au réveil, tu reviens tester.

Si tu veux, **lance les deux dans des sessions Copilot Chat séparées** (panneau de gauche). Copilot peut faire les deux en parallèle puisque le mode pilote (Message 1) modifie seulement le VPS, et le Sprint 2 (Message 2) modifie seulement le code local.

---

## Si Copilot bloque

Cas 1 — il refuse SSH : "Copilot ne peut pas SSH directement, je vais le faire moi-meme avec ton aide etape par etape."
→ Dans ce cas, suis manuellement `05_JOURNAUX/PROCEDURE_VPS_OVH_pilote_email.md` (5 min copier-coller).

Cas 2 — il dit "le brief est trop long" :
→ Réponds : "Concentre-toi sur la Phase A puis Phase B. Quand c'est fait et commite, on enchaine Phase C."

Cas 3 — il pose une question sur les voix :
→ Réponds : "Les MP3 sont dans 09_app_ivia_merlin/public/assets/voix_pilote/voix_01_presence_corporelle.mp3 a voix_06_deuil_transition.mp3. Le mapping est dans le README a cote."

---

## En cas de pépin pendant ta nuit

Tu te lèves le matin, tu reviens, tu relances une session Computer en disant simplement :
"Ou en est on apres la nuit Copilot ?"

Computer relit l'historique git, vérifie la prod, te fait un bilan en 30 secondes.

---

*Au sein de l'être — En actes.*

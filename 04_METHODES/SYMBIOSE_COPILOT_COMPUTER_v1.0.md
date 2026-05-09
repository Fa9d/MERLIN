# SYMBIOSE COPILOT ↔ COMPUTER — Mode d'emploi

**Version** : 1.0
**Date** : 9 mai 2026
**Auteur** : Computer (Perplexity), pour David Phaneuf

---

## L'idée en une phrase

**Copilot dans VS Code** fait le travail répétitif et localisé (édition de code, build, tests locaux, commits). **Computer (Perplexity)** fait l'orchestration stratégique, la cohérence inter-documents, le déploiement, la QA visuelle. Tu navigues entre les deux selon le coût-token de l'action.

---

## Répartition naturelle des rôles

### Copilot fait mieux

- Édition ciblée de fichiers source (Python, HTML, CSS, JS)
- Refactoring local (renommage, déplacement de fonctions)
- Génération de boilerplate (nouvelles pages mockup, formulaires, composants)
- Fix de bugs simples (typos, liens cassés, erreurs de syntaxe)
- Tests unitaires locaux
- Lecture de stack traces et debug
- Commits Git granulaires

### Computer (Perplexity) fait mieux

- Cohérence inter-documents (BP ↔ pitch ↔ CGU ↔ protocole urgence ↔ site)
- Recherche web et collecte de données (INSPQ, CAMH, CNESST, etc.)
- Rédaction longue de documents stratégiques (briefs, analyses, plans)
- Production de visuels (screenshots, QA visuelle, comparaison desktop/mobile)
- Déploiement sur ivia.pplx.app (deploy_website + publish_website)
- Mémoire de la doctrine sur 5+ vagues
- Connecteurs externes (GitHub, futurs Notion/Stripe/etc.)
- Orchestration de tâches longues sans supervision continue

### Zone grise (à toi de choisir selon le coût)

- Refonte UX d'une page : **Copilot** si tu sais déjà ce que tu veux ; **Computer** si tu veux une analyse + recommandation + exécution
- Documentation : **Copilot** si c'est inline dans le code ; **Computer** si c'est un document standalone
- Tests bout-en-bout : **Copilot** en local ; **Computer** une fois déployé

---

## Le flux de travail recommandé pour le chantier en cours

### Étape 1 — Tu lances Copilot (maintenant)

Sur ta machine, dans VS Code :

```bash
# Cloner ou pull le repo MERLIN à jour
cd ~/projets/  # ou ton dossier habituel
git clone https://github.com/Fa9d/MERLIN.git  # première fois
# ou
cd MERLIN && git pull origin master  # mise à jour

# Vérifier que le site mockup est là
ls ivia_mockups/
cat ivia_mockups/README.md  # contexte pour Copilot
```

Puis dans VS Code, ouvre le repo et passe ces fichiers à Copilot dans son contexte :

1. **`04_METHODES/BRIEF_COPILOT_REFONTE_LANDING_LIENS_v1.0.md`** ← le brief des 5 chantiers
2. **`ivia_mockups/README.md`** ← architecture du site
3. **`ivia_mockups/pages_public.py`** ← source du landing
4. **`ivia_mockups/pages_client.py`** ← sources espace client
5. **`ivia_mockups/pages_praticien.py`** ← sources espace praticien
6. **`ivia_mockups/pages_admin.py`** ← sources espace admin

Prompt initial à Copilot (en français, copie-colle) :

> Tu travailles sur le site IVIA (mockup pilote). Lis d'abord `ivia_mockups/README.md` puis `04_METHODES/BRIEF_COPILOT_REFONTE_LANDING_LIENS_v1.0.md` qui détaille les 5 chantiers à mener. Commence par le **Chantier 1 (activation des 112 liens morts)**. Les sources à éditer sont dans `ivia_mockups/pages_*.py` — ne jamais éditer les `.html` générés. Après chaque modification, lance `cd ivia_mockups && python build_pages.py` pour régénérer, puis `python -m http.server 8000` pour tester sur http://localhost:8000. Signale-moi avant de passer au chantier suivant.

### Étape 2 — Test local en continu

Pendant que Copilot travaille, garde un terminal avec :

```bash
cd ivia_mockups
python -m http.server 8000
```

Et ton navigateur sur **http://localhost:8000/tests.html** pour entrer dans les espaces fictifs et tester chaque parcours.

**Parcours à valider** (après chaque chantier de Copilot) :

| Persona | Parcours minimal |
|---|---|
| Visiteur public | Index → CTA hero → audio-async → retour index |
| Camille (cliente) | tests.html → dashboard → lancer écoute → résumé exemple → journal → praticiens → paiement |
| Mylène (praticienne) | tests.html → dashboard praticien → audios à traiter → audio-traiter → agenda → mes offres |
| David (admin) | tests.html → dashboard admin → analytique → praticiens → audios → finance |

### Étape 3 — Copilot commit + push

Quand Copilot estime avoir fini un chantier, il commit avec un message clair :

```
feat(site): chantier 1 - activation 112 liens morts

- Footers internes (client/praticien/admin) -> liens vers ../mentions, etc.
- Sidebars Compte -> redirection vers parametres / abonnement
- Inscription/connexion/paiement -> liens CGU/confidentialite actifs
- Cards dashboard -> redirection vers outils existants
- Bouton lien magique -> simulation visuelle (alert + confirmation)
- Pages mockup creees : client/compte, client/mot-de-passe-oublie, praticien/compte

Verification : grep -rh 'href=\"#\"' --include=\"*.html\" -> 0 occurrences
Build OK, test local OK sur 4 parcours.
```

Puis `git push origin master`.

### Étape 4 — Tu me pings quand un chantier est prêt

Tu reviens sur Computer (Perplexity) et tu me dis simplement :

> Chantier 1 fait, push sur master. Pull et redéploie sur ivia.pplx.app.

Ce que je fais alors :
1. `git pull origin master` dans mon workspace
2. Synchronisation `ivia_mockups/` (copie dans mon environnement de déploiement)
3. `python build_pages.py` (vérification que le build passe)
4. `deploy_website` puis `publish_website` avec le `site_id` existant (`95d9a5aa-bdb5-4aca-a524-dd62c489f205`)
5. **QA visuelle** : screenshots Playwright desktop (1280x900) + mobile (375x812) sur 6-8 pages clés
6. Vérification des parcours bout-en-bout en mode automatisé
7. Rapport visuel + diagnostic des restes éventuels

**Coût-token côté Computer** : limité (pas de rédaction longue, juste exécution + QA), donc pas de gaspillage.

### Étape 5 — Itération

Tu enchaînes les chantiers 2 → 3 → 4 → 5 avec Copilot, en m'appelant à chaque déploiement (ou tous les 2 chantiers si tu veux grouper).

---

## Règles d'or de la symbiose

### Règle 1 — Une seule source de vérité : `master` sur GitHub

Tout passe par le repo `Fa9d/MERLIN` (master). Pas de modifs en local non poussées qui se perdent. Pas de modifs Computer non poussées. **Je m'engage à toujours pull avant de redéployer**, et à push toutes mes modifs avant de te rendre la main.

### Règle 2 — Copilot ne déploie pas sur ivia.pplx.app

Le déploiement passe exclusivement par moi (Computer). Raison : le `site_id` est lié à mon environnement, et la QA visuelle automatisée tourne mieux ici. Si tu veux un environnement de staging séparé pour Copilot, on peut créer un sous-domaine `ivia-dev.pplx.app` plus tard.

### Règle 3 — Ne jamais éditer les `.html` générés

Toujours éditer les `pages_*.py`. Les `.html` sont régénérés par `build_pages.py`. Ce point est rappelé en gras dans le `README.md` et dans le brief Copilot.

### Règle 4 — Communication claire entre nous deux

Quand tu me ping après Copilot, dis-moi :
- Quel chantier est fait
- Si Copilot a rencontré des blocages ou pris des libertés
- Si tu veux une QA approfondie ou juste un déploiement express

Quand je te rends la main après déploiement, je te donne :
- Le lien vers la page modifiée
- Les screenshots
- Un avis franc (« le hero est bon » / « la section X a un problème de wrapping mobile »)
- La liste des points qui restent à reprendre (si pertinent)

### Règle 5 — Copilot peut me lire

Tous les briefs et la doctrine IVIA sont dans le repo (`04_METHODES/`, `00_GOUVERNANCE/`, `12_JURIDIQUE_AFFAIRES/`). Copilot peut s'y référer en autonomie. Si tu remarques que Copilot oublie un invariant doctrinal (couleurs interdites, ton, devises), pointe-lui le fichier concerné dans son contexte.

---

## Ce qui est sur GitHub maintenant (push 9 mai 2026, 13h)

5 commits poussés sur `origin/master` :

| Commit | Contenu |
|---|---|
| `9cecee3` | Site mockup `ivia_mockups/` (75 fichiers, 1.4 Mo) + README onboarding |
| `5bb2540` | Brief Copilot refonte landing v1.0 |
| `5bbd963` | Brief partenariats institutionnels v1.0 (CIUSSS / employeurs / fondations) |
| `2b74837` | Chantiers 1+4 doctrine : pitch v1.1, BP v2.2, protocole urgence v1.1, CGU clients v1.2, CGU praticiens v1.2 |
| `a4f6fb1` | Corpus de preuves comportements + synthèse maître v1.0 |

**Repo** : `https://github.com/Fa9d/MERLIN` (privé)
**Branche** : `master`

---

## Limite à connaître

Le déploiement sur ivia.pplx.app reste centralisé chez Computer. Si tu veux une autonomie totale côté Copilot (déploiement + tests visuels), il faudra :
- Soit configurer un environnement de déploiement Vercel/Netlify directement depuis le repo GitHub
- Soit créer un compte de service Perplexity pour Copilot (pas évident, à explorer)

Pour l'instant, le flux **Copilot édite → Computer déploie** est le plus économe et le plus fiable.

---

**Au sein de l'être — En actes.**

*Mode d'emploi v1.0 — 9 mai 2026*
*David Phaneuf, fondateur IVIA*
*Préparé par Computer (Perplexity)*

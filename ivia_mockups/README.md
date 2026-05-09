# IVIA — Site mockup pilote

**Version** : Vague 9 — 9 mai 2026
**Statut** : Mockup pilote, déployé sur https://ivia.pplx.app
**Stack** : Python 3.12 + HTML/CSS statique (pas de JS frontend, pas de framework)

---

## Architecture

Le site est **généré dynamiquement par des scripts Python**. **Ne jamais éditer les `.html` à la main** — toujours éditer les sources `pages_*.py` puis régénérer.

| Source Python | Pages générées | Rôle |
|---|---|---|
| `pages_public.py` | `index.html`, `comment.html`, `pourquoi.html`, `bibliotheque.html`, `urgence.html`, `mentions.html`, `confidentialite.html`, `cgu.html`, `tests.html` | Site public (landing + accès libre) |
| `pages_client.py` | `client/*.html` (21 pages) | Espace client·e (Camille en mode test) |
| `pages_praticien.py` | `praticien/*.html` (8 pages) | Espace praticien·ne (Mylène en mode test) |
| `pages_admin.py` | `admin/*.html` (7 pages) | Espace admin (David en mode test) |
| `pages_funnel.py` | (à vérifier) | Tunnel d'inscription |
| `articles_meta.py` | (métadonnées) | Métadonnées des 16 articles bibliothèque |
| `page_index.py` | (utilitaires) | Helpers de navigation |
| `build_pages.py` | (orchestrateur) | Point d'entrée du build |

### Articles bibliothèque

`articles_md/` contient 16 fichiers Markdown (`IVIA_ARTICLE_X_Y_v1.0.md`) qui sont injectés inline dans `bibliotheque.html` au build.

### Assets partagés

- `shared/public.css` — design system du site public
- `shared/coupe.css` — design system des espaces internes
- `assets/` — images statiques

---

## Comment générer le site

```bash
cd ivia_mockups
python build_pages.py
```

Cette commande :
1. Lit toutes les sources `pages_*.py` et `articles_md/*.md`
2. Génère/écrase tous les `.html` à plat dans `ivia_mockups/` et dans les sous-dossiers `client/`, `praticien/`, `admin/`, `demo/`

**Aucune dépendance npm ou autre.** Python 3 standard suffit.

## Comment tester en local

```bash
cd ivia_mockups
python -m http.server 8000
```

Puis ouvrir http://localhost:8000 dans un navigateur. Naviguer librement, cliquer sur tous les liens, observer les comportements.

**Page de test recommandée** : http://localhost:8000/tests.html — accès direct aux trois comptes fictifs (Camille / Mylène / David) sans authentification.

## Comment redéployer en production

Le déploiement sur https://ivia.pplx.app est fait depuis l'environnement Computer (Perplexity) par David, via les outils `deploy_website` + `publish_website` avec `site_id = 95d9a5aa-bdb5-4aca-a524-dd62c489f205`.

**Flux de symbiose** (recommandé) :
1. Copilot édite les sources Python en local
2. Copilot lance `python build_pages.py` puis `python -m http.server 8000` pour vérifier
3. Copilot commit + push sur la branche `master` (ou une feature branch)
4. David ping Computer (Perplexity) qui pull et redéploie

---

## Doctrine et invariants à respecter

### Couleurs CSS valides

Disponibles : `--color-creme`, `--color-aubergine`, `--color-rose`, `--color-rose-deep`, `--color-abricot`, `--color-miel`, `--color-mousse`, `--color-glacier`, `--color-lavande`, `--color-prune`.

**N'existent PAS** (ne jamais utiliser) : `--color-vert`, `--color-or`, `--color-bleu`.

### Typographies

- **Fraunces** (display, serif italique optique variable) — titres
- **Lora** (serif text, italique fin) — corps long, citations
- **Inter** (sans-serif variable) — UI, navigation, boutons

### Voix

- Français québécois exclusivement
- **Pas d'emoji**
- **Pas de point d'exclamation** (sauf ressource d'urgence où la concision impose un appel à l'action)
- Honnêteté radicale : nommer les limites d'IVIA aussi clairement que les forces
- Devises (à conserver en pied de page et dans les signatures) :
  - *Au sein de l'être — En actes.*
  - *Pour le peuple, par le peuple.*

### Promesse-cœur

> Quand tout se mélange, commencez par être entendu.

IVIA = espace d'écoute audio (rendez-vous direct OU différé 24-72h) + résumé écrit + 3 pistes concrètes + journal de vie. Pas un service d'urgence. Pas un service de psychothérapie. Pas un chatbot.

---

## Ressources d'urgence (à afficher de manière cohérente partout)

Cohérence stricte avec `IVIA_PROTOCOLE_URGENCE_DETRESSE_v1.1.md` (Partie III) et `IVIA_CGU_CLIENTS_v1.2.md` (article 9.4) :

| Population | Ressource | Numéro |
|---|---|---|
| Urgence vitale | Services d'urgence | 911 |
| Crise / suicide | Suicide Action Montréal / Ligne provinciale | 1 866 APPELLE (277-3553) |
| Soutien psychosocial 24/7 | Info-Social | 811 option 2 |
| Écoute générale | Tel-Aide Québec | 514 935-1101 |
| Crise Montréal | Centre de crise | 514 338-4090 |
| Orientation services | 211 Québec | 211 ou 211qc.ca |
| Jeunes | Tel-jeunes | 1 800 263-2266 / texto 514 600-1002 |
| Jeunes | Jeunesse, J'écoute | 1 800 668-6868 |
| 2SLGBTQ+ | Interligne | 1 888 505-1010 |
| Dépendances | Drogue: aide et référence | 1 800 265-2626 |
| Violence conjugale | SOS violence conjugale | 1 800 363-9010 |

---

## Brief de travail courant

Voir `04_METHODES/BRIEF_COPILOT_REFONTE_LANDING_LIENS_v1.0.md` (à la racine du repo MERLIN) pour la mission Copilot en cours :
- Chantier 1 — résoudre les 112 liens morts (`href="#"`)
- Chantier 2 — refonte du landing (un seul CTA, hero plus court, visuel SVG organique)
- Chantier 3 — cohérence des tunnels test (Camille / Mylène / David)
- Chantier 4 — exposer les 16 articles `.md` directement
- Chantier 5 — visuels SVG (hero, pictos, mini-cercle des 5 zones)

---

## Ne pas modifier sans coordination

- `articles_md/IVIA_ARTICLE_*.md` — contenu doctrinal, validé en Vague 7
- Les couleurs et la typographie du design system (`shared/public.css` et `shared/coupe.css`) — modification doit être validée avec David
- Le `site_id` Perplexity (déploiement)

---

**Au sein de l'être — En actes.**

*Site IVIA — Vague 9 — 9 mai 2026*
*David Phaneuf, fondateur*

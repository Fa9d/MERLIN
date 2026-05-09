# BRIEF COPILOT — Refonte landing IVIA + activation des liens

**Version** : 1.0
**Date** : 9 mai 2026
**Destinataire** : GitHub Copilot (mode auto, VS Code, repo MERLIN)
**Périmètre** : `ivia_mockups/` (site déployé sur https://ivia.pplx.app)
**Auteur du brief** : Computer (Perplexity)
**Mandat** : David Phaneuf, fondateur IVIA

---

## CONTEXTE

Le site IVIA (mockup pilote, ivia.pplx.app) présente deux problèmes bloquants pour un test bout-en-bout :

1. **112 liens morts** (`href="#"`) répartis sur 32 pages, principalement dans les footers, certaines sidebars « Compte », et quelques cards utilitaires.
2. **Landing peu attrayant** : pavé de texte dense, hero très long sans visuel, CTA double qui dilue l'action, pas d'image/illustration, hiérarchie verticale fatiguante.

David veut un site testable de bout-en-bout (côté client ET côté praticien) avec un message d'accueil simple et évident, fidèle à la doctrine IVIA :

> *« On est là pour proposer un service d'écoute et d'interprétation selon nos principes visant l'équilibre et la compréhension de ce qui se passe à un moment donné. Puis d'amener les gens vers l'indépendance et l'autonomie vitale. »*

---

## ARCHITECTURE DU SITE (à comprendre avant d'éditer)

Le site est **généré dynamiquement** par des scripts Python qui produisent les `.html` dans `ivia_mockups/`. **Ne pas éditer directement les `.html` générés** — éditer les sources Python.

| Fichier source | Pages générées |
|---|---|
| `pages_public.py` | `index.html`, `comment.html`, `pourquoi.html`, `bibliotheque.html`, `urgence.html`, `mentions.html`, `confidentialite.html`, `cgu.html`, `tests.html` |
| `pages_client.py` | `client/*.html` (21 pages) |
| `pages_praticien.py` | `praticien/*.html` (8 pages) |
| `pages_admin.py` | `admin/*.html` (7 pages) |
| `pages_funnel.py` | tunnel d'inscription (à vérifier) |
| `build_pages.py` | orchestrateur principal — appelé pour régénérer le site |

**Commande de build** : `cd ivia_mockups && python build_pages.py`

**Articles bibliothèque** : 16 fichiers Markdown dans `articles_md/` (`IVIA_ARTICLE_X_Y_v1.0.md`). Aujourd'hui ils sont injectés inline dans `bibliotheque.html` via ancres `#article-X_Y`. Quatre seulement ont un lien direct vers le `.md`.

**Espace tests** : `tests.html` propose trois comptes fictifs (Camille — cliente, Mylène — praticienne, David — admin) qui permettent d'entrer dans les espaces sans authentification. C'est la porte de test. Mais aujourd'hui les liens internes des espaces clients/praticiens/admin contiennent ~110 liens morts qui cassent l'illusion de réalité.

---

## OBJECTIFS

1. **Zéro lien mort** : tout `href="#"` devient soit un lien vers une page existante, soit un `<button>` avec un comportement (modale, alerte, scroll), soit un retrait pur si l'élément n'a pas de raison d'exister.
2. **Landing simplifié et attrayant** : un seul CTA principal, un visuel/illustration en hero, une promesse en trois mouvements (écouter · clarifier · marcher seul).
3. **Tunnels client + praticien testables bout-en-bout** : depuis `tests.html`, on doit pouvoir cliquer dans tous les sens sans tomber sur un cul-de-sac. Les pages mockup peuvent contenir des données factices, mais chaque action doit avoir un retour visuel.
4. **Footer unifié et fonctionnel** : 4 colonnes (Découvrir / Pratique / Mentions / Contact), tous les liens actifs.

---

## CHANTIER 1 — Activation des 112 liens morts

### 1.1 Footers internes (admin/, client/, praticien/) — 80+ occurrences

**Problème** : tous les footers des espaces internes ont `<a href="#">` pour Nous écrire / Mentions / Confidentialité / CGU.

**Action** : dans `pages_client.py`, `pages_praticien.py`, `pages_admin.py`, identifier la fonction qui génère le footer interne (probablement `_footer_interne()` ou équivalent). Remplacer par :

```python
# Liens depuis client/, praticien/, admin/ → remonter d'un niveau (../)
INTERNAL_FOOTER_LINKS = {
    "Nous écrire": "mailto:contact@ivia.quebec",
    "Mentions légales": "../mentions.html",
    "Confidentialité (Loi 25)": "../confidentialite.html",
    "CGU": "../cgu.html",
}
```

Si chaque module a sa propre fonction footer, harmoniser. Le test : `grep -rh 'href="#"' ivia_mockups/client/ ivia_mockups/praticien/ ivia_mockups/admin/` doit ne plus rien retourner sur ces 4 entrées spécifiques après build.

### 1.2 Sidebars « Compte » (admin/, praticien/) — 7 occurrences

**Problème** : la dernière entrée de sidebar (« Admin · D. Phaneuf », « Praticien·ne · Mylène ») pointe vers `href="#"`.

**Action** : transformer cette entrée en lien vers une page `compte.html` (à créer) OU vers `parametres.html` (existe déjà côté admin). Côté praticien, créer un `praticien/compte.html` minimal (nom, courriel, plan, déconnexion) ou rediriger vers `abonnement.html`.

Recommandation : pointer vers `parametres.html` (admin) et `abonnement.html` (praticien) — pas besoin de créer une nouvelle page.

### 1.3 Liens « CGU » et « politique de confidentialité » dans les formulaires d'inscription/paiement — 4 occurrences

**Fichiers** : `client/inscription.html` ligne 191, `client/connexion.html` ligne 162 (« Oublié »), `client/paiement.html` ligne 198 (« Détails »).

**Actions** :
- inscription.html : `href="../cgu.html"` et `href="../confidentialite.html"`
- connexion.html « Oublié » → créer un lien vers `mot-de-passe-oublie.html` (page mockup à créer, voir 1.6) OU au minimum un `<button onclick="alert('Lien envoyé à votre adresse courriel')">Oublié</button>`
- paiement.html « Détails » → ouvrir une modale CSS-only ou pointer vers une ancre `#details-paiement` avec les infos déployées

### 1.4 Cards utilitaires dashboard.html — 2 occurrences (lignes 156, 160)

**Action** : identifier ce que ces cards doivent montrer. Si ce sont des « raccourcis vers une action future », les pointer vers la page la plus proche (ex. `outil-ou-en-etes-vous.html`, `journal.html`, `audio-async.html`). Sinon, les retirer.

### 1.5 Connexion — bouton « Recevoir un lien par courriel » (ligne 171)

**Action** : transformer en `<button type="button" onclick="document.getElementById('lien-magique-confirme').hidden=false">` avec un message de confirmation caché juste en dessous : « Lien envoyé à votre adresse courriel (mockup — pas d'envoi réel) ».

### 1.6 Pages mockup à créer (3 pages)

Pour fermer les boucles :

- `client/mot-de-passe-oublie.html` — formulaire courriel + bouton « Recevoir un lien » avec confirmation visuelle. Style identique aux autres pages client/.
- `praticien/compte.html` — informations praticien, lien vers `abonnement.html`, bouton déconnexion (pointe vers `../tests.html`).
- `client/compte.html` — informations cliente, préférences notifications, bouton déconnexion (pointe vers `../tests.html`).

Toutes ces pages utilisent les fonctions existantes de mise en page (`_layout_client`, `_layout_praticien` ou équivalent) — pas de CSS nouveau.

### 1.7 Footer public (index.html, etc.) — vérifier déjà OK

Le footer public (vu dans `pages_public.py`) semble correct. Vérifier que tous les liens du footer sont actifs.

---

## CHANTIER 2 — Refonte du landing (`index.html` via `pages_public.py`)

### 2.1 Diagnostic actuel

- Hero textuel très long (4 phrases en gros, puis 3 phrases en sous-texte)
- Deux CTA côte-à-côte qui se concurrencent (« Commencer une écoute » + « Comprendre comment ça fonctionne »)
- Pas d'image, pas d'illustration, pas de respiration visuelle
- Sections suivantes correctes mais lourdes (3 portes, ce qu'IVIA est/n'est pas, 5 zones, 4 étapes, articles, confiance, urgence)
- Le scroll mobile fait 4500px+ — épuisant

### 2.2 Nouvelle structure proposée

**Hero (1 écran complet, ~95vh) — radicalement simplifié** :

```
[En haut]   IV I A    [nav minimaliste]   [☾ Mode calme]   [Espace tests]

[Centre, gauche]
  Petit chapeau : « Espace d'écoute · Québec »

  Un titre, deux lignes maximum :
    Quand tout se mélange,
    commencez par être entendu.

  Sous-titre, une phrase :
    Vous parlez. On vous écoute, on vous renvoie une lecture claire,
    et trois pistes concrètes pour avancer seul·e.

  [Bouton primaire grand]    Commencer une écoute  →
  [Petit lien sous bouton]   ou voir comment ça se passe

[Centre, droite — ou en arrière-plan flou]
  Un visuel d'accueil : forme organique douce (cercle qui respire,
  ligne d'onde audio stylisée, fond dégradé crème → rose pâle).
  PAS de photo de personne. PAS de stock. Une forme abstraite IVIA.

[Bandeau bas du hero]
  IVIA n'est pas un service d'urgence. Si vous êtes en détresse,
  composez le 9-8-8 (Canada · prévention suicide) ou le 911.
```

**Pourquoi cette structure** :
- Un seul CTA primaire — pas deux qui se concurrencent
- Le titre intègre déjà la doctrine : « tout se mélange » = état de manque de clarté (signal-pivot du Protocole urgence v1.1)
- Le sous-titre nomme la mécanique en trois temps (parler · lecture claire · pistes pour avancer seul) — c'est exactement la promesse de David : *« amener les gens vers l'indépendance et l'autonomie vitale »*
- Un visuel = repos visuel + différenciation versus apps santé mentale qui sont toutes en photos sourires

### 2.3 Sections suivantes — alléger, pas refondre

**Section 1 — Trois portes** : conserver mais raccourcir chaque carte à 2 lignes max (au lieu de 4-5 actuellement).

**Section 2 — Ce qu'IVIA est / n'est pas** : conserver telle quelle, c'est la signature honnêteté radicale.

**Section 3 — Cinq zones du cercle** : conserver mais déplacer après « Comment ça se passe » (ordre logique : action → mécanique → cadre conceptuel).

**Section 4 — Comment ça se passe (4 étapes)** : remonter avant les 5 zones. Cohérence : action → mécanique.

**Section 5 — Articles à lire** : conserver, c'est bien.

**Section 6 — Confiance / Loi 25** : conserver, c'est nécessaire.

**Section 7 — En détresse maintenant** : conserver, fusionner avec le bandeau footer si possible pour réduire le scroll.

### 2.4 Éléments visuels à ajouter

1. **Hero** : forme organique SVG inline (cercle qui pulse, ou onde audio horizontale). Aucune dépendance externe. Couleurs : aubergine, rose, crème.
2. **Trois portes** : remplacer les pictos texte (𝟍, 📖, ⊕) par 3 SVG simples cohérents (1 cercle plein, 1 livre ouvert, 1 spirale temporelle).
3. **Cinq zones du cercle** : ajouter un mini-cercle SVG visuel à gauche du tableau (5 secteurs colorés selon `--color-rose`, `--color-mousse`, `--color-glacier`, `--color-lavande`, `--color-abricot`).
4. **Comment ça se passe** : numéros des étapes en gros chiffres serif (Fraunces) plutôt que des bullets.

### 2.5 Mobile

Le hero doit tenir en moins de 90vh sur 375x812 (iPhone). Le sous-titre doit pouvoir être tronqué/élargi via media query.

---

## CHANTIER 3 — Cohérence du tunnel test (Camille → écoute complète)

Une fois entré comme Camille via `tests.html`, l'utilisateur doit pouvoir :

1. Voir son `dashboard.html` avec données pré-remplies
2. Cliquer sur **« Lancer une nouvelle écoute »** → arriver sur `audio-async.html`
3. Choisir le format différé OU rendez-vous → écran d'enregistrement (mockup, simulateur 60s)
4. Soumettre → `audio-attente.html` (« Votre écoute sera traitée sous 24-72h »)
5. Cliquer sur « Voir un exemple de résumé reçu » → `audio-resume.html`
6. Depuis le résumé, cliquer sur les pistes proposées → arriver sur `outil-ou-en-etes-vous.html`, `outil-frequence.html`, etc.
7. Aller dans `journal.html` → voir l'historique
8. Aller dans `praticiens.html` → choisir un·e praticien·ne → `paiement.html` → `confirmation-paiement.html`

**Action Copilot** : tester chaque étape de ce parcours, identifier les liens cassés ou les CTA absents, et corriger. Idéalement, ajouter un **petit bandeau « Mode démo »** en haut de chaque page interne quand on est dans le tunnel test, qui indique « Vous testez IVIA en mode démo · [Sortir du mode démo →] ».

### Tunnel praticien (Mylène)

Même logique. Depuis `tests.html` → entrer comme Mylène :

1. `praticien/index.html` (tableau de bord avec 3 audios à traiter)
2. Cliquer sur un audio → `audio-traiter.html` (timeline + transcription mockup + champ rédaction résumé)
3. Soumettre le résumé → retour sur `audios.html` avec l'audio marqué traité
4. Aller dans `agenda.html` → voir les rendez-vous
5. `clients.html` → fiche détail client
6. `mes-offres.html` → modifier ses tarifs
7. `outils.html` → voir les outils disponibles
8. `abonnement.html` → gérer son plan

### Tunnel admin (David)

Plus court mais doit aussi être fluide :

1. `admin/index.html` (vue d'ensemble)
2. `analytique.html` → graphes mockup
3. `praticiens.html` → liste + fiche
4. `clients.html` → liste + fiche
5. `audios.html` → audios en cours
6. `finance.html` → flux financiers
7. `parametres.html` → réglages plateforme

---

## CHANTIER 4 — Lien direct vers les articles `.md`

**Problème actuel** : la bibliothèque (`bibliotheque.html`) contient les 16 articles inline avec des ancres. Mais 4 articles seulement ont un lien `.md` direct (1.1, 2.2, 2.3, 4.4).

**Action Copilot** : dans `pages_public.py`, au sein de `build_bibliotheque()`, pour chaque article ajouter à la fin de l'article :

```html
<p class="article-source">→ Texte source : <a href="articles_md/IVIA_ARTICLE_{X}_{Y}_v1.0.md">IVIA_ARTICLE_{X}_{Y}_v1.0.md</a></p>
```

Pour que les visiteurs puissent télécharger / lire le markdown brut.

Vérifier ensuite que `articles_md/` est bien servi par le déploiement (il faut que `dist/public/articles_md/*.md` soit présent, ou que le déploiement copie ce dossier).

---

## CHANTIER 5 — Détail visuel landing (à exécuter avec le 2)

### 5.1 SVG hero

Créer un fichier `shared/hero-onde.svg` (ou inline) :

```svg
<svg viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;">
  <!-- Cercle organique qui respire (animation subtile) -->
  <defs>
    <radialGradient id="halo" cx="50%" cy="50%">
      <stop offset="0%" stop-color="var(--color-rose)" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="var(--color-creme)" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <circle cx="300" cy="200" r="160" fill="url(#halo)">
    <animate attributeName="r" values="160;170;160" dur="6s" repeatCount="indefinite"/>
  </circle>
  <!-- Onde audio stylisée -->
  <g stroke="var(--color-aubergine)" stroke-width="1.5" fill="none" opacity="0.6">
    <path d="M 120 200 Q 200 150, 280 200 T 480 200" />
    <path d="M 140 200 Q 200 180, 280 200 T 460 200" opacity="0.4"/>
  </g>
</svg>
```

### 5.2 Trois portes — pictos SVG

Remplacer les caractères Unicode actuels par 3 micro-SVG inline cohérents (cercle plein simple, livre ouvert simple, spirale).

### 5.3 Mini-cercle des 5 zones

Ajouter dans la section « Cinq zones » un SVG circulaire divisé en 5 secteurs de couleur (corps · relation · sens · ressources · fréquence). Pas de label sur le SVG (les labels sont dans le tableau à côté).

---

## ORDRE D'EXÉCUTION RECOMMANDÉ

1. **Chantier 1** (liens morts) — c'est la priorité. Sans ça, le test bout-en-bout est impossible. Estimation : 30-45 min.
2. **Chantier 4** (liens articles `.md`) — petit, peut être fait en passant. Estimation : 10 min.
3. **Chantier 3** (cohérence des tunnels) — vérifier chaque parcours, fixer les CTA manquants. Estimation : 30 min.
4. **Chantier 2 + 5** (refonte landing + visuels) — le plus créatif, à faire en dernier. Estimation : 1h-1h30.

**Total estimé** : 2h15 à 3h.

Après chaque chantier : `python build_pages.py` pour régénérer, puis vérification visuelle dans le navigateur local sur les pages clés.

---

## VALIDATION FINALE

Après tous les chantiers, faire tourner :

```bash
cd ivia_mockups
grep -rh 'href="#"' --include="*.html" | wc -l
# Attendu : 0
```

Et tester dans le navigateur :

1. Landing → cliquer le CTA → arriver sur `audio-async.html`
2. Depuis `tests.html` → entrer comme Camille → faire 5 clics aléatoires → ne jamais tomber sur une page blanche ou un cul-de-sac
3. Depuis `tests.html` → entrer comme Mylène → traiter un audio → revenir au dashboard
4. Depuis le footer de n'importe quelle page → cliquer Mentions / Confidentialité / CGU → arriver sur les bonnes pages

Une fois validé : redéployer via la commande de déploiement habituelle (David ou Computer Perplexity gère cette étape).

---

## RÈGLES DE STYLE (rappel)

- Variables CSS disponibles : `--color-creme`, `--color-aubergine`, `--color-rose`, `--color-rose-deep`, `--color-abricot`, `--color-miel`, `--color-mousse`, `--color-glacier`, `--color-lavande`, `--color-prune`. **N'existent PAS** : `--color-vert`, `--color-or`.
- Polices : Fraunces (display, serif), Lora (serif text), Inter (sans-serif).
- Pas d'emoji, pas de point d'exclamation dans les textes UI.
- Français québécois exclusivement.
- Devises IVIA en pied de page : *Au sein de l'être — En actes.* / *Pour le peuple, par le peuple.*

---

## ARTICULATION AVEC LES AUTRES DOCUMENTS IVIA

Ce brief est complémentaire à :
- `IVIA_PROTOCOLE_URGENCE_DETRESSE_v1.1.md` (les ressources urgence du landing doivent être cohérentes avec la Partie III mise à jour : 988, 911, 211, Tel-jeunes, Interligne, Drogue: aide et référence)
- `IVIA_CGU_CLIENTS_v1.2.md` (article 9.4 liste les ressources d'aide — la page urgence du site doit refléter exactement la même liste)
- `STRATEGIE_MARQUE_COMMUNICATION.md` v2.0 (ton, voix, devises)

---

**Au sein de l'être — En actes.**

*Brief Copilot v1.0 — 9 mai 2026*
*David Phaneuf, fondateur IVIA*
*Préparé par Computer (Perplexity)*

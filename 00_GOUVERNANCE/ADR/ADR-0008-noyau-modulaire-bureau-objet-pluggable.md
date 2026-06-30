---
titre: Noyau modulaire + bureau C-suite complet + objet d'analyse pluggable
id: ADR-0008
statut: active
couche: FOND
type: ADR
auteur: fondateur
date: 2026-06-30
version: 1.0
décideurs: fondateur
dépend_de: [ADR-0004, ADR-0006, ADR-0007]
remplace: []
remplacé_par: []
arbitrage_requis: oui — tout changement du noyau, de la liste des sièges, des contrats CARE, ou de la loi de circulation des sources
source_canonique: 00_GOUVERNANCE/ADR/ADR-0008-noyau-modulaire-bureau-objet-pluggable.md
---

# ADR-0008 — Noyau modulaire + bureau C-suite complet + objet d'analyse pluggable

> **Statut** : active — 2026-06-30
> **Couche concernée** : FOND
> **Documents liés** : `05_JOURNAUX/JOURNAL_AUDIT_REFONTE_BUREAU_20260630.md`,
> `11_PROMPTS/06_CSUITE/_anatomie-siege.md`, `11_PROMPTS/06_CSUITE/INDEX_CSUITE_V1.md`

---

## Contexte

Le projet souffrait d'un **excès de portée** et d'une **absence de règle sur les sources**,
pas d'un manque de contenu (cf. journal du 2026-06-30). Trois documents stratégiques récents
se contredisent : un modèle SaaS B2B praticiens (CAC/LTV), un moteur analytique ambitieux
(synthèse des concepts), et un recentrage sur une offre solo. En parallèle, six agents
C-suite ont été créés (`11_PROMPTS/06_CSUITE/` : STRAT, ARCH, COMM, UX, FIN, QA), mais sans
les sièges de mise en marché, de conformité et d'orchestration, et sans architecture qui
permette de faire évoluer le produit sans tout reconstruire.

Une décision de cadrage est nécessaire **maintenant** pour : (1) fixer le niveau d'ambition,
(2) poser une architecture modulaire opposable, (3) compléter le bureau de direction,
(4) instaurer une discipline qui empêche le retour du désordre documentaire.

---

## Options considérées

**Option A — Offre solo minimale d'abord, le reste plus tard**
Revenir à la boucle de service la plus simple (offre → réservation → paiement → séance).
*Rejeté* : choix de niveau d'ambition du fondateur, qui aurait pu livrer le solo depuis des
mois et ne le veut pas. Ne traite pas la modularité ni la dette structurelle.

**Option B — Repo neuf, reconstruction depuis zéro**
*Rejeté* : perte de la traçabilité Git, du backend et du site live, et de la doctrine. Risque
de casser la prod pour récupérer exactement les mêmes éléments.

**Option C — Noyau modulaire + bureau complet + objet d'analyse pluggable, par consolidation**
Garder le dépôt et son historique ; restructurer autour d'un noyau agnostique, d'un bureau
complet et d'instances ; figer une discipline de sources.
*Retenu* : préserve l'existant et l'historique, sert l'ambition complète, et rend le produit
extensible (multi-objets, multi-marchés) sans réécriture.

---

## Décision

1. **Noyau agnostique.** `MERLIN` est un **noyau d'analyse multidimensionnelle agnostique au
   domaine** (classer, situer, orienter, tracer). Il ne présuppose pas ce qu'il analyse.

2. **L'objet d'analyse est un paramètre, pas une constante.** Une **instance** lie le noyau à
   un objet d'analyse concret. `IVIA` est la **première instance**, avec **deux objets** :
   - objet = **CLIENT** (personne accompagnée) ;
   - objet = **PRATICIEN** (professionnel consentant qui lit sa propre pratique).

3. **CARE = contrat gardien lié à l'objet.** Chaque objet d'analyse a son **contrat CARE**, qui
   définit ses règles de sécurité, de vocabulaire, d'exposition et de propriété des données :
   - **CARE-client** : strict — non-clinique, Loi 21, triade Observation/Hypothèse/Orientation,
     scores **jamais** exposés au client, sensibilité haute.
   - **CARE-praticien** : réflexif — le pro voit **ses propres** patterns/angles morts,
     vocabulaire plus ouvert (auto-évaluation, recadrage), **donnée réflexive propriété du
     praticien**, jamais de notation opposable ni de surveillance sans consentement.
   Changer l'objet → changer le contrat CARE → le même noyau dessert un autre marché.

4. **Bureau C-suite complet (~11 sièges).** Existants : STRAT, ARCH, UX, QA, FIN, COMM.
   Ajoutés : **GROWTH** (mise en marché, actif), **LEGAL** (conformité Loi 21/25, actif),
   **COS** (chief of staff — cadence, actif), **OPS** (succès client, dormant), **DATA**
   (rentabilité des méthodes, dormant). **CARE** est traité à part : non un pair des autres,
   mais la couture de domaine (un contrat par objet). Anatomie et circulation : voir
   `_anatomie-siege.md`.

5. **Discipline qui protège la vision (anti-abstraction prématurée).** Le noyau gagne sa
   généralité en ayant **une instance qui tourne pour vrai**. La boucle minimale IVIA-personne
   se livre en premier ; les coutures (`objet d'analyse`, `contrat CARE`) sont dessinées dès le
   départ pour que le marché #2 soit une **config, pas une réécriture**.

6. **Loi de circulation des sources (anti-bordel).** Tout fichier appartient à **une seule**
   des trois classes :
   - **Intrant** — matière brute (ex. `PROD perplexity/`) : consommée une fois, puis **gelée**
     dans `_archives/intrants/AAAA-MM/`. Jamais une source vivante.
   - **Canon** — vérité vivante (ADR, doctrine, contrats, prompts) : **une seule par sujet**,
     versionnée *dans* le fichier. On la modifie, on ne la duplique pas.
   - **Dérivé** — produit à partir du canon (code, site, docs générés) : jetable et
     reconstructible, jamais source de vérité.
   Règles dures : **un fait = une source canonique** ; **Git est l'historique** (zéro `_v2`,
   `_final`, `_old`, `.bak`, zéro fichier daté orphelin) ; tout intrant va à l'archive ;
   **aucun orphelin** (chaque fichier produit a une destination déclarée). Le siège **COS**
   fait respecter cette loi à chaque session.

7. **Arborescence cible** (raffine ADR-0004) :
   ```
   noyau/        → moteur d'analyse agnostique (référentiels, axes, scoring)
   bureau/       → les ~11 sièges C-suite (11_PROMPTS/06_CSUITE étendu)
   contrats/     → CARE : un contrat par objet d'analyse
     ├── client/
     └── praticien/
   doctrine/     → 00_DOCTRINE (la pensée)
   instances/
     └── ivia/   → 1re instance : objets {client, praticien}
           └── produit/   → site + backend, boucle minimale d'abord
   _archives/    → intrants gelés + legacy (Next.js, mockups)
   ```

---

## Conséquences

### Avantages

- Produit extensible : nouveaux objets / nouveaux marchés sans réécriture du noyau.
- Différenciateur praticien (miroir réflexif) = levier de rétention/LTV (cf. CAC/LTV).
- Fin du désordre documentaire : une source canonique par fait, intrants gelés.
- Bureau de direction complet et orchestré (COS), pas seulement des chapeaux.

### Inconvénients ou risques

- **Risque d'abstraction prématurée** : construire la généralité avant un concret qui tourne.
  *Mitigation* : décision §5 — livrer la boucle minimale IVIA-personne d'abord.
- **Risque de sur-promesse côté praticien** (« vue objective », « plus besoin de
  supervision »). *Mitigation* : CARE-praticien impose « miroir réflexif » et
  « complément, non remplacement » de la supervision.
- Coût de restructuration et de réconciliation avec ADR-0004.

### Actions requises

- [ ] Réconcilier l'arborescence cible avec ADR-0004 (normalisation).
- [ ] Créer les sièges GROWTH, LEGAL, COS (actifs) ; OPS, DATA (dormants) ; CARE (contrats).
- [ ] Rédiger les contrats CARE-client et CARE-praticien dans `contrats/`.
- [ ] Exécuter le nettoyage (journal du 2026-06-30) après validation du plan final.
- [ ] Consommer puis geler les intrants `PROD perplexity/`.
- [ ] Inscrire la loi de circulation des sources dans `.claude/rules/` (gardée par COS).

---

## Entrée registre associée

> DEC-008 | 2026-06-30 | architecture | Noyau modulaire + bureau complet + objet pluggable | validated | ADR-0008

---

## Historique de révisions

| Version | Date | Auteur | Nature de la révision |
|---|---|---|---|
| 1.0 | 2026-06-30 | fondateur | Création initiale — décision de refonte structurelle |

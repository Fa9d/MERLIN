# IVIA — Audit du discours marketing et orientation stratégique

**Version** : v1.0 — 21 mai 2026  
**Auteur** : Copilot / session David Phaneuf  
**Statut** : Actif — à transmettre à Perplexity pour continuation  
**Objet** : Analyse critique du gap entre le discours actuel du site IVIA/MÉSANGES et le positionnement défini dans la Charte doctrinaire v2.0. Recommandations d'orientation du discours public.

---

## I. ÉTAT DU DISCOURS ACTUEL — snapshot 21 mai 2026

### Ce que le site affiche (ivia.quebec / localhost:3000)

| Zone | Contenu actuel |
|------|---------------|
| Navbar | "IVIA - MÉSANGES" + logo |
| Hero H1 | "MÉSANGES" |
| Hero sous-titre 1 | "Écoute empathique, ancrée au Québec." |
| Hero sous-titre 2 | "Votre PRATICIEN MÉSANGES vous aide à clarifier et à préparer la suite." |
| CTA 1 | "M'inscrire" → /orientation |
| CTA 2 | "Prendre RDV" → /rendez-vous |
| Section 2 | "Une voix et une écoute qui respecte votre parcours." |
| Section 2 corps | "MÉSANGES ne remplace ni la médecine, ni les services d'urgence. Nous vous aidons à mettre des mots, à **reconnaître les troubles**, en vous laissant choisir et déterminer votre voie d'action." |
| Section 3 | Processus 6 étapes : Vous déposez → MERLIN structure → Les possibles - VOS SOLUTIONS → MÉSANGES accompagne → Vous agissez → Nous suivons l'évolution |
| Section 4 | "Quelques questions pour préparer une conversation." + CTA "Faire le Parcours" → /orientation |
| Section 5 | "Ce que le numérique fait à votre équilibre." — 4 angles (Isolation, Surcharge, Disponibilité constante, Identité fragmentée) |
| Footer | "MÉSANGES · Québec" / "IVIA · Montréal. Données au Québec." |

---

## II. CE QUE LES DOCUMENTS FONDATEURS DÉFINISSENT

### Architecture décidée (DÉC-V3-15, 8 mai 2026)
- **IVIA inc. (SPA-mère)** = structure économique et juridique. Héberge MERLIN, MÉSANGES et les divisions futures. Propriétaire : David Phaneuf à 100 %.
- **MERLIN** = noyau d'analyse. Moteur IA/analytique, pipeline, mémoire de parcours. L'actif technologique principal. Ne s'expose pas au client.
- **MÉSANGES** = **Espace d'écoute et d'accompagnement vers l'autonomie.** Division d'IVIA inc., interface de première ligne. La trajectoire est toujours : écoute → clarification → orientation → autonomie. MÉSANGES ne vise pas la fidélisation — elle vise l'indépendance de la personne.
- **IVIA OBNL (satellite)** = entité philanthropique distincte, reçoit des licences sociales d'IVIA inc. pour redistribution à des populations en besoin.

### Positionnement client (Charte v2.0, 21 mai 2026)

**Identité** : Centre d'écoute, d'orientation individuelle et d'accompagnement vers l'équilibre, l'autonomie et l'indépendance.

**Marché cible** : Santé de première ligne au Québec — anxiété, stress chronique, transitions professionnelles, isolement, crises relationnelles, deuils ordinaires.

### Couche philosophique (absente du site actuel — GAP structurel)

IVIA = **In Vivo In Actu** (*Au sein de l'être — En actes*). Ce n'est pas un nom : c'est la posture fondatrice. Les 7 principes de la Charte sont l'opérationnalisation de cette philosophie. Cette couche doit être présente dans le discours à la bonne altitude : pas dans le héro (trop abstrait), mais dans le « À propos » et les documents institutionnels — c'est ce qui donne de la profondeur à la promesse et la différencie de toute appli de bien-être générique.

**Données de marché documentées** :
- 385 000 Montréalais sans médecin de famille (début 2024)
- 15 % des adultes : trouble anxieux diagnostiqué (ISQ 2024)
- 25–35 % de la population QC : détresse psychologique élevée (EQSP K6/K10)
- 20 % des Canadiens : trouble mental ou consommation sur 12 mois (ESCC)
- 1/3 des Montréalais 55+ : isolement social (INSPQ)

**Devise** : *Au sein de l'être — En actes.*

**Vocabulaire permis** : accompagnement, écoute, personne accompagnée, pratique de soin de soi, ressource  
**Vocabulaire interdit** (Loi 21, art. 187.1 Code des professions) : thérapie, thérapeute, psychothérapie, traitement, diagnostic, patient, clinique, guérison

---

## III. AUDIT — GAPS IDENTIFIÉS

### GAP 1 — INVISIBILITÉ DU MARCHÉ CIBLE ⚠️ CRITIQUE
**Problème** : La réalité québécoise chiffrée est absente du site. Pas un chiffre. Pas une référence à la crise d'accès aux soins. Le visiteur n'est pas interpellé par une réalité qu'il reconnaît.  
**Impact** : Taux d'accroche faible. La personne qui se sent seule avec son anxiété ne se voit pas représentée.  
**Solution** : Ancrer l'hero ou une section haut de page sur les données réelles. Exemple : *"385 000 personnes n'ont pas de médecin de famille à Montréal. MÉSANGES est là pour ce que le système ne couvre pas."*

---

### GAP 2 — CONFUSION DES MARQUES ⚠️ CRITIQUE
**Problème** : "IVIA" et "MÉSANGES" sont utilisés de façon interchangeable et confuse sur le site. Le header dit "IVIA - MÉSANGES", l'H1 dit "MÉSANGES", le footer dit les deux. Un client qui cherche "IVIA" se retrouve sur une page qui parle surtout de "MÉSANGES" sans comprendre la relation.  
**Impact** : Désorientation. Perte de confiance. Impossibilité de mémoriser la marque.  
**Solution** : Définir une hiérarchie claire et la tenir :
- IVIA = l'institution, la maison, la garantie qualité et éthique (niveau "maison mère")
- MÉSANGES = le service client quotidien, l'écoute de première ligne (niveau "porte d'entrée")  
Et l'afficher : *"MÉSANGES, un service IVIA"* — une seule fois, proprement.

---

### GAP 3 — VOCABULAIRE À RISQUE LÉGAL ⚠️ URGENT
**Problème** : La section 2 du site contient : *"Nous vous aidons à mettre des mots, à **reconnaître les troubles**"*.  
"Reconnaître les troubles" est du vocabulaire diagnostique réservé au sens de l'art. 187.1. Un professionnel réglementé (OPQ, OTSTCFQ) pourrait s'en saisir.  
**Impact** : Risque légal direct. Ce fragment expose IVIA à une plainte d'exercice illégal de la psychothérapie.  
**Solution immédiate** : Remplacer par *"à nommer ce que vous ressentez"* ou *"à comprendre ce qui pèse"*.

---

### GAP 4 — PROMESSE MÈRE ABSENTE DU SITE ⚠️ IMPORTANT
**Problème** : La formule mère définie dans `MERLIN_GOUV_PROMESSE_CLIENT_ULTRA_COURTE_IVIA_V1.md` — *"Un espace d'écoute pour clarifier ce que vous vivez et repartir avec une suite plus lisible."* — n'apparaît nulle part sur le site.  
**Impact** : Le hero actuel "Écoute empathique, ancrée au Québec." est moins précis, moins désirable, et moins distinctif.  
**Solution** : La promesse mère doit être visible dans les 5 premières secondes de visite.

---

### GAP 5 — SECTION NUMÉRIQUE HORS POSITIONNEMENT ⚠️ IMPORTANT
**Problème** : La section "Ce que le numérique fait à votre équilibre" introduit un angle "digital wellness" qui n'est pas cohérent avec le positionnement santé de première ligne QC. Elle ressemble à un produit de détox numérique (Calm, Headspace) plutôt qu'à un centre d'orientation santé.  
**Impact** : Dilution du message. Confusion sur l'offre. Risque de positionnement dans le segment "app de bien-être" au lieu de "centre de santé première ligne".  
**Solution** : Soit supprimer cette section, soit la recentrer sur l'isolement numérique comme facteur de détresse QC (lié aux stats INSPQ sur l'isolement des 55+).

---

### GAP 6 — CTA MULTIPLES ET CONTRADICTOIRES ⚠️ MODÉRÉ
**Problème** : Trois chemins vers la même action (orientation) : "M'inscrire", "Prendre RDV", "Faire le Parcours". Le visiteur ne sait pas par où commencer.  
**Impact** : Paralysie de décision. Taux de conversion réduit.  
**Solution** : Un seul CTA principal dans l'hero. Règle de base : une page, une action principale.

---

### GAP 7 — DEVISE ABSENTE ⚠️ MINEUR
**Problème** : "Au sein de l'être — En actes." n'apparaît nulle part sur le site.  
**Impact** : La signature philosophique de la marque est invisible pour les clients.  
**Solution** : La placer dans le footer ou en signature sous le logo.

---

### GAP 8 — PROCESSUS EXPOSE L'OUTIL INTERNE ⚠️ MODÉRÉ
**Problème** : L'étape "MERLIN structure" dans le processus 6 étapes expose le moteur à l'utilisateur. MERLIN est le nom de l'outil interne / du projet global — pas un nom de service client.  
**Impact** : Le client s'interroge sur "MERLIN" sans contexte. Crée de la confusion technologique là où il devrait y avoir de la chaleur humaine.  
**Solution** : Renommer l'étape côté client. Ex : "Votre portrait est préparé" ou "L'analyse prend forme".

---

### GAP 9 — AUCUNE PREUVE SOCIALE ⚠️ MODÉRÉ
**Problème** : Pas de témoignages, pas de chiffres d'usage, pas de citation.  
**Impact** : Faible crédibilité initiale pour un nouveau visiteur.  
**Solution** : En phase pilote, utiliser des témoignages anonymisés ou des affirmations quantitatives simples (*"Plus de X séances accompagnées"*).

---

## IV. ORIENTATION RECOMMANDÉE DU DISCOURS

### Principe directeur
> Le visiteur doit se reconnaître dans une réalité québécoise précise, comprendre en 10 secondes ce que MÉSANGES fait pour lui, et avoir un chemin unique vers la première étape.

### Architecture du message en 3 niveaux

**Niveau 1 — Réalité** (ancrage émotionnel + données)  
*"385 000 Montréalais n'ont pas de médecin de famille. Vous n'êtes pas seul·e dans ce que vous vivez."*

**Niveau 2 — Promesse** (ce que MÉSANGES fait, en langage client)  
*"Un espace d'écoute pour clarifier ce que vous vivez et repartir avec une suite plus lisible."*  
*(formule mère, à garder intacte)*

**Niveau 3 — Chemin** (un seul CTA)  
*"Commencer — 15 minutes d'écoute pour commencer à y voir clair."*

### Vocabulaire à adopter systématiquement

| À UTILISER | À BANNIR |
|-----------|----------|
| accompagnement | thérapie / thérapeute |
| écoute | psychothérapie |
| personne accompagnée | patient |
| clarification | diagnostic |
| orientation | traitement |
| pratique de soin de soi | guérison |
| ressource | clinique |
| nommer ce que vous ressentez | reconnaître les troubles |
| comprendre ce qui pèse | identifier un trouble |

### Structure de page recommandée

1. **Hero** : Réalité QC + Promesse mère + 1 CTA
2. **Section confiance** : MÉSANGES, un service IVIA — qui nous sommes, ce que nous ne sommes pas (cadre légal, non médical, non thérapeutique)
3. **Section processus** : 4 étapes max, centrées sur l'expérience client (pas sur la technologie)
4. **Section preuves** : Témoignages ou chiffres pilote
5. **Section portails** : Séparation claire Clients / Praticiens
6. **Footer** : Devise + liens légaux

---

## V. WHAT IVIA VEND RÉELLEMENT (clarification produit)

Ce que le client achète quand il réserve une séance MÉSANGES :

1. **La permission de parler** — un espace non médical, non stigmatisant, où nommer ce qu'on vit n'entraîne pas une ordonnance
2. **Une clarification** — pas un diagnostic, mais une lecture structurée de sa situation
3. **Une orientation** — trois prochains pas concrets, pas une liste de ressources vague
4. **Une continuité** — si la personne revient, elle repart de là où elle en était

Ce que le client ne peut pas acheter et que le discours ne doit jamais promettre :
- Une guérison
- Un diagnostic
- Un remplacement de professionnel réglementé
- Une garantie de résultat

---

## VI. RECOMMANDATIONS POUR PERPLEXITY

Voir `07_EXPORTS/CONTEXT_PERPLEXITY_STANDING_v1.0.md` — brief permanent à transmettre à Perplexity en début de chaque session marketing.

**Tâches immédiates à confier à Perplexity :**
1. Réécriture du hero section (H1 + sous-titre + CTA) selon les données et la promesse mère
2. Réécriture de la section "Reconnaître les troubles" → vocabulaire légalement sûr
3. Proposition de 3 variantes de tagline ancrées sur les stats QC
4. Réécriture du processus 6 étapes → expérience client centrée, sans MERLIN exposé
5. Réflexion sur la section numérique : supprimer ou recentrer ?

---

## VII. PRIORITÉS D'ACTION

| Priorité | Action | Urgence |
|---------|--------|---------|
| 🔴 P0 | Corriger "reconnaître les troubles" → vocabulaire sûr | Immédiate (légal) |
| 🔴 P0 | Clarifier hiérarchie IVIA / MÉSANGES sur le site | Immédiate |
| 🟠 P1 | Injecter promesse mère dans hero | Court terme |
| 🟠 P1 | Ancrer 1-2 stats QC dans hero ou section 2 | Court terme |
| 🟡 P2 | Réduire à 1 CTA principal | Court terme |
| 🟡 P2 | Renommer "MERLIN structure" dans le processus | Court terme |
| 🟢 P3 | Recentrer ou supprimer section numérique | Moyen terme |
| 🟢 P3 | Ajouter preuve sociale (témoignages pilote) | Moyen terme |
| 🟢 P3 | Ajouter devise dans footer | Court terme |

---

*Source discours actuel : snapshot site `ivia.quebec` / `localhost:3000` du 21 mai 2026*  
*Référence charte : `00_GOUVERNANCE/IVIA_CHARTE_DOCTRINAIRE_v2.0.md`*  
*Référence rapport marché : `05_PREUVES_SOURCES/Rapport_MESANGE_Soins_Quebec_2026-05.pdf`*

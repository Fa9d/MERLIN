# MERLIN - Grille comparative marche V1

Date: 2026-04-20
Statut: draft
Objet: fournir une grille standard pour comparer les services existants au projet MERLIN

---

## 1) Finalite

Cette grille sert a comparer des acteurs de marche de facon homogene.

Elle doit permettre de repondre a trois questions:
- a qui MERLIN ressemble-t-il le plus?
- en quoi MERLIN est-il distinct?
- quel modele economique et quelle promesse sont defendables?

---

## 2) Unites de comparaison

Chaque acteur benchmarke doit etre documente comme une fiche distincte.

Une fiche = un acteur ou une offre principale.

Exemples:
- une plateforme de therapie
- une ligne d'ecoute
- une app bien-etre
- un logiciel praticien
- un service de care navigation

Ne pas melanger plusieurs offres d'une meme entreprise dans une seule fiche si elles ont:
- des publics differents;
- des prix differents;
- des promesses differentes.

---

## 3) Champs descriptifs obligatoires

Pour chaque acteur, relever:

- `acteur_id`
- `nom`
- `url_principale`
- `territoire`
- `langue`
- `famille_comparable`
- `public_cible`
- `probleme_principal_resolu`
- `promesse_commerciale_courte`
- `type_service`
- `intervenants_ou_praticiens`
- `humain_ou_numerique`
- `canaux`
- `orientation_vers_tiers`
- `continuite_historique`
- `transcription_ou_notes`
- `application_praticien`
- `ia_ou_automatisation`
- `tarification_client`
- `tarification_praticien`
- `modele_economique`
- `discours_urgence_limites`
- `forces_apparentes`
- `faiblesses_apparentes`
- `risques_de_confusion_avec_merlin`
- `commentaire_strategique`

---

## 4) Valeurs conseillees

### `famille_comparable`

- `therapie_en_ligne`
- `ecoute_soutien_non_clinique`
- `app_bien_etre_sante_mentale`
- `logiciel_praticien_telepratique`
- `care_navigation_orientation`
- `integratif_holistique_complementaire`
- `autre`

### `type_service`

- `marketplace`
- `plateforme_service`
- `service_humain_direct`
- `application_mobile`
- `logiciel_saas`
- `modele_hybride`

### `humain_ou_numerique`

- `principalement_humain`
- `principalement_numerique`
- `hybride`

### `canaux`

Liste ouverte, valeurs conseillees:
- `telephone`
- `web`
- `mobile`
- `visio`
- `messagerie`
- `presentiel`

### `orientation_vers_tiers`

- `aucune`
- `faible`
- `moyenne`
- `forte`

### `continuite_historique`

- `aucune`
- `faible`
- `moyenne`
- `forte`

### `transcription_ou_notes`

- `aucune`
- `notes_basiques`
- `notes_structurees`
- `transcription`
- `non_clair`

### `application_praticien`

- `oui`
- `non`
- `partiel`

### `ia_ou_automatisation`

- `aucune_visible`
- `assistance_legere`
- `forte`
- `non_clair`

### `modele_economique`

- `b2c_abonnement`
- `b2c_par_seance`
- `b2b_saas`
- `b2b2c`
- `commission`
- `freemium`
- `mixte`
- `non_clair`

---

## 5) Axes d'evaluation strategique

Au-dela de la description, chaque acteur doit etre note sur 10 axes.

Echelle simple:
- `0 = absent`
- `1 = faible`
- `2 = moyen`
- `3 = fort`

### Axe 1 - Clarification de situation

L'acteur aide-t-il vraiment a comprendre ce qui se passe?

### Axe 2 - Lecture du risque / triage

L'acteur distingue-t-il bien urgence, crise et non-urgence?

### Axe 3 - Orientation accompagnee

L'acteur aide-t-il a choisir une bonne prochaine porte d'entree?

### Axe 4 - Continuite / memoire

L'acteur garde-t-il une memoire utile entre les interactions?

### Axe 5 - Valeur humaine

La valeur percue repose-t-elle sur une vraie relation humaine?

### Axe 6 - Valeur logicielle

La valeur percue repose-t-elle sur un outillage, une interface ou une automatisation forte?

### Axe 7 - Discipline de cadre / limites

L'acteur pose-t-il clairement ce qu'il fait et ne fait pas?

### Axe 8 - Monetisation explicite

Le modele economique est-il lisible et defendable?

### Axe 9 - Risque de confusion avec MERLIN

Le public pourrait-il confondre cet acteur avec MERLIN?

### Axe 10 - Menace strategique reelle

Cet acteur peut-il capter le meme besoin que MERLIN, meme avec une offre differente?

---

## 6) Questions d'analyse a remplir pour chaque acteur

1. Quel besoin principal cet acteur capte-t-il?
2. Que vend-il reellement?
3. Quelle promesse comprend-on en 10 secondes?
4. Quelle partie de sa valeur est humaine?
5. Quelle partie de sa valeur est logicielle?
6. Que fait-il mieux que MERLIN aujourd'hui?
7. Que ferait MERLIN mieux si son offre etait bien formulee?
8. Quel risque de confusion ou d'imitation existe?
9. Cet acteur tire-t-il ses revenus du client, du praticien, d'un tiers, ou d'un mix?
10. Quelle lecon immediate pour MERLIN?

---

## 7) Lecture strategique finale

Une fois plusieurs fiches remplies, classer les acteurs selon 4 statuts:

### A. Concurrent direct percu

Le client peut croire que c'est la meme chose que MERLIN.

### B. Substitut fonctionnel

Ce n'est pas la meme chose, mais cela peut absorber le meme besoin.

### C. Outil complementaire

Peut coexister avec MERLIN ou inspirer une brique produit.

### D. Faux comparable

Intuitivement proche, mais trop different pour piloter le positionnement.

---

## 8) Table resume recommandee

Utiliser a la fin une table de synthese avec:

| Acteur | Famille | Ce qu'il vend vraiment | Qui paie | Force principale | Faiblesse principale | Risque de confusion | Lecon pour MERLIN |
| --- | --- | --- | --- | --- | --- | --- | --- |

---

## 9) Regles de prudence

- Ne pas noter trop vite sans avoir lu le site, les tarifs et les limites.
- Ne pas confondre discours marketing et realite produit.
- Ne pas survaloriser un acteur parce qu'il est visuellement fort.
- Ne pas sous-estimer un acteur simple mais bien positionne.
- Ne pas comparer MERLIN a un seul type d'acteur.

---

## 10) Decision active

Cette grille devient le standard V1 de benchmark de marche pour MERLIN.

Elle doit servir avant:
- le positionnement final;
- la tarification finale;
- la segmentation praticiens;
- le modele economique definitif.

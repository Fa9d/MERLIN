# MERLIN - Modele de couts de production documentaire en tokens V1

Date: 2026-04-27
Statut: draft
Objet: definir une base standardisee pour mesurer le cout reel de production des documents MERLIN en tokens, audio, image et sorties textuelles

---

## 1) But

MERLIN doit connaitre le cout reel de ce qu'il produit.

Chaque document doit pouvoir etre rattache a:

- un volume d'entree;
- un volume de sortie;
- un nombre de passes de traitement;
- un cout de transcription si audio;
- un cout d'image si image produite;
- un cout total estimatif.

Doctrine:

`aucun document MERLIN ne doit etre traite comme gratuit; chaque sortie doit avoir un cout standard mesurable`

---

## 2) Principe de calcul

Le cout standard d'un document est:

`cout total = cout transcription + cout tokens texte + cout image + cout revue humaine`

### A. Cout transcription

Si un document depend d'un audio:

- mesurer la duree de l'audio en minutes;
- appliquer le cout minute du moteur de transcription retenu.

### B. Cout tokens texte

Pour chaque passe LLM:

- `cout passe = (tokens entree / 1 000 000 x tarif entree modele) + (tokens sortie / 1 000 000 x tarif sortie modele)`

### C. Cout image

Si un visuel est genere:

- appliquer le cout unitaire image selon le format retenu.

### D. Cout revue humaine

Si une validation praticien ou supervision est requise:

- ajouter un temps standard de revue interne.

---

## 3) Unites de mesure MERLIN

MERLIN doit suivre au minimum:

- `audio_minutes_source`
- `tokens_transcription_source`
- `tokens_prompt_systeme`
- `tokens_contexte_client`
- `tokens_contexte_seance`
- `tokens_entree_totale`
- `tokens_sortie_totale`
- `nb_passes_llm`
- `nb_images_generees`
- `minutes_revue_humaine`

---

## 4) Tarifs de reference a parametrer

Les tarifs doivent rester parametrables dans l'admin ou dans la couche finance.

Variables de reference:

- `tarif_stt_minute_cad`
- `tarif_llm_mini_entree_cad_par_1m`
- `tarif_llm_mini_sortie_cad_par_1m`
- `tarif_llm_standard_entree_cad_par_1m`
- `tarif_llm_standard_sortie_cad_par_1m`
- `tarif_llm_premium_entree_cad_par_1m`
- `tarif_llm_premium_sortie_cad_par_1m`
- `tarif_image_unitaire_cad`
- `tarif_revue_humaine_cad_par_minute`

Important:

- ces valeurs doivent etre actualisees regulierement;
- le modele de cout doit survivre au changement de fournisseur.

### Hypothese MERLIN V1 de travail

Pour disposer d'un coutant exploitable des maintenant, MERLIN retient une base interne standard.

Valeurs de reference V1:

| Variable | Valeur standard |
|---|---:|
| `tarif_stt_minute_cad` | `0,008 CAD / minute` |
| `tarif_llm_mini_entree_cad_par_1m` | `0,40 CAD / 1M tokens` |
| `tarif_llm_mini_sortie_cad_par_1m` | `1,60 CAD / 1M tokens` |
| `tarif_llm_standard_entree_cad_par_1m` | `4,00 CAD / 1M tokens` |
| `tarif_llm_standard_sortie_cad_par_1m` | `16,00 CAD / 1M tokens` |
| `tarif_llm_premium_entree_cad_par_1m` | `20,00 CAD / 1M tokens` |
| `tarif_llm_premium_sortie_cad_par_1m` | `80,00 CAD / 1M tokens` |
| `tarif_image_unitaire_cad` | `0,08 CAD / image` |
| `tarif_revue_humaine_cad_par_minute` | `1,00 CAD / minute` |

Lecture:

- les couts IA purs restent faibles a l'unite;
- la revue humaine et la validation praticien dominent rapidement le cout reel;
- le modele MERLIN doit donc raisonner en `cout technique` et en `cout complet`.

---

## 5) Hypothese standard de production V1

Pour standardiser MERLIN, on retient 4 types de passes.

### Passe 1 - Extraction

Role:

- nettoyer;
- extraire les points utiles;
- structurer la matiere.

Modele recommande:

- mini ou standard leger

### Passe 2 - Analyse

Role:

- produire une lecture structuree;
- degager les tensions, tendances, contexte et suites.

Modele recommande:

- standard

### Passe 3 - Redaction

Role:

- produire le document final lisible.

Modele recommande:

- standard

### Passe 4 - Adaptation client

Role:

- reformuler prudemment pour le client;
- retirer les formulations internes;
- respecter les limites legales.

Modele recommande:

- standard ou premium selon niveau d'exigence

---

## 6) Capacite standard par type de document

Les valeurs ci-dessous sont des budgets de production V1.

### A. Note interne praticien

Usage:

- document interne court apres seance.

Budget standard:

- transcription source: `45 a 60 min audio`
- tokens transcription utiles en entree: `10 000 a 16 000`
- prompt systeme et contexte: `1 500`
- passe extraction entree: `12 000`
- passe extraction sortie: `1 500`
- passe analyse entree: `7 000`
- passe analyse sortie: `2 000`
- passe redaction entree: `4 500`
- passe redaction sortie: `1 200`

Budget total texte:

- entree: `23 500`
- sortie: `4 700`
- total tokens: `28 200`

### B. Compte rendu praticien

Usage:

- document praticien plus structure et plus diffusable.

Budget standard:

- transcription source: `45 a 60 min`
- entree totale: `28 000`
- sortie totale: `6 500`
- total tokens: `34 500`

Structure:

- extraction
- analyse
- redaction praticien

### C. Document client valide

Usage:

- version prudente remise au client apres validation.

Budget standard:

- reutilise le compte rendu praticien comme base;
- passe supplementaire d'adaptation client.

Budget total:

- entree totale: `34 000`
- sortie totale: `8 000`
- total tokens: `42 000`

Structure:

- extraction
- analyse
- redaction praticien
- adaptation client

### D. Document de mise en pratique

Usage:

- fiche concrete pour alleger le quotidien.

Budget standard:

- entree totale: `18 000`
- sortie totale: `4 500`
- total tokens: `22 500`

Structure:

- lecture du contexte;
- generation de pistes;
- redaction en format pratique.

### E. Synthese de parcours

Usage:

- synthese multi-seances.

Budget standard:

- source: `3 a 6 seances`
- entree totale: `45 000 a 90 000`
- sortie totale: `8 000 a 15 000`
- total tokens: `53 000 a 105 000`

Structure:

- consolidation historique;
- comparaison;
- redaction synthetique;
- adaptation diffusion si requise.

#### Variante standard - Synthese 3 seances

Hypothese:

- `3 seances` de `60 min`
- `180 min` audio source

Budget standard:

- entree totale: `55 000`
- sortie totale: `9 000`
- total tokens: `64 000`

#### Variante renforcee - Synthese 10 seances

Hypothese:

- `10 seances` de `60 min`
- `600 min` audio source

Budget standard:

- entree totale: `150 000`
- sortie totale: `20 000`
- total tokens: `170 000`

### F. Capsule ou fiche bibliotheque

Usage:

- contenu bibliotheque textuel ou script audio/video.

Budget standard texte seul:

- entree totale: `8 000`
- sortie totale: `2 500`
- total tokens: `10 500`

Si script + visuel:

- ajouter `1 image`
- ou plusieurs blocs visuels selon format.

---

## 7) Tableau de reference standard

| Document | Audio requis | Passes LLM | Entree totale | Sortie totale | Total tokens | Cout technique estime | Cout complet estime |
|---|---:|---:|---:|---:|---:|---:|---:|
| note interne praticien | oui | 3 | 23 500 | 4 700 | 28 200 | `0,58 CAD` | `4,58 CAD` |
| compte rendu praticien | oui | 3 | 28 000 | 6 500 | 34 500 | `0,70 CAD` | `6,70 CAD` |
| document client valide | oui | 4 | 34 000 | 8 000 | 42 000 | `0,84 CAD` | `8,84 CAD` |
| document mise en pratique | optionnel | 2 a 3 | 18 000 | 4 500 | 22 500 | `0,14 CAD` | `4,14 CAD` |
| synthese de parcours standard | oui | 3 a 4 | 45 000 a 90 000 | 8 000 a 15 000 | 53 000 a 105 000 | `0,88 a 1,55 CAD` | `12,88 a 25,55 CAD` |
| synthese 3 seances | oui | 3 a 4 | 55 000 | 9 000 | 64 000 | `1,80 CAD` | `13,80 CAD` |
| synthese 10 seances | oui | 4 | 150 000 | 20 000 | 170 000 | `6,60 CAD` | `31,60 CAD` |
| fiche bibliotheque | non | 2 | 8 000 | 2 500 | 10 500 | `0,05 CAD` | `2,05 CAD` |

Notes:

- `cout technique estime` = transcription + passes IA + image si applicable
- `cout complet estime` = cout technique + revue humaine standard
- les montants sont calcules sur la base MERLIN V1 posee en section 4

---

## 8) Cout standardisable par document

MERLIN doit stocker pour chaque type de document:

- `cout_direct_ai_estime_cad`
- `cout_direct_audio_estime_cad`
- `cout_direct_image_estime_cad`
- `cout_revue_humaine_estime_cad`
- `cout_total_estime_cad`

Formule type:

`cout_total_estime_cad = cout_stt + cout_passes_llm + cout_image + cout_revue_humaine`

---

## 9) Exemple de parametrage pratique

Exemple de calcul si les tarifs reels sont definis.

### Note interne praticien

- STT: `60 min x tarif_stt_minute_cad`
- LLM extraction:
  - entree `12 000`
  - sortie `1 500`
- LLM analyse:
  - entree `7 000`
  - sortie `2 000`
- LLM redaction:
  - entree `4 500`
  - sortie `1 200`
- revue humaine:
  - `3 a 5 min`

Exemple chiffre sur base MERLIN V1:

| Operation | Hypothese | Coutant |
|---|---|---:|
| transcription audio | `60 x 0,008` | `0,48 CAD` |
| extraction mini | `12 000 in + 1 500 out` | `0,01 CAD` |
| analyse standard | `7 000 in + 2 000 out` | `0,06 CAD` |
| redaction standard | `4 500 in + 1 200 out` | `0,04 CAD` |
| revue humaine | `4 min x 1,00` | `4,00 CAD` |
| total |  | `4,58 CAD` |

### Document client valide

- STT: `60 min x tarif_stt_minute_cad`
- passes texte:
  - entree `34 000`
  - sortie `8 000`
- revue praticien:
  - `5 a 10 min`

Exemple chiffre sur base MERLIN V1:

| Operation | Hypothese | Coutant |
|---|---|---:|
| transcription audio | `60 x 0,008` | `0,48 CAD` |
| extraction mini | `12 000 in + 1 500 out` | `0,01 CAD` |
| analyse standard | `9 000 in + 2 500 out` | `0,08 CAD` |
| redaction praticien standard | `8 000 in + 2 000 out` | `0,06 CAD` |
| adaptation client standard | `5 000 in + 2 000 out` | `0,05 CAD` |
| revue praticien | `8 min x 1,00` | `8,00 CAD` |
| total |  | `8,68 CAD` |

### Synthese 3 seances

Base:

- audio source `180 min`
- passes:
  - consolidation standard
  - comparaison standard
  - redaction standard
  - adaptation diffusion optionnelle

Exemple chiffre sur base MERLIN V1:

| Operation | Hypothese | Coutant |
|---|---|---:|
| transcription audio | `180 x 0,008` | `1,44 CAD` |
| consolidation standard | `25 000 in + 4 000 out` | `0,16 CAD` |
| comparaison standard | `20 000 in + 3 000 out` | `0,13 CAD` |
| redaction standard | `10 000 in + 2 000 out` | `0,07 CAD` |
| revue humaine | `12 min x 1,00` | `12,00 CAD` |
| total |  | `13,80 CAD` |

### Synthese 10 seances

Base:

- audio source `600 min`
- passes:
  - consolidation premium
  - comparaison standard
  - redaction standard
  - adaptation diffusion standard

Exemple chiffre sur base MERLIN V1:

| Operation | Hypothese | Coutant |
|---|---|---:|
| transcription audio | `600 x 0,008` | `4,80 CAD` |
| consolidation premium | `80 000 in + 10 000 out` | `2,40 CAD` |
| comparaison standard | `40 000 in + 5 000 out` | `0,24 CAD` |
| redaction standard | `20 000 in + 3 000 out` | `0,13 CAD` |
| adaptation diffusion standard | `10 000 in + 2 000 out` | `0,07 CAD` |
| revue humaine | `24 min x 1,00` | `24,00 CAD` |
| total |  | `31,64 CAD` |

---

## 10) Niveaux de production recommandes

MERLIN doit avoir trois niveaux standard.

### Niveau S - Sobre

- peu de passes;
- documents courts;
- cout bas;
- bonne solution pour offre de base.

### Niveau M - Standard

- documents structurants;
- validation praticien;
- cout raisonnable;
- niveau recommande pour le marche initial.

### Niveau L - Renforce

- multi-passes;
- adaptation client;
- synthese plus longue;
- cout plus eleve;
- reserve aux offres plus hautes ou aux supplements.

---

## 11) Usage produit et finance

Ce modele doit servir a:

- fixer les prix des options documentaires;
- definir les marges par document;
- limiter les abus de production;
- arbitrer les offres praticiens;
- choisir ce qui est inclus dans un abonnement et ce qui devient un extra.

Exemple de doctrine:

- note interne simple: peut etre incluse en partie dans un abonnement haut
- document client valide: doit etre valorise comme production payante
- synthese de parcours: doit rester une sortie premium

---

## 12) Decision immediate

MERLIN doit maintenant:

1. rattacher chaque type de document a un budget standard de tokens;
2. rattacher chaque type de document a un cout AI estime;
3. integrer ces couts dans les offres praticiens et clients;
4. suivre en production l'ecart entre cout theorique et cout reel.

Doctrine finale:

`la capacite de production documentaire MERLIN doit etre standardisee, mesurable, actualisable et adaptee au marche Quebecois, sans vendre des sorties dont le cout reel n'est pas maitrise`

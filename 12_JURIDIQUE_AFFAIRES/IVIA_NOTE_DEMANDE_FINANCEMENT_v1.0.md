# IVIA — Note de demande de financement

**Version** : v1.0 — 2026-07-13
**Sources canoniques** : `IVIA_BP_FINANCEMENT_v2.4.md` · `FINANCEMENT_PUBLIC_PROGRAMMES_2026.md` · pitch/deck v2.0
**Statut** : actif — champs administratifs restants marqués « À compléter »

---

## 1. Objet et contexte du projet IVIA/MERLIN

IVIA est un écosystème civique québécois d'innovation sociale qui développe,
opère et redistribue des outils numériques d'utilité collective. La maison
publique (ivia.quebec) accueille ; MERLIN, cœur d'analyse et de gouvernance,
structure ; MÉSANGES, voix d'accompagnement, oriente — sans jamais poser de
diagnostic ni prescrire : toute sortie suit la triade Observation / Hypothèse /
Orientation, sous validation humaine.

L'écosystème suit une trajectoire de portage en trois temps (BP §2.1.0) :
l'exploitation actuelle est assurée par le fondateur en **entreprise
individuelle** (NEQ en cours d'obtention) ; **IVIA OBNL** viendra porter la
mission et les financements publics et philanthropiques ; une **entité
commerciale dédiée** (cible : société par actions à mission, LSAQ) portera
ensuite MERLIN, les revenus marchands, les contrats B2B et le capital privé,
liée à l'OBNL par une convention de licence sociale.

Le projet répond à une réalité documentée : détresse massive, première ligne
saturée, et une obligation légale nouvelle (Loi 27) qui transforme la santé
psychologique au travail en marché structuré. Les données sont hébergées au
Québec (Loi 25) ; le lexique clinique réservé (Loi 21) est exclu par
construction, filtré dans le code même de la plateforme.

## 2. Description du projet et périmètre financé

Le périmètre financé n'est pas une preuve de concept : la plateforme est **en
production** (backend FastAPI, site public, séances audio, transcription
locale souveraine par faster-whisper — aucune parole ne quitte le Québec).

Le financement porte sur l'accélération de quatre volets :

1. **MERLIN, moteur d'analyse gouverné** — pipeline complet séance →
   transcription → note (validée par un humain) → analyses (prosodie locale,
   lecture sémantique, croisements), chaque capacité passant par un catalogue
   gouverné : prompt versionné, suite d'évaluation de sûreté ≥ 0,90, vanne
   d'activation par profil.
2. **MÉSANGES et le mode autonome** — journal intime, miroirs directs au
   client sous triple verrou (suite de sûreté, filtre Loi 21 en code,
   protocole d'urgence en code — ressources 9-8-8 / 8-1-1 injectées serveur).
3. **IA instrumentée, économiquement transparente** — chaque appel de modèle
   est mesuré (tokens, coût réel, rattachement à la séance) dans un grand
   livre consultable : les coûts d'IA sont un poste comptable, pas une boîte
   noire.
4. **Conformité et structuration** — constitution juridique et fiscale,
   sécurité, onboarding praticiens, offre employeurs Loi 27, amorce de
   recherche universitaire.

## 3. Programmes publics visés en 2026

| # | Cible | Programmes | Fourchette | Véhicule | Horizon |
|---|---|---|---:|---|---|
| 1 | Crédits R&D | **RS&DE** (fédéral) + **CRIC** (Québec) | 120–180 K$ | entité commerciale (SPCC) | post-constitution |
| 2 | Finance solidaire | **Fondaction** · **Filaction** · **FAQDD** | 40–90 K$ | ent. comm./OBNL | Palier 1-2 |
| 3 | Innovation PME | **Investissement Québec** · **CDAE** | 30–70 K$ | ent. comm. | Palier 1-2 |
| 4 | Fédéral innovation | **PARI-CNRC** · **Mitacs** | 30–60 K$ | ent. comm. | Palier 1-3 |
| 5 | Mission / impact | Fondations · MSSS · RPS Loi 27 | 30–80 K$ | OBNL | Palier 2 |
| | **Total première vague** | | **250–480 K$** | | |

**Logique de recours par volet** : les crédits R&D (cible 1) s'appuient sur la
traçabilité expérimentale déjà en place (prompts versionnés, suites
d'évaluation datées, journal d'opérations, grand livre des coûts IA) ; la
finance solidaire et l'impact (cibles 2 et 5) passent par la mission et le
satellite OBNL ; l'innovation PME et le fédéral (cibles 3 et 4) financent la
structuration produit et les partenariats de recherche. Cette première vague
publique alimente l'objectif non-dilutif global du BP (920 K$ de subventions
et fonds publics + 280 K$ de crédits d'impôt sur 36 mois).

## 4. Montants, phases et calendrier (BP v2.4)

**Besoin total sur 36 mois : 2 200 000 $ CAD**, dont **54,5 % non-dilutif par
conception** :

| Source | Montant | % |
|---|---:|---:|
| Subventions et fonds publics non-dilutifs | 920 000 $ | 41,8 % |
| Crédits d'impôt remboursables (RS&DE, CRIC) | 280 000 $ | 12,7 % |
| Capital patient / à mission (dilutif ≤ 25 %) | 600 000 $ | 27,3 % |
| Prêts patients / BDC (à partir du Palier 2) | 200 000 $ | 9,1 % |
| Auto-financement (revenus opérationnels) | 200 000 $ | 9,1 % |

**Phases** (affectation BP §6.1.2 : Palier 1 = 170 K$ · Palier 2 = 500 K$ ·
Palier 3 = 1 227 K$ · marge = 303 K$) :

- **Palier 0 — réalisé** (mai-juillet 2026) : plateforme en production,
  pilote MERLIN actif ;
- **Palier 1** (M7-M9, automne 2026 → février 2027) : constitution juridique,
  premières demandes publiques, 18-25 praticiens, ARR ~108 K$ ;
- **Palier 2** (→ novembre 2027) : MÉSANGE en revenu, 50-70 praticiens,
  ARR ~380 K$ ;
- **Palier 3** (→ mai 2029) : 200-350 praticiens, ARR ~1 850 K$,
  équilibre courant visé M28-M30.

## 5. Statut juridique et plan d'immatriculation

| Temps | Véhicule | Rôle | État |
|---|---|---|---|
| Court terme (2026) | Entreprise individuelle — David Phaneuf | Exploitation actuelle, premiers revenus | **NEQ en cours d'obtention** |
| Moyen terme | IVIA OBNL (LCQ Partie III) | Mission, partenariats publics, fonds philanthropiques | À constituer |
| Structuration | Entité commerciale (cible : SPA à mission, LSAQ) | MERLIN, B2B Loi 27, capital privé, RS&DE/CRIC | À constituer |

Chaque demande de financement est déposée par le véhicule admissible au
moment du dépôt ; aucun numéro ni forme n'est revendiqué avant son existence.

## 6. Coordonnées et identifiants administratifs

| Champ | Valeur |
|---|---|
| Porteur actuel | David Phaneuf, entreprise individuelle — **À compléter : NEQ** (immatriculation REQ en cours) |
| Entités à venir | IVIA OBNL puis entité commerciale — NEQ respectifs à leur constitution |
| Fondateur et contact principal | David Phaneuf — david@ivia.quebec |
| Contact général | bonjour@ivia.quebec |
| Responsable protection des renseignements personnels | confidentialite@ivia.quebec |
| Contact investisseurs | invest@ivia.quebec (**à activer**) |
| Adresse | 1556, boulevard Saint-Joseph Est, Montréal (Québec) — **À compléter : code postal** |
| Téléphone | 438 221-0353 |
| Site / plateforme | https://ivia.quebec · API : https://api.ivia.quebec/api/docs |

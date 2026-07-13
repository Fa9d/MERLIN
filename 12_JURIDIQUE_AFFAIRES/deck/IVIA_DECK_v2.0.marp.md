---
marp: true
theme: ivia
paginate: true
footer: 'IVIA — Confidentiel · juillet 2026'
title: IVIA — Pitch investisseurs v2.0
description: Plateforme québécoise de santé mentale — produit en production
---

<!--
SCRIPT ORAL 7 MIN (VERSION RESSERREE)

0:00-0:30  Cover (IVIA)
- Message: produit en production, on parle d'acceleration, pas d'idee.

0:30-1:00  Detresse massive
- Message: besoin structurel + acces limite = fenetre concrete.

1:00-1:30  Solution infrastructure
- Message: parcours complet operationnel, validation humaine integree.

1:30-2:00  IVIA · MERLIN · MESANGES
- Message: investissement sur une architecture complete, pas un module isole.

2:00-2:30  Infrastructure de production
- Message: actif verifiable en ligne, fondation technique deja en place.

2:30-3:00  Economie IA
- Message: couts traces, lisibles, pilotables; pas de zone opaque.

3:00-3:30  Financement 2026
- Message: articulation public/prive coherente et complementaire.

3:30-4:15  Financer l'acceleration
- Message: capital oriente execution, equipe, conformite et deploiement.

4:15-5:00  Chaque dollar -> jalon
- Message: allocation disciplinee, logique par etapes et preuves.

5:00-5:40  Etat cible 2029
- Message: scenario median ambitieux mais realiste, trajectoire durable.

5:40-6:20  Slide conclusion "Investir dans IVIA"
- Message: lieu habitable, gouvernance claire, impact concret.

6:20-7:00  Q&A courte
- Message: ouvrir sur 3 questions: allocation, risques, cadence execution.
-->

<!-- _class: cover -->
<!-- _paginate: false -->
<!-- _footer: '' -->

# IVIA

## Au sein de l'être — En actes.

**Plateforme québécoise de santé mentale**
MERLIN structure · IVIA accueille

Produit **en production** — Montréal, Québec — juillet 2026
Version 2.1 — traction réelle

<!--
Bienvenue. IVIA n'est plus un projet prévu : la plateforme est en production. Le site public, l'espace client, l'espace praticien, la console admin et l'API sont en ligne. Cette version du deck met à jour la promesse de mai 2026 avec l'exécution réelle de juillet 2026.
-->

---

# Détresse massive, système saturé

<div class="kpi">
<div><span class="v">16 000</span><span class="l">en attente publique</span></div>
<div><span class="v">6–24 mois</span><span class="l">de délais</span></div>
<div><span class="v">75 %</span><span class="l">ne consultent pas</span></div>
</div>

- Privé : **120–180 $ / séance** — inaccessible pour beaucoup
- Jeunes : détresse psychologique élevée
- Un vide entre l'absence de réponse et le soin spécialisé

<!--
Les données de marché n'ont pas changé : le Québec manque de capacité d'écoute. IVIA se positionne dans l'espace entre l'absence de réponse et le soin spécialisé : écoute structurée, orientation prudente, validation humaine, respect strict du cadre québécois.
-->

---

# La solution : une infrastructure de pratique d'écoute

- **Parcours complet** : intake → réservation → paiement → séance
- Audio/vidéo **LiveKit** intégré
- Transcription **locale** (faster-whisper) — l'audio ne sort pas
- Analyses IA **sous validation humaine**
- Documents livrés au client

> MERLIN n'est pas un chatbot clinique : c'est une infrastructure de pratique, gouvernée par le praticien.

<!--
Le parcours bout en bout fonctionne aujourd'hui : une personne arrive sur ivia.quebec, soumet une demande, reçoit un magic link, réserve un créneau réel, paie, tient une séance audio/vidéo, puis reçoit des documents validés par le praticien.
-->

---

# IVIA · MERLIN · MÉSANGES

## Ce que les investisseurs financent

- **IVIA — Maison du vivant**  
   Lieu public où les personnes arrivent, reviennent, se situent dans leurs axes de vie.  
   On finance : l'accueil, l'expérience, la capacité à tenir ce lieu dans le temps.

- **MERLIN — Coeur d'analyse et de gouvernance**  
   Structure les données, encadre les capacités d'IA, garantit la conformité (Loi 25, données au Québec).  
   On finance : l'infrastructure, les moteurs d'analyse encadrés, les cadres de sécurité.

- **MÉSANGES — Voix d'accompagnement subtile**  
   Reflets, miroirs, lectures prudentes, toujours en **Observation / Hypothèse / Orientation**.  
   On finance : la manière dont IVIA reste présent dans le temps auprès des personnes.

<!--
Slide d'alignement BP/pitch : la demande d'investissement porte sur une architecture complète,
pas sur une simple fonctionnalité applicative.
-->

---

# Gouvernée par principes, pas seulement KPIs

- Le **vivant d'abord** — autonomie émotionnelle comme horizon
- **Pas de diagnostic automatisé**, pas de prescription
- Orientation **sans commission cachée**
- La **sortie honorable** fait partie du produit
- Principes **opposables juridiquement** — structure, contrats, interfaces

<!--
La doctrine reste le cœur. IVIA ne diagnostique pas, ne prescrit pas, ne remplace pas les services d'urgence, et n'enferme pas le client dans un abonnement.
-->

---

# Une offre en production, configurable, opérable

| Offre | Contenu |
|---|---|
| **Client** | Intake → réservation → paiement → séance → documents |
| **Praticien** | Créneaux, séances, enregistrements, validations |
| **Admin** | Comptes, demandes, vigilance, facturation, droits |
| **Analytique** | Prosodie locale + sémantique IA + profilage contrôlé |

- Console admin séparée `/admin/` · Stripe actif + mode test
- **Vannes produit** activables en un clic

<!--
En mai, l'offre était une grille et une trajectoire. En juillet, elle est opérable : parcours client, praticiens, droits, paiements, documents et interrupteurs d'exposition analytique.
-->

---

# 4 strates, déploiement progressif gouverné

| Strate | Cible | État |
|---|---|---|
| **S1 IVIA Cœur** | Praticiens d'écoute | <span class="ok">Pilote en production</span> |
| **S2 IVIA Pros** | Psychologues, psychothérapeutes | Après audit ordres |
| **S3 IVIA Soins** | Corps, fréquence, alternatives | Après validation |
| **S4 IVIA Réseau** | Référencement éthique | Sans commission |

- Chaque strate s'ouvre par un **jalon de validation** — usage, conformité, stabilité

<!--
La logique multi-strates reste inchangée, mais S1 n'est plus théorique. Le palier technique de l'écoute, de la séance, de l'enregistrement et de la livraison documentaire est construit.
-->

---

# Transformer la parole sans l'exposer

```
Consentement → Séance → Enregistrement → Transcription locale
   → Analyse contrôlée → Validation praticien → Document client
   → Audit · effacement · données minimisées
```

- Consentements capturés **par contexte**
- Audio traité **sur serveur IVIA** — transcription locale
- Documents **validés par le praticien**
- Accès sensibles **journalisés**

<!--
La différence majeure est la transcription locale : l'audio ne quitte pas le serveur. Les analyses sensibles sont contrôlées par profils d'exposition et les accès journalisés. La chaîne de traitement n'est pas conforme en intention seulement : elle est implémentée.
-->

---

# L'avantage défendable : doctrine, données, moteur, conformité

- Chaîne de traitement gouvernée **déjà déployée**
- Moteur analytique **propriétaire actif**
- Conformité **Loi 25 intégrée au produit**
- **Profils d'exposition** contrôlés (vannes par profil)
- La confiance est difficile à copier

<!--
L'avantage défendable s'est matérialisé : moteur plein avec vannes par profil — client Québec conforme Loi 25/21, praticien certifié, recherche sociétale. Les inférences sensibles ne sont pas exposées par défaut.
-->

---

# Le marché : TAM Québec 110–210 M$ / an

| Strate | Praticiens | Potentiel |
|---|---|---|
| S1 écoute | 3 500–5 000 | ~12–36 M$ |
| S2 ordres | 12 000+ | ~58–86 M$ |
| S3 soins | 15 000+ | ~36–72 M$ |
| S4 réseau | 30 000+ | ~6–15 M$ |

- Employeurs : coût psychosocial majeur · le privé est déjà utilisé
- Cible M36 : **une part très modeste du TAM suffit**

<!--
IVIA ne cherche pas à conquérir tout le marché : devenir la référence francophone québécoise sur l'écoute structurée, la conformité et la gouvernance des données sensibles.
-->

---

# Souveraineté numérique : Loi 25 explicite

- Veille : les concurrents sont **peu explicites** sur la Loi 25
- IVIA : conformité **documentée** et intégrée
- Audio : **aucun export externe**
- Hébergement OVH, TLS, PostgreSQL — données au Québec
- Sauvegardes **AES-256 automatisées**

<!--
L'API FastAPI est en ligne sur api.ivia.quebec, PostgreSQL 15, Docker, nginx TLS, OVH. Sauvegardes AES-256 quotidiennes, copie hors-site OVH Québec en cours. La transcription audio est locale : aucune donnée audio ne part vers un tiers.
-->

---

# Pivot Loi 27 : une obligation légale devient marché

- Loi 27 **en vigueur** depuis octobre 2025
- Employeurs **20+ employés** concernés
- Risques **psychosociaux** explicitement visés
- Besoin réel **hors PAE classique**
- IVIA prépare l'offre **employeurs** — après stabilisation S1

<!--
IVIA n'est pas un PAE ni un service clinique d'urgence. C'est une infrastructure d'écoute et de structuration, complémentaire aux démarches RH et prévention, quand S1 sera stabilisé.
-->

---

# Six différenciateurs maintenant vérifiables

- **Non-clinique assumé**, documenté
- Multi-strates, **vannes par profil**
- **Loi 25 intégrée** au produit
- Ancrage **11 nations** du Québec
- **Sortie honorable** visible dans le produit
- IP : indicateur de temporalité décalée — *prior art GitHub, 9 mai 2026*

<!--
Les différenciateurs de v1.3 demeurent, mais plusieurs sont vérifiables dans le produit : profils d'exposition, console admin, journalisation, documents juridiques, transcription locale, droits praticiens.
-->

---

# Propriété intellectuelle collective

- **Pas de brevet privatif** — prior art GitHub horodaté
- Licence **recherche ouverte** encadrée
- Licence **commerciale doctrinale**
- Volet universitaire à amorcer

**Actifs IP** :
1. Indicateur de temporalité décalée
2. Méthode des 4 voies d'entrée
3. Couplage anti-funnel / calendrier
4. Moteur d'exposition par profils

<!--
La stratégie IP n'est pas de verrouiller la connaissance commune, mais d'empêcher son appropriation abusive. Nouvel actif depuis v1.3 : l'architecture moteur plein / vannes par profil.
-->

---

# IVIA seul sur l'intersection critique

| Critère | IVIA | Inkblot | TELUS | BetterHelp | Teladoc |
|---|:-:|:-:|:-:|:-:|:-:|
| FR québécois natif | ✓ | ~ | ~ | ✗ | ✗ |
| Loi 25 explicite | ✓ | ✗ | ✗ | ✗ | ✗ |
| Audio local souverain | ✓ | ✗ | ✗ | ✗ | ✗ |
| Non-clinique structuré | ✓ | ✗ | ✗ | ✗ | ✗ |
| Sortie honorable | ✓ | ✗ | ✗ | ✗ | ✗ |
| Vannes inférences | ✓ | ✗ | ✗ | ✗ | ✗ |

<!--
Inkblot, TELUS, BetterHelp et Teladoc disposent de moyens supérieurs, mais ne combinent pas l'ancrage québécois, la Loi 25 explicite, l'audio local, la doctrine anti-funnel et les vannes d'inférence. IVIA occupe une intersection très précise.
-->

---

# Une infrastructure de production déjà opérante

| Composant | État |
|---|---|
| Site public | `https://ivia.quebec` — en ligne |
| API | `https://api.ivia.quebec` — en ligne |
| Admin | `/admin/` séparé |
| Séance | LiveKit audio/vidéo |
| Transcription | faster-whisper **local** |
| Sauvegardes | AES-256, cron quotidien |

- FastAPI · PostgreSQL 15 · Docker · nginx TLS · OVH

<!--
En v1.3, l'infrastructure était une fondation prévue. En v2.0, elle existe. La plateforme est prête pour l'intégration de praticiens partenaires, avec un praticien actif aujourd'hui : le fondateur.
-->

---

# Économie IA

## Coûts mesurés, pas une boîte noire

- Chaque appel IA (Claude) est tracé :  
   modèle · tokens · coût USD · conversion CAD.

- Les coûts sont **rattachés à des finalités claires** :  
   note de séance, synthèse de journal, reflet client, reflet praticien, insights.

- Une console d'**économie IA** montre :  
   coûts par modèle, par usage, par séance, croisés avec les revenus.

> Pour l'investisseur : une IA utile, encadrée, dont les coûts sont lisibles,
> intégrés au BP et aux décisions de financement.

<!--
Les coûts d'IA ne sont pas estimés au doigt mouillé : ils sont instrumentés et pilotables.
Cela sécurise la marge et la trajectoire de financement.
-->

---

# Modèle économique pilote : coût fortement réduit

| Service | Tarif |
|---|---|
| BetterHelp | 240–400 $ USD / mois |
| Talkspace | 396 $ USD / mois |
| Inkblot Therapy | ~90 $ CAD / heure |
| Psychologue privé | 120–180 $ CAD / séance |
| **IVIA pilote** | **80 $ CAD / séance** |

- Stripe actif + mode test · offre gratuite activable
- **Palier 1 quasi-autofinancé** — l'IA comme levier de productivité

<!--
Le plan prévoyait ~50 K$ pour le palier 1 pilote. En pratique : quasi-autofinancement, une fraction du budget, grâce au développement assisté par IA. Le financement sert à accélérer le déploiement responsable, pas à prouver que le produit peut exister.
-->

---

# Les leviers de revenus (grille BP v2.3)

| Levier | Tarif | État |
|---|---|---|
| Séance d'écoute (client) | 80 $ / 60 min (pilote) | En production |
| Frais plateforme par séance (praticien) | 3,90–12,90 $ selon plan et volume | Grille définie |
| Abonnement mensuel praticien | 27,99–84,99 $ selon palier | Grille définie |
| Services analytiques à la carte | 1–8 $ / séance | Moteur déployé |
| Enregistrement solo + transcription | 35 $ | En production |
| Journal étendu (client) | 7 $/mois au-delà du seuil gratuit | Cadré |
| Employeurs Loi 27 | 5–15 K$/an par employeur | An 1 : 25–300 K$ potentiel |
| Diffusion MÉSANGES (dons, commandites éthiques) | — | 0–15 K$ palier 1 → 150–350 K$ palier 3 |

<!--
Le revenu ne repose pas sur la seule séance. Huit leviers documentés dans le plan d'affaires v2.3 : la séance client, les frais plateforme et l'abonnement praticien selon trois plans et trois paliers de volume, les services analytiques à la carte, l'enregistrement solo, le journal étendu au-delà du seuil gratuit de 50 entrées par mois, l'offre employeurs Loi 27 et la diffusion MÉSANGES. Les leviers employeurs et journal ne sont pas budgétés dans le scénario médian : ils constituent un potentiel de hausse.
-->

---

# Trajectoire 36 mois — scénario médian, jalons de validation

| | M3 | M6 | M12 | M18 | M24 | M36 |
|---|---|---|---|---|---|---|
| Praticiens actifs | 3 | 8–10 | 30–40 | 50–70 | 90–130 | 200–350 |
| Clients actifs (est.) | ~30 | ~100 | ~350 | ~800 | ~1 500 | ~3 500 |
| RMR portefeuille | ~0,7 K$ | ~4 K$ | ~16,5 K$ | ~32 K$ | ~63 K$ | ~177 K$ |
| RAR équivalent | ~8 K$ | ~48 K$ | ~198 K$ | ~384 K$ | ~756 K$ | ~2,1 M$ |

- RMR / RAR = revenus mensuels / annuels récurrents
- Jalons avant chaque palier · équilibre courant vers **M28–M32**
- Journal étendu et employeurs Loi 27 **non budgétés** : potentiel de hausse

<!--
Trajectoire du scénario médian du plan d'affaires v2.3, portefeuille complet : MERLIN environ 125 K$ de revenus mensuels récurrents à M36, MÉSANGES environ 22 K$, autres sous-marques environ 30 K$. Les clients actifs sont une estimation dérivée du volume de séances par praticien. Ces cibles restent une trajectoire, pas une promesse : le risque technique initial a diminué, le risque se déplace vers l'acquisition, l'intégration et la rétention.
-->

---

# Variantes : praticiens × clients × revenus (M36)

| Scénario | Praticiens | Clients actifs (est.) | RAR M36 |
|---|---:|---:|---:|
| Minimal (financement contraint) | MERLIN seul | ~1 000 | 700–900 K$ |
| Pessimiste (−30 % acquisition) | ~200 | ~2 500 | ~1,35 M$ |
| **Médian (référence)** | **200–280** | **~3 500** | **~2,1 M$** |
| Optimiste (+25 %) | ~350 | ~4 500 | 3,0–3,5 M$ |

- Optimiste inclut : employeurs Loi 27 (5–15 signés an 1, 25–150 K\$) et journal étendu (1 000–3 000 abonnés, +7 à 21 K\$ RMR)
- Journal : ~30 % des clients actifs dépassent le seuil gratuit → 7 $/mois
- Financement requis : 2,5 M$ (pess.) · 2,2 M$ (médian) · 1,9–2,0 M$ (optim.)

<!--
Les quatre scénarios de sensibilité du plan d'affaires v2.3. Le scénario minimal, si le financement réuni est inférieur à 1,5 M$, concentre tout sur MERLIN et reporte les autres sous-marques. Le médian sert de référence au besoin de financement. L'optimiste active les leviers non budgétés : employeurs Loi 27 et journal étendu. Le journal suit une règle simple : environ 30 % d'une base de clients actifs dépasse le seuil gratuit — 100 clients donnent environ 210 $ par mois, 2 000 clients environ 4 200 $ par mois, avec une marge nette de 40 à 60 %.
-->

---

# Traction : production réelle, actifs vérifiables

- **ivia.quebec + API en ligne** — parcours client bout en bout
- Intake magic link → réservation → paiement → séance
- LiveKit → enregistrement → **transcription locale**
- Prosodie locale + sémantique Claude/Anthropic
- Profilage 5 couches, **vannes par profil**, audit d'accès
- Console admin complète · corpus juridique v1.1 / v2.0

<!--
C'est la diapositive qui change le plus. En mai, la traction était une fondation et un calendrier. En juillet, la traction est produit. Un praticien actif — le fondateur — et la plateforme est prête pour l'intégration de partenaires.
-->

---

# Feuille de route : palier 0 réalisé, accélération contrôlée

| Palier | Contenu | Jalon / échéance |
|---|---|---|
| **P0** <span class="ok">Réalisé</span> | Produit en production + pilote technique | Juillet 2026 |
| P1 · T3 2026 | Intégration partenaires S1 | 30+ séances |
| P2 · T4 2026 | Cohorte 5–8 + opérations admin | RMR 2 KMRR 2 K$+ |
| P3 · S1 2027 | Signaux, qualité, conformité S2 | RMR 8 KMRR 8 K$+ |
| P4 · S2 2027 | Employeurs Loi 27 + S2 encadré | RMR 25 KMRR 25 K$+ |
| P5 · 2028–29 | S3/S4 + recherche + modèle propriétaire | RMR 155 K$ |

<!--
La feuille de route est recalée à partir de juillet 2026. Le palier 0 et le pilote technique sont réalisés. Prochains jalons : intégration de praticiens partenaires, preuve d'usage réelle, stabilisation, puis offre employeurs Loi 27, S2, S3, S4 et recherche universitaire.
-->

---

# L'équipe : fondateur opérateur, produit construit

- **David Phaneuf**, fondateur — développement complet, IA, gouvernance
- Praticien actif initial
- **Exécution frugale démontrée** — plateforme complète, quasi-autofinancée
- Recrutements **par jalons** :

| Période | Recrutements |
|---|---|
| T3–T4 2026 | Conseiller juridique + praticiens partenaires |
| 2027 | Support dev + partenariats + conformité |
| 2028 | Responsable commercial employeurs + scientifique de données |
| 2029 | ML engineer + opérations multi-strates |

<!--
Le risque fondateur existe et reste lucide. Mais l'exécution récente réduit une incertitude majeure : une seule personne a construit et mis en production une plateforme complète. La priorité : ajouter les bonnes personnes aux bons jalons, sans diluer la doctrine.
-->

---

<!-- _class: divider -->

# Pourquoi maintenant ?

**Produit en production, pas une promesse** · Loi 27 crée la demande
Loi 25 favorise le local · confiance envers les apps IA fragilisée
Données gouvernées dès aujourd'hui

<!--
Le besoin est massif, les obligations employeurs sont en vigueur, la souveraineté numérique devient un critère réel. IVIA arrive au bon moment avec un avantage nouveau : le produit n'est plus théorique.
-->

---

# Risques principaux et mitigations

| Risque | Prob. | Mitigation |
|---|---|---|
| Adoption praticiens lente | Moyen | Intégration restreinte, accompagnement serré |
| Sous-performance des revenus récurrents | Moyen | Jalons, offres gratuites, itérations |
| Conformité S2 | Moyen | Audit avant ouverture ordres |
| Épuisement fondateur | Moyen | Financement support et délégation |
| Dérive analytique IA | Faible | Vannes, audit, validation humaine |

<!--
Le risque principal n'est plus « peut-on construire la plateforme ? » — la réponse est oui. Les risques sont l'adoption, la stabilité opérationnelle, la conformité, et la capacité de délégation autour du fondateur.
-->

---

# Financement 2026

## Programmes publics + investisseurs

**Programmes publics ciblés (déjà cartographiés)**
RS&DE · CRIC · Fondaction · Filaction · FAQDD · Investissement Québec · CDAE · PARI-CNRC · Mitacs

- Les programmes publics soutiennent l'**amorce et l'innovation**  
   R&D, structuration des analyses, conformité, démonstrations.

- Les investisseurs accompagnent la **stabilisation et la montée en puissance**  
   Capacité d'accueil, consolidation des équipes, industrialisation des cadres.

> Le BP décrit les montants et les scénarios.
> Ce deck montre comment les apports publics et privés s'emboîtent dans une architecture unique.

<!--
Slide charnière de financement : articulation public/privé cohérente avec
FINANCEMENT_PUBLIC_PROGRAMMES_2026.md et le BP v2.4.
-->

---

# Financer l'accélération, pas l'existence

<div class="kpi">
<div><span class="v">2,25 M$</span><span class="l">besoin total 36 mois</span></div>
<div><span class="v">100 K$</span><span class="l">première tranche</span></div>
<div><span class="v">600 K$</span><span class="l">pré-money</span></div>
</div>

- Dilution indicative : **14–18 %**
- Mix : subventions + capital patient + revenus
- Besoins : intégration praticiens, conformité, recherche universitaire, offre employeurs Loi 27

<!--
On ne demande pas au capital de financer une preuve abstraite : la preuve technique existe. Le capital sert à accélérer l'intégration, sécuriser la conformité, soutenir le fondateur, structurer l'offre employeurs, et transformer un produit en production en organisation durable.
-->

---

# Chaque dollar rattaché à un jalon

| Poste | Montant |
|---|---:|
| R&D et sécurité produit | 520 000 $ |
| Rémunération fondateur | 495 000 $ |
| Recrutements équipe | 540 000 $ |
| Marketing et commercial | 185 000 $ |
| Offre employeurs Loi 27 et partenariats | 60 000 $ |
| Recherche universitaire | 57 500 $ |
| Juridique, conformité, assurance | 130 000 $ |
| Infrastructure et sauvegardes | 70 000 $ |
| Charges structurelles | 242 500 $ |
| **TOTAL** | **2 300 000 $ max** |

<!--
Le palier technique ayant été construit à coût très réduit, une part plus importante va vers la sécurité, la conformité, l'intégration et la qualité. Montants indicatifs, pilotés par jalons, pas par calendrier rigide.
-->

---

# L'état cible en juillet 2029

<div class="kpi">
<div><span class="v">200–350</span><span class="l">praticiens actifs</span></div>
<div><span class="v">177 K$</span><span class="l">RMR cible (médian)</span></div>
<div><span class="v">~2,1 M$</span><span class="l">RAR cible (médian)</span></div>
</div>

- Équipe : 7–8 personnes · équilibre courant M28–M32
- Corpus synthétique : **5 000+ cas gouvernés**
- Chaîne de traitement auditable · co-publication scientifique visée · doctrine publique

<!--
En 2029, l'objectif n'est pas seulement une taille de revenus : c'est une infrastructure québécoise durable. La valorisation cible découle de cette crédibilité, pas d'une croissance artificielle.
-->

---

<!-- _class: divider -->
<!-- _paginate: false -->
<!-- _footer: '' -->

# Prochaines étapes

## Investir dans IVIA

- **On ne finance pas une app.**
  On finance une maison du vivant qui tient dans le temps, articulée entre IVIA (accueil), MERLIN (coeur d'analyse, Loi 25, données au Québec) et MÉSANGES (accompagnement subtil).

- **On ne finance pas en silo.**
  Les programmes publics soutiennent l'amorce et l'innovation.  
  L'investissement privé stabilise, consolide et déploie cette architecture.

- **On ne finance pas une boîte noire d'IA.**
  Les usages, les coûts et les garde-fous de l'IA sont instrumentés, lisibles, et intégrés à la gouvernance.

> Être investisseur dans IVIA, c'est rendre possible un lieu durable, habitable et responsable pour la santé mentale.

---

# Q&A — version courte

IVIA transforme un besoin social massif en infrastructure durable et gouvernée.

- Public + privé : même architecture, même cap.
- IA instrumentée : coûts lisibles, pilotage continu.

<!--
Je ne cherche pas des actionnaires qui pousseront IVIA à grandir plus vite que sa doctrine. Je cherche des partenaires patients qui comprennent que la confiance est l'actif principal. Prochaine étape : voir le produit, examiner les documents, valider les risques, financer l'accélération responsable.
-->

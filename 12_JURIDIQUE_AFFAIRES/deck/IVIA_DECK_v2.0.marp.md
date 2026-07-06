---
marp: true
theme: ivia
paginate: true
footer: 'IVIA — Confidentiel · juillet 2026'
title: IVIA — Pitch investisseurs v2.0
description: Plateforme québécoise de santé mentale — produit en production
---

<!-- _class: cover -->
<!-- _paginate: false -->
<!-- _footer: '' -->

# IVIA

## Au sein de l'être — En actes.

**Plateforme québécoise de santé mentale**
MERLIN structure · IVIA accueille

Produit **live** — Montréal, Québec — juillet 2026
Version 2.0 — traction réelle

<!--
Bienvenue. IVIA n'est plus un projet prévu : la plateforme est en production. Le site public, l'espace client, l'espace praticien, la console admin et l'API sont live. Cette version du deck met à jour la promesse de mai 2026 avec l'exécution réelle de juillet 2026.
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

# Une offre live, configurable, opérable

| Offre | Contenu |
|---|---|
| **Client** | Intake → réservation → paiement → séance → documents |
| **Praticien** | Créneaux, séances, enregistrements, validations |
| **Admin** | Comptes, demandes, vigilance, facturation, droits |
| **Analytique** | Prosodie locale + sémantique IA + profilage contrôlé |

- Console admin séparée `/admin/` · Stripe live + mode test
- **Vannes produit** activables en un clic

<!--
En mai, l'offre était une grille et une trajectoire. En juillet, elle est opérable : parcours client, praticiens, droits, paiements, documents et interrupteurs d'exposition analytique.
-->

---

# 4 strates, déploiement progressif gouverné

| Strate | Cible | État |
|---|---|---|
| **S1 IVIA Cœur** | Praticiens d'écoute | <span class="ok">Live pilote</span> |
| **S2 IVIA Pros** | Psychologues, psychothérapeutes | Après audit ordres |
| **S3 IVIA Soins** | Corps, fréquence, alternatives | Après validation |
| **S4 IVIA Réseau** | Référencement éthique | Sans commission |

- Chaque strate s'ouvre par un **gate** d'usage, de conformité, de stabilité

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
La différence majeure est la transcription locale : l'audio ne quitte pas le serveur. Les analyses sensibles sont contrôlées par profils d'exposition et les accès journalisés. Le pipeline n'est pas conforme en intention : il est implémenté.
-->

---

# Le moat : doctrine, données, moteur, conformité

- Pipeline gouverné **déjà déployé**
- Moteur analytique **propriétaire actif**
- Conformité **Loi 25 intégrée au produit**
- **Profils d'exposition** contrôlés (vannes par profil)
- La confiance est difficile à copier

<!--
Le moat s'est matérialisé : moteur plein avec vannes par profil — client Québec conforme Loi 25/21, praticien certifié, recherche sociétale. Les inférences sensibles ne sont pas exposées par défaut.
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
L'API FastAPI est live sur api.ivia.quebec, PostgreSQL 15, Docker, nginx TLS, OVH. Sauvegardes AES-256 quotidiennes, copie hors-site OVH Québec en cours. La transcription audio est locale : aucune donnée audio ne part vers un tiers.
-->

---

# Pivot Loi 27 : une obligation légale devient marché

- Loi 27 **en vigueur** depuis octobre 2025
- Employeurs **20+ employés** concernés
- Risques **psychosociaux** explicitement visés
- Besoin réel **hors PAE classique**
- IVIA prépare l'offre **B2B** — après stabilisation S1

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

# Une stack production déjà opérante

| Composant | État |
|---|---|
| Frontend | `https://ivia.quebec` — live |
| API | `https://api.ivia.quebec` — live |
| Admin | `/admin/` séparé |
| Séance | LiveKit audio/vidéo |
| Transcription | faster-whisper **local** |
| Sauvegardes | AES-256, cron quotidien |

- FastAPI · PostgreSQL 15 · Docker · nginx TLS · OVH

<!--
En v1.3, l'infrastructure était une fondation prévue. En v2.0, elle existe. La plateforme est prête pour l'onboarding de praticiens partenaires, avec un praticien actif aujourd'hui : le fondateur.
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

- Stripe live + mode test · offre gratuite activable
- **Palier 1 quasi-autofinancé** — l'IA comme levier de productivité

<!--
Le plan prévoyait ~50 K$ pour le palier 1 pilote. En pratique : quasi-autofinancement, une fraction du budget, grâce au développement assisté par IA. Le financement sert à accélérer le déploiement responsable, pas à prouver que le produit peut exister.
-->

---

# Trajectoire 36 mois, gates Go/No-Go

| | M3 | M6 | M12 | M18 | M27 | M36 |
|---|---|---|---|---|---|---|
| Praticiens | 2 | 8 | 15 | 45 | 140 | 350 |
| MRR | 500 $ | 3,5 K$ | 8,5 K$ | 28 K$ | 68 K$ | 155 K$ |
| ARR | — | 42 K$ | 102 K$ | 335 K$ | 810 K$ | 1,86 M$ |
| Marge brute | — | ~55 % | ~58 % | ~62 % | ~66 % | ~70 % |

- Hypothèses conservatrices · gates avant chaque palier · équilibre vers M28–M30

<!--
Ces cibles restent une trajectoire, pas une promesse. La nouveauté : le risque technique initial a diminué. Le risque se déplace vers l'acquisition, l'onboarding, la conformité opérationnelle et la rétention.
-->

---

# Traction : production réelle, actifs vérifiables

- **ivia.quebec + API live** — parcours client bout en bout
- Intake magic link → réservation → paiement → séance
- LiveKit → enregistrement → **transcription locale**
- Prosodie locale + sémantique Claude/Anthropic
- Profilage 5 couches, **vannes par profil**, audit d'accès
- Console admin complète · corpus juridique v1.1 / v2.0

<!--
C'est la slide qui change le plus. En mai, la traction était une fondation et un calendrier. En juillet, la traction est produit. Un praticien actif — le fondateur — et la plateforme est prête pour l'onboarding de partenaires.
-->

---

# Roadmap : palier 0 réalisé, accélération contrôlée

| Palier | Contenu | Gate / échéance |
|---|---|---|
| **P0** <span class="ok">Réalisé</span> | Produit live + pilote technique | Juillet 2026 |
| P1 · T3 2026 | Onboarding partenaires S1 | 30+ séances |
| P2 · T4 2026 | Cohorte 5–8 + opérations admin | MRR 2 K$+ |
| P3 · S1 2027 | Signaux, qualité, conformité S2 | MRR 8 K$+ |
| P4 · S2 2027 | B2B Loi 27 + S2 encadré | MRR 25 K$+ |
| P5 · 2028–29 | S3/S4 + recherche + modèle propriétaire | 155 K$ MRR |

<!--
La roadmap est recalée à partir de juillet 2026. Le palier 0 et le pilote technique sont réalisés. Prochains jalons : onboarding de praticiens partenaires, preuve d'usage réelle, stabilisation, puis B2B Loi 27, S2, S3, S4 et recherche universitaire.
-->

---

# L'équipe : fondateur opérateur, produit construit

- **David Phaneuf**, fondateur — full-stack, IA, gouvernance
- Praticien actif initial
- **Exécution frugale démontrée** — plateforme complète, quasi-autofinancée
- Recrutements **par gates** :

| Période | Recrutements |
|---|---|
| T3–T4 2026 | Conseiller juridique + praticiens partenaires |
| 2027 | Support dev + partenariats + conformité |
| 2028 | Commercial B2B + data scientist |
| 2029 | ML engineer + opérations multi-strates |

<!--
Le risque fondateur existe et reste lucide. Mais l'exécution récente réduit une incertitude majeure : une seule personne a construit et mis en production une plateforme complète. La priorité : ajouter les bonnes personnes aux bons gates, sans diluer la doctrine.
-->

---

<!-- _class: divider -->

# Pourquoi maintenant ?

**Produit live, pas promesse** · Loi 27 crée la demande
Loi 25 favorise le local · confiance envers les apps IA fragilisée
Données gouvernées dès aujourd'hui

<!--
Le besoin est massif, les obligations employeurs sont en vigueur, la souveraineté numérique devient un critère réel. IVIA arrive au bon moment avec un avantage nouveau : le produit n'est plus théorique.
-->

---

# Risques principaux et mitigations

| Risque | Prob. | Mitigation |
|---|---|---|
| Adoption praticiens lente | Moyen | Onboarding restreint, accompagnement serré |
| Sous-performance MRR | Moyen | Gates, offres gratuites, itérations |
| Conformité S2 | Moyen | Audit avant ouverture ordres |
| Épuisement fondateur | Moyen | Financement support et délégation |
| Dérive analytique IA | Faible | Vannes, audit, validation humaine |

<!--
Le risque principal n'est plus « peut-on construire la plateforme ? » — la réponse est oui. Les risques sont l'adoption, la stabilité opérationnelle, la conformité, et la capacité de délégation autour du fondateur.
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
- Besoins : onboarding, conformité, recherche universitaire, B2B Loi 27

<!--
On ne demande pas au capital de financer une preuve abstraite : la preuve technique existe. Le capital sert à accélérer l'onboarding, sécuriser la conformité, soutenir le fondateur, structurer le B2B, et transformer un produit live en organisation durable.
-->

---

# Chaque dollar rattaché à un gate

| Poste | Montant |
|---|---:|
| R&D et sécurité produit | 520 000 $ |
| Rémunération fondateur | 495 000 $ |
| Recrutements équipe | 540 000 $ |
| Marketing et commercial | 185 000 $ |
| B2B Loi 27 et partenariats | 60 000 $ |
| Recherche universitaire | 57 500 $ |
| Juridique, conformité, assurance | 130 000 $ |
| Infrastructure et sauvegardes | 70 000 $ |
| Charges structurelles | 242 500 $ |
| **TOTAL** | **2 300 000 $ max** |

<!--
Le palier technique ayant été construit à coût très réduit, une part plus importante va vers la sécurité, la conformité, l'onboarding et la qualité. Montants indicatifs, pilotés par gates, pas par calendrier rigide.
-->

---

# L'état cible en juillet 2029

<div class="kpi">
<div><span class="v">350</span><span class="l">praticiens actifs</span></div>
<div><span class="v">155 K$</span><span class="l">MRR cible</span></div>
<div><span class="v">1,86 M$</span><span class="l">ARR cible</span></div>
</div>

- Équipe : 7–8 personnes · équilibre courant M28–M30
- Dataset synthétique : **5 000+ cas gouvernés**
- Pipeline auditable · co-publication scientifique visée · doctrine publique

<!--
En 2029, l'objectif n'est pas seulement une taille de revenus : c'est une infrastructure québécoise durable. La valorisation cible découle de cette crédibilité, pas d'une croissance artificielle.
-->

---

<!-- _class: cover -->
<!-- _paginate: false -->
<!-- _footer: '' -->

# Prochaines étapes

## Au sein de l'être — En actes.

- **Démo produit disponible** · due diligence sous NDA
- Onboarding partenaires T3 2026 · première tranche automne 2026
- Partenaires **patients** recherchés

David Phaneuf, fondateur
**david@ivia.quebec** · invest@ivia.quebec · ivia.quebec

<!--
Je ne cherche pas des actionnaires qui pousseront IVIA à grandir plus vite que sa doctrine. Je cherche des partenaires patients qui comprennent que la confiance est l'actif principal. Prochaine étape : voir le produit, examiner les documents, valider les risques, financer l'accélération responsable.
-->

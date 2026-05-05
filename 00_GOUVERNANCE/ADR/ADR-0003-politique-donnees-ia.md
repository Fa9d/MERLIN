---
titre: Politique initiale de données et IA — contexte québécois et canadien
id: ADR-0003
statut: accepted
date: 2026-05-05
décideurs: fondateur
remplace: []
remplacé_par: []
---

# ADR-0003 — Politique initiale de données et IA : contexte québécois et canadien

> **Statut** : accepted — 2026-05-05
> **Couche** : FOND (politique de haut niveau) + PROD (contraintes d'implémentation)
> **Loi de référence** : Loi 25 (Québec) — Loi modernisant des dispositions législatives
> en matière de protection des renseignements personnels (RLRQ c P-39.1)
> **Loi fédérale** : LPRPDE — Loi sur la protection des renseignements personnels
> et les documents électroniques

---

## Contexte

MERLIN opère dans un contexte légal, culturel et éthique spécifique :

**Contexte légal** :
- La Loi 25 (Québec, entrée en vigueur progressive 2022-2023) impose des obligations
  strictes sur la collecte, le traitement, la conservation et le transfert des renseignements
  personnels. Elle s'applique à toute organisation qui collecte des données sur des personnes
  physiques situées au Québec.
- La LPRPDE s'applique aux organisations à caractère commercial au niveau fédéral.
- Les deux régimes ont des exigences en matière de consentement, de transparence,
  d'hébergement et de transfert de données hors Canada.

**Contexte opérationnel** :
- MERLIN traite des données potentiellement sensibles : séances cliniques,
  transcriptions audio, profils clients, informations de santé mentale.
- L'application IVIA envoie des données à des APIs externes (Anthropic, AssemblyAI,
  LiveKit) pour le traitement IA et la gestion des sessions audio.
- Ces fournisseurs sont principalement hébergés aux États-Unis.
- Le transfert de données hors Canada à destination de fournisseurs américains
  exige des garanties contractuelles et une évaluation des risques.

**Enjeu** :
En l'absence d'une politique formelle, des données sensibles pourraient être envoyées
brutes à des APIs externes sans arbitrage explicite ni évaluation des risques.
Cela constituerait une violation potentielle de la Loi 25 et un risque de réputation
pour MERLIN.

---

## Options considérées

**Option A — Politique permissive : envoyer les données au fur et à mesure des besoins**
Envoyer les données aux APIs IA sans filtrage ni évaluation préalable.
*Rejeté* : non conforme à la Loi 25. Risque légal élevé pour une organisation
qui traite des données de santé mentale.

**Option B — Politique restrictive : interdire tout envoi de données à des APIs externes**
Ne jamais envoyer de données réelles à des fournisseurs hors Canada.
*Rejeté* : rend MERLIN inopérant dans sa version actuelle (Anthropic, AssemblyAI sont externes).
Contredit les choix techniques déjà validés.

**Option C — Politique arbitrée : encadrer l'envoi de données par des règles explicites,
des niveaux de sensibilité, et des évaluations de risque documentées**
Distinguer les catégories de données, définir les règles par catégorie, documenter
les fournisseurs et les garanties, et exiger un arbitrage pour tout nouveau flux de données
sensibles vers l'extérieur.
*Retenu* : proportionné, défendable légalement, et compatible avec l'architecture actuelle.

---

## Décision

### Principe général

**Les données sensibles ne doivent pas être envoyées brutes à des APIs IA ou tierces
sans arbitrage explicite préalable.** Un arbitrage est requis pour tout nouveau flux
de données personnelles ou potentiellement identifiantes vers un fournisseur externe.

### Classification des données par niveau de sensibilité

| Niveau | Type de données | Règle |
|---|---|---|
| **Niveau 0 — Public** | Données sans aucun lien à une personne (ex. : prompts génériques, statistiques agrégées) | Envoi libre, pas de restriction |
| **Niveau 1 — Interne** | Données d'usage non identifiantes (ex. : métriques, logs d'erreur sans PII) | Envoi autorisé vers fournisseurs contractualisés |
| **Niveau 2 — Personnel** | Données nominatives, emails, numéros de téléphone, identifiants de compte | Exige consentement explicite + évaluation de risque |
| **Niveau 3 — Sensible** | Données de santé mentale, transcriptions de séances, historiques cliniques, données sur des mineurs | Exige arbitrage explicite + garanties contractuelles + évaluation de risque documentée |

### Règle sur l'hébergement

**L'hébergement canadien est le défaut stratégique pour les données de niveau 2 et 3.**

- Le VPS prod est hébergé en Europe (OVH — France). Ce choix est connu et accepté
  en phase initiale, sous réserve d'évaluation de risque documentée.
- Tout déplacement de l'hébergement vers un pays hors Canada / UE
  exige un arbitrage et une entrée dans le registre des décisions.
- Les données de niveau 3 ne doivent jamais être hébergées aux États-Unis
  sans garanties contractuelles spécifiques (clauses de protection des données,
  Privacy Shield ou équivalent), validées par un arbitrage.

### Règle sur les APIs IA externes (Anthropic, AssemblyAI)

- **Anthropic** : utilisé pour l'analyse IA des séances. Les données envoyées
  doivent être pseudonymisées dans la mesure du possible avant envoi.
  Aucune donnée nominative ou directement identifiante ne doit apparaître dans le prompt.
- **AssemblyAI** : utilisé pour la transcription audio. Les enregistrements audio
  transmis doivent être effacés des serveurs AssemblyAI dès que la transcription est complète.
  Cette garantie doit être documentée dans le contrat ou les conditions d'usage.
- Tout nouveau fournisseur IA ou tiers recevant des données de niveau 2+ exige un ADR.

### Règle sur le consentement

- Tout client dont les données sont traitées par MERLIN doit avoir donné un consentement
  éclairé, spécifique et documenté (voir `MERLIN_GOUV_POLICY_CONSENTEMENTS_SEANCES_DONNEES_v1.0.md`).
- Le consentement doit mentionner explicitement l'usage de l'IA, les fournisseurs tiers,
  et le droit de retrait.

### Règle sur les données de mineurs

- Les données concernant des personnes mineures appartiennent au niveau 3 par défaut.
- Leur traitement exige un ADR spécifique et la validation de la politique mineurs
  (`MERLIN_GOUV_POLICY_MINEURS_PARENTS_SANTE_MENTALE_v1.0.md`).

---

## Conséquences

### Avantages

- MERLIN dispose d'une politique de données défendable légalement en contexte québécois.
- Les arbitrages futurs sur de nouveaux flux de données ont un cadre clair.
- La conformité Loi 25 peut être démontrée à un auditeur ou à une autorité réglementaire.

### Inconvénients ou risques

- La pseudonymisation systématique des données avant envoi aux APIs IA ajoute
  une couche de traitement.
  → Règle : implémenter progressivement ; commencer par les données les plus sensibles.
- La vérification des garanties contractuelles des fournisseurs demande un suivi.
  → Règle : documenter dans `MERLIN_GOUV_CADRE_OPERATOIRE_TRAITEMENT_DONNEES_IVIA_MERLIN_V1.md`.

### Actions requises

- [ ] Vérifier les conditions d'usage d'AssemblyAI concernant la rétention des enregistrements.
- [ ] Documenter la politique de pseudonymisation dans le backend (Vague 2).
- [ ] Mettre à jour `MERLIN_GOUV_POLICY_CONSENTEMENTS_SEANCES_DONNEES_v1.0.md`
      pour mentionner explicitement Anthropic et AssemblyAI.
- [ ] Évaluer l'hébergement OVH/France par rapport aux exigences de la Loi 25
      (transfert hors Québec vers un pays sans protection équivalente).
- [ ] Ajouter l'entrée DEC-038 dans le registre de décisions.

---

## Références

- Loi 25 (Québec) : https://www.legisquebec.gouv.qc.ca/fr/document/lc/P-39.1
- LPRPDE (Canada) : https://www.priv.gc.ca/fr/sujets-lies-a-la-protection-de-la-vie-privee/lois-sur-la-protection-des-renseignements-personnels-au-canada/la-loi-sur-la-protection-des-renseignements-personnels-et-les-documents-electroniques-lprpde/
- Commission d'accès à l'information (CAI) : https://www.cai.gouv.qc.ca/

---

## Entrée registre associée

> DEC-038 | 2026-05-05 | données | politique initiale données IA — contexte québécois — hébergement canadien par défaut | validated | ADR-0003

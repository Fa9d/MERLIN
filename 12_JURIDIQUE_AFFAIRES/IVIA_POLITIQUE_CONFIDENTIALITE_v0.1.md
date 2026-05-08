---
titre: Politique de confidentialité — IVIA / MERLIN
id: JURIDIQUE-DIFF-003-B
version: 0.1
statut: draft (à valider par David + cabinet juridique avant publication)
auteur: Perplexity (rédaction initiale) — David Phaneuf (validation)
date_creation: 2026-05-07
loi_reference: Loi 25 (Québec, RLRQ c P-39.1) · LPRPDE (Canada)
adr_associe: ADR-0003-politique-donnees-ia
publication_cible: https://ivia.quebec/confidentialite
---

# Politique de confidentialité

**Dernière mise à jour : 7 mai 2026**
**Version : 0.1 (initiale)**

La présente politique encadre la manière dont IVIA et MERLIN (ci-après « la Plateforme ») collectent, utilisent, conservent, communiquent et protègent vos renseignements personnels. Elle est rédigée pour respecter la **Loi 25** du Québec (Loi modernisant des dispositions législatives en matière de protection des renseignements personnels) et la **LPRPDE** au niveau fédéral canadien.

> **À retenir en une phrase** : nous collectons le moins de données possible, uniquement pour rendre le service. Vos données sensibles (séances, transcriptions, notes) ne quittent jamais nos serveurs sans votre consentement explicite et sans garanties documentées.

---

## 1. Personne responsable de la protection des renseignements personnels

Conformément à l'article 3.1 de la Loi 25, une personne est désignée responsable de la protection des renseignements personnels au sein de l'organisation :

- **Personne responsable** : David Phaneuf, fondateur
- **Courriel dédié** : confidentialite@ivia.quebec
- **Délai de réponse cible** : 30 jours civils (conformément à la Loi 25)

Toute demande relative à vos renseignements personnels — accès, rectification, retrait, portabilité, plainte — doit être adressée à cette personne.

## 2. Renseignements que nous collectons

### 2.1 — Renseignements que vous nous fournissez directement

| Catégorie | Exemples | Quand |
|---|---|---|
| **Identité** | Nom, prénom, courriel, numéro de téléphone | Création de compte |
| **Profil** | Préférences linguistiques, fuseau horaire, code postal (3 premiers caractères) | Inscription |
| **Demande d'écoute** | Réponses au formulaire de besoin (5-7 questions courtes) | Formulaire `/demarche` |
| **Contenu de séance** | Enregistrement audio de la séance (si vous y consentez), transcription textuelle, notes du praticien | Pendant la séance |
| **Paiement** | Données bancaires gérées **directement par Stripe Canada** — IVIA ne stocke jamais votre numéro de carte | Au moment du paiement |
| **Communications** | Courriels et messages que vous nous adressez | À votre initiative |

### 2.2 — Renseignements collectés automatiquement

| Catégorie | Détail | Finalité |
|---|---|---|
| **Données techniques** | Adresse IP, type de navigateur, système d'exploitation | Sécurité, prévention de la fraude, débogage |
| **Cookies de session** | Identifiant de session chiffré | Maintien de votre connexion |
| **Journaux d'accès** | Horodatage, page consultée, code de réponse HTTP | Diagnostic technique, sécurité |

**Aucun cookie publicitaire, aucun cookie de profilage tiers, aucun pixel de réseau social** n'est déposé sur le site IVIA. Nous n'utilisons pas Google Analytics ni Meta Pixel.

### 2.3 — Renseignements que nous ne collectons pas

Pour être clairs sur ce que **nous évitons délibérément** :

- Aucun numéro d'assurance maladie (RAMQ) ni numéro d'assurance sociale
- Aucun antécédent médical détaillé sauf si vous choisissez de l'inscrire vous-même dans une note
- Aucune donnée de géolocalisation précise (seulement les 3 premiers caractères du code postal pour l'analyse régionale)
- Aucun contenu de vos comptes de réseaux sociaux

## 3. Finalités du traitement

Vos renseignements sont traités exclusivement pour les finalités suivantes :

1. **Vous offrir le service IVIA** — création de compte, formulaire de besoin, suggestion d'un praticien partenaire, réservation de séance, déroulement de la séance audio, génération du rapport (si vous le demandez).
2. **Sécuriser la plateforme** — prévention des accès non autorisés, lutte contre la fraude, sauvegardes.
3. **Améliorer le service** — analyse statistique anonymisée (sans identification individuelle).
4. **Répondre à nos obligations légales** — conservation des pièces comptables, réponse à une ordonnance judiciaire valide.
5. **Vous communiquer des informations utiles** — confirmations de rendez-vous, rappels, infolettre Mésange (uniquement si vous y êtes inscrit explicitement, avec retrait possible à tout moment).

**Toute utilisation à des fins de marketing ciblé, de revente à des tiers ou d'entraînement de modèles d'intelligence artificielle externes est interdite par notre politique interne** (voir [ADR-0003 sur la politique de données](https://github.com/Fa9d/MERLIN/blob/master/00_GOUVERNANCE/ADR/ADR-0003-politique-donnees-ia.md)).

## 4. Bases légales du traitement

Conformément à la Loi 25 et à la LPRPDE :

| Finalité | Base légale |
|---|---|
| Création de compte, prestation du service | Exécution d'un contrat (vous + IVIA) |
| Enregistrement audio, transcription, génération de rapport | **Consentement explicite** (case à cocher dédiée, retirable) |
| Envoi à un fournisseur IA (Anthropic, AssemblyAI) | Consentement explicite + arbitrage documenté (voir section 6) |
| Sauvegardes, sécurité, journaux | Intérêt légitime + obligation légale |
| Conservation comptable | Obligation légale (Loi sur les impôts du Québec) |
| Infolettre Mésange | Consentement explicite (opt-in, jamais opt-out par défaut) |

## 5. Durées de conservation

| Type de donnée | Durée de conservation | Après expiration |
|---|---|---|
| Compte utilisateur actif | Tant que le compte est actif | — |
| Compte inactif (sans connexion) | 24 mois après dernière connexion | Suppression automatique avec préavis 30 jours |
| Réponses au formulaire de besoin | 12 mois | Suppression automatique |
| Enregistrement audio de séance | **Maximum 90 jours** sauf demande explicite de conservation prolongée | Suppression irréversible |
| Transcription textuelle | 24 mois (utile pour suivi praticien) | Anonymisation puis suppression |
| Notes du praticien | Selon les obligations professionnelles du praticien (généralement 5 ans pour une note clinique) | Conservation par le praticien sous sa responsabilité |
| Rapports générés | 24 mois sur la plateforme, téléchargeables à tout moment | Suppression de la copie serveur |
| Données de paiement | 7 ans (obligation comptable Revenu Québec) | Archivage chiffré |
| Journaux d'accès techniques | 12 mois | Purge automatique |

**Vous pouvez à tout moment demander la suppression anticipée d'une de ces catégories** — voir section 9 (vos droits).

## 6. Communication à des tiers — fournisseurs et sous-traitants

IVIA fait appel à un nombre limité de fournisseurs spécialisés pour assurer le service. Chaque fournisseur est encadré contractuellement et fait l'objet d'une évaluation documentée (voir [ADR-0003](https://github.com/Fa9d/MERLIN/blob/master/00_GOUVERNANCE/ADR/ADR-0003-politique-donnees-ia.md)).

| Fournisseur | Rôle | Données concernées | Localisation |
|---|---|---|---|
| **OVH SAS** | Hébergement applicatif et base de données | Toutes données opérationnelles | France (UE) |
| **Stripe Canada** | Traitement des paiements | Identité, courriel, données de carte (jamais stockées par IVIA) | Canada (siège canadien) + États-Unis |
| **Anthropic (Claude API)** | Analyse intelligente des notes et formulaires | Texte des notes et réponses, **pseudonymisé avant envoi** | États-Unis |
| **AssemblyAI** | Transcription audio des séances | Fichiers audio (effacés du serveur AssemblyAI dès transcription terminée) | États-Unis |
| **Deepgram** *(fallback transcription)* | Transcription audio de secours | Idem AssemblyAI | États-Unis |
| **LiveKit** | Infrastructure de séance audio temps réel | Flux audio en direct (non stocké par LiveKit) | Hébergement IVIA OVH (open source self-hosted) |

### Transferts hors Canada

Certains fournisseurs (Anthropic, AssemblyAI, Deepgram) sont situés aux États-Unis. Conformément à l'article 17 de la Loi 25, nous avons procédé à une **évaluation des facteurs relatifs à la vie privée (EFVP)** pour ces transferts. Les principales mesures de protection sont :

- **Pseudonymisation systématique** des données envoyées aux APIs IA (suppression des noms, adresses, numéros de téléphone avant envoi)
- **Effacement immédiat** des fichiers audio sur les serveurs AssemblyAI dès la fin de la transcription (clause contractuelle vérifiée)
- **Aucun usage des données** par ces fournisseurs pour entraîner leurs propres modèles (clause contractuelle)
- **Choix d'un hébergement principal en Union européenne** (OVH France) plutôt qu'aux États-Unis pour les données de niveau le plus sensible

Une copie de l'EFVP peut être obtenue sur demande à confidentialite@ivia.quebec.

### Aucune vente, aucun courtier de données

IVIA **ne vend, ne loue, ne partage et ne cède jamais** vos renseignements personnels à des courtiers en données, des annonceurs ou des tiers à des fins commerciales.

### Communication imposée par la loi

Vos renseignements peuvent être communiqués sans votre consentement uniquement si la loi nous y oblige (ordonnance judiciaire valide d'un tribunal québécois ou canadien, demande légale d'une autorité publique). Dans la mesure permise par la loi, nous vous en informerions.

## 7. Sécurité

IVIA met en œuvre des mesures techniques et organisationnelles raisonnables pour protéger vos renseignements :

- **Chiffrement en transit** — TLS 1.2+ sur toutes les communications (Let's Encrypt, certificats renouvelés automatiquement)
- **Chiffrement au repos** — base de données chiffrée au niveau du système de fichiers
- **Hachage des mots de passe** — algorithme bcrypt, jamais de mot de passe en clair
- **Contrôle d'accès** — séparation stricte des rôles (client / praticien / opérateur / superviseur / admin), audit en cours (référence interne ROLES-010)
- **Sauvegardes** — quotidiennes, conservées 30 jours, chiffrées
- **Journaux d'accès** — toute action sensible est journalisée pour traçabilité
- **Mise à jour régulière** — dépendances et système maintenus à jour

**En cas d'incident de confidentialité présentant un risque sérieux**, nous nous engageons à :

1. Vous en informer dans les meilleurs délais
2. Notifier la Commission d'accès à l'information du Québec (CAI), conformément à la Loi 25
3. Tenir un registre interne des incidents

## 8. Cookies

Le site IVIA utilise un nombre limité de cookies, tous **strictement nécessaires** au fonctionnement du service :

| Cookie | Finalité | Durée |
|---|---|---|
| `session_id` | Maintenir votre connexion | Fin de session ou 7 jours |
| `csrf_token` | Protection contre les attaques CSRF | Fin de session |
| `lang` | Mémoriser votre préférence de langue | 12 mois |

Aucun cookie publicitaire, aucun cookie de mesure tierce (Google, Meta, TikTok, etc.) n'est déposé. **Nous n'avons donc pas besoin de bandeau de consentement complexe** — votre consentement aux cookies fonctionnels est implicite à votre utilisation du service.

## 9. Vos droits

En vertu de la Loi 25 et de la LPRPDE, vous disposez des droits suivants sur vos renseignements :

| Droit | Comment l'exercer |
|---|---|
| **Accès** — savoir quelles données nous détenons sur vous | Demande à confidentialite@ivia.quebec — réponse sous 30 jours |
| **Rectification** — corriger une donnée inexacte | Directement dans votre espace utilisateur ou par courriel |
| **Suppression** — demander l'effacement | Bouton « Supprimer mon compte » dans les paramètres, ou par courriel |
| **Portabilité** — recevoir vos données dans un format structuré (JSON) | Sur demande à confidentialite@ivia.quebec |
| **Retrait du consentement** — pour les traitements qui en dépendent | À tout moment, dans les paramètres ou par courriel |
| **Opposition** — refuser un traitement (ex. : infolettre) | Lien de désinscription en bas de chaque envoi, ou par courriel |
| **Plainte** | Auprès de la Commission d'accès à l'information du Québec : [cai.gouv.qc.ca](https://www.cai.gouv.qc.ca) |

L'exercice de ces droits est **gratuit**. Vous ne subirez aucune dégradation de service pour avoir exercé un droit.

## 10. Données des personnes mineures

IVIA est destiné aux personnes majeures (18 ans et plus). Le traitement de données concernant des personnes mineures est strictement encadré :

- Pour une personne de **moins de 14 ans** : consentement obligatoire d'un parent ou tuteur légal
- Pour une personne de **14 à 17 ans** : consentement de la personne mineure ET d'un parent ou tuteur

Si vous estimez qu'un compte concernant une personne mineure a été créé sans consentement parental approprié, contactez-nous à confidentialite@ivia.quebec — nous procéderons à la suspension immédiate et à la vérification.

## 11. Décisions automatisées et intelligence artificielle

Conformément à l'article 12.1 de la Loi 25 :

- **Aucune décision produisant des effets juridiques significatifs n'est prise de façon entièrement automatisée** sur la plateforme IVIA.
- L'analyse IA des formulaires sert à **suggérer** un praticien adapté ; la décision finale d'accepter ou non une rencontre revient toujours au client et au praticien.
- L'analyse IA des séances sert à **assister** le praticien dans sa prise de notes ; le praticien valide ou modifie systématiquement avant tout usage.

Vous avez le droit d'obtenir une explication sur la logique d'une suggestion automatisée vous concernant. Adressez votre demande à confidentialite@ivia.quebec.

## 12. Modifications de la présente politique

Cette politique peut être modifiée pour refléter une évolution de nos pratiques ou de la législation. Toute modification substantielle vous sera notifiée :

- Par courriel à l'adresse associée à votre compte
- Par un avis visible sur le site lors de votre prochaine connexion
- Au moins 30 jours avant son entrée en vigueur, sauf urgence légale

L'historique des versions est public et consultable à : [github.com/Fa9d/MERLIN](https://github.com/Fa9d/MERLIN) (dossier `12_JURIDIQUE_AFFAIRES/`).

## 13. Comment nous joindre

| Type de demande | Courriel |
|---|---|
| Question générale sur la confidentialité | confidentialite@ivia.quebec |
| Exercice d'un droit (accès, rectification, suppression, etc.) | confidentialite@ivia.quebec |
| Signalement d'incident de sécurité | confidentialite@ivia.quebec |
| Question commerciale ou support | bonjour@ivia.quebec |

**Personne responsable** : David Phaneuf
**Délai de réponse cible** : 30 jours civils (article 32 de la Loi 25)

En cas d'insatisfaction de notre réponse, vous avez le droit de porter plainte à la **Commission d'accès à l'information du Québec** :
- Site : [cai.gouv.qc.ca](https://www.cai.gouv.qc.ca)
- Téléphone : 1 888 528-7741

---

*Document interne · Version 0.1 · 2026-05-07 · À valider par cabinet juridique spécialisé Loi 25/santé avant publication. Référence : DIFF-003 du backlog MERLIN_GOUV_BACKLOG_MAITRE_V2. ADR de référence : ADR-0003-politique-donnees-ia.*

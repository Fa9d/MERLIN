# IVIA — Consentement funnel quiz : conformité Loi 25 v1.0

**Date** : 9 mai 2026
**Document compagnon de** : `04_METHODES/IVIA_FUNNEL_QUIZ_TO_GUIDANCE_v1.0.md`
**Référence légale** : Loi 25 (Loi modernisant des dispositions législatives en matière de protection des renseignements personnels), articles 8.1, 9, 28.1.
**Statut** : doctrine — à valider par avocat société multi-entités (cf. `brief_avocat_societe_multientites`).

---

## 1. Cartographie des données collectées par le funnel

| Écran | Donnée | Catégorie Loi 25 | Strate gouvernance IVIA | Délai conservation par défaut |
|---|---|---|---|---|
| 1 | Locale, source, variant A/B | Technique non-identifiante | A (technique) | 24 mois (analytics agrégés) |
| 2 | État du moment (4 valeurs) | Renseignement personnel sensible (santé mentale au sens large) | C (réponses qualifiées) | 30 min si pas de compte, sinon profil |
| 3 | Thèmes (multi-sélection) | Renseignement personnel sensible | C | 30 min si pas de compte, sinon profil |
| 3 | Champ libre "Autre" | Renseignement personnel sensible **non structuré** | D (texte libre chiffré) | 30 min si pas de compte, sinon journal |
| 4 | Voie d'entrée | Préférence non sensible | A | 24 mois agrégé |
| 5 | Rythme | Préférence non sensible | A | 24 mois agrégé |
| 6 | Mode d'écoute | Préférence non sensible | A | 24 mois agrégé |
| 7 | Texte d'ancrage | Renseignement personnel sensible | D (texte libre chiffré) | 30 min si pas de compte, sinon journal |
| 7 | Année souvenir évoqué | Renseignement personnel | E (temporalité décalée — IP collective) | Conservé chiffré si compte créé |
| 8 | Choix CTA | Comportemental | A | 24 mois agrégé |

**Strates** définies dans `00_DOCTRINE/politique_gouvernance_donnees_agregees_v1.md`.

---

## 2. Niveaux de consentement (granulaires)

Loi 25 art. 8.1 exige un consentement **manifeste, libre, éclairé, et donné à des fins spécifiques**. Pour le funnel IVIA :

### N0 — Consentement implicite minimal (Écran 1)

**Couvre** : strate A (technique, préférences non sensibles).
**Mécanisme** : mention sous bouton "Commencer le point".
**Texte** : "En continuant, vous acceptez nos Conditions et notre Politique de confidentialité. Aucune donnée personnelle n'est demandée avant la fin."
**Limites** : ne couvre **pas** les strates C/D/E.

### N1 — Consentement actif pour réponses sensibles (Écran 2 implicite, validé Écran 3)

**Couvre** : strate C (état du moment, thèmes structurés).
**Mécanisme** : visualisation explicite avant Écran 3 — "Les questions suivantes touchent votre état intérieur. Vos réponses sont anonymes tant que vous ne créez pas de compte. Elles s'effacent automatiquement après 30 minutes d'inactivité."
**Bouton de continuation** : "J'ai compris, je continue" (équivalent visuel à "Je préfère ne pas répondre").

### N2 — Consentement explicite pour texte libre (Écran 3 champ "Autre" + Écran 7 ancrage)

**Couvre** : strate D (texte non structuré chiffré).
**Mécanisme** : mention contextuelle au-dessus du champ — "Ce texte est chiffré au repos. Il n'est jamais affiché en clair côté administration. Si vous fermez la page sans créer de compte, il est détruit dans 30 minutes."
**Validation** : la simple saisie vaut consentement à la conservation temporaire (30 min). La conservation longue requiert création de compte = N3.

### N3 — Consentement écrit pour conservation longue (Écran 8 → création compte)

**Couvre** : strates C, D, et **E** (indicateur de temporalité décalée).
**Mécanisme** : page de création de compte **dédiée** (pas in-funnel), avec :
- Récapitulatif des données collectées pendant le funnel.
- Cases à cocher granulaires :
  - [ ] J'autorise IVIA à conserver mes réponses du quiz dans mon profil (strate C).
  - [ ] J'autorise IVIA à conserver mon texte d'ancrage et mon année souvenir, chiffrés (strate D + E).
  - [ ] J'autorise l'usage agrégé et anonymisé pour la recherche IVIA (strate E — indicateur de temporalité décalée). **Cette case est décochée par défaut.**
- Bouton "Créer mon compte" actif seulement si cases obligatoires (C) cochées. La case E reste optionnelle.

---

## 3. Procédure d'effacement (Loi 25 art. 28.1)

### Effacement avant création de compte

- **Automatique** : 30 min d'inactivité → destruction de la session côté serveur (cache Redis ou équivalent, TTL 30 min).
- **Manuel** : lien "Effacer mes données maintenant" visible sur tous les écrans 2-8. Un clic = destruction immédiate + redirection vers Écran 1 vierge.

### Effacement après création de compte

- Section dédiée du compte client : "Effacer mon compte et toutes mes données".
- Délai légal max : 30 jours (Loi 25 art. 28.1).
- Délai cible IVIA : **72 heures**.
- Confirmation par courriel + délai de grâce 24h pour annulation.
- Données agrégées strate E déjà anonymisées : **ne sont pas effaçables individuellement** (légal — pas un renseignement personnel au sens de la loi). Mention claire à l'utilisateur lors de la création de compte.

---

## 4. Mention obligatoire pour le champ libre Écran 3 "Autre"

Texte exact à afficher au-dessus du champ libre :

> Si rien ne correspond, vous pouvez décrire en quelques mots — maximum 200 caractères. Ce texte est chiffré et n'est jamais affiché en clair côté administration. Si vous fermez la page sans créer de compte, il est détruit dans 30 minutes. Évitez d'inscrire des données très identifiantes (nom, adresse, numéro de téléphone) ; le quiz n'en a pas besoin pour vous orienter.

---

## 5. Procédure de re-consentement

Si le funnel évolue de manière à modifier :
- les catégories de données collectées,
- les fins d'usage,
- les durées de conservation,

alors **tous les comptes existants** doivent recevoir un courriel de re-consentement, avec :
- Description claire du changement.
- Bouton "J'accepte" / "Je refuse".
- Si refus : possibilité de continuer sur le compte avec les anciennes conditions, ou de fermer le compte.

Délai de réponse minimum offert : **30 jours**. Pas de re-consentement implicite (par poursuite d'usage). Loi 25 art. 9 exige consentement éclairé et manifeste.

---

## 6. Registre des activités de traitement (RAT)

À jour dans `00_DOCTRINE/politique_gouvernance_donnees_agregees_v1.md` §RAT. Mise à jour requise avant lancement pilote :

- Ajouter ligne "Funnel quiz-to-guidance" avec fins, base légale (consentement art. 8.1), durée, destinataires (interne IVIA seul, jamais de tiers).
- Ajouter procédure escalade Commission d'accès à l'information (CAI) en cas d'incident.

---

## 7. Décisions à valider par avocat (escalade)

1. Le champ libre "Autre" en Écran 3 est-il un **renseignement personnel sensible** au sens de la Loi 25 même s'il est techniquement anonyme (pas d'identifiant lié) ? Recommandation : oui, traiter comme tel par précaution.
2. La conservation 30 min de session non-converti nécessite-t-elle une mention explicite d'autorité de contrôle (CAI) ? Recommandation : non, mais à confirmer.
3. La strate E (indicateur de temporalité décalée) anonymisée et agrégée : peut-on légalement la conserver indéfiniment et la valoriser auprès de tiers (recherche universitaire, MSSS) avec consentement N3 explicite ? Recommandation : oui sous conditions strictes — à formaliser dans contrat client à long terme.

---

*Au sein de l'être — En actes. Pour le peuple, par le peuple.*

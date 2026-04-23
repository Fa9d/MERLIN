# IVIA - Prompt Perplexity pour verification du discours de marque client V1

Date: 2026-04-21
Statut: actif
Objet: fournir un prompt unique et une liste de documents a transmettre a Perplexity pour verifier la solidite du discours de marque IVIA cote client payeur de seances

---

## 1) Documents a transmettre a Perplexity

Priorite haute:

1. [MERLIN_GOUV_ARCHITECTURE_MARQUE_PLATEFORMES_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_ARCHITECTURE_MARQUE_PLATEFORMES_V1.md)
2. [MERLIN_GOUV_POSITIONNEMENT_PUBLIC_SITE_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_POSITIONNEMENT_PUBLIC_SITE_V1.md)
3. [MERLIN_GOUV_DOCTRINE_APPUIS_THEORIQUES_MERLIN_v1.0.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_DOCTRINE_APPUIS_THEORIQUES_MERLIN_v1.0.md)

Priorite utile:

4. [page.tsx](C:/MERLIN/09_app_ivia_merlin/src/app/page.tsx)
5. [page.tsx](C:/MERLIN/09_app_ivia_merlin/src/app/rendez-vous/page.tsx)

Optionnel:

6. [MERLIN_GOUV_PLAN_EXECUTION_OPTIMAL_PROJET_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_PLAN_EXECUTION_OPTIMAL_PROJET_V1.md)

Regle:
- si tu veux un retour rapide, envoie seulement les 5 premiers;
- si tu veux un retour plus strategique, ajoute le 6e.

---

## 2) Prompt principal a copier dans Perplexity

```text
J'ai besoin d'une revue critique et strategique du discours de marque d'un service appele IVIA.

Contexte:
- IVIA est la porte publique cote client.
- MERLIN est le moteur methodologique et documentaire derriere IVIA.
- Le public vise ici n'est pas le praticien, mais la personne qui paie une seance pour etre ecoutee, clarifiee, orientee ou soutenue.
- Le service ne doit pas se presenter comme un acte medical, ni comme une psychotherapie cachee, ni comme une promesse de guerison.
- La doctrine centrale actuelle est: ecoute, clarification, orientation, continuite.
- La signature conceptuelle est: In Vivo In Actu = Au sein de l'etre - En acte.
- Une autre formule de campagne existe: La puissance du silence.

Je te transmets plusieurs documents de travail internes.

Ta mission:
1. Evaluer si le discours actuel est commercialement convaincant pour un client payeur de seances.
2. Evaluer s'il est suffisamment clair, desirable, credible et distinctif.
3. Dire si le discours est trop technique, trop abstrait, trop prudent, trop froid, trop clinique, trop poetique, ou insuffisamment incarné.
4. Identifier les contradictions entre:
   - la promesse client;
   - le cadre legal implicite;
   - l'experience emotionnelle promise;
   - la conversion commerciale.
5. Determiner ce que IVIA vend reellement du point de vue client:
   - une seance d'ecoute;
   - une seance de clarification;
   - une experience de soutien;
   - un espace de recentrage;
   - une aide a la decision;
   - autre.
6. Me dire si le discours donne vraiment envie de reserver et de payer.
7. Me dire ce qu'il manque pour qu'une personne se dise:
   - "c'est pour moi"
   - "je me sens comprise"
   - "je peux leur faire confiance"
   - "cela peut m'aider concretement"
   - "cela vaut une seance payante"

Livrable attendu:

Partie A - Diagnostic brutal mais precis
- points forts reels
- points faibles reels
- zones floues
- risques de mauvaise comprehension
- risque de sous-conversion

Partie B - Positionnement recommande
- ce que IVIA devrait promettre en une phrase
- ce que IVIA ne doit surtout pas promettre
- la bonne definition du service du point de vue du client
- le bon angle de desirabilite

Partie C - Evaluation marketing
- clarté
- desirabilite
- credibilite
- chaleur humaine
- differenciation
- capacite de conversion
Donne une note sur 10 pour chaque critere avec justification courte.

Partie D - Recommandations de discours
- proposition de headline principale
- proposition de sous-headline
- proposition de promesse centrale
- proposition de paragraphe de page d'accueil
- proposition de bloc "pour qui"
- proposition de bloc "ce que vous en retirez"
- proposition de formulation du cadre prudent sans casser le desir

Partie E - Verification theorique et sectorielle
- compare le discours a ce qui fonctionne habituellement dans:
  - relation d'aide non medicale
  - accompagnement humain
  - soutien psychologique non reserve
  - services premium de clarification ou d'accompagnement
- dis si le discours s'aligne davantage sur une logique:
  - d'orientation
  - de soutien
  - de soulagement
  - de clarification
  - de transformation
- dis quel mix serait le plus juste pour convertir sans trahir la realite du service

Contraintes importantes:
- ne propose pas un discours pseudo-clinique
- ne propose pas un discours de spiritualite floue
- ne propose pas un discours startup froid
- ne dilue pas la singularite d'IVIA
- garde une haute exigence de clarte commerciale
- si tu vois un risque de promesse illegitime, signale-le explicitement

Style de reponse attendu:
- franc
- structure
- critique
- sans complaisance
- oriente conversion reelle et coherence de marque
```

---

## 3) Prompt court si tu veux un retour plus rapide

```text
Analyse ces documents comme si tu etais un expert en positionnement de marque, conversion web et services d'accompagnement humain.

Question centrale:
Le discours actuel d'IVIA donne-t-il vraiment envie a une personne en difficulte, mais non en urgence, de payer une seance ?

Je veux une reponse structuree en 5 parties:
1. Ce que le service semble vendre reellement
2. Ce qui est fort
3. Ce qui est faible ou flou
4. Ce qui empeche la conversion
5. La version de promesse de marque que tu recommanderais

Sois direct. Ne menage pas le projet. Je veux savoir si le discours actuel est assez fort pour convertir ou non.
```

---

## 4) Ce qu'il faut demander explicitement a Perplexity

Tu peux ajouter a la fin:

```text
Si tu devais resumer le probleme principal en une phrase:
"IVIA echoue ou reussit a convertir parce que..."

Puis donne-moi:
- la meilleure promesse possible
- la plus grosse erreur actuelle
- le mot ou l'idee a mettre au centre
```

---

## 5) Ce que nous cherchons a verifier

Le vrai sujet n'est pas seulement:
- "est-ce joli ?"
- "est-ce noble ?"

Le vrai sujet est:
- est-ce qu'une personne comprend ce que IVIA peut lui apporter ?
- est-ce qu'elle percoit un benefice concret ?
- est-ce qu'elle sent une valeur assez claire pour payer une seance ?
- est-ce que la prudence juridique affaiblit trop la desirabilite ?
- est-ce que le discours est assez distinctif pour exister face a d'autres offres d'ecoute, de soutien ou d'accompagnement ?

---

## 6) Usage recommande

Faire d'abord une passe Perplexity sur:
- la clarte du discours;
- la desirabilite commerciale;
- les comparables de marche;
- les codes de confiance du secteur.

Ensuite seulement:
- reprendre la landing page IVIA;
- reprendre la page rendez-vous;
- figer la promesse centrale;
- affiner le style editorial.

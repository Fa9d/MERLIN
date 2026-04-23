# MERLIN - Decision audio dans l'application V1

Date: 2026-04-21
Statut: decision active
Objet: fixer le mode de communication audio cible pour MERLIN et pour l'offre praticiens

---

## 1) Decision nette

MERLIN retient comme ligne principale:

`l'audio se fait dans l'application`

Cela vaut:
- pour les operateurs MERLIN;
- pour les praticiens utilisant la plateforme;
- pour les futures seances client / praticien supportees par le systeme.

Le telephone classique ou les outils externes ne sont pas la ligne produit cible.

Ils peuvent exister:
- comme secours transitoire;
- comme solution exceptionnelle;
- ou comme fallback operationnel;

mais pas comme socle principal du produit.

---

## 2) Pourquoi cette decision

Cette decision est retenue pour 6 raisons:

1. elle unifie l'experience operateur et praticien;
2. elle permet un enregistrement natif de la seance;
3. elle permet une transcription proprement rattachee a la seance;
4. elle facilite l'audit, les consentements et la gouvernance des traces;
5. elle evite de dependre de multiples outils externes peu maitrisables;
6. elle prepare une vraie couche temps reel coherente avec MERLIN.

En clair:

`si l'audio vit hors de l'app, la memoire et la gouvernance vivent hors du produit`

ce qui est contraire a la logique MERLIN.

---

## 3) Consequence produit

Le cycle cible devient:

1. creation de seance;
2. demarrage de seance;
3. connexion audio dans l'application;
4. enregistrement audio gouverne;
5. cloture de seance;
6. transcription;
7. derivees et note structuree;
8. historique.

Cela veut dire que le coeur de seance MERLIN doit etre pense comme:

`une seance audio native, pas comme un simple formulaire autour d'un appel externe`

---

## 4) Consequence technique

La brique cible est:

- audio temps reel dans l'app via WebRTC;
- orchestration de salle / participants;
- enregistrement cote serveur;
- stockage objet pour les fichiers source;
- transcription asynchrone apres seance.

La recommandation technique de travail devient:

- `LiveKit` ou equivalent pour la couche media temps reel;
- MERLIN garde la source de verite metier;
- le backend MERLIN rattache toute capture audio a un `session_id`;
- l'audio n'est jamais une ressource orpheline.

---

## 5) Regle d'usage

Le poste principal de travail reste:

- ordinateur;
- casque avec micro de bonne qualite;
- environnement calme.

Le mobile reste possible dans l'app, mais il est considere:

- comme extension;
- comme mode de secours;
- ou comme usage secondaire.

Il ne doit pas devenir le standard de qualite pour le MVP.

---

## 6) Perimetre V1

Pour V1, la cible n'est pas encore:

- visio complexe multi-participants;
- routage telephonique SIP complet;
- bascule telephone reseau classique;
- suppression parfaite de bruit en cuisine ou en deplacement.

La cible V1 est plus sobre:

- une seance audio 1 a 1 dans l'application;
- un demarrage propre;
- un enregistrement fiable;
- un rattachement propre a la seance;
- une transcription batch apres cloture.

---

## 7) Ordre d'implementation

L'ordre retenu apres cette decision est:

1. cycle metier `scheduled -> in_progress -> completed`;
2. rattachement audio natif a `session`;
3. capture / enregistrement audio;
4. stockage objet;
5. transcription batch;
6. derivees et documents.

Donc:

`on ne branche pas la transcription avant d'avoir branche la capture audio de seance`

et

`on ne branche pas la capture audio avant d'avoir une seance demarrable dans l'app`

---

## 8) Decision active

MERLIN adopte officiellement la ligne suivante:

- audio natif dans l'application pour operateurs;
- audio natif dans l'application pour praticiens;
- telephone et outils externes seulement en fallback transitoire.

References:
- [MERLIN_GOUV_PLAN_EXECUTION_OPTIMAL_PROJET_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_PLAN_EXECUTION_OPTIMAL_PROJET_V1.md)
- [MERLIN_GOUV_CHOIX_STACK_TECHNIQUE_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_CHOIX_STACK_TECHNIQUE_V1.md)

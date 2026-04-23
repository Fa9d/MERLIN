# MERLIN - Architecture marque et plateformes V1

Date: 2026-04-20
Statut: draft
Objet: definir s'il faut separer la plateforme client et la plateforme praticien, comment articuler IVIA et MERLIN, et sous quels noms de domaine lancer l'offre

---

## 1) Decision courte

Oui, il est adapte d'avoir:
- une interface client publique;
- une interface praticien separee et non exposee publiquement;
- mais un seul socle produit et documentaire.

Autrement dit:

`deux portes d'entree`

mais

`une seule machine MERLIN derriere`

---

## 2) Pourquoi separer

La separation est utile pour trois raisons.

### A. Le client n'achete pas la meme chose que le praticien

Le client cherche:
- une ecoute;
- une clarification;
- une orientation;
- une continuite.

Le praticien cherche:
- un outil;
- une trace;
- une synthese;
- une memoire;
- une infrastructure de pratique.

Si tout est melange sur un seul site, MERLIN risque:
- de paraitre confus;
- de ne convaincre ni l'un ni l'autre;
- de mal nommer ce qu'il vend.

### B. Les parcours sont differents

Le client doit comprendre vite:
- ce que c'est;
- si c'est pour lui;
- comment commencer;
- quelles sont les limites.

Le praticien doit comprendre:
- les forfaits;
- les fonctions;
- les modules;
- la logique de volume;
- l'onboarding.

### C. Le discours public n'est pas le meme

Cote client:
- empathie;
- clarification;
- prochaine etape;
- securite;
- continuite.

Cote praticien:
- gain de temps;
- qualite de trace;
- synthese;
- cadre;
- memoire;
- reporting.

---

## 3) Recommandation d'architecture

Je recommande:

### Plateforme 1 - Client

Role:
- entree publique;
- ecoute;
- clarification;
- prise de rendez-vous;
- journal ou synthese remise;
- parcours d'accompagnement.

### Plateforme 2 - Praticien

Role:
- choix de forfait;
- onboarding;
- gestion des seances;
- transcription;
- resumes;
- historique;
- offres MERLIN Pro.

Mode d'acces recommande:
- non visible dans la navigation publique principale;
- accessible sur invitation, lien direct ou offre d'acces;
- reservee aux praticiens qualifies ou aux leads deja engages.

### Couche commune invisible

Role:
- comptes;
- consentements;
- documents derives;
- historique;
- gouvernance;
- referentiels;
- facturation.

Conclusion:

`deux experiences visibles`

`une infrastructure commune`

---

## 4) Nom de domaine recommande

Je vous deconseille:
- `ivia.quebec/MERLIN`

Pourquoi:
- cela melange produit, marque et navigation;
- cela rend MERLIN secondaire alors que c'est votre moteur de valeur;
- cela est moins propre qu'une architecture par sous-domaines.

Je recommande plutot:

### Option A - Marque ombrelle IVIA

- `ivia.quebec` = site client
- `pro.ivia.quebec` = site praticien
- `app.ivia.quebec` = application authentifiee

Usage:
- IVIA devient la facade publique;
- MERLIN devient le moteur, la methode ou la couche interne.

### Option B - Marque publique MERLIN

- `merlin.ivia.quebec` = offre client
- `pro.ivia.quebec` ou `merlinpro.ivia.quebec` = praticiens

Usage:
- plus direct si vous voulez pousser MERLIN comme nom principal.

### Ma recommandation

Si vous tenez a IVIA et a MERLIN en meme temps:

- `ivia.quebec` pour le public client
- `pro.ivia.quebec` pour les praticiens, sans exposition publique directe
- MERLIN comme nom de la methode, de l'intelligence documentaire et de la couche d'analyse

Formule:

`IVIA est la porte d'entree`

`MERLIN est le moteur de lecture, de continuite et de structuration`

---

## 5) Position sur les noms

### IVIA

Forces:
- plus abstrait;
- plus institutionnel;
- plus adaptable a plusieurs offres.

Faiblesses:
- peu explicite au premier contact;
- demande plus de travail de pedagogie.

### MERLIN

Forces:
- plus memorable;
- plus incarn e;
- plus distinctif.

Faiblesses:
- peut sembler plus conceptuel ou plus proprietaire;
- peut paraitre moins neutre si mal cadre.

### Recommandation de marque

Pour le public:
- garder `IVIA` comme contenant

Pour la valeur methodologique:
- garder `MERLIN` comme systeme de lecture, de synthese et de continuite

Exemples:
- `IVIA, propulse par MERLIN`
- `L'ecoute IVIA, avec la continuite MERLIN`
- `MERLIN Pro pour les praticiens`

---

## 6) Position sur le slogan

### `La puissance du silence`

C'est fort, mais il faut bien le placer.

Usage recommande:
- signature de marque;
- phrase de campagne;
- accroche emotionnelle secondaire.

Usage deconseille:
- promesse principale unique de la page d'accueil.

Pourquoi:
- c'est beau, mais trop poetique seul;
- cela ne dit pas assez clairement ce que vous faites;
- cela ne parle ni de clarification, ni de suite, ni de continuite.

### `IN VIVO IN ACTU`

C'est fort comme signature de doctrine.

Sens retenu:

`Au sein de l'etre - En acte`

Usage recommande:
- signature conceptuelle;
- page "notre approche";
- page marque / methode;
- footer, manifeste, a propos.

Usage deconseille:
- headline principal au-dessus du pli pour le grand public.

Pourquoi:
- cela demande interpretation;
- ce n'est pas immediatement comprehensible;
- cela fonctionne mieux comme profondeur de marque que comme message de conversion.

---

## 7) Recommandation de messaging

### Page client - `ivia.quebec`

Headline recommande:

`Un espace d'ecoute pour clarifier ce que vous vivez et repartir avec une suite concrete.`

Sous-ligne possible:

`La puissance du silence, quand elle devient ecoute, clarification et prochaine etape.`

Place de `IN VIVO IN ACTU`:
- en page approche;
- ou en signature.

### Page praticien - `pro.ivia.quebec`

Headline recommande:

`Transformez chaque seance en trace utile, en synthese claire et en continuite exploitable.`

Sous-ligne possible:

`MERLIN Pro outille votre pratique avec transcription, resumes, memoire et lecture longitudinale prudente.`

---

## 8) Structure de navigation recommandee

### `ivia.quebec`

- Accueil
- Comment ca fonctionne
- Nos services
- Limites et urgence
- Notre approche
- Prendre rendez-vous
- Espace client

Regle:
- ne pas afficher `Pour les praticiens` dans la navigation publique standard;
- si une page praticien publique existe, elle doit etre tres sobre et orientee prise de contact, pas acces direct plateforme.

### `pro.ivia.quebec`

- Accueil praticiens
- Offres et forfaits
- Fonctions
- MERLIN Pro
- Securite et consentements
- Onboarding
- Connexion

Regle:
- acces par URL directe, invitation ou relance commerciale;
- pas d'indexation recherche recommande e en phase initiale;
- authentification ou page d'acces restreint des l'entree si necessaire.

---

## 9) Funnel recommande

### Funnel client

Chemin:
- arrivee sur `ivia.quebec`
- comprehension de l'offre
- prise de rendez-vous ou contact

Objectif:
- ne capter que des personnes en recherche d'ecoute, de clarification ou de continuite.

### Funnel praticien

Chemin:
- contact via le site client ou via demarchage direct
- qualification manuelle ou semi-manuelle
- envoi d'une offre d'acces
- redirection vers `pro.ivia.quebec`
- choix du forfait et onboarding

Objectif:
- transformer le portail praticien en espace commercialement filtre;
- savoir qu'un praticien qui demande acces est deja interesse;
- eviter l'effet "catalogue public" trop tot.

### Consequence strategique

Le site client devient aussi un capteur de leads praticiens.

Mais il faut distinguer clairement dans les formulaires:
- `je cherche un espace d'ecoute`
- `je suis praticien et je veux decouvrir l'offre`

---

## 10) Ce qu'il faut eviter

- un site unique qui melange client vulnerable et praticien acheteur;
- `La puissance du silence` comme seule promesse compréhensible;
- `IN VIVO IN ACTU` comme premier message commercial;
- faire de MERLIN un nom fantome cache dans une URL;
- faire de IVIA une facade vide sans valeur expliquee.
- une plateforme praticien totalement ouverte si vous voulez garder un effet de qualification et de desirabilite.

---

## 11) Recommandation finale

La meilleure architecture de depart me semble etre:

- `ivia.quebec` = plateforme d'ecoute client
- `pro.ivia.quebec` = plateforme praticiens non exposee publiquement
- `MERLIN` = moteur, methode et couche d'intelligence documentaire

Slogan de campagne possible:

`La puissance du silence`

Promesse operative a garder au premier plan:

`ecoute, clarification, orientation, continuite`

Signature conceptuelle possible:

`IN VIVO IN ACTU`

---

## 12) Decision active

MERLIN retient a ce stade:

- deux portes d'entree distinctes;
- une base produit commune;
- IVIA comme facade publique possible;
- MERLIN comme nom de methode, de moteur et d'offre praticien;
- un portail praticien non visible du grand public et active par offre d'acces.

Prochaine etape recommandee:
- rediger la version site client;
- rediger la version site praticien;
- puis figer la nomenclature de domaines et sous-domaines.

References:
- [MERLIN_GOUV_POSITIONNEMENT_PUBLIC_SITE_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_POSITIONNEMENT_PUBLIC_SITE_V1.md)
- [MERLIN_GOUV_DOCTRINE_APPUIS_THEORIQUES_MERLIN_v1.0.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_DOCTRINE_APPUIS_THEORIQUES_MERLIN_v1.0.md)
- [MERLIN_GOUV_OFFRE_PRATICIENS_GRILLE_COMMERCIALE_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_OFFRE_PRATICIENS_GRILLE_COMMERCIALE_V1.md)

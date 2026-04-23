# MERLIN - Cadre operatoire de traitement des donnees IVIA / MERLIN V1

Date: 2026-04-21
Statut: draft
Objet: definir le cadre operatoire de traitement des donnees pour IVIA / MERLIN, avant la spec data, l'application et la couche IA

---

## 1) Finalite

Ce document ne remplace pas:
- les mentions legales;
- la politique de confidentialite publique;
- les contrats avec fournisseurs;
- les documents de consentement.

Il sert a definir, en interne:
- quelles donnees existent;
- pourquoi elles existent;
- qui peut les utiliser;
- sous quelles conditions;
- combien de temps elles vivent;
- ce que l'IA peut en faire;
- ce qui est interdit;
- ce que l'application devra imposer.

Doctrine:

`aucune donnee sensible ne doit etre capturee, derivee, conservee, exposee ou transmise sans finalite explicite, base operatoire claire et trace exploitable`

---

## 2) Perimetre V1

Ce cadre vaut d'abord pour le noyau V1 retenu:
- adulte;
- demande non urgente;
- entree client IVIA;
- seance MERLIN standard;
- note structuree;
- historique court;
- orientation simple;
- transcription optionnelle gouvernee;
- documents derives utiles.

Ce cadre s'applique aussi a la future couche praticiens seulement dans la mesure ou elle consomme les memes objets et les memes regles.

---

## 3) Logique generale de traitement

IVIA / MERLIN traite les donnees selon 4 niveaux.

### Niveau 1 - Donnees d'entree

Exemples:
- formulaire d'entree;
- identite minimale;
- disponibilites;
- demandes initiales;
- consentements.

But:
- accueillir;
- qualifier;
- cadrer;
- creer la fiche minimale.

### Niveau 2 - Donnees de seance

Exemples:
- meta de seance;
- note structuree;
- enregistrement si applicable;
- transcription si applicable;
- orientation proposee;
- statut de validation humaine.

But:
- produire une trace utile;
- permettre la continuite;
- documenter la relation.

### Niveau 3 - Donnees derivees

Exemples:
- besoins dominants;
- drapeaux rouges;
- facteurs de blocage;
- themes recurrents;
- resume de seance;
- synthese d'evolution.

But:
- structurer;
- comparer;
- restituer;
- soutenir l'orientation.

### Niveau 4 - Donnees d'exploitation

Exemples:
- audit;
- logs techniques;
- roles et acces;
- evenements de traitement;
- version de referentiel;
- journal de generation documentaire.

But:
- prouver;
- superviser;
- corriger;
- gouverner.

---

## 4) Finalites autorisees

Les finalites V1 autorisees sont les suivantes.

### F-01 - Creation et gestion d'une demande

Permet:
- d'enregistrer une demande;
- de la qualifier;
- de la relier a une personne ou un contexte;
- de preparer une prise en charge minimale.

### F-02 - Conduite de la seance MERLIN

Permet:
- de realiser une seance;
- d'en garder la trace operatoire;
- de ne pas recommencer a zero;
- de cadrer la suite.

### F-03 - Continuite de parcours

Permet:
- d'alimenter l'historique;
- de comparer les seances;
- de suivre l'evolution;
- de produire une memoire utile.

### F-04 - Production de documents derives

Permet:
- resume de seance;
- journal de parcours;
- synthese d'evolution;
- note de transmission;
- releves operatoires.

### F-05 - Orientation prudente

Permet:
- de documenter une orientation;
- d'expliquer pourquoi elle est suggeree;
- de garder trace du niveau de confiance;
- de relier l'orientation aux limites du cadre MERLIN.

### F-06 - Qualite, supervision et audit interne

Permet:
- de verifier la qualite;
- de revoir certaines suggestions IA;
- de tracer qui a fait quoi;
- de corriger les erreurs de traitement.

### F-07 - Exploitation technique et securite

Permet:
- d'heberger;
- de journaliser;
- de sauvegarder;
- de monitorer;
- de restaurer;
- de traiter les incidents.

---

## 5) Finalites interdites ou non ouvertes en V1

Sont interdites ou hors perimetre V1:
- diagnostic clinique automatise;
- notation opaque de sante mentale;
- profilage commercial agressif;
- revente de donnees;
- publicite fondee sur la parole recueillie;
- usage du verbatim comme matiere marketing;
- transmission a un tiers non explicitement justifiee;
- inférence automatique spirituelle ou transgenerationnelle comme verite operatoire;
- entrainement libre de modeles externes sur les donnees sans cadre specifique ferme.

Doctrine:

`ce qui augmente la valeur commerciale mais degrade la legitimite du cadre de confiance est interdit`

---

## 6) Categories de donnees

## A. Donnees d'identification minimale

Exemples:
- prenom ou identifiant d'usage;
- nom si necessaire;
- courriel;
- telephone;
- fuseau / territoire;
- langue.

Regle:
- minimum necessaire seulement.

## B. Donnees de contexte d'entree

Exemples:
- pour soi / proche / autre;
- besoin principal;
- perception du niveau d'urgence;
- suivi deja en place ou non;
- attentes de la personne.

Regle:
- privilegier choix guides et champs courts.

## C. Donnees de consentement

Exemples:
- consentement seance;
- consentement note;
- consentement historique;
- consentement enregistrement;
- consentement transcription;
- consentement remise client;
- consentement transmission tiers.

Regle:
- chaque consentement doit etre date, versionne et traçable.

## D. Donnees de seance

Exemples:
- date;
- duree;
- canal;
- operateur;
- statut;
- note;
- orientation;
- validations.

## E. Donnees sensibles source

Exemples:
- audio brut;
- transcription integrale;
- citations longues;
- details personnels sensibles.

Regle:
- acces restreint;
- retention plus courte ou fortement justifiee;
- pas de circulation par defaut.

## F. Donnees derivees

Exemples:
- resume;
- themes;
- besoins dominants;
- facteurs de vigilance;
- comparaison inter-seances;
- documents remis.

Regle:
- distinguer fait, derive, hypothese, suggestion.

## G. Donnees techniques

Exemples:
- logs applicatifs;
- evenements d'API;
- echec de job;
- temps de traitement;
- version du referentiel.

---

## 7) Principe de minimisation

Pour toute nouvelle donnee, IVIA / MERLIN doit pouvoir repondre a 4 questions:

1. pourquoi la capture-t-on;
2. qui en a besoin;
3. combien de temps doit-elle vivre;
4. peut-on atteindre le meme but avec moins de donnees.

Regles:
- ne pas demander au premier contact ce qui n'est utile qu'en phase ulterieure;
- ne pas conserver la source brute quand l'objet derive suffit;
- ne pas ouvrir l'audio ou le verbatim a plus de personnes que necessaire;
- ne pas transformer une recherche ou une intuition doctrinale en champ obligatoire.

---

## 8) Regimes de consentement

Ce cadre reprend la logique modulaire deja retenue.

### Consentements structurels

Sans eux, le service V1 ne peut pas fonctionner normalement:
- seance;
- note structuree;
- historique court minimal si continuite revendiquee.

### Consentements optionnels sensibles

Ils ne sont jamais presumes:
- enregistrement;
- transcription;
- remise de transcription;
- transmission a un tiers.

### Regle de revocation

Une revocation doit distinguer:
- futur interdit;
- futur limite;
- trace passee deja produite;
- objet deja transmis.

L'application devra donc separer:
- `revoked_for_future_use`
- `already_processed`
- `already_shared`

---

## 9) Regles de retention

Les durees exactes pourront etre affinees plus tard.
Mais les regimes V1 doivent deja etre clairs.

### R-01 - Audio brut

Doctrine:
- retention la plus courte possible;
- suppression rapide apres transcription verifiee ou cloture du besoin technique;
- pas de conservation longue par inertie.

### R-02 - Transcription integrale source

Doctrine:
- retention plus longue que l'audio si regime consenti;
- acces tres limite;
- revue periodique;
- pas de conservation indefinie sans justification.

### R-03 - Note de seance et historique court

Doctrine:
- couche principale de continuite;
- retention plus stable;
- versionnage et audit.

### R-04 - Documents derives remis

Doctrine:
- conservation de la version remise;
- trace de remise;
- statut explicite.

### R-05 - Logs techniques et audit

Doctrine:
- retention suffisante pour securite, supervision et preuve;
- pas de contenu sensible inutile dans les logs.

---

## 10) Regles d'acces

Les acces doivent etre fondes sur le besoin d'en connaitre.

### Operateur seance

Peut acceder a:
- fiche client utile;
- note;
- historique necessaire;
- orientation;
- documents derives.

N'accede pas par defaut a:
- audio brut ancien;
- toutes les transcriptions sources;
- informations hors besoin operatoire.

### Supervision qualite

Peut acceder selon cadre:
- echantillons necessaires;
- audit des sorties IA;
- evenements critiques.

### Admin technique

Peut acceder a:
- infrastructure;
- metadonnees;
- journaux techniques;
- supports necessaires a la maintenance.

N'accede pas par defaut au contenu sensible lisible si une solution technique permet de l'eviter.

### Client

Peut acceder selon droits et format prevu a:
- documents derives remis;
- certains releves;
- certaines informations de compte;
- pas necessairement a toute source brute par defaut.

---

## 11) Regles pour la couche IA

L'IA n'a pas un droit general sur les donnees.
Elle agit dans des traitements bornes.

### L'IA peut

- transcrire si consentement adapte;
- resumer;
- extraire des faits derives;
- suggerer une lecture prudente;
- comparer avec l'historique;
- preparer un document derive;
- signaler des drapeaux rouges textuels.

### L'IA doit toujours distinguer

- citation ou fait rapporte;
- derive ou synthese;
- hypothese;
- suggestion;
- validation humaine ou non.

### L'IA ne peut pas en V1

- poser un diagnostic;
- attribuer une cause profonde certaine;
- deduire une lecture spirituelle ou transgenerationnelle operatoire;
- agir seule sur une transmission critique;
- presenter une orientation comme medicalement certaine.

### Regles de journalisation IA

Pour chaque sortie IA importante, l'application devra pouvoir tracer:
- entree source utilisee;
- version du prompt ou de la regle;
- modele utilise;
- date et heure;
- statut de validation humaine;
- document final remis ou non.

---

## 12) Transmission a des tiers

Une transmission a un tiers n'est autorisee que si les 4 conditions sont reunies:

1. finalite claire;
2. consentement explicite adapte ou base imperative documentee;
3. objet transmis proportionne;
4. trace de transmission exploitable.

Par defaut, ce qui se transmet est:
- une synthese;
- une note de relais;
- un resume de demarches;
- des points de vigilance;
- pas la source brute integrale sauf cas justifie.

L'application devra stocker au minimum:
- destinataire;
- finalite;
- base de transmission;
- objet transmis;
- date;
- auteur;
- statut.

---

## 13) Contraintes d'hebergement et d'exploitation

Le cadre technique devra respecter au minimum:
- secrets separes par environnement;
- chiffrement transport;
- politique de sauvegarde;
- restauration testable;
- journal des incidents;
- stockage objet separe pour fichiers sensibles;
- principe du moindre privilege;
- environnement dev ne contenant pas de vraies donnees sensibles en libre circulation.

Regle forte:

`la commodite de developpement ne justifie jamais la circulation libre de donnees sensibles`

---

## 14) Traduction applicative obligatoire

Le futur systeme devra rendre ce cadre executable.

Exigences V1:
- identifiants stables pour consentements, statuts, niveaux de risque et orientations;
- champ `retention_class`;
- champ `data_sensitivity_class`;
- champ `human_validation_status`;
- champ `referential_version`;
- champ `source_type`;
- champ `transmission_status`;
- champ `shared_with_third_party`;
- audit des acces critiques.

Sans ces champs, le cadre ne sera qu'une declaration.

---

## 15) Incidents et anomalies

Doivent etre traites comme incidents:
- acces inapproprie;
- mauvaise transmission;
- conservation non conforme;
- generation d'un document interdit;
- sortie IA trompeuse non corrigee;
- log technique contenant du contenu sensible inutile.

Minimum de traitement:
- detection;
- qualification;
- mesure immediate;
- correction;
- trace;
- revue preventive.

---

## 16) Regles de decision pour ajouter une nouvelle donnee ou un nouveau traitement

Toute nouvelle idee doit etre testee contre cette grille:

1. finalite explicite;
2. categorie de donnee;
3. sensibilite;
4. base de consentement ou autre base operatoire;
5. retention;
6. acces;
7. sortie autorisee;
8. impact BDD / API / UI;
9. impact IA;
10. risque de surcaptation.

Si une de ces cases n'est pas claire:
- l'idee ne va pas en production;
- elle reste en recherche ou en backlog.

---

## 17) Ce que ce cadre corrige dans notre trajectoire

Il corrige 5 faiblesses actuelles:
- flou sur ce qui est reellement collecte;
- flou sur ce que l'IA peut produire;
- flou sur la retention;
- flou sur la transmission;
- flou sur la traduction produit / BDD.

Autrement dit:

`ce document ferme la Phase 1 sur le versant donnees`

et ouvre correctement:
- la spec donnees V1;
- la spec ecrans V1;
- la construction BDD / API;
- la pipeline IA gouvernee.

---

## 18) Decision active

IVIA / MERLIN adopte les principes suivants:

- minimisation par defaut;
- consentement modulaire;
- source brute gouvernee;
- objets derives privilegies;
- IA bornee et auditable;
- transmission proportionnee;
- retention explicite;
- acces par besoin d'en connaitre;
- traduction obligatoire en champs, statuts, versions et audits applicatifs.

Prochaine etape recommandee:
- rediger la `spec donnees V1` a partir de ce cadre.

References:
- [MERLIN_GOUV_POLICY_CONSENTEMENTS_SEANCES_DONNEES_v1.0.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_POLICY_CONSENTEMENTS_SEANCES_DONNEES_v1.0.md)
- [MERLIN_GOUV_POLICY_TRANSCRIPTION_GOUVERNEE_v1.0.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_POLICY_TRANSCRIPTION_GOUVERNEE_v1.0.md)
- [MERLIN_GOUV_POLICY_VERSIONNAGE_REFERENTIELS_BDD_APP_v1.0.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_POLICY_VERSIONNAGE_REFERENTIELS_BDD_APP_v1.0.md)
- [MERLIN_GOUV_CADRAGE_ANALYSE_IA_TEMPS_REEL_ORIENTATION_PRUDENTE_v1.0.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_CADRAGE_ANALYSE_IA_TEMPS_REEL_ORIENTATION_PRUDENTE_v1.0.md)
- [MERLIN_GOUV_PLAN_EXECUTION_OPTIMAL_PROJET_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_PLAN_EXECUTION_OPTIMAL_PROJET_V1.md)

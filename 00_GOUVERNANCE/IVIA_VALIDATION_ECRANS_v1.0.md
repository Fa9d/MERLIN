# VALIDATION DES ÉCRANS — registre canonique (v1.0, 2026-07-10)

> Réponse à la question fondateur : « chaque écran doit être revu, repensé et
> validé — par où commencer ? ». UN registre, UNE grille, UN ordre de passage.
> On coche ICI, jamais ailleurs. Un écran est validé quand les 8 critères
> passent sur téléphone ET sur grand écran.

## La grille — 8 critères identiques pour chaque écran

1. **Aucun défilement horizontal** (mobile 360 px et desktop) ;
2. **Cibles tactiles ≥ 44 px** (boutons, liens de navigation) ;
3. **Navigation au pouce** : barre mobile / retour accessibles sans effort ;
4. **On sait où l'on est** : titre + fil d'Ariane (ou équivalent) justes ;
5. **Action principale visible sans défiler** (au moins amorcée) ;
6. **Les 3 états existent** : vide (premier usage), chargement, erreur douce ;
7. **Thème cohérent** (couleurs/typo de la maison) ;
8. **Le chemin fonctionne de bout en bout** (les liens mènent où ils disent).

## Ordre de passage (par valeur, un bloc à la fois)

1. **Public** — la vitrine convertit (accueil → réserver → activer) ;
2. **Client sur téléphone** — l'usage quotidien réel (journal, reflets, enregistrements, agenda) ;
3. **Praticien sur desktop** — l'outil de travail (agenda, préparation, analyses) ;
4. **Admin** — un seul utilisateur : toi. En dernier.

## Méthode de session (30-45 min par bloc, jamais plus)

- David ouvre le parcours sur SON téléphone et avance écran par écran ;
- il dicte ce qui cloche en langage libre (« ce bouton est minuscule », « je suis perdu ici ») ;
- Claude corrige en lot, redéploie, et coche les colonnes ;
- un bloc à la fois — fini = coché = on n'y revient que sur régression.

## Public — PRIORITÉ 1

| Écran | Chemin | Mobile | Desktop | Fonctionnel | Notes |
|---|---|:---:|:---:|:---:|---|
| 404 · Page introuvable | `/404.html` | ☐ | ☐ | ☐ | |
| prototype header + journal (style getacuity) | `/_proto/index.html` | ☐ | ☐ | ☐ | |
| Registre des routes : valider / invalider / rediriger | `/_proto/registre-routes.html` | ☐ | ☐ | ☐ | |
| « Ton espace en trois temps » (animé) | `/_proto/section-trois-temps.html` | ☐ | ☐ | ☐ | |
| Mobile Screens Showcase (spec mss) | `/_proto/showcase.html` | ☐ | ☐ | ☐ | |
| Activation de votre espace | `/activer.html` | ☐ | ☐ | ☐ | |
| L'écoute qui n'attend pas | `/attente.html` | ☐ | ☐ | ☐ | |
| Conditions générales d'utilisation | `/cgu.html` | ☐ | ☐ | ☐ | |
| Politique de confidentialité | `/confidentialite.html` | ☐ | ☐ | ☐ | |
| Réservation confirmée | `/confirmation.html` | ☐ | ☐ | ☐ | |
| Se connecter | `/connexion.html` | ☐ | ☐ | ☐ | |
| Archive maquette interactive Client / Praticien (home V1) | `/design-system/apercu-interfaces-client-praticien.html` | ☐ | ☐ | ☐ | |
| Maquette : Accueil de l'espace (Signature / Doux) | `/design-system/espace-client-accueil.html` | ☐ | ☐ | ☐ | |
| Maquette : Déposer ma voix (Signature / Doux) | `/design-system/espace-client-deposer.html` | ☐ | ☐ | ☐ | |
| Maquette : Écrire (Signature / Doux) | `/design-system/espace-client-ecrire.html` | ☐ | ☐ | ☐ | |
| Maquette : Rencontrer un·e praticien·ne (Signature / Doux) | `/design-system/espace-client-rencontrer.html` | ☐ | ☐ | ☐ | |
| Maquette : Voir, ma carte de vie (Signature / Doux) | `/design-system/espace-client-voir.html` | ☐ | ☐ | ☐ | |
| Démonstration : l'espace vivant (Client / Praticien) | `/design-system/interface-miracle.html` | ☐ | ☐ | ☐ | |
| Maquette : parcours Première fois (Signature / Doux) | `/design-system/parcours-premiere-fois.html` | ☐ | ☐ | ☐ | |
| Démo : ProfileRadar statique (Signature / Doux) | `/design-system/profile-radar-demo.html` | ☐ | ☐ | ☐ | |
| RecorderCard (Signature / Doux) | `/design-system/recorder-card.html` | ☐ | ☐ | ☐ | |
| Pas une thérapie. Une écoute. | `/ecoute.html` | ☐ | ☐ | ☐ | |
| Employeurs et Loi 27 | `/employeurs.html` | ☐ | ☐ | ☐ | |
| Être écouté et avancer | `/index.html` | ☐ | ☐ | ☐ | |
| Créer mon espace | `/inscription.html` | ☐ | ☐ | ☐ | |
| Mentions légales | `/mentions.html` | ☐ | ☐ | ☐ | |
| Où en es-tu ? | `/ou-en-es-tu.html` | ☐ | ☐ | ☐ | |
| Pourquoi | `/pourquoi.html` | ☐ | ☐ | ☐ | |
| Pour un proche | `/proche.html` | ☐ | ☐ | ☐ | |
| Réserver une séance | `/rendez-vous.html` | ☐ | ☐ | ☐ | |
| Réserver une séance | `/reserver.html` | ☐ | ☐ | ☐ | |
| De la performance à la présence : vers une politique du soin  Ressources | `/ressources/de-la-performance-a-la-presence.html` | ☐ | ☐ | ☐ | |
| Suzuki : quand l&#x27;économie oublie qu&#x27;elle vit dans la nature  Ressources | `/ressources/economie-et-nature.html` | ☐ | ☐ | ☐ | |
| Qu&#x27;est-ce qu&#x27;une écoute qui respecte le vivant ?  Ressources | `/ressources/ecoute-qui-respecte-le-vivant.html` | ☐ | ☐ | ☐ | |
| Quand l&#x27;empathie devient instrument de pouvoir  Ressources | `/ressources/empathie-et-pouvoir.html` | ☐ | ☐ | ☐ | |
| Empathie éthique : ressentir sans se perdre  Ressources | `/ressources/empathie-ethique.html` | ☐ | ☐ | ☐ | |
| Pourquoi certains espaces collectifs nous épuisent  Ressources | `/ressources/espaces-collectifs-qui-epuisent.html` | ☐ | ☐ | ☐ | |
| Créer des espaces de parole vrais  Ressources | `/ressources/espaces-de-parole-vrais.html` | ☐ | ☐ | ☐ | |
| Fréquence et autonomie : habiter sa vie depuis l&#x27;intérieur  Ressources | `/ressources/frequence-et-autonomie.html` | ☐ | ☐ | ☐ | |
| Habiter son corps dans un monde qui le nie  Ressources | `/ressources/habiter-son-corps.html` | ☐ | ☐ | ☐ | |
| Ressources · Le labo du vivant | `/ressources/index.html` | ☐ | ☐ | ☐ | |
| Le cercle comme carte d&#x27;équilibre  Ressources | `/ressources/le-cercle-carte-d-equilibre.html` | ☐ | ☐ | ☐ | |
| Le corps comme premier instrument de présence  Ressources | `/ressources/le-corps-instrument-de-presence.html` | ☐ | ☐ | ☐ | |
| Plantes, minéraux, vivant : pistes sérieuses de régénération  Ressources | `/ressources/le-savoir-des-plantes.html` | ☐ | ☐ | ☐ | |
| Le vivant sait se régénérer  Ressources | `/ressources/le-vivant-sait.html` | ☐ | ☐ | ☐ | |
| Les lois de l&#x27;échange : pourquoi certains liens épuisent  Ressources | `/ressources/lois-de-l-echange.html` | ☐ | ☐ | ☐ | |
| Nous ne sommes pas des machines : penser sa vie en cycles  Ressources | `/ressources/penser-sa-vie-en-cycles.html` | ☐ | ☐ | ☐ | |
| Plusieurs regards sur ce que vous vivez  Ressources | `/ressources/plusieurs-regards.html` | ☐ | ☐ | ☐ | |
| La responsabilité comme acte de dignité  Ressources | `/ressources/responsabilite-et-dignite.html` | ☐ | ☐ | ☐ | |
| Tout vibre : ce que la physique montre vraiment  Ressources | `/ressources/tout-vibre.html` | ☐ | ☐ | ☐ | |
| Souffler, sans dossier | `/travail.html` | ☐ | ☐ | ☐ | |
| Confirmation du courriel | `/verify-email.html` | ☐ | ☐ | ☐ | |

## Client — PRIORITÉ 2

| Écran | Chemin | Mobile | Desktop | Fonctionnel | Notes |
|---|---|:---:|:---:|:---:|---|
| Réserver une séance | `/client/agenda.html` | ☐ | ☐ | ☐ | |
| Votre carte de vie | `/client/carte-de-vie.html` | ☐ | ☐ | ☐ | |
| Mon compte | `/client/compte.html` | ☐ | ☐ | ☐ | |
| Mon espace | `/client/dashboard.html` | ☐ | ☐ | ☐ | |
| Enregistrer ma voix | `/client/enregistrement.html` | ☐ | ☐ | ☐ | |
| Nouvelle entrée de journal | `/client/journal-nouvelle-entree.html` | ☐ | ☐ | ☐ | |
| Journal | `/client/journal.html` | ☐ | ☐ | ☐ | |
| Ma progression | `/client/ma-progression.html` | ☐ | ☐ | ☐ | |
| Mes enregistrements | `/client/mes-enregistrements.html` | ☐ | ☐ | ☐ | |
| Mes exercices | `/client/mes-exercices.html` | ☐ | ☐ | ☐ | |
| Mes repères | `/client/mes-reperes.html` | ☐ | ☐ | ☐ | |
| Mes résumés de séance | `/client/mes-resumes.html` | ☐ | ☐ | ☐ | |
| Mon profil | `/client/mon-profil.html` | ☐ | ☐ | ☐ | |
| Mon reflet | `/client/mon-reflet.html` | ☐ | ☐ | ☐ | |
| Mot de passe oublié | `/client/mot-de-passe-oublie.html` | ☐ | ☐ | ☐ | |
| Premier ancrage | `/client/premier-ancrage.html` | ☐ | ☐ | ☐ | |
| Séance en cours | `/client/seance-active.html` | ☐ | ☐ | ☐ | |
| Votre séance | `/client/seance-express-join.html` | ☐ | ☐ | ☐ | |
| Votre séance | `/client/seance.html` | ☐ | ☐ | ☐ | |
| Mes séances | `/client/seances.html` | ☐ | ☐ | ☐ | |

## Praticien — PRIORITÉ 3

| Écran | Chemin | Mobile | Desktop | Fonctionnel | Notes |
|---|---|:---:|:---:|:---:|---|
| praticien/agenda.html | `/praticien/agenda.html` | ☐ | ☐ | ☐ | |
| Carte de Vie (lecture praticien) | `/praticien/carte-de-vie.html` | ☐ | ☐ | ☐ | |
| praticien/clients-journal.html | `/praticien/clients-journal.html` | ☐ | ☐ | ☐ | |
| Compte-rendu de séance | `/praticien/compte-rendu-seance.html` | ☐ | ☐ | ☐ | |
| praticien/compte.html | `/praticien/compte.html` | ☐ | ☐ | ☐ | |
| Tableau de bord praticien | `/praticien/dashboard.html` | ☐ | ☐ | ☐ | |
| Profil praticien·ne | `/praticien/fiche.html` | ☐ | ☐ | ☐ | |
| Guide praticien·ne | `/praticien/guide.html` | ☐ | ☐ | ☐ | |
| Analyses de séances | `/praticien/livraisons.html` | ☐ | ☐ | ☐ | |
| Ma pratique | `/praticien/ma-pratique.html` | ☐ | ☐ | ☐ | |
| Préparer l'entretien | `/praticien/preparation.html` | ☐ | ☐ | ☐ | |
| praticien/profil.html | `/praticien/profil.html` | ☐ | ☐ | ☐ | |
| Créer une séance express | `/praticien/seance-express.html` | ☐ | ☐ | ☐ | |
| Pour les praticiens : reprenez votre présence | `/praticiens.html` | ☐ | ☐ | ☐ | |

## Admin — PRIORITÉ 4

| Écran | Chemin | Mobile | Desktop | Fonctionnel | Notes |
|---|---|:---:|:---:|:---:|---|
| Analyses &amp; droits  Admin | `/admin/analyses.html` | ☐ | ☐ | ☐ | |
| Comptabilité  Admin | `/admin/comptabilite.html` | ☐ | ☐ | ☐ | |
| Comptes  Admin | `/admin/comptes.html` | ☐ | ☐ | ☐ | |
| Administration   Connexion | `/admin/connexion.html` | ☐ | ☐ | ☐ | |
| Demandes d'entrée  Admin | `/admin/demandes.html` | ☐ | ☐ | ☐ | |
| Dossiers clients | `/admin/dossiers.html` | ☐ | ☐ | ☐ | |
| Économie IA  Admin | `/admin/economie.html` | ☐ | ☐ | ☐ | |
| Facturation  Admin | `/admin/facturation.html` | ☐ | ☐ | ☐ | |
| Administration | `/admin/index.html` | ☐ | ☐ | ☐ | |
| Atelier des lectures  Admin | `/admin/lectures.html` | ☐ | ☐ | ☐ | |
| Vue d'ensemble  Admin | `/admin/vue.html` | ☐ | ☐ | ☐ | |

## Transverse — au fil de l’eau

| Écran | Chemin | Mobile | Desktop | Fonctionnel | Notes |
|---|---|:---:|:---:|:---:|---|
| Paiement annulé | `/checkout/cancel.html` | ☐ | ☐ | ☐ | |
| Paiement (mode test) | `/checkout/paiement-test.html` | ☐ | ☐ | ☐ | |
| Paiement reçu | `/checkout/success.html` | ☐ | ☐ | ☐ | |

# IVIA - Runbook traitement prospects pilote

Date: 2026-05-11
Statut: actif pilote
Portee: demandes recues depuis `https://ivia.quebec/rendez-vous`

## Objectif

Transformer une demande publique en traitement operateur sans confondre prospect et client actif.

Regle centrale:

`Le prospect depose une demande. Il devient client actif quand un operateur qualifie la demande et planifie une premiere seance.`

## Verification immediate apres demande

1. Ouvrir `/operator` avec un compte `operator` ou `practitioner`.
2. Consulter la section `File prospects`.
3. Reperer la demande par code client, date, nom ou contact.
4. Verifier les champs minimums:
   - contact disponible: courriel ou telephone;
   - besoin principal;
   - niveau d'urgence affiche;
   - texte libre transmis;
   - consentements `E`, `T`, `S`, `N`; l'historique `H` peut rester optionnel.

Legende consentements:

- `E`: enregistrement
- `T`: transcription
- `S`: seance
- `N`: note de seance
- `H`: historique de suivi

## Qualification avant rappel

Classer mentalement la demande en un des etats operatoires suivants:

- `a_rappeler`: demande complete, non urgente, contact possible;
- `a_clarifier`: information insuffisante ou ambiguite sur le besoin;
- `vigilance`: signaux de detresse, incoherence, urgence possible ou besoin de redirection;
- `non_traitable`: mineur, urgence immediate, hors cadre, absence de contact utilisable.

En V1, ces etats ne sont pas encore persistants dans la base. Ils guident le geste operateur et la note interne.

## Action operateur V1

1. Cliquer `Traiter` dans la file prospects.
2. Relire la fiche selectionnee dans `Creer un creneau d'ecoute`.
3. Si besoin, utiliser `Analyser` dans le tableau clients pour detecter les signaux de risque ou de non-reponse.
4. Contacter la personne par le canal disponible.
5. Si le contact confirme la suite, choisir:
   - mode: `Premier RDV`;
   - canal: `Direct`, `Presentiel` ou `Asynchrone` selon le cas;
   - date/heure planifiee si connue;
   - duree estimee.
6. Cliquer `Creer et preparer la salle` si la seance audio doit etre prete tout de suite, sinon `Creer la seance`.

La seance creee depuis une demande selectionnee est rattachee a l'`intake_request_id`, ce qui permet de voir que le prospect a ete pris en charge.

## Cas de vigilance

Si la demande contient une detresse intense, une mention de danger immediat, d'ideation suicidaire, de violence ou d'incapacite a attendre:

1. Ne pas promettre une prise en charge IVIA comme solution d'urgence.
2. Reprendre le cadre public: IVIA n'est pas un service d'urgence.
3. Orienter vers 911 ou 988 selon le contexte.
4. Noter le signal dans la suite operateur.
5. Ne creer une seance IVIA que si la situation revient dans le cadre non urgent ou accompagne.

## Donnees a ne pas faire circuler hors outil

- transcription brute;
- audio;
- note interne non validee;
- hypothese sensible;
- donnees de contact dans des documents partageables.

## Validation pilote du 2026-05-11

Demande production verifiee:

- code client: `CLI-BB98B134F6`;
- intake: `ff78d6e9-5098-4b63-a944-df2128187db1`;
- canal: `web_form`;
- besoin: `distress`;
- urgence declaree: `non_urgent`;
- consentements publics: `E`, `T`, `S`, `N`, `H` accordes.

Aucune coordonnee personnelle n'est reproduite dans ce runbook.

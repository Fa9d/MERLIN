# MERLIN - Strategie experience prospect / client

Date : 2026-05-11  
Statut : reference produit immediate  
Portee : site IVIA, parcours rendez-vous, conversion, qualification, passage vers MERLIN  
Confidentialite : interne IVIA / MERLIN

## 1. Decision produit

IVIA doit distinguer clairement le prospect du client.

Une personne qui visite le site, lit l'offre ou remplit une premiere demande n'est pas encore client. Elle est prospect.

Une personne devient client seulement lorsqu'une etape de validation est franchie : inscription confirmee, demande acceptee, premiere seance planifiee ou engagement explicite selon le processus retenu.

Cette distinction doit orienter le langage, le design, les donnees, les permissions, les messages et les priorites de developpement.

## 2. Definitions

### Visiteur

Personne qui arrive sur le site sans avoir encore manifeste une intention claire.

Objectif du site : lui permettre de comprendre rapidement si IVIA peut l'aider.

### Prospect

Personne qui manifeste un interet ou remplit une premiere demande.

Objectif du site : la rassurer, qualifier sa demande, reduire la friction et l'amener vers une prochaine etape humaine ou structuree.

### Demande qualifiee

Demande recue avec informations minimales, consentements necessaires et absence de situation d'urgence immediate incompatible avec le cadre IVIA.

Objectif interne : permettre a IVIA de contacter, orienter, accepter, reporter ou refuser proprement.

### Client

Personne entree dans le parcours IVIA apres validation explicite.

Objectif de MERLIN : soutenir la seance, l'enregistrement, la transcription, la note, la validation humaine, le compte rendu et la continuite.

## 3. Principe central

L'experience prospect doit etre traitee avec autant de soin que l'experience client, car elle est la porte d'entree vers la conversion.

Le prospect ne doit pas rencontrer trop tot la complexite interne MERLIN : comptes, workflows, enregistrements techniques, notes, historiques, architecture agentique.

Le prospect doit d'abord rencontrer :

- une promesse claire ;
- une ambiance de confiance ;
- une explication sobre ;
- un premier pas simple ;
- des limites honnetes ;
- une suite concrete.

## 4. Probleme actuel observe

Le site contient deja plusieurs briques utiles : page d'accueil, page rendez-vous, formulaire, consentements, suivi client, routes API, audio, notes et documents derives.

Mais l'experience reelle melange encore plusieurs niveaux :

- vitrine publique ;
- demande prospect ;
- consentements sensibles ;
- logique client ;
- reservation technique ;
- compte utilisateur ;
- concepts internes MERLIN ;
- suivi apres seance.

Ce melange nuit a la conversion parce qu'il demande au prospect de comprendre trop de choses avant d'avoir confiance.

## 5. Parcours cible

```text
visiteur
  -> prospect interesse
    -> demande prospect
      -> demande qualifiee
        -> contact / validation IVIA
          -> client
            -> seance
              -> note / compte rendu / suivi
```

Le site public doit optimiser les trois premiers etats. MERLIN doit operer fortement a partir de la demande qualifiee et du statut client.

## 6. Experience prospect cible

### Objectif

Transformer une personne interessee ou hesitante en demande qualifiee, sans la forcer a creer un compte.

### Questions auxquelles le site doit repondre

- Suis-je au bon endroit ?
- Est-ce que je peux parler sans etre juge ?
- Est-ce que c'est une therapie ?
- Est-ce que c'est une urgence ?
- Qu'est-ce qui se passe apres ma demande ?
- Combien ca coute ?
- Est-ce que mes informations sont protegees ?
- Est-ce que je dois creer un compte maintenant ?

### Reponses attendues

- IVIA offre une premiere seance d'ecoute et de clarification.
- IVIA ne remplace pas les soins, ne pose pas de diagnostic et ne prescrit pas.
- IVIA ne traite pas les urgences immediates.
- Une demande peut etre faite sans compte.
- L'equipe reprend contact ou confirme la suite.
- Les donnees sont traitees avec prudence.
- Les consentements sont expliques progressivement.

## 7. Structure recommandee de `/rendez-vous`

La page `/rendez-vous` devient la page de conversion prospect.

Structure cible :

1. Accroche rassurante
   - "Vous n'avez pas besoin d'avoir les mots parfaits."
   - "Commencez par dire ce qui est la."

2. Pour qui
   - adultes ;
   - situation non urgente ;
   - besoin de clarté, d'ecoute, d'orientation ou de suite concrete.

3. Ce que la premiere seance permet
   - deposer ;
   - clarifier ;
   - nommer ;
   - repartir avec une prochaine etape.

4. Ce que ce n'est pas
   - pas un service d'urgence ;
   - pas un diagnostic ;
   - pas une prescription ;
   - pas un remplacement des soins.

5. Informations pratiques
   - duree ;
   - prix ;
   - format ;
   - delai de recontact ;
   - confidentialite.

6. Formulaire prospect
   - prenom ou alias ;
   - courriel ou telephone ;
   - adulte confirme ;
   - besoin principal ;
   - texte libre ;
   - soutien deja en place ;
   - urgence immediate oui/non.

7. Consentements progressifs
   - d'abord expliquer pourquoi ;
   - ensuite demander les cases requises ;
   - distinguer requis et optionnel ;
   - eviter l'avalanche administrative.

8. Confirmation
   - reference de demande ;
   - ce qui se passe maintenant ;
   - rappel urgence ;
   - delai de recontact ;
   - aucun compte obligatoire a cette etape.

## 8. Experience client cible

L'experience client commence apres validation.

Fonctions attendues :

- confirmation de seance ;
- rappel des consentements ;
- acces a l'audio ou aux consignes ;
- preparation de seance ;
- consultation des syntheses diffusees ;
- suivi des prochaines etapes ;
- historique si consenti ;
- possibilite de correction ou retrait selon politique.

Cette experience peut etre plus fonctionnelle, car la personne a deja franchi le seuil de confiance.

## 9. Implications techniques

### Court terme

- Garder `/rendez-vous` comme entree publique principale.
- Rediriger `/rendez-vous/reserver` vers `/rendez-vous` tant que la reservation autonome n'est pas coherente avec le parcours prospect.
- Ne pas forcer la creation de compte pour une demande prospect.
- Autoriser les consentements requis par le formulaire public.
- Renommer les libelles visibles : ne pas appeler client ce qui est encore prospect.

### Moyen terme

- Introduire un statut metier distinct : prospect / demande / client.
- Ajouter un cockpit de qualification pour l'equipe IVIA.
- Permettre la conversion d'une demande en client.
- Relier la demande a une seance.
- Relier la seance a l'audio, a la note et au compte rendu.

### Long terme

- Reservation autonome seulement si elle ne nuit pas a la conversion.
- Espace client complet seulement apres validation.
- Mesure des taux de conversion et d'abandon.

## 10. Priorites de developpement

### Priorite 1 - Conversion prospect

Objectif : une personne peut faire une demande sans friction et recevoir une confirmation rassurante.

Critere de sortie :

```text
/rendez-vous permet une demande complete sans compte, sans erreur 401, avec reference affichee.
```

### Priorite 2 - Qualification interne

Objectif : l'equipe IVIA peut traiter les demandes.

Fonctions :

- liste des demandes ;
- detail prospect ;
- consentements ;
- statut de traitement ;
- notes internes ;
- action : contacter, refuser, convertir, planifier.

### Priorite 3 - Conversion client

Objectif : transformer une demande qualifiee en client et seance.

Fonctions :

- creer client confirme ;
- creer seance ;
- assigner praticien / operateur ;
- envoyer consignes ;
- preparer audio ou alternative.

### Priorite 4 - Cycle seance

Objectif : conduire une seance testable.

Fonctions :

- demarrer seance ;
- enregistrer ou importer audio ;
- stopper enregistrement ;
- produire transcription ou trace ;
- fermer seance.

### Priorite 5 - Note et compte rendu

Objectif : produire une suite utile.

Fonctions :

- generer note structuree ;
- evaluer avec Telescope ;
- valider humainement ;
- produire compte rendu client ;
- publier dans suivi client.

## 11. Ce qu'il ne faut pas faire maintenant

- Ne pas imposer la creation de compte au prospect.
- Ne pas commencer par la reservation autonome si elle ajoute de la friction.
- Ne pas afficher trop tot les details internes MERLIN.
- Ne pas automatiser la livraison client avant validation humaine.
- Ne pas appeler client une personne qui n'a pas encore franchi l'etape de validation.
- Ne pas deplacer l'effort vers audio / IA / rapports tant que l'entree prospect n'est pas fiable.

## 12. Indicateurs de conversion

A suivre des que possible :

- visiteurs page rendez-vous ;
- taux de debut formulaire ;
- taux de formulaire soumis ;
- erreurs formulaire ;
- abandons aux consentements ;
- demandes qualifiees ;
- demandes refusees / hors cadre ;
- demandes converties en client ;
- delai de recontact ;
- taux de seance realisee ;
- satisfaction apres premiere seance.

## 13. Prochaine sequence recommandee

1. Commiter le correctif public `/rendez-vous` deja valide localement.
2. Revoir le contenu de `/rendez-vous` selon cette strategie.
3. Remplacer les mots visibles `client` par `prospect`, `demande` ou `reference` selon le contexte.
4. Ajouter un champ urgence immediate ou une porte de sortie claire.
5. Ajouter une confirmation plus rassurante apres soumission.
6. Creer le cockpit minimal de qualification interne.
7. Seulement ensuite raccorder seance, audio, note et compte rendu.

## 14. Formulation de reference

### Pour prospect

"Vous n'avez pas besoin de savoir exactement quoi demander. Dites-nous simplement ou vous en etes. Nous verifierons ensemble si IVIA est le bon espace pour vous, et quelle suite serait la plus juste."

### Pour client

"Votre seance est confirmee. MERLIN aide l'equipe IVIA a structurer la note et la continuite de votre suivi, avec validation humaine avant toute synthese diffusee."

## 15. Conclusion

La priorite n'est pas de montrer toute la puissance de MERLIN au premier contact. La priorite est de creer une porte d'entree claire, rassurante et digne de confiance.

Le prospect doit sentir :

```text
je peux commencer simplement
je comprends ce qui va se passer
je ne suis pas piege dans un systeme
je peux faire confiance
```

C'est seulement apres cette conversion que l'experience client, l'audio, l'analyse, les notes et les comptes rendus doivent prendre toute leur place.

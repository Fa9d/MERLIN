# Audit frontend parcours client / praticien

Date : 2026-05-13  
Objet : etat reel des pages critiques pour fermer le parcours client -> praticien -> session -> suivi.

## 1. Verdict rapide

Le frontend n'est pas vide. Plusieurs surfaces existent et certaines sont deja assez riches.

Etat actualise apres implementation v0.2 : le pont client minimal existe. Il couvre connexion, creation de compte par invitation, dashboard client authentifie, fiche `Client` liee et vraie page de reservation.

Le risque produit principal est donc passe de "trou produit" a "durcissement et E2E production" : migration PostgreSQL, donnees praticiens disponibles et validation reservation live.

## 2. Etat des routes critiques

### `/rendez-vous`

Etat : fonctionnel comme formulaire d'intake public.

Ce qui existe :

- creation client ;
- creation intake request ;
- consentements ;
- reference client ;
- reference intake ;
- lien vers `/suivi?code=...&intake=...` apres soumission.

Limite :

- la suite reste manuelle ;
- le message confirme que l'equipe recontacte, mais ne cree pas de compte ;
- pas de lien d'activation ;
- pas de reservation directe.

### `/rendez-vous/reserver`

Etat initial : redirection immediate vers `/rendez-vous`.

Etat apres implementation v0.1 du 2026-05-13 : vraie page de reservation.

Ce qui existe maintenant :

- liste des praticiens publics ;
- selection d'une plage de dates ;
- chargement des disponibilites ;
- selection d'un creneau ;
- hold materialise via `/api/v1/bookings/hold-calculated` si le slot est virtuel ;
- confirmation via `/api/v1/bookings/confirm`.

Limite : demande un compte client connecte et courriel verifie pour confirmer.

### `/espace-praticien`

Etat : vraie interface praticien, pas une coquille vide.

Ce qui existe :

- login praticien ;
- session stockee en localStorage ;
- chargement clients, consentements, intake requests, sessions, notes, salles audio, recordings, documents ;
- creation de seance ;
- provisioning audio ;
- demarrage seance ;
- note rapide ;
- validation de note ;
- cloture de session ;
- historique ;
- agenda hebdomadaire et exceptions.

Risques :

- tres grande page monolithique ;
- depend fortement de donnees backend disponibles ;
- a tester en vrai avec compte praticien seed ;
- pas encore confirme que les clients assignes / matching alimentent proprement cette interface.

### `/suivi`

Etat : page de suivi public par references.

Ce qui existe :

- formulaire reference client + reference intake ;
- lecture de documents diffuses via `listPublicDerivedDocuments` ;
- affichage de documents visibles client.

Limite :

- ce n'est pas un espace client authentifie ;
- experience fragile car depend de deux references manuelles ;
- utile comme pont provisoire, mais pas comme retention durable.

### `/ressources`

Etat : page editoriale statique.

Ce qui existe :

- categories ;
- articles codifies en dur ;
- filtre local ;
- CTA vers `/rendez-vous/reserver`.

Limite :

- le CTA pointe vers une route qui redirige vers `/rendez-vous` ;
- les articles semblent etre des cartes sans pages detaillees verifiees ici ;
- pas encore relie a MESANGE comme pipeline de contenu.

### `/audio-room`

Etat : composant audio LiveKit utilisable si lien complet.

Ce qui existe :

- lecture de `wsUrl`, `token`, `roomName`, `identity`, `role` en query params ;
- demande explicite d'autorisation micro ;
- connexion LiveKit ;
- publication micro ;
- lecture audio distant ;
- deconnexion.

Limite :

- depend d'un lien tokenise correctement provisionne ;
- UX encore tres technique ;
- ne suffit pas seul sans reservation/session/dashboard.

## 3. Routes client ajoutees le 2026-05-13

- `/connexion`
- `/creer-mon-compte`
- `/mon-espace`

Ces trois routes ferment le pont client minimal. Le vrai token d'invitation post-intake et le lien durable entre `AppUser(public_client)` et `Client` ont ete ajoutes en v0.2.

## 4. Cluster semantique Telescope

Cluster : rupture post-intake / activation client absente.

Symptome initial : le client pouvait soumettre une demande mais ne disposait pas d'un chemin clair pour creer son compte, reserver, voir son praticien ou revenir.

Etat v0.2 : le chemin de creation/activation compte est implemente et valide localement par test HTTP.

Reproduction E2E :

1. aller sur `/rendez-vous` ;
2. soumettre une demande valide ;
3. suivre le lien propose ;
4. constater que le suivi repose sur references et non sur compte ;
5. tenter de reserver via `/rendez-vous/reserver` ;
6. constater la redirection vers `/rendez-vous`.

Hypothese : la conversion et la retention chutent parce que le flow apres intake n'a pas de phase d'activation client.

Correction proposee :

1. `/creer-mon-compte?token=...` ;
2. `/connexion` ;
3. `/mon-espace` ;
4. email invitation apres assignation praticien ;
5. `/rendez-vous/reserver` relie au praticien ou a une session candidate.

## 5. Ordre recommande

### Etape 1 - Pont minimal sans casser l'existant

- garder `/suivi` comme fallback public temporaire ;
- creer `/connexion` ;
- creer `/mon-espace` minimal ;
- specifier `/creer-mon-compte?token=...` meme si backend token a finaliser.

### Etape 2 - Reservation

- remplacer la redirection de `/rendez-vous/reserver` par une vraie page ;
- accepter un contexte `practitionerId`, `sessionId` ou `inviteToken` ;
- afficher praticien, creneaux, prix, prochaine etape.

### Etape 3 - Espace praticien

- tester avec donnees seed ;
- verifier que l'assignation matching remonte dans la file praticien ;
- decouper plus tard la page monolithique en composants.

## 6. Definition de done pour le prochain chantier frontend

Un test manuel doit pouvoir faire :

```text
/rendez-vous
  -> soumission intake
  -> operator assigne praticien
  -> email ou lien d'invitation
  -> /creer-mon-compte
  -> /connexion
  -> /mon-espace
  -> reservation ou prochaine etape visible
```

Tant que ce test ne passe pas, les optimisations visuelles sont secondaires.
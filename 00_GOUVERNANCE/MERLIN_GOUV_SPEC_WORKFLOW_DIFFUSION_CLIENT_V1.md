# IVIA / MERLIN - Spec workflow diffusion client V1

Date: 2026-04-23
Statut: actif
Objet: formaliser le passage d'un contenu interne vers une sortie client gouvernee, utile et tracable

---

## 1) Role de cette spec

Cette spec complete:
- le tableau `donnees / consentements / diffusion client`
- la spec donnees V1
- le backlog `roles / acces / visibilite`

Elle ne redefinit pas ce qui est diffusable.

Elle fixe:
- quand une donnee reste interne;
- quand elle peut etre preparee pour le client;
- qui peut la valider;
- a quel moment elle est consideree comme remise.

---

## 2) Decision courte

MERLIN distingue des maintenant 4 etats logiques de diffusion:

1. `internal_only`
2. `prepared_for_client`
3. `validated_for_client`
4. `delivered_to_client`

Regle centrale:

`une donnee marquee visible n'est pas encore une donnee remise`

Et:

`la diffusion client est un acte documentaire, pas un effet de bord de l'interface`

---

## 3) Principe directeur

Le systeme doit separer 3 choses:

- la matiere interne de travail;
- la preparation d'une restitution;
- la remise effective au client.

En consequence:

- une note brute operateur reste interne par defaut;
- une synthese reformulee peut etre preparee pour diffusion;
- une validation humaine peut etre requise avant remise;
- la remise doit laisser une trace d'audit.

---

## 4) Objets concernes

Les objets V1 concernes en premier sont:

- `session_note`
- `document_derived`
- `orientation`
- certains fragments explicitement marques `client_visible`

Regle:

`audio_source` et `transcript_source` ne deviennent jamais des sorties client directes en V1.

---

## 5) Etats logiques de diffusion

| Etat logique | Sens | Visible client | Action typique |
|---|---|---|---|
| `internal_only` | contenu interne ou non prepare | non | travail, relecture, structuration |
| `prepared_for_client` | contenu reformule ou selectionne pour une restitution possible | non | preparation operateur |
| `validated_for_client` | contenu juge diffusable selon cadre et consentement | non ou pas encore remis | validation humaine finale |
| `delivered_to_client` | contenu effectivement remis ou rendu accessible au client | oui | publication, envoi ou mise a disposition |

Regle:

`delivered_to_client` implique une date, un canal et une trace.

---

## 6) Mapping V1 avec les champs existants

V1 peut fonctionner sans nouveau schema lourd, en combinant les champs deja poses.

| Etat logique | `client_visible` | `human_validation_status` | `delivered_to_client` |
|---|---|---|---|
| `internal_only` | `false` ou absent | `not_required` / `pending` | `false` |
| `prepared_for_client` | `true` | `pending` | `false` |
| `validated_for_client` | `true` | `validated` | `false` |
| `delivered_to_client` | `true` | `validated` | `true` |

Interpretation V1:

- `client_visible` signifie `eligibilite documentaire a la diffusion`, pas remise effective;
- `human_validation_status` porte la validation humaine;
- `delivered_to_client` ferme l'acte de remise.

Evolution recommandee apres V1:

- ajouter un champ explicite `client_delivery_status_code`;
- conserver la compatibilite avec les trois champs ci-dessus pendant la transition.

---

## 7) Regles par role

### `operator`

L'operateur peut:

- preparer une synthese ou une note reformulee;
- marquer une sortie comme candidate a la diffusion;
- corriger avant validation;
- remettre directement si le cadre V1 autorise une diffusion simple non sensible.

L'operateur ne peut pas:

- diffuser une note brute par commodite;
- rendre visible une transcription brute;
- assimiler preparation et validation quand une revue est requise.

### `supervisor`

Le superviseur peut:

- relire les contenus sensibles;
- valider ou rejeter une sortie preparee;
- demander reformulation;
- arbitrer les cas limites.

### `public_client`

Le client peut:

- voir uniquement ce qui est deja `delivered_to_client`;
- ne jamais voir les etats intermediaires de preparation interne.

### `admin_tech`

L'admin technique peut:

- maintenir le mecanisme de livraison;
- voir les metadonnees de diffusion et l'integrite des traces;
- ne pas lire librement le contenu sensible sans mandat distinct.

---

## 8) Conditions obligatoires avant validation

Avant de faire passer un contenu a `validated_for_client`, verifier:

1. `le contenu est-il utile a la personne ?`
2. `est-il comprehensible sans lecture experte ?`
3. `respecte-t-il le perimetre non medical et les limites du service ?`
4. `le consentement applicable couvre-t-il cette remise ?`
5. `le texte evite-t-il l'alarme, la fixation ou la surinterpretation ?`
6. `s'agit-il d'une reformulation et non d'un deversement de matiere interne ?`

Si une reponse est negative:

- le contenu reste `internal_only`;
- ou revient a `prepared_for_client` pour reprise.

---

## 9) Cas qui exigent une validation supervision

Une validation `supervisor` est recommandee ou requise si la sortie contient:

- un niveau de vigilance formule;
- une orientation sensible;
- un resume inter-seances potentiellement structurant;
- une formulation pouvant etre interpretee comme quasi-clinique;
- un cas litigieux, reclamation ou risque documentaire.

Une diffusion simple peut rester operateur en V1 si la sortie est:

- un resume post-seance bref;
- une prochaine etape concrete;
- un rappel logistique;
- une note deja standardisee et explicitement prevue pour le client.

---

## 10) Modes de remise autorises V1

Modes autorises:

- affichage dans un espace client authentifie minimal;
- remise directe en fin de seance via support gouverne;
- envoi controle d'un document derive si le cadre le permet.

Chaque remise doit idealement tracer:

- `delivered_at`
- `delivered_by_user_id` ou acteur systeme
- `delivery_channel_code`
- `source_object_type`
- `source_object_id`

Si tous ces champs n'existent pas encore partout, la logique d'audit doit au minimum permettre de les reconstruire.

---

## 11) Interdits actifs V1

Interdits:

- diffuser une transcription brute au client comme restitution standard;
- rendre une note interne visible juste parce qu'un champ de front l'affiche;
- confondre validation humaine et publication automatique;
- permettre a un role technique de contourner la chaine de diffusion;
- remplacer une reformulation par un copier-coller de matiere operatoire.

---

## 12) Implications produit et data

Implications immediates:

- l'interface operateur doit distinguer `interne`, `pret client`, `valide`, `remis`;
- la supervision doit voir ce qui attend validation;
- l'espace client ne doit lire que les contenus deja remis;
- l'audit doit permettre de savoir qui a prepare, valide et remis.

Implications schema recommandees:

- conserver `client_visible` en V1 court;
- s'appuyer sur `human_validation_status` pour la validation;
- utiliser `document_derived.delivered_to_client` et `delivered_at` pour la remise;
- introduire ensuite `client_delivery_status_code` pour simplifier les requetes et l'UX.

---

## 13) Decision active

A compter de cette note:

- `client_visible` n'est plus interprete comme une remise client;
- la diffusion client suit un workflow logique distinct;
- la validation humaine devient un verrou explicite des sorties sensibles;
- la remise client doit etre tracable comme evenement documentaire.

---

## 14) References

- [MERLIN_GOUV_TABLEAU_DONNEES_CONSENTEMENTS_DIFFUSION_CLIENT_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_TABLEAU_DONNEES_CONSENTEMENTS_DIFFUSION_CLIENT_V1.md)
- [MERLIN_GOUV_TABLEAU_ROLES_ACCES_VISIBILITE_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_TABLEAU_ROLES_ACCES_VISIBILITE_V1.md)
- [MERLIN_GOUV_BACKLOG_IMPLEMENTATION_ROLES_ACCES_VISIBILITE_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_BACKLOG_IMPLEMENTATION_ROLES_ACCES_VISIBILITE_V1.md)
- [MERLIN_GOUV_SPEC_DONNEES_V1_IVIA_MERLIN.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_SPEC_DONNEES_V1_IVIA_MERLIN.md)
- [MERLIN_GOUV_SPEC_ECRANS_V1_PARCOURS_CLIENT_IVIA_MERLIN.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_SPEC_ECRANS_V1_PARCOURS_CLIENT_IVIA_MERLIN.md)

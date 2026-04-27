# MERLIN - Checklist validation audio prod V1

Date: 2026-04-27
Statut: actif
Objet: fournir une recette unique, courte et rejouable pour valider la chaine audio de production sur le flux canonique frontend `audio-sessions` / `audio-recordings`

---

## 1) Portee

Cette checklist valide en production:

- l'authentification operateur sur le flux audio canonique;
- la creation d'un client et d'une seance de test propres;
- la preparation d'une session audio;
- l'emission des contextes de jonction `operator` et `client`;
- une connexion navigateur reelle a la salle LiveKit via `/audio-test`;
- le cycle `start recording -> stop recording`;
- l'ecriture en base des statuts audio et du `failure_reason` si echec;
- le nettoyage des objets de test crees.

Cette checklist ne remplace pas:

- la recette e2e documentaire `public -> operator -> supervisor -> public`;
- un audit fin de qualite reseau micro / casque;
- une supervision applicative automatisee.

Regle:

`utiliser cette recette pour l'audio, pas une suite de commandes shell improvisees`

---

## 2) Chemin canonique retenu

Pour cette validation, le chemin cible est:

- `POST /api/v1/audio-sessions/sessions/{session_id}/provision`
- `POST /api/v1/audio-sessions/{audio_session_id}/operator-join`
- `POST /api/v1/audio-sessions/{audio_session_id}/client-join`
- `POST /api/v1/audio-recordings/audio-sessions/{audio_session_id}/start`
- `POST /api/v1/audio-recordings/{audio_recording_id}/stop`

Le vieux chemin `/sessions/{id}/room` et `/sessions/{id}/recording/*` reste utile pour le diagnostic backend, mais ce n'est pas le flux principal consomme par le frontend `operator`.

---

## 3) Preconditions

Necessaire:

- acces SSH au VPS `ubuntu@137.74.42.121`;
- cle SSH locale fonctionnelle;
- compte operateur de test actif;
- possibilite de definir un mot de passe temporaire pour ce compte depuis le VPS;
- un navigateur local avec micro fonctionnel pour ouvrir les URLs de test generees.

Reference secrets:

- [MERLIN_GOUV_RUNBOOK_COMPTES_SECRETS_ACCES_TEST_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_RUNBOOK_COMPTES_SECRETS_ACCES_TEST_V1.md)

Script canonique:

- [merlin_prod_audio_validation.sh](C:/MERLIN/deploy/checks/merlin_prod_audio_validation.sh)

---

## 4) Execution canonique

Depuis PowerShell local:

```powershell
scp -i C:\Users\PC\.ssh\id_ed25519 C:\MERLIN\deploy\checks\merlin_prod_audio_validation.sh ubuntu@137.74.42.121:/home/ubuntu/
```

```powershell
ssh -i C:\Users\PC\.ssh\id_ed25519 ubuntu@137.74.42.121
```

Depuis le VPS:

```bash
chmod +x /home/ubuntu/merlin_prod_audio_validation.sh
```

```bash
/home/ubuntu/merlin_prod_audio_validation.sh
```

Le script:

- demande un mot de passe temporaire operateur;
- reinitialise le hash du compte operateur cible directement depuis le conteneur API;
- cree un client public, une intake et une seance de test;
- demarre la seance;
- prepare la salle audio;
- affiche deux URLs `audio-test` a ouvrir dans deux navigateurs;
- attend la connexion reelle des deux participants;
- lance puis arrete l'enregistrement;
- affiche l'etat BDD audio;
- propose le nettoyage immediat des objets de test.

---

## 5) Resultat attendu

Succes minimal:

- les deux pages `audio-test` rejoignent la meme salle;
- `audio_recording_status_code` passe par `recording` puis `ready`;
- `failure_reason` reste vide;
- `output_location` est renseigne;
- si `output_location` pointe vers un chemin local, le fichier existe dans le conteneur `merlin-api-1`.

Si echec:

- conserver la sortie du script;
- noter explicitement la valeur de `failure_reason`;
- distinguer:
  - echec de config `MERLIN_MEDIA_*` ou `LIVEKIT_*`;
  - echec de jonction navigateur / micro;
  - echec d'egress ou d'ecriture de fichier.

---

## 6) Interpretation

Si cette checklist passe:

- le risque audio n'est plus un flou general;
- le control-plane backend, le join navigateur et le cycle d'enregistrement sont verifies ensemble sur le flux reel du frontend.

Si cette checklist echoue:

- l'audio reste un perimetre borne et secondaire pour le pilote;
- l'incident doit etre traite a partir de la sortie du script canonique, pas d'essais ad hoc disperses.

---

## 7) References

- [MERLIN_GOUV_DECISION_GO_NO_GO_PILOTE_FERME_2026-04-26_v1.0.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_DECISION_GO_NO_GO_PILOTE_FERME_2026-04-26_v1.0.md)
- [MERLIN_GOUV_PLANNING_OPERATIONNEL_10_JOURS_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_PLANNING_OPERATIONNEL_10_JOURS_V1.md)
- [MERLIN_GOUV_CHECKLIST_RECETTE_PROD_E2E_J8_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_CHECKLIST_RECETTE_PROD_E2E_J8_V1.md)
- [MERLIN_GOUV_PROCEDURE_REDEPLOIEMENT_STANDARD_VPS_BACKEND_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_PROCEDURE_REDEPLOIEMENT_STANDARD_VPS_BACKEND_V1.md)

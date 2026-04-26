# MERLIN - Log incident VPS / recuperation acces / redeploiement backend 2026-04-24 v1.0

Date: 2026-04-24
Statut: valide
Objet: consigner la recuperation de l'acces admin VPS, le diagnostic de derive entre code local et backend prod, et le redeploiement correctif

---

## 1) Contexte

Le VPS `137.74.42.121` etait de nouveau joignable le 2026-04-24:

- ports `22`, `80` et `443` ouverts;
- `https://api.ivia.quebec/api/health` repondait `ok`;
- mais l'acces SSH admin n'etait plus recupere localement.

Le depot local montrait aussi une divergence potentielle entre le code backend courant et le backend effectivement deployee sur `/opt/merlin`.

---

## 2) Symptome initial

Constats verifies:

- la prod repondait en HTTP/HTTPS;
- l'API renvoyait bien `status = ok`;
- le SSH ne time-outait plus mais refusait les couples utilisateur / cle testes;
- le VPS avait deja la stack `db + api + livekit + nginx` active;
- la route publique `GET /api/v1/derived-documents/public/client/{public_client_code}` renvoyait `404 Not Found` au niveau route.

---

## 3) Recuperation acces admin

Actions effectuees:

1. passage temporaire du VPS en mode `rescue` via OVH;
2. montage du disque systeme sur `/mnt/vps` depuis le rescue;
3. verification de `sshd_config`;
4. injection de la cle publique `pc-merlin-ovh` dans:
   - `/root/.ssh/authorized_keys`
   - `/home/ubuntu/.ssh/authorized_keys`
5. sortie du mode `rescue` et redemarrage normal;
6. reconnexion reussie sur le systeme normal avec:
   - user `ubuntu`
   - cle `C:\Users\PC\.ssh\id_ed25519`

Resultat:

- acces admin VPS restaure;
- `ubuntu` ajoute au groupe `docker`;
- exploitation Docker ensuite possible sans `sudo`.

Commande d'acces validee:

```powershell
ssh -i C:\Users\PC\.ssh\id_ed25519 ubuntu@137.74.42.121
```

---

## 4) Diagnostic backend prod

Verification sur le VPS:

- `/opt/merlin` n'etait pas un clone git;
- le backend deploye ne contenait pas:
  - `app/api/routes/derived_documents.py`
  - `app/models/derived_document.py`
  - `app/schemas/derived_document.py`
- `app/main.py` n'importait pas `derived_documents_router`;
- la table PostgreSQL `derived_documents` n'existait pas.

Conclusion:

`la prod tournait correctement en infra, mais avec un backend plus ancien que le code local`

---

## 5) Correctif applique

Correctifs locaux:

- ajout de la migration Alembic `20260424_0010_add_derived_documents.py`.

Correctifs sur le VPS:

1. sauvegarde du backend deploye;
2. copie du backend local a jour vers `/opt/merlin/10_backend_merlin_api`;
3. rebuild de l'image `merlin-api`;
4. execution de:

```bash
docker compose --env-file .env.prod -f docker-compose.prod.yml run --rm api alembic upgrade head
```

5. redemarrage du service `api`.

---

## 6) Etat final verifie

Etat technique:

- `docker ps` ok sans `sudo` pour `ubuntu`;
- `merlin-api`, `merlin-db`, `merlin-livekit`, `merlin-nginx` actifs;
- `merlin-api` et `merlin-db` en `healthy`;
- timer `merlin-certbot-renew.timer` actif.

Etat API:

- `GET /api/health` repond `ok`;
- `GET /api/v1/auth/me` sans token repond `401` proprement;
- `openapi.json` expose maintenant `derived-documents`;
- `GET /api/v1/derived-documents/public/client/TEST-CODE` ne renvoie plus un `404` de route,
  mais un `404` metier:

```json
{"detail":"Reference client introuvable."}
```

Etat BDD:

- la table `derived_documents` existe bien apres migration.

---

## 7) Decision operative

A compter de cette sequence:

- l'acces admin standard au VPS se fait via `ubuntu` + cle SSH, pas via mot de passe root;
- toute mise a jour backend prod doit verifier explicitement:
  - les fichiers deployes;
  - la revision schema;
  - la presence de la route dans `openapi.json`;
- un changement applicatif qui ajoute un nouvel objet persistant ne doit plus partir en prod sans migration Alembic explicite.

---

## 8) Restes a faire

- faire un vrai test de flux metier `session -> session_note -> derived_document`;
- documenter la procedure de redeploiement standard VPS;
- reduire le risque de derive entre code local et `/opt/merlin` en adoptant une methode de sync plus stricte.

---

## 9) Addendum 2026-04-25

Un correctif supplementaire a ete prepare localement puis redeploye le 2026-04-25 pour ameliorer le rendu du document client derive:

- ajout d'une normalisation defensive des fragments textuels;
- suppression des doubles ponctuations dans `body_text`;
- normalisation du titre vers `Synthese de seance {n}`.

Redeploiement:

1. creation d'une archive de deploiement legere depuis `C:\MERLIN\10_backend_merlin_api`, sans `.venv`, caches ni fichiers `.db`;
2. copie de l'archive vers `/home/ubuntu`;
3. extraction dans `/home/ubuntu/10_backend_merlin_api`;
4. remplacement de `/opt/merlin/10_backend_merlin_api`;
5. rebuild de `merlin-api`.

Incident rencontre:

- le redemarrage du conteneur `merlin-api-1` a echoue avec:

```text
runtime "io.containerd.runc.v2" binary not installed "containerd-shim-runc-v2": file does not exist
```

- la pile Docker du VPS etait donc temporairement incoherente au niveau runtime;
- une reinstallation via paquets Ubuntu (`containerd`, `docker.io`, `runc`) a permis de redemarrer `merlin-api-1`;
- cette reinstallation a toutefois laisse le systeme paquets dans un etat non complet, avec echecs de configuration sur `dnsmasq-base` et `ubuntu-fan`.

Etat verifie apres reprise:

- `merlin-api-1` redemarre;
- `GET /api/health` repond `ok`;
- le conteneur charge bien:
  - `_ensure_terminal_punctuation`
  - `_build_generated_document_title`
  - `Synthese de seance`
- un nouveau test prod genere un document derive avec:
  - titre corrige;
  - ponctuation corrigee;
  - pipeline Anthropic toujours fonctionnel.

Point restant ouvert:

- assainir l'etat du runtime et du systeme paquets du VPS avant tout autre chantier infra.

---

## 10) Complement 2026-04-26 - Procedure canonique documentee

La procedure canonique de redeploiement backend standard VPS a ete formalisee a part pour eviter que le mode operatoire reste disperse entre incident log, checklist et historique shell.

Portee:

- archive legere locale;
- copie VPS;
- backup du code deploye;
- rebuild `api`;
- `alembic upgrade head`;
- restart `api`;
- verification health, schema et changement charge.

Reference canonique:

- [MERLIN_GOUV_PROCEDURE_REDEPLOIEMENT_STANDARD_VPS_BACKEND_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_PROCEDURE_REDEPLOIEMENT_STANDARD_VPS_BACKEND_V1.md)

Le point ouvert runtime reste distinct:

- cette documentation ne vaut pas preuve d'assainissement complet de `docker/containerd/runc`;
- la checklist `J1` reste la reference pour verifier le runtime du VPS.

---

## 11) References

- [MERLIN_GOUV_REGISTRE_DECISIONS_REVISIONS_IVIA_MERLIN_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_REGISTRE_DECISIONS_REVISIONS_IVIA_MERLIN_V1.md)
- [deploy-ovh.md](C:/MERLIN/docs/deploy-ovh.md)
- [20260424_0010_add_derived_documents.py](C:/MERLIN/10_backend_merlin_api/alembic/versions/20260424_0010_add_derived_documents.py)
- [MERLIN_GOUV_PROCEDURE_REDEPLOIEMENT_STANDARD_VPS_BACKEND_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_PROCEDURE_REDEPLOIEMENT_STANDARD_VPS_BACKEND_V1.md)

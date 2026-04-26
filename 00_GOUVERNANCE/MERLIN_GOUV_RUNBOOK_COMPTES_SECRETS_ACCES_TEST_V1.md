# MERLIN - Runbook comptes / secrets / acces test V1

Date: 2026-04-26
Statut: actif
Objet: fixer les regles operatoires pour les comptes internes, les secrets, l'acces VPS et les comptes de test utilises pour la recette et le pilote ferme

---

## 1) Principe

Ce document est un runbook de procedure.

Il ne doit jamais contenir:

- mots de passe en clair;
- clefs privees SSH;
- tokens JWT;
- secrets applicatifs `.env`;
- captures d'ecran montrant des valeurs secretes.

Il peut contenir:

- emails ou identifiants publics de comptes de test;
- roles associes;
- procedure de reset;
- emplacement du coffre de secrets hors repo;
- regles d'usage et de rotation.

Regle forte:

`le repo documente la methode, pas les valeurs secretes`

---

## 2) Perimetre couvert

Ce runbook couvre:

- acces admin VPS MERLIN;
- comptes internes de test `operator` et `supervisor`;
- regeneration et usage temporaire des tokens de test;
- discipline de stockage et rotation des secrets;
- gestes minimaux apres recette ou incident.

Ce runbook ne remplace pas:

- la configuration applicative `.env.prod`;
- le coffre de secrets prive hors repo;
- les logs d'incident ou de redeploiement;
- le log de nettoyage des objets de test prod.

---

## 3) Inventaire operatoire minimal

### A. Acces VPS

Acces standard retenu:

- hote: `137.74.42.121`
- utilisateur: `ubuntu`
- methode: cle SSH locale autorisee

Commande canonique:

```powershell
ssh -i C:\Users\PC\.ssh\id_ed25519 ubuntu@137.74.42.121
```

Interdits:

- connexion admin reguliere via `root`;
- mot de passe root partage;
- copie de cle privee dans le repo;
- stockage de la passphrase SSH dans un fichier `.md`.

### B. Comptes de test applicatifs actuellement utilises

Comptes verifies pour la recette prod:

- `davidphaneuf+test-merlin-operator-2-20260426@gmail.com`
- `davidphaneuf+test-merlin-supervisor-20260426@gmail.com`

Regle:

- le compte `operator` sert a creer et cloturer la seance;
- le compte `supervisor` sert a relire et valider;
- ne pas reutiliser un compte `supervisor` comme compte de production courante.

### C. Secrets concernes

Les valeurs secretes a maintenir hors repo sont:

- passphrase de la cle SSH locale;
- mots de passe des comptes de test;
- secrets applicatifs de `.env.prod`;
- secrets JWT, LiveKit, SMTP ou equivalents.

---

## 4) Stockage hors repo

Les valeurs secretes doivent etre conservees dans un support prive dedie, distinct du repo Git.

Formats acceptables:

- gestionnaire de mots de passe prive avec historique;
- coffre chiffre equipe restreinte;
- support hors ligne protege, si la discipline de mise a jour est reelle.

Formats a eviter:

- fichier `.md` dans le repo;
- note locale non chiffree;
- message de chat persistant avec secret en clair;
- historique shell contenant des mots de passe en dur.

Minimum attendu dans le coffre prive:

- nom du compte;
- email de login;
- role;
- date de creation ou dernier reset;
- date de derniere rotation;
- personne responsable;
- raison du dernier changement.

Gabarit recommande hors repo:

| Element | Valeur reelle | Dernier reset | Responsable | Emplacement | Notes |
|---|---|---|---|---|---|
| `ssh ubuntu@137.74.42.121` | hors repo | a renseigner | a renseigner | coffre prive | acces admin VPS |
| `operator test 2` | hors repo | a renseigner | a renseigner | coffre prive | recette prod |
| `supervisor test` | hors repo | a renseigner | a renseigner | coffre prive | validation supervision |

---

## 5) Regles d'usage

### A. Pendant une recette

- executer une commande par ligne;
- preferer `read -s` pour saisir un mot de passe sans echo;
- ne pas coller le prompt shell dans les commandes;
- ne pas sauvegarder un `access_token` dans un fichier;
- supprimer ou laisser expirer les variables d'environnement en fin de session.

Exemple de saisie correcte:

```bash
read -s OPERATOR2_PW; echo
```

```bash
read -s SUPERVISOR_PW; echo
```

### B. Frontiere des roles

- `operator` ne valide pas une note supervisee;
- `supervisor` ne sert pas aux gestes de production ordinaires si un compte `operator` existe;
- `admin_tech` gere l'infra et les incidents, pas la lecture libre des contenus sensibles.

### C. Donnees de test

- toute recette prod cree des objets fictifs distincts;
- les objets crees doivent etre traces dans le log de nettoyage;
- le nettoyage doit etre execute apres verification ou au plus tard avant ouverture pilote reelle.

---

## 6) Procedure standard si le login d'un compte de test echoue

Symptomes typiques:

- `401`
- `{"detail":"Identifiants invalides."}`
- `KeyError: 'access_token'` lors de l'extraction Python

Ordre de verification:

1. verifier que l'email est exact;
2. verifier que le compte existe encore et est `active`;
3. tester le login brut avec `curl -i` avant d'essayer d'extraire `access_token`;
4. si echec confirme, reinitialiser le mot de passe;
5. mettre a jour la valeur dans le coffre prive hors repo;
6. rejouer le login puis la recette.

Verification DB sur le VPS:

```bash
cd /opt/merlin
```

```bash
docker exec merlin-db-1 psql -U merlin -d merlin_v1 -c "select email, role, record_status from app_users where email in ('davidphaneuf+test-merlin-operator-2-20260426@gmail.com','davidphaneuf+test-merlin-supervisor-20260426@gmail.com') order by email;"
```

Test de login brut:

```bash
curl -s -i -X POST https://api.ivia.quebec/api/v1/auth/login -H 'Content-Type: application/json' -d '{"email":"davidphaneuf+test-merlin-operator-2-20260426@gmail.com","password":"<MOT_DE_PASSE_A_TESTER>"}'
```

---

## 7) Procedure de reset mot de passe

Condition:

- reserver ce reset aux comptes de test ou aux incidents controles;
- choisir une nouvelle valeur forte;
- l'enregistrer uniquement dans le coffre prive hors repo.

Reset `operator` depuis le conteneur API:

```bash
docker exec merlin-api-1 sh -lc "python -c \"from app.db.session import SessionLocal; from app.models.app_user import AppUser; from app.core.security import hash_password; db=SessionLocal(); u=db.query(AppUser).filter(AppUser.email=='davidphaneuf+test-merlin-operator-2-20260426@gmail.com').first(); assert u is not None, 'operator not found'; u.password_hash=hash_password('<NOUVEAU_MOT_DE_PASSE_OPERATOR>'); db.commit(); print(u.email); db.close()\""
```

Reset `supervisor` depuis le conteneur API:

```bash
docker exec merlin-api-1 sh -lc "python -c \"from app.db.session import SessionLocal; from app.models.app_user import AppUser; from app.core.security import hash_password; db=SessionLocal(); u=db.query(AppUser).filter(AppUser.email=='davidphaneuf+test-merlin-supervisor-20260426@gmail.com').first(); assert u is not None, 'supervisor not found'; u.password_hash=hash_password('<NOUVEAU_MOT_DE_PASSE_SUPERVISOR>'); db.commit(); print(u.email); db.close()\""
```

Verification immediate:

```bash
curl -s -i -X POST https://api.ivia.quebec/api/v1/auth/login -H 'Content-Type: application/json' -d '{"email":"davidphaneuf+test-merlin-operator-2-20260426@gmail.com","password":"<NOUVEAU_MOT_DE_PASSE_OPERATOR>"}'
```

```bash
curl -s -i -X POST https://api.ivia.quebec/api/v1/auth/login -H 'Content-Type: application/json' -d '{"email":"davidphaneuf+test-merlin-supervisor-20260426@gmail.com","password":"<NOUVEAU_MOT_DE_PASSE_SUPERVISOR>"}'
```

Si le login repond `200`:

- mettre a jour le coffre prive;
- noter date, auteur et motif du reset;
- reprendre la recette standard.

---

## 8) Generation temporaire des tokens de recette

Usage:

- ne generer les tokens que pour la session de test courante;
- ne pas les recopier dans un document;
- les laisser expirer ou fermer la session shell.

Exemple `operator`:

```bash
export OPERATOR2_TOKEN=$(curl -s -X POST https://api.ivia.quebec/api/v1/auth/login -H 'Content-Type: application/json' -d "{\"email\":\"davidphaneuf+test-merlin-operator-2-20260426@gmail.com\",\"password\":\"$OPERATOR2_PW\"}" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
```

Exemple `supervisor`:

```bash
export SUPERVISOR_TOKEN=$(curl -s -X POST https://api.ivia.quebec/api/v1/auth/login -H 'Content-Type: application/json' -d "{\"email\":\"davidphaneuf+test-merlin-supervisor-20260426@gmail.com\",\"password\":\"$SUPERVISOR_PW\"}" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
```

Nettoyage minimal de session:

```bash
unset OPERATOR2_PW
```

```bash
unset SUPERVISOR_PW
```

```bash
unset OPERATOR2_TOKEN
```

```bash
unset SUPERVISOR_TOKEN
```

---

## 9) Discipline de rotation

Rotation obligatoire:

- apres suspicion de fuite;
- apres copie accidentelle dans un chat, screenshot ou historique partage;
- apres demonstration publique ou semi-publique;
- apres changement de personne ayant acces;
- apres usage intensif de debug en prod.

Rotation recommandee:

- a chaque nouveau cycle majeur de recette prod;
- au minimum avant ouverture d'un pilote reel si les anciens mots de passe ont circule.

Si une valeur a ete exposee:

- la considerer comme compromise;
- la remplacer;
- mettre a jour le coffre prive;
- ne pas tenter de "faire confiance" a une valeur deja trop diffusee.

---

## 10) Journal minimal hors repo

Chaque evenement ci-dessous doit etre note dans le support prive:

- reset de mot de passe;
- changement de passphrase ou de cle SSH;
- suppression ou creation d'un compte de test;
- incident d'authentification repete;
- perte de controle sur une valeur secrete;
- execution d'un nettoyage prod apres recette.

Champs minimaux:

- date et heure;
- acteur;
- compte ou secret concerne;
- motif;
- action prise;
- verification post-action.

---

## 11) Liens operatoires

Documents a relire avant une recette prod:

- [MERLIN_GOUV_CHECKLIST_RECETTE_PROD_E2E_J8_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_CHECKLIST_RECETTE_PROD_E2E_J8_V1.md)
- [MERLIN_GOUV_LOG_TEST_PROD_TRACE_NETTOYAGE_2026-04-24_v1.0.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_LOG_TEST_PROD_TRACE_NETTOYAGE_2026-04-24_v1.0.md)
- [MERLIN_GOUV_LOG_INCIDENT_VPS_RECUPERATION_REDEPLOIEMENT_BACKEND_2026-04-24_v1.0.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_LOG_INCIDENT_VPS_RECUPERATION_REDEPLOIEMENT_BACKEND_2026-04-24_v1.0.md)
- [MERLIN_GOUV_TABLEAU_ROLES_ACCES_VISIBILITE_V1.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_TABLEAU_ROLES_ACCES_VISIBILITE_V1.md)
- [MERLIN_GOUV_DECISION_GO_NO_GO_PILOTE_FERME_2026-04-26_v1.0.md](C:/MERLIN/00_GOUVERNANCE/MERLIN_GOUV_DECISION_GO_NO_GO_PILOTE_FERME_2026-04-26_v1.0.md)

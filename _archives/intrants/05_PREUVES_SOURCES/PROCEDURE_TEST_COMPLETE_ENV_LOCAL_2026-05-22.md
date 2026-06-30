---
id: TEST-LOCAL-2026-05-22
type: procédure de test guidée
date: 2026-05-22
auteur: David Phaneuf
version: v2.0
---

# Procédure de test complète — IVIA/MERLIN local
## Guide pas à pas — 22 mai 2026

---

> **Comment lire ce document**
> Chaque étape indique exactement **où aller**, **quoi taper**, et **ce que tu dois voir**.
> Les blocs de code sont à copier-coller tels quels dans PowerShell.
> Une case à cocher confirme que l'étape est passée.

---

## ÉTAPE 0 — Vérifier que l'infrastructure tourne

### 0-A. Ouvrir un terminal PowerShell

1. Appuyer sur `Win + X` → choisir **Terminal Windows** (ou **PowerShell**)
2. Tu dois voir un prompt du type : `PS C:\>`

### 0-B. Vérifier Docker Desktop

```powershell
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

**Ce que tu dois voir :**

```
NAMES                   STATUS          PORTS
merlin-frontend-1       Up X minutes    0.0.0.0:3001->3000/tcp
merlin-backend-1        Up X minutes    0.0.0.0:8000->8000/tcp
merlin-postgres-1       Up X minutes    0.0.0.0:5432->5432/tcp
```

> **Si tu vois "Cannot connect to the Docker daemon"** → Docker Desktop n'est pas démarré.
> Ouvrir Docker Desktop depuis le bureau ou le menu Démarrer. Attendre que l'icône Docker dans la barre des tâches soit stable (pas animée), puis relancer la commande.

> **Si les conteneurs ne sont pas là** → aller dans le dossier MERLIN et les démarrer :
> ```powershell
> Set-Location C:\MERLIN
> docker compose up -d
> ```
> Attendre 15 secondes, puis relancer la vérification.

- [ ] `merlin-postgres-1` apparaît avec statut `Up`
- [ ] `merlin-backend-1` apparaît avec statut `Up`

### 0-C. Vérifier l'API backend

```powershell
Invoke-RestMethod -Uri 'http://localhost:8000/health'
```

**Ce que tu dois voir :**

```
status      : ok
service     : MERLIN API
environment : production
database    : ok
```

> **Note :** `environment: production` est normal — le conteneur Docker local est configuré en mode production. L'important est `database: ok`.

> **Si tu vois une erreur rouge** → le conteneur backend n'est pas prêt. Attendre 10 secondes et réessayer.

- [ ] `status : ok` et `database : ok`

### 0-D. Démarrer le serveur Next.js (frontend de développement)

Le frontend de développement tourne **en dehors de Docker**, directement sur ta machine.

1. Ouvrir un **deuxième terminal PowerShell** (garder le premier ouvert)
2. Taper :

```powershell
Set-Location C:\MERLIN\09_app_ivia_merlin
npm run dev
```

3. Attendre jusqu'à voir :

```
▲ Next.js 16.x
- Local: http://localhost:3000
✓ Ready in Xs
```

> **Ne pas fermer ce terminal** — le serveur doit rester actif pendant toute la procédure.

4. Dans le **premier terminal**, vérifier que le frontend répond :

```powershell
Invoke-WebRequest -Uri 'http://localhost:3000' -UseBasicParsing | Select-Object StatusCode
```

**Ce que tu dois voir :**

```
StatusCode
----------
       200
```

- [ ] StatusCode 200

---

## ÉTAPE 1 — Obtenir les tokens d'authentification

> On va récupérer les 3 tokens (admin, praticien, client) en une seule fois et les stocker dans des variables. Ces variables seront réutilisées dans toutes les étapes suivantes.

Dans le **premier terminal PowerShell**, copier-coller ce bloc entier :

```powershell
# --- TOKEN ADMIN ---
$adminToken = (Invoke-RestMethod `
    -Uri 'http://localhost:8000/api/v1/auth/login' `
    -Method POST `
    -Body (@{email='admin@ivia.quebec'; password='AdminIVIA2026!'} | ConvertTo-Json) `
    -ContentType 'application/json').access_token

# --- TOKEN PRATICIEN ---
$praticienToken = (Invoke-RestMethod `
    -Uri 'http://localhost:8000/api/v1/auth/login' `
    -Method POST `
    -Body (@{email='jean.beaumont@example.com'; password='TestIVIA2026!'} | ConvertTo-Json) `
    -ContentType 'application/json').access_token

# --- TOKEN CLIENT ---
$marieToken = (Invoke-RestMethod `
    -Uri 'http://localhost:8000/api/v1/auth/login' `
    -Method POST `
    -Body (@{email='marie.tremblay@example.com'; password='TestIVIA2026!'} | ConvertTo-Json) `
    -ContentType 'application/json').access_token

# --- VÉRIFICATION ---
Write-Host "Admin  : $(if ($adminToken) { 'OK' } else { 'ECHEC' })"
Write-Host "Jean   : $(if ($praticienToken) { 'OK' } else { 'ECHEC' })"
Write-Host "Marie  : $(if ($marieToken) { 'OK' } else { 'ECHEC' })"
```

**Ce que tu dois voir :**

```
Admin  : OK
Jean   : OK
Marie  : OK
```

> **Si tu vois ECHEC** → l'un des comptes n'existe pas. Relancer le script de seeding :
> ```powershell
> powershell -ExecutionPolicy Bypass -File "C:\MERLIN\04_METHODES\seed_full_v2.ps1"
> ```
> Puis relancer ce bloc.

- [ ] Les 3 tokens sont OK

> ⚠️ **Important** : Ces variables ($adminToken, $praticienToken, $marieToken) sont actives dans ce terminal uniquement. Si tu fermes le terminal ou ouvres un nouvel onglet, tu devras relancer ce bloc.

---

## ÉTAPE 2 — PARCOURS A : Visiteur public

> Aucune connexion requise. Ouvrir Firefox.

### 2-A. Ouvrir Firefox et tester les pages publiques

Ouvrir **Firefox** et naviguer vers chacune de ces adresses :

| Page | URL | Ce que tu dois voir |
|------|-----|---------------------|
| Accueil | `http://localhost:3000` | Page d'accueil IVIA, navigation |
| Praticiens | `http://localhost:3000/praticiens` | Liste des praticiens pilotes |
| Démarche | `http://localhost:3000/demarche` | Explication du service |
| Ressources | `http://localhost:3000/ressources` | Page ressources |
| Rendez-vous | `http://localhost:3000/rendez-vous` | Formulaire de prise de contact |

- [ ] Toutes les pages s'affichent sans écran blanc ni erreur

### 2-B. Tester le formulaire de prise de contact (depuis l'API)

Dans le terminal PowerShell :

```powershell
$intakeBody = @{
    client_first_name        = "Test"
    client_last_name         = "Visiteur"
    client_email             = "test.visiteur@example.com"
    client_phone             = "514 555 0099"
    request_channel_code     = "web_form"
    request_for_code         = "self"
    primary_need_code        = "support"
    perceived_urgency_code   = "non_urgent"
    support_already_in_place = $false
    referential_version      = "v1"
} | ConvertTo-Json

$newIntake = Invoke-RestMethod `
    -Uri 'http://localhost:8000/api/v1/intake-requests' `
    -Method POST `
    -Body $intakeBody `
    -ContentType 'application/json'

Write-Host "Intake créé : $($newIntake.id)"
```

**Ce que tu dois voir :**

```
Intake créé : xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

- [ ] Un ID est retourné

---

## ÉTAPE 3 — PARCOURS B : Client connecté → Espace client → Suivi

### 3-A. Se connecter comme Marie Tremblay dans Firefox

1. Dans Firefox, aller à : `http://localhost:3000/acces-client`
2. Saisir :
   - **Email** : `marie.tremblay@example.com`
   - **Mot de passe** : `TestIVIA2026!`
3. Cliquer sur **Se connecter**

**Ce que tu dois voir :** Redirection vers `/mon-espace` (tableau de bord client)

- [ ] Connectée, page `/mon-espace` visible

### 3-B. Vérifier le profil de Marie via l'API

Dans le terminal PowerShell :

```powershell
$marieHeaders = @{'Authorization' = "Bearer $marieToken"}
$marieProfil = Invoke-RestMethod `
    -Uri 'http://localhost:8000/api/v1/clients/me' `
    -Method GET `
    -Headers $marieHeaders

Write-Host "Nom     : $($marieProfil.first_name_or_alias) $($marieProfil.last_name)"
Write-Host "Code    : $($marieProfil.public_client_code)"
Write-Host "Statut  : $($marieProfil.record_status)"
```

**Ce que tu dois voir :**

```
Nom     : Marie Tremblay
Code    : CLI-68E7023A24
Statut  : active
```

- [ ] Profil retourné avec le bon code public

### 3-C. Voir le document de suivi dans Firefox

1. Dans Firefox, aller à :

```
http://localhost:3000/suivi?code=CLI-68E7023A24&intake=0198a43e-1bc6-434f-bcb2-ffaa0da86c11
```

**Ce que tu dois voir :** Le document "Compte rendu - Seance du 22-05-2026" affiché.

- [ ] Le document est visible à l'écran

### 3-D. Vérifier que l'API retourne bien ce document

Dans le terminal PowerShell :

```powershell
$docs = Invoke-RestMethod `
    -Uri 'http://localhost:8000/api/v1/derived-documents/public/client/CLI-68E7023A24?intake_request_id=0198a43e-1bc6-434f-bcb2-ffaa0da86c11' `
    -Method GET

Write-Host "Nombre de documents : $($docs.Count)"
Write-Host "Titre               : $($docs[0].title)"
Write-Host "Visible client      : $($docs[0].client_visible)"
```

**Ce que tu dois voir :**

```
Nombre de documents : 1
Titre               : Compte rendu - Seance du 22-05-2026
Visible client      : True
```

- [ ] 1 document, `client_visible = True`

---

## ÉTAPE 4 — PARCOURS C : Praticien → Cycle complet d'une séance

### 4-A. Se connecter comme Jean Beaumont dans Firefox

1. Dans Firefox, aller à : `http://localhost:3000/espace-praticien`
2. Saisir :
   - **Email** : `jean.beaumont@example.com`
   - **Mot de passe** : `TestIVIA2026!`
3. Cliquer sur **Se connecter**

**Ce que tu dois voir :** Tableau de bord praticien

- [ ] Connecté à l'espace praticien

### 4-B. Vérifier l'identité et le rôle de Jean

Dans le terminal PowerShell :

```powershell
$praticienHeaders = @{'Authorization' = "Bearer $praticienToken"}

$jeanProfil = Invoke-RestMethod `
    -Uri 'http://localhost:8000/api/v1/auth/me' `
    -Method GET `
    -Headers $praticienHeaders

Write-Host "Email  : $($jeanProfil.email)"
Write-Host "Rôle   : $($jeanProfil.role)"
```

**Ce que tu dois voir :**

```
Email  : jean.beaumont@example.com
Rôle   : operator
```

- [ ] Rôle `operator` confirmé

### 4-C. Voir la liste des clients de Jean

```powershell
$clients = Invoke-RestMethod `
    -Uri 'http://localhost:8000/api/v1/clients' `
    -Method GET `
    -Headers $praticienHeaders

Write-Host "Clients visibles par Jean : $($clients.Count)"
$clients | ForEach-Object { Write-Host "  - $($_.first_name_or_alias) $($_.last_name) [$($_.id)]" }
```

**Ce que tu dois voir :**

```
Clients visibles par Jean : 1
  - Marie Tremblay [c7603ae9-6a0c-4a69-8a9b-03fe9591faa3]
```

- [ ] Marie Tremblay est visible

### 4-D. Voir la séance existante

```powershell
$sessions = Invoke-RestMethod `
    -Uri 'http://localhost:8000/api/v1/sessions' `
    -Method GET `
    -Headers $praticienHeaders

$sessions | ForEach-Object {
    Write-Host "Séance $($_.id.Substring(0,8))... statut=$($_.session_status_code)"
}
```

**Ce que tu dois voir :**

```
Séance 1c98fb88... statut=completed
```

- [ ] La séance de test apparaît avec statut `completed`

### 4-E. Créer une nouvelle séance (cycle complet)

> On crée ici une **deuxième séance** pour tester le flux de bout en bout.

```powershell
# Créer la séance
$newSess = Invoke-RestMethod `
    -Uri 'http://localhost:8000/api/v1/sessions' `
    -Method POST `
    -Body (@{
        client_id            = "c7603ae9-6a0c-4a69-8a9b-03fe9591faa3"
        session_mode_code    = "individual"
        session_channel_code = "video"
    } | ConvertTo-Json) `
    -ContentType 'application/json' `
    -Headers $praticienHeaders

$newSessionId = $newSess.id
Write-Host "Séance créée  : $newSessionId"
Write-Host "Statut initial: $($newSess.session_status_code)"
```

**Ce que tu dois voir :**

```
Séance créée  : xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
Statut initial: scheduled
```

- [ ] Séance créée, statut `scheduled`

### 4-F. Démarrer la séance

```powershell
$started = Invoke-RestMethod `
    -Uri "http://localhost:8000/api/v1/sessions/$newSessionId/start" `
    -Method POST `
    -Headers $praticienHeaders

Write-Host "Statut : $($started.session_status_code)"
```

**Ce que tu dois voir :**

```
Statut : in_progress
```

- [ ] Statut `in_progress`

### 4-G. Saisir une note de séance

```powershell
$note = Invoke-RestMethod `
    -Uri 'http://localhost:8000/api/v1/session-notes' `
    -Method POST `
    -Body (@{
        client_id      = "c7603ae9-6a0c-4a69-8a9b-03fe9591faa3"
        session_id     = $newSessionId
        note_text      = "Deuxieme seance. Marie a tenu son journal 5 jours sur 7. Elle note une legere amelioration le matin."
        client_visible = $true
    } | ConvertTo-Json) `
    -ContentType 'application/json' `
    -Headers $praticienHeaders

$newNoteId = $note.id
Write-Host "Note créée : $newNoteId"
Write-Host "Validée    : $($note.validated_by_practitioner)"
```

**Ce que tu dois voir :**

```
Note créée : xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
Validée    : False
```

- [ ] Note créée (non validée pour l'instant — normal)

### 4-H. Clôturer la séance

```powershell
$closed = Invoke-RestMethod `
    -Uri "http://localhost:8000/api/v1/sessions/$newSessionId/close" `
    -Method POST `
    -Headers $praticienHeaders

Write-Host "Statut final : $($closed.session_status_code)"
```

**Ce que tu dois voir :**

```
Statut final : completed
```

- [ ] Statut `completed`

### 4-I. Générer un document dérivé

```powershell
$doc = Invoke-RestMethod `
    -Uri 'http://localhost:8000/api/v1/derived-documents' `
    -Method POST `
    -Body (@{
        client_id          = "c7603ae9-6a0c-4a69-8a9b-03fe9591faa3"
        session_id         = $newSessionId
        source_note_id     = $newNoteId
        document_kind_code = "session_summary"
        title              = "Compte rendu - Seance 2 du 22-05-2026"
        body_text          = "Deuxieme seance. Suite positive du journal. Identification des contextes ressourcants entamee."
        client_visible     = $true
    } | ConvertTo-Json) `
    -ContentType 'application/json' `
    -Headers $praticienHeaders

$newDocId = $doc.id
Write-Host "Document créé  : $newDocId"
Write-Host "Visible client : $($doc.client_visible)"
```

**Ce que tu dois voir :**

```
Document créé  : xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
Visible client : False
```

> **Pourquoi `False` ?** Le document n'est visible qu'après validation de la note par un superviseur. L'étape suivante fait le bypass pour les tests locaux.

- [ ] Document créé (visible = False attendu)

### 4-J. Valider la note et rendre le document visible (bypass test)

```powershell
docker exec merlin-postgres-1 psql -U merlin -d merlin_v1 -c "
    UPDATE session_notes
    SET validated_by_practitioner = true, validated_at = now()
    WHERE id = '$newNoteId';

    UPDATE derived_documents
    SET client_visible = true, audience_code = 'client'
    WHERE id = '$newDocId';
"
```

**Ce que tu dois voir :**

```
UPDATE 1
UPDATE 1
```

- [ ] 2 × `UPDATE 1`

### 4-K. Vérifier que le document est maintenant visible

```powershell
$docsAll = Invoke-RestMethod `
    -Uri 'http://localhost:8000/api/v1/derived-documents' `
    -Method GET `
    -Headers $praticienHeaders

$docsAll | ForEach-Object {
    Write-Host "$($_.title) — visible=$($_.client_visible)"
}
```

**Ce que tu dois voir (au moins ces 2 lignes) :**

```
Compte rendu - Seance 2 du 22-05-2026 — visible=True
Compte rendu - Seance du 22-05-2026   — visible=True
```

- [ ] Les deux documents sont visibles

---

## ÉTAPE 5 — PARCOURS D : Admin → Vue globale

### 5-A. Vérifier l'identité admin

```powershell
$adminHeaders = @{'Authorization' = "Bearer $adminToken"}

$adminProfil = Invoke-RestMethod `
    -Uri 'http://localhost:8000/api/v1/auth/me' `
    -Method GET `
    -Headers $adminHeaders

Write-Host "Email : $($adminProfil.email)"
Write-Host "Rôle  : $($adminProfil.role)"
```

**Ce que tu dois voir :**

```
Email : admin@ivia.quebec
Rôle  : admin_tech
```

- [ ] Rôle `admin_tech`

### 5-B. Vue de toutes les séances

```powershell
$allSessions = Invoke-RestMethod `
    -Uri 'http://localhost:8000/api/v1/sessions?limit=50' `
    -Method GET `
    -Headers $adminHeaders

Write-Host "Total séances : $($allSessions.Count)"
$allSessions | ForEach-Object {
    Write-Host "  $($_.id.Substring(0,8))... $($_.session_status_code)"
}
```

- [ ] Au moins 2 séances visibles (completed)

### 5-C. Vue de tous les documents

```powershell
$allDocs = Invoke-RestMethod `
    -Uri 'http://localhost:8000/api/v1/derived-documents?limit=50' `
    -Method GET `
    -Headers $adminHeaders

Write-Host "Total documents : $($allDocs.Count)"
$allDocs | ForEach-Object {
    Write-Host "  [$($_.audience_code)] $($_.title)"
}
```

- [ ] Au moins 2 documents visibles

---

## ÉTAPE 6 — PARCOURS E : Tests de sécurité

> Ces tests vérifient que les protections de rôle fonctionnent. On s'attend à des erreurs ici.

### 6-A. Accès sans token → doit retourner 401

```powershell
try {
    Invoke-RestMethod -Uri 'http://localhost:8000/api/v1/clients/me' -Method GET
} catch {
    $code = [int]($_.Exception.Response.StatusCode)
    Write-Host "Statut : $code $(if ($code -eq 401) { '(OK)' } else { '(ECHEC attendu 401)' })"
}
```

**Ce que tu dois voir :**

```
Statut : 401 (OK)
```

- [ ] 401 retourné

### 6-B. Client essaie d'accéder aux séances → doit retourner 403

```powershell
try {
    Invoke-RestMethod `
        -Uri 'http://localhost:8000/api/v1/sessions' `
        -Method GET `
        -Headers @{'Authorization' = "Bearer $marieToken"}
} catch {
    $code = [int]($_.Exception.Response.StatusCode)
    Write-Host "Statut : $code $(if ($code -eq 403) { '(OK)' } else { '(ECHEC attendu 403)' })"
}
```

**Ce que tu dois voir :**

```
Statut : 403 (OK)
```

- [ ] 403 retourné

### 6-C. Opérateur essaie de valider une note → doit être refusé

```powershell
try {
    Invoke-RestMethod `
        -Uri 'http://localhost:8000/api/v1/session-notes/4ed33f9b-7cde-4411-a6e4-97056dd470bb/validate' `
        -Method PATCH `
        -Body (@{validated = $true} | ConvertTo-Json) `
        -ContentType 'application/json' `
        -Headers @{'Authorization' = "Bearer $praticienToken"}
} catch {
    Write-Host "Erreur : $($_.ErrorDetails.Message)"
}
```

**Ce que tu dois voir :**

```
Erreur : {"detail":"Role insuffisant pour cette operation."}
```

- [ ] Accès refusé avec message métier

---

## ÉTAPE 7 — Smoke test final (toutes les routes en une passe)

> Copier-coller ce bloc entier. Il vérifie toutes les routes critiques en 30 secondes.

```powershell
$base   = 'http://localhost:8000'
$errors = 0

function Test-Route {
    param($label, $uri, $method='GET', $body=$null, $token=$null, $expected=200)
    $h = @{}
    if ($token) { $h['Authorization'] = "Bearer $token" }
    try {
        $p = @{ Uri=$uri; Method=$method; Headers=$h; UseBasicParsing=$true }
        if ($body) { $p['Body']=$body; $p['ContentType']='application/json' }
        $r = Invoke-WebRequest @p
        $ok = $r.StatusCode -eq $expected
        Write-Host "$(if ($ok) {'[OK  ]'} else {'[FAIL]'}) $label => $($r.StatusCode)"
        if (-not $ok) { $script:errors++ }
    } catch {
        $got = [int]($_.Exception.Response.StatusCode)
        $ok  = $got -eq $expected
        Write-Host "$(if ($ok) {'[OK  ]'} else {'[FAIL]'}) $label => $got (attendu $expected)"
        if (-not $ok) { $script:errors++ }
    }
}

Write-Host "`n=== INFRASTRUCTURE ==="
Test-Route "Health"                      "$base/health"

Write-Host "`n=== PAGES PUBLIQUES ==="
Test-Route "GET /praticiens"             "$base/api/v1/praticiens"
Test-Route "GET /suivi public (doc)"     "$base/api/v1/derived-documents/public/client/CLI-68E7023A24?intake_request_id=0198a43e-1bc6-434f-bcb2-ffaa0da86c11"

Write-Host "`n=== ESPACE CLIENT ==="
Test-Route "GET /clients/me (Marie)"     "$base/api/v1/clients/me"           -token $marieToken

Write-Host "`n=== ESPACE PRATICIEN ==="
Test-Route "GET /sessions (Jean)"        "$base/api/v1/sessions"             -token $praticienToken
Test-Route "GET /session-notes (Jean)"   "$base/api/v1/session-notes"        -token $praticienToken
Test-Route "GET /derived-documents"      "$base/api/v1/derived-documents"    -token $praticienToken

Write-Host "`n=== ADMIN ==="
Test-Route "GET /auth/me (admin)"        "$base/api/v1/auth/me"              -token $adminToken

Write-Host "`n=== SECURITE ==="
Test-Route "Sans token => 401"           "$base/api/v1/clients/me"           -expected 401
Test-Route "Client => sessions 403"      "$base/api/v1/sessions"             -token $marieToken -expected 403

Write-Host ""
if ($errors -eq 0) {
    Write-Host "========================================"
    Write-Host "  TOUS LES TESTS SONT PASSES (0 erreur)"
    Write-Host "========================================"
} else {
    Write-Host "========================================"
    Write-Host "  $errors TEST(S) EN ECHEC"
    Write-Host "========================================"
}
```

**Ce que tu dois voir à la fin :**

```
========================================
  TOUS LES TESTS SONT PASSES (0 erreur)
========================================
```

- [ ] 0 erreur

---

## CHECKLIST FINALE

### Infrastructure
- [ ] Docker : `merlin-postgres-1`, `merlin-backend-1` UP
- [ ] `GET /health` → `status: ok`, `database: ok`
- [ ] Next.js `npm run dev` actif sur port 3000

### Comptes
- [ ] Admin `admin@ivia.quebec` → token OK, rôle `admin_tech`
- [ ] Praticien `jean.beaumont@example.com` → token OK, rôle `operator`
- [ ] Client `marie.tremblay@example.com` → token OK, rôle `public_client`

### Flux client
- [ ] `GET /clients/me` (Marie) → profil avec `public_client_code=CLI-68E7023A24`
- [ ] Page `/suivi?code=CLI-68E7023A24&intake=0198a43e...` → document visible

### Flux praticien
- [ ] Séance créée → `scheduled`
- [ ] Séance démarrée → `in_progress`
- [ ] Note créée
- [ ] Séance clôturée → `completed`
- [ ] Document créé et validé (bypass SQL) → `client_visible=True`

### Sécurité
- [ ] Sans token → 401
- [ ] Client sur route opérateur → 403
- [ ] Opérateur sur validation → "Rôle insuffisant"

---

## Comptes de test — Référence rapide

| Rôle | Email | Mot de passe |
|------|-------|-------------|
| Admin | `admin@ivia.quebec` | `AdminIVIA2026!` |
| Praticien | `jean.beaumont@example.com` | `TestIVIA2026!` |
| Client | `marie.tremblay@example.com` | `TestIVIA2026!` |

## IDs de référence

| Objet | ID |
|-------|-----|
| Client Marie (profil) | `c7603ae9-6a0c-4a69-8a9b-03fe9591faa3` |
| Code public client | `CLI-68E7023A24` |
| Intake request | `0198a43e-1bc6-434f-bcb2-ffaa0da86c11` |
| Séance de test (séance 1) | `1c98fb88-748f-4c7a-97b5-3806d870ce0c` |
| Note de test (séance 1) | `4ed33f9b-7cde-4411-a6e4-97056dd470bb` |
| Document de test (séance 1) | `9deb4166-a110-472b-acae-293560649208` |

---

*Procédure v2.0 — 22 mai 2026 — Environnement de développement local uniquement*

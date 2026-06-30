---
id: TEST-LOCAL-2026-05-24
type: procédure de test guidée
date: 2026-05-24
auteur: David Phaneuf
version: v4.0
---

# Procédure de test complète — IVIA/MERLIN local
## Guide pas à pas — 24 mai 2026

---

> **Comment lire ce document**
> Chaque étape indique exactement **où aller**, **quoi taper**, et **ce que tu dois voir**.
> Les blocs de code sont à copier-coller tels quels dans PowerShell.
> Une case à cocher confirme que l'étape est passée.

---

## Corrections intégrées — 24 mai 2026

| # | Correction | Fichiers touchés |
|---|-----------|-----------------|
| 1 | Token expiré côté client : `isTokenExpired()` détecte l'expiration avant appel API, redirige vers `/acces-client` | `src/lib/merlin-api.ts` |
| 2 | Bouton **Annuler** affiché sur chaque RDV à venir dans Mon espace | `src/app/mon-espace/page.tsx` |
| 3 | Libellés français des statuts RDV : `hold` → "En attente", `confirmed` → "Confirmé", `cancelled` → "Annulé" | `src/app/mon-espace/page.tsx` |
| 4 | Badge CSS ambre pour statut `hold` (`.rdv-badge--hold`) | `src/app/styles.css` |
| 5 | `GET /bookings/my` : expire automatiquement les holds dont le TTL est dépassé — ils disparaissent de la liste | `app/api/routes/bookings.py` |
| 6 | Demande Interac e-transfer : prolonge le hold à **72 h** (au lieu de 15 min) pour laisser le temps au virement d'arriver | `app/api/routes/payments.py` |

> **Note sur les holds expirés** : Les holds créés pendant les tests précédents (TTL = 15 min) ont été nettoyés automatiquement au premier appel de `GET /bookings/my`. 7 créneaux ont été libérés.

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
merlin-backend-1        Up X minutes    0.0.0.0:8000->8000/tcp
merlin-postgres-1       Up X minutes    0.0.0.0:5432->5432/tcp
```

> **Si tu vois "Cannot connect to the Docker daemon"** → Docker Desktop n'est pas démarré.
> Ouvrir Docker Desktop depuis le bureau ou le menu Démarrer. Attendre que l'icône Docker soit stable, puis relancer.

> **Si les conteneurs ne sont pas là** :
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

> ⚠️ **Important** : Après chaque `docker restart merlin-backend-1`, réinjecter les fichiers modifiés **avant** le redémarrage :
> ```powershell
> docker cp "C:\MERLIN\10_backend_merlin_api\app\api\routes\bookings.py" merlin-backend-1:/app/app/api/routes/bookings.py
> docker cp "C:\MERLIN\10_backend_merlin_api\app\api\routes\payments.py" merlin-backend-1:/app/app/api/routes/payments.py
> docker restart merlin-backend-1
> ```

- [ ] `status : ok` et `database : ok`

### 0-D. Démarrer le serveur Next.js (frontend de développement)

Le frontend de développement tourne **en dehors de Docker**, directement sur ta machine.

1. Ouvrir un **deuxième terminal PowerShell**
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

> On récupère les 4 tokens (admin, praticien Aelis, opérateur Jean, client Marie) et on les stocke dans des variables.

Dans le **premier terminal PowerShell**, copier-coller ce bloc entier :

```powershell
# --- TOKEN ADMIN ---
$adminToken = (Invoke-RestMethod `
    -Uri 'http://localhost:8000/api/v1/auth/login' `
    -Method POST `
    -Body (@{email='admin@ivia.quebec'; password='AdminIVIA2026!'} | ConvertTo-Json) `
    -ContentType 'application/json').access_token

# --- TOKEN PRATICIEN (Aelis) ---
$aelisToken = (Invoke-RestMethod `
    -Uri 'http://localhost:8000/api/v1/auth/login' `
    -Method POST `
    -Body (@{email='pilote.aelis@ivia.quebec'; password='IVIA2026!'} | ConvertTo-Json) `
    -ContentType 'application/json').access_token

# --- TOKEN OPÉRATEUR (Jean) ---
$jeanToken = (Invoke-RestMethod `
    -Uri 'http://localhost:8000/api/v1/auth/login' `
    -Method POST `
    -Body (@{email='jean.beaumont@example.com'; password='IVIA2026!'} | ConvertTo-Json) `
    -ContentType 'application/json').access_token

# --- TOKEN CLIENT (Marie) ---
$marieToken = (Invoke-RestMethod `
    -Uri 'http://localhost:8000/api/v1/auth/login' `
    -Method POST `
    -Body (@{email='marie.tremblay@example.com'; password='TestIVIA2026!'} | ConvertTo-Json) `
    -ContentType 'application/json').access_token

# --- IDs de référence ---
$cId = 'c7603ae9-6a0c-4a69-8a9b-03fe9591faa3'   # Marie (client_id)
$aId = '2c72a544-e324-45ec-bbf0-9d158b44953a'   # Aelis (praticien_id)

# --- VÉRIFICATION ---
Write-Host "Admin  : $(if ($adminToken) { 'OK' } else { 'ECHEC' })"
Write-Host "Aelis  : $(if ($aelisToken) { 'OK' } else { 'ECHEC' })"
Write-Host "Jean   : $(if ($jeanToken)  { 'OK' } else { 'ECHEC' })"
Write-Host "Marie  : $(if ($marieToken) { 'OK' } else { 'ECHEC' })"
```

**Ce que tu dois voir :**

```
Admin  : OK
Aelis  : OK
Jean   : OK
Marie  : OK
```

> **Si tu vois ECHEC** → l'un des comptes n'existe pas. Relancer le script de seeding :
> ```powershell
> powershell -ExecutionPolicy Bypass -File "C:\MERLIN\04_METHODES\seed_full_v2.ps1"
> ```
> Puis relancer ce bloc.

- [ ] Les 4 tokens sont OK

> ⚠️ **Important** : Ces variables sont actives dans ce terminal uniquement. Si tu fermes le terminal, relancer ce bloc.

---

## ÉTAPE 2 — PARCOURS A : Visiteur public

> Aucune connexion requise. Ouvrir Firefox.

### 2-A. Tester les pages publiques dans Firefox

Ouvrir **Firefox** et naviguer vers chacune de ces adresses :

| Page | URL | Ce que tu dois voir |
|------|-----|---------------------|
| Accueil | `http://localhost:3000` | Page d'accueil IVIA, navigation en haut |
| Praticiens | `http://localhost:3000/praticiens` | Liste des praticiens pilotes |
| Démarche | `http://localhost:3000/demarche` | Explication du service |
| Ressources | `http://localhost:3000/ressources` | Page ressources |
| Rendez-vous | `http://localhost:3000/rendez-vous` | Formulaire de prise de contact |

- [ ] Toutes les pages s'affichent sans écran blanc ni erreur

### 2-B. Vérifier le texte du héros sur la page d'accueil

1. Sur `http://localhost:3000`, regarder le grand titre en haut
2. Le titre doit lire exactement :

```
Quelqu'un à votre écoute.
```

- [ ] Le titre affiché est bien **"Quelqu'un à votre écoute."**

### 2-C. Vérifier la navigation persistante (sticky)

1. Sur chaque page publique, faire défiler vers le bas
2. La barre de navigation doit rester visible en haut (sticky)
3. Le bouton CTA doit afficher **"Connexion"** (car non connecté)

- [ ] La nav reste visible en défilant sur toutes les pages
- [ ] Le CTA affiche **"Connexion"** quand non connecté

### 2-D. Tester la création d'une demande d'entrée (API)

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

**Ce que tu dois voir :** Redirection automatique vers `/mon-espace` (tableau de bord client)

- [ ] Connectée, page `/mon-espace` visible
- [ ] Le CTA dans la nav affiche maintenant **"Mon espace"** (changement après connexion)

### 3-B. Vérifier le profil de Marie via l'API

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

### 3-C. Voir le document de suivi dans Firefox *(accessible sans connexion)*

1. Dans Firefox, **se déconnecter d'abord** (ou ouvrir un onglet privé)
2. Aller à :

```
http://localhost:3000/suivi?code=CLI-68E7023A24&intake=0198a43e-1bc6-434f-bcb2-ffaa0da86c11
```

**Ce que tu dois voir :** Le document "Compte rendu - Seance du 22-05-2026" affiché, **sans avoir à se connecter**.

- [ ] Le document est visible sans connexion préalable
- [ ] La page affiche la navigation (PublicLayout) en haut et en bas

### 3-D. Vérifier l'API du document de suivi

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

## ÉTAPE 4 — PARCOURS C : Praticien → Connexion unifiée + Cycle complet d'une séance

### 4-A. Se connecter comme Aelis (praticien) via `/acces-client`

1. Dans Firefox, aller à : `http://localhost:3000/acces-client`
2. Saisir :
   - **Email** : `pilote.aelis@ivia.quebec`
   - **Mot de passe** : `IVIA2026!`
3. Cliquer sur **Se connecter**

**Ce que tu dois voir :**
- Redirection automatique vers `/espace-praticien`
- Tableau de bord praticien affiché : "Espace praticien — Aelis · pilote.aelis@ivia.quebec"

- [ ] Connecté en tant que praticien, page `/espace-praticien` visible
- [ ] Nom "Aelis" visible dans le tableau de bord

### 4-B. Vérifier l'identité et le rôle d'Aelis

```powershell
$aelisHeaders = @{'Authorization' = "Bearer $aelisToken"}

$aelisProfil = Invoke-RestMethod `
    -Uri 'http://localhost:8000/api/v1/auth/me' `
    -Method GET `
    -Headers $aelisHeaders

Write-Host "Email  : $($aelisProfil.email)"
Write-Host "Rôle   : $($aelisProfil.role)"
```

**Ce que tu dois voir :**

```
Email  : pilote.aelis@ivia.quebec
Rôle   : practitioner
```

- [ ] Rôle `practitioner` confirmé

### 4-C. Voir les clients d'Aelis

```powershell
$clients = Invoke-RestMethod `
    -Uri 'http://localhost:8000/api/v1/clients?limit=10' `
    -Method GET `
    -Headers $aelisHeaders

Write-Host "Clients visibles : $($clients.Count)"
$clients | ForEach-Object { Write-Host "  $($_.first_name_or_alias) $($_.last_name)" }
```

- [ ] Au moins un client apparaît

### 4-D. Créer une nouvelle séance (cycle complet)

```powershell
$newSess = Invoke-RestMethod `
    -Uri 'http://localhost:8000/api/v1/sessions' `
    -Method POST `
    -Body (@{
        client_id            = $cId
        session_mode_code    = "individual"
        session_channel_code = "video"
    } | ConvertTo-Json) `
    -ContentType 'application/json' `
    -Headers $aelisHeaders

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

### 4-E. Démarrer la séance

```powershell
$started = Invoke-RestMethod `
    -Uri "http://localhost:8000/api/v1/sessions/$newSessionId/start" `
    -Method POST `
    -Headers $aelisHeaders

Write-Host "Statut : $($started.session_status_code)"
```

**Ce que tu dois voir :**

```
Statut : in_progress
```

- [ ] Statut `in_progress`

### 4-F. Saisir une note de séance

```powershell
$note = Invoke-RestMethod `
    -Uri 'http://localhost:8000/api/v1/session-notes' `
    -Method POST `
    -Body (@{
        client_id      = $cId
        session_id     = $newSessionId
        note_text      = "Seance du 24-05. Aelis note une progression dans la régulation. Journal tenu 6 jours sur 7."
        client_visible = $true
    } | ConvertTo-Json) `
    -ContentType 'application/json' `
    -Headers $aelisHeaders

$newNoteId = $note.id
Write-Host "Note créée : $newNoteId"
Write-Host "Validée    : $($note.validated_by_practitioner)"
```

**Ce que tu dois voir :**

```
Note créée : xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
Validée    : False
```

- [ ] Note créée

### 4-G. Clôturer la séance

```powershell
$closed = Invoke-RestMethod `
    -Uri "http://localhost:8000/api/v1/sessions/$newSessionId/close" `
    -Method POST `
    -Headers $aelisHeaders

Write-Host "Statut final : $($closed.session_status_code)"
```

**Ce que tu dois voir :**

```
Statut final : completed
```

- [ ] Statut `completed`

### 4-H. Générer un document dérivé

```powershell
$doc = Invoke-RestMethod `
    -Uri 'http://localhost:8000/api/v1/derived-documents' `
    -Method POST `
    -Body (@{
        client_id          = $cId
        session_id         = $newSessionId
        source_note_id     = $newNoteId
        document_kind_code = "session_summary"
        title              = "Compte rendu - Seance du 24-05-2026"
        body_text          = "Seance du 24-05. Progression dans la régulation. Journal tenu 6 jours sur 7."
        client_visible     = $true
    } | ConvertTo-Json) `
    -ContentType 'application/json' `
    -Headers $aelisHeaders

$newDocId = $doc.id
Write-Host "Document créé  : $newDocId"
Write-Host "Visible client : $($doc.client_visible)"
```

**Ce que tu dois voir :**

```
Document créé  : xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
Visible client : False
```

> **Pourquoi `False` ?** Le document n'est visible qu'après validation. L'étape suivante fait le bypass pour les tests locaux.

- [ ] Document créé

### 4-I. Valider la note et rendre le document visible (bypass test)

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

### 4-J. Vérifier que le document est maintenant visible

```powershell
$docsAll = Invoke-RestMethod `
    -Uri 'http://localhost:8000/api/v1/derived-documents' `
    -Method GET `
    -Headers $aelisHeaders

$docsAll | ForEach-Object {
    Write-Host "$($_.title) — visible=$($_.client_visible)"
}
```

- [ ] Le nouveau document apparaît avec `visible=True`

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
Rôle  : admin
```

- [ ] Rôle `admin` confirmé

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

- [ ] Au moins 2 séances visibles (dont au moins une `completed`)

### 5-C. Vue de tous les documents

```powershell
$allDocs = Invoke-RestMethod `
    -Uri 'http://localhost:8000/api/v1/derived-documents?limit=50' `
    -Method GET `
    -Headers $adminHeaders

Write-Host "Total documents : $($allDocs.Count)"
$allDocs | ForEach-Object {
    Write-Host "  $($_.title) — visible=$($_.client_visible)"
}
```

- [ ] Au moins 1 document visible avec `client_visible = True`

### 5-D. Vérifier les accès non autorisés

```powershell
# Sans token → 401
try {
    Invoke-RestMethod -Uri 'http://localhost:8000/api/v1/clients/me' -Method GET
} catch { Write-Host "Sans token → $($_.Exception.Response.StatusCode.value__)" }

# Client sur route opérateur → 403
try {
    Invoke-RestMethod `
        -Uri 'http://localhost:8000/api/v1/payments/interac/etransfer/FAKE-ID/mark-paid' `
        -Method POST `
        -Body (@{confirmed_amount_cents=100;confirmed_by_note='test'} | ConvertTo-Json) `
        -ContentType 'application/json' `
        -Headers @{Authorization="Bearer $marieToken"}
} catch { Write-Host "Client sur mark-paid → $($_.Exception.Response.StatusCode.value__)" }
```

**Ce que tu dois voir :**

```
Sans token → 401
Client sur mark-paid → 403
```

- [ ] 401 sans token
- [ ] 403 pour accès non autorisé

---

## ÉTAPE 6 — PARCOURS E : Prise de RDV complet — Hold → Interac → Confirmation → Mon espace *(nouveau 24-05)*

> Ce parcours simule le flux complet d'une réservation par Marie Tremblay :
> 1. Marie consulte les créneaux disponibles
> 2. Marie pose un hold (réservation temporaire)
> 3. Marie initie un virement Interac
> 4. L'opérateur Jean marque le paiement reçu
> 5. Le RDV passe à `confirmed`
> 6. Marie voit le RDV confirmé dans Mon espace

### 6-A. Consulter les créneaux disponibles

```powershell
$slots = Invoke-RestMethod `
    -Uri "http://localhost:8000/api/v1/schedules/available?praticien_id=$aId&date_from=2026-05-24&date_to=2026-06-15" `
    -Headers @{Authorization="Bearer $marieToken"}

Write-Host "Créneaux disponibles : $($slots.Count)"
$slots | ForEach-Object { Write-Host "  $($_.slot_date) $($_.start_time) — $($_.end_time)" }
```

**Ce que tu dois voir :** Au moins 10 créneaux à partir du 25 mai 2026.

```
Créneaux disponibles : 18
  2026-05-25 09:00:00 — 10:00:00
  2026-05-27 13:00:00 — 14:00:00
  ...
```

- [ ] Au moins 5 créneaux disponibles dans le futur

### 6-B. Poser un hold sur un créneau

> On utilise le créneau **2026-05-27 13:00** d'Aelis.

```powershell
$held = Invoke-RestMethod `
    -Uri 'http://localhost:8000/api/v1/bookings/hold' `
    -Method POST `
    -Body (@{
        praticien_id = $aId
        slot_date    = '2026-05-27'
        start_time   = '13:00:00'
        end_time     = '14:00:00'
        session_type = 'intake'
    } | ConvertTo-Json) `
    -ContentType 'application/json' `
    -Headers @{Authorization="Bearer $marieToken"}

$holdId = $held.id
Write-Host "Hold posé     : $holdId"
Write-Host "Statut        : $($held.status)"
Write-Host "Expire à      : $($held.hold_expires_at)"
```

**Ce que tu dois voir :**

```
Hold posé     : xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
Statut        : hold
Expire à      : 2026-05-27T13:15:xx.xxxxxxZ   (15 min TTL)
```

> **Explication** : Le TTL est 15 min à ce stade. Il sera **prolongé à 72 h** dès que la demande Interac est créée (étape suivante).

- [ ] Statut `hold`, un ID est retourné

> **Si tu vois `"Ce créneau n'est plus disponible."`** → le créneau est déjà pris. Relancer 6-A et choisir un autre créneau disponible.

### 6-C. Créer une demande de virement Interac

```powershell
$order = Invoke-RestMethod `
    -Uri 'http://localhost:8000/api/v1/payments/interac/etransfer/request' `
    -Method POST `
    -Body (@{
        client_id               = $cId
        slot_id                 = $holdId
        product_code            = 'session_intake'
        product_label           = 'Séance IVIA — Intake'
        product_kind_code       = 'session_intake'
        fulfillment_mode_code   = 'grant_entitlement_only'
        amount_cents            = 6500
        currency                = 'cad'
        entitlement_type_code   = 'intake_session_credit'
        entitlement_quantity    = 1
    } | ConvertTo-Json) `
    -ContentType 'application/json' `
    -Headers @{Authorization="Bearer $marieToken"}

$orderId = $order.order_id
Write-Host "Ordre créé       : $orderId"
Write-Host "Référence        : $($order.transfer_reference)"
Write-Host "Destinataire     : $($order.recipient_name) <$($order.recipient_email)>"
Write-Host "Courriel envoyé  : $($order.instructions_emailed)"
```

**Ce que tu dois voir :**

```
Ordre créé       : xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
Référence        : IVIA-XXXXXXXX
Destinataire     : IVIA <david@fa9.quebec>
Courriel envoyé  : True
```

> **Ce qui se passe en coulisses** :
> 1. Un `PaymentOrder` de type `interac_etransfer` est créé, lié au `slot_id`
> 2. Le `hold_expires_at` du slot est prolongé à `now + 72h` (correction 24-05)
> 3. Un courriel avec les instructions de virement est envoyé à Marie
> 4. Marie envoie le virement à l'adresse `david@fa9.quebec` avec la référence

- [ ] Un `order_id` est retourné
- [ ] Une `transfer_reference` de format `IVIA-XXXXXXXX` est affichée
- [ ] `instructions_emailed : True`

### 6-D. Vérifier que le hold est prolongé à 72 h

```powershell
$mine = Invoke-RestMethod `
    -Uri 'http://localhost:8000/api/v1/bookings/my' `
    -Headers @{Authorization="Bearer $marieToken"}

$myHold = $mine | Where-Object { $_.id -eq $holdId }
Write-Host "Statut      : $($myHold.status)"
Write-Host "Expire à    : $($myHold.hold_expires_at)"
```

**Ce que tu dois voir :** L'expiration doit être dans ~72 h (pas dans 15 min).

```
Statut      : hold
Expire à    : 2026-05-27T13:xx:xx.xxxxxxZ   (≈ now + 72h)
```

- [ ] Statut toujours `hold`
- [ ] `hold_expires_at` est dans le futur à ~72 h

### 6-E. Marquer le paiement comme reçu (opérateur Jean)

> Jean (opérateur) vérifie la réception du virement Interac et le confirme.

```powershell
$markPaid = Invoke-RestMethod `
    -Uri "http://localhost:8000/api/v1/payments/interac/etransfer/$orderId/mark-paid" `
    -Method POST `
    -Body (@{
        confirmed_amount_cents = 6500
        confirmed_by_note      = 'Virement Interac reçu — test 24-05'
    } | ConvertTo-Json) `
    -ContentType 'application/json' `
    -Headers @{Authorization="Bearer $jeanToken"}

Write-Host "Statut ordre  : $($markPaid.status)"
Write-Host "Ordre ID      : $($markPaid.order_id)"
Write-Host "Entitlement   : $($markPaid.entitlement_id)"
```

**Ce que tu dois voir :**

```
Statut ordre  : created
Ordre ID      : xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
Entitlement   : xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

> **Qui peut faire `mark-paid` ?** Uniquement le rôle `operator`. Ni le client (Marie) ni l'admin ne peuvent le faire directement.

- [ ] Statut `created` (entitlement accordé)

### 6-F. Vérifier que le RDV est confirmé

```powershell
$mine = Invoke-RestMethod `
    -Uri 'http://localhost:8000/api/v1/bookings/my' `
    -Headers @{Authorization="Bearer $marieToken"}

Write-Host "Nombre de RDV : $($mine.Count)"
$mine | ForEach-Object {
    Write-Host "  $($_.slot_date) $($_.start_time) | statut: $($_.status)"
}
```

**Ce que tu dois voir :** Le hold est passé à `confirmed`.

```
Nombre de RDV : X
  2026-05-25 10:15:00 | statut: confirmed
  2026-05-27 13:00:00 | statut: confirmed   ← notre nouveau RDV
  2026-06-03 14:15:00 | statut: confirmed
```

- [ ] Le créneau `2026-05-27 13:00` est maintenant `confirmed`
- [ ] Aucun hold expiré n'apparaît dans la liste

### 6-G. Vérifier Mon espace dans Firefox *(nouveau 24-05)*

1. Dans Firefox, se reconnecter comme Marie : `http://localhost:3000/acces-client`
2. Aller dans **Mon espace** (ou recharger la page)
3. Cliquer sur l'onglet **Rendez-vous**

**Ce que tu dois voir :**

| Élément | Attendu |
|---------|---------|
| Statut du nouveau RDV | Badge vert **"Confirmé"** |
| Anciens holds | **Disparus** (nettoyés automatiquement) |
| Bouton "Annuler" | Visible sur chaque RDV à venir |
| Anciens holds (si encore présents) | Badge ambre **"En attente"** |

- [ ] Badge vert "Confirmé" visible sur le nouveau RDV
- [ ] Aucun hold expiré dans la liste
- [ ] Bouton "Annuler" visible sur les RDV à venir

### 6-H. Tester l'annulation d'un RDV

> ⚠️ Cette étape annule le RDV que tu viens de créer. Ne l'effectue que si tu veux tester le flux d'annulation.

```powershell
# Annuler le hold/RDV créé en 6-B
$cancelled = Invoke-RestMethod `
    -Uri 'http://localhost:8000/api/v1/bookings/cancel' `
    -Method POST `
    -Body (@{ slot_id = $holdId } | ConvertTo-Json) `
    -ContentType 'application/json' `
    -Headers @{Authorization="Bearer $marieToken"}

Write-Host "Nouveau statut : $($cancelled.status)"
```

**Ce que tu dois voir :**

```
Nouveau statut : cancelled
```

**Dans Firefox :** Recharger Mon espace → le RDV doit avoir disparu de la liste des RDV à venir.

- [ ] Statut `cancelled` retourné
- [ ] RDV disparu de Mon espace après rechargement

### 6-I. Test de sécurité : expiration de token

```powershell
# Tenter d'appeler /bookings/my avec un token invalide → 401
try {
    Invoke-RestMethod `
        -Uri 'http://localhost:8000/api/v1/bookings/my' `
        -Headers @{Authorization='Bearer invalid.token'}
} catch { Write-Host "Token invalide → $($_.Exception.Response.StatusCode.value__)" }
```

**Ce que tu dois voir :**

```
Token invalide → 401
```

**Dans Firefox :** Si le token localStorage est expiré (> 120 min), recharger Mon espace → redirection automatique vers `/acces-client` (correction 24-05).

- [ ] 401 pour token invalide
- [ ] Token expiré → redirection vers `/acces-client` dans le navigateur

---

## ÉTAPE 7 — Validation rapide complète (script autonome)

> Ce bloc exécute toutes les vérifications API en une seule passe et affiche un résumé.

```powershell
$errors = 0

function Check($label, $test) {
    try {
        $result = & $test
        if ($result) { Write-Host "  [OK] $label" }
        else { Write-Host "  [FAIL] $label"; $script:errors++ }
    } catch {
        Write-Host "  [ERROR] $label : $($_.Exception.Message)"
        $script:errors++
    }
}

Write-Host "`n=== VÉRIFICATIONS BACKEND ==="

Check "Health" { (Invoke-RestMethod 'http://localhost:8000/health').status -eq 'ok' }
Check "Login admin" { $adminToken -and $adminToken.Length -gt 10 }
Check "Login Aelis" { $aelisToken -and $aelisToken.Length -gt 10 }
Check "Login Jean"  { $jeanToken -and $jeanToken.Length -gt 10 }
Check "Login Marie" { $marieToken -and $marieToken.Length -gt 10 }
Check "Profil Marie (clients/me)" {
    $p = Invoke-RestMethod -Uri 'http://localhost:8000/api/v1/clients/me' -Headers @{Authorization="Bearer $marieToken"}
    $p.public_client_code -eq 'CLI-68E7023A24'
}
Check "Créneaux disponibles (≥ 5)" {
    $s = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/schedules/available?praticien_id=$aId&date_from=2026-05-24&date_to=2026-06-15" -Headers @{Authorization="Bearer $marieToken"}
    $s.Count -ge 5
}
Check "Mes RDV — pas de hold expiré" {
    $mine = Invoke-RestMethod -Uri 'http://localhost:8000/api/v1/bookings/my' -Headers @{Authorization="Bearer $marieToken"}
    $now = [datetime]::UtcNow
    $expiredHolds = $mine | Where-Object { $_.status -eq 'hold' -and $_.hold_expires_at -and ([datetime]$_.hold_expires_at) -lt $now }
    $expiredHolds.Count -eq 0
}
Check "401 sans token" {
    try { Invoke-RestMethod -Uri 'http://localhost:8000/api/v1/clients/me'; $false }
    catch { $_.Exception.Response.StatusCode.value__ -eq 401 }
}
Check "403 mark-paid (client)" {
    try {
        Invoke-RestMethod `
            -Uri 'http://localhost:8000/api/v1/payments/interac/etransfer/FAKE-ID/mark-paid' `
            -Method POST `
            -Body (@{confirmed_amount_cents=100;confirmed_by_note='test'} | ConvertTo-Json) `
            -ContentType 'application/json' `
            -Headers @{Authorization="Bearer $marieToken"}
        $false
    } catch { $_.Exception.Response.StatusCode.value__ -in @(403, 404) }
}

Write-Host "`n========================================"
if ($errors -eq 0) {
    Write-Host "  TOUS LES TESTS SONT PASSÉS (0 erreur)"
} else {
    Write-Host "  $errors ERREUR(S) DÉTECTÉE(S)"
}
Write-Host "========================================"
```

**Ce que tu dois voir à la fin :**

```
========================================
  TOUS LES TESTS SONT PASSÉS (0 erreur)
========================================
```

- [ ] 0 erreur

---

## CHECKLIST FINALE

### Infrastructure
- [ ] Docker : `merlin-postgres-1`, `merlin-backend-1` UP
- [ ] `GET /health` → `status: ok`, `database: ok`
- [ ] Next.js `npm run dev` actif sur port 3000, `.env` contient `JWT_SECRET`
- [ ] Fichiers backend injectés : `bookings.py` et `payments.py`

### Comptes
- [ ] Admin `admin@ivia.quebec` → token OK, rôle `admin`
- [ ] Praticien `pilote.aelis@ivia.quebec` → token OK, rôle `practitioner`
- [ ] Opérateur `jean.beaumont@example.com` → token OK, rôle `operator`
- [ ] Client `marie.tremblay@example.com` → token OK, rôle `public_client`

### Flux client
- [ ] Login via `/acces-client` → redirigé vers `/mon-espace`
- [ ] CTA nav passe de "Connexion" à "Mon espace" après login
- [ ] `GET /clients/me` (Marie) → profil avec `public_client_code=CLI-68E7023A24`
- [ ] Page `/suivi?code=CLI-68E7023A24&intake=0198a43e...` → document visible **sans connexion**

### Flux praticien
- [ ] Login via `/acces-client` → redirigé vers `/espace-praticien` automatiquement
- [ ] Accès direct `/espace-praticien` sans cookie → redirigé vers `/acces-client`
- [ ] Séance créée → `scheduled`
- [ ] Séance démarrée → `in_progress`
- [ ] Note créée
- [ ] Séance clôturée → `completed`
- [ ] Document créé et validé (bypass SQL) → `client_visible=True`

### Flux RDV complet *(nouveau 24-05)*
- [ ] Créneaux disponibles : au moins 5 à partir du 25 mai 2026
- [ ] Hold posé → statut `hold`, TTL 15 min
- [ ] Demande Interac → `transfer_reference` générée, courriel envoyé
- [ ] Hold prolongé à **72 h** après demande Interac *(correction 24-05)*
- [ ] `mark-paid` (Jean) → entitlement accordé
- [ ] Statut RDV passe à `confirmed`
- [ ] Annulation → statut `cancelled`, créneau libéré

### Mon espace *(nouveau 24-05)*
- [ ] Token expiré → redirection vers `/acces-client` (pas d'erreur blanche)
- [ ] Holds expirés filtrés automatiquement (nettoyage lazy)
- [ ] Libellés français : "En attente", "Confirmé", "Annulé"
- [ ] Badge ambre pour statut `hold`
- [ ] Bouton "Annuler" sur chaque RDV à venir

### Navigation
- [ ] Titre hero homepage : "Quelqu'un à votre écoute."
- [ ] Nav sticky sur toutes les pages
- [ ] PublicLayout présent sur `/suivi` et `/rendez-vous/confirmation`

### Sécurité
- [ ] Sans token → 401
- [ ] Client sur route opérateur → 403
- [ ] Opérateur sur `mark-paid` → OK ; Client → 403
- [ ] Accès non autorisé `/espace-praticien` → redirect `/acces-client` (pas 404)

---

## Comptes de test — Référence rapide

| Rôle | Email | Mot de passe |
|------|-------|-------------|
| Admin | `admin@ivia.quebec` | `AdminIVIA2026!` |
| Praticien | `pilote.aelis@ivia.quebec` | `IVIA2026!` |
| Praticien | `pilote.nael@ivia.quebec` | `IVIA2026!` |
| Opérateur | `jean.beaumont@example.com` | `IVIA2026!` |
| Client | `marie.tremblay@example.com` | `TestIVIA2026!` |

## IDs de référence

| Objet | ID |
|-------|-----|
| Client Marie (profil) | `c7603ae9-6a0c-4a69-8a9b-03fe9591faa3` |
| Praticien Aelis | `2c72a544-e324-45ec-bbf0-9d158b44953a` |
| Code public client | `CLI-68E7023A24` |
| Intake request | `0198a43e-1bc6-434f-bcb2-ffaa0da86c11` |
| Séance de test (séance 1) | `1c98fb88-748f-4c7a-97b5-3806d870ce0c` |
| Note de test (séance 1) | `4ed33f9b-7cde-4411-a6e4-97056dd470bb` |
| Document de test (séance 1) | `9deb4166-a110-472b-acae-293560649208` |

## Créneaux disponibles — Aelis (au 24 mai 2026)

| Date | Début | Fin |
|------|-------|-----|
| 2026-05-25 | 09:00 | 10:00 |
| 2026-05-27 | 13:00 | 14:00 |
| 2026-05-27 | 14:15 | 15:15 |
| 2026-05-29 | 09:00 | 10:00 |
| 2026-05-29 | 10:15 | 11:15 |
| 2026-06-01 | 09:00 | 10:00 |
| 2026-06-01 | 10:15 | 11:15 |
| 2026-06-03 | 13:00 | 14:00 |
| 2026-06-05 | 09:00 | 10:00 |
| 2026-06-05 | 10:15 | 11:15 |
| 2026-06-08 | 09:00 | 10:00 |
| 2026-06-08 | 10:15 | 11:15 |
| 2026-06-10 | 13:00 | 14:00 |
| 2026-06-10 | 14:15 | 15:15 |
| 2026-06-12 | 09:00 | 10:00 |
| 2026-06-12 | 10:15 | 11:15 |
| 2026-06-15 | 09:00 | 10:00 |
| 2026-06-15 | 10:15 | 11:15 |

> **Note** : Le créneau `2026-05-24 10:15` (dernier créneau passé) n'est plus disponible — comportement attendu.

---

*Procédure v4.0 — 24 mai 2026 — Environnement de développement local uniquement*

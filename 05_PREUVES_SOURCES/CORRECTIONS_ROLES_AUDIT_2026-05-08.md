# Corrections issues de l'audit ROLES-003 — 8 mai 2026

**Référence amont** : `AUDIT_ROLES_ROUTES_2026-05-08.md` (PR #3 — branche `feat/finalisation-merlin-pilote`)
**Branche correctifs** : `fix/roles-audit-corrections-back-pay-001` (cette PR)
**Devise** : *Au sein de l'être — En actes.*

---

## 1. Résumé

Cette PR ferme les **4 actions ouvertes** par l'audit ROLES-003 du 8 mai 2026 :

| Ticket | Priorité | Description | Statut |
|---|---|---|---|
| BACK-PAY-001 | P1 (bloquant pilote payant) | Guard `require_operator` sur Stripe Checkout | ✅ corrigé |
| BACK-BOOK-001 | P2 | `cancel_slot` aligné sur `require_verified_email_user` | ✅ corrigé |
| BACK-DEPS-001 | P3 | Renommage `require_supervision_roles` → `require_supervisor` | ✅ corrigé (avec alias rétroactif) |
| BACK-AUDIO-001 | P2 | Clarification docstring `client-join` | ✅ corrigé |

Tests : **9 nouveaux tests pytest** dans `tests/test_roles_audit_corrections.py` — tous passent (9/9).

---

## 2. BACK-PAY-001 — guard sur Stripe Checkout

### Avant
```python
@router.post("/checkout/audio-async", ...)
def create_audio_async_checkout_session(
    payload: StripeAudioAsyncCheckoutCreate,
    db: Session = Depends(get_db),  # AUCUN guard d'auth
) -> StripeCheckoutSessionRead:
    _ensure_stripe_config()
    ...
```

### Après
```python
@router.post("/checkout/audio-async", ...)
def create_audio_async_checkout_session(
    payload: StripeAudioAsyncCheckoutCreate,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_operator()),  # ← guard ajouté
) -> StripeCheckoutSessionRead:
    """Crée une session Stripe Checkout pour le flux audio-async.

    Sécurité (BACK-PAY-001) : route réservée aux opérateurs internes.
    Le webhook Stripe (POST /payments/stripe/webhook) reste public — il est
    sécurisé par vérification de signature serveur (stripe-signature header).
    """
    _ = current_user  # garde appliqué par Depends
    _ensure_stripe_config()
    ...
```

### Tests (3)
- `test_anonymous_call_rejected_with_401` : appel anonyme → 401/403, plus jamais 404/200/201.
- `test_public_client_rejected_with_403` : public_client authentifié → 403 (rôle insuffisant).
- `test_operator_passes_guard_then_404_on_missing_client` : operator authentifié → atteint la logique métier, retourne 404 sur client UUID inexistant.

---

## 3. BACK-BOOK-001 — `cancel_slot` aligné

### Avant
```python
def cancel_slot(
    body: BookingCancelIn,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user),  # asymétrie avec hold/confirm
) -> BookingSlotOut:
```

### Après
```python
def cancel_slot(
    body: BookingCancelIn,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(require_verified_email_user),  # aligné
) -> BookingSlotOut:
    """Annule un créneau (hold ou confirmed).

    Sécurité (BACK-BOOK-001) : aligné sur hold/confirm — exige email vérifié.
    Autorisé : client propriétaire, praticien concerné, ou opérateur.
    """
```

### Tests (3)
- `test_anonymous_rejected` : 401.
- `test_unverified_email_rejected` : utilisateur authentifié mais email non vérifié → 401/403.
- `test_verified_user_passes_guard_then_404` : email vérifié → 404 sur slot inexistant (passe le guard).

---

## 4. BACK-DEPS-001 — renommage `require_supervisor`

### Avant
```python
def require_supervision_roles():
    return require_roles(AppRole.supervisor)
```

### Après
```python
def require_supervisor():
    """Guard réservé au rôle `supervisor` uniquement.

    Renommé depuis `require_supervision_roles` (BACK-DEPS-001) pour cohérence
    avec `require_operator` / `require_practitioner` (singulier = un seul rôle).
    """
    return require_roles(AppRole.supervisor)


# Alias rétroactif — à supprimer après migration complète des appels.
require_supervision_roles = require_supervisor
```

**Impact** : aucun changement comportemental. L'alias rétroactif évite toute rupture pour les imports externes.

### Migration effectuée
- `app/api/routes/session_notes.py` : `require_supervision_roles` → `require_supervisor` (1 import + 1 usage).

### Tests (3)
- `test_require_supervisor_exists` : helper exposé.
- `test_alias_retroactif_pointe_meme_fonction` : `require_supervision_roles is require_supervisor`.
- `test_session_notes_validate_uses_supervisor_role` : `PATCH /session-notes/{id}/validate` refuse un operator (403) — preuve que le renommage n'a pas cassé le guard.

---

## 5. BACK-AUDIO-001 — clarification `client-join`

### Avant
Pas de docstring — sémantique ambiguë (`participant_name="Client test"` mais guard `require_operator`).

### Après
Docstring complète documentant :
- Usage opérateur interne (test salle ou diffusion hors-bande au client).
- ⚠️ Avertissement : token ouvre la salle pour le client, à diffuser uniquement par canal sécurisé + journaliser.
- Évolution future : remplacer par flux client authentifié (cf. ROLES-005).

Aucun changement comportemental — uniquement documentation.

---

## 6. Tests pytest

Fichier : `10_backend_merlin_api/tests/test_roles_audit_corrections.py` (231 lignes).

```
============================= test session starts ==============================
collected 9 items

tests/test_roles_audit_corrections.py::TestBackPay001StripeCheckoutGuard::test_anonymous_call_rejected_with_401 PASSED
tests/test_roles_audit_corrections.py::TestBackPay001StripeCheckoutGuard::test_public_client_rejected_with_403 PASSED
tests/test_roles_audit_corrections.py::TestBackPay001StripeCheckoutGuard::test_operator_passes_guard_then_404_on_missing_client PASSED
tests/test_roles_audit_corrections.py::TestBackBook001CancelSlotGuard::test_anonymous_rejected PASSED
tests/test_roles_audit_corrections.py::TestBackBook001CancelSlotGuard::test_unverified_email_rejected PASSED
tests/test_roles_audit_corrections.py::TestBackBook001CancelSlotGuard::test_verified_user_passes_guard_then_404 PASSED
tests/test_roles_audit_corrections.py::TestBackDeps001SupervisorRename::test_require_supervisor_exists PASSED
tests/test_roles_audit_corrections.py::TestBackDeps001SupervisorRename::test_alias_retroactif_pointe_meme_fonction PASSED
tests/test_roles_audit_corrections.py::TestBackDeps001SupervisorRename::test_session_notes_validate_uses_supervisor_role PASSED

============================== 9 passed in 2.18s ===============================
```

---

## 7. Mise à jour suite à merger après PR #3

Une fois PR #3 mergée (qui contient la matrice + l'audit), les statuts des 4 tickets devront être mis à jour :
- `MERLIN_GOUV_MATRICE_ROLES_ROUTES_V1.md` : passer `POST /payments/stripe/checkout/audio-async` de 🚨 à ✅, `cancel_slot` de ⚠️ à ✅, et reformuler la mention `require_supervision_roles` en `require_supervisor`.
- `AUDIT_ROLES_ROUTES_2026-05-08.md` : marquer les 4 tickets comme corrigés dans la section §5.
- `MERLIN_GOUV_BACKLOG_MAITRE_V2.md` : passer **ROLES-003 de `active` à `done`** (si seule cette faille était bloquante).

Cette MAJ est volontairement différée pour ne pas créer de conflit de merge avec PR #3.

---

*Pour le peuple, par le peuple.*

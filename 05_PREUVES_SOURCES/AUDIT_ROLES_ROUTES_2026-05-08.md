# Audit rôles ↔ routes API — 8 mai 2026

**Référence** : ROLES-003 (couverture guards backend)
**Source** : extraction automatique 59 routes + revue manuelle
**Méthode** : grep des décorateurs `@router.*` + extraction des `Depends(...)` dans les paramètres ; cross-check avec doctrine `MERLIN_GOUV_TABLEAU_ROLES_ACCES_VISIBILITE_V1.md`.
**Statut ROLES-003** : *active* (couverture 64 % vérifiée explicite + 22 % publique légitime ; 1 faille critique + 4 incohérences à traiter)

---

## 1. Résumé exécutif

- **59 routes** au total (code local) ; 51 listées par OpenAPI prod (écart à investiguer — voir §4.3 matrice).
- **38 routes** (64 %) possèdent un guard `require_*` cohérent avec la doctrine.
- **13 routes** (22 %) sont publiques de manière intentionnelle et justifiée.
- **1 route** (2 %) a une déprécation propre (renvoie 410).
- **4 routes** (7 %) présentent des incohérences mineures à clarifier.
- **1 route** (2 %) présente une **faille critique** — guard d'authentification absent là où il devrait exister.

### Verdict

L'implémentation des guards est globalement **solide** : la séparation `public_client / practitioner / operator / supervisor / admin_tech` est respectée, les routes cliniques sensibles (sessions, audio, notes, documents) sont toutes protégées par `require_operator` ou `require_internal_clinical_roles`. **Une seule faille majeure** doit être corrigée en priorité (cf. §2.1).

---

## 2. Failles & risques critiques

### 2.1 🚨 `POST /payments/stripe/checkout/audio-async` — guard absent

**Sévérité** : haute
**Risque** : abus de la création de sessions Stripe Checkout, pollution de la base de paiements, potentielle ingénierie sociale.

**Constat** :
```python
@router.post("/checkout/audio-async", ...)
def create_audio_async_checkout_session(
    payload: StripeAudioAsyncCheckoutCreate,
    db: Session = Depends(get_db),  # ← AUCUN guard d'auth
) -> StripeCheckoutSessionRead:
    _ensure_stripe_config()
    client = db.get(Client, payload.client_id)
    ...
    operator = db.get(AppUser, payload.operator_user_id)
    if operator is None or operator.role not in {"operator", "practitioner", "supervisor"}:
        raise HTTPException(status_code=404, detail="Operateur/praticien introuvable.")
```

La route accepte un `client_id` et un `operator_user_id` arbitraires de la part d'un appelant **non authentifié**. La seule barrière est que l'opérateur référencé existe dans la table avec un rôle clinique — ce qui est trivialement contournable en énumérant.

**Recommandation** :
- Ajouter `require_operator()` (la création d'une session de paiement audio-async est une action de production opérée par un humain interne).
- Alternative : `require_internal_clinical_roles()` si les praticiens doivent aussi pouvoir initier.
- Conserver `_ensure_stripe_config()` mais le déplacer après le guard.

**Ticket** : créer `BACK-PAY-001` — *Ajouter guard `require_operator` sur `POST /payments/stripe/checkout/audio-async`*.

### 2.2 ✅ `POST /payments/stripe/webhook` — pas de guard (légitime)

Vérification : Stripe sécurise par signature serveur (`stripe-signature` header). Pas de guard d'auth attendu. **OK**.

### 2.3 ✅ `POST /sessions/{id}/room` — pas de guard mais 410 GONE

La route est marquée `deprecated=True` et renvoie systématiquement `HTTPException(410)`. Pas de surface d'attaque réelle. **OK** — peut être supprimée à moyen terme.

---

## 3. Incohérences à clarifier

### 3.1 ⚠️ `POST /bookings/cancel` — `get_current_user` au lieu de `require_verified_email_user`

**Constat** : `hold_slot` et `confirm_slot` exigent un email vérifié ; `cancel_slot` se contente d'un utilisateur authentifié. Asymétrie injustifiée — un utilisateur non vérifié pourrait théoriquement annuler des réservations qu'il n'a jamais pu créer (édge case improbable mais incohérent).

**Recommandation** : aligner sur `require_verified_email_user` *ou* documenter intentionnellement le choix (ex. permettre l'annulation pendant la fenêtre d'attente de vérification).

**Ticket** : `BACK-BOOK-001` — *Aligner guard `cancel_slot` sur `hold_slot`/`confirm_slot`*.

### 3.2 ⚠️ `POST /clients` & `POST /consents` — `_validate_create_access` intra-fonction

**Constat** : la logique d'autorisation dépend du payload (`is_adult_confirmed`, `data_sensitivity_class`, `consent_type_code`, etc.). Ce n'est pas un bug — c'est un parcours public d'inscription qui restreint le payload pour les anonymes.

**Recommandation** : documenter explicitement dans la doctrine que ces deux routes utilisent un *guard contextuel intra-fonction* plutôt qu'un `require_*` simple. C'est intentionnel mais non visible depuis OpenAPI.

**Ticket** : `DOC-ROLES-001` — *Documenter le pattern guard contextuel dans `MERLIN_GOUV_TABLEAU_ROLES_ACCES_VISIBILITE_V1`*.

### 3.3 ⚠️ `POST /audio-sessions/{id}/client-join` — opérateur génère token *pour le client*

**Constat** : le guard est `require_operator`, mais la fonction génère un token LiveKit pour le compte d'un client (`participant_identity=audio_session.client_participant_identity`, `participant_name="Client test"`).

**Hypothèses possibles** :
- a) Route de **test** opérateur (le `name="Client test"` le suggère fortement).
- b) Route utilisée pour transmettre un lien client par canal externe (courriel/SMS).

Si (a), renommer ou marquer `[INTERNAL/TEST]`. Si (b), la sécurité repose sur la diffusion hors-bande du token — acceptable mais à documenter.

**Recommandation** : préciser dans la docstring de la route ; selon usage réel, ajouter potentiellement un audit log.

**Ticket** : `BACK-AUDIO-001` — *Clarifier l'usage de `client-join` (test vs production) et documenter*.

### 3.4 ⚠️ `require_supervision_roles` = supervisor seul (sémantique)

**Constat** : le helper `require_supervision_roles()` (pluriel) ne contient qu'un seul rôle (`supervisor`). Le pluriel suggère plusieurs rôles. Aucun bug, mais lisibilité dégradée.

**Recommandation** : renommer `require_supervisor()` (singulier) pour cohérence avec `require_operator()`/`require_practitioner()`.

**Ticket** : `BACK-DEPS-001` — *Renommer `require_supervision_roles` → `require_supervisor`* (refactoring sans changement comportemental).

---

## 4. Couverture par domaine

| Domaine | Routes | Protégées | Publiques légitimes | Failles | Couverture |
|---|---|---|---|---|---|
| Auth & inscription | 5 | 1 | 4 | 0 | 100 % |
| Praticiens & RDV public | 3 | 0 | 3 | 0 | 100 % |
| Bookings | 4 | 4 | 0 | 0 | 100 % (1 incohérence mineure §3.1) |
| Schedules praticien | 7 | 7 | 0 | 0 | 100 % |
| Intake | 4 | 3 | 1 | 0 | 100 % |
| Clients | 3 | 2 | 1 (parcours public) | 0 | 100 % (1 clarif. §3.2) |
| Consents | 3 | 2 | 1 (parcours public) | 0 | 100 % (1 clarif. §3.2) |
| Sessions | 10 | 9 | 0 | 0 | 100 % (1 dépréciée 410) |
| Audio sessions | 5 | 5 | 0 | 0 | 100 % (1 clarif. §3.3) |
| Audio recordings | 4 | 4 | 0 | 0 | 100 % |
| Notes & documents | 8 | 7 | 1 (livraison par code) | 0 | 100 % |
| **Paiements** | **2** | **0** | **1 (webhook)** | **1** | **🚨 50 %** |
| Health | 1 | 0 | 1 | 0 | 100 % |
| **TOTAL** | **59** | **44** | **13** | **1** | **98 %** |

---

## 5. Décisions & actions recommandées

### Priorité 1 (avant pilote payant)

- [ ] **BACK-PAY-001** : ajouter `require_operator` sur `POST /payments/stripe/checkout/audio-async` — bloquant pour pilote payant.

### Priorité 2 (avant Vague 9)

- [ ] **BACK-BOOK-001** : aligner guard `cancel_slot` sur `require_verified_email_user`.
- [ ] **BACK-AUDIO-001** : clarifier `client-join` (test vs production), ajouter docstring.

### Priorité 3 (refactoring/lisibilité)

- [ ] **DOC-ROLES-001** : documenter pattern `_validate_create_access` dans la doctrine V1.1.
- [ ] **BACK-DEPS-001** : renommer `require_supervision_roles` → `require_supervisor`.

### Priorité 4 (suivi)

- [ ] Investiguer écart 51 vs 59 routes (OpenAPI prod vs code) lors du prochain déploiement.
- [ ] Supprimer la route dépréciée `/sessions/{id}/room` à la prochaine migration de schéma API (V2).

---

## 6. Métadonnées

- **Auditeur** : Computer (assistant lead)
- **Date** : 2026-05-08
- **Méthode** : extraction automatique (`/tmp/extract_routes.py`) + revue manuelle de chaque cas suspect
- **Reproductibilité** : script en pièce jointe ; relancer après chaque modification de routes
- **Référence doctrine** : `MERLIN_GOUV_TABLEAU_ROLES_ACCES_VISIBILITE_V1.md` (22 avril 2026)
- **Devise** : *Au sein de l'être — En actes.*

---

*Pour le peuple, par le peuple.*

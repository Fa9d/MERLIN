# MERLIN - Schema lien de connaissance (v1)

Date: 2026-04-18
Statut: draft
Type: schema

---

## Finalite

Un lien sert a declarer pourquoi deux objets sont relies.

---

## Champs recommandes

- `id`
- `from_id`
- `to_id`
- `link_type`
- `statement`
- `confidence`
- `source_basis`
- `status`
- `created_at`
- `notes`

---

## Types de lien recommandes

- `supports`
- `contradicts`
- `extends`
- `refines`
- `derives_from`
- `inspired_by`
- `applies_to`
- `requires_review`

---

## Exemple minimal

```yaml
id: LNK-0001
from_id: SRC-0001
to_id: ASR-0003
link_type: supports
statement: Cette source appuie partiellement l'assertion.
confidence: medium
source_basis: citation directe
status: review
created_at: 2026-04-18
notes: verification finale requise
```

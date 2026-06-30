# MERLIN - Schema pattern terrain (v1)

Date: 2026-04-19
Statut: draft
Type: schema

---

## Finalite

Ce schema sert a formaliser un pattern de terrain observe par MERLIN sans le confondre avec:
- un cas individuel;
- une doctrine stable;
- une verite populationnelle.

---

## Champs recommandes

- `id`
- `date_created`
- `label`
- `pattern_type`
- `statement`
- `scope`
- `source_basis`
- `case_count_estimate`
- `confidence`
- `status`
- `risk_of_overgeneralization`
- `possible_method_impact`
- `linked_changes`
- `review_due`
- `notes`

---

## Types recommandes

### `pattern_type`

- `needs_pattern`
- `risk_pattern`
- `orientation_pattern`
- `family_pattern`
- `youth_pattern`
- `alternative_pattern`
- `system_blockage_pattern`
- `practice_pattern`
- `population_hypothesis`

### `confidence`

- `low`
- `medium`
- `high`

### `status`

- `suspected`
- `in_review`
- `confirmed`
- `deprecated`

### `risk_of_overgeneralization`

- `low`
- `medium`
- `high`

---

## Exemple minimal

```yaml
id: pat_2026_04_19_001
date_created: 2026-04-19
label: hausse des demandes d alternatif liees a une mefiance du reseau
pattern_type: alternative_pattern
statement: Plusieurs personnes formulent une demande d alternatif moins pour des raisons de preference therapeutique que pour eviter une experience negative du reseau.
scope: clientele premiere ligne sante mentale MERLIN
source_basis:
  - cas multiples notes sur 6 semaines
  - retours operateurs
  - supervision interne
case_count_estimate: 12
confidence: medium
status: in_review
risk_of_overgeneralization: high
possible_method_impact:
  - renforcer script demande d alternatif
  - distinguer mefiance du reseau et refus de soin
linked_changes: []
review_due: 2026-05-19
notes: hypothese terrain a recroiser avec veille et donnees futures
```

---

## Regle critique

Un `pattern terrain` n'est pas une doctrine.

Il doit:
- etre revu;
- pouvoir etre contredit;
- pouvoir etre degrade;
- mentionner explicitement son risque de surgeneralisation.

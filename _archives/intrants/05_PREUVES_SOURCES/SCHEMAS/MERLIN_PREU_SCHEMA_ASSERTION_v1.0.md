# MERLIN - Schema assertion (v1)

Date: 2026-04-18
Statut: draft
Type: schema

---

## Finalite

Une assertion est un enonce de travail dans MERLIN.
Elle peut etre descriptive, theorique, normative ou inferentielle.

---

## Champs recommandes

- `id`
- `label`
- `assertion_type`
- `statement`
- `scope`
- `status`
- `confidence`
- `created_at`
- `last_reviewed_at`
- `owner`
- `notes`

---

## Types recommandes

- `fact_statement`
- `concept_statement`
- `theory_statement`
- `normative_statement`
- `inference`
- `open_question`

---

## Regle critique

Une assertion doit pouvoir etre reliee a:
- au moins une source;
- ou une observation documentee;
- ou une hypothese explicitement marquee.

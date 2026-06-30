# MERLIN - Schema source (v1)

Date: 2026-04-18
Statut: draft
Type: schema

---

## Champs recommandes

- `id`
- `title`
- `source_type`
- `origin`
- `author_or_holder`
- `people_or_tradition`
- `territory`
- `language`
- `date_or_period`
- `status`
- `evidence_level`
- `summary`
- `themes`
- `keywords`
- `notes`

---

## Types de source recommandes

- `primary_text`
- `community_source`
- `oral_transmission`
- `field_note`
- `secondary_study`
- `scientific_reference`
- `legal_reference`
- `internal_merlin_note`

---

## Exemple minimal

```yaml
id: SRC-0001
title: Exemple
source_type: community_source
origin: corpus ancestral
author_or_holder: inconnu
people_or_tradition: a definir
territory: a definir
language: fr
date_or_period: unknown
status: review
evidence_level: B
summary: Resume tres court
themes:
  - cosmologie
  - terre
keywords:
  - vivant
  - relation
```

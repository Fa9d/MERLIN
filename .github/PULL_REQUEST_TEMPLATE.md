## Quoi
<!-- une phrase -->

## Pourquoi
<!-- lien backlog / journal / décision -->

## Checklist
- [ ] CI verte (lint, unit, full-suite, gitleaks, pip-audit)
- [ ] Prompts touchés (`11_PROMPTS/**`) → version bumpée + safety evals ≥ 0.85
- [ ] Auth / paiements / données client touchés → `security-review` passée
- [ ] Périmètre §11 de CLAUDE.md touché → CLAUDE.md mis à jour dans cette PR
- [ ] Migration Alembic → `alembic upgrade head` testé + head unique vérifié
- [ ] Aucun secret, aucun fichier `.bak` / `.env` dans le diff
- [ ] Décision structurante → journal `05_JOURNAUX/`

# Index — Fiches sur les besoins de société et les comportements humains

Date de création : 2026-05-09
Statut : actif
Objet : pointage et règle de maintenance pour le bloc documentaire « besoins de société et comportements humains au Québec » consolidé en mai 2026
Mainteneur : équipe IVIA

---

## Document maître

| Code | Titre | Chemin | Lignes | Date |
|------|-------|--------|--------|------|
| **MAÎTRE** | IVIA — Synthèse maître : besoins de société et comportements humains | `IVIA_BESOINS_SOCIETE_COMPORTEMENTS_SYNTHESE_MAITRE_v1.0.md` | 357 | 2026-05-09 |

Le document maître consolide les six fiches ci-dessous en synthèse stratégique exploitable (pitch investisseurs, site public, partenariats, doctrine).

---

## Six fiches de recherche documentaire (corpus)

| Code | Titre | Chemin (relatif à `CORPUS/`) | Lignes |
|------|-------|------------------------------|--------|
| A | Détresse psychologique au Québec — prévalence 2020-2026 | `SANTE_MENTALE_PSY/SOIN__synthese__detresse-psychologique-qc-prevalence__2026-05.md` | 392 |
| B | Accès aux soins de santé mentale au QC — listes d'attente, inégalités | `SYSTEMES_SOINS_INSTITUTIONNELS/QUEBEC/SOIN__synthese__acces-soins-sante-mentale-qc__2026-05.md` | 377 |
| C | Isolement, solitude, lien social au Québec | `SANTE_MENTALE_PSY/SOIN__synthese__isolement-solitude-lien-social-qc__2026-05.md` | 468 |
| D | Comportements de recherche d'aide (help-seeking) | `SANTE_MENTALE_PSY/SOIN__synthese__comportements-recherche-aide-help-seeking__2026-05.md` | 516 |
| E | Numérique en santé mentale — marché et risques | `SANTE_MENTALE_PSY/SOIN__synthese__numerique-sante-mentale-marche-risques__2026-05.md` | 447 |
| F | Comportements humains contemporains au QC | `PENSEE_THEORIE/PENS__synthese__comportements-humains-contemporains-qc__2026-05.md` | 606 |

**Total : 2 806 lignes, environ 262 Ko de matière documentaire, plus de 100 sources primaires citées avec URLs.**

---

## Cartographie thématique

### Bloc « Portrait des besoins » (faits chiffrés)
- A — Détresse psychologique
- B — Accès aux soins
- C — Isolement et lien social

### Bloc « Comportements et trajectoires »
- D — Recherche d'aide (help-seeking)
- F — Comportements humains contemporains

### Bloc « Marché et concurrence »
- E — Numérique en santé mentale

---

## Usage selon le contexte

| Contexte | Documents prioritaires |
|----------|------------------------|
| Pitch investisseurs (problem / market size) | MAÎTRE Partie I + V, fiches A, B, E |
| Site public — page « Pourquoi IVIA » | MAÎTRE Partie I (chiffres incarnés) |
| Partenariat CIUSSS / CISSS | MAÎTRE Partie V + fiches B, D |
| Partenariat OPQ / OTSTCFQ | MAÎTRE Partie III + IV + fiche E (cadre OPQ) |
| Partenariat employeurs | Fiches A (burnout) + F (charge mentale) |
| Argumentaire doctrine | Fiche D (confirme thèse « manque de clarté avant manque d'aide ») |
| Position éthique vs IA conversationnelle | Fiche E (cas Setzer III, Replika, BetterHelp) |
| Tarification / accessibilité | Fiche B (coûts privés 120-180 $) + E (90-210 $ télésanté) |

---

## Règles de maintenance

1. **Mise à jour annuelle minimale** : à chaque parution d'un nouveau Portrait INSPQ, d'une nouvelle EQSP/ESCC/ESMAS, d'un rapport annuel MSSS, d'un rapport du Commissaire à la santé ou du VGQ. La date de prochaine révision visée : mai 2027.

2. **Mise à jour trimestrielle des sources volatiles** : tarifs psychothérapie privée (sondage OPQ), positions ordres professionnels sur l'IA, jurisprudence Loi 25, scandales/règlements du marché numérique.

3. **Versioning** : chaque mise à jour majeure d'une fiche incrémente le suffixe (`__2026-05` → `__2027-05`). Les anciennes versions sont conservées dans `ARCHIVES/`.

4. **Avant tout usage externe d'un chiffre** issu de ces fiches, recouper contre la source primaire URL. Les fiches sont des synthèses secondaires utiles pour la stratégie interne ; elles ne sont pas suffisantes seules pour citer dans un livrable contractuel ou réglementaire.

5. **Toute nouvelle fiche** sur le même thème doit être référencée dans cet index dans les 24 heures.

6. **Cas de contradiction** entre une fiche et une nouvelle donnée publique : créer une note de contradiction dans le dossier sources, ne pas modifier la fiche sans mention explicite de l'ancienne valeur.

---

## Sources primaires les plus mobilisées (top 10)

Pour faciliter le recoupage rapide :

1. [INSPQ — Surveillance santé mentale](https://www.inspq.qc.ca/sante-mentale)
2. [Institut de la statistique du Québec](https://statistique.quebec.ca/fr/sujet/sante)
3. [MSSS — Publications et rapports annuels](https://publications.msss.gouv.qc.ca/msss)
4. [Statistique Canada — Santé mentale et soins](https://www150.statcan.gc.ca/)
5. [Commissaire à la santé et au bien-être](https://www.csbe.gouv.qc.ca/)
6. [Vérificateur général du Québec](https://www.vgq.qc.ca)
7. [Ordre des psychologues du Québec](https://www.ordrepsy.qc.ca)
8. [IRIS — Recherche socioéconomique](https://iris-recherche.qc.ca)
9. [CNESST — Lésions psychologiques](https://www.cnesst.gouv.qc.ca)
10. [Recensement 2021 — Statistique Canada](https://www12.statcan.gc.ca/census-recensement/2021)

---

## Pointeurs vers documents IVIA connexes

- Charte doctrinaire v2.0 — `00_GOUVERNANCE/IVIA_CHARTE_DOCTRINAIRE_v2.0.md` (la doctrine que ces données documentent)
- Cartographie grands champs de soin v1 — `05_PREUVES_SOURCES/MERLIN_PREU_CARTOGRAPHIE_GRANDS_CHAMPS_SOINS_ACCOMPAGNEMENT_v1.0.md` (le cadre des sept champs)
- Cadre base de connaissance soins v1 — `05_PREUVES_SOURCES/MERLIN_PREU_CADRE_BASE_CONNAISSANCE_SOINS_v1.0.md`
- Bloc santé mentale psychosocial QC v1 — `CORPUS/SANTE_MENTALE_PSY/SOIN__perplexity__bloc-sante-mentale-psychosocial-qc-synthese-secondaire__2026-04-19.md` (le précurseur de cette série)
- Pitch deck investisseurs — `pitch_deck_investisseurs` (à enrichir avec les chiffres extraits)
- Plan financement v2 — `bp_financement_v2`
- Note confidentielle investisseurs — `note_confidentielle_investisseurs`

---

*Index produit dans la phase de consolidation documentaire pré-pilote praticien — mai 2026.*
*Pour le peuple, par le peuple.*

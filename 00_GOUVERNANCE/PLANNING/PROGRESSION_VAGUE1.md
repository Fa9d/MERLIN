# Progression Vague 1 — IVIA Base Documentaire

**Statut** : TERMINÉ
**Dernière mise à jour** : Mai 2026

## Documents complétés

- [✅] CHARTE_DOCTRINAIRE_IVIA.md (505 lignes, 5 075 mots — 7 principes détaillés avec exemples, règles Blocs A&B, doctrine monétisation C.1, gouvernance Comité doctrinal, audit annuel, non-cession données F, statuts protecteurs G)
- [✅] STRUCTURE_JURIDIQUE_RECOMMANDEE.md (426 lignes, 3 389 mots — 4 options analysées, recommandation hybride OBNL+SPA motivée, schéma gouvernance, calendrier 6-8 semaines, coûts 11-21 K$, implications levée de fonds)
- [✅] CHARTE_TRANSFORMATION_GOUVERNEE_DONNEES.md (381 lignes, 3 323 mots — définitions Loi 25/RGPD, pipeline 8 étapes détaillé, consentement granulaire 3 niveaux, droits clients/praticiens, charte cession, audit annuel)
- [✅] BP_FINANCEMENT_V2.md (655 lignes, 5 228 mots — sections A à S complètes, structure hybride intégrée, multi-strates documenté, P&L estimé, scénarios sensibilité, mix financement 70/30, rémunération fondateur explicite)
- [✅] PLAN_FINANCEMENT_DETAILLE.md (412 lignes, 3 155 mots — décomposition par palier P1-P6, sources ciblées détaillées avec probabilités et délais, calendrier décaissement trimestriel, conditions/contreparties, Plans A/B/C)
- [✅] POLITIQUE_CONFIDENTIALITE_LOI25.md (447 lignes, 3 108 mots — catégories données, finalités, consentement granulaire, durées conservation, droits personnes, sécurité, sous-traitants, transferts hors QC, RPRP, incident, EFVP, mineurs)
- [✅] NOTE_CONFIDENTIELLE_INVESTISSEURS.md (350 lignes, 2 541 mots — avertissement, résumé exécutif, TAM multi-strates, moat 3 actifs, équipe, paliers, chiffres clés, conditions levée, valorisation 600 K$ pré-money)
- [✅] PITCH_DECK_INVESTISSEURS.md (457 lignes, 3 014 mots — 20 slides complets avec titre + bullets + notes conférencier, instructions mise en forme PowerPoint)

## Totaux Vague 1

- **Lignes totales** : 3 633
- **Mots totaux** : 28 833
- **Taille totale** : ~183 Ko

## Notes d'attention soulevées pendant la production

1. **Constitution structure hybride — avocat spécialisé obligatoire** : La rédaction des droits de veto anti-dilution de l'OBNL sur MERLIN inc. est critique. Un avocat commercial ordinaire pourrait produire des statuts techniquement corrects mais insuffisamment protecteurs. Un cabinet avec expérience documentée en gouvernance d'organisations à mission sociale (coopératives, économie sociale) est requis.

2. **Strate 4 — ligne non-commission à cadrer contractuellement** : La distinction entre "frais de mise en avant dans l'annuaire" et "commission déguisée" devra être définie avec précision dans le contrat d'inscription S4. La règle A.2 de la Charte doctrinaire est claire, mais l'application pratique nécessitera des clauses contractuelles spécifiques.

3. **RS&DE — documentation dès le Jour 1** : Le crédit RS&DE représente 50-150 K$ de financement non-dilutif sur 36 mois. Il requiert une documentation rigoureuse des activités de R&D dès le premier jour de développement du pipeline. Recruter un consultant RS&DE dès le Palier 2 est rentable.

4. **MRR M36 — sensibilité à l'adoption de la Strate 3** : L'ARR 1,86 M$ à M36 dépend significativement de l'adoption par 80-150 praticiens soins corporels (Strate 3) d'ici M27. Un retard de 3-6 mois sur S2 repousse S3 proportionnellement. Le scénario bas (1,2 M$ ARR, Plan B) reste viable mais compromet le modèle propriétaire.

5. **Effacement audio J+30 — process certifié obligatoire** : L'engagement "voix effacée à J+30" est la garantie centrale du pipeline. Ce process doit être techniquement irréversible (overwrite sécurisé), automatisé (cron certifié), journalisé et auditable. Sa défaillance serait un incident de conformité grave et un risque doctrinal majeur.

## Incohérences identifiées dans le corpus existant

1. **Tension BP V1.1 Palier 6 vs décision structurante** : Le plan 36 mois indique Strate 4 à M28-M36, la décision structurante la retarde à M30. La raison (maturité dataset synthétique 5 000+ cas requise) est maintenant documentée dans le BP V2. Cohérence restaurée.

2. **Rémunération fondateur absente du BP V1.1** : La Section D du BP V1.1 liste "Rémunération fondateur" comme case à remplir ([ ]) sans montant. La décision 75-90 K$/an est maintenant explicite dans le BP V2 et le Plan de financement. Cohérence restaurée.

3. **Mix financement non spécifié dans V1.1** : Le BP V1.1 mentionne plusieurs sources potentielles mais sans le ratio 70/30 ni la règle "pas de BDC avant Palier 4". Ces décisions structurantes sont maintenant documentées dans le BP V2 et le Plan financement.

4. **Simulation économique V2 vs grille tarifaire V1** : La simulation V2 (MERLIN_GOUV_SIMULATION_ECO_COUTS_REELS_V2.md) utilise "Stripe à la charge du praticien" alors que le BP V1.1 a tranché "MERLIN collecte le paiement". Ces deux documents donnent des coûts variables différents. Le BP V2 suit l'arbitrage V1.1 (MERLIN collecte), qui est la décision tranchée.

5. **Grille commerciale V1 vs BP V1.1** : La grille commerciale V1 ne prend pas encore en compte la structure 3×3 (plan × palier volume) qui a été décidée dans le BP V1.1. Les deux grilles coexistent dans le corpus — la grille V1 représente l'état antérieur à l'arbitrage.

## Recommandations pour la Vague 2 (Ordre 2 — 10 documents structurels)

### Priorités absolues

1. **Contrats praticiens (template)** : accord praticien IVIA Cœur incluant clause doctrinaire, droits/obligations, formation minimale requise, conditions de résiliation

2. **CGU et conditions générales de service** : pour clients et praticiens — avec intégration de la Charte doctrinaire et de la politique de confidentialité

3. **Manuel de formation doctrine minimale praticiens** : niveau 2 obligatoire (ce que MERLIN fait/ne fait pas, drapeaux rouges, règles de consentement, limites d'exercice)

4. **Cahier des charges technique pipeline** : spécifications détaillées des 8 étapes pour le développement (tickets backlog BACK-011+)

5. **Modèle de dossier de candidature subventions** : template pour PSCSE PME MTL, Fondation Chagnon, IQ — à adapter par source

### Priorités importantes

6. **Politique d'annulation et de remboursement** : protocole clients + praticiens

7. **Protocole de gestion des situations d'urgence** : que fait le praticien si un client exprime des pensées suicidaires ou de détresse sévère ?

8. **Plan de communication et de marketing** : positionnement S1, messages clés, canaux

9. **Grille d'évaluation et d'onboarding des praticiens** : critères de sélection, processus d'intégration

10. **Rapport type d'audit annuel** : template pour le premier audit doctrinaire (prévu fin 2027)

# Deck investisseurs IVIA / MERLIN

## 1. Couverture
- Nom du projet : IVIA / MERLIN / MÉSANGES
- Stade : Pré-seed (proto fonctionnel, module méthodo avancé)
- Localisation : Montréal / Longueuil, QC

## 2. Problème & tension
- Fragmentation des suivis, surcharge documentaire, manque de contextualisation (environnement, langue, culture).
- Praticiens : temps administratif élevé, outils non adaptés aux parcours complexes.
- Personnes : parcours éclatés, absence de fil conducteur entre consultations, programmes et outils numériques.

## 3. Solutions actuelles et limites
- Dossiers cliniques / EMR : centrés sur facturation et médical, peu sur vécu et contexte relationnel.
- Apps bien-être grand public : éloignées des praticiens, peu structurantes et rarement francophones.
- Outils génériques (notes, CRM) : ne portent pas de modèles comportementaux ni d’ancrage culturel ou territorial.

## 4. Vision IVIA
- Mission : donner aux personnes et aux praticiens un fil structurant, ancré dans leur environnement, pour comprendre et agir sur la santé mentale.
- IVIA accueille, MERLIN structure, MÉSANGES accompagne.
- Articuler le vivant (RGNR), les savoirs autochtones et la médecine moderne dans une même maison numérique.

## 5. Solution – architecture produit
- IVIA.quebec : maison commune, interface web pour personnes et praticiens.
- MERLIN : moteur FastAPI (sessions, notes structurées, modèles comportementaux, audio).
- MÉSANGES : interface vocale (LiveKit, Deepgram) pour accueil, guidage et accompagnement.
- Stack : OVH Canada, PostgreSQL, Redis, S3, GPT/Claude, Stripe, analytics, etc.

## 6. Produit – snapshot fonctionnel
- MERLIN : endpoints pour créer des séances, ouvrir des salles LiveKit, démarrer/arrêter l’enregistrement, valider des notes de séance.
- IVIA.quebec : pages de comptes clients/praticiens, parcours de rendez-vous, interface unifiée.
- Module modèles comportementaux : environ 20 modèles, classés par strates et IPM (Big Five, Leary, etc.).

## 7. Marché & opportunité
- Marché digital mental health / behavioral health : fort besoin de structuration des suivis, pression sur les praticiens.
- Sous-segment francophone / Québec + savoirs autochtones : largement sous-servi par les outils actuels.
- Cibles initiales : praticiens indépendants, petites cliniques, organismes communautaires et programmes de santé mentale.

## 8. Modèle économique
- SaaS B2B / B2B2C : abonnement par praticien ou par organisation.
- Modules additionnels : voix (MÉSANGES), modèles avancés, rapports analytiques MERLIN.
- Logique de valeur : réduction du temps administratif, meilleure continuité des parcours, profondeur documentaire et analytique.

## 9. Traction & état actuel
- Backend MERLIN : migrations Alembic, endpoints sessions / LiveKit / notes de séance déjà en place.
- Site IVIA.quebec : branche refonte, pages comptes et rendez-vous développées.
- Dossiers : IVIA_STRATEGIE_TECHNOLOGIQUE, ANALYSE_STACK_OUTILS, MERLIN_modeles_comportementaux, corpus RGNR.

## 10. Go-to-market & pilotes
- Phase 1 (0–6 mois) : 3–5 praticiens, 1–2 organismes communautaires, pilotes en conditions réelles au Québec.
- Phase 2 (6–12 mois) : stabilisation produit, création de templates de parcours, premiers contrats B2B.
- Phase 3 (12–24 mois) : extension à d’autres régions francophones, partenariats avec programmes de santé mentale.

## 11. Impact & posture santé
- Impact praticiens : baisse du temps administratif, meilleure structuration et continuité.
- Impact personnes : parcours plus lisibles, ancrés dans leur environnement et leur culture.
- Posture santé : prudence sur médication, aucun diagnostic automatique, travail avec des professionnels et respect des cadres de protection des données.

## 12. Équipe
- Fondateur : profil dev full-stack, linguistique/computational linguistics, documentation-first, immersion dans santé mentale et savoirs autochtones.
- Besoins futurs : produit, clinique, data/AI, partenariats communautaires.

## 13. Besoin & usage des fonds
- Montant visé (pré-seed) : à préciser selon stratégie.
- Usage : produit/tech, pilotes/partenariats, conformité/infra, premières embauches.
- Objectifs avec ce tour : pilotes signés, premiers clients payants, version 1.0 stable, MRR initial.
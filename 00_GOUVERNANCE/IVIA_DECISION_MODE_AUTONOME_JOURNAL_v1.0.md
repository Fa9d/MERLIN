# IVIA — Décision fondateur : mode autonome du journal (amendement constitutionnel)

**Version** : v1.0 — 2026-07-09
**Statut** : canon — décision fondateur actée en session du 2026-07-09
**Décideur** : David Phaneuf (fondateur)
**Références** : CLAUDE.md §6.4 (constitution), §16 (« toute sortie IA est soumise
à validation humaine avant archivage ») ; `11_PROMPTS/07_analyses/PROMPT_reflet_
journal_client_v1.md` (PROD-ANA-004) ; `app/services/journal_reflection.py`.

---

## La décision

1. **Le client autonome est un état normal d'IVIA.** Une personne peut utiliser
   le journal — et sa puissance d'analyse — sans praticien, dans un espace
   complètement intime. `clients.praticien_id` est nullable : NULL = autonome.

2. **Le « reflet de journal » est la première sortie IA→client sans relecture
   praticien.** Pour cette surface UNIQUEMENT, la règle « validation humaine
   par restitution » est remplacée par un **triple verrou technique** :
   - safety suite dédiée `journal_client_safety_suite_v1` ≥ 0.90, re-run
     obligatoire à chaque bump du prompt (§8.3) ;
   - filtre lexical Loi 21 **en code** sur toute la voix du reflet — un mot
     interdit et rien ne sort ;
   - **protocole d'urgence en code** : signal détecté → ressources de crise
     (9-8-8, 8-1-1 opt. 2, 9-1-1) injectées par le serveur (jamais dépendantes
     du seul modèle), analyse neutralisée (pas de fils, pas de piste), reflet
     réduit à la présence.

3. **La relation praticien reste souveraine quand elle existe.** Le lien
   client→praticien est durable (`clients.praticien_id`) ; les séances gardent
   leur praticien historique. Changement de praticien : mode **resume** par
   défaut (le fil visible seulement — la parole confiée ne voyage pas sans son
   auteur) ; mode **integral** sous consentement explicite du client, tracé
   (`client_practitioner_transfers`).

4. **Rattachement au besoin** : un client autonome qui choisit un praticien
   garde la main — `consent_history` gouverne ce que ce praticien voit du
   journal passé. Rien n'est automatique.

## Garde-fous additionnels du reflet

- Cadence : un reflet par 20 h (rythme sain + maîtrise du coût).
- Fenêtre : 21 jours d'écriture, 40 entrées max.
- Interrupteurs : `MERLIN_INSIGHTS_ENABLED` (global) + capacité
  `journal_reflet_client` (un clic admin, Atelier des lectures).
- Le reflet ne mentionne jamais de praticien sauf si les écrits en parlent ;
  jamais de « tu devrais » ; l'autonomie de la personne est la boussole.

## Perspective produit (à cadrer séparément)

Ce mode ouvre la voie à une **application indépendante** (journal intime +
reflets, sous une autre marque) sur la même API. Décisions restantes avant
tout lancement : nom, tarification, périmètre embarqué, hébergement des
comptes. Aucun engagement pris ici.

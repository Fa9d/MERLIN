# IVIA — Parcours vivant de A à Z

**Version** : v0.1 — 2026-06-11 — **statut : PROPOSITION** (à amender par le fondateur)
**Principe** : *dense en analyse, évident en compte rendu* — nous simplifions aux gens des
situations complexes. Toute la densité (axes, tensions, signaux, gap Y→Z) vit côté moteur
et praticien ; la personne ne reçoit que de la clarté.

---

## 1. Le parcours en neuf temps

| # | Temps | Surface | État |
|---|-------|---------|------|
| A | Arriver (`index`) → comprendre les 4 voies | site public | ✅ en ligne |
| B | Créer son espace (`inscription`) → courriel de confirmation 48 h | site + `/register/client` | ✅ câblé |
| C | Confirmer (`verify-email`) → se connecter (`connexion`, JWT) | site + `/auth/login` | ✅ câblé |
| D | Réserver (`reserver`) : praticien → créneau → hold 15 min → payer (Stripe, prix serveur) ou pilote offert | `/bookings/*` | ✅ câblé |
| E | **Habiter son espace** (`client/dashboard`) : prochaine séance, journal, carte de vie | `/clients/me`, `/bookings/my`, `/me/journal` | 🔧 ce sprint |
| F | **Écrire** (`client/journal`) : entrées datées, ton émotionnel, ancrage à une année | `/me/journal` | 🔧 ce sprint |
| G | **Vivre la séance** (`client/seance-active`) : salle d'attente, enregistrement local consenti, notes horodatées | LiveKit + `upload_session_audio` | ✅ v1 (consentements séance à finaliser) |
| H | **Recevoir** : transcription (faster-whisper local) → note Cercle (METH-003) → validation praticien → compte rendu client doux | pipeline + `derived-documents` | ✅ moteur / 🔜 surface client |
| I | **Voir son chemin** (`client/carte-de-vie`) : lecture douce de la Carte de Vie | référentiels + composition | 🔜 sprint suivant |

## 2. Le modèle de représentation — une seule source, trois rendus

**La Carte de Vie est l'objet pivot.** On ne crée pas un modèle « dashboard » de plus :
chaque surface est une *lecture* de la même composition (spec `CARTE_DE_VIE_modele_v0.1.md` §4).

```
Sources (déjà migrées)                 Composition                  Lectures
SessionNote (axes, tensions,    →  GET /clients/{id}/carte-de-vie  →  client     : douce
  signaux, vigilance)               (à construire — endpoint           praticien  : dense
ClientLifeEvent + anchors           de composition, strate             observatoire: agrégats
ClientJournalEntry                  par strate, jamais de copie)       anonymisés (Loi 25)
EraContext · referentiels YAML
```

**Règles de traduction dense → évident (lecture client)** :
- jamais de codes ni de scores : `tension_charge_exigences (marquee, 0.7)` devient
  « *Vous portez beaucoup, depuis longtemps. C'est un endroit où regarder ensemble.* » ;
- vocabulaire du lexique vivant uniquement (Loi 21 : ni diagnostic ni trouble) ;
- triade Observation → Hypothèse → Orientation sur tout compte rendu ;
- signaux METH et niveaux de confiance : **praticien seulement** ;
- le client voit *son mouvement* (journal, séances, horizon), pas *son évaluation*.

## 3. Écarts à combler (constatés sur le code)

1. **`GET /clients/{id}/carte-de-vie` n'existe pas** — l'endpoint de composition est la
   pièce maîtresse manquante. Tout le reste s'y branche.
2. **`/clients/{id}/life-events` est réservé aux rôles cliniques** : le client ne peut ni
   voir ni nourrir sa propre ligne de vie. Décision à prendre : route `/me/life-events`
   (lecture + ajout doux), cohérente avec `/me/journal`.
3. **Compte rendu client** : `DerivedDocument` existe, mais aucune page client ne le rend.
   → page « Mes séances » : chaque séance close affiche son compte rendu validé (et rien
   d'autre — pas de note praticien).
4. **Dashboard praticien** : déjà partiellement réel (agenda) ; la lecture dense de la
   Carte de Vie (démo actuelle) doit se brancher sur la composition (même endpoint, rendu complet).
5. **Consentements de séance** (`consent_recording`, `consent_transcription`) : à capturer
   au moment G, jamais à l'inscription (règle CLAUDE.md §16).

## 4. Ordre de réalisation proposé

1. **Sprint courant** : dashboard client réel + journal réel (E, F) — fait dans la PR de ce doc.
2. `/me/life-events` + endpoint de composition `carte-de-vie` (lectures client/praticien servies).
3. Page « Mes séances » avec comptes rendus (H côté client) + consentements de séance (G).
4. Carte de Vie client douce (I) + bascule de la démo praticien sur la composition réelle.
5. Lecture observatoire (agrégats anonymisés) — après safety evals dédiées.

> Chaque étape doit passer la safety suite avant toute sortie client (CLAUDE.md §8).

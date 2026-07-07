# JOURNAL — Veille concurrentielle et intégrations doctrinales — 2026-07-07

Référence les journaux précédents : `JOURNAL_alignement-doctrinal-pages_20260706.md`.

## Contexte

Analyse de deux produits concurrents à la demande du fondateur :
1. **happilyloneliness.org** (« Happily Alone ») — guide numérique + parcours 30 jours sur la solitude, 29,90 $US.
2. **app.culturallogicsystems.com** (« Viora ») — évaluation de vie 12 domaines + 8 archétypes + protocoles 30/90 jours, freemium 19–49 $A/mois. Analyse faite via le code public de l'application (contenu embarqué en clair dans le JS).

## Constats de veille (résumé)

- Ces produits monétisent l'accompagnement intérieur **sans humain dans la boucle** et **sans mention d'urgence/détresse** — c'est le contre-modèle d'IVIA.
- Viora utilise un pixel Meta sur une application de bien-être mental (impensable sous Loi 25) et adapte ton et interface selon un profilage non consenti.
- Leurs meilleures idées rhétoriques sont transposables **si filtrées par la doctrine** : retournement doux, anti-étiquetage, entonnoir gratuit d'orientation.

## Décisions et intégrations (ce jour)

### 1. Lexique vivant v0.2 → v0.3
Ajout d'une section `principes_transversaux` :
- **saison-pas-verdict** — toute restitution décrit un moment, jamais une identité. Formulations autorisées/interdites incluses.
- **retournement-doux** — valider ce que la personne porte, puis retourner la question vers son besoin. Garde-fous : jamais culpabilisant, la porte n'impose pas d'être franchie.

⚠️ Règle du lexique : toute modification de wording nécessite **relecture humaine** — à valider par David.

### 2. Pages d'atterrissage — accroches-retournement
- `/proche` : « Tu prends soin de tout le monde. Qui prend soin de toi ? » (remplace « Et toi, dans tout ça ? »)
- `/travail` : « Tu tiens tout à bout de bras. Qui te tient, toi ? »
- `/attente` : « Tu attends qu'on s'occupe de toi. Et si tu commençais sans attendre ? »
- `/ecoute` : « Fonctionner, ce n'est pas la même chose que vivre. » + phrase saison-pas-verdict ajoutée à la triade publique.

### 3. Refusé (contraire à la doctrine)
- Archétypes/étiquettes publiques, score de vie chiffré, adaptation d'interface par profilage non consenti, rareté fabriquée (prix fondateur « à vie »), pixel Meta sans consentement.

## Chantiers ouverts (todos session)
- `questionnaire-orientation` — page publique « Où en es-tu ? » : 5-6 questions en langage du lexique, orientation vers la bonne page/formule **et un humain**, triade en acte, aucun score.
- `ton-par-pattern` — consigne de ton par correspondance vivante dans les prompts MERLIN (bump versions + safety suite).

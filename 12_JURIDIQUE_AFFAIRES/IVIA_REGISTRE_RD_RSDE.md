# REGISTRE R&D — Traçabilité RS&DE / CRIC
**Ouvert le** : 6 juillet 2026
**But** : documenter les heures et dépenses de R&D admissibles aux crédits d'impôt
RS&DE (fédéral, 35 % remboursable) et CRIC (Québec, 30 % première tranche).
La rétroactivité est possible après l'incorporation d'IVIA inc. — d'où l'importance
de tenir ce registre DÈS MAINTENANT, chaque semaine.

## Règles de tenue

- Une ligne par semaine minimum ; par projet si possible.
- Décrire l'**incertitude technologique** (ce qu'on ne savait pas faire) et
  l'**avancement** (ce qu'on a appris/résolu) — c'est le langage RS&DE.
- Conserver les preuves : messages de validation (commits Git = horodatage parfait),
  factures (hébergement, API IA, outillage).
- 15 minutes par semaine suffisent.

## Projets R&D admissibles en cours

| Code | Projet | Incertitude technologique |
|---|---|---|
| RD-01 | Transcription locale souveraine (faster-whisper) | Qualité/performance de la transcription française québécoise sur serveur modeste sans exposition des données |
| RD-02 | Moteur d'analyse à vannes par profil | Architecture séparant capacité analytique maximale et exposition légale contrôlée (Loi 25/21) — sans précédent connu |
| RD-03 | Analyse prosodique locale (librosa) | Extraction de marqueurs prosodiques fiables (pauses, F0, énergie) sur audio de séance réel, compressé webm/opus |
| RD-04 | Chaîne documentaire gouvernée | Pipeline consentement → analyse → validation humaine → livraison, avec journalisation d'accès opposable |
| RD-05 | Indicateur de temporalité décalée | Méthode d'analyse temporelle des récits (prior art GitHub a2d493c, 9 mai 2026) |

## Journal des travaux (ajouter chaque semaine EN HAUT)

### Semaine du 30 juin au 6 juillet 2026
- **Projets** : RD-02, RD-03
- **Heures fondateur** : ~40 h (estimation à affiner)
- **Travaux** : conception et implémentation du moteur plein / vannes par profil
  (modèles de données, service de filtrage par sensibilité, journalisation des accès) ;
  analyse prosodique locale librosa (F0 pyin, ratio de pauses, énergie RMS) intégrée
  au conteneur de production avec ffmpeg pour décodage webm/opus.
- **Incertitudes résolues** : filtrage à la lecture (et non à la production) permettant
  la capacité maximale sans exposition ; performance librosa acceptable en conteneur.
- **Preuves** : commits 30652ac, 2c69496 (dépôt Fa9d/MERLIN).

### Gabarit de semaine (copier-coller)
### Semaine du JJ au JJ mois AAAA
- **Projets** :
- **Heures fondateur** :
- **Travaux** :
- **Incertitudes résolues / rencontrées** :
- **Preuves** (commits, factures) :

## Dépenses R&D (cumul depuis le 6 juillet 2026)

| Date | Fournisseur | Description | Montant | Projet |
|---|---|---|---|---|
| (récurrent) | OVH | VPS production (part R&D estimée 50 %) | ~xx $/mois | Tous |
| (récurrent) | Anthropic | API Claude (analyses) | variable | RD-02/04 |
| | | | | |

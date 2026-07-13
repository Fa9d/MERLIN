# Architecture IVIA / MERLIN

## Vue d'ensemble

```
┌─────────────────────────────────────┐
│         IVIA.quebec (frontend)      │
│  Site public + interface praticien  │
└───────────────┬─────────────────────┘
                │ HTTP / WebSocket
┌───────────────▼─────────────────────┐
│         MERLIN (FastAPI backend)    │
│                                     │
│  ┌─────────────────────────────┐    │
│  │  Routes                     │    │
│  │  /sessions   /notes         │    │
│  │  /audio      /validation    │    │
│  │  /comptes    /praticiens    │    │
│  └────────────┬────────────────┘    │
│               │                     │
│  ┌────────────▼────────────────┐    │
│  │  Modules métier             │    │
│  │  comportementaux/           │    │
│  │  analyse/                   │    │
│  │  contexte/                  │    │
│  └────────────┬────────────────┘    │
│               │                     │
│  ┌────────────▼────────────────┐    │
│  │  Schémas Pydantic           │    │
│  │  schemas/                   │    │
│  └─────────────────────────────┘    │
└───────────────┬─────────────────────┘
                │
┌───────────────▼─────────────────────┐
│         MÉSANGES (LiveKit)          │
│  Interface vocale + enregistrement  │
└─────────────────────────────────────┘
```

---

## Flux principaux

### Flux 1 — Création de séance
```
Praticien → POST /sessions/create
         → MERLIN crée la séance
         → Retourne session_id + room_url (LiveKit)
         → Praticien et patient rejoignent la salle
```

### Flux 2 — Enregistrement et notes
```
Séance active → MÉSANGES capte l'audio
             → Transcription en cours
             → POST /notes/draft (brouillon en temps réel)
             → Fin de séance → POST /notes/validate
             → Note structurée disponible pour le praticien
```

### Flux 3 — Analyse comportementale
```
Note validée → GET /analyse/{session_id}
            → MERLIN applique les modèles comportementaux
            → Retourne les patterns identifiés
            → Stockés dans le profil de suivi
```

### Flux 4 — Consultation du suivi
```
Praticien → GET /suivi/{patient_id}
          → MERLIN agrège les séances précédentes
          → Retourne la vue longitudinale
          → Praticien voit l'évolution du patient
```

---

## Modèles comportementaux

Situés dans `/modules/comportementaux/`.

Organisés en strates :
- **Strate 1** — Contexte environnemental (lieu, langue, culture)
- **Strate 2** — Patterns comportementaux observés en séance
- **Strate 3** — Indicateurs longitudinaux (évolution sur plusieurs séances)
- **Strate 4** — Signaux d'alerte (patterns préoccupants à signaler)

Chaque modèle expose :
- `analyse(session_data)` → résultat structuré
- `schema_entree` → Pydantic model attendu
- `schema_sortie` → Pydantic model retourné

---

## Schémas clés

### Session
```python
class SessionCreate(BaseModel):
    praticien_id: str
    patient_id: str
    type_seance: str  # "individuel" | "groupe" | "évaluation"
    contexte: dict    # informations contextuelles optionnelles

class SessionResponse(BaseModel):
    session_id: str
    room_url: str
    created_at: datetime
    statut: str  # "en_attente" | "active" | "terminée"
```

### Note
```python
class NoteDraft(BaseModel):
    session_id: str
    contenu_brut: str
    timestamp: datetime

class NoteValidee(BaseModel):
    session_id: str
    contenu_structure: dict
    modeles_appliques: list[str]
    validated_at: datetime
    praticien_id: str
```

---

## Règles d'architecture

- **Un seul point d'entrée** : `main.py`
- **Séparation stricte** : routes → services → modules métier → schémas
- **Pas de logique métier dans les routes** : les routes orchestrent, les modules calculent
- **Chaque module est testable indépendamment**
- **Les modèles comportementaux ne lisent pas la base de données directement** : ils reçoivent des données structurées

---

## Dépendances externes

| Service | Usage | Notes |
|---|---|---|
| LiveKit | Audio/vidéo en temps réel | Clés dans `.env` |
| PostgreSQL | Stockage principal | Connexion via SQLAlchemy |
| (à définir) | Transcription audio | Whisper local ou API externe |

---

## Variables d'environnement requises

```env
LIVEKIT_URL=...
LIVEKIT_API_KEY=...
LIVEKIT_API_SECRET=...
DATABASE_URL=postgresql://...
SECRET_KEY=...
ENVIRONMENT=development  # ou production
```

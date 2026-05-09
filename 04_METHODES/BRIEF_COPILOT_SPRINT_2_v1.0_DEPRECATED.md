# Brief Copilot — Sprint 2 IVIA (vague 9)

**Date** : 9 mai 2026
**Contexte** : production déployée OVH `ivia.quebec` + `api.ivia.quebec` (FastAPI + Next.js 16)
**Mode** : pilote — David seul praticien, voix pilotes 6 personas fictifs
**Devise** : *Au sein de l'être — En actes.*

---

## Objectif Sprint 2

Refondre `/praticiens` (page liste) et brancher le funnel quiz `/demarche` au matching backend, en respectant la doctrine carte abstraite (zéro visage, voix + texture + couleur). Intégrer les 6 voix pilotes enregistrées par David.

---

## Sources de vérité (à lire AVANT de coder)

1. `00_DOCTRINE/IVIA_DOCTRINE_CARTE_ABSTRAITE_v1.0.md` — règles strictes anti-visage
2. `04_METHODES/IVIA_SPEC_PAGE_PRATICIENS_v2.0.md` — spec UI page liste 1012 lignes
3. `04_METHODES/IVIA_FUNNEL_QUIZ_TO_GUIDANCE_v1.2_ADDENDUM.md` — alignement écran 8 cartes
4. `04_METHODES/IVIA_FUNNEL_QUIZ_TO_GUIDANCE_v1.1.md` — funnel complet 8 écrans
5. `ivia_mockups/assets/voix_pilote/README.md` — mapping voix ↔ personas
6. `10_backend_merlin_api/app/models/app_user.py` — schéma BD existant

---

## TODO — ordre d'exécution strict

### Phase A — Backend : enrichir le modèle praticien (1h)

**Fichier** : `10_backend_merlin_api/app/models/app_user.py`

Champs déjà présents (NE PAS RECRÉER) :
- `display_name`, `title_line`, `intro_text`, `presentation_audio_url`
- `spoken_languages` (JSON array string), `available_channels` (JSON array string)
- `is_publicly_listed`, `role`, `record_status`

**Champs à AJOUTER** (carte abstraite) :
```python
# Doctrine carte abstraite — palette + texture + voix
abstract_palette: Mapped[str | None] = mapped_column(String(64), nullable=True)
# Valeurs: "vert_sauge", "ocre_doux", "ardoise", "lin", "argile", "ambre"

abstract_texture: Mapped[str | None] = mapped_column(String(64), nullable=True)
# Valeurs: "ondulation", "grain_papier", "souffle", "veinure", "halo", "trame"

abstract_motif: Mapped[str | None] = mapped_column(String(64), nullable=True)
# Valeurs: "cercle", "ligne_horizon", "spirale_ouverte", "vague", "feuille", "pierre"

# Modalités d'écoute (Mésange)
listening_modalities: Mapped[str | None] = mapped_column(Text, nullable=True)
# JSON array: ["corps_silence", "mots_structure", "frequence_vibration",
#              "contemplation_ancrage", "energie_mouvement", "deuil_transition"]

# Disponibilité phase pilote
pilot_persona_label: Mapped[str | None] = mapped_column(String(64), nullable=True)
# Pour les 6 personas fictifs pilote : "voix_pilote_01" à "voix_pilote_06"
```

**Migration Alembic** :
```bash
cd 10_backend_merlin_api
alembic revision --autogenerate -m "praticien carte abstraite + modalites ecoute"
# Vérifier le fichier généré, puis :
alembic upgrade head
```

**Schema FastAPI** (`10_backend_merlin_api/app/schemas/auth.py`) — étendre `PraticienPublic` :
```python
class PraticienPublic(MerlinSchema):
    id: str
    display_name: str
    title_line: str | None
    intro_text: str | None
    spoken_languages: str | None
    available_channels: str | None
    # Doctrine carte abstraite
    abstract_palette: str | None
    abstract_texture: str | None
    abstract_motif: str | None
    listening_modalities: str | None
    presentation_audio_url: str | None
    pilot_persona_label: str | None
```

---

### Phase B — Backend : seed des 6 personas pilotes (30 min)

**Nouveau fichier** : `10_backend_merlin_api/scripts/seed_pilot_personas.py`

Crée 6 `AppUser` avec `role=practitioner`, `is_publicly_listed=True`, `email_verified=True`,
mots de passe random non-utilisables (compte fictif, pas de login). Mapping :

| `pilot_persona_label` | `display_name` | `title_line` | `presentation_audio_url` | `listening_modalities` | `abstract_palette` / `texture` / `motif` |
|---|---|---|---|---|---|
| `voix_pilote_01` | Aëlis | Présence corps & silence | `/assets/voix_pilote/voix_01_presence_corporelle.mp3` | `["corps_silence"]` | `vert_sauge` / `souffle` / `pierre` |
| `voix_pilote_02` | Naël | Parole & clarté | `/assets/voix_pilote/voix_02_mots_structure.mp3` | `["mots_structure"]` | `ardoise` / `grain_papier` / `ligne_horizon` |
| `voix_pilote_03` | Sève | Fréquence & vibration | `/assets/voix_pilote/voix_03_frequence_vibration.mp3` | `["frequence_vibration"]` | `lin` / `ondulation` / `vague` |
| `voix_pilote_04` | Telma | Contemplation & ancrage | `/assets/voix_pilote/voix_04_contemplation_ancrage.mp3` | `["contemplation_ancrage"]` | `argile` / `veinure` / `cercle` |
| `voix_pilote_05` | Nori | Énergie & mouvement | `/assets/voix_pilote/voix_05_energie_mouvement.mp3` | `["energie_mouvement"]` | `ambre` / `halo` / `spirale_ouverte` |
| `voix_pilote_06` | Solène | Deuil & transition | `/assets/voix_pilote/voix_06_deuil_transition.mp3` | `["deuil_transition"]` | `ocre_doux` / `trame` / `feuille` |

Tous : `spoken_languages='["fr"]'`, `available_channels='["direct","async"]'`.
Idempotent : si email pilote existe déjà, mettre à jour les champs au lieu d'insérer.
Emails : `voix_pilote_01@ivia.quebec` à `voix_pilote_06@ivia.quebec` (override pilote redirige déjà sur Gmail).

**Important** : les fichiers audio sont sous `ivia_mockups/assets/voix_pilote/` (Python statique).
Pour qu'ils soient servis sur `ivia.quebec`, deux options :
- **Option A (rapide)** : copier les MP3 dans `09_app_ivia_merlin/public/assets/voix_pilote/`
  → servis en `/assets/voix_pilote/voix_*.mp3` par Next.js
- **Option B** : monter en S3 OVH et utiliser URLs signées
**Choisir Option A pour le pilote.**

---

### Phase C — Backend : route matching v1 (1h)

**Nouveau fichier** : `10_backend_merlin_api/app/api/routes/matching.py` (vérifier si existe, étendre sinon)

Route à créer/garantir :
```python
POST /api/v1/matching/recommend
Body: {
  "primary_need_code": "clarification" | "support" | "orientation" | "loneliness" | "distress" | "other",
  "preferred_modalities": ["corps_silence" | ...]  # optionnel
}
Response: list[PraticienPublic]  // 1 à 3 praticiens, ordonnés par score
```

**Algorithme matching v1 (simple, déterministe)** :
- Mapping `primary_need_code` → modalités préférées :
  - `clarification` → `mots_structure`, `contemplation_ancrage`
  - `support` → `corps_silence`, `frequence_vibration`
  - `orientation` → `mots_structure`, `energie_mouvement`
  - `loneliness` → `corps_silence`, `frequence_vibration`
  - `distress` → `deuil_transition`, `corps_silence`
  - `other` → toutes
- Score = nb modalités praticien intersectées avec préférées
- Trier par score desc, prendre top 3
- Si `preferred_modalities` fourni dans le body, utiliser plutôt ça

Ne pas appeler de LLM. Algo pur Python.

---

### Phase D — Frontend : refonte `/praticiens` carte abstraite (3h)

**Fichier** : `09_app_ivia_merlin/src/app/praticiens/page.tsx`

Remplacer entièrement la page actuelle. Composants à créer dans `09_app_ivia_merlin/src/components/praticiens/` :

1. **`AbstractCardVisual.tsx`** — SVG décoratif basé sur palette + texture + motif (zéro photo)
   - Palette : map vers couleurs CSS variables `--accent-*`
   - Motif : SVG inline (cercle, ligne, vague, feuille, pierre, spirale)
   - Texture : overlay `feTurbulence` SVG selon valeur
   - Aspect ratio carré, 280-320px
2. **`VoicePlayer.tsx`** — lecteur audio minimaliste
   - HTML5 `<audio>` avec contrôles custom (play/pause + barre progression + durée)
   - Auto-pause des autres lecteurs quand un nouveau démarre (event bus simple)
   - Pas d'autoplay
   - Indicateur "Voix de présentation — XXs"
3. **`PraticienCard.tsx`** — combine visuel + voix + intro + tags + CTA
   - Layout : visuel SVG haut + nom + title_line + intro_text + lecteur voix + tags + bouton "Prendre rendez-vous"
   - Lien `Réserver` → `/rendez-vous/reserver?praticien_id={p.id}`
4. **`PraticiensGrid.tsx`** — grille responsive avec filtre simple par modalité
   - Filtres en pills : "Toutes", "Corps & silence", "Parole & clarté", "Fréquence & vibration", "Contemplation & ancrage", "Énergie & mouvement", "Deuil & transition"
   - Aucun filtre par défaut

**Hero de la page** :
- Eyebrow : "Équipe IVIA — phase pilote"
- H1 : "Six voix, six manières d'écouter"
- Sous-titre : "Vous n'avez pas à choisir parfaitement. Écoutez-les, laissez quelque chose résonner. Ou prenez celle qui parle d'abord. *Au sein de l'être — En actes.*"
- Mention discrète sous le hero : "En phase pilote, ces six voix incarnent six manières de vous accompagner. Vous serez reçu par David Phaneuf, fondateur d'IVIA, qui adapte son écoute à la voix qui vous a appelé."

---

### Phase E — Frontend : brancher le funnel `/demarche` au matching (1h)

**Fichier** : `09_app_ivia_merlin/src/app/demarche/page.tsx`

Ajouter une 4e étape `recommandation` après `confirmation` :
- Au submit confirmation, appeler `recommendPraticiens(primary_need_code)` (à ajouter dans `merlin-api.ts`)
- Afficher 1 à 3 cartes praticiens recommandés avec lecteurs voix
- CTA principal : "Réserver avec [nom]" → `/rendez-vous/reserver?praticien_id={id}&intake_id={intakeId}`
- CTA secondaire : "Voir tous les praticiens" → `/praticiens`

**Nouveau dans `merlin-api.ts`** :
```typescript
export async function recommendPraticiens(payload: {
  primary_need_code: string;
  preferred_modalities?: string[];
}): Promise<PraticienPublic[]> {
  const res = await fetch(`${MERLIN_API_BASE_URL}/api/v1/matching/recommend`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`Erreur matching: ${res.status}`);
  return res.json();
}
```

---

### Phase F — Frontend : copier les voix dans /public (5 min)

```bash
cd 09_app_ivia_merlin
mkdir -p public/assets/voix_pilote
cp ../ivia_mockups/assets/voix_pilote/voix_*.mp3 public/assets/voix_pilote/
cp ../ivia_mockups/assets/voix_pilote/README.md public/assets/voix_pilote/README.md
```

Vérifier que `ivia.quebec/assets/voix_pilote/voix_01_presence_corporelle.mp3` répond 200 après déploiement.

---

### Phase G — Stripe : produit pilote 80 $ CAD 60 min (30 min)

**Fichier** : `10_backend_merlin_api/app/api/routes/payments.py`

Ajouter une variante de produit pour le pilote 60 min :
- Variable env : `MERLIN_STRIPE_PILOT_60MIN_AMOUNT_CENTS=8000`
- Variable env : `MERLIN_STRIPE_PILOT_60MIN_PRICE_ID` (à créer dans dashboard Stripe)
- Endpoint existant `POST /api/v1/payments/stripe/checkout` — ajouter param `session_type="pilot_60min" | "audio_async"`
- Default : `audio_async` (45 $ CAD), comportement actuel inchangé

David doit créer manuellement le produit Stripe dans son dashboard et copier le `price_id` dans `.env.production` du VPS OVH.

---

### Phase H — Tests + commits (30 min)

1. **Tests locaux** :
   - `cd 10_backend_merlin_api && pytest tests/test_matching.py -v`
   - `cd 09_app_ivia_merlin && npm run lint && npm run build`
2. **Test smoke local** :
   - `npm run dev` + backend up local
   - Visiter `http://localhost:3000/praticiens` → 6 cartes abstraites + voix qui jouent
   - Faire le funnel `/demarche` → recevoir 1-3 recommandations
3. **Commits granulaires** :
   ```
   feat(praticien-model) champs carte abstraite + modalites ecoute + migration
   feat(seed) 6 personas pilote avec voix David
   feat(matching) endpoint /api/v1/matching/recommend algo simple
   feat(praticiens-page) refonte carte abstraite + lecteur voix + filtres
   feat(funnel) etape 4 recommandation branchee matching
   feat(stripe) produit pilote 60min 80 CAD
   chore(public) copie voix pilote dans /public/assets
   ```
4. **Push** : `git push origin master`
5. **Déploiement OVH** : Copilot ou David pull sur VPS + `alembic upgrade head` + `pm2 restart` ou systemd reload

---

## Anti-doctrine — INTERDITS ABSOLUS

- ❌ Aucune image de visage, photo, illustration humaine reconnaissable
- ❌ Pas d'avatar généré par IA, même stylisé
- ❌ Pas d'emoji, pas de point d'exclamation
- ❌ Pas de "découvrez nos experts", "rencontrez l'équipe"
- ❌ Pas de "premium", "premium+", "best match" — vocabulaire commercial
- ❌ Ne pas exposer `email`, `legal_name`, `password_hash` dans `PraticienPublic`

---

## Variables env à ajouter (`.env.production` VPS OVH)

```env
MERLIN_PILOT_EMAIL_OVERRIDE=1
MERLIN_PILOT_CLIENT_PRACTITIONER_EMAIL=davidphaneuf@gmail.com
MERLIN_PILOT_ADMIN_EMAIL=lagent009@gmail.com
MERLIN_STRIPE_PILOT_60MIN_AMOUNT_CENTS=8000
MERLIN_STRIPE_PILOT_60MIN_PRICE_ID=price_xxxxx  # à créer dans dashboard Stripe
```

---

## Critères d'acceptation

1. ✅ `https://ivia.quebec/praticiens` affiche 6 cartes abstraites avec lecteurs voix qui jouent les MP3
2. ✅ Aucune photo / aucun visage sur la page
3. ✅ `https://ivia.quebec/demarche` produit 1-3 recommandations à la fin du funnel
4. ✅ `https://api.ivia.quebec/api/v1/matching/recommend` accepte POST et retourne JSON
5. ✅ `https://api.ivia.quebec/api/v1/praticiens` retourne 6 entrées avec `presentation_audio_url`
6. ✅ Test end-to-end : inscription → quiz → recommandation → réservation → mail (override Gmail) reçu
7. ✅ Build Next.js sans warning, lint pass
8. ✅ Migration Alembic appliquée sur prod sans erreur

---

## Ressources

- Doctrine vivante : `00_DOCTRINE/`
- Spec page : `04_METHODES/IVIA_SPEC_PAGE_PRATICIENS_v2.0.md`
- Voix : `ivia_mockups/assets/voix_pilote/`
- Backend prod : `https://api.ivia.quebec`
- Frontend prod : `https://ivia.quebec`
- Repo : `Fa9d/MERLIN` master

---

**Estimé total Sprint 2** : 7-8h Copilot + 1h David (Stripe dashboard + déploiement OVH).

**Lance-toi. Code propre, commits granulaires, doctrine respectée.**

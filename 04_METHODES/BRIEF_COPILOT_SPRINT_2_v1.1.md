# Brief Copilot — Sprint 2 IVIA v1.1 (corrigé)

**Date** : 9 mai 2026
**Remplace** : `BRIEF_COPILOT_SPRINT_2_v1.0.md` (erreurs de schéma corrigées)
**Production** : `ivia.quebec` + `api.ivia.quebec` (FastAPI + Next.js 16, OVH)
**Devise** : *Au sein de l'être — En actes.*

---

## Ce que j'avais raté dans v1.0 (à savoir AVANT de coder)

1. **La route matching EXISTE DÉJÀ** : `POST /api/v1/matching/suggest`
   - Body : `{"need": ClientNeedProfile, "exclude_ids": []}`
   - Réponse : `MatchingSuggestResponse` (1 suggestion + remaining_count + waitlist_mode)
   - Algo pondéré : domaine×3, approche×2, langue×3, dispo×1
2. **Modèle praticien = 2 tables** : `AppUser` + `PractitionerProfile` (relation 1-1)
   - Champs visuels (`presentation_audio_url`, `domaines`, `approches`, `langues`, `disponibilites`, `tarif_horaire_cents`, `bio`, `title_line`, `intro_text`) sont sur **`PractitionerProfile`**, pas `AppUser`
   - Champs `display_name`, `intro_text`, `title_line`, `presentation_audio_url`, `spoken_languages`, `available_channels` sur `AppUser` sont **dupliqués** mais utilisés par la route `/praticiens` simple
3. **Enums matching existants** :
   - `Domaine` : travail, relation, famille, deuil, anxiete, identite, sante, trauma, transition, autre
   - `Approche` : ecoute_active, outils_concrets, approche_systemique, psychocorporel, spirituel, cognitif_comportemental, narratif, autochtone
   - `LangueMatching` : fr, en, bil
   - `DispoSlot` : matin, apres_midi, soir, fin_semaine
4. **Page `/demarche` envoie `primary_need_code`** (clarification, support, orientation, loneliness, distress, other) — c'est **différent** des `Domaine` matching. Il faut un mapping.

---

## Sources de vérité (lire AVANT)

1. `00_DOCTRINE/IVIA_DOCTRINE_CARTE_ABSTRAITE_v1.0.md`
2. `04_METHODES/IVIA_SPEC_PAGE_PRATICIENS_v2.0.md`
3. `04_METHODES/IVIA_FUNNEL_QUIZ_TO_GUIDANCE_v1.2_ADDENDUM.md`
4. `ivia_mockups/assets/voix_pilote/README.md`
5. `10_backend_merlin_api/app/models/practitioner_profile.py` (LE modèle riche)
6. `10_backend_merlin_api/app/schemas/matching.py` (enums + ClientNeedProfile)
7. `10_backend_merlin_api/app/services/matching.py` (algo pondéré)
8. `10_backend_merlin_api/app/api/routes/matching.py` (route /suggest existante)

---

## Phase A — Backend : enrichir `PractitionerProfile` (45 min)

**Fichier** : `10_backend_merlin_api/app/models/practitioner_profile.py`

Ajouter ces champs (carte abstraite + persona pilote) :

```python
# Doctrine carte abstraite
abstract_palette: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
# valeurs: "vert_sauge" | "ocre_doux" | "ardoise" | "lin" | "argile" | "ambre"

abstract_texture: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
# valeurs: "ondulation" | "grain_papier" | "souffle" | "veinure" | "halo" | "trame"

abstract_motif: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
# valeurs: "cercle" | "ligne_horizon" | "spirale_ouverte" | "vague" | "feuille" | "pierre"

# Modalité d'écoute Mésange (1 par persona pilote)
listening_modality: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
# valeurs: "corps_silence" | "mots_structure" | "frequence_vibration"
#       | "contemplation_ancrage" | "energie_mouvement" | "deuil_transition"

# Persona pilote (NULL pour vrais praticiens P2)
pilot_persona_label: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
# valeurs: "voix_pilote_01" à "voix_pilote_06"
```

**Migration Alembic** :
```bash
cd 10_backend_merlin_api
alembic revision --autogenerate -m "praticien carte abstraite + modalite ecoute + persona pilote"
# Vérifier le fichier généré, puis :
alembic upgrade head
```

---

## Phase B — Backend : seed des 6 personas pilotes (45 min)

**Nouveau fichier** : `10_backend_merlin_api/scripts/seed_pilot_personas.py`

Crée 6 paires `AppUser` + `PractitionerProfile`. Idempotent (upsert par email).

| pilot_persona_label | display_name (AppUser + PP) | listening_modality | abstract_palette | abstract_texture | abstract_motif | domaines (mapping) | approches |
|---|---|---|---|---|---|---|---|
| voix_pilote_01 | Aëlis | corps_silence | vert_sauge | souffle | pierre | `["anxiete","trauma","sante"]` | `["psychocorporel","ecoute_active"]` |
| voix_pilote_02 | Naël | mots_structure | ardoise | grain_papier | ligne_horizon | `["travail","transition","identite"]` | `["cognitif_comportemental","outils_concrets"]` |
| voix_pilote_03 | Sève | frequence_vibration | lin | ondulation | vague | `["anxiete","relation","sante"]` | `["psychocorporel","spirituel"]` |
| voix_pilote_04 | Telma | contemplation_ancrage | argile | veinure | cercle | `["identite","famille","trauma"]` | `["narratif","autochtone","spirituel"]` |
| voix_pilote_05 | Nori | energie_mouvement | ambre | halo | spirale_ouverte | `["transition","travail","relation"]` | `["outils_concrets","ecoute_active"]` |
| voix_pilote_06 | Solène | deuil_transition | ocre_doux | trame | feuille | `["deuil","famille","trauma"]` | `["ecoute_active","narratif"]` |

Pour tous :
- `AppUser.email` = `voix_pilote_0X@ivia.quebec`
- `AppUser.password_hash` = bcrypt random 32 bytes (compte fictif, jamais utilisé)
- `AppUser.role` = `AppRole.practitioner`
- `AppUser.record_status` = `RecordStatus.active`
- `AppUser.is_publicly_listed` = True
- `AppUser.email_verified` = True
- `AppUser.title_line` = à composer selon modalité
- `AppUser.intro_text` = court, 1-2 phrases doctrinaires (pas commercial)
- `AppUser.presentation_audio_url` = `/assets/voix_pilote/voix_0X_<modalite>.mp3`
- `AppUser.spoken_languages` = `'["fr"]'` (JSON string)
- `AppUser.available_channels` = `'["direct"]'` (JSON string, pas `async` pour pilote)
- `PractitionerProfile.user_id` = id de l'AppUser créé
- `PractitionerProfile.public_visible` = True
- `PractitionerProfile.accepting_clients` = True
- `PractitionerProfile.actif` = True
- `PractitionerProfile.langues` = `["fr"]` (liste Python via colonne JSON)
- `PractitionerProfile.disponibilites` = `'["matin","apres_midi","soir"]'` (JSON string sur Text)
- `PractitionerProfile.tarif_horaire_cents` = `8000` (80 $ CAD)
- `PractitionerProfile.bio` = identique à `intro_text`
- `PractitionerProfile.modalites` = `[listening_modality]` (liste Python via JSON)

**Note technique** : `PractitionerProfile.modalites/langues/approches` sont colonnes `JSON` (acceptent listes Python). `PractitionerProfile.domaines/disponibilites` sont colonnes `Text` (JSON serialisé string). Respecter la différence.

**Pour les fichiers audio** : Phase F déjà faite par Computer (les MP3 sont dans `09_app_ivia_merlin/public/assets/voix_pilote/` du repo). Pas besoin de copier.

**Lancement** :
```bash
cd 10_backend_merlin_api
python -m scripts.seed_pilot_personas
```

---

## Phase C — Backend : étendre route matching pour cartes abstraites (30 min)

**Fichier** : `10_backend_merlin_api/app/api/routes/matching.py`

La route `POST /api/v1/matching/suggest` existe déjà (1 seule suggestion). Pour le funnel `/demarche`, on veut **3 suggestions max** (cartes abstraites) :

Ajouter une route `POST /api/v1/matching/recommend` qui retourne top 3 :

```python
from app.schemas.matching import MatchingSuggestRequest, PractitionerCard

@router.post("/recommend", response_model=list[PractitionerCard])
def recommend_practitioners(payload: MatchingSuggestRequest, db: Session = Depends(get_db)):
    ranked = get_ranked_practitioners(db=db, need=payload.need, exclude_ids=payload.exclude_ids)
    return [_build_card(p, p.user) for p in ranked[:3]]
```

**Étendre `PractitionerCard`** dans `schemas/matching.py` pour inclure les nouveaux champs carte abstraite :

```python
class PractitionerCard(BaseModel):
    user_id: str
    display_name: str
    title_line: Optional[str]
    intro_text: Optional[str]
    presentation_audio_url: Optional[str]
    domaines: list[str]
    approches: list[str]
    langues: list[str]
    disponibilites: list[str]
    tarif_horaire_cents: Optional[int]
    # nouveaux carte abstraite
    abstract_palette: Optional[str]
    abstract_texture: Optional[str]
    abstract_motif: Optional[str]
    listening_modality: Optional[str]
    pilot_persona_label: Optional[str]
    model_config = {"from_attributes": True}
```

Et adapter `_build_card()` pour inclure les nouveaux champs depuis `profile`.

---

## Phase D — Mapping `primary_need_code` → `Domaine` matching (30 min)

**Nouveau fichier** : `10_backend_merlin_api/app/services/intake_to_matching.py`

```python
from app.schemas.matching import ClientNeedProfile, Domaine, LangueMatching

# Mapping Mésange → matching
NEED_TO_DOMAINES = {
    "clarification": [Domaine.identite, Domaine.transition, Domaine.travail],
    "support":       [Domaine.anxiete, Domaine.relation, Domaine.sante],
    "orientation":   [Domaine.transition, Domaine.travail, Domaine.identite],
    "loneliness":    [Domaine.relation, Domaine.identite],
    "distress":      [Domaine.deuil, Domaine.trauma, Domaine.anxiete],
    "other":         [Domaine.autre],
}

def primary_need_to_client_profile(primary_need_code: str) -> ClientNeedProfile:
    return ClientNeedProfile(
        domaines=NEED_TO_DOMAINES.get(primary_need_code, [Domaine.autre]),
        langues=[LangueMatching.fr],
    )
```

**Branchement frontend** : la page `/demarche` appelle `recommendPraticiens(primary_need_code)` qui POST `/api/v1/matching/recommend` avec un body construit par cette fonction. **Soit** faire la conversion côté frontend TypeScript (dupliquer la map), **soit** créer une route facilitatrice :

```python
# routes/matching.py — route helper "from_intake"
class IntakeRecommendRequest(BaseModel):
    primary_need_code: str

@router.post("/recommend-from-intake", response_model=list[PractitionerCard])
def recommend_from_intake(payload: IntakeRecommendRequest, db: Session = Depends(get_db)):
    need = primary_need_to_client_profile(payload.primary_need_code)
    ranked = get_ranked_practitioners(db=db, need=need)
    return [_build_card(p, p.user) for p in ranked[:3]]
```

→ **choisir cette deuxième option** (plus propre, évite duplication map).

---

## Phase E — Frontend : refonte `/praticiens` carte abstraite (3h)

**Fichier** : `09_app_ivia_merlin/src/app/praticiens/page.tsx`

### Étape E1 — étendre `PraticienPublic` dans `lib/merlin-api.ts`

```typescript
export interface PraticienPublic {
  id: string;
  display_name: string;
  title_line: string | null;
  intro_text: string | null;
  spoken_languages: string | null;
  available_channels: string | null;
  // nouveaux champs (depuis backend MAJ)
  presentation_audio_url?: string | null;
  abstract_palette?: string | null;
  abstract_texture?: string | null;
  abstract_motif?: string | null;
  listening_modality?: string | null;
  pilot_persona_label?: string | null;
}
```

**Note** : la route `/api/v1/praticiens` doit retourner ces nouveaux champs aussi. Étendre `PraticienPublic` dans `schemas/auth.py` côté backend (déjà partiellement fait dans v1.0 du brief). Et étendre la query SQL pour joindre `PractitionerProfile`.

### Étape E2 — composant `AbstractCardVisual.tsx`

`09_app_ivia_merlin/src/components/praticiens/AbstractCardVisual.tsx`

SVG décoratif 100% inline, aucune image externe. Props :
```typescript
interface Props {
  palette: string | null;
  texture: string | null;
  motif: string | null;
  size?: number;  // défaut 280
}
```

Mapping palette → couleurs OKLCH (cohérence avec theme `globals.css`) :
- `vert_sauge` → bg `oklch(93% 0.04 145)`, accent `oklch(42% 0.09 145)`
- `ocre_doux` → bg `oklch(93% 0.05 75)`, accent `oklch(45% 0.10 75)`
- `ardoise` → bg `oklch(92% 0.02 230)`, accent `oklch(38% 0.06 230)`
- `lin` → bg `oklch(95% 0.02 80)`, accent `oklch(48% 0.05 80)`
- `argile` → bg `oklch(88% 0.04 50)`, accent `oklch(40% 0.08 50)`
- `ambre` → bg `oklch(90% 0.06 70)`, accent `oklch(45% 0.12 70)`

Motif = SVG simple :
- `cercle` → cercle concentrique
- `ligne_horizon` → 3 lignes horizontales décalées
- `spirale_ouverte` → spirale path
- `vague` → sinusoïde Bézier
- `feuille` → ellipse pointue
- `pierre` → polygone organique

Texture = overlay `<filter><feTurbulence baseFrequency="..."/></filter>` selon valeur.

### Étape E3 — composant `VoicePlayer.tsx`

`09_app_ivia_merlin/src/components/praticiens/VoicePlayer.tsx`

```typescript
interface Props {
  src: string;
  label?: string;  // défaut "Voix de présentation"
}
```

- HTML5 `<audio>` (preload="metadata")
- Bouton play/pause custom (icône Lucide ou SVG inline)
- Barre de progression cliquable
- Affichage durée totale + temps actuel (mm:ss)
- **Auto-pause des autres lecteurs** : event `CustomEvent('voice-player-play')` global, chaque player écoute et se pause si l'event vient d'un autre src
- Pas d'autoplay, jamais
- Accessible : `aria-label`, focus ring, `<track kind="descriptions">` optionnel

### Étape E4 — composant `PraticienCard.tsx`

Combine : `AbstractCardVisual` (haut) + nom + title_line + intro_text (~2 lignes) + `VoicePlayer` + tags (langues, modalité d'écoute) + bouton "Prendre rendez-vous".

CTA → `/rendez-vous/reserver?praticien_id={p.id}` (on passe l'id pour pré-sélection).

### Étape E5 — composant `PraticiensGrid.tsx`

Grille responsive (`auto-fill, minmax(300px, 1fr)`).

Filtres en pills au-dessus :
- Toutes (défaut)
- Corps & silence
- Parole & clarté
- Fréquence & vibration
- Contemplation & ancrage
- Énergie & mouvement
- Deuil & transition

Filtre côté client sur `listening_modality`.

### Étape E6 — refonte `app/praticiens/page.tsx`

Hero :
- Eyebrow : "Équipe IVIA — phase pilote"
- H1 : "Six voix, six manières d'écouter"
- Sous-titre : "Vous n'avez pas à choisir parfaitement. Écoutez-les, laissez quelque chose résonner. Ou prenez celle qui parle d'abord."
- Mention discrète : "En phase pilote, ces six voix incarnent six manières de vous accompagner. Vous serez reçu par David Phaneuf, fondateur d'IVIA, qui adapte son écoute à la voix qui vous a appelé. *Au sein de l'être — En actes.*"

Body : `<PraticiensGrid />` qui appelle `listPraticiens()`.

---

## Phase F — Frontend : étape recommandation au bout de `/demarche` (1h)

**Fichier** : `09_app_ivia_merlin/src/app/demarche/page.tsx`

Ajouter `Step = "besoin" | "identite" | "confirmation" | "recommandation"`.

Au submit confirmation (après `createIntakeRequest` + `createConsent`), appeler nouvelle fonction `recommendPraticiensFromIntake(primary_need_code)` qui POST `/api/v1/matching/recommend-from-intake`.

Stocker dans `useState<PractitionerCard[]>` et passer à `setStep("recommandation")`.

Vue `recommandation` :
- Titre : "Trois voix pour vous"
- Sous-titre : "Selon ce que vous avez partagé, ces trois voix peuvent vous accompagner. Écoutez-les. Choisissez celle qui résonne."
- 3 `<PraticienCard />` empilées (responsive)
- CTA primaire sur chaque carte : "Réserver avec [nom]" → `/rendez-vous/reserver?praticien_id={id}&intake_id={intakeId}`
- CTA secondaire global en bas : "Voir tous les praticiens" → `/praticiens`

**Nouveau dans `lib/merlin-api.ts`** :
```typescript
export async function recommendPraticiensFromIntake(
  primary_need_code: string
): Promise<PractitionerCard[]> {
  const res = await fetch(`${MERLIN_API_BASE_URL}/api/v1/matching/recommend-from-intake`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ primary_need_code }),
  });
  if (!res.ok) throw new Error(`Erreur recommandation: ${res.status}`);
  return res.json();
}

export interface PractitionerCard {
  user_id: string;
  display_name: string;
  title_line: string | null;
  intro_text: string | null;
  presentation_audio_url: string | null;
  domaines: string[];
  approches: string[];
  langues: string[];
  disponibilites: string[];
  tarif_horaire_cents: number | null;
  abstract_palette: string | null;
  abstract_texture: string | null;
  abstract_motif: string | null;
  listening_modality: string | null;
  pilot_persona_label: string | null;
}
```

---

## Phase G — Stripe pilote 80 $ CAD 60 min (30 min)

### G1 — Créer le produit dans Stripe Dashboard (David, 5 min)

David se connecte sur `dashboard.stripe.com` :
1. Products → Create product
2. Name : "RDV pilote IVIA — 60 min"
3. Pricing : One-time, 80.00 CAD
4. Save → copier le `price_id` (ex: `price_1ABC...`)

### G2 — Backend : étendre la route checkout (Copilot)

`10_backend_merlin_api/app/api/routes/payments.py`

Endpoint existant `POST /api/v1/payments/stripe/checkout` :
- Ajouter param body `session_type: Literal["audio_async", "pilot_60min"] = "audio_async"`
- Si `pilot_60min` : utiliser `MERLIN_STRIPE_PILOT_60MIN_PRICE_ID` au lieu du prix dynamique audio_async
- Si `audio_async` : comportement actuel inchangé

### G3 — Frontend : passer `session_type=pilot_60min` depuis `/rendez-vous/reserver`

Modifier la page de réservation pour utiliser `session_type=pilot_60min` quand l'utilisateur vient du funnel pilote (`?intake_id=...`).

### G4 — Variables env VPS OVH

Sur le VPS, ajouter dans `.env.prod` :
```env
MERLIN_STRIPE_PILOT_60MIN_AMOUNT_CENTS=8000
MERLIN_STRIPE_PILOT_60MIN_CURRENCY=cad
MERLIN_STRIPE_PILOT_60MIN_PRICE_ID=price_XXXXXXX  # copié depuis dashboard
```

---

## Phase H — Tests + commits + déploiement (30 min)

### Tests locaux
```bash
cd 10_backend_merlin_api
pytest tests/ -v -k "matching or seed"
cd ../09_app_ivia_merlin
npm run lint
npm run build
npm run dev  # test smoke
```

### Smoke test
- `http://localhost:3000/praticiens` → 6 cartes abstraites + 6 lecteurs voix qui jouent
- `http://localhost:3000/demarche` → finir le funnel → recevoir 3 recommandations
- Cliquer "Réserver avec Aëlis" → page réservation pré-remplie

### Commits granulaires
```
feat(praticien-model): champs carte abstraite + modalite ecoute + persona pilote
feat(seed): 6 personas pilote avec voix David
feat(matching): route /recommend top 3 + helper from-intake
feat(praticiens-page): refonte carte abstraite + lecteur voix + filtres
feat(funnel): etape recommandation branchee matching
feat(stripe): produit pilote 60min 80 CAD via session_type
```

### Push + déploiement OVH
```bash
git push origin master
# Sur le VPS OVH :
ssh root@137.74.42.121
cd /opt/merlin   # ou chemin réel
git pull origin master
sudo make migrate   # applique alembic upgrade
sudo make up        # rebuild + restart
curl -s https://api.ivia.quebec/api/v1/praticiens | jq '. | length'  # doit dire 7 (David + 6 personas)
```

---

## Critères d'acceptation

1. ✅ `https://ivia.quebec/praticiens` affiche 6 cartes abstraites (+ David si toujours listé) avec lecteurs voix qui jouent les MP3
2. ✅ Aucune photo / aucun visage sur la page
3. ✅ `https://ivia.quebec/demarche` produit 3 recommandations à la fin du funnel
4. ✅ `https://api.ivia.quebec/api/v1/matching/recommend-from-intake` accepte POST et retourne JSON 3 cartes
5. ✅ `https://api.ivia.quebec/api/v1/praticiens` retourne au moins 6 entrées avec `presentation_audio_url`
6. ✅ Migration Alembic appliquée sur prod sans erreur
7. ✅ Build Next.js sans warning, lint pass
8. ✅ Test E2E manuel : inscription → quiz → 3 recommandations → réserver Aëlis → checkout Stripe 80 CAD → mail (override Gmail) reçu

---

## Anti-doctrine — INTERDITS ABSOLUS

- ❌ Aucune image de visage, photo, illustration humaine reconnaissable
- ❌ Pas d'avatar généré par IA, même stylisé
- ❌ Pas d'emoji, pas de point d'exclamation
- ❌ Pas de "découvrez nos experts", "rencontrez l'équipe"
- ❌ Pas de "premium", "best match" — vocabulaire commercial
- ❌ Ne pas exposer `email`, `legal_name`, `password_hash` dans `PractitionerCard`
- ❌ Ne pas autoplay les voix
- ❌ Ne pas afficher le tarif sur la carte praticien (seulement à la réservation)

---

## Estimé total

7-8h Copilot + 5 min David (Stripe dashboard).

---

*Au sein de l'être — En actes.*

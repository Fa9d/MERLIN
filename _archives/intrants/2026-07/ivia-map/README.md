# 🌿 IVIA — Système Intégré de Valorisation par l'Intelligence Artificielle

> Plateforme de santé mentale régénérative combinant IA conversationnelle, analyse audio et suivi RGNR (Régénération — Corps / Émotions / Pensées / Environnement)

---

## 📁 Structure du projet

```
_IVIA.map/
├── src/
│   ├── client/              → Interface client (app mobile/web)
│   ├── practitioner/        → Dashboard praticien (MERLIN)
│   ├── shared/              → Composants partagés, design system
│   └── audio-pipeline/      → ivia-audio-pipeline (Whisper + SpeechBrain + MERLIN)
├── docs/                    → Documentation technique & clinique
├── assets/                  → Ressources visuelles, icons, brand
├── config/                  → Variables d'environnement, configs
└── README.md
```

---

## 🧠 Les deux interfaces

| Interface | Public | Rôle |
|-----------|--------|------|
| **Client** | Personne suivie | Check-ins RGNR, ressources, boucle de récupération |
| **Praticien** | Thérapeute / Coach | Dashboard MERLIN, alertes, notes de séance, insights |

---

## 🎙️ ivia-audio-pipeline

Pipeline de transcription et d'analyse des séances audio :

```
Audio brut → Whisper (transcription) → SpeechBrain (diarisation) → MERLIN (analyse RGNR) → Dashboard praticien
```

Voir [`src/audio-pipeline/README.md`](./src/audio-pipeline/README.md)

---

## 🚀 Démarrage rapide

```bash
# Cloner le repo
git clone git@github.com:Fa9d/_IVIA.map.git
cd _IVIA.map

# Installer les dépendances
npm install          # Interface web (client + praticien)
pip install -r src/audio-pipeline/requirements.txt  # Pipeline audio

# Variables d'environnement
cp config/.env.example config/.env
# → Remplir OPENAI_API_KEY, HUME_API_KEY, etc.

# Lancer en développement
npm run dev
```

---

## 📐 Concepts RGNR

Basés sur les principes de [My Thriving Mind](https://mythrivingmind.io) et [Thriving Minds](https://thrivingminds.ca) :

- **R**écupération — Le repos n'est pas une récompense, c'est une nécessité
- **G**estion — Stress ≠ ennemi. Déséquilibre = problème
- **N**ourrir — Corps / Émotions / Pensées / Environnement
- **R**ythme — Boucle continue entre séances, micro-pratiques

---

## 🔐 Sécurité & Conformité

- Données de santé → chiffrement AES-256 au repos, TLS 1.3 en transit
- Conformité PIPEDA (Canada) / RGPD (Europe)
- Aucune donnée audio conservée après traitement (optionnel)

---

## 📄 Licence

Propriétaire — © 2026 IVIA. Tous droits réservés.

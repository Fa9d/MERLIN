# Design System Master File — IVIA

> **LOGIC:** When building a specific page, first check `design-system/pages/[page-name].md`.
> If that file exists, its rules **override** this Master file.
> If not, strictly follow the rules below.

---

**Project:** IVIA — Plateforme d'écoute et d'accompagnement non-clinique
**Site:** ivia.quebec
**Stack:** Next.js (frontend) · FastAPI Python (backend) · PostgreSQL · Tailwind CSS
**Generated:** 2026-05-29 (manuellement curée — override du résultat automatique)
**Category:** Healthcare / Wellness — Listening Service · Civic Tech Québec

---

## Identité produit (à respecter dans chaque copie UI)

- IVIA **n'est pas** un service d'urgence — jamais suggérer un usage de crise
- IVIA **ne pose pas de diagnostic** — toujours « espace d'écoute », jamais « thérapie »
- Audio-only intentionnel — pas de vidéo, c'est un choix doctrinal
- Conforme Loi 25 Québec — badge de confiance visible
- Voix effacée à J+30 — communiquer la protection des données
- Public : adultes Québec, tous profils, accès non-clinique

---

## Global Rules

### Style — Organic Biophilic + Trust & Authority

Style principal : **Organic Biophilic** — nature, courbes organiques, chaleur, bien-être
Accents : **Trust & Authority** — badges Loi 25, données protégées, cadre éthique

> ⚠ Override du résultat automatique "Vibrant & Block-based" — inadapté à une plateforme d'écoute thérapeutique non-clinique. Le style botanique correspond à la charte existante des mockups (`puces--vert`, palette verte) et à l'identité québécoise civique d'IVIA.

**Keywords retenus** : calme, organique, confiance, éthique, nature québécoise, humain, bienveillant
**Anti-patterns** : couleurs neon, animations agressives, dark mode OLED, gradients AI purple/pink, jargon clinique

### Color Palette

| Role | Hex | CSS Variable | Usage |
|------|-----|--------------|-------|
| Primary | `#4A7C59` | `--color-primary` | Vert forêt — boutons principaux, headings |
| Secondary | `#8FB99A` | `--color-secondary` | Sauge clair — accents, hover |
| CTA | `#2D6A4F` | `--color-cta` | Vert profond — CTA principal |
| Background | `#FAFDF8` | `--color-background` | Blanc légèrement vert — fond pages |
| Surface | `#F0F7F2` | `--color-surface` | Sections alternées douces |
| Text | `#1A2E1D` | `--color-text` | Vert très sombre — texte principal |
| Text muted | `#4B6350` | `--color-muted` | Corps de texte secondaire |
| Border | `#D4E8D0` | `--color-border` | Séparations, cartes |
| Trust | `#2563EB` | `--color-trust` | Badges Loi 25, sécurité, confiance |
| Warning | `#D97706` | `--color-warning` | Urgence — bandeau footer discret |

**Color Notes:** Palette botanique québécoise — évoque forêt, calme, soin. Le vert foncé donne l'autorité éthique sans la froideur clinique du bleu hospitalier.

### Typography

- **Heading Font:** Lora (serif élégant — éditorial, chaleureux, humain)
- **Body Font:** Raleway (sans-serif léger — lisibilité, modernité douce)
- **Mood:** calm, wellness, health, relaxing, natural, organic
- **Google Fonts:** [Lora + Raleway](https://fonts.google.com/share?selection.family=Lora:wght@400;500;600;700|Raleway:wght@300;400;500;600;700)

**CSS Import:**
```css
@import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600;700&family=Raleway:wght@300;400;500;600;700&display=swap');
```

### Spacing Variables

| Token | Value | Usage |
|-------|-------|-------|
| `--space-xs` | `4px` / `0.25rem` | Tight gaps |
| `--space-sm` | `8px` / `0.5rem` | Icon gaps, inline spacing |
| `--space-md` | `16px` / `1rem` | Standard padding |
| `--space-lg` | `24px` / `1.5rem` | Section padding |
| `--space-xl` | `32px` / `2rem` | Large gaps |
| `--space-2xl` | `48px` / `3rem` | Section margins |
| `--space-3xl` | `64px` / `4rem` | Hero padding |

### Shadow Depths

| Level | Value | Usage |
|-------|-------|-------|
| `--shadow-sm` | `0 1px 2px rgba(0,0,0,0.05)` | Subtle lift |
| `--shadow-md` | `0 4px 6px rgba(0,0,0,0.1)` | Cards, buttons |
| `--shadow-lg` | `0 10px 15px rgba(0,0,0,0.1)` | Modals, dropdowns |
| `--shadow-xl` | `0 20px 25px rgba(0,0,0,0.15)` | Hero images, featured cards |

---

## Component Specs

### Buttons

```css
/* Primary Button */
.btn-primary {
  background: #10B981;
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  transition: all 200ms ease;
  cursor: pointer;
}

.btn-primary:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

/* Secondary Button */
.btn-secondary {
  background: transparent;
  color: #8B5CF6;
  border: 2px solid #8B5CF6;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  transition: all 200ms ease;
  cursor: pointer;
}
```

### Cards

```css
.card {
  background: #FAF5FF;
  border-radius: 12px;
  padding: 24px;
  box-shadow: var(--shadow-md);
  transition: all 200ms ease;
  cursor: pointer;
}

.card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}
```

### Inputs

```css
.input {
  padding: 12px 16px;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 200ms ease;
}

.input:focus {
  border-color: #8B5CF6;
  outline: none;
  box-shadow: 0 0 0 3px #8B5CF620;
}
```

### Modals

```css
.modal-overlay {
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
}

.modal {
  background: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: var(--shadow-xl);
  max-width: 500px;
  width: 90%;
}
```

---

## Style Guidelines

**Style:** Organic Biophilic + Trust & Authority (override manuel — voir note ci-dessus)

**Keywords:** nature québécoise, organique, courbes douces, calme, confiance, éthique, botanique, bienveillant

**Effects:** border-radius 16-24px organique, ombres naturelles douces, transitions 200ms ease-out, SVG blob shapes en fond, organic curves

**Key Effects:** Sections généreuses (48px+ gaps), courbes organiques en SVG fond hero, hover doux (couleur, pas de scale), transitions 200ms, type lisible (18px+ corps)

### Page Pattern — Landing IVIA

**Pattern:** Hero-Centric + Étapes + Social Proof + Cadre Éthique + CTA

| # | Section | Contenu |
|---|---------|---------|
| 1 | **Hero** | Titre 2 lignes max · CTA primaire grand · lien secondaire discret · visuel SVG organique |
| 2 | **Comment ça marche** | 3 étapes simples (Réserve → Parle → Reçois) |
| 3 | **Ce qu'IVIA est / n'est pas** | Cadre doctrinal non-clinique, liste claire |
| 4 | **Praticiens** | 2-3 praticiens avec photo, prénom, spécialité — social proof humain |
| 5 | **Cadre éthique** | Badge Loi 25 · voix effacée J+30 · pas de diagnostic · données QC |
| 6 | **CTA final** | Répéter CTA + lien "voir comment ça se passe" |

**CTA Placement:** Hero sticky + après praticiens
**CTA Copy:** "Commencer une écoute →" (primaire) · "voir comment ça se passe" (secondaire, discret)

---

## Anti-Patterns (Do NOT Use)

- ❌ Flat design sans profondeur
- ❌ Pages text-heavy sans respirations visuelles
- ❌ **Gradients AI purple/pink** — hors identité IVIA
- ❌ **Dark mode OLED** — contre l'identité chaleureuse
- ❌ **Neons ou couleurs criardes** — incompatible bien-être
- ❌ **Jargon clinique** — "thérapie", "traitement", "diagnostic"
- ❌ **Animations agressives** — bounce, flash, clignotement
- ❌ **Emojis comme icônes** — SVG Heroicons/Lucide uniquement
- ❌ **cursor:pointer manquant** — tous les éléments cliquables
- ❌ **Focus states invisibles** — accessibilité obligatoire
- ❌ **Contraste insuffisant** — minimum 4.5:1 texte principal
- ❌ **Transitions instantanées** — toujours 150-300ms ease

### Règles IVIA-spécifiques

- ❌ Ne jamais suggérer qu'IVIA peut remplacer un suivi médical
- ❌ Aucune mention "urgence" sans pointer vers `urgence.html` + ressources
- ❌ Ne jamais afficher de données audio ou de transcriptions en UI publique
- ✅ Toujours afficher le badge Loi 25 Québec sur pages avec formulaire
- ✅ Toujours inclure la mention "IVIA n'est pas un service d'urgence" en footer

---

## Pre-Delivery Checklist

Before delivering any UI code, verify:

- [ ] No emojis used as icons (use SVG Heroicons/Lucide instead)
- [ ] All icons from consistent icon set
- [ ] `cursor-pointer` on all clickable elements
- [ ] Hover states with smooth transitions (150-300ms)
- [ ] Light mode: text contrast 4.5:1 minimum (#1A2E1D sur #FAFDF8 = ✅)
- [ ] Focus states visible for keyboard navigation
- [ ] `prefers-reduced-motion` respected
- [ ] Responsive: 375px, 768px, 1024px, 1440px
- [ ] No content hidden behind fixed navbars
- [ ] No horizontal scroll on mobile
- [ ] Badge Loi 25 présent sur toute page avec formulaire
- [ ] Mention disclaimer urgence présente en footer
- [ ] Aucun jargon clinique (thérapie, diagnostic, traitement)
- [ ] Police `font-display: swap` pour Lora + Raleway
- [ ] Images lazy-loaded si below-fold (`loading="lazy"`)
- [ ] Input Next.js validé avec Zod côté serveur

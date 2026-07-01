## IVIA – Design tokens de base (clair + sombre)

### 1. Couleurs

#### 1.1 Palette claire

```json
{
  "color.background": "#F5F4EE",
  "color.surface": "#FFFFFF",
  "color.surfaceSubtle": "#FAFAF8",

  "color.text.primary": "#1F2933",
  "color.text.secondary": "#6B7280",
  "color.text.invert": "#F9FAFB",

  "color.accent.rgnr": "#3B7F6A",
  "color.accent.soft1": "#FBE8D3",
  "color.accent.soft2": "#E3F4E0",

  "color.border.default": "#E5E7EB",
  "color.border.strong": "#D1D5DB",

  "color.nav.background": "#FAFAF8",
  "color.nav.iconInactive": "#9CA3AF",
  "color.nav.iconActive": "#3B7F6A",

  "color.button.primary.background": "#3B7F6A",
  "color.button.primary.text": "#FFFFFF",
  "color.button.secondary.background": "#FFFFFF",
  "color.button.secondary.text": "#3B7F6A",
  "color.button.secondary.border": "#3B7F6A",

  "color.badge.success.background": "#E3F4E0",
  "color.badge.success.text": "#166534"
}
```

#### 1.2 Palette sombre

```json
{
  "color.background": "#0F1720",
  "color.surface": "#111827",
  "color.surfaceSubtle": "#020617",

  "color.text.primary": "#F9FAFB",
  "color.text.secondary": "#9CA3AF",
  "color.text.invert": "#0F1720",

  "color.accent.rgnr": "#5BD9A3",
  "color.accent.soft1": "#1F2933",
  "color.accent.soft2": "#064E3B",

  "color.border.default": "#1F2933",
  "color.border.strong": "#4B5563",

  "color.nav.background": "#020617",
  "color.nav.iconInactive": "#6B7280",
  "color.nav.iconActive": "#5BD9A3",

  "color.button.primary.background": "#5BD9A3",
  "color.button.primary.text": "#03110C",
  "color.button.secondary.background": "#0F1720",
  "color.button.secondary.text": "#5BD9A3",
  "color.button.secondary.border": "#5BD9A3",

  "color.badge.success.background": "#064E3B",
  "color.badge.success.text": "#A7F3D0"
}
```

---

### 2. Typographie

```json
{
  "font.family.base": "Inter, system-ui, -apple-system, BlinkMacSystemFont, 'SF Pro Text'",
  "font.size.h1": 24,
  "font.size.h2": 18,
  "font.size.body": 15,
  "font.size.small": 13,

  "font.weight.regular": 400,
  "font.weight.medium": 500,
  "font.weight.semibold": 600
}
```

---

### 3. Rayons, espacements, ombres

```json
{
  "radius.sm": 8,
  "radius.md": 12,
  "radius.lg": 16,
  "radius.pill": 999,

  "space.xs": 4,
  "space.sm": 8,
  "space.md": 12,
  "space.lg": 16,
  "space.xl": 24,

  "shadow.card": "0 8px 20px rgba(15, 23, 42, 0.08)",
  "shadow.nav": "0 -4px 12px rgba(15, 23, 42, 0.10)"
}
```

---

### 4. Composants clés (structure)

#### 4.1 Bouton primaire

- Hauteur : 48 px  
- Rayon : `radius.md`  
- Padding horizontal : `space.lg`  
- Couleurs :  
  - Fond : `color.button.primary.background`  
  - Texte : `color.button.primary.text`  

#### 4.2 Bottom nav

- Hauteur : 72 px  
- Fond : `color.nav.background`  
- 4 icônes + 1 bouton central RGNR.  
- Bouton central RGNR :  
  - Diamètre : 56 px  
  - Position : centré horizontalement, chevauche légèrement la barre.  
  - Fond : `color.accent.rgnr`  
  - Icône : taille 24 px, couleur `color.text.invert`.

#### 4.3 Card standard

- Fond : `color.surface`  
- Rayon : `radius.md`  
- Padding : `space.lg`  
- Ombre : `shadow.card`  
- Utilisé pour : suggestions de pratiques, intentions, éléments de timeline RGNR.

---

### 5. Ce que tu dois générer

À partir de ces tokens + de la spec d’écrans fournie, génère :

1. Une librairie de styles (Figma ou code) pour les deux thèmes (clair/sombre).  
2. Les 3 maquettes de téléphones scrollables décrites dans la spec précédente, avec :  
   - bottom nav fixe, bouton RGNR central  
   - respect strict des couleurs, rayons, typographies  
   - variantes clair et sombre.
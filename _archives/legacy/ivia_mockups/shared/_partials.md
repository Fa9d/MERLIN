# Partials de référence — IVIA mockups

## Logo IVIA (SVG inline, monochrome currentColor)

```html
<svg class="brand__mark" viewBox="0 0 36 36" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true">
  <!-- vrille botanique stylisée — coupe transversale -->
  <circle cx="18" cy="18" r="14.5" stroke-opacity="0.4"/>
  <path d="M18 4.5 C 11 12, 25 24, 18 31.5" stroke-linecap="round"/>
  <path d="M11 18 C 14 16, 22 20, 25 18" stroke-linecap="round" stroke-opacity="0.7"/>
  <circle cx="18" cy="18" r="2.5" fill="currentColor" stroke="none"/>
</svg>
```

## Brand mark complet (header)

```html
<a href="/" class="brand">
  <svg class="brand__mark" viewBox="0 0 36 36" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true">
    <circle cx="18" cy="18" r="14.5" stroke-opacity="0.4"/>
    <path d="M18 4.5 C 11 12, 25 24, 18 31.5" stroke-linecap="round"/>
    <path d="M11 18 C 14 16, 22 20, 25 18" stroke-linecap="round" stroke-opacity="0.7"/>
    <circle cx="18" cy="18" r="2.5" fill="currentColor" stroke="none"/>
  </svg>
  <span class="brand__name">IV<em>I</em>A</span>
</a>
```

## Vrille décorative fixe (Le Fil)

```html
<div class="vrille-fixe" aria-hidden="true">
  <svg viewBox="0 0 500 800" fill="none" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="vrille-grad" x1="0" x2="1" y1="0" y2="1">
        <stop offset="0%" stop-color="#C58A8A" stop-opacity="0.8"/>
        <stop offset="50%" stop-color="#D9A441" stop-opacity="0.5"/>
        <stop offset="100%" stop-color="#6B8266" stop-opacity="0.4"/>
      </linearGradient>
    </defs>
    <!-- vrille principale -->
    <path d="M 250 0 C 100 200, 400 350, 200 500 C 50 650, 350 750, 250 800"
          stroke="url(#vrille-grad)" stroke-width="1.5" fill="none"/>
    <path d="M 280 0 C 130 220, 430 360, 230 510 C 80 660, 380 760, 280 800"
          stroke="#C58A8A" stroke-width="0.8" stroke-opacity="0.4" fill="none"/>
    <!-- petites feuilles -->
    <ellipse cx="200" cy="180" rx="14" ry="5" fill="#6B8266" fill-opacity="0.3" transform="rotate(-30 200 180)"/>
    <ellipse cx="320" cy="280" rx="12" ry="4" fill="#D89260" fill-opacity="0.3" transform="rotate(20 320 280)"/>
    <ellipse cx="180" cy="430" rx="16" ry="6" fill="#C58A8A" fill-opacity="0.35" transform="rotate(-15 180 430)"/>
    <ellipse cx="290" cy="600" rx="13" ry="5" fill="#9A8AB8" fill-opacity="0.3" transform="rotate(40 290 600)"/>
  </svg>
</div>
```

## Header (interface CLIENT)

```html
<header class="site-header">
  <div class="container site-header__inner">
    <!-- brand -->
    <nav class="nav" aria-label="Navigation principale">
      <a href="index.html" aria-current="page">Accueil</a>
      <a href="praticiens.html">Praticiens</a>
      <a href="ressources.html">Ressources</a>
      <a href="rendez-vous.html">Rendez-vous</a>
    </nav>
    <div class="header-actions">
      <button class="mode-calme-toggle" data-mode-calme aria-pressed="false">
        <span aria-hidden="true">◐</span> Mode calme
      </button>
      <a href="dashboard.html" class="btn btn--ghost btn--sm">Mon espace</a>
    </div>
  </div>
</header>
```

## Footer commun (avec cadre éthique)

```html
<footer class="site-footer">
  <div class="container">
    <div class="site-footer__cols">
      <div>
        <p class="brand__name" style="font-size:1.6rem; margin-bottom:1rem;">IV<em>I</em>A</p>
        <p style="opacity:0.75; max-width:32ch; font-family:var(--font-serif); font-style:italic;">
          Au sein de l'être — En actes.
        </p>
        <p style="opacity:0.5; margin-top:1rem; font-size:var(--text-xs); letter-spacing:0.08em;">IN VIVO · IN ACTU</p>
      </div>
      <div>
        <h4>Découvrir</h4>
        <ul>
          <li><a href="#">Notre démarche</a></li>
          <li><a href="#">Praticiens</a></li>
          <li><a href="#">Ressources</a></li>
          <li><a href="#">Outils</a></li>
        </ul>
      </div>
      <div>
        <h4>Pratique</h4>
        <ul>
          <li><a href="rendez-vous.html">Prendre rendez-vous</a></li>
          <li><a href="#">Tarifs</a></li>
          <li><a href="#">FAQ</a></li>
          <li><a href="#">Nous écrire</a></li>
        </ul>
      </div>
      <div>
        <h4>Mentions</h4>
        <ul>
          <li><a href="#">Mentions légales</a></li>
          <li><a href="#">Confidentialité (Loi 25)</a></li>
          <li><a href="#">CGU</a></li>
        </ul>
      </div>
    </div>
    <div class="site-footer__bottom">
      <span>© 2026 IVIA — Pour le peuple, par le peuple.</span>
      <span>IVIA n'est pas un service d'urgence et ne pose pas de diagnostic.</span>
    </div>
  </div>
</footer>
```

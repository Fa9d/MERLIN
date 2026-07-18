# 🏷️ Meta tags SEO — Pages IVIA

> Balises `<title>`, `<meta description>`, Open Graph et Twitter Card pour chaque page.
> Longueur title : max 60 caractères. Description : 120–160 caractères.

---

## Page d'accueil (client)

```html
<title>IVIA — Votre santé mentale, entre les séances</title>
<meta name="description" content="IVIA vous accompagne au quotidien avec des check-ins RGNR, des analyses IA et des ressources cliniques. L'allié de votre praticien.">

<!-- Open Graph -->
<meta property="og:title" content="IVIA — Votre santé mentale, entre les séances">
<meta property="og:description" content="Check-ins RGNR · Analyse MERLIN · Ressources cliniques. Commencez gratuitement.">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_CA">
<meta property="og:image" content="https://ivia.app/assets/og-home.png">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="IVIA — Votre santé mentale entre les séances">
<meta name="twitter:description" content="Suivi RGNR · IA · Ressources validées. Le partenaire de votre thérapeute.">
```

---

## Page Dashboard client

```html
<title>Mon espace IVIA — Tableau de bord santé mentale</title>
<meta name="description" content="Votre tableau de bord RGNR : suivez Corps, Émotions, Pensées et Environnement au quotidien. Votre praticien voit votre progression en temps réel.">
```

---

## Page Check-in RGNR

```html
<title>Check-in RGNR — 3 minutes pour calibrer votre journée | IVIA</title>
<meta name="description" content="Un check-in rapide sur 4 axes : Corps, Émotions, Pensées, Environnement. Analysé par MERLIN, partagé avec votre praticien.">
<meta name="keywords" content="check-in santé mentale, bilan bien-être quotidien, suivi RGNR, routine santé mentale Québec">
```

---

## Page Ma progression

```html
<title>Ma progression RGNR — Évolution sur 30 jours | IVIA</title>
<meta name="description" content="Visualisez votre évolution sur les 4 axes RGNR. Identifiez vos tendances et préparez vos séances en connaissance de cause.">
```

---

## Page Ressources

```html
<title>Ressources cliniques validées — TCC, DBT, ACT | IVIA</title>
<meta name="description" content="Fiches pratiques, exercices et outils cliniques recommandés par votre praticien. Approches TCC, DBT, ACT adaptées à votre profil RGNR.">
<meta name="keywords" content="ressources thérapie cognitive, exercices TCC Québec, outils DBT, pleine conscience santé mentale">
```

---

## Page Praticien (landing)

```html
<title>IVIA pour praticiens — Tableau de bord MERLIN | Psychologues & Coachs</title>
<meta name="description" content="Suivez l'évolution de vos clients entre les séances. Alertes en temps réel, analyse IA MERLIN, pipeline audio. Pour psychologues, thérapeutes et coachs au Québec.">
<meta name="keywords" content="logiciel psychologue Québec, suivi patient thérapie, outil thérapeute IA, dashboard praticien santé mentale">

<meta property="og:title" content="IVIA Praticien — L'IA au service de votre pratique clinique">
<meta property="og:description" content="Alertes MERLIN · Suivi RGNR temps réel · Analyse audio séances. Rejoignez les praticiens IVIA.">
```

---

## Articles de blog (schéma générique)

```html
<!-- Schéma Article (JSON-LD — à placer dans <head>) -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[TITRE ARTICLE]",
  "description": "[META DESCRIPTION]",
  "author": {
    "@type": "Organization",
    "name": "IVIA",
    "url": "https://ivia.app"
  },
  "publisher": {
    "@type": "Organization",
    "name": "IVIA",
    "logo": {
      "@type": "ImageObject",
      "url": "https://ivia.app/assets/logo.svg"
    }
  },
  "inLanguage": "fr-CA",
  "datePublished": "[DATE]",
  "dateModified": "[DATE]"
}
</script>

<!-- FAQ Schema (si article contient une section FAQ) -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[QUESTION]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[RÉPONSE COURTE]"
      }
    }
  ]
}
</script>
```

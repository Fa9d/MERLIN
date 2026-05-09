"""Page démo — anciennement index racine, désormais sous /demo/index.html.
Hub de navigation entre les 3 mockups d'interfaces (client / praticien / admin)
et le funnel d'inscription. Rangé sous /demo/ pour libérer la racine au profit
de la VRAIE landing publique (voir pages_public.py).
"""
from pathlib import Path

OUT = Path(__file__).parent / "demo"

INDEX = '''<!DOCTYPE html>
<html lang="fr-CA" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>IVIA — Démo des 3 interfaces</title>
<meta name="description" content="Démo navigable des 3 interfaces IVIA — client, praticien, admin. Direction visuelle « La Coupe ».">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..600;1,9..144,300..600&family=Lora:ital,wght@0,400..600;1,400..500&family=Inter:wght@300..600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../shared/coupe.css">
<style>
  body { background: linear-gradient(180deg, var(--color-creme) 0%, var(--color-creme-warm) 100%); }
  .index-hero { padding-block: var(--space-24) var(--space-16); text-align: center; }
  .index-hero h1 { font-size: var(--text-2xl); margin-bottom: var(--space-4); }
  .index-hero h1 em { font-style: italic; color: var(--color-rose); }
  .index-hero p { font-family: var(--font-serif); color: var(--color-text-muted); max-width: 56ch; margin-inline: auto; font-size: var(--text-lg); }

  .interfaces-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: var(--space-6); margin-bottom: var(--space-16); }
  .interface-card {
    background: var(--color-surface);
    border: 1px solid var(--color-divider);
    border-radius: var(--radius-xl);
    padding: var(--space-8);
    text-decoration: none;
    color: var(--color-text);
    transition: all var(--transition);
    display: flex;
    flex-direction: column;
    gap: var(--space-4);
    position: relative;
    overflow: hidden;
    cursor: pointer;
  }
  .interface-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-lg); border-color: var(--color-aubergine); }
  .interface-card__title-link { text-decoration: none; color: inherit; }
  .interface-card__title-link:hover h2 { color: var(--color-aubergine); }
  .interface-card__visual {
    aspect-ratio: 16/10;
    border-radius: var(--radius-lg);
    background: linear-gradient(135deg, var(--c1), var(--c2));
    margin-bottom: var(--space-2);
    position: relative;
    overflow: hidden;
  }
  .interface-card__visual::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 70% 30%, rgba(240,233,220,0.4), transparent 60%);
  }
  .interface-card__visual svg { position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0.3; }
  .interface-card__category { font-size: var(--text-xs); letter-spacing: 0.16em; text-transform: uppercase; color: var(--color-rose-deep); }
  .interface-card h2 { font-family: var(--font-display); font-size: var(--text-xl); }
  .interface-card p { font-family: var(--font-serif); color: var(--color-text-muted); font-size: var(--text-sm); }
  .interface-card .pages { display: flex; flex-wrap: wrap; gap: var(--space-2); margin-top: var(--space-2); }
  .interface-card .pages a {
    font-size: var(--text-xs);
    padding: var(--space-1) var(--space-3);
    background: var(--color-surface-warm);
    border-radius: var(--radius-full);
    color: var(--color-text-muted);
    text-decoration: none;
    transition: all var(--transition);
  }
  .interface-card .pages a:hover { background: var(--color-aubergine); color: var(--color-creme); }

  .demo-banner {
    background: var(--color-aubergine);
    color: var(--color-creme);
    padding: var(--space-3) var(--space-4);
    border-radius: var(--radius-md);
    margin-bottom: var(--space-8);
    text-align: center;
    font-family: var(--font-serif);
  }
  .demo-banner a { color: var(--color-creme); text-decoration: underline; font-weight: 600; }

  .legende {
    background: var(--color-surface-2);
    border-radius: var(--radius-lg);
    padding: var(--space-8);
    margin-block: var(--space-12) var(--space-16);
  }
  .legende h2 { font-family: var(--font-display); font-size: var(--text-lg); margin-bottom: var(--space-4); }
  .legende p { font-family: var(--font-serif); color: var(--color-text-muted); margin-bottom: var(--space-4); }
  .legende ul { list-style: none; padding: 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: var(--space-3); }
  .legende li { display: flex; gap: var(--space-3); font-size: var(--text-sm); }
  .legende li strong { color: var(--color-text); }
</style>
</head>
<body>

<div class="vrille-fixe" aria-hidden="true">
  <svg viewBox="0 0 500 800" fill="none" xmlns="http://www.w3.org/2000/svg">
    <defs><linearGradient id="vg" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0%" stop-color="#C58A8A" stop-opacity="0.8"/>
      <stop offset="50%" stop-color="#D9A441" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="#6B8266" stop-opacity="0.4"/>
    </linearGradient></defs>
    <path d="M 250 0 C 100 200, 400 350, 200 500 C 50 650, 350 750, 250 800" stroke="url(#vg)" stroke-width="1.5" fill="none"/>
    <path d="M 280 0 C 130 220, 430 360, 230 510 C 80 660, 380 760, 280 800" stroke="#C58A8A" stroke-width="0.8" stroke-opacity="0.4" fill="none"/>
  </svg>
</div>

<header class="site-header">
  <div class="container site-header__inner">
    <a href="../index.html" class="brand">
      <svg class="brand__mark" viewBox="0 0 36 36" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true">
        <circle cx="18" cy="18" r="14.5" stroke-opacity="0.4"/>
        <path d="M18 4.5 C 11 12, 25 24, 18 31.5" stroke-linecap="round"/>
        <path d="M11 18 C 14 16, 22 20, 25 18" stroke-linecap="round" stroke-opacity="0.7"/>
        <circle cx="18" cy="18" r="2.5" fill="currentColor" stroke="none"/>
      </svg>
      <span class="brand__name">IV<em>I</em>A</span>
      <span style="margin-left: var(--space-3); font-size: var(--text-xs); color: var(--color-text-muted); letter-spacing: 0.12em; text-transform: uppercase;">Démo · La Coupe</span>
    </a>
    <div class="header-actions">
      <a href="../index.html" class="btn btn--ghost btn--sm">↩ Site public</a>
      <a href="../tests.html" class="btn btn--ghost btn--sm">Espace tests</a>
      <button class="mode-calme-toggle" data-mode-calme aria-pressed="false">
        <span aria-hidden="true">◐</span> Mode calme
      </button>
    </div>
  </div>
</header>

<main class="container container--default">

  <p class="demo-banner">
    Vous êtes dans la <strong>démo développeur</strong> — toutes les pages d'un coup. Pour les tests réels, allez dans l'<a href="../tests.html">espace tests</a> ou voyez la <a href="../index.html">vraie landing publique</a>.
  </p>

  <section class="index-hero">
    <p class="eyebrow">Wireframe sensoriel · 9 mai 2026</p>
    <h1>Trois <em>portes</em>, une seule maison.</h1>
    <p>
      Démo navigable des trois interfaces IVIA — la voix publique pour les personnes accompagnées,
      l'espace de travail des praticien·ne·s, et le pilotage de la maison.
      Direction visuelle « La Coupe » : palette botanique, typographie éditoriale, présence sensible.
    </p>
  </section>

  <section class="interfaces-grid">

    <div class="interface-card" data-href="../client/index.html" style="--c1:#C58A8A; --c2:#D89260;">
      <div class="interface-card__visual">
        <svg viewBox="0 0 200 125" fill="none" stroke="white" stroke-width="0.5">
          <circle cx="100" cy="62" r="50"/><circle cx="100" cy="62" r="35"/><circle cx="100" cy="62" r="20"/>
          <path d="M 30 62 Q 100 20, 170 62 T 30 62"/>
        </svg>
      </div>
      <p class="interface-card__category">Interface 1 · Public</p>
      <a href="../client/index.html" class="interface-card__title-link"><h2>Côté client</h2></a>
      <p>Pour les personnes qui cherchent une écoute. Le visage public d'IVIA — promesse, voies, audio asynchrone, journal de vie.</p>
      <div class="pages">
        <a href="../client/index.html">Accueil</a>
        <a href="../client/praticiens.html">Praticiens</a>
        <a href="../client/rendez-vous.html">Rendez-vous</a>
        <a href="../client/audio-async.html">Audio async</a>
        <a href="../client/audio-resume.html">Résumé reçu</a>
        <a href="../client/dashboard.html">Mon espace</a>
        <a href="../client/journal.html">Journal</a>
        <a href="../client/ressources.html">Ressources</a>
      </div>
    </div>

    <div class="interface-card" data-href="../praticien/index.html" style="--c1:#6B8266; --c2:#8DA9B8;">
      <div class="interface-card__visual">
        <svg viewBox="0 0 200 125" fill="none" stroke="white" stroke-width="0.5">
          <rect x="25" y="20" width="150" height="85" rx="4"/>
          <line x1="25" y1="40" x2="175" y2="40"/>
          <line x1="55" y1="40" x2="55" y2="105"/>
          <line x1="25" y1="55" x2="55" y2="55"/><line x1="25" y1="75" x2="55" y2="75"/><line x1="25" y1="90" x2="55" y2="90"/>
          <rect x="65" y="50" width="100" height="20" rx="2" fill="white" fill-opacity="0.2"/>
          <rect x="65" y="78" width="65" height="16" rx="2" fill="white" fill-opacity="0.15"/>
        </svg>
      </div>
      <p class="interface-card__category">Interface 2 · Pro · accessible</p>
      <a href="../praticien/index.html" class="interface-card__title-link"><h2>Côté praticien·ne</h2></a>
      <p>Espace de travail des écoutant·e·s. Agenda, audios à traiter, fiches clients, abonnement mensuel — soigné, jamais médicalisé.</p>
      <div class="pages">
        <a href="../praticien/index.html">Tableau de bord</a>
        <a href="../praticien/agenda.html">Agenda</a>
        <a href="../praticien/audios.html">Audios à traiter</a>
        <a href="../praticien/audio-traiter.html">Répondre à un audio</a>
        <a href="../praticien/clients.html">Mes clients</a>
        <a href="../praticien/outils.html">Outils</a>
        <a href="../praticien/abonnement.html">Mon abonnement</a>
      </div>
    </div>

    <div class="interface-card" data-href="../admin/index.html" style="--c1:#9A8AB8; --c2:#7B5B7E;">
      <div class="interface-card__visual">
        <svg viewBox="0 0 200 125" fill="none" stroke="white" stroke-width="0.5">
          <rect x="25" y="25" width="40" height="20" rx="2" fill="white" fill-opacity="0.15"/>
          <rect x="75" y="25" width="40" height="20" rx="2" fill="white" fill-opacity="0.15"/>
          <rect x="125" y="25" width="40" height="20" rx="2" fill="white" fill-opacity="0.15"/>
          <path d="M 30 95 L 60 80 L 90 70 L 120 60 L 150 50 L 175 42" stroke-width="1"/>
          <line x1="25" y1="100" x2="175" y2="100" stroke-opacity="0.3"/>
        </svg>
      </div>
      <p class="interface-card__category">Interface 3 · Pilotage</p>
      <a href="../admin/index.html" class="interface-card__title-link"><h2>Côté admin</h2></a>
      <p>Pilotage de la maison. Praticien·ne·s, clients, audios, finance, paramètres doctrinaires & Loi 25 — sans accès au contenu des notes.</p>
      <div class="pages">
        <a href="../admin/index.html">Vue d'ensemble</a>
        <a href="../admin/analytique.html">Analytique</a>
        <a href="../admin/praticiens.html">Praticiens</a>
        <a href="../admin/clients.html">Clients</a>
        <a href="../admin/audios.html">Audios</a>
        <a href="../admin/finance.html">Finance</a>
        <a href="../admin/parametres.html">Paramètres</a>
      </div>
    </div>

  </section>

  <section class="legende">
    <h2>Notes de lecture</h2>
    <p>
      Cette démo regroupe en un seul endroit toutes les pages des 3 interfaces IVIA. Pour la
      <strong>vraie landing publique</strong>, c'est <a href="../index.html">ici</a>. Pour
      <strong>tester comme un·e utilisateur·ice</strong> avec un compte fictif déjà connecté,
      c'est dans <a href="../tests.html">l'espace tests</a>.
    </p>
    <ul>
      <li><strong>Palette :</strong> Crème · Aubergine · Bois de rose · Mousse · Glacier · Lavande</li>
      <li><strong>Typo :</strong> Fraunces (display) · Lora (serif éditorial) · Inter (UI)</li>
      <li><strong>Mode Calme :</strong> bouton dans l'en-tête de chaque page · désature & coupe les animations</li>
      <li><strong>Vrille décorative :</strong> Le Fil reborn — fixe à droite ≥ 1200 px · respire toutes les 16 s</li>
      <li><strong>Cadre éthique :</strong> mention « pas un service d'urgence · pas de diagnostic » obligatoire et présente partout</li>
      <li><strong>Frontières discours :</strong> vocabulaire OK & vocabulaire à éviter listé dans Admin → Paramètres → Doctrine</li>
      <li><strong>Audio asynchrone :</strong> flux complet — enregistrement → attente → résumé reçu → conversion</li>
      <li><strong>Données fictives :</strong> tous noms, montants, dates, statistiques sont des placeholders crédibles</li>
    </ul>
  </section>

  <p style="text-align:center; font-family:var(--font-serif); color:var(--color-text-muted); font-style:italic; margin-bottom: var(--space-16);">
    Au sein de l'être — En actes.
  </p>

</main>

<script src="../shared/coupe.js"></script>
<script>
  // Carte cliquable : clic sur fond -> navigue. Les <a> internes restent prioritaires.
  document.querySelectorAll('.interface-card[data-href]').forEach(card => {
    card.addEventListener('click', (e) => {
      if (e.target.closest('a')) return;
      window.location = card.dataset.href;
    });
  });
</script>
</body>
</html>
'''


def build():
    OUT.mkdir(exist_ok=True)
    (OUT / "index.html").write_text(INDEX, encoding="utf-8")

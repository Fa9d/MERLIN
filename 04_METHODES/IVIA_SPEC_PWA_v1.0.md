# SPÉCIFICATION TECHNIQUE — PWA IVIA
## Progressive Web App : architecture, implémentation, conformité

**Version** : 1.0  
**Date** : 9 mai 2026  
**Statut** : Spécification technique — Implémentation phase pilote  
**Auteur** : David Phaneuf (fondateur) + Perplexity Computer (analyse technique)  
**Contexte** : Extension PWA du site ivia.pplx.app (Python build_pages.py + pages_*.py)  
**Cohérence** : Aligné avec `IVIA_DECISION_MOBILE_PWA_VS_NATIF_v1.0.md`, `IVIA_STRATEGIE_TECHNOLOGIQUE_36MOIS_v1.0.md`

---

## 1. VUE D'ENSEMBLE ARCHITECTURE

### 1.1 Architecture actuelle (Python build statique)

```
ivia_mockups/
├── build_pages.py          # Générateur principal — produit les HTML
├── page_index.py           # Page d'accueil
├── pages_public.py         # Pages publiques (pourquoi, services, etc.)
├── pages_praticien.py      # Interface praticiens
├── pages_client.py         # Interface clients
├── pages_admin.py          # Interface admin
├── pages_funnel.py         # Funnel quiz-to-guidance
└── articles_meta.py        # Métadonnées articles
```

Le build génère des fichiers HTML statiques servis sur ivia.pplx.app. La PWA s'ajoute sans modifier cette architecture — elle étend le build avec 4 fichiers nouveaux et des modifications ciblées.

### 1.2 Architecture cible (PWA étendue)

```
ivia_mockups/
├── build_pages.py          # Modifié : injection manifest + SW meta tags
├── [pages existantes...]
├── pages_pwa.py            # NOUVEAU : génère manifest.json, sw.js, offline.html
├── static/
│   ├── manifest.json       # NOUVEAU : déclaration PWA
│   ├── sw.js               # NOUVEAU : Service Worker
│   ├── offline.html        # NOUVEAU : page hors ligne
│   └── icons/              # NOUVEAU : icônes 8 tailles
│       ├── icon-72.png
│       ├── icon-96.png
│       ├── icon-128.png
│       ├── icon-144.png
│       ├── icon-152.png
│       ├── icon-192.png
│       ├── icon-384.png
│       ├── icon-512.png
│       ├── icon-192-maskable.png
│       ├── icon-512-maskable.png
│       └── icon.svg
└── push_backend/           # NOUVEAU : backend FastAPI notifications
    ├── main.py
    ├── vapid_keys.py
    └── requirements.txt
```

### 1.3 Modifications à build_pages.py

Chaque page HTML doit inclure dans `<head>` :

```html
<!-- PWA -->
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#C58A8A">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="IVIA">
<link rel="apple-touch-icon" href="/static/icons/icon-192.png">
<link rel="apple-touch-icon" sizes="152x152" href="/static/icons/icon-152.png">

<!-- Service Worker -->
<script>
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/sw.js')
        .catch(err => console.warn('SW registration failed:', err));
    });
  }
</script>
```

---

## 2. MANIFEST.JSON

```json
{
  "name": "IVIA — Accompagnement non-clinique",
  "short_name": "IVIA",
  "description": "Plateforme québécoise d'accompagnement non-clinique. Au sein de l'être — En actes.",
  "lang": "fr-CA",
  "start_url": "/",
  "scope": "/",
  "display": "standalone",
  "orientation": "portrait-primary",
  "theme_color": "#C58A8A",
  "background_color": "#FAF8F4",
  "categories": ["health", "lifestyle"],
  "icons": [
    {
      "src": "/static/icons/icon-72.png",
      "sizes": "72x72",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/static/icons/icon-96.png",
      "sizes": "96x96",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/static/icons/icon-128.png",
      "sizes": "128x128",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/static/icons/icon-144.png",
      "sizes": "144x144",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/static/icons/icon-152.png",
      "sizes": "152x152",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/static/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/static/icons/icon-192-maskable.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "maskable"
    },
    {
      "src": "/static/icons/icon-384.png",
      "sizes": "384x384",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/static/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/static/icons/icon-512-maskable.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "maskable"
    },
    {
      "src": "/static/icons/icon.svg",
      "sizes": "any",
      "type": "image/svg+xml",
      "purpose": "any"
    }
  ],
  "shortcuts": [
    {
      "name": "Praticiens",
      "short_name": "Praticiens",
      "description": "Trouver un praticien IVIA",
      "url": "/praticiens",
      "icons": [
        {
          "src": "/static/icons/icon-96.png",
          "sizes": "96x96"
        }
      ]
    },
    {
      "name": "Quiz",
      "short_name": "Quiz",
      "description": "Démarrer le questionnaire d'orientation",
      "url": "/quiz",
      "icons": [
        {
          "src": "/static/icons/icon-96.png",
          "sizes": "96x96"
        }
      ]
    }
  ],
  "screenshots": [
    {
      "src": "/static/screenshots/home-mobile.png",
      "sizes": "390x844",
      "type": "image/png",
      "form_factor": "narrow",
      "label": "Accueil IVIA sur mobile"
    },
    {
      "src": "/static/screenshots/praticiens-mobile.png",
      "sizes": "390x844",
      "type": "image/png",
      "form_factor": "narrow",
      "label": "Page praticiens IVIA"
    }
  ],
  "prefer_related_applications": false
}
```

**Notes manifest :**
- `prefer_related_applications: false` : indique au navigateur de préférer la PWA à toute app store équivalente
- `background_color: #FAF8F4` : couleur du splash screen au démarrage (doit correspondre au fond CSS du site)
- `screenshots` : requis pour l'installation in-app sur Android et pour le futur PWA in store (Chrome Web Store)
- `shortcuts` : accessibles via un appui long sur l'icône (Android) et le menu de partage (iOS 16+)

---

## 3. ICÔNES — PALETTE ET PRODUCTION

### 3.1 Palette IVIA dérivée

La palette est extraite de la vrille SVG dans build_pages.py :

| Rôle | Couleur hex | Usage |
|---|---|---|
| Rose rosé (primaire) | `#C58A8A` | Fond icône, theme_color |
| Ocre doré | `#D9A441` | Accent, gradient icône |
| Vert sauge | `#6B8266` | Accent secondaire |
| Mauve subtil | `#9A8AB8` | Accent tertiaire |
| Fond clair | `#FAF8F4` | background_color manifest |

### 3.2 Logique visuelle icône

L'icône reprend le logo SVG IVIA (cercle + vrille + point central) sur fond `#C58A8A`, légèrement désaturé pour les petites tailles. Version maskable : zone safe area de 40 % (le logo doit tenir dans le cercle central de 60 % de la surface pour ne pas être coupé par les masques Android adaptatifs).

### 3.3 Production icônes

Outil recommandé : PWA Builder (pwabuilder.com) — génère les 10 tailles à partir du SVG source en un clic. Outil alternatif : Maskable.app pour valider les zones safe de l'icône maskable.

```
Tailles requises : 72, 96, 128, 144, 152, 192, 384, 512 (px × px)
Formats : PNG (toutes tailles) + SVG (fallback "any")
Variantes : any (fond plein) + maskable (zone safe 60 %)
Total fichiers : 10 PNG + 1 SVG = 11 fichiers icônes
```

---

## 4. SERVICE WORKER (sw.js)

### 4.1 Stratégies de cache

| Ressource | Stratégie | Justification |
|---|---|---|
| HTML (pages) | Network-first | Contenu qui doit rester à jour — SW sert le cache uniquement si le réseau est indisponible |
| CSS, JS, fonts | Cache-first | Assets statiques versionnés — charge immédiate, mise à jour via versioning |
| Images | Cache-first | Images optimisées, rarement modifiées |
| Audio praticiens (.opus) | Stale-while-revalidate | Sert le cache immédiatement, met à jour en arrière-plan |
| API calls (/api/*) | Network-only | Données en temps réel, pas de cache |

### 4.2 sw.js complet

```javascript
// sw.js — Service Worker IVIA v1.0
// Stratégies : network-first (HTML), cache-first (assets), stale-while-revalidate (audio)

const CACHE_VERSION = 'ivia-v1.0.0';
const SHELL_CACHE = `${CACHE_VERSION}-shell`;
const AUDIO_CACHE = `${CACHE_VERSION}-audio`;
const RUNTIME_CACHE = `${CACHE_VERSION}-runtime`;

// App shell : ressources précachées à l'installation
const APP_SHELL = [
  '/',
  '/index.html',
  '/praticiens',
  '/quiz',
  '/offline.html',
  '/static/css/main.css',
  '/static/js/main.js',
  '/static/icons/icon-192.png',
  '/static/icons/icon-512.png',
  '/manifest.json',
];

// Audio praticiens : précachés pour lecture offline
// Pilote : 5 praticiens × ~200 Ko Opus = ~1 Mo footprint
const AUDIO_SHELL = [
  '/static/audio/praticien-01-intro.opus',
  '/static/audio/praticien-02-intro.opus',
  '/static/audio/praticien-03-intro.opus',
  '/static/audio/praticien-04-intro.opus',
  '/static/audio/praticien-05-intro.opus',
];

// ── Installation ──────────────────────────────────────────────────────────────
self.addEventListener('install', event => {
  event.waitUntil(
    Promise.all([
      caches.open(SHELL_CACHE).then(cache => cache.addAll(APP_SHELL)),
      caches.open(AUDIO_CACHE).then(cache => cache.addAll(AUDIO_SHELL)),
    ]).then(() => self.skipWaiting())
  );
});

// ── Activation (nettoyage anciens caches) ─────────────────────────────────────
self.addEventListener('activate', event => {
  const validCaches = [SHELL_CACHE, AUDIO_CACHE, RUNTIME_CACHE];
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys
          .filter(key => !validCaches.includes(key))
          .map(key => caches.delete(key))
      )
    ).then(() => self.clients.claim())
  );
});

// ── Fetch (routage des requêtes) ──────────────────────────────────────────────
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // Ignorer les requêtes non-GET et les API
  if (request.method !== 'GET') return;
  if (url.pathname.startsWith('/api/')) return;
  if (url.pathname.startsWith('/push/')) return;

  // Audio : stale-while-revalidate
  if (url.pathname.startsWith('/static/audio/')) {
    event.respondWith(staleWhileRevalidate(request, AUDIO_CACHE));
    return;
  }

  // Assets statiques (CSS, JS, images, icônes) : cache-first
  if (
    url.pathname.startsWith('/static/') ||
    url.pathname.startsWith('/icons/') ||
    url.pathname === '/manifest.json'
  ) {
    event.respondWith(cacheFirst(request, SHELL_CACHE));
    return;
  }

  // HTML et navigation : network-first, fallback offline.html
  if (request.headers.get('accept')?.includes('text/html')) {
    event.respondWith(networkFirstWithOfflineFallback(request));
    return;
  }

  // Tout le reste : network-first
  event.respondWith(networkFirst(request, RUNTIME_CACHE));
});

// ── Stratégies ────────────────────────────────────────────────────────────────

async function cacheFirst(request, cacheName) {
  const cached = await caches.match(request);
  if (cached) return cached;
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, response.clone());
    }
    return response;
  } catch {
    return new Response('Ressource non disponible hors ligne.', { status: 503 });
  }
}

async function networkFirst(request, cacheName) {
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, response.clone());
    }
    return response;
  } catch {
    const cached = await caches.match(request);
    return cached || new Response('Hors ligne.', { status: 503 });
  }
}

async function networkFirstWithOfflineFallback(request) {
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(SHELL_CACHE);
      cache.put(request, response.clone());
    }
    return response;
  } catch {
    const cached = await caches.match(request);
    if (cached) return cached;
    return caches.match('/offline.html');
  }
}

async function staleWhileRevalidate(request, cacheName) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(request);
  const networkPromise = fetch(request).then(response => {
    if (response.ok) cache.put(request, response.clone());
    return response;
  });
  return cached || networkPromise;
}

// ── Notifications push ────────────────────────────────────────────────────────
self.addEventListener('push', event => {
  if (!event.data) return;
  const data = event.data.json();
  const options = {
    body: data.body || '',
    icon: '/static/icons/icon-192.png',
    badge: '/static/icons/icon-96.png',
    tag: data.tag || 'ivia-notification',
    data: { url: data.url || '/' },
    requireInteraction: false,
    vibrate: [200, 100, 200],
  };
  event.waitUntil(
    self.registration.showNotification(data.title || 'IVIA', options)
  );
});

self.addEventListener('notificationclick', event => {
  event.notification.close();
  const url = event.notification.data?.url || '/';
  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then(clientList => {
      const existingClient = clientList.find(c => c.url === url && 'focus' in c);
      if (existingClient) return existingClient.focus();
      return clients.openWindow(url);
    })
  );
});
```

### 4.3 Gestion des versions

Le champ `CACHE_VERSION` doit être mis à jour à chaque déploiement. Convention :

```
ivia-v{MAJEUR}.{MINEUR}.{PATCH}
```

Exemple : `ivia-v1.0.0` → `ivia-v1.0.1` après un patch CSS. L'activation du nouveau SW supprime automatiquement les anciens caches.

---

## 5. AUDIO OFFLINE — ARCHITECTURE

### 5.1 Spécifications techniques

| Paramètre | Valeur |
|---|---|
| Format | Opus (WebM container) |
| Débit | 32 kbps mono (voix uniquement) |
| Durée visée | ~60 secondes par échantillon |
| Taille estimée | ~200 Ko par fichier |
| Nombre pilote | 5 praticiens × 1 échantillon = 5 fichiers |
| Footprint total pilote | ~1 Mo |
| Footprint production (20 praticiens) | ~4 Mo |

### 5.2 Pourquoi Opus

Opus est le codec audio ouvert de référence pour le web. Il est supporté par tous les navigateurs cibles (Chrome, Firefox, Edge, Safari 15.4+). À 32 kbps, la qualité vocale est excellente. MP3 à qualité équivalente pèserait 2 à 3 fois plus. AAC serait une alternative pour iOS mais Opus est désormais supporté nativement par iOS/Safari depuis 2022.

### 5.3 Mise à jour des fichiers audio

Problème : si un praticien met à jour son échantillon audio, le Service Worker peut servir l'ancien fichier depuis le cache.

Solution : nommage avec hash de contenu.

```
/static/audio/praticien-01-intro.{sha256[:8]}.opus
```

Exemple : `praticien-01-intro.a3f7c2b1.opus`

Quand le fichier est mis à jour, le hash change, le SW détecte une nouvelle URL et met à jour le cache. L'ancienne version est supprimée lors de l'activation du SW suivant.

Le manifest audio (liste des fichiers courants) est servi depuis `/api/audio-manifest.json` en network-only — le SW peut ainsi détecter les changements et déclencher une mise à jour du cache audio.

---

## 6. NOTIFICATIONS PUSH

### 6.1 Architecture Web Push + VAPID

```
[Client navigateur]
      |
      | 1. Opt-in utilisateur → navigator.serviceWorker.ready
      |    .then(reg => reg.pushManager.subscribe({
      |      userVisibleOnly: true,
      |      applicationServerKey: VAPID_PUBLIC_KEY
      |    }))
      |
      | 2. Subscription envoyée au backend IVIA
      ↓
[Backend FastAPI IVIA — push_backend/main.py]
      |
      | 3. Stockage subscription (PostgreSQL ou SQLite chiffré)
      |
      | 4. Déclenchement (RDV, message praticien, fin exercice)
      |    → pywebpush.webpush(subscription_info, data, vapid_private_key)
      ↓
[Service Push (FCM pour Chrome/Android, APNs pour Safari/iOS)]
      ↓
[Service Worker sw.js — événement 'push']
      ↓
[Notification affichée sur l'écran de l'utilisateur]
```

### 6.2 Backend FastAPI — push_backend/main.py

```python
# push_backend/main.py — Backend push VAPID IVIA (simplifié)
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pywebpush import webpush, WebPushException
import json, os

app = FastAPI(title="IVIA Push Backend")

# Configuration CORS stricte
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ivia.pplx.app"],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

VAPID_PRIVATE_KEY = os.environ["VAPID_PRIVATE_KEY"]
VAPID_PUBLIC_KEY  = os.environ["VAPID_PUBLIC_KEY"]
VAPID_CLAIMS      = {"sub": "mailto:david@ivia.ca"}

# Stockage en mémoire pour le pilote — remplacer par DB en production
subscriptions: dict[str, dict] = {}

class Subscription(BaseModel):
    user_id: str
    subscription: dict
    categories: list[str] = ["rdv", "message", "exercice"]

class PushPayload(BaseModel):
    user_id: str
    title: str
    body: str
    url: str = "/"
    tag: str = "ivia"
    category: str = "rdv"

@app.post("/push/subscribe")
async def subscribe(sub: Subscription):
    subscriptions[sub.user_id] = {
        "subscription": sub.subscription,
        "categories": sub.categories,
    }
    return {"status": "subscribed"}

@app.post("/push/send")
async def send_push(payload: PushPayload):
    record = subscriptions.get(payload.user_id)
    if not record:
        raise HTTPException(404, "Utilisateur non abonné")
    if payload.category not in record["categories"]:
        return {"status": "skipped", "reason": "category_not_subscribed"}
    try:
        webpush(
            subscription_info=record["subscription"],
            data=json.dumps({
                "title": payload.title,
                "body": payload.body,
                "url": payload.url,
                "tag": payload.tag,
            }),
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims=VAPID_CLAIMS,
        )
        return {"status": "sent"}
    except WebPushException as e:
        raise HTTPException(500, str(e))

@app.post("/push/broadcast")
async def broadcast(payload: dict):
    """Envoi à tous les abonnés d'une catégorie — usage admin uniquement."""
    # Authentification admin requise en production
    results = []
    for uid, record in subscriptions.items():
        if payload.get("category", "rdv") in record["categories"]:
            results.append(await send_push(PushPayload(user_id=uid, **payload)))
    return {"sent": len(results)}
```

### 6.3 Génération des clés VAPID

```bash
# Installation
pip install py-vapid

# Génération
vapid --gen

# Produit deux fichiers :
# private_key.pem  → VAPID_PRIVATE_KEY (variable d'environnement, jamais committé)
# public_key.pem   → VAPID_PUBLIC_KEY (utilisé dans le frontend manifest push)
```

Les clés VAPID ne doivent jamais être committées dans le repo. Elles sont stockées comme variables d'environnement sécurisées sur l'hébergeur.

### 6.4 Opt-in côté client (conforme Loi 25)

```javascript
// push-consent.js — Opt-in granulaire conforme Loi 25
// Déclenché depuis la page "Mes notifications" (/notifications), jamais au chargement

const VAPID_PUBLIC_KEY = 'VOTRE_CLE_PUBLIQUE_VAPID_BASE64URL';

async function subscribeToPush(categories = ['rdv', 'message']) {
  if (!('PushManager' in window)) {
    console.warn('Push non supporté sur ce navigateur.');
    return null;
  }

  // Demander la permission seulement si pas déjà accordée
  if (Notification.permission === 'denied') {
    showPushBlockedMessage();
    return null;
  }

  const permission = await Notification.requestPermission();
  if (permission !== 'granted') return null;

  const registration = await navigator.serviceWorker.ready;
  const subscription = await registration.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: urlBase64ToUint8Array(VAPID_PUBLIC_KEY),
  });

  // Envoyer la subscription au backend avec les catégories choisies
  await fetch('/push/subscribe', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: getCurrentUserId(),
      subscription: subscription.toJSON(),
      categories,
    }),
  });

  return subscription;
}

function urlBase64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');
  const rawData = atob(base64);
  return Uint8Array.from([...rawData].map(c => c.charCodeAt(0)));
}
```

### 6.5 Cas d'usage notifications — phase pilote

| Événement | Titre | Corps | URL cible |
|---|---|---|---|
| Rappel rendez-vous (24 h avant) | "Votre séance demain" | "Rappel : séance avec [Prénom praticien] demain à [heure]" | `/mon-espace/rdv` |
| Message du praticien | "Message de [Prénom]" | "Votre praticien vous a laissé un message." | `/mon-espace/messages` |
| Fin d'exercice (timer) | "Exercice terminé" | "Votre exercice de [durée] est terminé." | `/exercices` |
| Nouveau contenu disponible | "Nouveau sur IVIA" | "Un nouvel article de [praticien] est disponible." | `/articles` |

---

## 7. INSTALLATION — INSTRUCTIONS PAR PLATEFORME

### 7.1 iOS Safari (instructions visuelles requises)

iOS ne propose pas de bannière automatique d'installation. L'utilisateur doit suivre une procédure manuelle. IVIA doit afficher ces instructions dans l'interface.

```html
<!-- Composant d'installation iOS — affiché uniquement sur iOS Safari non installé -->
<div id="ios-install-prompt" class="install-prompt" hidden>
  <div class="install-prompt__content">
    <img src="/static/icons/icon-96.png" alt="IVIA" class="install-prompt__icon">
    <div class="install-prompt__text">
      <strong>Installer IVIA sur votre iPhone</strong>
      <ol class="install-steps">
        <li>Appuyez sur <strong>Partager</strong> 
            <img src="/static/icons/ios-share.svg" alt="icône Partager" class="inline-icon">
            en bas de l'écran</li>
        <li>Faites défiler et appuyez sur <strong>Sur l'écran d'accueil</strong></li>
        <li>Appuyez sur <strong>Ajouter</strong> en haut à droite</li>
      </ol>
    </div>
  </div>
  <button id="ios-install-dismiss" class="install-prompt__dismiss">Plus tard</button>
</div>

<script>
// Détecter iOS Safari non installé
const isIOS = /iphone|ipad|ipod/i.test(navigator.userAgent);
const isStandalone = window.navigator.standalone === true;
const isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);

if (isIOS && isSafari && !isStandalone) {
  // Afficher après 30 secondes sur le site, pas à chaque visite
  const lastPrompt = localStorage.getItem('ivia_ios_prompt_shown');
  const now = Date.now();
  if (!lastPrompt || now - parseInt(lastPrompt) > 7 * 24 * 60 * 60 * 1000) {
    setTimeout(() => {
      document.getElementById('ios-install-prompt').removeAttribute('hidden');
      localStorage.setItem('ivia_ios_prompt_shown', now.toString());
    }, 30000);
  }
}

document.getElementById('ios-install-dismiss')?.addEventListener('click', () => {
  document.getElementById('ios-install-prompt').setAttribute('hidden', '');
});
</script>
```

### 7.2 Android Chrome (beforeinstallprompt automatique)

```javascript
// install-android.js — Gestion du prompt Android natif
let deferredPrompt = null;
const installButton = document.getElementById('android-install-btn');

window.addEventListener('beforeinstallprompt', event => {
  event.preventDefault();
  deferredPrompt = event;
  // Afficher un bouton "Installer IVIA" discret dans le header ou le footer
  if (installButton) installButton.hidden = false;
});

installButton?.addEventListener('click', async () => {
  if (!deferredPrompt) return;
  deferredPrompt.prompt();
  const { outcome } = await deferredPrompt.userChoice;
  if (outcome === 'accepted') {
    installButton.hidden = true;
    // Analytics interne (sans Google Analytics) : incrémenter compteur installations
    fetch('/api/metrics/install', { method: 'POST' });
  }
  deferredPrompt = null;
});

window.addEventListener('appinstalled', () => {
  deferredPrompt = null;
  if (installButton) installButton.hidden = true;
});
```

---

## 8. DÉTECTION EN LIGNE / HORS LIGNE

### 8.1 Banner statut connexion

```javascript
// connectivity.js — Banner état connexion
function updateConnectionStatus() {
  const banner = document.getElementById('offline-banner');
  if (!banner) return;
  if (navigator.onLine) {
    banner.setAttribute('hidden', '');
    banner.removeAttribute('aria-live');
  } else {
    banner.removeAttribute('hidden');
    banner.setAttribute('aria-live', 'assertive');
  }
}

window.addEventListener('online',  updateConnectionStatus);
window.addEventListener('offline', updateConnectionStatus);
updateConnectionStatus(); // état initial
```

```html
<!-- Banner offline — à inclure dans toutes les pages via build_pages.py -->
<div id="offline-banner" class="offline-banner" hidden role="status">
  Vous êtes hors ligne. Certaines fonctionnalités sont limitées.
  L'audio et les pages visitées restent disponibles.
</div>
```

### 8.2 Page offline.html

```html
<!DOCTYPE html>
<html lang="fr-CA">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Hors ligne — IVIA</title>
  <link rel="stylesheet" href="/static/css/main.css">
  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#C58A8A">
</head>
<body class="offline-page">
  <main class="offline-container">
    <img src="/static/icons/icon-192.png" alt="IVIA" class="offline-logo">
    <h1>Vous êtes hors ligne</h1>
    <p>
      La connexion réseau est momentanément indisponible. 
      L'audio de vos praticiens reste accessible si vous l'avez déjà écouté.
    </p>
    <p class="offline-hint">
      Vos pages visitées récemment sont également disponibles.
      Reconnectez-vous pour accéder au reste de la plateforme.
    </p>
    <button onclick="location.reload()" class="btn btn--primary">
      Réessayer
    </button>
  </main>
</body>
</html>
```

---

## 9. PERFORMANCE — CIBLES ET AUDIT

### 9.1 Cibles Lighthouse

| Critère | Cible | Outil de mesure |
|---|---|---|
| Performance | > 90 | Lighthouse CLI / DevTools |
| Accessibilité | > 90 | Lighthouse, axe-core |
| Bonnes pratiques | > 90 | Lighthouse |
| SEO | > 90 | Lighthouse |
| PWA | 100 % des critères | Lighthouse PWA audit |
| LCP (Largest Contentful Paint) | < 2.5 s | Web Vitals |
| FID / INP (Interaction to Next Paint) | < 200 ms | Web Vitals |
| CLS (Cumulative Layout Shift) | < 0.1 | Web Vitals |
| TTFB (Time to First Byte) | < 800 ms | WebPageTest |

### 9.2 Optimisations requises

- Images en WebP avec `<picture>` + fallback PNG
- CSS critique inline (above-the-fold) pour éviter le render-blocking
- Fonts subsettées (latin + latin-ext uniquement pour le français québécois)
- Lazy loading sur les images hors viewport (`loading="lazy"`)
- Compression gzip ou brotli activée sur le serveur
- `rel="preload"` sur la font principale et le CSS critique
- `dns-prefetch` sur les domaines tiers (si présents)

---

## 10. SÉCURITÉ

### 10.1 HTTPS

Obligatoire pour toute PWA. ivia.pplx.app est déjà HTTPS via Let's Encrypt. Le renouvellement automatique doit être vérifié.

### 10.2 Content Security Policy (CSP)

```
Content-Security-Policy:
  default-src 'self';
  script-src 'self' 'nonce-{NONCE}';
  style-src 'self' 'nonce-{NONCE}';
  img-src 'self' data: blob:;
  media-src 'self' blob:;
  connect-src 'self' https://ivia.pplx.app;
  font-src 'self';
  manifest-src 'self';
  worker-src 'self';
  frame-ancestors 'none';
```

Le nonce est généré côté serveur à chaque requête. Les scripts inline doivent utiliser ce nonce, pas `'unsafe-inline'`.

### 10.3 Headers de sécurité

```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(self), microphone=(self), camera=(self),
                    push=(self), notifications=(self)
```

### 10.4 Subresource Integrity (SRI)

Pour toute dépendance externe chargée depuis un CDN :

```html
<script
  src="https://cdn.example.com/lib.js"
  integrity="sha384-[HASH]"
  crossorigin="anonymous">
</script>
```

La politique IVIA préfère héberger les dépendances en local (dans `/static/`) pour éliminer le besoin de SRI et réduire les dépendances tierces.

---

## 11. CONFORMITÉ LOI 25

### 11.1 Principes appliqués à la PWA

| Exigence Loi 25 | Implémentation PWA |
|---|---|
| Pas de collecte sans consentement | Aucun tracker par défaut. Pas de Google Analytics. |
| Consentement explicite pour push | Opt-in sur page dédiée `/notifications`, jamais au chargement |
| Droit à l'effacement | Endpoint `/push/unsubscribe` qui supprime la subscription du backend |
| Stockage minimal | localStorage uniquement pour préférences UI (pas de données personnelles) |
| Données sensibles chiffrées | IndexedDB chiffré via Web Crypto API pour données de séance |
| Localisation des données | Backend push hébergé au Canada (voir décision `IVIA_DECISION_MOBILE_PWA_VS_NATIF_v1.0.md` §7.1) |
| Transparence | Politique de confidentialité mise à jour mentionnant les notifications push |

### 11.2 IndexedDB chiffré pour données sensibles

Si des données de séance sont stockées localement (notes offline, journal parcours client), elles doivent être chiffrées via Web Crypto API :

```javascript
// crypto-storage.js — Stockage IndexedDB chiffré (simplifié)
async function encryptAndStore(db, key, data) {
  const cryptoKey = await getCryptoKey(); // clé dérivée du token session utilisateur
  const encoded = new TextEncoder().encode(JSON.stringify(data));
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const encrypted = await crypto.subtle.encrypt(
    { name: 'AES-GCM', iv },
    cryptoKey,
    encoded
  );
  const tx = db.transaction('sessions', 'readwrite');
  tx.objectStore('sessions').put({ key, iv: Array.from(iv), data: encrypted });
}
```

---

## 12. COMPATIBILITÉ NAVIGATEURS

| Navigateur | Version minimale | Fonctionnalités PWA |
|---|---|---|
| iOS Safari | 16.4 (mars 2023) | Manifest, SW, push, install |
| Chrome (Android + Desktop) | 90+ | Tout |
| Firefox | 90+ | Manifest, SW, push (pas d'install prompt) |
| Edge | 90+ | Tout (Chromium) |
| Samsung Internet | 14+ | Manifest, SW, push, install |
| Opera | 76+ | Manifest, SW, push |

**Note iOS Safari < 16.4** : les versions antérieures supportent partiellement les Service Workers mais pas les notifications push ni l'installation. Le profil pilote (praticiens + clients 2026) est majoritairement sur iOS 17+ — la couverture est suffisante.

---

## 13. CHECKLIST PRÉ-DÉPLOIEMENT

### 13.1 Vérifications techniques

- [ ] `manifest.json` valide (PWA Builder validator)
- [ ] Service Worker enregistré sans erreur (DevTools > Application > Service Workers)
- [ ] App shell précachée (DevTools > Application > Cache Storage)
- [ ] Audio offline : couper le réseau, vérifier la lecture
- [ ] `offline.html` servie quand toutes les ressources sont hors cache
- [ ] Lighthouse PWA : 100 % des critères verts
- [ ] Lighthouse Performance : > 90
- [ ] LCP < 2.5 s (réseau 4G simulé)
- [ ] CLS < 0.1 (pas de décalage de mise en page)
- [ ] Headers CSP présents et valides (securityheaders.com)
- [ ] HSTS activé
- [ ] HTTPS uniquement (redirection HTTP → HTTPS)
- [ ] Icônes toutes présentes (toutes les tailles)
- [ ] Icône maskable valide (maskable.app)

### 13.2 Tests iOS

- [ ] Safari 16.4+ : prompt d'installation manuel affiché correctement
- [ ] Installation via "Partager → Sur l'écran d'accueil" fonctionne
- [ ] App s'ouvre en plein écran (standalone)
- [ ] Barre de statut : couleur `theme_color` correcte
- [ ] Audio : lecture dans l'app installée
- [ ] Notification push reçue (si iOS 16.4+)

### 13.3 Tests Android

- [ ] Chrome : bannière `beforeinstallprompt` déclenchée
- [ ] Installation depuis la bannière fonctionne
- [ ] App s'ouvre en mode standalone
- [ ] Icône adaptative (maskable) correcte sur l'écran d'accueil
- [ ] Raccourcis (shortcuts) manifest : appui long → menu /quiz et /praticiens
- [ ] Notification push reçue et tappable (ouvre la bonne URL)

### 13.4 Outils de validation

| Outil | Usage | URL |
|---|---|---|
| PWA Builder | Validation manifest + génération icônes | pwabuilder.com |
| Lighthouse | Audit performance, accessibilité, PWA | DevTools ou `npx lighthouse` |
| Maskable.app | Validation icône maskable | maskable.app |
| WebPageTest | Mesure TTFB, LCP réseau réel | webpagetest.org |
| SecurityHeaders | Validation headers HTTP | securityheaders.com |

---

## 14. PLAN D'IMPLÉMENTATION — 5 SPRINTS DE 2 JOURS

### Sprint 1 — Manifest + Icônes (2 jours)

**Objectif** : PWA installable, score Lighthouse PWA ≥ 70 %.

1. Créer `static/icons/icon.svg` à partir du SVG IVIA existant
2. Générer les 10 PNG via PWA Builder (ou ImageMagick)
3. Valider l'icône maskable sur maskable.app
4. Écrire `manifest.json` (complet, voir §2)
5. Modifier `build_pages.py` pour injecter les meta tags PWA dans `<head>`
6. Déployer et tester l'installation iOS + Android
7. Prendre les screenshots (390×844) pour le manifest

**Critère de succès** : installation fonctionne sur iOS Safari 16.4 et Android Chrome.

### Sprint 2 — Service Worker de base (2 jours)

**Objectif** : App shell précachée, site disponible offline, score Lighthouse Performance ≥ 80.

1. Écrire `sw.js` (voir §4.2 complet)
2. Lister les ressources APP_SHELL à précacher
3. Créer `offline.html` (voir §8.2)
4. Créer le banner statut connexion (voir §8.1)
5. Modifier `build_pages.py` pour injecter le script d'enregistrement SW
6. Tester en mode avion : app shell disponible, page offline affichée si non cachée
7. Audit Lighthouse Performance

**Critère de succès** : Lighthouse Performance > 80, SW actif dans DevTools.

### Sprint 3 — Cache audio offline (2 jours)

**Objectif** : Audio praticiens disponible hors ligne.

1. Préparer 5 fichiers audio .opus (32 kbps, ~60 s, ~200 Ko chacun)
2. Nommer avec hash de contenu (voir §5.3)
3. Ajouter `AUDIO_SHELL` dans `sw.js`
4. Implémenter la stratégie stale-while-revalidate pour les audio
5. Tester en mode avion : lecture audio praticien sans réseau
6. Tester la mise à jour : changer un fichier, vérifier que le SW le récupère

**Critère de succès** : lecture audio offline confirmée sur iOS et Android.

### Sprint 4 — Notifications push (2 jours)

**Objectif** : Premier push envoyé et reçu sur iOS et Android.

1. Générer les clés VAPID (voir §6.3)
2. Stocker les clés comme variables d'environnement sur l'hébergeur
3. Déployer `push_backend/main.py` (FastAPI)
4. Créer la page `/notifications` avec opt-in granulaire (voir §6.4)
5. Tester la subscription depuis iOS Safari et Android Chrome
6. Tester l'envoi via le backend `/push/send`
7. Tester le clic sur la notification → navigation vers la bonne URL

**Critère de succès** : notification reçue et cliquable sur les deux plateformes.

### Sprint 5 — Optimisation + Tests (2 jours)

**Objectif** : Lighthouse > 90 tous critères, checklist §13 complète.

1. Audit Lighthouse complet (mobile + desktop)
2. Corriger les points bloquants (LCP, CLS, accessibilité)
3. Valider les headers de sécurité (securityheaders.com)
4. Test CSP : vérifier qu'aucune ressource n'est bloquée
5. Compléter la checklist §13 (iOS + Android)
6. Rédiger le RUNBOOK_PWA.md (procédure déploiement + rollback)
7. Documenter la procédure de mise à jour du cache (versioning CACHE_VERSION)

**Critère de succès** : Lighthouse > 90 tous critères, checklist §13 complète à 100 %.

---

## 15. TICKETS BACKLOG

### Épique : Fondations PWA

| ID | Titre | Sprint | Priorité | Estimation |
|---|---|---|---|---|
| PWA-01 | Créer icon.svg IVIA pour PWA | S1 | Haute | 2 h |
| PWA-02 | Générer 10 PNG icônes (72 → 512, any + maskable) | S1 | Haute | 1 h |
| PWA-03 | Valider icône maskable sur maskable.app | S1 | Haute | 0.5 h |
| PWA-04 | Écrire manifest.json complet | S1 | Haute | 2 h |
| PWA-05 | Modifier build_pages.py : injection meta tags PWA | S1 | Haute | 2 h |
| PWA-06 | Prendre screenshots 390×844 pour le manifest | S1 | Moyenne | 1 h |
| PWA-07 | Test installation iOS Safari 16.4+ | S1 | Haute | 1 h |
| PWA-08 | Test installation Android Chrome | S1 | Haute | 1 h |

### Épique : Service Worker

| ID | Titre | Sprint | Priorité | Estimation |
|---|---|---|---|---|
| PWA-09 | Écrire sw.js (cache-first, network-first, SWR) | S2 | Haute | 4 h |
| PWA-10 | Créer offline.html | S2 | Haute | 2 h |
| PWA-11 | Créer banner statut connexion (online/offline) | S2 | Haute | 1 h |
| PWA-12 | Injecter enregistrement SW dans build_pages.py | S2 | Haute | 1 h |
| PWA-13 | Audit Lighthouse Performance après SW | S2 | Haute | 1 h |

### Épique : Audio offline

| ID | Titre | Sprint | Priorité | Estimation |
|---|---|---|---|---|
| PWA-14 | Produire 5 échantillons audio .opus praticiens pilote | S3 | Haute | 3 h |
| PWA-15 | Nommage hash contenu (sha256[:8]) + pipeline build | S3 | Moyenne | 2 h |
| PWA-16 | Ajouter AUDIO_SHELL au SW + stratégie SWR | S3 | Haute | 2 h |
| PWA-17 | Test lecture audio offline iOS + Android | S3 | Haute | 1 h |
| PWA-18 | Implémenter manifest audio JSON pour détection MAJ | S3 | Moyenne | 2 h |

### Épique : Notifications push

| ID | Titre | Sprint | Priorité | Estimation |
|---|---|---|---|---|
| PWA-19 | Générer clés VAPID, configurer variables d'env | S4 | Haute | 1 h |
| PWA-20 | Déployer push_backend/main.py FastAPI | S4 | Haute | 3 h |
| PWA-21 | Créer page /notifications avec opt-in granulaire | S4 | Haute | 3 h |
| PWA-22 | Gérer événements push + notificationclick dans SW | S4 | Haute | 2 h |
| PWA-23 | Test push iOS Safari 16.4+ | S4 | Haute | 1 h |
| PWA-24 | Test push Android Chrome | S4 | Haute | 1 h |

### Épique : Sécurité + Conformité

| ID | Titre | Sprint | Priorité | Estimation |
|---|---|---|---|---|
| PWA-25 | Configurer CSP stricte avec nonce côté serveur | S5 | Haute | 3 h |
| PWA-26 | Configurer HSTS + headers sécurité sur le serveur | S5 | Haute | 1 h |
| PWA-27 | Audit securityheaders.com → score A+ | S5 | Haute | 1 h |
| PWA-28 | Checklist Loi 25 PWA : vérification stockage local | S5 | Haute | 2 h |

---

## 16. OUVERTURES ET DÉCISIONS EN SUSPENS

**16.1 Fournisseur push backend — hébergement Québec/Canada/France**

Le backend FastAPI pour les notifications push doit être hébergé dans une juridiction conforme à la Loi 25. Options évaluées :

| Option | Région | Coût mensuel estimé (CAD) | Conformité Loi 25 |
|---|---|---|---|
| Railway.app | us-west (par défaut) — à configurer Canada | 5 – 20 | Bonne avec config région |
| Fly.io | ca-central (Montréal) | 3 – 15 | Bonne |
| OVH Cloud | Montréal (BHS) | 10 – 30 | Excellente (données Canada) |
| Clever Cloud | Paris (FR) | 15 – 40 | Acceptable (RGPD, hors Loi 25) |
| Auto-hébergé (VPS Hetzner CA) | Montréal | 8 – 20 | Bonne |

La décision est à arbitrer par David (voir `IVIA_DECISION_MOBILE_PWA_VS_NATIF_v1.0.md` §7.1).

**16.2 Provider VAPID vs service tiers**

VAPID auto-hébergé : gratuit, complexité opérationnelle modérée, conformité maximale.  
OneSignal Free : 10 000 abonnés gratuits, serveurs USA, conformité Loi 25 à valider.  
Novu open-source : auto-hébergeable, communauté active.  

Recommandation doctrinaire IVIA : VAPID auto-hébergé sur infrastructure Canada.

**16.3 Web Push sur iOS — évolution Apple**

Apple a introduit le support Web Push sur iOS 16.4 en mars 2023. Les versions iOS < 16.4 (estimé < 5 % du parc en 2026) ne reçoivent pas de push. La décision à arbitrer : proposer un fallback SMS (ex : Vonage ou AWS SNS avec numéro canadien) pour les utilisateurs sans push, ou ignorer ce segment. Coût SMS : ~0.007 CAD/message.

---

## 17. RÉFÉRENCES CROISÉES

- Document de décision mobile : `IVIA_DECISION_MOBILE_PWA_VS_NATIF_v1.0.md`
- Page praticiens (shortcut PWA /praticiens) : `IVIA_SPEC_PAGE_PRATICIENS_v1.0.md`
- Funnel quiz (shortcut PWA /quiz) : `IVIA_FUNNEL_QUIZ_TO_GUIDANCE_v1.1.md`
- Consentement Loi 25 : `12_JURIDIQUE_AFFAIRES/IVIA_CONSENTEMENT_FUNNEL_LOI25_v1.0.md`
- Stack et infra : `IVIA_ANALYSE_STACK_OUTILS_v1.1.md`

---

*Document produit le 9 mai 2026 — IVIA / MERLIN — "Au sein de l'être — En actes."*

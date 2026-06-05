/**
 * IVIA — Shared JS utilities
 * Utilisé par toutes les pages de l'espace connecté (client, praticien)
 */

// ── Lenis smooth scroll ───────────────────────────────────────────────────────
if (typeof Lenis !== 'undefined') {
  const lenis = new Lenis({ autoRaf: true, anchors: true, allowNestedScroll: true });
  if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
    gsap.registerPlugin(ScrollTrigger);
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add((time) => lenis.raf(time * 1000));
    gsap.ticker.lagSmoothing(0);
  }
}

// ── Bandeau Loi 25 sur les formulaires ──────────────────────────────────────
function renderLoi25Badge(container) {
  const badge = document.createElement('div');
  badge.className = 'flex items-center gap-2 bg-blue-50 border border-blue-100 rounded-[10px] px-4 py-2.5 text-xs text-trust';
  badge.setAttribute('role', 'note');
  badge.innerHTML = `
    <svg class="w-4 h-4 shrink-0" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
      <path fill-rule="evenodd" d="M10 1.944A11.954 11.954 0 012.166 5C2.056 5.649 2 6.319 2 7c0 5.225
        3.34 9.67 8 11.317C14.66 16.67 18 12.225 18 7c0-.682-.057-1.35-.166-2.001A11.954 11.954 0 0110
        1.944z" clip-rule="evenodd"/>
    </svg>
    <span>Conforme à la <a href="/confidentialite.html" class="underline underline-offset-2 font-medium">Loi 25 du Québec</a>
    · Données hébergées au Canada</span>`;
  if (container) container.prepend(badge);
}

// ── Bandeau urgence footer ────────────────────────────────────────────────────
function renderEmergencyFooter(container) {
  const strip = document.createElement('p');
  strip.className = 'text-center text-xs text-muted';
  strip.setAttribute('role', 'note');
  strip.innerHTML = `IVIA n'est pas un service d'urgence et ne pose pas de diagnostic.
    En crise&nbsp;: <strong><a href="tel:18662773553" class="underline">1&nbsp;866&nbsp;APPELLE&nbsp;(277-3553)</a></strong>`;
  if (container) container.appendChild(strip);
}

// ── Toast notifications ───────────────────────────────────────────────────────
function showToast(message, type = 'info') {
  const colors = { info: 'bg-surface border-bdr text-ink', success: 'bg-green-50 border-green-200 text-green-900', error: 'bg-red-50 border-red-200 text-red-900' };
  const toast = document.createElement('div');
  toast.className = `fixed bottom-6 left-1/2 -translate-x-1/2 z-[9999] px-5 py-3 rounded-[12px] border shadow-lg text-sm font-medium transition-all duration-300 ${colors[type] || colors.info}`;
  toast.setAttribute('role', 'status');
  toast.setAttribute('aria-live', 'polite');
  toast.textContent = message;
  document.body.appendChild(toast);
  setTimeout(() => { toast.style.opacity = '0'; setTimeout(() => toast.remove(), 300); }, 3500);
}

// ── Journal — tags (max 3) ────────────────────────────────────────────────────
function initTagCheckboxes(container) {
  if (!container) return;
  const checks = container.querySelectorAll('input[type="checkbox"]');
  checks.forEach(cb => {
    cb.addEventListener('change', () => {
      const checked = Array.from(checks).filter(c => c.checked);
      if (checked.length >= 3) {
        checks.forEach(c => { if (!c.checked) c.disabled = true; });
      } else {
        checks.forEach(c => { c.disabled = false; });
      }
    });
  });
}

/* IVIA — interactions douces */
(function () {
  'use strict';

  /* ---------- 1. Mode Calme ---------- */
  const STORAGE_KEY = 'ivia.calme';
  const body = document.body;
  const toggle = document.getElementById('calmeToggle');

  // Restore on load
  try {
    if (localStorage.getItem(STORAGE_KEY) === '1') {
      body.classList.add('calme');
      if (toggle) toggle.setAttribute('aria-pressed', 'true');
    }
  } catch (_) { /* localStorage indisponible */ }

  if (toggle) {
    toggle.addEventListener('click', function () {
      const active = body.classList.toggle('calme');
      toggle.setAttribute('aria-pressed', active ? 'true' : 'false');
      try { localStorage.setItem(STORAGE_KEY, active ? '1' : '0'); } catch (_) {}
    });
  }

  /* ---------- 2. Reveal au scroll ---------- */
  const reveals = document.querySelectorAll('.reveal');
  if (reveals.length && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }

  /* ---------- 3. Barre de progression de lecture ---------- */
  const bar = document.querySelector('.progress-bar');
  const article = document.querySelector('.article-body');
  if (bar && article) {
    const update = function () {
      const rect = article.getBoundingClientRect();
      const total = rect.height - window.innerHeight + 200;
      const scrolled = Math.max(0, -rect.top + 200);
      const ratio = Math.min(1, Math.max(0, scrolled / Math.max(total, 1)));
      bar.style.width = (ratio * 100).toFixed(2) + '%';
    };
    document.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    update();
  }

  /* ---------- 4. Sauvegarder pour plus tard (démo locale) ---------- */
  const saveBtn = document.querySelector('[data-action="save"]');
  if (saveBtn) {
    const id = saveBtn.getAttribute('data-id') || location.pathname;
    const KEY = 'ivia.saved';
    const getSaved = function () {
      try { return JSON.parse(localStorage.getItem(KEY) || '[]'); }
      catch (_) { return []; }
    };
    const setSaved = function (arr) {
      try { localStorage.setItem(KEY, JSON.stringify(arr)); } catch (_) {}
    };
    const refresh = function () {
      const list = getSaved();
      const isSaved = list.indexOf(id) !== -1;
      saveBtn.setAttribute('aria-pressed', isSaved ? 'true' : 'false');
      saveBtn.querySelector('.label').textContent =
        isSaved ? 'Sauvegardé' : 'Sauvegarder pour plus tard';
    };
    saveBtn.addEventListener('click', function () {
      const list = getSaved();
      const idx = list.indexOf(id);
      if (idx === -1) list.push(id); else list.splice(idx, 1);
      setSaved(list);
      refresh();
    });
    refresh();
  }
})();

/* IVIA — interactions partagées (Mode Calme + petits comportements) */
(function () {
  // Mode Calme : préférence en mémoire (pas localStorage car sandboxes peuvent bloquer)
  const root = document.documentElement;
  const toggle = document.querySelector('[data-mode-calme]');
  let calme = false;

  // Si l'utilisateur préfère reduced motion, on active Mode Calme par défaut
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    calme = true;
    root.setAttribute('data-mode', 'calme');
  }

  if (toggle) {
    toggle.setAttribute('aria-pressed', calme ? 'true' : 'false');
    toggle.addEventListener('click', () => {
      calme = !calme;
      root.setAttribute('data-mode', calme ? 'calme' : 'normal');
      toggle.setAttribute('aria-pressed', calme ? 'true' : 'false');
    });
  }

  // Petits boutons audio fictifs : play/pause UX placeholder
  document.querySelectorAll('[data-audio-fake]').forEach(btn => {
    btn.addEventListener('click', () => {
      const playing = btn.getAttribute('aria-pressed') === 'true';
      btn.setAttribute('aria-pressed', playing ? 'false' : 'true');
      btn.textContent = playing ? '▶︎ Écouter' : '⏸ En lecture';
    });
  });

  // Enregistrement audio simulé (mockup uniquement) : barre de progression + minuteur
  document.querySelectorAll('[data-record-fake]').forEach(btn => {
    let timer = null;
    let seconds = 0;
    const display = btn.parentElement.querySelector('[data-record-time]');
    const wave    = btn.parentElement.querySelector('[data-record-wave]');
    btn.addEventListener('click', () => {
      const recording = btn.getAttribute('aria-pressed') === 'true';
      if (!recording) {
        btn.setAttribute('aria-pressed', 'true');
        btn.querySelector('.label').textContent = 'Arrêter';
        if (wave) wave.classList.add('is-recording');
        timer = setInterval(() => {
          seconds++;
          if (display) {
            const m = String(Math.floor(seconds / 60)).padStart(2, '0');
            const s = String(seconds % 60).padStart(2, '0');
            display.textContent = `${m}:${s}`;
          }
        }, 1000);
      } else {
        btn.setAttribute('aria-pressed', 'false');
        btn.querySelector('.label').textContent = 'Reprendre';
        if (wave) wave.classList.remove('is-recording');
        clearInterval(timer);
      }
    });
  });

  // Tabs simples
  document.querySelectorAll('[data-tabs]').forEach(tabs => {
    const buttons = tabs.querySelectorAll('[role="tab"]');
    const panels  = tabs.querySelectorAll('[role="tabpanel"]');
    buttons.forEach(btn => {
      btn.addEventListener('click', () => {
        const target = btn.getAttribute('data-target');
        buttons.forEach(b => b.setAttribute('aria-selected', b === btn ? 'true' : 'false'));
        panels.forEach(p => p.hidden = (p.id !== target));
      });
    });
  });
})();

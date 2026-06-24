/* IVIA — design system « Maison habitée » : ambiance + menu compte.
   Partagé par toutes les maquettes design-system. */
function setTheme(t){
  document.body.dataset.theme = t;
  const s = document.getElementById('t-signature'), d = document.getElementById('t-doux');
  if (s){ s.classList.toggle('on', t === 'signature'); s.setAttribute('aria-selected', t === 'signature'); }
  if (d){ d.classList.toggle('on', t === 'doux'); d.setAttribute('aria-selected', t === 'doux'); }
  try{ localStorage.setItem('ivia_recorder_theme', t); }catch(e){}
}
function toggleMenu(e){
  e.stopPropagation();
  const p = document.getElementById('menu-panel'), b = document.getElementById('menu-btn');
  const open = p.classList.toggle('open');
  b.setAttribute('aria-expanded', open);
}
document.addEventListener('click', (e) => {
  const p = document.getElementById('menu-panel');
  if (p && p.classList.contains('open') && !e.target.closest('.menu')){
    p.classList.remove('open');
    document.getElementById('menu-btn').setAttribute('aria-expanded', 'false');
  }
});
document.addEventListener('DOMContentLoaded', () => {
  try{ const s = localStorage.getItem('ivia_recorder_theme'); if (s) setTheme(s); }catch(e){}
});

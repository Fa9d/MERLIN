/**
 * IVIA — Mesure d'audience souveraine (Matomo auto-hébergé, données Québec).
 *
 * Mode SANS TÉMOIN (cookieless) : aucun cookie déposé, aucune donnée
 * personnelle collectée → conforme Loi 25 sans bandeau de consentement.
 * L'adresse IP est anonymisée côté serveur Matomo (2 octets masqués).
 *
 * Événement de conversion : appeler window.iviaTrackDemande() quand une
 * demande de rendez-vous est soumise avec succès.
 *
 * La balise ne s'active que si stats.ivia.quebec répond (Matomo déployé) ;
 * sinon elle échoue silencieusement — aucun impact sur le site.
 */
(function () {
  // Ne pas mesurer en local / hors production
  if (!/\.quebec$/.test(location.hostname)) return;

  var _paq = (window._paq = window._paq || []);
  _paq.push(['disableCookies']);          // mode sans témoin — Loi 25
  _paq.push(['setDoNotTrack', true]);     // respecter le signal "ne pas suivre"
  _paq.push(['trackPageView']);
  _paq.push(['enableLinkTracking']);

  var u = 'https://stats.ivia.quebec/';
  _paq.push(['setTrackerUrl', u + 'matomo.php']);
  _paq.push(['setSiteId', '1']);

  var d = document,
    g = d.createElement('script'),
    s = d.getElementsByTagName('script')[0];
  g.async = true;
  g.src = u + 'matomo.js';
  g.onerror = function () {}; // Matomo absent → silence
  s.parentNode.insertBefore(g, s);

  /** Conversion : demande de rendez-vous envoyée. */
  window.iviaTrackDemande = function (detail) {
    try {
      _paq.push(['trackEvent', 'conversion', 'demande_envoyee', detail || '']);
    } catch (e) { /* silence */ }
  };
})();

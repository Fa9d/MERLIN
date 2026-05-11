import { expect, test } from '@playwright/test';

/**
 * Parcours public critique — IVIA / MERLIN
 *
 * Périmètre :
 *   - Pages publiques répondent 200
 *   - API répond et expose un schéma cohérent
 *   - Aucune action mutative (pas de création de compte / réservation en prod)
 *
 * Pourquoi ce périmètre :
 *   Le pilote tourne avec 2 praticiens (Mylène, Émilie). Casser la home,
 *   /praticiens ou /demarche en prod est inacceptable. Casser /admin ou
 *   /espace-praticien est désagréable mais non bloquant pour un client.
 *   Cette spec sécurise le minimum vital côté client.
 *
 * Référence : MERLIN_GOUV_BACKLOG_MAITRE_V2.md FRONT-004
 */

const PUBLIC_PAGES = [
  { path: '/', label: 'Accueil IVIA' },
  { path: '/praticiens', label: 'Liste des praticiens' },
  { path: '/demarche', label: 'Démarche' },
  { path: '/rendez-vous', label: 'Rendez-vous' },
  { path: '/ressources', label: 'Ressources' },
] as const;

test.describe('Pages publiques — accessibilité', () => {
  for (const page of PUBLIC_PAGES) {
    test(`${page.path} répond 200 et affiche du contenu`, async ({ page: browserPage, request }) => {
      const response = await request.get(page.path);
      expect(response.status(), `${page.path} doit répondre 200`).toBe(200);

      await browserPage.goto(page.path);

      const title = await browserPage.title();
      expect(title.length, `${page.path} doit avoir un title non vide`).toBeGreaterThan(0);

      const bodyText = await browserPage.locator('body').innerText();
      expect(bodyText.length, `${page.path} doit avoir du contenu visible`).toBeGreaterThan(50);
    });
  }
});

test.describe('Console errors — pas d\'erreur JS critique sur les pages publiques', () => {
  for (const page of PUBLIC_PAGES) {
    test(`${page.path} sans erreur console critique`, async ({ page: browserPage }) => {
      const errors: string[] = [];
      browserPage.on('pageerror', (err) => errors.push(err.message));
      browserPage.on('console', (msg) => {
        if (msg.type() === 'error') {
          const text = msg.text();
          // Ignorer les warnings réseau/CSP non bloquants connus
          if (!text.match(/Failed to load resource|net::ERR_/i)) {
            errors.push(text);
          }
        }
      });

      await browserPage.goto(page.path, { waitUntil: 'networkidle' });
      await browserPage.waitForTimeout(1000);

      expect(errors, `${page.path} ne doit pas avoir d'erreur JS:\n${errors.join('\n')}`).toEqual([]);
    });
  }
});

test.describe('Rendez-vous — parcours public pilote', () => {
  test('/rendez-vous/reserver redirige vers le formulaire public sans mur de compte', async ({ page }) => {
    await page.goto('/rendez-vous/reserver');

    await expect(page).toHaveURL(/\/rendez-vous$/);
    await expect(page.getByRole('button', { name: 'Demander ma seance' })).toBeVisible();
    await expect(page.getByText('Créer mon compte')).toHaveCount(0);
    await expect(page.getByText('Déjà inscrit')).toHaveCount(0);
  });
});

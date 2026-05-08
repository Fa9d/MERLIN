import { defineConfig, devices } from '@playwright/test';

/**
 * Configuration Playwright — IVIA / MERLIN
 *
 * Stratégie pilote (mai-août 2026) :
 *   - Tests e2e ciblent par défaut la production (api.ivia.quebec + ivia.quebec)
 *   - Aucun mock, aucun seed : on valide ce que voit réellement le client
 *   - Aucune action mutative non-réversible (pas de créer-utilisateur en prod)
 *   - Pour tester en local : BASE_URL=http://localhost:3000 npx playwright test
 *
 * Référence backlog : FRONT-004, ROLES-009 (tests e2e par rôle)
 * Référence audit : SMOKE_TEST_PROD_2026-05-08.md
 */

const BASE_URL = process.env.BASE_URL ?? 'https://ivia.quebec';
const API_BASE_URL = process.env.API_BASE_URL ?? 'https://api.ivia.quebec';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: process.env.CI ? 'github' : 'list',

  use: {
    baseURL: BASE_URL,
    extraHTTPHeaders: {
      'X-Test-Origin': 'playwright-e2e',
    },
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    actionTimeout: 10_000,
    navigationTimeout: 20_000,
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    // Décommenter pour étendre la couverture
    // { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    // { name: 'webkit',  use: { ...devices['Desktop Safari']  } },
    // { name: 'mobile-chrome', use: { ...devices['Pixel 7'] } },
  ],

  // Pas de webServer : on cible la prod par défaut.
  // Pour lancer en local, démarrer `npm run dev` à part et exporter BASE_URL.

  metadata: {
    apiBaseUrl: API_BASE_URL,
  },
});

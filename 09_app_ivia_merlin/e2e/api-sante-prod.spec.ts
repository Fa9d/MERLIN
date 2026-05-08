import { expect, test } from '@playwright/test';

/**
 * Sanité API production — IVIA / MERLIN
 *
 * Périmètre :
 *   - L'API répond et expose son schéma OpenAPI
 *   - Les routes critiques renvoient les codes HTTP attendus
 *   - Aucune action mutative
 *
 * Référence : SMOKE_TEST_PROD_2026-05-08.md (preuves INFRA-004)
 */

const API_BASE_URL = process.env.API_BASE_URL ?? 'https://api.ivia.quebec';

test.describe('API santé', () => {
  test('GET /api/health → 200 + payload attendu', async ({ request }) => {
    const r = await request.get(`${API_BASE_URL}/api/health`);
    expect(r.status()).toBe(200);

    const body = await r.json();
    expect(body).toMatchObject({
      status: 'ok',
      service: expect.any(String),
      environment: expect.any(String),
      database: 'ok',
    });
  });

  test('GET /api/openapi.json → schéma OpenAPI cohérent', async ({ request }) => {
    const r = await request.get(`${API_BASE_URL}/api/openapi.json`);
    expect(r.status()).toBe(200);
    expect(r.headers()['content-type']).toContain('application/json');

    const spec = await r.json();
    expect(spec.openapi, 'OpenAPI doit avoir un champ openapi version').toMatch(/^3\./);
    expect(spec.info?.title).toBe('MERLIN API');
    expect(Object.keys(spec.paths ?? {}).length, 'Au moins 40 routes attendues').toBeGreaterThanOrEqual(40);
  });
});

test.describe('Routes critiques publiques', () => {
  test('GET /api/v1/praticiens → 200 + tableau', async ({ request }) => {
    const r = await request.get(`${API_BASE_URL}/api/v1/praticiens`);
    expect(r.status()).toBe(200);

    const body = await r.json();
    expect(Array.isArray(body), 'Réponse doit être un tableau').toBe(true);

    if (body.length > 0) {
      // Vérifie le schéma PraticienPublic (auth.py)
      const expectedKeys = ['id', 'display_name', 'title_line', 'intro_text', 'spoken_languages', 'available_channels'];
      for (const key of expectedKeys) {
        expect(body[0], `PraticienPublic doit avoir le champ ${key}`).toHaveProperty(key);
      }
    }
  });
});

test.describe('Sécurité — endpoints protégés rejettent sans auth', () => {
  test('GET /api/v1/auth/me sans token → 401', async ({ request }) => {
    const r = await request.get(`${API_BASE_URL}/api/v1/auth/me`);
    expect(r.status()).toBe(401);
  });
});

test.describe('Validation Pydantic — endpoints rejettent body vide', () => {
  const ENDPOINTS_REQUIRING_BODY = [
    '/api/v1/intake-requests',
    '/api/v1/auth/login',
    '/api/v1/register/client',
  ];

  for (const path of ENDPOINTS_REQUIRING_BODY) {
    test(`POST ${path} avec body vide → 422`, async ({ request }) => {
      const r = await request.post(`${API_BASE_URL}${path}`, {
        data: {},
        headers: { 'Content-Type': 'application/json' },
      });
      expect(r.status(), `${path} doit refuser un body vide`).toBe(422);
    });
  }
});

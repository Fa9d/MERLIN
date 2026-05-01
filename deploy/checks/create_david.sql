INSERT INTO app_users (id, email, password_hash, display_name, legal_name, role, record_status, created_at, updated_at)
VALUES (
  gen_random_uuid()::text,
  'davidphaneuf@gmail.com',
  'scrypt:fc9fe17665fc8cb5d3f2e354b585bc6d:5cf139ebbb77aa37d932b6e8595e8d4440fc0710ae2f42bf016d381fcf788be485a25af395fb6db68992b8872d1a43007609fc996ea37369d19a82c035589241',
  'David',
  'David Phaneuf',
  'practitioner',
  'active',
  now(),
  now()
)
ON CONFLICT (email) DO NOTHING;
SELECT id, email, display_name, legal_name, role, record_status FROM app_users WHERE email = 'davidphaneuf@gmail.com';

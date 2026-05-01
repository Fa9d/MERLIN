UPDATE app_users
SET
  title_line         = 'Intervenant en soutien émotionnel',
  intro_text         = 'À votre écoute, active ou pas. Une oreille, une voix, une sensibilité. De plusieurs écoles et autodidacte, une réelle expérience de la vie, ici au Québec mais aussi en Europe, Maghreb et USA. Un test de 10 minutes gratuit si vous voulez ;-)',
  spoken_languages   = '["fr"]',
  available_channels = '["direct"]',
  is_publicly_listed = false,
  updated_at         = now()
WHERE email = 'davidphaneuf@gmail.com';

SELECT id, email, display_name, title_line, intro_text, spoken_languages, available_channels, is_publicly_listed
FROM app_users
WHERE email = 'davidphaneuf@gmail.com';

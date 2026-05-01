UPDATE app_users SET is_publicly_listed = true WHERE email = 'davidphaneuf@gmail.com';
SELECT email, display_name, is_publicly_listed FROM app_users WHERE email = 'davidphaneuf@gmail.com';

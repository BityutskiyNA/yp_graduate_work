BEGIN;

-- создаем схему
CREATE SCHEMA IF NOT EXISTS content;
-- делаем созданную схему основной
SET search_path TO content,public;

-- устанавливаем схему по умолчанию
ALTER ROLE app SET search_path TO content,public;

COMMIT;
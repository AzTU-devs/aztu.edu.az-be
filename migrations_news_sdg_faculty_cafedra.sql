-- =====================================================================
-- News: add optional SDG numbers (1..17), faculty_code, cafedra_code
-- News Category: nothing schema-level needed (count is derived at runtime).
--
-- Apply on Postgres. Safe to re-run thanks to IF NOT EXISTS guards.
-- =====================================================================

BEGIN;

-- 1) sdg_numbers — optional integer array stored as JSON
ALTER TABLE news
    ADD COLUMN IF NOT EXISTS sdg_numbers JSON NULL;

-- 2) faculty_code — optional reference to faculties.faculty_code
ALTER TABLE news
    ADD COLUMN IF NOT EXISTS faculty_code VARCHAR(50) NULL;

-- 3) cafedra_code — optional reference to cafedras.cafedra_code
ALTER TABLE news
    ADD COLUMN IF NOT EXISTS cafedra_code VARCHAR(50) NULL;

-- Helpful indexes for filtering by faculty / cafedra / category
CREATE INDEX IF NOT EXISTS ix_news_faculty_code ON news (faculty_code);
CREATE INDEX IF NOT EXISTS ix_news_cafedra_code ON news (cafedra_code);
CREATE INDEX IF NOT EXISTS ix_news_category_id  ON news (category_id);

COMMIT;

-- =====================================================================
-- Optional rollback
-- =====================================================================
-- BEGIN;
-- DROP INDEX IF EXISTS ix_news_faculty_code;
-- DROP INDEX IF EXISTS ix_news_cafedra_code;
-- DROP INDEX IF EXISTS ix_news_category_id;
-- ALTER TABLE news DROP COLUMN IF EXISTS sdg_numbers;
-- ALTER TABLE news DROP COLUMN IF EXISTS faculty_code;
-- ALTER TABLE news DROP COLUMN IF EXISTS cafedra_code;
-- COMMIT;

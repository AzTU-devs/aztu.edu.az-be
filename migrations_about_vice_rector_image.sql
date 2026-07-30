-- =====================================================================
-- MIGRATION — About: vice-rector portrait
--
-- Adds:
--   about_persons.image_url  → the vice-rector's photo, an uploaded
--       file's path or a pasted URL, language-neutral like every other
--       column on the person row
--
-- The upload itself reuses the existing page image endpoint
-- (PUT /api/about/admin/pages/{page_key}/image), which only stores the
-- file and returns its path; the path then travels in the person's
-- `image_url` on the next whole-page save. No new endpoint is needed.
--
-- Run AFTER migrations_about_vice_rector.sql. Idempotent and additive.
-- =====================================================================


-- =====================================================================
-- STEP 1 — SCHEMA
-- =====================================================================
alter table about_persons add column if not exists image_url varchar(2048);


-- =====================================================================
-- STEP 2 — VERIFY. Expect one row.
-- =====================================================================
select column_name, data_type
from information_schema.columns
where table_name = 'about_persons' and column_name = 'image_url';

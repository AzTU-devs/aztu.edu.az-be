-- =====================================================================
-- PRODUCTION MIGRATION — Research Institutes (Tədqiqat İnstitutları)
--
-- Adds the contact/extra-content fields the admin form now edits:
--   research_institutes      → website_url, email          (both optional)
--   research_institutes_tr   → additional_info_html        (optional, per language)
--
-- Run the whole file in one psql session against the production DB.
-- Every statement is idempotent: re-running the file is safe, and every
-- change is additive — nothing is dropped or rewritten.
-- =====================================================================


-- =====================================================================
-- STEP 1 — SCHEMA
-- =====================================================================
alter table research_institutes add column if not exists website_url varchar(2048);
alter table research_institutes add column if not exists email varchar(255);

alter table research_institutes_tr add column if not exists additional_info_html text;


-- =====================================================================
-- STEP 2 — VERIFY
--
-- Expect five rows: website_url, email on the parent table and
-- additional_info_html on the translations table.
-- =====================================================================
select table_name, column_name, data_type
from information_schema.columns
where (table_name = 'research_institutes' and column_name in ('website_url', 'email'))
   or (table_name = 'research_institutes_tr' and column_name = 'additional_info_html')
order by table_name, column_name;

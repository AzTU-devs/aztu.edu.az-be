-- =====================================================================
-- DROP — remove the About-page CMS from the database entirely
--
-- ⚠️  DESTRUCTIVE AND IRREVERSIBLE. This deletes the ten About tables and
--     everything in them: every page, block, item, person and translation,
--     including any copy already typed into the dashboard. There is no
--     undo. Take a backup first if there is any doubt:
--
--         pg_dump "$DATABASE_URL" -t 'about_*' > about_backup.sql
--
-- Run this only when starting the About section over from zero. Nothing
-- else in the schema references these tables, so dropping them cannot
-- affect news, faculties, cafedras, departments or any other module.
--
-- Uploaded files under static/about/ are NOT removed by this script —
-- delete that directory separately if the images and PDFs are unwanted.
-- =====================================================================


-- =====================================================================
-- STEP 1 — PREVIEW. Run this alone first to see what will be lost.
-- =====================================================================
select 'about_pages'          as table_name, count(*) from about_pages
union all select 'about_page_tr',              count(*) from about_page_tr
union all select 'about_sections',             count(*) from about_sections
union all select 'about_section_tr',           count(*) from about_section_tr
union all select 'about_items',                count(*) from about_items
union all select 'about_item_tr',              count(*) from about_item_tr
union all select 'about_people',               count(*) from about_people
union all select 'about_person_tr',            count(*) from about_person_tr
union all select 'about_person_education',     count(*) from about_person_education
union all select 'about_person_education_tr',  count(*) from about_person_education_tr
order by table_name;


-- =====================================================================
-- STEP 2 — DROP. Only run once the preview has been checked.
--
-- CASCADE is unnecessary between these tables (dropping in dependency
-- order would do), but it is used so the statement cannot fail on a
-- foreign key added later by hand.
-- =====================================================================
drop table if exists about_person_education_tr cascade;
drop table if exists about_person_education    cascade;
drop table if exists about_person_tr           cascade;
drop table if exists about_people              cascade;
drop table if exists about_item_tr             cascade;
drop table if exists about_items               cascade;
drop table if exists about_section_tr          cascade;
drop table if exists about_sections            cascade;
drop table if exists about_page_tr             cascade;
drop table if exists about_pages               cascade;


-- =====================================================================
-- STEP 3 — VERIFY. Expect zero rows.
-- =====================================================================
select table_name
from information_schema.tables
where table_schema = 'public'
  and table_name like 'about%'
order by table_name;

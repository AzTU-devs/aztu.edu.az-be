-- =====================================================================
-- Clear staff telephone numbers — faculties, cafedras, departments
--
-- Sets phone (and phone_code) to NULL on the three STAFF tables only:
--   faculty_workers, cafedra_workers, department_workers
--
-- DELIBERATELY NOT TOUCHED — these keep their numbers:
--   faculty_directors, cafedra_directors, department_directors   (directors)
--   menu_contact_phones                                          (unit contact)
--   faculty_deputy_deans, cafedra_deputy_directors               (see block B)
--   faculty_scientific_council, cafedra_scientific_council       (see block B)
--   office_staff, institute_staff, about_persons, employee_contacts
--
-- This is IRREVERSIBLE — the numbers are overwritten, not archived. Take the
-- backup in step 1 first; it is a single statement and it is what lets you undo.
-- =====================================================================


-- ── 1. BACKUP (run this FIRST, on its own) ───────────────────────────
-- Keeps id + phone + phone_code for every row about to change, so the update
-- can be reversed. Drop the table once you are satisfied.
create table if not exists staff_phone_backup_20260901 as
select 'faculty_workers'    as source_table, id, phone, phone_code from faculty_workers    where phone is not null or phone_code is not null
union all
select 'cafedra_workers'    as source_table, id, phone, phone_code from cafedra_workers    where phone is not null or phone_code is not null
union all
select 'department_workers' as source_table, id, phone, phone_code from department_workers where phone is not null or phone_code is not null;

-- How many rows are in scope, per table:
select source_table, count(*) as rows_backed_up
  from staff_phone_backup_20260901
 group by source_table
 order by source_table;


-- ── 2. THE UPDATE ────────────────────────────────────────────────────
begin;

update faculty_workers
   set phone = null, phone_code = null
 where phone is not null or phone_code is not null;

update cafedra_workers
   set phone = null, phone_code = null
 where phone is not null or phone_code is not null;

update department_workers
   set phone = null, phone_code = null
 where phone is not null or phone_code is not null;

commit;


-- ── 3. VERIFY (expect 0 everywhere) ──────────────────────────────────
select 'faculty_workers'    as tbl, count(*) as remaining from faculty_workers    where phone is not null or phone_code is not null
union all
select 'cafedra_workers',         count(*) from cafedra_workers    where phone is not null or phone_code is not null
union all
select 'department_workers',      count(*) from department_workers where phone is not null or phone_code is not null;

-- And confirm the directors were NOT touched (expect non-zero if they had numbers):
select 'faculty_directors'    as tbl, count(*) as still_have_phone from faculty_directors    where phone is not null
union all
select 'cafedra_directors',        count(*) from cafedra_directors    where phone is not null
union all
select 'department_directors',     count(*) from department_directors where phone is not null;


-- ── 4. TO UNDO ───────────────────────────────────────────────────────
-- begin;
-- update faculty_workers w set phone = b.phone, phone_code = b.phone_code
--   from staff_phone_backup_20260901 b
--  where b.source_table = 'faculty_workers' and b.id = w.id;
-- update cafedra_workers w set phone = b.phone, phone_code = b.phone_code
--   from staff_phone_backup_20260901 b
--  where b.source_table = 'cafedra_workers' and b.id = w.id;
-- update department_workers w set phone = b.phone, phone_code = b.phone_code
--   from staff_phone_backup_20260901 b
--  where b.source_table = 'department_workers' and b.id = w.id;
-- commit;


-- =====================================================================
-- BLOCK B — OPTIONAL, NOT PART OF THE ABOVE
--
-- Deputy deans, deputy directors and scientific council members are neither
-- "staff" nor "directors", so they were left alone. They are individuals with
-- personal numbers published too, so you may well want them cleared as well.
-- Run this ONLY if you do.
-- =====================================================================
-- create table if not exists leadership_phone_backup_20260901 as
-- select 'faculty_deputy_deans'       as source_table, id, phone, phone_code from faculty_deputy_deans       where phone is not null
-- union all
-- select 'cafedra_deputy_directors',       id, phone, phone_code from cafedra_deputy_directors       where phone is not null
-- union all
-- select 'faculty_scientific_council',     id, phone, phone_code from faculty_scientific_council     where phone is not null
-- union all
-- select 'cafedra_scientific_council',     id, phone, phone_code from cafedra_scientific_council     where phone is not null;
--
-- begin;
-- update faculty_deputy_deans       set phone = null, phone_code = null where phone is not null or phone_code is not null;
-- update cafedra_deputy_directors   set phone = null, phone_code = null where phone is not null or phone_code is not null;
-- update faculty_scientific_council set phone = null, phone_code = null where phone is not null or phone_code is not null;
-- update cafedra_scientific_council set phone = null, phone_code = null where phone is not null or phone_code is not null;
-- commit;

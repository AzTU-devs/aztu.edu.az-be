-- =====================================================================
-- MIGRATION — Faculty module: contact fields for director, deputy dean
--             & worker
--
-- Adds the standard contact block to the three in-scope person entities
-- of the FACULTY module. The scientific council (faculty_scientific_council
-- / faculty_council_member_tr) is intentionally OUT OF SCOPE and left
-- untouched.
--
-- DIRECTOR (faculty_directors / faculty_director_tr):
--   * phone_code  -> NEUTRAL varchar(50)  on the parent row (internal ext.)
--       (email / phone already exist on the parent row)
--   * room        -> BILINGUAL varchar(255) on the *_tr sibling.
--       The room was previously a neutral column `room_number` on the
--       parent. We ADD `room` to the tr table and BACKFILL it from the old
--       `room_number` into BOTH the az and en tr rows. `room_number` stays
--       in place (deprecated) — it is no longer written or read.
--   NOTE: director already has a working-hours schedule child table
--         (faculty_director_working_hours), so we do NOT add working_hours
--         here and do NOT touch that schedule.
--
-- DEPUTY DEAN (faculty_deputy_deans / faculty_deputy_dean_tr):
--   * phone_code    -> NEUTRAL varchar(50)  on the parent row
--       (email / phone already exist on the parent row)
--   * room          -> BILINGUAL varchar(255) on the *_tr sibling
--   * working_hours -> BILINGUAL varchar(500) on the *_tr sibling
--
-- WORKER (faculty_workers / faculty_worker_tr):
--   * phone_code    -> NEUTRAL varchar(50)  on the parent row
--       (email / phone already exist on the parent row)
--   * room          -> BILINGUAL varchar(255) on the *_tr sibling
--   * working_hours -> BILINGUAL varchar(500) on the *_tr sibling
--
-- Neon / alembic-unstamped DB: additive & idempotent only.
-- =====================================================================


-- ── DIRECTOR: neutral phone_code on parent ──────────────────────────
alter table faculty_directors add column if not exists phone_code varchar(50);

-- ── DIRECTOR: bilingual room on the translation sibling ─────────────
alter table faculty_director_tr add column if not exists room varchar(255);

-- Backfill room from the deprecated neutral room_number into both langs.
update faculty_director_tr t
set    room = d.room_number
from   faculty_directors d
where  t.director_id = d.id
  and  t.room is null
  and  d.room_number is not null
  and  d.room_number <> '';


-- ── DEPUTY DEAN: neutral phone_code on parent ───────────────────────
alter table faculty_deputy_deans add column if not exists phone_code varchar(50);

-- ── DEPUTY DEAN: bilingual room + working_hours on the tr sibling ────
alter table faculty_deputy_dean_tr add column if not exists room          varchar(255);
alter table faculty_deputy_dean_tr add column if not exists working_hours varchar(500);


-- ── WORKER: neutral phone_code on parent ────────────────────────────
alter table faculty_workers add column if not exists phone_code varchar(50);

-- ── WORKER: bilingual room + working_hours on the translation sibling ─
alter table faculty_worker_tr add column if not exists room          varchar(255);
alter table faculty_worker_tr add column if not exists working_hours varchar(500);


-- ── Verify ──────────────────────────────────────────────────────────
select table_name, column_name, data_type, character_maximum_length
from   information_schema.columns
where  (table_name = 'faculty_directors'      and column_name in ('phone_code'))
   or  (table_name = 'faculty_director_tr'     and column_name in ('room'))
   or  (table_name = 'faculty_deputy_deans'    and column_name in ('phone_code'))
   or  (table_name = 'faculty_deputy_dean_tr'  and column_name in ('room', 'working_hours'))
   or  (table_name = 'faculty_workers'         and column_name in ('phone_code'))
   or  (table_name = 'faculty_worker_tr'       and column_name in ('room', 'working_hours'))
order by table_name, column_name;

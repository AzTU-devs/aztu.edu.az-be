-- =====================================================================
-- MIGRATION — Department module: contact fields for director & worker
--
-- Adds the standard contact block to the two person entities of the
-- DEPARTMENT module (director and worker). This module has NO deputy and
-- NO scientific council, so only these two entities are touched.
--
-- DIRECTOR (department_directors / department_director_tr):
--   * email       -> NEUTRAL varchar(255) on the parent row
--   * phone       -> NEUTRAL varchar(100) on the parent row
--   * phone_code  -> NEUTRAL varchar(50)  on the parent row (internal ext.)
--   * room        -> BILINGUAL varchar(255) on the *_tr sibling.
--       The room was previously a neutral column `room_number` on the
--       parent. We ADD `room` to the tr table and BACKFILL it from the old
--       `room_number` into BOTH the az and en tr rows. `room_number` stays
--       in place (deprecated) — it is no longer written or read.
--   NOTE: director already has a working-hours schedule child table, so we
--         do NOT add working_hours here.
--
-- WORKER (department_workers / department_worker_tr):
--   * phone_code    -> NEUTRAL varchar(50)  on the parent row
--       (email / phone already exist on the parent row)
--   * room          -> BILINGUAL varchar(255) on the *_tr sibling
--   * working_hours -> BILINGUAL varchar(500) on the *_tr sibling
--
-- Neon / alembic-unstamped DB: additive & idempotent only.
-- =====================================================================


-- ── DIRECTOR: neutral contact columns on parent ─────────────────────
alter table department_directors add column if not exists email       varchar(255);
alter table department_directors add column if not exists phone       varchar(100);
alter table department_directors add column if not exists phone_code  varchar(50);

-- ── DIRECTOR: bilingual room on the translation sibling ─────────────
alter table department_director_tr add column if not exists room varchar(255);

-- Backfill room from the deprecated neutral room_number into both langs.
update department_director_tr t
set    room = d.room_number
from   department_directors d
where  t.director_id = d.id
  and  t.room is null
  and  d.room_number is not null
  and  d.room_number <> '';


-- ── WORKER: neutral phone_code on parent ────────────────────────────
alter table department_workers add column if not exists phone_code varchar(50);

-- ── WORKER: bilingual room + working_hours on the translation sibling ─
alter table department_worker_tr add column if not exists room          varchar(255);
alter table department_worker_tr add column if not exists working_hours varchar(500);


-- ── Verify ──────────────────────────────────────────────────────────
select table_name, column_name, data_type, character_maximum_length
from   information_schema.columns
where  (table_name = 'department_directors'   and column_name in ('email', 'phone', 'phone_code'))
   or  (table_name = 'department_director_tr'  and column_name in ('room'))
   or  (table_name = 'department_workers'      and column_name in ('phone_code'))
   or  (table_name = 'department_worker_tr'    and column_name in ('room', 'working_hours'))
order by table_name, column_name;

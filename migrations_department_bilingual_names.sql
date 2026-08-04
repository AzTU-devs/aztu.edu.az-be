-- =====================================================================
-- MIGRATION — Department module: bilingual names, drop father_name
--
-- Makes the person NAME bilingual for the two person entities of the
-- DEPARTMENT module (director and worker), mirroring how `room` was moved
-- onto the *_tr sibling. This module has NO deputy and NO scientific
-- council, so only these two entities are touched.
--
-- For each in-scope person:
--   * first_name / last_name -> BILINGUAL varchar(100) on the *_tr sibling.
--       We ADD them to the tr table and BACKFILL from the deprecated neutral
--       parent columns into BOTH the az and en tr rows (only where null).
--   * The neutral parent first_name / last_name become NULLABLE. They stay
--       in place (deprecated) and are still mirrored from the az name for
--       backward-compat / NOT NULL safety.
--   * father_name is DROPPED from the parent entirely.
--
-- Neon / alembic-unstamped DB: additive/idempotent only.
-- =====================================================================


-- ── DIRECTOR: bilingual name on the translation sibling ─────────────
alter table department_director_tr add column if not exists first_name varchar(100);
alter table department_director_tr add column if not exists last_name  varchar(100);

-- Backfill name from the deprecated neutral parent columns into both langs.
update department_director_tr t
set    first_name = d.first_name,
       last_name  = d.last_name
from   department_directors d
where  t.director_id = d.id
  and  t.first_name is null;

-- Relax the neutral columns (deprecated, now mirrored from az) and drop father_name.
alter table department_directors alter column first_name drop not null;
alter table department_directors alter column last_name  drop not null;
alter table department_directors drop column if exists father_name;


-- ── WORKER: bilingual name on the translation sibling ───────────────
alter table department_worker_tr add column if not exists first_name varchar(100);
alter table department_worker_tr add column if not exists last_name  varchar(100);

-- Backfill name from the deprecated neutral parent columns into both langs.
update department_worker_tr t
set    first_name = w.first_name,
       last_name  = w.last_name
from   department_workers w
where  t.worker_id = w.id
  and  t.first_name is null;

-- Relax the neutral columns (deprecated, now mirrored from az) and drop father_name.
alter table department_workers alter column first_name drop not null;
alter table department_workers alter column last_name  drop not null;
alter table department_workers drop column if exists father_name;


-- ── Verify: new tr columns exist, father_name gone, sample backfill ─
select table_name, column_name, data_type, character_maximum_length
from   information_schema.columns
where  (table_name = 'department_director_tr' and column_name in ('first_name', 'last_name'))
   or  (table_name = 'department_worker_tr'   and column_name in ('first_name', 'last_name'))
order by table_name, column_name;

select 'father_name remaining' as check, count(*) as cols
from   information_schema.columns
where  table_name in ('department_directors', 'department_workers')
  and  column_name = 'father_name';

select 'director_tr sample' as src, director_id, lang_code, first_name, last_name
from   department_director_tr
order by director_id, lang_code
limit 4;

select 'worker_tr sample' as src, worker_id, lang_code, first_name, last_name
from   department_worker_tr
order by worker_id, lang_code
limit 4;

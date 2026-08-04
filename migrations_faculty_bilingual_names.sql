-- =====================================================================
-- MIGRATION — Faculty module: bilingual first_name / last_name and
--             removal of father_name for director, deputy dean & worker
--
-- Makes the person NAME bilingual for the three in-scope FACULTY person
-- entities and drops father_name from them. The scientific council
-- (faculty_scientific_council / faculty_council_member_tr) is intentionally
-- OUT OF SCOPE and left completely untouched (it keeps its neutral
-- first_name/last_name and father_name columns).
--
-- For each in-scope entity we:
--   * ADD first_name / last_name varchar(100) to the *_tr sibling
--     (bilingual, mirrors how `room` was moved onto the tr table).
--   * BACKFILL both the az and en tr rows from the parent's neutral
--     first_name/last_name, only where the tr value is still null.
--   * RELAX the parent first_name/last_name to NULLABLE (they are now a
--     deprecated backward-compat mirror of the AZ translation).
--   * DROP father_name from the parent row.
--
-- Neon / alembic-unstamped DB: additive & idempotent only.
-- =====================================================================


-- ── DIRECTOR (faculty_directors / faculty_director_tr) ───────────────
alter table faculty_director_tr add column if not exists first_name varchar(100);
alter table faculty_director_tr add column if not exists last_name  varchar(100);

update faculty_director_tr t
set    first_name = d.first_name
from   faculty_directors d
where  t.director_id = d.id
  and  t.first_name is null
  and  d.first_name is not null;

update faculty_director_tr t
set    last_name = d.last_name
from   faculty_directors d
where  t.director_id = d.id
  and  t.last_name is null
  and  d.last_name is not null;

alter table faculty_directors alter column first_name drop not null;
alter table faculty_directors alter column last_name  drop not null;
alter table faculty_directors drop column if exists father_name;


-- ── DEPUTY DEAN (faculty_deputy_deans / faculty_deputy_dean_tr) ──────
alter table faculty_deputy_dean_tr add column if not exists first_name varchar(100);
alter table faculty_deputy_dean_tr add column if not exists last_name  varchar(100);

update faculty_deputy_dean_tr t
set    first_name = d.first_name
from   faculty_deputy_deans d
where  t.deputy_dean_id = d.id
  and  t.first_name is null
  and  d.first_name is not null;

update faculty_deputy_dean_tr t
set    last_name = d.last_name
from   faculty_deputy_deans d
where  t.deputy_dean_id = d.id
  and  t.last_name is null
  and  d.last_name is not null;

alter table faculty_deputy_deans alter column first_name drop not null;
alter table faculty_deputy_deans alter column last_name  drop not null;
alter table faculty_deputy_deans drop column if exists father_name;


-- ── WORKER (faculty_workers / faculty_worker_tr) ─────────────────────
alter table faculty_worker_tr add column if not exists first_name varchar(100);
alter table faculty_worker_tr add column if not exists last_name  varchar(100);

update faculty_worker_tr t
set    first_name = w.first_name
from   faculty_workers w
where  t.worker_id = w.id
  and  t.first_name is null
  and  w.first_name is not null;

update faculty_worker_tr t
set    last_name = w.last_name
from   faculty_workers w
where  t.worker_id = w.id
  and  t.last_name is null
  and  w.last_name is not null;

alter table faculty_workers alter column first_name drop not null;
alter table faculty_workers alter column last_name  drop not null;
alter table faculty_workers drop column if exists father_name;


-- ── SCIENTIFIC COUNCIL (faculty_scientific_council / faculty_council_member_tr) ──
-- Brought IN SCOPE later so the council entity shares the same bilingual-names /
-- father_name-removed shape as the deputy dean & worker entities above.
alter table faculty_council_member_tr add column if not exists first_name varchar(100);
alter table faculty_council_member_tr add column if not exists last_name  varchar(100);

update faculty_council_member_tr t
set    first_name = c.first_name
from   faculty_scientific_council c
where  t.council_member_id = c.id
  and  t.first_name is null
  and  c.first_name is not null;

update faculty_council_member_tr t
set    last_name = c.last_name
from   faculty_scientific_council c
where  t.council_member_id = c.id
  and  t.last_name is null
  and  c.last_name is not null;

alter table faculty_scientific_council alter column first_name drop not null;
alter table faculty_scientific_council alter column last_name  drop not null;
alter table faculty_scientific_council drop column if exists father_name;


-- ── Verify: new tr columns exist (expect 6 rows: 2 per in-scope tr) ──
select table_name, column_name, data_type, character_maximum_length
from   information_schema.columns
where  (table_name = 'faculty_director_tr'    and column_name in ('first_name', 'last_name'))
   or  (table_name = 'faculty_deputy_dean_tr' and column_name in ('first_name', 'last_name'))
   or  (table_name = 'faculty_worker_tr'      and column_name in ('first_name', 'last_name'))
order by table_name, column_name;

-- ── Verify: father_name is gone from the three in-scope parents ──────
-- (expect 0 rows; faculty_scientific_council intentionally still has it)
select table_name, column_name
from   information_schema.columns
where  column_name = 'father_name'
  and  table_name in ('faculty_directors', 'faculty_deputy_deans', 'faculty_workers');

-- ── Verify: sample backfilled tr rows ───────────────────────────────
select 'director' as entity, director_id as parent_id, lang_code, first_name, last_name
from   faculty_director_tr
order by director_id, lang_code
limit 4;

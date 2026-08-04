-- =====================================================================
-- MIGRATION — Cafedra module: bilingual names + drop father_name
--
-- For every person entity of the CAFEDRA module — DIRECTOR, DEPUTY
-- DIRECTOR, WORKER and SCIENTIFIC COUNCIL — the name becomes BILINGUAL (moved onto
-- the *_tr translation sibling, served per-lang and as nested az/en)
-- and the neutral `father_name` column is DROPPED.
--
--   * first_name / last_name -> BILINGUAL varchar(100) on the *_tr row.
--       Backfilled from the deprecated neutral parent columns into BOTH
--       the az and en tr rows (only where the tr value is still null).
--   * the neutral parent first_name / last_name columns are kept
--       (deprecated) but made NULLABLE — they are now only mirrored from
--       the az translation for backward-compat.
--   * father_name is DROPPED from each parent.
--
-- Neon / alembic-unstamped DB: idempotent only.
-- =====================================================================


-- ── DIRECTOR ────────────────────────────────────────────────────────
alter table cafedra_director_tr add column if not exists first_name varchar(100);
alter table cafedra_director_tr add column if not exists last_name  varchar(100);

update cafedra_director_tr t
set    first_name = d.first_name,
       last_name  = d.last_name
from   cafedra_directors d
where  t.director_id = d.id
  and  t.first_name is null;

alter table cafedra_directors alter column first_name drop not null;
alter table cafedra_directors alter column last_name  drop not null;
alter table cafedra_directors drop column if exists father_name;


-- ── DEPUTY DIRECTOR ─────────────────────────────────────────────────
alter table cafedra_deputy_director_tr add column if not exists first_name varchar(100);
alter table cafedra_deputy_director_tr add column if not exists last_name  varchar(100);

update cafedra_deputy_director_tr t
set    first_name = d.first_name,
       last_name  = d.last_name
from   cafedra_deputy_directors d
where  t.deputy_director_id = d.id
  and  t.first_name is null;

alter table cafedra_deputy_directors alter column first_name drop not null;
alter table cafedra_deputy_directors alter column last_name  drop not null;
alter table cafedra_deputy_directors drop column if exists father_name;


-- ── WORKER ──────────────────────────────────────────────────────────
alter table cafedra_worker_tr add column if not exists first_name varchar(100);
alter table cafedra_worker_tr add column if not exists last_name  varchar(100);

update cafedra_worker_tr t
set    first_name = w.first_name,
       last_name  = w.last_name
from   cafedra_workers w
where  t.worker_id = w.id
  and  t.first_name is null;

alter table cafedra_workers alter column first_name drop not null;
alter table cafedra_workers alter column last_name  drop not null;
alter table cafedra_workers drop column if exists father_name;


-- ── SCIENTIFIC COUNCIL ──────────────────────────────────────────────
-- Council now matches the other person entities: bilingual names on the
-- *_tr row, neutral parent names made nullable, father_name dropped.
alter table cafedra_council_member_tr add column if not exists first_name varchar(100);
alter table cafedra_council_member_tr add column if not exists last_name  varchar(100);

update cafedra_council_member_tr t
set    first_name = c.first_name,
       last_name  = c.last_name
from   cafedra_scientific_council c
where  t.council_member_id = c.id
  and  t.first_name is null;

alter table cafedra_scientific_council alter column first_name drop not null;
alter table cafedra_scientific_council alter column last_name  drop not null;
alter table cafedra_scientific_council drop column if exists father_name;


-- ── Verify ──────────────────────────────────────────────────────────
-- (a) the eight new tr columns exist
select table_name, column_name, data_type, character_maximum_length
from   information_schema.columns
where  (table_name = 'cafedra_director_tr'          and column_name in ('first_name', 'last_name'))
   or  (table_name = 'cafedra_deputy_director_tr'   and column_name in ('first_name', 'last_name'))
   or  (table_name = 'cafedra_worker_tr'            and column_name in ('first_name', 'last_name'))
   or  (table_name = 'cafedra_council_member_tr'    and column_name in ('first_name', 'last_name'))
order by table_name, column_name;

-- (b) father_name is gone from every person parent (council included)
select table_name, column_name
from   information_schema.columns
where  column_name = 'father_name'
  and  table_name in (
        'cafedra_directors', 'cafedra_deputy_directors', 'cafedra_workers',
        'cafedra_scientific_council'
       )
order by table_name;

-- (c) a sample backfilled worker translation row
select t.worker_id, t.lang_code, t.first_name, t.last_name
from   cafedra_worker_tr t
order by t.worker_id, t.lang_code
limit 5;

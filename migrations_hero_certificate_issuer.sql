-- =====================================================================
-- MIGRATION — Hero Certificates: second issuer (AQAS)
--
-- migrations_hero_certificates.sql IS ALREADY APPLIED and must NOT be
-- edited: the live table already holds 4 real QS certificates entered
-- from the dashboard. This file only ALTERs that existing table.
--
-- AzTU also holds AQAS certificates. AQAS is a German programme-
-- accreditation agency, NOT a ranking body: its certificates are issued
-- per programme ("Process Automation Engineering (MA)") and carry no
-- rank position and no ranking family. The original schema forced every
-- certificate to look like a QS ranking — that is what this fixes.
--
-- Adds:
--   hero_certificate.issuer  varchar(16) not null default 'qs'
--       'qs' | 'aqas'. Defaulted so the 4 existing rows are backfilled by
--       the ALTER itself and so an older client that never sends the
--       field keeps producing QS rows.
--
-- Relaxes:
--   hero_certificate.rank_label  -> nullable  (AQAS has no rank)
--   hero_certificate.family      -> nullable  (world/europe/subject is QS-only)
--
-- Why no check constraint on the issuer/rank_label/family matrix: same
-- reason the "at least one of image / document / external_url" rule has
-- none — the API owns the rule (422) so an editor can never be locked out
-- of an existing row by a constraint that predates it.
--
-- Run AFTER migrations_hero_certificates.sql. Idempotent, additive and
-- safe to run twice.
--
-- ORDERING — APPLY THIS *BEFORE* DEPLOYING THE BACKEND THAT GOES WITH IT.
-- The ORM model declares `issuer`, so every SELECT against hero_certificate
-- emits the column. Ship the code first and /api/hero-certificate/public
-- answers 500 (UndefinedColumn) until this file lands; the live homepage
-- swallows that error and renders the hero with ZERO certificates, so the
-- 4 QS slides silently disappear. Applying this file first is safe in the
-- other direction: the currently-deployed backend never names the column,
-- and the default keeps its writes on 'qs'.
-- =====================================================================


-- =====================================================================
-- STEP 1 — SCHEMA
-- =====================================================================
-- New column. `not null default 'qs'` backfills every existing row in the
-- same statement; `if not exists` makes a re-run a no-op.
alter table hero_certificate
    add column if not exists issuer varchar(16) not null default 'qs';

-- Drop the two NOT NULLs. `drop not null` is idempotent — dropping a
-- constraint that is already gone succeeds silently.
alter table hero_certificate alter column rank_label drop not null;
alter table hero_certificate alter column family     drop not null;


-- =====================================================================
-- STEP 2 — BACKFILL (belt and braces)
--
-- The ALTER above already wrote 'qs' into every pre-existing row. This
-- update only matters if the column was somehow added without the
-- default on an earlier partial run. All 4 live rows are QS.
-- =====================================================================
update hero_certificate
   set issuer = 'qs'
 where issuer is null
    or btrim(issuer) = '';


-- =====================================================================
-- STEP 3 — VERIFY. Expect every existing row to read issuer = 'qs', with
-- rank_label / family untouched. AQAS rows are entered from the
-- dashboard afterwards and will show issuer = 'aqas' with empty
-- rank_label and family.
-- =====================================================================
select c.certificate_id,
       c.issuer,
       c.rank_label,
       c.family,
       c.display_order,
       c.is_active,
       (select count(*) from hero_certificate_tr t
         where t.certificate_id = c.certificate_id) as translations
from hero_certificate c
order by c.display_order;

-- ============================================================================
--  Honorary doctors — manual equivalent of Alembic revision d4e5f6a7b8c9
--  (revises c2d3e4f5a6b7)
--
--  Run this INSTEAD of `alembic upgrade head`, not in addition to it.
--  It creates the two tables and then moves alembic_version forward, so a later
--  `alembic upgrade head` skips this revision rather than trying to create the
--  tables a second time.
--
--  STEP 0 FIRST. The stamp at the end only fires if the database is currently on
--  c2d3e4f5a6b7. If step 0 shows anything else, stop and read the notes at the
--  bottom of this file.
-- ============================================================================


-- ── STEP 0 — preflight, run on its own and read the output ──────────────────
-- Expected: exactly one row, version_num = 'c2d3e4f5a6b7'.
SELECT version_num FROM alembic_version;

-- Expected: 0. If it returns 2, the tables already exist and you are done.
SELECT count(*) AS existing_tables
FROM   information_schema.tables
WHERE  table_schema = current_schema()
AND    table_name IN ('honorary_doctor', 'honorary_doctor_tr');


-- ── STEP 1 — the migration ──────────────────────────────────────────────────
BEGIN;

CREATE TABLE IF NOT EXISTS honorary_doctor (
    id            SERIAL       PRIMARY KEY,
    image         TEXT         NULL,
    display_order INTEGER      NOT NULL,
    is_active     BOOLEAN      NOT NULL DEFAULT true,
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT now(),
    updated_at    TIMESTAMPTZ  NULL
);

CREATE INDEX IF NOT EXISTS ix_honorary_doctor_id
    ON honorary_doctor (id);

CREATE TABLE IF NOT EXISTS honorary_doctor_tr (
    id          SERIAL      PRIMARY KEY,
    doctor_id   INTEGER     NOT NULL,
    lang_code   VARCHAR(2)  NOT NULL,
    full_name   TEXT        NOT NULL,
    description TEXT        NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NULL,
    CONSTRAINT honorary_doctor_tr_doctor_id_fkey
        FOREIGN KEY (doctor_id) REFERENCES honorary_doctor (id) ON DELETE CASCADE,
    -- One row per language per person: the service upserts on (doctor_id, lang_code).
    CONSTRAINT uq_honorary_doctor_tr_doctor_lang UNIQUE (doctor_id, lang_code)
);

CREATE INDEX IF NOT EXISTS ix_honorary_doctor_tr_id
    ON honorary_doctor_tr (id);

CREATE INDEX IF NOT EXISTS ix_honorary_doctor_tr_doctor_id
    ON honorary_doctor_tr (doctor_id);

-- Move the revision pointer. Guarded by the WHERE clause, so if the database is
-- not on the expected parent revision this updates 0 rows and you can resolve it
-- before anything drifts. Check the reported row count: it must be 1.
UPDATE alembic_version
SET    version_num = 'd4e5f6a7b8c9'
WHERE  version_num = 'c2d3e4f5a6b7';

COMMIT;


-- ── STEP 2 — verify ─────────────────────────────────────────────────────────
-- Expected: 'd4e5f6a7b8c9'
SELECT version_num FROM alembic_version;

-- Expected: 2 rows — honorary_doctor, honorary_doctor_tr
SELECT table_name
FROM   information_schema.tables
WHERE  table_schema = current_schema()
AND    table_name IN ('honorary_doctor', 'honorary_doctor_tr')
ORDER  BY table_name;

-- Expected: 3 rows — the two ix_* indexes on _tr and one on the parent
SELECT indexname
FROM   pg_indexes
WHERE  schemaname = current_schema()
AND    tablename IN ('honorary_doctor', 'honorary_doctor_tr')
ORDER  BY indexname;


-- ============================================================================
--  NOTES
--
--  If STEP 0 returned a version other than 'c2d3e4f5a6b7':
--    The database is not on the revision this migration was written against.
--    Do NOT edit the WHERE clause to force the stamp — that would mark the
--    intervening revisions as applied without running them. Run
--    `alembic upgrade head` instead, which applies everything in order
--    including this one, and skip this file entirely.
--
--  If STEP 0 showed the tables already exist:
--    Someone has already applied this. Run only the STEP 2 queries to confirm
--    the version pointer is 'd4e5f6a7b8c9'.
--
--  Rollback (drops the roll and everything in it):
--    BEGIN;
--    DROP TABLE IF EXISTS honorary_doctor_tr;
--    DROP TABLE IF EXISTS honorary_doctor;
--    UPDATE alembic_version
--    SET    version_num = 'c2d3e4f5a6b7'
--    WHERE  version_num = 'd4e5f6a7b8c9';
--    COMMIT;
-- ============================================================================

-- ============================================================================
--  Honorary doctors — manual equivalent of Alembic revision d4e5f6a7b8c9
--
--  Production has no `alembic_version` table: alembic has never been run against
--  it, and the schema was created out of band. So this file only creates the
--  tables. It deliberately does NOT write a revision stamp — inserting one would
--  assert that every migration up to this one has been applied, which is not
--  established, and would make a later `alembic upgrade head` skip real work.
--
--  Safe to re-run: every statement is IF NOT EXISTS, and the whole thing is one
--  transaction, so a failure leaves the database untouched.
-- ============================================================================


-- ── STEP 0 — preflight ──────────────────────────────────────────────────────
-- Expected: 0. If it returns 2 the tables are already there and you are done.
SELECT count(*) AS existing_tables
FROM   information_schema.tables
WHERE  table_schema = current_schema()
AND    table_name IN ('honorary_doctor', 'honorary_doctor_tr');


-- ── STEP 1 — create the tables ──────────────────────────────────────────────
BEGIN;

CREATE TABLE IF NOT EXISTS honorary_doctor (
    id            SERIAL       PRIMARY KEY,
    image         TEXT         NULL,
    display_order INTEGER      NOT NULL,
    is_active     BOOLEAN      NOT NULL DEFAULT true,
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT now(),
    updated_at    TIMESTAMPTZ  NULL
);

-- Redundant with the primary key index, but the model declares index=True and
-- this keeps the schema matching what alembic autogenerate expects.
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

COMMIT;


-- ── STEP 2 — verify ─────────────────────────────────────────────────────────
-- Expected: 2 rows
SELECT table_name
FROM   information_schema.tables
WHERE  table_schema = current_schema()
AND    table_name IN ('honorary_doctor', 'honorary_doctor_tr')
ORDER  BY table_name;

-- Expected: 3 ix_* rows plus the two primary key indexes
SELECT indexname
FROM   pg_indexes
WHERE  schemaname = current_schema()
AND    tablename IN ('honorary_doctor', 'honorary_doctor_tr')
ORDER  BY indexname;

-- Expected: the unique constraint and the cascading foreign key
SELECT conname, contype
FROM   pg_constraint
WHERE  conrelid = 'honorary_doctor_tr'::regclass
ORDER  BY conname;


-- ============================================================================
--  ROLLBACK — drops the roll and everything in it
--
--    BEGIN;
--    DROP TABLE IF EXISTS honorary_doctor_tr;
--    DROP TABLE IF EXISTS honorary_doctor;
--    COMMIT;
--
--  ON ADOPTING ALEMBIC LATER
--    Do not simply create `alembic_version` and insert this revision. That claims
--    every earlier migration has run, and the ones that have not would then be
--    skipped forever. Adopting alembic means first diffing the live schema
--    against Base.metadata, then stamping the revision the database genuinely
--    matches. Worth doing deliberately, not as part of this change.
-- ============================================================================

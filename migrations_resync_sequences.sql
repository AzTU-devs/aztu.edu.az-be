-- =====================================================================
-- Resync every identity/serial sequence to max(id).
--
-- Fixes: duplicate key value violates unique constraint "<table>_pkey"
--        DETAIL: Key (id)=(N) already exists.
--
-- Cause: rows were inserted with EXPLICIT ids (seed files, data imports,
-- restores), which does not advance the sequence. The sequence then hands out
-- ids that are already taken, and every insert fails until it catches up.
--
-- Why migrations_fix_identity.sql does not cover this: that script only touches
-- columns where is_identity = 'NO', so a table that already had an identity was
-- skipped and kept its stale sequence. This one resyncs unconditionally.
--
-- Safe: read-only apart from setval, idempotent, and a no-op on tables that are
-- already in sync. Run it after ANY seed file.
-- =====================================================================

do $$
declare
    r        record;
    seq      text;
    max_id   bigint;
    next_val bigint;
    fixed    int := 0;
begin
    for r in
        select c.table_schema, c.table_name, c.column_name
        from information_schema.columns c
        join information_schema.table_constraints tc
          on  tc.table_schema   = c.table_schema
          and tc.table_name     = c.table_name
          and tc.constraint_type = 'PRIMARY KEY'
        join information_schema.key_column_usage k
          on  k.constraint_name = tc.constraint_name
          and k.table_schema    = tc.table_schema
          and k.column_name     = c.column_name
        where c.table_schema = 'public'
          and c.data_type in ('integer', 'bigint')
    loop
        seq := pg_get_serial_sequence(
            format('%I.%I', r.table_schema, r.table_name), r.column_name
        );
        -- No sequence at all means the column is a plain integer PK; that is the
        -- separate problem migrations_fix_identity.sql exists to solve.
        continue when seq is null;

        execute format('select coalesce(max(%I), 0) from %I.%I',
                       r.column_name, r.table_schema, r.table_name)
        into max_id;

        execute format('select last_value from %s', seq) into next_val;

        if next_val <= max_id then
            perform setval(seq, max_id, true);
            fixed := fixed + 1;
            raise notice 'resynced %.% (%): sequence was %, max(id) is %',
                r.table_schema, r.table_name, r.column_name, next_val, max_id;
        end if;
    end loop;

    raise notice 'sequences resynced: %', fixed;
end $$;


-- =====================================================================
-- Verification. Re-checks every sequence and reports any still behind.
-- Expected output: "sequences still behind: 0".
-- =====================================================================
do $$
declare
    r        record;
    seq      text;
    max_id   bigint;
    next_val bigint;
    behind   int := 0;
begin
    for r in
        select c.table_schema, c.table_name, c.column_name
        from information_schema.columns c
        join information_schema.table_constraints tc
          on  tc.table_schema   = c.table_schema
          and tc.table_name     = c.table_name
          and tc.constraint_type = 'PRIMARY KEY'
        join information_schema.key_column_usage k
          on  k.constraint_name = tc.constraint_name
          and k.table_schema    = tc.table_schema
          and k.column_name     = c.column_name
        where c.table_schema = 'public'
          and c.data_type in ('integer', 'bigint')
    loop
        seq := pg_get_serial_sequence(
            format('%I.%I', r.table_schema, r.table_name), r.column_name
        );
        continue when seq is null;

        execute format('select coalesce(max(%I), 0) from %I.%I',
                       r.column_name, r.table_schema, r.table_name)
        into max_id;
        execute format('select last_value from %s', seq) into next_val;

        if next_val < max_id then
            behind := behind + 1;
            raise warning 'STILL BEHIND: %.% sequence=% max=%',
                r.table_schema, r.table_name, next_val, max_id;
        end if;
    end loop;

    raise notice 'sequences still behind: %', behind;
end $$;

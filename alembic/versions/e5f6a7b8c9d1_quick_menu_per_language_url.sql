-- ============================================================================
--  Quick menu per-language URL — manual equivalent of revision e5f6a7b8c9d1
--
--  Production has no alembic_version table, so this is DDL only, no stamp.
--  Safe to re-run: IF NOT EXISTS on both columns, one transaction.
--
--  NULL means "use the shared url on the parent row", so existing quick-menu
--  links keep working with no backfill.
-- ============================================================================

BEGIN;

ALTER TABLE menu_quick_left_item_translations
    ADD COLUMN IF NOT EXISTS url TEXT NULL;

ALTER TABLE menu_quick_section_item_translations
    ADD COLUMN IF NOT EXISTS url TEXT NULL;

COMMIT;

-- Verify — expect two rows, both is_nullable = YES
SELECT table_name, column_name, data_type, is_nullable
FROM   information_schema.columns
WHERE  table_schema = current_schema()
AND    table_name IN ('menu_quick_left_item_translations',
                      'menu_quick_section_item_translations')
AND    column_name = 'url'
ORDER  BY table_name;

-- Rollback:
--   BEGIN;
--   ALTER TABLE menu_quick_section_item_translations DROP COLUMN IF EXISTS url;
--   ALTER TABLE menu_quick_left_item_translations    DROP COLUMN IF EXISTS url;
--   COMMIT;

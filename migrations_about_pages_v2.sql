-- =====================================================================
-- MIGRATION — About pages, follow-up columns
--
-- Additive only; safe to run on a database that already has the About
-- tables and content. Run AFTER migrations_about_pages.sql.
--
--   about_section_tr.video_url  → the 75th-anniversary film is a different
--                                 YouTube cut per language, so the URL has
--                                 to sit on the translation, not the block.
--   about_section_tr.list_intro → blocks like "Rektora tabe olan strukturlar"
--                                 carry a heading, an intro paragraph AND a
--                                 list; description was already taken by the
--                                 plain-text lead, so the rich-text intro
--                                 needs its own column.
-- =====================================================================

alter table about_section_tr add column if not exists video_url  varchar(2048);
alter table about_section_tr add column if not exists list_intro text;


-- =====================================================================
-- VERIFY — expect both rows.
-- =====================================================================
select column_name, data_type
from information_schema.columns
where table_name = 'about_section_tr'
  and column_name in ('video_url', 'list_intro')
order by column_name;

-- =====================================================================
-- MIGRATION — Academic: "CDIO" (Təhsil və proqramlar)
--
-- The second page of the Akademik → Təhsil və proqramlar sub-section.
-- Like the MBA page it reuses the About CMS with NO new tables/columns:
-- an about_page with template 'cdio' and an /akademik/... slug, assembled
-- from the generic children the model already has:
--
--   title / description          → page title and short description
--   section_title / section_body → "CDIO Initiative" heading + rich text
--   pillars_title                → the "What is CDIO?" heading
--   about_pillars                → the "What is CDIO?" text boxes; each box is
--                                  one pillar's rich description (no title/tags),
--                                  unlimited and reorderable
--   about_blocks:
--     institutes  → "CDIO Research Institutes at AzTU" heading + rich desc
--     society     → "Student Scientific Society" heading + rich desc
--   about_lists:
--     institute_items → the institute names (bilingual, unlimited)
--     society_items   → the Student Scientific Society list (bilingual)
--
-- There is deliberately no "More in this section" — the page has none.
-- Seeding the blocks/lists just gives the editor stable rows with sensible
-- default headings; the dashboard self-heals if any are missing.
--
-- Run AFTER migrations_academic_mba.sql. Idempotent and additive.
-- =====================================================================


-- =====================================================================
-- STEP 1 — the page
-- =====================================================================
insert into about_pages (page_key, template, slug_az, slug_en, display_order, is_active, created_at)
values ('cdio', 'cdio',
        'akademik/tehsil-ve-proqramlar/cdio',
        'academic/education-and-programs/cdio', 16, false, current_timestamp)
on conflict (page_key) do nothing;

insert into about_page_tr (page_id, lang_code, title, section_title, pillars_title, created_at)
select p.id, 'az', 'CDIO', 'CDIO Təşəbbüsü', 'CDIO nədir?', current_timestamp
from about_pages p where p.page_key = 'cdio'
on conflict (page_id, lang_code) do nothing;

insert into about_page_tr (page_id, lang_code, title, section_title, pillars_title, created_at)
select p.id, 'en', 'CDIO', 'CDIO Initiative', 'What is CDIO?', current_timestamp
from about_pages p where p.page_key = 'cdio'
on conflict (page_id, lang_code) do nothing;


-- =====================================================================
-- STEP 2 — blocks: the two heading + rich-text sections
-- =====================================================================
insert into about_blocks (page_id, block_key, display_order, created_at)
select p.id, v.block_key, v.ord, current_timestamp
from about_pages p
cross join (values ('institutes', 0), ('society', 1)) as v(block_key, ord)
where p.page_key = 'cdio'
on conflict (page_id, block_key) do nothing;

insert into about_block_tr (block_id, lang_code, title, created_at)
select b.id, 'az', v.title_az, current_timestamp
from about_blocks b join about_pages p on p.id = b.page_id
join (values
    ('institutes', 'AzTU-nun CDIO Tədqiqat İnstitutları'),
    ('society',    'Tələbə Elmi Cəmiyyəti')
) as v(block_key, title_az) on v.block_key = b.block_key
where p.page_key = 'cdio'
on conflict (block_id, lang_code) do nothing;

insert into about_block_tr (block_id, lang_code, title, created_at)
select b.id, 'en', v.title_en, current_timestamp
from about_blocks b join about_pages p on p.id = b.page_id
join (values
    ('institutes', 'CDIO Research Institutes at AzTU'),
    ('society',    'Student Scientific Society')
) as v(block_key, title_en) on v.block_key = b.block_key
where p.page_key = 'cdio'
on conflict (block_id, lang_code) do nothing;


-- =====================================================================
-- STEP 3 — lists: the institute names and the society list
-- =====================================================================
insert into about_lists (page_id, list_key, style, display_order, created_at)
select p.id, v.list_key, 'bullet', v.ord, current_timestamp
from about_pages p
cross join (values ('institute_items', 1), ('society_items', 2)) as v(list_key, ord)
where p.page_key = 'cdio'
on conflict (page_id, list_key) do nothing;


-- =====================================================================
-- STEP 4 — VERIFY. Expect the cdio page, 2 blocks, 2 lists, unpublished.
-- =====================================================================
select p.page_key, p.template, p.display_order, p.is_active,
       (select count(*) from about_blocks b where b.page_id = p.id) as blocks,
       (select count(*) from about_lists  l where l.page_id = p.id) as lists
from about_pages p
where p.page_key = 'cdio';

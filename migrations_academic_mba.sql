-- =====================================================================
-- MIGRATION — Academic: "MBA" (Təhsil və proqramlar)
--
-- The first page of the new Akademik section. It reuses the About CMS
-- wholesale — NO new tables or columns. The page is an about_page with
-- template 'mba' and an /akademik/... slug; its content is assembled from
-- the generic children the model already has:
--
--   title / description         → page title and short description
--   section_title / section_body → "About the MBA Program" heading + text
--   pillars_title               → the "Program Highlights" heading
--   about_lists:
--     highlights          → the 4 highlight numbers (fixed labels live on
--                            the website); language-neutral, 4 positions
--     languages           → Languages of Instruction (title + items)
--     program_structure   → Program Structure (title + items)
--     doctoral_formats    → the 3 doctoral format cards (items)
--     phd                 → Doctor of Philosophy card (title + items)
--     doctor_of_sciences  → Doctor of Sciences card (title + items)
--     phones              → contact phone numbers (language-neutral items)
--     emails              → contact e-mails (language-neutral items)
--   about_blocks:
--     doctoral            → "Doctoral Pathways" heading + rich description
--     contact             → the contact address (in the block body)
--   about_links                 → the "More in this section" buttons
--
-- Seeding the blocks/lists here just gives the editor stable rows with
-- sensible default headings; the dashboard also self-heals if any are
-- missing. Idempotent and additive.
--
-- Run AFTER migrations_about_regulatory_documents.sql.
-- =====================================================================


-- =====================================================================
-- STEP 1 — the page
-- =====================================================================
insert into about_pages (page_key, template, slug_az, slug_en, display_order, is_active, created_at)
values ('mba', 'mba',
        'akademik/tehsil-ve-proqramlar/mba',
        'academic/education-and-programs/mba', 15, false, current_timestamp)
on conflict (page_key) do nothing;

insert into about_page_tr (page_id, lang_code, title, section_title, pillars_title, links_title, created_at)
select p.id, 'az', 'MBA Proqramı', 'MBA Proqramı haqqında',
       'Proqramın əsas göstəriciləri', 'Bölmədə daha çox', current_timestamp
from about_pages p where p.page_key = 'mba'
on conflict (page_id, lang_code) do nothing;

insert into about_page_tr (page_id, lang_code, title, section_title, pillars_title, links_title, created_at)
select p.id, 'en', 'MBA Program', 'About the MBA Program',
       'Program Highlights', 'More in this section', current_timestamp
from about_pages p where p.page_key = 'mba'
on conflict (page_id, lang_code) do nothing;


-- =====================================================================
-- STEP 2 — blocks: the two heading + rich-text sections
-- =====================================================================
insert into about_blocks (page_id, block_key, display_order, created_at)
select p.id, v.block_key, v.ord, current_timestamp
from about_pages p
cross join (values ('doctoral', 0), ('contact', 1)) as v(block_key, ord)
where p.page_key = 'mba'
on conflict (page_id, block_key) do nothing;

-- Only the doctoral block gets a default heading; the contact block uses its
-- body for the address and needs no title.
insert into about_block_tr (block_id, lang_code, title, created_at)
select b.id, 'az', 'Doktorantura yolları', current_timestamp
from about_blocks b join about_pages p on p.id = b.page_id
where p.page_key = 'mba' and b.block_key = 'doctoral'
on conflict (block_id, lang_code) do nothing;

insert into about_block_tr (block_id, lang_code, title, created_at)
select b.id, 'en', 'Doctoral Pathways', current_timestamp
from about_blocks b join about_pages p on p.id = b.page_id
where p.page_key = 'mba' and b.block_key = 'doctoral'
on conflict (block_id, lang_code) do nothing;


-- =====================================================================
-- STEP 3 — lists: the highlight numbers and every itemised section
-- =====================================================================
insert into about_lists (page_id, list_key, style, display_order, created_at)
select p.id, v.list_key, v.style, v.ord, current_timestamp
from about_pages p
cross join (values
    ('highlights',         'number', 1),
    ('languages',          'bullet', 2),
    ('program_structure',  'bullet', 3),
    ('doctoral_formats',   'bullet', 4),
    ('phd',                'bullet', 5),
    ('doctor_of_sciences', 'bullet', 6),
    ('phones',             'bullet', 7),
    ('emails',             'bullet', 8)
) as v(list_key, style, ord)
where p.page_key = 'mba'
on conflict (page_id, list_key) do nothing;

-- Default headings for the sections that have a fixed name. The rest
-- (highlights, doctoral_formats, phones, emails) carry no heading.
insert into about_list_tr (list_id, lang_code, title, created_at)
select l.id, 'az', v.title_az, current_timestamp
from about_lists l join about_pages p on p.id = l.page_id
join (values
    ('languages',          'Tədris dilləri'),
    ('program_structure',  'Proqramın strukturu'),
    ('phd',                'Fəlsəfə doktoru (PhD)'),
    ('doctor_of_sciences', 'Elmlər doktoru')
) as v(list_key, title_az) on v.list_key = l.list_key
where p.page_key = 'mba'
on conflict (list_id, lang_code) do nothing;

insert into about_list_tr (list_id, lang_code, title, created_at)
select l.id, 'en', v.title_en, current_timestamp
from about_lists l join about_pages p on p.id = l.page_id
join (values
    ('languages',          'Languages of Instruction'),
    ('program_structure',  'Program Structure'),
    ('phd',                'Doctor of Philosophy (PhD)'),
    ('doctor_of_sciences', 'Doctor of Sciences')
) as v(list_key, title_en) on v.list_key = l.list_key
where p.page_key = 'mba'
on conflict (list_id, lang_code) do nothing;


-- =====================================================================
-- STEP 4 — VERIFY. Expect the mba page, 2 blocks and 8 lists, unpublished.
-- =====================================================================
select p.page_key, p.template, p.display_order, p.is_active,
       (select count(*) from about_blocks b where b.page_id = p.id) as blocks,
       (select count(*) from about_lists  l where l.page_id = p.id) as lists
from about_pages p
where p.page_key = 'mba';

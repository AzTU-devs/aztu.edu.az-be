-- =====================================================================
-- MIGRATION — Research: "Elmi jurnallar" (Scientific Journals)
--
-- A set of journal pages in the Tədqiqat section (template 'journal').
-- Each reuses the research_pages hero (title + short description) and the
-- page's intro text (body_html = "About the journal"), and adds a block of
-- journal-specific columns:
--
--   research_pages (language-neutral):
--     image_url         → the cover image
--     issn / eissn      → the ISSN / E-ISSN numbers
--     doi               → a DOI string or URL
--     publication_year  → the publication year
--     yearly_count      → the yearly publication number
--     button_url        → the "visit the journal" button target
--   research_page_tr (per language):
--     journal_name      → the journal's own name (distinct from the title)
--     journal_language  → the language(s) the journal publishes in
--     founder           → the founder ("Jurnalın təsisçisi")
--     button_label      → the "visit the journal" button text
--
-- Seeds three journals (the fourth is added when its content is supplied).
-- Each stays unpublished until an editor publishes it. Idempotent/additive.
-- Run AFTER migrations_research_seminars.sql.
-- =====================================================================


-- ── STEP 1 — SCHEMA ─────────────────────────────────────────────────────
alter table research_pages    add column if not exists image_url        varchar(2048);
alter table research_pages    add column if not exists issn             varchar(50);
alter table research_pages    add column if not exists eissn            varchar(50);
alter table research_pages    add column if not exists doi              varchar(2048);
alter table research_pages    add column if not exists publication_year varchar(50);
alter table research_pages    add column if not exists yearly_count     varchar(50);
alter table research_pages    add column if not exists button_url       varchar(2048);
alter table research_page_tr  add column if not exists journal_name     varchar(500);
alter table research_page_tr  add column if not exists journal_language varchar(255);
alter table research_page_tr  add column if not exists founder          varchar(500);
alter table research_page_tr  add column if not exists button_label     varchar(500);


-- ── STEP 2 — SEED: the three journal pages ──────────────────────────────
insert into research_pages (page_key, template, slug_az, slug_en, display_order, is_active, created_at)
values
  ('journal-machine-science', 'journal',
   'tedqiqat/elmi-jurnallar/masin-elmi',
   'research/scientific-journals/machine-science', 3, false, current_timestamp),
  ('journal-energy-sustainability', 'journal',
   'tedqiqat/elmi-jurnallar/enerji-davamliligi-riskler-ve-qerarlarin-qebul-edilmesi',
   'research/scientific-journals/energy-sustainability-risks-and-decision-making', 4, false, current_timestamp),
  ('journal-scientific-works', 'journal',
   'tedqiqat/elmi-jurnallar/elmi-eserler',
   'research/scientific-journals/scientific-works', 5, false, current_timestamp)
on conflict (page_key) do nothing;

-- Titles + journal names + button label, per language.
insert into research_page_tr (page_id, lang_code, title, journal_name, button_label, created_at)
select p.id, 'az', v.title_az, v.title_az, 'Jurnalın saytına keç', current_timestamp
from research_pages p
join (values
  ('journal-machine-science',        'Maşınşünaslıq'),
  ('journal-energy-sustainability',  'Enerji Davamlılığı, Risklər və Qərarların Qəbul Edilməsi'),
  ('journal-scientific-works',       'Elmi Əsərlər')
) as v(page_key, title_az) on v.page_key = p.page_key
on conflict (page_id, lang_code) do nothing;

insert into research_page_tr (page_id, lang_code, title, journal_name, button_label, created_at)
select p.id, 'en', v.title_en, v.title_en, 'Visit the journal', current_timestamp
from research_pages p
join (values
  ('journal-machine-science',        'Machine Science'),
  ('journal-energy-sustainability',  'Energy Sustainability, Risks and Decision-Making'),
  ('journal-scientific-works',       'Scientific Works')
) as v(page_key, title_en) on v.page_key = p.page_key
on conflict (page_id, lang_code) do nothing;


-- ── STEP 3 — VERIFY. Expect three unpublished journal pages. ────────────
select page_key, template, display_order, is_active
from research_pages
where template = 'journal'
order by display_order;

-- =====================================================================
-- MIGRATION — Students ("Tələbələr"): the four "Tədris təqvimi və
-- qaydalar" pages. Fixed editorial pages on the About CMS, one template
-- each, seeded here. Their sections reuse the generic About children:
--
--   title / description  → page title + short description (all pages)
--   about_milestones     → the academic-calendar's semesters (year = the
--                          shared date string, title, rich description)
--   about_pillars + pillars_title → "Additional Information" cards
--   about_blocks         → each heading + rich-text section (download,
--                          assessment, requirement, grade, credit,
--                          bachelor, master, lms, guidelines, support)
--   about_lists          → the itemised lists (assessment_items,
--                          bachelor_items, master_items)
--   about_documents      → extra downloadable files (the LMS "trained
--                          staff" file), tagged by category_key
--   document_url + document_label → the primary "Download" button
--   about_pages.grade_scale (NEW jsonb column) → the grade-scale table,
--          rows of {points, grade, description_az, description_en}
--
-- The blocks/lists/documents are scaffolded by the dashboard, so only the
-- pages and their headings are seeded here. Idempotent and additive.
-- Run AFTER migrations_academic_cdio.sql.
-- =====================================================================


-- ── STEP 1 — SCHEMA: the grade-scale column ─────────────────────────────
alter table about_pages add column if not exists grade_scale jsonb;


-- ── STEP 2 — SEED: the four pages ───────────────────────────────────────
insert into about_pages (page_key, template, slug_az, slug_en, display_order, is_active, created_at)
values
  ('academic-calendar', 'academic-calendar',
   'telebeler/tedris-teqvimi-ve-qaydalar/2025-2026-tedris-ili-teqvimi',
   'students/academic-calendar-and-rules/2025-2026-academic-year-calendar', 17, false, current_timestamp),
  ('assessment-rules', 'assessment-rules',
   'telebeler/tedris-teqvimi-ve-qaydalar/qiymetlendirme-ve-imtahan-teskili-qaydalari',
   'students/academic-calendar-and-rules/assessment-and-examination-organization-rules', 18, false, current_timestamp),
  ('credit-system', 'credit-system',
   'telebeler/tedris-teqvimi-ve-qaydalar/bakalavr-ve-magistratura-seviyyelerinde-kredit-sistemi',
   'students/academic-calendar-and-rules/credit-system-at-bachelors-and-masters-levels', 19, false, current_timestamp),
  ('lms-guidelines', 'lms-guidelines',
   'telebeler/tedris-teqvimi-ve-qaydalar/lms-telimatlari',
   'students/academic-calendar-and-rules/lms-guidelines', 20, false, current_timestamp)
on conflict (page_key) do nothing;


-- Page titles, the "Additional Information" heading, and the download button.
insert into about_page_tr (page_id, lang_code, title, pillars_title, document_label, links_title, created_at)
select p.id, 'az', v.title_az, 'Əlavə məlumat', v.doc_label_az, 'Bölmədə daha çox', current_timestamp
from about_pages p
join (values
  ('academic-calendar', '2025-2026 Tədris İli üçün Akademik Təqvim', null),
  ('assessment-rules',  'Qiymətləndirmə və İmtahanın Təşkili Qaydaları', 'Sənədi yüklə'),
  ('credit-system',     'Bakalavr və Magistratura Səviyyələrində Kredit Sistemi', 'Sənədi yüklə'),
  ('lms-guidelines',    'LMS Təlimatları', 'Sənədi yüklə')
) as v(page_key, title_az, doc_label_az) on v.page_key = p.page_key
on conflict (page_id, lang_code) do nothing;

insert into about_page_tr (page_id, lang_code, title, pillars_title, document_label, links_title, created_at)
select p.id, 'en', v.title_en, 'Additional Information', v.doc_label_en, 'More in this section', current_timestamp
from about_pages p
join (values
  ('academic-calendar', 'Academic Calendar for the 2025-2026 Academic Year', null),
  ('assessment-rules',  'Assessment and Examination Organization Rules', 'Download Full Documentation'),
  ('credit-system',     'Credit System at Bachelor''s and Master''s Levels', 'Download Full Documentation'),
  ('lms-guidelines',    'LMS Guidelines', 'Download Full Documentation')
) as v(page_key, title_en, doc_label_en) on v.page_key = p.page_key
on conflict (page_id, lang_code) do nothing;


-- ── STEP 3 — VERIFY. Expect four new, unpublished pages. ────────────────
select page_key, template, display_order, is_active
from about_pages
where page_key in ('academic-calendar', 'assessment-rules', 'credit-system', 'lms-guidelines')
order by display_order;

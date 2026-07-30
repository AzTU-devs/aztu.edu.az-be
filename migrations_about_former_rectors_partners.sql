-- =====================================================================
-- MIGRATION — About: "Sabiq Rektorlarımız" (Former Rectors) and the
--                    "Partner Universities and Related Institutes" pages
--
-- Both page types are person-listing pages, so they reuse the generic
-- `about_persons` table rather than growing new ones. Three small columns
-- are added to carry what those pages need beyond a vice-rector card:
--   about_persons.year_start / .year_end  → a former rector's years in
--       office ("1950" .. "1955"). Language-neutral free text.
--   about_person_tr.surname               → the family name, kept separate
--       on the former-rectors page and for a partner institution's director.
--       Vice-rectors leave it null (their `name` carries the whole label).
--
-- FORMER RECTORS (template 'former-rectors') reuses:
--   title + description        → the page title and short description
--   about_persons              → one card per former rector:
--       name, surname, year_start/year_end, bio (the rich description)
--
-- PARTNER INSTITUTIONS (template 'partner-institution', five pages) reuse:
--   title + description        → the page title and short description
--   section_title + section_body → the "About X" heading and its rich text
--   document_label + document_url → the "visit website" button (label + URL)
--   image_url                  → the institution logo (optional)
--   about_persons (one row)    → the director: image_url (photo), name,
--       surname, degree (the scientific title)
--   about_pillars              → the research areas (title + rich description),
--       optional and unlimited
--   about_links                → the "More in this section" buttons
--
-- Run AFTER migrations_about_scientific_board.sql. Idempotent and additive.
-- =====================================================================


-- =====================================================================
-- STEP 1 — SCHEMA
-- =====================================================================
alter table about_persons  add column if not exists year_start varchar(20);
alter table about_persons  add column if not exists year_end   varchar(20);
alter table about_person_tr add column if not exists surname   varchar(500);


-- =====================================================================
-- STEP 2 — SEED: the pages (structure and known chrome only; the people,
-- research areas and copy are entered from the dashboard). Every page
-- stays unpublished until an editor publishes it.
-- =====================================================================
insert into about_pages (page_key, template, slug_az, slug_en, display_order, is_active, created_at)
values
  ('former-rectors', 'former-rectors',
   'haqqimizda/rehbetlik-ve-idareetme/sabiq-rektorlarimiz',
   'about/leadership-and-management/former-rectors', 7, false, current_timestamp),
  ('turkiye-azerbaijan-university', 'partner-institution',
   'haqqimizda/terefdas-universitet-ve-elaqeli-institutlar/turkiye-azerbaycan-universiteti',
   'about/partner-universities-and-related-institutes/turkiye-azerbaijan-university', 8, false, current_timestamp),
  ('institute-of-information-technologies', 'partner-institution',
   'haqqimizda/terefdas-universitet-ve-elaqeli-institutlar/informasiya-texnologiyalari-institutu',
   'about/partner-universities-and-related-institutes/institute-of-information-technologies', 9, false, current_timestamp),
  ('management-systems-institute', 'partner-institution',
   'haqqimizda/terefdas-universitet-ve-elaqeli-institutlar/idareetme-sistemleri-insitutu',
   'about/partner-universities-and-related-institutes/management-systems-institute', 10, false, current_timestamp),
  ('baku-technical-college', 'partner-institution',
   'haqqimizda/terefdas-universitet-ve-elaqeli-institutlar/baki-texniki-kolleci',
   'about/partner-universities-and-related-institutes/baku-technical-college', 11, false, current_timestamp),
  ('baku-state-college-of-communication-and-transport', 'partner-institution',
   'haqqimizda/terefdas-universitet-ve-elaqeli-institutlar/baki-dovlet-rabite-ve-neqliyyat-kolleci',
   'about/partner-universities-and-related-institutes/baku-state-college-of-communication-and-transport', 12, false, current_timestamp)
on conflict (page_key) do nothing;


-- Former rectors — az / en.
insert into about_page_tr (page_id, lang_code, title, links_title, created_at)
select p.id, 'az', 'Sabiq Rektorlarımız', 'Bölmədə daha çox', current_timestamp
from about_pages p where p.page_key = 'former-rectors'
on conflict (page_id, lang_code) do nothing;

insert into about_page_tr (page_id, lang_code, title, links_title, created_at)
select p.id, 'en', 'Former Rectors', 'More in this section', current_timestamp
from about_pages p where p.page_key = 'former-rectors'
on conflict (page_id, lang_code) do nothing;


-- Partner institutions — seeded from a small mapping so the five pages
-- share one insert per language.
insert into about_page_tr (page_id, lang_code, title, section_title, document_label, links_title, created_at)
select p.id, 'az', s.title_az, s.section_az, 'Vebsayta keç', 'Bölmədə daha çox', current_timestamp
from about_pages p
join (values
  ('turkiye-azerbaijan-university',                    'Türkiyə-Azərbaycan Universiteti',            'Universitet haqqında'),
  ('institute-of-information-technologies',            'İnformasiya Texnologiyaları İnstitutu',      'İnstitut haqqında'),
  ('management-systems-institute',                     'İdarəetmə Sistemləri İnstitutu',             'İnstitut haqqında'),
  ('baku-technical-college',                           'Bakı Texniki Kolleci',                       'Kollec haqqında'),
  ('baku-state-college-of-communication-and-transport','Bakı Dövlət Rabitə və Nəqliyyat Kolleci',    'Kollec haqqında')
) as s(page_key, title_az, section_az) on s.page_key = p.page_key
on conflict (page_id, lang_code) do nothing;

insert into about_page_tr (page_id, lang_code, title, section_title, document_label, links_title, created_at)
select p.id, 'en', s.title_en, s.section_en, 'Visit website', 'More in this section', current_timestamp
from about_pages p
join (values
  ('turkiye-azerbaijan-university',                    'Türkiye-Azerbaijan University',                     'About the University'),
  ('institute-of-information-technologies',            'Institute of Information Technologies',              'About the Institute'),
  ('management-systems-institute',                     'Management Systems Institute',                      'About the Institute'),
  ('baku-technical-college',                           'Baku Technical College',                            'About the College'),
  ('baku-state-college-of-communication-and-transport','Baku State College of Communication and Transport', 'About the College')
) as s(page_key, title_en, section_en) on s.page_key = p.page_key
on conflict (page_id, lang_code) do nothing;


-- =====================================================================
-- STEP 3 — VERIFY. Expect 6 new pages, all unpublished, 0 people to start.
-- =====================================================================
select p.page_key, p.template, p.display_order, p.is_active,
       (select count(*) from about_persons x where x.page_id = p.id) as persons
from about_pages p
where p.page_key in (
    'former-rectors', 'turkiye-azerbaijan-university',
    'institute-of-information-technologies', 'management-systems-institute',
    'baku-technical-college', 'baku-state-college-of-communication-and-transport'
)
order by p.display_order;

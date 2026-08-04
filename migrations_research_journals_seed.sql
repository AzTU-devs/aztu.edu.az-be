-- =====================================================================
-- SEED — Research journals: content + publish
--
-- Why the site shows "jurnal tapılmadı": the public API 404s a journal
-- that is either missing or still a draft, and the seeded journals had no
-- content and were unpublished. This migrates the content that used to be
-- hard-coded on the site into the CMS and publishes the two journals that
-- had that data (Machine Science, Energy Sustainability).
--
-- Self-contained and idempotent: it (re)creates the pages if the structural
-- migration was never run, fills the fields with ON CONFLICT DO UPDATE, and
-- sets is_active = true. Safe to run more than once.
--
-- The third journal (Elmi Əsərlər) had no site content, so it is left as an
-- unpublished draft — fill it in the dashboard and press "Dərc et".
--
-- Run AFTER migrations_research_journals.sql (or on its own — it also creates
-- the pages if they are missing).
-- =====================================================================


-- ── Make sure the three journal pages exist ─────────────────────────────
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


-- ── Machine Science — content + publish ─────────────────────────────────
insert into research_page_tr (page_id, lang_code, title, journal_name, journal_language, founder, button_label, description, links_title, created_at)
select id, 'az', 'Maşınşünaslıq', 'Maşınşünaslıq', 'Azərbaycan, Rus, İngilis',
       'Azərbaycan Texniki Universiteti', 'Jurnalın saytına keç',
       '<p>AzTU tərəfindən nəşr edilən elmi jurnal. Mühəndislik və texnologiya sahəsində orijinal tədqiqat işlərini dərc edir.</p>',
       'Bölmədə daha çox', current_timestamp
from research_pages where page_key = 'journal-machine-science'
on conflict (page_id, lang_code) do update set
    title = excluded.title, journal_name = excluded.journal_name,
    journal_language = excluded.journal_language, founder = excluded.founder,
    button_label = excluded.button_label, description = excluded.description;

insert into research_page_tr (page_id, lang_code, title, journal_name, journal_language, founder, button_label, description, links_title, created_at)
select id, 'en', 'Machine Science', 'Machine Science', 'Azerbaijani, Russian, English',
       'Azerbaijan Technical University', 'Visit the journal',
       '<p>A scientific journal published by AzTU. Publishes original research in engineering and technology.</p>',
       'More in this section', current_timestamp
from research_pages where page_key = 'journal-machine-science'
on conflict (page_id, lang_code) do update set
    title = excluded.title, journal_name = excluded.journal_name,
    journal_language = excluded.journal_language, founder = excluded.founder,
    button_label = excluded.button_label, description = excluded.description;

update research_pages set
    issn = '2227-6912', eissn = '2790-0479', publication_year = '1948', yearly_count = '2',
    button_url = 'https://aztu.edu.az/elmi-jurnallar/masin-elmi',
    is_active = true, updated_at = current_timestamp
where page_key = 'journal-machine-science';


-- ── Energy Sustainability — content + publish ───────────────────────────
insert into research_page_tr (page_id, lang_code, title, journal_name, journal_language, founder, button_label, description, links_title, created_at)
select id, 'az',
       'Enerji Davamlılığı, Risklər və Qərarların Qəbul Edilməsi',
       'Enerji Davamlılığı, Risklər və Qərarların Qəbul Edilməsi',
       'İngilis', 'Azərbaycan Texniki Universiteti', 'Jurnalın saytına keç',
       '<p>Enerji davamlılığı, risk idarəetməsi və qərar qəbul etmə proseslərinə dair beynəlxalq elmi jurnal.</p>',
       'Bölmədə daha çox', current_timestamp
from research_pages where page_key = 'journal-energy-sustainability'
on conflict (page_id, lang_code) do update set
    title = excluded.title, journal_name = excluded.journal_name,
    journal_language = excluded.journal_language, founder = excluded.founder,
    button_label = excluded.button_label, description = excluded.description;

insert into research_page_tr (page_id, lang_code, title, journal_name, journal_language, founder, button_label, description, links_title, created_at)
select id, 'en',
       'Energy Sustainability, Risks and Decision-Making',
       'Energy Sustainability, Risks and Decision-Making',
       'English', 'Azerbaijan Technical University', 'Visit the journal',
       '<p>An international scientific journal on energy sustainability, risk management and decision-making processes.</p>',
       'More in this section', current_timestamp
from research_pages where page_key = 'journal-energy-sustainability'
on conflict (page_id, lang_code) do update set
    title = excluded.title, journal_name = excluded.journal_name,
    journal_language = excluded.journal_language, founder = excluded.founder,
    button_label = excluded.button_label, description = excluded.description;

update research_pages set
    issn = '3023-5294', publication_year = '2023', yearly_count = '2',
    button_url = 'https://aztu.edu.az/elmi-jurnallar/enerji-davamliligi',
    is_active = true, updated_at = current_timestamp
where page_key = 'journal-energy-sustainability';


-- ── VERIFY. The two seeded journals should read is_active = true. ───────
select p.page_key, p.is_active, p.issn, p.publication_year,
       (select journal_name from research_page_tr t where t.page_id = p.id and t.lang_code = 'az') as name_az
from research_pages p
where p.template = 'journal'
order by p.display_order;

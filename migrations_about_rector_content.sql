-- =====================================================================
-- SEED — Rector page: offices list items + related links
--
-- The rector page skeleton was created with an empty 'offices' list and
-- no links, so those two sections fell back to the website's built-in
-- copy while everything else (portrait, message, bio, gallery) came from
-- the CMS. This fills them from the same source, making the page fully
-- backend-driven.
--
-- Non-destructive: each statement only writes where the CMS is still
-- empty, so it never overwrites anything entered from the dashboard.
-- Safe to re-run.
--
-- Run AFTER migrations_about_rector.sql.
-- =====================================================================


-- ── Offices (the 'Rektora tabe olan bölmələr' list) ──────────────────
-- Items live on the translation row as a JSONB array. Set only when the
-- current value is null or empty, so a dashboard edit is never clobbered.
update about_list_tr t
set items = '["Rektorun Katibliyi", "Tədris İşləri Direktorluğu", "Elm və İnnovasiya Direktorluğu", "Beynəlxalq Əlaqələr və Bolonya Prosesi Ofisi", "Strateji Planlaşdırma və İnkişaf Şöbəsi", "Keyfiyyətin Təminatı Şöbəsi", "Hüquqi Təminat və Uyğunluq Ofisi", "İnformasiya Texnologiyaları Şöbəsi", "Mətbuat və İctimaiyyətlə Əlaqələr Ofisi", "İnsan Resursları Şöbəsi", "Daxili Audit və Nəzarət Bölməsi", "Kapital Tikintisi və İnfrastruktur Şöbəsi"]'::jsonb, updated_at = current_timestamp
from about_lists l
join about_pages p on p.id = l.page_id
where t.list_id = l.id and t.lang_code = 'az'
  and p.page_key = 'rector' and l.list_key = 'offices'
  and (t.items is null or jsonb_array_length(t.items) = 0);

update about_list_tr t
set items = '["Office of the Rector", "Directorate of Academic Affairs", "Directorate of Science and Innovation", "International Relations and Bologna Process Office", "Strategic Planning and Development", "Quality Assurance Department", "Legal Affairs and Compliance Office", "Information Technology Department", "Press and Public Relations Office", "Human Resources Department", "Internal Audit Unit", "Infrastructure and Capital Construction"]'::jsonb, updated_at = current_timestamp
from about_lists l
join about_pages p on p.id = l.page_id
where t.list_id = l.id and t.lang_code = 'en'
  and p.page_key = 'rector' and l.list_key = 'offices'
  and (t.items is null or jsonb_array_length(t.items) = 0);


-- ── Related links ('Bölmədə daha çox') ───────────────────────────────
-- Inserted only when the page has no links yet, so a re-run or a
-- dashboard edit is never duplicated.
do $$
declare
    v_page_id integer;
    v_link_id integer;
begin
    select id into v_page_id from about_pages where page_key = 'rector';
    if v_page_id is null then return; end if;
    if exists (select 1 from about_links where page_id = v_page_id) then return; end if;

    insert into about_links (page_id, url, display_order)
    values (v_page_id, '/haqqimizda/terefdas-universitet-ve-elaqeli-institutlar', 1) returning id into v_link_id;
    insert into about_link_tr (link_id, lang_code, label) values
        (v_link_id, 'az', 'Tərəfdaş Universitetlər'),
        (v_link_id, 'en', 'Partner Universities');

    insert into about_links (page_id, url, display_order)
    values (v_page_id, '/haqqimizda/vizyon-ve-missiya/strateji-plan', 2) returning id into v_link_id;
    insert into about_link_tr (link_id, lang_code, label) values
        (v_link_id, 'az', 'Strateji Plan'),
        (v_link_id, 'en', 'Strategic Plan');
end $$;


-- =====================================================================
-- VERIFY. Expect the offices list with 12 items and 2 links.
-- =====================================================================
select
    (select jsonb_array_length(t.items)
     from about_list_tr t join about_lists l on l.id = t.list_id
     join about_pages p on p.id = l.page_id
     where p.page_key = 'rector' and l.list_key = 'offices' and t.lang_code = 'az') as office_items,
    (select count(*) from about_links x join about_pages p on p.id = x.page_id
     where p.page_key = 'rector') as links;

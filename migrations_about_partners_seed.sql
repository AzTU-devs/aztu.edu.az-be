-- =====================================================================
-- SEED — Partner institutions: content + publish (the 4 unpublished ones)
--
-- Migrates the About text and website that used to be hard-coded on the site
-- into the About CMS for the four institutes/colleges, and publishes them, so
-- their pages stop showing "hazırlanır". Türkiyə-Azərbaycan Universiteti is
-- deliberately NOT touched — it is already filled in and published.
--
-- Only description (subtitle) and section_body are updated on existing rows;
-- the title / section_title the structural migration set are preserved. Add
-- the logo, director and research areas from the dashboard. Idempotent.
--
-- Run AFTER migrations_about_former_rectors_partners.sql.
-- =====================================================================

insert into about_page_tr (page_id, lang_code, description, section_body, created_at)
select id, 'az', '<p>AzTU-nun İKT sahəsində tədqiqat və təhsil mərkəzi.</p>', '<p>AzTU təhsil, tədqiqat və innovasiyanın inteqrasiyasını gücləndirən strateji tərəfdaşlıqlar vasitəsilə müasir akademik ekosistem formalaşdırır.</p><p>AMEA-nın İnformasiya Texnologiyaları İnstitutu rəqəmsal transformasiya, süni intellekt və data elmi sahəsində ölkənin aparıcı elmi mərkəzidir.</p><p>AzTU ilə əməkdaşlıq çərçivəsində institut birgə elmi layihələr həyata keçirir və qabaqcıl biliklərin tədrisə inteqrasiyasını təmin edir.</p>', current_timestamp
from about_pages where page_key = 'institute-of-information-technologies'
on conflict (page_id, lang_code) do update set
    description = excluded.description, section_body = excluded.section_body;

insert into about_page_tr (page_id, lang_code, description, section_body, created_at)
select id, 'en', '<p>AzTU’s hub for ICT research and education.</p>', '<p>AzTU fosters a dynamic academic ecosystem through strategic partnerships.</p><p>The Institute of Information Technology (ANAS) is a leader in digital transformation, AI, and data science.</p><p>Through joint initiatives, we integrate cutting-edge tech into our curricula.</p>', current_timestamp
from about_pages where page_key = 'institute-of-information-technologies'
on conflict (page_id, lang_code) do update set
    description = excluded.description, section_body = excluded.section_body;

update about_pages set document_url = 'https://ict.az/', is_active = true, updated_at = current_timestamp
where page_key = 'institute-of-information-technologies';

insert into about_page_tr (page_id, lang_code, description, section_body, created_at)
select id, 'az', '<p>Avtomatlaşdırma və idarəetmə texnologiyaları üzrə lider tədqiqat müəssisəsi.</p>', '<p>İdarəetmə Sistemləri İnstitutu sistem mühəndisliyi və intellektual idarəetmə texnologiyaları sahəsində ixtisaslaşmış nüfuzlu elmi müəssisədir.</p><p>AzTU ilə tərəfdaşlıq çərçivəsində fənlərarası tədqiqatlar dəstəklənir və mühəndislik təhsilinin inkişafına töhfə verilir.</p>', current_timestamp
from about_pages where page_key = 'management-systems-institute'
on conflict (page_id, lang_code) do update set
    description = excluded.description, section_body = excluded.section_body;

insert into about_page_tr (page_id, lang_code, description, section_body, created_at)
select id, 'en', '<p>Leading research in automation and control technologies.</p>', '<p>The Institute of Control Systems specializes in systems engineering and automation.</p><p>Our partnership enhances interdisciplinary research and the development of intelligent management systems.</p>', current_timestamp
from about_pages where page_key = 'management-systems-institute'
on conflict (page_id, lang_code) do update set
    description = excluded.description, section_body = excluded.section_body;

update about_pages set document_url = 'https://isi.az/', is_active = true, updated_at = current_timestamp
where page_key = 'management-systems-institute';

insert into about_page_tr (page_id, lang_code, description, section_body, created_at)
select id, 'az', '<p>Əmək bazarının tələblərinə uyğun peşəkar kadrların hazırlanması.</p>', '<p>Bakı Texniki Kolleci 1996-cı ildə Bakı Politexnik və Maşınqayırma texnikumlarının birləşdirilməsi əsasında yaradılmışdır.</p><p>2015-ci ildən AzTU-nun nəzdində fəaliyyət göstərən kollec subbakalavr səviyyəsində müasir təhsil proqramları təqdim edir.</p>', current_timestamp
from about_pages where page_key = 'baku-technical-college'
on conflict (page_id, lang_code) do update set
    description = excluded.description, section_body = excluded.section_body;

insert into about_page_tr (page_id, lang_code, description, section_body, created_at)
select id, 'en', '<p>Preparing competitive professionals for the modern labor market.</p>', '<p>Founded in 1996 through a merger of historic technical schools, it has a long legacy in engineering training.</p><p>Since 2015, it has operated under AzTU, offering sub-bachelor level programs in various technical fields.</p>', current_timestamp
from about_pages where page_key = 'baku-technical-college'
on conflict (page_id, lang_code) do update set
    description = excluded.description, section_body = excluded.section_body;

update about_pages set document_url = 'https://bakitexnikikolleci.edu.az/', is_active = true, updated_at = current_timestamp
where page_key = 'baku-technical-college';

insert into about_page_tr (page_id, lang_code, description, section_body, created_at)
select id, 'az', '<p>Rabitə və nəqliyyat sahələrində orta ixtisas təhsilini təmin edən aparıcı müəssisə.</p>', '<p>Bakı Dövlət Rabitə və Nəqliyyat Kolleci AzTU-nun nəzdində fəaliyyət göstərən, rəqabətədavamlı mütəxəssislər hazırlayan təhsil ocağıdır.</p><p>Kollecin tarixi 1931-ci ilə söykənir. Bu gün müasir tədris mühiti ilə tələbələrin peşəkar kompetensiyalarını inkişaf etdirir.</p>', current_timestamp
from about_pages where page_key = 'baku-state-college-of-communication-and-transport'
on conflict (page_id, lang_code) do update set
    description = excluded.description, section_body = excluded.section_body;

insert into about_page_tr (page_id, lang_code, description, section_body, created_at)
select id, 'en', '<p>A leader in mid-level communication and transport education.</p>', '<p>AzTU''s specialized college for transport and communication, producing competitive experts since 1931.</p><p>We emphasize technical proficiency and analytical thinking through modern practice-oriented methods.</p>', current_timestamp
from about_pages where page_key = 'baku-state-college-of-communication-and-transport'
on conflict (page_id, lang_code) do update set
    description = excluded.description, section_body = excluded.section_body;

update about_pages set document_url = 'https://rabitakolleci.edu.az/', is_active = true, updated_at = current_timestamp
where page_key = 'baku-state-college-of-communication-and-transport';


select page_key, is_active, document_url,
       (select left(section_body, 40) from about_page_tr t where t.page_id = p.id and t.lang_code='az') as body_az
from about_pages p
where template = 'partner-institution' order by display_order;

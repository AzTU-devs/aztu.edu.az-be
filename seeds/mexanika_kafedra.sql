-- ============================================================
-- Mexanika kafedrası — Full DB Import
-- cafedra_code: 'mechanics'
-- faculty_code: 'MMF'
-- ============================================================

BEGIN;

-- ── 1. Cafedra base record ──────────────────────────────────
INSERT INTO cafedras (
    faculty_code,
    cafedra_code,
    bachelor_programs_count,
    master_programs_count,
    phd_programs_count,
    international_collaborations_count,
    laboratories_count,
    projects_patents_count,
    industrial_collaborations_count,
    sdgs,
    created_at
) VALUES (
    'MMF',
    'mechanics',
    1, 1, 2, 8, 3, 5, 3,
    '[4, 9]'::jsonb,
    NOW()
) ON CONFLICT (cafedra_code) DO NOTHING;


-- ── 2. Cafedra translations ─────────────────────────────────
INSERT INTO cafedras_tr (cafedra_code, lang_code, cafedra_name, about_text, created_at)
VALUES
(
    'mechanics',
    'az',
    'Mexanika kafedrası',
    '<p>Mexanika kafedrası 1920-ci ildə yaradılan Azərbaycan Politexnik İnstitutunun (AzPİ) tərkibində fəaliyyətə başlamış və 1950-ci ildə AzPİ ikinci dəfə bərpa olunduqdan sonra böyük inkişaf yolu keçmişdir.</p><p>2011-ci ilin aprel ayında AzTU-nun Elmi Şurasının qərarı ilə Nəzəri mexanika və Materiallar müqaviməti kafedraları birləşdirilərək Texniki mexanika kafedrası adlandırılıb, 2016-cı ilin may ayında isə Texniki mexanika və Hidravlika və Hidropnevmo qurğular kafedralarının əsasında Mexanika kafedrası yaradılıb.</p><p>Uzun illər ərzində kafedranın texniki bazası xeyli yaxşılaşdırılmış, yeni tədris və elmi-tədqiqat laboratoriyaları yaradılmışdır.</p><p>Mexanika müasir texnikanın, maşın və mexanizmlərin, müxtəlif inşaat, körpü və qurğuların elmi əsasıdır. Kafedrada yeni nəsil maşın və mexaniki qurğuların yaradılması, istismarı və onların etibarlığı üzrə kadr hazırlığı və həmçinin bu sahədə geniş elmi-tədqiqat işləri aparılır.</p>',
    NOW()
),
(
    'mechanics',
    'en',
    'Department of Mechanics',
    '<p>The Department of Mechanics began its activity within the Azerbaijan Polytechnic Institute (AzPI), established in 1920, and underwent significant development after the re-establishment of AzPI in 1950.</p><p>In April 2011, by the decision of the Scientific Council of AzTU, the Departments of Theoretical Mechanics and Strength of Materials were merged and renamed the Department of Technical Mechanics. Later, in May 2016, the Department of Mechanics was established on the basis of the Departments of Technical Mechanics and Hydraulics and Hydropneumatic Systems.</p><p>Over the years, the technical infrastructure of the department has been significantly improved, and new educational and research laboratories have been established.</p><p>Mechanics forms the scientific foundation of modern technology, machines and mechanisms, as well as various structures, bridges, and installations. The department provides training for specialists in the design, operation, and reliability of next-generation machines and mechanical systems, while also conducting extensive research in these fields.</p>',
    NOW()
) ON CONFLICT (cafedra_code, lang_code) DO UPDATE
SET cafedra_name = EXCLUDED.cafedra_name, about_text = EXCLUDED.about_text, updated_at = NOW();


-- ── 3. Directions of action ─────────────────────────────────
DELETE FROM cafedra_directions_of_action WHERE cafedra_code = 'mechanics';

WITH direction_ids AS (
    INSERT INTO cafedra_directions_of_action (cafedra_code, display_order, created_at)
    VALUES
    ('mechanics', 1, NOW()),
    ('mechanics', 2, NOW()),
    ('mechanics', 3, NOW()),
    ('mechanics', 4, NOW()),
    ('mechanics', 5, NOW()),
    ('mechanics', 6, NOW())
    RETURNING id
)
INSERT INTO cafedra_direction_of_action_tr (direction_of_action_id, lang_code, title, description, created_at)
SELECT id, 'az', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'Mexanika mühəndisliyi üzrə mütəxəssis hazırlığı',
        'Mexanika mühəndisliyi ixtisası üzrə müasir tələblərə cavab verən mütəxəssis hazırlığı'),
    (2, 'Transregional neft və qaz kəmərlərinin texniki etibarlığı',
        'Transregional neft və qaz kəmərlərinin texniki etibarlığı və ətraf mühitə təsirinin tədqiqi'),
    (3, 'Külək və dalğa enerji qurğularının elmi-praktiki əsaslarının işlənməsi',
        'Külək və dalğa enerji qurğularının elmi-praktiki əsaslarının işlənməsi'),
    (4, 'Müasir mütərəqqi materialların mexaniki xassələrinin tədqiqi',
        'Müasir mütərəqqi materialların mexaniki xassələrinin tədqiqi'),
    (5, 'Nanomexanika və onun tətbiqi üzrə elmi-tədqiqat işləri',
        'Nanomexanika və onun tətbiqi üzrə elmi-tədqiqat işləri'),
    (6, 'Çoxaşırımlı vant körpülərin dinamik tədqiqi',
        'Çoxaşırımlı vant körpülərin dinamik tədqiqi və müvafiq normativ sənədin işlənməsi')
) v(row_num, title, description) ON d.row_num = v.row_num
UNION ALL
SELECT id, 'en', title, description, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM direction_ids
) d JOIN (
    VALUES
    (1, 'Training of specialists in Mechanical Engineering',
        'Training of specialists in Mechanical Engineering in accordance with modern requirements'),
    (2, 'Technical reliability of transregional oil and gas pipelines',
        'Technical reliability and environmental aspects of transregional oil and gas pipelines'),
    (3, 'Development of scientific and practical foundations of wind and wave energy systems',
        'Development of scientific and practical foundations of wind and wave energy systems'),
    (4, 'Investigation of mechanical properties of advanced modern materials',
        'Investigation of mechanical properties of advanced modern materials'),
    (5, 'Research in nanomechanics and its applications',
        'Research in nanomechanics and its applications'),
    (6, 'Dynamic analysis of multi-span cable-stayed bridges',
        'Dynamic analysis of multi-span cable-stayed bridges and development of relevant regulatory documents')
) v(row_num, title, description) ON d.row_num = v.row_num;


-- ── 4. Director + translations + working hours + educations ──
WITH director_insert AS (
    INSERT INTO cafedra_directors (
        cafedra_code,
        first_name, last_name, father_name,
        email, phone, room_number,
        created_at
    ) VALUES (
        'mechanics',
        'Valeh', 'Baxşəli', 'İsmixan oğlu',
        'v.bakhshali@aztu.edu.az',
        '+994 50 518 39 12',
        '201-IV korpus',
        NOW()
    ) ON CONFLICT (cafedra_code) DO UPDATE
    SET first_name   = EXCLUDED.first_name,
        last_name    = EXCLUDED.last_name,
        father_name  = EXCLUDED.father_name,
        email        = EXCLUDED.email,
        phone        = EXCLUDED.phone,
        room_number  = EXCLUDED.room_number,
        updated_at   = NOW()
    RETURNING id
)
INSERT INTO cafedra_director_tr (director_id, lang_code, scientific_degree, scientific_title, bio, scientific_research_fields, created_at)
SELECT id, 'az',
    'Texnika elmləri doktoru',
    'Professor',
    '<p>Valeh İsmixan oğlu Baxşəli "Maşınların, cihazların və aparatların dinamikası, möhkəmliyi" ixtisası üzrə dissertasiya müdafiə edərək texnika elmləri namizədi – PhD (1987) və həmin ixtisas üzrə texnika elmləri doktoru (2007) elmi dərəcəsi almışdır.</p><p>O, "Problems of Mechanics" (Journal of IFToMM - International Federation for the Promotion of Mechanism and Machine Science) və American Journal of Mechanical and Industrial Engineering (ABŞ) beynəlxalq elmi jurnallarının redaksiya heyətinin üzvü, bir neçə xarici elmi jurnalların rəyçisi, beynəlxalq elmi konfransların təşkilat komitəsinin üzvü olmuşdur.</p><p>O, Avropa Birliyinin 7-ci Çərçivə Proqramı (BS-ERA.NET Pilot Joint Call 2010/2011) üzrə qalib gəlmiş Elmi Konsorsiumun (Almaniya, Türkiyə, Gürcüstan, Azərbaycan) rəhbəri olmuş, Avropa Birliyinin HORİZON2020 Tədqiqat və İnnovasiya Proqramının "Smart nəqliyyat" elmi istiqaməti üzrə milli koordinatoru təyin edilmişdir.</p><p>Azərbaycan Respublikasının Prezidenti İlham Əliyevin 30.12.2020-ci il tarixli sərəncamına əsasən Azərbaycan Texniki Universitetinin 70 illiyi münasibətilə "Əməkdar mühəndis" fəxri adı verilmişdir. O, ölkə daxilində və xaricdə 200-dən çox elmi məqalə və konfrans məruzələri, monoqrafiyalar, dərslik və dərs vəsaitləri çap etdirmişdir. Onun 3 monoqrafiyası xaricdə nüfuzlu nəşriyyatlarda (LAP Lambert Academic Publishing (Almaniya), Springer International Publishing) nəşr edilmişdir.</p>',
    '["Texniki və tətbiqi mexanika", "Maşın və mexanizmlər nəzəriyyəsi", "Maşın hissələri", "Tribotexnika", "Nanomexanika"]'::jsonb,
    NOW()
FROM director_insert
UNION ALL
SELECT id, 'en',
    'Doctor of Technical Sciences',
    'Professor',
    '<p>Valeh I. Bakhshali defended his dissertation in the specialty "Dynamics, Strength, and Reliability of Machines, Devices, and Apparatus" and was awarded the degree of Candidate of Technical Sciences – PhD in 1987, and later the degree of Doctor of Technical Sciences in the same specialty in 2007.</p><p>He is a member of the editorial boards of the international scientific journals Problems of Mechanics (Journal of IFToMM – International Federation for the Promotion of Mechanism and Machine Science) and American Journal of Mechanical and Industrial Engineering (USA). He also serves as a reviewer for several international scientific journals and has been a member of organizing committees of various international scientific conferences.</p><p>He served as the head of a Scientific Consortium (Germany, Türkiye, Georgia, Azerbaijan) that won a grant under the European Union''s 7th Framework Programme (BS-ERA.NET Pilot Joint Call 2010/2011). He was also appointed as the National Contact Point for the "Smart Transport" research area within the EU HORIZON 2020 Research and Innovation Programme.</p><p>By the decree of the President of the Republic of Azerbaijan, dated December 30, 2020, he was awarded the honorary title "Honored Engineer" on the occasion of the 70th anniversary of Azerbaijan Technical University. He has published more than 200 scientific articles, conference papers, monographs, textbooks, and teaching materials both domestically and internationally. Three of his monographs have been published abroad by reputable publishing houses such as LAP Lambert Academic Publishing (Germany) and Springer International Publishing.</p>',
    '["Technical and applied mechanics", "Theory of machines and mechanisms", "Machine elements", "Tribotechnics", "Nanomechanics"]'::jsonb,
    NOW()
FROM director_insert
ON CONFLICT (director_id, lang_code) DO UPDATE
SET scientific_degree         = EXCLUDED.scientific_degree,
    scientific_title          = EXCLUDED.scientific_title,
    bio                       = EXCLUDED.bio,
    scientific_research_fields = EXCLUDED.scientific_research_fields,
    updated_at                = NOW();

-- Working hours
WITH wh_insert AS (
    INSERT INTO cafedra_director_working_hours (director_id, time_range, created_at)
    SELECT id, '12:00–14:00', NOW()
    FROM cafedra_directors WHERE cafedra_code = 'mechanics'
    RETURNING id
)
INSERT INTO cafedra_director_working_hour_tr (working_hour_id, lang_code, day, created_at)
SELECT id, 'az', 'Həftə içi', NOW() FROM wh_insert
UNION ALL
SELECT id, 'en', 'Weekdays',   NOW() FROM wh_insert
ON CONFLICT (working_hour_id, lang_code) DO UPDATE SET day = EXCLUDED.day;

-- Director educations
INSERT INTO cafedra_director_educations (director_id, start_year, end_year, created_at)
SELECT id, '1975', '1980', NOW() FROM cafedra_directors WHERE cafedra_code = 'mechanics'
UNION ALL
SELECT id, '1983', '1987', NOW() FROM cafedra_directors WHERE cafedra_code = 'mechanics'
UNION ALL
SELECT id, '2003', '2007', NOW() FROM cafedra_directors WHERE cafedra_code = 'mechanics';

WITH edu_ids AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS row_num
    FROM cafedra_director_educations
    WHERE director_id = (SELECT id FROM cafedra_directors WHERE cafedra_code = 'mechanics')
    ORDER BY id DESC
    LIMIT 3
)
INSERT INTO cafedra_director_education_tr (education_id, lang_code, degree, university, created_at)
SELECT id, 'az', degree, university, NOW() FROM (
    SELECT id, row_num FROM edu_ids
) e JOIN (
    VALUES
    (1, 'Mühəndis-mexanik',                 'Azərbaycan Texniki Universiteti, Mexanika fakültəsi'),
    (2, 'Elmlər namizədi (PhD)',            'Azərbaycan Texniki Universiteti, Nəzəri Mexanika kafedrası'),
    (3, 'Elmlər doktoru (DSc)',             'Azərbaycan Texniki Universiteti, Texniki Mexanika kafedrası')
) v(row_num, degree, university) ON e.row_num = v.row_num
UNION ALL
SELECT id, 'en', degree, university, NOW() FROM (
    SELECT id, row_num FROM edu_ids
) e JOIN (
    VALUES
    (1, 'Mechanical Engineer (M.Sc.)',       'Azerbaijan Technical University, Faculty of Mechanics'),
    (2, 'Candidate of Sciences (PhD)',       'Azerbaijan Technical University, Department of Theoretical Mechanics'),
    (3, 'Doctor of Sciences (DSc)',          'Azerbaijan Technical University, Department of Engineering Mechanics')
) v(row_num, degree, university) ON e.row_num = v.row_num;


-- ── 5. Workers ──────────────────────────────────────────────
DELETE FROM cafedra_workers WHERE cafedra_code = 'mechanics';

WITH worker_inserts AS (
    INSERT INTO cafedra_workers (cafedra_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES
    -- Professors (professorlar)
    ('mechanics', 'Elşən',     'Həşimov',       'Qiyas oğlu',          'elshan.hashimov@aztu.edu.az',     '+994 50-350-02-88',  NOW()),  -- 1
    ('mechanics', 'Fazil',      'Həsənov',       'Əbdüləzim oğlu',      'fazilha@aztu.edu.az',             '+994 70-334-81-60',  NOW()),  -- 2
    -- Associate Professors (dosentlər)
    ('mechanics', 'Elbəy',     'Aslanov',       'Aslan oğlu',           'e.aslanov@aztu.edu.az',           '+994 55-225-17-18',  NOW()),  -- 3
    ('mechanics', 'Abilqani',   'Əliyev',        'Məhəmməd oğlu',       'abilgani.aliyev@aztu.edu.az',     '+994 99-664-40-00',  NOW()),  -- 4
    ('mechanics', 'İsmayıl',   'İsmayıl',       'Allahverdi oğlu',      'ismayil_i@aztu.edu.az',           '+994 55-736-00-77',  NOW()),  -- 5
    ('mechanics', 'Eldar',      'Axundov',       'Fikrət oğlu',          'akhundov.eldar@aztu.edu.az',      '+994 50-330-70-23',  NOW()),  -- 6
    -- Assistants (assistentlər)
    ('mechanics', 'Ayaz',       'Novruzov',      'Novruz oğlu',          'ayazno@aztu.edu.az',              '+994 51-515-51-19',  NOW()),  -- 7
    ('mechanics', 'Fərhad',    'Quliyev',       'Vüqar oğlu',           'farhad.guliyev@aztu.edu.az',      '+994 77-590-93-13',  NOW()),  -- 8
    -- Lecturer (müəllim)
    ('mechanics', 'Könül',     'Hüseynzadə',    'Rüfət qızı',           'konul.huseynzade@aztu.edu.az',    '+994 55-797-95-13',  NOW()),  -- 9
    -- Clerk (kargüzar)
    ('mechanics', 'Rəna',      'Hacıağayeva',   'Mirzəməmməd',          'rena.hajiagayeva@aztu.edu.az',    '+994 99-306-02-13',  NOW())   -- 10
    RETURNING id
)
INSERT INTO cafedra_worker_tr (worker_id, lang_code, duty, scientific_name, scientific_degree, created_at)
SELECT id, 'az', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    -- Professors
    (1,  'Mexanika kafedrası, professor',                          'Professor',  'm.t.h.e.d.'),
    (2,  'Mexanika kafedrası, professor',                          'Professor',  'f.-r.e.n.'),
    -- Associate Professors
    (3,  'Mexanika kafedrası, dosent',                             'Dosent',     'f.-r.e.n.'),
    (4,  'Mexanika kafedrası, dosent',                             'Dosent',     't.e.n.'),
    (5,  'Mexanika kafedrası, dosent',                             'Dosent',     't.ü.f.d.'),
    (6,  'Mexanika kafedrası, dosent (xarici əvəzçiliklə)',        'Dosent',     't.e.n.'),
    -- Assistants
    (7,  'Mexanika kafedrası, assistent',                          NULL,         NULL),
    (8,  'Mexanika kafedrası, assistent',                          NULL,         NULL),
    -- Lecturer
    (9,  'Mexanika kafedrası, müəllim',                            NULL,         NULL),
    -- Clerk
    (10, 'Mexanika kafedrası, kargüzar',                           NULL,         NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num
UNION ALL
SELECT id, 'en', duty, scientific_name, scientific_degree, NOW() FROM (
    SELECT id, ROW_NUMBER() OVER () AS row_num FROM worker_inserts
) w JOIN (
    VALUES
    -- Professors
    (1,  'Department of Mechanics, Professor',                              'Professor',             'm.t.h.e.d.'),
    (2,  'Department of Mechanics, Professor',                              'Professor',             'f.-r.e.n.'),
    -- Associate Professors
    (3,  'Department of Mechanics, Associate Professor',                    'Associate Professor',   'f.-r.e.n.'),
    (4,  'Department of Mechanics, Associate Professor',                    'Associate Professor',   't.e.n.'),
    (5,  'Department of Mechanics, Associate Professor',                    'Associate Professor',   't.ü.f.d.'),
    (6,  'Department of Mechanics, Associate Professor (external part-time)', 'Associate Professor', 't.e.n.'),
    -- Assistants
    (7,  'Department of Mechanics, Assistant',                              NULL,                    NULL),
    (8,  'Department of Mechanics, Assistant',                              NULL,                    NULL),
    -- Lecturer
    (9,  'Department of Mechanics, Lecturer',                               NULL,                    NULL),
    -- Clerk
    (10, 'Department of Mechanics, Clerk',                                  NULL,                    NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num;

COMMIT;

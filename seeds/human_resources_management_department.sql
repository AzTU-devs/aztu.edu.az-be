-- ============================================================
-- İnsan resurslarının idarə edilməsi şöbəsi /
-- Department of Human Resources Management
-- department_code: 'human_resources_management'
-- ============================================================

BEGIN;

-- ── 1. Department base record ───────────────────────────────
INSERT INTO departments (department_code, created_at)
VALUES ('human_resources_management', NOW())
ON CONFLICT (department_code) DO NOTHING;


-- ── 2. Department translations ──────────────────────────────
INSERT INTO departments_tr (department_code, lang_code, department_name, about_html, created_at)
VALUES
(
    'human_resources_management',
    'az',
    'İnsan resurslarının idarə edilməsi şöbəsi',
    '<p>İnsan resurslarının idarə edilməsi şöbəsi Azərbaycan Texniki Universitetinin (AzTU) əsas inzibati struktur bölmələrindən biri olaraq, birbaşa universitetin rektoruna tabedir və fəaliyyətini Azərbaycan Respublikasının "Təhsil haqqında" Qanunu, "Əmək Məcəlləsi", digər normativ hüquqi aktlar və AzTU-nun nizamnaməsi əsasında həyata keçirir.</p><p>Şöbə AzTU-nun Elmi Şurasının 12 iyul 2024-cü il tarixli qərarı və "Universitetin yeni strukturunun təsdiq edilməsi haqqında" 30.09.2024-cü il tarixli F-159 nömrəli əmrinə əsasən yaradılmışdır və universitetin insan kapitalının strateji idarə olunmasında mühüm rol oynayır.</p><p>Şöbənin strukturuna "Kadr əməliyyatları" və "Qiymətləndirmə və təlim" istiqamətləri daxildir və bu istiqamətlər üzrə fəaliyyət universitetin institusional inkişafına yönəldilmiş vahid insan resursları siyasətinin həyata keçirilməsini təmin edir.</p>',
    NOW()
),
(
    'human_resources_management',
    'en',
    'Department of Human Resources Management',
    '<p>The Human Resource Management Division is one of the key administrative structural units of Azerbaijan Technical University (AZTU), directly reporting to the Rector and operating in accordance with the Law of the Republic of Azerbaijan "On Education", the Labor Code, other relevant normative legal acts, and the University''s Charter.</p><p>The Division was established based on the decision of the Academic Council dated July 12, 2024, and Order No. F-159 dated September 30, 2024, on the approval of the University''s new structure. It plays a vital role in the strategic management of the University''s human capital.</p><p>The Division includes the "Personnel Operations" and "Evaluation and Training" units, ensuring the implementation of a unified human resource policy aligned with the University''s institutional development goals.</p>',
    NOW()
)
ON CONFLICT (department_code, lang_code) DO UPDATE
SET department_name = EXCLUDED.department_name,
    about_html      = EXCLUDED.about_html,
    updated_at      = NOW();


-- ── 3. Objectives ───────────────────────────────────────────
DELETE FROM department_objectives WHERE department_code = 'human_resources_management';

WITH objective_ids AS (
    INSERT INTO department_objectives (department_code, display_order, created_at)
    VALUES
    ('human_resources_management', 1, NOW()),
    ('human_resources_management', 2, NOW()),
    ('human_resources_management', 3, NOW())
    RETURNING id
),
objective_numbered AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS row_num FROM objective_ids
)
INSERT INTO department_objective_tr (objective_id, lang_code, html_content, created_at)
SELECT id, 'az', html_content, NOW() FROM objective_numbered o JOIN (
    VALUES
    (1, '<p>Akademik və inzibati heyətin effektiv və strateji idarə olunmasını təmin etmək.</p>'),
    (2, '<p>İstedadların cəlb olunması, inkişafı və saxlanılması üzrə müasir yanaşmalar tətbiq etmək.</p>'),
    (3, '<p>Universitetin strateji prioritetlərinə uyğun insan kapitalının formalaşdırılmasına töhfə vermək.</p>')
) v(row_num, html_content) ON o.row_num = v.row_num
UNION ALL
SELECT id, 'en', html_content, NOW() FROM objective_numbered o JOIN (
    VALUES
    (1, '<p>To ensure effective and strategic management of academic and administrative staff.</p>'),
    (2, '<p>To implement modern approaches to talent attraction, development, and retention.</p>'),
    (3, '<p>To contribute to the development of human capital in line with the University''s strategic priorities.</p>')
) v(row_num, html_content) ON o.row_num = v.row_num;


-- ── 4. Core functions ───────────────────────────────────────
DELETE FROM department_core_functions WHERE department_code = 'human_resources_management';

WITH cf_ids AS (
    INSERT INTO department_core_functions (department_code, display_order, created_at)
    VALUES
    ('human_resources_management', 1, NOW()),
    ('human_resources_management', 2, NOW()),
    ('human_resources_management', 3, NOW()),
    ('human_resources_management', 4, NOW()),
    ('human_resources_management', 5, NOW()),
    ('human_resources_management', 6, NOW())
    RETURNING id
),
cf_numbered AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS row_num FROM cf_ids
)
INSERT INTO department_core_function_tr (core_function_id, lang_code, html_content, created_at)
SELECT id, 'az', html_content, NOW() FROM cf_numbered c JOIN (
    VALUES
    (1, '<p>İnsan resurslarına olan tələbatın strateji planlaşdırılması və təhlili.</p>'),
    (2, '<p>Şəffaf və rəqabətqabiliyyətli kadr seçimi və işə qəbul prosesinin təşkili.</p>'),
    (3, '<p>Əmək münasibətlərinin müasir idarəetmə prinsipləri əsasında tənzimlənməsi.</p>'),
    (4, '<p>İnsan resursları üzrə vahid rəqəmsal məlumat bazasının idarə olunması.</p>'),
    (5, '<p>Əmək intizamının və institusional standartların qorunmasına nəzarət.</p>'),
    (6, '<p>Analitik yanaşmaya əsaslanan dövri və illik hesabatların hazırlanması.</p>')
) v(row_num, html_content) ON c.row_num = v.row_num
UNION ALL
SELECT id, 'en', html_content, NOW() FROM cf_numbered c JOIN (
    VALUES
    (1, '<p>Strategic planning and analysis of human resource needs.</p>'),
    (2, '<p>Organization of transparent and competitive recruitment and selection processes.</p>'),
    (3, '<p>Regulation and management of employment relations based on modern HR principles.</p>'),
    (4, '<p>Management of a unified digital human resource database.</p>'),
    (5, '<p>Monitoring compliance with labor discipline and institutional standards.</p>'),
    (6, '<p>Preparation of periodic and annual reports based on analytical approaches.</p>')
) v(row_num, html_content) ON c.row_num = v.row_num;


-- ── 5. Director + translations + working hours + educations ──
-- Note: department_directors schema has no email/phone columns; contact
-- details for the head are preserved inside the bio HTML so no data is lost.
WITH director_insert AS (
    INSERT INTO department_directors (
        department_code,
        first_name, last_name, father_name,
        room_number,
        created_at
    ) VALUES (
        'human_resources_management',
        'Rəna', 'Hətəmova', 'Xosrov qızı',
        '2-ci korpus, 2-ci mərtəbə, otaq 212',
        NOW()
    ) ON CONFLICT (department_code) DO UPDATE
    SET first_name  = EXCLUDED.first_name,
        last_name   = EXCLUDED.last_name,
        father_name = EXCLUDED.father_name,
        room_number = EXCLUDED.room_number,
        updated_at  = NOW()
    RETURNING id
)
INSERT INTO department_director_tr (director_id, lang_code, scientific_degree, scientific_title, bio, created_at)
SELECT id, 'az',
    NULL,
    'Şöbə müdiri',
    '<p><strong>Əlaqə:</strong> rena.hatamova@aztu.edu.az · +994 12 538 67 17 · İP telefon – 1100 · 2-ci korpus, 2-ci mərtəbə, otaq 212 · Qəbul saatları: Bazar ertəsi – Cümə, 14:00–15:30</p><p>Hətəmova Rəna Xosrov qızı 1988-ci ildə riyaziyyat ixtisası üzrə ali təhsilini başa vurmuş və əmək fəaliyyətinə "Kosmik tədqiqatlar" Elmi-İstehsalat Birliyində (hazırda Milli Aerokosmik Agentlik) mühəndis kimi başlamışdır.</p><p>1993-cü ildən etibarən Azərbaycan Texniki Universitetində fəaliyyət göstərən Rəna Hətəmova kadrlar üzrə mütəxəssis kimi əmək fəaliyyətini davam etdirmiş, daha sonra insan resurslarının idarə edilməsi sahəsində müxtəlif rəhbər vəzifələrdə çalışmışdır.</p><p>O, insan resurslarının strateji idarə olunması sahəsində uzunillik peşəkar təcrübəyə malikdir və bu istiqamətdə universitetin institusional inkişafına mühüm töhfələr vermişdir.</p><p>2020-ci ildə Azərbaycan Respublikasının elm və təhsil naziri tərəfindən "Fəxri Fərman"la təltif edilmişdir.</p><p>Rəna Hətəmova eyni zamanda "Strateji insan resurslarının idarə edilməsi" üzrə beynəlxalq sertifikata malikdir.</p>',
    NOW()
FROM director_insert
UNION ALL
SELECT id, 'en',
    NULL,
    'Head of Department',
    '<p><strong>Contact:</strong> rena.hatamova@aztu.edu.az · +994 12 538 67 17 · IP phone – 1100 · Room 212, 2nd building, 2nd floor · Reception hours: Monday – Friday, 14:00–15:30</p><p>Rena Hatamova Khosrov graduated in Mathematics in 1988 and began her professional career as an engineer at the "Space Research" Scientific-Production Association (currently the National Aerospace Agency).</p><p>Since 1993, she has been working at Azerbaijan Technical University, where she initially served as a personnel specialist and later held various managerial positions in the field of human resource management.</p><p>She has extensive professional experience in strategic human resource management and has made a significant contribution to the institutional development of the University.</p><p>In 2020, she was awarded the "Honorary Diploma" by the Minister of Science and Education of the Republic of Azerbaijan.</p><p>Rena Hatamova Khosrov also holds an international certification in Strategic Human Resource Management.</p>',
    NOW()
FROM director_insert
ON CONFLICT (director_id, lang_code) DO UPDATE
SET scientific_degree = EXCLUDED.scientific_degree,
    scientific_title  = EXCLUDED.scientific_title,
    bio               = EXCLUDED.bio,
    updated_at        = NOW();

-- Working hours
WITH wh_insert AS (
    INSERT INTO department_director_working_hours (director_id, time_range, created_at)
    SELECT id, '14:00–15:30', NOW()
    FROM department_directors WHERE department_code = 'human_resources_management'
    RETURNING id
)
INSERT INTO department_director_working_hour_tr (working_hour_id, lang_code, day, created_at)
SELECT id, 'az', 'Bazar ertəsi – Cümə', NOW() FROM wh_insert
UNION ALL
SELECT id, 'en', 'Monday – Friday',    NOW() FROM wh_insert
ON CONFLICT (working_hour_id, lang_code) DO UPDATE SET day = EXCLUDED.day;

-- Director educations
INSERT INTO department_director_educations (director_id, start_year, end_year, created_at)
SELECT id, '1983', '1988', NOW() FROM department_directors WHERE department_code = 'human_resources_management';

WITH edu_ids AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS row_num
    FROM (
        SELECT id FROM department_director_educations
        WHERE director_id = (SELECT id FROM department_directors WHERE department_code = 'human_resources_management')
        ORDER BY id ASC
        LIMIT 1
    ) sub
)
INSERT INTO department_director_education_tr (education_id, lang_code, degree, university, created_at)
SELECT id, 'az', degree, university, NOW() FROM edu_ids e JOIN (
    VALUES
    (1, 'Ali təhsil (Riyaziyyat)', 'Bakı Dövlət Universiteti')
) v(row_num, degree, university) ON e.row_num = v.row_num
UNION ALL
SELECT id, 'en', degree, university, NOW() FROM edu_ids e JOIN (
    VALUES
    (1, 'Higher Education (Mathematics)', 'Baku State University')
) v(row_num, degree, university) ON e.row_num = v.row_num;


-- ── 6. Workers ──────────────────────────────────────────────
DELETE FROM department_workers WHERE department_code = 'human_resources_management';

WITH worker_inserts AS (
    INSERT INTO department_workers (department_code, first_name, last_name, father_name, email, phone, created_at)
    VALUES
    ('human_resources_management', 'Samirə',  'Kərimova',   'Qəmbər qızı', 'samira.karimova@aztu.edu.az', 'İP telefon – 1104', NOW()),  -- 1
    ('human_resources_management', 'İradə',   'İbrahimova', 'Rəşid qızı',  'irada.ibrahimova@aztu.edu.az', 'İP telefon – 1103', NOW()),  -- 2
    ('human_resources_management', 'Natiqə',  'Babayeva',   'Xosrov qızı', 'natiqa.babayeva@aztu.edu.az',  'İP telefon – 1106', NOW()),  -- 3
    ('human_resources_management', 'Lalə',    'Cəfərova',   'Cəmil qızı',  'ceferova.lale@aztu.edu.az',    'İP telefon – 1107', NOW())   -- 4
    RETURNING id
),
worker_numbered AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS row_num FROM worker_inserts
)
INSERT INTO department_worker_tr (worker_id, lang_code, duty, scientific_name, scientific_degree, created_at)
SELECT id, 'az', duty, scientific_name, scientific_degree, NOW() FROM worker_numbered w JOIN (
    VALUES
    (1, 'Akademik heyətin idarəedilməsi üzrə böyük mütəxəssis',         NULL::varchar, NULL::varchar),
    (2, 'İnzibati heyətin idarəedilməsi üzrə böyük mütəxəssis',         NULL,          NULL),
    (3, 'Sənədləşdirmə mütəxəssisi',                                     NULL,          NULL),
    (4, 'İnsan resursları informasiya sistemi üzrə böyük mütəxəssis',    NULL,          NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num
UNION ALL
SELECT id, 'en', duty, scientific_name, scientific_degree, NOW() FROM worker_numbered w JOIN (
    VALUES
    (1, 'Senior Specialist in Academic Staff Management',            NULL::varchar, NULL::varchar),
    (2, 'Senior Specialist in Administrative Staff Management',      NULL,          NULL),
    (3, 'Documentation Specialist',                                   NULL,          NULL),
    (4, 'Senior Specialist in Human Resources Information Systems',   NULL,          NULL)
) v(row_num, duty, scientific_name, scientific_degree) ON w.row_num = v.row_num;

COMMIT;
